import psycopg2
from config import DB_NAME,DB_PASSWORD,DB_PORT,DB_USER,DB_HOST

def get_connection():
    """
    
    Establish connection to the PostgreSQL database. 

    Returns: 
        conn(connection): An object that represents a connection to the database. 
    Raises:
        Exception: If connection fails due to incorrect credentials or network errors. 

    """

    try: 
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def post_to_datbase(activity:str,productivity:str): 
    """

    Function adds user message to database

    """

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO entries(text,label) VALUES (%s,%s);",
        (activity,productivity))
        conn.commit()
        print("Entry added succesfully")
    except Exception as e:
        print(f"Database connection not succesful:{e}")
    finally: 
        if conn:
            cur.close()
            conn.close()