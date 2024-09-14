from .base_saver import ContentSaver
import logging
import os

class HTMLSaver(ContentSaver):
    """
    Content saver for HTML format.
    """

    async def save(self, page, url, html, output_dir):
        """
        Save the content as an HTML file.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The directory to save the content.
        """
        base_filename = self.get_base_filename(url)
        html_path = os.path.join(output_dir, f"{base_filename}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        logging.info(f"Saved HTML file: {html_path}")