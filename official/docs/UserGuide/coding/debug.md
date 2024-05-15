# 调试代码方块

我们支持下列IDE对代码方块的代码进行编辑和调试。

- paracraft内置编辑器: 适合初学者，支持文本和图形化编程。
- NPL code wiki (Web)：适合高级用户、跨平台调试或远程调试。
- visual studio: 适合高级用户本地调试
- visual studio code: 适合高级用户本地调试

更多内容： [https://github.com/LiXizhi/NPLRuntime/wiki/DebugAndLog](https://github.com/LiXizhi/NPLRuntime/wiki/DebugAndLog)

## paracraft内置编辑器

初学者可以在代码方块的设置中， `开启步进运行模式`，此时无论文本还是图块，运行速度会降低，并高亮正在运行的代码。高级用户，可以直接在代码方块中， 右键某行代码，设置断点，激活NPL Code WIKI 调试器。

### 基于日志的调试

日志是最常用的脚本调试方式之一，高级和初级开发者都会经常使用日志调试。 可以用下面3种语句输出日志。在聊天窗口或日志窗口看结果。也可以直接查看安装目录下的log.txt或使用F11的NPL Code wiki看结果。

```javascript
echo({any_data})
print("any text")
log("any text")
```

如果遇到特殊的情况，我们可以在日志中打印call stack

```javascript
commonlib.echo(commonlib.debugstack(2, 5, 1))
```

### 内置开发工具 Dev Tools

- F12可以打开paracraft内置的dev tools. 这里可以临时运行一些代码。
- Ctrl+F3可以打开内置MCML浏览器，调试带UI的代码。 

## NPL code wiki（F11）

NPL Code Wiki是Paracraft自带的一个基于网页的调试工具。默认地址为`http://127.0.0.1:8099`, 如果开多个客户端，则端口号依次加1. 我们可以通过菜单或F11快捷键打开NPL Code Wiki。

由于NPL code wiki是一个本地网站服务器， 所以我们可以用它调试运行在远程或其他设备（例如手机）上的代码。
NPL Code Wiki同时还支持基于网页的代码编辑、对象查看、日志分析、设置断点调试等功能。

> NPL Code Wiki可以用来调试已经发布的只读世界，世界中的代码在_codeblocks_虚拟文件夹中。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35490/raw#1709519306590image.png
  ext: png
  filename: 1709519306590image.png
  size: 113591
  isNew: true
          
```
更多内容：https://github.com/LiXizhi/NPLRuntime/wiki/NPLCodeWiki

## Visual studio 插件： NPL Language Service

Visual Studio是paracraft的内部开发人员使用的IDE. 到visual studio官网扩展中心搜索NPL，安装NPL Language service. 就可以在visual studio 中调试代码了，支持自定义文档类型，设置断点等。

## Visual studio Code 插件： NPL Remote Debugger

VsCode是目前最流行的paracraft脚本代码高级开发工具。到扩展中心搜索NPL，安装NPL Remote Debugger. 同时我们也推荐安装lua Language Server 插件。

如果我们的世界中代码很多，可以用vs code进行编程。 在Paracraft文件菜单中选择 `文件::用VsCode打开代码...`
此时会自动打开本机的vscode, 并创建映射所有代码方块到文件。磁盘文件和paracraft世界的代码方块会自动同步。

> 每次打开paracraft（同步了世界）后， 建议都从这里打开vs code 世界目录，以保证文件的一致性。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35491/raw#1709520022914image.png
  ext: png
  filename: 1709520022914image.png
  size: 12845
  isNew: true
          
```

如果你只希望临时用vscode编辑和调试某个代码方块， 可以在代码方块中右键并选择`用VsCode打开代码...`
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35494/raw#1709520483718image.png
  ext: png
  filename: 1709520483718image.png
  size: 30484
  isNew: true
          
```
我们会注意到在当前世界目录下会临时生成一个`.codeblock/`文件夹。 这个文件夹在世界同步时并不会上传。它只用于和paracraft双向同步文件。文件名为代码方块的名字+3D坐标。如果代码方块改名或位置变化了， 需要在paracraft中重新打开并生成新的对应的文件。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35493/raw#1709520408084image.png
  ext: png
  filename: 1709520408084image.png
  size: 123697
  isNew: true
          
```
如图所示，右键点击某行代码，可以进入paracraft菜单。 

> 你可以通过Ctrl+R编译并运行当前的代码方块（含所有相连的代码方块）。

你也可以临时新建任意文件，这些文件会被当成普通代码运行。 如果你编辑的是.codeblock/目录之外的代码， 这些代码也会被当成普通NPL代码运行。