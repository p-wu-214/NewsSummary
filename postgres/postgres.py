import psycopg2

def model_name_to_db_column(model_name):
    return model_name.replace('google/', '').replace('-', '_')

class PostGres:
    def __init__(self):
        self.connection = psycopg2.connect(user="patterson",
                                      password="jeramywu0214",
                                      host="localhost",
                                      port="5432",
                                      database="patterson")
        self.cursor = self.connection.cursor()

    # Redownloading the models is a pain, maybe a better solution is to keep the models on the ram and transfer back and forth from video card
    def summaries_to_db(self, summaries):
        try:
            records_to_insert = []
            for article_id, summary in summaries.items():
                records_to_insert.append((article_id, summary['google/pegasus-xsum'], summary['google/pegasus-newsroom'],
                                     summary['google/pegasus-multi_news'], summary['google/pegasus-cnn_dailymail'],
                                     summary['google/pegasus-large'], summary['google/pegasus-gigaword']))
            sql = """
                INSERT INTO summaries (article_id, pegasus_xsum, pegasus_newsroom, pegasus_multi_news, 
                pegasus_cnn_dailymail, pegasus_large, pegasus_gigaword) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            self.cursor.executemany(sql, records_to_insert)
            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print("Failed to insert record into articles table", error)

    def articles_to_db(self, articles):
        try:
            if articles is None:
                return
            sql = """INSERT INTO articles (date_published, title, url, language, content)
                   VALUES (%s,%s,%s,%s,%s);"""
            records_to_insert = []
            for article in articles:
                if article['title'] is None or article['date_publish'] is None or article['maintext'] is None:
                    continue
                title_len = len(article['title']) if len(article['title']) < 80 else 79
                records_to_insert.append((article['date_publish'], article['title'][:title_len], article['url'], article['language'], article['maintext']))
            self.cursor.executemany(sql, records_to_insert)

            self.connection.commit()

        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print("Failed to insert record into articles table", error)

    def get_articles_to_summarize(self):
        query_filename = '../summarizer/get_articles_to_summarize.sql'
        try:
            query_file = open('{}'.format(query_filename))
            query_as_string = query_file.read()
            self.cursor.execute(query_as_string)

            articles = self.cursor.fetchall()
            return articles
        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print('Failed to execute query: {}'.format(query_filename), error)

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")