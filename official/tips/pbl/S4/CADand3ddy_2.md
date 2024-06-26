## 《CAD与3D打印》第二节
 
提示：如视频播放不了，可在课程项目世界里，点击“讲解回放”进行观看。
 
<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/22339/raw#CAD与3d打印L2.webm" type="video/webm" />
  <source src="https://api.keepwork.com/ts-storage/siteFiles/22338/raw#CAD与3d打印L2.mp4" type="video/mp4" />
   
  你的浏览器不支持播放
</video>
<style>
video::-webkit-media-controls-fullscreen-button { display: none; } 
</style>

## 字幕


上一节课中，我们制作了一个灯笼模型
接下来的两节课，我们对灯笼模型进行优化改造
将灯笼模型变成一个小鹿矿车
这一小节，我们先来添加小鹿的其中两条腿


### 步骤一

打开场景中的CAD方块，名字和注释已经取好了
然后，将【创建】指令拖过来，创建一个对象
修改一下对象名
将【柱体】指令拖过来，作为其中的一条腿
调整一下柱体指令的参数到合适
这里，我们将它的半径调整为0.15，高度调整为0.5
点击运行，可以看到柱体现在在正中间位置
接着，我们使用【移动】指令调整一下位置
红色轴代表的是X轴方向，我们让柱体往红色轴正方向移动一段距离
调整一下X轴参数为0.57
点击运行，看到柱体往外移动了一段距离
太靠近中间了，我们让柱体再往前移动一点
想要让柱体往前移动，我们需要修改Z轴参数，也就是绿色轴
调整一下Z轴参数为0.5
点击运行，可以看到柱体往前移动了
位置调整好后，我们再来添加另一条腿
复制上面两条指令
这两条腿大小是一样的，我们只需要修改一下它的位置就可以了
调整一下X轴参数为负0.57
点击运行，可以看到生成了两条腿
到这里，两条腿就生成好啦


### 步骤二

上一小节，我们给小鹿矿车添加了两条腿
这一小节，我们学习一条新的指令—【镜像】指令
【镜像】指令是一条用于复制图形的指令
使用它，我们可以快速生成另外两条腿
将【镜像】指令拖过来，它一共有两个参数
前面的参数为参照面，以参照面为基础，在它的另一边复制出一模一样的图形
就类似于我们照镜子一样
点击这个参数可以切换对应的平面，我们运行一下试试看
调整为xz平面，点击运行，发现这不是我们想要的效果
再来调整为yz平面，点击运行
调整为xy平面，点击运行，发现这是我们要的效果
后面的参数是中心点的位置，指以这个点为对称点
没有特殊需要的话我们一般使用默认的原点即可
到这里，关于【镜像】指令如何使用你学会了吗？


### 步骤三

上一小节，我们使用【镜像】指令添加好了另外两条腿
我们再来添加一对钩子和钩子环，这样就可以将矿车连起来了
这一小节，我们先来给矿车添加一个钩子环
跟前面一样，我们先来创建对象
然后，将【长方体】指令拖过来
修改一下它的参数
我们将X轴参数调整为0.5，代表它的宽度
Y轴参数调整为0.1，代表它的高度
Z轴参数为0.5，代表它的长度
调整好后，点击运行，图形出现在下方
我们将【移动】指令拖过来
调整Y轴参数为0.5，Z轴参数为1，将图形往外移动一定距离
点击运行，可以看到生成了一个长方体
最后，我们再用一个正方体它的中间挖空
将【正方体】指令拖过来，布尔运算符号修改为减号，修改参数为0.4
点击运行，可以看到中间被挖空了
到这里，一个钩子环就成功添加好了


### 步骤四

上一小节，我们给矿车添加了一个钩子环
有了钩子环，还缺少一个钩子跟它配套使用呢
这一小节，我们就来给矿车添加一个钩子
打开场景中的CAD方块，注释和对象已经给我们创建好了
我们使用两个长方体组合来完成钩子的搭建
将【长方体】指令拖过来，修改一下它的参数
修改好后，将【移动】指令拖过来
修改参数，让图形移动到合适位置
点击运行，一个钩子的钩就做好啦
我们再来制作钩子的连接部分
将【长方体】指令拖过来，修改一下参数
同样的，添加【移动】指令，调整位置
点击运行，发现长方体是竖着的
这里，我们要让长方体横着连接，所以我们将高度变小一点
将Z轴的参数变大一些
调整好后，点击运行，我们再来看看效果
这样，钩子的效果就成功实现了
钩子和钩子环都有了，我们就可以将矿车拼接在一起，形成一条小火车啦
如果使用3D打印技术打印出来，我们可以把这个当做笔筒来使用哦
下一节课，我们会给小鹿矿车添加上脖子、头等等




