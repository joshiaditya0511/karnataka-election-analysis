from sqlalchemy import create_engine
import pandas as pd
from mysql.connector import Error
from mysql.connector import (connection)
import warnings
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objs as go
import json
import os
import sys
import pickle

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object", ex)


# warnings.filterwarnings(action='ignore') # , category=UserWarning, module='pandas'

HOST = st.secrets['DB_HOST']
USER = st.secrets['DB_USER']
PASSWORD = st.secrets['DB_PASS']
DATABASE = 'kea'
is_connected = False
conn = None  # Initialize the connection  

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

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

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################
@st.cache_resource
def get_parliament_seats():
    connection = create_connection()
    query = (r"""SELECT name,constituency,party,const_num, 2018 AS year FROM kea.const18_post
UNION
SELECT name,constituency,party,const_num, 2013 AS year FROM kea.const13
UNION
SELECT name,constituency,party,const_num, 2023 AS year FROM kea.const23""")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    
    try:
        df = pd.read_sql_query(query, connection) #, dtype=df_config
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None
    
############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

BJY_const_list = ['Raichur','Raichur Rural','Bellary','Bellary City','Molakalmuru','Challakere','Hiriyur','Chiknayakanhalli',
                  'Tiptur','Turuvekere','Nagamangala','Melukote','Mandya','Shrirangapattana','Chamundeshwari','Krishnaraja',
                  'Chamaraja','Narasimharaja','Varuna','Nanjangud','Gundlupet']

@st.cache_resource
def get_BJY_parliament_seats():
    connection = create_connection()
    query = (f"""SELECT * FROM (SELECT name,constituency,party,const_num, 2018 AS year FROM kea.const18_post
UNION
SELECT name,constituency,party,const_num, 2013 AS year FROM kea.const13
UNION
SELECT name,constituency,party,const_num, 2023 AS year FROM kea.const23) temp
WHERE constituency IN {tuple(BJY_const_list)}""")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df = pd.read_sql_query(query, connection) #, dtype=df_config
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None    


############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################
@st.cache_resource
def get_vote_margin_data():
    connection = create_connection()
    query = r"""SELECT name, temp.constituency, `winning party`, votes, margin, `runner up party`, year, const_num, `margin percent` FROM (
(WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid_ndtv23)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2023 AS 'year', ROUND((margin/(votes-margin))*100,2) AS `margin percent` FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
JOIN (SELECT constituency, party AS 'runner up party' FROM ranked_votes WHERE vote_rank = 2) t2
ON t1.constituency=t2.constituency)
UNION
(WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid18_post)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2018 AS 'year', ROUND((margin/(votes-margin))*100,2) AS `margin percent` FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
JOIN (SELECT constituency, party AS 'runner up party' FROM ranked_votes WHERE vote_rank = 2) t2
ON t1.constituency=t2.constituency)
UNION
(WITH ranked_votes AS (SELECT name, constituency, party, votes, 
		DENSE_RANK() OVER(PARTITION BY constituency ORDER BY votes desc) AS vote_rank
FROM kea.candid_opencity13)
SELECT name, t1.constituency, `winning party`, votes, margin, `runner up party`, 2013 AS 'year', ROUND((margin/(votes-margin))*100,2) AS `margin percent` FROM (SELECT name, constituency, party as 'winning party', votes, margin FROM (SELECT *, votes - LEAD(votes) OVER(PARTITION BY constituency ORDER BY vote_rank ASC) AS margin FROM ranked_votes) temp WHERE temp.vote_rank = 1) t1
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
    
############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################    

@st.cache_resource
def get_total_voteshare_percent():
    connection = create_connection()
    query = r"""SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13 GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23 GROUP BY party) t2 ON t1.party = t2.party"""

    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df = pd.read_sql_query(query, connection) #, dtype=df_config
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None
    
############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################    

isNot = ''
exclusiveINC = ''
BJY_query = f"""SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party"""

isNot = 'NOT'
not_BJY_query = f"""SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC})
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`
HAVING party = 'INC') t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23
WHERE constituency {isNot} IN {tuple(BJY_const_list)} {exclusiveINC}
GROUP BY party) t2 ON t1.party = t2.party"""

main_query = r"""SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13 GROUP BY party) t2 ON t1.party = t2.party
WHERE t1.party = 'INC'
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post GROUP BY party) t2 ON t1.party = t2.party
WHERE t1.party = 'INC'
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC','JD(S)')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23 GROUP BY party) t2 ON t1.party = t2.party
WHERE t1.party = 'INC'"""

@st.cache_resource
def BJY_vote_percent():
    connection = create_connection()
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df_BJY = pd.read_sql_query(BJY_query, con=connection, dtype={'year':'str'})
        df_not_BJY = pd.read_sql_query(not_BJY_query, connection, dtype={'year':'category'})
        df = pd.read_sql_query(main_query, connection, dtype={'year':'category'})

        return df_BJY, df_not_BJY, df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

@st.cache_resource
def get_bipolarity_vote_share_percent():
    connection = create_connection()
    query = (f"""SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13 GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`)*100,2) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`
HAVING party IN ('BJP','INC')) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23 GROUP BY party) t2 ON t1.party = t2.party""")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None 

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

@st.cache_resource
def get_ENOP():
    connection = create_connection()
    query = (r"""(SELECT year, ROUND(SUM(`ENOP`),2) AS `ENOP`, 'With respect to vote share' AS `Type` FROM (SELECT *, 1/(1 + (POWER(MAX(`vote share percent`) OVER(PARTITION BY year ORDER BY `vote share percent` DESC),2)/`vote share percent`) - `vote share percent`) AS `ENOP` FROM 
(SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp13 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid13)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`),4) AS `vote share percent`, 2013 AS year FROM temp13
GROUP BY party, `total votes`) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const13 GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp18 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid18_post)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`),4) AS `vote share percent`, 2018 AS year FROM temp18
GROUP BY party, `total votes`) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const18_post GROUP BY party) t2 ON t1.party = t2.party
UNION
SELECT t1.party, party_total, `total votes`, `vote share percent`, `year`, `constituencies won` FROM (WITH temp23 AS (SELECT party,constituency,votes,
SUM(votes) OVER() AS `total votes` 
FROM kea.candid23)
SELECT party, SUM(votes) AS `party_total`,`total votes`, ROUND((SUM(votes)/`total votes`),4) AS `vote share percent`, 2023 AS year FROM temp23
GROUP BY party, `total votes`) t1
JOIN (SELECT party, COUNT(party) AS `constituencies won` FROM kea.const23 GROUP BY party) t2 ON t1.party = t2.party) temp) temp2
GROUP BY year)
UNION 
(SELECT year, ROUND(SUM(`ENOP`),2) AS `ENOP`, 'With respect to number of seats' AS `Type` FROM (SELECT *, 1/(1 + (POWER(MAX(`constituency percent`) OVER(PARTITION BY year ORDER BY `constituency percent` DESC),2)/`constituency percent`) - `constituency percent`) AS `ENOP`
FROM (SELECT *, `constituencies won`/224 AS `constituency percent`
FROM (SELECT party, COUNT(party) AS `constituencies won`, '2013' AS year FROM kea.const13 GROUP BY party
UNION
SELECT party, COUNT(party) AS `constituencies won`, '2018' AS year FROM kea.const18_post GROUP BY party
UNION
SELECT party, COUNT(party) AS `constituencies won`, '2023' AS year FROM kea.const23 GROUP BY party) temp) temp2) temp3
GROUP BY  year)""")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None     

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

@st.cache_resource
def get_contesting_party_count():
    connection = create_connection()
    query = (r"""SELECT '2013' AS year , COUNT(DISTINCT(party)) AS `Number of Parties` FROM kea.candid_opencity13
UNION
SELECT '2018' AS year , COUNT(DISTINCT(party)) AS `Number of Parties` FROM kea.candid_eci18
UNION
SELECT '2023' AS year , COUNT(DISTINCT(party)) AS `Number of Parties` FROM kea.candid_ndtv23""")
    
    if connection is None:
        print("Unable to establish a connection with the database.")
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None     

############################################################################################################################################    
############################################################################################################################################    
############################################################################################################################################
############################################################################################################################################
############################################################ NEW FILE ######################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

st.set_page_config(layout="wide", page_title="Karnataka Election Analysis", initial_sidebar_state="expanded")

with open("combined.json",'r',encoding='utf-8') as file:
        acmap = json.loads(file.read())

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

# Set up the Streamlit app
def main():
    options = ["Homepage","Karnataka's Electoral History","Impact of Bharat Jodo Yatra","Emerging Bi-polarity in Karnataka",'Seat distribution','parliament','Vote margins','What am I working on right now?']

    # Create a sidebar with index and sub-index
    st.sidebar.title('Navigation')
    selected_page = st.sidebar.radio('Go to', options)

    if selected_page == "Homepage":
        show_homepage()
    elif selected_page == "Karnataka's Electoral History":
        show_analysis()
    elif selected_page == "Impact of Bharat Jodo Yatra":
        show_BJY()
    elif selected_page == "Emerging Bi-polarity in Karnataka":
        show_emerging_bipolarity()
    elif selected_page == 'Seat distribution':
        trial()
    elif selected_page == 'parliament':
        parliament()
    elif selected_page == 'Vote margins':
        vote_margin_map()
    else:
        working_on_right_now()

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def show_homepage():
    left_gap, content, right_gap = st.columns([0.075,0.85,0.075])
    with content:
        st.markdown("""<h1 style="font-family: Georgia; font-size: 48px;">Karnataka Assembly Elections: Data Analysis</h1>

<p style="font-family: Georgia; text-align: justify;">
Welcome to my analysis of the Karnataka Assembly Elections. This project explores different aspects of the election using data.
</p>

<p style="font-family: Georgia; font-weight: bold; text-align: justify;">
🛈 Disclaimer: I am not affiliated with any political party. All the insights here are based on data. Some conclusions are made using common sense and basic understanding. I am a data analyst and not a political scientist.
</p>

## <span style="font-family: Georgia;">Contents</span>
* [<span style="font-family: Georgia; color: #007BFF;">Using the Site</span>](#using-the-site)
  * [<span style="font-family: Georgia; color: #007BFF;">Best Viewing Experience</span>](#best-viewing-experience)
  * [<span style="font-family: Georgia; color: #007BFF;">Interactive Charts</span>](#interactive-charts)
  * [<span style="font-family: Georgia; color: #007BFF;">Search in Select Boxes</span>](#search-in-select-boxes)
* [<span style="font-family: Georgia; color: #007BFF;">Data Notes and Discrepancies</span>](#data-notes-and-discrepancies)
* [<span style="font-family: Georgia; color: #007BFF;">Sources and References</span>](#sources-and-references)
* [<span style="font-family: Georgia; color: #007BFF;">Get in Touch</span>](#get-in-touch)
                    
<h3 style="font-family: Georgia;" id="using-the-site">Using the Site</h3>

<h4 style="font-family: Georgia; padding-left: 40px;" id="best-viewing-experience">Best Viewing Experience</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
For an optimal experience, I recommend viewing this site on a desktop or laptop browser. While the site is accessible on mobile phones, it's not fully optimized for such devices. If you're accessing the site on a mobile phone, ensure to select the "Desktop Site" option in your browser and use landscape mode for a better view.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;" id="interactive-charts">Interactive Charts</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
All charts, maps, and graphs on this site are interactive. Feel free to click on different elements within the visualizations; there's likely an interactive feature waiting for you. Additionally, I've provided helpful tips throughout the analysis pages to guide your exploration.
</p>
                    
<h4 style="font-family: Georgia; padding-left: 40px;" id="search-in-select-boxes">Search in Select Boxes</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
When using the dropdown menus (select boxes) on this site, you can quickly find options by typing. As you type, the list will narrow down to match your input, making it easy to locate and select specific items.
</p>
                    
<h3 style="font-family: Georgia;" id="data-notes-and-discrepancies">Data Notes and Discrepancies</h3>

<h4 style="font-family: Georgia; padding-left: 40px;">Votes Data</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
While the data from the 2013 and 2018 elections is valid, there may be some discrepancies to note. The 2013 data has not been adjusted for any bye-elections conducted between 2013 and 2018. On the other hand, the 2018 data includes the results from bye-elections held in 2019 for 15 constituencies. Any subsequent bye-elections after 2019 have not been accounted for.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">Census Data</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
The analysis uses the official census data from 2011. Given the significant changes in Karnataka since then, especially in the Bangalore district, Bangalore's data has been excluded. Any in-depth analysis requiring census data for Bangalore has been avoided due to these changes. For constituencies with available data, it has been duly utilized. In cases where data wasn't accessible, such as for parts of Bangalore, this has been explicitly mentioned in the analysis.
</p>

<h3 style="font-family: Georgia;" id="sources-and-references">Sources and References</h3>

<h4 style="font-family: Georgia; padding-left: 40px;">MyNeta</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
Data concerning assets, liabilities, criminal cases, profession, and education of candidates across three assembly elections was scraped from MyNeta. This data was freely available to the general public.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">NDTV</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
Vote count data for every candidate contesting in the 2023 elections was scraped from NDTV's live election results page. This data was also freely available to the public.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">OpenCity</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
Detailed results for the 2013 Assembly elections were freely available on OpenCity in the form of a CSV file.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">ECI (Election Commission of India)</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
The Election Commission of India published the detailed results of the 2018 elections in September 2018. This data was freely accessible to the public.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">CEO (Chief Election Officer) of Karnataka</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
Information about eligible voters and their gender-wise distribution was available in PDF format for all polling stations in Karnataka. Although these PDFs were free for the public, they were protected by a captcha. Only data regarding the number of eligible voters and their gender distribution was retrieved.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">KGIS (Karnataka Geographic Information System)</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
The shape file for Karnataka's assembly constituency boundaries was obatined from KGIS website owned by the Karnataka government. For visualization purposes, Bangalore district’s constituencies have been extracted and displayed separately due to their high number and smaller area. No harm or alteration to Karnataka's sovereign boundaries is intended.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">MapShaper</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
MapShaper was used to convert the Shape file to GeoJSON for better compatibility. The tool also smoothened the borders for quicker visualization rendering in this project. Again, no harm or alteration to Karnataka's sovereign boundaries is intended.
</p>

<h4 style="font-family: Georgia; padding-left: 40px;">OpenAI</h4>
<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
OpenAI's API was employed to segment and classify the education and profession details provided by the candidates. This segmentation was done using OpenAI’s proprietary GPT-3.5 model, and while efficient, it may not be entirely accurate.
</p>

<p style="font-family: Georgia; text-align: justify; padding-left: 40px;">
All extracted or scraped data is solely for educational and academic purposes. None of the content on this website is used commercially or monetized in any form (ads, referral links, etc.).
</p>
                    
<h3 style="font-family: Georgia;" id="get-in-touch">Get in Touch</h3>
<p style="font-family: Georgia; text-align: justify;">
If you have any questions, suggestions, or feedback, feel free to connect with me on:
</p>
<ul style="font-family: Georgia; padding-left: 40px;">
    <li>
        <a href="https://github.com/joshiaditya0511/karnataka-election-analysis" target="_blank"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" alt="GitHub Logo"/> GitHub</a>
    </li>
    <li>
        <a href="https://www.linkedin.com/in/joshiaditya0511" target="_blank"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="20" alt="LinkedIn Logo"/> LinkedIn</a>
    </li>
</ul>




""", unsafe_allow_html=True)

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def show_total_voteshare_percent():
    
    df = get_total_voteshare_percent()
    if not isinstance(df, pd.DataFrame):
        st.error("An error occurred when retrieving data.")
        return
    df = df.astype({'party':'object','party_total':'Int64','total votes':'Int64','year':'Int32'})

    # Define custom colors for parties
    color_discrete_map = {
        'INC': 'blue',
        'BJP': '#FF7500',
        'JD(S)': 'green'
    }

    # Create a bar chart with custom colors for parties
    fig = px.bar(df, x='year', y='vote share percent', color='party', 
                barmode='group', color_discrete_map=color_discrete_map, hover_data = ['party','vote share percent'],
                labels={'party':'Party', 'year':'Year','vote share percent':'Vote Share Percent'})
    fig2 = px.bar(df, x='year', y='constituencies won', color='party', 
                barmode='group', color_discrete_map=color_discrete_map, hover_data=['party','constituencies won'],
                labels={'party':'Party', 'year':'Year','constituencies won':'Constituencies Won'})
        

    # Customize the appearance of the chart
    fig.update_layout(
        title="Vote Share Percent by Party and Year",
        xaxis_title="Year",
        yaxis_title="Vote Share Percent",
        bargap=0.7,  # Gap between bars for different years
        bargroupgap=0.1,  # Gap between bars for different parties within the same year
        xaxis=dict(
            tickvals=df['year'].unique(),
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        yaxis=dict(
            tickvals = [0,5,10,15,20,25,30,35,40,45,50],
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        title_font=dict(family="Cambria", size=18, color="black"),
        legend_title_font=dict(family="Cambria", size=14, color="black"),
        legend_font=dict(family="Cambria", size=14, color="black"),
    )

    fig2.update_layout(
        title="Constituencies Won by Party and Year",
        xaxis_title="Year",
        yaxis_title="Constituencies Won",
        bargap=0.7,  # Gap between bars for different years
        bargroupgap=0.1,  # Gap between bars for different parties within the same year
        xaxis=dict(
            tickvals=df['year'].unique(),
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        yaxis=dict(
            tickvals = [0,20,40,60,80,100,120,140],
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        title_font=dict(family="Cambria", size=18, color="black"),
        legend_title_font=dict(family="Cambria", size=14, color="black"),
        legend_font=dict(family="Cambria", size=14, color="black"),
    )

    fig.update_traces(
    hovertemplate="<b>Party:</b> %{customdata[0]}<br><b>Vote Share Percent:</b> %{customdata[1]}"
    )
    fig2.update_traces(
    hovertemplate="<b>Party:</b> %{customdata[0]}<br><b>Constituencies Won:</b> %{customdata[1]}"
    )

    return fig, fig2

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def show_analysis():

    st.title(r"Karnataka's Electoral History")
    vote_share, const = show_total_voteshare_percent()
    if not (isinstance(vote_share, go._figure.Figure) and isinstance(const, go._figure.Figure)):
        st.error("An error occurred when retrieving data.")
        return
    img, gap, description = st.columns([0.5, 0.05, 0.45])
    with img:
        st.plotly_chart(vote_share, use_container_width=True)
        st.plotly_chart(const, use_container_width=True)
    with description:
        st.markdown("""<div style="font-family: Georgia; text-align: justify;">

### Yearly Analysis:

- **2013**: The INC secured a decisive victory, winning a majority of the constituencies, while the BJP and JD(S) both trailed significantly, securing an equal number of seats. 
- **2018**: The BJP led in the popular vote and won a considerable number of constituencies, surpassing the INC by a significant margin. This discrepancy between the popular vote and constituencies won suggests that the BJP might have secured marginal victories in certain constituencies or the INC underperformed in constituencies with a relatively lower population.
- **2023**: The INC rebounded, not only winning the popular vote but also securing a landslide in the number of constituencies won. Although the vote share difference between the INC and BJP was just 6.2 percentage points, the INC won more than double the constituencies. This pattern once again indicates potential narrow-margin victories for the INC or the BJP's underperformance in certain constituencies.

### Party-wise Analysis:

- **BJP**: 2013 was a subdued year for the BJP in both vote share and constituencies won. However, 2018 marked a significant turnaround with a drastic increase in both metrics. By 2023, while their vote share remained relatively stable, the number of constituencies they secured plummeted.
  
- **INC**: The INC maintained a consistent vote share from 2013 to 2018. However, while their vote share saw a modest increase in 2023, the number of constituencies they won surged, indicating their strong comeback.
  
- **JD(S)**: JD(S) has been witnessing a steady decline since 2013 in both vote share and constituencies won. Their alliance with the INC in 2018 did provide temporary stability, but the subsequent government collapse impacted their performance. This decline has paved the way for a more pronounced two-party dominance in Karnataka.

</div>
""",unsafe_allow_html=True)        

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def show_BJY():
    st.markdown("""<div style="font-family: Georgia; text-align: justify">
                
# Impact of Bharat Jodo Yatra
                
</div>""",unsafe_allow_html=True)
    st.markdown("##")
    hint = st.expander("""##### What's the Bharat Jodo Yatra?""", expanded=False)
    with hint:
        st.markdown("""<div style="font-family: Georgia; text-align: justify">
                
Bharat Jodo Yatra was a mass movement which was held by the political party Indian National Congress ("the Congress" or INC as short form). Senior Congress leader Rahul Gandhi was orchestrating the movement by encouraging the party cadre and the public to walk from Kanyakumari at the southern tip of India to the union territory of Jammu and Kashmir, a journey of 4,080 kilometres (2,540 miles) over almost 150 days.

According to INC, the movement was intended to unite the country against the "divisive politics" of the Bharatiya Janata Party (BJP)-led Government of India. The Bharat Jodo Yatra movement was launched by Rahul Gandhi and Tamil Nadu chief minister M. K. Stalin; on September 7, 2022.
                    
The Yatra covered 21 assembly constituencies in Karnataka. It spanned 511km in Karnataka over 22 days, moving from Gundlupet constituency to Raichur Rural constituency.
                
<div>""",unsafe_allow_html=True)
        st.markdown("""<div style="font-family: Georgia; text-align: right; color: darkgrey;">
                
Source: [Wikipedia](https://en.wikipedia.org/wiki/Bharat_Jodo_Yatra)
                
<div>""",unsafe_allow_html=True)
    st.markdown("##")
    
    df_BJY, df_not_BJY, df_total = BJY_vote_percent()
    if not (isinstance(df_BJY, pd.DataFrame) and isinstance(df_not_BJY, pd.DataFrame) and isinstance(df_total, pd.DataFrame)):
        st.error("An error occurred when retrieving data.")
        return
    df_BJY['yatra type'] = 'BJY Passed through'
    df_not_BJY['yatra type'] = "BJY didn't pass through"
    df_total['yatra type'] = 'Overall'

    df = pd.concat([df_BJY,df_not_BJY,df_total],axis=0)
    df.year = df.year.astype(str)

    fig = px.bar(df, 
                x='year', 
                y='vote share percent', 
                color='yatra type', 
                labels={'vote share percent': 'Vote Share Percent','yatra type':'Yatra Type'},
                title="Vote Share Percent by Year for INC",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                barmode='group',
                hover_data=['yatra type','vote share percent'],
                ) #category_orders={"year": ["2013", "2018", "2023"]}
    
    # Adjust the layout to set tickvals for x-axis and the gap between bars
    fig.update_layout(
        bargap=0.5,  # Adjust the gap between bars
        bargroupgap=0.2,
        xaxis_title="Year",
        yaxis_title="Vote Share Percent",
        xaxis=dict(
            tickvals=df['year'].unique(),
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        yaxis=dict(
            tickvals = [0,10,20,30,40,50],
            tickfont=dict(family="Cambria", size=14, color="black"),
            titlefont=dict(family="Cambria", size=16, color="black")
        ),
        title_font=dict(family="Cambria", size=18, color="black"),
        legend_title_font=dict(family="Cambria", size=14, color="black"),
        legend_font=dict(family="Cambria", size=14, color="black"),
        height=400,
    )

    fig.update_traces(
    hovertemplate="<b>Yatra Type:</b> %{customdata[0]}<br><b>Vote Share Percent:</b> %{customdata[2]}"
    )

    fig2 = px.bar(df, 
                x='vote share percent', 
                y='yatra type', 
                color='year', 
                labels={'vote share percent': 'Vote Share Percent','year':'Year'},
                title="Vote Share Percent with respect to whether Yatra passed through",
                color_discrete_map = {'2013':'#636EFA','2018':'#EF553B','2023':'#00CC96'},
                barmode='group',
                category_orders={"year": [2013,2018,2023]},  # Specify the order of bars within each group
                hover_data=['year','vote share percent'],
    )   
    
    fig2.update_layout(
            bargap=0.3,
            bargroupgap=0.2,
            xaxis_title="Vote Share Percent",
            yaxis_title="Yatra Type",
            height=400,
            xaxis=dict(
                tickvals=[0,10,20,30,40,50],
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            yaxis=dict(
                tickvals = df['yatra type'].unique(),
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
        )
    fig2.update_traces(
    hovertemplate="<b>Year:</b> %{customdata[1]}<br><b>Vote Share Percent:</b> %{customdata[2]}"
    )


    global acmap
    geojson = acmap

    ndf = get_parliament_seats()
    global BJY_const_list
    ndf_BJY = ndf.loc[ndf.constituency.isin(BJY_const_list)].copy()

    @st.cache_data
    def show_year(ndf,ndf_BJY):
        base_layer = px.choropleth_mapbox(
            ndf,
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color='party',
            color_discrete_map={
                'INC': '#0D5BE1',
                'BJP': '#FF7500',
                'IND': 'grey',
                'JD(S)': 'green',
                'KRPP' : 'brown',
                'SKP' : '#A51C30',
                'KJP':'lightgreen',
                'BSRC':'blue'
            },
            labels={'party': 'Winning Party'},
            hover_data=['name', 'constituency', 'party'],
            zoom=7,
            opacity=0.1,
        )
        BJY_layer = px.choropleth_mapbox(
            ndf_BJY,
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color='party',
            color_discrete_map={
                'INC': '#0D5BE1',
                'BJP': '#FF7500',
                'IND': 'grey',
                'JD(S)': 'green',
                'KRPP' : 'brown',
                'SKP' : '#A51C30',
                'KJP':'lightgreen',
                'BSRC':'blue'
            },
            labels={'party': 'Winning Party'},
            hover_data=['name', 'constituency', 'party'],
            zoom=7,
            opacity=1
        )

        fig = go.Figure()
        for trace in base_layer.data:
            fig.add_trace(trace)
        for trace in BJY_layer.data:
            fig.add_trace(trace)

        fig.update_traces(
            hovertemplate="<b>Winner:</b> %{customdata[0]}<br><b>Constituency:</b> %{customdata[1]}<br><b>Party:</b> %{customdata[2]}"
        )            

        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_zoom=6,
            mapbox_center={"lat": 15.3173, "lon": 76.7139},  # Center coordinates for Karnataka
            uirevision='lock',  # Disable user-driven changes in the view
            dragmode=False,  # Disable panning and zooming
            plot_bgcolor='rgba(0,0,0,0)',  # This sets the plot background to transparent.
            paper_bgcolor='rgba(0,0,0,0)', # rgba(14,17,23,1.000)
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
        )
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_geos(visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(width=600,height=700)
        return fig
    # fig2018 = load_object('2018bjy.pickle')
    # fig2023 = load_object('2018bjy.pickle')

    with open('Figures/BJY/Map2018.html','r',encoding='utf-8') as f:
        html2018 = f.read()
    with open('Figures/BJY/Map2023.html','r',encoding='utf-8') as f:
        html2023 = f.read()
    map1, map2 = st.columns(2)
    st.write('\n')
    with map1:
        st.markdown("""<div style="font-family: Georgia; text-align: center">
                
#### Bharat Jodo Yatra route - projected for 2018
                
<div>""",unsafe_allow_html=True)
        # st.plotly_chart(show_year(ndf[ndf.year==2018],ndf_BJY[ndf_BJY.year==2018]), use_container_width=True)
        components.html(html2018,width=610,height=725) 
    with map2:
        st.markdown("""<div style="font-family: Georgia; text-align: center">
                
#### Bharat Jodo Yatra route - 2023
                
<div>""",unsafe_allow_html=True)
        # st.plotly_chart(show_year(ndf[ndf.year==2023],ndf_BJY[ndf_BJY.year==2023]), use_container_width=True) 
        components.html(html2023,width=610,height=725)
    st.write('\n')
    img, gap, description = st.columns([0.5,0.05,0.45])
    with img:
        st.plotly_chart(fig , use_container_width=True) #
        st.plotly_chart(fig2,use_container_width=True) #  
    with description:
        st.markdown("""<div style="font-family: Georgia; text-align: justify">

## Bharat Jodo Yatra Analysis:

The Bharat Jodo Yatra (BJY), led by Rahul Gandhi and the Congress Party, covered 21 assembly constituencies in Karnataka. The Yatra spanned 511km in Karnataka over 22 days, moving from Gundlupet constituency to Raichur Rural constituency.

The map shows that the Yatra  went through constituencies that the INC didn't win much in 2018. Out of 21 constituencies, the INC won in only 5, while the BJP won in 12 and the JD(S) in 4. But in 2023, things changed. The INC won in 15 of these constituencies and joined forces with SKP in Melukote, making their total 16.

If we look at the charts, we see that constituencies visited by the BJY had almost the same vote share as other constituencies. This may imply that the Yatra wasn't all that beneficial for INC. But if we compare this to the last election, there's a big change. The vote share in constituencies visited by BJY went up a lot (by about 9.78%) from 2018 to 2023. In other constituencies, it went up too, but only by about 5.80%.

So, what does this mean? It looks like the Bharat Jodo Yatra made a difference. It seems to have helped the INC do better in the places it visited, especially since they didn't do well there in 2018.
                    
While the Yatra is seen as a factor in the improved performance, it's essential to note that correlation doesn't imply causation, and other factors might have contributed to the results.

</div>
""", unsafe_allow_html=True)



############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def show_emerging_bipolarity():
    st.title("Emerging Bi-polarity in the Karnataka")
    st.markdown("###")
    df = get_bipolarity_vote_share_percent()
    enop = get_ENOP()

    if not (isinstance(df, pd.DataFrame) and isinstance(enop, pd.DataFrame)):
        st.error("An error occurred when retrieving data.")
        return
    
    df.year = df.year.astype(str)
    enop.year = enop.year.astype(str)
    party_num = get_contesting_party_count()

    fig = px.bar(df, y='vote share percent', x='year',
                title='Vote Share of Top Two Parties',
                hover_data=['constituencies won'], color='party',
                labels={'vote share percent':'Vote Share Percent'},
                color_discrete_map={'INC': '#0062C6', 'BJP': '#FF7500',})

    fig.update_layout(
            xaxis=dict(
                tickvals=df['year'].unique(),  # Explicitly specify tick values for the y-axis
                tickfont=dict(family="Lora", size=14, color="black"),  # Set font, size, and color for y-axis tick labels
                titlefont=dict(family="Lora", size=16, color="black")  # Set font, size, and color for y-axis title
            ),
            yaxis=dict(
                range=[0, 100],
                tickfont=dict(family="Lora", size=14, color="black"),
                titlefont=dict(family="Lora", size=16, color="black")
            ),
            title_font=dict(family="Lora", size=18, color="black"),  # Set font, size, and color for the main title
            legend_title_font=dict(family="Lora", size=16, color="black"),  # Set font, size, and color for the legend title
            legend_font=dict(family="Lora", size=14, color="black"),  # Set font, size, and color for the legend items
            bargap=0.9
    )
    
    fig2 = px.bar(enop, y='ENOP', x='year',
                title='Effective Number of Parties Over the Years',
                labels={'ENOP':'Effective Number of Parties'},
                barmode='group',
                color='Type',
                color_discrete_sequence=px.colors.qualitative.Plotly,)
    fig2.update_layout(
            xaxis_title="Year",
            yaxis_title="Effective Number of Parties",
            xaxis=dict(
                tickvals=enop['year'].unique(),
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            yaxis=dict(
                range=[0, 4],
                tickvals = [0,0.5,1.0,1.5,2,2.5,3,3.5,4],
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
            bargap=0.65,
            bargroupgap=0.2,
    )

    fig3 = px.bar(party_num, y='Number of Parties', x='year',
                title='Number of Contesting Parties Over the Years',
                color_discrete_sequence=px.colors.qualitative.Plotly,)
    fig3.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Parties",
            xaxis=dict(
                tickvals=party_num['year'].unique(),
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            yaxis=dict(
                range=[0, 100],
                tickvals = [0,10,20,30,40,50,60,70,80,90,100],
                tickfont=dict(family="Cambria", size=14, color="black"),
                titlefont=dict(family="Cambria", size=16, color="black")
            ),
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
            bargap=0.85
    )

    img1, gap, description1 = st.columns([0.45,0.05,0.5])
    
    with img1:
        st.plotly_chart(fig, use_container_width=True)
    with description1:
        st.markdown("""<div style="font-family: Georgia; text-align: justify;">

### The Power Shift: National vs. Regional Parties

Over the past three assembly elections, there's been a noticeable shift in the political landscape. The data reveals a continuous rise in the combined vote share of the two leading national parties, BJP and INC. As depicted in the graph, their collective vote share has consistently increased over the years.

But what does this mean for regional parties and their candidates? 

As the national parties grow stronger, regional parties are facing a decline in their vote share. This trend might raise questions for voters who support local parties. If the trajectory continues, will their preferred regional party have the influence and representation they once had?

Moreover, candidates from these regional parties might find themselves at a crossroads. A dwindling vote share could mean reduced chances of electoral success, prompting them to reconsider their affiliations. 

In essence, the rising dominance of national parties could reshape the political fabric, nudging voters and candidates to reevaluate their loyalties. As we move forward, it will be intriguing to see how this dynamic evolves and impacts the broader political spectrum.

</div>
""",unsafe_allow_html=True)
    st.markdown("#")
    description2, gap, img2 = st.columns([0.45,0.05,0.5])
    with description2:
        st.markdown("""<div style="font-family: Georgia; text-align: justify;">
                    
### Effective Number of Parties (ENP)

The concept of the Effective Number of Parties (ENP) is used to measure the number of "effective" parties in a political system. It's not just a count of total parties; rather, it's a weighted measure that takes into consideration the relative strength of each party.
<div>""", unsafe_allow_html=True)
        hint = st.expander("""**How is ENOP calculated?**""", expanded=False)
        with hint:
            st.latex(r"""ENP = \sum_{i=0}^{n} \frac{1}{1 + \frac{p_L^2}{p_i} - p_i} \\
\begin{align*}
&\text{Where:} \\
&p_L \text{ is the largest party's proportion of all votes or seats;} \\
&p_i \text{ is each party's proportion of votes or seats;} \\
&n \text{ is the total number of parties with at least 1 vote or seat.}
\end{align*}
""")
            st.markdown("""<div style="font-family: Georgia; text-align: right; color: darkgrey;">
                
Source: [Wikipedia](https://en.wikipedia.org/wiki/Effective_number_of_parties)
                
<div>""",unsafe_allow_html=True)
        


        st.markdown("""<div style="font-family: Georgia; text-align: justify;">
In a two-party system, the ENP will be close to 2, while in a system with many small parties, the ENP will be much higher.

The idea of dwindling regional parties and the emergence of a bi-polarity in the political landscape is bolstered by this metric. A decreasing ENP over time would suggest a consolidation towards fewer dominant parties.
<div>""",unsafe_allow_html=True)
    with img2:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#")
    img3, gap, description3 = st.columns([0.4,0.05,0.55])

    with img3:
        st.plotly_chart(fig3, use_container_width=True)
    with description3:
        st.markdown("""<div style="font-family: Georgia; text-align: justify;">

### **The Paradox of Participation**

While our previous analysis highlighted the increasing vote share of the two major national parties, BJP and INC, suggesting a consolidation of power, there's another dimension to this story that's worth noting.

The number of parties contesting the elections has seen a remarkable rise over the years. In 2013, a total of 60 parties contested the elections. This number surged to 92 by 2018 and remained consistent in 2023. At first glance, this might seem counterintuitive. A question arises that if the political landscape is being dominated by two major parties, why are more parties entering the electoral race?

Now, I am not a poltical scientist. So, I cannot answer that question. But, in essence, while the vote share data suggests a clear trend towards two-party dominance, the increase in parties contesting elections reveals the dynamic and varied nature of our political landscape. It highlights the vibrancy of our democracy, where multiple voices seek representation, even in the face of daunting odds.

</div>
""", unsafe_allow_html=True)
    

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

def trial():
    st.subheader('State Map with Winning Parties')
    st.text("Note- Constituencies from Bangalore district are shown separately on the side.")
    
    global acmap
    geojson = acmap
    
    ndf = get_parliament_seats()
    ndf.year = ndf.year.astype(str)

    with open('Figures/Seat Distribution/Map2013.html','r', encoding='utf-8') as f:
        Map2013 = f.read()
    with open('Figures/Seat Distribution/Map2018.html','r', encoding='utf-8') as f:
        Map2018 = f.read()
    with open('Figures/Seat Distribution/Map2023.html','r', encoding='utf-8') as f:
        Map2023 = f.read()

    if not (isinstance(ndf, pd.DataFrame)):
        st.error("An error occurred when retrieving data.")
        return

    options = sorted(ndf.year.unique())

    # Let the user select a year
    selected_year = st.radio('Select a Year:', options, horizontal=True)

    # Filter the DataFrame based on the selected year
    ndf_year = ndf[ndf['year'] == selected_year]
    
    @st.cache_data
    def show_year(ndf_year):
        fig = px.choropleth_mapbox(
            ndf_year,
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color='party',
            color_discrete_map={
                'INC': '#0D5BE1',
                'BJP': '#FF7500',
                'IND': 'grey',
                'JD(S)': 'green',
                'KRPP' : 'brown',
                'SKP' : '#A51C30',
                'KJP':'lightgreen',
                'BSRC':'blue'
            },
            labels={'party': 'Winning Party'},
            hover_data=['name', 'constituency', 'party'],
            zoom=7,
        )

        fig.update_traces(
            hovertemplate="<b>Winner:</b> %{customdata[0]}<br><b>Constituency:</b> %{customdata[1]}<br><b>Party:</b> %{customdata[2]}"
        )


        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_zoom=6,
            mapbox_center={"lat": 15.3173, "lon": 76.7139},  # Center coordinates for Karnataka
            uirevision='lock',  # Disable user-driven changes in the view
            dragmode=False,  # Disable panning and zooming
            plot_bgcolor='rgba(0,0,0,0)',  # This sets the plot background to transparent.
            paper_bgcolor='rgba(0,0,0,0)', # rgba(14,17,23,1.000)
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
        )
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_geos(visible=False)  # Fit the map to the boundaries of the locations
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(width=800,height=700)
        return fig

    # st.plotly_chart(show_year(ndf_year),use_container_width=True)
    if selected_year=='2013':
        components.html(html=Map2013,width=1350,height=1200)
    elif selected_year=='2018':
        components.html(html=Map2018,width=1350,height=1200)
    elif selected_year=='2023':
        components.html(html=Map2023,width=1350,height=1200)
    


############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################


def parliament():
    st.subheader('Parliament seat distribution')
    
    components.html("""<div class="flourish-embed flourish-parliament" data-src="visualisation/14582483"><script src="https://public.flourish.studio/resources/embed.js"></script></div>""",height = 710, width=750) #

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################


def vote_margin_map():
    st.header('Heatmap of Vote margins')

    df = get_vote_margin_data()
    df.year = df.year.astype(str)
    if not isinstance(df, pd.DataFrame):
        st.error("An error occurred when retrieving data.")
        return

    # if isinstance(df, pd.DataFrame):

    options = sorted(df.year.unique())

    # Let the user select a year
    
    col1, col2 = st.columns([1,2])

    # User selection of constituency
    with col1:
        selected_year = st.radio('Select a Year:', options, horizontal=True)
    with col2:
        ncol1, ncol2 = st.columns(2)
        with ncol1:
            selected_constituency = st.selectbox('Select a constituency', ['All'] + sorted(list(df['constituency'].unique())))
        with ncol2:
            selected_party = st.selectbox('Select a party', ['All'] + sorted(list(df.loc[df.year==selected_year,'winning party'].unique())))


    party_opacity = const_opacity = opacity = 1
    show_attr = 'Both'
    if selected_party!='All' and selected_constituency != 'All':
        st.warning('Please choose only one of the either.')
        party_opacity = const_opacity = 0
    if selected_constituency=='All' and selected_party!='All':
        const_opacity = 0
        opacity = 0.1
        party_opacity = 1
        show_attr = 'party'
    if selected_party=='All' and selected_constituency!='All':
        opacity = 0.1
        party_opacity = 0
        const_opacity = 1
        show_attr = 'const'
    if selected_party=='All' and selected_constituency == 'All':
        const_opacity = party_opacity = 0
        opacity = 1
        show_attr = 'Both'

    with col2:
        if show_attr=='const':
            df[['votes','margin']] = df[['votes','margin']].astype('Int64')
            show_df = df.loc[df.constituency==selected_constituency,['year','winning party','runner up party','votes','margin','margin percent']].sort_values('year').pivot(columns='year').stack()
            show_df = show_df.reset_index().drop(columns='level_0').set_index('year').transpose().rename(index={'votes': 'winner votes'})
            st.dataframe(show_df)
        elif show_attr=='party':
            show_df = df.loc[df['winning party']==selected_party,['margin','year','margin percent']].groupby('year')[['margin','margin percent']].mean()
            show_df['margin'] = show_df['margin'].apply(lambda x: round(x))
            show_df['margin percent'] = show_df['margin percent'].apply(lambda x: round(x,2))
            show_df = show_df.rename(columns={'margin':'avg margin','margin percent':'avg margin percent'})
            show_df['highest margin percent'] = df.loc[df['winning party']=='BJP',['year','margin percent']].groupby('year')['margin percent'].apply(lambda x: x.sort_values().tail(1).squeeze())
            show_df['lowest margin percent'] = df.loc[df['winning party']=='BJP',['year','margin percent']].groupby('year')['margin percent'].apply(lambda x: x.sort_values().head(1).squeeze())
            show_df = show_df.transpose()
            show_df['change'] = show_df.apply(lambda row: row.values.tolist(), axis=1)
            st.dataframe(show_df, column_config={'change':st.column_config.LineChartColumn('change',width = 'small')}, use_container_width =True)            
        elif show_attr == 'Both':
            st.markdown("""<div style="font-family: Georgia; text-align: center;">
                        
##
##
    
**Choose either of Party or Constituency to see the summary in a tabular format**

<div>""",unsafe_allow_html=True)

    @st.cache_data
    def show_year(df,color_attribute,selected_year,selected_party,selected_constituency,party_opacity,const_opacity,opacity):

        global acmap
        geojson = acmap

        base = px.choropleth_mapbox(
            df.loc[(df.year==selected_year)],
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color=color_attribute,
            color_continuous_scale="turbo",
            labels={'winning party': 'Winning Party'},
            hover_data=['name', 'constituency', 'winning party'],  # Add the hover data
            zoom=7,
            opacity=opacity
        )

        party_layer = px.choropleth_mapbox(
            df.loc[(df.year==selected_year) & (df['winning party']==selected_party)],
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color=color_attribute,
            color_continuous_scale="turbo",
            labels={'winning party': 'Winning Party'},
            hover_data=['name', 'constituency', 'winning party'],  # Add the hover data
            zoom=7,
            opacity=party_opacity
        )

        const_layer = px.choropleth_mapbox(
            df.loc[(df.year==selected_year) & (df['constituency']==selected_constituency)],
            geojson=geojson,
            locations='const_num',
            featureidkey='properties.AC_CODE',
            color=color_attribute,
            # color_continuous_scale="turbo",
            color_discrete_sequence=['red'],
            labels={'winning party': 'Winning Party'},
            hover_data=['name', 'constituency', 'winning party', 'margin'],  # Add the hover data
            zoom=7,
            opacity=const_opacity
        )
        fig = go.Figure()
        for trace in base.data:
            fig.add_trace(trace)

        for trace in party_layer.data:
            fig.add_trace(trace)

        for trace in const_layer.data:
            fig.add_trace(trace)

        fig.layout = base.layout

        fig.update_traces(
            hovertemplate="<b>Winner:</b> %{customdata[0]}<br><b>Constituency:</b> %{customdata[1]}<br><b>Party:</b> %{customdata[2]}<br><b>Margin:</b> %{customdata[3]}"
        )
        fig.update_layout(
            mapbox_style="white-bg",  # Use "white-bg" style
            mapbox_zoom=6,  # Adjust the zoom level as needed (higher zoom for closer view)
            mapbox_center={"lat": 15.3173, "lon": 76.7139},  # Center coordinates for Karnataka
            uirevision='lock',  # Disable user-driven changes in the view
            dragmode=False,  # Disable panning and zooming
            plot_bgcolor='rgba(0,0,0,0)',  # This sets the plot background to transparent.
            paper_bgcolor='rgba(0,0,0,0)', # rgba(14,17,23,1.000)
            title_font=dict(family="Cambria", size=18, color="black"),
            legend_title_font=dict(family="Cambria", size=14, color="black"),
            legend_font=dict(family="Cambria", size=14, color="black"),
        )
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_geos(visible=False)  # Fit the map to the boundaries of the locations
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(height=700) # width=800,
        return fig
    
    img1, img2 = st.columns(2)
    with img1:
        st.plotly_chart(show_year(df,'margin',selected_year,selected_party,selected_constituency,party_opacity,const_opacity,opacity),use_container_width=True)
    with img2:
        st.plotly_chart(show_year(df,'margin percent',selected_year,selected_party,selected_constituency,party_opacity,const_opacity,opacity),use_container_width=True)

    # top_5_highest_margin = df.groupby('year').apply(lambda x: x.nlargest(5, 'margin')).reset_index(drop=True)
    # top_5_lowest_margin = df.groupby('year').apply(lambda x: x.nsmallest(5, 'margin')).reset_index(drop=True)

    # # Get the constituencies with highest and lowest margins
    # highest_margin_constituencies = top_5_highest_margin['constituency'].unique()
    # lowest_margin_constituencies = top_5_lowest_margin['constituency'].unique()

    # # Filter the original data for these constituencies
    # highest_margin_data = df[df['constituency'].isin(highest_margin_constituencies)]
    # lowest_margin_data = df[df['constituency'].isin(lowest_margin_constituencies)]

    # # Get the trends of winning parties in these constituencies
    # highest_margin_trends = highest_margin_data.pivot(index='year',columns='constituency',values='winning party')
    # lowest_margin_trends = lowest_margin_data.pivot(index='year',columns='constituency',values='winning party')

    # highest_margin_trends_to_show = highest_margin_trends[['B.T.M.Layout','Hukkeri','Arabhavi','Davanagere North','Pulakeshinagar']]

    # st.header('Overview of constituencies with highest vote margins over the years')
    # st.text('Here are the trends for few of the constituencies with the highest margins:')
    # st.dataframe(highest_margin_trends_to_show)

#     st.markdown("""
# From this table we can see how the winning party in each constituency changes over time.
                
# - In some constituencies like B.T.M. Layout and Hukkeri, the same party wins consistently. This indiacates that respective party has a stronghold in the constituency.
# - While in other constituencies, the winning party changed this year copmared to previous years. For example, we can see that Arabhavi was a stronghold for BJP in both 2013 and 2018. But, in 2023 the situation changed drastically and Congress (INC) came in power, that too with a high margin! The scenario is completely reversed in Anekal constituency. To determine what might be the reasons behind this, further analysis is required. (Coming Soon...)
# - In some constituencies like Davanagere North and Pulakeshinagar, the voter preferences have shifted each term. Hence, both of them have different winning parties in each election.
# """)


############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################


############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################


def working_on_right_now():
    st.markdown("""

## Project Overview

This project involves comprehensive data analysis of election data. Currently, I am working on the following analysis tasks:

- *__Identifying Constituencies with High Marginal Wins:__* Uncovering the constituencies where candidates won by significant margins.
- *__Region cluster analysis for party strongholds:__*            
- *__Highlighting Swing States:__* Analyzing the constituencies with the smallest win margins, similar to the concept of "swing states" in the U.S.
- *__Tracking Re-election of Candidates:__* Investigating whether any candidates have been re-elected in consecutive elections.
- *__Analyzing Voter Count and Turnout:__* Identifying the constituencies with the highest voter counts and voter turnout percentages.
- *__Exploring the 'None of the Above' (NOTA) Option:__* Assessing the constituencies with the highest NOTA vote percentages and the overall total NOTA percentage.
- *__Creating a Word Cloud:__* Generating a word cloud from words used in affidavits favoring criminal MLAs.
- *__Examining Candidates' Education:__* Determining how the average and median education levels of candidates have changed over the years, across different political parties and genders.
- *__Profiling Highly Qualified Candidates:__* Tracking the number of highly qualified candidates in various political parties over the years.
- *__Monitoring Voter Turnout Over the Years:__* Investigating the patterns and trends in voter turnout over different election years.
- *__Criminal Records of Candidates by Party:__* Creating a line graph showing the number of candidates with criminal records from each political party, with marker sizes determined by the average number of cases.
- *__Swing Constituency Analysis:__* Conducting a detailed study of constituencies which have a fluctuating voting pattern.

## Future Enhancements

Here are potential future enhancements to this project that I am considering:

- *__Studying Candidates' Strategies in Marginal Constituencies:__* If a constituency had a narrow winning vote margin in a previous election, I aim to analyze how candidates change their strategy in the subsequent election to not let history repeat itself.
- *__Investigating the Impact of the NOTA Option:__* I plan to explore whether NOTA votes are actually useless, or if people do not realize their potential power.
- *__Delving into Serious Crimes:__* I wish to examine which candidates have committed serious crimes and whether they have been convicted.
- *__Election Expenditure Analysis:__* I intend to analyze the declared election expenditure of candidates, and compare it with seizures of money reported in local newspapers of constituencies/districts during elections/campaigns.

    """)

############################################################################################################################################
############################################################ NEW FUNCTION ##################################################################
############################################################################################################################################

# Run the app
if __name__ == '__main__':
    main()