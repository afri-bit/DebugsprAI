from jsonfetcher.logger import setup_logger

logger = setup_logger(__name__)


class PostData:
    """
    A class to process and hold post information.
    """

    def __init__(self, data):
        try:
            self.post_id = data["postId"]
            self.title = data["title"]
            self.body = data["content"] if "content" in data else "N/A"
        except KeyError as e:
            logger.error(f"Error extracting data: {e}")

    def display(self):
        logger.info(f"Post ID: {self.post_id}")
        logger.info(f"Title: {self.title}")
        logger.info(f"Body: {self.body}")
