from crawler import Crawler
from summarizer import Summarizer

crawler = Crawler()
summarizer = Summarizer()

if __name__ == "__main__":
    articles = crawler.get_articles()
    print(articles)
