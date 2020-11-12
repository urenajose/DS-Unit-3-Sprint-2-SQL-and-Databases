import sqlite3
import pandas as pd

conn = sqlite3.connect('rpg_db.sqlite3')
cur = conn.cursor()

query_1 = """SELECT *,
cm.character_ptr_id as mage, 
cf.character_ptr_id as fighter, 
ct.character_ptr_id as thief,
cn.mage_ptr_id as necromancer,
cc1.character_ptr_id as cleric
FROM charactercreator_character cc
LEFT JOIN charactercreator_cleric cc1
ON cc1.character_ptr_id = cc.character_id
LEFT JOIN charactercreator_fighter cf
ON cf.character_ptr_id = cc.character_id
LEFT JOIN charactercreator_mage cm 
ON cm.character_ptr_id = cc.character_id
LEFT JOIN charactercreator_thief ct 
ON ct.character_ptr_id = cc.character_id
LEFT JOIN charactercreator_necromancer cn
ON cn.mage_ptr_id = cm.character_ptr_id
"""
cur.execute(query_1)

df_rpg_characters = pd.read_sql(query_1, conn)

print(df_rpg_characters.head(3))
print('Number of colums in  df Characters : ',
      len(df_rpg_characters.columns))
print('Number of rows in df Characters : ',
      len(df_rpg_characters.index))
print("How many total Characters are there?",
      len(df_rpg_characters.name.unique()), "\n")
print("How many of each specific subclass?", '\n'
      ,df_rpg_characters[['fighter','thief',
      'necromancer', 'cleric', 'mage']].count())

query_2 = ("""SELECT COUNT(DISTINCT item_id)id, character_id, item_id
FROM charactercreator_character_inventory;""")

cur.execute(query_2)
Inventory_items = cur.fetchall()

print('\n','How many total Items?',Inventory_items[0][0])

query_3 = ("""SELECT COUNT(aw.item_ptr_id) as weapon
FROM armory_item ai
LEFT JOIN armory_weapon aw 
ON aw.item_ptr_id = ai.item_id""")

cur.execute(query_3)
weapons = cur.fetchall()

print('\n','How many of the Items are weapons?',
      weapons[0][0],'How many are not?',
      Inventory_items[0][0]-weapons[0][0])

query_4 = ("""SELECT name, COUNT(cci.item_id)
FROM charactercreator_character cc
LEFT JOIN charactercreator_character_inventory cci
ON cc.character_id = cci.character_id
GROUP by cc.character_id """)

cur.execute(query_4)

df_rpg_characters_i = pd.read_sql(query_4, conn)
df_rpg_characters_i
print('\n','How many Items does each character have?','\n \n',df_rpg_characters_i.head(20),'\n')

query_5 = ("""SELECT name, COUNT(aw.item_ptr_id) 
FROM charactercreator_character cc
LEFT JOIN charactercreator_character_inventory cci
ON cc.character_id = cci.character_id
LEFT JOIN armory_weapon aw 
ON cci.item_id = aw.item_ptr_id 
GROUP by cc.character_id""")

cur.execute(query_5)

df_rpg_characters_w = pd.read_sql(query_5, conn)
df_rpg_characters_w

query_6 = ("""SELECT cc.character_id,cc.name, COUNT(ai.item_id)
FROM charactercreator_character cc
LEFT JOIN charactercreator_character_inventory cci
ON cci.character_id = cc.character_id 
LEFT JOIN armory_item ai 
ON ai.item_id = cci.item_id
GROUP BY cc.character_id""")

cur.execute(query_6)
df_rpg_characters_i = pd.read_sql(query_6, conn)

print('\n','How many weapons does each character have?','\n \n',df_rpg_characters_w.head(20),'\n')
print('\n')
print('On average, how many Items does each Character have?',df_rpg_characters_i.sum()[2]/
      len(df_rpg_characters.name.unique()))
print('\n')
print('On average, how many Weapons does each character have?',df_rpg_characters_w.sum()[1]
      /len(df_rpg_characters.name.unique()))



