import flask, uuid, random
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

""" Helper functions """


def gen_id():
    return str(uuid.uuid4())


def gen_date():
    return datetime.now.strftime("%d/%m/%Y, %H:%M:%S")


""" Helper varirables """

SERVER = {}
USER_LIST = set()
POSTS = {}

""" Helper classes """


class User:
    def __init__(self, name, email):
        self.user_id = gen_id()
        self.liked_post_ids = set()
        self.post_ids = set()

        self.name = name
        self.email = email


class Post:
    def __init__(self, post_title, post_img_base64, user_id):
        self.post_id = gen_id()
        self.comment_ids = set()
        self.like_count = 0
        self.date = gen_date()

        self.post_title = post_title
        self.post_img_base64 = post_img_base64
        self.user_id = user_id

    def json(self):
        return {"post_title": self.post_title, "post_img_base64": self.post_img_base64, "like_count": self.like_count,
                "date": self.date}


class Comment:
    def __init__(self, comment_string, post_id):
        self.comment_id = gen_id()
        self.date = gen_date()

        self.comment_string = comment_string
        self.post_id = post_id

    def json(self):
        return {"comment_id": self.comment_id, "date": self.date, "comment_string": self.comment_string,
                "post_id": self.post_id}


""" Helper function for retrieval of user and post objects """


def retrieve_user_object(name, pswrd):
    if not (name in USER_LIST): return False
    server_key = hash(name + pswrd)
    if not (server_key in SERVER): return False
    return SERVER[server_key]


def retrieve_post_object(post_title, post_img_base64):
    post_hash = hash(post_title + post_img_base64)
    if not (post_hash in POSTS): return False

    post_object = POSTS[post_hash]
    return post_object


"""
Add user to database given json {name: String, pswrd: String, email: String}
Returns True or False if succesfully added
"""


def add_user(name, pswrd, email):
    if name in USER_LIST: return False
    server_key = hash(name + pswrd)
    SERVER[server_key] = User(name, email)
    USER_LIST.add(name)
    return True


""" 
Add post to database given json
Returns True or False if successfuly addded
"""


def add_post(name, pswrd, post_title, post_img_base64):
    user_object = retrieve_user_object(name, pswrd)
    if not (user_object): return False

    post_object = Post(post_title, post_img_base64, user_object.user_id)
    post_hash = hash(post_title + post_img_base64)
    user_object.post_ids.add(post_object.post_id)
    POSTS[post_hash] = post_object
    return True


"""
Adds comment to post given json
Returns True or False if successfully added
"""


def comment_post(post_title, post_img_base64, comment_string):
    post_object = retrieve_post_object(post_title, post_img_base64)
    comment_object = Comment(comment_string, post_object.post_id)
    post_object.comment_ids[comment_object.comment_id] = comment_object
    return True


"""
Likes post given json
Returns True or False if successfully added
"""


def like_post(post_title, post_img_base64):
    post_object = retrieve_post_object(post_title, post_img_base64)
    post_object.like_count += 1
    return True


"""
Returns comments (list of json) given json
"""


def get_post_comments(post_title, post_img_base64):
    post_object = retrieve_post_object(post_title, post_img_base64)
    return list(comment_object.json() for comment_object in post_object.comment_ids.values())


"""
Returns randoms post (json) from all posts
"""


def retrieve_random_post():
    return random.choice(list(POSTS.values())).json()


""" EACH OF THE FUNCTIONS BELOW RETURN JSON / BOOLEAN DATA WHEN PROMPTED WITH A POST REQUEST + JSON TO THE /route_path"""


@app.route("/add_user", methods=["POST"])
def _add_user():
    content = request.get_json()
    return add_user(content["name"], content["pswrd"], content["email"])


@app.route("/add_post", methods=["POST"])
def _add_post():
    content = request.get_json()
    return add_post(content["name"], content["pswrd"], content["post_title"], content["post_img_base64"])


@app.route("/comment_post", methods=["POST"])
def _comment_post():
    content = request.get_json()
    return comment_post(content["post_title"], content["post_img_base64"], content["comment_string"])


@app.route("/like_post", methods=["POST"])
def _like_post():
    content = request.get_json()
    return like_post(content["post_title"], content["post_img_base64"])


@app.route("/get_post_comments", methods=["GET"])
def _get_post_comments():
    content = request.get_json()
    return get_post_comments(content["post_title"], content["post_img_base64"])


@app.route("/retrieve_random_post", methods=["GET"])
def _retrieve_random_post():
    return retrieve_random_post()


if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5050, debug=True)
