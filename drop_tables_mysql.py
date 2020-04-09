import mysql.connector

db_conn = mysql.connector.connect(host="ec2-52-25-67-56.us-west-2.compute.amazonaws.com", user="user", password="password", database="readings")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          DROP TABLE inventory
          ''')

db_cursor.execute('''
          DROP TABLE status
          ''')

db_conn.commit()
db_conn.close()
