
<style>
  .markdown-body hr {
    height: 1px;
  }
</style>





```@Lesson
styleID: 0
lesson:
  animations: []

```


# **一、	教学目标：**
1.知识目标：
- 如何创造自定义模型并保存为BMax文件；
- 学习在世界中使用BMax模型；
- BMax模型的普通模型与物理模型的区别。

2.实践操作目标
- 创建BMax模型
- 能够将合适的BMax模型放置在合适的位置。

3.思维与价值观目标
- 培养学生的对比分析思维与空间规划能力；
- 提升学生的动脑思考已动手操作能力。

# **二、	教学重难点：**
### 教学重点：
* 创建BMax模型
* BMax模型在场景中的使用
* 物理模型与普通模型的认识对比

### 教学难点：

* Bmax模型在场景中的使用；
* 两种BMax模型——物理模型与普通模型的认识与对比。


# **三、	教学准备：**
* 课件
* 带鼠标、键盘的电脑
* 上课学员的账号、密码
* 顺畅的网络环境


# **四、	教学过程：**
### **1.	情景引入（5‘）：**
今天，我们去来看一个简短的动画 《`The Great Inventor》伟大的发明家`。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3452/raw#101. 伟大的发明家 201710.mp4
  ext: mp4
  filename: 101. 伟大的发明家 201710.mp4
  size: 92733365
          
```


你能够用自己的话将动画的意思简单地描述一下吗？
示例：动画主要简单记录了发明家设计与建造轮船的过程。
想一想：视频中出现的哪些，是我们已经学习过的知识呢？
示例：相册的知识已学……


### **2.	知识点解析（55’）**
* 平面与立体（2D与3D）
在paracraft的3D编程平台，我们能够制作富有立体感的三维模型与场景。什么是2D与3D呢？
在一个平面上的内容为二维，坐标为X  Y，有四个方向（左、右、前、后）
三维富有立体感，三维是坐标轴的三个轴，即x轴、y轴、z轴，其中x表示左右空间，y表示前后空间，z表示上下空间。需要注意的是：前后，左右，上下都只是相对于观察的视点来说。没有绝对的前后，左右，上下。

 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/19039/raw#1605859941409image.png
  ext: png
  filename: 1605859941409image.png
  size: 107167
          
```






## 2.1 什么是BMax模型

BMax 是 `block max / block model` 的简称，意思是`方块模型`。它能帮助我们用方块创建出更精致的静态或动画模型。

其实在我们课前看过的动画中，有很多对象是用BMax模型创建的。比如下图中用方框划出来的模型，都是BMax模型。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4105/raw#image.png'
  ext: png
  filename: image.png
  size: '540396'
  unit: '%'
  percent: 80

```

要想让自己的Paracraft世界更丰富，BMax模型是必不可少的。让我们一起来学习吧！

## 2.2 创造BMax模型



创造BMax的过程是非常简单的。我们只需要：
1. 用方块搭建出我们想要的模型形状
2. 将所有方块保存为BMax文件


让我们来试一下，搭建一把椅子。


#### 首先，输入账号密码，登录账号：
 
* 登录账户》点击更新》使用远程版本》打开场景
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4950/raw#登录和载入.gif'
  ext: gif
  filename: 登录和载入.gif
  size: '282875'
  unit: '%'
  percent: 60

```



1. 进入编辑模式（第一节的内容，还记得吗？）
2. 打开工具栏，选择 建造->电影->颜色方块。使用颜色方块，我们可以准确的控制模型所有地方的颜色。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4106/raw#image.png'
  ext: png
  filename: image.png
  size: '260933'
  unit: '%'
  percent: 60

```

3. 发挥想象，使用方块搭建一把椅子吧~任何形状的椅子都可以

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4107/raw#image.png'
  ext: png
  filename: image.png
  size: '597347'
  unit: '%'
  percent: 80

```

4. 选择椅子的所有方块。可以使用 `Ctrl+鼠标左键` 点击椅子的四角；或者使用 `Ctrl+鼠标左键` 选择椅子最下方的一个方块，再按 `Ctrl+A` 选中所有椅子方块。


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4108/raw#select-blocks.mp4'
  ext: mp4
  filename: select-blocks.mp4
  size: '961965'
  unit: '%'
  percent: 80

```


5. 在属性窗口中单击`保存`按钮，会弹出一个导出对话框，选择`另存为bmax模型`。输入名称（如：chair，建议使用英文/拼音），点击`确定`按钮。你会看到，在底部快捷导航栏，出现一个模型项目。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4109/raw#image.png'
  ext: png
  filename: image.png
  size: '676012'
  unit: '%'
  percent: 80

```


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4110/raw#image.png'
  ext: png
  filename: image.png
  size: '573769'
  unit: '%'
  percent: 80

```



```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4111/raw#image.png'
  ext: png
  filename: image.png
  size: '605595'
  unit: '%'
  percent: 80

```



```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4112/raw#image.png'
  ext: png
  filename: image.png
  size: '683498'
  unit: '%'
  percent: 80

```


## 2.3 在世界中使用BMax模型

接下来，我们就可以在场景中使用椅子模型了。

1. 先选择模型。使用模型方块，允许你将许多基于文件的对象作为标准块放入3d世界 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4206/raw#image.png'
  ext: png
  filename: image.png
  size: '505635'
  unit: '%'
  percent: 80

```

2. 选择我们之前创建的椅子文件
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4207/raw#image.png'
  ext: png
  filename: image.png
  size: '357006'
  unit: '%'
  percent: 80

```

3. 在地面使用`鼠标右键`可以放置模型
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4208/raw#image.png'
  ext: png
  filename: image.png
  size: '507000'
  unit: '%'
  percent: 80

```

4. 对椅子模型进行编辑，我们可以点击下方白色窗口中的模型创造按钮，切换到模型编辑模式。也可以直接右键单击椅子模型，切换到编辑模式。然后我们可以拖动红绿蓝箭头，来调整椅子的位置，也可以拖动方箭头，来调整椅子的大小，还可以拖动蓝色圆环，来调整椅子的转向。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4209/raw#image.png'
  ext: png
  filename: image.png
  size: '516013'
  unit: '%'
  percent: 80

```


## 2.4 带物理属性的BMax模型

在上一步中创建的模型是没有物理碰撞的，什么意思呢？
因为模型也是一个方块，所以不管它放大多少倍，它始终占据一个方块的空间。比如下面的视频：


```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/4210/raw#bmax-without-physics.mp4
  ext: mp4
  filename: bmax-without-physics.mp4
  size: '5040086'
  unit: '%'
  percent: 80

```

当然，我们也可以使用 BMax 文件创建有物理碰撞的模型，这就要用到另外一个方块，物理模型方块。

1. 选择使用物理模型方块
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4213/raw#image.png'
  ext: png
  filename: image.png
  size: '546684'
  unit: '%'
  percent: 80

```

2. 同样的过程，选择椅子的 BMax 文件
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4214/raw#image.png'
  ext: png
  filename: image.png
  size: '435163'
  unit: '%'
  percent: 80

```

3. 创建椅子，并放大椅子
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4215/raw#image.png'
  ext: png
  filename: image.png
  size: '540459'
  unit: '%'
  percent: 80

```


这时候，我们创建的模型是有物理碰撞的，就像下面的视频里一样：



```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4217/raw#bmax-with-physics.mp4'
  ext: mp4
  filename: bmax-with-physics.mp4
  size: '1380866'
  unit: '%'
  percent: 80

```


## 2.5 BMax模型的删除

由于BMax仅仅占据一个方格的位置，较难选中。因此，当BMax模型错误地在场景中放置，需要删除，我们可以尝试在其周围搭建一般方块，然后Ctrl+左键选中BMax模型四周的方块，接着点击界面右边属性框中的全选，最后再点击删除。即可删除被错误放置的BMax模型啦！

### **3.实操演练与拓展（25‘）**

找到空地，利用方块搭建常见的物品并保存为Bmax模型。



- 在Paracraft里创建动画，Bmax模型是一个很重要的概念，大家要多尝试
- 现在，请大家试着将Bmax模型再导回到场景中吧！


### **4.保存并上传你的世界（10‘）**
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4833/raw#image.png'
  ext: png
  filename: image.png
  size: '144911'
  unit: '%'
  percent: 60

```

 





### **5.	总结分享（4‘）**
#### 1. 今天我们观看了哪部短视频呢？
#### 2. 如何将你的模型保存为Bmax模型呢？
#### 3. 如何放置Bmax模型到场景中？
#### 4. 给大家介绍一下自己作品的名字和想法吧。



### 课后任务
请课后回家与家人一同观看《The Great Inventor—伟大的发明家》短片，向他们分享关于BMax的秘密吧！并为家人制作一个专属BMax模型吧！


 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/19168/raw#1606726505064image.png
  ext: png
  filename: 1606726505064image.png
  size: 467587
          
```