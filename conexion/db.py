# db.py
import psycopg2

def get_connection():
    connection = psycopg2.connect(
        dbname="constructora",
        user="constructora_user",
        password="3mxhSYupgYNxm1L4Cs6V1k9UYLJBFyXS",
        host="postgres://constructora_user:3mxhSYupgYNxm1L4Cs6V1k9UYLJBFyXS@dpg-claduqpm6hds73ehit2g-a/constructora",
        port="5432"
    )
    return connection

