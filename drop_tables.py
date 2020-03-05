import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE inventory
          ''')
c.execute('''
          DROP TABLE status
          ''')
conn.commit()
conn.close()