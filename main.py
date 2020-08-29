from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from crawler import Crawler
from summarizer import Summarizer

crawler = Crawler()
summarizer = Summarizer()

def get_links():
    news_url = "https://news.google.com/news/rss"
    client = urlopen(news_url)
    xml_page = client.read()
    client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")

    return news_list


def get_google_news():
    news_list = get_links()
    crawler.google_news_to_db(news_list)


if __name__ == "__main__":
    articles = crawler.get_articles()
    print(articles)
