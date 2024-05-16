
<style>
  .markdown-body hr {
    height: 1px;
  }
</style>



```@Lesson
styleID: 0
lesson:
  animations: []
  updated: '2020/04/17 18:14:47'

```


# **一、	教学目标：**
1.知识目标：
* 学习Python的基础语法：判断语句、运算符

2.能力素养：
* 在编程的过程中，对运行中发现的问题进行代码调试，培养独立思考和解决问题的能力

3.思维提升：
* 通过项目练习，训练学生的数学运用能力，感受编程的严谨性和创造性。

# **二、	教学重难点：**

### 教学重点：
* 学习Python的基础语法：判断语句、运算符
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
&emsp;&emsp;小朋友们，我们每天都需要做出各种各样的判断。例如，“今天会不会下雨？”，“今天妈妈会不会带我去游乐园玩？”，“我的作业都做完了么？”，“我是谁？我来自哪里？我将要去何方？”，人们每天都会做各种各样的判断和决定，计算机也会通过回答问题来做出决断，下面就让我们一起学习一下程序中的判断语句吧！

### **2.知识点解析（25‘）**
* 判断语句介绍：
&emsp;（1）生活中的判断场景
&emsp;&emsp;①地铁站过安检（判断乘客是否携带易燃易爆危险品）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10650/raw#1583975148983image.png
  ext: png
  filename: 1583975148983image.png
  size: 588577
          
```

 

&emsp;&emsp;②刷抖音APP会提示相关设置（APP使用人自行判断应该开启哪一种模式）：
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10652/raw#1583975326342image.png
  ext: png
  filename: 1583975326342image.png
  size: '297490'
  unit: '%'
  percent: 45

```

&emsp;&emsp;③密码判断（密码正确才能进门）
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10654/raw#1583976032876image.png
  ext: png
  filename: 1583976032876image.png
  size: '1630559'
  unit: '%'
  percent: 100

```


&emsp;&emsp;④小结：
&emsp;&emsp;&emsp;&emsp;如果某些条件满足，才能做某件事情；条件不满足时，则不能做，这就是所谓的判断。
 

* if判断语句：
&emsp;不仅生活中有，在计算机程序中"判断"功能也经常会用到。计算机提出的问题经常是把一个东西和另外一个东西作比较。比如5大于3么？如果是，就执行一组指令，如果不是就跳过或者执行另外一组指令。
 &emsp;（1）If判断语句的基本格式如下:

 ```python
 #格式

if 要判断的条件:
        条件成立时，要做的事情


```


```python
#例子1
age = 30
print("------if判断开始------")

if age >= 18:
  print("我已经成年了")
  
print("------if判断结束------")


运行结果:
------if判断开始------
        我已经成年了
------if判断结束------

```


```python
#例子2
age = 16
print("------if判断开始------")

if age >= 18:
  print("我已经成年了")

print("------if判断结束------")

运行结果:
   ------if判断开始------

   ------if判断结束------
    
```

&emsp;（2）小结
&emsp;&emsp;以上2个例子仅仅是age变量的值不一样，导致结果却不同；
&emsp;&emsp;能够看得出if判断语句的作用：就是当满足一定条件时才会执行代码块语句，否则就不执行代码块语句。
&emsp;&emsp;注意：代码的缩进为一个tab键，或者4个空格；
&emsp;&emsp;思考：判断age大于或者等于18岁使用的是 >=，如果是其他判断，还有哪些呢？

 </br>

* 运算符：
（1）python中的比较运算符如下表：
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10665/raw#1583981398905image.png
  ext: png
  filename: 1583981398905image.png
  size: 123261
          
```
&emsp;&emsp;前面我们学过Python3的数据类型，表格中的“Ture”、“False”就是布尔类型。如果一个语句使用了运算符对变量和数值进行比较，那么它总是会给出一个布尔值：Ture或者False，注意它们必须以大写字母开头。

 ```python
#例子

num1 = 18
num2 = 30

# == 等于：表示左右两个操作数是否相等，如果相等则整个表达式的值为 True；不相等则为False
print(num1 == num2)  
结果为：
   False
    
# != 不等于
print(num1 != num2)
结果为：
  True

# > 大于
print(num1 > num2)
结果为：
  False

# < 小于
print(num1 < num2)
结果为：
  True

# >= 大于等于: num1 大于 或者 等于 num2 ，条件都成立
print(num1 >= num2)
结果为：
  False

# <= 小于等于： num1 小于 或者 等于 num2 ，条件都成立
print(num1 <= num2)
结果为：
  True

  
   ```



&emsp;（2）python中的逻辑运算符如下表：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10656/raw#1583979285455image.png
  ext: png
  filename: 1583979285455image.png
  size: 60266
          
```

&emsp;&emsp;有时候我们的比较判断不止一个，可能有多个，这时候我们可以用and和or把多个比较判断连接起来。如果使用and，只有两边的比较都是真，整个判断才会是真。如果使用or，只要有一边的判断是真，整个判断就是真。
 ```python
#例子

# and : 左右表达式都为True，整个表达式结果才为 True
if (1 == 1) and (2 > 1):
    print("条件成立！")
结果为：
    条件成立！


# or : 左右表达式有一个为True，整个表达式结果就为 True
if (1 == 2) or (2 > 1):
    print("条件成立！")
结果为：
    条件成立！
    

# not：将右边表达式的逻辑结果取反，Ture变为False，False变为True
if not (1 == 2):
    print("条件成立！")
结果为：
    条件成立！
    
  
   ```
   
 </br>
 
* if-else语句格式：
思考：在使用if的时候，它只能做到满足条件时要做的事情。那万一需要在不满足条件的时候，做某些事，该怎么办呢？
答：使用 if-else。
（1）if-else的使用格式：
 ```python
 
if 条件:
        满足条件时要做的事情1
        满足条件时要做的事情2
        满足条件时要做的事情3
        ...(省略)...
else:
        不满足条件时要做的事情1
        不满足条件时要做的事情2
        不满足条件时要做的事情3
        ...(省略)...
    
  
   ```
   
   
 ```python
 
#例子

chePiao = 1 # 用1代表有车票，0代表没有车票
if chePiao == 1:
    print("有车票，可以上火车")
    print("放假啦，终于可以回家吃到妈妈做的饭，美滋滋~~~")
else:
    print("没有车票，不能上车")
    print("妈妈，今年不回家过年了，买不到车票，呜呜~~~"）
    
    
结果1：（有车票的情况）

    有车票，可以上火车
    放假啦，终于可以回家吃到妈妈做的饭，美滋滋~~~
    
结果2：（没有车票的情况）

    没有车票，不能上车
    妈妈，今年不回家过年了，买不到车票，呜呜~~~


 
   ```
* if...elif...else...语句格式：
通过刚才的学习，我们知道：
（1）if能完成当xxx时做事情；
（2）if-else能完成当xxx时做事情1，否则做事情2；
    思考：如果有这样一种情况：当xxx1满足时做事情1；当xxx1不满足、xxx2满足时做事情2；当xxx1不满足、xxx2不满足、xxx3满足时做事情3，那该怎么实现呢？

&emsp;&emsp;答:elif。

&emsp;（1）elif的使用格式：

```python
if xxx1:
    事情1
elif xxx2:
    事情2
elif xxx3:
    事情3
    
说明:
    当xxx1满足时，执行事情1，然后整个if结束
    当xxx1不满足时，那么判断xxx2，如果xxx2满足，则执行事情2，然后整个if结束
    当xxx1不满足时，xxx2也不满足，如果xxx3满足，则执行事情3，然后整个if结束

   
#例子
score = 88
if score>=90 and score<=100:
    print('本次考试，等级为A')
elif score>=80 and score<90:
    print('本次考试，等级为B')
elif score>=70 and score<80:
    print('本次考试，等级为C')
elif score>=60 and score<70:
    print('本次考试，等级为D')
elif score>=0 and score<60:
    print('本次考试，等级为E')

结果为：
    本次考试，等级为B
    
 
 ```
&emsp;（2）可以和else一起使用：

```python

if 性别为男性:
    输出男性的体重
    
elif 性别为女性:
    输出女性的体重
       
else:
    第三种性别的体重
 
说明:
    当 “性别为男性” 满足时，执行 “输出男性的体重”的相关代码；
    当 “性别为男性” 不满足时，如果 “性别为女性”满足，则执行 “输出女性的体重”的相关代码；
    当 “性别为男性” 不满足，“性别为女性”也不满足，那么就默认执行else后面的代码，即 “第三种性别的体重”相关代码；
    elif必须和if一起使用，否则出错；
    else 一般用在最后，即所有条件都不满足时使用；


 ```


* if嵌套（了解）：
通过学习if的基本用法，已经知道了：
（1）当需要满足条件去做事情的这种情况需要使用if；
（2）当满足条件时做事情A，不满足条件做事情B的这种情况使用if-else；
思考：坐火车或者地铁的实际情况是：先进行安检如果安检通过才会判断是否有车票，或者是先检查是否有车票之后才会进行安检，即实际的情况某个判断是再另外一个判断成立的基础上进行的，这样的情况该怎样解决呢？
答：if嵌套。

（1）if嵌套的格式：
```python

if 条件1:
    满足条件1 做的事情1
    满足条件1 做的事情2
    if 条件2:
         满足条件2 做的事情1
         满足条件2 做的事情2
说明：
    外层的if判断，也可以是if-else
    内层的if判断，也可以是if-else
    根据实际开发的情况，进行选择


```

```python

#例子

chePiao = 1     # 用1代表有车票，0代表没有车票
daoLenght = 9    # 刀子的长度，单位为cm

if chePiao == 1:
    print("有车票，可以进站")
    if daoLenght < 10:
        print("通过安检")
        print("放假啦，终于可以回家吃到妈妈做的饭，美滋滋~~~")
    else:
        print("没有通过安检")
        print("刀子的长度超过规定，等待警察处理...")
else:
    print("没有车票，不能进站")
    print("妈妈，今年不回家过年了，买不到车票，呜呜~~~")
    


结果1：chePiao = 1;daoLenght = 9

    有车票，可以进站
    通过安检
    放假啦，终于可以回家吃到妈妈做的饭，美滋滋~~~
    
结果2：chePiao = 1;daoLenght = 20

    有车票，可以进站
    没有通过安检
    刀子的长度超过规定，等待警察处理...
    
结果3：chePiao = 0;daoLenght = 9

    没有车票，不能进站
    妈妈，今年不回家过年了，买不到车票，呜呜~~~
    
结果4：chePiao = 0;daoLenght = 20

    没有车票，不能进站
    妈妈，今年不回家过年了，买不到车票，呜呜~~~
    
思考：为什么结果3和结果4相同？？？
答：因为都没有车票，程序只执行else部分的语句。


```














 
### **3.思维导图（10‘）**
&emsp; &emsp;下面运用我们所学知识完成一个小项目吧！
 *  项目分析：
 需求：从键盘获取自己的年龄，判断是否大于或者等于18岁，如果满足就输出“哥，你已成年，可以去网吧上网啦！”
 分析：
  （1）使用input从键盘中获取数据，并且存入到一个变量中；
  （2）使用if语句，来判断 age >= 18是否成立；
  （3）在脚本区窗口中，输入下面这行文字。
  
```python

#input()返回一个字符串，所以需要使用float()方法将字符串转换为数字，才能进行数学运算
age = float( input("请输入你的年龄："))
if age >= 18:
    print("哥，你已成年，可以去网吧上网啦！")
   
   ```
   
   
&emsp;&emsp;（4）假设输入20，点击上方的“编辑并运行”，程序输出结果如下：
  
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10669/raw#1583985354354999.gif
  ext: gif
  filename: 1583985354354999.gif
  size: 232290
          
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
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2FPython%E5%9F%BA%E7%A1%80%E8%AF%AD%E6%B3%95%EF%BC%88%E4%BA%8C%EF%BC%89.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2FPython%E5%9F%BA%E7%A1%80%E8%AF%AD%E6%B3%95%EF%BC%88%E4%BA%8C%EF%BC%89.svg

```



### **4.实操演练与拓展（40’）**
* 练习一：
要求：从键盘输入身高，使用if-else判断，如果身高没有超过150cm，则进动物园不用买票，否则需要买票。

```python

height = float(input("请输入你的身高："))
if height < 150:
    print("你还小，不用买票，可以进动物园啦")
else:
    print("你长大啦，需要买票才可以进动物园哦")
  
  
```

* 练习二：
要求:从键盘输入数字，使用if-elif-else语句判断数字是正数、负数或零。


```Python

num = float(input("输入一个数字:"))
if num > 0:
    print("正数")
elif num == 0:
    print("零")
else:
    print("负数")


```

* 练习三：
要求:从键盘输入数字，判断是奇数还是偶数。


```Python
#int()函数可以将字符串转换为整数，进行数学运算
#如果是偶数除于 2 余数为 0
#如果余数为1，则为奇数
num = int(input("输入一个数字:"))
if (num % 2) == 0:
    print("输入的是偶数")
else:
    print("输入的是奇数")


```


* 练习四（可作为课后作业）：
要求：从键盘输入年份，判断该年份是闰年还是平年。
提示：
    （1）公元年分除以4不可整除，为平年；
    （2）公元年分除以4可整除但除以100不可整除，为闰年；
    （3）公元年分除以100可整除但除以400不可整除，为平年；
    （4）公元年分除以400可整除，为闰年。
 
```Python
#方法一：
year = int(input("输入一个年份："))
if (year % 4) == 0:
   if (year % 100) == 0:
       if (year % 400) == 0:
           print("%d是闰年" % year)   # 整百年能被400整除的是闰年
       else:
           print("%d不是闰年" % year)
   else:
       print("%d是闰年" % year)       # 非整百年能被4整除的为闰年
else:
   print("%d不是闰年" % year)


#方法二：
year = int(input("输入一个年份："))
if(year % 4 ==0 and year %100 != 0) or (year % 400 == 0):   
    print ("%d是闰年" % year)
else:
    print ("%d不是闰年" % year)


#方法三
...


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
    https://api.keepwork.com/storage/v0/siteFiles/10679/raw#1583997259124Python基础语法（二）.png
  ext: png
  filename: 1583997259124Python基础语法（二）.png
  size: 693864
          
```

 


 *  学生总结分享
 
 
 