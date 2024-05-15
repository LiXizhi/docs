## 宏示教使用教程
通过宏示教，用户可以根据AI角色的指引点击鼠标和键盘完成paracraft中的任意复杂的UI操作序列动作。仿佛有AI手把手教你使用制作动画或编写程序。请看下面演示案例。

```@Project
styleID: 1
project:
  projectId: '41716'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

教学视频：

1. 如何上AI私教课： [https://keepwork.com/official/tips/sx1/2_1](https://keepwork.com/official/tips/sx1/2_1)
2. 如何制作AI课件：https://keepwork.com/official/tips/sx1/2_2
3. Agent开发指南：https://keepwork.com/official/tips/sx1/2_3

## 方法1：高级宏示教智能模组
在资源库中搜索宏示教，可以直接添加宏示教智能模组

使用方法如下： https://keepwork.com/wyx9529/macro_use/index

## 方法2：Agent告示牌

找到`宏示教`Agent告示牌，并在场景中创建。
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20047/raw#1615276240682image.png
  ext: png
  filename: 1615276240682image.png
  size: '60195'
  unit: px
  width: '200'
  alignment: left

```

## 使用技巧

## 1.关于录制和测试
  * F9 快速录制
  * Shift+F9 在不清除场地的情况下快速录制 
  * F5 快速测试

## 2.注意事项
* 录制时，paracraft窗口不要全屏 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20046/raw#161527496136411.png
  ext: png
  filename: 161527496136411.png
  size: 1193499
          
```

 
* 在点击的时候，要尽量对准方块的中间
* 操作尽量集中在窗口的中间，不要太靠边
* 录制代码方块时不要用end、Del键，避免用小键盘
* cameraMove不能删，所有鼠标点击， 前都要设置这个， 否则点不准
* 尽量别用鼠标中键，因为Mac上没有中键

## 3.小技巧
  * 当一个案例需要分多个宏示教时：
  * 首先站在场地中间，然后将模型导出为template模版
  * 勾选“演员使用相对位置”、“使用自定义原点”
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20030/raw#1615257917784image.png
  ext: png
  filename: 1615257917784image.png
  size: '94725'
  unit: '%'
  percent: 40

```


  * 导出模版后在进行下一个宏录制时，可以使用shift+f9直接开始
  * 在粘贴宏指令时，将loadtemplate("ww")放在上方即可实现开始前先加载模型
  * 以上操作，可以在相对位置生成模版，这样无论复制到哪个场景，都不会出现坐标错误
  * text("ABC",5000)，后面的是显示时间，可加可不加。可以用text()来结束
  * 是按照名字排序的，所以在存Bmax时，自用的Bmax以Z开始，用户的以A开始，方便用户选择
  * 示教过程中，如有替换Bmax操作将不会有提示
  * 自动播放模式下无法激活声音
  * 如果希望一个语音必须播放完才启动后面的操作，可以使用Wait(1000) ，用Idle，那么语音可以一边播，一边启动后面的操作
  * Wait(100)和Idle(100,true)，都可以强行等待，区别是Wail会锁定操作，Idle不锁定
  * 一般来说，Idel、text、sound会加在操作的上面，每一段操作以空行隔出，方便查看和调整
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20031/raw#1615260706623image.png
  ext: png
  filename: 1615260706623image.png
  size: '31767'
  unit: '%'
  percent: 40

```

  * 在配置文件里，通过更改参数，可改变训练场的位置、半径大小和材质等，具体看图
  
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20036/raw#1615267088947image.png
  ext: png
  filename: 1615267088947image.png
  size: '5473'
  unit: '%'
  percent: 60

```
  * 修改配置文件时，可修改1号代码方块，2号成组的代码方块都不要去更改，一方面是如果改错会影响运行，另一方面，未来这组代码方块将会实现同步更新，避免修改内容被自动替换掉。
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20040/raw#1615269361840image.png
  ext: png
  filename: 1615269361840image.png
  size: '396510'
  unit: '%'
  percent: 50

```
  
  * 修改配置文件后，最下面这行代码，务必改为SetCurrentTask("myTask");
   
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20041/raw#1615269487189image.png
  ext: png
  filename: 1615269487189image.png
  size: '185506'
  unit: '%'
  percent: 50

```