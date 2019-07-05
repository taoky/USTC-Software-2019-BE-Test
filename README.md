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

## 报告（需要完成）


1.
**简要描述：** 

- 用户注册接口

**请求URL：** 
- ` http://localhost:8000/account/register/
  
**请求方式：**
- POST  GET

**参数：** 

|表单|参数名|必选|类型|说明|
|:--|:----    |:---|:----- |-----   |
|form|username |是  |string |用户名   |
|form|password |是  |string | 密码    |
|form|password2     |是  |string | 确认密码    |
|form|email|是|string|邮件|
|proform|phone|否|string|电话|
|proform|company|否|string|工作单位|
|proform|selfpro|否|text|个人简介|

 **返回参数说明** 

|请求方式|类型|内容|备注|
|:-----  |:-----|:-----|:--                           |
|POST|HttpRedirect   |reverse('account:login')  |成功|
|POST|HttpResponse|fail|失败|
|GET|json|{'form': user_form, 'proform': userpro_form}|account/register.html|

 **备注** 



2.   
**简要描述：** 

- 用户修改个人信息接口

**请求URL：** 
- ` http://localhost:8000/account/edit/
  
**请求方式：**
- POST  GET

**参数：** 

|表单|参数名|必选|类型|说明|
|:--|:----    |:---|:----- |-----   |
|user_form|username |是  |string |用户名   |
|user_form|email|是|string|邮件|
|userprofile_form|phone|否|string|电话|
|userprofile_form|company|否|string|工作单位|
|userprofile_form|selfpro|否|text|个人简介|


 **返回参数说明** 

|请求方式|类型|内容|备注|
|:-----  |:-----|-----|:--                           |
|POST|HttpRedirect   |reverse('account:self')  |成功|
|GET|json|{"user_form": user_form, "userprofile_form": userprofile_form}|account/edit.html|

 **备注** 


3.  
**简要描述：** 

- 个人信息展示接口

**请求URL：** 
-  http://localhost:8000/account/edit/
  
**请求方式：**
- GET

**参数：** 

|表单|参数名|必选|类型|说明|
|:--|:----    |:---|:----- |-----   |
|user|username |是  |string |用户名   |
|user|email|是|string|邮件|
|proform|phone|否|string|电话|
|proform|company|否|string|工作单位|
|proform|selfpro|否|text|个人简介|


 **返回参数说明** 

|请求方式|类型|内容|备注|
|:-----  |:-----|-----|:--                           |
|GET|json|{'user': request.user, 'proform': userpro}|account/myself.html|

 **备注** 
