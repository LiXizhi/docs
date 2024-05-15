# keepwork 第三方登录流程

dev配置：
前端页面：http://dev.kp-para.cn/third_login
后端api: http://api-dev.kp-para.cn

## 第一步 获取 `client_id` 以及 `client_secret`

## 第二步 跳转至keepwork第三方授权页

需要三个query参数：`client_id`、`state`、`redirect_uri`
`state`自行传值
`redirect_uri`需进行 urlencode
例如：

http://dev.kp-para.cn/third_login?client_id=123&state=aaa&redirect_uri=https%3A%2F%2Fkeepwork.com

## 第三步 用户登录授权后会跳转至redirect_uri并且会带上三个参数

`{{redirect_uri}}?code=38067_3089440&client_id=123&state=aaa`
例如：
https://keepwork.com/?code=38067_3089440&client_id=123&state=aaa

## 第四步 后端使用code去换取用户access_token

接口:

`POST http://api-dev.kp-para.cn/oauth_apps/access_token`

Request Body:

```
{
  "client_id": YOUR_CLIENT_ID, 
  "code": THE_CODE, 
  "client_secret": YOUR_CLIENT_SECRET
}
```

Response Body:

```
{
  "access_token": FOR_GET_USER_PROFILE
}
```

注意：<span style="color:red">code有效期十分钟，用一次就失效</span>
access_token的有效期为两小时

## 第五步 根据access_token获取用户信息

接口:

`GET http://api-dev.kp-para.cn/oauth_apps/user_info?access_token=xxx`

Response Body:
```
{
  "userId": 123, // 用户id
  "username": "test",
  "nickname": "test",
  "portrait": "用户头像链接，可为null"
}
```