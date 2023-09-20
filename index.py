import sqlite3
import re
import nltk
import string

# Get databases 
# Get words and stuff that relate to databases through the values 
# Use topic model to find main words in query / Might not need this preprocessing is very good
# Use main words to locate tables(s) that the user might want 
# After finding the tables, then turn prompt into a query
# Return results

con = sqlite3.connect("chinook.db")
cur = con.cursor()

cur.execute("""SELECT name FROM sqlite_master
    WHERE type='table';""")

databases = []  
for row in cur.fetchall():
    databases.append(row[0])

for names in databases:
    cur.execute("SELECT * FROM " + names)
    for row in cur.fetchall():
        print(row, names)



"""
def preprocess_text(text):
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # remove whitespace
    text = text.strip()
    # remove stopwords
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.word_tokenize(text)
    text = [w for w in word_tokens if not w in stop_words]
    # stemming
    stemmer = nltk.stem.PorterStemmer()
    text = [stemmer.stem(word) for word in text]
    # lemmatization
    lemmatizer = nltk.stem.WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text]
    return text


teriminal = True
while teriminal:
    val = input("Enter prompt: ")
    if val == "quit":
        teriminal = False
        con.close() 
        print("Thank you !")
    else:
        cleanText = preprocess_text(val)
        print(cleanText)
    """