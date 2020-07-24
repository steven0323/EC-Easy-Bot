import pandas as pd 
from bs4 import BeautifulSoup
import requests

ls_url = "https://buy.line.me/daily"
r = requests.get(ls_url)
soup = BeautifulSoup(r.content,'lxml')
df = {'price':[],'item':[],'provider':[],'line point':[]}
tag = soup.find("ul",class_="thumbnails1-list").find_all("li",class_="thumbnails1-item")
for t in tag:
    print(t.text)
    try:
        df['price'].append(t.find("span",class_="heading-thumbnailPrice").text)
    except:
        df['price'].append(t.find("span",class_="thumbnails-PriceDiscounted heading-thumbnailPriceDiscounted").text)
    df['item'].append(t.find("div",class_="thumbnails1-description heading-thumbnailDescription").text)        
    df['provider'].append(t.find("div",class_="thumbnails1-hVendor").text)
    df['line point'].append(t.find("div",class_="heading-thumbnailPoint thumbnails1-point").text)
df = pd.DataFrame(df)
print(df)

i=1
for p,item,provider,point in zip(df['price'],df['item'],df['provider'],df['line point']):
    msg = "今日熱銷品"+str(i)+"\n價格: "+p+"\n品名: "+item+"\n廠商: "+provider+"\n回饋 LINE Point: "+point
    print(msg)
    i+=1