import urllib
from newsplease import NewsPlease

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

def get_news_urls():
    news_url = "https://news.google.com/news/rss"
    client = urlopen(news_url)
    xml_page = client.read()
    client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    return news_list


def get_google_news():
    news_list = get_news_urls()
    articles = []
    for news in news_list:
        try:
            articles.append(NewsPlease.from_url(news.link.text).get_serializable_dict())
        except urllib.error.HTTPError:
            continue
    return articles
