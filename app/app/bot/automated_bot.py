import json
import os
import random

import requests
from faker import Faker

HOST = "http://127.0.0.1:9000"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.json')
SIGNUP_URL = '{}/api-v1/auth/signup/'.format(HOST)
POST_URL = '{}/api-v1/posts/'.format(HOST)
LIKE_POST_URL = '{HOST}/api-v1/posts/like/{post_id}/'
SIGNIN_URL = '{}/api-v1/auth/token/'.format(HOST)

fake = Faker()


class UserBot:
    """Bot should read the configuration and create this activity:
        ● signup users (number provided in config)
        ● each user creates random number of posts with any content (up to
        max_posts_per_user)
        ● After creating the signup and posting activity, posts should be liked randomly, posts
        can be liked multiple times"""
    def __init__(self, email, password='password'):
        self.email = email
        self.password = password
        self.access_token = None
        self.session = requests.Session()

    def check_is_authorized(self):
        assert 'Authorization' in self.session.headers

    def signup(self, sign_in=True):
        print("Trying to sign up user {}".format(self.email))
        data = {'email': self.email, 'password': self.password}
        try:
            response = requests.post(SIGNUP_URL, data=data)
        except requests.exceptions.ConnectionError:
            print('Connection error.')
            return False

        is_ok = response.status_code == 201
        if is_ok and sign_in:
            self.signin()
        if not is_ok:
            print("Error signing up {user}. Status code is {code}. Error is {error}".format(
                code=response.status_code,
                error=response.content,
                user=self.email
            ))
        return is_ok

    def create_post(self, data):
        self.check_is_authorized()
        print("Trying to create post by user {}".format(self.email))
        response = self.session.post(POST_URL, data=data)
        is_ok = response.status_code == 201
        if not is_ok:
            print("Error during creating post by user {user}. Status code is {code}. Error is {error}".format(
                code=response.status_code,
                error=response.content,
                user=self.email
            ))

        return is_ok

    def like_random_post(self):
        self.check_is_authorized()

        random_post_id = self.get_random_post_id()
        url = LIKE_POST_URL.format(HOST=HOST, post_id=random_post_id)
        print("Trying to like post {}".format(url))
        response = self.session.post(LIKE_POST_URL.format(HOST=HOST, post_id=random_post_id))

        is_ok = True if response.status_code == 204 else False

        if not is_ok:
            print("Error during liking post {post_id}. Status code is {code}. Error is {error}".format(
                code=response.status_code,
                error=response.content,
                post_id=random_post_id
            ))

        return is_ok

    def signin(self):
        response = requests.post(SIGNIN_URL, data={'email': self.email, 'password': self.password})
        is_ok = True if response.status_code == 200 else False
        if is_ok:
            self.access_token = response.json()['access']
            self.session.headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})
        else:
            print('Error during getting a token by user {user}. Status code is {code}. Error is {error}'.format(
                user=self.email,
                code=response.status_code,
                error=response.content
            ))
        return is_ok

    def get_random_post_id(self):
        response = requests.get(POST_URL, headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        if response.status_code != 200:
            print("Error during getting random post. Status code is {code}. Error is {error}".format(
                code=response.status_code,
                error=response.content
            ))
        all_posts = response.json()
        return random.choice(all_posts).get('id', 0)


def read_config():
    with open(CONFIG_PATH, 'r') as config_file:
        confs = json.loads(config_file.read())
        return confs


def run_bot():
    users = []
    confs = read_config()
    for _ in range(confs['number_of_users']):
        email = fake.email()
        user = UserBot(email)
        result = user.signup()

        if result:
            users.append(user)

    for _ in range(confs['max_posts_per_user']):
        for user in users:
            user.create_post(data={'content': fake.text(200), 'name': fake.text(100)})

    for _ in range(confs['max_likes_per_user']):
        for user in users:
            if not user.like_random_post():
                print('Not liked.')
            else:
                print('liked by user {}'.format(user.email))


run_bot()
