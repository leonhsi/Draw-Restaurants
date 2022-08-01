from flask import Flask, g, render_template, request
import csv
import sqlite3
import random

app = Flask(__name__)
SQLITE_DB_PATH = 'restaurants.db'
SQLITE_DB_SCHEMA = 'create_db.sql'
MEMBER_CSV_PATH = 'restaurants.csv'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(SQLITE_DB_PATH)
		db.execute("PRAGMA foreign_keys = ON")
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
	db = get_db()
	
	# Draw restaurant ids from given style
	# If ALL is given then draw from all restaurants
	style = request.form.get('style', 'ALL')
	valid_restaurants_sql = 'SELECT id FROM restaurants '
	if style == 'ALL':
		cursor = db.execute(valid_restaurants_sql)
	else:
		valid_restaurants_sql += 'WHERE style = ?'
		cursor = db.execute(valid_restaurants_sql, (style, ))
	valid_restaurant_ids = [
		row[0] for row in cursor
	]

    # If no valid restaurants return 404 (unlikely)
	if not valid_restaurant_ids:
		err_msg = "<p>No restaurant in style '%s'</p>" % style
		return err_msg, 404

	# Randomly choose a restaurant
	chosen_restaurant_id = random.choice(valid_restaurant_ids)

	# Obtain the chosen restaurant's information
	restaurant_name, restaurant_style = db.execute(
		'SELECT name, style FROM restaurants WHERE id = ?',
		(chosen_restaurant_id, )
	).fetchone()
	
	# Update draw history
	with db:
		db.execute('INSERT INTO draw_histories (restaurant_id) VALUES (?)', (chosen_restaurant_id, ))

	return render_template('draw.html', name=restaurant_name, style=restaurant_style, )

@app.route('/history')
def history():
	db = get_db()
	recent_histories = db.execute(
			'SELECT r.name, r.style, d.time '
			'FROM draw_histories AS d, restaurants as r '
			'WHERE r.id == d.restaurant_id '
			'ORDER BY d.time DESC '
			'LIMIT 10').fetchall()
	return render_template('history.html', recent_histories=recent_histories)

if __name__ == '__main__':
	app.run(debug=True)
