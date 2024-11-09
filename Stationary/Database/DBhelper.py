from sqlalchemy import create_engine
import pandas as pd
import os
import json
# import mysql.connector
from mysql.connector import Error
from mysql.connector import (connection)
import warnings

warnings.filterwarnings(action='ignore') # , category=UserWarning, module='pandas'

DB_PASS = os.getenv('AWS_DB_PASS')
DIR = os.getenv('KEA_BASE_DIR')

with open(f'{DIR}/Database/df_config.json','r',encoding='utf-8') as f:
    df_config = json.load(f)

from sqlalchemy import create_engine, exc
import pandas as pd

DB_STRING = "mysql+pymysql://root:@localhost/kea"
HOST = 'kea.c0bv97lmyhtx.ap-south-1.rds.amazonaws.com'
USER = 'admin'
PASSWORD = 'GIRISH05'
DATABASE = 'kea'
is_connected = False
# conn = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD)

# def create_connection():
#     global is_connected
#     try:
#         # Check if connection is None or not alive
#         if not is_connected:
#             conn = connection.MySQLConnection(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
#             # connection = engine.connect()
#             is_connected = True
#             return conn
#         if not conn.ping(reconnect=False):
#             conn = connection.MySQLConnection(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
#             # connection = engine.connect()
#         return conn           
#     except Error as e:
#         print(f"An error occurred while creating the connection: {e}")
#         return None
conn = None  # Initialize the connection    
def create_connection():
    global is_connected
    global conn
    try:
        # Check if connection is None or not alive
        if not is_connected or (conn is not None and not conn.ping(reconnect=True, attempts=2, delay = 5)):
            conn = connection.MySQLConnection(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
            is_connected = True
        return conn           
    except Error as e:
        print(f"An error occurred while creating the connection: {e}")
        return None

def get_parliament_seats():
    connection = create_connection()
    query = ("SELECT name,constituency,party,const_num, 2018 AS year FROM kea.const18\n"
"UNION\n"
"SELECT name,constituency,party,const_num, 2013 AS year FROM kea.const13\n"
"UNION\n"
"SELECT name,constituency,party,const_num, 2023 AS year FROM kea.const23")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    
    try:
        df = pd.read_sql_query(query, connection) #, dtype=df_config
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None
    

def get_vote_margin_data():
    connection = create_connection()
    query = r"""SELECT name, temp.constituency, `winning party`, votes, margin, `runner up party`, year, const_num FROM ((WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid_ndtv23)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2023 AS 'year' FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
JOIN (SELECT constituency, party AS 'runner up party' FROM ranked_votes WHERE vote_rank = 2) t2
ON t1.constituency=t2.constituency)
UNION
(WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid_eci18)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2018 AS 'year' FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
JOIN (SELECT constituency, party AS 'runner up party' FROM ranked_votes WHERE vote_rank = 2) t2
ON t1.constituency=t2.constituency)
UNION
(WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid_opencity13)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2013 AS 'year' FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
JOIN (SELECT constituency, party AS 'runner up party' FROM ranked_votes WHERE vote_rank = 2) t2
ON t1.constituency=t2.constituency)) temp
JOIN (SELECT * FROM kea.const_num) temp2
ON temp.constituency = temp2.constituency"""
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    
    try:
        df = pd.read_sql_query(query, connection) #, dtype=df_config
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None
