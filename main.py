import argparse

from summarizer import Summarizer

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from news_crawler import NewsCrawler

crawler = NewsCrawler()


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
    crawler.close_connection()

def summarize():
    summarized_articles = {}
    summarizer = Summarizer()
    for article_id, content in crawler.get_articles_to_summarize():
        # Try to optimize, maybe at model at a time
        summarized_articles[article_id] = summarizer.generate_summary(content)
    print(summarized_articles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-m', '--mode', help='Two modes [crawl] or [summarize]', action='store',
                        dest='mode', required=True, type=str)

    args = parser.parse_args()
    if args.mode == 'crawl':
        get_google_news()
    if args.mode == 'summarize':
        summarize()

