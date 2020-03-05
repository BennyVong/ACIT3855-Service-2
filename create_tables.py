import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE inventory
          (id INTEGER PRIMARY KEY ASC, 
           item_id VARCHAR(250) NOT NULL,
           name VARCHAR(250) NOT NULL,
           manufacturer VARCHAR(250) NOT NULL,
           warehouse VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE status
          (id INTEGER PRIMARY KEY ASC, 
           item_id VARCHAR(250) NOT NULL,
           status VARCHAR(250) NOT NULL,
           destination VARCHAR(250) NOT NULL,
           deliverydate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
