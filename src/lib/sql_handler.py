import os
import psycopg2
# from datetime import datetime

# Set up PostgreSQL
pg_host = os.environ.get('POSTGRES_HOST', 'postgres')
pg_port = os.environ.get('POSTGRES_PORT', '5432')
pg_user = os.environ.get('POSTGRES_USER', 'xhslink')
pg_password = os.environ.get('POSTGRES_PASSWORD', 'xhslink-password')
# pg_database = os.environ.get('POSTGRES_DB', 'postgres')

def create_table_if_not_exists():
    # use default database 'postgres'
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_password,
        host=pg_host,
        port=pg_port,
        database='postgres'
    )
    # Open a cursor to perform database operations
    cursor = conn.cursor()
    
    # create table
    cursor.execute("""CREATE TABLE IF NOT EXISTS shortlinks (
                   shortcode VARCHAR(255) PRIMARY KEY,
                   actual_link TEXT
                   )
    """)

    conn.commit()
    conn.close()
    print("db created")

def get_shortcode_from_database(shortcode):
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_password,
        host=pg_host,
        port=pg_port,
        database='postgres'
    )
    cursor = conn.cursor()

    cursor.execute('SELECT actual_link FROM shortlinks WHERE shortcode = %s', (shortcode,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

def add_shortcode_to_database(shortcode, actual_link):
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_password,
        host=pg_host,
        port=pg_port,
        database='postgres'
    )
    cursor = conn.cursor()

    # ts = datetime.timestamp(datetime.now())

    query = '''INSERT INTO shortlinks (shortcode, actual_link) VALUES (%s, %s)''' 
    # ON CONFLICT (shortcode) DO UPDATE SET actual_link = %s'''

    cursor.execute(query, (shortcode, actual_link))

    conn.commit()
    conn.close()
