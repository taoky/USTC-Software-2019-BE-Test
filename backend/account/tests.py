from django.test import TestCase
from django.test import Client
from .models import LoginForm,RegisterForm,User
import json

class AccountTests(TestCase):

    user = User()
    user.name = 'bill'
    user.password = '123456'
    user.gender = 'male'
    user.email = '1111@qq.com'

    def test_index(self):

        self.client = Client()
        response=self.client.get('http://127.0.0.1:8000/account/')
        self.assertEqual(response.status_code,200)
        
    def test_login(self):
        
        response=self.client.get('http://127.0.0.1:8000/account/login')
        self.assertEqual(response.status_code,200)
      #  self.request.POST = self.form
        response=self.client.post('http://127.0.0.1:8000/account/login',self.form)
        self.assertEqual(response.status_code,200)

    def test_register(self):

        response=self.client.get('http://127.0.0.1:8000/account/register')
        self.assertEqual(response.status_code,200)
    
    def test_logout(self):

        response=self.client.get('http://127.0.0.1:8000/account/logout')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)["err_code"],"300")#借鉴了他人的写法

    def test_user_index_invalid(self):

        response=self.client.get('http://127.0.0.1:8000/account/user_index')
        self.assertEqual(json.loads(response.content)["err_code"],"401")

# Create your tests here.
