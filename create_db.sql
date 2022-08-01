CREATE TABLE restaurants(
	id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	name TEXT NOT NULL,
	style TEXT
);

CREATE TABLE draw_histories(
	restaurant_id INTEGER,
	time DATETIME DEFAULT (datetime('now', 'localtime')),
	FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
);
