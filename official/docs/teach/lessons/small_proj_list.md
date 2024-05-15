
<style>
@media(max-width: 800px){.markdown-body h2 { font-size: 20px; }
                         .markdown-body h1{font-size: 30px;}  
                         .markdown-body h1::before{width:20px;padding-right:0.8em;} 
                         .markdown-body h1::after{width:50px;margin-left:0.5em;} 
  }
div.markdown-body{
  /*background:url("https://api.keepwork.com/storage/v0/siteFiles/497/raw")no-repeat top; 
  border:2px dashed rgba(230,197,140,1);
  box-shadow:0px 9px 26px 0px rgba(215,112,50,0.28);*/
  padding-left:1.5em;
  padding-right:1.5em;
  margin-top:2em;
  margin-bottom:2em;
  }
.markdown-body h2{
  text-align:center;
  padding:1em; 
  border-bottom:0px;
  }
  
h4{
  color:#FF7800;
  }
h1{
   text-align:center;
   align-items: center;
   justify-content: center;
   display: flex;
   padding:1em; 
  }
h1::before{
    content: "";
    width: 40px;
    background: url(https://api.keepwork.com/storage/v0/siteFiles/499/raw)no-repeat;  
    height: 50px;
    display: inline-block;
    padding-right:1em;
  }
h1::after{
    content: "";
    width: 40px;
    background: url(https://api.keepwork.com/storage/v0/siteFiles/500/raw)no-repeat;  
    height: 50px;
    display: inline-block;
    /*padding-left:1em;*/
    margin-left:1.2em;
    margin-bottom:-1em
  }  
div.teacher_odd{  
padding:0.5em;  
padding-bottom:5px; 
padding-left:2em;   
background:rgba(59,164,255,0.1);
border-radius:15px;
  position: relative;
  }
div.teacher_odd::before{
  content: "";
  position:absolute;
  left:0px;
  top:0px;
  display: inline-block;
  border-top-left-radius:15px;
  border-bottom-left-radius:15px;
  width: 10px;
  height: 100%;
background:rgba(59,164,255,1);  
}  
  
div.teacher_even{  
padding:0.5em;  
padding-bottom:5px; 
padding-left:2em;   
background:rgba(240,202,98, 0.1);
border-radius:15px;
  position: relative;
  }
div.teacher_even::before{
  content: "";
  position:absolute;
  left:0px;
  top:0px;
  display: inline-block;
  border-top-left-radius:15px;
  border-bottom-left-radius:15px;
  width: 10px;
  height: 100%;
background:rgba(240,181,98,1);
}    
  
/*hand pointing for the expanded content*/  
span.click_to_display {
    color: #008B8B;
    cursor:pointer;
    font-weight: 900;
    font-size: 1.1em;
}
span.hand_left{
  width:20px;
  height:20px;
  padding:20px;
  background:url("https://api.keepwork.com/storage/v0/siteFiles/443/raw")no-repeat center;
  cursor:pointer;
  background-size: 25px 25px;
}
span.hand_down{
  display:none;
  width:20px;
  height:20px;
  padding:20px;
  background:url("https://api.keepwork.com/storage/v0/siteFiles/444/raw")no-repeat center;
  cursor:pointer;
  background-size: 25px 25px;
 }  
  
span.click_to_hide {
    color: #008B8B;
    cursor:pointer;
    font-weight: 900;
    font-size: 1.1em;
}
  .inline_display_title{
    color: #008B8B;
    font-weight: 900;
    font-size: 1.1em;
    margin: 0.5em;
    margin-left: 0em;
}
  
div.click_to_hide {
    color: #008B8B;
    cursor:pointer;
}
div.inline_display{
  display:none;
  z-index:1000;
  border:dashed;
  padding:1em;
  margin:1em;
  background-color:#ffd699;
}
div.annot_display{  
  z-index:1000;
  border:dashed;
  padding:1em;
  margin:1em;
  background-color:#ffe0b3;
}  
  .title{
   text-align: center;
    padding: 1em;
    border-bottom: 0px;
    /* text-align: center; */
    display: flex;
    align-items: center;
    justify-content: center;
  }
.fake-title-line{
    background: url(https://api.keepwork.com/storage/v0/siteFiles/501/raw) no-repeat;
    height: 50px;
    display: inline-block;
    padding-right: 1em;
    flex: 1;
    width: 100%;
    background-size: 70%;
    background-position: left center;
    /* padding: 0 5em; */
    max-width: 120px;
    flex: 1;
  }
  .fake-title-line.line-after{
  transform: rotate(180deg)
  }
  .fake-title-quote{
    background: url(https://api.keepwork.com/storage/v0/siteFiles/511/raw) no-repeat ;    
    margin-top:-20px;
    height: 100px; 
    width:5px;
    display: inline-block;   
    padding-right: 1em;
    flex: 1;
    
    background-size: 70%;
    background-position: left center;
    /* padding: 0 5em; */
    max-width: 5px;
    flex: 1;
  
  }
  .fake-title-quote.quote-after{
  transform: rotate(180deg);
  margin-bottom:-20px;
  }
</style>



# 小项目

小项目是你在学习Paracraft时可以做的事情。这些事情都可以帮助你去增加对Paracraft的了解和对相关技能的掌握。你可以按照自己的需求去尝试。我们大概分了几个不同难易的等级，但难易划分仅供你参考。很多项目你可以先根据自己的需要做快速的尝试，获取你现在能吸收的知识。以后感觉这些项目又有帮助时，可以再深入继续尝试。

我们都是自学者，如何使用下面的资源和小项目列表？来了解一下[自主学习口诀](/official/paracraft/selflearning-poem)吧。


## 资源
首先大家应该熟悉几个资源：

#### 文档
https://keepwork.com/official/docs/index

大家在学习的过程中要多学会查阅官方文档。甚至可以先把官方文档大致通读一遍，不需要都看懂，只要大概知道文档里有什么即可。

#### 推荐用户作品

我们有大量的优秀用户作品，包括动画电影和小游戏，并且在Paracraft里就可以<span class="click_to_display" id="user-works">**访问**<span class="hand_left"></span><span class="hand_down"></span></span></span>。


<div class="inline_display" id="user-works_display">
<div class="click_to_hide">隐藏 >> </div>
<div class="inline_display_title">推荐用户作品</div>
  在Paracraft这个界面上有推荐用户作品的入口：
  <img src="https://api.keepwork.com/storage/v0/siteFiles/5147/raw#image.png" height="auto" width="100%"/>

    
   点击后是这个窗口：
  <img src="https://api.keepwork.com/storage/v0/siteFiles/5047/raw#image.png" height="auto" width="100%"/>
  

  

  
   

  
</div> 

#### 免费课程

分别在三个地方你可以访问到我们的免费课程：

- <span class="click_to_display" id="free-lessons">**Paracraft里**<span class="hand_left"></span><span class="hand_down"></span></span></span>


<div class="inline_display" id="free-lessons_display">
<div class="click_to_hide">隐藏 >> </div>
<div class="inline_display_title">Paracraft免费课程</div>
 在Paracraft这个界面上有网课的入口，如下图： <br/>
  
 <img src="https://api.keepwork.com/storage/v0/siteFiles/5149/raw#image.png" height="auto" width="100%"/>
  
  
  则会如下窗口出现。里面有许多可以选择的课程。点击某个课程则进入该课程的世界。
  <img src="https://api.keepwork.com/storage/v0/siteFiles/5012/raw#image.png" height="auto" width="100%"/>
 
  
  
  
 


  
  </div>


- [网页版](https://keepwork.com/kecheng/cs/all)
  这里的一些课程与上面Paracraft里的课程内容是差不多的。个别课程内容的质量有待提高，请注意选用。

- [公开课](https://study.163.com/course/introduction.htm?courseId=1209451840)
  这是河马老师在网易云课堂上开设的公开课。都是视频的形式，河马老师带着大家一步步学Paracraft。


#### 编程小世界

[项目536](https://keepwork.com/pbl/project/536)里有大量的小游戏，分别从易到难的顺序。可以一个个尝试过来，打开代码方块看看其中的代码。

#### 编程小示例

[项目530](https://keepwork.com/pbl/project/530)里有大量代码用例。供有一些编程经验的人快速了解Paracraft里代码可以做的事情。

#### 动画一小时

[项目1149](https://keepwork.com/pbl/project/1149)里有大量的动画相关的小项目，从浅入深的学习动画制作。

#### AI课程



## 小项目列表

#### 小白们

- **新手上路视频**
  看完[这个页面](https://keepwork.com/official/docs/videos/new_user_video)的视频，就可以学会Paracraft的安装以及基本操作。你可以看一开始那个26分钟的视频，也可以看下面的分段视频。内容是一样的。

- **F1帮助**
  在Paracraft里按下F1, 会有很多作为新手教程的小项目供你来完成。<span class="click_to_display" id="f1">**详细**<span class="hand_left"></span><span class="hand_down"></span></span></span>
  
- **搭建筑**
  如花园，塔，书房，学校等


- **学习批量操作**
  [学习批量操作](https://keepwork.com/kecheng/cs/lv0/batch_operations)，可以快速的搭建场景

- **观看他人优秀作品**
  浏览欣赏[推荐用户作品](https://keepwork.com/official/docs/teach/lessons/small_proj_list#%E6%8E%A8%E8%8D%90%E7%94%A8%E6%88%B7%E4%BD%9C%E5%93%81)


<div class="inline_display" id="f1_display">
<div class="click_to_hide">隐藏 >> </div>
<div class="inline_display_title">F1新手教程</div>
 在Paracraft里按下F1, 会出来如下图的窗口，其中会有很多作为新手教程的小项目供你来完成。 
  
 <img src="https://api.keepwork.com/storage/v0/siteFiles/5006/raw#image.png" height="auto" width="100%"/>


</div>  

- **玩创意几何**
  创意几何是训练空间思维能力的小游戏。项目id是1212

- **玩boxboy小游戏**
  boxboy是个训练观察能力和逻辑推理能力的小游戏。项目id是712
  
  
- **玩推理大师小游戏**
  推理大师是个训练观察能力和逻辑推理能力的小游戏。项目id是677
  
- **玩解密小游戏** 
  [推荐用户作品](https://keepwork.com/official/docs/teach/lessons/small_proj_list#%E6%8E%A8%E8%8D%90%E7%94%A8%E6%88%B7%E4%BD%9C%E5%93%81)里有很多解密小游戏。去玩玩吧。
  
  
- **观看公开课**  
  观看河马老师的[公开课](https://study.163.com/course/introduction.htm?courseId=1209451840)
  
- **观看更多教学视频**
  观看文档里的更多教学视频

- **阅读浏览文档**  
  可以把文档大致看一遍。碰到看不懂的地方没有关系。看完后大概就知道文档里有什么内容，什么时候你需要去查阅文档。#学会使用文档#
  

- **玩动画一小时**
  [项目1149](https://keepwork.com/pbl/project/1149)
  
- **上AI课**  

#### 进阶

- **过山车**
  孩子们都爱玩的[过山车](/official/roller_coaster/index)。去看看如何搭建惊险好玩的过山车，有其他小朋友的过山车作品可以玩哦。

- **代码方块基础**
  请阅读[这门网课](https://keepwork.com/kecheng/cs/codeblock/codeblock)。可以把其中的几个视频看了，文字如何看不明白没有关系。
- **一个代码方块【编程】**
  [项目536](https://keepwork.com/pbl/project/536)
- **两个代码方块【编程】**
  [项目536](https://keepwork.com/pbl/project/536)
- **迷宫（10岁以上）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到迷宫小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/maze)进行实现。10岁以上请尝试直接使用代码。
- **乒乓球（10岁以上）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到乒乓球小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/pingpong)进行实现。10岁以上请尝试直接使用代码。
- **钢琴（10岁以上）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到钢琴小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/piano)进行实现。10岁以上请尝试直接使用代码。
  
- **孙子兵法（10岁以上）【编程】**  
[项目19405](https://keepwork.com/pbl/project/19405)该系列闯关游戏可以帮助练习写代码。编程需要大量的打字，需要非常熟悉键盘和代码。所以你可以通过这个闯关游戏来专门练习敲代码的能力。以最快的速度通过所有关卡，从而克服对敲代码的恐惧心理。

- **征程（10岁以上）【编程】**  
[项目73139](https://keepwork.com/pbl/project/73139)该系列闯关游戏可以帮助练习写代码。编程需要大量的打字，需要非常熟悉键盘和代码。所以你可以通过这个闯关游戏来专门练习敲代码的能力。以最快的速度通过所有关卡，从而克服对敲代码的恐惧心理。

- **迷宫（10岁以下）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到迷宫小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/maze)进行实现。10岁以下的如果直接使用代码有困难，可以使用条块式编程。
- **乒乓球（10岁以下）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到乒乓球小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/pingpong)进行实现。10岁以下的如果直接使用代码有困难，可以使用条块式编程。
- **钢琴（10岁以下）【编程】**
  [项目536](https://keepwork.com/pbl/project/536)里找到钢琴小游戏，并参考该[网课](https://keepwork.com/kecheng/cs/codeblock/piano)进行实现。10岁以下的如果直接使用代码有困难，可以使用条块式编程。




- **玩BlockBot小游戏【编程】**
  BlockBot小游戏可以帮助你训练如何控制指令执行顺序，是编程的基础技能之一。BlockBot小游戏的项目id是709。
- **玩人力资源游戏【编程】**
  人力资源游戏是训练对编程中最常用的数据结构列表的操作的。人力资源游戏的项目id是1562。
 

- **打字练习**
  进入[打字练习项目](https://keepwork.com/pbl/project/867/)，项目id是867。完成里面的打字任务（左边四个任务）。如<span class="click_to_display" id="tasks-left">**下图**<span class="hand_left"></span><span class="hand_down"></span></span></span>


<div class="inline_display" id="tasks-left_display">
<div class="click_to_hide">隐藏 >> </div>
<div class="inline_display_title">打字练习项目左边四个任务</div>

 
  <img src="https://api.keepwork.com/storage/v0/siteFiles/5139/raw#image.png" height="auto" width="100%"/>
 
  
  </div>
  
 



- **打字练习进阶**
  完成上面的打字练习任务后，创建自己的关卡，即右边的两个任务。如<span class="click_to_display" id="tasks-right">**下图**<span class="hand_left"></span><span class="hand_down"></span></span></span>


<div class="inline_display" id="tasks-right_display">
<div class="click_to_hide">隐藏 >> </div>
<div class="inline_display_title">打字练习项目右边两个任务</div>

 
  <img src="https://api.keepwork.com/storage/v0/siteFiles/5141/raw#image.png" height="auto" width="100%"/>
  
 
 

  
  </div>
  
  
- **吃青蛙的怪物【编程】**
  [项目536](https://keepwork.com/pbl/project/536)
- **跟屁虫【编程】**
  [项目536](https://keepwork.com/pbl/project/536)
- **飞行的小鸟【编程】**  
  [项目694](https://keepwork.com/pbl/project/694)，请参考[这个网课](https://keepwork.com/kecheng/cs/codeblock/flappybird)

- **全局变量**
  [项目536](https://keepwork.com/pbl/project/536)，请参考[这个网课](https://keepwork.com/kecheng/cs/codeblock/ask_and_global)

- **用户界面UI，图层字幕演员**
  [项目536](https://keepwork.com/pbl/project/536)，请参考[这个网课](https://keepwork.com/kecheng/cs/codeblock/gui)
- **双重机关与事件**
  [项目536](https://keepwork.com/pbl/project/536)，请参考[这个网课](https://keepwork.com/kecheng/cs/codeblock/lock_and_event)


- **查看代码方块里各指令下的范例【编程】**
  适合已经完成了前面几个编程小项目的同学。建议把各指令以及相关范例都大致的看一遍，了解Paracraft的代码都可以做哪些事情。
- **项目530里有大量代码用例【编程】**
  适合已经完成了前面几个编程小项目的同学。如果想更多的了解Paracraft里代码可以做的事情，可以看看项目530里的许多用例。建议先大致浏览一遍，了解各大概，知道Paracraft都可以做什么事。有大概的了解，需要使用的时候能够快速的查到就可以。



- **查阅《自我检测表》**
  阅读[《自我检测表》](https://keepwork.com/official/docs/teach/lessons/paracraft_exams)，看看相关的知识机构里自己有哪些还没有掌握的。

- **BMAX模型制作：汽车**

- **BMAX模型制作：我们来做个虫子**  
  请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_bmax_2)，做出一样的虫子出来 
- **动画电影制作：各种各样的虫子**
  上面我们按照[这个网课](https://keepwork.com/kecheng/cs/lv0/case_bmax_2)，做出了一个虫子出来。这次我们试着用Paracraft来制作个不同的虫子吧！你想做什么虫子？蝗虫？蜻蜓？蝴蝶？蟋蟀？还是你自己想象出一个没有人见过的虫子出来？让我们来看看你做出来的虫子吧！ 
- **动画电影制作：会动的虫子**
  按照[这个网课](https://keepwork.com/kecheng/cs/lv0/case_bmax_2)里所教的方法，让你的虫子动起来！
- **场景搭建：游泳池**
  项目id是2639。请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_1)来实现。
- **动画电影制作：夏天游泳**
  项目id是2639。请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_1)来实现。
- **角色和动作**
  请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_3)做出让角色做操的动作
- **BMAX模型制作：我们来做个吉他**
  项目id是2763。请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_bmax_1)来实现。
- **动画电影制作：弹吉他的女孩【骨骼】**
  项目id是2763。请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_bmax_1)来实现。
- **行走的大象与镜头震动效果【骨骼】**
  请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_5)，来实现一个行走的大象，并实现镜头震动的效果。

- **制作简易动画开头【骨骼】**
  请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_2)，制作一个简易的动画开头。

- **玩绘图程序小游戏**
  项目id是852
  
  
  

- **玩曼德勃罗特集**
  项目id是936


- **阅读参考资料**
  阅读文档里的参考资料：命令列表，物品列表，功能列表
  
  
- **我们来认识几个朋友**  
  给大家介绍几位小朋友，大家关注一下他们，看看我们能从他们的作品里学到什么。
  [lixizhi](https://keepwork.com/u/lixizhi)，[qizai](https://keepwork.com/u/qizai)， [pcljj](https://keepwork.com/u/pcljj)， [ryan](https://keepwork.com/u/ryan),[qq965555](https://keepwork.com/u/qq965555),[eric](https://keepwork.com/u/eric), [dreamanddead](https://keepwork.com/u/dreamanddead) [offcial](https://keepwork.com/u/official), [rainy](https://keepwork.com/u/rainy), [wolf2018](https://keepwork.com/u/wolf2018), [ben666](https://keepwork.com/u/ben666)
  

#### 高阶


- **坦克大战【编程】**
  项目id是708，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。
- **赛车小游戏【编程】**
  项目id是1598，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。


- **打地鼠【编程】**
  在[项目536](https://keepwork.com/pbl/project/536)中找到这个游戏，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。
- **接金币【编程】**
  在[项目536](https://keepwork.com/pbl/project/536)中找到这个游戏，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。
- **跳一跳【编程】**
  在[项目536](https://keepwork.com/pbl/project/536)中找到这个游戏，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。
- **弹弹堂【编程】**
  在[项目536](https://keepwork.com/pbl/project/536)中找到这个游戏，玩这个游戏，并研究其代码，尝试对代码进行改进，做出你的升级版本出来。

- **动画模型方块**
  请参考[这个网课](https://keepwork.com/kecheng/cs/lv0/case_animations_4)，了解动画模型方块的功能
- **BMAX骨骼：扭动的蛇**
  [项目853](https://keepwork.com/pbl/project/853/)







<script type="text/javascript"> 
  var click_to_displays = document.getElementsByClassName('click_to_display');
  for(var i = 0; i < click_to_displays.length; i++) {
    (function(index) {
      click_to_displays[index].addEventListener("click", displayDiv);
    })(i);
  }  
  function displayDiv() {
      val = this.getAttribute("id");
      display_elem = document.getElementById(val+'_display');
      display_elem.style.display='block';
      clicked_elem = document.getElementById(val);
      clicked_elem.getElementsByClassName('hand_down')[0].style.display = 'inline';
      clicked_elem.getElementsByClassName('hand_left')[0].style.display = 'none';
      clicked_elem.removeEventListener('click', displayDiv);                                       
      clicked_elem.addEventListener("click", trigger_hide);
  }
                                              
  function trigger_hide(){
      val = this.getAttribute("id");                                        
      click_to_hide_elem = document.getElementById(val+'_display').getElementsByClassName('click_to_hide')[0];                   click_to_hide_elem.click();                                     
  }
  
  var click_to_hides = document.getElementsByClassName("click_to_hide");
  for(var i = 0; i < click_to_hides.length; i++) {
      (function(index) {
        click_to_hides[index].addEventListener("click", hideDiv);
      })(i);
  }                                         
  function hideDiv() {
       parent = this.parentElement
       parent.style.display='none'; 
       val = parent.getAttribute("id");
       val = val.substring(0, val.length-8);  
       to_click_elem = document.getElementById(val);
       to_click_elem.removeEventListener('click', trigger_hide);
       to_click_elem.addEventListener("click", displayDiv);
       to_click_elem.getElementsByClassName('hand_down')[0].style.display='none';
       to_click_elem.getElementsByClassName('hand_left')[0].style.display='inline';
     
  }
</script> 