## 《太阳系的奥秘》第二节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21801/raw#太阳系的奥秘L2.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21800/raw#太阳系的奥秘L2.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>

## 字幕


在上一节课中，我们实现了太阳自转的效果
这一节课，我们将实现地球自转的效果以及围绕太阳公转的效果
公转是什么意思呢？
公转指的就是地球围绕太阳旋转
被太阳照射的向阳面就形成了白天，背阳面就变成了黑夜
同时，地球在围绕太阳公转时南北半球得到的阳光照射强度不同
因此，地球上才会出现四季变化
这一小节，我们先来添加一个代表地球的角色

### 步骤一

点击E按钮，打开工具栏
选择电影子标签下的代码方块和电影方块
在场景中放置一组代码方块+电影方块
接着，打开代码方块
点击代码编辑窗口左上角的角色模型，切换角色
这里，我们选择保存好的白色星球bmax模型
将角色名称修改为：earth

### 步骤二

上一小节，我们已经添加好了地球角色
这一小节，我们调整一下地球的属性，并且将地球放置到合适位置
打开场景中控制地球角色的代码方块
点击图块，切换到图块模式
将数据项下的【设置角色的名字为】指令拖过来
点击名字，将名字修改为颜色
将数据项下的【颜色】指令拖放到【设置角色的颜色】指令中
点击【颜色】指令，我们通过颜色滑动条将地球调整为合适的颜色
点击运行，可以看到白球变成了蓝色
颜色设置好后，我们将地球放在场景中标记的蓝色位置
在运动项下拖出【设置角色位置】指令，输入对应的参数
点击运行，可以看到地球出现在了指定位置
位置调整好后，我们再来将地球变大一些
将外观项下的【缩放到】指令拖过来，修改参数为150
点击运行，可以看到地球变大了

### 步骤三

通过上一小节的学习，我们将地球初始状态调整好了
接下来，我们继续编写程序实现地球的公转与自转
第一步，我们先来实现地球的公转，也就是让地球围绕着太阳旋转
我们需要用到一条新的指令，打开场景中的代码方块
在运动项下找到【固定到父角色的骨骼__上】，拖过来
我们把这里的父角色改为太阳的角色名，也就是sun
注意，这条指令的第二个参数不是骨骼名，而是link
它代表将当前的角色，也就是地球，连接到太阳角色上
并且一直保持太阳和地球之间的位置关系
相当于中间用一根隐形的线将两者连接起来了
最后，为了保证在太阳被创建之后再将地球固定到太阳上
我们需要在【固定到sun的骨骼link上】指令上方放置【等待0.1秒】指令
点击运行，我们可以看到，地球围绕着太阳旋转起来了
到这里，地球的公转效果就成功实现了
下一步，我们来实现地球自转的效果
跟太阳自转效果一样，我们要让地球一直旋转，先来添加一个【永远重复】指令
将控制项下的【永远重复】指令拖放到【固定到sun的骨骼link上】指令的下方
然后，将运动项下的【旋转__度】指令拖放到【永远重复】指令的里面
修改旋转指令的参数
最后，为了避免出现死循环，我们需要在【永远重复】指令的里面添加一条【等待】指令
将控制项下的【等待__秒】指令拖放到【旋转__度】指令下方
修改【等待1秒】指令的参数
点击运行，可以看到地球不仅有公转效果，自转的功能也成功实现了