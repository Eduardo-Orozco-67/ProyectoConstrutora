# db.py
import psycopg2

def get_connection():
    connection = psycopg2.connect(
        dbname="constructora",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )
    return connection

