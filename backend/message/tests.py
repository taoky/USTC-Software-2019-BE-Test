import json
from time import sleep
from django.test import TestCase, Client
from django.shortcuts import reverse

from message.models import Message


class MessageTests(TestCase):
    _test_user_info = {
        'username': 'test',
        'email': 'test@test',
        'password': 'testtest123654',
        'first_name': 'test_first',
        'last_name': 'test_last'
    }

    def _register_then_login(self):
        self.client = Client()
        request = {'register_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:register'), request)
        self.assertEqual(response.status_code, 201)
        request = {'login_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:login'), request)
        self.assertEqual(response.status_code, 200)

    def _logout(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 200)

    def test_login_then_send_message_then_get_message(self):
        self._register_then_login()
        request = {
            'message_info': json.dumps({
                'hidden_seconds': 1,
                'content': 'test'
            })
        }
        response = self.client.post(reverse('message:send'), request)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('message:recieve'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('content' not in json.loads(response.content)['messages'][0].keys())
        sleep(1)
        response = self.client.get(reverse('message:recieve'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['messages'][0]['content'], 'test')
