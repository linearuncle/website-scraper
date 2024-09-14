from abc import ABC, abstractmethod

class ContentSaver(ABC):
    """
    Abstract base class for content savers.
    """

    @abstractmethod
    def save(self, page, url, html, output_dir):
        """
        Save the content in the specified format.

        Args:
            page: The Playwright page object.
            url (str): The URL of the webpage.
            html (str): The HTML content of the webpage.
            output_dir (str): The output directory for saved content.
        """
        pass
