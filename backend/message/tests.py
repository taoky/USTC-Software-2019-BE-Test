from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message

from time import sleep

import json


# Create your tests here.
class MessageTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='kaleid-liner', password='123456')
        User.objects.create_user(username='Swordyu', password='123456')

    def login(self, username='kaleid-liner', password='123456'):
        self.client.post(reverse('account:login'), {
            'username': username,
            'password': password,
        })

    def send_message(self, content, duration, username='kaleid-liner'):
        self.client.post(reverse('message:create', args=(username,)), {
            'msg_content': content,
            'duration': duration,
        })

    def get_messages(self, username='kaleid-liner'):
        return self.client.get(reverse('message:index', args=(username,)))

    def test_create_and_view_message(self):
        self.login()

        self.send_message('hello', '0')

        response = self.get_messages()
        response = json.loads(response.content)

        self.assertEqual(response['messages'][0]['content'], 'hello')

    def test_view_future_message(self):
        self.login()

        self.send_message('hello', '5')  # five seconds
        self.send_message('world', '1')

        response = self.get_messages()
        response = json.loads(response.content)

        self.assertEqual(len(response['messages']), 0)

        sleep(2)
        response = self.get_messages()
        response = json.loads(response.content)

        self.assertEqual(len(response['messages']), 1)

        sleep(3)
        response = self.get_messages()
        response = json.loads(response.content)

        self.assertEqual(len(response['messages']), 2)

    def test_view_others_message(self):
        expect = {
            'err_code': 2,
            'err_msg': 'Permission denied',
        }

        response = self.get_messages('kaleid-liner')

        self.assertJSONEqual(response.content, expect)

        self.login('Swordyu', '123456')

        response = self.get_messages('kaleid-liner')

        self.assertJSONEqual(response.content, expect)

