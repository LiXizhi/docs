# Paracraft图形UI动态语言MCMLv1.0

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

**源代码行数**: 10万 [点击这里查看](Paracraft图形UI动态语言MCMLv1.0_code)

## 使用手册



# UI系统
## UI
### 综述

2D GUI是ParaEngine的重要特征，它是玩家和虚拟世界的控制链接。它从接收玩家从鼠标，键盘或者其他输入设备的信号，并激活相应的脚本去处理对应的输入信息，并对虚拟世界做出相应的改变。
在NPLRuntime中，提供了许多支持玩家和虚拟世界交互的方式。其中两个关键的特点是低门槛和可靠性。在可靠性方面，有着对虚拟元素进行操作的稳定架构。NPLRuntime允许我们将不同层级的图片混合起来，这样能够使结果丰富多彩。此外，还提供了丰富的和UI引擎交互的API函数，使我们能够对UI对象的每一个非常微小的部分进行操作。在操作函数方面，有着许多不同种类参数的函数。
对于整个UI体系，可以用下图描述：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4149/raw#image.png'
  ext: png
  filename: image.png
  size: '111077'
  unit: '%'
  percent: 60

```

>  UI体系结构
	
  底层是UI库，包含按钮，容器等。 有了UI库就可以用于构造UI模型，NPL用的是通用的3层UI模型： 背景-工艺-覆盖。 然后管理UI模型的方法是显示和逻辑分离的方法， 用MCML语言编写显示部分（也可以用脚本写UI显示，但是因为难以管理，所以不推荐）， 用NPL脚本控制UI逻辑。这种显示，逻辑分离的架构有点像网站开发的MVC开发模式。
### UI创建流程
1. 使用ParaUI.CreateUIObject()创建一个对象。
2. 设置相关属性。
3. 将所创建的对象附加到某一个东西上面。（使用AttachToRoot()函数将UI对象附加到UI root上，使用AddChild()将新UI对象附加到旧UI对象上，作为其子对象。Root对象是UI树的根，不可见，控制着整个UI系统的逻辑）
4. 重复上述过程

### UI对象类别
根控件对象：它是所有GUI对象的最上层容器，它收集所有输入设备的状态信息然后发送给它的子对象。同时，它也控制着子对象的渲染过程。
资源对象：它是一种与控制无关的对象，它包含着为渲染一类特殊控件的所有必要的资源。例如，如果我们想要交换按钮A和B，我们不需要交换按钮只需要交换相应的资源对象。
脚本对象：它是一个脚本容器和激活器,通常被附加到一个资源对象上。

### GUI类层次结构
整个GUI系统的骨架及之间的关系可以总结为下图：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4150/raw#image.png'
  ext: png
  filename: image.png
  size: '18229'
  unit: '%'
  percent: 60

```

>   GUI 类层级结构

CGUIbase：所有GUI元素的基类，它定义了GUI对象的基本行为，如各种对象的get、set方法，bool CGUIBase::Equals(const IObject *obj)const、bool CGUIBase::OnClick(int MouseState, int X, int Y)、bool CGUIBase::OnMouseLeave()等等。
CGUIResource：CGUIResource类封装了渲染一个类的必要资源，描述一个元素的必要游戏数据，和游戏引擎交互的必要脚本从而达到轻易地交换相同类型的控件。如将一个背包中的元素拖动到活动元素表。这个类中包含了控制控件这种行为的代码。
CGUIScript：提供为GUI对象添加控制脚本的接口
CGUIContainer：所有能够拥有子对象的控件都必须继承CGUIContainer。CGUIContainer提供了一个容器应有的基本的函数和属性，例如：get/lost focus and mouse in/out。
CGUIRoot：这个类充当GUI系统的基本容器和控制器，它负责管理键盘和鼠标，将键盘鼠标还有其他事件调度到合适的位置，帮助管理GUI对象。

### UI资源架构

资源对象被设计成独立对象，意思是它们不会和某一对象有关联。要交换两个对象的展示效果非常简单，只需要把两个对象的资源对象交换。下图展示了资源对象的架构。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4151/raw#image.png'
  ext: png
  filename: image.png
  size: '47380'
  unit: '%'
  percent: 60

```

>  UI资源架构

从上面的架构图中，我们可以看到UI资源架构包含三个层级：overlay，artwork和background。这三个层级都是用alpha blending绘制的。（详见Direct X SDK帮助文档）
层（layer）被用来将不同的纹理结合在一起，来达到特殊的效果。例如在下图中所展示的效果至少是由两个层级所结合起来的。支持不同的层级不仅仅使UI设计者能够将不同的纹理结合在一起，同时也减少了艺术效果方面的工作量。如果只有一个层，则必须为每个按钮制作这样的倒计时效果。如果存在多层，则只需要为一个按钮做出这种倒计时效果，然后根据对应的按钮事件，对不同的按钮实现这种效果。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4152/raw#image.png'
  ext: png
  filename: image.png
  size: '25006'
  unit: '%'
  percent: 60

```

> 按钮倒计时效果

覆盖层（overlay layer）：覆盖层处在工艺层之上，它展示对象的上层工艺。只有在明确设置它的时候才会存在。
工艺层（artwork layer）：工艺层在背景层之上，它是一个默认的层级。它包含着对象的默认工艺。在大多数情况下，使用该层就足够了。（当背景层和覆盖层存在的时候，引擎会自动绘制它们。因此将增加引擎的渲染时间且影响引擎的性能。因此只有在必要的情况下才会使用另外两个层级）
背景层（background layer）：背景层是处在最底端的一个层级。它用来展示背景工艺。只有在明确设置它的时候才会存在。

对于每一个层级，有四种状态：normal, highlight, pressed and disabled。
Normal状态：一个对象的默认状态。
Highlight状态：一个对象的hightlight状态。例如鼠标停留在一个按钮上的时候。
Pressed状态：一个对象的pressed状态。例如一个按钮被鼠标点击的时候。
Disabled状态：一个对象的disabled状态。一些对象当它们disabled，它们将有不同的表现。
对于每一种状态，有许多字体元素和纹理元素。每个元素包含着有关渲染的许多信息。（更多信息见NPL参考文献）
一个对象的脚本同样也储存在UI资源架构体系中。对于UI资源架构体系中每一种事件，最多只有一个脚本实例。

### 常见属性

|属性|	描述|
|---|----|
|name	|String类型，对象的名字|
|x|	number类型，对象左上角的坐标|
|y	|number类型，对象左下角的坐标|
|width|	number类型，对象的宽度|
|height|	number类型，对象的高度|
|candrag	|boolean类型，对象是否能被拖动，默认为false|
|receivedrag|	boolean类型，对象是否能接收一个拖动事件，默认为false。尽管所有UI控件均有该属性，仍不建议在除container之外的控件中使用它|
|type	|string类型，只读，对象的种类。可以是“button”，“text”，“editbox”，“imeeditbox”和“container”|
|lifetime|	number类型，离对象被自动删除的帧数。如果为正数，lifetime将在每帧自动减少。默认值为-1，意味着永久有效|
|parent	|ParaUI对象，gets或sets对象的parent|
|tooltip	|string类型，gets或sets当前对象的提示信息。默认为“”。tooltip是一种在帮助人们理解对象的含义或将人们注意力转移到对象上非常有用的弹出信息对话框|
|enabled|	boolean类型，enables者disables指定对象。一个disabled对象是可见的但是不能接收任何事件，默认为true|
|visible	|boolean类型，控制对象是否可见。一个不可见的对象是看不见但是任然能够接受事件，默认为true|


### 常见方法

|方法|	描述|
|--|-|
|IsValid	|获取对象是否是一个有效deGUI对象。如果对象无效，用户将不能够使用这个对象，则结果不可预测。|
|AttachToRoot|	将对象附加到root上|
|AttachTo3D|	将对象附加到3D对象上|
|GetFont  |	根据给定的名字获取对象的字体|
|GetTexture|	根据给定的名字获取对象的纹理|
|SetCurrentState|	设置当前状态|
|SetActiveLayer	|设置活动层|


### UI对象实例


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4153/raw#image.png'
  ext: png
  filename: image.png
  size: '12211'
  unit: '%'
  percent: 60

```

> 按钮
 
代表着GUI的按钮控件。

一个按钮能够使用鼠标点击。它能够接收以下事件：onclick,ondoubleclick, ondragbegin, ondragend, onmousedown, onmouseup, onmousehover
创建方法：

    object= ParaUI.CreateUIObject("button","buttonname","_lt",50,20,600,400)

|属性 | 类型|
|-|-|
|text	|string类型，对象的文本信息
|background|	string类型，对象的背景图片文件路径+[“;”+left+””+top+””+width+””+height]“left”,“top“，“width”和“height”一起形成了一个矩形，表明了背景图片展示的区域。“[]”内均是可选的，如果没有指定，则表明整张图片图片文件路径+[“:”+left+””+top+””+width+””+height]“；“表示截取图，”：”表示点九图，即保持四个角不变，对选中的区域进行扩展
|background	|对象的背景纹理
|text	|对象的文本信息，用来在按钮上显示文字


container
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4154/raw#image.png'
  ext: png
  filename: image.png
  size: '38036'
  unit: '%'
  percent: 60

```

>  容器
	
表示一个GUI中的容器控件。它能够有子控件，一个容器有两个滚动条——垂直滚动条和水平滚动条。如果属性“scrollable”是false或者在容器中的控件完全在容器的客户区，那么滚动条将不会显示出来。
一个容器不接收任何事件。

创建方法：

    object= ParaUI.CreateUIObject("container","containername","_lt",50,20,600,400)
|属性|描述|
|-|-|
|scrollable|	boolean类型，控制容器是否可滚动，默认为false
|scrollbarwidth|	number类型，容器的滚动条的宽度，默认为25
|fastrender|	boolean类型，决定是否在容器内使用快速渲染模式，默认为true
|background|	string类型，对象的背景
|GetChild	|获取容器的给定名字的第一个子对象（如果存在重复的名字），根据给定的名字返回ParaUI对象，如果对象不存在，返回ParaUI对象的IsValid()方法的false返回值
|GetChildAt	|根据给定的索引获得子对象
|AddChild  	|添加一个子对象到容器
|background|	对象的背景纹理

scrollbar
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4156/raw#image.png'
  ext: png
  filename: image.png
  size: '15839'
  unit: '%'
  percent: 60

```

>  滚动条
	
表示一个GUI中的滚动条控件。滚动条不是独立存在的，它是容器的一部分，所以用户不能创建滚动条。
个滚动条能够被鼠标点击后拖动。

|属性|描述|
|-|-|
|SetTrackRange	|设置滚动条的范围。默认值为0到1
|SetPageSize	|设置滚动条的页尺寸，默认值为1
|track|	滚动条轨道的纹理
|up_left	|滚动条左/上按钮的纹理
|down_right	|滚动条右/下按钮的纹理
|thumb	|滚动条滑块的纹理

editbox & imeeditbox
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4157/raw#image.png'
  ext: png
  filename: image.png
  size: '11195'
  unit: '%'
  percent: 60

```

>  文本编辑框

表示一个GUI中的文本框控件。
一个文本框接收键盘的输入，一个imeeditbox不仅仅接收键盘的输入，还能接收输入法的输入，例如中文拼音。
一个editbox或者imeeditbox当被选定就可接收来自键盘的输入，点击控件就可选定。editbox和meeditbox中的内容能够被选中，删除，复制，粘贴和插入。某种意义上说就和windows标准输入框一样。
当内容改变时会触发onchange事件，当RETURN按下会触发onstring。
创建方法：

    object= ParaUI.CreateUIObject("editbox","editboxname","_lt",50,20,600,400)
    object= ParaUI.CreateUIObject("imeeditbox","editboxname","_lt",50,20,600,400)

|属性|描述|
|-|-|
|text	|string类型，对象的文本
|background|	string类型，对象的背景
|readonly	|boolean类型，控制editbox和meeditbox是否只读
|background	|edibox的背景纹理
|text|	editbox的文本字体
|selected_text|	editbox中被选中的文本字体

text
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4158/raw#image.png'
  ext: png
  filename: image.png
  size: '6675'
  unit: '%'
  percent: 60

```

>  文本
	
表示一个GUI中的文本。
一个文本控件和按钮一样可以接受鼠标点击。
创建方法：

    object= ParaUI.CreateUIObject("text","textname","_lt",50,20,600,400)

|属性|描述|
|-|-|
|text	|string类型，对象的文本
|background|	string类型，对象的背景
|background	|对象的背景纹理
|text|	对象的文本字体，用来显示按钮中的文本

listbox

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4159/raw#image.png'
  ext: png
  filename: image.png
  size: '24187'
  unit: '%'
  percent: 60

```

>  列表框
	
表示一个GUI中的列表框。
一个列表框允许用户添加文本元素并且按照一定顺序展示它们。属性“text“总是返回当前选中的元素。如果没有任何元素被选中，将返回”“。设置属性”text“是不允许的。
一个列表框接收鼠标点击和一些键盘输入。键盘控制行为和windows标准列表框控件一样。当遇一个元素被鼠标或键盘选取，会出发onselect事件，当一个元素被双击，会触发ondoubleclick事件。
创建方法：

    object= ParaUI.CreateUIObject("listbox","listboxname","_lt",50,20,600,400)

|属性|描述|
|-|-|
|itemheight|	number类型，列表元素中的元素高度。
|scrollable	|boolean类型，列表框是否能被滚动，默认为true
|scrollbarwidth|	number类型，列表框滚动条的宽度，默认为25
|background	|string类型，对象的背景
|wordbreak	|boolean类型，决定每个文本元素在太长的情况下是否可以被分作多行，默认为false。当在false的情况下，超出部分将被截除掉
|AddTextItem	|将一个文本元素添加到列表框中
|RemoveItem|	移除给定索引的元素
|RemoveAll|	移除列表框中所有的元素
|background|	对象的背景纹理
|text|	对象的文本字体，用来显示按钮中的文本

slider
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4160/raw#image.png'
  ext: png
  filename: image.png
  size: '14215'
  unit: '%'
  percent: 60

```


>  滑块
	
表示一个GUI的滑块控件。
一个滑块可以接收鼠标和键盘的输入，击背景条或者拖动按钮将改变滑块控件的值。点击左下将值减少一，右上值增加一。使用向上翻页可将值增加范围的1/10,向下减少1/10。
无论值怎么改变，都会触发onchange事件。

|属性|描述|
|-|-|
|value|	number类型，滑块的当前值，默认为范围的一半
|button	|string类型，对象中的按钮
|background	|string类型，对象中的背景
|SetTrackRange|	设置滑块的范围，默认0到100
|background	|对象的背景纹理
|button|	对象中的按钮的纹理

## MCML
### 什么是MCML
MCML——类似HTML的标记语言， 用类似HTML/Java的模式快速开发游戏UI。
MicroCosmos Markup Language, 是ParaEngine定义并开发在ParaWorld中使用的标记语言。 MCML基于XML标准，通过嵌套的元素和属性，使用了基于Tag的结构，支持大部分CSS和HTML Tag，可以用来描述社区或游戏中的许多UI, 例如几乎所有windows常用控件, 任务, 道具, 等等。我们可以将它理解为Web中的HTML，打个比方，可以把它看作是三维社交网络中的HTML，用来描述二维和三维网络中的可渲染对象。其中以pe开头的标记是ParaEngine中所特有的Tag, 常常对应一个NPL类库中的UI控件，它的作用是将数据绑定到NPL控件。 MCML的渲染器是用NPL脚本编写的，具有较高的扩展性，它可以让开发者定义自己的Tag。

### MCML Tags
作为和HTML类似的标记语言，MCML面向的是三维社交网络，它支持的标签更加广泛，可以分为8类：
MCML支持的标签

|类别|标签|
|-|-|
|HTML tags|	_text_  h1  h2  h3  h4  li  p  div  hr  font  span  strong a(href)  form img(attr: src,height, width, title)等等支持大量HTML标记，更多信息见http://www.paraengine.com/twiki/bin/view/Main/HTMLTags
|Design tags|	pe:gridview pe:xmldatasource pe:mqldatasource pe:dialog pe:tabs pe:tab-item pe:treeview pe:treenode pe:image pe:flash pe:container pe:editor pe:editor input(button, listbox, text, radio, checkbox, file, etc) pe:slide (interval=3 order="sequence"|"random"), pe:filebrowser(rootfolder="script" filter="*.lua;*.txt") pe:fileupload pe:progressbar pe:canvas3d pe:numericupdown pe:sliderbar pe:colorpicker pe:ribbonbar
|Social tags	|pe:name pe:profile-photo pe:avatar pe:profile pe:userinfo pe:friends pe:app pe:profile-action pe:profile-box pe:app-home-button
|Map tags	|pe:land pe:map pe:map-mark pe:map-mark2d pe:map-tile
|Control tags|	pe:if-is-user pe:if pe:if-not
|Component tags	|pe:roomhost pe:market pe:comments pe:ribbonbar pe:command pe:asset pe:bag
|Worlds tags	|pe:world pe:world-ip pe:model
|Motion tags	|pe:animgroup pe:animlayer pe:animator

#### 后台代码解析
在MCML脚本体系中，存在两种脚本，行内脚本和外部脚本。行内脚本是存在于html文件中的脚本，行外脚本通常定义在lua文件中。
行内脚本
script/kids/3DMapSystemUI/Desktop/LoginPage.html

```
<script type="text/npl">
    <![CDATA[
    function OnInit()
       local self = document:GetPageCtrl();
       self:SetNodeValue("username", Map3DSystem.User.Name);
       self:SetNodeValue("password", Map3DSystem.User.Password);
    end
    OnInit()
    ]]>
</script>
```

行内代码范围(页面)。每次加载或刷新页面时都要编译。所调用的函数均在页面内。
外部脚本
为了将MCML与表达逻辑分离开来，可以将逻辑代码放入一个单独的lua文件中。这样的lua文件称为外部脚本。可使用以下代码在MCML文件中设置外部脚本:
```
<script type="text/npl" src="*********.lua"></script>
```
上述代码等同于NPL.load()，外部脚本中的代码仅仅会被编译一次。
PageCtrl.lua解析
	MCML文件和相应的外部脚本文件定义了一个页面模版。我们可以使用这个相同的模板创建许多实例，只要我们创建的页面源自PageCtrl，我们就能够使用PageCtrl:Create(name, _parent, alignment, left, top, width, height)来为我们的界面创建新的实例。
  
|概述|	一个从MCML文件初始化的交互式NPL控件|
|-|-|
|文件位置	|script/kids/3DMapSystemApp/mcml/PageCtrl.lua
|描述	|PageCtrl通过在MCML文件中创建NPL控件的方式，自动实现从静态或异步的MCML文件中构建交互式控件，这个MCML文件包含着所有UI元素的布局和默认数据绑定。我们可以在其中实现预定义或MCML页面定义事件处理器，同时我们能够轻松地接入在MCML中定义好的UI和数据绑定控件。我们将之称为MCML/NPL Code Behind 模式，用作分离UI和实现逻辑。

### MCML架构

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4161/raw#image.png'
  ext: png
  filename: image.png
  size: '60621'
  unit: '%'
  percent: 80

```


>  MCML架构

### MCML作用
MCML用来在地图浏览器中展示地理数据。例如ParaEngine 3D地图系统。MCML的作用可以总结为以下6条：
- 指定地图标记（图标和标签）以便在地图上确定位置
- 创建不同的相机位置为每个特性定义独特的视点
- 在MCML中嵌入NPL脚本来在地图上创建复杂的UI
- 从远程或本地网络位置中动态地获取和更新KML文件
- 在地图观察器上基于变化获取KML数据
- 在地图上显示与ParaX兼容的3D对象

## 系统窗口
系统窗口即2D GUI的主容器。最通用的创建系统窗口的方法是使用mcml标记语言，编程模式就像编写HTML/js网页。
要创建系统窗口，首先要创建一个html文件。要使用html文件创建并显示窗口：


```
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/PageCtrl.lua");
	local page = System.mcml.PageCtrl:new({url="source/HelloWorldMCML/mcml_window.html"});
	page:Create("testpage", nil, "_lt", 0, 0, 300, 400);
```


# MCML Markup Language For 2D GUI
MCML or Micro Cosmos Markup Language is a metalanguage written in NPL since 2008. Since then it has become the standard way of writing 2D user interface in NPL. MCML is inspired by the early version of ASP.net, however, it uses local architecture for local user interface. 

### Quick Sample

Here is an example of mcml page in a `.html` file, such as `source/HelloWorldMCML/mcml_window.html`. The file extension only makes it possible for you to preview the page in other html code editor. 

```html
<pe:mcml>
<script refresh="false" type="text/npl" src="mcml_window.lua"><![CDATA[
    function OnClickOK()
        local content = Page:GetValue("content") or "";
        _guihelper.MessageBox("你输入的是:"..content);
    end
]]></script>
<div style="color:#33ff33;background-color:#808080">
    <div style="margin:10px;">
        Hello World from HTML page!
    </div>
    <div style="margin:10px;">
        <input type="text" name="content" style="width:200px;height:25px;" />
        <input type="button" name="ok" value="确定" onclick="OnClickOK"/>
    </div>
</div>
</pe:mcml>
```

To render with mcml v1, use:
```lua
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/PageCtrl.lua");
local page =  Map3DSystem.mcml.PageCtrl:new({url="source/HelloWorldMCML/mcml_window.html"});
page:Create("pageName", nil, "_fi", 0, 0, 0, 0)
```

### MCML Preview and Debug Tools
`Mcml browser` window can be used to preview the mcml page layout and test functions without restarting your application. 
To launch the `mcml browser`, one can press `Ctrl+F3` in paracraft. If you want to launch it in your own custom application. Simply run the code
```
System.App.Commands.Call("File.MCMLBrowser", {url="", name="MyBrowser", title="My browser", DisplayNavBar = true});
```
If you do not have the default system application loaded, one can create the mcml browser window like below:
```
NPL.load("(gl)script/kids/3DMapSystemApp/WebBrowser/MCMLBrowserWnd.lua");
System.App.WebBrowser.MCMLBrowserWnd.ShowWnd()
```

![image](https://user-images.githubusercontent.com/94537/32358871-612c78ee-c084-11e7-9fa6-9d2b08bab7de.png)

When you change the mcml file content, simply press the `refresh` button to see the change taking effect immediately without restarting your application. This is useful when you need to test the page UI functions by interacting with the real application code. This is why we write all of our UI code in mcml so that we can easily test and debug while the application is running. 

> All paracraft UI is written in MCML and tested in mcml browser first.

### Mcml tags
There are a number of tags which you can use to create interactive content. Besides, one can also create your own custom tags with UI controls, see [System.Window](System.Window) for details. All mcml build-in tags are in the `pe:` xml namespace, which stands for ParaEngine or pe.

- [pe:div](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_div.lua)
- [pe:button](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_button.lua)
- [pe:container](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_container.lua)
- [pe:custom](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_custom.lua)
- [pe:editbox](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_editbox.lua)
- [pe:identicon](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_identicon.lua)
- [pe:if](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_if.lua)
- [pe:input](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_input.lua)
- [pe:repeat](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_repeat.lua)
- [pe:script](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_script.lua)
- [pe:span](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_span.lua)
- [pe:text](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_text.lua)
- For a complete list of supported mcml tags, [click here](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements)

Standard html tags are mapped as follows:
- The `div` tag is mapped to `pe:div` class.  
- plain text is mapped to `pe:text`. 
- `input type=button` is mapped to `pe:button`, etc. 

### Examples
There are many mcml examples where you browse in the paracraft package.

Following is just some quick examples:
```html
<pe:mcml>
<script type="text/npl" refresh="false">
<![CDATA[
globalVar = "test global var";
function OnButtonClick()
    _guihelper.MessageBox("refresh page now?", function()
        Page:SetValue("myBtn", "refreshed");
        Page:Refresh(0);
    end);
end

repeat_data = { {a=1}, {a=2} };
function GetDS()
    return repeat_data;
end
]]>
</script>
    <div align="right" style="background-color:#ff0000;margin:10px;padding:10px;min-width:400px;min-height:150px">
        <div align="right" style="padding:5px;background:url(Texture/Aries/Common/ThemeKid/btn_thick_hl_32bits.png:7 7 7 7)">
            <div style="float:left;background-color:#000000;color:#ffd800;font-size:20px;">
                hello world中文<font color="#ff0000">fontColor</font>
            </div>
            <div style="float:left;background-color:#0000ff;margin-left:10px;width:20px;height:20px;">
            </div>
        </div>
        <div valign="bottom">
            <div style="float:left;background-color:#00ff00;width:60px;height:20px;">
            </div>
            <div style="float:left;background-color:#0000ff;margin-left:10px;width:20px;height:20px;">
            </div>
        </div>
    </div>
    <div>
        hello world中文<font color="#ff0000">fontColor</font>
        <span color="#ff0000">fontColor</span>
    </div>
    <span color="#ff0000">
        <%=Eval('globalVar')%>
        <%=document.write('hello world')%>
    </span>
    <pe:container style="padding:5px;background-color:#ff0000">
        button:<input type="button" name="myBtn" value="RefreshPage" onclick="OnButtonClick" style=""/>
        editbox:<input type="text" name="myEditbox" value="" style="margin-left:2px;width:64px;height:25px"/><br/>
        pe_if: <pe:if condition='<%=globalVar=="test global var"%>'>true</pe:if>
    </pe:container>
    <pe:repeat value="item in repeat_data" style="float:left">
        <div style="float:left;"><%=item.a%></div>
    </pe:repeat>
    <pe:repeat value="item in GetDS()" style="float:left">
        <div style="float:left;"><%=item.a%></div>
    </pe:repeat>
    <pe:repeat DataSource='<%=GetDS()%>' style="float:left">
        <div style="float:left;"><%=a%></div>
    </pe:repeat>
</pe:mcml>
```

### MCML Layout
Please see [System.Window](System.Window) first for basic alignment types. There are over 12 different alignment types, which supports automatic resizing of controls according to parent window size. 

- mcml v1 have a `<pe:container>` control which supports all alignment types via `alignment` attribute.


#### Relative positioning
Relative position is a way to position controls without occupying any space. It can be specified with `style="position:relative;"`. If all controls in a container is relatively positioned, they can all be accurately positioned at desired location relative to their parent. 

However, relative position is NOT recommended, because a single change in child control size may result in changing all other child controls' position values and if parent control's size changes, the entire UI may be wrong. The recommended way of position is "float:left" or line based position. `<div>` defaults to line based position, in which it will automatically add `line break` at end. Specify "float:left" to make it float. Many other controls default to "float:left", such as `<input>`, `<span>`. Some UI designer in special product may still prefer relative position despite of this.


### MCML vs HTML
MCML only supports a very limited subset of HTML. The most useful layout method in mcml is `<div>` tag. 

### NPL Code Behind and Embedding
In MCML page, there are three ways to embed NPL code. 
- Use `<script src="helloworld.lua">`, this will load the npl file relative to the current page file. 
- Embed NPL code section inside `<script>` anywhere in the page file
- Embed code in xml attribute in quotations like this `attrname='<%= %>'`. Please note it depends on whether the tag implementation support it. For each attribute you can not mix code with text. Unlike in NPL web server page, all code in MCML are evaluated at runtime rather than preprocessed. This is very important. 

```html
<script type="text/npl" src="somefile.lua" refresh="false">
<![CDATA[
globalVar = "test global var";
function OnButtonClick()
    _guihelper.MessageBox("refresh page now?", function()
        Page:SetValue("myBtn", "refreshed");
        Page:Refresh(0);
    end);
end
repeat_data = { {a=1}, {a=2} };
function GetDS()
    return repeat_data;
end
]]>
</script>
<div style='<%=format("width:%dpx", 100) %>'></div>
```

#### Page Variable Scoping
Global variables or functions defined in inline script are local to the page and not visible outside the page.
So consider using a separate code behind file if one wants to expose values to external environment or simply your code is too long. 

There is a predefined variable called `Page`, which is accessible to the page's sandbox's environment. 

#### Two-Way Databinding
Many HTML developers have a `jquery` mindset, where they like to manipulate the DOM (Document Object Model or XML node) directly, which is **NOT** supported in mcml. Instead, one should have a `databinding mindset` like in `angularjs`. In MCML v1, `DOM != Controls`. DOM is only a static template for creating controls in a page. Controls can never modify static template unless you write explicit code, which is really rare. 

Most mcml tags only support one-way data binding from static DOM template to controls only at the time when controls are created (i.e. Page Refresh, see below). To read value back from controls, one must either listen to `onchange` event of individual control or manually call `Page:GetValue(name)` for a collection of controls in a callback function, such as when user pressed `OK` button. 

```lua
<pe:mcml>
<p>Two-way databinding Example in mcml:</p>
<script type="text/npl" refresh="false"><![CDATA[
-- nodes are generated according to this data source object, ds is global in page scope so that it is shared between page refresh
ds = {
    block1 = nil,
    block2 = nil,
};

function asyncFillBlock1()
    PullData();
    -- use timer to simulate async API, such as fetching from a remote server.
    commonlib.TimerManager.SetTimeout(function()  
        -- simulate some random data from remote server
        ds.block1 = {};
        for i=1, math.random(2,8) do
            ds.block1[i] = {key="firstdata"..i, value=false};
        end
        ds.block2 = nil;
        ApplyData();
    end, 1000)
end

function asyncFillBlock2()
    PullData();
    commonlib.TimerManager.SetTimeout(function()  
        ds.block2 = {};

        -- count is based on the number of checked item in data1(block1)
        local data1_count = 0;
        for i, data in pairs(ds.block1) do
            data1_count = data1_count + (data.value and 1 or 0);
        end
        
        -- generate block2 according to current checked item in data1(block1)
        for i=1, data1_count do
            ds.block2[i] = {key="seconddata"..i, value=false};
        end
        ApplyData();
    end, 1000)
end

-- apply data source to dom
function ApplyData()
    Page("#block1"):ClearAllChildren();
    Page("#block2"):ClearAllChildren();

    if(ds.block1) then
        local parentNode = Page("#block1");
        for i, data in pairs(ds.block1) do
            local node = Page("<span />", {attr={style="margin:5px"}, data.key });
            parentNode:AddChild(node);
            local node = Page("<input />", {attr={type="checkbox", name=data.key, checked = data.value and "true"} });
            parentNode:AddChild(node);
        end
        local node = Page("<input />", {attr={type="button", value="FillBlock2", onclick = "asyncFillBlock2"} });
        parentNode:AddChild(node);
    end

    if(ds.block2) then
        local parentNode = Page("#block2");
        for i, data in pairs(ds.block2) do
            local node = Page("<span />", {attr={style="margin:5px"}, data.key });
            parentNode:AddChild(node);
            local node = Page("<input />",  {attr={type="text", EmptyText="enter text", name=data.key, value=data.value, style="width:80px;"} });
            parentNode:AddChild(node);
        end
    end

    Page:Refresh(0.01);
end

-- pull data from DOM
function PullData()
    if(ds.block1) then
        for i, data in pairs(ds.block1) do
            data.value = Page:GetValue(data.key);
        end
    end
    if(ds.block2) then
        for i, data in pairs(ds.block2) do
            data.value = Page("#"..data.key):value(); -- just another way of Page:GetValue()
        end
    end
end

function OnClickSubmit()
    -- TODO: one can also use a timer and hook to every onchange event of controls to automatically invoke Apply and Pull Data. 
    -- Here we just need to manually call it. 
    PullData();
    _guihelper.MessageBox(ds);
end
]]></script>
<div>
    <input type="button" value="FillBlock1" onclick="asyncFillBlock1()"/><br />
    block1: <div name="block1"></div>
    block2: <div name="block2"></div>
</div>
<input type="button" value="Submit" onclick="OnClickSubmit()" /><br />
</pe:mcml>
```

In above example, When user clicks `FillBlock1` button, some random data is filled in `ds.block1`, each data is displayed as checkbox, and the user can check any number of them and click the `FillBlock2` button. This time we will fill `ds.block2` with same number of checked items in `ds.block1`, and each item is displayed as a text input box. When user clicks `Submit` button, the current `ds` is displayed in a message box with user filled data. 

We call `ApplyData` to rebuild all related DOM whenever `ds` is modified externally, and we call `PullData` in the first line of each callback function so that our `ds` data is always up to date with mcml controls. The above example is called manual two-way binding because we have to call `ApplyData` and `PullData` manually. One can also use a timer and hook to every onchange event of controls to automatically invoke `ApplyData` and `PullData`, so that we do not have to write them everywhere in our callback functions. 

> There is an old two-way data binding code called [BindingContext](https://github.com/NPLPackages/main/blob/master/script/ide/DataBinding.lua), which is only used in `<form>` tag in mcml, it may cause some strange behaviors when you are manipulating DOM. 

#### Page Refresh
For dynamic pages, it is very common to change some variable in NPL script and refresh the page to reflect the changes. 

`<script refresh='false'>` means that the code section will not be reevaluated when page is refreshed. 
Also note that global variables or functions are shared between multiple script sections or multiple page refreshes.

Please also note that code changes in inline script blocks are usually reparsed when window is rebuild. However, if one use code behind model, npl file is cached and you need to restart your application to take effect. It is good practise to write in inline script first, and when code is stable move them to a code behind page. This will also make your page load faster during frequent page refresh or rebuild. 

### Writing Dynamic Pages
MCML has its own way of writing dynamic pages. In short, mcml uses frequent full `page refresh` to build responsive UI layout. Please note that each mcml page refresh does NOT rebuild (reparse) the entire DOM tree again, it simply reuses the old DOM tree and re-execute any embedded code on them each time. If the code is marked as `refresh="false"` (see last section), its last calculated value will be used.

Generally, MCML v1 uses a single pass to render the entire web page. 

Unlike HTML/Javascript(especially jquery) where programmers are encouraged to manipulate the document tree directly, in mcml, you are NOT advised to change the DOM with your own code (although we do provide a jquery like interface to its DOM). Instead, we encourage you to data-bind your code and create different code paths using conditional component like `<pe:if>`, when everything is set you do a full page refresh with `Page:refresh()`. This is a little bit like `AngularJS`, but we do it with real-time executed inline code. The difference is that `AngularJS` will compile all tags and convert everything from angular DOM to HTML DOM, but mcml just does one pass rendering of the mcml tags and execute the code as it converts DOM to real NPL controls. 

Another thing is that unlike in AngularJS where data changes are watched and page is automatically refreshed, in mcml, one has to manually call `Page:refresh(delayTimeSeconds)` to refresh the whole page, such as when user pressed a button to change the layout. Please note, changing the DOM does not automatically refresh the page, one still need to call the refresh function.  Mcml code logics is much simpler to understand and learn, while angularJS, although powerful, but with too many hidden dark-magic that programmers will never figure out on their own.

Finally, mcml page is NOT preprocessed into a second DOM tree before rendering like what NPL web server page or PHP does. Every tag in mcml is a real mcml control or [PageElement](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/PageElement.lua) and the DOM tree is persistent across page refresh. MCML uses a single pass to render all of them. This also makes full page `Page:refresh()` much faster than other technologies.

#### MCML Controls
Remember mcml is meant to be replacement for tedious control creation in the whole application, not a stateless and isolated web page.  Each mcml page is an integral part of the application, they run in the same thread and have access to everything in that thread. They usually have direct interactions (or data-binding) with the 3D scene and other UI controls. To get the underlying control, one can use `Page:FindControl(name)`

#### MCML Page:Refresh(DelayTime)
`Page:Refresh(DelayTime)` refresh the entire page after DelayTime seconds. Please note that during the delay time period, 
if there is another call to this function with a longer delay time, the actual refresh page activation will be further delayed 
Note: This function is usually used with a design pattern when the MCML page contains asynchronous content such as pe:name, etc. whenever an asynchronous tag is created, it will first check if data for display is available at that moment. if yes, it will just display it as static content; if not, it will retrieve the data with a callback function. In the callback function, it calls this Refresh method of the associated page with a delay time. Hence, when the last delay time is reached, the page is rebuilt and the dynamic content will be accessible by then. 

- @param DelayTime: if nil, it will default to self.DefaultRefreshDelayTime (usually 1.5 second). 
- tip: If one set this to a negative value, it may causes an immediate page refresh. 


### Page Styling and Themes
MCML has some support of css in `style` or `class` parameter. 

Here is an example of defining styles with different class names, all mcml tags can have zero or more class names. Both mcss and css classes can be mixed together. 
```xml
<pe:mcml>
<style type="text/css" src="script/ide/System/test/test_css_style.css"></style>
<style type="text/mcss" src="script/ide/System/test/test_file_style.mcss">
{
    color_red = { color = "#ff0000" },
    color_blue = { color = "#0000ff", ["margin-left"] = 10 },
    bold = { ["font-weight"]="bold"    }
}
</style>
<span class="color_blue bold">css class</span>
</pe:mcml>
```

External css files are loaded and cached throughout the lifetime of the application process. Its content is also NPL table, such as `script/ide/System/test/test_file_style.mcss`:

```lua
-- Testing mcml css: script/ide/System/test/test_file_style.mcss
{
["default"] = { color="#ffffff" },
["mobile_button"] = {
	background = "Texture/Aries/Creator/Mobile/blocks_UI_32bits.png;1 1 34 34:12 12 12 12", 
},
color_red = { color = "#ff0000" },
color_blue = { color = "#0000ff", ["margin-left"] = 10, ["font-size"] = 16 },
bold = { ["font-weight"] = "bold"    },
["pe:button"] = {padding = 10, color="#00ff00"},
}
```
```css
/*Testing mcml css: script/ide/System/test/test_css_style.css*/
span
{
    color:#ff0000;
    margin:20px;
}
pe:button 
{
    padding:10px;
    color:#00ffff
}
```

In most cases, we can style the object directly in style attributes using 9 tiled image file.  See next section.

To change the style of unthemed tags or buildin classes, one must progammatically modify the following table:
- In mcml v1, there is a global table like [this one](https://github.com/NPLPackages/paracraft/tree/master/script/apps/Aries/Creator/Game/DefaultTheme.mc.lua)


### 9-Tile Image
MCML supports a feature called image tiling. It can use a specified section of an image and divide the subsection into 9 images and automatically stretch the 5 middle images as the target resizes (4 images at the corner are unstretched).  This is very useful to create good looking buttons with various sizes.

![image](https://cloud.githubusercontent.com/assets/94537/24950246/fa9e3888-1fa2-11e7-9f16-eb398fb53db3.png)

The syntax is like this: 
`<div style="background:url(someimage_32bits.png#0 0 64 21: 10 10 10 10);" >`
- `#left top width height` is optional, which specifies a sub region. if ignored it means the entire image. 
- `:left top to_right to_bottom` means distance to left, top, right and bottom of the above sub region. 
- `_32bits.png` means that we should use 32bits color, otherwise we will compress the color to save video memory
- Image size must of order of 2, like 2,4,8,16,64, 128, 256, etc. Because `directX/openGL` only supports order of 2 images. If your image file is not order of 2, they will be stretched and become blurred when rendered. 

Please note, in css file or `<style>` tag, `#` can also be `;` when specifying a sub region.

### Setting Key Focus
For mcml v1, one can set key focus by following code. It only works for text box.  
```lua
local ctl = Page:FindControl(name);
if(ctl) then
   ctl:Focus();
end
```
For input text box, one can also use. 
```
<input type="text" autofocus="true"  ... />
```

But there can only be one such control in a window. If there are multiple ones, the last one get focus. For example
```xml
<pe:mcml>
    <div>
        Text: <input type="text" name="myAutoFocusEditBox" />
    </div>
    ... many other div here...
    <!-- This should be the last in the page -->
    <script type="text/npl" refresh="true">
        local ctl = Page("#myAutoFocusEditBox"):GetControl()
        ctl:Focus();
        ctl:SetCaretPosition(-1);
    </script>
</pe:mcml>
```


### FAQ 
> Why large font size appears to be blurred in mcml?

MCML uses 3D API to do all the graphical drawing. For each font size, an image must be loaded into video memory. Thus by default, mcml may scale an existing font to prevent creating unnecessary image. To prevent this behavior, one can use `style="base-font-size:30;font-size:30"` this will always create a base font image for your current font setting. In general, an application should limit the number of font settings used in your graphical application. 

















