 

## 创建方块

**1.  理论**
今天，我们来观看一部名为`A Day For The Hungry 吃货的一天`的动画短片。学习创建方块等基本操作是创作一切作品的基础。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3448/raw#吃货的一天.mp4
  ext: mp4
  filename: 吃货的一天.mp4
  size: 136704179
          
```


**2. 实践**
- 删除方块：`点击鼠标左键`
- 创建方块：`点击鼠标右键`
- 按下 `F3` 键，弹出屏幕左上角的信息框
- 学习 `/setblock` 命令
- 创建一个新的世界
- 保存世界


```@Project
styleID: 1
project:
  projectId: '1149'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

**步骤1：请在Paracraft里面练习以下操作：**

- 按斜杠键 `/` 打开命令行窗口，输入 `mode` 并按下 `Enter` 键切换到编辑模式。 
- `点击鼠标左键` 来删除正常的方块。 
- 按下 `空格` 键多次，跳到空中。 
- 按下 `F` 键，切换到飞行模式。在飞行模式下，按 `空格` 键上升按 `X` 键下降。
  - 再次按下 `F` 键退出飞行模式。
- 输入 `/home` 并按下 `Enter` 键回到出生点。
- 电影方块中包含了其他的东西，你需要按住鼠标左键几秒钟，然后释放就可以删除电影方块了。


**步骤2：现在我们将要学习很酷的事情：创建方块！**

- 按下 `E` 键或者点击下方的 `E` 按钮来打开工具栏。有两个标签 `建造` 和 `环境` 如下图所示：
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2616/raw#1.jpg'
  ext: jpg
  filename: 1.jpg
  size: '131213'
  percent: '70'
  alignment: left
  unit: '%'

```
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2615/raw#2.png'
  ext: png
  filename: 2.png
  size: '21522'
  percent: 25
  alignment: left

```



- 再次按下 `E` 键来关闭它。如果你没有处于编辑模式下，按 `E` 键只会显示玩家的背包。所以请确保你处于编辑模式。
- 在工具栏中 `鼠标左键点击` 一个物品来选择它。
- `点击鼠标右键`来放置你当前选择的物品，你可以把它放到任何你想放到的地方。

请记住，在Paracraft中，你用鼠标或键盘做的每一个操作都是一个命令。比如，创建和删除块就相当于执行 `/setblock` 命令。你可以通过手动鼠标单击方块来快速执行它，或者你可以在命令行窗口中缓慢地输入执行它。

**步骤3：现在，让我们学习如何用 `/setblock` 命令来创建方块。**

我们必须在文本中指定位置坐标，并将其作为输入传递给 `/setblock` 命令，而不是手动单击方块。为了找到方块的位置坐标，我们需按下 `F3` 键，弹出信息框，将鼠标悬停在方块上。请注意，你的鼠标可以放在它的 `六个面` 之中的一个上。如下图的雪块。
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2617/raw#3.jpg'
  ext: jpg
  filename: 3.jpg
  size: '70795'
  percent: 70
  alignment: left

```


请自己记住这个方块的位置坐标，或者按下 `Ctrl+T` 来自动存储位置坐标到剪贴板。

`/setblock [x] [y] [z] [blockId]` 命令中，你在 `F3` 信息框中看到的位置坐标 `19199 5 19199` 即为x y z，雪块后面的数字 `5` 即为blockID。

此时 `鼠标左键单击` 雪块来删除它，按下 `Enter` 键，在命令行窗口输入 `/setblock 19199 5 19199 5`，再次按下 `Enter` 键执行命令，即在原位置重新生成雪块。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2618/raw#4.jpg'
  ext: jpg
  filename: 4.jpg
  size: '112514'
  alignment: left
  percent: 70

```

在上面的例子中，我们输入 `/setblock 19198 5 19200 62` 并按下 `Enter` 键来执行它，会在雪块旁边生成一个草块。
每个方块都有一个id，你可以通过将鼠标放到 `E` 键工具栏中的方块图标上，或放到底部的quickbar中的图标上，来查看id。草块的id是 `62`。空气或空块的id为 `0`，因此执行 `/setblock 19198 5 19200 0` 将在 `19198 5 19200` 的位置删除该方块。

使用命令行，并没有像鼠标右键创建方块那样方便，但是，文本命令的威力在于，你可以将它们保存到某个地方，比如内部命令或电影方块，并运行无数次。我们将在以后的课程中学习有关命令的细节。

最后我们来学习怎样自己创建一个新的世界。
- 当你启动Paracraft时，点击界面任意位置，然后点击 `创建世界`。你现在不需要注册你的帐户。
- 输入世界的名称，然后选择平坦或者随机地形，然后点击 `创建世界`。
- 你可以在你的世界里创造一些东西。按下 `Ctrl+S` 键来定期保存。
- 当你已经进入3D世界中，按下 `Esc` 键来显示系统菜单，在那里你可以创建，加载，保存，分享一个3D世界。
- 你也可以通过点击蓝色的 `...` 按钮来打开包含所有你的世界数据的文件夹。按钮如下图。
- 定期备份你的世界数据，我们也会自动为你备份。点击 `历史` 按钮来查看你的备份文件。
 

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2619/raw#5.png'
  ext: png
  filename: 5.png
  size: '79799'
  percent: '70'
  alignment: left

```

- 你还可以将其他人的世界数据复制或解压缩到 `/worlds/DesignHouse` 文件夹中，并通过 `加载世界` 来加载它。