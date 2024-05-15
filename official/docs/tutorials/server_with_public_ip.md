# 如何让互联网的用户访问我的服务器？

Paracraft可以免费创建局域网服务器， 但是只有同一个局域网的用户才能彼此访问：比如连接同一个WIFI的多台电脑或者学校机房中的电脑， 一般都在同一个局域网下。 

那么有没有办法让互联网上的任意用户访问我创建的服务器呢？答案是肯定的。

## 方法1：使用"花生壳"第三方软件

我们的家庭网络大都是没有公网的固定IP的。 `花生壳`是一款第三方软件， 它可以将一个固定的`网址+端口`映射到我们的家庭网络中的任何一台计算机的`指定端口`上。 Paracraft默认的端口为8099。

> 下面我们来介绍方法。只需10分钟轻松搞定。 

### 1 安装花生壳（内网穿透）客户端
- 1.打开下载好的安装文件（[戳我下载](http://hsk.oray.com/download/)）
- 2.双击安装包，按照提示安装。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9938/raw#1580829424748image.png
  ext: png
  filename: 1580829424748image.png
  size: '157039'
  unit: px
  width: '600'
  alignment: left

```

### 2 启动Paracraft局域网服务器

- 1.进入世界，点击ESC键， 然后点击架设私服
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9939/raw#1580829517901image.png
  ext: png
  filename: 1580829517901image.png
  size: '44560'
  unit: px
  width: 300

```

- 2.点击创建服务器（全部用默认值即可）
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9940/raw#1580829706871image.png
  ext: png
  filename: 1580829706871image.png
  size: '168854'
  unit: px
  width: 640

```

记录一下你的局域网的IP地址和端口(默认是8099)


### 3 配置花生壳的端口映射

- 1 安装花生壳客户端，输入帐号密码登录（如没有帐号则先点界面右下角 立即注册）。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9941/raw#1580829901090image.png
  ext: png
  filename: 1580829901090image.png
  size: '472773'
  unit: px
  width: 600

```

- 2 花生壳全面免费提供内网穿透服务，若未开通内网穿透服务的帐号在首次登录花生壳客户端时可直接激活。点击右下角的“+”，则可以添加映射了。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9942/raw#1580829932008image.png
  ext: png
  filename: 1580829932008image.png
  size: '40310'
  unit: px
  width: 600

```

- 3 设置服务器配置（端口和ip）。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9943/raw#1580830172302image.png
  ext: png
  filename: 1580830172302image.png
  size: '60127'
  unit: px
  width: 600

```

> 内网地址一般是192或10或172或127开头的IP地址。如果你不知道内网IP地址，也可用`127.0.0.1`

> 注：如果有在花生壳官网购买过固定的端口，外网端口选固定端口填写购买的端口，否则选择临时端口。

- 4 添加成功，产生一个外网访问地址。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9944/raw#1580830307047image.png
  ext: png
  filename: 1580830307047image.png
  size: '83535'
  unit: px
  width: 600

```

这个地址每个人是不同的，将它记录下来。注意不需要前面的tcp://。我们只需要`a29007140r.zicp.vip:26564`


### 4 用客户端测试
你现在可以用公网IP邀请任何人访问你的paracraft服务器了。其他人只需要在Paracraft的加载界面上输入刚刚生成的外网网址即可，例如下面：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/9945/raw#1580830733973image.png
  ext: png
  filename: 1580830733973image.png
  size: '174931'
  unit: px
  width: 600

```

如果你希望获得固定的公网IP，或者更大的带宽，你需要购买花生壳的VIP服务。

## 方法2：使用"神卓互联"第三方软件
方法和花生壳类似，这里就不重复讲解了。
"神卓互联"下载地址为：https://www.kingdriod.cn/

> 目前"神卓互联"是永久免费的。据说有3000台中转服务器。

> 当然，你也可以用其它NAT穿透软件。

## 方法3：使用Paracraft官方代理服务器
> 目前为Beta版，只提供给机构用户， 即将上线。 

我们的服务使用了云端服务器做流量转发，性能更稳定，并且集成了权限管理，自动保存，多人编辑冲突解决等多项功能。

