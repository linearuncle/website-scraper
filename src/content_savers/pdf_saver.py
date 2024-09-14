from .base_saver import ContentSaver
import logging
import os

class PDFSaver(ContentSaver):
    """
    Content saver for PDF format.
    """

    async def save(self, page, url, html, output_dir):
        """
        Save the content as a PDF file.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The directory to save the content.
        """
        base_filename = self.get_base_filename(url)
        pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
        await page.pdf(path=pdf_path)
        logging.info(f"Saved PDF file: {pdf_path}")
