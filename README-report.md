# USTC-Software 2019 iGEM 后端测试题 报告
## 综述
`backend` 下装载有 `accounts` 和 `message` 两个 app：
- `accounts`：用户登录、登出、注册、信息查询、信息修改。对应必做部分。
- `message`：为自己发送信息，间隔一段时间后才可以查看。对应选做部分。

两个 app 对应的 url 分别为：
- `accounts`：/accounts/
- `message`：/message/

### Request
同一类信息将被放到同一属性下。例如：
```python
request = {
    'login_info': json.dumps({
        'username': 'test',
        'password': 'testasdf'
    })
}
```
所有数据均通过 POST 方法传递

### Response
利用 HTTP status code 表示事务状态：
- 2xx：成功
- 4xx：用户错误

当返回 2xx 时，有以下几种情况：
- 200 成功
- 201 创建成功
- 204 删除成功

若未做说明，则应认为成功时返回 200。

当返回 4xx 时，response 中将会有 `error_code` 和 `message` 属性，以表示错误信息。
`error_code` 为可转为 int 的 str。前三位对应 HTTP status code，后三位分级指定一项特殊的错误。
例如：
```python
json.loads(response.content) == {
    'error_code': '401000',
    'message': ''
}
```
对应放回 401，特定的错误为 000。
后三位中的 0 一律用来表示较为特殊的错误，如 401000 中后三位 000 表示无需错误信息，HTTP status code 已经包含了所有必要的错误信息。具体的规则将在下文一一描述。

## /accounts/login/ 登录
使 request 登入

### Request
`request.POST['login_info']` 转为 json 后必须有 `username` 和 `password` 项用于登录的验证

### Response
可能的错误码与错误信息如下：
- `401001 username or password error`: 用户验证失败

### Examples
```python
request.data = {
    'login_info': json.dumps({
      'username': 'test',
      'password': 'testtest'
    })
}
```
可以以用户名为 `test`，密码为`testtest` 的用户的身份登入

## /accounts/logout/ 登出
使 request 登出。

### Request
无需数据

### Response
暂时仅 200。

### Examples
无

## /accounts/register/ 注册
注册一个可以登录的新用户。

### Request
`request.POST['register_info']` 转为 json 后必须有 `username` 和 `password` 项用于注册，可以有 `first_name`，`last_name` 和 `email` 项用于初始化用户。

### Response
成功时返回 201。

可能的错误码与错误信息如下：
- `409111 duplicate username`：用户名与已有用户重复
- `400111 invailed user information: too long username`：用户名过长
- `400112 invailed user information: username can not be blank`：用户名不能为空
- `400113 invailed user information: username contains invailed character: %s`：用户名不能包含不合法字符。%s 为检测到的不合法字符。
- `400121 invailed user information: too long first_name`：first_name 过长
- `400131 invailed user information: too long last_name`：last_name 过长
- `400141 invailed user information: too long email`：邮箱过长
- `400142 invailed user information: email is invailed`：邮箱不合法
- `400151 invailed user information: too long password`：密码过长
- `400152 invailed user information: too short password`：密码过短
- `400001 invailed user information: except attribute: %s`：所给信息不全。%s 为缺少的信息。

### Examples
```python
request.data = {
    'register_info': json.dumps({
      'username': 'test',
      'password': 'testtest',
      'email': 'test@test'
    })
}
```
可以注册为一个用户名为 `test`， 密码为 `testtest`，邮箱为 `test@test` 的用户

## /accounts/profile/show/ 用户信息的查询
返回当前用户的基本信息。需要登录。

### Request
无需数据。需要登录。

### Response
未登录时，返回 401，错误码与错误信息为 `401000 `，即 `message` 为空。

返回的 `response.content` 中应有 `username`，`email`，`first_name`，`last_name` 三项，为用户信息，无论此信息是否为空。

### Examples
对于用户信息为：
```python
user_info = {
    'username': 'test',
    'password': 'testasdf',
    'email': 'test@test',
    'first_name': '',
    'last_name': ''
}
```
的用户，登录后访问此链接返回的 response 有：
```python
response.content == json.dumps({
    'profile': {
        'username': 'test',
        'email': 'test@test',
        'first_name': '',
        'last_name': ''
    }
})
```

## /accounts/profile/edit/ 用户信息的修改
利用所给的信息修改用户信息。需要登录。

### Request
`request.POST['new_profile']` 转为 json 后应有 `email`，`first_name`，`last_name`，`password` 这些项中的若干项（也可以一项都没有）。需要登录。

### Response
若未登入，返回 401，错误码与错误信息为 `401000 `。

可能的错误码与错误信息如下：
- `400121 invailed user information: too long first_name`：first_name 过长
- `400131 invailed user information: too long last_name`：last_name 过长
- `400141 invailed user information: too long email`：邮箱过长
- `400142 invailed user information: email is invailed`：邮箱不合法
- `400151 invailed user information: too long password`：密码过长
- `400152 invailed user information: too short password`：密码过短
- `400001 invailed user information: except attribute: %s`：所给信息不全。%s 为缺少的信息。

### Examples
```python
request = {
    'new_profile': json.dumps({
        'password': 'testtestasdf'
    })
}
```
将会使得后端将当前用户的密码修改为 `testtestasdf`，其他信息保持不变

## /message/send/ 发送信息
发送一条信息给自己，并设置多久后可以查看。

### Request
`request.POST['message_info']` 转为 json 后应有 `content`，`hidden_seconds` 项。需要登录。

### Response
成功时返回 201。

可能的错误码与错误信息如下：
- `400211 invailed message information: too long content`：消息内容过长
- `400212 invailed message information: content can not be blank`：消息内容不能为空
- `400221 invailed message information: hidden secoonds can not be minus`：隐藏秒数不能为负
- `400001 invailed message information: except attribute: %s`：所给信息不全。%s 为缺少的信息。

### Examples
```python
request = {
    'message_info': json.dumps({
        'content': 'test',
        'hidden_seconds': 5
    })
}
```
将会创建一条内容为 test，5 秒后可见的消息给自己。

## /message/recieve/ 接收信息
查询获得已经发给自己的所有消息。如已可见则显示内容，否则不显示内容而只显示其他信息。

### Request
无需数据。需要登录。

### Response
转为 json 后 `response.content['messages']` 为一数组，其中每一项为一个对象，对应一条消息，有 `sent_time`，`recieved_time`，`hidden_seconds` 三项属性，且如果消息已经可见，则还有 `content` 属性。消息间按照 `sent_time` 从大到小（从前到后）的顺序排序。相关时间项使用了 `isoformat()` 函数输出 ISO 标准时间格式。

### Examples
```python
json.loads(response) == {
    'messages': [
        {
            'hidden_seconds': 50,
            'sent_time': ...,
            'recieved_time': ...
        },
        {
            'hidden_seconds': 5,
            'sent_time': ...,
            'recieved_time': ...,
            'content': 'test'
        }
    ]
}
```
为可能的一个 response。
