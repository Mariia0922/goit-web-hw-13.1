import pymongo
import psycopg2
from psycopg2.extras import execute_values

# Налаштування MongoDB
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['quotes_db']
quotes_collection = mongo_db['quotes']
authors_collection = mongo_db['authors']

# Налаштування PostgreSQL
pg_conn = psycopg2.connect(dbname='quotes_db', user='your_db_user', password='your_db_password', host='localhost')
pg_cursor = pg_conn.cursor()

# Міграція авторів
authors = list(authors_collection.find())
author_values = [(author['name'], author['birth_date'], author['birth_place'], author['description']) for author in authors]
execute_values(pg_cursor, "INSERT INTO quotes_app_author (name, birth_date, birth_place, description) VALUES %s", author_values)

# Міграція цитат
quotes = list(quotes_collection.find())
quote_values = [(quote['text'], quote['author'], quote['added_by']) for quote in quotes]
execute_values(pg_cursor, "INSERT INTO quotes_app_quote (text, author_id, added_by_id) VALUES %s", quote_values)

# Збереження змін
pg_conn.commit()

# Закриття з'єднань
pg_cursor.close()
pg_conn.close()
mongo_client.close()

