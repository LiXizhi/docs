## 创建课程

Keepwork课程系统通过[智慧教育云平台](https://edu.palaka.cn)提供了创建课程的功能，大家可以用它为自己的作品制作课程包，分享出来，供他人学习。 创建课程包分为以下3个步骤：

- 新建课程
- 制作课程网页
- 发布课程

**1 新建课程**

一个课程是多个keepwork网页的集合。首先，点击keepwork导航栏的**个人头像**，然后点击**我的课程**，开始创建属于自己的课程。点击 “**创建自定义课程**”按钮，在“课程编辑”页面，设置课程的基本信息，包括名称、封面图、简介等。

![1710653171075image.png](https://api.keepwork.com/ts-storage/siteFiles/35645/raw)

**2 制作课程网页**

每节课的内容是以网页（可计算文档）的形式进行呈现的，Keepwork提供了免费的文档和网页编辑工具。

关于网站编辑器的基本操作，[制作个人网站](https://keepwork.com/official/docs/UserGuide/share/personalsite)。
在编辑器中，创建这个课程的网页。首先需要为所有课程网页新建一个网站，再在网站下建立网页。

编辑网页内容，这里我们编辑课程网页的内容并复制网页的URL到课程编辑页面。
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3080/raw#课程网页.png'
  ext: png
  filename: 课程网页.png
  size: '252831'
  unit: px
  width: 500
  alignment: left

```
这里，先把课程内容分成了4个部分：理论、游戏、测试、分享和讨论

先在“理论”中，输入一段文本，并插入一个视频。

在 “游戏”中，将自己制作的项目作品添加进入，使用“项目”模块来完成。输入世界作品的项目ID就可以了。
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3081/raw#项目模块.png'
  ext: png
  filename: 项目模块.png
  size: '315547'
  unit: px
  width: 500
  alignment: left

```

在“测试”部分，添加测试题，需要使用问题模块。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35648/raw#1710653998232image.png
  ext: png
  filename: 1710653998232image.png
  size: 78539
  isNew: true
          
```
测试题提供了5种题型供选择，单选题、多选题、判断题、文本匹配题和代码API（支持大语言模型自动评价）。
单选、多选、判断题，都可以算作选择题。需设置题干内容、选项内容、正确答案、题目分值和答案解析。
文本匹配题，主要是为了锻炼学生的代码书写熟练度的，所以会把答案文本附上，并提供了输入多个答案文本的可能性。

**3 发布课程**

如果你的账号属于一个学校或机构，并且为老师身份，则课包对机构内的学生默认可见，如果希望对所有人可见，则需要提交官方审核。对于发布的课包，开发者可以设置价格（即将上线）。

你可以将整个网站设置为私有，然后让有权限的用户通过智慧教育云平台访问你的课程。

> 注意：如果你的网站是公开的，那么所有获得了课程连接的用户将都能访问网页。

## 测评与作业批改

如果网页中增加了测评模组，可以在课程编辑页面勾选**展示测评**， 勾选后将展示作业测评入口。

老师可以直接点击测评入口，以班级为单位进行作业的批改和点评，支持大语言模型辅助批改。

![1710653284792image.png](https://api.keepwork.com/ts-storage/siteFiles/35646/raw)

老师身份点击后，会跳到作业批改页面。 可以选择班级，并看到班级的答题情况，选择学生或题目可以对题目进行点评，支持AI自动点评。学生在访问自己的课程页面时可以看到所有老师的评价，也可以直接在评论区和老师互动。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35647/raw#1710653788382image.png
  ext: png
  filename: 1710653788382image.png
  size: 103395
  isNew: true
          
```