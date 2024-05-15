```@Toc
 toc:
  title: 目录
```




# 系统说明
[一网乾坤网络架构](overview)

## 应用研发规范
[一网乾坤应用研发规范](http://keepwork.com/tatfook/wiki/unity)

## 接口介绍
相比严格审核的Keepwork普通接口，开放平台可为第三方服务商提供一套更为**安全的账号验证机制**和更多的**接口操作频率**。
> 注：直接调用普通接口，现会受到Keepwork的严格限制，如：IP流量限制、每个IP每5分钟不能注册接口300次。如果第三方服务商使用普通接口登录，可能会出现IP被封的情况。

## 接入流程
1.【申请接入】[点击此链接](https://github.com/tatfook/wikicraft/issues/415) 在底部留言申请，我们将会尽快处理你的需求。  
2.审核通过后，申请人/申请组织将收到一份含有client_id和client_secret的机密邮件。  
3.用户通过Keepwork 开放平台接口验证流程图，如下：  

* 用户通过客户端登录keepwork普通接口获取keepwork token
* 客户端使用keepwork token换取OAuthCode
* 客户端将OAuthCode发给第三方服务器
* 返回第三方服务器Token给客户端，也可以直接将TCP长连接认证（例如游戏服务器）。

4.第三方服务器通过OAuthCode换取OAuthToken的流程，如下：

* 客户端将OAuthCode发送过第三方服务器
* 第三方服务器通过OAuthCode换取OAuthToken
* 第三方服务器将OAuthToken保存在数据库，并返回第三方服务器token给客户端或将TCP长连接认证

## 服务器接入
**通过OAuthCode换取OAuthToken**

oauthToken是用户在第三方服务器的唯一凭据，用户通过第三方服务商调用Keepwork开放接口，需要使用此凭证，获取成功请将OAuthToken保存在服务器数据中。

**接口调用请求说明：**  

    http请求方式：GET
    http://keepwork.com/api/wiki/models/oauth_app/getTokenByCode?client_id=xxx&code=xxx&client_secret=xxx&username=xxx

**参数说明：**

    |参数          |是否必须|说明
    |code          |是     |在网站或客户端获取的OAuthToken，需与username一致，否则返回空数据
    |username      |否     |keepwork用户名，需与code一致，否则返回空数据
    |client_id     |是     |第三方服务商唯一凭证
    |client_secret |是     |第三方服务商唯一凭证密钥，即client_secret

**返回说明：**  
正确返回：

    {"token":"OAuthToken"}

错误返回：

1.参数错误

    {
        "error": {
            "message": "request params error",
            "id": 2
        }
    }

2.username和code不一致

    {
        "error": 10003,
        "message": "username error"
    }

## 网站接入

**Keepwork登录流程，如下：**
![](https://user-images.githubusercontent.com/3422640/27847646-76180812-6171-11e7-842c-982609da6d20.png)

1. 从Web页面获取OAuthCode
2. 将OAuthCode发送给第三方服务器，用户获得第三方服务器Token

**从Web页面获取OAuthCode**
开发者可以在第三方网站在前端页面发起访问此接口，获取OAuthCode凭证后换取OAuthToken

**接口调用请求说明：**  

    http请求方式：GET
    http://keepwork.com/wiki/oauth?response_type=code&client_id=YOURS&redirect_uri=YOURS

**参数说明：**  

    |参数           |是否必须|说明
    |response_type |是     |填code
    |client_id     |是     |为应用程序申请的client_id
    |redirect_uri  |是     |Keepwork通过GET方式携带OAuthCode参数重定向至第三方服务商认证的页面(URL)


## API调用说明

1. url 默认前缀http://keepwork.com/api/wiki/models, 自带http的url除外
2. 通信数据格式json(请求与响应皆是)
3. 数据类型 string(字符串), number(数字), object(对象), array(数组), unknow(不定未知)
4. 注释符--, #, //, /**/
5. api响应格式{error:{id:number,message:string}, data:object}, 接口返回值默认是data字段值 
6. api请求采用oauth2认证方式， 请将登陆或注册返回的token设置http的请求头Authorization字段中（Authorization: Bearer tokencontent）
7. 分页page指定当前页数，pageSize指定每页记录数量
8. 文档书写格式模仿gitlab(https://docs.gitlab.com/ce/api/users.html) 


# 用户接口

## 用户登录

>用户登录,仅用于非web客户端采用oauth认证时获取用户认证授权调用
```
POST /user/login
```
参数:
* username  string 必填, 用户名 
* password  string 必填, 密码
```
{
  username:string   # 用户名
  password:string   # 密码
}
```
返回:
* token  string 认证token,后续需要验证api需将此值填入Authorization头部
* userinfo object 用户信息对象
```
{
  token:"xxxxxx",
  userinfo:{
    username:"xxxxx",
    ...
  }
}
```

## 用户注册

>用户注册, 所有类型客户端皆可用接口注册用户
```
POST /user/register
```
参数:
* username  string 必填, 用户名 
* password  string 必填, 密码
* channel  string 可选 客户类型 值可为:keepwork, haqi, unknown(default) 
```
{
  username:string   # 用户名
  password:string   # 密码
  channel:string    # 注册来源
}
```
返回:
* token  string 认证token,后续需要验证api需将此值填入Authorization头部
* userinfo object 用户信息对象
* isNewUser number 是否为新用户  1 -- 新用户  0 -- 旧用户(用户已存在,第三方登录绑定时使用)
```
{
  token:"xxxxxx",
  userinfo:{
    username:"xxxxx",
    ...
  },
  isNewUser:1    # 此值可忽略, keepwork内部使用
}
```


## 更改密码

> 更改当前用户密码
```
POST user/changepw
```
参数:
* oldpassword string 旧密码
* newpassword string 新密码 
```
request_params:
{
  oldpassword:string,  # 旧密码
  newpassword:string,  # 新密码 
}
```
返回:
* object 用户信息对象


## 获取当前用户信息
> 只有在当前用户已经登录的情况下才有效
```
GET /user/getProfile
```
参数:
* 无
返回:
* object 用户信息对象


## 判断用户是否登录
> 合作伙伴APP在已登录的情况下会自动授权
```
GET /user/isLogin
```
参数:
* 无
返回:
* object({isLogin:true|false}) 用户登录信息


## 获取用户信息
> 通过用户名获取用户信息
```
GET /user/getBaseInfoByName?username=xiaoyao
```
参数:
* username string 用户名
返回:
* obejct 简短用户信息对象


# 站点接口
## 用户站点列表
>获取用户所有的站点信息不分页  **需求应控制创建数量限制**
```
GET /website/getAllByUsername?username=xiaoyao
```
参数:
* username: string 用户名
返回:
* array([{},{}...]) 站点信息列表

## 用户站点信息
> 通过用户名和站点名获取单一站点
```
GET /website/getByName?username=xiaoyao&sitename=test 
```
参数:
* username string 用户名
* sitename string 站点名
返回:
* object 站点信息

## 创建站点
> 为当前用户创建站点
```
POST /website/createSite
```
参数:
* username string (require) 用户名
* sitename string (require) 站点名
* displayName string 显示名
* ... 略
返回:
* siteinfo object 站点信息
* dataSource object 站点所用的数据源信息, 
```
{
  "siteinfo":{},
  "dataSource":{}   
}
```

## 修改站点
> 修改当前用户管理的站点
```
POST /website/updateByName
```
参数:
* 同创建参数
返回：
* siteinfo object 站点信息



# 大文件上传接口
> 系列接口均需用户认证，并只能操作自己的大文件数据 

## 获取文件
> 通过文件名获取文件信息
```
GET /bigfile/getByFilename?filename=test.mp4
```
参数：
* filename: string 文件名
返回：
* object: 大文件对象

## 获取指定文件列表
> 通过文件名列表获取文件对象列表, 只返回文件名存在的对象列表
```
GET /bigfile/getByFilenameList
```
参数:
* filelist: string array 文件名列表
```
{
  filelist:["file1", "file2"]
}
```
返回:
* object array 文件对象列表


## 获取文件列表
> 获取用户的文件列表
```
GET /bigfile/getByUsername
```
参数：
* 无
返回:
* total number 记录总数
* filelist object array  文件对象列表


## 获取用户存储空间信息
```
GET /bigfile/getUserStoreInfo
```
参数:
* 无
返回：
* total 用户存贮总大小
* used 用户已使用的空间大小

## 文件上传
> 文件上传需要使用qiniu js-sdk将文件先上传至七牛服务器， 上传成功后再调用此接口以便keepwork进行文件管理. 该接口参数信息均在qiniu上传成功回调函数参数可以取到。
```
POST /bigfile/upload
```
参数:
* filename string 文件名
* domain: string 七牛bucket所在域
* key: string 七牛key
* size: number 文件大小
* type: string 文件类型
* hash: string 文件hash值
* channel string **必填 默认为qiniu**
返回：
* object 文件对象
**jssdk配置:**
* unique\_name: true
* uptoken\_url: /api/wiki/models/qiniu/uploadToken
* domain: ov62qege8.bkt.clouddn.com
常规上传步骤:
1. 用户点击按钮，打开文件对话框，选择要上传文件(或直接拖拽文件)
2. 检测上传的文件是否超过用户存贮总量(超了上传会失败)
3. 查询上传的文件是否存在， 已存在提示是否覆盖(filename为key)
4. 上传文件七牛
5. 上传文件信息到keepwork


## 获取文件下载地址
>通过文件对象id获取文件下载地址
```
GET /bigfile/getDownloadUrlById?_id=fileId
```
参数：
* \_id number  文件对象id
返回：
* download\_url string 下载地址

## 删除文件
> 通过文件对象id删除文件
```
DELETE /bigfile/deleteById?_id=fileId
```
参数:
* \_id number 文件对象id
返回：
* 无

## 更改文件名
```
POST /bigfile/changeFilename
```
参数:
* \_id number 文件id
* filename  string  新文件名
返回：
* 略


# 数据源接口
## 获取站点数据源
> 通过用户名和站点名获取站点数据源
```
GET /site_data_source/getSiteDataSource?username="xiaoyao"&sitename="test"
```
参数:
* username string 用户名
* sitename string 站点名 可选 当为空时，取用用户的默认的站点数据源
返回:
* object 数据信息对象
```
{
  "projectName":"keepworktest",   # git仓库名
  "projectId":1111            # git仓库id
  "lastCommitId":"1629dnjsd63",   # 最后一次提交的CommitId
  "dataSourceUsername":"gitlab_rls_xiaoyao",  # git 用户名
  "dataSourceUserId":1233,              # git 用户ID
  "dataSourceToken":"xxxxd"             # private token 权限认证token
  "apiBaseUrl":"http://git.keepwork.com/api/v4", # api url 前缀
  "rawBaseUrl":"http://git.keepwork.com", # raw url 前缀 用于下载
  ...
}
```
> 通projectId，dataSourceToken两个值便可以用户站点的页面进行增删改查, 
> 具体接口文档参考:https://docs.gitlab.com/ce/api/README.html
> 具体页面存贮方式参考: 数据源设计与实现(暂无) 基本原则:存储路径与访问路劲一致,如:
> 访问路径:http://keepwork.com/xiaoyao/test/api 则存储库的路径应为/xiaoyao/test/api.md (注：网页存贮需加后缀.md)


# 页面搜索

## 提交搜索页
> 通过网络爬取到的页面数据通过此接口提交到内部搜索引擎，并存储为网站网页
```
POST /elastic_search/spiderSubmitPageinfo
```
参数:
* filepath: string 必填 文件路径,每篇文章应有自己的独立文件路径(可以直接使用存gitlab的路径,如/dir1/dir2/test)
* content: string 必填 文章内容 md文本
* title: string 可选 表题
* author: stirng 可选 作者
* ... 其它 可选
```
{
  "filepath":"/dir/file",
  "content":"# test",
  "title":"test",
  "author":"xiaoyao",
  ... # 其它可选字段
}
```
返回：
* 忽略
实例:
```
curl -H "Content-Type: application/json" -X POST  --data '{"filepath":"/dir/file", "content":"# test", "title":"test", "author":"xiaoyao"}'  http://keepwork.com/api/wiki/models/elastic_search/spiderSubmitPageinfo
```

# 支付服务
> 第三方服务商接入Keepwork支付前，需先申请OAuth账号，[点击此链接](https://github.com/tatfook/wikicraft/issues/415) 在底部留言申请

## 支付对接信息
> 请开发者在[点击此链接](https://github.com/tatfook/wikicraft/issues/415) 底部留言填写支付对接信息
```
  支付结果通知回调地址：http://example.com/payHook
  商品名：测试商品
  商品描述：测试商品描述
  Keepwork给第三方开发者的app_name: 测试商家
  自定义字段：order_no|订单号
```

## 支付接入流程

![](https://user-images.githubusercontent.com/3422640/29372220-146dd99c-82dd-11e7-925d-0f5a08c8ef5c.png)

### 1.第三方网站发起支付

开发者从第三方网站通过url传参的方式跳转进入支付网关 

> keepwork支付网站地址：http://keepwork.com/wiki/pay

相关参数：

    username：keepwork用户名
    app_name：第三方OAuth账号
    app_goods_id：第三方商品ID
    price：支付金额（单位：元）
    redirect：支付成功后前端跳转的url
    channel：支付渠道，目前支持支付宝（alipay）、微信(wechat)
    additional: 自定义字段（JSON对象格式）

范例：

    http://keepwork.com/wiki/pay?username=username&app_name=demo&app_goods_id=1&price=100&redierct=ttp%3A%2F%2Fkeepwork.com&channel=wechat&additional=%7B"user_nid"%3A13%7D

>注意：请将参数部分进行encodeUrlComponent

### 2.用户支付费用

用户通过手机客户端电脑屏幕的二维码支付。
![](https://user-images.githubusercontent.com/3422640/29404379-694889cc-836d-11e7-868a-d66358675313.png)

### 3.结果回调

#### 支付成功后

前端：若开发者在url中有填写redirect参数，浏览器将会重定向至指定的url。  
后端：Keepwork服务器会通过异步的方式发送支付成功的结果至开发者配置的payCallbackUrl中，开发者需判定请求来源IP是否为：120.132.120.183，否则不予处理。



# 基础服务

## 短信接口
> 只允许指定的内部ip调用发送短信
```
POST /user/sendSms
```
参数:
* cellphone string 电话号码
* code    string 验证码
* expires  string 时间 如 3分钟  用于过期提示   业务方自行实现过期机制
返回:
* 无

