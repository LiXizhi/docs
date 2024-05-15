 
## 安装Paracraft和编辑模式


**1 理论**
今天，我们将观看一小段动画视频，叫做 `What Do You Do With An Idea? 有了想法你怎么做？`
这个视频由Paracraft制作。Paracraft允许你能利用方块创建高级的3D动画和游戏。如果你已经玩过minecraft或者乐高，你将会喜欢它，但是Paracraft是一个更强大的3D动画和编程工具，并且是免费和开源的。你将要看到的动画是由像你这样的人仅仅使用Paracraft制作的。我们将学习阅读它的源代码来完成这一课。


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3458/raw#有了想法你怎么做.mp4
  ext: mp4
  filename: 有了想法你怎么做.mp4
  size: 75331242
          
```


**2 游戏**
学习如何从官方网站安装软件和工具是一项关键技能。许多人没有成功的学会编程是因为不知道怎样用家里的电脑下载和安装最新的软件。

首先你需要到官方网站安装Paracraft。

https://paracraft.cn/download

在浏览器中打开上面链接，然后点击下载，你需要根据你的操作系统安装相应的版本。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2434/raw#image.png'
  ext: png
  filename: image.png
  size: '66425'
  unit: px
  alignment: left
  width: 500

```

编程需要打字，我们强力建议你在最新的PC操作系统上安装`Windows版`。点击图中的下载按钮，下载完成后，你需要运行下载的`paracraft_full.exe`文件。

根据指引完成软件的安装，如果你的电脑出现安全警告或提示，请允许程序运行。

安装完成后，在你的桌面会生成一个图标 ![]( https://api.keepwork.com/storage/v0/siteFiles/2435/raw#image.png)， 点击它并完成软件的更新，就可以启动Paracraft了。 

> 每次启动时，我们强烈建议您更新到最新的版本。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2436/raw#image.png'
  ext: png
  filename: image.png
  size: '539044'
  unit: px
  alignment: left
  width: 600

```

上面是软件的启动界面， Paracraft软件的版本号在窗口左上方和左下方都有显示。 

- 学习用`W A S D`键来移动。
![图 1.2](https://api.keepwork.com/storage/v0/siteFiles/2442/raw#image.png)
- 按住`Ctrl`键并滚动鼠标滚轮来放大和缩小视角。
![图 1.3](https://api.keepwork.com/storage/v0/siteFiles/2443/raw#image.png)
- 学习按住`鼠标右键`并拖动来改变视角。
![图 1.4](https://api.keepwork.com/storage/v0/siteFiles/2444/raw#image.png)
 
当你打开一个用户创建的世界时，比如`有了想法你怎么做？`,你可以在游戏和编辑模式之间切换。在游戏模式中，你只能局限于创造者设定的游戏规则。在编辑模式下，你可以修改这个世界，并读取特殊方块中的源代码。

- 按`Ctrl+G`键切换到编辑模式，或者按下`Esc`键，在左上角点击播放模式切换模式。
![图 1.5](https://api.keepwork.com/storage/v0/siteFiles/2445/raw#image.png)

- 另一种切换模式的方式是通过命令。请记住：在大多数工具中，不仅仅是Paracraft，`你能用鼠标和键盘做的所有操作都可以通过命令来完成，所有命令能做的事情也可以通过代码来完成`。
- 命令就像是一种更加人性化的代码，具有输入和输出。许多专业程序员只使用命令与计算机交互，这样他们就可以几乎手不离开键盘的操控计算机。
- 因此，现在让我们像一个专业的程序员一样工作，只使用键盘来切换游戏模式。
  - 按下 `Enter` 或者 `/` 键 来打开在屏幕左下角的命令行窗口。
  - 然后输入 `/mode`。记住不要使用鼠标。现在再次按下 `Enter`来确认命令。
  - 尝试组合输入 `/mode`，`Enter`几次。恭喜你，你已经学会了第一个指令。
  - 按下 `Esc` 键(在键盘的左上角)来取消一个命令。
- 命令行可以用来做简单的编程，我们将会逐步学习。

> 用命令打字是非常重要的，试着提高打字的速度。
 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2446/raw#image.png'
  ext: png
  filename: image.png
  size: '85085'
  unit: px
  alignment: left
  width: 500

```

<div style="float:right;margin-left:10px;width:400px">
  
![图 1.6](https://api.keepwork.com/storage/v0/siteFiles/2447/raw#image.png)
  
</div>

在Paracraft使用中，右键单击一个方块意味着编辑或打开它。

- 在编辑模式下，`右键点击`电影方块读取它的源代码。在这节课，你不需要理解它们。只要四处走走，尽可能多地探索电影方块内的代码。
- 你可以通过单击上图所示的按钮来在编辑模式下播放动画。
- 如果你不小心进入播放模式，按下`Ctrl+P`键退出电影。


> 如果你离起点太远而走丢了，键入`/home` 命令并按回车键将人物传送到出生点。

**按F1键可以查看帮助**
帮助窗口中，有大量的Paracraft建造，动画与编程的小例子。 你可以随时将他们导入当前的世界。

<div style="clear:both"/>
<div style="margin-left:10px;">
  
![图 1.7](https://api.keepwork.com/storage/v0/siteFiles/3436/raw#image.png)

</div>