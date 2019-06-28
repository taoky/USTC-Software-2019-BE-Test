import json
import time

from django.shortcuts import reverse
from django.test import TestCase
from django.test.client import Client

# 如果时间过短，可能会导致数据没写进去，使得在展示消息的时候，无法获取到那一条消息
SLEEP_TIME = 0.2


class MsgModelTest(TestCase):
    def register_and_login(self):
        c = Client()

        user_info = {
            'username': 'abcd',
            'password': '12345678abcd'
        }

        resp = c.post(reverse('accounts:register'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        resp = c.post(reverse('accounts:login'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        return c

    def create_message(self, c, msg_data):
        resp = c.post(reverse('msg:create_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        return body

    def test_create_message(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        resp = c.get(reverse('msg:my_all_message'), data=msg_data)
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)
        self.assertEqual(body['content'][0]['content'], '1234567890test@aa')
        self.assertEqual(body['content'][0]['user'], 'abcd')

    def test_show_my_message(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)
        self.assertEqual(body['content'][0]['content'], '1234567890test@aa')
        self.assertEqual(body['content'][0]['user'], 'abcd')

        msg_data = {
            'content': 'niegoj3gi',
            'public': False,
            'delay_time': '0:0:1:0'  # 1 mins delay
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        resp = c.get(reverse('msg:my_all_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 2)

    def test_all_message(self):
        c = self.register_and_login()

        # no public msg, no delay
        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        # public msg, no delay
        msg_data = {
            'content': 'asdgnireon',
            'public': True,
            'delay_time': '0:0:0:0'  # no delay
        }
        self.create_message(c, msg_data)

        # public msg, with delay
        msg_data = {
            'content': 'wertyuioasdfghjk',
            'public': True,
            'delay_time': '0:0:1:0'  # 1 mins delay
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:all_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

    def test_message_detail(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        uuid = body['content'][0]['uuid']

        resp = c.get(reverse('msg:message_detail', args=(uuid,)))
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(body['content']['content'], '1234567890test@aa')
        self.assertEqual(body['content']['uuid'], uuid)
        self.assertEqual(body['content']['user'], 'abcd')

    def test_message_detail_with_invaild_uuid(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        import uuid

        new_uuid = uuid.uuid1()

        resp = c.get(reverse('msg:message_detail', args=(new_uuid,)))
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 404)

    def test_create_msg_wrong_format(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0'  # lack of ":"
        }
        resp = c.post(reverse('msg:create_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 410)

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': ':a:&:'  # non-num
        }
        resp = c.post(reverse('msg:create_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 410)

    def test_not_public_message_wrong_user(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        uuid = body['content'][0]['uuid']

        # logout
        resp = c.post(reverse('accounts:logout'))
        body = json.loads(resp.content)

        self.assertEqual(body['code'], 200)

        # register a new user and login
        user_info = {
            'username': 'dcba',
            'password': '12345678abcd'
        }

        resp = c.post(reverse('accounts:register'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        resp = c.post(reverse('accounts:login'), data=user_info)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        resp = c.get(reverse('msg:message_detail', args=(uuid,)))
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 403)

    def test_edit_message(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        old_edit_time = body['content'][0]['edit_time']

        uuid = body['content'][0]['uuid']

        new_msg_data = msg_data.copy()
        new_msg_data['content'] = 'adasf34g34g34'
        new_msg_data['public'] = True

        resp = c.put(reverse('msg:message_detail', args=(uuid,)),
                     data=new_msg_data, content_type='application/json')
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        self.assertNotEqual(body['content'][0]['edit_time'], old_edit_time)
        self.assertEqual(body['content'][0]['content'], 'adasf34g34g34')

    def test_delete_message(self):
        c = self.register_and_login()

        msg_data = {
            'content': '1234567890test@aa',
            'public': False,
            'delay_time': '0:0:0:0'
        }
        self.create_message(c, msg_data)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 1)

        uuid = body['content'][0]['uuid']

        resp = c.delete(reverse('msg:message_detail', args=(uuid,)))
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)

        time.sleep(SLEEP_TIME)

        resp = c.get(reverse('msg:my_message'), data=msg_data)
        body = json.loads(resp.content)
        self.assertEqual(body['code'], 200)
        self.assertEqual(len(body['content']), 0)
