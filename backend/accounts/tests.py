import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthTests(TestCase):
    _test_user_info = {
        'username': 'test',
        'email': 'test@test',
        'password': 'testtest123654',
        'first_name': 'test_first',
        'last_name': 'test_last'
    }

    def _test_register_and_login(self):
        request = {'register_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:register'), request)
        self.assertEqual(response.status_code, 201)
        request = {'login_info': json.dumps(self._test_user_info)}
        response = self.client.post(reverse('accounts:login'), request)
        self.assertEqual(response.status_code, 200)

    def test_login_then_logout(self):
        self._test_register_and_login()
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 200)

    def test_show_profile_then_edit_profile_then_show_profile(self):
        self._test_register_and_login()
        response = self.client.post(reverse('accounts:profile_show'))
        self.assertEqual(response.status_code, 200)
        test_profile = self._test_user_info.copy()
        test_profile.pop('password')
        self.assertEqual(json.loads(json.loads(
            response.content)['profile']), test_profile)
        request = {
            'new_profile': json.dumps({
                'first_name': 'first',
                'last_name': 'last',
                'email': 'testtest@test'
            })
        }
        response = self.client.post(reverse('accounts:profile_edit'), request)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('accounts:profile_show'))
        self.assertEqual(response.status_code, 200)
        test_profile = {
            'username': 'test',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'testtest@test'
        }
        self.assertEqual(json.loads(json.loads(
            response.content)['profile']), test_profile)

    def test_edit_profile_with_invailed_password(self):
        """Excepted to fail"""
        self._test_register_and_login()
        request = {
            'new_profile': json.dumps({
                'password': 'new'
            })
        }
        response = self.client.post(reverse('accounts:profile_edit'), request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error_code'], 400001)
        response = self.client.post(reverse('accounts:profile_show'))
        self.assertEqual(response.status_code, 200)
        test_profile = self._test_user_info.copy()
        test_profile.pop('password')
        self.assertEqual(json.loads(json.loads(
            response.content)['profile']), test_profile)

    def test_register_with_invailed_password(self):
        """Excepted to fail"""
        self.client = Client()
        request = {
            'register_info': json.dumps({
                'username': 'test',
                'password': 't'
            })
        }
        response = self.client.post(reverse('accounts:register'), request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error_code'], 400001)

    def test_register_with_invailed_username(self):
        """Excepted to succeed, for Django should call in-built function to
        convert the attribute to the proper value"""
        self.client = Client()
        request = {
            'register_info': json.dumps({
                'username': 'a' * 10000,
                'password': 'asqwrefd'
            })
        }
        response = self.client.post(reverse('accounts:register'), request)
        self.assertEqual(response.status_code, 201)
        request = {
            'login_info': json.dumps({
                'username': 'a' * 10000,
                'password': 'asqwrefd'
            })
        }
        response = self.client.post(reverse('accounts:login'), request)
        self.assertEqual(response.status_code, 200)
