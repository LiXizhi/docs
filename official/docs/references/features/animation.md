# 强大易用的骨骼动画系统

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8266/raw#骨骼动画1.mp4
  ext: mp4
  filename: sunclock.mp4
  size: 11528698
          
```

#### 骨骼系统
为了方便创作更具有感情的动画，在Paracraft中，内置了一套强大的骨骼系统。
和人体的骨骼类似，它可以控制角色做出更多精细的动作！
骨骼是一种特殊的有方向的方块，它总是指向它的上一级骨骼，并且可以控制与之相连的其它方块（类似人体的肌肉）运动。
骨骼A指向骨骼B，我们称骨骼A为骨骼B的子骨骼，骨骼B为骨骼A的父骨骼。 父骨骼运动，子骨骼也跟着运动。模型中最上级的一个父骨骼，没有指向任何其它骨骼，我们称之为根骨骼，它控制了人物整体的运动。
肢体语言是传达人物情绪的重要手段，Paracraft的骨骼系统，大部分内置角色都配备了骨骼系统，只需导入角色即可创作骨骼动画。
特有的颜色识别功能，也为蒙皮提供了更加简单的解决方案。
`注：
骨骼权重与彩色方块：骨骼的位置和方向，会影响周围的普通方块（肌肉）。
一个普通方块可能受到多个骨骼的影响，普通方块受到某个骨骼的影响大小叫做权重。
数值1代表某个方块完全跟随某个骨骼运动，0代表不跟随骨骼运动。 
在Bmax中，这个数值不是1就是0，也就是所Bmax中的某个普通方块只会受到一个骨骼方块的影响。 
此时我们也称这个方块绑定到了这个骨骼上。
父骨骼：每个骨骼最多有一个父骨骼。父骨骼移动，子骨骼也跟着运动。例如手掌与手臂相连，手臂与肩膀相连。
根骨骼：最上层的骨骼为主骨骼也叫做根骨骼， 根骨骼没有父骨骼。`


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6591/raw#BMAX02.jpg'
  ext: jpg
  filename: BMAX02.jpg
  size: '228009'
  unit: '%'
  percent: '60'
  alignment: left

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8329/raw#1574749441243U`~5QQGLSX73A2ZA@1}XUVC.jpg
  ext: jpg
  filename: '1574749441243U`~5QQGLSX73A2ZA@1}XUVC.jpg'
  size: '115775'
  unit: '%'
  percent: 60
  alignment: left

```

#### X 文件
X 文件是ParaX文件的缩写，是Paracraft中的通用模型文件格式。
X 文件是一种比Bmax文件更加通用的模型文件格式。
X 文件不仅可以记录静态的3D模型和骨骼位置关系， 还可以存储多组骨骼动画。
在Paracraft中，我们可以将一个或多个包含人物动作的电影方块，保存成一个X文件。 
然后， 我们可以在任何其它地方，重复使用它，比如可以用做NPC， 电影人物或者场景模型。
当然我们也可以将其它外部软件制作的动画模型，转化为X文件。
 
 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8332/raw#1574749944059image.png
  ext: png
  filename: 1574749944059image.png
  size: '395390'
  unit: '%'
  percent: 80
  alignment: left

```