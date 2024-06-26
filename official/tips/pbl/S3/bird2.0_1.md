## 《飞翔的小鸟2.0》第一节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21821/raw#飞翔的小鸟2.0_L1.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21820/raw#飞翔的小鸟2.0_L1.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>

## 字幕


通过前面《飞翔的小鸟》的学习
我们学会了通过拖拽的方式让小鸟往前飞
控制小鸟躲开各种障碍物，最终顺利通关
这节课开始，我们将学习一些新的知识来继续优化《飞翔的小鸟》
迭代出《飞翔的小鸟2.0》，带来更优的项目体验
这一小节，我们学习如何通过键盘上的按键控制小鸟飞行


### 步骤一

首先，我们打开工具栏，选择代码方块
放置于场景中，右键打开代码方块
可以看到，自动生成了一个电影方块，角色默认添加为演员
然后，点击代码编辑窗口上的角色模型，切换角色
这里，我们切换为小鸟模型
注意看左边这里有小鸟对应的动作编号
比如4号代表走路动作
这个动作编号可以用来设置小鸟不同的运动状态
了解了动作编号后，点击确定，这样我们成功添加了小鸟模型
拖动蓝色圆环，可以把小鸟模型旋转到合适方向
接着，我们点击图块，切换到图块模式
在外观项下拖出【播放动作编号】指令
【播放动作编号】指令可以播放角色的相应动作
默认是4号，4号代表走路动作
我们点击运行，可以看到小鸟处于飞行状态
接着，我们拖入【观看此角色】指令
这条指令代表把摄影机视角固定到了小鸟身上
接下来，我们让小鸟一直往前飞行
这里我们使用【永远重复】和【位移】指令
在控制项下拖入【永远重复】指令
【永远重复】指令表示将里面包含的程序一直重复执行
在运动项下拖入【位移】指令，【位移】指令可以使角色往任意方向移动
前面三个参数分别代表角色在X、Y、Z轴三个方向移动的距离
第四个参数是设定移动的时间
大家可以看到，小鸟这里有三个不同颜色的箭头
其中红色为X轴，蓝色为Y轴，绿色为Z轴
下面我们让小鸟一直往X轴正方向移动
将代表X轴方向的参数改为0.2，Y、Z轴两个方向的参数为0
点击运行，可以看到小鸟就往X轴正方向移动了
如果我想让小鸟一直往前，也就是X轴反方向去移动，那该怎么办？
我们应该把X轴方向的参数改为：-0.2
点击运行，可以看到小鸟就往前，也就是X轴反方向移动了
我们再来修改一下后面的时间参数，让小鸟移动更快一点
点击运行，可以看到小鸟移动的速度就变快啦
到这里，小鸟一直往前飞的效果就成功实现了

### 步骤二

在上一小节中，我们成功让小鸟一直往前飞行
接下来，我们编写程序控制小鸟上下移动
打开代码方块
在事件项下找到【当空格键被按下时】指令，拖入代码编辑区
当键盘上的空格键被按下时，就会执行这里面的程序
这里，我们想要当空格键被按下时，小鸟就往上移动1格
将运动项下【位移】指令放入【当空格键被按下时】指令的里面
将代表Y轴方向的参数改为1，X、Z轴两个方向的参数为0
时间修改为0.3秒
点击运行，按下空格键，我们看到小鸟就往上移动了1格
接着我们实现当X键被按下时，小鸟往下移动1格
我们直接复制这条指令，修改按键为X
将代表Y轴方向的参数改为-1
点击运行，按下X键，小鸟就往下移动了1格
这样，我们就可以通过空格键和X键分别控制小鸟上下移动了

### 步骤三

在上一小节中，我们实现了小鸟上下移动的效果
这一小节，我们编写程序控制小鸟左右移动
跟上、下移动的原理类似，首先，打开代码方块
直接复制这条指令，修改按键为a
我们需要实现当a键被按下时，小鸟往左边移动1格
想要让小鸟往左边移动，也就是往绿色Z轴的反方向移动
我们将代表Z轴方向的参数改为-1，X、Y轴两个方向的参数为0
点击运行，按下a健，可以看到，小鸟就往左边移动了1格
接着我们实现当d键被按下时，小鸟往右移动1格
直接复制这条指令，修改按键为b，将代表Z轴方向的参数改为1
点击运行，按下b键，可以看到，小鸟就往右边移动了1格
到这里，控制小鸟左、右移动的程序也编写好了
现在小鸟会一直往前飞行，那我们该如何结束程序呢？
在事件项下拖入【当空格键按下时】指令，修改按键为q
在控制项下拖入【结束程序】指令
【结束程序】指令会让互相连接的所有代码方块的程序全部停止运行
点击运行，按下q键，程序就结束了
最后，我们拖入【说】指令，把游戏规则说明一下
为了让玩家看清楚游戏规则，我们加入【等待1秒】指令
修改参数为3秒
关闭代码方块编辑窗口，添加拉杆
自己启动拉杆，试试效果吧
体验完后，你也快去自己的世界中，给小鸟添加上这些效果吧！


