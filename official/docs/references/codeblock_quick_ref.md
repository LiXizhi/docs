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

> 瞬移到`19194` `5` `19188`
moveTo(19194, 5, 19188)

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

> 行走`1` `0` `0`持续`-1`秒
walk(1, 0, 0, -1)

</div>
<div style="float:left;">

```lua
-- 例子1:
walk(1,0) -- x,z
walk(0,1) -- x,z
walk(-1,0,-1) -- x,y,z
walk(0,0,0,-1) -- walk and stop
-- 例子2:精准行走模式
walk(0.1, 0, 0, 0.1, true)
walk(0,0,0) -- stop
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
-- 例子3:精准行走模式
walkForward(0.1, 0.1, true)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 固定到`父角色`的骨骼``上
attachTo("父角色","")

</div>
<div style="float:left;">

```lua
-- 例子1:
attachTo("parent", "R_Hand")
-- with position offset
attachTo("parent", "R_Hand", {0,1,1})
-- with offset and rotation {roll, pitch, roll}
attachTo("parent", "R_Hand", {0,1,1}, {0, 0, 1.57})
-- without parent bone's rotation
attachTo("parent", "R_Hand", nil, nil, false)
-- detach
attachTo(nil)
-- properties
parent = getActorValue("parent")
setActorValue("parentOffset", "0, 2, 0")
setActorValue("parentRot", {0, 3.14, 0})
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

> 设置角色位置`19194` `5` `19188`
setPos(19194, 5, 19188)

</div>
<div style="float:left;">

```lua
-- 例子1:
local x, y, z = getPos()
setPos(x, y+0.5, z)
setPos(x, y+0.5, z, "actorName")
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
anim(4) -- walking 
anim(5) -- running
move(-2,0,0,1)
anim(0, 500) -- standing and wait 500 ms
-- 例子2:定义新动作
-- anim(name, fromTime, toTime, isLooped)
anim("dance1", 0, 2000, true)
anim("dance2", 2000, 3000)
-- play a user defined animation by name
anim("dance1")
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

> 播放并等待从`10`到`1000`毫秒
playAndWait(10, 1000)

</div>
<div style="float:left;">

```lua
-- 例子1:播放电影方块中的角色动画
playAndWait(10, 1000)
say("finished")
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

> 骨骼`*`从`10`到`1000`并循环`true`
playBone("*", 10, 1000, true)

</div>
<div style="float:left;">

```lua
-- 例子1:
playBone("Neck", 2000)
-- play all bones, this is fast
playBone("*", 1000, 2000, true)
wait(1)
playBone("*") -- stop it
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
setActorValue("playSpeed", 1)
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

> 是否匹配电影`myself`
isMatchMovie("myself")

</div>
<div style="float:left;">

```lua
-- 例子1:myself代表当前代码方块的名字
if(isMatchMovie("myself")) then
    playMatchedMovie("myself")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 播放匹配的电影`myself`,`并等待`
playMatchedMovie("myself", true)

</div>
<div style="float:left;">

```lua
-- 例子1:myself代表当前代码方块的名字
if(isMatchMovie("myself")) then
    playMatchedMovie("myself")
end
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

<div style="float:left;margin-right:10px;">

> 窗口`html`,`左上`,`0`,`0`,`300`,`100`
window([[
html
]],"_lt", 0, 0, 300, 100)

</div>
<div style="float:left;">

```lua
-- 例子1:绘图板
wnd = window([[<div>draw something</div>]], "_lt",200,20,300,300);
local ctx = wnd:getContext();
ctx.strokeStyle = "#ff0000"
ctx.lineWidth = 2
ctx.font="System;20;"
ctx:fillText("left click and drag", 10, 30)
ctx.fillStyle = "#80808080"
ctx:fillRect(0,0,ctx:getWidth(),ctx:getHeight())
wnd:registerEvent("onmousedown", function(event)
    ctx:strokeRect(event:pos():x(), event:pos():y(), 1, 1)
    ctx:beginPath()
    ctx:moveTo(event:pos():x(), event:pos():y())
end)
wnd:registerEvent("onmousemove", function(event)
    if(event:LeftButton()) then
        ctx:lineTo(event:pos():x(), event:pos():y())
        ctx:stroke()
        ctx:beginPath()
        ctx:moveTo(event:pos():x(), event:pos():y())
    end
end)
wnd:registerEvent("onmouseup", function(event)
    if(event:button() == "right") then
        wnd:CloseWindow()
    end
end)
-- 例子2:MCML UI
test = {key="hello world"}

function OnClickTest2()
    test.key = document:GetPageCtrl():GetValue("myName")
    cmd("/tip clicked2!"..test.key)
end

function GetTitle()
    return "Enter text:"
end

window([[ 
<script>
function OnClose()
    cmd("/tip clicked!"..Page:GetValue("myName"))
    Page:CloseWindow()
end
</script>
<div style="margin:10px"> 
    <%=GetTitle()%> 
    <input name="myName"  type="text" style="width:90px" value='<%=test.key%>'/> 
    <input type="button" onclick="OnClickTest2" value="click me"/> 
    <input type="button" onclick="OnClose" value="close" style="margin-left:5px"/> 
</div> 
]], "_lt", 10, 10, 300, 100)
-- 例子3:Context2d API
local wnd = window([[<div>draw something</div>]], "_lt",200,20,300,300);
local ctx = wnd:getContext();
ctx.globalAlpha = 0.5
ctx:clearRect()
ctx.fillStyle = "#80808080"
ctx:fillRect(0, 0, ctx.width, ctx.height)
ctx.lineWidth = 2
ctx.font="System;20;"
ctx:save()
ctx:translate(50, 10)
ctx:rotate(-0.2)
ctx:drawImage("preview.jpg", 70, 60, 64, 32)
ctx:strokeText("left click and drag", 10, 30)
ctx:restore()
ctx.strokeStyle = "#ff0000"
ctx:moveTo(0,0)
ctx:lineTo(80,80)
ctx:lineTo(0,80)
ctx:stroke()
ctx:beginPath()
ctx:arc(100, 100, 40, 0, 1.4, true)
ctx:lineTo(190, 120)
ctx:closePath()
ctx:stroke()
ctx.fillStyle = "blue"
ctx:fill()
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
-- unregister the given key press event
registerKeyPressedEvent("any", nil);
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

> 每`1`帧执行``
registerTickEvent(1, function()
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
i=1
registerTickEvent(1, function(msg)
    i = i + 1
    say(i)
end)
wait(10)
-- unregister
registerTickEvent(1, nil)
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
registerBroadcastEvent("msg1", function(msg)
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

> 广播消息给`username`,`title`,`{}`
broadcastTo("username", "title", {})

</div>
<div style="float:left;">

```lua
-- 例子1:
registerBroadcastEvent("Hello", function(msg)
    tip(msg.text.." from "..(msg.from or ""))    
end)
setActorValue("name", "Alice")
broadcastTo("Alice", "Hello", {text="hello"})
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

> 当收到`TryCreate`智能消息时(`msg`)``
registerAgentEvent("TryCreate", function(msg)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:
registerAgentEvent("TryCreate", function(msg)
    setBlock(msg.x, msg.y, msg.z, 62)
end)
registerAgentEvent("OnSelect", function(msg)
    tip("you selected agent item")
end)
registerAgentEvent("OnDeSelect", function(msg)
    tip("you de-selected agent item")
end)
registerAgentEvent("GetIcon", function()
    return "Texture/blocks/items/apple.png"
end)
registerAgentEvent("OnClickInHand", function(msg)
    tip("you clicked me!")
end)
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当收到网络消息`ps_用户加入`(`msg`)时``
registerNetworkEvent("ps_user_joined", function(msg)
end)

</div>
<div style="float:left;">

```lua
-- 例子1:私服模式:
registerNetworkEvent("ps_user_joined", function(msg)
    tip(format("user join: %s id:%d", msg.username, msg.entityId))
    wait(1)
    sendNetworkEvent(msg.username, "Hello", {text=msg.username})
    sendNetworkEvent(msg.entityId, "Hello", {text="welcome"})
end)
registerNetworkEvent("ps_user_left", function(msg)
    tip(format("user left: %s id:%d", msg.username, msg.entityId))
end)
registerNetworkEvent("ps_server_started", function(msg)
    tip(format("server start: %s id:%d", msg.username, msg.entityId))
end)
registerNetworkEvent("Hello", function(msg)
    tip(msg.from..":"..msg.text)
end)
-- 例子2:大厅模式:
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

> 广播网络消息`msgname`(`{}`)
broadcastNetworkEvent("msgname", {})

</div>
<div style="float:left;">

```lua
-- 例子1:私服模式:
registerNetworkEvent("HelloText", function(msg)
    tip("HelloText: "..msg.text.." from: "..msg.from)
    if(GameLogic.isServer) then
        broadcastNetworkEvent("HelloText", {text=msg.text, from=msg.from}) 
    end
end)
if(GameLogic.isRemote) then
    for i=1, 2000 do
        sendNetworkEvent("admin",  "HelloText", {text=i}) 
        wait(1)
    end
end
-- 例子2:大厅模式:
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
sendNetworkEvent("username", "title", {})

</div>
<div style="float:left;">

```lua
-- 例子1:私服模式:
registerNetworkEvent("HelloText", function(msg)
    tip("HelloText: "..msg.text.." from: "..msg.from)
    if(GameLogic.isServer) then
        broadcastNetworkEvent("HelloText", {text=msg.text, from=msg.from}) 
    end
end)
if(GameLogic.isRemote) then
    for i=1, 2000 do
        sendNetworkEvent("admin",  "HelloText", {text=i}) 
        wait(1)
    end
end
-- 例子2:大厅模式:发送消息给指定用户
registerNetworkEvent("title", function(msg)
   tip(msg.userinfo.keepworkUsername)
   wait(1)
   tip(msg.a)
end)

sendNetworkEvent("username", "title", {a=1})
-- 例子3:UDP模式:发送原始消息给指定地址(无需登录)
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

> 执行命令`/tip`,`""`
cmd("/tip", "")

</div>
<div style="float:left;">

```lua
-- 例子1:
cmd("/setblock ~0 ~0 ~1 62")
cmd("/cameradist 12")
cmd("/camerayaw 0")
cmd("/camerapitch 0.5")
cmd("/time", "0")
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

> 重复执行只要`status == "start"```
while (status == "start") do
end

</div>
<div style="float:left;">

```lua
-- 例子1:
i=3
while(i>0) do
    tip(i)
    i=i-1
end
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
-- 例子2:终止执行当前线程
say("Press X key to terminate")
while(true) do
    turn(1)
    if(isKeyPressed("x")) then
        terminate()
    end
end
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

> 播放音符`1`持续`0.25`节拍
playNote("1", 0.25)

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

<div style="float:left;margin-right:10px;">

> 朗读文字`你好`
playText("你好")

</div>
<div style="float:left;">

```lua
-- 例子1:使用文本播放语音
playText("欢迎来到我的世界")
-- 例子2:参数2可以延迟执行后面的代码
playText("你好", 2)
tip("你好")
-- 例子3:参数3可以选择不同的声音 0为女声，1为男声， 3为情感合成-逍遥，4为情感合成-丫丫，默认为丫丫(女童音)
playText("你好", 1, 1)
tip("你好")
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

> 提问`你叫什么名字?`并等待回答选项``
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

-- 例子2:彩色按钮
ask("color <span style='color:#ff0000'>choices</span>", {
    {text="choice A", color="#00FF00"}, 
    {text="choice B", color="#0000FF"}, 
    "choice C"
})
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

> 回答
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
    elseif(isMouseDown(2)) then
        tip("right mouse button down")
        wait(0.3)
    end
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 鼠标XY
local x, y = getMousePoint()

</div>
<div style="float:left;">

```lua
-- 例子1:
-- x in [-500, 500]
local x, y = getMousePoint()
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

> 获取方块`19194` `5` `19188`
getBlock(19194, 5, 19188)

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

> 放置方块`19194` `5` `19188` `62`
setBlock(19194, 5, 19188, 62)

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
-- with additional block data
local data = 0
setBlock(x,y+2,z, id, data)
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

> 设置模式`游戏模式`
cmd("/mode", "game")

</div>
<div style="float:left;">

```lua
-- 例子1:
if(GameLogic.GetGameMode() == "edit") then
    cmd("/mode", "game")
end
```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 当前游戏模式
GameLogic.GetGameMode()

</div>
<div style="float:left;">

```lua
-- 例子1:防作弊密码锁
if(GameLogic.GetGameMode() == "edit") then
    cmd("/mode", "game")
end
local hasPassword
while(not hasPassword) do
    if(GameLogic.GetGameMode() == "edit") then
        cmd("/mode", "game")
        run(function()
            ask("Enter password: 1234")
            if(answer == "1234") then
                hasPassword = true;
                cmd("/mode", "edit")
            end
        end)
    end
    wait(1)
end
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

> 连接`hello`和`world`
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

> ``的长度
(#"")

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

<div style="float:left;margin-right:10px;">

> 删除`变量名`的第`1`项
table.remove(变量名, 1)

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> `变量名`包含`东西`?
table.contains(变量名, "东西")

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

### 数据
<div style="float:left;margin-right:10px;">

> `变量名`
变量名

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

> `变量名`赋值为`1`
变量名 = 1

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

> 全局`变量名`赋值为`1`
set("变量名", 1)

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

> 新建本地`变量名`为`0`
local 变量名 = 0

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

> 当角色被克隆时(`name`)``
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

> 克隆`"myself"`(``)
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

> 删除此克隆角色
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

> 设置角色的`名字`为``
setActorValue("name", "")

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

> `真`
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

> `#ff0000`
"#ff0000"

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> {}
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

> `_G`中的`key`
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

> 函数(``)``
function()
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

> 调用函数`log`(``)
log()

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

> 调用函数并返回`log`(``)
log()

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

> 显示变量`score`,``,`#0000ff`,`14`
showVariable("score", "", "#0000ff", 14)

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

<div style="float:left;margin-right:10px;">

> 代码``


</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 注释 ``
-- 

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>

<div style="float:left;margin-right:10px;">

> 注释全部 ``
--[[
]]

</div>
<div style="float:left;">

```lua
-- 例子1:

```

</div>
<div style="clear:both"/>
