from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

import json


# Create your tests here.
class AccountTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="kaleid-liner", password="123456")

    def test_create_user_with_same_name(self):
        expect = {
            'err_code': 2,
            'err_msg': 'This username has been used'
        }

        response = self.client.post(reverse('account:register'), {
            'username': 'kaleid-liner',
            'password': 'something-else',
        })
        self.assertJSONEqual(response.content, expect)

    def test_login_success(self):
        expect = {
            'err_code': 0,
            'err_msg': ''
        }

        response = self.client.post(reverse('account:login'), {
            'username': 'kaleid-liner',
            'password': '123456',
        })

        self.assertJSONEqual(response.content, expect)

    def test_login_failed(self):
        expect = {
            'err_code': 1,
            'err_msg': 'No such user or wrong password',
        }

        response = self.client.post(reverse('account:login'), {
            'username': 'kaleid-liner',
            'password': '012345',
        })

        self.assertJSONEqual(response.content, expect)

    def test_register_success(self):
        expect = {
            'err_code': 0,
            'err_msg': '',
        }

        response = self.client.post(reverse('account:register'), {
            'username': 'Swordyu',
            'password': 'Swordyu',
        })
        self.assertJSONEqual(response.content, expect)

        response = self.client.post(reverse('account:login'), {
            'username': 'Swordyu',
            'password': 'Swordyu',
        })
        self.assertJSONEqual(response.content, expect)

    def test_logout_failed(self):
        expect = {
            'err_code': 1,
            'err_msg': 'Logout before login'
        }

        response = self.client.get(reverse('account:logout'))
        self.assertJSONEqual(response.content, expect)

    def test_logout_success(self):
        expect = {
            'err_code': 0,
            'err_msg': '',
        }

        self.client.post(reverse('account:login'), {
            'username': 'kaleid-liner',
            'password': '123456',
        })

        response = self.client.get(reverse('account:logout'))
        self.assertJSONEqual(response.content, expect)



