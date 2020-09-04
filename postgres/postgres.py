import psycopg2

def model_name_to_db_column(model_name):
    return model_name.replace('google/', '').replace('-', '_')

class PostGres:
    def __init__(self, model_name):
        self.connection = psycopg2.connect(user="patterson",
                                      password="jeramywu",
                                      host="localhost",
                                      port="5432",
                                      database="patterson")
        self.cursor = self.connection.cursor()

    def update_to_db(self, summaries_dict):
        article_ids = summaries_dict.keys()
        columns = [summaries_dict[article_ids].keys() for article_id in article_ids]
        values = [summaries_dict[article_ids]]
        sql = """
                INSERT INTO summaries (%s) VALUES (%s)
        """
        sql = sql.format(column_name)
        self.cursor.executemany(sql, list_of_summaries)