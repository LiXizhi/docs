## 第四节 可计算文档
[点击查看全部课程](https://keepwork.com/official/open/lessons/AI/teachertraining)
:point_right: [本节视频回放](https://v.qq.com/x/page/r3521s6eqb9.html)

### 导引：

本节课我们学习可计算文档的使用，制作个人项目网站。

###> 作业点评
- 优秀作业1：深圳市龙岗区德琳学校，沙国君，[1780051](https://webparacraft.keepwork.com/?pid=1780051)
- 优秀作业2：深圳市龙岗区坪地兰陵学校，肖桂花，[1779911](https://webparacraft.keepwork.com/?pid=1779911)
- 优秀作业3：深圳市龙华区锦华实验学校，张翠红，[1780281](https://webparacraft.keepwork.com/?pid=1780281)
###

### 什么是可计算文档？
可计算文档是专门针对数字教材设计的一种互联网文档格式，它是对Word等静态文档的升级。用户可以在数字文档中添加`代码方块`，从而直接在网页中编辑和运行各种代码。我们使用web assembly技术，使得NPL, Paracraft, Python, C/C++等代码可以直接在浏览器中运行，并且支持复杂的在线3D仿真和编辑环境。 

:point_right: 点击 [查看详情](https://keepwork.com/official/open/lessons/AI/CodeLab)

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: print("hello world")
  outputMode: autoParacraft
  output: |
    hello world
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: false

```
###> 为什么用可计算文档？
大多数的纸质和电子图书只能阅读，无法进行自由创造和练习。我们希望创造和推广一种`教、学、练、测、评`一体化的数字教材格式。

其实在国外大学中，例如[jupyter notebook](https://jupyter.org/)的可计算文档已经广泛应用于计算机专业的数字教材。人工智能的IT企业，例如openai，也广泛使用[google codelab](https://developers.google.cn/codelabs), [microsoft github codespace](https://docs.github.com/zh/codespaces)等基于docker容器的可计算文档，来发布产品的使用手册。

[keepwork.com](https://keepwork.com)是我们今天要学习的一款专门针对教育和科研领域的可计算文档创作平台。本页面包括之前的所有交互课件也都是使用这个工具制作的。

当教材通过可计算文档的方式数字化后，老师将成为创造者，学生则可以更快的边学边练，得到快速的反馈。数字教材可以取代常规的纸质教材和教师课件。
老师可以基于标准教材，随时随地创造属于自己的数字教材。每一次备课，都是一次再创造的过程。老师可以融入个性化的教学。而学生则通过与真实世界中类似的方式在互联网上学习知识。当学生走入社会后，大部分知识将通过类似的方式自主学习，培养学生通过互联网学习知识和动手创作的良好习惯。
###

###> 进化论与项目式教学
可计算文档可以将一个项目的制作过程，以生命成长的方式线性的呈现出来。 从一行代码到上千行代码的进化和演变过程，可以线性的呈现出来，并且读者可以随时在任意位置更改代码，好比修改一个在进化中的生命的DNA。所以可计算文档是项目式教学非常好的载体。

我们希望数字教材的每个章节都包含一个完整的项目作品的循序渐进的制作过程。

- 对于学生：在使用教材学习的过程中可以直接动手联系，学习完之后，可以创造属于自己的作品。 
- 对于老师：我们提供了一个人可随意修改的数字教材的格式和编辑器，方便老师之间共享数字资源，创造出更多丰富多彩的、跨学科的课程。 
###

###> 个性化教学与AI
像ChatGPT这样的大语言模型AI也是一种可计算的文档模块。 将大语言模型AI引入可计算文档，可以让我们的数字教材更加智能，甚至个性化的提供问题的解决步骤，驱动文档中的其他可计算资源(Agent)。 在可预见的未来，每本教材、每个学生都有一个专属的AI老师伴学，实现1v1的教学体验。

 ![](https://api.keepwork.com/ts-storage/siteFiles/30570/raw#16994134665309638e5bbda8c6316d1b2ebcc7a699bb.jpg)
上图为ChatGPT Copilot驱动Paracraft的图块编程的示例。

这一切的基础就是可计算文档。可计算文档提供了一个基于`markdown`的语言框架和众多代理(Agent)的可计算环境(`Runtime`)。下面我们先来学习Markdown语言。
###

### 提出基于相似原理的数字课程设计模型
基于相似原理，学习的本质是对动画的控制力。针对新课标，我们可以分成下面5个步骤去设计数字课程。
- 1. 寻找生活中的相似情景
- 2. 定义1-2个重要体验：重要体验一般由动画片段（记忆）和对动画的控制力(思维)。我们需要寻找或制作能清晰表达重要体验的短动画。
- 3. 设计课堂动手实验：心理学研究表明，当学生动手参与时，更容易形成重要体验。因此，我们要设计在课堂上可以让学生动手的实验，目标是帮助学生形成重要体验。 
- 4. 课后继续迭代：基于课堂项目，鼓励学生回家后继续动手迭代项目。
- 5. 通过反转课堂获得反馈：提供让学生展示个人作品的场所。 

```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2FPBL.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2FPBL.svg

```
其中
- 针对1：我们制作了500个针对3-9年级的2022新课标的3D动画和虚拟仿真实验。 
- 针对2：我们提供了基于可计算文档的在数字教材中直接进行3D虚拟仿真和动手实验的工具，让老师可以成为教材的创造者，让学生可以自由探索并创造属于自己的作品。

参考数字教材章节案例： https://keepwork.com/official/open/lessons/AI/teacher/5gradeAlgorithm


### 可计算文档入门

####> 什么是markdown? 'MarkUp' vs 'MarkDown' 
- HTML = HyperText **Markup** Language
- **Markdown**
HTML是超文本，例如`<div style="color:red">Hello</div>`， 使用`<>`作为文档的标记(Mark), 它更适合机器读写。 Markdown的字面意思是标记(Mark)下来（Down）,也就是不要HTML中的标记(Mark). 所以它更适合人类读写，同时也支持简单的超链接和常用格式。
全世界的wiki维基百科，都是采用markdown这种格式编写的。大语言模型(例如ChatGPT)的输入和输出也是采用markdown格式（例如大语言模型中的步骤列表、清单、文本和代码、超链接等）。
####

#### 常用的markdown语法

markdown是没有语法的，任何语言、文字、代码都是合法的。 但是它有一些常用的标点符号，可以实现下面内容的格式化显示：==标题、加粗、高亮、列表、连接、分割线、图片、表格、表情包、代码、引用==

详见: [如何创建个人网站？](https://keepwork.com/official/docs/UserGuide/share/personalsite)

### 项目：创建一个项目官网

下面我们学习如何为自己的作品制作一个项目官网，我们先来看一个做好的模板：
:point_right: 点击 [查看网页](https://keepwork.com/luo142587/Other/《小池》数字课件模板)
```@Project
styleID: 1
project:
  projectId: '530'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
####> 步骤一：登录可计算文档的编辑器
- 点击[keepwork.com](https://keepwork.com)，登录自己的账号即可。
 ![](https://api.keepwork.com/ts-storage/siteFiles/30536/raw#1699322449734image.png)
####

####> 步骤二：创建个人网站
- 点击【创建新网站】,选择【经典布局】，点击下一步：
![](https://api.keepwork.com/ts-storage/siteFiles/30537/raw#1699336059414image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/30538/raw#1699336115044image.png)
- 设定网站的访问地址（这里大家根据自己需求起名字即可），点击创建：
 ![](https://api.keepwork.com/ts-storage/siteFiles/30539/raw#1699336270447image.png)
- 网站创建成功，点击【开始编辑】,在右边空白的地方，就可以开始编辑自己的网站啦
![](https://api.keepwork.com/ts-storage/siteFiles/30540/raw#1699336420137image.png)
![](https://api.keepwork.com/ts-storage/siteFiles/30542/raw#1699336699244image.png)
- 写一段文字，介绍一下你的项目吧
 ![](https://api.keepwork.com/ts-storage/siteFiles/30547/raw#1699347937847image.png)
####

####> 步骤三：添加引用
- 行首使用>加上一个空格表示引用段落，内部可以嵌套多个段落。语法：
```javascript
>这里是一个引用
>>内部嵌套
```
<div style="clear:both"></div>

- 这里我们添加一个《小池》原文的引用，添加语法：
 ![](https://api.keepwork.com/ts-storage/siteFiles/30568/raw#1699410738387image.png)
- 看效果
 ![](https://api.keepwork.com/ts-storage/siteFiles/30569/raw#1699410835883image.png)
####

####> 步骤四：添加项目模块
- 下面把我们做好的《小池》项目添加进来
- 点击右上方【模块】，在左边弹出的栏目中选择【项目】，点击添加
  ![](https://api.keepwork.com/ts-storage/siteFiles/30548/raw#1699348727349image.png)
- 在左边弹出的栏目中填入《小池》作品ID，把【显示网页版开关按钮】打开
  ![](https://api.keepwork.com/ts-storage/siteFiles/30549/raw#1699348970777image.png)
- 可以看到我们成功把项目模块添加到文档中了
  ![](https://api.keepwork.com/ts-storage/siteFiles/30550/raw#1699349168705image.png)
####

####> 步骤五：添加代码方块
- 接着我们可以添加代码方块，实现AI对话
- 点击右上方【模块】，在左边弹出的栏目中选择【其它】-【代码方块】，点击添加
  ![](https://api.keepwork.com/ts-storage/siteFiles/30551/raw#1699349537013image.png)
- 点击下拉，选择【AI对话】
  ![](https://api.keepwork.com/ts-storage/siteFiles/30552/raw#1699349713034image.png)
- 在【AI对话】框中输入问题，点击【运行】按钮，看看Ai对话的表现吧
  ![](https://api.keepwork.com/ts-storage/siteFiles/30553/raw#1699349985306image.png)
- :point_right: 更多用法，点击 [查看详情](https://keepwork.com/official/open/lessons/AI/CodeLab)
####

####> 步骤六：添加图片和视频
- 如果需要添加图片或者视频，直接把图片或者视频从电脑端拖入编辑窗口中即可
 ![](https://api.keepwork.com/ts-storage/siteFiles/30559/raw#1699351905248image.png)
- 图片插入成功（插入视频也是类似操作）
 ![](https://api.keepwork.com/ts-storage/siteFiles/30561/raw#1699351992539image.png)
####

####> 步骤七：添加可折叠模块
- 那如何把步骤一的内容折叠起来呢？我们按如下图所示，添加一些语法即可
 ![](https://api.keepwork.com/ts-storage/siteFiles/30562/raw#1699407483357image.png)
- 可以看到部分内容已经被折叠起来了
 ![](https://api.keepwork.com/ts-storage/siteFiles/30563/raw#1699407579964image.png)
- 现在就差图片部分没有折叠，我们需要使用另外一种语法处理一下，我们先找到图片的链接，如图所示，点击展开按钮就能看到图片的链接：
 ![](https://api.keepwork.com/ts-storage/siteFiles/30564/raw#1699408151451image.png)
- 复制图片链接，把它填入下面这个语法中，填入后记得删除原图片链接部分
  - 英文输入法下，输入：一个叹号!+一个双括号[]+小括号()，小括号()里面填入图片链接，语法如下：
```javascript
![]()
```
<div style="clear:both"></div>

![](https://api.keepwork.com/ts-storage/siteFiles/30566/raw#1699408771992image.png)

- 添加语法后，可以看到图片部分也被折叠进去了
 ![](https://api.keepwork.com/ts-storage/siteFiles/30565/raw#1699408584958image.png)
####

####> 步骤八：添加思维导图
- 项目制作过程分享完毕，我们用思维导图来个总结吧
- 点击右上方【模块】，在左边弹出的栏目中选择【常用】-【绘图板】，点击添加
![](https://api.keepwork.com/ts-storage/siteFiles/30571/raw#1699421036664image.png)
- 点击【打开绘图板】
![](https://api.keepwork.com/ts-storage/siteFiles/30572/raw#1699421113234image.png)

- 先给文件起个名字，这点很重要哈，然后点击【创建】
![](https://api.keepwork.com/ts-storage/siteFiles/30573/raw#1699421251070image.png)
- 从左边选择需要的元素拖到右边即可
![](https://api.keepwork.com/ts-storage/siteFiles/30574/raw#1699421382105image.png)
- 编辑好内容，点击上方的【修改未保存，点击此处保存】，然后点击【关闭】
![](https://api.keepwork.com/ts-storage/siteFiles/30575/raw#1699422068178image.png)
- 最终效果，支持随时修改
![](https://api.keepwork.com/ts-storage/siteFiles/30576/raw#1699423531863image.png)

####

####> 步骤九：添加首页导航
- 下面我们给网站添加首页导航
- 点击右上方【模块】，在左边弹出的栏目中选择【导航】-【首页导航】，选择其中一种元素，点击添加
![](https://api.keepwork.com/ts-storage/siteFiles/30577/raw#1699424112874image.png) 
 

- 在左边弹窗中可以设置首页导航的【图标】、【主标题】、【菜单】等信息
![](https://api.keepwork.com/ts-storage/siteFiles/30578/raw#1699424514373image.png) 
 
- 看最终效果 
![](https://api.keepwork.com/ts-storage/siteFiles/30579/raw#1699424671730image.png) 
 
- 编辑过程中，记得及时按Ctrl+S保存内容，编辑好内容后，把这个链接提交到作业里面即可。
![](https://api.keepwork.com/ts-storage/siteFiles/30581/raw#1699427027361image.png) 
 
####


### 作业

- :dart: 用 [https://keepwork.com](https://keepwork.com) 创建一个个人网站，里面至少包含一个项目介绍的页面。
- :dart: 提交作业链接：https://jinshuju.net/f/Y253Kj

####> 作业评分说明
- 总分100分，60分及格；
- 创建了个人网站：30分
- 有添加项目模块：20分
- 有添加导航和思维导图：10分
- 教案中有插入图片：10分
- 教案中有插入视频：10分
- 有使用AI对话模块：10分
- 部分教案内容可折叠和展开：10分
- 如有不清楚的地方，可添加人工智能培训-周老师
![](https://api.keepwork.com/ts-storage/siteFiles/30689/raw#1699536315947888888.png) 
 
 


####

###> 参考资料
- 可计算文档使用说明：https://keepwork.com/official/docs/tutorials/codelab
- 点击[查看更多官方文档](https://keepwork.com/official/docs/index)
  - 点击左边栏目可以查看更多内容
  ![](https://api.keepwork.com/ts-storage/siteFiles/30580/raw#1699425862831image.png)
  
  - 进入编辑模式可以查看原代码，如何进入编辑模式？如图所示，在网址中输入ed即可:
  ![](https://api.keepwork.com/ts-storage/siteFiles/30535/raw#1699321249959image.png)
###