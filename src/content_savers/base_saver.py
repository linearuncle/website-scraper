from abc import ABC, abstractmethod
from urllib.parse import urlparse

class ContentSaver(ABC):
    """
    Abstract base class for content savers.
    """

    @abstractmethod
    async def save(self, page, url, html, output_dir):
        """
        Save the content of a webpage.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The directory to save the content.
        """
        pass

    @staticmethod
    def get_base_filename(url):
        """
        Generate a base filename from the given URL.

        Args:
            url (str): The URL of the webpage.

        Returns:
            str: The base filename.
        """
        base_filename = urlparse(url).path.split('/')[-1]
        if not base_filename:
            import random
            random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            base_filename = f'index_{random_suffix}'
        return base_filename
