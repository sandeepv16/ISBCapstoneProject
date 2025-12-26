#from dotenv import load_dotenv
#load_dotenv() ## load all the environemnt variables
import psycopg
from psycopg import sql

# import streamlit as st
import os
# import sqlite3

import google.generativeai as genai

genai.configure(api_key="AIzaSyChzqCtNmvxHNAt5rbsJmY6Il9Huz6-QeA")


# def get_gemini_response(question,prompt):
   

## Fucntion To retrieve query from the database

# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
#     for row in rows:
#         print(row)
#     return rows


def get_query_from_llm(question):
   

    prompt=  """
        You are an AI assistant specialized in converting natural language questions into PostgreSQL queries. Your task is to generate SQL queries for a database table called 'steelpipes' with the following schema:
        Each entry in the below table will be the number of steel pipes of each shape in an image along with the image_id. The possible shapes are these: 'circle', 'square', 'rectangle',  'hexagon'. The total_pipes field indicates the total number of pipes in the image
    Table: steelpipes
    - id SERIAL PRIMARY KEY,
    - image_id VARCHAR(100) NOT NULL,
    - no_of_square_pipes INTEGER,
    - no_of_rectangle_pipes INTEGER,
    - no_of_circle_pipes INTEGER,
    - no_of_hexagon_pipes INTEGER,
    - total_pipes INTEGER,
    - updation_time TIMESTAMPTZ

    Examples:
    Q: "How many circular pipes are there?"
    A: SELECT SUM(no_of_circle_pipes) FROM steelpipes ;

    Q: "Show me all pipes with number of pipes greater than 50"
    A: SELECT * FROM steelpipes WHERE total_pipes > 50;

    Q: "What's the total count of all pipes updated in the last 7 days?"
    A: SELECT SUM(total_pipes) FROM steelpipes WHERE updation_time >= NOW() - INTERVAL '7 days';

    Q: How many number of pipes are there in the last updated image?
    A: SELECT total_pipes FROM steelpipes WHERE image_id = (   SELECT image_id   FROM steelpipes   ORDER BY updation_time DESC   LIMIT 1 );

    Guidelines:
    1. Generate standard PostgreSQL compatible queries
    2. Use proper date/time functions for timestamp operations
    3. Consider case-insensitive string comparisons where appropriate
    4. Handle aggregations (COUNT, SUM, AVG) when needed
    5. Use appropriate WHERE clauses for filtering
    6. Include ORDER BY for questions about sorting
    7. Use LIMIT when asked for specific number of results

    Note: Always ensure queries are optimized and handle NULL values appropriately.

    also the sql code should not have ``` in beginning or end and sql word in output


        """
    
    
    # query=get_gemini_response(question,prompt)
    # if(type="query"):
    model=genai.GenerativeModel('gemini-1.5-flash-8b')
    response=model.generate_content([prompt,question])
    return response.text


def generate_response_llm(question,query, results):

    response_prompt = f"""
    Given the original question: "{question}"
    And the SQL query: "{query}"
    And the query results: {results}
    
    Please provide a natural language response following this format:
    1. Summary of the findings
    2. Specific details if relevant
    3. Any notable patterns or observations
    4. In case of datatime objects, convert it into proper human readable datetime format
    
    Generate the output in a single paragraph format with proper spacing and line breaks. Don't include any section titles from the above bullet points
    Make sure the response is clear and well-structured.
    """

    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([response_prompt])
    return response.text



# print(query)



def getDataFromSQL(host, user, password, port, query):
    connection = psycopg.connect(host=host, user=user, password=password,  port=port)
    cursor = connection.cursor()
    connection.autocommit = True  


    rows=cursor.execute(query)
    connection.commit()  
    data= rows.fetchall()
    cursor.close()
    connection.close()

    return data

def main():

    question="list the updation times of all pipes"
    # print(query)

    query = get_query_from_llm(question)
    data  = getDataFromSQL(
        host="localhost", user="postgres", password="postgres", port=5432, query=query
    )



    print(generate_response_llm(question, query, data))


if __name__ == "__main__":
    main()












# print(rows.fetchall())
# print(type(rows.fetchall()))



