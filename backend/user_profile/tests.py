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

        prof_json = {
            'email': 'noob@mail.ustc.edu.cn',
            'bio': 'A sophomore at USTC'
        }

        response = self.client.post(reverse('user_profile:edit', kwargs={
            'username': 'kaleid-liner',
        }), prof_json)

        expect['email'] = prof_json['email']
        expect['bio'] = prof_json['bio']

        self.assertJSONEqual(response.content, expect)

        response = self.client.get(reverse('user_profile:index', kwargs={
            'username': 'kaleid-liner',
        }))
        self.assertJSONEqual(response.content, expect)

    def test_edit_without_login(self):
        expect = {
            'err_code': 2,
            'err_msg': 'Permission denied',
        }

        prof_json = {
            'email': 'noob@mail.ustc.edu.cn',
            'bio': 'A sophomore at USTC'
        }

        response = self.client.get(reverse('user_profile:edit', kwargs={
            'username': 'Swordyu',
        }), prof_json)

        self.assertJSONEqual(response.content, expect)

    def test_edit_other_profile(self):
        expect = {
            'err_code': 2,
            'err_msg': 'Permission denied',
        }

        prof_json = {
            'email': 'noob@mail.ustc.edu.cn',
            'bio': 'A sophomore at USTC'
        }

        self.login()

        response = self.client.get(reverse('user_profile:edit', kwargs={
            'username': 'Swordyu',
        }), prof_json)

        self.assertJSONEqual(response.content, expect)








