## 《飞翔的小鸟2.0》第二节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21823/raw#飞翔的小鸟2.0_L2.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21822/raw#飞翔的小鸟2.0_L2.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>


### 步骤一

上节课，我们已经实现了编程控制小鸟飞行
这节课，我们来编写检测碰撞的程序
小鸟在飞行的过程中碰到任何方块，都会提示游戏失败
场景中放置了一组代码方块和电影方块
这是我们上节课学习的控制小鸟飞行的系统
在旁边，我们新建一个代码方块来编写检测碰撞的代码
打开代码方块，切换到图块编辑模式
在控制项下拖入【永远重复】和【如果那么】指令
【如果那么】指令是条件判断语句
如果这里的条件成立，则执行这里面包含的所有程序
如果这里的条件不成立，则会按照程序执行顺序继续执行下面的程序
接着，在感知项下拖入【是否碰到方块】指令
【是否碰到方块】指令可以感知场景中所有方块
如果想要感知某个具体的方块或者角色
那么只需要将后面的参数修改为对应方块的id或者角色名称即可
这里我们希望小鸟碰到场景中任何的方块都会提示失败，所以我们不做修改
接着在外观项下拖入【提示文字】指令
修改内容为：你输了，再来一局吧
如果玩家已经失败了，我们需要让游戏重新启动
所以我们在控制项下拖入【重新开始】指令
【重新开始】指令会让互相连接的所有代码方块的程序全部重新运行
点击运行，我们来看看效果
按下A键让小鸟往左飞
按下D键让小鸟往右飞
可以看到，当小鸟碰到任何一种方块都会提示失败，并且游戏重新开始

### 步骤二

在上一小节中，我们实现了小鸟碰到方块游戏失败的效果
这一小节，我们实现小鸟碰到红色的蛋就会变大的效果
首先，点击E键，打开工具栏，在工具子标签下找到活动模型
在物品分类下选择红色的蛋，把蛋放置在合适位置上
鼠标右键选中蛋，点击属性
在自定义标签这里，给蛋取个标签名为：egg
名字取好后，点击确定
接着我们在场景中再复制一个蛋出来
按住Ctrl键，鼠标指向蛋后拖动鼠标即可快速复制一个蛋出来
鼠标右键选中蛋，打开属性面板
可以看到这个复制出来的蛋，自定义标签也是：egg
因此场景中这两个蛋都同属于一个标签组类别：egg
在Paracraft中，同属于一个标签组的活动模型
可以以标签组名字作为检测对象被感知检测到
具体如何使用我们接着往下看
打开代码方块，复制这段代码
这里输入蛋所属的标签组的名字：@egg
这里务必注意格式，标签组名字前面一定要加：@
然后，修改提示文字内容为：小鸟变大了
删掉这条【重新开始】指令
在外观项下拖入【放缩百分之】指令
【放缩百分之】指令可以让当前角色放大或者缩小
我们把参数改为5
点击运行，可以看到当小鸟碰到第一个蛋时候，变大了
当碰到第二个蛋的时候，也变大了
你可以在场景的不同地方放置更多的蛋
只要同属于一个标签组的蛋
都可以被我们写的程序感知检测到
快去试试吧

### 步骤三

这一小节，我们实现小鸟碰到光圈会获得加速的效果
点击E键，打开工具栏
在工具子标签下找到活动模型
在特效分类下选择火法阵，把火法阵放置到合适位置上
鼠标右键选中火法阵，点击属性
在自定义标签这里，给火法阵取个标签名为：fire
名字取好后，点击确定
接着复制这段代码
这里修改为@fire
提示文字内容改为：小鸟获得临时加速
删掉这条指令
在运动项下拖入【位移】指令，将代表X轴方向的参数改为-5
点击运行
可以看到，当小鸟碰到火法阵的时候，获得了一个临时加速效果
最后，我们设置一个检测通关成功的碰撞效果
点击活动模型，在特效分类下选择红色飞龙之心
把红色飞龙之心放置在合适位置上
鼠标右键选中红色飞龙之心，点击属性
在自定义标签这里，给红色飞龙之心取个标签名为：heart
点击确定
打开代码方块，复制这段代码
这里修改为@heart
提示文字内容改为：恭喜通关
删掉这条指令
在控制项下拖入【结束程序】指令
再拖入【等待1秒】，修改为0.01秒
点击运行
可以看到，当小鸟碰到heart的时候
提示恭喜通关，程序结束
你可以把检测通关成功的碰撞物放到游戏路线的最后
这样只有当玩家碰到这个碰撞物才会提示游戏通关成功
好啦，你也来设置更多好玩的碰撞效果吧