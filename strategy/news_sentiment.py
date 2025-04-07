from util.singleton import singleton


@singleton
class NewsSentiment:
    def __init__(self):
        self.url = "https://news.google.com/rss/search?q=query+when:1d&hl=en&gl=US&ceid=US:en"
