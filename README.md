Deploying-LineBot-with-PostgreSQL-to-heroku
==== 

Descript
-------
Because I meet lots of difficulties in deploying linebot with PostgreSQL to heroku, I take notes step by step.

Required packages
-------
CMD
```
pip install Flask-Migrate
pip install Flask-Script
pip install psycopg2
```
requirements.txt
```
Flask
Flask-Migrate
Flask-Script
Flask-SQLAlchemy
psycopg2
```
deploy cmd Command
-------
1.(I name the file dbModel.py, and you can transform it into your file name)
```
python dbModel.py db init
```





