# Paracraft记忆方块 v1.0

**软件用途：** Paracraft记忆方块被应用在Paracraft 3D动画与编程工具软件中。它利用相似性原理，来由现实驱动电影动画，尝试对智能进行仿真。 
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** NPL语言, C++
**开发完成时间：** 2018年6月1日
**发表日期：** 2018年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 一种新的看待智能的方法
- 电影驱动现实
- 电影触发器

**源代码行数**: 2万  [点击这里查看](Paracraft记忆方块_code)

## 《Paracraft记忆方块》使用手册

## 记忆方块
![image](https://user-images.githubusercontent.com/94537/27119068-ec86c22a-5110-11e7-9afe-65c6855d6aa5.png)


### 单独使用和测试
- 放在电影方块旁边
- 点击一下可加入Working　Memory, 用`0`键激活
- 也可以用红石信号直接激活



# Autonomous Animation Using Time Series

## Design
- When there is no matching position, we can increase the deviation threshold until one is found. 
- Creativity is the result of repetitive thinking plus deviation threshold. 
- We can reward deviation actions (creativity) that lead to familiar situations.  It is like finding the way to a solution. A solution is the activation path to a target situation. 
- Memory blocks are always associated with emotions. 
- Languages are special auxiliary tags. Vocabularies in natural language is rich enough to describe almost everything.  
- When memory block is activated, it is inactive for some time. 
- We match both initial position and speed in movie blocks. Initial speed is calculated as mass point speed at the start of the animation. 
- When player moves to initial position, if target movie block has no initial speed, we will walk to the position and stops before starting the new animation. If the avatar in movie block has speed, we will walk to it and immediately start playing. 

工作原理如下：

包含两个关键模块：
- 电影驱动现实：用电影方块中的内容驱动现实中的虚拟人物
- 电影触发器：通过实现制作好的许多电影方块中的人物的初始空间位置，以及一些其它输入条件，自动启动符合条件的一个电影方块并驱动现实中的虚拟人物。

### 电影驱动现实
用电影方块，驱动同名的真实物体。
例如可以用电影方块控制BMAX模型的门的开和关闭; 控制主角和NPC的真实行为。

### 电影触发器
当现实中的物品与某个电影方块中的物品的初始位置接近时，自动触发电影方块中的内容，并驱动现实物品
这个功能可以用于制作Action & Puzzle Game。

### 研究方向与意义
未来可以形成闭环并加入物理仿真。 用户的行为又可以变成新的时间序列。 最终可以让人物在一个变化的环境中自主运动和生存。

### 道与人工智能的相似关系
尝试建立`道`， `人工智能`， `生物大脑`之间的相似关系。这个是系统，能量层次的相似，已经不是神经元形态的局部相似。
- 道： 在Paracraft的人工智能中，它本质是一个无限大的没有绝对时间起点的时空序列的大集合：Memory。目前认为Hipocampus（神经元密度最高的一个大脑组织，如图）和长期记忆有关。
- 出有： 相似原理：根据注意力（attention），对齐时间起点， 形成Working Memory( in concious mind 意识)， 大脑皮层（面积最大）。
- 归无： Working memory又消亡为没有绝对时间起点的时空序列，long term Memory。Decay parameters。

对于`出有`（形成意识）有一个非常重要的器官是杏核体(如图)，它主要控制人类的情感Emotion。Emotion是为“出有”（形成意识）提供能量（原动力）的重要器官，如果分泌过多，会影响人脑归无的能力。
归无能力出现问题的时候： 人们会反复的思考一个问题， 不停的播放同一段影像。造成重复思考和抑郁症 （例如刚刚看到的人物会反复的做一个动作）。
`归无`（形成无意识下的长期记忆）是人脑的基本工作机制，为了节约能量，相似的内容链接越通常，熵值变小，链接在不断减少， 14-25岁形成了成年人大脑的主要模式。


## Code Architecture
MemoryContext is the entry point for an AI brain. It can be assigned to a player entity to provide memory based actions.

This is like the AI brain of the player entity. 
All long term Memory is stored in memory clips inside memory context. 
Memory clips can be played in parallel but always in one direction.

MemoryContext contains MovieClips, PlayerContext, VisionContext, etc. 

A MemoryClip can be time series of multiple actors. EntityMovieClip can be assigned and used as a read-only data source of memory clip. 
MemoryClip may be activated according to a set of rules or explicitly. 
Once activated, MemoryClip uses MemoryActor to play its memory into the 3d virtual world using the current PlayerContext.

PlayerContext manages major sensor input origin of the current player entity that the memory context belongs to. 

One major component of player context is the VisionContext of the player entity. 
The vision context generates Attention Objects for nearby observed objects in the virtual world. 
Attention Objects are automatically created and expired according to eye position of the player entity.
Two points of attentions are honored, one is the mouse cursor, the other is the block close to the player.

MemoryContext uses Attention Objects to activate the proper memory clip plus a number of other complex rules. 

## The Theory 

## 相似原理在3D动画与编程工具中的应用
我们长期以来致力于将相似原理应用到人工智能领域，让计算机拥有和人脑相似的能力。 

人类的记忆如同计算机中的3D动画；人类的思维如同计算机中的编程。

> 人脑 = 记忆 + 思维 = 3D动画 + 编程 = Paracraft

本节将介绍我们的一个基于相似原理的研发成果Paracraft。Paracraft(创意空间)是一款免费开源的3D动画与编程创作软件。你可以用它创建3D场景和人物，制作动画和电影，学习和编写计算机程序。与成千上万的用户一起学习和分享你的个人作品。

> Paracraft官网： https://paracraft.keepwork.com

### 推荐书籍《Paracraft编程入门》
3D动画与编程工具是推动整个计算机技术向前发展的两个重要动力。电影，游戏，各种图形化软件都需要借助3D动画与编程工具来开发。这里推荐我们的另外一本书籍《Paracraft编程入门》。我们创作这本书时，还有一个备选副标题：相似原理入门教程。**相似性和相似原理**是驱动人类大脑的基本工作原理，Paracraft也可以看成是使用相似原理进行创作的一个工具。我们尽量将相似原理的思想融入到此书中，让你在学会编程的同时对人脑和宇宙万物的工作方式有一定的认知。程序员是虚拟世界的造物主，而虚拟世界与现实世界和人类大脑必然有相似之处。

宇宙内部的相似性从易经开始，到亚里士多德，到后来，它已经被无数科学家研究过。可能是它太普遍，导致我们在使用它时，忽略了它的存在。在人工智能时代，我们有必要将它系统的作为一门独立的理论去研究。人类的大脑由记忆与单向连接构成。记忆就是时间序列，或者说是3D动画，我们很难去修改自己的某个记忆，但是我们可主观的选择一组记忆的时间起点在大脑中同时播放，而背后驱动这些记忆播放的源动力就是我们的思维，或者说是相似性。如果说万有引力让苹果掉到地上，那么相似之力则让我们的大脑可以呈现异彩纷呈的画面并具有逻辑思维。

《Paracraft编程入门》是一本面向7岁以上学生、家长、教师的AI与编程入门教材。Paracraft和魔法哈奇社区自从2009年上线以来，有500多万的注册用户。它们中大多数为小朋友，还有大学生，老师和专业IT人员。 在书中， 第一步：我们要教会你如何随心所欲的创建任意复杂的三维时空序列，也就是动画。我们的网上有成千上万的小朋友自己创建的Paracraft动画片或电影供你学习和参考。第二步：我们要教会你如何用代码去控制这些动画的播放起点，你就像一个导演或音乐指挥家一样让你的动画在你代码的指挥下播放。当你可以随心所欲的掌握这2个技能时，你发现你已经可以像控制自己的思想和梦境一样去控制数字世界中的一切。 

### Paracraft原理介绍
Paracraft(创意空间)是一款免费开源的3D动画与编程创作软件。

> 动画 + 编程 = Paracraft

![blank](https://api.keepwork.com/storage/v0/siteFiles/2675/raw#image.png) 

Paracraft使用NPL语言开发完成。NPL语言全称Neural Parallel Language(神经元并行计算机语言)是本书作者李西峙于2004年为了解决基于相似原理的AI仿真问题研发的一个编程语言，语法与主流编程语言兼容，NPL社区通过github开源了200多万行引擎与NPL类库代码，期待编程爱好者的加入。

> NPL语言官网：https://github.com/LiXizhi/NPLRuntime

Paracraft模拟了人类大脑的工作方式。人脑具有下面几个核心能力：
- 1. 对3D世界的抽象建模能力：我们生活在3D的世界中，而人脑天生对3D世界具有抽象建模能力。最近的研究发现，人脑中存在大量相似的神经元细胞具有和3D几何世界对应的空间关系。
- 2. 对动画的记忆能力：人脑的记忆不是静止的，而是随时间变化的动画片段。这些记忆一但形成，很难被修改。如果将一个人从出生到20岁看到和听到的一切用手机录制下来，大概需要6000GB，约等于15部512GB的手机容量，对计算机来说，并不是很多。
- 3. 对记忆的控制能力：人类的语言与行为其实是对过去记忆的重新剪接与播放。你的大脑仿佛是一个电影导演，指挥着很多动画记忆片段的播放。而驱动记忆重放的主要原则是相似性。

通过Paracraft软件，你可以控制计算机去做类似的这3类事情。在Paracraft中：
- 1. 我们主要用方块构建3D几何世界：人脑中的信号单元也是粒子化的，比如视网膜上有650-700万个视锥细胞可感受颜色和强光；而我们用手机拍摄的照片则由大概2000万个方块点构成。科学家观测到，在人脑深处，当我们从不同角度观察一个熟悉的环境时，某些神经元细胞构成的点阵，也会以相似的模式被依次激活；仿佛在我们脑海深处也有一个相似的由点阵组成的立体世界。这也许可以解释为何孩子对乐高积木特别喜欢，因为这种建模方式与人脑相似。
- 2. 我们用电影方块记录动画：本书中有相当的篇幅和项目是教你如何制作和播放3D动画片段。3D动画（也包括图片，声音）其实是编程的主要素材。我们在各类软件中看到的一切可操作的图形界面，或者游戏中会动的人物都需要先制作成可被计算机调用的动画素材。3D动画就如同我们的记忆一样。没有海量的记忆，人类无法思考；没有大量的动画素材，程序无法呈现。 
- 3. 我们用代码方块控制动画：编程可以看成用逻辑去控制动画的过程。人类的思维也可以看成是通过相似匹配去控制记忆播放的过程。只不过人类还没有搞清楚这个相似匹配的全部规律。但是我们可以用人类语言去描述输入和输出的关系，从而控制在什么情况下，动画从哪里播放，到哪里结束。这种描述方法就是我们要学习的编程。在Paracraft中，我们提出一种简单易学的`面向动画`的编程方式。

总结：Paracraft致力于提供一个面向个人的3D动画与编程创作环境。我们探索了一种类似人脑的建模方式。无论你是小学生还是成年人，通过学习Paracraft，你可以随心所欲的创建3D动画，游戏以及专业计算机软件，并可以独立发布软件到Windows/MAC/Android/iOS等众多平台。

### 相似原理在Paracraft中的应用举例
2004年，我在做基于相似原理的人脑仿真研究时，发明了NPL语言。人脑仿真需要3D动画，因此2005年我又编写了ParaEngine分布式3D游戏引擎，后者逐渐成为了NPL语言的一部分。Paracraft是完全用NPL语言编写的一款创作工具。下面展示几个相似原理在Paracraft中的具体应用。我们无法呈现它的全部功能。其实Paracraft已经是NPL语言的重要开发工具，它包含了电影方块，记忆方块，自主动画系统，视觉系统，代码方块等等，是一个开源了百万行NPL代码的复杂系统。 

**应用1：粒子性**
宇宙是由完全相同的粒子构成的，这既是相似原理成立的原因，也是它的推论。遗憾的是人类用计算机去创建和仿真3D物体所采用的方法很少是基于粒子的。乐高积木算是一种近似的粒子化的建模方式。

在Paracraft中用方块构建3D世界是一种基于粒子的建模方式；相似的，编程也是一种抽象的用代码去建模的方式。其实学习任何知识，都应该具有这种粒子化的建模能力，因为我们的大脑也是粒子化的。

在编程领域有一个最常用的建模方法叫做`面向对象`的建模。Paracraft中的方块，人物，图形界面都可以看成是对象，对象的内部还可以有其它对象。`克里斯多夫亚历山大`在1960-1970年代提出模式语言，直接催生了对象化编程和设计模式的发展，但是他本人更希望将软件看成是生命体，每个生命体有很多`生命中心`构成。

原子，分子，蛋白质，细胞，器官，生命体(人)，社会，地球，太阳系，银河系，宇宙都可以看成是不同层级下的`生命中心`。其中生命体(人)是自然界中最复杂和有序的形态。生命的结构与软件的结构具有相似性。生命的进化与软件的开发过程也具有相似性。在Paracraft中，我们不强调`面向对象`的编程方法，我们强调的是希望用户在一开始就能`将写代码看成是一个粒子化的创造生命的过程`。你创作的程序，可能只是一个单细胞生物，也可能是个庞然大物，但是你创造它的过程需要让它时时刻刻保持`活力`。

**应用2：动画系统**
如下图所示，在Paracraft中，场景和人物角色可以由粒子构成，并且可以在时间轴上做骨骼动画。角色本身也是一种粒子，可以随意的存放在电影方块中，电影方块可以有任意数量的角色，他们的时间起点被对齐后，就形成了动画。我们还可以通过扮演的方式分别录制多个角色动画，再将他们的时间起点对齐。利用这种方式，7-12岁的小朋友就可以制作出任意复杂的3D动画了， 在视频网站上有上万的小朋友，用这样的方式创作出了自己人生的第一部动画片。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3580/raw#image.png'
  ext: png
  filename: image.png
  size: '749566'
  unit: px
  width: '600'
  alignment: left

```

如下图所示，多个电影方块在场景中，串联或并联可以形成长动画（电影）。
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3581/raw#image.png'
  ext: png
  filename: image.png
  size: '351138'
  unit: px
  width: '400'
  alignment: left

```


**应用3：面向动画的编程系统**

人类的大脑是一台超级计算机。而人类智能的本质其实就是通过层层的相似性去控制自己的记忆（动画）。 你可以将我们记忆中的每个词汇，动作，概念，情绪都看成是虚拟角色。这种抽象能力是人类大脑的核心能力， 也是程序员的核心能力。 当我们用计算机去代替人脑解决问题时，我们要能够将问题抽象成虚拟角色，然后用代码控制它们。在Paracraft中，我们提出了一种面向动画的编程模式。你也许听过面向过程的编程和面向对象的编程。 
- 面向过程是一种底层的基于单方向的输入和输出模型的编程模式，人脑中的单个神经元就是按照这种单向的输入输出模型工作的。至今面向过程的编程仍然是被应用最广泛的编程模式。 
- 面向对象是一种建立粒子化层级的编程模式。在面向过程的基础上，它不断的抽象出功能相同的粒子模块，再由这些模块组成更高级的模块。虽然人脑并非按照这种方式在工作，但是人脑中却存在着相似的层级关系。
- 面向动画（记忆）的编程是我们在Paracraft中提出的一种新的编程模式。 

我们可以这样来看待面向动画的编程的合理性：假如计算机处理的输入和输出信息只有动画，也就是多组时间序列，那么我们应该如何编程呢？很显然人脑作为一台超级计算机所面临的情况就是这样的，我们的视觉和听觉输入是动画，我们的肢体动作和语言的输出也是动画，而我们记忆中存储的数据也大都是动画格式的。Paracraft作为一款3D动画工具已经让用户可以随心所欲的创作出基于粒子的3D动画；很自然的，我们需要一种对动画进行编程的方法。 

我们采用在电影方块的旁边放置一个代码方块的方式来控制其中的动画。而我们的代码主要用来控制电影方块中角色的动画播放的时间起点，场景中所有的代码方块以并行的方式运行。我们用这种方法制作了成百上千的小游戏，目前还没有遇到不能编写的程序，同时它让一个游戏的代码量变得十分的少，而且我们结合了图块化编程，让7岁的用户就可以掌握。 

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

如上图所示，代码方块永远控制的是离它最近的电影方块。在真实的3D世界中，我们会看到有很多代码方块组成的程序。如下图所示，蓝色框中的三个代码方块控制的都是蓝色框中的电影方块，因为他们三个离电影方块最近；红色框中的代码方块控制的是红色框中的电影方块。图中左侧是一个拉杆开关，打开时代码方块亮起，里面的逻辑才生效。
 
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

如下图所示，点击代码方块，我们可以对它进行图形化或文本化的编程，我们提供了丰富的指令去控制电影中的动画，比如`play(10, 1000)`代表播放从10到1000毫秒的一段动画。 

```@BigFile
bigFile:
  src: 'https://biz.keepwork.com/public/img/%E4%BC%98%E5%8A%BF22.cfb9432e.jpg'
  ext: png
  filename: image.png
  size: '221188'
  unit: px
  width: 550
  alignment: left

```


**应用4：动画方块与动画识别**

如下图所示，在Paracraft中用户可以用方块搭建任意模型，并在它附近放置一个动画方块，系统会识别出它像一头牛，并自动赋予了牛的骨骼和动画，自动变成了一个会行走和摇尾巴的四足动物。 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/1019/raw#image.png'
  ext: png
  filename: image.png
  size: '221188'
  unit: px
  width: 350
  alignment: left

```

动画方块初步实现了对粒子的静态相似匹配过程，并且能够将记忆库中的任意动画（骨骼）赋予任意的角色模型。 


**应用5：记忆方块**
Paracraft中的记忆方块是一套更复杂的相似匹配与自主动画系统。记忆方块和代码方块类似，总是会触发与之相邻的电影方块。所不同的是，代码方块用开关和编程的方式控制电影方块中的时间序列，而记忆方块则通过主角附近的输入，以及它本身所处的状态来决定是否会播放。

如下图所示，人物会通过视觉观察周围的环境，并自动触发记忆中的动画，并与真实环境发生互动。例如中间图中人物抓住绳子的动作来自用户用记忆方块和电影方块制作的一段动画。人脑也是利用相似原理，将我们过去的静态记忆重新对齐时间起点，并播放和作用于物理仿真环境的。

![](https://api.keepwork.com/storage/v0/siteFiles/2983/raw#image.png) 

记忆方块是一个还在不断开发中的模块，我们在其中仿真了人类的注意力，长期与短期记忆，神经元的不应期（一种避免重复播放，类似人类强迫证的保护机制），情绪（一种与注意力相关的无处不在的能量维度），时空相似匹配（基于粒子时间序列的快速匹配算法）等。

**应用6：Paracraft在教育中的应用**
目前，我们有一个团队，致力于将Paracraft应用到青少年儿童的编程教育中。学习计算机语言和学习其它自然语言，如中文和英文，是一样的，你要不停的使用它，创造出自己的作品。其实人类学习任何技能都是一样的，因为教育的本质就是让人保持思考和一直有事可做。因此，我们还为Paracraft开发了一个学习平台，叫做KeepWork，官网是：

```
https://keepwork.com 
```

KeepWork有2个字面意思：
- 保持(keep)有事可做(work): 人不能放弃工作和创作，大人小孩都一样。这个是教育的本质。
- 保存(keep)作品(work): 我们保存了你的所有作品和更改历史。作品是未来教育的重要评估方式，不再需要考试的分数。

只要你安装了Paracraft，后面的一切就可以教给孩子自己去探索、学习和创造了。而你只需要观察孩子是否一直保持有事可做即可。

目前国内的编程教育体系不重视3D动画，缺乏合适的工具，最终学生只掌握了编程的思维，无法真正做到随心所欲的创作计算机作品。

控制机器去做梦（动画）与思考（编程）是未来人类的必备技能。传统的教学模式无法满足高效的计算机普及教育。我们通过工具和教学模式的创新：让每个学生都有当老师的机会：结伴学习，相互启发，激发兴趣，创造出个人作品。

我们相信让更多的儿童从小就掌握相似原理，并学会使用Paracraft创作动画或游戏，将能为社会培养更多的高科技人才。

