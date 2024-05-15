 

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
