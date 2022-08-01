import sqlite3
import csv

with open('./restaurants.csv', newline='') as f:
	csv_reader = csv.DictReader(f)
	restaurants = [ (row['餐廳'], row['風格']) for row in csv_reader ]
	print("res : ", restaurants)

with open('create_db.sql') as f:
	create_db_sql = f.read()

db = sqlite3.connect('restaurants.db')
with db:
	db.executescript(create_db_sql)
	db.executemany('INSERT INTO restaurants (name, style) VALUES (?, ?)', restaurants)

#c = db.execute('SELECT * FROM restaurants WHERE style = ? LIMIT 3', ('japan', ))
c = db.execute('SELECT * FROM restaurants')
for row in c:
	print(row)
