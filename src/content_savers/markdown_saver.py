from .base_saver import ContentSaver
import logging
import os
from markdownify import markdownify as md

class MarkdownSaver(ContentSaver):
    """
    Saver for Markdown format.
    """

    async def save(self, page, url, html, output_dir):
        """
        Save the content as a Markdown file.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The directory to save the content.
        """
        base_filename = self.get_base_filename(url)
        markdown_path = os.path.join(output_dir, f"{base_filename}.md")
        markdown_content = md(html, heading_style="ATX")
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(f"# {url}\n\n")
            f.write(markdown_content)
        logging.info(f"Saved Markdown file: {markdown_path}")
