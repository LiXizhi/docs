# Paracraft电影方块 v1.0

**软件用途：** Paracraft电影方块被应用在Paracraft 3D动画与编程工具软件中。它提供一种自由编辑模型动作，根据时间帧制作电影动作的功能。用户可以通过电影方块制作任意可想象的动画和电影出来，而且可以和代码协作进行动作控制。 
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** NPL语言, C++
**开发完成时间：** 2018年6月1日
**发表日期：** 2018年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 自定义电影人物模型
- 可自由控制的镜头
- 时间序列关键帧管理
- 动作自动补间
- 音效和字幕支持
- 可编程控制

**源代码**: 10万 [点击这里查看](Paracraft电影方块_code)

## 《Paracraft电影方块》使用手册

## 1.2 虚拟人物与虚拟人物的运动
虚拟人物怎么运动？本项目分类是一些和动画与角色运动相关的项目。用方块创造的虚拟人物与真实的人物具有一定的相似性。你将体验下列内容：

- 运动需要关节，关节越多，人物越复杂逼真。真人有360多个关节，我们的虚拟人物通常只有少量关节，比如8个，运动起来已经像模像样了。
- 每个关节都有自己的三维坐标，在场景中运动，还需要场景地面的三维坐标以及周围环境的三维坐标。这么多的坐标，随虚拟人物的运动、随时间都在变化，所以涉及极其复杂的坐标变换（要知道普通工业机器人只有6个关节，工作环境比虚拟人物所处的环境简单很多很多）。所以要描述虚拟人物的运动、编辑、存储、复现其运动是极其复杂和困难的世界性难题。目前人类只能通过“示教”来代替编辑。16个关节以上的机器人控制至今还没有人尝试并成功过，而我们在Paracraft中创造出的虚拟机器人可以有几十个关节。可以看出，你已经达到世界水平了。
- 相似原理可以描述多维虚拟人物的运动，而且它的基本步骤比较简单。
- 设计创造虚拟人物的运动、编辑、存储、复现其运动，你都可以在Paracraft中做到。

 

## 演员和动画

**1. 理论**

今天，我们来看一个简短的动画，名为 `Heart and Hands 致匠心`。看完后，我们会阅读它的源代码。这部动画片由一位年迈的、非常受欢迎的中国词曲作家李宗盛做旁白。这也是我们的用户在2015年用Paracraft制作的第一个基于骨骼的动画。 


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3451/raw#致匠心.mp4
  ext: mp4
  filename: 致匠心.mp4
  size: 53117592
          
```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3707/raw#电影方块字幕.mp4
  ext: mp4
  filename: 电影方块字幕.mp4
  size: 116812115
          
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3708/raw#创意空间电影方块动画.mp4
  ext: mp4
  filename: 创意空间电影方块动画.mp4
  size: 50286708
          
```

 
**2. 实践**

- 学习在电影方块中添加演员。
- 学习扮演和录制演员的动作。
- 学习为演员制作关键帧动画。

<div style="float:right;margin-left:10px;width:230px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2647/raw#image.png)
  
</div>

 
**步骤1：创建一个新的电影方块并添加演员。 如果你的电脑速度较慢，请输入`/shader 2` 命令，在播放时使用较低的图像设置。**

- 现在，让我们创建一个新的电影方块，然后右键单击它来编辑。
- 接下来，我们将在电影方块中添加几个默认的角色，并对它们进行编辑。我们将在以后的课程中学习如何创建自定义角色。本节，我们将使用默认的`方块人`角色。
- 左键单击`添加演员` 按钮，它是电影片段窗口中的第一个按钮(下图)，或者点击一个空槽并选择演员（如右图）。我们将看到一个默认演员出现在电影方块的顶部，代表这个新演员的物品也出现在电影片段窗口中。
- 像摄影机物品一样，你可以随时点击演员来切换到它的视角并扮演它。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2646/raw#16.png'
  ext: png
  filename: 16.png
  size: '154889'
  percent: '70'
  alignment: left
  unit: px
  width: 650

```

**步骤2：使演员动起来有两种方式。一种是通过`角色扮演`，另一种是通过`关键帧`，就像你已经用过的摄影机一样。角色扮演很简单，但高级用户总是使用关键帧。让我们先试试角色扮演。**
- 设置时间为0。并将演员移到起始位置。你的演员在默认情况下是`锁定`的，你需要按下`L`键来解锁，以便角色扮演。
- 现在按`R`键，或者点击`角色扮演`按钮。整个时间线变红了。你可以用W、A、S、D、空格、shift等键来移动你的演员。系统会自动记录你的所有关键帧，直到时间轴结束，或者你再次按下`R`键停止。如果你对你的录制不满意，回到时间起点，移动人物，然后按`R`键再次录制。一旦开始录制，系统将删除这个演员之前录制的所有关键帧。

- 接下来，尝试创建另一个角色，并通过`角色扮演`来录制它的行为。当你扮演角色时，你会看到之前的演员和摄影机也跟着你一起运动，是不是越来越像真实的电影拍摄？只不过你一次只能扮演一个 `角色`，通过不停的回到过去，添加新的角色。

**步骤3：接下来，我们将学习一个更高级和专业的方法来操控演员，叫做关键帧动画。**

- 首先，我们需要`锁定`我们想要操作的演员。`锁定模式`是您第一次打开一个电影块时的默认模式。在锁定模式下，你不能直接扮演角色，相反，演员只能通过时间轴上的关键帧在运动。所以先确保当前演员为锁定模式。
- 接下来，您可以删除旧的角色并创建一个新的角色。要删除一个演员，按住`shift`键不要松手，然后在电影片段窗口中左键点击它的图标。或者你只需要左键点击那个演员图标，然后再左键点击窗口之外的3D世界就可以把它扔掉。在Paracraft中，所有的图标物品的操作方式都差不多， 后面我们还会学习如何在不同的方块中复制和移动这些图标物品。
- 和摄影机物品一样，一个演员也有很多`子键`（sub key），可以在他们各自的时间轴上独立编辑。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2649/raw#19.png'
  ext: png
  filename: 19.png
  size: '108564'
  alignment: left
  percent: '60'
  unit: px
  width: 500

```


- 现在我们点击时间轴左下角的蓝色按钮来选择`骨骼`子键。你也可以按两次`1`来选择它。
- 当你处于骨骼模式时，你将看到演员所有的骨骼，你可以操作演员的身体上的骨骼来添加骨骼的关键帧。
- 你可以滚动你的`鼠标滚轮`按钮，来拉近视角，而`W,A,S,D`键可以帮助你移动到一个更好的视角。
- 选择手部骨骼，并拖动三个箭头中的一个可以移动手的位置。
- 然后拖动底部时间，来到不同的时间。然后再对手的位置做一些修改。
- 返回时间起点，并点击`P`键播放，你将看到在你刚刚设置的两个关键帧上手在平滑地移动。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2650/raw#20.png'
  ext: png
  filename: 20.png
  size: '229575'
  unit: px
  percent: '60'
  alignment: left
  width: 550

```


- 请注意，手和脚是4个特殊的骨骼，显示为`浅蓝色`的点。浅蓝色的点意味着你可以直接改变它的位置。它会自动生成两个父骨骼的关键帧，前臂(肘部)和上臂，因为手的位置变化其实是由旋转肘部和上臂的骨骼完成的。这种计算被称为反向运动学或Inverse kinematics（IK）。所有其他的骨头都只是普通的骨头，显示为`绿点`。
- 现在点击演员肘部的绿点。你会看到三个半圆出现了。拖动它们来旋转前臂。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2651/raw#21.png'
  ext: png
  filename: 21.png
  size: '225150'
  unit: px
  alignment: left
  percent: '60'
  width: 550

```

- 现在你可以用上臂骨骼做同样的事情。所有的骨骼都有`父子关系`。手骨的父骨骼是前臂，前臂的父骨骼是上臂。旋转父骨骼将影响所有的子骨骼。你可以按`- `和` + `键来选择一个骨骼的父骨骼或最近的子骨骼。最上级的骨骼没有父骨骼，被称为主骨骼或叫根骨骼，每个演员身上都有一个主骨骼。
- 现在你可以尝试用调整IK手骨的位置或旋转上臂和前臂来做一些上肢晃动的动作。
- 除了旋转，我们还可以位移或缩放骨骼。选择一根骨头，按`2`进入位移模式，`3`旋转模式，`4`缩放模式。你可以试试看。 但是最常用的是旋转模式，也是默认模式。 

**步骤4：最后，我们将学习改变演员的位置和方向。**
- 选择`位置`子属性，然后用鼠标中键点击场景中的某个地方将演员瞬移过去。或者你可以拖动三个坐标轴来移动演员。您可以使用位置属性创建多个关键帧，让你的角色在场景中移动。

<div style="float:left;margin-left:0px;width:500px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2652/raw#image.png)
  
</div>

<div style="float:left;margin-left:5px;width:500px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2653/raw#image.png)
  
</div>
<div style="clear:both" />


- 现在，在时间轴上尝试用多个关键帧来控制`角色的朝向`。热键是3。如果你再按3，它会切换到3轴旋转模式，这让你可以绕着这三个轴旋转。在大多数情况下，默认的单轴旋转就足够了。


- 现在按`1`或选择`动作`子属性。动作是一个数字Id， 每个Id对应了角色的预定义动画序列。例如，id:0表示站立动画，id:4表示行走，id:5表示跑。您可以在动作时间轴上指定两个关键帧之间的预定义动画。骨骼动画会叠加到预定义动作之上。


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2654/raw#24.png'
  ext: png
  filename: 24.png
  size: '203999'
  alignment: left
  percent: '60'
  unit: px
  width: 450

```

- 若要修改关键帧，请单击时间轴上的关键帧并选择`编辑…`

<div style="float:left;margin-left:10px;width:450px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2655/raw#image.png)
  
</div> 
<div style="clear:both" />


 
## 电影方块

**1. 理论**
电影方块是Paracraft的核心功能：你可以用它制作从简单到复杂的3D角色动画。在电影方块中，你可以通过先后扮演导演，摄影师，演员来制作一个电影片段。 

**2.实践**
- 了解电影方块
- 学习在时间轴上为摄影机添加关键帧
- 学习添加电影字幕
- 学习连接电影方块，制作长动画

在Paracraft中，`有些特殊的方块可以包含其他物品`，比如可以存放物品的箱子方块。电影方块也是一种容器方块。它的内部可以包含摄影机、演员、字幕、音乐、命令，甚至还可以包含其他的电影方块，等等。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3706/raw#11. 电影方块教学7.mp4
  ext: mp4
  filename: 11. 电影方块教学7.mp4
  size: 981243668
          
```

电影方块在 `E` 键工具栏的 `电影` 类别里。在场景中 `右键单击` 可以将一个电影方块放置到场景中，然后再 `右键单击` 已放置好的电影方块，就可以编辑它里面的内容了。
- 电影方块：`E` 键 -> `电影` -> 电影方块 (id:228) -> `右键单击` 电影方块进行编辑

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2623/raw#9.png'
  ext: png
  filename: 9.png
  size: '235758'
  unit: px
  alignment: left
  percent: '70'
  width: 500

```

`右键单击` 电影方块，进入编辑界面：
- 可以看到右下角有一个 `电影片段` 窗口，里面有电影方块中的各种物品。你可以通过拖动来移动它。
- 在屏幕的底部，你会看到一个 `蓝色时间轴`。你可以在上面拖动 `长灰色按钮` 来改变当前的时间。`长灰色按钮` 上的数字为 `当前时间/总时间`，单位为毫秒（1秒=1000毫秒）。
- 在时间轴的右边，你会看到一个数字，它代表时间轴的结束时间，即电影方块时长，单位是 `秒`。默认情况下，电影方块时长是30秒，你可以把它改为10秒。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2624/raw#10.png'
  ext: png
  filename: 10.png
  size: '147393'
  alignment: left
  percent: '80'
  unit: px
  width: 500

```


**步骤1：在 `电影片段` 窗口中：**
- `左键单击` 第一行第一个 ` + ` 号按钮可以添加演员。
- `左键/右键单击` 第一行第二个 `主角` 按钮都可以将视角切换到主角人物的视角，也就是我们在场景中控制的小人。切换成功后，`主角` 按钮背影呈橙色。此时我们就像电影导演一样，通过控制主角人物的移动，来观察演员和灰色摄影机的位置。
- `右键单击` 第二行第一个 `摄影机` 按钮可以切换到摄影机视角。摄影机是电影方块中的默认物品。此时我们就像摄影师一样，同样可以通过 `W A S D` 键来控制摄影机的移动，通过拖动 `鼠标右键` 和 `Ctrl+鼠标滚轮` 来调整和缩放摄影机的视角。摄影机默认处于飞行模式，无需按 `F` 键，直接按 `空格` 键上升，`X` 键下降。


 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2625/raw#11.png'
  ext: png
  filename: 11.png
  size: '151602'
  percent: '80'
  alignment: left
  unit: px
  width: 500

```

- 现在，我们将 `长灰色按钮` 拖动至时间轴的开头，即当前时间为0秒。

> 这里，我们要引入一个重要的概念，叫做 `关键帧` (Key Frame)。如果我们想让摄影机沿着一定的轨迹移动，那么这条轨迹的起点和终点就是 `关键帧`。换句话说，摄影机总是在两个 `关键帧` 之间移动的。我们调整好摄影机起点和终点的位置角度，`左键单击` 电影片段窗口下方的 `钥匙` 按钮，在时间轴上分别添加两个 `关键帧`，快捷键是 `K` 键。然后摄影机会在两个 `关键帧` 之间自动匀速平滑地移动。

- 我们在0秒处，先通过 `W A S D` 等键将摄影机移动到我们想要的起点位置，然后按 `K` 键添加一个关键帧。我们会听到一个声音，同时在时间轴上出现一个新的灰色标记。这个标记就是我们刚刚添加的关键帧，它记录了摄影机起点的位置角度等信息。
- 接下来，我们将 `长灰色按钮` 拖动至5秒处左右（5000毫秒），即摄影机从起点到终点所经历的时间为5秒。时间间距越长，摄影机运动得越慢。
- 然后，我们将摄影机移动到我们想要的终点位置，`左键单击` `钥匙` 按钮或者按 `K` 键，就在时间轴上添加了终点的关键帧。
   - 注意，一定要先拖动时间轴，设置好时间间距，再移动摄影机来添加关键帧。
- 点击电影片段窗口左下角的左箭头 `到开始` 按钮，让 `长灰色按钮` 回到0秒处。
- 点击旁边的三角形 `播放` 按钮，快捷键是 `P` 键。播放时会看到，摄影机在起点和终点两个关键帧之间匀速平滑地移动。
- 你也可以通过来回拖动 `长灰色按钮` 来反复查看摄影机的路径轨迹。
- 我们重复上面的步骤，来添加第三个关键帧。我们将 `长灰色按钮` 拖动至10秒处。然后将摄影机移动到我们想要的下一个终点的位置，按 `K` 键添加关键帧。然后我们将 `长灰色按钮` 拖回至5秒处，点击 `播放` 按钮，就可以看到摄影机在5至10秒之间的运动了。
- 我们再点击 `到开始` 按钮，点击 `播放` 按钮，就可以看到摄影机从0至10秒的完整运动了。
- 如果我们想让摄影机运动得更快或更慢，则需要调整关键帧之间的时间间距。我们可以 `左键单击` 第二个关键帧，会看到它变成红色，然后移动鼠标可以在时间轴上移动这个关键帧，`左键再次单击`确认或`右键点击`取消。
- 点击`主角按钮`切换回主玩家视角（导演视角）。如果你现在点击`播放`按钮，你会看到摄影机在场景中按照我们设置的关键帧运动起来。

**现在我们将学习如何添加字幕。**
- 选择主角或摄影机。每个电影方块中的物品都包含许多可添加关键帧动画的`子键`或`子属性`。字幕是摄影机的子键。就仿佛身高和年龄是我们人类的子属性，这些属性会随时间变化。
- 点击左下角的蓝色按钮，选择`文字`子属性，此时时间轴上会显示这个属性的所有关键帧。实际上，`文字`是默认选中的子属性。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2626/raw#12.png'
  ext: png
  filename: 12.png
  size: '167204'
  percent: '80'
  alignment: left
  unit: px
  width: 500

```

- 点击右下角的`+`键在时间轴上来设置一个新的关键帧。实际上，底部有两个时间轴，上面的白色时间轴显示的是当前选择的子属性的所有关键帧；下面的黑色时间轴，我们刚刚使用的，总是用于显示摄像机位置和方向的关键帧。
- 在为字幕文本添加多个关键帧后，可以右键单击关键帧标记来重新编辑它的内容。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2627/raw#13.png'
  ext: png
  filename: 13.png
  size: '146303'
  alignment: left
  percent: '80'
  unit: px
  width: 500

```


**最后，我们将学习如何连接多个电影块，以便他们可以按顺序播放。**
- `E` 键 -> `电影` -> 选择 `按钮`, `中继器` 和 `导线`。他们是链接多个电影方块的重要工具。
- 尝试创建它们，如下图所示，连接两个电影方块。
  - 记住：中继器是有方向的，当你创建它时，它将始终朝向你当前角色的视角，所以在你将中继器放置在3D场景之前，要转动主角视角。Paracraft中很多有方向的方块，都采用这种原则，你需要反复练习熟练掌握这个技巧。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2628/raw#14.png'
  ext: png
  filename: 14.png
  size: '242967'
  alignment: left
  percent: '70'
  unit: px
  width: 450

```

这里，我们不会深入讲解中继器是如何工作的。只做简要说明：
- 该按钮(id:105)给了一个`输入`的信号，该信号传入左边电影方块，将它激活（播放）。
- 当电影方块停止播放时，它会发出另一个信号，只有中继器才能捕捉到。中继器(id:197)沿箭头方向传递该信号。
- 导线会把信号传递到右边的电影方块和一个电灯方块。
- 如果你点击按钮，你会看到左边的电影方块先播放，然后灯被点亮，同时右边的第二个电影方块开始播放。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2629/raw#15.png'
  ext: png
  filename: 15.png
  size: '355545'
  alignment: left
  percent: '80'
  unit: px
  width: 500

```