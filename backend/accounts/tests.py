import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthTests(TestCase):
    _test_user_info = {
        'username': 'test',
        'email': 'test@test',
        'password': 'testtest',
        'first_name': 'test_first',
        'last_name': 'test_last'
    }

    def _test_register_and_login(self):
        self.client = Client()
        request = {'register_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:register'), request)
        self.assertEqual(response.status_code, 201)
        request = {'login_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:login'), request)
        self.assertEqual(response.status_code, 200)

    def test_register_then_login_then_logout(self):
        self._test_register_and_login()
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 200)

    def test_login_then_show_profile_then_edit_profile_then_show_profile(self):
        self._test_register_and_login()
        request = {'profile': json.dumps({'method': 'show'})}
        response = self.client.post(reverse('accounts:profile'), request)
        self.assertEqual(response.status_code, 200)
        test_profile = self._test_user_info.copy()
        test_profile.pop('password')
        self.assertEqual(json.loads(response.content), test_profile)
        request = {
            'profile': json.dumps({
                'method': 'edit',
                'new_profile': {
                    'first_name': 'first',
                    'last_name': 'last',
                    'email': 'testtest@test'
                }
            })
        }
        response = self.client.post(reverse('accounts:profile'), request)
        self.assertEqual(response.status_code, 200)
        request = {'profile': json.dumps({'method': 'show'})}
        response = self.client.post(reverse('accounts:profile'), request)
        self.assertEqual(response.status_code, 200)
        test_profile = {
            'username': 'test',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'testtest@test'
        }
        self.assertEqual(json.loads(response.content), test_profile)
