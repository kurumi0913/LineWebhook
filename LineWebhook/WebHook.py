"""
Routes and views for the flask application.
"""

from argparse import Action
from cgi import test
from cgitb import handler
from flask import request
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MemberJoinedEvent, MessageAction, MessageEvent, PostbackEvent, QuickReply, QuickReplyButton, TextMessage, TextSendMessage
from LineWebhook import app



app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = 'aT17mBd40MXFymNIdfNpwcsOPWJHpXdJZBStLTGbSkfDGfhiWj0NzRyOOd1cFfXQIkyLVI53Ac1ZH4RQp3nBORu/A2hd1XbxjaZBfPxRWC5fYeoudFDpcrTiGkV+lbl1rw5JWLMdYzID+tRS6869MAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'd076c13e943ac3a6eb9e883479aa28de'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # msg=str(event.message.text)
    # line_bot_api.reply_message(event.reply_token, TextSendMessage("你傳送的訊息是: "+msg))
    msg = event.message.text
    if msg =='@傳送文字':
        try: 
            quick_reply_buttons = [
                QuickReplyButton(action=MessageAction(label='YES!', text='Y')),
                QuickReplyButton(action=MessageAction(label='NO!', text='N'))
            ]
            # 建立文字訊息，並加入快速回覆按鈕
            text_message = TextSendMessage(
                text='$如何?',
                emojis=[
                    {'index': 0,
                     'productId': '5ac1bfd5040ab15980c9b435',
                     'emojiId': '008'
                    },
                ],
                quick_reply = QuickReply(items=quick_reply_buttons)
            )
            line_bot_api.reply_message(event.reply_token, text_message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50000))
    app.run(host='0.0.0.0', port=port,debug=True)

def handle_webhook():
    # 在这里处理 WebHook 请求
    # 例如，你可以从 request 对象中获取发送到 WebHook 的数据
    data = request.get_json()
    # ...
    return 'OK'


