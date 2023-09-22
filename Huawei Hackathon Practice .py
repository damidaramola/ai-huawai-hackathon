#!/usr/bin/env python
# coding: utf-8



# In[1]:
class ai_assistant:

    def connect_fun(self, database_name: str) -> object:
        try:
            # Huawei Hackathon Practice DB // static Chinook queries
            import sqlite3  # the db we're required to use
            # import pandas as pd #will come in handy later, currently being used to visulise my csv
            # import torch
            # from transformers
            # import BertTokenizer, BertForQuestionAnswering #will be used for the question answering part
            # connect database - connecting one just for testing
            conn = sqlite3.connect(database_name)
            # conn = sqlite3.connect("Chinook_Sqlite.sqlite") #depends on the format of the db, either works

            cursor = conn.cursor()
            return cursor
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None



    # In[2]:

    def query_fun(self, question: str, 
                  tables_hints: list[str], 
                  cursor: object) -> str:

        import spacy    # NLP Lib, requires pip install tho...
        # Load spaCy NLP model
        nlp = spacy.load("en_core_web_sm")


        # This is where we work on the Schema of the Database
        # Based of a template code on GitHub

        # Function to parse a simple question on the db: just for testing, will make more dynamic later
        def parse_question(user_question):
            parsed_data = {}
            
            # spaCy for NLP parsing
            doc = nlp(user_question)
            
            # Get the relevant entities and keywords
            # This example just checks for list artist or albums in the db: just for testing
            for token in doc:
                if token.text.lower() == "list" and token.head.text.lower() == "artists":
                    parsed_data["action"] = "list artists"
                if token.text.lower() == "list" and token.head.text.lower() == "albums":
                    parsed_data["action"] = "list albums"
            
            return parsed_data


        # In[3]:

        # Function to generate an SQL query based on parsed data
        def generate_sql_query(parsed_data):
            if "action" in parsed_data:
                if parsed_data["action"] == "list artists":
                    # SQL query to list artists
                    return "SELECT ArtistId, Name FROM artists"
                elif parsed_data["action"] == "list albums":
                    # SQL query to list albums
                    return "SELECT AlbumId, Title FROM albums"
            
            return None  # cant handle your query yet 


        # In[4]:

        # Function to retrieve data from the database
        def retrieve_data(sql_query):
            if sql_query:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                return result
            
            return None


        # In[5]:

        # Function to generate an answer - This function is important but will be conidered low on priority
        def generate_answer(result_data):
            if result_data is not None:
                if len(result_data) > 0:
                    # basically formats the string line by line from the generated sql response
                    result_str = "\n".join([f"{row[0]}. {row[1]}" for row in result_data])
                    return result_str
                else:
                    return "No results found."
            else:
                return "sorry, cant help you."
            
        parsed_data = parse_question(question)
        sql_query = generate_sql_query(parsed_data)
        result_data = retrieve_data(sql_query)
        answer = generate_answer(result_data)
        return answer

# In[ ]:


# Sample user interaction loop
# Infinite loop is NOT needed but just for debugging to avoid running the whole notebook over and over again esp with limited credits
if __name__ == "__main__":
    print("Successful")
    while True:
        user_question = input("Ask me to list artists of albums...: ")
        
        if user_question.lower() == "exit":
            break
        
        ai = ai_assistant()
        database_name = "chinook.db"
        hints = ["artists", "albums"]
        dbObject = ai.connect_fun(database_name)
        answer = ai.query_fun(user_question, hints, dbObject)
                                              
        print("Answer is:\n", answer)

    # In[ ]:

    # Close db connection
    # conn.close() // not needed for now
