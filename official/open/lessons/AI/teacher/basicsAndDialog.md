## 第二节 低代码模组1：对话与事件
[点击查看全部课程](https://keepwork.com/official/open/lessons/AI/teachertraining)
:point_right: [本节视频回放](https://v.qq.com/x/page/n3516h3tsls.html)

### 导引：
帕拉卡是一款对标和模拟自然界的创作平台。本节课我们将学习帕拉卡的基础操作，并制作一个有对话交互的课程世界。

### 基础搭建教学（5分钟）

:point_right: 自然界是由粒子构成的；Paracraft世界也是由粒子构成的。

- [基础搭建：官方文档链接](https://keepwork.com/official/docs/UserGuide/scene/create_blocks)

:point_right: 自然界是有层级和实体的；Paracraft世界中的粒子可以变成活动模型

- [BMAX模型：官方文档链接](https://keepwork.com/official/docs/UserGuide/scene/bmax_model)

:dart: 练习：搭建一个五子棋的棋子，并将棋子转变成活动模型。


```@Project
styleID: 1
project:
  projectId: '42701'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

### 基础电路教学（5分钟）

:point_right: 自然界的运转需要能量；Paracraft中的代码方块和电脑一样，需要电源才能启动。

* [电路教学1：电路简介，输入输出，充能](https://keepwork.com/official/paracraft/videos/vt_circuit_1)
* （选修）[电路教学2：向上下传导，逻辑电路](https://keepwork.com/official/paracraft/videos/vt_circuit_2)
* （选修）[电路教学3：锁存器，中继器](https://keepwork.com/official/paracraft/videos/vt_circuit_3)
* （选修）[电路教学4：连闪器，自动门，隐藏门](https://keepwork.com/official/paracraft/videos/vt_circuit_4)

:dart: 练习：用拉杆或能量块给代码方块充能， 用按钮或压力板激活电影方块。

### 说课演示（5分钟）
:dart: 第一课[《人工智能各行各业》](https://keepwork.com/official/open/lessons/AI/intro78?layout=none)

- 了解并体验人工智能在制造业、农业、交通、医疗、教育等行业场景中的应用；
- 了解自然语言处理、智能语音、计算机视觉、生物特征识别、虚拟现实/增强现实、人机交互等关键领域技术的应用场景。

### 项目教学：《元宇宙说课》（20分钟）

我们本节课将制作一个具有对话功能的元宇宙世界，我们先来看下最终的效果。

```@Project
styleID: 1
project:
  projectId: '1714052'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```


#### > 步骤一：搭建一面墙
  - 使用快捷键可以事半功倍哦
    - W、A、S、D：移动
    - 双击W不放：加速向前移动
    - F：进入/退出飞行模式（空格键飞高，X键下落）
    - 点击鼠标中键：瞬间移动
    - 按住鼠标右键并移动：旋转视角
    - Ctrl+S：保存
    - Ctrl+Z：撤销
    - 鼠标右键：建造方块
    - 鼠标左键：删除普通方块（部分方块需要长按鼠标左键才能删除）
    - Shift+鼠标右键：快速创建3个或多个方块
    - Shift+鼠标左键：删除光标周围3*3的方块
    - Ctrl+鼠标左键：选中物品，按住Ctrl键，继续点击左键，可选中一片区域的物品
    - Ctrl+Shift+鼠标左键：选择所有与当前方块相连的方块
   - 墙体搭建参考：
   ![](https://api.keepwork.com/ts-storage/siteFiles/30096/raw#1697611980347image.png)  

#### > 步骤二：放置相册，添加图片
 - 相册的使用参考资料:
    - 相册的使用: https://keepwork.com/official/tips/s1/1_211
    - 可点击的相册: https://keepwork.com/official/tips/s1/1_197

![](https://api.keepwork.com/ts-storage/siteFiles/30098/raw#1697613359437image.png)

#### > 步骤三：对话框模板的使用

- 点击【E】按钮旁边的资源按钮【...】,打开资源库，在【代码】分类下选择【对话框模板】

![](https://api.keepwork.com/ts-storage/siteFiles/30271/raw#1698138607169image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/30270/raw#1698138505591image.png)
- 选择【对话框模板】后，根据提示，走到一个空旷的地方，按下【X】键，就可以在场景中放置【对话框模板】了
  ![](https://api.keepwork.com/ts-storage/siteFiles/30242/raw#1698112857896image.png)
- 对话框模板使用说明手册: [https://keepwork.com/wyx9529/dialog_use/index](https://keepwork.com/wyx9529/dialog_use/index)

#### > 步骤四：使用活动模型触发广播消息

- 在【工具】子标签下找到【活动模型】
 ![](https://api.keepwork.com/ts-storage/siteFiles/30114/raw#1697620828851image.png)
- 点击【模型】，在弹出的对话框中，选择一个模型，点击确定
  ![](https://api.keepwork.com/ts-storage/siteFiles/30115/raw#1697621004631image.png)
- 右键把模型放置在场地中，接着右键点击模型，点击【属性】，在弹出的模型属性框中修改对应参数即可。
 ![](https://api.keepwork.com/ts-storage/siteFiles/30116/raw#1697621205027image.png)
- 比如我们在【点击事件】这里填入：01，那么当我们在世界中点击这个人物模型，就会广播一个“01”消息出去啦
  ![](https://api.keepwork.com/ts-storage/siteFiles/30117/raw#1697621346566image.png)

#### > 步骤五：使用木压力板和命令方块触发广播消息

- 木压力板属于触发能量的一种方块，当角色踩在踏板上时会触发效果
- 命令方块可以用来编写程序和写入指令，通过踏板按钮等开关触发效果
  ![](https://api.keepwork.com/ts-storage/siteFiles/30099/raw#1697615284755image.png)
- 我们可以通过/sendevent发送事件，右键打开命令方块编辑窗口，写入命令：/sendevent 01，也就是向世界中广播消息“01”
  ![](https://api.keepwork.com/ts-storage/siteFiles/30100/raw#1697615618750image.png)

#### > 步骤六：点击NPC触发广播消息

- 在【代码】子标签下找到【代码方块】
![](https://api.keepwork.com/ts-storage/siteFiles/30118/raw#1697621808845image.png)
- 右键把代码方块在场地中:
![](https://api.keepwork.com/ts-storage/siteFiles/30119/raw#1697621963217image.png)
- 接着右键点击打开代码方块，点击【图块】，切换到图块编辑模式：
![](https://api.keepwork.com/ts-storage/siteFiles/30120/raw#1697622001398image.png)
- 点击上方的【角色模型】，可以更改默认的方块人模型，拖动三色箭头可以移动模型位置：
 ![](https://api.keepwork.com/ts-storage/siteFiles/30121/raw#1697622256679image.png)
- 在【事件】分类下拖出【当演员被点击时】和【广播】指令到右边的脚本区
![](https://api.keepwork.com/ts-storage/siteFiles/30122/raw#1697622324566image.png)
- 关闭代码方块编辑窗口，并在代码方块旁边放置一个拉杆，鼠标点击拉杆，启动拉杆，这样刚才写的程序就运行起来了
![](https://api.keepwork.com/ts-storage/siteFiles/30123/raw#1697622502186image.png)
- 这时候鼠标点击人物模型，就会广播“01”消息出去啦

### 总结

- 自然界的粒子性：
- 层级与实体
- 自然界的能量守恒：能量块与拉杆
- 智能模组《对话框》的使用

## 作业

1952年人类的第一个AI应用是跳棋Checker程序，因此我们的作业是比跳棋高级的《五子棋》程序。通过帕拉卡智慧教育平台，自主学习AI课程《五子棋》，并创作属于自己的五子棋作品。按要求提交作业后，鼓励大家把作品录制视频分享到微信沟通群。

- :dart: 激活并登录平台 https://edu.palaka.cn
- :dart: 课程中心 > 教师提升 > 教师小项目列表 > 《五子棋》
- :dart: 提交作品项目ID https://jinshuju.net/f/pOjWlp

### > 作业详细指南

#### 步骤一：注册教学云平台，开通超管账号：

- 使用最新版本谷歌或QQ浏览器，登录平台（edu.palaka.cn），点击【还没账号？去注册】-【学校注册】，根据系统提示，填写基本信息、单位资料、信息提交后，我们将会尽快审核完毕。
- 说明：
  - 单个学校多个老师申请的情况下，请先进行内部沟通，指定一位老师作  为超管入驻平台，然后由超管在平台内添加其他老师。
  - 超管入驻当天会通过审核；如果入驻申请被驳回，说明学校已有超管入驻，可先联系超管，若无法联系到超管，可在群里咨询培训服务-廖老师。
  - 学校统一社会信用代码可登录百度（baidu.com）搜索学校名称进行查询。

 ![](https://api.keepwork.com/ts-storage/siteFiles/30243/raw#1698114199339image.png)
 
 - 如已有账号，请在【学校注册】页面选择【账号登录】。

 ![](https://api.keepwork.com/ts-storage/siteFiles/30257/raw#1698127820244image.png)
 
 - 超管入驻成功后，可再创建3个老师账号（如需创建更多账号，可联系培训服务-廖老师）。
   - 登录平台，点击【教务管理】-【邀请老师】添加老师手机号码邀请老师加入学校；若老师已有账号，可点击“添加账号”邀请入校。若老师账号添加错误，可点击“删除”后重新添加。
![](https://api.keepwork.com/ts-storage/siteFiles/30258/raw#1698127975754image.png)
 


#### 步骤二：登录（https://edu.palaka.cn/login）：

- 使用刚注册的手机号码登录。
 ![](https://api.keepwork.com/ts-storage/siteFiles/30241/raw#1698112622327image.png)

#### 步骤三：下载并安装客户端

- 登录平台（edu.palaka.cn），在首页【应用中心】-【智慧教育客户端】进行下载，并根据提示进行安装。
![](https://api.keepwork.com/ts-storage/siteFiles/30248/raw#1698117236455image.png)

#### 步骤四：依次点击【课程中心】-【教师提升】，找到【教师小项目列表】课包，跟着AI课程进行学习和创作。

![](https://api.keepwork.com/ts-storage/siteFiles/30240/raw#1698112262898image.png)
 - 可以先看看【作品欣赏】的内容，然后选择【学习清单】内容，点击右下角【启动3D世界】开始学习：
![](https://api.keepwork.com/ts-storage/siteFiles/30259/raw#1698128450749image.png)
 

#### 步骤五：创作作品：

- 跟着AI课程《五子棋》学习完毕后，点击【开始创作】，创作自己的《五子棋》作品：
![](https://api.keepwork.com/ts-storage/siteFiles/30255/raw#1698126783011image.png)
 

- 例如：创作中的《五子棋》作品截图：
![](https://api.keepwork.com/ts-storage/siteFiles/30246/raw#1698115767594image.png)

- 创作过程中，要经常按**【Ctrl+S】**保存作品到本地，保存后会有对应版本提示：
![](https://api.keepwork.com/ts-storage/siteFiles/30250/raw#1698118025019image.png)
 
 
- 作品创作完成后，点击【保存世界】，获得作品ID：
 ![](https://api.keepwork.com/ts-storage/siteFiles/30251/raw#1698118182947image.png)
 
![](https://api.keepwork.com/ts-storage/siteFiles/30252/raw#1698118221923image.png)
 
- 上传成功后可在客户端左上角查看自己**作品ID**。


![](https://api.keepwork.com/ts-storage/siteFiles/30249/raw#1698117847693image.png)
 

#### 步骤六：提交作业：

- 点击链接提交作业：https://jinshuju.net/f/pOjWlp
![](https://api.keepwork.com/ts-storage/siteFiles/30286/raw#1698297987846image.png)


 
### > 参考资料
- 《五子棋》参考作品：
- 官方作品：151131、153032、172803
- 学生作品：1011329、1014287、1012465、1668203
- 优秀作品《画展》欣赏，作品id：75309
- 电影方块学习：https://keepwork.com/official/docs/UserGuide/animation/movie_block
- 演员和动画学习：https://keepwork.com/official/docs/UserGuide/animation/actor
- 如何用Paracraft创造虚拟展厅：https://keepwork.com/official/docs/tutorials/webXR
- 导出360度VR全景视频：https://keepwork.com/official/docs/tutorials/vr360
- 分享作品到微信群的方法;[https://keepwork.com/official/tips/s1_wx/1_208](https://keepwork.com/official/tips/s1_wx/1_208)
- 活动模型的简单使用方法：https://keepwork.com/luo142587/jspx/huodongmoxing
---
####
