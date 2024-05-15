## KeepWork 可计算文档创作平台

### 什么是可计算文档？

可计算文档是一种互联网文档格式，它是对Word等静态文档的升级。用户可以在文档中添加各种可计算的`模块`，从而直接在网页中编辑和运行各种代码。我们使用web assembly技术，使得Paracraft虚拟仿真, Python, C/C++，CAD，大语言模型等多种可计算模块可以直接在浏览器中运行。

Keepwork致力于成为下一代的`可计算文档`创作平台。无论`数字教材`、文档网站、个人作品，人人都可以成为数字内容的开发者。在人工智能时代，我们鼓励学生、老师将个人作品数字化，建立`个人成长档案`；通过文本与可计算模块结合的方式发布属于自己的数字资源，建立`数字化自我`。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/36110/raw#1713178957667KeepWork 可计算文档创作平台.mp4
  ext: mp4
  filename: 1713178957667KeepWork 可计算文档创作平台.mp4
  size: 117671971
  isNew: true
          
```

### 功能介绍

#### 演示1: 通用计算能力

点击代码右上角的下拉列表可选择：NPL/Python/C++等多种编程语言的边缘计算或云端计算环境。
```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    for i = 1, 2 do
       print("helloworld "..i)
    end
  outputMode: autoParacraft
  output: |
    helloworld 1
    helloworld 2
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: false

```
:point_right:查看全部例子： [https://keepwork.com/official/docs/tutorials/codelab](https://keepwork.com/official/docs/tutorials/codelab)

#### 演示2： 支持内嵌Paracraft 3D元宇宙世界和可计算环境

下面为信息科技教材中体验算法控制的一个例子。点击`访问世界`**左侧**的按钮可直接在文档中打开3D世界， 右键点击世界中的代码方块可以进行图形化编程和文本编程。
```@Project
styleID: 1
project:
  projectId: '2098864'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
根据上面3D世界中的内容， 编写一段程序，先询问用户的年龄，判断是否为免费、全价票或优惠票。也可以直接在网页中编程，并直接运行在3D世界中运行。
```@CodeBlock
styleID: 0
codeblock:
  projectId: '2098864'
  title: ticketCode
  name: ticketCode
  language: codeblock
  code: |-
    say('点我咨询购票');
    registerClickEvent(function()
        nianling = tonumber(ask('请输入您的年龄：'));
        if (nianling < 6) then
            say('免票');
        else
            if (nianling < 14) then
                say('优惠票');
            else
                say('全价票');
            end
        end
    end)
  outputMode: hideParacraft
  output: >
    2024-03-27 12:53:41 293386|main|warn|Entity:SetSkin|skin files does not
    exist 80001;84089;81005;88020;85109;83202
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: false

```

#### 演示3： 基于Markdown的文本编辑环境

您正在浏览的页面就是用keepwork制作的，包括视频、图片存储与审核。url中加入`ed/`可以编辑本页面。
[https://keepwork.com/ed/official/docs/tutorials/keepwork](https://keepwork.com/ed/official/docs/tutorials/keepwork)

支持团队权限管理，GIT版本控制和CDN云端访问加速。

#### 演示4： 支持基于大语言模型的题目测评模组

#####  题目：请用NPL或Python编写程序，计算`1加到100等于多少`

请用`output(result)`函数打印出1加到100的结果，点击运行并提交结果。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    -- 这里的代码是隐藏的，可以定义一些用户会使用到的函数
    function _G.output(value)
        _G.lastOutput = value
        print(lastOutput)
    end
  outputMode: hideParacraft
  output: ''
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: true

```

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    local r = 0
    for i=1, 101 do
       r = r + i
    end
    output(r)
  outputMode: autoParacraft
  output: |
    5151
  output_image: ''
  serialBatchExecution: true
  hideInNonEditMode: false

```

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |
    -- 下面是一个判断用户是否回答正确的检测代码，会串行执行。
    if(tostring(lastOutput) == "5050") then
       print("回答正确!")
    else
       print("回答错误!")
    end
  outputMode: autoParacraft
  output: |
    回答错误!
  output_image: ''
  serialBatchExecution: true
  hideInNonEditMode: true

```

```@Quiz
styleID: 0
quiz:
  data:
    - id: 67dc3130-ebf6-11ee-b728-fbfc1ffe7df7
      type: '4'
      title: quiz title
      score: 1
      desc: desc
      answer:
        - A
      options:
        - item: option 1
        - item: option 2
      nums: 1
      testCode: ''
      isShare: true

```
:point_right: 文档中可以通过隐藏代码的方式加入自动化测评。

#####>  点击查看隐藏的代码
![](https://api.keepwork.com/ts-storage/siteFiles/35774/raw#1711515554875image.png)
#####

:heart: 支持用`大语言模型`对任意题目进行打分和点评。
:book: 支持通过[智慧教育平台](https://edu.palaka.cn)，批量查看或批改学生的基于可计算文档的作业。

![](https://api.keepwork.com/ts-storage/siteFiles/35647/raw#1710653788382image.png)

#### 演示5： 支持Geogrebra数学可计算模组

直接使用数学语言与geogebra数学组件进行交互计算

本次案例探究常见一元二次方程的图像与一般表达式中$f(x)=ax^2+bx+c$ 中常数变量$a,b,c$之间的关联性

- 步骤一：在geogebra中构建变量$a,b,c$，并设定范围
- 步骤二：绘制$f(x)=ax^2+bx+c$ 图形
- 步骤三：探究一元二次方程图像与$a,b,c$之间的关系
- 步骤四：总结规律
```@GeoGebra
styleID: 0
geogebra:
  filename: math_demo_1.ggb
  url: >-
    https://api.keepwork.com/core/v0/repos/official%2Fdocs/files/official%2Fdocs%2F_config%2Fmod%2Fgeogebra%2Fmath_demo_1.ggb

```

#### 演示6：集成了drawio等开源图表工具

可以直接在文档中制作各种UI设计图、思维导图、流程图等，如下。
```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.svg

```
#### 演示7：文档直接与硬件打通，支持数字孪生的课件开发

例如支持物联网，人工智能等智能硬件，包括**micropython, arduino, 外部摄像头**等。只需Chrome浏览器，无需安装其它程序，连接USB就可以直接实现文档与硬件的通讯。

:heart: 亮点：**数字孪生，软件托底**

对于没有经费的学校或学生，我们提供了纯软件的VR仿真解决方案，保证学生完整的操作体验，适合全省普及。VR仿真的代码，连接硬件可以直接写入并在物理世界运行。 
```@Project
styleID: 1
project:
  projectId: 1522980
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29929/raw#1696163759303mpython_CarDemo.mp4
  ext: mp4
  filename: 1696163759303mpython_CarDemo.mp4
  size: 59331515
  isNew: true
  isExpand: true
          
```
#### 演示8：3D动画编程，代表AI时代的编程模式

- 软件层面：用户可以随心所欲的创造出任意复杂的3D动画和软件交互。
- 硬件层面：提供了1对多的协同硬件编程系统。从而实现更多维度的硬件控制系统，支持大多数开源硬件。以及提供面向动画的硬件控制系统。

- [面向动画的AI编程视频](https://keepwork.com/official/open/showcase/AI)

:heart: 亮点：**AI无处不在**
AI前言技术被直接应用到了教学和项目制作之中。创造属于你的AI作品。
```@Project
styleID: 1
project:
  projectId: 1569115
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29979/raw#1696824445151handpose ML.mp4
  ext: mp4
  filename: 1696824445151handpose ML.mp4
  size: 37287994
  isNew: true
  isExpand: true
          
```

```@Project
styleID: 1
project:
  projectId: '1624471'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
### 演示8：助力深圳市开展人工智能教学

2023年10月19日——12月7日期间，举办了《深圳市中小学人工智能教育系列培训活动》。

培训的主题围绕相似原理，人工智能创作工具和可计算文档展开。培训（自愿）报名人数共计1924人，建立10个用户服务群，单场直播最高观看人数1500+，累计提交作业3200+，作业80分以上占比82%，累计交作业4次以上占比38%。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34318/raw#1702262767111image.png
  ext: png
  filename: 1702262767111image.png
  size: 135703
  isNew: true
  isExpand: true
          
```
**“内容可计算，老师成为创造者”** 是本次培训活动的主旨。

- 第1周，主要介绍为何老师要成为创作者，以及AI创作工具的能力边界。
- 第2-3周 介绍了如何基于相似原理和paracraft构建与自然界相似的虚拟世界。
- 第4周 介绍了可计算文档：一种新的数字课件的发布媒介，让学生和老师可以创建以文档为中心的教、学、练、测、评的课堂体验。 
- 第5-6周 引导老师构建一个完整的基于低代码模组的AI课程所需的3D世界。
- 第7-8周 构建基于可计算文档的完成的数字教案。

:point_right: [在线课件与视频回放](https://keepwork.com/official/open/lessons/AI/teachertraining)

### 演示9：基于班级和学校的课程管理与数字化课件创作系统

通过智慧教育平台， 老师可以**将可计算文档转变为可课程**。老师通过分享URL连接可以发布课程或作业。 

老师可以直接点击测评入口，以班级为单位对文档中的测试题目进行作业的统计、批改和点评，支持大语言模型辅助批改。

![1710653284792image.png](https://api.keepwork.com/ts-storage/siteFiles/35646/raw)

老师身份点击后，会跳到作业批改页面。 可以选择班级，并看到班级的答题情况，选择学生或题目可以对题目进行点评，支持AI自动点评。学生在访问自己的课程页面时可以看到所有老师的评价，也可以直接在评论区和老师互动。

:heart: 查看如何创建基于可计算文档的校本课程： [https://keepwork.com/official/docs/UserGuide/share/createlessons](https://keepwork.com/official/docs/UserGuide/share/createlessons)


### 演示10：以网页或WPS文档形式分享，无需安装插件

- 制作的内容， 可以直接在手机微信，PC浏览器等地方打开，支持3D仿真

####> 手机微信扫码访问本网页
![](https://api.keepwork.com/ts-storage/siteFiles/35775/raw#1711519998375image.png)

####

- 支持内嵌WPS PPT文件或Ms Office 演示文稿中，让你的PPT变成互动元宇宙

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35799/raw#1711712285915image.png
  ext: png
  filename: 1711712285915image.png
  size: 813123
  isNew: true
          
```

:point_right: 了解更多 https://keepwork.com/official/docs/UserGuide/share/ppt

### 演示11：作品以VR，360全景视频等多形式呈现

bilibili, youtube等大部分视频平台都支持360全景视频，如果你有VR眼镜可以直接观看，如果没有VR眼镜，也可以在电脑上通过鼠标拖动视频窗口模拟头部的运动来观看。 

- 示例1：360VR全景画展短片：[Jingji的画展](https://www.bilibili.com/video/BV1BG4y1k711)

> 点击上面连接去B站观看，可通过鼠标模拟头部的运动来观看。

```@Project
styleID: 1
project:
  projectId: '75309'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
```@Project
styleID: 1
project:
  projectId: '2518'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

```@Project
styleID: 1
project:
  projectId: '23540'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
- 也支持传统的红蓝、偏振光、左右眼立体输出。
:point_right: 了解更多 https://keepwork.com/official/open/showcase/VR360
  
### 演示12：优秀课程参考案例

- 深圳市宝安区航城学校-王伟老师的公开课《AI助我记单词》6年级
    - [推文链接](https://mp.weixin.qq.com/s/YBqNPqcCM6FZuqHzJ_oTsA)
    - [49分钟上课视频回放](https://v.qq.com/x/page/f3532yjzp4s.html)
- 《相似原理与AI互动游戏》， 1-2年级**AI+英语课**。 [https://keepwork.com/official/open/lessons/AI/teacher/1or2gradeAILesson](https://keepwork.com/official/open/lessons/AI/teacher/1or2gradeAILesson)


```@Project
styleID: 1
project:
  projectId: '1974758'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

```@Project
styleID: 1
project:
  projectId: '1442417'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

### 总结

可计算文档官网： keepwork.com
- 帕拉卡官网： paracraft.cn
- 智慧教育云平台官网： edu.palaka.cn

#### > 功能列表

- 基于Markdown的在线文本编辑环境
- 支持富文本编辑 (含视频、图片存储与审核)
- 基于Git的云端存储、版本控制与多人协作
- 基于CDN的内容加速
- 支持Python/C++/NPL/CAD浏览器计算环境
- 支持内嵌Paracraft 3D元宇宙世界和可计算环境
- 支持Geogrebra数学模组, drawio等开源可计算模组
- 基于班级和学校的课程管理与数字化课件创作系统
- 支持基于大语言模型的题目测评模组
- 支持多种可DIY的网站样式，支持多种导航方式

#### 了解更多：
- https://keepwork.com/official/docs/UserGuide/share/keepwork_intro
- https://keepwork.com/official/open/showcase/AI
- [在线课件与视频回放](https://keepwork.com/official/open/lessons/AI/teachertraining)