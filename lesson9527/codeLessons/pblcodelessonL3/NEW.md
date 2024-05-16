
<style>
  .markdown-body hr {
    height: 1px;
  }
</style>





```@Lesson
styleID: 0
lesson:
  animations: []

```


# 一、	教学目标：
### 1.知识与技能目标：
* 学习XXX指令的用法及规则；
* 学习XXXX指令的用法及规则。

### 2.编程实践目标：
* 利用XXXXX指令、循环指令、移动指令与旋转指令完成“播种的季节”项目程序。

### 3.思维与价值观目标：
* 让学生对农事活动有基本的认识，锻炼学生的逻辑思维能力，令学生理解简化程序与一题多解的思想。 

# 二、	教学重难点：

### 教学重点：
* XXXX指令四个参数的含义；
* XXXX指令实现有限次循环的作用——简化程序。
### 教学难点：
* XXXX指令简化程序的内在逻辑。


# 三、	教学准备：
### 1、教师端：
* 电脑1台，麦克风1个
* 网络编程环境检查与测试（包括软/硬件、网络、投影仪等）
* 课程PPT
* 本课素材包
* 其他教学辅助资料：如拓展视频、图片、实体教具等

### 2、学生端：
* 电脑1台	
* 声音设备
* 网络编程环境检查与测试（包括软/硬件、网络）
* 其他学习辅助资料：如学生手册等


# 四、重点功能与指令解析
	
		
```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2Ftest.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/lesson9527%2FcodeLessons/files/lesson9527%2FcodeLessons%2F_config%2Fboard%2Ftest.svg

```


# 五、教学流程表

|  时间节点   | 内容  | 教具  |
|  --------  | --------  | --------  |
| 00:00-10:00  | 课前导入 | 学生手册 |
| 10:00-50:00  | 编程实现+教师讲解+互动穿插 | ppt+其他教学资料 |
| 50:00-80:00  | 自主创作与知识拓展 | ppt |
| 80:00-90:00  | 课程总结+展示 | ppt |



# 六、教学步骤

## 第1环节：课前导入（10分钟）

### 1、课前导入
* 通过上节课作品，回顾旋转指令的用法。
xxxxx
* 通过跨学科知识点导入。
xxxxx

### 2、本课要点
   老师展示本节课的要点的思维导图，让学生了解本节课需要掌握的核心要点内容。
 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21005/raw#1629277432114image.png
  ext: png
  filename: 1629277432114image.png
  size: 61515
          
```


## 第2环节：编程实现（40分钟）

### 挑战1：帮助奇仔实现种植要求--在直线花圃里每格都种上小树苗


 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21000/raw#1629276495317image.png
  ext: png
  filename: 1629276495317image.png
  size: '582019'
  unit: '%'
  percent: 60

```

### 1、数一下总共需要种植多少树苗？
>>老师可以引导学生，通过按下Ctrl使用鼠标选取起始点与终点并查看选中方块数 

### 2、角色移动
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21001/raw#1629276800241image.png
  ext: png
  filename: 1629276800241image.png
  size: '15455'
  unit: '%'
  percent: 30

```


### 3、在第一个位置上种植树苗
#### 小树苗的方块ID是119，我们可以通过放置方块119来营造种植小树苗的效果，使用功能区感知模块的积木【放置方块（）（）（）（）】，前面三个空格中我们填入需要放置方块的位置坐标x、y、z，最后一个空格中我们填入放置的方块的ID，例如我们想要在坐标为（0,0，0）的位置放置草块（ID为62），即使用“放置方块0,0,0,62”。
>>教学建议：老师指引学生通过放置方块来营造“种树”的效果，引出感知模块中的【放置方块（）（）（）（）】，并详细讲解四个参数的含义，通过不断测试来让学生明白四个参数分别是放置的x坐标、y坐标、z坐标和方块ID。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21002/raw#1629276839798image.png
  ext: png
  filename: 1629276839798image.png
  size: '20271'
  unit: '%'
  percent: 30

```

### 4、如何确定奇仔移动后的坐标？

使用运动模块中的的【x坐标】、【y坐标】、【z坐标】积木能够表示当前奇仔的坐标（实时坐标）.因此使用就可以在奇仔当前位置放置一个小树苗。

>>教学建议：老师演示【x坐标】、【y坐标】、【z坐标】三个积木的具体含义，它们能够获取角色的实时坐标数值。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21003/raw#1629277016150image.png
  ext: png
  filename: 1629277016150image.png
  size: '19106'
  unit: '%'
  percent: 40

```

### 挑战2：围着花圃种植一圈小树苗

 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21006/raw#1629277801384image.png
  ext: png
  filename: 1629277801384image.png
  size: 529743
          
```





## 第3环节：自主创作与知识拓展（30分钟）

### 1、自主创作：帮助奇仔把花圃种满小树苗吧
  
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21007/raw#1629278007611image.png
  ext: png
  filename: 1629278007611image.png
  size: '585469'
  unit: '%'
  percent: 30

```



### 2、知识拓展：除了小树苗，我们还可以种点什么其他东西呢？
>>教学建议：学生操作时间可能较久，可以根据实际情况选择是否进行拓展。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21009/raw#1629279533096image.png
  ext: png
  filename: 1629279533096image.png
  size: '540200'
  unit: '%'
  percent: 60

```

## 第4环节：课程总结与展示（10分钟）

### 1、学生作品展示
教师从班级中挑选2-3名优秀学生上台进行作品介绍。教师可以从以下几个方面引导学生展示的内容：
设计的思路、作品的闪光点等等
搭建作品过程中遇到了哪些问题？是如何解决的？
总结课堂内容（从以下方面总结，仅供参考）
  （1）对于【瞬移到___】指令，你可以用它来实现你的哪些想法呢？（头脑风暴）
>> 教学建议：可以视课堂进展情况及课堂时间，灵活安排是否需要进行学生作品展示，此部分意在锻炼学生的语言表达能力。

### 2、教师答疑解惑，学生交流分享
（1）学生自由提问，老师回答学生问题，解决学生的疑惑。
（2）学生之间通过访问项目ID互相查看作品。

# 七、教学反思
老师们上完课后，对本节课进行总结和反思。需要以下内容：
1、学生对于知识点的接受程度，哪些学生理解得不够好？哪些学生需要重点关注？
2、学生对于哪些知识点理解比较困难？
3、上课遇到哪些异常情况，怎么处理的？处理是否及时妥当？










