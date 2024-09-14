import asyncio
import os
import re
import logging
from urllib.parse import urlparse, urljoin
import argparse

from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from content_savers import MarkdownSaver, PDFSaver, HTMLSaver

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebsiteScraper:
    """
    A class for scraping websites and saving content in various formats.
    """

    def __init__(self, start_url, output_dir="", formats=None, concurrency=10):
        """
        Initialize the WebsiteScraper.

        Args:
            start_url (str): The starting URL for scraping.
            output_dir (str, optional): The output directory for saved content.
            formats (list, optional): List of formats to save content in.
            concurrency (int, optional): Number of concurrent scraping tasks.
        """
        self.start_url = start_url
        self.website_name = self.get_website_name(start_url)
        if not output_dir:
            self.output_dir = os.path.join(SCRIPT_DIR, "download", self.website_name)
        else:
            self.output_dir = output_dir
        self.formats = formats or ['markdown']
        self.domain = self.get_domain(start_url)
        self.visited = set()
        self.to_visit = asyncio.Queue()
        self.savers = {
            'markdown': MarkdownSaver(),
            'pdf': PDFSaver(),
            'html': HTMLSaver()
        }
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)

    @staticmethod
    def get_domain(url):
        """
        Extract the domain from a URL.

        Args:
            url (str): The URL to extract the domain from.

        Returns:
            str: The domain of the URL.
        """
        parsed = urlparse(url)
        return parsed.netloc

    @staticmethod
    def get_website_name(url):
        """
        Extract the website name from a URL.

        Args:
            url (str): The URL to extract the website name from.

        Returns:
            str: The website name.
        """
        parsed = urlparse(url)
        domain_parts = parsed.netloc.split('.')
        return domain_parts[-2] if len(domain_parts) > 1 else parsed.netloc

    @staticmethod
    def generate_filename(title, url):
        """
        Generate a filename from the title or URL.

        Args:
            title (str): The title of the webpage.
            url (str): The URL of the webpage.

        Returns:
            str: The generated filename.
        """
        filename = title if title else url
        return re.sub(r'[\\/*?:"<>|]', "_", filename) + ".md"

    async def save_content(self, page, url, html):
        """
        Save the content in all specified formats.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
        """
        for format in self.formats:
            if format in self.savers:
                try:
                    await self.savers[format].save(page, url, html, self.output_dir)
                except Exception as e:
                    logging.error(f"Failed to save {format} file: {url}, Error: {e}")

    @staticmethod
    def is_internal_link(link, domain):
        """
        Check if a link is internal to the domain.

        Args:
            link (str): The link to check.
            domain (str): The domain to compare against.

        Returns:
            bool: True if the link is internal, False otherwise.
        """
        parsed = urlparse(link)
        return parsed.netloc == "" or parsed.netloc == domain

    async def crawl_impl(self, page, url):
        """
        Implementation of the crawling logic for a single page.

        Args:
            page: The Playwright page object.
            url (str): The URL to crawl.
        """
        if url in self.visited:
            return
        self.visited.add(url)
        logging.info(f"Crawling: {url}")
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state('networkidle')
            html = await page.content()
            await self.save_content(page, url, html)
            
            soup = BeautifulSoup(html, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                joined_href = urljoin(url, href)
                parsed_href = urlparse(joined_href)
                clean_href = parsed_href._replace(fragment='').geturl()
                if self.is_internal_link(clean_href, self.domain) and clean_href not in self.visited:
                    await self.to_visit.put(clean_href)
        except Exception as e:
            logging.error(f"Crawl failed: {url}, Error: {e}")

    async def crawl(self, page, url):
        """
        Crawl a single URL with semaphore control.

        Args:
            page: The Playwright page object.
            url (str): The URL to crawl.
        """
        async with self.semaphore:
            await self.crawl_impl(page, url)

    async def worker(self, page):
        """
        Worker function for concurrent crawling.

        Args:
            page: The Playwright page object.
        """
        while True:
            url = await self.to_visit.get()
            await self.crawl(page, url)
            self.to_visit.task_done()

    def setup_output_directory(self):
        """
        Set up the output directory structure.
        """
        # Ensure the download directory exists
        download_dir = os.path.dirname(self.output_dir)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logging.info(f"Created download root directory: {download_dir}")

        # Ensure the website-specific output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"Created website output directory: {self.output_dir}")
        
        logging.info(f"Domain: {self.domain}")
        logging.info(f"Website name: {self.website_name}")
        logging.info(f"Output directory: {self.output_dir}")

    async def run(self):
        """
        Run the website scraper.
        """
        self.setup_output_directory()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            # Create multiple workers
            workers = []
            for _ in range(self.concurrency):
                page = await context.new_page()
                worker = asyncio.create_task(self.worker(page))
                workers.append(worker)
            
            # Add the starting URL to the queue
            await self.to_visit.put(self.start_url)
            
            # Wait for all tasks to complete
            await self.to_visit.join()
            
            # Cancel all workers
            for worker in workers:
                worker.cancel()
            
            # Wait for all workers to finish
            await asyncio.gather(*workers, return_exceptions=True)
            
            await browser.close()
        
        logging.info("Crawling task completed")

async def main(start_url, formats, output_dir, concurrency):
    """
    Main function to run the website scraper.

    Args:
        start_url (str): The starting URL for scraping.
        formats (list): List of formats to save content in.
        output_dir (str): The output directory for saved content.
        concurrency (int): Number of concurrent scraping tasks.
    """
    scraper = WebsiteScraper(start_url, output_dir, formats, concurrency)
    await scraper.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper supporting Markdown, PDF, and HTML formats")
    parser.add_argument('start_url', help='Starting URL for scraping')
    parser.add_argument('--formats', nargs='+', choices=['markdown', 'pdf', 'html'], 
                        default=['markdown'], help='Choose file formats to save')
    parser.add_argument('--output', help='Specify output directory')
    parser.add_argument('--concurrency', type=int, default=10, help='Number of concurrent crawling tasks')
    args = parser.parse_args()

    asyncio.run(main(args.start_url, args.formats, args.output, args.concurrency))
