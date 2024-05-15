# 无限分裂方块 Voxel Model

用户可以对默认大小为1的方块，进行任意尺度的动态编辑。
无限分裂方块内部使用了一个无指针的Octree, 磁盘加载速度极快，占用内存很小，支持自动lod。

## 从ply文件导入
我们可以从`*.ply` point cloud文件初始化和加载一个Voxel Model. 
> 注意：不是ply的多边形格式，只支持point格式的ply文件，不支持face. 

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35544/raw#1709699990427image.png
  ext: png
  filename: 1709699990427image.png
  size: 286412
  isNew: true
          
```
### 如何生成ply文件

很多外部工具可以导出ply格式的点云数据。这里推荐 [MagicaVoxel](https://ephtracy.github.io/)

点击MagicaVoxel中的Export，并选择point. **注意不要选择ply, 一定是point**.  就可以导出ply格式的文件了。 拖动到paracraft窗口中可以安装。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35545/raw#1709700191610image.png
  ext: png
  filename: 1709700191610image.png
  size: 113630
  isNew: true
          
```

Paracraft也可以导出ply格式的模型， 选择方块，然后点击保存，选择ply点云即可。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35546/raw#1709700365746image.png
  ext: png
  filename: 1709700365746image.png
  size: 137550
  isNew: true
          
```


## VoxelModel基础编辑API

我们可以针对任意的bmax文件模型，进行体素编辑。如下：

```javascript
--local model = GetEntity():GetInnerObject():GetPrimaryAsset():GetAttributeObject():GetChildAt(0):GetChild("VoxelModel")
local model = ParaScene.GetPlayer():GetPrimaryAsset():GetAttributeObject():GetChildAt(0):GetChild("VoxelModel")
model:SetField("MinVoxelPixelSize", 4);

local function SetModelblock(x, y, z, level, color)
	model:SetField("SetBlock", format("%d,%d,%d,%d,%d", x, y, z, level, color or -1));
end
local function PaintModelblock(x, y, z, level, color)
	model:SetField("PaintBlock", format("%d,%d,%d,%d,%d", x, y, z, level, color or -1));
end
local function DumpModel()
	model:CallField("DumpOctree");
end
model:SetField("SetBlock", "0,0,0,1,-1");
```

## 批量编辑指令

我们可以使用批量编辑指令对BMAX模型进行体素化编辑。 **model:SetField("run", "")**

```javascript
model:SetField("run", "color 0;level 64;setrect 0,0,0,63,63,0");
model:SetField("run", "level=4;paintrect 0,0,0:2,0,0:#ff0000#00ff00#ff");
model:SetField("run", "level=4;paintrect 2,1,0:0,1,0:#ff0000#00ff00#ff");
```

全部支持的命令如下：

- [e.g.](e.g.) "setblock 0,0,0,1,-1 level 8 color #ff0000 set 0,0,0,1,1,1,0,1,0"
- @note: one can also call this function multiple times to separate a long command like:
-   first send "offset 4,4,4 level 8 color #ff0000 setwithoffset", then "0,0,0,1,1,1,0,1,0".  it will cache previous states of cmd, level and color.
-   this allows one to reuse long command list string with different offset, level, and color.
- offset x,y,z: [e.g.](e.g.) "offset 2,0,0", all position in the following commands will be offset by 2,0,0.
- level l: [e.g.](e.g.) "level 8", all positions in the following commands will be at level 8.
- color c: [e.g.](e.g.) "color #ff0000", "color -1", all colors in the following commands will be set to 0xff0000.
- del x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "del block at all given positions at predefined level. 
- delwithoffset x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "del block at all given positions at predefined level. 
- set x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "set block at all given positions at predefined level and color.
- setwithoffset x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "set block at all given positions at predefined offset, level, and color.
- setxyzcolor x1,y1,z1,color1,x2,y2,z2,color2, ... : [e.g.](e.g.) "set block at all given positions at predefined level.
- setblock x,y,z,level,color,... : [e.g.](e.g.) "setblock 0,0,0,1,-1". set the block at (0,0,0) at level 1 to empty.
- setrect fromX,fromY,fromZ,toX,toY,toZ: [e.g.](e.g.) "color 0;level 64;setrect 0,0,0,63,63,0". with current color and level.
- paint x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "paint block at all given positions at predefined level and color.
- paintwithoffset x1,y1,z1,x2,y2,z2, ... : [e.g.](e.g.) "paint block at all given positions at predefined level and color.
- paintblock x,y,z,level,color,... : [e.g.](e.g.) "paintblock 0,0,0,1,#ff0000". paint all blocks to red. 
- paintxyzcolor x1,y1,z1,color1,x2,y2,z2,color2, ... : [e.g.](e.g.) "paint block at all given positions at predefined level.
- paintrect fromX,fromY,fromZ,toX,toY,toZ,color1,color2,...: [e.g.](e.g.) "paintrect 0,0,0,63,63,0,#ff#ff00#ffff00(...64*64 color values)". 
-    if for example fromX is bigger than toX, the rect will be painted flipped on x axis, this allow applys to y and z. 
- paintrect fromX,fromY,fromZ,toX,toY,toZ,data:image/png;base64,...: paint the rect with image data.

## 动态打印3D网页

我们可以用bmax模型 512*512 分辨率动态3D打印 网页视频。 可分裂方块有很高的动态更新性能，同时占用很少的内存和磁盘空间。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35324/raw#1706869952647bmax camera.mp4
  ext: mp4
  filename: 1706869952647bmax camera.mp4
  size: 6467559
  isNew: true
          
```


## 无限分裂方块的应用案例分析

```@Project
styleID: 1
project:
  projectId: '2155789'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
###> 项目简介

:heart:这是一款专为paracraft玩家设计的`解压游戏`：打印模型，粉碎模型 

- 将任意BMAX模型`拖动`到打印机方框中，开始打印。
- 打印完毕后，模型分身会自动从高处掉落并`粉碎`，十分解压。
- 支持`纳米级`3D打印，和自动lod分辨率，占用很少内存。
- 可以从`商城`中找一些`上百万`方块的bmax模型尝试打印。 
- 可以通过可计算文档，更改打印机的`材料颜色`。
- `站在`不同颜色的方块上可以打印不同颜色的物品。
- 你可以同时启动`多台`打印机，触发隐藏剧情。

### 设置打印材料的颜色

下面代码根据打印的进度**msg.progress**, 设置打印机的物料的颜色HSL，从红到紫，每秒改一点。
```@CodeBlock
styleID: 0
codeblock:
  projectId: '2155789'
  title: ''
  name: printerproperty
  language: codeblock
  code: |-
    registerBroadcastEvent("VoxelPrinterOnProgress", function(msg) 
        fromColor = System.Core.Color.HSLToColor(msg.progress or 0, 0.5, 0.5, 0)
        broadcast("SetPrinterProperty", {color = fromColor, speed = 1})
    end)
  outputMode: autoParacraft
  output: ''
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: false

```

## VoxelPrinter 体素打印机模组

### 使用说明

- 拖动任意bmax活动模型到静态标签为`3dprinter`的活动模型，可以将模型打印到带标签的模型中。
- 你也可以通过发送下面的消息打印任意bmax文件到活动模型中：
```
broadcast("PrintBmaxFileOnModel", {filename="some.bmax", entityName="AnyBmaxEntityNameInTheScene"})
```
在打印的过程中，可以发送下面消息，改变打印机物料的颜色，打印速度，最小颗粒的屏幕像素等属性。
```
broadcast("SetPrinterProperty", {color = 0xff0000, speed = 1, MinVoxelPixelSize=4})
```
注册下面事件，可以监听打印机的状态：
```
registerBroadcastEvent("VoxelPrinterOnProgress", function(msg)
  tip(msg.progress)
end)
```
