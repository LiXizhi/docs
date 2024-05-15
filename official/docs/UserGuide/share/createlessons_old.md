
## 创建课程

Keepwork课程系统通过[智慧教育云平台](https://edu.palaka.cn)提供了创建课程的功能，大家可以用它为自己的作品制作课程包，分享出来，供他人学习。如果你的账号属于一个学校或机构，并且为老师身份，则课包对机构内的学生可见，如果希望对所有人可见，则需要提交审核。 创建课程包分为以下3个步骤：

- 新建课程
- 制作课程网页
- 发布课程

**1 新建课程**

一个课程是多个keepwork网页的集合。首先，点击keepwork导航栏的**个人头像**，然后点击**我的课程**，开始创建属于自己的课程。点击 “**创建自定义课程**”按钮，在“课程编辑”页面，设置课程的基本信息，包括名称、封面图、简介等。

**2 制作课程网页**

每节课的内容是以网页（可计算文档）的形式进行呈现的，Keepwork提供了免费的文档和网页编辑工具。

关于网站编辑器的基本操作，[制作个人网站](https://keepwork.com/official/docs/UserGuide/share/personalsite)。
在编辑器中，创建这个课程的网页。首先需要为所有课程网页新建一个网站，再在网站下建立网页。

编辑网页内容，这里我们编辑课程网页的内容，先添加一个课程模块，并把这个课程网页与之前我们创建的课程关联起来，表示课程的网页内容就是这个网页了。
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3078/raw#课程模块.png'
  ext: png
  filename: 课程模块.png
  size: '57666'
  unit: px
  width: 500
  alignment: left

```

关联完毕后，编辑这个模块的信息。在新建课程时设置的课程基本信息也会同步显示过来，若在新建课程时未完成基本信息的设置，也可以在这里进行设置。

课程的主体内容，使用markdown文本模块来完成。可以在最左侧输入文本内容，也可以在最右侧输入。我们可以看到右侧上方提供了很多文本编辑工具，如标题字体设置、加粗、斜体、分割线、链接等等。我们可以利用这些文本编辑工具，设置课程内容。

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

在 “游戏”中，将自己制作的游戏作品添加进入，使用“项目”模块来完成。输入游戏作品的项目ID就可以了。

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
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3082/raw#问题模块.png'
  ext: png
  filename: 问题模块.png
  size: '79951'
  unit: px
  width: 500
  alignment: left

```

测试题提供了4种题型供选择，单选题、多选题、判断题、文本匹配题。
单选、多选、判断题，都可以算作选择题。需设置题干内容、选项内容、正确答案、题目分值和答案解析。
文本匹配题，主要是为了锻炼学生的代码书写熟练度的，所以会把答案文本附上，并提供了输入多个答案文本的可能性。

测试题设置好后，允许再次修改和通过拖动模块的方式调整题目顺序。

另外，在课程内容中，我们可能需要添加一个对老师的提示，方便老师运用这个课程教学时可以更高效，并且，我们又不希望学生看到这些提示内容。“提示”模块，就可以完美解决这个问题，只需输入提示内容，系统会自动根据身份显示或隐藏这些内容。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3083/raw#提示模块.png'
  ext: png
  filename: 提示模块.png
  size: '329110'
  unit: px
  width: 500
  alignment: left

```

**3 将课程加入课程包** 

课程编辑好后，需要把课程加入课程包。
先新建一个课程包，设置课程包的基本信息：科目、年龄（就是这个课程包适合哪个年龄段的人学习，可以选择所有人群，也可以自定义年龄段）、课程包名称、简介，封面图等。
基本信息编辑好后，再选择目录，在这里添加课程。点击“添加课程”按钮，将创建好的课程加入课程包。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3084/raw#将课程加入课程包.png'
  ext: png
  filename: 将课程加入课程包.png
  size: '133133'
  unit: px
  width: 500
  alignment: left

```

上图所示，就是该课程包下的课程目录了。使用“删除”按钮，可以将这个课程从课程包移除；使用“上下移动”按钮，可以调整课程的顺序，拖动课程即可。

**4 分享课程包**

未审核通过的课程包是只能创建者本人使用的，如果想要把自己创建的课程包分享到Keepwork课程系统，供他人使用，可以使用“提交”功能，将课程包提交审核。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3085/raw#提交审核.png'
  ext: png
  filename: 提交审核.png
  size: '79231'
  unit: px
  width: 500
  alignment: left

```

系统会在5个工作日反馈审核结果。待课程包审核通过后，平台上所有用户都可以使用这个课程包学习、讲课了。