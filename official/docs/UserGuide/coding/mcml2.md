# GUI图形界面

Paracraft中内置了一种与HTML非常类似的标记语言，叫做MCML。 MCML除了支持所有常用的HTML语法， 还支持内嵌NPL代码，数据绑定等高级功能。

- 代码方块中：可以通过window命令，显示一个MCML窗口
- 告示牌中：可以直接用MCML/HTML代码

:point_right: 教学视频：[HTML与用户UI](https://keepwork.com/official/tips/s1/1_19)
:point_right: HTML基础教学: [https://www.w3school.com.cn/html/index.asp](https://www.w3school.com.cn/html/index.asp)

> 你知道么？ Paracraft中所有的用户界面都是用MCML制作的。

### 视频教程：

#### UI事件

:point_right: 教学视频：[响应HTML中的按钮事件(上）](https://keepwork.com/official/tips/s1/1_38)

:point_right: 教学视频：[响应HTML中的按钮事件(下）](https://keepwork.com/official/tips/s1/1_39)

#### 数据绑定

:point_right: 教学视频：[HTML中的数据绑定 （上）](https://keepwork.com/official/tips/s1/1_40)
:point_right: 教学视频：[HTML中的数据绑定 （下）](https://keepwork.com/official/tips/s1/1_41)

---

## 什么是MCML标记语言？

MCML 或 Micro Cosmos 标记语言是自 2008 年以来用 NPL 编写的元语言。从那时起，它已成为在 NPL/ParaEngine 中编写2D用户界面的标准方式。 MCML的灵感来自早期版本的ASP.net，但是，它使用本地架构来实现本地用户界面。

> MCML有多种用法和版本，详情请看 (高级开发者必看 :point_right:): [https://github.com/LiXizhi/NPLRuntime/wiki/mcml](https://github.com/LiXizhi/NPLRuntime/wiki/mcml)

本文档只讲解如何在Paracraft的代码方块中使用MCML标记语言创建2D和3D的图形界面。

### Mcml 标签

您可以使用许多标签来创建交互式内容。 此外，您还可以使用 UI 控件创建自己的自定义标签，所有 mcml 内置标签都在 `pe:` xml 命名空间中，代表 ParaEngine 或 pe。

[pe:div](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_div.lua)
[pe:button](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_button.lua)
[pe:container](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_container.lua)
[pe:custom](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_custom.lua)
[pe:editbox](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_editbox.lua)
[pe:identicon](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_identicon.lua)
[pe:if](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_if.lua)
[pe:input](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_input.lua)
[pe:repeat](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_repeat.lua)
[pe:script](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_script.lua)
[pe:span](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_span.lua)
[pe:text](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements/pe_text.lua)

有关支持的 mcml 标签的完整列表，[单击此处](https://github.com/NPLPackages/main/tree/master/script/ide/System/Windows/mcml/Elements)

标准的 html 标签映射如下：

- `div` 标签映射到 `pe:div` 类。
- 纯文本映射到 `pe:text`。
- `input type=button` 映射到 `pe:button` 等。

### MCML布局

有超过 12 种不同的对齐类型，支持根据父窗口大小自动调整控件的大小。

- mcml 中有一个 `<pe:container>` 控件，它通过 `alignment` 属性支持所有对齐类型。
- mcml 的 `<div>` 通过 `align` 和 `valign` 属性支持一组有限的对齐类型，您可以在其中将对象左对齐或右对齐。

#### 相对定位

相对位置是一种在不占用任何空间的情况下定位控件的方法。 它可以用 `style="position:relative;"` 指定。 如果容器中的所有控件都是相对定位的，则它们都可以相对于其父级准确定位在所需位置。

但是，不推荐使用相对位置，因为子控件大小的一次更改可能会导致所有其他子控件的位置值发生更改，如果父控件的大小发生更改，则整个 UI 可能会出错。 推荐的位置方式是“float:left”或基于行的位置。 `<div>` 默认为基于行的位置，它会在末尾自动添加 `line break`。 指定“float:left”使其浮动。 许多其他控件默认为“float:left”，例如`<input>`、`<span>`。 尽管如此，一些特殊产品的UI设计师可能仍然更喜欢相对位置。

### MCML 与 HTML

MCML 只支持非常有限的 HTML 子集。 mcml 中最有用的布局方法是 `<div>` 标签。

### NPL代码隐藏和嵌入

在MCML页面中，可以通过2种方式嵌入NPL代码。

- 在页面文件的任意位置将 NPL 代码部分嵌入到 `<script>` 中
- 将代码嵌入引号中的 xml 属性中，例如“attrname='<%= %>'”。 请注意，这取决于代码实现是否支持它。 对于每个属性，您不能将代码与文本混合。 与 NPL 网络服务器页面不同，MCML 中的所有代码都在运行时评估而不是预处理。 这个非常重要。

#### 页面变量作用域

内联脚本中定义的全局变量或函数是页面本地的，在页面外是不可见的。
因此，如果想要将值暴露给外部环境或者您的代码太长，请考虑使用单独的代码隐藏文件。

#### MCML 页面：刷新（延迟时间）

`Page:Refresh(DelayTime)` 在 DelayTime 秒后刷新整个页面。 请注意，在延迟时间内，
如果再次调用此函数且延迟时间更长，则实际刷新页面激活将进一步延迟
注意：当MCML页面包含pe:name等异步内容时，此功能通常与设计模式一起使用。每当创建异步标签时，它都会首先检查当时是否有数据可供显示。 如果是，它只会将其显示为静态内容； 如果没有，它将使用回调函数检索数据。 在回调函数中，延时调用关联页面的这个Refresh方法。 因此，当达到最后延迟时间时，将重新构建页面，届时将可以访问动态内容。

- @param DelayTime：如果为零，它将默认为 self.DefaultRefreshDelayTime（通常为 1.5 秒）。
- 提示：如果将此设置为负值，可能会立即刷新页面。

### 页面样式和主题

MCML 在 `style` 或 `class` 参数中有一些对 css 的支持。
我们可以在其中以标准 NPL 表或标准 css 文件的形式定义内联或基于文件的 css。 如果您更喜欢 NPL 表语法，请指定 `text/mcss`，而不是 `text/css`。 它只是一个带有键值对的表对象。

下面是一个用不同类名定义样式的例子，所有的 mcml 标签都可以有零个或多个类名。 mcss 和 css 类都可以混合在一起。

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

在应用程序进程的整个生命周期中加载和缓存外部 css 文件。 其内容也是NPL表，如`script/ide/System/test/test_file_style.mcss`：

```javascript
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

### 图片的路径

我们一般用div显示图片，如下。

```javascript
window([[
<div style="background:url(preview.jpg);width:300px;height:100px" >
</div>    
]],"_lt", 10, 10, 300, 100)
```

大多数图片的搜索路径如下：

- 如果是相对路径，则先寻找当前世界目录， 然后再寻找3D引擎的安装目录。
- 建议不要使用绝对路径
- 目前只有`<img src="https://your_image_url.jpg" style="width:300px;height:100px;"/>`标签，支持http贴图。

### 9-Tile 图像

MCML 支持称为图像平铺的功能。 它可以使用图像的指定部分并将该部分划分为 9 个图像，并随着目标调整大小自动拉伸中间的 5 个图像（角部的 4 个图像未拉伸）。 这对于创建各种尺寸的美观按钮非常有用。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26389/raw#1682558864429image.png
  ext: png
  filename: 1682558864429image.png
  size: 47800
          
```

语法是这样的：
`<div style="background:url(someimage_32bits.png#0 0 64 21: 10 10 10 10);" >`
- `#left top width height` 可选，指定子区域。 如果忽略它意味着整个图像。
- `:left top to_right to_bottom` 表示到上述子区域的左侧、顶部、右侧和底部的距离。
- `_32bits.png` 表示我们应该使用 32 位颜色，否则我们将压缩颜色以节省显存
- 图像大小必须为 2 的顺序，如 2、4、8、16、64、128、256 等。因为 `directX/openGL` 仅支持 2 图像的顺序。 如果您的图像文件不是 2 的顺序，它们将被拉伸并在渲染时变得模糊。

请注意，在 css 文件或 `<style>` 标签中，指定子区域时，`#` 也可以是 `;`。

### 常问问题
> 为什么大字体在 mcml 中显得模糊？

MCML 使用 3D API 进行所有图形绘制。 对于每种字体大小，必须将图像加载到显存中。 因此默认情况下，mcml 可以缩放现有字体以防止创建不必要的图像。 为了防止这种行为，可以使用 `style="base-font-size:30;font-size:30"` 这将始终为您当前的字体设置创建一个基本字体图像。 通常，应用程序应该限制图形应用程序中使用的字体设置的数量。


### 参考
##### MCML V1 文档
- [mcml v1源代码](https://github.com/NPLPackages/main/tree/master/script/kids/3DMapSystemApp/mcml)，例如：
    - [pe_html](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_html.lua)
    - [pe_editor](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_editor.lua)
    - [pe_html_input](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_html_input.lua)
    - [pe_gridview](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_gridview.lua): [更多示例](pe_gridview_doc)
    - [pe_treeview](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_treeview.lua)
    - [pe_design](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_design.lua)
    - [pe_component](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_component.lua)
    - [pe_script](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/pe_script.lua)
- [mcml v1 的测试用例（示例）](https://github.com/NPLPackages/main/tree/master/script/kids/3DMapSystemApp/mcml/test)
    - [test_pe_gridview](https://github.com/NPLPackages/main/blob/master/script/kids/3DMapSystemApp/mcml/test/test_pe_gridview.html)

> 此外，许多现有的 paracraft GUI 实际上是使用 mcml v1 创建的。 搜索任何 HTML 页面的源代码以获取示例。

## 常用例子

### 渲染电影方块到UI

- 首先保存1个电影方块到template文件，例如movie1.blocks.xml。注意导出时演员需要用相对位置。
- 然后在代码方块中输入如下代码：

```lua
hide()
window([[
this is a demo 3d canvas from a movie block file
<pe:canvas3d name="myCustomScene" isLooping="true" 
    moviefile="blocktemplates/movie1.blocks.xml" 
    RenderTargetSize = "256"
    style="width:128px;height:128px" >
</pe:canvas3d>
]],"_lt", 0, 0, 200, 200)

```
内部会创建一个大小为RenderTargetSize的贴图，并渲染电影方块的内容到贴图中， 贴图可以显示在屏幕任意位置。
我们使用了`pe:canvas3d`标签将电影方块中的3D动画渲染到2D UI中。 

### pe:canvas3d 参数列表

| 属性 | 描述 |
|---|---|
| value | this can be a table string like inner text in the example. It support embedded code. |
| autoRotateSpeed | such as 0.12 |
| miniscenegraphname | the render target name. if not set, a default render target is used. this default render target are the same for pe:canvas3d objects |
| ExternalSceneName | if not nil, it will render into miniscenegraphname; if not nil, object will be rendered into an external mini scene graph with this name. | 
| IgnoreExternalCamera | if not provided, it means "false". if true and ExternalSceneName is provided, we will set the external mini scene's camera according to this node's settings.  | 
| ExternalOffsetX | in case ExternalSceneName is provided, this is the offset used for displaying the object.  | 
| ExternalOffsetY | in case ExternalSceneName is provided, this is the offset used for displaying the object.  | 
| ExternalOffsetZ | in case ExternalSceneName is provided, this is the offset used for displaying the object.  | 
| DefaultCameraObjectDist | number |
| DefaultLiftupAngle | |
| DefaultRotY | |
| FieldOfView | defaults to 3.14/6 (60 degrees)|
| MaskTexture | alpha mask texture |
| RenderTargetSize | such as 128, 256 |
| objectbinding | "selection",  it binds to System.obj.GetObjectParams(objectbinding); |
| cameraName  |   model config camera name  --clayman
| value | table or table string of inner text |
| moviefile | block template file containing a movie block |
| fromTime | movie file from time, default to 0 |
| toTime | movie file to time, default to -1, which is default movie length |
| isLooping | if movie file should be played looped |
| originX | movie file relative origin result to 0, 128, 0 |
| originY | |
| originZ | |


## 告示牌显示代码方块中的变量
告示牌中，可以这样写
```html
<div style="margin-left:-45px;font-size:20px;color:red">
   动态<br/>
   globalVar1<br/>
   <pe:label value="<%=globalVar1%>" getter="value"/>
</div>
```

代码方块中可以这样定义`globalVar1`
```lua
for i=1,100000  do
    _G.globalVar1 = tostring(i)
    wait(0.5)
end
```

:point_right: 教学视频： [彩色告示牌: 创建MCML](https://keepwork.com/official/tips/s1/1_18)


## 3D 场景中的UI

我们可以在代码方块中，使用`window`命令在3D 角色的头顶显示任意的图形界面。我们可以通过控制角色位置和角度来控制UI在3D场景中的位置。
当然大多数时候我们需要将角色的模型设置为空： `setActorValue("assetfile", "")`。 这样我们只显示UI，不显示3D模型。 
如果你使用show,hide命令隐藏角色， 那么3D UI也会被隐藏起来。 如下图。 

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26388/raw#1682557173671image.png
  ext: png
  filename: 1682557173671image.png
  size: '115007'
  unit: px
  alignment: left
  width: 299

```
```javascript
setActorValue("assetfile", "") -- use empty model for 3d model file

window([[
<div style="margin-left:-150px;margin-top:-100px" >
    <img src="https://api.keepwork.com/ts-storage/siteFiles/20942/raw#1628675678228image.png" style="width:300px;height:100px;"/>
</div>    
]],"headon3D", 0, 0, 300, 100)
```