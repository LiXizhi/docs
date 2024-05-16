## 《超级农场》第四节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21627/raw#超级农场4_4.1.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21628/raw#超级农场4_4.1.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>

## 字幕


这节课，我们将来学习一个新的知识点——骨骼
骨骼主要可以用来做什么呢？
它会控制与它连接且颜色相同的所有方块
通过操作骨骼，可以让模型动起来
具体的效果在接下来的课程中我们可以感受一下
可以看到，在场景的左边有一只放置好的兔子
我们来给这个兔子添加上一块骨骼

### 步骤一

首先，点击E按钮，打开工具栏
选择电影子标签下的骨骼方块
左键打掉兔子模型下方的一个方块
右键放置骨骼方块
这里需要注意的是骨骼有一头是尖的， 代表了骨骼的方向
然后，选中放置了骨骼的兔子模型
保存为bmax模型，取名为rabbit
注意保存的时候要面向X轴正方向，也就是红色箭头所指向的方向
设置模型属性为可拖动
右键放置兔子在场景中
到这里，带有骨骼的兔子就成功放置好啦
拖动兔子，可以注意到，虽然添加了骨骼，但是兔子现在是静态没有动作的
想要让兔子动起来，我们还需要对骨骼进行一些操作
### 步骤二
想要让兔子动起来，我们需要给它制作骨骼动画
要制作动画，必不可少的就是电影方块了
点击E按钮，打开工具栏
选择电影子标签下的电影方块
右键放置在场景中
打开电影方块
修改右下角的时间为1秒
点击电影片段窗口中的+号，添加角色
这里，我们选择上一小节保存的兔子模型
点击确定，兔子就成功添加好了
可以注意到左下角的属性为动作
接着，点击右下角蓝色框的+号，选择0号，代表待机动作，点击确定
点击左下角的动作属性，切换为大小属性
拖动坐标轴，可以调整兔子的大小
关闭电影方块，到这里，待机状态下的动画就制作好啦
接下来，我们制作走路状态下的动画
在保存待机动作电影方块的旁边，再添加一个电影方块
打开新添加的电影方块
同样的方法，将时间修改为1秒
添加兔子角色，调整角色的大小
接着，点击左下角的大小属性，切换为骨骼属性
可以看到有一个绿色的小点，这个小点就是骨骼所在的位置
点击它，会出现旋转轴，三个颜色代表三个不同的方向
调整旋转轴，可以设计兔子的动作
首先，拖动旋转轴，设置模型的初始状态
然后，右键点击下方的时间滑块，输入500，调整时间到500毫秒
再次拖动旋转轴，设置模型的中间状态
最后，右键点击下方的时间滑块，输入1000，调整时间到1000毫秒
再次拖动旋转轴，设置模型的最终状态
到这里，让兔子前后摇摆的动作就设计完成啦
点击到开始，点击播放看看效果
最后，我们给这个动作设置一个动作编号
点击左下角的骨骼，切换到动作属性
点击到开始，让时间轴来到第一帧
点击+号，选择4号，代表走路动作，点击确定
点击播放，可以看到兔子就前后摆动起来啦
关闭电影方块
到这里，待机动作和走路动作的骨骼动画就分别制作好了


### 步骤三

骨骼动画已经制作好了
在给农场添加青蛙和小狗时，我们注意到青蛙和小狗是有动作编号的
这种带动作的模型就叫做ParaX动画模型
如何将骨骼动画保存为ParaX动画模型呢？
操作也比较简单，与保存bmax模型的操作是类似的
按下Ctrl键，点击鼠标左键
选中两个电影方块
点击保存，选择ParaX动画模型导出
命名为rabbit
点击确定，动画模型成功导出
点击E按钮，打开工具栏
选择工具子标签下的活动模型
点击模型，选择刚刚保存的X文件
可以注意到，模型下方有0和4两个动作编号
这就是骨骼动画里设计的动作
点击确定，右键放置模型到   场景中
拖动坐标轴上的小方块，调整兔子大小
点击属性，切换到属性面板
修改待机动画为“走路”
修改自动转向为“是”
点击确定，拖动来看看效果
可以看到，兔子一边旋转一边前后摆动
如何制作和导出动画模型的方法你学会了吗？
你也去制作一个ParaX动画模型来丰富你的农场吧
带有多个骨骼的ParaX动画模型，我们在后面的课程中会继续学习