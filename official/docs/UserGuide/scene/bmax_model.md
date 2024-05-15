## BMAX模型

**1. 理论**
今天，我们来看一个简短的动画 `The Great Inventor 伟大的发明家`。Bmax模型在动画作品中被广泛使用，已经成为动画作品不可或缺的元素。它可以实现比立方体更加精细的模型或人物，让场景细节更加丰富。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3452/raw#101. 伟大的发明家 201710.mp4
  ext: mp4
  filename: 101. 伟大的发明家 201710.mp4
  size: 92733365
          
```
腾讯视频观看地址：https://v.qq.com/x/page/e0502dkvdtf.html

**2. 实践**
- 将标准方块搭建的模型导出为Bmax模型文件，创建自定义模型方块。
- Bmax是 `Block Max/Block Model` 的简称，它能帮助我们创建更精致的静态或动画模型。
- 我们刚看过的视频中，有很多对象是用Bmax模型文件创建的。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2659/raw#26.png'
  ext: png
  filename: 26.png
  size: '433670'
  percent: 60
  alignment: left
  unit: '%'

```


**步骤1：首先，我们用标准方块搭建电影中需要使用到的对象，比如先搭建一把椅子。**
> 虽然任何一个方块都可以搭建对象，但是建议你只用`彩色方块`来搭建，这样就可以精确控制模型的颜色了。 
> 在工具栏 `建造` 标签下的 `工具` 中选择 `彩色方块`，搭建一把椅子，如下图所示。在以后的课程中，我们会介绍更多关于 `彩色方块` 的内容。 

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2660/raw#27.png'
  ext: png
  filename: 27.png
  size: '455348'
  alignment: left
  percent: '60'
  unit: '%'

```




**步骤2：选中椅子的所有方块。你可以按住 `Ctrl+左键` 点击椅子的四角(外边缘)。或者按住 `Ctrl` + `Shift`，`左键单击` 椅子最下端的一个方块(椅子脚)，即可选中所有比它高且相连的方块。**
> 在左侧属性框中点击 `保存` 按钮。 

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2661/raw#28.png'
  ext: png
  filename: 28.png
  size: '410662'
  alignment: left
  percent: 60
  unit: '%'

```


**步骤3：在弹出的导出对话框中，选择第一个 `保存为bmax模型`。**
>  输入Bmax模型文件名称（如：chair，或任何你喜欢的名字，但是建议你尽量用英文或拼音），点击 `确定` 按钮。
>  你会看到，在底部快捷栏，出现了一个模型物品chair，即模型方块。

 
 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3262/raw#未标题-1.png'
  ext: png
  filename: 未标题-1.png
  size: '386059'
  unit: '%'
  percent: '60'
  alignment: left

```

 

**步骤4：接下来，你就可以在场景中 `右键单击` 创建椅子模型了。**
>  模型方块允许你将许多基于文件的对象像普通方块一样放入3D世界中。你可以 `左键单击` 其图标来更改要使用的模型文件。除了Bmax文件，你还可以使用ParaX动画模型文件（后面章节会讲到）或FBX文件（一种全世界通用的3D模型文件格式）。
>  在场景中 `右键单击` 放置好椅子模型后，点击下方窗口中的 `模型创造` 进入编辑模式，`左键单击` 场景中的椅子模型，拖动蓝色圆环调整模型转向，拖动红绿蓝箭头调整模型位置，拖动方箭头调整模型大小。
>  模型占一个方块的空间，没有精确的物理碰撞，即人物只能走上并站在隐形的方块上，并不能真正紧贴地站在模型上。模型被放大后，由于没有精确的物理碰撞，人物可直接穿过模型。
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2663/raw#30.png'
  ext: png
  filename: 30.png
  size: '320070'
  alignment: left
  percent: '60'
  unit: px
  width: 550

```


如果你想让模型具有精确的物理碰撞，你可以使用Bmax文件创建一个 `物理模型`：
- 在 `E` 键工具栏 `电影` 项下，选择 `物理模型` 图标（有橙色背景的）。
- `左键单击` 底部快捷栏中 `物理模型` 的图标，将Bmax文件更改为 `blocktemplates/chair.bmax`。你也可以点击 `...` 按钮，通过文件浏览器来选择它。
- 同理，在场景中 `右键单击` 放置好椅子的物理模型后，点击下方窗口中的 `模型创造` 进入编辑模式，`左键单击` 场景中椅子的物理模型，对其转向，位置和大小进行调整。
- 物理模型具有精确的物理碰撞，人物可以精确紧贴地站在物理模型上，不可穿过物理模型。
 


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2664/raw#31.png'
  ext: png
  filename: 31.png
  size: '572384'
  alignment: left
  percent: 60

```

##### 延伸知识：关于保存成模板template的使用
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4012/raw#image.png'
  ext: png
  filename: image.png
  size: '215953'
  unit: '%'
  percent: 50
  alignment: left

```
如果我们想将建筑物在其它的世界中打开使用，可以通过保存为template模板后复制模板到场景中。template将为我们记录了所有方块信息，也包括电影方块的镜头，以及所有演员。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4013/raw#image.png'
  ext: png
  filename: image.png
  size: '105922'
  alignment: left
  unit: '%'
  percent: 40

```
保存信息的填写，如果不勾选演员使用相对位置选项，则演员会使用绝对位置，也就是当前世界电影演员所在的坐标位置。
模型名称需要命名，目录的路径选择全局模板，全局模板可在任意世界中共享使用。
确认好以上信息后，按保存。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4014/raw#image.png'
  ext: png
  filename: image.png
  size: '39145'
  unit: '%'
  percent: 40
  alignment: left

```
加载模板方法：
按E键打开菜单栏，模板项下的标签中选择全局模板。首次使用请按刷新按钮，以保证保存的模板已同步。
在全局模板中左键单击选择刚刚所保存的模板命名，模板就会出现在世界场景中了。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4015/raw#image.png'
  ext: png
  filename: image.png
  size: '415024'
  unit: '%'
  percent: 60
  alignment: left

```
## 关于无限分裂方块 VoxelModel

Paracraft模型还支持一种特殊的模型，叫做体素模型VoxelModel，也叫做**无限分裂方块**。
点击了解更多[VoxelModel](https://keepwork.com/official/docs/UserGuide/scene/voxelmodel)