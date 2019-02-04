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

Step 1. initialization 
```
python dbModel.py db init
```
Step 2. Migrate
```
python dbModel.py db migrate
```
Step 3. Upgrade
```
python dbModel.py db upgrade
```

Find SQLALCHEMY_DATABASE_URI on heroku
-------
1.
![](https://i.imgur.com/K6CyCMu.png")
2.
![](https://i.imgur.com/vhdr47P.png")

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

app.py code
-------
```
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
     InvalidSignatureError
)
from linebot.models import (
    SourceUser,SourceGroup,SourceRoom,LeaveEvent,JoinEvent,
    TemplateSendMessage,PostbackEvent,AudioMessage,LocationMessage,
    MessageEvent, TextMessage, TextSendMessage
)
import os
from dbModel import *
import json
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    bodyjson=json.loads(body)
    #app.logger.error("Request body: " + bodyjson['events'][0]['message']['text'])
    app.logger.error("Request body: " + body)
    #insertdata
    print('-----in----------')
    add_data = usermessage(
            id = bodyjson['events'][0]['message']['id'],
            user_id = bodyjson['events'][0]['source']['userId'],
            message = bodyjson['events'][0]['message']['text'],
            birth_date = datetime.fromtimestamp(int(bodyjson['events'][0]['timestamp'])/1000)
        )
    db.session.add(add_data)
    db.session.commit()
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息:
@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    if event.message.text.lower() == 'test':
        print('-----------in')
        data_UserData = usermessage.query.all()
        history_dic = {}
        history_list = []
        for _data in data_UserData:
            history_dic['id'] = _data.id
            history_dic['User_Id'] = _data.user_id
            history_dic['Mesaage'] = _data.message
            history_dic['Date'] = _data.birth_date
            history_list.append(history_dic)
            history_dic = {}
        print(history_list)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text= str(history_list)))  
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

LINEBOT screenshop
====
![](https://i.imgur.com/wgPAnmv.jpg")

Reference
====
https://github.com/twtrubiks/Deploying-Flask-To-Heroku

https://github.com/HowardNTUST/Deploying-flask-linebot-Heroku-with-PostgreSQL-

http://tw.gitbook.net/postgresql/2013080998.html

https://ithelp.ithome.com.tw/articles/10198221
