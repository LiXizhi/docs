# NPLBlockCAD v1.0
**全称：** 基于NPL语言和代码方块的计算机图形辅助设计软件
**简称：** NPLBlockCAD
**软件用途：** 通过编程的方式创造彩色的3D模型。
**运行环境：** Windows 10
**编程语言：** NPL语言, C++
**开发完成时间：** 2019年1月18日
**发表日期：** 2019年1月18日
**产品特点：**
 - 一种全新的面向图形设计的编程模式
 - 丰富的3D建模指令，操作简单
 - 支持可视化与文本式编程
 - 实时编辑，实时预览
 - 支持.x|.stl|.gltf等格式文件的导出
 
**源代码行数**: 5.5万行 [点击这里查看](NPLBlockCad_code)
## NPL Block CAD 使用手册
### 创建一个桌子
- 创建npl block cad 代码方块
![](https://api.keepwork.com/storage/v0/siteFiles/2677/raw#7ca9b3d0-3b11-11e9-9f68-37fa0c8ce72e.png)
- 将代码方块命名为table
 ![](https://api.keepwork.com/storage/v0/siteFiles/2678/raw#image.png)
- 点击【图块】
 ![](https://api.keepwork.com/storage/v0/siteFiles/2679/raw#image.png)
- 在网页上输入代码
 ![](https://api.keepwork.com/storage/v0/siteFiles/2712/raw#image.png)

- 点击【运行】，查看效果
![](https://api.keepwork.com/storage/v0/siteFiles/2681/raw#image.png)
![](https://api.keepwork.com/storage/v0/siteFiles/2683/raw#image.png)

 
- 把【不合并】改为【合并】，运行代码，再次查看效果
![](https://api.keepwork.com/storage/v0/siteFiles/2680/raw#image.png)

![](https://api.keepwork.com/storage/v0/siteFiles/2682/raw#image.png)

```lua
createNode("object1",'#ff0000',true)
box("union",4.5,4.5,3.5,'#ff0000')
move(0,0.6,0)
box("difference",3.5,10,3.5,'#00ffb6')
box("difference",10,3.5,3.5,'#0043ff')
```
### 创建一个空心的盒子
- 创建npl block cad 代码方块，并命名为hollowbox
- 点击【图块】,在网页上输入代码
![](https://api.keepwork.com/storage/v0/siteFiles/2702/raw#image.png)


- 点击【运行】
![](https://api.keepwork.com/storage/v0/siteFiles/2700/raw#image.png)


 
- 把【不合并】改为【合并】，再次运行
![](https://api.keepwork.com/storage/v0/siteFiles/2703/raw#image.png)
- 点击【运行】
![](https://api.keepwork.com/storage/v0/siteFiles/2699/raw#image.png)
- 接下来增加代码
![](https://api.keepwork.com/storage/v0/siteFiles/2704/raw#image.png)
 
- 点击【运行】
![](https://api.keepwork.com/storage/v0/siteFiles/2705/raw#image.png)
```lua
createNode("object1",'#fff600',true)
cube("union",2,'#ff0000')
sphere("intersection",1.3,'#ff0000')

createNode("object2",'#0083ff',true)
cube("union",3,'#ff0000')
sphere("difference",2,'#ff0000')
```
 ## NPL Block CAD的指令集
下面是NPL Block CAD的常用指令集和例子。全部CAD指令分成了：图形，修改，名称， 控制，运算，数据，布尔运算几个大类。 


**"图形"指令**
图形指令主要用于创建基本的几何体。 大多数复杂的几何体都是由这些简单的几何体构成的。

**正方体**

<div style="float:left;width:120px;">
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2779/raw#image.png) 
  
</div>
<div style="float:left;margin-left:10px">
  
![图 3.1](https://api.keepwork.com/storage/v0/siteFiles/2770/raw#image.png) 

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
  
![图 3.2](https://api.keepwork.com/storage/v0/siteFiles/2771/raw#image.png) 

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
  
![图 3.3](https://api.keepwork.com/storage/v0/siteFiles/2772/raw#image.png) 

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
  
![图 3.4](https://api.keepwork.com/storage/v0/siteFiles/2773/raw#image.png) 

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
  
![图 3.5](https://api.keepwork.com/storage/v0/siteFiles/2774/raw#image.png) 

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
  
![图 3.6](https://api.keepwork.com/storage/v0/siteFiles/2775/raw#image.png) 

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
  
![图 3.7](https://api.keepwork.com/storage/v0/siteFiles/2767/raw#image.png) 

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
  
![图 3.8](https://api.keepwork.com/storage/v0/siteFiles/2768/raw#image.png) 

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
  
![图 3.9](https://api.keepwork.com/storage/v0/siteFiles/2769/raw#image.png) 

```lua
wedge("union",1,1,1,'#ff0000')
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

```lua
cloneNode("union",'#ff0000')
```
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

**"名称"指令**
我们可以给几何体起名字， 然后复制或删除它们。 

**对象名称列表**
所有的变量名称会显示在这里，方便选取

![](https://api.keepwork.com/storage/v0/siteFiles/3344/raw#image.png)

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

![](https://api.keepwork.com/storage/v0/siteFiles/2796/raw#image.png)

**"数据"指令**
这里和`代码方块`中的`数据`是完全一样的。我们可以创建变量，函数等等。
![](https://api.keepwork.com/storage/v0/siteFiles/2797/raw#image.png)


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