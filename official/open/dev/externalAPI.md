### API说明
- API返回2xx表示成功 响应数据为api返回数据
- baseURL(下列API中url会省略此前缀) http://10.27.3.3:7001/api/v0/(本地环境)  http://api-stage.keepwork.com/core/v0/(stage环境) http://api.keepwork.com/core/v0/(正式环境)
- 认证token使用keepwork的token
- 默认增删查改(POST|DELETE|UPDATE|GET)都是对用户个人数据操作, 对系统范围资源检索默认提供search接口(post resouces/search) 资源打包默认提供(get resources/detail)
- 非默认接口按归属方式定义,如课程包内课程(packages/:id/lessons 创建-POST 获取-GET) 用户购买(user/:id/subscribe 创建-POST 获取-GET)
- 每个资源默认包含createdAt(创建时间) updatedAt(更新时间)两个字段 

**上海团体使用http非https**

### http status code
- 2xx 请求成功处理  
- 400 客户端请求不合法 输入参数有误
- 401 未认证
- 404 资源不存在
- 409 资源冲突 
- 500 服务端异常

### 用户认证
> 旧接口/api/wiki/models/user/login已被废弃, 使用此接口替代

```
POST users/login
```

参数:
- usernmae string
- password string

返回:
- token string 用户认证token(用于其它API接口头部, Authorization: Bearer token)
- id number 用户ID
- username string 用户名
- nickname string 昵称
- portrait string 头像
- ...

示例
```
curl -H "Content-Type:application/json" -X POST --data "{'username':'xxxx', 'password':'xxxxx'}" https://api.keepwork.com/core/v0/users/login
```

### 获取认证用户信息
> 旧接口/api/wiki/models/user/getProfile废弃, 使用此接口替代

```
GET users/profile/
```
输入:
- 无(需在请求头带认证token)

输出:
- id number 用户ID
- username string 用户名
- nickname string 昵称
- portrait string 头像
- ...

示例
```
curl -H "Authorization: Bearer token"  https://api.keepwork.com/core/v0/users/profile
```

### 接入流程
1. 客户端通过用户名密码登录keepwork获取keepwork的token
2. 客户端将toekn作为自己服务器的登录凭证，发给第三方服务器，第三方服务器通过token像keepwork验证token有效性的(通过接口user/profile, 有效返回对应用户信息, 无效返回非200状态码)
3. 第三方服务器验证token有效表keepwork登录成功，可返回第三方自己的token给用户，也可以直接将TCP长连接认为已经认证（例如游戏服务器）。