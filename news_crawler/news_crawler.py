import urllib
from newsplease import NewsPlease

import datetime

import psycopg2


class NewsCrawler:

    def __init__(self):
        self.connection = psycopg2.connect(user="patterson",
                                           password="jeramywu",
                                           host="localhost",
                                           port="5432",
                                           database="patterson")
        self.cursor = self.connection.cursor()

    def google_news_to_db(self, news_list):
        x = datetime.datetime.now()
        for news in news_list:
            try:
                article = NewsPlease.from_url(news.link.text).get_serializable_dict()
                self.write_to_db(article['date_publish'], article['title'], article['url'], article['language'],
                                 article['maintext'])
            except urllib.error.HTTPError:
                continue

    def write_to_db(self, date_published, title, url, language, content):
        try:
            if content is None:
                return
            sql = """INSERT INTO articles (date_published, title, url, language, content)
                   VALUES (%s,%s,%s,%s,%s) RETURNING article_id, date_saved;"""

            title_len = len(title) if len(title) < 80 else 79
            record_to_insert = (date_published, title[:title_len], url, language, content)
            self.cursor.execute(sql, record_to_insert)

            article_id, date_saved = self.cursor.fetchone()

            self.connection.commit()

            return article_id, date_saved

        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print("Failed to insert record into articles table", error)




    def get_articles_to_summarize(self):
        query_filename = 'summarizer/get_articles_to_summarize.sql'
        try:
            query_file = open('{}'.format(query_filename))
            query_as_string = query_file.read()
            self.cursor.execute(query_as_string)

            articles = self.cursor.fetchall()
            return articles
        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print('Failed to execute query: {}'.format(query_filename), error)

    # def get_articles(self):
    #     try:
    #         self.cursor.execute("SELECT article_id, content from articles")
    #         results = self.cursor.fetchall()
    #         return results
    #
    #     except (Exception, psycopg2.Error) as error:
    #         if self.connection:
    #             print("Failed to select from articles table", error)
    #
    #     finally:
    #         # closing database connection.
    #         if self.connection:
    #             self.cursor.close()
    #             self.connection.close()
    #             print("PostgreSQL connection is closed")

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
