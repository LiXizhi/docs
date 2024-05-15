# keepwork编辑器 v1.0

**软件用途：** keepwork编辑器提供了一种基于markdown的全新网站制作方式。用户可以通过markdown制作编辑网页，同时也可以通过图形化的编辑器调整网页模块的参数。 
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** JavaScript
**开发完成时间：** 2018年8月1日
**发表日期：** 2018年8月1日
**技术特点：** 该产品在技术方面支持以下功能
- 一种基于markdown的全新网站制作方式
- 支持可视化与文本式网页编写
- 多文件编辑
- 自定义网页功能扩展模块
- 历史记录

**源代码行数**: 8万行  [点击这里查看](keepwork编辑器_code)

## 《keepwork编辑器》使用手册
### 制作个人网站 


Keepwork提供了一款免费的网站编辑工具，网站编辑器。大家可以使用它，创建自己的个人网站，展示自己的作品。

进入Keepwork网站（ https://keepwork.com），登录后，在顶部导航栏上，点击“工具”菜单展开，选择“网站编辑器”进入（如下方左图）。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3066/raw#进入编辑器和编辑器主页.png'
  ext: png
  filename: 进入编辑器和编辑器主页.png
  size: '234798'
  unit: px
  width: '600'
  alignment: left

```

进入网站编辑器后（如上方右图），左侧显示创建的网站和参与的网站，右侧，有一块区域采用图文的形式展示了网站编辑器的一些小技巧，大家可以观看了解一下。右下角，有一个“帮助”按钮，这是Keepwork的帮助中心，记录了很多关于编辑器使用和Keepwork使用的一些方法，可以根据需要进行查看。


**1 新建网站**

如下图，设定网站的访问地址

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3068/raw#设置访问地址.png'
  ext: png
  filename: 设置访问地址.png
  size: '104259'
  unit: px
  width: 500
  alignment: left

```

**2 设置网站的属性**

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3069/raw#网站设置.png'
  ext: png
  filename: 网站设置.png
  size: '63487'
  unit: px
  width: 500
  alignment: left

```

基本信息设置，如：网站名称、网站图标、网站介绍等

网站布局设置，可设置该网站下的所有页面都采用同一个布局方案，也可对某个页面的布局进行个性化设置。

网站样式设置，包含字体、字号、颜色等

网站权限设置，对网站的编辑权限和浏览权限进行设置，可以多人编辑一个网站。

**3 编辑网页内容**

**3.1 如何添加模块**

网站都是由很多网页搭建起来的，先编辑网站的index页面。网页是由很多小模块拼起来的，像堆积木一样，一个模块就是一个小积木。点击“添加模块”按钮，左侧出现了很多模块，有常用、导航、图形、文本、交互等各种类型。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3071/raw#模块.png'
  ext: png
  filename: 模块.png
  size: '60388'
  unit: px
  width: 500
  alignment: left

```

在index页面中，添加一个顶部导航，选中导航下的“页首导航”模块，这里提供了好几种不同的页首导航样式，

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3072/raw#分区.png'
  ext: png
  filename: 分区.png
  size: '74201'
  unit: px
  width: 500
  alignment: left

```

可以在左侧编辑模块属性，设置图标、主标题、副标题、菜单，也可以改变模块样式。我们在左侧编辑时，中间预览区会实时根据我们的输入进行呈现，所见即所得。最右侧代码区也是编辑区，这里支持代码呈现，可以使用Markdown代码编辑方式去编辑页面内容。（Markdown语法在下一部分详细讲解）

左侧属性编辑区，可以满足用户运用已有的模块样式，不需太多设计经验轻松制作漂亮的网页。
而对于有一定编程知识的程序员，也可以在右侧代码编辑区中直接编写代码实现页面的呈现。
大家可以根据自己的习惯选择喜欢的编辑方式。

这个页首导航编辑好后，再在下方添加其他模块，点击该模块下侧的 + ，从左侧选择模块，完成编辑。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3073/raw#个人网站.png'
  ext: png
  filename: 个人网站.png
  size: '475706'
  unit: px
  width: 500
  alignment: left

```

页面是以模块为单位从上至下布局，可以添加模块，选中某个模块，点击该模块上方或下方的+按钮，即表示在这个模块的上方或下方添加模块；可以删除模块，选择需要删除的模块，点击删除图标，即可删除该模块；也可以上下拖拽模块重新排序。

**3.2 MarkDown语法**
我们平时上网，看到的所有的网页都是采用HTML（Hyper Text MarkUp Language）超文本（Hyper Text）标记（MarkUp）语言(Language)写的。其中MarkUp中的Mark是一种特殊的标记，例如`<div>`。 这种标记主要用来告诉计算机如何去显示文字，例如文字的颜色，大小，位置等。由于这些标记的大量存在，使得HTML原始文本（源文件）非常不适合人类阅读，而且它有严格的语法，学习它比学习其它计算机语言可能还要复杂。 MarkDown是与HTML(MarkUp)相反的一种标记语言, 它是一种标记（Mark）被去掉（Down）了的语言，因此它非常适合人类阅读，基本和自然语言兼容。KeepWork中的所有网页都是用MarkDown语言来写的。 全世界所有的在线百科和大部分程序文档也都是使用markdown格式书写。 

Markdown是一种可以使用普通文本编辑器编写的标记语言，通过简单的标记语法，它可以使普通文本内容具有一定的格式。

Keepwork网站编辑器，代码区上方提供了很多文本编辑工具，这些就是markdown语法的快捷方式，在对markdown语法使用不熟练的时候，可以直接使用快捷工具进行属性设置，达到我们想要的内容展现效果。

同时，代码区也支持markdown语言的所有基础语法，这里，列举一些常用的markdown语法示例：

**3.2.1 标题**


<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2956/raw#标题.png)
  
</div>

显示标题语法：

```
## 标题2
### 标题3
###### 标题6
```
<div style="clear:both"></div>

**3.2.2 引用**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3239/raw#引用-new.png)
  
</div>

行首使用>加上一个空格表示引用段落，内部可以嵌套多个段落。语法：

```
>这里是一个引用
>>内部嵌套
```
<div style="clear:both"></div>

**3.2.3 列表**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2958/raw#无序列表.png)
  
</div>

无序列表语法：
```
* Item 1      + Item 1     - Item 1
* Item 2      + Item 2     - Item 2
* Item 3      + Item 3     - Item 3
```
<div style="clear:both"></div>

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2959/raw#有序列表.png)
  
</div>


有序列表语法：

```
1. Item 1
2. Item 2
3. Item 3
```
<div style="clear:both"></div>

**3.2.4 强调**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/2960/raw#强调.png)
  
</div>

强调语法：

```
*斜体* 或者 _斜体_
**加粗** 或者  __ 加粗__ ~~删除线~~
```
<div style="clear:both"></div>

**3.2.5 链接**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
 [链接1](wwww.baidu.com)
  
</div>

链接语法：

`[链接1](http://www.baidu.com “百度”)`
或者 `[链接2][ref]` 或者`[ref]:http://www.baidu.com`

<div style="clear:both"></div>

**3.2.6 代码**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
 ```lua
print("hello world")

```
  
</div>

代码语法：

\```lua

\```

<div style="clear:both"></div>

**3.2.7 图片**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3359/raw#钢琴.jpg)
  
</div>


图片语法：


`![Alt text](/path/to/img.jpg “图片文件名”)`
  

<div style="clear:both"></div>

**3.2.8 表格**

<div style="float:right;padding-left:20px;width:50%">
  
  效果：
  
  ![](https://api.keepwork.com/storage/v0/siteFiles/3240/raw#表格-new.png)
  
</div>

语法：

```
表头|表头|表头
---|:--:|---:
内容|内容|内容
内容|内容|内容
```

<div style="clear:both"></div>

**4 分享网站**

编辑完成，我们保存一下（支持Ctrl+S快捷方式保存）。然后，我们进入网站浏览一下，点击上方的url地址，在新窗口打开，这就是我们新建好的网站页面了。


```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3074/raw#个人网站预览.png'
  ext: png
  filename: 个人网站预览.png
  size: '457580'
  unit: px
  width: 500
  alignment: left

```


使用“分享”功能，可以把网站分享给好友观看；或者将网站url地址分享给好友，

以上就是网站编辑器的基本操作，大家可以运用这些操作技巧，搭建自己的个人网站。

### 创建课程




Keepwork课程系统提供了创建课程包的功能，大家可以用它为自己的作品制作课程包，分享出来，供他人学习。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3076/raw#课程管理.png'
  ext: png
  filename: 课程管理.png
  size: '97109'
  unit: px
  alignment: left
  width: 500

```

创建课程包分为以下4个步骤：新建课程、设置课程网页、将课程加入课程包、分享课程包。

**1 新建课程**


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3890/raw#创建课程001.mp4
  ext: mp4
  filename: 创建课程001.mp4
  size: 8276985
          
```


课程包是多个课程的集合，每个课程包下包含多个课程。
我们创建课程包，第一步需要新建课程。首先，选中 课程 菜单，点击 “新建课程”按钮，在“新建课程”页面，设置课程的基本信息，包括科目、名称、封面图等。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3077/raw#新建课程.png'
  ext: png
  filename: 新建课程.png
  size: '77931'
  unit: px
  width: 500
  alignment: left

```

**2 设置课程网页**


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3891/raw#创建课程002.mp4
  ext: mp4
  filename: 创建课程002.mp4
  size: 100827781
          
```


课程内容是以网页的形式进行呈现的，Keepwork提供了免费的网站编辑工具。 

关于网站编辑器的基本操作，详见 项目29x118：制作个人网站。
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


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3892/raw#创建课程003.mp4
  ext: mp4
  filename: 创建课程003.mp4
  size: 13837045
          
```


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


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3893/raw#创建课程004.mp4
  ext: mp4
  filename: 创建课程004.mp4
  size: 14318839
          
```


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
