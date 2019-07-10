# backend

[![Build Status](https://travis-ci.org/kaleid-liner/USTC-Software-2019-BE-Test.svg?branch=master)](https://travis-ci.org/kaleid-liner/USTC-Software-2019-BE-Test)

## 功能

- `account`: 登陆，登出，注册账号
- `user_profile`: 显示，修改用户相关的信息
- `message`: 用户给自己发送、修改信息，并设置延时
- 完整的单元测试

## API

### Login: `account.views.login_view`

#### Description

登陆

#### URL

[account/login]() or `reverse('account:login')`

### Method

`POST`

### Parameters

这里指 request.POST 中的参数，下同。

|  property  | description |
| :--------: | :---------: |
| 'username' |  username   |
| 'password' |  password   |

#### Response (Json)

| err_code |               err_msg                |               description                |
| :------: | :----------------------------------: | :--------------------------------------: |
|    0     |                  ''                  |                 Success                  |
|    1     |   'No such user or wrong password'   |     Wrong username or wrong password     |
|    2     |     'Please logout before login'     | You haven't logged out before logging in |
|    3     | 'Please enter username and password' |     Not type in username or password     |

#### 备注

> 为什么自己实现了账号的登陆，登出功能？

直接 `path('account/', include('django.contrib.auth.urls'))` 会非常简单，当然那样就无法返回 Json 了（当然总有办法可以改的）。但鉴于此次似乎想考一下我们自己怎么写（？），所以自己随便实现了一下。但用户的模型、authentication 和 session 相关的内容仍然是使用由 django 提供的。

### Logout: `account.views.logout_view`

#### Description

登出

#### URL

[account/logout]() or `reverse('account:logout')`

#### Method

`GET` or `POST`

#### Parameters

None

#### Response (Json)

| err_code |        err_msg        |       description       |
| :------: | :-------------------: | :---------------------: |
|    0     |          ''           |         Success         |
|    1     | 'Logout before login' | You should log in first |

### Register: `account:views.register_view`

#### Description

注册

#### URL

[account/register]() or `reverse('account:register')`

#### Method

`POST`

#### Parameters

|  property  | description |
| :--------: | :---------: |
| 'username' |  username   |
| 'password' |  password   |

#### Response (Json)

| err_code |               err_msg                |           description            |
| :------: | :----------------------------------: | :------------------------------: |
|    0     |                  ''                  |             Success              |
|    1     | 'Please enter username and password' | Not type in username or password |
|    2     |    'This username has been used'     |   This username has been used    |

#### 备注

> 为什么不自动跳转到登陆界面？

因为要返回 Json。下面一些本来应该 redirect 的也没有 redirect，原因与这个相同。

### View user profile: `user_profile.views.index_view`

#### Description

查看用户的个人信息

#### URL

[profile/<slug:username>]() or `reverse('user_profile:index', username)`

#### Method

`GET`

#### Parameters

None

#### Response (Json)

| err_code |    err_msg     | description  | Other Properties |
| :------: | :------------: | :----------: | :--------------: |
|    0     |       ''       |   Success    |        -         |
|    1     | 'No such user' | No such user |        -         |

其中，在成功时，other properties 的内容为：

| property |  description   |
| :------: | :------------: |
| 'email'  | 用户的邮箱地址 |
|  'bio'   | 用户的自我描述 |

#### 备注

> 为什么有只有这几个信息？email 啥的不是能直接存 `django.contrib.auth.models.User` 里吗？

只有这两条个人信息，只是用来展示我完成了用户 profile 的功能。我是通过 `OneToOneField` 的方式将用户和个人信息联系起来，并且通过 django signals 中的 `post_save` 事件实现在创建用户时自动创建对应的 `UserProfile` 模型。

### Edit user profile: `user_profile.views.edit_view`

#### Description

修改用户的个人信息

#### URL

[profile/<slug:username>/edit]() or `reverse('user_profile:edit', username)`

#### Method

`POST`

#### Parameters

| property |  description   |
| :------: | :------------: |
| 'email'  | 用户的邮箱地址 |
|  'bio'   | 用户的自我描述 |

#### Response (Json)

| err_code |       err_msg       |                         description                          | Other Properties |
| :------: | :-----------------: | :----------------------------------------------------------: | :--------------: |
|    0     |         ''          |                           Success                            |        -         |
|    1     |   'No such user'    |                         No such user                         |        -         |
|    2     | 'Permission denied' | You haven't logged in or you have no access to this profile.  (for example, you are a not superuser and you are trying to edit other's profile)|-|

其中，如果成功， Other Properties 的内容是修改后的内容。即：

| property |  description   |
| :------: | :------------: |
| 'email'  | 用户的邮箱地址 |
|  'bio'   | 用户的自我描述 |

#### 备注

> 为什么要在 URL 中加入用户名这个变量？用户要修改肯定得登陆啊，用户名完全可以从 session 中获取啊？

除了与 index view 保持 consistency 外，另一方面的原因是权限控制之后完全可能改变。可能用户可以修改其他用户的 profile，例如超级用户？现在不行，但加入 username 可以保证向后兼容性。

> 为什么不用 `login_required` 控制登陆？

`login_required` 的默认行为是 redirect。与我需求的不同，不如自己返回对应的 `err_code` 和 `err_msg`。

### View messages: `message.views.index_view`

#### Description

看用户给自己发的消息

#### URL

[message/<slug:username>]() or `reverse('message:index', username)`

#### Method

`GET`

#### Parameters

None

#### Response (Json)

| err_code |       err_msg       |                         description                          | Other Properties |
| :------: | :-----------------: | :----------------------------------------------------------: | :--------------: |
|    0     |         ''          |                           Success                            |     messages     |
|    1     |   'No such user'    |                         No such user                         |        -         |
|    2     | 'Permission denied' | You haven't logged in or you have no access to messages.     |        -         |

当成功时，其它属性的内容是：

```json
{
    // --snippet--
    messages: [
        {
            'content': 'content of the message',
            'created_time': '2019-07-10 10:59:43.243448+00:00',
        },
        // more
    ]
}
```

### Create messages: `message.view.create_view`

#### Description

给自己发送消息

#### URL

[message/<slug:username>/create]() or `reverse('message:create', username)`

#### Method

`POST`

#### Parameters

|   property    |                         description                          |
| :-----------: | :----------------------------------------------------------: |
| 'msg_content' |                    content of the message                    |
|  'duration'   | Certain amount of time this message will be hidden from user. Format: "**DD** **HH:MM:SS.uuuuuu**". Default zero if not set. (e.g. "1":  one second, "01:01:01": 3661 seconds, "21 01:01:01": 21 days and 3661 seconds) |

#### Response (Json)

| err_code |       err_msg       |                       description                        |
| :------: | :-----------------: | :------------------------------------------------------: |
|    0     |         ''          |                         Success                          |
|    1     |   'No such user'    |                       No such user                       |
|    2     | 'Permission denied' | You haven't logged in or you have no access to messages. |
|    3     | 'Parameter missing' |                        *Not used*                        |
