import psycopg2

def model_name_to_db_column(model_name):
    return model_name.replace('google/', '').replace('-', '_')

class PostGres:
    def __init__(self):
        self.connection = psycopg2.connect(user="patterson",
                                      password="jeramywu",
                                      host="localhost",
                                      port="5432",
                                      database="patterson")
        self.cursor = self.connection.cursor()

    def summaries_to_db(self, summaries_dict):
        article_ids = summaries_dict.keys()
        columns = [summaries_dict[article_ids].keys() for article_id in article_ids]
        values = [summaries_dict[article_ids]]
        sql = """
                INSERT INTO summaries (%s) VALUES (%s)
        """
        # sql = sql.format(column_name)
        # self.cursor.executemany(sql, list_of_summaries)

    def articles_to_db(self, articles):
        try:
            if articles is None:
                return
            sql = """INSERT INTO articles (date_published, title, url, language, content)
                   VALUES (%s,%s,%s,%s,%s) RETURNING article_id, date_saved;"""
            for idx, article in enumerate(articles):
                title_len = len(article['title']) if len(article['title']) < 80 else 79
                articles[idx] = article['title'][:title_len]
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

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")