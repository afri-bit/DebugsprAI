import unittest
from unittest.mock import patch
from jsonfetcher.model import PostData
from jsonfetcher.fetcher import JSONPlaceholderFetcher


class TestJSONPlaceholderFetcher(unittest.TestCase):
    """
    Unit tests for JSONPlaceholderFetcher class with mock
    """

    @patch("jsonfetcher.fetcher.requests.get")
    def test_fetch_posts(self, mock_get):
        mock_response = [
            {"postId": 1, "title": "Mock Post", "body": "N/A"}
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = JSONPlaceholderFetcher.fetch_posts()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], PostData)
        self.assertEqual(result[0].post_id, 1)
        self.assertEqual(result[0].title, "Mock Post")
        self.assertEqual(result[0].body, "N/A")

    def test_post_data_initialization(self):
        sample_data = {"postId": 1, "title": "Test Post", "body": "N/A"}
        post = PostData(sample_data)

        self.assertEqual(post.post_id, sample_data["postId"])  # Corrected key
        self.assertEqual(post.title, sample_data["title"])
        self.assertEqual(post.body, sample_data["body"])  # Corrected key


if __name__ == "__main__":
    unittest.main()
