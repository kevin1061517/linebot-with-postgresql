Deploying-LineBot-with-PostgreSQL-to-heroku
==== 

Descript
-------
Because I meet lots of difficulties in deploying linebot with PostgreSQL to heroku, I take notes step by step. I hope this article can help you solve your problem and use PostgreSQL more freely. If you need any futher information, Please feel free to contact me.

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
psycopg2
```
deploy cmd Command
-------
(I name the file dbModel.py, and you can transform it into your file name)
After you have accomplished the step 1, if you would like to insert or delete the column, you just need repaet the step 2 and step 3. 
Step 1.initialization 
```
python dbModel.py db init
```
Step 2.Migrate
```
python dbModel.py db migrate
```
Step 3.Upgrade
```
python dbModel.py db upgrade
```

dbModel.py code
-------
```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql_url',None)#postgres://...........
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class usermessage(db.Model):
    __tablename__ = 'usermessage'
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50))
    message = db.Column(db.Text)
    birth_date = db.Column(db.TIMESTAMP)

    def __init__(self
                 , id
                 , user_id
                 , message
                 , birth_date
                 ):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.birth_date = birth_date


if __name__ == '__main__':
    manager.run()
```





