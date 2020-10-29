import requests
import json
from bs4 import BeautifulSoup as bs
from flask import Flask
import time

app = Flask(__name__)

global worked
global worked2
global count
global igtv
global posts
igtv = {}
posts = {}
count = 0
worked = False
workedi = False

@app.route('/resetvar',methods=['GET'])
def reset_globals():
    global worked
    global workedi
    global val
    val = {}
    worked = False
    workedi = False
    return str(worked)+str(worked2)

@app.route('/',methods=['GET'])
def status_check():
    global worked
    global workedi
    return str(worked)+str(workedi)

@app.route('/youtube/<channel>',methods=['GET'])
def scrape_youtube(channel):
    global dat
    global worked
    if(worked):
        return json.dumps(dat, sort_keys=True, indent=4)
    resp = requests.get('https://721b4e1f1fe8.ngrok.io/youtube/TechTatva')
    dat = resp.json()
    worked = True
    return json.dumps(dat, sort_keys=True, indent=4)

@app.route('/insta/<username>',methods=['GET'])
def scrape_insta(username):
    global count
    global val
    global igtv
    global posts
    global workedi
    if(workedi):
       return json.dumps(val)
    resp = requests.get('https://721b4e1f1fe8.ngrok.io/instaPage')
    soup = bs(resp.text,"html.parser")
    soup_Ar = soup.find_all('script',{'type':'text/javascript'})
    res = []
    for soup_ele in soup_Ar:
        print(soup_ele)
        print(soup_ele.decode_contents())
        if(soup_ele.decode_contents()[:19].strip() == 'window._sharedData'):
            res = res + [soup_ele]
    for soup_ele in res:
        json_str = soup_ele.decode_contents()[21:].strip()[:-1]
        val = json.loads(json_str)
    igtv = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_felix_video_timeline']
    posts = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_owner_to_timeline_media']
    workedi = True
    return json.dumps(val)

@app.route('/igtv/<username>',methods=['GET'])
def scrape_igtv(username):
    global igtv
    return json.dumps(igtv)

@app.route('/posts/<username>',methods=['GET'])
def scrape_posts(username):
    global posts
    return json.dumps(posts)
    

if __name__ == '__main__':
    app.run(host='127.1.1.1',port='5000')
