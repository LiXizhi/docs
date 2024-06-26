# 《100个编程游戏》策划与思路

<style>details{  border:dashed;  padding:1em;  margin-top:0.5em;  margin-bottom:0.5em;  background-color:#ffd699;} details summary{ cursor:pointer;}</style> 

<details>
  <summary>前言 </summary>

《100个编程游戏》策划与思路
作者：李西峙 等
出版社：XXX

  
## 前言
  
本书中的所有项目需要下载安装帕拉卡Paracraft，Paracraft是一款免费开源的3D动画与编程创作工具。
下载地址: https://paracraft.cn/ 

本书是《创意空间》配套丛书，《创意空间》是Paracraft从创立之初就提出的基于自主学习的产品与教学理念。
随着科学技术的发展，未来老师的角色也在发生着变化。
  
![](https://api.keepwork.com/ts-storage/siteFiles/21114/raw#1631674812942image.png) 
  
- 教育1.0： 老师是信息的单向输出者；学生是被动的接受者
- 教育2.0： 老师是指挥家、CEO；学生通过合作解决问题
- 教育3.0： 老师是导游；学生是探索者，自学者和创造者

《创意空间》为孩子提供了一个丰富多彩的和自然界相似的3D虚拟世界。
当学生面对的不再是书本和教室，而是一个足够广阔和吸引人的世界时；
学生们需要的不再是教学，而是导游。如同来到名胜古迹、游乐场，我们更希望在导游的提示下，自主游玩。

教育3.0的核心是为孩子提供一个足够丰富和吸引人的自主学习空间；
老师的核心角色是导游和伯乐：告诉孩子从哪里可以获得更多知识， 启发孩子做出更好的作品。

将这本书放在你的书架上，等你的孩子去发现吧！

### 如何使用本书？
  
每个项目第一页讲述了游戏的基本规则和美术参考图。
第二页是创作思路和参考资料。 对于复杂的项目我们提供了关键性参考代码，简单的项目则提供了代码思路。
在Paracraft软件中，按下F1键可以找到很多基础模板和原理介绍。 大多数游戏都可以通过将若干个模板组合起来完成。

### 为何写这本书？  
我从1989年大概7岁时开始玩电脑游戏和自学编程。从小学到初中，我大概编写了7个非常完整的游戏和一个非常复杂的俄罗斯方块网络对战程序，后者我花了1年多的时间，还制作了片头动画。
  
在我小学3-4年级时，我偶然在家中的书架上发现了一本叫《100个游戏程序设计》的书。只是后来我找不到了，所以我组织编写了这本类似的书，送给希望自学编程的青少年。书中的这些项目大都是我小时候曾经思考过或计划编写的项目，其中有8个是我小时候真实编写过的，而且都做到了我当时能做到的最高水准。
  
希望你可以从小学到中学：(1) 选择书中3-7个项目做到完美。(2) 将1个项目做到极致，包含开场动画、AI、界面、多人联网、玩法扩充等等，这可能要花1-2年的时间。

当你积累代码量到1万行时，你未来必然可以成为一名优秀的程序员。

2021年10月，写于深圳，NPL语言研发中心
</details>

<details>
  <summary>项目1：走迷宫 </summary>

## 走迷宫
  ![]( https://api.keepwork.com/ts-storage/siteFiles/21166/raw#1634018560401image.png) 
  
  （1）用键盘控制角色的移动
  （2）目标是找到金块
  （3）墙面无法穿越
  （4）碰到金块胜利
  
### 创作思路
  
#### 角色： 青蛙

代码1：定义感知事件
  （1）while永远重复，if如果某个键被按下，then那么旋转到相应的方向并向前移动；
  （2）if如果碰到墙面会后退，if如果碰到金块会提示说胜利；
  
```lua
while 永远重复 do
    if 某个键被按下 then
        旋转到相应的方向
        向前移动0.1格
    end
    ...
    if 碰到墙面 then
        后退0.1格    
    end
    if 碰到金块 then
        提示胜利    
    end
end
```
代码2：镜头跟随与游戏提示
  
```lua
focus() -- 让镜头永远跟随角色
camera(12, 45, 0) -- 保持固定摄影机视角

registerKeyPressedEvent("escape", function()
    exit() -- 按下ESC键退出游戏
end)
```

### 参考：F1菜单：沿墙壁行走、控制主角运动。项目：536
### 思考：可以用其他按键来控制角色吗？
  
</details>

<details>
  <summary>项目10：五子棋 </summary>

## 五子棋
 
![](https://api.keepwork.com/ts-storage/siteFiles/21159/raw#1633773466677image.png) 


（1）对局双方各执一色棋子。
（2）空棋盘开局。
（3）黑先、白后，交替下子，每次只能下一子。
（4）棋子下在棋盘的空白点上，棋子下定后，不得向其它点移动，不得从棋盘上拿掉或拿起另落别处。
（5）先形成五子连线者获胜。

### 创作思路
#### 角色1：棋盘 board
代码1：将格子角色克隆16*16次，构建一个棋盘
  
代码2：当任意一个角色被点击时，检测当前的步数step, 奇数clone白字，偶数clone黑子，并更新16*16的棋盘数组的状态，最后发送一个全局消息itemPlaced通知judger判断是否一方获胜。    
  
```lua
function PlaceItem(dx, dz) 
    local id = dx..", "..dz; 
    if(not board.data[id]) then 
        board.step = board.step + 1; 
        if(board.step%2 == 1) then 
            board.data[id] = "black"; 
            clone("black", {dx, dy}) 
        else 
            board.data[id] = "white"; 
            clone("white", {dx, dy}) 
        end 
        broadcast("itemPlaced")
    end     
end   
```
  
#### 角色2：黑子 black
收到clone消息，将新建的棋子移动到{dx, dy}的位置上。
  
#### 角色3：白子 white
代码和黑子类似
  
#### 角色4：判断输赢 judger
每当收到itemPlaced的消息，都检查下棋盘数组的每个点。是否横竖对角线四个方向上有连续的5个棋子。
```
function CheckWin() 
    for dx=1, board.size do 
        for dz=1, board.size do 
            if(CheckWinAt(dx, dz)) then 
                return; 
            end 
        end 
    end 
end
```  
  
#### 参考：F1克隆角色，项目530，F1数组
#### 思考：可以编写能自动下棋的计算机对手么？
  
</details>

<details open>
  <summary>项目20：123木头人 </summary>

## 123木头人
（1）一个裁判站在远处的大树下，背对其它玩家说“123木头人”
（2）裁判说话时不能转身，此时其它玩家可以从远处起跑线靠近玩家
（3）裁判说完可以转身，看到任何玩家在移动，则玩家出局，需要从起点重新开始
（4）第一个走到裁判身后的玩家获胜
  
附加规则：
1. 裁判可以连续转身，可以用各种语速说“123木头人” 
2. 玩家经过的路面可以设置障碍，例如水坑。
3. 可以考虑多人一起游戏，或计算机控制的角色。 
4. 玩家之间可以碰撞
  

### 创作思路
#### 角色1：countman
代码1：裁判实现数数和转身，并判断当前是否有移动的玩家，并通知移动的玩家重新开始
    
代码2：Level
生成随机的地形，和一些全局的关卡参数
  
#### 角色2：Player
可以clone 4个角色。

#### 角色3：

```
```  
  
#### 参考
#### 思考
  
</details>
迷宫

双人乒乓球

贪吃蛇，越吃越大

计算器与函数绘制

打字游戏

华容道

五子棋

围棋

俄罗斯方块

跑酷

赛车

横版闯关

飞机躲子弹

密室逃脱

解谜

第三人称射击游戏

坦克大战

flappy bird

画笔程序 Painter

弹弹堂

跳一跳

键盘音游 

推箱子

塔防游戏 tower defense

台球游戏

忍者神龟 横盘动作

双人格斗 类KOF

扫雷

象棋或国际象棋

动作冒险，类波斯王子, 古墓丽影

立体魔方

逃离：用机关将一群人物运送出去

警察抓小偷

沙丘， 类红色警戒，孙子兵法

第一人称射击   类似quake, doom

八皇后问题


--------------------------------------------------

多人联机射击对战，  类CS，和平精英

挖一挖联网版

站到最后联网版

俄罗斯方块联网版

贪吃蛇联网版