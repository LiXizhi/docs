# 基于粒子的3D建模


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8265/raw#方块建模h264.mp4
  ext: mp4
  filename: sunclock.mp4
  size: 11528698
          
```


#### 场景搭建
Paracraft内置上百种不同材质的方块，通过按键E，可以打开建造背包，利用各式方块打造属于自己的3D世界。
在我们搭建场景时，配合各种复合快捷键，可以实现批量搭建，熟悉运用后可以使我们的搭建速度变的更高效快速。
注：按E键打开界面右侧菜单栏，在建造栏项下左键单击，选择方块，然后在场景里就可以开始建造了。
在菜单栏中，一般的建造方块分别在建造栏和装饰栏项下，如需搭建Bmax模型，可在电影栏项下找到彩色方块进行搭建。


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6577/raw#山川.jpg'
  ext: jpg
  filename: 山川.jpg
  size: '429410'
  unit: '%'
  percent: '60'
  alignment: left

```


#### Template模板
Template记录了方块的全部信息，包括电影方块内部的演员。可以通过/loadtemplate等命令复制模板到场景中，实现跨世界完美复制所需的场景方块、电影方块等。
具体操作方式：将选中的方块保存为 template模板（全局模板文件可以在多个世界中共享）加载模板文件：E 键 -->模板标签-->全局模板

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8333/raw#1574750543860image.png
  ext: png
  filename: 1574750543860image.png
  size: '436502'
  unit: '%'
  percent: '60'
  alignment: left

```


#### 快捷命令
内置大量针对方块的命令，只需要一行简单的命令，就可以让计算机自动实现复杂的功能。
按回车键打开输入聊天框，输入各种命令，快速实现我们想要的效果。
通过输入指定的命令，我们可以批量编辑，快速搭建一些指定的形状，甚至是改变天气和时间，添加背景音乐等。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8334/raw#1574750596467image.png
  ext: png
  filename: 1574750596467image.png
  size: '292250'
  unit: '%'
  percent: '60'
  alignment: left

```


#### Bmax系统
这是一个可以为模型添加动画效果的强大系统！
我们将标准方块搭建后所导出的模型文件叫做Bmax文件，Bmax是 Block Max/Block Model 的简称，它能帮助我们创建各种精致的静动态的自定义模型方块。
在我们的电影动画中，有许多演员和道具都是由Bmax模型文件创建的。
Bmax模型又分为静态模型和动态模型，静态模型一般用于一些小道具，如椅子、铅笔等。
赋予了骨骼的模型也称为动态模型，如小动物和原创人物，直升飞机和汽车等，绑好骨骼的方块搭建保存成Bmax模型文件后导出，Bmax模型就可以在电影中动起来了。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8335/raw#1574750633228image.png
  ext: png
  filename: 1574750633228image.png
  size: '399961'
  unit: '%'
  percent: '60'
  alignment: left

```


Paracraft中的一切可视化的编辑工具都是物品，点击物品栏中的物品，你可以在上百种编辑工具间自由切换。
Paracraft定义了多种全局模式，例如编辑模式和浏览模式，每个物品在不同的模式下有不同的输入输出行为。
例如大多数物品的编辑UI和快捷键只在编辑模式下可用。你可以随时在多种模式间动态切换(Ctrl+G)。
几乎每个物品的所有的UI操作都可以通过命令来完成。
几乎所有的命令都支持无限次数的撤消(Ctrl+Z)与反撤消(Ctrl+Y)。
通过安装插件或使用内部命令可以定义新的物品。


 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6584/raw#批量旋转等.png'
  ext: png
  filename: 批量旋转等.png
  size: '947034'
  unit: '%'
  percent: '60'
  alignment: left

```


#### 延伸补充
**机关类物品**
命令方块：触发后可执行任意命令序列， 内部可包含其他物品。
触发器与连接器：按钮，开关，含羞草，含羞石，压力板，导线，中继器，红石火把，向上导体，红石灯，出生点，音符，唱片机等等。
铁轨与矿车：铁轨，探测铁轨，红石铁轨，矿车，传送石等。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6578/raw#机关.jpg'
  ext: jpg
  filename: 机关.jpg
  size: '677702'
  unit: '%'
  percent: '60'
  alignment: left

```


**装饰类物品**
灯光，楼梯，藤蔓，玻璃，窗户，门， 告示牌，相册，围栏，地毯, 蜘蛛网，斜面等等。
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6579/raw#装饰.jpg'
  ext: jpg
  filename: 装饰.jpg
  size: '257530'
  unit: '%'
  percent: '60'
  alignment: left

```

**工具类物品**
代码书， 命令书：可输入NPL代码或命令。
地形笔刷工具: 可快速创建山脉和海洋。
画笔工具：可快速大范围替换方块，或铺设植被。
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6580/raw#工具栏.jpg'
  ext: jpg
  filename: 工具栏.jpg
  size: '18497'
  unit: '%'
  percent: 20
  alignment: left

```