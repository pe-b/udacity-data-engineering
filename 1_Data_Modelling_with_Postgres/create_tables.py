import psycopg2
from sql_queries import create_table_queries, drop_table_queries, create_enum_queries, drop_enum_queries
    

def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)
        
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e)
        
    conn.set_session(autocommit=True)
    
    # create sparkify database with UTF8 encoding
    try:
        cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    except psycopg2.Error as e:
        print("Error: Could not drop sparkifydb")
        print(e)
        
    try:
        cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")
    except psycopg2.Error as e:
        print("Error: Could not create sparkifydb")
        print(e)

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    except psycopg2.Error as e:
        print("Could not make connection to the Postgres database for sparkifydb")
        print(e)
        
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the sparkifydb Database")
        print(e)
        
    conn.set_session(autocommit=True)

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print("Error: Could not execute query")
            print(e)
        
        try:
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Could not commit query")
            print(e)


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print("Error: Could not execute query")
            print(e)
        
        try:
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Could not commit query")
            print(e)

            
def create_enums(cur, conn):
    """
    Creates the enums required for creating the tables
    """
    for query in create_enum_queries:
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print("Error: Could not execute query")
            print(e)
        
        try:
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Could not commit query")
            print(e)


def drop_enums(cur, conn):
    """
    Drops the enums if they already exists
    """
    for query in drop_enum_queries:
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print("Error: Could not execute query")
            print(e)
        
        try:
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Could not commit query")
            print(e)
            
            
def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    drop_enums(cur, conn)
    create_enums(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()