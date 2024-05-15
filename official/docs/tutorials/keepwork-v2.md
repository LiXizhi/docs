# KeepWork可计算文档在教育创新中的应用

## 教学目标
- 理解可计算文档的概念及其在教育中的重要性。
- 掌握KeepWork平台的核心功能及其在教学中的应用。
- 探索如何通过KeepWork平台提高教学质量和学生的学习体验。

## 教学内容与步骤

### 1. 引入介绍
开场白：“尊敬的教育局领导们，今天我将向您介绍一项本公司最新的教育技术产品——KeepWork可计算文档创作平台。
KeepWork可计算文档创作平台基于Markdown语法，允许人们使用易读易写的纯文本格式编写文档，然后转换成结构化的HTML页面，比如您现在正在浏览的页面，包括视频、图片存储与审核。
这个平台不仅仅是一个文档编辑工具，它通过集成多种计算模块和交互功能，为教育领域带来了前所未有的创新和便利。”


### 2. 可计算文档与大语言模型
讲解：“首先，让我们了解什么是可计算文档。与传统的Word等静态文档不同，可计算文档允许用户在文档中嵌入并运行各种代码，如Python、C++等，从而直接在网页中编辑和运行各种代码。
同时，可计算文档也可以让老师和学生在文档中直接调用大语言模型，与人工智能实现对话。
这种文档格式的升级，使得教学内容更加动态和互动，极大地丰富了教学手段和学习体验。”

:point_right: **演示--语文学科：《小池》的作者是谁？他还写过其他什么诗呢？**
在网页（可计算文档）中直接运行代码。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: AI
  code: 《小池》的作者是谁？他还写过其他什么诗呢？
  outputMode: autoParacraft
  output: >-
    《小池》的作者存在争议，一说为南宋诗人杨万里，另一说为晚清名臣曾国藩。


    先来看杨万里。他是南宋的文学家和官员，字廷秀，号诚斋野客，吉水（今属江西）人。杨万里在文学史上被称为“南宋四大家”之一，他的诗作语言浅近明白，意境清新深远，尤其擅长描写自然景物，被誉为“诚斋体”。他的《小池》一诗，通过细腻的笔触，描绘了小池、小荷、蜻蜓等自然元素，表现了初夏时节的生机与活力。


    再来看曾国藩。他是晚清的重臣和军事家，字伯涵，号涤生，湖南湘乡人。曾国藩在镇压太平天国运动中发挥了重要作用，并倡导了洋务运动。他的诗文以豪放著称，抒发了内心的豪情壮志。他的《小池》一诗，虽然具体内容有所不同，但同样表现了自然景物的美好和诗人的豪情。


    由于《小池》的作者存在争议，因此无法确定是哪位诗人所作。不过，无论是杨万里还是曾国藩，他们都是中国文学史上杰出的文学家和政治家，他们的作品都对中国文化产生了深远的影响。


    希望以上信息对你有帮助，如需了解更多关于杨万里或曾国藩的生平信息，建议查阅相关历史文献或咨询历史专家。

```



### 3. 一个文档，满足不同的编译环境
演示与讲解：“KeepWork提供了强大的通用计算能力。现在，我将演示如何在文档中选择不同的编程语言环境，进行代码编写、运行和调试。”

接下来，我将为大家展示一个简单的可计算文档示例，这段一段简单的通用代码，使用了for循环和print函数，最终输出"**hello world 1**"和"**hello world 2**"。
请大家观察代码的运行结果，以及它是如何与文档内容互动的。

:point_right: **演示--计算机学科: 通用计算能力**

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

### 4. 元宇宙与虚拟仿真
演示与讲解：“通过集成Paracraft虚拟仿真技术，KeepWork使得用户可以在3D世界中创建和编程，例如，通过编写程序来判断用户在虚拟场景中的票务情况。”

:point_right: **演示--信息科技：在可计算文档中打开Paracraft 3D元宇宙世界**

下面以**信息科技教材**中体验算法控制的一个例子。
我们可以直接在可计算文档中打开3D元宇宙世界。
注：进入世界后能看到两组代码方块，我们通过**代码**和**图块**两种方式，编写一段程序，先询问用户的年龄，判断是否为免费、全价票或优惠票。

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
### 5.支持Geogrebra数学可计算模组

接下来这个案例， 我们将直接使用数学语言与geogebra数学组件进行交互计算。
:point_right: **演示--高等数学：Geogrebra数学可计算模组**

本案例探究常见一元二次方程的图像与一般表达式中$f(x)=ax^2+bx+c$ 中常数变量$a,b,c$之间的关联性

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

### 6.基于大语言模型的题目测评模组
演示与讲解：在KeepWork可计算文档创作平台中，可以实现基于大语言模型的题目测评模块的功能。这个模块允许教师创建编程题目，并设定自动评分的标准，从而对学生的编程作业进行评估和反馈。
具体来说，这个功能包含了以下几个部分：
**题目描述：** 学生被要求使用Python或其他编程语言编写一个程序，计算从1加到100的总和，并使用output(result)函数打印出结果。

**隐藏代码块：** 在可计算文档中，可以定义一些辅助函数，比如_G.output，这个函数用于记录学生的输出结果，并将其打印出来。这部分代码对学生是不可见的，用于后续的评分逻辑。

**学生作答代码块：** 学生在这里编写自己的代码来解决问题。例如，使用一个循环从1加到101，最后调用output(r)输出结果。

**自动评分代码块：** 这部分代码用于检测学生的答案是否正确。如果学生的输出与预期的答案（在这个例子中是5050）相符，则打印“回答正确!”；否则打印“回答错误!”。

**测验组件：** 最后，文档中还包含了一个测验组件，它允许教师设置题目、选项和正确答案。学生可以选择答案并提交，系统将根据学生的选择给出相应的评分和反馈。

通过这种方式，KeepWork平台不仅提供了一个交互式的编程学习环境，还实现了自动化的题目测评和反馈机制。这使得教师能够高效地管理大量的学生作业，同时也让学生能够及时了解自己的学习进度和问题所在。这种自动化的测评方式大大提高了教学的效率和质量。

:point_right: **演示--计算机编程**

#####  题目：请用NPL或Python编写程序，计算`1加到100等于多少`


请用`output(result)`函数打印出1加到100的结果，点击运行并提交结果。
注：文档中可以通过隐藏代码的方式加入自动化测评。


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


### 7.UI设计图、思维导图、流程图轻松制作
演示与讲解：在KeepWork可计算文档创作平台中，用户可以直接在文档中制作UI设计图、思维导图和流程图等，为用户提供了一个直观的界面来创建和编辑图形内容，极大地提高了文档的视觉效果和信息传达的效率。
:point_right: **演示--图表制作**

可以直接在可计算文档中制作各种UI设计图、思维导图、流程图等，如下。
```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.svg

```

### 8.可计算文档与硬件打通，支持数字孪生的课件开发
演示与讲解：在KeepWork可计算文档创作平台中，一项特别引人注目的功能是其**与硬件的直接集成能力**，这为数字孪生技术的课件开发提供了强大支持。
数字孪生技术允许老师创建一个真实物体或系统的虚拟副本，从而在虚拟环境中**模拟和分析**其行为和性能。

通过KeepWork平台，教师和学生可以利用物联网和人工智能等智能硬件技术，如micropython、arduino和外部摄像头，来**创建交互式的学习体验**。这些硬件设备可以通过USB连接到任何配备Chrome浏览器的设备，无需安装其他软件即可实现与文档的即时通讯和数据交换。

而对于那些经费有限，无法购买实体硬件的学校或学生，KeepWork提供了纯软件的**VR仿真**解决方案。
这个方案不仅能够确保学生获得**完整的操作体验**，还能够在全省范围内普及，使得每个学生都能够接触到最新的技术教育。
VR仿真的代码可以直接写入并用于物理世界中的硬件设备，这意味着学生可以在虚拟环境中进行编程和测试，然后将这些代码**应用到现实世界**的硬件上。

这种硬件集成和仿真能力，不仅为学生提供了一个实践和探索的平台，还为教师提供了丰富的教学资源。通过这种方式，KeepWork平台不仅促进了STEM教育的发展，也为学生的未来职业生涯奠定了坚实的基础。


:point_right: **虚拟世界演示**

```@Project
styleID: 1
project:
  projectId: '1522980'
  eventName: ''
  projectTagsShow: false
  projectMembersShow: false
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
:point_right: **视频演示**

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

### 9.AI时代的编程新模式

演示与讲解：在AI时代，编程模式正在经历一场革命性的变化，其中**3D动画编程**成为了一个新的趋势。KeepWork可计算文档创作平台正是这一变革的代表，它为用户提供了一个能够创造复杂3D动画和软件交互的环境。

- 软件层面
在软件层面上，KeepWork平台赋予了用户强大的创作自由度。用户可以利用平台提供的工具和功能，设计出丰富多彩的3D动画效果，同时实现复杂的软件交互逻辑。无论是游戏开发、模拟教学还是可视化数据展示，用户都能够通过编程将自己的想法变为现实。这种3D动画编程不仅提升了用户体验，也使得信息的表达更加直观和生动。

- 硬件层面
在硬件层面上，KeepWork平台提供了1对多的协同硬件编程系统，这意味着用户可以通过单一的软件接口控制多个硬件设备。这样的系统支持了更多维度的硬件控制，使得用户能够将创意扩展到物理世界中。平台支持大多数开源硬件，极大地拓宽了可编程硬件的种类和应用范围。此外，面向动画的硬件控制系统使得硬件设备能够与3D动画同步，为用户提供了更加丰富和沉浸式的交互体验。

通过结合软件和硬件的编程能力，KeepWork平台为用户提供了一个全面的解决方案，使得用户能够在AI时代中充分发挥创造力，开发出创新的项目和应用。这种融合了3D动画和硬件控制的编程模式，不仅推动了技术的发展，也为教育、娱乐、设计等多个领域带来了新的可能性。

:point_right: **演示--跨学科学习：动画 + 编程 + 机器人**
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/11552/raw#1586274007401基于动画的AI可编程机器人_small.mp4
  ext: mp4
  filename: 1586274007401基于动画的AI可编程机器人_small.mp4
  size: 7391594
          
```
:point_right: **虚拟世界演示--人工智能：视觉识别**
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

:point_right: **视频演示--人工智能：视觉识别**
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


### 10.课程管理与数字化课件创作
演示与讲解：通过智慧教育平台，教师可以轻松地将**可计算文档转变为课程**，进行班级和学校的课程管理。教师可以通过分享链接发布课程或作业，并通过系统进行作业的统计、批改和点评，实现教学管理的数字化和智能化。
老师可以直接点击测评入口，以班级为单位对文档中的测试题目进行作业的统计、批改和点评，支持大语言模型辅助批改。

![1710653284792image.png](https://api.keepwork.com/ts-storage/siteFiles/35646/raw)

老师身份点击后，会跳到作业批改页面。 可以选择班级，并看到班级的答题情况，选择学生或题目可以对题目进行点评，支持AI自动点评。学生在访问自己的课程页面时可以看到所有老师的评价，也可以直接在评论区和老师互动。

:heart: 查看如何创建基于可计算文档的校本课程： [https://keepwork.com/official/docs/UserGuide/share/createlessons](https://keepwork.com/official/docs/UserGuide/share/createlessons)


### 11.跨平台分享与互动
演示与讲解：最后，KeepWork的文档可以在多种平台上分享和互动，如手机微信、PC浏览器等。这使得教学内容的传播更加便捷，学生和教师之间的沟通更加顺畅。
- 制作的内容， 可以直接在手机微信，PC浏览器等地方打开，支持3D仿真

####> 手机微信扫码访问本网页
![](https://api.keepwork.com/ts-storage/siteFiles/35854/raw#1712479458034image.png)

 


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
### 总结

通过以上演示，我们可以看到KeepWork可计算文档创作平台在教育领域的广泛应用和巨大潜力。
它不仅能够提升教学质量和效率，还能够激发学生的创造力和探索精神。
我们期待与教育局合作，共同推动教育信息化和现代化的进程。

最后，我将展示KeepWork的官方网站和相关资源，以便大家了解更多信息，并亲自体验这个强大的平台。

###> 助力深圳市开展人工智能教学
2023年10月19日——12月7日期间，举办了《深圳市中小学人工智能教育系列培训活动》。

培训的主题围绕相似原理，人工智能创作工具和可计算文档展开。培训（自愿）报名人数共计1924人，建立10个用户服务群，单场直播最高观看人数1500+，累计提交作业3200+，作业80分以上占比82%，累计交作业4次以上占比38%。
![](https://api.keepwork.com/ts-storage/siteFiles/34318/raw#1702262767111image.png)
###

###> “内容可计算，老师成为创造者”
- 第1周，主要介绍为何老师要成为创作者，以及AI创作工具的能力边界。
- 第2-3周 介绍了如何基于相似原理和paracraft构建与自然界相似的虚拟世界。
- 第4周 介绍了可计算文档：一种新的数字课件的发布媒介，让学生和老师可以创建以文档为中心的教、学、练、测、评的课堂体验。 
- 第5-6周 引导老师构建一个完整的基于低代码模组的AI课程所需的3D世界。
- 第7-8周 构建基于可计算文档的完成的数字教案。
:point_right: [在线课件与视频回放](https://keepwork.com/official/open/lessons/AI/teachertraining)
###

###> 内嵌PPT演示文稿，让你的PPT变成互动元宇宙
[https://keepwork.com/official/docs/UserGuide/share/ppt](https://keepwork.com/official/docs/UserGuide/share/ppt)
###

###> 优秀课程参考案例
- 深圳市宝安区航城学校-王伟老师的公开课《AI助我记单词》6年级
    - [推文链接](https://mp.weixin.qq.com/s/YBqNPqcCM6FZuqHzJ_oTsA)
    - [49分钟上课视频回放](https://v.qq.com/x/page/f3532yjzp4s.html)
- 《相似原理与AI互动游戏》， 1-2年级**AI+英语课**。 [https://keepwork.com/official/open/lessons/AI/teacher/1or2gradeAILesson](https://keepwork.com/official/open/lessons/AI/teacher/1or2gradeAILesson)
###

###> 功能列表
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
###

###> 官网导航
- 可计算文档官网： [keepwork.com](keepwork.com)
- 帕拉卡官网： [paracraft.cn](paracraft.cn)
- 智慧教育云平台官网： [edu.palaka.cn](edu.palaka.cn)
###

###> 更多资料
- [https://keepwork.com/official/docs/UserGuide/share/keepwork_intro](https://keepwork.com/official/docs/UserGuide/share/keepwork_intro)
- [https://keepwork.com/official/open/showcase/AI](https://keepwork.com/official/open/showcase/AI)
- [在线课件与视频回放](https://keepwork.com/official/open/lessons/AI/teachertraining)
###