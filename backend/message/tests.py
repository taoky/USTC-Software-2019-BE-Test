from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message

import json


# Create your tests here.
class MessageTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="kaleid-liner", password="123456")

    def login(self):
        self.client.post(reverse('account:login'), {
            'username': 'kaleid-liner',
            'password': '123456',
        })

    def test_create_and_view_message(self):
        self.login()

        self.client.post(reverse('message:create', args=('kaleid-liner',)), {
            'msg_content': 'hello',
            'duration': 0,
        })

        response = self.client.get(reverse('message:index', args=('kaleid-liner',)))
        response = json.loads(response.content)

        self.assertEqual(response['messages'][0], 'hello')


    def test_view_future_message(self):
        self.client



