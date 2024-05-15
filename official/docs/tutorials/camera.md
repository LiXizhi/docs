# 摄像头

我们可以在代码方块中使用`/capture`命令捕捉摄像头数据，也可以捕捉语音数据。 更多请看[capture命令参考](https://keepwork.com/official/paracraft/docs/cmd_capture)

## 视频捕捉

每次点击会发送一个消息。可以指定消息的名字， 如下。

```javascript
cmd("/capture video -event onCameraCaptured")

registerBroadcastEvent("onCameraCaptured", function(msg)
  say(format('<div style="background:url(%s);width:100px;height:100px;"></div>', msg.filename))
end)

```

可以指定窗口的大小和位置

`cmd("/capture video -x 10 -y 10 -width 300 -height 200 -event onCameraCaptured")`

关闭窗口`/capture none`

## 捕捉一张图片

和捕捉视频一样，点击就会捕捉一张图片, 并立即关闭， 也可以用ESC关闭。
捕捉单个图片无需注册事件，只需接受命令的返回值即可。 如下

```javascript
local filename = cmd("/capture image")
tip(filename)
say(format('<div style="background:url(%s);width:100px;height:100px;"></div>', filename))
```

我们也可以指定窗口位置和文件名。默认文件名在temp目录下，如果指定了文件名，默认为相对当前世界的路径。 文件名需要围绕jpg或png.

```javascript
local filename = cmd("/capture image -file test.jpg")
say(filename)
```

## 捕捉声音

你需要有麦克风，就可以捕捉声音了。 支持wav和ogg两种格式，默认频率16000，单声道。 同样默认文件名在temp目录下，如果指定了文件名，默认为相对当前世界的路径。

```javascript
local filename = cmd("/capture sound -file test.wav")
say(filename)
```

如果你希望马上开始捕捉声音， 并在3秒后自动结束，无需用户点击录音按钮， 可以用下面的命令。playSound可以用于播放任意声音文件。

```javascript
local filename = cmd("/capture sound -duration 3 -file test.ogg")
playSound(filename)
```

## 捕捉声音文字

捕捉文字相当于先捕捉语音，再转为中文或英文。 需要联网并登录，我们使用百度语音API做转化，免费和会员用户有不同的每日使用次数。

例子1： 自动录制3秒中文

```javascript
local text = cmd("/capture text -duration 3")
say(text)
```

例子2： 自动录制3秒英文，用playText阅读文字

```javascript
local text = cmd("/capture text -language en -duration 3")
playText(text)
```

我们也可以结合/ask命令制作一个语音聊天机器人。可以用`playText`朗读文字。

```javascript
local text = cmd("/ask", cmd("/capture text -duration 3")))
say(text)
playText(text)
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28878/raw#1690538205361image.png
  ext: png
  filename: 1690538205361image.png
  size: 338413
  isNew: true
          
```
## 物体识别

目前可以识别80种物品， 首次加载比较慢，运行过一次, 第二次就很快了， 因为第一次要下载tensorflow model到本地。目前用的是开源模型， 运算在本地。

开始识别

```javascript
cmd("/capture objectdetection start -event OnObjectDetection")
registerBroadcastEvent("OnObjectDetection", function(msg)
  say(commonlib.serialize_compact(msg))
end)
```

结束识别

```javascript
cmd("/capture objectdetection stop")
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28880/raw#1690538355577image.png
  ext: png
  filename: 1690538355577image.png
  size: 747708
  isNew: true
          
```



## 捕捉人物姿势
可以识别人物四肢和头部的运动。 驱动3D角色。 目前用的是开源模型， 运算在本地。 

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28879/raw#1690538260054image.png
  ext: png
  filename: 1690538260054image.png
  size: 80914
  isNew: true
          
```
开始识别

```javascript
cmd("/capture pose start -event OnPose")
registerBroadcastEvent("OnPose", function(msg)
  say(commonlib.serialize_compact(msg))
end)
```

结束识别

```javascript
cmd("/capture pose stop")
```

```@Project
styleID: 1
project:
  projectId: 1624471
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: false

```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30040/raw#1697159205331bipedpose.mp4
  ext: mp4
  filename: 1697159205331bipedpose.mp4
  size: 14153429
  isNew: true
  isExpand: true
          
```

## 捕捉手指运动

开始识别

```javascript
cmd("/capture handpose start -event OnHandPose")
registerBroadcastEvent("OnHandPose", function(msg)
  echo(commonlib.serialize_compact(msg))
end)
```

结束识别

```javascript
cmd("/capture none")
```

通过本地显卡上的深度学习算法先将摄影机图像实时转化为关键点，再将关键点实时映射到用BMAX搭建的骨骼模型上。
```@Project
styleID: 1
project:
  projectId: 1597302
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: false

```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29931/raw#1696316266051AI_handpose.mp4
  ext: mp4
  filename: 1696316266051AI_handpose.mp4
  size: 15474867
  isNew: true
  isExpand: true
          
```