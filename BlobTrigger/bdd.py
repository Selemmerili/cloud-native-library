import mysql.connector
from mysql.connector import errorcode
from .listage_livre import listage_livre

# Obtain connection string information from the portal
config = {
  'host': 'groupeaskd.mysql.database.azure.com',
  'user': 'adminaskd@groupeaskd',
  'password': 'Simplongroupeaskd4',
  'database': 'table_askd',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': "BaltimoreCyberTrustRoot.crt.pem"
}


def connection():
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        return conn, cursor


def insert_bdd(title, myblob):
    conn, cursor = connection()
    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS table_askd;")
    print("Finished dropping table (if existed).")

    # Create table
    cursor.execute(
        """CREATE TABLE table_askd (
            ID serial PRIMARY KEY,
            Titre VARCHAR(255),
            Infos VARCHAR(255),
            Total INTEGER,
            URL_BLOB VARCHAR(255));""")
    print("Finished creating table.")

    # Insert some data into table
    Infos, Total = listage_livre(myblob)
    url = "https://stockageaskd.blob.core.windows.net/storageblobaskd/"
    cursor.execute("""INSERT INTO table_askd (
        Titre, Infos, Total, URL_BLOB)
        VALUES (%s, %s, %s, %s);""", (title, Infos, Total, url+title))
    print("Inserted", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")