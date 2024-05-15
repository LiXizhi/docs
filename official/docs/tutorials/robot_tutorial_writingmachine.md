# 写字机器人的设置指南
项目地址：https://keepwork.com/pbl/project/7129/
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11100/raw#1585028527200image.png
  ext: png
  filename: 1585028527200image.png
  size: '295344'
  unit: '%'
  percent: 50

```
**写字机器人主要是由三个舵机组成，两个舵机控制摆臂用来写字每一个舵机控制抬笔和落笔。**

## 1.设置CAD方块并绑定骨骼。
 **在摆臂前端制作一个标记点。**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11107/raw#1585032064377image.png
  ext: png
  filename: 1585032064377image.png
  size: '95063'
  unit: '%'
  percent: 50

```
 **旋转重合左右上摆臂使标记点重合，（之后制作的动画中也需要将两个标记点重合模拟写字动画）。**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11110/raw#1585033574806image.png
  ext: png
  filename: 1585033574806image.png
  size: '75546'
  unit: '%'
  percent: 50

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11105/raw#1585031515456image.png
  ext: png
  filename: 1585031515456image.png
  size: '393857'
  unit: '%'
  percent: 80

```
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11106/raw#1585031617984image.png
  ext: png
  filename: 1585031617984image.png
  size: '442117'
  unit: '%'
  percent: 80

```
## 2.设置舵机节点属性。
**写字机器人使用的舵机依然是180°舵机，设置属性和6轴机械臂一致。**
## 3.设置IK链。
**为了交互式操纵多个CAD图块，必须对骨架的所选部分应用反向运动学解算器（IK 解算器）。IK 解算器计算（解算）骨骼应如何以目标对象为基础移动或旋转。例如，将对首部应用 IK 解算器，目标位于尾部。在移动目标时，首部将移动到指定位置，尾部的骨骼将相应地移动和旋转。**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11114/raw#1585034814579image.png
  ext: png
  filename: 1585034814579image.png
  size: '28294'
  unit: '%'
  percent: 50

```
**这里我们使用骨骼系统中的IK图块**
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11113/raw#1585034297571image.png
  ext: png
  filename: 1585034297571image.png
  size: '2443'
  unit: '%'
  percent: 30

```
**为骨骼层次指定的 IK 解算器称为 IK 链。若要创建 IK 链，先选择填入将属于 IK 链的层次中最高的骨骼名称。在IK后面的数值中填入自顶点计算之后要控制的骨骼数。就可以创建从底部到顶部的 IK 链。在动画制作中，拖动顶点移动跟随骨骼会自动跟随移动并记录关键帧**
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11124/raw#1585100296344image.png
  ext: png
  filename: 1585100296344image.png
  size: '307541'
  unit: '%'
  percent: 90

```
**注意**
**在动画制作中，两条摆臂的顶点要相交**
**每完成一次笔画制作后，要设置抬笔和落笔舵机的动画控制，舵机旋转角度不易过大，建议设置在+20°和-5°之间**
 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11127/raw#1585101553075image.png
  ext: png
  filename: 1585101553075image.png
  size: '35063'
  unit: '%'
  percent: 70

```