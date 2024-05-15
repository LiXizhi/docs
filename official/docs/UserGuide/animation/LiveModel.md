# 活动模型

前面我们学习了如何制作[Bmax模型](https://keepwork.com/official/docs/UserGuide/scene/bmax_model)，但是常规的Bmax模型并不能在世界中任意拖动，而活动模型则是在Bmax模型基础上，支持了任意拖动和编程的功能。可以观察一下我们身边的世界，很多东西都是可以拖动的，例如笔、书、桌子、板凳等。本节我们教大家如何制作活动模型。


## 添加活动模型
下面几种方式都可以添加活动模型：
1. 从资源库中添加活动模型。
2. 在编辑模式，拖动普通bmax模型，将它变成活动模型。 
3. 从E键菜单中添加, 如下图。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29643/raw#1694577262114image.png
  ext: png
  filename: 1694577262114image.png
  size: 15200
  isNew: true
          
```

## 编辑活动模型
右键点击场景中的活动模型，可以显示编辑面板。 
:point_right: 你也可以通过Ctrl+F搜索模型， 然后按住Ctrl点击对应的条目去编辑它，如下图。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29645/raw#1694577420079image.png
  ext: png
  filename: 1694577420079image.png
  size: 47033
  isNew: true
          
```

活动模型`必须有唯一`的名字，在编辑面板，点击下方的`属性...`按钮，可以显示完整的属性面板，在这里你可以给模型起一个名字。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29644/raw#1694577322756image.png
  ext: png
  filename: 1694577322756image.png
  size: 269305
  isNew: true
          
```

- :star: 自动转向: 如果你希望拖动模型时，模型自动转向，可以将`自动转向`设置为`是`。

## 为活动模型创建代码方块
我们可以创建一组代码方块来控制活动模型。 这里有个快捷的方法，点击角色名字，可以在人物所在位置自动创建一组同名的代码方块。如下图。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29642/raw#1694577027013image.png
  ext: png
  filename: 1694577027013image.png
  size: 248232
  isNew: true
          
```

注意有告示牌的代码方块被设置为了`延迟执行`，并且代码方块的名字和活动模型是一样的。所以左侧的代码方块会等右侧的代码方块执行后才执行。我们在右侧的代码方块中可以看到`becomeAgent("entityName")`，代表当前这组代码方块用来控制场景中的某个角色。

:star: **小技巧：点击活动模型自动打开同名代码方块**
有时，我们需要玩家可以更方便的对活动模型编程。 这里有一个低代码的实现方法：
1. 在属性面板点击`点击事件`， 这里有很多常用行为。
2. 勾选`打开代码方块`，如果参数为空代表打开同名的代码方块。 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29646/raw#1694578023855image.png
  ext: png
  filename: 1694578023855image.png
  size: 132579
  isNew: true
          
```