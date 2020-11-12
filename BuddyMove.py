import sqlite3
import pandas as pd

conn = sqlite3.connect('buddymove_holidayiq.sql')
cur = conn.cursor()

buddymove = pd.read_csv('buddymove_holidayiq.csv')
print(buddymove.head(5))
print(buddymove.shape)

# buddymove_con = sqlite3.connect('buddymove_holidayiq.sql')
# buddymove.to_sql('Main',buddymove_con)


query_1 = ("""SELECT COUNT("index")
FROM Main""")

cur.execute(query_1)
buddymove_1 = cur.fetchall()
print('how many rows you have?', buddymove_1[0][0], '\n')

query_2 = ("""SELECT 'User ID',
COUNT(CASE WHEN Nature>=100 
AND Shopping>=100 THEN 1 END)
FROM Main""")

cur.execute(query_2)
buddymove_2 = cur.fetchall()

print("""How many users who reviewed at 
least 100 Nature in the category also
reviewed at least 100 in the Shopping category?""", buddymove_2[0][1])




