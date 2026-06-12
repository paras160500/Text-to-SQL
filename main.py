# Imports
from sqlalchemy import create_engine, inspect
import json , re
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import sqlite3

db_path = "amazon.db"

db_url = "sqlite:///amazon.db"

def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
        
    return json.dumps(schema)


# Text To SQL
def text_to_sql(schema , user_prompt):
    SYSTEM_PROMPT = """
        You are an expert SQL generator. Given a database schema and a user prompt, generate a valid SQL query that answers the prompt. 
        Only use the tables and columns provided in the schema. ALWAYS ensure the SQL syntax is correct and avoid using any unsupported features. 
        Output only the SQL as your response will be directly used to query data from the database. No preamble please. Do not use <think> tags.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:")
    ]) 

    model = ChatOllama(model="deepseek-r1:8b")

    chain = prompt_template | model

    raw_response = chain.invoke({'schema' : schema , 'user_prompt' : user_prompt})
    cleaned_text = re.sub(r"<think>.*?</think>" , "" , raw_response.content , flags=re.DOTALL)
    return cleaned_text.strip() 


def get_data_from_database(prompt):
    schema = extract_schema(db_url)
    sql_query = text_to_sql(schema,prompt)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    res = cur.execute(sql_query)
    results = res.fetchall()
    conn.close()
    return results