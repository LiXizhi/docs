
<style>
  .markdown-body hr {
    height: 1px;
  }
</style>





```@Lesson
styleID: 0
lesson:
  animations: []
  updated: '2020/04/17 18:13:11'

```


# **一、	教学目标：**
1.知识目标：
* 认识Python，开发第一个Python程序

2.能力素养：
* 在编程的过程中，对运行中发现的问题进行代码调试，培养独立思考和解决问题的能力

3.思维提升：
* 通过项目练习，训练学生的数学运用能力，感受编程的严谨性和创造性。

# **二、	教学重难点：**

### 教学重点：
* 熟悉Paracraft的操作界面
* 认识python代码方块

### 教学难点：
* 认识Python代码方块

# **三、	教学准备：**
* 课件（**项目id：**）
* 带鼠标、键盘的电脑
* 上课学员的账号、密码
* 顺畅的网络环境


# **四、	教学过程：**
### **1.	情景引入（10‘）：**
&emsp;&emsp;欢迎大家来到Paracraft3D编程课堂。前面我们学习了普通代码方块，相信很多同学都能够熟练掌握并使用普通代码方块来创作属于自己的作品了。今天我们来认识一下Paracraft的另外一个代码方块：Python代码方块。那么Python代码方块与普通代码方块类似， 只是语法是Python3语言的。 底层我们将Python代码编译为NPL代码， 然后再执行。 所以代码方块中的Python具有普通Python没有的一些新特性。下面让我们一起去开发我们的第一个Python程序吧
 

### **2.知识点解析（25‘）**
* 认识Python
&emsp;&emsp;Python是一门简单易学且功能强大的，全世界最流行的编程语言之一。它正式诞生于1991年，它拥有很多优点，例如免费、开源，可移植性，解释型语言，面向对象，可扩展性，丰富的库等等，现在已经广泛运用于网站开发、游戏、网络爬虫、大数据分析、人工智能等领域中。
&emsp;（1）Python发展历史
&emsp;&emsp;Python 是由 Guido van Rossum （吉多·范·罗苏姆，中国Python程序员都叫他 龟叔）在八十年代末和九十年代初，在荷兰国家数学和计算机科学研究所设计出来的。
&emsp;&emsp;Python 本身也是由诸多其他语言发展而来的,这包括 ABC、Modula-3、C、C++、Algol-68、SmallTalk、Unix shell 和其他的脚本语言等等。
&emsp;&emsp;Python崇尚优美、清晰、简单，是一个优秀并广泛使用的语言。Python在2020年3月TIOBE排行榜中排行第三，它是Google的第三大开发语言，Dropbox的基础语言，豆瓣的服务器语言，知乎的主力语言。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10555/raw#1583803030078Python语言排行榜2020.3.png
  ext: png
  filename: 1583803030078Python语言排行榜2020.3.png
  size: '231213'
  unit: '%'
  percent: 80

```

&emsp;&emsp;现在 Python 是由一个核心开发团队在维护，Guido van Rossum 仍然占据着至关重要的作用，指导其进展。
&emsp;&emsp;Python目前有两个版本，Python2和Python3，最新版分别为2.7.17和3.8.2。
&emsp;&emsp;Python至理名言：Life is shot, you need Python. 人生苦短，我用Python。为何这样说呢？同样的问题，用不同的语言解决，代码量差距很大，一般情况下python是java的1/5，代码量小，维护成本低，编程效率高，所以说人数苦短，我用python。
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10554/raw#1583801701820image.png
  ext: png
  filename: 1583801701820image.png
  size: '210674'
  unit: '%'
  percent: 60

```

&emsp;（2）Python=大蟒蛇？
&emsp;&emsp;Python的中文意思是大蟒蛇，但是它的名字和蟒蛇无关。Python这个名字，来自龟叔所挚爱的电视剧Monty Python's Flying Circus。Monty Python是英国六人喜剧团体，喜剧界的披头士。龟叔是这个团体的忠实粉丝。他希望这个新的叫做Python的语言，能符合他的理想：创造一种C和shell之间，功能全面，易学易用，可拓展的语言。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10565/raw#1583810480065image.png
  ext: png
  filename: 1583810480065image.png
  size: '199585'
  unit: '%'
  percent: 30

```

&emsp;（3）为什么选择Python？
&emsp;&emsp;Python 是应用极为广泛的编程语言，是初学者的语言，在人工智能时代，Python 将越来越受到重视，很多中小学和大学都使用Python来教授编程。我们选择Python编程的充分理由如下：
&emsp;&emsp;①易于学习和阅读：Python有相对较少的关键字，结构简单，使用英文单词、标点、符号和数字等就能编程，有明确定义的语法，代码定义清晰，学习起来很简单。
&emsp;&emsp;②一个广泛的标准库：Python的最大的优势之一是丰富的库，我们可以理解为各类工具包，我们可以把这些工具包运用到自己的程序中，从而更加方便快捷的编写自己的程序。
&emsp;&emsp;③随处可运行：由于它的开源本质，Python已经被移植在许多平台上（经过改动使它能够工作在不同平台上），同样的python代码可以运行在Linux、Windows和Mac上，并且运行结果一样。
&emsp;&emsp;④可扩展性：Python之所以被称为“胶水语言”，就是因为其具有很好的扩展性。如果你需要你的一段关键代码运行得更快或者希望某些算法不公开，你可以把你的部分程序用C或C++编写，然后在你的Python程序中使用它们，看起来就像是Python把其它语言“粘”在一起了。
&emsp;（4）Python的实际应用
&emsp;&emsp;①互联网领域：谷歌公司的应用程序引擎、代码、Google.com、 Google 爬虫、Google 广告和其他项目正在广泛使用 Python；CIA：美国中情局网站是用 Python 开发的；NASA：美国航天局广泛使用 Python 进行数据分析和计算；YouTube：世界上最大的视频网站 YouTube 是用 Python 开发的；Dropbox：美国最大的在线云存储网站，全部用 Python 实现，每天处理 10 亿的文件上传和下载；Facebook：大量的基本库是通过 Python 实现的；知乎：中国最大的 Q＆A 社区，通过 Python 开发（国外 Quora）；除此之外，还有搜狐、金山、腾讯、盛大、网易、百度、阿里、淘宝、土豆、新浪、果壳等公司正在使用 Python 来完成各种任务。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10566/raw#1583811912044image.png
  ext: png
  filename: 1583811912044image.png
  size: '352387'
  unit: '%'
  percent: 80

```

&emsp;&emsp;②金融商业领域：定量交易、金融分析，在金融工程领域，Python不仅使用最多，而且使用最多，其重要性逐年增加。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10564/raw#1583810393402image.png
  ext: png
  filename: 1583810393402image.png
  size: '442597'
  unit: '%'
  percent: 80

```

&emsp;&emsp;③科学计算和人工智能领域：典型的图书馆NumPy、SciPy、Matplotlib、Enided图书馆等。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10562/raw#1583810133176image.png
  ext: png
  filename: 1583810133176image.png
  size: '562823'
  unit: '%'
  percent: 80

```

&emsp;&emsp;④云计算开发领域：Python是从事云计算工作需要掌握的一门编程语言，目前很火的云计算框架OpenStack就是由Python开发的，如果想要深入学习并进行二次开发，就需要具备Python的技能。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10563/raw#1583810208047image.png
  ext: png
  filename: 1583810208047image.png
  size: '171146'
  unit: '%'
  percent: 80

```

&emsp;&emsp;⑤爬虫开发领域：在爬虫领域，Python几乎是霸主地位，将网络一切数据作为资源，通过自动化程序进行有针对性的数据采集以及处理。从事该领域应学习爬虫策略、高性能异步IO、分布式爬虫等，并针对Scrapy框架源码进行深入剖析，从而理解其原理并实现自定义爬虫框架。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10561/raw#1583809986206image.png
  ext: png
  filename: 1583809986206image.png
  size: '100023'
  unit: '%'
  percent: 80

```

&emsp;&emsp;⑥医疗领域：在医疗领域，Python人工智能应用已逐渐渗透，如病理诊断、影像、肿瘤治疗等。Python还可以用来给机器人编写程序，让机器人来完成非常复杂的手术。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10560/raw#1583809789933image.png
  ext: png
  filename: 1583809789933image.png
  size: '294979'
  unit: '%'
  percent: 80

```


 


 

* 认识Python代码方块
  为了方便大家学习Python语言，Paracraft为大家提供了Python代码方块。区别于一般的Python编辑器，Python代码方块可以直接运行Python代码，无需下载安装Python软件就可以进行python编程，极大降低了初学者的门槛。
  下面让我们简单认识一下Python代码方块吧！
  （1）、Python代码方块在E键代码分类下，ID是10516, 是蓝色的，带Py字样。
  
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10520/raw#1583724243832image.png
  ext: png
  filename: 1583724243832image.png
  size: '89037'
  unit: '%'
  percent: 50

```
   （2）我们右键创建Python代码方块，右键单击Python代码方块，我们就进入了Python代码方块的编辑界面。我们看到下面显示: 我们在Python代码方块旁边自动创建了一个电影方块，现在我们可以用Python代码控制电影方块中的演员。这就像我们用普通代码方块去控制电影方块中的演员一样，关于这点我们将在后面的章节中会学到。
   
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10523/raw#1583724670811image.png
  ext: png
  filename: 1583724670811image.png
  size: 458931
          
```


  （3）Python代码方块主要分为二大区域，脚本区和终端区：
  
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10537/raw#1583739703645image.png
  ext: png
  filename: 1583739703645image.png
  size: 66586
          
```
&emsp;脚本区：写代码，编辑Python程序。
&emsp;终端区：点击运行，即可看到代码运行结果。

  （4）如果想更多地了解Python 3 这门语言，可以查阅 教程。  
  
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10527/raw#1583725254298image.png
  ext: png
  filename: 1583725254298image.png
  size: 28622
          
```



 
### **3.思维导图（10‘）**
&emsp; &emsp;至此，我们已经简单的了解过Python和Python代码方块了，下面我们用Python编写我们的第一个程序啦！

 *  项目分析：
 我们的第一个程序是，在Python代码方块的终端区显示消息：“Hello World!”
 （1）在脚本区窗口中，输入下面这行文字。“print”函数是系统内置函数，主要功能是输出，它告诉计算机在屏幕上显示一些内容，比如这句话“Hello World!”
   ```python
   print("Hello World!")
 
   
   ```
   
   
   &emsp;&emsp;（2）点击上方的“编辑并运行”，程序输出结果如下：
  
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10539/raw#1583741605267image.png
  ext: png
  filename: 1583741605267image.png
  size: 248245
          
```

  &emsp;&emsp;（3）如果代码没有正常工作，别慌！每一个程序都会犯错，想要成为一个编程高手，寻找程序中的“bug”是必备技能之一。现在我们回到程序中，确保是在英文状态下输入的，检查一下“print”拼对了么？输入双引号或者单引号了么?输入圆括号了么？修正你发现的任何错误，然后再次运行你的程序。
    
 *  程序工作流程图：
  <style>
  .comp-board{
    text-align: center;
  }
</style>


```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2F%E6%88%91%E7%9A%84%E7%AC%AC%E4%B8%80%E4%B8%AAPython%E7%A8%8B%E5%BA%8F.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2F%E6%88%91%E7%9A%84%E7%AC%AC%E4%B8%80%E4%B8%AAPython%E7%A8%8B%E5%BA%8F.svg

```



### **4.实操演练与拓展（40’）**
* 练习一：
要求：编写一个程序，输出“我爱编程，我爱Paracraft！”
   ```python
   print("我爱编程，我爱Paracraft！")
   ```
* 练习二：
要求：编写代码完成你的第一张名片吧！参考格式如下：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10531/raw#1583736630079image.png
  ext: png
  filename: 1583736630079image.png
  size: '95198'
  unit: '%'
  percent: 50

```

```Python
print("==========我的名片==========")
print("姓名: paracraft")
print("QQ:839673135")
print("电话：0755-86967012")
print("公司地址:深圳南山区科技园德赛科技大厦西座2303")
print("============================")
```

* 练习三（可作为课后作业）：
要求：编写代码打印九九乘法表，参考格式如下：
 
 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10558/raw#1583806991174image.png
  ext: png
  filename: 1583806991174image.png
  size: 45023
          
```





```Python
print("1*1 = 1")
print("1*2 = 2 2*2 = 04 ")
print("1*3 = 3 2*3 = 06 3*3 = 09")
print("1*4 = 4 2*4 = 08 3*4 = 12 4*4 = 16")
print("1*5 = 5 2*5 = 10 3*5 = 15 4*5 = 20 5*5 = 25")
print("1*6 = 6 2*6 = 12 3*6 = 18 4*6 = 24 5*6 = 30 6*6 = 36" )
print("1*7 = 7 2*7 = 14 3*7 = 21 4*7 = 28 5*7 = 35 6*7 = 42 7*7 = 49" )
print("1*8 = 8 2*8 = 16 3*8 = 24 4*8 = 32 5*8 = 40 6*8 = 48 7*8 = 56 8*8 = 64" )
print("1*9 = 9 2*9 = 18 3*9 = 27 4*9 = 36 5*9 = 45 6*9 = 54 7*9 = 63 8*9 = 72 9*9 = 81")
```
**注**：（在后面的章节，我们会学习如何用更简单的方法打印九九乘法表）       




        
* 保存并上传
 &emsp;&emsp;Python程序的文件名通常以.py结尾，很容易识别他们。当你使用其它Python编辑器写代码，保存一个程序时，Python会自动在文件名的末尾添加“.py”，一般你不需要手动输入。
  &emsp;&emsp;而在我们Paracraft软件中，Python代码是保存在Python代码方块里面的，所以你只需要保存好你的世界，那么你的代码都会自动保存下来。保存并上传世界的方法如下：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4833/raw#image.png'
  ext: png
  filename: image.png
  size: '144911'
  unit: '%'
  percent: 100

```


### **5.总结与分享（5‘）**
 *  老师总结（思维导图）
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10538/raw#1583740121312我的第一个Python程序.png
  ext: png
  filename: 1583740121312我的第一个Python程序.png
  size: 501505
          
```

 
 
 




 


 *  学生总结分享
 
 
 






















