from jsonfetcher.fetcher import JSONPlaceholderFetcher


if __name__ == "__main__":
    posts = JSONPlaceholderFetcher.fetch_posts()

    if posts:
        for post in posts:
            post.display()
