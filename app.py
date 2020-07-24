'''
    local updated !!! 

'''
import sqlite3
import requests
import random
from ga import main as m1
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerMessage,StickerSendMessage
)

from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np 
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
from datetime import date,timedelta
import datetime
import os.path
from os import path
import os 




app = Flask(__name__)

line_bot_api = LineBotApi('k/jYg6OB/x9USD5owDtBubPdyD4IqSloC5o7BsuiCeKf1FXV1SZE88wCKhPJDAMLEFAaTsRT0MR8v8zyKi4JKq170lJc6iKgvL4vt32FatLQQPT1VUDLTf3vcZyvJJuVqy+qbkSruRHYIFZrNV9/DwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('beffee348122312dd9435b3214ac39f9')


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





def insert_db(message,id_):
    x = datetime.datetime.now() 
    date_ = x.strftime('%Y-%m-%d %H:%M')
    
    connection = sqlite3.connect("user_db.db")
    c = connection.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_message (user_id text,message text,date text)''')
    
    # Insert a row of data
    c.execute("INSERT INTO user_message (user_id,message,date) VALUES (?,?,?)",(id_,message,date_))
    connection.commit()
    connection.close()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_id = event.source.user_id
    mg = event.message.text
    insert_db(mg,user_id)
    
    if event.message.text =="嗨":
        
        msg = "哈囉,請問是哪個單位的呢？"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    
    elif event.message.text == "測試":
        
        
        msg = date_+"\n測試正常"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
        
    elif event.message.text == "ecmk" or event.message.text=="ECMK":
        
        
        msg = "好的 MK的夥伴想知道什麼?"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    
    elif event.message.text == "今天購物的數據":
        try:
            
            df = m1()
            
            bounces = df.iloc[0,1]
            new_user = df.iloc[0,2]
            users = df.iloc[0,4]
            bounce_rate = str(round(float(df.iloc[0,6])))+"%"
            msg = "今天的 Bounces 是: "+bounces+"\nBounces Rate 是: "+bounce_rate+"\nNew Users 是: "+new_user+"\nUsers 是: "+users
           
            
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))
            
            
            
        except:
            msg = "connect failed !!"
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))
            
    else:
        msg = "我不明白你的意思,你是說"+event.message.text+"?"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
    
    

if __name__ == "__main__":
    app.run()

