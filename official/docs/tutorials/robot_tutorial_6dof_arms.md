# 6轴机器人的设置指南
项目地址：https://keepwork.com/pbl/project/7592/


## 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11074/raw#1585015573173image.png
  ext: png
  filename: 1585015573173image.png
  size: '261659'
  unit: '%'
  percent: 50

```

## 1.首先进行CAD建模

**先按照比例依次设计每个关节需要的CAD方块，默认坐标为0.点击运行效果如下。**
**按照实体机械臂的比例放置积木（按照实体比例编辑骨骼是为了方便之后调整动画），这里建议每个积木方向统一，方便之后设置骨骼。**
**在这个模型中，一共使用到六个舵机。所以制作模型的时候至少不少于六块CAD积木。每块积木可以控制一个舵机。**
 
如图所示
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11075/raw#1585015779914image.png
  ext: png
  filename: 1585015779914image.png
  size: '379216'
  unit: '%'
  percent: 50

```
## 2.设置骨骼。将CAD方块按照实体机械臂的组装逻辑用骨骼系统链接起来。
如图所示
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11076/raw#1585016013550image.png
  ext: png
  filename: 1585016013550image.png
  size: '60310'
  unit: '%'
  percent: '30'
  alignment: center

```
**注意；每一个骨骼的中心0坐标都以上一根骨骼0坐标为中心。（如调整第一根骨骼坐标移动1.第二根骨骼则不需要移动坐标，会跟随第一根骨骼移动），每一个骨骼默认控制移动选择大小的坐标点都在其方块的最中心。骨骼绑定系统的中可以调节骨骼点的位置。方块object的坐标可以调整cad方块的位置。**

**例如以下示例**

**初始数值默认都为0**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11078/raw#1585016131690image.png
  ext: png
  filename: 1585016131690image.png
  size: '122309'
  unit: '%'
  percent: 80

```
**方块向左Z轴移动1  骨骼点向上Y轴移动2**
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11080/raw#1585016425622image.png
  ext: png
  filename: 1585016425622image.png
  size: '176185'
  unit: '%'
  percent: 80

```


**将CAD方块依次按照示例六轴机械模型比例适配骨骼系统之后，一共有六个节点对应六个舵机。**
如图所示
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11081/raw#1585016494984image.png
  ext: png
  filename: 1585016494984image.png
  size: '221742'
  unit: '%'
  percent: 80

```
## 3.设置骨骼节点对应舵机属性。（在这里我们使用的舵机扭转角度为0-180°）。
**将约束属性依次拖入骨骼名称下**
如图所示
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11082/raw#1585016633819image.png
  ext: png
  filename: 1585016633819image.png
  size: '20021'
  unit: '%'
  percent: 30

```
### 设置参数详解
**骨骼名称：填写节点的名称。**

**最小角度最大角度：舵机以角度0为中心。正负角度旋转。所以180°的舵机分为+90和-90度范围值**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11083/raw#1585016735889image.png
  ext: png
  filename: 1585016735889image.png
  size: '64578'
  unit: '%'
  percent: 30

```

**偏移角度：舵机左右旋转最大夹角数。**

**舵机通道：对应micro:bit扩展转接板上的插槽。**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11084/raw#1585016801702image.png
  ext: png
  filename: 1585016801702image.png
  size: '139710'
  unit: '%'
  percent: 30

```

**舵机缩放值：缩放值只有1和-1两个选项填写。默认为1.当实体舵机测试时发现旋转方向和动画相反，即填写相反的数值再运行。**

**旋转轴：对应XYZ三个轴，只能旋转一个方向旋转，根据实体机械臂的需要设置。**

**隐藏骨骼：默认（false）显示骨骼，不显示骨骼选择（true）。**

## 制作完成