
<style>
  .markdown-body hr {
    height: 1px;
  }
</style>





```@Lesson
styleID: 0
lesson:
  animations: []
  updated: '2020/04/17 18:14:24'

```


# **一、	教学目标：**
1.知识目标：
* 学习Python的基础语法：注释、变量及其类型、运算符、标识符和关键字、输入

2.能力素养：
* 在编程的过程中，对运行中发现的问题进行代码调试，培养独立思考和解决问题的能力

3.思维提升：
* 通过项目练习，训练学生的数学运用能力，感受编程的严谨性和创造性。

# **二、	教学重难点：**

### 教学重点：
* 熟悉Python基础语法 ：注释、变量及其类型、运算符、标识符和关键字、输入
* 灵活应用所学知识解决实际问题

### 教学难点：
* 灵活运用所学知识解决实际问题

# **三、	教学准备：**
* 课件（**项目id：**）
* 带鼠标、键盘的电脑
* 上课学员的账号、密码
* 顺畅的网络环境


# **四、	教学过程：**
### **1.	情景引入（10‘）：**
&emsp;&emsp;小朋友们请列举一下你家都有哪些家电？（冰箱、电视节、洗衣机等）那么，大家都会使用这些家电设备么？无论是家电设备还是小玩具，当我们购买一样商品时候，厂家都会在商品上或者包装里附带一样东西给我们，来指导我们怎么使用这款产品，这个东西叫啥?（说明书）对了，就是说明书。说明书的作用就在于指导我们正确使用相关产品的。既然产品有说明书，那么，在我们的程序中有没有“说明书”来指导我们理解程序中的相关信息呢？有的，那就是程序中的【注释】指令，下面我们一起学习一下程序中的【注释】指令吧。

### **2.知识点解析（25‘）**
* 注释
&emsp;（1）注释的引入
&emsp;&emsp;①看下图程序示例（未使用注释）：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10570/raw#1583819456872image.png
  ext: png
  filename: 1583819456872image.png
  size: '15727'
  unit: '%'
  percent: 80

```

&emsp;&emsp;②看下图程序示例（使用注释）：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10569/raw#1583819406314image.png
  ext: png
  filename: 1583819406314image.png
  size: '51502'
  unit: '%'
  percent: 80

```

&emsp;&emsp;③小总结（注释的概念和作用）：
&emsp;&emsp;注释：在程序代码中对程序代码进行解释说明的文字。
&emsp;&emsp;作用：注释不是程序，不能被执行，只是对程序代码进行解释说明，让别人可以看懂程序代码的作用，能够大大增强程序的可读性。
 
&emsp;（2）注释的分类
&emsp;&emsp;①单行注释：
&emsp;&emsp;以#开头，#右边的所有文字当作说明，而不是真正要执行的程序，起辅助说明作用。
   ```python
   
   # 我是注释，可以在里写一些功能说明之类的哦
   print("Hello World!")
   
   
   ```
&emsp;&emsp;②多行注释：
&emsp;&emsp;多行注释用三个单引号 ''' 或者三个双引号 """ 将注释括起来，例如:
&emsp;&emsp;*单引号（'''）


```python

'''
这是多行注释，用三个单引号
这是多行注释，用三个单引号 
这是多行注释，用三个单引号
'''
print("Hello, World!")
```
&emsp;&emsp;*双引号（"""）

```python

"""
这是多行注释，用三个双引号
这是多行注释，用三个双引号 
这是多行注释，用三个双引号
"""
print("Hello, World!")


 ```


 
* 变量及其类型
 &emsp;（1）变量的定义
 &emsp;&emsp;在程序中，有时我们需要对2个数据进行求和，那么该怎样做呢？我们类比一下现实生活中，比如去超市买东西，往往咱们需要一个菜篮子，用来进行存储物品，等到所有的物品都购买完成后，在收银台进行结账即可。
&emsp;&emsp;如果在程序中，需要把2个数据，或者多个数据进行求和的话，那么就需要把这些数据先存储起来，然后把它们累加起来即可。
&emsp;&emsp;在Python中，存储一个数据，需要一个叫做变量的东西，如下示例:

 ```python

num1 = 100 #num1就是一个变量，就好比是一个小菜篮子

num2 = 86  #num2也是一个变量

result = num1 + num2 #把num1和num2这两个"菜篮子"中的数据进行累加，然后放到 result变量中


```

&emsp;&emsp;从示例中，我们可以看出：
&emsp;&emsp;①所谓变量，可以理解为菜篮子，如果需要存储多个数据，最简单的方式是有多个变量，当然了也可以使用一个；
&emsp;&emsp;②程序就是用来处理数据的，而变量就是用来存储数据的；
&emsp;&emsp;③Python 中的变量不需要声明，每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建；
&emsp;&emsp;④等号（=）用来给变量赋值；
&emsp;&emsp;⑤等号（=）运算符左边是一个变量名,等号（=）运算符右边是存储在变量中的值；


&emsp;（2）变量的类型
&emsp;&emsp;想一想：我们应该让变量占用多大的空间，保存什么样的数据？
&emsp;&emsp;生活中“类型”的例子：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10571/raw#1583825157077image.png
  ext: png
  filename: 1583825157077image.png
  size: '247230'
  unit: '%'
  percent: 80

```

&emsp;&emsp;小朋友们，图片中哪个盒子占的空间最大？（红色盒子）没错，就是红色盒子占的空间最大。
&emsp;&emsp;所以同样都是盒子，但是类型会不一样，会有大小的区别。那么在程序中，为了更充分的利用内存空间以及更有效率的管理内存，变量也是有不同的类型的哦，在Python3 中，数据类型如下所示:
  
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10646/raw#1583913267263数据类型.png
  ext: png
  filename: 1583913267263数据类型.png
  size: 231477
          
```


&emsp;&emsp;在Python3中数据类型有很多，本节课我们学习int（整型）和float（浮点型），其它数据类型我们将在后面的课程一一进行学习。
&emsp;&emsp;int（整型）：整数被称为“integers”（整型数），比如：1，2，3，8，9；
&emsp;&emsp;float（浮点数）：包含小数点的数字被称为“float”（浮点数），比如：0.5，5.20，8.88；
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10603/raw#1583899309572image.png
  ext: png
  filename: 1583899309572image.png
  size: '408295'
  unit: '%'
  percent: 60

```

 
 
 
* 运算符
python支持以下几种运算符：
&emsp;&emsp;(1) 算术运算符
&emsp;&emsp;变量可以用来存放数字和计算。变量和运算符号可以一起使用，进行数学计算，方法和你在数学课上所学的一样。有的运算符看上去非常熟悉，但你要小心乘法和除法运算符，它们和你在课堂上学的稍有不同。
&emsp;&emsp;下面以a=10 ,b=20为例进行计算：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10607/raw#1583906437083image.png
  ext: png
  filename: 1583906437083image.png
  size: 60183
          
```


&emsp;&emsp;(2) 赋值运算符
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10608/raw#1583906685578image.png
  ext: png
  filename: 1583906685578image.png
  size: 33023
          
```

 ```python

# 单个变量赋值
num = 10
print(num)

 ```
&emsp;&emsp;结果为：10


 ```python
 
# 多个变量赋值
num1, num2, f1, str1 = 10, 20, 3.14, "hello world"
print(num1, num2, f1, str1)


 ```
&emsp;&emsp;结果为：10 20 3.14 hello world


&emsp;&emsp;(3)复合赋值运算符（了解）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10609/raw#1583908852672image.png
  ext: png
  filename: 1583908852672image.png
  size: 104993
          
```


* 标识符和关键字
 &emsp;（1）标识符
 &emsp;&emsp;什么是标识符？看下图：
 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10577/raw#1583829344217image.png
  ext: png
  filename: 1583829344217image.png
  size: '244770'
  unit: '%'
  percent: 80

```
&emsp;&emsp;小朋友，你能说出这张图的意思么？（挖掘机哪家强，中国山东找蓝翔）
&emsp;&emsp;总结：标识符就是自己定义的，如变量名 、函数名等，开发人员在程序中自定义的一些符号和名称也是标识符。

 &emsp;（2）标识符的规则
 &emsp;&emsp;①标识符由字母、下划线和数字组成，且数字不能开头。
 &emsp;&emsp;②如下符号不允许使用：-、/、#、@
 &emsp;&emsp;③不允许使用空格
 &emsp;&emsp;④要区分大写和小写字母，比如“Paracraft”和“paracraft”是两个不同的变量
 &emsp;&emsp;⑤避免使用Python中的关键词（关键词就是python已经使用的了，不允许开发者自己定义和关键字相同的名字的具有特殊功能的标识符），比如“print”、“class”、“import”等，更多关键词，我们会在后面的课程中一一进行学习。 
&emsp;&emsp;思考：下面的标识符哪些是正确的，哪些不正确，为什么？
&emsp;&emsp;&emsp;&emsp;Paracraft123       正确
&emsp;&emsp;&emsp;&emsp;Paracraft#123      不正确
&emsp;&emsp;&emsp;&emsp;Love-Paracraft     不正确
&emsp;&emsp;&emsp;&emsp;Love_Paracraft     正确
&emsp;&emsp;&emsp;&emsp;520_Paracraft      不正确
&emsp;&emsp;&emsp;&emsp;Paracraft520       正确
&emsp;&emsp;&emsp;&emsp;_test            正确
&emsp;&emsp;&emsp;&emsp;_test@123         不正确
&emsp;&emsp;&emsp;&emsp;print           不正确
&emsp;&emsp;&emsp;&emsp;int/123         不正确 
   
  
 * 输出print()
 （1）print的格式化输出：
 &emsp;&emsp;上节课我们简单学习了print()函数，写出了我们的第一个程序。现在老师有这样一个需求，比如以下这段代码：
 ```python
pirnt("我今年9岁")
pirnt("我今年10岁")
pirnt("我今年11岁")
    ...
   
 思考：在输出年龄的时候，用了多次"我今年xx岁"，能否简化一下程序呢？？？  
 答：字符串格式化输出。
 那么，什么是格式化？看如下代码:

age = 9
print("我今年%d岁" % age)

age += 1
print("我今年%d岁" % age)

age += 1
print("我今年%d岁" % age)

...

在程序中，看到了%这样的操作符，这就是Python中格式化输出。

#例子
age = 18
name = "qizai"
print("我的姓名是%s, 年龄是%d" % (name, age))
   
   ```
   
&emsp;&emsp;（2）常用的格式符号：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10734/raw#1584077156287image.png
  ext: png
  filename: 1584077156287image.png
  size: '89642'
  unit: '%'
  percent: 80

```


 
 
 * 输入input()
 &emsp;&emsp;小朋友们，我们去银行ATM机取钱时，肯定需要输入密码，对不对？那么怎样才能让程序知道咱们刚刚输入的是什么呢？？
&emsp;&emsp;大家应该知道了，如果要完成ATM机取钱这件事情，首先需要从键盘中输入一个数据，然后用一个变量来保存，程序只要读取到这个变量，就能知道刚才输入的是什么信息啦，是不是很好理解呢
&emsp;&emsp;在Python中，获取键盘输入的数据的方法是采用 input()函数（至于什么是函数，咱们以后的章节中讲解），那么这个input()怎么用呢?看如下示例:
 ```python

password = input("请输入密码:")
print("您刚刚输入的密码是:%d" % password)
   
   
   ```
&emsp;&emsp;运行结果:
 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10736/raw#1584078617820输入密码.gif
  ext: gif
  filename: 1584078617820输入密码.gif
  size: 223074
          
```



&emsp;&emsp;注意：
&emsp;&emsp;input()的小括号中放入的是，提示信息，用来在获取数据之前给用户的一个简单提示；
&emsp;&emsp;input()在从键盘获取了数据以后，会存放到等号右边的变量中；
&emsp;&emsp;input()会把用户输入的任何值都作为字符串来对待。
 


### **3.思维导图（10‘）**
&emsp; &emsp;下面运用我们所学知识完成一个小项目吧！
 *  项目分析：
 需求：编写一个程序，通过用户输入三角形三边长度，并计算三角形的面积。
 （1）要实现获取用户输入数据，我们使用input()函数，并定义变量用来存储用户输入的数据，在脚本区窗口中，输入下面这行文字。
```python

#input()返回一个字符串，所以需要使用float()方法将字符串转换为数字，才能进行数学运算
a = float( input("输入三角形第一边长："))
b = float(input("输入三角形第二边长："))
c = float(input("输入三角形第三边长："))
#计算半周长（海伦公式）
s = (a + b + c) / 2
#计算面积
area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
#在终端区显示三角形面积，0.2f表示：浮点型数据，只保留前两位小数。
print("三角形面积为：%0.2f" % area)
   
   ```
   
   
   &emsp;&emsp;（2）假设输入的边长分别为：3、4、5，点击上方的“编辑并运行”，程序输出结果如下：
  
 
   
 

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10735/raw#1584078404833三角形面积计算.gif
  ext: gif
  filename: 1584078404833三角形面积计算.gif
  size: 420932
          
```


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
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2FPython%E5%9F%BA%E7%A1%80%E8%AF%AD%E6%B3%95%EF%BC%88%E4%B8%80%EF%BC%89.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2FPython%E5%9F%BA%E7%A1%80%E8%AF%AD%E6%B3%95%EF%BC%88%E4%B8%80%EF%BC%89.svg

```



### **4.实操演练与拓展（40’）**
* 练习一：
要求：编写一个程序，打印一首诗，并用注释标明诗歌的诗名，作者、所属朝代等信息。
```python
  
  
'''
    下面的代码完成打印一首诗。
    诗名：《小池》
    作者：杨万里
    朝代：宋
'''

print('╔═╤═╤═╤═╤═╤═╗')
print('║　│　│　│　│　│　║')
print('║　│泉│树│小│早│　║')
print('║　│眼│阴│荷│有│  ║')
print('║小│无│照│才│蜻│  ║')
print('║　│声│水│露│蜓│  ║')
print('║池│惜│爱│尖│立│  ║')
print('║  │细│晴│尖│上│  ║')
print('║  │流│柔│角│头│  ║')
print('║　│，│。│，│。│　║')
print('║　│　│　│　│　│　║')
print('╚═╧═╧═╧═╧═╧═╝')
  
```

* 练习二：
要求：编写一个程序，计算圆的面积。


```Python

r = float(input("请输入圆的半径："))
#定义圆周率（Pi）的值
Pi = 3.14
#计算面积
area = Pi * (r * r)
#在终端区显示圆面积，小数点保留2位：
print("圆的面积为：%0.2f" % area)

```

* 练习三：
要求：妈妈去超市买了8.00斤苹果，苹果单价是8.88元／⽄，请编写程序计算一下妈妈需要支付多少钱？
 
 
```Python

price = float(input("请输入苹果的单价："))
weight = float(input("请输入苹果的重量："))

#计算总价格=单价*重量
money = price * weight

#在终端区显示内容，小数点保留2位
print("妈妈需要支付：%0.2f 元" % money)


```
     


        
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
    https://api.keepwork.com/storage/v0/siteFiles/10737/raw#1584078897677Python基础语法（一）.png
  ext: png
  filename: 1584078897677Python基础语法（一）.png
  size: 1150784
          
```



 


 *  学生总结分享
 
 
 






















