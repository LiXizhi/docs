## MPython与PC之间的蓝牙通讯

我们可以用图块实现mpython和pc之间的无限通讯。请见下面的例子。 

```@Project
styleID: 1
project:
  projectId: 2564505
  eventName: ''
  projectCustomName: ''
  projectTagsShow: true
  projectMembersShow: false
  projectWorldShow: false
  projectDescriptionShow: false
  projectWorldOpenInWebsite: true

```
### MPython端编程

在mpython端， 我们主要使用下面的方式收发消息。例如定义了一个echo的消息处理函数用于接收来自其他设备（PC）的消息， 我们可以定义多个消息。  

![1714466393156image.png](https://api.keepwork.com/ts-storage/siteFiles/37196/raw)

> 注意1: 由于蓝牙的默认消息只有**20Bytes**， 所以你发送的文本不能超过20Bytes，这里其实是消息名字+文本不能超过20Bytes。 如果超过了， 你需要想办法自己拆包或拼接包。 

> 注意2: 蓝牙的消息是可能丢失的，有时甚至有20%的概率丢掉某个数据包。

注意当你写入注册或发送蓝牙消息函数时，系统会自动创建默认名为**paracraft_ble**的蓝牙外围服务器。如果你有多个蓝牙设备， 可以用下面的命令更改蓝牙服务的名字，例如改为**paracraft_ble2**。 

![1714466511885image.png](https://api.keepwork.com/ts-storage/siteFiles/37198/raw)

> 注意蓝牙的初始化很慢，开机可能需要10-20秒，最好显示一个成功的文字如上。烧录时，第一次可能会出现报错，需要烧录2次。


### PC端的编程

我们可以用图块或命令来编程，和mPython端非常类似： 注册消息，发送消息，启动并连接设备。 同样的只要你注册或发送了蓝牙消息，系统会自动连接名为**paracraft_ble**的外部设备。 如果你希望更改这个名字，可以用 `/bluetooth start paracraft_ble2` 命令。 注意PC和mPython必须用一样的名字，才能成功连接。

下面为注册、发送、连接的三个命令的说明：

```javascript
/bluetooth [start|send|register] [msg_name] [msg]
命令描述
-- send a 'test' message with 'helloworld' string
/bluetooth send test helloworld
-- register a 'test' message with 'test' event handler
/bluetooth register test
-- register a 'test' message with TestEventhandler
/bluetooth register test TestEventhandler
-- start ble and connect to paracraft_ble(default name), 
-- however, there is no need to call start if we use the default name
/bluetooth start
/bluetooth start paracraft_ble
```

当然，我们也提供文本和图形化的方式在代码方块中编程。

```javascript
cmd("/bluetooth start paracraft_ble2")

registerNetworkEvent("ble:echo", function(msg)
    tip(msg)
    msg = tonumber(msg) + 1;
    if(msg <= 300) then
        sendNetworkEvent("ble", "echo", tostring(msg))
    end
end)
```

注意， `ble:` 开头代表蓝牙设备,  后面的名字才是蓝牙消息名。 例如下面的图块定义和发送echo消息。

![1714467488788image.png](https://api.keepwork.com/ts-storage/siteFiles/37211/raw)

这里自己是不会收到发给自己的消息的。所以上面的echo是发给mpython外围设备的。

> 注意： 默认情况下一但蓝牙在PC启动，就会默认自动重连，直到蓝牙的名字被改掉或程序退出。
### 关于ESP32蓝牙芯片的性能

虽然理论是90KB/s, 但在不改MTU等默认值的情况下只能有1KB/s的传输速度。下面是一些测试用例和结果。使用的是matrix:bit掌控版。

1. mpy给PC发500个消息是同步的， 没有延时。 但是mpy发的很慢， 一秒才40-50个int数字短消息。在mpy上发送函数是一个同步函数, 可以大概认为当PC收到了才返回。

![1714467855709image.png](https://api.keepwork.com/ts-storage/siteFiles/37214/raw)

2. PC给mpy发300个消息是异步的。 PC发消息非常快，不需要时间，瞬间显示发送了300个消息。但是这些消息没有真的发成功，会被放在一个PC端的队列中没有真正发出去。mpy接收消息的速度非常慢，一秒只能收到7-9条int短消息， 收完PC300个消息用了38秒，但是都收到了。

```javascript
registerClickEvent(function()
    for i=1, 300 do
        -- send event message
        sendNetworkEvent("ble", "mpy", tostring(i))
        wait(0.01)
        tip(i)
    end
end)
```

3. Round-trip echo是每秒6个来回。 不是很快。 
#### 结论

在不优化MTU等属性的情况下， 默认的ESP32 Matrix:bit板子只适合同步和传送非常少的数据和指令。
#### 参考文献

[https://www.reddit.com/r/esp32/comments/x2c3dd/fixing_slow_ble_data_transmission_esp32_to/](https://www.reddit.com/r/esp32/comments/x2c3dd/fixing_slow_ble_data_transmission_esp32_to/)


