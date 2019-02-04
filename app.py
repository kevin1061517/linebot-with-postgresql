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
