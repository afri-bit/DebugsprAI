import requests

from jsonfetcher.model import PostData


class JSONPlaceholderFetcher:
    """
    A class to fetch posts from JSONPlaceholder API.
    """

    BASE_URL = "https://jsonplaceholder.typicode.com/posts"

    @staticmethod
    def fetch_posts():
        """
        Fetches a list of posts from JSONPlaceholder API.
        """
        response = requests.get(JSONPlaceholderFetcher.BASE_URL)

        if response.status_code == 200:
            data = response.json()
            return [
                PostData(item) for item in data
            ]  # Incorrect: Not handling empty responses properly
        else:
            print(
                "Failed to fetch data. Status code:", response.code
            )  # Incorrect attribute (should be status_code)
            return None
