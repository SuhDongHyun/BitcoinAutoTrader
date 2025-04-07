from util.singleton import singleton
import feedparser


@singleton
class NewsSentiment:
    def __init__(self):
        self.url = "https://news.google.com/rss/search?q=query+when:1d&hl=en&gl=US&ceid=US:en"

    def get_news(self, query="economy", max_items=100):
        feed = feedparser.parse(self.url.replace('query', query))
        news_items = [entry['title'] for entry in feed['entries'][:max_items]]
        return news_items
