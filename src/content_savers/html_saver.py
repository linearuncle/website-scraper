from .base_saver import ContentSaver

class HTMLSaver(ContentSaver):
    """
    Saver for HTML format.
    """

    async def save(self, page, url, html, output_dir):
        """
        Save the content in HTML format.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The output directory for saved content.
        """
        # Implementation for saving content in HTML format
        pass
