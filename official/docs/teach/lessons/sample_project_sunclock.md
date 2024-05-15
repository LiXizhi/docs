# 《太阳钟》

> [点击查看：关于使用Paracraft参加由中国科协举办的2019年《全国青少年科学影像节》比赛集训通知](/docs/teach/lessons/science_festival)

科学探究纪录片 举例

##  科学探究纪录片：太阳钟

```@Project
styleID: 0
project:
  projectId: '2423'
  projectTagsShow: false
  projectMembersShow: false

```


- **第一步：学生多看，多听，多学相关知识**
   太阳钟是小学科学课上学生们都制作过的内容，这里学生继续百度下太阳钟和日晷了解更多的知识。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4080/raw#image.png'
  ext: png
  filename: image.png
  size: '650272'
  unit: px
  width: '400'
  alignment: left

```
 
- **第二步：学生提出困难的问题**
   为什么中国古代的日晷（太阳钟）都要倾斜一定的角度？日晷上的刻度是均匀的么?
   
- **第三步：学生需要想办法搞清楚问题的答案，清楚解决问题的详细过程。**
   学生了解到日晷的罗盘的平面是朝向南北方向的，指针两侧应该是东西方向。 我们无法等待1天的时间去观察不同的倾斜角度与时间的关系， 所以我们选择用计算机仿真
   
- **第四步：学生进行头脑风暴，在众多想法中思考一个大概的剧本方案。**
    我们需要设计一个仿真的3D日晷， 然后让它倾斜不同的角度，然后在计算机仿真软件中进行观察，并寻求问题的答案。
    
- **第五步：开始设计具体的剧本，分镜头，写下来，然后开始创作，最终形成一个作品。**

   - **第一步：** 制作日晷CAD模型
我们可以用BMax模型搭建，并存为文件clockmodel.bmax
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4084/raw#image.png'
  ext: png
  filename: image.png
  size: '185786'
  unit: px
  width: '300'
  alignment: left

```

我们也可以采用编程的方式用CAD建模，这样更精确，我们使用了CAD编程方块制作钟的模型。


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4103/raw#image.png'
  ext: png
  filename: image.png
  size: '48598'
  unit: px
  width: '250'
  alignment: left

```

代码如下：
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4104/raw#image.png'
  ext: png
  filename: image.png
  size: '14634'
  unit: px
  width: '340'
  alignment: left

```


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4085/raw#image.png'
  ext: png
  filename: image.png
  size: '201584'
  unit: px
  width: 600
  alignment: left

```

后来我们又加入了一些刻度，代码如下：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4086/raw#image.png'
  ext: png
  filename: image.png
  size: '272637'
  unit: px
  width: '650'
  alignment: left

```

```lua
cylinder("union",1,0.2,'#ffffff')
cylinder("union",0.04,2,'#7e7e7e')
move(0,0.5,0)
for i=1, 12 do
  if(i%3==0) then
    box("union",1,0.02,0.02,'#ffb0c5')
  else
    box("union",1,0.02,0.02,'#b0c5ff')
  end
  move(0.5,0.1,0)
  rotateFromPivot('y',((i) * (30)),0,0,0)
end
```
   
   - **第二步：** 编写计算机仿真代码
我们分别采用了图块和文字化的编程方式仿真了太阳种
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4088/raw#image.png'
  ext: png
  filename: image.png
  size: '26321'
  unit: px
  width: '500'
  alignment: left

```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/4087/raw#image.png
  ext: png
  filename: image.png
  size: 186747
          
```

```lua
cmd("/shader 2")

local time = -0.5
while(true) do
    for i=1, 120 do
        time = -0.5 + i/120
        cmd("/time "..time)
        wait(0.02)
        tip("当前时间:"..math.floor((time+0.5)*12))
    end
end
```

我们希望通过键盘来控制当前的时间和太阳钟的角度，为了方便观察有了下面的最终仿真程序
```lua
cmd("/shader 2")
_G.help1 = "按A键S键可调整当前时间"
showVariable("help1")
_G.help2 = "按上下左右键可调整角度, esc退出"
showVariable("help2")

focus("myself")

local time=0
registerKeyPressedEvent("s", function(msg)
    time = time - 1/12
end)

registerKeyPressedEvent("a", function(msg)
    time = time + 1/12
end)

local angle = 0;
while(true) do
    cmd("/time "..format("%f", time))
    wait(0.01)
    tip("当前时间:"..math.floor((time+0.5)*12))
    if(isKeyPressed("left")) then
        turn(-1)
    elseif(isKeyPressed("right")) then
        turn(1)
    elseif(isKeyPressed("up")) then
        angle = math.min(90, angle + 1);
        play(angle*1000)
    elseif(isKeyPressed("down")) then
        angle = math.max(0, angle - 1);
        play(angle*1000)
    elseif(isKeyPressed("escape")) then
        exit()
    end
end
```

   - **第三步：** 观察和记录
我们看到当太阳钟越垂直地面，刻度越均匀，但影子越模糊。 
当太阳钟倾斜45读时，中午的刻度变化更大， 早晚的刻度变化较小，但影子很清晰。 


   
   - **第四步：**  得出结论
太阳钟的刻度不是均韵的，太阳钟应该尽量与地面垂直，但也不能太垂直，否则影子太暗。 
反过来， 我们可以通过太阳种的角度和刻度的密度，来反推太阳在空中的平面，从而推算出地球和太阳之间的相对关系
   
   - **第五步：** 用手机记录上述过程，作者入镜，并剪辑成科学记录片

下面是初步的拍摄样片
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/4064/raw#sunclock.mp4
  ext: mp4
  filename: sunclock.mp4
  size: 11528698
          
```


 
- **第六步：学生发布自己的作品（分享或提交比赛）**
制作海报，宣传视频， 介绍文字， 个人介绍，提交大赛