## 制作图形界面
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/18135/raw#1604202302003codeblock8_small.mp4
  ext: mp4
  filename: 1604202302003codeblock8_small.mp4
  size: 33326731
          
```
[在腾讯视频播放](https://v.qq.com/x/page/i07076tx5ti.html)

**1. 理论**

> 思考：

- 你都用过哪些方式和计算机交流？
- 如何制作图形界面？

> 知识点：详见第二章：基础理论

- 如何删除电影里的一个角色（shift+left或者拖拽到电影编辑框外）
- 如何在电影里增加一个图层（左键单击空格子，然后选择图层）
- setActorValue除了可以设置角色名字（name）外，还可以设置图层的文字(text)
- 图层字幕也是演员，可以使用控制演员的那些函数去控制
- 屏幕坐标：详见1.5节
- 用代码去编写图层字幕
- scaleTo函数，tip函数， exit函数可以退出
- 制作多个字幕并让它们同时消失（使用广播）

**2. 实践**

**步骤1：创建3D立体文字动画**

> 代码编辑器默认输入法是英文。如果要打中文的话，老师需要提醒学生切换到中文输入。

<div style="float:left;">

```javascript
scaleTo(200)
setActorValue("text", "点击我播放电影!")

registerClickEvent(function()
    move(0, 0.4, 0, 0.3) 
    move(0, -0.4, 0, 0.3) 
end)

while(true) do
   turn(2)
   wait(0.01)
end
```

</div>
<div style="float:left;margin-left:10px;width:280px">

![图 1.4.1](https://api.keepwork.com/storage/v0/siteFiles/587/raw#2018-09-06_23_41_46-840-image.png)

</div>
<div style="clear:both" />

**步骤2： 2D UI与事件**

<div style="float:right;margin-left:10px;width:220px">

  ![](https://api.keepwork.com/storage/v0/siteFiles/588/raw#image.png)

</div>

代码方块1：开始按钮

```javascript
registerClickEvent(function()
    move(0, 0, 10, 0.2)
    move(0, 0, -10, 0.2)
    broadcast("GameStart")
end)

registerBroadcastEvent("GameStart", function()
    hide()
    tip("Game Started!")
end)
```

代码方块2：UI图片动画

```javascript
registerBroadcastEvent("GameStart", function()
    hide()
end)

for i=100, 200 do
   scaleTo(i)
   wait(0.01)
end
```

<div style="clear:both"/>

**步骤3: Clone角色与UI**

用一个代码方块，制作多个UI按钮

<div style="float:right;margin-left:10px;width:220px">

  ![](https://api.keepwork.com/storage/v0/siteFiles/589/raw#image.png)

</div>

```javascript
registerClickEvent(function()
     move(-10, 0, 0,0.1)
     move(10, 0, 0,0.1)
     local name = getActorValue("name")
     if(name == "startGame") then
        tip("Game Started!")
        broadcast("GameStart")
     elseif(name == "authors") then
        tip(name)
     elseif(name == "exit") then
        tip(name)
        exit()
     end
end)

registerBroadcastEvent("GameStart", function()
    hide()
end)

registerCloneEvent(function(name)
    setActorValue("name", name)
    if(name == "startGame") then
        play(0)
    elseif(name == "authors") then
        play(1000)
    elseif(name == "exit") then
        play(2000)
    end
end)

hide()
clone("myself", "startGame")
clone("myself", "authors")
clone("myself", "exit")
```