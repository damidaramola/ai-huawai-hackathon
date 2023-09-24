#!/usr/bin/env python
# coding: utf-8

COLUMNS = {}


# In[1]:
class ai_assistant:
    def connect_fun(self, database_name: str) -> object:
        try:
            # Huawei Hackathon Practice DB // static Chinook queries
            import sqlite3  # the db we're required to use
            from typing import List

            conn = sqlite3.connect(database_name)
            # conn = sqlite3.connect("Chinook_Sqlite.sqlite") #depends on the format of the db, either works

            cursor = conn.cursor()
            return cursor
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    # In[2]:
    def f(*args, **kwargs):
        print(args, kwargs)

    def query_fun(self, question: str, tables_hints: list[str], cursor: object) -> str:

        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        tokenizer = AutoTokenizer.from_pretrained(
            "juierror/flan-t5-text2sql-with-schema-v2"
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            "juierror/flan-t5-text2sql-with-schema-v2"
        )

        def get_prompt(tables, question):
            prompt = f"""convert question and table into SQL query. tables: {tables}. question: {question}"""
            return prompt

        def prepare_input(question: str, tables: list[str]):
            tables = [
                f"""{table_name}({",".join(tables[table_name])})"""
                for table_name in tables
            ]
            tables = ", ".join(tables)
            prompt = get_prompt(tables, question)
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids
            return input_ids

        def inference(question: str, tables: list[str]) -> str:
            input_data = prepare_input(question=question, tables=tables)
            input_data = input_data.to(model.device)
            outputs = model.generate(
                inputs=input_data, num_beams=10, max_new_tokens=512
            )
            result = tokenizer.decode(
                token_ids=outputs[0], skip_special_tokens=True)
            print("final result: ", result)

            return result

        def replace_columns(query: str) -> str:
            import re

            print("init query = ", query)
            for col_underscore, col in COLUMNS.items():
                regex = re.compile(re.escape(col_underscore), re.IGNORECASE)
                tmp = query
                query = regex.sub(r"'" + col + r"'", query)

                # if tmp == query:
                #     regex = re.compile(re.escape(col), re.IGNORECASE)
                #     query = regex.sub(r"'" + col + r"'", query)

            print("query = ", f"{query}")
            return f"{query}"

        # Function to retrieve data from the database
        def retrieve_data(sql_query):
            try:
                if sql_query:
                    cursor.execute(
                        sql_query
                    )  # cursor.execute(replace_columns(sql_query))
                    result = cursor.fetchall()
                    return (True, result)
            except Exception as e:
                return (False, e)

        def get_tables(cursor):
            tables = {}
            for table in cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall():
                table_name = table[0]
                tables[table_name] = []
                for column in cursor.execute(f"PRAGMA table_info({table_name});"):
                    tables[table_name].append(column[1])
            print("func =", tables)
            return tables

        # In[5]:

        # Function to generate an answer - This function is important but will be cons idered low on priority
        def generate_answer(result_data, question):
            if result_data[0]:
                if len(result_data[1]) > 0:
                    # basically formats the string line by line from the generated sql response
                    return result_data[1]
                else:
                    return "No results found."
            else:
               return result_data[1]

        sql_query = inference(question, get_tables(cursor))
        # print(sql_query) # for debugging
        if not sql_query:
            return "sorry, cant help you."
        else:
            # sql_query = replace_columns(sql_query)
            result_data = retrieve_data(sql_query)
            answer = generate_answer(result_data, question)
        # print(result_data) # for debugging

        # return answer
        return answer


# In[ ]:


# Sample user interaction loop
# Infinite loop is NOT needed but just for debugging to avoid running the whole notebook over and over again esp with limited credits
if __name__ == "__main__":
    import testing
    ai = ai_assistant()


    def query_fun(question, table_hints, conn):
        print("success")
        return ai.query_fun(question, table_hints, conn)

    print("testing")
    testing.run_test("example-simple",
            ai.connect_fun, query_fun)


    ############# active below for manual testing

    # flag = True
    # while flag:
    #     print("success")
    #     # flag = False
    #     user_question = input("Query : ")

    #     if user_question.lower() == "exit":
    #         break

    #     ai = ai_assistant()
    #     database_name = "example-simple.sqlite3"
    #     dbObject = ai.connect_fun(database_name)
    #     tables = {}
    #     conn = ai.connect_fun(database_name)
    #     for table in conn.execute(
    #         "SELECT name FROM sqlite_master WHERE type='table';"
    #     ).fetchall():
    #         print(table)
    #         table_name = table[0]
    #         tables[table_name] = []
    #         for column in conn.execute(f"PRAGMA table_info({table_name});"):
    #             print(column[1])
    #             col = "_".join(column[1].split())
    #             tables[table_name].append(col)
    #             COLUMNS[col] = f"{column[1]}"

    #     # print(COLUMNS, "\n")

    #     hints = tables
    #     from pprint import pp

    #     print("table below")
    #     pp(hints)
    #     answer = ai.query_fun(user_question, hints, dbObject)
    #     print("\n\n --------Answer--------- \n")
    #     print(answer)
    #     print("\n\n ----------------------- \n")

    ############# active above for manual testing

    # In[ ]:

    # Close db connection
    # conn.close() // not needed for now
