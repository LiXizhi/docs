##  **第三课 创建飞翔的小鸟场景** 



<details style="background-color:white" open>
  <summary>项目介绍</summary><p>
 
  ![](https://api.keepwork.com/ts-storage/siteFiles/24073/raw#1667444121831lQLPJxbWeiOxUz7NA57NBQCw41f7G21VJ7gDYHcxPgCFAA_1280_926.png) 
  


  你有玩过电脑游戏吗？
王者荣耀？赛车？坦克大战？
当你在玩游戏的时候，心里有没有想过，这些游戏是怎么做出来的？为什么通过键盘鼠标就可以控制游戏中的角色呢？
今天我们一起来挑战一下，从零开始创作一款《飞翔的小鸟》的小项目吧！
《飞翔的小鸟》是一款曾经比较火热的小游戏，游戏规则非常简单，玩家只需通过点击键盘，控制小鸟避开管道等障碍物即可继续前进，前进过程中不能碰到管子哦，然后比比谁能飞的更远。操作虽然简单，但是非常具有挑战。
让我们开始今天的挑战吧！
  
### 学习目标
  - 场景的搭建；
  - 小鸟模型的导入和设置；

### 上课步骤
1. 打开课程学习链接（手机微信和电脑都可以）
2. 同时打开帕拉卡客户端，并打开上节课的作品
3. 观看课程视频
4. 边看视频教程边创作
5. 在客户端中发布作品，把作品id发给老师
6. 完成微信群内的随堂测试
  
</p></details>


<div style="text-align:center;margin:40px">
  
   
</div>

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24060/raw#1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  ext: png
  filename: 1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  size: '82680'
  unit: '%'
  percent: 10

```
<div style="text-align:center;margin:40px">
  
   
</div>

### 步骤1：搭建游戏场景，设置障碍物



<video width="100%" oncontextmenu="return false;" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
   <source src="https://api.keepwork.com/ts-storage/siteFiles/24156/raw#1668066910600飞翔的小鸟1.1.mp4" type="video/mp4" />
   

  你的浏览器不支持播放
</video>
<div id="play-btn" class="video-controls"></div>

<style>
video::-webkit-media-controls-fullscreen-button {
    display: none;
}

#play-btn::after {
  content:url("https://www.wonderplugin.com/download/playbutton.png");
  z-index:999;
  position:absolute;
  top:50%;
  left:50%;
  margin-left:-32px;
  margin-top:-32px;
}

</style>





<div style="text-align:center;margin:40px">
  
   
</div>

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24060/raw#1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  ext: png
  filename: 1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  size: '82680'
  unit: '%'
  percent: 10

```
<div style="text-align:center;margin:40px">
  
   
</div>

### 步骤2：创建可拖动的小鸟和鸟巢模型

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24157/raw#1668066997635飞翔的小鸟1.2.mp4
  ext: mp4
  filename: 1668066997635飞翔的小鸟1.2.mp4
  size: 10041111
          
```




<div style="text-align:center;margin:40px">
  
   
</div>

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24060/raw#1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  ext: png
  filename: 1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  size: '82680'
  unit: '%'
  percent: 10

```
<div style="text-align:center;margin:40px">
  
   
</div>

### 步骤3：给模型命名并调整属性

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24158/raw#1668067036553飞翔的小鸟1.3.mp4
  ext: mp4
  filename: 1668067036553飞翔的小鸟1.3.mp4
  size: 9291176
          
```




<div style="text-align:center;margin:40px">
  
   
</div>

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24060/raw#1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  ext: png
  filename: 1667388574396lQLPJxbV7Wl0EJXNBqjNA0CwExzyNb1Y7v8DX5CgEABwAA_832_1704.png
  size: '82680'
  unit: '%'
  percent: 10

```
<div style="text-align:center;margin:40px">
  
   
</div>

## 创作自己的作品
  
要求：
1. 打开昨天创作的作品世界；
2. 开启多人联机模式；
3. 上传分享作品；
4. 将作品ID提交在群里，完成作业打卡。
5. 邀请爸爸妈妈一起玩五子棋；
 

<details style="background-color:white">
  <summary>创作百科</summary><p>

#### 电脑基础知识

计算机，俗称电脑，它是20世纪最先进的科学技术发明之一，对人类的生产活动和社会活动产生了极其重要的影响。计算机是由硬件系统和软件系统两部分组成的。电脑的主要硬件有主机、显示器、键盘、鼠标等。硬件设备又分为输入设备和输出设备。鼠标与键盘是计算机最常用且非常重要的输入设备。键盘由数字键区、打字键区、功能键区和编辑控制区组成，3D动画编程软件帕拉卡中常用的三大功能键：Shift、Alt、 Ctrl、组合快捷键以及功能键。鼠标则是计算机的一种外接输入设备，也是计算机显示系统纵横坐标定位的指示器，因形似老鼠而得名，英文名"Mouse"，鼠标使计算机的操作更加简便快捷。鼠标由左键、右键、滚轮（中键）组成，使用方式：单击-点击一下按键；双击-快速点击两下按键；长按-按住按键不放手；拖拽-长按按键的同时移动鼠标。
  

  
  
  ![](https://api.keepwork.com/ts-storage/siteFiles/23197/raw#1665646249737image.png) 
  

#### 快速创作技巧
鼠标右键：建造方块/触发机关
鼠标左键:删除普通方块，长按删除交互方块（部分方块需要长按鼠标左键才能删除）

#### 调整活动模型的方向和大小
鼠标右键点击活动模型，拖动蓝色圆环可以改变方向，推动三轴上的小方框可以改变大小
  


    ![](https://api.keepwork.com/ts-storage/siteFiles/23198/raw#1665646310768image.png) 
  
  
  

