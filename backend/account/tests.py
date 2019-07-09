from django.test import TestCase
from django.test import Client
from .models import LoginForm,RegisterForm,User
import json

class AccountTests(TestCase):

    def setUp(self):

        self.user = User()
        self.user.name = 'bill'
        self.user.password = '123456'
        self.user.sex = 'male'
        self.user.email = '1111@qq.com'
        self.user.save()

    def test_index(self):

        self.client = Client()
        response=self.client.get('http://127.0.0.1:8000/account/')
        self.assertEqual(response.status_code,200)
        
    def test_login(self):
        
        response=self.client.get('http://127.0.0.1:8000/account/login')
        self.assertEqual(response.status_code,200)
    
      #  data={"username":"bill","password":"123456"}
      #  response=self.client.post('http://127.0.0.1:8000/account/login',data,content_type="application/json")
      #  self.assertEqual(response.status_code,200)

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

    def test_user_index_valid(self):
        
        session = self.client.session
        session['username'] = 'bill'
        session.save()
        response=self.client.get('http://127.0.0.1:8000/account/user_index')
        self.assertEqual(json.loads(response.content)["err_code"],"400")
        self.test_logout()

    def test_update_user_index_invalid(self):

        response=self.client.get('http://127.0.0.1:8000/account/update_user_index')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)["err_code"],"500")

    
    def test_update_user_index_valid(self):

        session = self.client.session
        session['username'] = 'bill'
        session.save()
        response=self.client.get('http://127.0.0.1:8000/account/update_user_index')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)["err_code"],"501")
        self.test_logout()

# Create your tests here.
