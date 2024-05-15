# 《Paracraft机器人设计平台》基础教程

https://keepwork.com/lixizhi/note/2020/ai_edu_milestone


## 基本设计流程介绍

 
### 制作CAD模型
在世界中打开CAD模块，按快捷键E，点选建造—代码—左键选中下方CAD模块。 点选之后可以看见人物手中持有CAD模块模型。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10845/raw#1584425097306image.png
  ext: png
  filename: 1584425097306image.png
  size: 322193
          
```


 关闭建造栏，在空地右键点击。建造CAD模块。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10847/raw#1584425233103image.png
  ext: png
  filename: 1584425233103image.png
  size: 367476
          
```

点选CAD模块。弹出对话框。选择上方图块，左键点击。第一次加载可能需要等待。点开CAD模块时旁边会自动生成电影模块，电影模块主要用户显示模型，并且在之后制作动画时需要。默认生成即可。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10850/raw#1584425359283image.png
  ext: png
  filename: 1584425359283image.png
  size: 262705
          
```

 使用界面（图形）中的各种立方体搭建机器人模型。图形中包含的各种立方体是最基本的设计素材，每个立方体都有不同参数可以设置大小半径等。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10859/raw#1584432485489创建.mp4
  ext: mp4
  filename: 1584432485489创建.mp4
  size: 28422664
          
```
 
 
### 骨骼绑定
 
用界面（骨骼根节点）将不同立方体分配不同骨骼。骨骼根节点是骨骼的集合，每个骨骼可以包含一个或多个立方体。骨骼根节点中至少包含一个骨骼。一个骨骼根节点中可以包含多付骨骼。但是骨骼根节点只有一个。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10865/raw#1584438062271绑定.mp4
  ext: mp4
  filename: 1584438062271绑定.mp4
  size: 62243286
          
```

 
 
### 将骨骼绑定到舵机
部分骨骼对应了舵机。可以使用动画项中的`设置舵机属性`来做骨骼到舵机的绑定和舵机参数设置。
- 使用舵机前要测试校正舵机再安装。可以先制作简单测试方块测试舵机性能。
- 不同舵机有不同的角度限制，在这里我们用角度范围为180的舵机为例。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10873/raw#1584508512276舵机测试.mp4
  ext: mp4
  filename: 1584508512276舵机测试.mp4
  size: 4478072
          
```

### 制作动画
 
使用Paracraft电影方块制作关键帧动画。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10877/raw#1584511463071动画.mp4
  ext: mp4
  filename: 1584511463071动画.mp4
  size: 19853846
          
```

动画制作完成后打开建造，点选机器人模块放置在世界中

 
## AI编程：基于动画的编程 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10882/raw#1584511692266image.png
  ext: png
  filename: 1584511692266image.png
  size: 790850
          
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10881/raw#1584511653010image.png
  ext: png
  filename: 1584511653010image.png
  size: 614812
          
```
- 右键打开机器人模块，点击图块
- 创建动画片段
- 用代码控制动画的播放
  - 设置芯片按钮属性控制播放动画


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10883/raw#1584511844731image.png
  ext: png
  filename: 1584511844731image.png
  size: 549231
          
```

### 连接硬件
- 通过USB, 连接microbit芯片
- 通过USB, 连接扩展板, 给扩展版供电（扩展版需要单独供电）
- 点击部署按钮，稍等片刻，将动画数据与代码写入控制芯片（microbit主机）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10884/raw#1584511964515image.png
  ext: png
  filename: 1584511964515image.png
  size: 276413
          
```

- 根据约束骨骼属性中的设置，接入舵机。
- 组件: micro:bit主板， 扩展板，舵机x2
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10887/raw#1584513913387微信图片_20200318143359.jpg
  ext: jpg
  filename: 1584513913387微信图片_20200318143359.jpg
  size: 69428
          
```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10888/raw#1584514197211微信图片_20200318143355.jpg
  ext: jpg
  filename: 1584514197211微信图片_20200318143355.jpg
  size: 74713
          
```


- 连接舵机与主板：
  - 注意正反方向，舵机电源线和转接板方向对应。
  - 浅色线为信号，中间红线为正级，深色先为负级。
- 连接完成之后，点击机器人模块中的部署，待闪烁黄灯停止闪烁，常亮代表部署完成。
- 按下面板上的控制按钮播放动画。
 
### 制作完成 & 测试
重复上述的动画与编程的过程，直到制作出满意的作品
 
## Paracraft创意空间示例
  
- [例子：写字机器人](/official/docs/tutorials/robot_tutorial_writingmachine)
  - https://keepwork.com/pbl/project/7129/
  - [淘宝购买链接](https://detail.tmall.com/item.htm?spm=a230r.1.14.49.681e5617cjsJC5&id=602550522398&ns=1&abbucket=7)
- [例子：6轴机械臂](/official/docs/tutorials/robot_tutorial_6dof_arms)
  - https://keepwork.com/pbl/project/7592/
  - [淘宝购买链接](https://item.taobao.com/item.htm?spm=a230r.1.14.151.661358a0gHYXQg&id=570647607093&ns=1&abbucket=7#detail)
 
 
 
 

