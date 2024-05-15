 

## 电影方块与过山车

**1. 理论**


> 思考：

- 打造一个简单的过山车需要用到什么方块或者工具？
- 过山车如何结合电影方块。

> 讲授知识点：


- 铁轨 id：103 普通的铁轨，连接成铁路矿车在上面可以缓慢行驶。(左图)

<div style="width:200px">
  
![图 1.3.1](https://api.keepwork.com/storage/v0/siteFiles/3114/raw#gol_block.png)
  
</div>
<div style="float:right;margin-left:10px;width:130px">
  
![图 1.3.2](https://api.keepwork.com/storage/v0/siteFiles/2919/raw#gol_block.png)

![图 1.3.3](https://api.keepwork.com/storage/v0/siteFiles/2941/raw#gol_block.png)
  
  
</div>

- 探测铁轨 id: 251 (右图)
用探测铁轨可以连接成铁路，矿车可以在上面行驶。
- 当矿车经过时，探测铁轨正下方的方块强充能。
并且
- 当矿车上无人时，经过探测铁轨周围4个方向的正下方方块不充能，也就是无法激活四周的中继器。
- 当矿车上有人时，经过探测铁轨周围4个方向的正下方方块弱充能，可以激活四周的中继器。

我们可以用这个方式来探测矿车中是否有人。 如下图：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4903/raw#image.png'
  ext: png
  filename: image.png
  size: '161112'
  unit: '%'
  percent: '40'
  alignment: left

```
当无人乘坐的矿车经过中继器时，无法激活中继器。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/5017/raw#image.png'
  ext: png
  filename: image.png
  size: '253071'
  alignment: left
  unit: '%'
  percent: 40

```

当有人乘坐的矿车经过中继器时，激活中继器。


 


我们可以在探测铁轨下加入电影方块，做出自己想要做的过山车+电影结合的效果。注意：电影方块上放探测铁轨才会生效，其它铁轨无效。



- 动力铁轨 id：250 搭配能量块（id：157）可持续为矿车提供能量让其快速行驶。


没有能量的动力铁轨无法发挥出正常作用，建议搭配能量块一起使用。


> 搭建装饰参考命令：
- /sphere 数值 创建一个球体


<div style="clear:both"/>

**2. 实践**


**步骤1：**

<div style="float:right;margin-left:10px;width:250px">
  
![图 1.3.4](https://api.keepwork.com/storage/v0/siteFiles/2946/raw#gol_block.png)
  
</div>

> 在过山车中的一些电影方块效果：

- 右键点击电影方块，shift+左键点击摄像机将其删除，再导入演员中的效果，如下图。当过山车经过时带有探测轨道的电影方块时，可以触发电影方块中的特效。


<div style="clear:both"/>
<div style="float:right;margin-left:10px;width:250px">
  
![图 1.3.5](https://api.keepwork.com/storage/v0/siteFiles/2951/raw#gol_block.png)
  
</div>

> 为过山车加入对白文字（参考推荐作品：我的故事）

- 同样，也是删除摄像机，在电影方块中加入文字，我们甚至可以利用命令方块加入过山车的背景音乐。


<div style="clear:both"/>
<div style="float:right;margin-left:10px;width:250px">
  
![图 1.3.6](https://api.keepwork.com/storage/v0/siteFiles/2954/raw#gol_block.png)
  
</div>

> 为过山车加入片段动画（参考推荐作品：爷爷的宝藏）

-  动画片段建议不要超过10秒。

<div style="clear:both"/>