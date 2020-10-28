import requests
from bs4 import BeautifulSoup as bs
import json
import asyncio

from flask import Flask

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
worked2 = False

@app.route('/resetvar',methods=['GET'])
def reset_globals():
    global worked
    global worked2
    global val
    val = {}
    worked = False
    worked2 = False
    return str(worked)+str(worked2)

@app.route('/',methods=['GET'])
def status_check():
    global worked
    global worked2
    return str(worked)+str(worked2)

@app.route('/youtube/<channel>',methods=['GET'])
def scrape_youtube(channel):
    global dat
    global worked
    url = 'https://www.youtube.com/c/'+channel+'/videos'
    curr_url = browser.current_url.lower()
    if(url.lower() != curr_url):
        browser.refresh()
        browser.get(url)
        time.sleep(1)
        browser.execute_script('document.body.style.zoom = "25%"')
        print('zoming out')
    elif(worked):
        return json.dumps(dat)
    worked = False
    thumb = browser.find_elements_by_tag_name('ytd-grid-video-renderer')
    data = {}
    arr = []
    for thumbnail in thumb:
        img_thumbnail = thumbnail.find_element_by_id('thumbnail')
        href = img_thumbnail.get_attribute('href')
        view = thumbnail.find_element_by_id('metadata').find_element_by_id('metadata-line').find_element_by_tag_name('span').get_attribute('innerHTML')
        img = img_thumbnail.find_element_by_id('img').get_attribute('src')
        #print(href)
        time_v = thumbnail.find_element_by_tag_name('ytd-thumbnail-overlay-time-status-renderer').find_element_by_tag_name('span').get_attribute('innerHTML')
        name = thumbnail.find_element_by_id('details').find_element_by_id('video-title').get_attribute('innerHTML')
        if(img is not None):
            arr = arr + [{
                'title': name,
                'time' : time_v,
                'view':view,
                'link':href,
                'thumbnail':img
                }]
    dat = {'count':len(thumb),'data':arr}
    print(dat)
    worked = True
    return json.dumps(dat)

global val
val = {}
chrome_options = Options()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')
browser = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe", options=chrome_options)

@app.route('/insta/<username>',methods=['GET'])
def scrape_insta(username):
    global count
    global val
    global igtv
    global posts
    if(bool(val)):
       return json.dumps(val) 
    url = 'https://www.instagram.com/'+username+'/'
    resp = requests.get('https://www.instagram.com/'+username+'/')
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
    with open('resp'+str(count)+'.json','w+') as out:
        json.dump(val,out)
        count = count + 1
    igtv = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_felix_video_timeline']
    posts = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_owner_to_timeline_media']
    return json.dumps(val)
    ret = {}
    ret_arr = []
    igtv = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_felix_video_timeline']
    posts = val["entry_data"]["ProfilePage"][0]['graphql']['user']['edge_owner_to_timeline_media']
    for igtv_post in igtv['edges']:
        igtv_post_data = igtv['node']
        cleaned = assign_mposts(igtv_post_data)
        ret_arr = ret_arr + [cleaned]
    ret['igtv'] = ret_arr
    ret_arr = []
    for igtv_post in igtv['edges']:
        igtv_post_data = igtv['node']
        cleaned = assign_mposts(igtv_post_data)
        ret_arr = ret_arr + [cleaned]
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
    app.run()
