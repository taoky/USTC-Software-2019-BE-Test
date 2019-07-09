from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

import json


# Create your tests here.
class UserProfileTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='kaleid-liner', password='123456')

    def login(self):
        self.client.post(reverse('account:login'), {
            'username': 'kaleid-liner',
            'password': '123456',
        })

    def test_view_and_edit_profile(self):
        expect = {
            'err_code': 0,
            'err_msg': '',
        }

        self.login()
        response = self.client.get(reverse('user_profile:index', kwargs={
            'username': 'kaleid-liner',
        }))
        expect['email'] = ''
        expect['bio'] = ''

        self.assertJSONEqual(response.content, expect)


