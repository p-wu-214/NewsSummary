import argparse

import time

from config import hyper_params
from summarizer import Summarizer
from postgres import PostGres

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from news_crawler import NewsCrawler

crawler = NewsCrawler()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-m', '--mode', help='Two modes [crawl] or [summarize]', action='store',
                        dest='mode', required=True, type=str)
    args = parser.parse_args()
    if args.mode == 'crawl':
        get_google_news()
        return
    if args.mode == 'summarize':
        summarize()
        return
    else:
        parser.print_help()


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
    f = open('test.txt')
    summarized_dict = {}
    start_time = time.time()
    for model in hyper_params['pegasus_models']:
        summarizer = Summarizer(model)
        count = 0
        for article_id, content in crawler.get_articles_to_summarize():
            if count == 6:
                break
            if article_id not in summarized_dict:
                summarized_dict[article_id] = {}
            summarized_dict[article_id][model] = summarizer.generate_summary(content)
            count = count + 1
        del summarizer
    print(summarized_dict)
    db = PostGres()
    # print("--- %s seconds ---" % (time.time() - start_time))
    # f.write(str(summarized_articles))


if __name__ == "__main__":
    main()
