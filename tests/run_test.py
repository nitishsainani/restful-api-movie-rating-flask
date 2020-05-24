import unittest
import requests
import json
import random
import string

unittest.TestLoader.sortTestMethodsUsing = None


def randomString(string_length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


url = 'http://0.0.0.0:8080/'
headers = {
    'Content-Type': 'application/json',
    'token': '',
}
token = ['']
movie = {}


class TestFlask(unittest.TestCase):
    def test_1_signup_and_login(self):
        email = randomString() + 'random@gmail.com'
        password = randomString()
        name = randomString(4) + " " + randomString(5)
        res = requests.request(
            'POST',
            url + "signup",
            headers=headers,
            data=json.dumps({
                'email': email,
                'password': password,
                'name': name
            }),
        )

        print(res.json())
        self.assertEqual(res.status_code, 200)
        res = requests.request(
            'POST',
            url + "login",
            headers=headers,
            data=json.dumps({
                'email': email,
                'password': password
            }),
        )
        self.assertEqual(res.status_code, 200)
        token[0] = res.json()['token']

    def test_2_movie(self):
        headers['token'] = token[0]
        title = randomString()
        res = requests.request(
            'POST',
            url + "movies",
            headers=headers,
            data=json.dumps({
                'title': title
            }),
        )
        self.assertEqual(res.status_code, 200)
        movie_id = res.json()['movie']['id']
        res = requests.request(
            'GET',
            url + "movies" + '/' + str(movie_id),
            headers=headers
        )
        print(res.json())
        self.assertEqual(res.json()['title'], title)
        movie.update(res.json())

    def test_3_movie_edit(self):
        headers['token'] = randomString(40)
        res = requests.request(
            'PUT',
            url + "movies" + "/" + str(movie['id']),
            headers=headers,
            data=json.dumps({
                'title': randomString()
            }),
        )
        self.assertNotEqual(res.status_code, 200)

        headers['token'] = token[0]
        new_title = randomString()
        res = requests.request(
            'PUT',
            url + "movies" + "/" + str(movie['id']),
            headers=headers,
            data=json.dumps({
                'title': new_title
            }),
        )
        self.assertEqual(res.status_code, 200)
        res = requests.request(
            'GET',
            url + "movies" + '/' + str(movie['id']),
            headers=headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['title'], new_title)
