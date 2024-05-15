# 计算机辅助设计CAD

> 你知道杯子，手机，汽车，等等是如何被设计并制造出来的么？

我们身边的大多数精密物品都是用计算机设计出来的。设计师完成设计后， 计算机会再生成控制机器人的指令，最后由专业机器人按照指令运动机械臂将物品制造出来。 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2870/raw#image.png'
  ext: png
  filename: image.png
  size: '391166'
  unit: px
  alignment: left
  width: 300

```

3D打印技术是一种更加廉价和通用的制作技术，它可以像打印照片一样，打印任意的3D物体，目前民用3D打印机每个点的精度可以小到0.3毫米，和头发的半径差不多。但是目前3D打印对材料有一定的限制。

无论哪种方式，人们首先都需要用计算机去做设计。计算机辅助设计Computer Aided Design (CAD)就是指上述过程。在Paracraft中，我们已经学会用方块设计物体，的确这也是一种可行的CAD过程；但是在专业的CAD设计领域中，工程师们是用代码和数学来生成所需的物体的，这样生成的物体具有更高的精度，并可以根据参数快速的调整模型。

<div style="float:right;width:250px;margin-left:10px">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2873/raw#image.png) 
  
</div>

在Paracraft中，有一个特殊的编程方块叫做`NPL Block CAD`, 它是`NPL CAD`的一部分，它让你可以用最接近专业CAD软件的方式去建模。

NPL CAD通过编程的方式实现了专业计算机辅助设计软件的常用功能，并在不断的扩充函数类库。编程人员一般可以在30分钟内从入门到精通。

在本书的上部中有多个项目使用了NPL CAD，请先完成这些项目，再阅读本章。

## 术语介绍

下面我们来介绍几个术语：

**计算机图形学**
 - 计算机图形学(Computer Graphics or CG)是最激动人心且快速增长的现代技术之一，它已成为应用软件和普通计算机系统中的标准特性。
 - 在早期的研究中，计算机图形学要解决的是如何在计算机中表示三维几何图形,以及如何利用计算机进行图形的生成、处理和显示的相关原理与算法，产生令人赏心悦目的真实感图像。
 - 随着近40年的发展，计算机图形学已经频繁地应用于多种领域，如科学、艺术、工程、商务，工业、医药、政府、娱乐、广告、教学、培训和家庭等各方面的应用。
 - 如今多数的计算机图形学研究重点仍在于增强有效性、现实性和图片生成的速度方面。这些领域的复杂材质如头发、布料和液压传动研究的现实渲染的困难性，以及图像处理、动画和表面表示，仍是研究人员关注的焦点。

**计算机辅助设计**
 - 计算机辅助设计(Computer Aided Design or CAD)是计算机图形学最广泛、最重要的应用领域。
 - CAD使工程设计的方法发生了巨大的改变，利用交互式计算机图形生成技术进行土建工程、机械结构和产品的设计正在迅速取代绘图板加工字尺的传统手工设计方法，担负起繁重的日常出图任务以及总体方案的优化和细节设计工作。事实上，一个复杂的大规模或超大规模集成电路板图根本不可能手工设计和绘制，用计算机图形系统不仅能设计和画图，而且可以在较短的时间内完成，将结果直接送至后续工艺进行加工处理。

**NPL CAD**
  - NPL CAD(Neural Parallel Language Computer Aided Design)是一个创建3D模型的工具集合，使用NPL语言开发。
  - NPL CAD是面向编程人员的一款CAD设计软件，它不提供可视化编辑。建模过程都通过输入代码完成，代码运行后会输出可预览和可工业制作的3D模型，也可以直接用在Paracraft中。
  - NPL CAD所使用的建模方法与专业CAD软件中的建模方法相同。
  
**NPL Block Cad**
- `NPL Block Cad`是`NPL CAD`的一个子集，它降低了CAD代码输入的难度。
- NPLBlockCad创建模型的过程，对编程教育有很大的帮助。
- NPLBlockCad是Paracraft的一个内置插件，它可以创建出更加逼真的模型。Paracraft的用户可以使用代码方块控制这些3D模型，制作动画或游戏。
- NPLBlockCad支持模型多种文件格式的导出，方便3D打印。

## NPL Block CAD的指令集
下面是NPL Block CAD的常用指令集和例子。全部CAD指令分成了：图形，修改，名称， 控制，运算，数据，布尔运算几个大类。 


**"图形"指令**
图形指令主要用于创建基本的几何体。 大多数复杂的几何体都是由这些简单的几何体构成的。

**正方体**

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2779/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2770/raw#image.png) 

```lua
cube("union",1,'#ff0000')
```
</div>
<div style="clear:both" />

**立方体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2777/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2771/raw#image.png) 

```lua
box("union",1,2,1,'#ff0000')
```
</div>
<div style="clear:both" />


**球体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2778/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2772/raw#image.png) 

```lua
sphere("union",1,'#ff0000')
```
</div>
<div style="clear:both" />

**柱体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2782/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2773/raw#image.png) 

```lua
cylinder("union",1,10,'#ff0000')
```
</div>
<div style="clear:both" />

**圆锥体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2783/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2774/raw#image.png) 

```lua
cone("union",2,4,10,'#ff0000')
```
</div>
<div style="clear:both" />

**圆环**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2784/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2775/raw#image.png) 

```lua
torus("union",10,2,'#ff0000')
```
</div>
<div style="clear:both" />

**棱柱**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2785/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2767/raw#image.png) 

```lua
prism("union",6,2,10,'#ff0000')
```
  
</div>
<div style="clear:both" />

**椭圆体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2786/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2768/raw#image.png) 

```lua
ellipsoid("union",2,4,0,'#ff0000')
```
  
</div>
<div style="clear:both" />

**楔体**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2781/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/2769/raw#image.png) 

```lua
wedge("union",1,1,1,'#ff0000')
```
  
</div>
<div style="clear:both" />

**平面**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11628/raw#plane_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11629/raw#plane_block.png) 

```lua
plane("union",1,1,"#ff0000")
```
  
</div>
<div style="clear:both" />

**圆**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11631/raw#circle_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11630/raw#circle_block.png) 

```lua
circle("union",2,0,360,"#ff0000")
```
  
</div>
<div style="clear:both" />

**椭圆**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11636/raw#ellipse_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11635/raw#ellipse_block.png) 

```lua
ellipse("union",4,2,0,360,"#ff0000")
```
  
</div>
<div style="clear:both" />

**正多边形**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11637/raw#regular_polygon_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11633/raw#regular_polygon_block.png) 

```lua
regularPolygon("union",6,2,"#ff0000")
```
  
</div>
<div style="clear:both" />

**多边形**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11639/raw#polygon_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11632/raw#polygon_block.png) 

```lua
polygon("union",{0,0,0, 1,0,0, 1,1,0},"#ff0000")
```
  
</div>
<div style="clear:both" />

**文字**
<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11638/raw#text_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11634/raw#text_block.png) 

```lua
text3d("union","Paracraft","C:/WINDOWS/FONTS/MSYH.TTC", 1, 0.1,"#ff0000")
```
  
</div>
<div style="clear:both" />

**"修改"指令**
我们可以用这些指令对最近一次创造出的几何体进行修改。

**创建对象**
一个对象将会有一个唯一的名字，它里面可以包含多个图形，在【合并】的情况下，里面的图形会进行`布尔运算`(见下文)，最终会返回一个图形。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2787/raw#image.png) 
  
</div>

```lua
createNode("object1",'#ff0000',true)
```

<div style="clear:both" />

**复制**
**复制指定名称的对象**
复制一个指定名称的对象，它的返回结果是【合并】后的一个图形。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2788/raw#image.png) 
  
</div>

```lua
cloneNodeByName("union","",'#ff0000')
```

<div style="clear:both" />

**复制上面最近的对象/图形**
复制上面最近的一个图形。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2789/raw#image.png) 
  
</div>
<div style="float:left;">
```lua
cloneNode("union",'#ff0000')
```
</div>
<div style="clear:both" />

**删除**
删除一个指定名称的对象。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2790/raw#image.png) 
  
</div>

```lua
deleteNode("")
```

<div style="clear:both" />


**移动**
移动上面最近的一个图形，它移动的是位置x,y,z的偏移值。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2791/raw#image.png) 
  
</div>

```lua
move(0,0,0)
```

<div style="clear:both" />

**旋转**
**绕中心点旋转**
找到上面最近的一个图形，在x/y/z轴，以它的中心点为原点，进行旋转。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2792/raw#image.png) 
  
</div>

```lua
rotate("x",0)
```

<div style="clear:both" />

**绕指定坐标旋转**
找到上面最近的一个图形，在x/y/z轴，以指定的世界坐标作为原点，进行旋转。

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2793/raw#image.png) 
  
</div>

```lua
rotateFromPivot("x",0,0,0,0)
```

<div style="clear:both" />

**圆角**
找到上面最近的一个图形，对该图形的选定边做圆角。

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11640/raw#fillet_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11599/raw#fillet_block.png) 

```lua
fillet('xyz',0.1)
```
  
</div>
<div style="clear:both" />


**倒角**
找到上面最近的一个图形，对该图形的选定边做倒角。

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11641/raw#chamfer_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11600/raw#chamfer_block.png) 

```lua
chamfer('xyz',0.1)
```
  
</div>
<div style="clear:both" />


**线性拉伸**
找到上面最近的一个图形，并且该图形是一个平面，沿着平面的法线方向拉伸。

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11642/raw#extrude_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11603/raw#extrude_block.png) 

```lua
extrude(1)
```
  
</div>
<div style="clear:both" />


**旋转拉伸**
找到上面最近的一个图形，并且该图形是一个平面，在x/y/z轴，以指定的世界坐标作为原点，进行旋转拉伸。

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/11643/raw#revolve_shape.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![](https://api.keepwork.com/storage/v0/siteFiles/11602/raw#revolve_block.png) 

```lua
revolve('x', 360)
```
  
</div>
<div style="clear:both" />


**"名称"指令**
我们可以给几何体起名字， 然后复制或删除它们。 

**对象名称列表**
所有的变量名称会显示在这里，方便选取

![blank](https://api.keepwork.com/storage/v0/siteFiles/3344/raw#image.png)

**"控制"指令**
这里和`代码方块`中的`控制`是完全一样的。 我们可以使用for, while, if, else等系统内置函数。

**循环**

<div style="float:left;margin-right:10px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2795/raw#image.png) 
  
</div>
<div style="float:left;">

  ```lua
for i=1, 10 do
end
```
  
</div>
<div style="clear:both" />

**"运算"指令**
这里和`代码方块`中的`运算`是完全一样的。 我们可以使用加减乘除等系统内置函数。

![blank](https://api.keepwork.com/storage/v0/siteFiles/2796/raw#image.png)

**"数据"指令**
这里和`代码方块`中的`数据`是完全一样的。我们可以创建变量，函数等等。
![blank](https://api.keepwork.com/storage/v0/siteFiles/2797/raw#image.png)


**布尔运算**
布尔运算是指CAD中几何体之间的运算。它包括：相加，相减，相交3种基本操作。 

在NPL Block Cad中，我们可以创建一个新的几何体（对象），并指定对象内部的几何体之间的关系。
首先有2种基本关系：`合并`与`不合并`。 `合并`表示对象内部的所有`布尔运算`是有效的， `不合并`则表示无效。

**合并**
  一个对象，在【合并】的情况下，【布尔运算】是【有效】的，它里面的图形会依次进行计算，顺序从上到下，计算结束后，里面的所有图形会合并成为一个图形。
  - 布尔运算: **相加 +**
  两个或多个图形进行相加的计算，最终合成为一个图形
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3029/raw#image.png)
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3024/raw#image.png)
  - 布尔运算: **相减 -**
  两个或多个图形进行相减的计算，运算顺序从上到下
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3030/raw#image.png)
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3026/raw#image.png)
  
  - 布尔运算: **相交 x**
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3031/raw#image.png)
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3027/raw#image.png)
  
**不合并**
  一个对象，在【不合并】的情况下，【布尔运算】是【无效】的，它里面存在多个图形。
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3032/raw#image.png)
  ![blank](https://api.keepwork.com/storage/v0/siteFiles/3028/raw#image.png)

## 总结
当今人类制造的大多数商品，例如杯子，手机，汽车等都是先用CAD计算机辅助设计软件设计，再将电子图纸交给机器生产出来的。 然而传统CAD软件往往操作复杂，难以熟练使用和全面掌握。NPL CAD通过编程的方式实现了专业计算机辅助设计软件的常用功能，并在不断的扩充函数类库。编程人员一般可以在30分钟内从入门到精通。

请配合本书上部的CAD项目来学习本章的内容：
- 通过编程的方式进行CAD建模
- 通过CAD，学习计算机编程语言，一举两得。
- 丰富的2D, 3D建模指令
- 随时3D预览，调试代码
- CAD模型可3D打印，或导入到Paracraft中变成角色模型

## 更多内容请见

- NPLCAD教学视频： https://keepwork.com/official/docs/videos/NPLCAD

## 附录：NPL CAD1教程
当今人类制造的大多数商品，例如杯子，手机，汽车等都是先用CAD计算机辅助设计软件设计，再将电子图纸交给机器生产出来的。 然而传统CAD软件往往操作复杂，难以熟练使用和全面掌握。NPL CAD通过编程的方式实现了专业计算机辅助设计软件的常用功能，并在不断的扩充函数类库。编程人员一般可以在30分钟内从入门到精通。


- 通过编程的方式进行CAD建模
- 通过CAD，学习计算机编程语言，一举两得。
- 丰富的2D,3D建模指令
- 随时3D预览，调试代码
- CAD模型可3D打印，或导入到Paracraft世界中变成bmax模型
- 正在构建基于NPL的专业CAD模型库和算法库

# NPL CAD 教学视频
> 课程大纲：
- [课程视频：百度云分享链接](https://pan.baidu.com/s/1Hlc-50IJyN-kJ6-fwuEiSw)

## 1. NPL CAD 安装与基本操作

![](http://git.keepwork.com/gitlab_rls_intro/keepworkkeepwork/raw/master/intro_images/img_1510248151878.jpeg)

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/351/raw#NPL CAD教学1.mp4
  ext: mp4
  filename: NPL CAD教学1.mp4
  size: 277824638
```
[在腾讯视频播放](https://v.qq.com/x/page/y0349l0lq3d.html)



## 2. NPL CAD 基本命令与实例


![](http://git.keepwork.com/gitlab_rls_intro/keepworkkeepwork/raw/master/intro_images/img_1510248378834.jpeg)
```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/352/raw#NPL CAD教学2.mp4
  ext: mp4
  filename: NPL CAD教学2.mp4
  size: 336504313
```
[在腾讯视频播放](https://v.qq.com/x/page/q0354s702rv.html)



## 3. NPL编程基础知识

![](http://git.keepwork.com/gitlab_rls_intro/keepworkkeepwork/raw/master/intro_images/img_1510248427739.jpeg)


### 3.1 语法

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/353/raw#NPL CAD教学3.1.mp4
  ext: mp4
  filename: NPL CAD教学3.1.mp4
  size: 14598980
```
[在腾讯视频播放](https://v.qq.com/x/page/s0356kaxtii.html)



### 3.2 程序的本质

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/354/raw#NPL CAD教学3.2.mp4
  ext: mp4
  filename: NPL CAD教学3.2.mp4
  size: 10164210
```
[在腾讯视频播放](https://v.qq.com/x/page/n0360pikfm0.html)



### 3.3 数字与数学

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/355/raw#NPL CAD教学3.3.mp4
  ext: mp4
  filename: NPL CAD教学3.3.mp4
  size: 11740754
```
[在腾讯视频播放](https://v.qq.com/x/page/f0361uvlgzi.html)



### 3.4 变量与名字

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/356/raw#NPL CAD教学3.4.mp4
  ext: mp4
  filename: NPL CAD教学3.4.mp4
  size: 38162422
```
[在腾讯视频播放](https://v.qq.com/x/page/r0364ayz4tj.html)



### 3.5 字符串与文字

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/357/raw#NPL CAD教学3.5.mp4
  ext: mp4
  filename: NPL CAD教学3.5.mp4
  size: 19233357
```
[在腾讯视频播放](https://v.qq.com/x/page/x03691lh7vr.html)



### 3.6 表与数组

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/358/raw#NPL CAD教学3.6.mp4
  ext: mp4
  filename: NPL CAD教学3.6.mp4
  size: 31668775
```
[在腾讯视频播放](https://v.qq.com/x/page/t0378skh757.html)



### 3.7.1 函数

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/359/raw#NPL CAD教学3.7.1.mp4
  ext: mp4
  filename: NPL CAD教学3.7.1.mp4
  size: 21894910
```
[在腾讯视频播放](https://v.qq.com/x/page/b0392s1jfxm.html)



### 3.7.2 内置函数

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/360/raw#NPL CAD教学3.7.2.mp4
  ext: mp4
  filename: NPL CAD教学3.7.2.mp4
  size: 36568707
```
[在腾讯视频播放](https://v.qq.com/x/page/s0537tzyib2.html)



## 4. NPL CAD 实例分析



![](http://git.keepwork.com/gitlab_rls_intro/keepworkkeepwork/raw/master/intro_images/img_1510248921410.jpeg)
### 4.1 NPL CAD 实例分析1

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/361/raw#NPL CAD教学4.1.mp4
  ext: mp4
  filename: NPL CAD教学4.1.mp4
  size: 35378245
```
[在腾讯视频播放](https://v.qq.com/x/page/j0538xrz07.html)



### 4.2 NPL CAD 实例分析2

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/362/raw#NPL CAD教学4.2.mp4
  ext: mp4
  filename: NPL CAD教学4.2.mp4
  size: 59259452
```
[在腾讯视频播放](https://v.qq.com/x/page/o05411w163j.html)



## 5. NPL CAD 对学习编程的建议



![](http://git.keepwork.com/gitlab_rls_intro/keepworkkeepwork/raw/master/intro_images/img_1511489648948.jpeg)

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/363/raw#NPL CAD教学5.mp4
  ext: mp4
  filename: NPL CAD教学5.mp4
  size: 37909777
```
[在腾讯视频播放](https://v.qq.com/x/page/x05091xf86y.html)

---
