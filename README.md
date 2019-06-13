# USTC-Software 2019 iGEM 后端测试题

**DDL: 2019 年 7 月 10 日**

## 任务

你需要：

1. Fork 此仓库至你的账号。
2. 使用 Django，完成如下所述的功能。
3. 在本文件末尾为前端组的同学撰写一份说明文档，使他们了解你的应用的接口等信息。
4. 发起 Pull Request。（请在 PR 时写上你的姓名、学号）

### 约定

为了节约大家的时间，请尽量使用默认配置的组件：

1. 使用 Python 3.6+ 与 Django 2.2。如果你使用了 Python 3.7 的特性，请在报告中注明。
2. 使用默认的数据库 (SQLite)、默认的 HTTP 服务器和默认的端口。
3. 不需要使用 template，不需要编写 HTML 文件。所有接口的返回内容为 JSON。

## 目标功能

### 必须完成的功能

- 登录账户
- 注册账户
- 退出 (log out) 账户
- 显示与修改账户的个人信息

### 可以选做的功能

- 「给未来的自己发送消息」，分为两个接口：
  - 接口 1: 用户可以输入一条消息与这条消息隐藏的时间。例如，某条消息隐藏时间为 5 分钟，则在用户提交 5 分钟之后，这条消息才能在接口 2 中显示。
  - 接口 2: 列出当前用户的所有信息和状态（时间是否达到）。如果某条信息的隐藏时间已经达到，可以显示信息内容，否则不应该显示信息内容。
  - 可以在此基础上扩充更多功能。

### 加分项

这些加分项都是值得提倡的良好的开发习惯，因此我们将它们作为加分项。

- 良好的代码风格（如变量命名）会有额外加分
- 良好的注释和文档会有额外加分
- 良好的 Git 提交记录（每次提交有明确的信息）会有额外加分
- 良好的安全性、鲁棒性和可扩展性会有额外加分
- 良好的单元测试有额外加分

## 其它注意事项和提醒

- 对于以上提到的各项功能，最基础的要求是：用户输入正确的请求时，程序可以给出正确的回复。同时，对于用户发起的错误的请求，程序不会受到灾难性的破坏，不会影响其它用户的正常使用（例如，在注册账户时把已有的账户「覆盖」掉是不容许的）。

  你可以选择将这些功能做得更完善和更安全，具体内容和方式请自行决定，例如检查输入并返回有意义的错误信息等。

- 你可以参考[去年的后端测试题](https://github.com/volltin/USTC-Software-2018-BE-Test)，但请注意，**不要抄袭其他人的代码**，如果某段代码对你编写有帮助，请在注释中写明来源。

- 允许使用任意 PyPI 中的模块，即可以使用 `pip` 命令安装的模块。

- 我们最终的代码会在 Linux 下执行，所以如果你在使用其它操作系统开发，请谨慎使用依赖于特定操作系统的特性。（但这里应该不会出现这种情况）

## 报告

App accounts 对应 /accounts/ 下的 url

Response 的状态码遵循 RESTful 原则：200 表示成功，4xx 表示用户的 request 无法实现。若返回 4xx 时 response.content 无内容，则状态码已可以表达所有错误信息，否则，`response['error_code']` 会对应一种特定的错误，相关错误信息也会被存储于 `response['message']` 中来返回。

### login/ 登录

使 request 登入

#### Request

`request.POST['login_info']` 转为 json 后必须有 `username` 和 `password` 项用于登录的验证

#### Response

可能的错误码与错误信息如下：
- `401001 username or password error`: 用户验证失败

#### Examples

```python
request.data = {
    'login_info': json.dumps({
      'username': 'test',
      'password': 'testtest'
    })
}
```
可以以用户名为 `test`，密码为`testtest` 的用户的身份登入

### logout/ 登出

使 request 登出。

#### Request

无需数据

#### Response

暂时仅 200。

#### Examples

无

### register/ 注册

#### Request

`request.POST['register_info']` 转为 json 后必须有 `username` 和 `password` 项用于注册，可以有 `first_name`，`last_name` 和 `email` 项用于初始化用户。

#### Response

可能的错误码与错误信息如下：
- `409001 duplicate username`：用户名与已有用户重复
- `400001 invailed password`：所希望设定的新密码不合法

#### Examples

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

### profile/ 用户信息的查询与修改

查看或修改用户信息。具体为查看或是修改取决于 `request.POST['profile']` 转为 json 后 `method` 项为 `show` 还是 `edit`。若为 `show`，则在 `response.content` 中将会有 `username`，`email`，`first_name`，`last_name` 项作为返回的用户的信息。若为 `edit`，则从与 `method` 同级的 `new_profile` 中获取新的用户信息以进行更新。

#### Request

要求必须先登入。必须带有的为 `request.POST['profile']` 转为 json 后的 `method` 项

若 `method` 为 `show`，则无需其他数据

若 `method` 为 `edit`，则与 `method` 同级的 `new_profile` 下应有 (`email`, `first_name`, `last_name`， `password`) 这些项中的若干项。

#### Response

若未登入，返回 401

若 `request.POST['profile']` 中的 `method` 项既不为 `show` 也不为 `edit`，返回 204

若 `request.POST['profile']` 中的 `method` 项为 `show`，则 `response.content` 中应有 `email`, `first_name`, `last_name` 三项，为用户信息

若 `request.POST['profile']` 中的 `method` 项为 `edit`，则 `response.content` 中只可能含错误相关的信息。可能的错误码与错误信息如下：
- `400001 invailed password`：所希望设定的新密码不合法

#### Examples

`show` 时：
```python
request.data = {
    'profile': json.dumps({
        'method': 'show'
    })
}
```
将可能使得后端返回如下 response:
```python
json.loads(response.content) == {
    'username': 'test',
    'first_name': '',
    'last_name': '',
    'email': ''
}
```

`edit` 时：
```python
request.data = {
    'profile': json.dumps({
        'method': 'edit',
        'new_profile': {
            'password': 'testtesttest'
        }
    })
}
```
将会使得后端将当前用户的密码修改为 `testtesttest`
