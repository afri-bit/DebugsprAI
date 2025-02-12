import requests

from jsonfetcher.model import PostData

from jsonfetcher.logger import setup_logger

logger = setup_logger(__name__)

class JSONPlaceholderFetcher:
    """
    A class to fetch posts from JSONPlaceholder API.
    """

    BASE_URL = "https://jsonplaceholder.typicode.com/posts"

    @staticmethod
    def fetch_posts(max_batch=10):
        """
        Fetches a list of posts from JSONPlaceholder API.
        """
        response = requests.get(JSONPlaceholderFetcher.BASE_URL)

        if response.status_code == 200:
            data = response.json()
            return [
                PostData(data[i]) for i in range(min(max_batch, len(data)))
            ]
        else:
            logger.error("Failed to fetch data. Status code:", response.code) 
            return None
