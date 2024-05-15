 
## bmax简易骨骼与X文件应用



**1. 理论**
利用bmax角色制作一个包含骨骼的模型，制作简单的重复的动作，并存为X文件。
本节内容较难，建议观看教学视频。

**2. 实践**
- 学习为简单的bmax角色放置正确的骨骼
- 学习利用骨骼做一个完整的循环动作
- 存成x文件导入电影方块中，并使用这个循环动作
- bmax骨骼应用
- X文件使用方法

案例视频：
- [视频1：用骨骼方块制作电风扇（上）](https://keepwork.com/official/tips/s1/1_55)
- [视频2：用骨骼方块制作电风扇（下）](https://keepwork.com/official/tips/s1/1_56)

**步骤1：认识bmax**
- 什么是bmax？
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3705/raw#13. 模型与动画人物教学.mp4
  ext: mp4
  filename: 13. 模型与动画人物教学.mp4
  size: 616642521
          
```

bmax就是【Block Max方块模型】，用来制作精致的静态和动态道具。无论是静态还是动态的bmax，都能用于电影或场景中。静态bmax可以没有骨骼，动态bmax需要赋予骨骼。

<div style="float:right;margin-left:10px;width:150px">
  
![图 1.2.8](https://api.keepwork.com/storage/v0/siteFiles/3256/raw#image.png)
  
</div>


- 什么是骨骼？

和人体的骨骼类似，在Paracraft中，骨骼是一种特殊的有方向的方块，骨骼总是指向它的上一级骨骼，并且可以控制与之相连的其它方块（类似人体的肌肉）运动。

骨骼A指向骨骼B，我们称骨骼A为骨骼B的子骨骼，骨骼B为骨骼A的父骨骼。 父骨骼运动，子骨骼也跟着运动。
模型中最上级的一个父骨骼，没有指向任何其它骨骼，我们称之为根骨骼，它控制了人物整体的运动。

- 骨骼权重与彩色方块
骨骼的位置和方向，会影响周围的普通方块（肌肉）。一个普通方块可能受到多个骨骼的影响，普通方块受到某个骨骼的影响大小叫做权重。数值1代表某个方块完全跟随某个骨骼运动，0代表不跟随骨骼运动。 在Bmax中，这个数值不是1就是0. 也就是所Bmax中的某个普通方块只会受到一个骨骼方块的影响。 此时我们也称这个方块绑定到了这个骨骼上。 

指定普通方块的权重是一个很复杂的过程，我们会用到`彩色方块id：10`。彩色方块可以有很多种不同的颜色，Paracraft会自动将颜色相同，并且彼此相连的一组方块看成一个肌肉群，并将他们统一绑定到与之相连的骨骼方块上。 

例如手掌与手臂相连，手臂与肩膀相连。这时手掌和手臂最好用不同颜色的彩色方块区分开，如下图。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3249/raw#image.png'
  ext: png
  filename: image.png
  size: '94830'
  unit: px
  percent: '35'
  alignment: left
  width: 200

```

- 什么是x文件？
x文件是ParaX文件的缩写，是Paracraft中的通用模型文件格式。x文件是一种比Bmax文件更加通用的模型文件格式。X文件不仅可以记录静态的3D模型和骨骼位置关系， 还可以存储多组骨骼动画。

在Paracraft中，我们可以将一个或多个包含人物动作的电影方块，保存成一个X文件。 然后， 我们可以在任何其它地方，重复使用它，比如可以用做NPC， 电影人物或者场景模型。 当然我们也可以将其它外部软件制作的动画模型，转化为X文件。
 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3252/raw#image.png'
  ext: png
  filename: image.png
  size: '65446'
  unit: px
  percent: '40'
  alignment: left
  width: 350

```




**步骤2：插入正确骨骼**

> 打开菜单栏(E键)，电影分类下的骨骼方块id：253
 
- 骨骼方块箭头的方向指向它的父骨骼，没有父骨骼的方块为根骨骼
- 骨骼方块会绑定和它后部以及侧面相连的方块，这些方块会随骨骼一同运动
- 建议用彩色方块搭建骨骼以外的（肌肉）方块

注意：
- 只有正常的方块会显示出来，半透明以及非方形的方块目前还不会显示，但是可以用来连接肌肉
   - 例如可以用蜘蛛网，连接2个悬空的区域，使它们绑定到同一根骨骼上
- Bmax模型也可以连接到骨骼上，形成Bmax模型的嵌套，为模型增加更多的细节
- 在最终显示时，骨骼方块本身也会变为离它最近的一个肌肉方块
 

 如下图，各部位的骨骼最终要指向父骨骼，末端-->中间-->前端-->父骨骼-->根骨骼。

<div style="float:left;width:200px">
  
![图 1.2.9](https://api.keepwork.com/storage/v0/siteFiles/3243/raw#image.png)
  
</div>
<div style="float:left;margin-left:10px;width:250px">
  
![图 1.2.10](https://api.keepwork.com/storage/v0/siteFiles/1992/raw#image.png)
  
</div>
<div style="clear:both"/>

`当父子骨骼不在同一直线上时，可添加中间骨骼进行连接。如果希望相连的方块属于不同的骨骼，我们需要用颜色区分开。如上图绿色和深绿色，紫色和浅紫色`

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3242/raw#image.png'
  ext: png
  filename: image.png
  size: '70035'
  unit: px
  alignment: left
  width: 500

```

`先搭建蛇头部位，只需搭建一半，再放入骨骼。后搭建蛇身一半，放入蛇身骨骼。`

- 在绑定骨骼时，Ctrl+右键点击骨骼，会显示所有骨骼的状态和权重。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3246/raw#image.png'
  ext: png
  filename: image.png
  size: '203488'
  unit: px
  alignment: left
  percent: '50'
  width: 300

```


**步骤3： 存成bmax，并为各个关节K动作帧**
 



- Ctrl+左键全选模型，Alt+左键选择模型的中心轴进行镜像
- Ctrl+左键选中道具进行保存并存为bmax模型
- 在电影方块中添加演员，点击添加按钮再选择bmax模型的路径

`快捷键1,1切换到骨骼轴后点击骨骼关节，出现该关节的三轴旋转圆环（绿色提示为该关节的名字，表示进入了该关节的专属骨骼轴），拖动红绿蓝圆环调整骨骼旋转角度。`
（补充：快捷键2切换到位置轴，快捷键3切换到转身轴，按两次3可切换到三轴旋转，快捷键4切换到大小轴）

> 注意：
1、要在头部骨骼的初始位置K帧，可防止头部受编号动作的影响。
2、Esc键退出当前关节的专属骨骼，回到全部骨骼。
3、若骨骼轴初始位置无关键帧，在中途位置K帧，初始位置会自动生成相同的关键帧。

 
把骨骼动作完成后关闭电影方块，将该电影方块保存为X文件。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3255/raw#image.png'
  ext: png
  filename: image.png
  size: '112247'
  unit: px
  percent: '40'
  alignment: left
  width: 300

```

 
**步骤4： 将X文件导入电影方块，在动作中插入该动作编号（默认0待机）并将秒数调整为10秒左右，小蛇调整好运动的位置，它就可以循环动作了。**

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3254/raw#image.png'
  ext: png
  filename: image.png
  size: '74978'
  unit: px
  percent: '40'
  alignment: left
  width: 200

```