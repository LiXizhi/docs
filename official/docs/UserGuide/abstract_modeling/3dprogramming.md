## 3D世界的编程模型



大家学习编程就要逐渐掌握抽象建模的过程和方法。


前面我们介绍过编程的抽象模型：包括指令，事件，控制指令执行顺序的控制语句，还有数据结构。 这个模型可以说是编程的最简模型。不管你是学习什么编程语言，也不管你是直接面对机器编程，还是面对操作系统，还是面对一个虚拟环境比如一个3D世界，这个抽象模型都是适用的。

而3D世界本身也是一个抽象模型，所以我们要在3D世界里编程，我们就需要了解一下3D世界这个抽象模型的要素：

> 这里大家自己想一想：3D世界里面应该有什么？（结合你们已经积累的对Paracraft世界的体验。）

**3D世界是个三维空间。**

3D世界，顾名思义，和2D的不同，是个三维空间。 3D世界里的运动或者位置变化往往表现为3维坐标的变化。我们可以获取角色的坐标，场景里某个方块的坐标，并通过改变这个坐标的方式来控制我们的角色或方块。对于机关类方块，我们甚至可以直接触发在某个位置的机关。

比如在钢琴小游戏里，我们通过坐标的变化来实现琴键按下再弹回原来位置的效果。
```lua
move(0,-0.3,0)
wait(0.25)
move(0,0.3,0)

```

比如在乒乓球小游戏里，我们要让乒乓球不停的运动，我们就在永远重复里加了这么一句 moveForward(0.1).

> 请大家回顾前面的各个项目，看看其中的坐标都是怎么运用的？自己做个汇总。

**3D世界里有角色**

顾名思义，“世界”里会有很多东西，包括不会动的东西如场景等，还有会动的东西如角色。

角色包括人物，动物，物品（比如在电梯调度小游戏里的电梯，是我们自己搭建的一个角色）。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3001/raw#image.png'
  ext: png
  filename: image.png
  size: '161313'
  unit: '%'

```



除了角色, 3D世界里还有场景，甚至机关。都是由各种方块构成的。对3D世界的掌握也包括对这些方块的掌握。

主角，3D世界默认是有个主角的。你通过键盘鼠标控制的默认是这个主角，包括控制主角的走动，飞行，转身，转换视角等。你是通过这个主角的视角去看这个3D世界的。

镜头默认是跟随主角的。所以在3D世界里除了我们跟着主角到处走和看，我们也能看到主角。我们也可以用鼠标或命令控制镜头，比如镜头的远近等。在编辑电影方块的时候，我们也可以编辑电影方块播放时镜头的位置动作等。比如迷宫小游戏里里我们对镜头的控制。
```lua
camera(12, 45, 0)
```

**角色可以做动作，也有控制这些动作的指令。**

比如人物角色可以向前走，可以说话，可以转身，这些都有相应的指令。我们可以通过这些指令控制角色做这些动作。

镜头的各种动作，也有相关的指令，如远近，转角，仰角。

在3D世界里，除了搭建场景设置机关外，最重要的工作就是控制角色。通过对角色的控制我们可以做动画电影，也可以编游戏。

对角色的控制是通过代码方块和电影方块来完成的。

每个角色都有控制它的代码（使用代码方块），以及代表电影片段的电影方块。简单的动作，我们可以用电影方块来完成，但比较复杂的动作尤其是逻辑比较复杂的，我们就需要编程来完成。

3D世界里的指令，除了控制角色的，也有跟整个3D世界乃至系统相关的 （exit--退出运行, restart--重新开始）

**3D世界里的事件**

<div style="float:left;width:50%">
  
**外部事件**

- 鼠标或键盘的按下
- 演员被点击
- 某方块被点击
 
</div>

**内部事件**
- 碰到方块
- 动画播放到某一帧

<div style="clear:both" />

**消息**

角色间也可以主动发消息。在Paracraft里都是广播消息。通过消息，角色间可以对话，像现实世界里人和人对话一样。比如跳一跳小游戏里用到的广播消息。

```lua
broadcast("startgame")
broadcast("createNextBlock")
broadcastAndWait("jump", strength)

registerBroadcastEvent("jump", function(strength)
    Jump(strength)
end)

registerBroadcastEvent("createNextBlock", function()
    _G.bZ = bZ - math.random(1.5, 4)
    clone("platform", {x = bX, y=bY, z = bZ})    
end)
```

**其他**

以上是基本的3D世界的抽象模型。我们可以看到主要是有3D世界特有的指令和事件。而控制指令执行顺序的控制语句其实是和其他领域的编程相似。

<div style="float:right;width:170px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3412/raw#piano.png)
  
</div>

在这个基本的3D世界的抽象模型的基础上，大家还可以根据自己在3D世界里玩游戏或者做动画编程的经验，进一步丰富这个抽象模型。

比如**3D世界里的事情，很多是永远执行的**。所以我们经常需要使用while(true)这个语句。


比如我们经常会需要**很多同样或类似的角色**，例如钢琴小游戏里我们制作的琴键。这就需要用到角色复制以及对被复制角色的控制。

<div style="clear:both"/>
<div style="float:right;width:200px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3130/raw#piano.png)
  
</div>


```lua
-- 对被克隆的角色进行控制和属性设置
registerCloneEvent(function(msg)
    move(0, 0, -msg.i*1.05)
    setActorValue("note", msg.note)
    if(msg.isBlack) then
        play(1000)
        move(1, 0.5, 0)
    end
end)

hide()

-- 克隆角色，并传递参数
clone("myself", {note=1, i=1 })
clone("myself", {note=2, i=1.5, isBlack=true})
clone("myself", {note=3, i=2})
clone("myself", {note=4, i=2.5, isBlack=true})
clone("myself", {note=5, i=3, })
clone("myself", {note=6, i=4, }) 
clone("myself", {note=7, i=4.5, isBlack=true})
clone("myself", {note=8, i=5})
clone("myself", {note=9, i=5.5, isBlack=true})
clone("myself", {note=10, i=6})
clone("myself", {note=11, i=6.5, isBlack=true})
clone("myself", {note=12, i=7})
```

<div style="clear:both" />

**Paracraft的代码方块+电影方块的模型**

在Paracraft的基础介绍里，给大家介绍了Paracraft的代码方块和电影方块，包括代码方块控制相邻的电影方块等，这些也是大家在Paracraft编程把模型转化成代码时需要考虑的。


**进阶：数据结构**

有了以上的基础，在更进阶的阶段，大家可以开始了解数据结构的使用。这点，在我们的编程课里其实也有涉及的，**最常见的数据结构有表和队列（一般叫列表，但暂时叫队列也可以）**。比如上图钢琴课里复制琴键角色时传递的参数

```lua
clone("myself", {note=7, i=4.5, isBlack=true})
```
这里的 `{note=7, i=4.5, isBlack=true}` 就是使用了一个叫做**table**(表)的数据结构。

