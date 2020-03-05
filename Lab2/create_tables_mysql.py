import mysql.connector

db_conn = mysql.connector.connect(host="MSI", user="user", password="password", database="readings")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE inventory
          (id INT NOT NULL AUTO_INCREMENT, 
           item_id VARCHAR(250) NOT NULL,
           name VARCHAR(250) NOT NULL,
           manufacturer VARCHAR(250) NOT NULL,
           warehouse VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT inventory_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE status
          (id INT NOT NULL AUTO_INCREMENT, 
           item_id VARCHAR(250) NOT NULL,
           status VARCHAR(250) NOT NULL,
           destination VARCHAR(250) NOT NULL,
           deliverydate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT status_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()
