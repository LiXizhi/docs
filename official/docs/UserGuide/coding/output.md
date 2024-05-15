## 代码方块的输出

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/18134/raw#1604202179478codeblock9_small.mp4
  ext: mp4
  filename: 1604202179478codeblock9_small.mp4
  size: 12417587
          
```
[在腾讯视频播放](https://v.qq.com/x/page/h0713cf16qf.html)

**1. 理论**

> 思考：代码方块如果可以输出信号，可以用来做什么？

> 讲授知识点：

- 代码方块可以有输出：通过setOutput函数。
- 代码方块输出可以通过中继器和导线控制其他电影方块或代码方块。
- setOutput函数的第一个参数表示信号的强度。15代表可以传递15格的距离。0表示没有输出。
- `setOutput(15); wait(3); setOutput(0)`可以构成3秒的脉冲信号。
- anim函数: 可播放人物动画
- restart函数：可以重新启动代码方块
- 中继器：可用来接受代码方块的输出，和电影方块类似。

**2. 实践**

<div style="float:right;margin-left:10px;width:180px">

![图 1.4.2](https://api.keepwork.com/storage/v0/siteFiles/3346/raw#image.png)

</div>

按照右图创建代码方块，中继器，导线，并输入下面代码。

```javascript
anim(0)
say("点击我开始游戏!")

registerClickEvent(function()
    say("Ctrl+P 停止播放")
    setOutput(15)
    wait(3)
    setOutput(0)
    restart()
end)
```

进入世界时，代码方块是激活状态， 所以会显示`点击我开始游戏!`, 此时用户只要点击角色代码方块就会产生一个3秒的脉冲输出，刚好可以激活后面的电影方块。

> 注意激活电影方块需要的是脉冲信号， 而激活代码方块需要的是持续的信号。