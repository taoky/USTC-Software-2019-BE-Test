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
        self.assertEqual(json.loads(response.content)["err_code"],"000")
        
    def test_login(self):
        
        response=self.client.get('http://127.0.0.1:8000/account/login')
        self.assertEqual(response.status_code,200)
    
        data={"username":"bill","password":"123456"}
        response=self.client.post('http://127.0.0.1:8000/account/login',data)
        self.assertEqual(response.status_code,200)

        data={"username":"bill","password":"12345"}
        response=self.client.post('http://127.0.0.1:8000/account/login',data)
        self.assertEqual(json.loads(response.content)["err_code"],"102")

        data={"username":"david","password":"123456"}
        response=self.client.post('http://127.0.0.1:8000/account/login',data)
        self.assertEqual(json.loads(response.content)["err_code"],"103")


    def test_register(self):

        response=self.client.get('http://127.0.0.1:8000/account/register')
        self.assertEqual(response.status_code,200)

        data={"username":"david",
        "password":"23456",
        "repassword":"23456",
        "sex":"male",
        "email":"12345@qq.com"}
        response=self.client.post('http://127.0.0.1:8000/account/register',data)
        self.assertEqual(json.loads(response.content)["err_code"],"201")

        data={"username":"david",
        "password":"23456",
        "repassword":"123456",
        "sex":"male",
        "email":"12345@qq.com"}
        response=self.client.post('http://127.0.0.1:8000/account/register',data)
        self.assertEqual(json.loads(response.content)["err_code"],"203")

 
    
    def test_logout(self):
        
        session = self.client.session
        session['username'] = 'bill'
        session.save()

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
        self.assertEqual(json.loads(response.content)["err_code"],"501")

    
    def test_update_user_index_valid(self):

        session = self.client.session
        session['username'] = 'bill'
        session.save()

        response=self.client.get('http://127.0.0.1:8000/account/update_user_index')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)["err_code"],"500")

        data={
            "new_password":"23456",
            "re_new_password":"23456",
            "new_sex":"male",
            "new_email":"12345@qq.com"}
        response=self.client.post('http://127.0.0.1:8000/account/update_user_index',data)
        self.assertEqual(json.loads(response.content)["err_code"],"502")

        data={
            "new_password":"23456",
            "re_new_password":"123456",
            "new_sex":"male",
            "new_email":"12345@qq.com"}
        response=self.client.post('http://127.0.0.1:8000/account/update_user_index',data)
        self.assertEqual(json.loads(response.content)["err_code"],"503")


# Create your tests here.
