from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql_url',None)
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