## MQTT 物联网 API接口

Host: `mqtt://iot.keepwork.com`
Port: `1883`
ClientId: 定义随机字符串
Username: keepwork用户
Password: keepwork用户密码


## 代码方块示例

### 1. 连接服务器
先调用 mqtt_connect 连接MQTT服务器， 注意请用你自己的paracraft用户名和密码。 
> :point_right: 注意你的密码可能被别人看到，请谨慎使用。

```lua
mqtt_connect({
    server="iot.keepwork.com", 
    user="lixizhi", 
    password="1234"
})
```

#### 如何关闭连接？
当调用mqtt_connect的代码方块停止运行时，会自动断开连接。 

### 2. 订阅主题消息

```lua
mqtt_subscribe("test/topic1", function(msg)
    say("received topic: "..msg)
end)
```

### 3. 发布主题消息
```lua

for i=1, 10 do
    mqtt_publish("test/topic1", "hello"..i)
    wait(1)
end

```
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/27417/raw#1688465721559image.png
  ext: png
  filename: 1688465721559image.png
  size: 180416
  isNew: true
          
```

> 可以在多台电脑上，运行上面的代码。 例如一台发消息， 2台收消息。