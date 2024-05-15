# Paracraft代码方块 v1.0

**软件用途：** Paracraft代码方块被应用在Paracraft 3D动画与编程工具软件中。它提供了一种面向动画的全新编程模式。用户可以用代码控制动画编写任意复杂的计算机动画与游戏。 
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** NPL语言, C++
**开发完成时间：** 2018年6月1日
**发表日期：** 2018年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 一种全新的面向动画的编程模式
- 支持可视化与文本式编程
- 多文件编辑
- 自定义扩展语言模块
- 并行执行所有代码
- 完善的类库

**源代码行数**: 5万行  [点击这里查看](Paracraft代码方块_code)

## 《Paracraft代码方块》使用手册

**代码方块入门教学1**

**1 理论**

知识点：
- 代码方块控制相邻的最近的电影方块
- 可以多个代码方块同时控制某个电影方块
- 代码编辑器的各个组成部分，如编译结果输出窗口
- 点击代码条块可以临时运行电影方块中的角色
- 拖拽代码条块到代码编辑区自动转化成代码，也可以直接在编辑区敲代码
- 点击代码条块说明框里的绿色小方块可以执行其中的例子，点击左上角灰色小方块可以一直显示该说明框
- **编程一定要会打字**
- 用电影方块可以制作电影
- 用骨骼可以制作动作
- 循环播放
- 图块编程
- 用拉杆控制代码方块
- for控制语句


<div style="float:right;margin-left:10px;width:280px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3352/raw#image.png)
  
</div>


我们在之前的章节中已经学会用电影方块制作动画， 这节课我们学习用`代码方块`写程序。


**2 实践：**

代码方块在E键代码或电影分类下，ID是219, 是蓝色的.
 

我们右键创建代码方块，右键单击代码方块，我们就进入了代码方块的编辑界面。我们看到下面显示: `我们在代码方块旁边自动创建了一个电影方块，你现在可以用代码控制电影方块中的演员了。` 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2719/raw#image.png'
  ext: png
  filename: image.png
  size: '280204'
  unit: px
  width: '550'
  alignment: left

```

点击`角色模型`，我们可以在这里选择一个之前做好的bmax模型。当然了我们也可以有另外一种操作方式，就是手工创建电影方块，然后再在旁边创建代码方块。 
我们右键单击电影方块，点击添加演员。加好演员后，我们关闭电影方块。

这里大家要注意的是，代码方块永远控制的是离它最近的电影方块。未来我们会看到有很多代码方块组成的程序。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2720/raw#image.png'
  ext: png
  filename: image.png
  size: '459339'
  unit: px
  alignment: left
  width: 450

```
比如红色框中两个代码方块控制的是红色框中的电影方块；蓝色框中代码方块控制的是蓝色框中的电影方块。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2721/raw#image.png'
  ext: png
  filename: image.png
  size: '221188'
  unit: px
  width: '450'
  alignment: left

```

我们再来看这个例子，蓝色框中的三个代码方块控制的都是蓝色框中的电影方块，因为他们三个离电影方块最近；红色框中的代码方块控制的是红色框中的电影方块。

我们右键打开代码方块，看一下编辑界面，左上角的按钮是运行代码，旁边是暂停，最下面是输出框，如果程序出现错误会显示在这里。 

左侧区域是我们所有可以使用的代码。当我们把鼠标放上去，会看到这个代码的一个例子。

`moveford(1, 0.5)`代表的是演员在0.5秒内前进一格。如果我们点击这条代码，就会看到演员在零点五秒内前进了一格，再点击一下，它又前进了一格，每点击一下，我们都可以临时的运行这个代码。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2722/raw#image.png'
  ext: png
  filename: image.png
  size: '15723'
  unit: px
  width: 400
  alignment: left

```

但我们现在并没有写这个代码。怎么写呢？有两种方式。
- 第一种我们可以复制粘贴代码，
- 第二种我们可以直接将它拖到右侧。

但是我们还是建议大家在未来熟悉之后，不要用拖，而是用打字的方式练习打字。 每一个代码的下面都会附上一个或多个例子，我们可以点击右侧的绿色小点执行这个例子。

我们可以看到演员旋转了30度，turn是旋转，同时演员向前走了一下。moveForwad如果括号里没有第二个参数，那么就是默认在1/20秒内，也就是在1/20秒内前进了0.05格。for是循环函数，它的意思是将do和end之间的代码执行20次。i是一个变量，表示次数。

那么这段代码的实际效果就是在一秒内前进一格。我们建议大家点击右侧的灰色小点一直显示，那么这个帮助窗口就会一直显示在右上方，如图。实际上就是方便大家在下面的代码区域照着打字。 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2723/raw#image.png'
  ext: png
  filename: image.png
  size: '134035'
  unit: px
  width: 480
  alignment: left

```

那么对于代码方块中的每一个代码，我们建议大家将每一个例子都在自己下面的代码区域敲一遍。像这样，我敲一遍上面例子中的代码：

```lua
turn(30); -- 结尾的分号加不加都可以
for i=1, 20 do
    moveForward(0.05)  `Tab键`缩进一格
end
```

> 大家要练习打字，编程一定要会打字，不会打字就没有办法成为程序员。

每行语句后面的`;`分号加不加都可以。`Tab键`是缩进一格，让代码更好看一些。代码写好后点击左上角的运行按钮，我们运行一下，就可以看到演员的效果了。

我们再来看第三个代码，旋转到90度，我们右键单击它，它的帮助窗口同样会一直显示在右上角，我们直接把这个例子复制粘贴过来，我们运行一下。 

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2724/raw#image.png'
  ext: png
  filename: image.png
  size: '32564'
  unit: px
  width: 400
  alignment: left

```

那么第一行`turnTo(-60)`表示演员会先转向-60度的位置。
`wait(1)`表示，等待一秒，然后演员再转向零度的位置，我们运行一下，我们可以看到演员先转向-60度再转回来，wait的代码在`控制`项下是有说明的，下面有两个例子。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2726/raw#image.png'
  ext: png
  filename: image.png
  size: '24589'
  unit: px
  width: '400'
  alignment: left

```

我们再来到`外观`项下来，看这条代码，`播放从第10到1000毫秒`的电影方块中的角色动画。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2725/raw#image.png'
  ext: png
  filename: image.png
  size: '22398'
  unit: px
  width: '400'
  alignment: left

```

右键代码方块旁边的电影方块，现在我们给演员做一个简单的动画，我们点击这个演员，按1切换到骨骼，做一个简单的招手动画。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2727/raw#image.png'
  ext: png
  filename: image.png
  size: '730849'
  unit: px
  width: '400'
  alignment: left

```

我们将电影方块时长缩短到3秒，我们在500毫秒时做一个抬手动作，在1000毫秒时再让手臂放下来。 
这时我们看到演员做了一个简单的招手动作，我们关闭电影方块，这时如果我们运行`播放从第10到1000毫秒`，我们每点一下动画就会播放一次，再点一下又播放一次。下面一个代码是`循环播放loop从第10到1000毫秒`，我们点击一下。现在我没有点击它，它会一直循环播放刚刚的动作。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2728/raw#image.png'
  ext: png
  filename: image.png
  size: '17360'
  unit: px
  alignment: left
  width: 400

```

下面我们来看第一个代码`说("hello")`，我们让它一直显示，我们在下面敲一段代码。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2729/raw#image.png'
  ext: png
  filename: image.png
  size: '146499'
  unit: px
  alignment: left
  width: 450

```

```lua
say("hello world!!")
```

`say("")`双引号之间是说的内容，大家记得一定要打英文的引号"hello world!!"。

这时我们点运行，我们看到这个演员会说"hello world!!"，如果我们想让hello world说完两秒后消失，我们可以在后面加上2秒，这时我们再点运行。hello world说完后2秒会自动消失。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2732/raw#image.png'
  ext: png
  filename: image.png
  size: '828156'
  unit: px
  width: 600
  alignment: left

```

我们再到运动项下。我们有一个`位移`的代码`move在0.5秒内向前移动一格`，我们将它拖过来，我们点下运行。演员会先说hello world，然后向前移动一格。

下面我们再来到事件项下。第一个，`当演员被点击时`，它会执行方function和end之间的代码，我们先删掉之前的代码，将它拖到代码区。 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2733/raw#image.png'
  ext: png
  filename: image.png
  size: '337760'
  unit: px
  width: '500'
  alignment: left

```

比如当演员被点击时，演员say("hello").
```lua
registerClickEvent(function()
   say("hello");
end)
```
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2734/raw#image.png'
  ext: png
  filename: image.png
  size: '565742'
  unit: px
  width: 550
  alignment: left

```

我们运行一下，点击一下这个演员，他就说hello了。

下面我们来看一下`图块`编辑器。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2735/raw#image.png'
  ext: png
  filename: image.png
  size: '22998'
  unit: px
  width: '400'
  alignment: left

```

图块是给低年龄层还不会打字的儿童使用的图块化的编程。对于已经会打字的学生，我们还是建议用打字的方式来输入代码。点击上方图块按钮，进入图块编辑器，刚才那段代码我们可以这样来写：点击事件，选择对应的代码把它拖过来，再选择外观。选择说两秒。把它嵌入到事件中，再点击运动，选择前进一格，同样把它嵌入到事件中。大家可以看到，这样就构成了一个像自然语言一样的描述。 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2736/raw#image.png'
  ext: png
  filename: image.png
  size: '34033'
  unit: px
  alignment: left
  width: 450

```

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2738/raw#image.png'
  ext: png
  filename: image.png
  size: '15353'
  unit: px
  width: '400'
  alignment: left

```

我们看到刚才的图块已经被翻译成了计算机代码，其实它和刚才图块中的中文基本是一一对应的，其实好的代码就像自然语言一样。
```lua
registerClickEvent(function()
  say('hello!', 2)
  moveForward(1, 0.5)
end)
```
registerClickEvent代表注册点击事件，当演员被点击时，他会先说hello两秒钟，然后`向前走1格，在0.5秒内`，我们运行一下这段代码，点击演员，他会先说hello两秒，然后向前运行1格。

现在我们将刚才学过的内容全部连起来做一个小游戏，右键单击代码方块，大家根据刚才学过的内容，能不能猜出这段代码的含义？ 

```lua
say("点击我!")
turnTo(180)
registerClickEvent(function()
   turn(15)
   play(0,1000);
   say("hi~",1);
end)
```

第一行演员说`点击我`，然后旋转到180度的位置，点击演员时他会先转15度，然后播放从0到1000毫秒的动画，然后说一秒`hi~`。这里大家要注意的是，play这条语句执行之后会立即返回，继续执行后面的代码，但是play的播放效果会持续到1000毫秒才停止。我们运行一下，我们看到人物是朝向我们的，因为他转到了180度的位置。这时我们点击演员，他转了15度，招招手说了一句hi，再点击他一下，我们可以看到同样的效果。 是不是很有趣？

这样我们就用代码方块控制了电影方块中的演员和动画。这时我们点击关闭，关闭了代码方块的编辑界面，那么刚才创建的演员和动画就随之消失了。

那么如何在游戏模式下, 在不显示代码方块编辑界面的模式下去执行代码方块中的代码呢？ 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2745/raw#image.png'
  ext: png
  filename: image.png
  size: '601397'
  unit: px
  width: 350
  alignment: left

```

我们需要让代码方块连接一个拉杆，你也可以不用导线，实现直接在代码方块旁边放拉杆。拉杆在电影项下的最后一个。现在我们点击拉杆，我们看到演员就出现了，我们点击演员，这就是我们刚刚做的小游戏。 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2746/raw#image.png'
  ext: png
  filename: image.png
  size: '575154'
  unit: px
  width: '300'
  alignment: left

```

关闭拉杆，演员就消失了。如果你的场景中有多个代码方块，你可以同时打开他们。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2744/raw#image.png'
  ext: png
  filename: image.png
  size: '1009295'
  unit: px
  width: 400
  alignment: left

```

比如左侧的拉杆是一个游戏，右侧的拉杆又是一个游戏，两个游戏可以同时存在，并且可以保存。

未来我们会用Paracraft和NPL语言制作很多游戏。 而游戏是由动画和程序构成的。 动画如同我们的记忆，是很多很多小的固定的动画片段。 在Paracraft中，我们用电影方块制作并存储这些动画的记忆，用代码方块来制作控制这些记忆何时播放的逻辑。


**代码方块入门教学2**

**1 理论**

讲授知识点：
- 两个或多个代码方块放在一起
- 多个代码方块的同时运行
- 给相邻的代码方块命名
- 用拉杆连接不同的代码方块，同时控制多个角色形成一个大的系统
  - 临时断开拉杆对某代码方块进行“单元测试”
- turn，say，play，moveForward，registerClickEvent函数
- while控制语句

**2 实践：**
上一节是一个代码方块。这一节我们来讲两个代码方块的例子。那么首先右键创建一个新的代码方块，右键编辑它，这时仍然在旁边自动创建了一个电影方块。右键单击电影方块，演员已经自动添加好了。我们给它做一段动画，时长改为3秒，我们做一个招手的动作，第0秒时让他的手臂举起来，500毫秒时让手臂降下来，敬个礼。 1000毫秒时再恢复举手的动作。我们关闭电影方块，演员就消失了。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2749/raw#image.png'
  ext: png
  filename: image.png
  size: '733092'
  unit: px
  width: 550
  alignment: left

```

这时我们先点击运行，在没有写代码的情况下，演员也会出现。此时演员是背对我们的。我们现在到运动项下，将`旋转到turnTo`拖过来，我们改成`turnTo(180)`度，点一下运行，演员就转过来了。

> 我们尽量每写一行代码就点一下运行，这样如果有错误的话，我们很好调试。

下面我们让他说一句话，在外观项下将`说hello`拖过来，我们让他说一句中文，`点击我`。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2750/raw#image.png'
  ext: png
  filename: image.png
  size: '17968'
  unit: px
  width: '400'
  alignment: left

```

点击代码窗口左上角的`En`(English)按钮可切换到系统输入法，并输入中文， 大家记得输完中文后一定要再次点击切回英文的输入法，因为中文的标点符号计算机语言无法识别，一定要使用英文的输入法，这点很重要。 

然后我们仍然马上运行一下，可以看到演员在180度的位置说`点击我`，然后我们到事件项下，将`当演员被点击时`这条代码拖过来，我们再到运动向下，将`旋转15度拖`过来，为了好看，我们敲Tab键，让代码缩进一格。这时我们运行一下，输出框没有报错，我们点击一下演员，他就转了15度，我们再点它就再转15度。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2751/raw#image.png'
  ext: png
  filename: image.png
  size: '421860'
  unit: px
  width: 550
  alignment: left

```


我们如何让演员不停地旋转呢？我们来到控制项下，找到`永远重复`(while true do end)。我们将它拖过来，同样为了好看，我们将它缩进。 

我们把turn(15)度剪切一下，粘贴到while true do end的中间。同样前面也缩进了一格。

```lua
turnTo(180)
say("点击我!")

registerClickEvent(function()
    while(true) do
        turn(15)   -- 改为turn(1)可以变慢
    end
end)
```
这里while是循环的意思，true是真。while(true)就是不停的循环，它会不停的执行do和end之间的代码，也就是不停地执行turn(15)度。那么效果是演员不停的旋转。我们点击运行，点击一下演员，可以看到演员在不停的旋转，它现在旋转的太快了，我们让它每一次只旋转1度。再运行一下，点击演员，可以看到它现在是缓慢地旋转了。

我们点击暂停。现在我们来添加第二个代码方块，我们在它旁边再添加一个。 

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2752/raw#image.png'
  ext: png
  filename: image.png
  size: '648582'
  unit: px
  width: 550
  alignment: left

```

那么在新的代码方块中，我们仍然让演员去响应点击事件。这一次当演员被点击时，我们让它不停地往前走，我们同样还是使用`永远重复`，右键点击`永远重复`让提示窗口一直显示在代码区的上方。我们照着上面的例子敲一下代码，这次我们不要拖拽了，我们要练习打字，Tab键是缩进。我要注意要用英文输入法。像下面：向前走，moveForward每次0.01格,在1/20秒内,永远重复执行。演员就会一直向前走。

```lua
registerClickEvent(function()
    while(true) do
        moveForward(0.01)
    end
end)
```

那么为了能够单独执行代码方块查看效果，我们先Ctrl加左键，把第一个代码方块移走，再把第二个代码方块移过来，我们看一下单独执行的效果。 右键单击代码方块，点击运行。我们点击一下演员，可以看到演员一直向前走是停不下来的，因为`while true`是永远重复执行。

现在我们将两个代码方块重新连接在一起。两个代码方块都控制的是电影方块中的演员。这时我们可以通过右键单击任何一个代码方块来切换它们两者之中的代码。还有一种切换方式，我们可以给每一个代码方块取一个名字，比如其中一个代码方块会让演员一直向前走，我们给它取名为move，此时我们将鼠标移至旁边的省略号，可以看到它的名字是move。 另外一个代码方块是`未命名`，我们点击切换过去，他会让演员一直旋转，我们给它取名为turn。这时我们也可以在通过点击名字右侧的`...`按钮方便的切换两个代码方块。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2753/raw#image.png'
  ext: png
  filename: image.png
  size: '22594'
  unit: px
  width: '400'
  alignment: left

```

这个时候我们无论在哪一个代码方块的编辑界面上点击运行，都会同时运行和它相连的所有代码方块中的代码。下面我们点击运行，那么演员会同时执行两个代码方块中的代码，也就是点击演员后，他会边走边旋转。我们点击运行就可以看到效果了。

我们点击暂停，回到第一个代码方块，我们之前还给演员做了一段招手的动画，我们也把它加入进来。 我们将外观项下的`循环播放`，拖入任意一个代码方块，比如拖到第一个里面，将它放到while的外面，我们将它改成从0秒开始到第1000毫秒循环播放，也就是在点击演员时，它会先循环播放动画, 再不停的旋转。
```lua
turnTo(180)
say("点击我!")
registerClickEvent(function()
    playLoop(0, 1000);
    while(true) do
        turn(1)
    end
end)
```
playLoop和play一样，执行之后立即返回，继续执行后面的代码。那么运行后最终的效果就是点击演员后，它会循环招手动作，同时不停地旋转。在另外一个代码方块中，演员被点击后会不停的向前走。那么我们点击一下运行，看一下最后的效果。 点击演员，可以看到演员一边做招手的动作, 一边旋转, 一边往前走，三者是同时执行的。

下面我们来看如何在场景中同时激活两个代码方块。我们到电影项下选择拉杆，拉杆可以放在两个代码方块旁边的任何一个位置，我们打开其中任意一个拉杆，可以看到两个代码方块同时亮起，表示两个代码方块都被执行了。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2754/raw#image.png'
  ext: png
  filename: image.png
  size: '1042602'
  unit: px
  width: 450
  alignment: left

```

点击演员可以看到同时执行的效果。关闭拉杆，打开另外一个拉杆，两个代码方块仍然是同时亮起，被执行的，效果也是一样的。我们还可以用电影项下的导线连接另外一组代码方块。 这时我们打开这个拉杆，可以看到两组代码方块也是同时执行的。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2755/raw#image.png'
  ext: png
  filename: image.png
  size: '1024029'
  unit: px
  width: '450'
  alignment: left

```

在调试程序时，我们会经常需要先调试一组代码方块，再调试另外一组，这在编程开发中叫做`单元测试`。像Paracraft这款软件，有一百多万行NPL代码，由6000多个像代码方块这样的文件组成。我们在写这样的大型程序时，经常需要让每一组文件可以独立的运行和被测试。

最后我再补充一下，到今天为止，我们还没有告诉大家计算机语言的语法，因为它并不重要，重要的是大多数计算机语言都和英语很接近。 越优秀的程序员，写的代码越接近英文。 

人类发明了上百种自然语言，中文，英文，等等，在过去几十年中，人类也发明了上百种计算机语言。我们刚刚使用的计算机语言叫做NPL，神经元并行计算机语言，是一款专门为人工智能，分布式计算以及3D仿真开发的编程语言。我们所使用的Paracraft动画软件，魔法哈奇，我们的网站都是用NPL语言编写的。 所以学会它，你可以写出像魔法哈奇这样复杂的大型3D软件或像keepwork.com这样的复杂网站服务器。青少年精通一门通用编程语言是很必要的，因为只要精通任意一门编程语言，其它语言基本都可以在几小时内学会。NPL是最佳的选择之一，因为它易于学习，功能强大，配合了Paracraft动画工具，并且语法和C/C++接近。 

代码方块中的所有命令可分为两大类：
- 一类是用于做相似匹配的。比如比较状态或响应事件。
- 一类是用于播放动画的。比如移动人物或播放电影方块中角色从某个时间点的动画

其实如果人脑也是一个计算机的，我们的思维也大概分成上面两大类。比如当我们看到一个和苹果很像的东西时，我们会做相似匹配，并从记忆的电影库中播放一段舌头或声音的动画，在脑海中产生了苹果的发音。


## 附录2：《代码方块》函数速查表



详细的参考手册请到Paracraft软件或官方网站中寻找。你也可以在Paracraft中访问项目`530`, 直接在3D世界中运行各种测试代码。

### 运动
<div style="float:left;margin-right:10px;">

> 前进`1`格 在`0.5`秒内
moveForward(1, 0.5)

</div>
<div style="float:left;">

```lua
-- 例子1:
turn(30);
for i=1, 20 do
    moveForward(0.05)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 旋转`15`度
turn(15)

</div>
<div style="float:left;">

```lua
-- 例子1:
turnTo(-60)
for i=1, 100 do
    turn(-3)
end
-- 例子2:点击我打招呼
say("Click Me!", 2)
registerClickEvent(function()
    turn(15)
    play(0,1000)
    say("hi!")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 旋转到`90`方向
turnTo(90)

</div>
<div style="float:left;">

```lua
-- 例子1:
turnTo(-60)
wait(1)
turnTo(0)
-- 例子2:三轴旋转
turnTo(0, 0, 45)
wait(1)
turnTo(0, 45, 0)
wait(1)
turnTo(0, nil, 45)
-- 例子3:
while(true) do
    setActorValue("pitch", getActorValue("pitch")+2)
    say(getActorValue("pitch"))
    wait()
end
-- 例子4:
while(true) do
    turnTo(nil, nil, getActorValue("roll")+2)
    wait()
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 转向`鼠标`
turnTo("mouse-pointer")

</div>
<div style="float:left;">

```lua
-- 例子1:转向鼠标,主角,指定角色
turnTo("mouse-pointer")
moveForward(1, 1)
turnTo("@p")
moveForward(1, 1)
turnTo("frog")
moveForward(1, 1)
-- 例子2:面向摄影机
while(true) do
    turnTo("camera")
    wait(0.01)
end
-- 例子3:面向摄影机
-- camera yaw and pitch
while(true) do
    turnTo("camera", "camera")
    wait(0.01)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 位移`1` `0` `0` 在`0.5`秒内
move(1, 0, 0, 0.5)

</div>
<div style="float:left;">

```lua
-- 例子1:
turnTo(0)
move(0.5,1,0, 0.5)
move(1,-1,0, 0.5)
say("jump!", 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 瞬移到`19176` `5` `19209`
moveTo(19176, 5, 19209)

</div>
<div style="float:left;">

```lua
-- 例子1:
moveTo(19257,5,19174)
moveTo("mouse-pointer")
moveTo("@p")
moveTo("frog")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 瞬移到`鼠标`
moveTo("mouse-pointer")

</div>
<div style="float:left;">

```lua
-- 例子1:瞬移到主角，鼠标，指定角色
say("current player", 1)
moveTo("@p")
say("mouse-pointer", 1)
moveTo("mouse-pointer")
say("the frog actor if any", 1)
moveTo("frog")
-- 例子2:瞬移到角色的某个骨骼
-- block position
moveTo("myActorName")
-- float position
moveTo("myActorName::")
-- bone position
moveTo("myActorName::bone_name")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 行走`1` `0` `0`持续`0.5`秒
walk(1, 0, 0, 0.5)

</div>
<div style="float:left;">

```lua
-- 例子1:
walk(1,0) -- x,z
walk(0,1) -- x,z
walk(-1,0,-1) -- x,y,z
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 向前走`1`持续`0.5`秒
walkForward(1, 0.5)

</div>
<div style="float:left;">

```lua
-- 例子1:
turnTo(0)
walkForward(1)
turn(180)
walkForward(1, 0.5)
-- 例子2:恢复默认物理仿真
play(0,1000, true)
moveForward(1, 0.5)
walkForward(0)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 速度`~ 5 ~`
velocity("~ 5 ~")

</div>
<div style="float:left;">

```lua
-- 例子1:
velocity("~ 10 ~")
wait(0.3)
velocity("add 2 ~ 2")
wait(2)
velocity("0 0 0")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 反弹
bounce()

</div>
<div style="float:left;">

```lua
-- 例子1:遇到方块反弹
turnTo(45)
while(true) do
    moveForward(0.02)
    if(isTouching("block")) then
        bounce()
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> X坐标
getX()

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    say(getX())
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> Y坐标
getY()

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    say(getY())
    if(getY()<3) then
        tip("Game Over!")
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> Z坐标
getZ()

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    say(getZ())
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 角色xyz位置
getPos()

</div>
<div style="float:left;">

```lua
-- 例子1:
local x, y, z = getPos()
setPos(x, y+0.5, z)
-- 例子2:
local x, y, z = getPos("actorName")
setPos(x, y+0.5, z)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置角色位置`19176` `5` `19209`
setPos(19176, 5, 19209)

</div>
<div style="float:left;">

```lua
-- 例子1:
local x, y, z = getPos()
setPos(x, y+0.5, z)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 方向
getFacing()

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    say(getFacing())
end
-- 例子2:
say(getFacing("someActorName"))
```

</div>
<div style="clear:both"/>

### 外观
<div style="float:left;margin-right:10px;">

> 说 `hello!` 持续 `2` 秒
say("hello!", 2)

</div>
<div style="float:left;">

```lua
-- 例子1:
say("Jump!", 2)
move(0,1,0)
-- 例子2:点击我打招呼
say("Click Me!", 2)
registerClickEvent(function()
    turn(15)
    play(0,1000)
    say("hi!")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 说 `hello!`
say("hello!")

</div>
<div style="float:left;">

```lua
-- 例子1:在人物头顶说些话
say("Hello!")
wait(1)
say("")
-- 例子2:点击我打招呼
say("Click Me!", 2)
registerClickEvent(function()
    turn(15)
    play(0,1000)
    say("hi!")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 提示文字`Start Game!`
tip("Start Game!")

</div>
<div style="float:left;">

```lua
-- 例子1:
tip("Start Game in 3!")
wait(1)
tip("Start Game in 2!")
wait(1)
tip("Start Game in 1!")
wait(1)
tip("")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 显示
show()

</div>
<div style="float:left;">

```lua
-- 例子1:显示/隐藏角色
hide()
wait(1)
show()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 隐藏
hide()

</div>
<div style="float:left;">

```lua
-- 例子1:显示/隐藏角色
hide()
wait(1)
show()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放动作编号 `4`
anim(4)

</div>
<div style="float:left;">

```lua
-- 例子1:
anim(4)
move(-2,0,0,1)
anim(0)
-- 例子2:常用动作编号
-- 0: standing
-- 4: walking 
-- 5: running
-- check movie block for more ids
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放从`10`到`1000`毫秒
play(10, 1000)

</div>
<div style="float:left;">

```lua
-- 例子1:播放电影方块中的角色动画
play(10, 1000)
say("No looping", 1)
-- 例子2:点击我打招呼
say("Click Me!", 2)
registerClickEvent(function()
    turn(15)
    play(0,1000)
    say("hi!")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 循环播放从`10`到`1000`毫秒
playLoop(10, 1000)

</div>
<div style="float:left;">

```lua
-- 例子1:播放电影方块中的角色动画
playLoop(10, 1000)
say("Looping", 3)
stop()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 骨骼`Root`从`10`到`1000`并循环`true`
playBone("Root", 10, 1000, true)

</div>
<div style="float:left;">

```lua
-- 例子1:
playBone("Neck", 2000)
-- regular expression supported
playBone(".*UpperArm", 5000, 7000)
playBone(".*Forearm", 5000, 7000)
play(0, 4000)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放速度`1`
playSpeed(1)

</div>
<div style="float:left;">

```lua
-- 例子1:
playSpeed(4)
playLoop(0, 1000)
say("Looping", 3)
playSpeed(1)
stop()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 停止播放
stop()

</div>
<div style="float:left;">

```lua
-- 例子1:播放/暂停角色动画
playLoop(10, 1000)
wait(2)
stop()
turn(15)
playLoop(10, 1000)
wait(2)
stop()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 放缩百分之`10`
scale(10)

</div>
<div style="float:left;">

```lua
-- 例子1:
scale(50)
wait(1)
scale(-50)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 放缩到百分之`100`
scaleTo(100)

</div>
<div style="float:left;">

```lua
-- 例子1:
for i=1, 20 do
    scale(10)
end
scaleTo(50)
wait(0.5)
scaleTo(200)
wait(0.5)
scaleTo(100)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 观看`此角色`
focus("myself")

</div>
<div style="float:left;">

```lua
-- 例子1:
focus()
moveForward(2,2)
focus("player")
-- 例子2:
focus("someName")
focus(getActor("someName2"))
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 摄影机距离`12`角度`45`朝向`90`
camera(12, 45, 90)

</div>
<div style="float:left;">

```lua
-- 例子1:
for i=1, 100 do
    camera(10+i*0.1, nil, nil)
    wait(0.05)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 放缩尺寸
getScale()

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    if(getScale() >= 200) then
        scaleTo(100)
    else
        scale(10)
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 动画时间
getPlayTime()

</div>
<div style="float:left;">

```lua
-- 例子1:
playLoop(10, 2000)
while(true) do
    if(getPlayTime() > 1000) then
        say("hi")
    else
        say("")
    end
    wait(0.01);
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置电影频道`myself`为:`0`,`0`,`0`
setMovie("myself", 0, 0, 0)

</div>
<div style="float:left;">

```lua
-- 例子1:不传参数代表与代码方块相邻的电影方块
hide()
setMovie("main")
playMovie("main", 0, -1);
-- 例子2:myself代表当前代码方块的名字
setMovie("myself")
playMovie("myself", 0, -1);
-- 例子3:指定电影方块的坐标
local x, y, z = codeblock:GetBlockPos();
setMovie("main", x, y, z+1)
playMovie("main", 0, -1);
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放电影频道`myself`从`0`到`-1`毫秒
playMovie("myself", 0, -1)

</div>
<div style="float:left;">

```lua
-- 例子1:播放与代码方块相邻的电影方块
hide()
-- -1 means end of movie
playMovie("myself", 0, -1);
stopMovie("myself");
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 循环播放电影频道`myself`从`0`到`-1`毫秒
playMovie("myself", 0, -1, true)

</div>
<div style="float:left;">

```lua
-- 例子1:播放与代码方块相邻的电影方块
hide()
playMovie("myself", 0, 1000, true);
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 停止播放电影频道`myself`
stopMovie("myself")

</div>
<div style="float:left;">

```lua
-- 例子1:
playMovie("myself", 0, -1);
stopMovie();
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置电影频道`myself`的属性`播放速度`为`1`
setMovieProperty("myself", "Speed", 1)

</div>
<div style="float:left;">

```lua
-- 例子1:
setMovieProperty("myself", "Speed", 2);
playMovie("myself", 0, -1);
stopMovie();
```

</div>
<div style="clear:both"/>

### 事件
<div style="float:left;margin-right:10px;">

> 当演员被点击时``
registerClickEvent(function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerClickEvent(function()
    for i=1, 20 do
        scale(10)
    end
    for i=1, 20 do
        scale(-10)
    end
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当`空格`键按下时``
registerKeyPressedEvent("space", function(msg)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:空格跳跃
registerKeyPressedEvent("space",function()
    say("Jump!", 1)
    move(0,1,0, 0.5)
    move(0,-1,0, 0.5)
    walkForward(0)
end)
-- 例子2:任意按键
registerKeyPressedEvent("any", function(msg)
    run(function()
        say(msg.keyname)
    end)
    if(isKeyPressed("e")) then
        return true
    end
end)
-- 例子3:鼠标按钮
registerKeyPressedEvent("mouse_buttons",function(event)
    say("button:"..event:buttons())
end)
-- 例子4:鼠标滚轮
registerKeyPressedEvent("mouse_wheel",function(mouse_wheel)
    say("delta:"..mouse_wheel)
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当方块`10`被点击时``
registerBlockClickEvent("10", function(msg)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:任意方块被点击
registerBlockClickEvent("any",function(msg)
	local blockid = msg.blockid;
	x, y, z, side = msg.x, msg.y, msg.z, msg.side
    say(blockid..":"..x..","..y..","..z..":"..side)
end)
-- 例子2:某个方块被点击
registerBlockClickEvent("10",function(msg)
	local blockid = msg.blockid;
	x, y, z, side = msg.x, msg.y, msg.z, msg.side
    tip("colorblock10:"..x..","..y..","..z..":"..side)
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当动画在`1000`帧时``
registerAnimationEvent(1000, function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerAnimationEvent(10, function()
    say("anim started", 3)
end)
registerAnimationEvent(1000, function()
    say("anim stopped", 1)
end)
registerClickEvent(function()
    play(10, 1000)
end);
say("click me!")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当收到`msg1`消息时(`msg`)``
registerBroadcastEvent("msg1", function(fromName)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerBroadcastEvent("jump", function(fromName)
    move(0,1,0)
    wait(1)
    move(0,-1,0)
end)
registerClickEvent(function()
    broadcastAndWait("jump")
    say("That was fun!", 2)
end)
say("click to jump!")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 广播`msg1`消息
broadcast("msg1")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerBroadcastEvent("hello", function(msg)
    say("hello"..msg)
    move(0,1,0, 0.5)
    move(0,-1,0, 0.5)
    say("bye")
end)
for i=1, 2 do
    broadcast("hello", i)
    wait(0.5)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 广播消息`msg1`(``)
broadcast("msg1", "")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerBroadcastEvent("hello", function(msg)
    say("hello"..msg)
    move(0,1,0, 0.5)
    move(0,-1,0, 0.5)
    say("bye")
end)
for i=1, 2 do
    broadcast("hello", i)
    wait(0.5)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 广播`msg1`消息并等待返回
broadcastAndWait("msg1")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerBroadcastEvent("hi", function(fromName)
    say("hi,"..tostring(fromName))
    wait(1)
    say("bye")
    wait(1)
end)
for i=1, 2 do
    broadcastAndWait("hi")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当代码方块停止时``
registerStopEvent(function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:只能执行马上可返回的代码
registerStopEvent(function()
    tip("stopped")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当收到网络消息`connect`(`msg`)时``
registerNetworkEvent("connect", function(msg)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerNetworkEvent("updateScore", function(msg)
   _G[msg.userinfo.keepworkUsername] = msg.score;
   showVariable(msg.userinfo.keepworkUsername)
end)

registerNetworkEvent("connect", function(msg)
   broadcastNetworkEvent("updateScore", {score = 100})
end)

registerNetworkEvent("disconnect", function(msg)
   hideVariable(msg.userinfo.keepworkUsername)
end)

while(true) do
   broadcastNetworkEvent("updateScore", {score = 100})
   wait(1);
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 广播网络消息`score`(`{}`)
broadcastNetworkEvent("score", {})

</div>
<div style="float:left;">

```lua
-- 例子1:
hide()
becomeAgent("@p")

registerNetworkEvent("updatePlayerPos", function(msg)
   runForActor(msg.userinfo.keepworkUsername, function()
      moveTo(msg.x, msg.y, msg.z)
   end)
end)

registerCloneEvent(function(name)
    setActorValue("name", name)
end)

registerNetworkEvent("connect", function(msg)
    clone(nil, msg.userinfo.keepworkUsername)
end)

registerNetworkEvent("disconnect", function(msg)
   runForActor(msg.userinfo.keepworkUsername, function()
      delete();
   end)
end)

while(true) do
   broadcastNetworkEvent("updatePlayerPos", {x = getX(), y=getY(), z=getZ()})
   wait(0.2);
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 发送网络消息给`username`,`title`,`{}`
sendNetworkEvent("usernames", "title", {})

</div>
<div style="float:left;">

```lua
-- 例子1:发送消息给指定用户
registerNetworkEvent("title", function(msg)
   tip(msg.userinfo.keepworkUsername)
   wait(1)
   tip(msg.a)
end)

sendNetworkEvent("username", "title", {a=1})
-- 例子2:发送原始消息给指定地址(无需登录)
-- __original is predefined name
registerNetworkEvent("__original", function(msg)
   log(msg.isUDP)
   log(msg.nid or msg.tid)
   log(msg.data)
end)

sendNetworkEvent(nid, nil, "binary \0 string")
-- given ip and port
sendNetworkEvent("\\\\192.168.0.1 8099", nil, "binary \0 string")
-- broadcast with subnet
sendNetworkEvent("\\\\192.168.0.255 8099", nil, "binary \0 string")
-- UDP broadcast
sendNetworkEvent("*8099", nil, "binary \0 string")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 执行命令`/tip hello`
cmd("/tip hello")

</div>
<div style="float:left;">

```lua
-- 例子1:
cmd("/setblock ~0 ~0 ~1 62")
cmd("/cameradist 12")
cmd("/camerayaw 0")
cmd("/camerapitch 0.5")
-- 例子2:关闭自动等待
set("count", 1)
showVariable("count")
cmd("/autowait false")
for i=1, 10000 do
    _G.count = count +1
end
say("it finished instantly with autowait false", 3)
cmd("/autowait true")
for i=1, 10000 do
    _G.count = count +1
end
```

</div>
<div style="clear:both"/>

### 控制
<div style="float:left;margin-right:10px;">

> 等待`1`秒
wait(1)

</div>
<div style="float:left;">

```lua
-- 例子1:
say("hi")
wait(1)
say("bye", 1)
-- 例子2:等待下一个时钟周期
while(true) do
    if(isKeyPressed("space")) then
        say("space is pressed", 1)
    end
    wait()
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 等待直到``
repeat wait(0.01) until()

</div>
<div style="float:left;">

```lua
-- 例子1:每帧检测一次
say("press space key to continue")
repeat wait(0.01) until(isKeyPressed("space"))
say("started")
-- 例子2:输入为某个变量或表达式
repeat wait(0.01) until(gamestate == "gameStarted")
repeat wait(0.01) until(current_level == 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 重复`10`次``
for i=1, 10 do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
for i=1, 10 do
    moveForward(0.1)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 永远重复``
while(true) do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    moveForward(0.01)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 循环:变量`i`从`1`到`10```
for i=1, 10 do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
for i=1, 10, 1 do
    moveForward(i)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 循环:变量`i`从`1`到`10`递增`1```
for i=1, 10, 1 do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
for i=1, 10, 1 do
    moveForward(i + 1)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 等待直到`status == "start"`为真
repeat wait() until(status == "start")

</div>
<div style="float:left;">

```lua
-- 例子1:
status = "gameStarted"
repeat wait() until(status == "gameStarted")
say("game started")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 如果``那么``
if() then
end

</div>
<div style="float:left;">

```lua
-- 例子1:
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 如果``那么``否则``
if() then
else
end

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    if(distanceTo("mouse-pointer")<3) then
        say("mouse-pointer")
    else
        say("")
    end
    wait(0.01)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 每个`key`,`value`在`data```
for key, value in pairs(data) do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
myData = {
    key1="value1", 
    key2="value2",
    key2="value2",
}
for k, v in pairs(myData) do
    say(v, 1);
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 每个`index`,`item`在数组`data```
for index, item in ipairs(data) do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
myData = {
    {x=1, y=0, z=0, duration=0.5},
    {x=0, y=0, z=1, duration=0.5},
    {x=-1, y=0, z=-1, duration=1},
}
for i, item in ipairs(myData) do
    move(item.x, item.y, item.z, item.duration)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 并行执行``
run(function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
run(function()
    say("follow mouse pointer!")
    while(true) do
        if(distanceTo("mouse-pointer") < 7) then
            turnTo("mouse-pointer");
        elseif(distanceTo("@p") > 14) then
            moveTo("@p")
        end
    end
end)
run(function()
    while(true) do
        moveForward(0.02)
    end
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 执行角色`myself`代码``
runForActor("myself", function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
runForActor("myself", function()
	say("hello", 1)
end)
say("world", 1)
-- 例子2:
local actor = getActor("myself")
local x, y, z = runForActor(actor, function()
    return getPos();
end)
say(x..y..z, 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 结束程序
exit()

</div>
<div style="float:left;">

```lua
-- 例子1:
say("Press X key to exit")
registerKeyPressedEvent("x", function()
    exit()
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 重新开始
restart()

</div>
<div style="float:left;">

```lua
-- 例子1:
say("Press X key to restart")
registerKeyPressedEvent("x", function()
    restart()
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 成为`当前玩家`的化身
becomeAgent("@p")

</div>
<div style="float:left;">

```lua
-- 例子1:成为当前角色的化身
becomeAgent("@p")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置方块输出`15`
setOutput(15)

</div>
<div style="float:left;">

```lua
-- 例子1:
setOutput(15)
wait(2)
setOutput(0)
```

</div>
<div style="clear:both"/>

### 声音
<div style="float:left;margin-right:10px;">

> 播放音符`7`持续`0.25`节拍
playNote("7", 0.25)

</div>
<div style="float:left;">

```lua
-- 例子1:
while (true) do
    playNote("1", 0.5)
    playNote("2", 0.5)
    playNote("3", 0.5)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放背景音乐`1`
playMusic("1")

</div>
<div style="float:left;">

```lua
-- 例子1:播放音乐后停止
playMusic("2")
wait(5)
playMusic()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放声音`击碎`
playSound("break")

</div>
<div style="float:left;">

```lua
-- 例子1:播放音乐后停止
playSound("levelup")
-- 例子2:播放声道
playSound("channel1", "levelup")
wait(0.5)
playSound("channel1", "breath")
-- 例子3:一个声音同时播放多次
for i=1, 80 do
    -- at most 5 at the same time
    playSound("breath"..(i % 5), "breath")
    wait(0.1)
end
-- 例子4:音调和音量不同
for pitch = 0, 1, 0.1 do
   playSound("click", "click", 0, 1, pitch)
   wait(0.5)
end
for volume = 0, 1, 0.1 do
   playSound("click", nil, 0, volume, 1)
   wait(0.5)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 暂停播放声音`击碎`
stopSound("break")

</div>
<div style="float:left;">

```lua
-- 例子1:
playSound("levelup")
wait(0.4)
stopSound("levelup")
-- 例子2:
playSound("levelup1", "levelup")
wait(0.5)
playSound("levelup2", "levelup")
wait(0.3)
stopSound("levelup2")
```

</div>
<div style="clear:both"/>

### 感知
<div style="float:left;margin-right:10px;">

> 是否碰到`方块`
isTouching("block")

</div>
<div style="float:left;">

```lua
-- 例子1:是否和方块与人物有接触
turnTo(45)
while(true) do
    moveForward(0.1)
    if(isTouching(62)) then
        say("grass block!", 1)
    elseif(isTouching("block")) then
        bounce()
    elseif(isTouching("box")) then
        bounce()
    end
end
-- 例子2:
local boxActor = getActor("box")
if(isTouching(boxActor)) then
    say("touched")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置名字为`frog`
setActorValue("name", "frog")

</div>
<div style="float:left;">

```lua
-- 例子1:复制的对象也可有不同的名字
registerCloneEvent(function(name)
    setActorValue("name", name)
    moveForward(1);
end)
registerClickEvent(function()
    local myname = getActorValue("name")
    say("my name is "..myname)
end)
setActorValue("name", "Default")
clone("myself", "Cloned")
say("click us!")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置物理半径`0.25`
setActorValue("physicsRadius", 0.25)

</div>
<div style="float:left;">

```lua
-- 例子1:
cmd("/show boundingbox")
setBlock(getX(), getY()+2, getZ(), 62)
setActorValue("physicsRadius", 0.5)
setActorValue("physicsHeight", 2)
move(0, 0.2, 0)
if(isTouching("block")) then
    say("touched!", 1)
end
setBlock(getX(), getY()+2, getZ(), 0)
wait(2)
move(0, -0.2, 0)
cmd("/hide boundingbox")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置物理高度`1`
setActorValue("physicsHeight", 1)

</div>
<div style="float:left;">

```lua
-- 例子1:
cmd("/show boundingbox")
setBlock(getX(), getY()+2, getZ(), 62)
setActorValue("physicsRadius", 0.5)
setActorValue("physicsHeight", 2)
move(0, 0.2, 0)
if(isTouching("block")) then
    say("touched!", 1)
end
setBlock(getX(), getY()+2, getZ(), 0)
wait(2)
move(0, -0.2, 0)
cmd("/hide boundingbox")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当碰到`name`时``
registerCollisionEvent("name", function(actor)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:某个角色
broadcastCollision()
registerCollisionEvent("frog", function(actor)
    local data = actor:GetActorValue("some_data")
end)
-- 例子2:任意角色
broadcastCollision()
registerCollisionEvent("", function(actor)
    local data = actor:GetActorValue("some_data")
    if(data == 1) then
        say("collide with 1")
    end
end)
-- 例子3:某个组Id
broadcastCollision()
setActorValue("groupId", 3);
registerCollisionEvent(3, function(actor)
    say("collide with group 3")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 广播碰撞消息
broadcastCollision()

</div>
<div style="float:left;">

```lua
-- 例子1:
broadcastCollision()
registerCollisionEvent("frog", function()
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 到`鼠标`的距离
distanceTo("mouse-pointer")

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    if(distanceTo("mouse-pointer") < 3) then
        say("mouse-pointer")
    elseif(distanceTo("@p") < 10) then
        say("player")
    elseif(distanceTo("@p") > 10) then
        say("nothing")
    end
    wait(0.01)
end
-- 例子2:
if(distanceTo(getActor("box")) < 3) then
    say("box")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 计算物理碰撞距离`0`,`0`,`0`
calculatePushOut(0, 0, 0)

</div>
<div style="float:left;">

```lua
-- 例子1:保证不与刚体重叠
while(true) do
   local dx, dy, dz = calculatePushOut()
   if(dx~=0 or dy~=0 or dz~=0) then
      move(dx, dy, dz, 0.1);
   end
   wait()
end
-- 例子2:尝试移动一段距离
for i=1, 100 do
   local dx, dy, dz = calculatePushOut(0.1, 0, 0)
   if(dx~=0 or dy~=0 or dz~=0) then
      move(dx, dy, dz, 0.1);
   end
   wait()
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 提问`你叫什么名字?`并等待回答
local result = ask("你叫什么名字?")

</div>
<div style="float:left;">

```lua
-- 例子1:
ask("what is your name")
say("hello "..tostring(answer), 2)

ask("select your choice", {"choice A", "choice B"})
if(answer == 1) then
    say("you choose A")
elseif(answer == 2) then
    say("you choose B")
end
-- 例子2:
local name = ask("what is your name?")
say("hello "..tostring(name), 2)
-- 例子3:关闭对话框
run(function()
   wait(3)
   ask()
end)
ask("Please answer in 3 seconds")
say("hello "..tostring(answer), 2)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 提问的结果
get("answer")

</div>
<div style="float:left;">

```lua
-- 例子1:
say("<div style='color:#ff0000'>Like A or B?</div>html are supported")
ask("type A or B")
if(answer == "A") then
   say("A is good", 2)
elseif(answer == "B") then
   say("B is fine", 2)
else
   say("i do not understand you", 2)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `空格`键是否按下
isKeyPressed("space")

</div>
<div style="float:left;">

```lua
-- 例子1:
say("press left/right key to move me!")
while(true) do
    if(isKeyPressed("left")) then
        move(0, 0.1)
        say("")
    elseif(isKeyPressed("right")) then
        move(0, -0.1)
        say("")
    end
    wait()
end
-- 例子2:
say("press any key to continue!")
while(true) do
    if(isKeyPressed("any")) then
        say("you pressed a key!", 2)
    end
    wait()
end
-- 例子3:按键列表
-- numpad0,numpad1,...,numpad9

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 鼠标是否按下
isMouseDown()

</div>
<div style="float:left;">

```lua
-- 例子1:点击任意位置传送
say("click anywhere")
while(true) do
    if(isMouseDown()) then
        moveTo("mouse-pointer")
        wait(0.3)
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 鼠标选取
local x, y, z, blockid = mousePickBlock()

</div>
<div style="float:left;">

```lua
-- 例子1:点击任意位置传送
while(true) do
    local x, y, z, blockid, side = mousePickBlock();
    if(x) then
        say(format("%s %s %s :%d", x, y, z, blockid))
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 获取方块`19176` `5` `19209`
getBlock(19176, 5, 19209)

</div>
<div style="float:left;">

```lua
-- 例子1:
local x,y,z = getPos();
local id = getBlock(x,y-1,z)
say("block below is "..id, 2)
-- 例子2:获取方块的Data数据
local x,y,z = getPos();
local id, data = getBlock(x,y-1,z)
-- 例子3:获取方块的Entity数据
local x,y,z = getPos();
local entity = getBlockEntity(x,y,z)
if(entity) then
    say(entity.class_name, 1)
    if(entity.class_name == "EntityBlockModel") then
        say(entity:GetModelFile())
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 放置方块`19176` `5` `19209` `62`
setBlock(19176, 5, 19209, 62)

</div>
<div style="float:left;">

```lua
-- 例子1:
local x,y,z = getPos()
local id = getBlock(x,y+2,z)
setBlock(x,y+2,z, 62)
wait(1)
-- 0 to delete block
setBlock(x,y+2,z, 0)
setBlock(x,y+2,z, id)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 计时器
getTimer()

</div>
<div style="float:left;">

```lua
-- 例子1:
resetTimer()
while(getTimer()<5) do
    moveForward(0.02)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 重置计时器
resetTimer()

</div>
<div style="float:left;">

```lua
-- 例子1:
resetTimer()
while(getTimer()<2) do
    wait(0.5);
end
say("hi", 2)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置为游戏模式
cmd("/mode game")

</div>
<div style="float:left;">

```lua

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置为编辑模式
cmd("/mode edit")

</div>
<div style="float:left;">

```lua

```

</div>
<div style="clear:both"/>

### 运算
<div style="float:left;margin-right:10px;">

> `` `+` ``
() + ()

</div>
<div style="float:left;">

```lua
-- 例子1:数字的加减乘除
say("1+1=?")
wait(1)
say(1+1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `` `>` ``
() > ()

</div>
<div style="float:left;">

```lua
-- 例子1:
if(3>1) then
   say("3>1 == true")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `` `==` ``
() == ()

</div>
<div style="float:left;">

```lua
-- 例子1:
if("1" == "1") then
   say("equal")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 随机选择从`1`到`10`
math.random(1,10)

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    say(math.random(1,100))
    wait(0.5)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `` `并且` ``
() and ()

</div>
<div style="float:left;">

```lua
-- 例子1:同时满足条件
while(true) do
    a = math.random(0,10)
    if(3<a and a<=6) then
        say("3<"..a.."<=6")
    else
        say(a)
    end
    wait(2)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 不满足``
(not )

</div>
<div style="float:left;">

```lua
-- 例子1:是否不为真
while(true) do
    a = math.random(0,10)
    if((not (3<=a)) or (not (a>6))) then
        say("3<"..a.."<=6")
    else
        say(a)
    end
    wait(2)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 连接字符串`hello`和`world`
("hello".."world")

</div>
<div style="float:left;">

```lua
-- 例子1:
say("hello ".."world".."!!!")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 字符串`hello`的长度
(#"hello")

</div>
<div style="float:left;">

```lua
-- 例子1:
say("length of hello is "..(#"hello"));
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `66`除以`10`的余数
(66%10)

</div>
<div style="float:left;">

```lua
-- 例子1:
say("66%10=="..(66%10))
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 四舍五入取整`5.5`
math.floor(5.5+0.5)

</div>
<div style="float:left;">

```lua
-- 例子1:
while(true) do
    a = math.random(0,10) / 10
    b = math.floor(a+0.5)
    say(a.."=>"..b)
    wait(2)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `开根号``9`
math.sqrt(9)

</div>
<div style="float:left;">

```lua
-- 例子1:
say("math.sqrt(9)=="..math.sqrt(9), 1)
say("math.cos(1)=="..math.cos(1), 1)
say("math.abs(-1)=="..math.abs(1), 1)
```

</div>
<div style="clear:both"/>

### 数据
<div style="float:left;margin-right:10px;">

> 变量`score`
score

</div>
<div style="float:left;">

```lua
-- 例子1:
local key = "value"
say(key, 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 新建本地变量`score`为`value`
local key = "value"

</div>
<div style="float:left;">

```lua
-- 例子1:
local key = "value"
say(key, 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `score`赋值为`1`
score = 1

</div>
<div style="float:left;">

```lua
-- 例子1:
text = "hello"
say(text, 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置全局变量`score`为`1`
set("score", "1")

</div>
<div style="float:left;">

```lua
-- 例子1:也可以用_G.a
_G.a = _G.a or 1
while(true) do
    _G.a = a + 1
    set("a", get("a") + 1)
    say(a)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当角色被复制时(`name`)``
registerCloneEvent(function(name)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerCloneEvent(function(msg)
    move(msg or 1, 0, 0, 0.5)
    wait(1)
    delete()
end)
clone()
clone("myself", 2)
clone("myself", 3)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 复制`此角色`(``)
clone("myself")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerClickEvent(function()
    move(1,0,0, 0.5)
end)
clone()
clone()
say("click")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 删除角色
delete()

</div>
<div style="float:left;">

```lua
-- 例子1:
move(1,0)
say("Default actor will be deleted!", 1)
delete()
registerCloneEvent(function()
    say("This clone will be deleted!", 1)
    delete()
end)
for i=1, 100 do
    clone()
    wait(2)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 设置角色的`名字`为`actor1`
setActorValue("name", "actor1")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerCloneEvent(function(name)
    setActorValue("name", name)
    moveForward(1);
end)
registerClickEvent(function()
    local myname = getActorValue("name")
    say("my name is "..myname)
end)
setActorValue("name", "Default")
setActorValue("color", "#ff0000")
clone("myself", "Cloned")
say("click us!")
-- 例子2:改变角色的电影方块
local pos = getActorValue("movieblockpos")
pos[3] = pos[3] + 1
setActorValue("movieblockpos", pos)
-- 例子3:改变电影角色
setActorValue("movieactor", 1)
setActorValue("movieactor", "name1")
-- 例子4:电影方块广告牌效果
local yaw, roll, pitch = getActorValue("billboarded")
setActorValue("billboarded", {yaw = true, roll = true, pitch = pitch});
setActorValue("billboarded", {yaw = true});
-- 例子5:选中特效
-- -1 disable. 0 unlit, 1 yellow border
setActorValue("selectionEffect", -1)
-- 例子6:多角色初始化参数
registerCloneEvent(function(name)
    local params = getActorValue("initParams")
    echo(params)
    say(params.userData)
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 获取角色的`名字`
getActorValue("name")

</div>
<div style="float:left;">

```lua
-- 例子1:
registerCloneEvent(function(msg)
    setActorValue("name", msg.name)
    moveForward(msg.dist);
end)
registerClickEvent(function()
    local myname = getActorValue("name")
    say("my name is "..myname)
end)
setActorValue("name", "Default")
clone("myself", {name = "clone1", dist=1})
clone(nil, {name = "clone2", dist=2})
say("click us!")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 获取角色对象`myself`
getActor("myself")

</div>
<div style="float:left;">

```lua
-- 例子1:
local actor = getActor("myself")
runForActor(actor, function()
	say("hello", 1)
end)
-- 例子2:
local actor = getActor("name1")
local data = actor:GetActorValue("some_data")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> "`string`"
"string"

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `true`
true

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `0`
0

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 获取表`_G`中的`key`
_G["key"]

</div>
<div style="float:left;">

```lua
-- 例子1:
local t = {}
t[1] = "hello"
t["age"] = 10;
log(t)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 空的表{}
{}

</div>
<div style="float:left;">

```lua
-- 例子1:
local t = {}
t[1] = "hello"
t["age"] = 10;
log(t)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 新函数(`param`)``
function(param)
end

</div>
<div style="float:left;">

```lua
-- 例子1:
local thinkText = function(text)
	say(text.."...")
end
thinkText("Let me think");
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 调用函数`log`(`param`)
log(param)

</div>
<div style="float:left;">

```lua
-- 例子1:
local thinkText = function(text)
	say(text.."...")
end
thinkText("Let me think");
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 调用函数并返回`log`(`param`)
log(param)

</div>
<div style="float:left;">

```lua
-- 例子1:
local getHello = function()
	return "hello world"
end
say(getHello())
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 显示全局变量`score`
showVariable("score")

</div>
<div style="float:left;">

```lua
-- 例子1:
_G.score = 1
_G.msg = "hello"
showVariable("score", "Your Score")
showVariable("msg", "", "#ff0000")
while(true) do
   _G.score = _G.score + 1
   wait(0.01)
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 隐藏全局变量`score`
hideVariable("score")

</div>
<div style="float:left;">

```lua
-- 例子1:
_G.score = 1
showVariable("score")
wait(1);
hideVariable("score")
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 输出日志`hello`
log("hello")

</div>
<div style="float:left;">

```lua
-- 例子1:查看log.txt或F11看日志
log(123)
log("hello")
log({any="object"})
log("hello %s %d", "world", 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 输出到聊天框`hello`
echo("hello")

</div>
<div style="float:left;">

```lua
-- 例子1:
echo(123)
echo("hello")
something = {any="object"}
echo(something)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 引用文件`hello.npl`
include("hello.npl")

</div>
<div style="float:left;">

```lua
-- 例子1:文件需要放到当前世界目录下
-- _G.hello = function say("hello") end
include("hello.npl")
hello()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 获取全局表`scores`
gettable("scores")

</div>
<div style="float:left;">

```lua
-- 例子1:
some_data = gettable("some_data")
some_data.b = "b"
say(some_data.b)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 继承表`baseTable`,新表`newTable`
inherit("baseTable", "newTable")

</div>
<div style="float:left;">

```lua
-- 例子1:
MyClassA = inherit(nil, "MyClassA");
function MyClassA:ctor()
end
function MyClassA:print(text)
    say("ClassA", 2)
end

MyClassB = inherit("MyClassA", "MyClassB");
function MyClassB:ctor()
end
function MyClassB:print()
    say("ClassB", 2)
end

-- class B inherits class A
MyClassB = gettable("MyClassB")
local b = MyClassB:new()
b:print()
b._super.print(b)
-- 例子2:
MyClassA = inherit(nil, gettable("MyClassA"));
function MyClassA:ctor()
end
function MyClassA:print(text)
    say("ClassA", 2)
end
local a = MyClassA:new()
a:print()
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 保存用户数据`name`为`value`
saveUserData("name", "value")

</div>
<div style="float:left;">

```lua
-- 例子1:存储本地世界的用户数据
saveUserData("score", 1)
saveUserData("user", {a=1})
local score = loadUserData("score", 0)
assert(score == 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 加载用户数据`name`默认值``
loadUserData("name", "")

</div>
<div style="float:left;">

```lua
-- 例子1:
saveUserData("score", 1)
local score = loadUserData("score", 0)
assert(score == 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 保存世界数据`name`为`value`
saveWorldData("name", "value")

</div>
<div style="float:left;">

```lua
-- 例子1:常用于开发关卡编辑器
-- only saved to disk when Ctrl+S, otherwise memory only
saveWorldData("maxLevel", 1)
local maxLevel = loadWorldData("maxLevel")
assert(maxLevel == 1)
-- 例子2:从指定的文件加载
saveWorldData("monsterCount", 1, "level1")
local monsterCount = loadWorldData("monsterCount", 0, "level1")
assert(monsterCount == 1)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 加载世界数据`name`默认值``
loadWorldData("name", "")

</div>
<div style="float:left;">

```lua
-- 例子1:常用于开发关卡编辑器
-- only saved to disk when Ctrl+S, otherwise memory only
saveWorldData("maxLevel", 1)
local maxLevel = loadWorldData("maxLevel")
assert(maxLevel == 1)
-- 例子2:从指定的文件加载
saveWorldData("monsterCount", 1, "level1")
local monsterCount = loadWorldData("monsterCount", 0, "level1")
assert(monsterCount == 1)
```

</div>
<div style="clear:both"/>
