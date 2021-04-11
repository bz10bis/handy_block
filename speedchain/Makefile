reset_db:
	rm app.db
	rm  -rf migrations/
	flask db init
	flask db migrate
	flask db upgrade

run:
	 export FLASK_APP=speedchain.py && python3 -m flask run