# Draw-Restaurants
Simple backend project to randomly draw restaurant from database

## Environment
Flask, SQLite, macOS

## Setup
create python virtual environment :

```
$ python3 -m venv VENV
$ source VENE/bin/activate
(VENV) $ which python
# path/to/VENV/bin/python
```

exit virtual environment :
```
(VENV) $ deactivate
```

install dependencies :
```
(VENV) $ pip install -r requirements.txt
```

## Database
create SQLite database :
```
python3 setup_db.py
```

## Run Server
```
python3 draw_restaurant.py
```

will run a server listening to http://localhost:5000

