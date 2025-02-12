

class PostData:
    """
    A class to process and hold post information.
    """

    def __init__(self, data):
        try:
            self.post_id = data["postId"]
            self.title = data["title"]
            self.body = (data["content"] if "content" in data else "N/A")
        except KeyError as e:
            print(f"Error extracting data: {e}")

    def display(self):
        print(f"Post ID: {self.post_id}")
        print(f"Title: {self.title}")
        print(f"Body: {self.body}")
