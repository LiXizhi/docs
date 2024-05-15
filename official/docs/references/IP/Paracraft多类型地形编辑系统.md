#  Paracraft多类型地形编辑系统 v1.0

**软件用途：** Paracraft多类型地形编辑系统提供了系统化的统一方案，对已有地形进行快速批量的编辑。
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** NPL语言, C++
**开发完成时间：** 2018年6月1日
**发表日期：** 2018年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 大批量的快速编辑
- 参数可调节
- 多种编辑模式
- 操作方法简单友好

**源代码行数**: 3万 [点击这里查看](Paracraft多类型地形编辑系统_code)

## 使用手册





## 地形


3d引擎中的地形是由一张高度图（heightMap）构成的，高度图通常是一张二值图，大小为（2^n+1）。它的每个像素的灰度值表示地形每一点的高度值。用这些高度值作为顶点信息绘制三角面片。

为了高效，实时绘制地形，Clark提出了层次细节模型（LOD）。这个模型认为当物体覆盖屏幕较小区域时，可以使用该物体描述较粗的模型。

基于LOD的地形网格简化算法分为动态LOD和静态LOD。在NPL中使用的ROAM算法（实时优化自适应网格），这个算法就是动态的LOD。而GeoMipMap算法是静态LOD。在NPL中提供了了基于四叉树的ROAM算法和geomipmap算法，可以根据不同需求使用这两种算法。

ROAM算法的思想是在对地形现实的时候，根据视点和视线的位置和方向等多种因素，对地形表面的三角片面进行三角形的分裂和合并，最终形成与原始表面近似的简化表面。ROAM算法的基础是等腰三角形可以从直角顶点到斜边引一条垂线，将这个等腰直角三角形分成大小相等的两个小等腰直角三角形，并且可以无限递归下去。

在NPL中用四叉树来组织描述地形，先把可视范围内的地形分割成4等份矩形子块，依靠计算判定影子来检测4个子块，如果检测到某个子块的网格精度达到绘制要求，就不再往下分割；否则就继续分割为更小的子块，知道所有子块的矩形网格达到渲染精度。

如果在NPL中使用GeoMipMap算法模拟地形，那么就要地形必须是$(2^n+1)*(2^n+1)$。GeoMipMap算法实际是把地形在xz平面分块（block），每块block都有自己的层次细节等级，边长满足$2^n+1$，用不同的分辨率网格模型来描述。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4141/raw#image.png'
  ext: png
  filename: image.png
  size: '64385'
  unit: '%'
  percent: 50

```

> GeoMipMap算法分割地形示意图
	
层次细节中基于四叉树的ROAM算法比较考验CPU的计算能力，而GeoMipMap算法则将计算中心放在GPU。

### 地形的组成
NPL地形中，无论哪种方法都是将TerrainBlock类作为层次细节算法的节点类。在这个类中定义了他的子节点和父节点：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4140/raw#image.png'
  ext: png
  filename: image.png
  size: '5009'
  unit: '%'
  percent: 40

```


如果使用GeoMipMap算法则还有：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4139/raw#image.png'
  ext: png
  filename: image.png
  size: '11006'
  unit: '%'
  percent: 40

```

等信息。
并且提供了构造不同三角带的方法

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4138/raw#image.png'
  ext: png
  filename: image.png
  size: '21493'
  unit: '%'
  percent: 60

```


还有修复裂缝的方法

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4137/raw#image.png'
  ext: png
  filename: image.png
  size: '17460'
  unit: '%'
  percent: 70

```


### 地形的管理
地形管理中主要用到了Terrain和CGlobalTerrain这两个类。在Terrain中实现了ROAM算法的主体里面有四叉树根节点：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4136/raw#image.png'
  ext: png
  filename: image.png
  size: '5381'
  unit: '%'
  percent: 60

```


Terrain中，实现了对上诉两种方法的算法支持，都提供了许多方法。首先是对基于四叉树的ROAM算法，有分割和合并方法，还有裂缝修复等。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4135/raw#image.png'
  ext: png
  filename: image.png
  size: '61683'
  unit: '%'
  percent: 80

```

在地形管理流程:
Geomipmap的管理流程（证据不足版本）：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4134/raw#image.png'
  ext: png
  filename: image.png
  size: '27403'
  unit: '%'
  percent: 80

```

>  GepMipMap的管理流程

基于四叉树的管理流程：


 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4133/raw#image.png'
  ext: png
  filename: image.png
  size: '29977'
  unit: '%'
  percent: 80

```

> 四叉树管理流程


### 地形笔刷和笔画

地形笔刷和笔画物品可批量修改地形地貌

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4131/raw#image.png'
  ext: png
  filename: image.png
  size: '562390'
  unit: '%'
  percent: 80

```



```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4132/raw#image.png'
  ext: png
  filename: image.png
  size: '674184'
  unit: '%'
  percent: 80

```



每个物品可以复制多个到下方快捷栏, 每个复制的物品可以有各自不同的参数：例如半径，材质，强度，子工具等。

所有工具都有如下几个参数：
   半径： +/-键或按住Shift键并滚动鼠标滚轮
   强度：可输入数值(0,1] 默认为0.5
   材质：可用Alt+左键在场景中吸取，或在E键物品列表中选取
   原点：鼠标所在位置

点击左键可使用工具一次， 也可以按住左键不放拖动鼠标，此时每0.2秒使用一次
Ctrl+Z/Y可撤销Undo/Redo. 注意：鼠标按下，拖动到抬起只算作一次操作，尽管期间可能执行了多次操作。
点击鼠标中键可瞬移
按住Shift键并点击鼠标，进入相反的模式，例如：地形的升/降, 平滑/锐化.

#### 地形笔刷物品

更改地形，地貌，创造或消除大面积的水等等。 有几个子工具：

用Gaussian Filter地形升降制作山脉或峡谷： 按住Shift为降低。可以长按并拖动鼠标大面积操作
平滑和锐化地表： 用一个4*4的Filter取平均值。可以长按并拖动鼠标大面积操作
    提示：我们一般先用地形升降后再使用平滑工具。
地表铲平: 将地表铲平到鼠标的高度. 可以长按并拖动鼠标大面积操作，高度会被锁死。
    提示：我们一般先用地形升降工具，然后地表铲平可以快速制造大面积的低洼河床或梯田。
在鼠标的高度创建湖泊：可以长按并拖动鼠标大面积操作，高度会被锁死。如果同时按住Shift键为取消湖泊。
    请先用地表铲平工具制造出低洼的地形（水坑），然后调大半径，从岸边你希望的高度开始点击并拖动鼠标，所有下面坑洼的地方会被自动填充。
   尽量不要在平地上直接使用这个工具，请从岸边开始。

##### 注意事项：

液体如水不会随地形改变而改变
非方块物品：如：花草会随地形一同升降
高地形时，其实是拉伸第二层，保留最上面一层
 地形时，则是直接降低，露出下面的地貌。

#### 画笔物品

需要先选择材质： 可用Alt+左键在场景中吸取，或在E键物品列表中选取

##### 注意事项：

非方块类物品是在地面上方增加： 如：花，草
方块类物品是替换：如：石子路
按住Shift键可强制使用替换模式
