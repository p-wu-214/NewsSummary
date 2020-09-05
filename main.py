import argparse

import time

from config import hyper_params

import news_crawler
from summarizer import Summarizer
from postgres import PostGres

db = PostGres()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-m', '--mode', help='Two modes [crawl] or [summarize]', action='store',
                        dest='mode', required=True, type=str)
    args = parser.parse_args()
    if args.mode == 'crawl':
        crawl()
        return
    if args.mode == 'summarize':
        summarize()
        return
    else:
        parser.print_help()

def crawl():
    articles = news_crawler.get_google_news()
    db.articles_to_db(articles)

def summarize():
    f = open('test.txt')
    summarized_dict = {}
    start_time = time.time()
    for model in hyper_params['pegasus_models']:
        summarizer = Summarizer(model)
        count = 0
        for article_id, content in db.get_articles_to_summarize():
            if count == 6:
                break
            if article_id not in summarized_dict:
                summarized_dict[article_id] = {}
            summarized_dict[article_id][model] = summarizer.generate_summary(content)
            count = count + 1
        del summarizer
    print(summarized_dict)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # f.write(str(summarized_articles))


if __name__ == "__main__":
    main()
