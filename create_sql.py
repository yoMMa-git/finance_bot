import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='RGZ',
    user='postgres',
    password='postgres',
    port=5432
)

curr = conn.cursor()

curr.execute("CREATE TABLE IF NOT EXISTS users ("
             " id INTEGER PRIMARY KEY,"
             " name VARCHAR(50) NOT NULL"
             ")")

curr.execute("CREATE TABLE IF NOT EXISTS operations ("
             " id SERIAL PRIMARY KEY,"
             " date DATE NOT NULL,"
             " sum INTEGER NOT NULL,"
             " chat_id VARCHAR(50) NOT NULL,"
             " type_operation VARCHAR(50) NOT NULL"
             ")")

conn.commit()
conn.close()
