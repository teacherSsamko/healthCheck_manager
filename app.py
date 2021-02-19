import os
import json
import time

import requests
from flask import Flask
from flask import request

from slackBot import SlackBot

app = Flask("api_test")
url_prefix = 'URL TO CHECK'

slack = SlackBot()

@app.route('/')
def hello():
    return 'Hello world'

@app.route('/health_check')
def health_check():
    condition = 'good'
    # health check here
    # check video
    res = check_video_upscaling()
    if res.status_code != 200:
        msg = f'Video Upscaler Stopped\ncode: {res.status_code}\nresponse: {res.text}'
        slack.send_msg(msg)
        condition = 'bad'
    elif res.status_code == 504:
        msg = f'Video Upscaler need re-check after 5 mins.\ncode: {res.status_code}\nresponse: {res.text}'
        slack.send_msg(msg)
        time.sleep(300)
        res = check_upscaling()
        if res.status_code == 200:
            msg = f'Pikavue Video Upscaler Condition is GOOD\nresponse: {res.text}'
            slack.send_msg(msg)
        else:
            msg = f'Video Upscaler Stopped\ncode: {res.status_code}\nresponse: {res.text}'
            slack.send_msg(msg)
            condition = 'bad'
    else:
        msg = f'Pikavue Video Upscaler Condition is GOOD\nresponse: {res.text}'
        slack.send_msg(msg)

    # check image
    res_img = check_image_upscaling()
    if res_img.status_code == 200:
        msg = f'Pikavue Image Upscaler Condition is GOOD\nresponse: {res_img.text}'
        slack.send_msg(msg)
    else:
        msg = f'Image Upscaler Stopped\ncode: {res_img.status_code}\nresponse: {res_img.text}'
        slack.send_msg(msg)
        condition = 'bad'
    
    return condition



def check_video_upscaling():
    url = url_prefix + '/check_video_upscaling'
    res = requests.get(url)
    return res

def check_image_upscaling():
    url = url_prefix + '/check_image_upscaling'
    res = requests.get(url)
    return res

def check_upload():
    url = url_prefix + '/upload'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    test_video = open(os.path.join(BASE_DIR,'test_video.mp4'), 'rb')
    files = {'file':test_video}
    data = {
        'uid':1,
        'model':'R1x2',
        'multiple':'2'
    }
    res = requests.post(url, files=files, data=data)
    idx = ''
    msg = 'Uploader Condition is Good'
    if res.status_code == 201:
        idx = res.json()['idx']
        do_upscale(idx)
    return res

def do_upscale(idx):
    """execute upscale api"""
    url = url_prefix + f'/upscaling'
    res = requests.get(url)
    result = f'{res.status_code} - {res.text}'
    if res.status_code == 200:
        return True
    return False


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)