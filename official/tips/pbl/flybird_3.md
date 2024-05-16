## 《飞翔的小鸟》第三节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21585/raw#飞翔的小鸟03_3.22.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21584/raw#飞翔的小鸟03_3.22.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>

## 字幕


在上节课中，我们实现了小鸟碰到障碍物返回初始位置的功能
可是小鸟回到初始位置并不容易被看到
想让这个效果体验更好应该怎么办呢？

### 步骤一

这节课，我们来学习一个新知识点——text命令
执行这条命令会生成一个用于提示的对话框
打开代码方块
因为场景中障碍物的方块变成了云杉树叶方块
所以这里修改了参数为云杉树叶的方块ID 91
接着，在事件标签下，拖出【执行命令】指令
输入/text
文字内容修改为“你输了，重新开始吧！”
关闭代码编辑界面，拖动小鸟看看效果吧！
当小鸟碰到障碍物的时候会弹出对话框，显示提示内容
这样的效果体验是不是更好了呢？
### 步骤二
接着，我们来看看这个休闲度假风的场景
可以看到添加了一些苹果模型作为障碍物
还有彩虹、休闲椅等一些bmax模型作为装饰
这些模型都是使用彩色方块搭建出来的
打开代码方块，程序代码有什么不同呢
这里，我们添加了两条【如果_那么】条件判断指令
可以注意到【是否碰到_】指令的参数
分别是苹果方块的ID，229和云杉树叶方块的ID，91
表示当碰到苹果和云杉树叶时都会提示失败
点击右上角退出代码编辑界面
拖动小鸟，我们来体验一下吧！
你也可以尝试着搭建出各种各样的场景地图
此外，创作出更多侦测碰撞的效果也是一个很不错的想法哦
快去尝试一下吧，更多可能在等着你去探索发现！


