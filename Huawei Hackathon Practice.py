#!/usr/bin/env python
# coding: utf-8



# In[1]:
class ai_assistant:

    def connect_fun(self, database_name: str) -> object:
        try:
            # Huawei Hackathon Practice DB // static Chinook queries
            import sqlite3  # the db we're required to use
            from typing import List

            
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
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        tokenizer = AutoTokenizer.from_pretrained("juierror/flan-t5-text2sql-with-schema-v2")
        model = AutoModelForSeq2SeqLM.from_pretrained("juierror/flan-t5-text2sql-with-schema-v2")

        
        def get_prompt(tables, question):
            prompt = f"""convert question and table into SQL query. tables: {tables}. question: {question}"""
            return prompt

        def prepare_input(question: str, tables:list[str]):
            tables = [f"""{table_name}({",".join(tables[table_name])})""" for table_name in tables]
            tables = ", ".join(tables)
            prompt = get_prompt(tables, question)
            input_ids = tokenizer(prompt,  return_tensors="pt").input_ids
            return input_ids


        def inference(question: str, tables:list[str]) -> str:
            input_data = prepare_input(question=question, tables=tables)
            input_data = input_data.to(model.device)
            outputs = model.generate(inputs=input_data, num_beams=10, max_new_tokens=512)
            result = tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
            #print("initial result: ", result)

            Map = {}
            list_tables = list(tables.values())
            for col in list_tables[0]:
                    if (" " in col):
                        ans = col.lower().replace(" ", "_")
                        Map[ans] = col
            result = result.replace("(", " a121lfvdfsv ")
            result = result.replace(")", " ggb34hgh ")

            for tokens in result.split():
                if tokens in Map:
                    result = result.replace(tokens, Map[tokens])
                    result = result.replace(" a121lfvdfsv ", "(",)
                    result = result.replace(" ggb34hgh ", ")")
            #print("final result: ", result)

            return result
            # return "select `Local Electoral Area` from covid_vaccinations where Statistic_Label='Fully Vaccinated' order by `TLIST(M1)` desc, `VALUE` desc limit 1"
            #         "SELECT T1.Local Electoral Area FROM covid_vaccinations AS T1 JOIN Age Group AS T2 ON T1.Statistic_Code = T2.Statistics_Code GROUP BY T1.Local Electoral Area ORDER BY count(*) DESC LIMIT 1"

        # Function to retrieve data from the database
        def retrieve_data(sql_query):
            try:
                if sql_query:
                    cursor.execute(sql_query)
                    result = cursor.fetchall()
                    return result
                return "Error Occured"
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        
        def get_tables(cursor):
            tables = {}
            for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
                table_name = table[0]
                tables[table_name] = []
                for column in cursor.execute(f"PRAGMA table_info({table_name});"):
                    tables[table_name].append(column[1])
            #print(tables)
            return tables



        # In[5]:

        # Function to generate an answer - This function is important but will be conidered low on priority
        # def generate_answer(result_data):
        #     if result_data is not None:
        #         if len(result_data) > 0:
        #             # basically formats the string line by line from the generated sql response
        #             result_str = "\n".join([f"{row[0]}. {row[1]}" for row in result_data])
        #             return result_str
        #         else:
        #             return "No results found."
        #     else:
        #         return "sorry, cant help you."
            

        sql_query = inference(question, get_tables(cursor))
        #print(sql_query) # for debugging
        result_data = retrieve_data(sql_query)
        #print(result_data) # for debugging
        # answer = generate_answer(result_data)

        
        # return answer
        return result_data

# In[ ]:


# Sample user interaction loop
# Infinite loop is NOT needed but just for debugging to avoid running the whole notebook over and over again esp with limited credits
if __name__ == "__main__":
    flag = True
    while flag == True:
        flag = False
        # user_question = input("Ask me to list artists of albums...: ")
        # user_question = "How many different age groups were tracked for covid vaccinations?"
        user_question = "Which electoral area has worst latest fully vaccinated rate?"
        
        if user_question.lower() == "exit":
            break
        
        ai = ai_assistant()
        # database_name = "chinook.db"
        database_name = "example-covid-vaccinations.sqlite3"
        dbObject = ai.connect_fun(database_name)
        tables = {}
        conn = ai.connect_fun(database_name)
        for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            table_name = table[0]
            tables[table_name] = []
            for column in conn.execute(f"PRAGMA table_info({table_name});"):
                tables[table_name].append(column[1])

        hints = tables
        answer = ai.query_fun(user_question, hints, dbObject)
        print("\n\n --------Answer--------- \n")
        print( answer)
        print("\n\n ----------------------- \n")

    # In[ ]:

    # Close db connection
    # conn.close() // not needed for now
