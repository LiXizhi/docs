<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/macro`**

**quick ref:**
> /macro [record|play|stop] [-i|interactive]

**description:**

```
record user actions and then playback. 
@param i|interactive: we will automatically insert trigger macros
e.g.
/macro    toggle recording mode
/macro record -i
/macro record
/macro play
/macro stop
```

<!-- END_AUTOGEN-->

## 宏命令

宏是键和鼠标文本命令的序列，可以在命令块或通过调用`GameLogic.Macros:Play(text)`

## Paracraft中支持录制的功能
- 【所有基础+高级建造操作】：拉伸，镜像，选择，复制， 存BMAX，E菜单(支持鼠标中间)， 各种高级快捷键，鼠标拖动，坐标轴拖动等。
- 【文本框，UI】： `/` 命令行输入加回车, 文件搜索，新建物品，主菜单，F1新手指引（仅针对建模），等
- 【MCML v2】： 物理模型（含SRT编辑），相册，打开文件，打开美术资源文件，彩色方块，地形笔刷（暂时只能点击）， 等
- 【代码方块】：代码方块，命令方块，告示牌， /text字幕，代码方块内部的UI
- 【电影方块】：电影方块时间轴，关键帧（复制，位移，删除，右键等），骨骼，摄影机 等
- 【其它】：箱子，箱子与背包物品拖动, MessageBox, 加了自动播放模式， 考试模式

【已知问题】
- 摄影机播放和运动还有些不完美， 500ms间隔
- 不支持R扮演录制
- 其它非主流UI还没有支持。 



## 什么是好的宏？
宏几乎与屏幕分辨率无关。但是，最好的做法是单击场景块的中心，
并且不要单击场景的边缘，因为视口的宽高比在用户的计算机上可能会有所不同
并且点击位置可能看不到。始终在场景中心附近单击，以确保有效地单击所有纵横比上的鼠标。
另外，请删除多余的步骤，例如频繁移动播放器或更改相机视图，因为它们会产生不必要的
宏命令。

## 互动模式
可以通过 `/macro record -i`命令以交互方式记录宏。这将生成附加的XXX Trigger命令。
这些触发命令将忽略先前的Idle（wait）命令。播放后，触发命令要求用户
执行相同的鼠标或键操作，以便继续播放下一个宏。

交互模式通常用作教学用户的教程。
在此模式下，优良作法是在文本编辑器中手动编辑触发器，然后插入“提示”或“广播”命令。
提示命令将仅在屏幕的左上角显示一些注释文本。
Broadcast命令可以将/事件发送到世界，以便外部代码（如代码块中的代码）可以知道播放宏的进度。
这使我们能够在播放宏的同时在外部代码中添加更多视觉或音频效果。

## 播放宏控制器
如果世界不是只读的，则播放宏控制器将显示进度条和停止按钮。

如果世界不是只读的，则播放宏控制器将显示进度条和停止按钮。
-`SetPlaySpeed(1.25)`：在运行时更改播放速度。
-`SetAutoPlay(true)`：播放触发
-`SetHelpLevel(0)`：-1显示按键和鼠标提示，0禁用鼠标提示，1（默认）显示所有可能的提示

以下代码非常适合播放电影序列
```
SetHelpLevel(-1)
SetAutoPlay(true)
SetPlaySpeed(1.25)
```
默认代码如下
```
SetHelpLevel(1)
SetAutoPlay(false)
SetPlaySpeed(1)
```


## 宏列表
```
Idle(500)
CameraMove(8,0.54347,0.18799)
CameraLookat(19980.29883,-126.59001,19998.52929)
PlayerMove(19181,5,19198,0.23781)
SceneClickTrigger("shift+right",-0.19781,0.07273)
SceneClick("shift+right",-0.19781,0.07273)
SceneDragTrigger("ctrl+left",-0.35925,0.23271,-0.05236,0.23562)
SceneDrag("ctrl+left",-0.35925,0.23271,-0.05236,0.23562)
Tip("some text")
Broadcast("globalGameEvent")
SetPlaySpeed(1.25)
```

## 如何使UI控件可记录？
在mcml v1中，可记录按钮（如input / div）应具有“ uiname”属性。
aries：窗口关闭按钮的属性名称为“ uiname_onclose”。
像（输入文本）这样的editbox应该同时具有“ uiname”和“ onchange”属性。您可以将虚拟函数分配给“ onchange”，但需要一个。

## 如何记录场景事件（按键和鼠标）？
我们可以在SceneContext的handleMouseEvent（）和handleKeyEvent（）方法中添加宏。
由于paracraft中的所有场景上下文都是从BaseContext派生的，因此我们在上面的BaseContext中进行了操作。


---

Macros are sequences of key and mouse text command that can be replayed in a command block or 
by calling GameLogic.Macros:Play(text). 

## What are good macros?
Macros are almost independent of screen resolution. However, it is good practice to click in the center of a scene block, 
and do not click around the edge of the scene, because the viewport aspect ratio may be different on the user's computer
and the click location may not be seen on it. Always clicking around the center of the scene to ensure valid mouse clicks on all aspect ratios. 
Also, remove redundant steps like frequently moving the player or changing camera view, because they will generate unnecessary
macro commands. 

## Interactive mode
One can record macro in Interactive mode by "/macro record -i" command.  This will generate additional [XXX]trigger command.
These trigger commands will ignore previous Idle(wait) command. Once played, trigger commands require the user to 
perform the same mouse or key actions in order to continue playing the next macro. 

Interactive mode is usually used as a tutorial for teaching users. 
In this mode, it is good practice to manually edit the triggers in a text editor and inject "Tip" or "Broadcast" commands. 
The Tip command will just display some comment text at the left top corner of the screen. 
The Broadcast command can /sendevent to the world, so that external code, like in a code block, can know the progress of the playing macros. 
This enables us to add more visual or audio effects in external code, while macros are being played. 

## Play Macro Controller
If the world is not readonly, the play macro controller will display a progress bar and a stop button. 
One can use the macro command `SetPlaySpeed(1.25)` to change the playback speed at runtime.

If the world is not readonly, the play macro controller will display a progress bar and a stop button. 
- `SetPlaySpeed(1.25)` : change the playback speed at runtime.
- `SetAutoPlay(true)` : play triggers through
- `SetHelpLevel(0)`: -1 to display key and mouse tips, 0 to disable mouse tips, 1 (default) to show all possible tips

Following code is good for playing the sequence as a movie
```
SetHelpLevel(-1)
SetAutoPlay(true)
SetPlaySpeed(1.25)
```
Following code is default

```
SetHelpLevel(1)
SetAutoPlay(false)
SetPlaySpeed(1)
```


## Macro Lists
```
Idle(500)
CameraMove(8,0.54347,0.18799)
CameraLookat(19980.29883,-126.59001,19998.52929)
PlayerMove(19181,5,19198,0.23781)
SceneClickTrigger("shift+right",-0.19781,0.07273)
SceneClick("shift+right",-0.19781,0.07273)
SceneDragTrigger("ctrl+left",-0.35925,0.23271,-0.05236,0.23562)
SceneDrag("ctrl+left",-0.35925,0.23271,-0.05236,0.23562)
Tip("some text")
Broadcast("globalGameEvent")
SetPlaySpeed(1.25)
```

## How to make UI control recordable?
In mcml v1, recordable button(like input/div) should have "uiname" attribute. 
aries:window close button attribute name is "uiname_onclose".
editbox like (input text) should have both "uiname" and "onchange" attribute. You can assign a dummy function to "onchange", but it needs one. 

## How to record scene event (both key and mouse)?
We can add macros in SceneContext's handleMouseEvent() and handleKeyEvent() method. 
Since all scene contexts in paracraft are derived from BaseContext, we did above in BaseContext. 





