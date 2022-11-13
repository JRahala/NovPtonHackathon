import requests as req
import json

post = {
    'post_title': 'uytujgy',
    'post_img': 'mjhbkjb',
    'user_id': 'kjnkjn'
}
req.get('http://127.0.0.1:5050/add_post',json=json.dumps(post))