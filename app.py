'''
    Project: LINE Internal Hackathon Compeition
    Stakeholder: Steven Tseng
                    Tony Yen
                    Alicia Chen
                    Evelyn Hsiao
                    David Lee

    Overview: Assisting LINE users to locate their intend purchasing items 
    LINE Bot: Deployed on local environment

'''
import sqlite3
import requests
import random
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
import requests 

'''
    Developing Web structure using Flask
'''

app = Flask(__name__)
line_bot_api = LineBotApi('k/jYg6OB/x9USD5owDtBubPdyD4IqSloC5o7BsuiCeKf1FXV1SZE88wCKhPJDAMLEFAaTsRT0MR8v8zyKi4JKq170lJc6iKgvL4vt32FatLQQPT1VUDLTf3vcZyvJJuVqy+qbkSruRHYIFZrNV9/DwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('beffee348122312dd9435b3214ac39f9')
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


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


def top_item():
    ls_url = "https://buy.line.me/daily"
    r = requests.get(ls_url,headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    df = {'price':[],'item':[],'provider':[],'line point':[]}
    tag = soup.find("ul",class_="thumbnails1-list").find_all("li",class_="thumbnails1-item")
    for t in tag:
        
        try:
            df['price'].append(t.find("span",class_="heading-thumbnailPrice").text)
        except:
            df['price'].append(t.find("span",class_="thumbnails-PriceDiscounted heading-thumbnailPriceDiscounted").text)
        df['item'].append(t.find("div",class_="thumbnails1-description heading-thumbnailDescription").text)        
        df['provider'].append(t.find("div",class_="thumbnails1-hVendor").text)
        df['line point'].append(t.find("div",class_="heading-thumbnailPoint thumbnails1-point").text)
    df = pd.DataFrame(df)
    return df


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

'''
    Handling message sent by the users

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_id = event.source.user_id
    mg = event.message.text
    insert_db(mg,user_id)
    
    if event.message.text =="嗨":
        
        msg = "哈囉,請問需要幫你找什麼嗎？"
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))
    
    elif event.message.text == "今日熱銷是什麼":
        df = top_item()
        i = 1
        msg=""
        for p,item,provider,point in zip(df['price'],df['item'],df['provider'],df['line point']):
            msg += "今日熱銷品 top-"+str(i)+"\n價格: "+p+"\n品名: "+item+"\n廠商: "+provider+"\n回饋 LINE Point: "+point+"\n\n"
            i+=1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        
            

    
            
    else:
        msg = "不好意思 我不明白你的意思,你是說 "+event.message.text+"?"
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

