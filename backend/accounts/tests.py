import json

from django.shortcuts import reverse
from django.test import TestCase
from django.test.client import Client


class AccountsModelTest(TestCase):

    def register_and_login(self, c, user_info):
        resp = c.post(reverse('accounts:register'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        resp = c.post(reverse('accounts:login'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

    def logout(self, c):
        resp = c.post(reverse('accounts:logout'))
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)

    def test_register_easy_password(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678'
        }

        resp = c.post(reverse('accounts:register'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 420)

    def test_duplicate_register(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }

        # First normal register
        resp = c.post(reverse('accounts:register'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        # Second try
        resp = c.post(reverse('accounts:register'), data=user_info)

        body = json.loads(resp.content)
        self.assertEqual(body['code'], 410)

    def test_register_and_login(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

    def test_login_without_correct_password(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

        self.logout(c)

        user_info['password'] = 'asdfdsfadf'
        resp = c.post(reverse('accounts:login'), data=user_info)
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 400)

    def test_change_password(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

        change_password_data = {
            'old_password': '12345678abcd',
            'new_password': 'notji45j9y'
        }
        resp = c.post(reverse('accounts:change_password'),
                      data=change_password_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        self.test_get_profile_without_login()

        user_info['password'] = 'notji45j9y'
        resp = c.post(reverse('accounts:login'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

    def test_get_profile(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

        resp = c.get(reverse('accounts:profile'))
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)
        self.assertEqual(body['nickname'], '')
        self.assertEqual(body['phone_number'], '')

    def test_update_profile(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

        new_profile = {
            'nickname': 'Elsa',
            'phone_number': '12345678'
        }
        resp = c.post(reverse('accounts:profile'), data=new_profile)
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)

        resp = c.get(reverse('accounts:profile'))
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)
        self.assertEqual(body['nickname'], 'Elsa')
        self.assertEqual(body['phone_number'], '12345678')

    def test_get_profile_without_login(self):
        c = Client()

        resp = c.get(reverse('accounts:profile'))
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 401)

        new_profile = {
            'nickname': 'Elsa',
            'phone_number': '12345678'
        }
        resp = c.post(reverse('accounts:profile'), data=new_profile)
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 401)

    def test_logout(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }
        self.register_and_login(c, user_info)

        new_profile = {
            'nickname': 'Elsa',
            'phone_number': '12345678'
        }
        resp = c.post(reverse('accounts:profile'), data=new_profile)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        self.logout(c)

        self.test_get_profile_without_login()
