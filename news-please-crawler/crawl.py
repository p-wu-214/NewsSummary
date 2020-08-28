from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from newsplease import NewsPlease

import datetime

import psycopg2

path = 'top-news/today-top-news.txt'

connection = psycopg2.connect(user="patterson",
                              password="jeramywu",
                              host="localhost",
                              port="5432",
                              database="patterson")
cursor = connection.cursor()

def get_links():
  news_url = "https://news.google.com/news/rss"
  Client = urlopen(news_url)
  xml_page = Client.read()
  Client.close()

  soup_page = soup(xml_page, "xml")
  news_list = soup_page.findAll("item")

  return news_list

def crawl_for_content(news_list):
  x = datetime.datetime.now()
  for news in news_list:
    article = NewsPlease.from_url(news.link.text).get_serializable_dict()
    write_to_db(article['date_publish'], article['title'], article['url'], article['language'], article['maintext'])

def write_to_db(date_published, title, url, language, content):
  try:

    sql = """INSERT INTO articles (date_published, title, url, language, content)
                 VALUES (%s,%s,%s,%s,%s) RETURNING article_id, date_saved;"""

    title_len = len(title) if len(title) < 80 else 79
    record_to_insert = (date_published, title[:title_len], url, language, content)
    cursor.execute(sql, record_to_insert)

    article_id, date_saved = cursor.fetchone()

    connection.commit()

    return article_id, date_saved

  except (Exception, psycopg2.Error) as error:
    if (connection):
      print("Failed to insert record into articles table", error)

  finally:
    # closing database connection.
    if (connection):
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")

if __name__== "__main__" :
  news_list = get_links()
  crawl_for_content(news_list)