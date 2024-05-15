## 代码方块教学1


```@Project
styleID: 1
project:
  projectId: 536
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

**代码方块教学视频**

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/18136/raw#1604203394908codeblock1_small.mp4
  ext: mp4
  filename: 1604203394908codeblock1_small.mp4
  size: 34684197
          
```

[在腾讯视频播放](https://v.qq.com/x/page/r07132jnxho.html)


**1 理论**
> 思考：游戏是由什么组成的？

答案： 游戏 = 动画 + 程序

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

```javascript
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

```javascript
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

```javascript
registerClickEvent(function()
  say('hello!', 2)
  moveForward(1, 0.5)
end)
```

registerClickEvent代表注册点击事件，当演员被点击时，他会先说hello两秒钟，然后`向前走1格，在0.5秒内`，我们运行一下这段代码，点击演员，他会先说hello两秒，然后向前运行1格。

现在我们将刚才学过的内容全部连起来做一个小游戏，右键单击代码方块，大家根据刚才学过的内容，能不能猜出这段代码的含义？

```javascript
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