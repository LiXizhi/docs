## 第五节 低代码模组2：答题
[点击查看全部课程](https://keepwork.com/official/open/lessons/AI/teachertraining)
:point_right: [本节视频回放](https://v.qq.com/x/page/i35246r4ljl.html)

### 导引：

本节课我们学习代码方块和低代码编程，并制作有趣的在线答题系统。

###> 作业点评
- 优秀作业1：南方科技大学附属中学，梁雪梅，[点击查看](https://keepwork.com/p0096627/pinapple/index)
- 优秀作业2：凤凰城实验学校，卢岱杰，[点击查看](https://keepwork.com/p0090029/xiaochi/index)
- 优秀作业3：深圳市龙岗区德琳学校，沙国君，[点击查看](https://keepwork.com/windofking/54321/index)
###




### 理论

paracraft中的代码都存储在代码方块中。今天我们系统的学习代码方块。
- [代码方块教学1](/official/docs/UserGuide/coding/codeblock1)
- [代码方块教学2](/official/docs/UserGuide/coding/codeblock2)
- [代码方块的输出](/official/docs/UserGuide/coding/output)
- [代码方块中的全局变量](/official/docs/UserGuide/coding/global_vars)

### 项目制作

下面我们学习如何制作一个有趣的在线答题系统，我们先来看一个做好的模板：

```@Project
styleID: 1
project:
  projectId: '1848958'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
### 智能模组介绍

智能模组是一组方块的集合，可能包含电影方块，代码方块，场景和活动角色等。 它有点像可复用的类库。
我们可以在资源库中看到别人分享的智能模组。

- [智能模组文档](https://keepwork.com/official/docs/tutorials/AgentSignBlock)

####> 智能模组1：选择题
- 点击【E】按钮旁边的资源按钮【...】,打开资源库，在【代码】分类下选择【选择题模板】
![](https://api.keepwork.com/ts-storage/siteFiles/30271/raw#1698138607169image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/32798/raw#1700029539618image.png)
- 选择【选择题模板】后，根据提示，走到一个空旷的地方，按下【X】键，就可以在场景中放置【选择题模板】了
  ![](https://api.keepwork.com/ts-storage/siteFiles/32799/raw#1700029675159image.png)
- 选择题模组使用手册: [https://keepwork.com/official/docs/mod/choice](https://keepwork.com/official/docs/mod/choice)
####

####> 智能模组2：填空题
- 点击【E】按钮旁边的资源按钮【...】,打开资源库，在【代码】分类下选择【填空题模板】
![](https://api.keepwork.com/ts-storage/siteFiles/32800/raw#1700029996976image.png)
- 选择【填空题模板】后，根据提示，走到一个空旷的地方，按下【X】键，就可以在场景中放置【填空题模板】了
![](https://api.keepwork.com/ts-storage/siteFiles/32801/raw#1700030063967image.png)
- 填空题模组使用手册: [https://keepwork.com/colaeks/document/fillBlank](https://keepwork.com/colaeks/document/fillBlank)
####

####> 智能模组3：MPython板子
- 点击【E】按钮旁边的资源按钮【...】,打开资源库，在【代码】分类下选择【MPython数控版模板】
![](https://api.keepwork.com/ts-storage/siteFiles/32804/raw#1700030383285image.png)
- 选择【MPython数控版模板】后，根据提示，走到一个空旷的地方，按下【X】键，就可以在场景中放置【MPython数控版模板】了
![](https://api.keepwork.com/ts-storage/siteFiles/32805/raw#1700030414426image.png)
- MPython硬件编程使用手册: [https://keepwork.com/official/docs/tutorials/micropython](https://keepwork.com/official/docs/tutorials/micropython)
####

### 作业

本节课与下一节课共用同一个世界ID，我们需要制作一个可用于翻转课堂的自主学习和测评世界。可以选择信息科技、语文、外语、数学等任意学科、任意年级的课程。
- :dart: 激活并登录平台 https://edu.palaka.cn
- :dart: 课程中心 > 教师提升 > 教师小项目列表 > 《在线答题系统》
- :dart: 作业世界中至少包含3套题目，类型任意（填空题、选择题都可以）
- :dart: 提交世界ID到作业链接：https://jinshuju.net/f/hSHT89

###> 作业详细指南
#### 步骤一：新建世界
- 方法一：自己新建一个世界进行创作
 ![](https://api.keepwork.com/ts-storage/siteFiles/32851/raw#1700099058157image.png)
 ![](https://api.keepwork.com/ts-storage/siteFiles/32852/raw#1700099119591image.png)
- 方法二：使用官方给出的模板进行创作
  - 依次点击【课程中心】-【教师提升】，找到【教师小项目列表】课包
  ![](https://api.keepwork.com/ts-storage/siteFiles/30240/raw#1698112262898image.png)
  - 选择第3课《在线答题系统》
  ![](https://api.keepwork.com/ts-storage/siteFiles/32853/raw#1700099238318image.png)
  - 选择【在线答题闯关模板1】，点击右下角的【开始创作】，使用给出的模板来创作作品。
  ![](https://api.keepwork.com/ts-storage/siteFiles/33209/raw#1700735061049image.png)
  
 

  
#### 步骤二：放置智能模组，添加题目
- 下面以【选择题模板】为例，大家也可以选择其它模板
- 点击【E】按钮旁边的资源按钮【...】,打开资源库，在【代码】分类下选择【选择题模板】
![](https://api.keepwork.com/ts-storage/siteFiles/30271/raw#1698138607169image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/32798/raw#1700029539618image.png)
- 选择【选择题模板】后，根据提示，走到一个空旷的地方，按下【X】键，就可以在场景中放置【选择题模板】了
![](https://api.keepwork.com/ts-storage/siteFiles/32875/raw#1700119946515image.png)

- 选择题模板给出了三个例子，我们选择使用中间的【连续作答】例子给大家演示。
- 鼠标右键打开这个代码方块，就可以添加题目啦
 ![](https://api.keepwork.com/ts-storage/siteFiles/32877/raw#1700120383568image.png)

- **大家需要根据实际情况修改题目内容哈，至少出三道题**
- 题目出完后，我们复制一下这里面的图块代码，鼠标右键点击空白处，选择【复制XML】
 ![](https://api.keepwork.com/ts-storage/siteFiles/32878/raw#1700120601608image.png)
- 然后我们在第一道关卡这里，设置一个NPC
  - 点击【E】键，在代码子标签下选择【代码方块】，右键放置在第一道关卡的旁边
  ![](https://api.keepwork.com/ts-storage/siteFiles/32880/raw#1700120740785image.png)
  - 鼠标右键打开代码方块，点击【图块】，切换到图块编辑模式
  ![](https://api.keepwork.com/ts-storage/siteFiles/32881/raw#1700120893421image.png)
  - 鼠标右键点击空白处，选择【粘贴XML】
  ![](https://api.keepwork.com/ts-storage/siteFiles/32882/raw#1700120913953image.png)
  - 可以看到题目代码就被复制过来了
  ![](https://api.keepwork.com/ts-storage/siteFiles/32883/raw#1700120969179image.png)
  - 我们在【事件】分类下，把【当演员被点击时】指令拖过来，如下图所示，把前面部分的代码拖到【当演员被点击时】指令里面
  - 这段代码代表：当演员被点击时，才会执行里面的程序
  ![](https://api.keepwork.com/ts-storage/siteFiles/32884/raw#1700121152969image.png)
  - 在【外观】分类下，拖入【说】指令，修改文字内容为：点击我开始答题！
  ![](https://api.keepwork.com/ts-storage/siteFiles/32888/raw#1700121724611image.png)
  - 点击【角色模型】，可以更换默认角色：
  ![](https://api.keepwork.com/ts-storage/siteFiles/32885/raw#1700121335457image.png)
  - 拖动三色箭头和蓝色圆环，调整NPC的位置
  ![](https://api.keepwork.com/ts-storage/siteFiles/32886/raw#1700121443096image.png)
  - 添加并启动拉杆，点击NPC看看效果吧
  ![](https://api.keepwork.com/ts-storage/siteFiles/32891/raw#1700122506977image.png)
  - 同样方法，大家在第二道和第三道关卡前面，各新增一个NPC代码吧
  ![](https://api.keepwork.com/ts-storage/siteFiles/32889/raw#1700121919074image.png)
  ![](https://api.keepwork.com/ts-storage/siteFiles/32890/raw#1700121979094image.png)

#### 步骤三：提交作业：

- 点击链接提交作业：https://jinshuju.net/f/hSHT89
![](https://api.keepwork.com/ts-storage/siteFiles/32850/raw#1700098958608image.png)

###

####> 作业评分说明
- 总分100分，60分及格；
- 作品中有使用智能模组 30分
- 至少有3套题（也就是3个关卡，一个关卡算一套题） 30分
- 每套题目不少于3道题 20分
- 每道关卡都添加了NPC 20分
- 如有不清楚的地方，可添加人工智能培训-周老师
![](https://api.keepwork.com/ts-storage/siteFiles/30689/raw#1699536315947888888.png)
####

###> 参考资料
- 出生点的使用：https://keepwork.com/official/tips/s1_wx/1_44
- 出生点常用命令：
  - 游戏模式：/mode game
  - 禁止飞行：/addrule Player CanFly false
  - 禁止跳跃：/addrule Player CanJump false
  - 隐藏底部快捷工具栏：/hide quickselectbar
  - 清空快捷工具栏的物品：/clearbag
  - 人物不能连跳：/addrule Player CanJumpInAir false
  - 多人联网：/ggs connect
- 密室教学：https://keepwork.com/ryan/project2/index
- 人物头顶文字：https://keepwork.com/official/tips/s1/1_149
- 彩色告示牌：https://keepwork.com/official/tips/s1_wx/1_18
- 代码方块深入学习可参考云平台中的【T2教师培训手册】课程内容：
![](https://api.keepwork.com/ts-storage/siteFiles/32762/raw#1700013489279image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/32763/raw#1700013545578image.png)
###