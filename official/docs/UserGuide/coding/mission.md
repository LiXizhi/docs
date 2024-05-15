## 双重机关与事件

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/18133/raw#1604201604934codeblock7_small.mp4
  ext: mp4
  filename: 1604201604934codeblock7_small.mp4
  size: 29758286
          
```

[在腾讯视频播放](https://v.qq.com/x/page/x077175uf77.html)
```@Project
styleID: 1
project:
  projectId: '1894218'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
**1. 理论**

> 思考：

- 学习如何使用全局变量
- 学习如何发布广播消息和接收广播消息

> 项目知识点：详细内容见本书第二章：编程理论

<div style="float:left;width:50%">

- 压力板的功用
- F3键获取当前鼠标坐标
- broadcast和registerBroadcastEvent函数
- 在代码里进行数学运算
- %运算操作符

</div>
<div style="float:left;width:50%">

- 什么是变量
- say, registerClickEvent函数 
- ask函数获取用户输入
- get函数, set函数
- answer全局变量
- turnTo， walkForward， moveTo等函数

</div>
<div style="clear:both" />

**2. 实践**

**步骤1： 制作简单密码锁**

```javascript
registerClickEvent(function()
    ask("密码是多少?")
    
    if(get("answer") == "1234") then
        say("答对了!")
        moveTo(19244, 5, 19136)
        walkForward(0.2, 0.5)
        wait(5)
        restart()
    else
        say("答错了!", 2)
    end    
end)
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33109/raw#1700647374149image.png
  ext: png
  filename: 1700647374149image.png
  size: 28242
  isNew: true
  isExpand: true
          
```
**步骤2： 双重机关与事件**

<div style="float:left;width:50%">

钥匙1：key1为当前钥匙的角度

```javascript
set("key1", 0)

registerClickEvent(function()
    for i=0, 90, 5 do
        turnTo(key1+i)
        wait(0.02)
    end
    set("key1",  (key1 + 90) % 360)
    broadcast("keyRotated")
end)
```

</div>
<div style="float:left;padding-left:10px;width:50%">

钥匙2：key2为当前钥匙的角度

```javascript
set("key2", 0)

registerClickEvent(function()
    for i=0, 90, 5 do
        turnTo(key2+i)
        wait(0.02)
    end
    set("key2", (key2 + 90) % 360)
    broadcast("keyRotated")
end)
```

</div>
<div style="clear:both" />
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33107/raw#1700647229194image.png
  ext: png
  filename: 1700647229194image.png
  size: 323971
  isNew: true
  isExpand: true
          
```
看门人：当2个钥匙在特定角度时，开门

```javascript
moveTo(19247,5,19147)
registerBroadcastEvent("keyRotated", function()
    if(key1==180 and key2==90) then
        walkForward(3, 2)
    else
        moveTo(19247,5,19147)
    end
end)
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33108/raw#1700647312415image.png
  ext: png
  filename: 1700647312415image.png
  size: 29204
  isNew: true
  isExpand: true
          
```