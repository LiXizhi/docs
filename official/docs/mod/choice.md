# 选择题模组

## 更新
v1.1 修改了例子中的错误
v1.2 加入朗读题目功能。新增图块"是否朗读题目"，"朗读播音员"
v1.3 加入新的样式“彩色二（纵向选项）”，选项支持更长文字

## 介绍
低代码选择题模组。此模板用于快速搭建选择题，只需输入题目与4个选择（1个正确，3个错误），可由用户自定义风格

## 下载模板
从资源商城选择模板并使用。
右边三个方块是模板功能代码，左边是一些例子。启用选择题模板功能只需要激活右边的三个方块，右边的开关默认打开。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30377/raw#1698653425338image.png
  ext: png
  filename: 1698653425338image.png
  size: 960782
  isNew: true
  isExpand: true
          
```


## 基本用法
模板左边默认预设了三组例子，打开左边的代码方块可以看到功能图块。
下面的示例是最简单的一种用法，只需配置题目和答案（包含1个正确，3个错误的），选项的顺序会自动被打乱。
### 例1
1+1 = ？
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28177/raw#1689315312357image.png
  ext: png
  filename: 1689315312357image.png
  size: 509317
  isNew: true
          
```

用户点击选项后会自动判断对错，并于3秒后关闭窗口（默认3秒，可修改），如
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28178/raw#1689315477910image.png
  ext: png
  filename: 1689315477910image.png
  size: 103467
  isNew: true
          
```


## 示例和高级用法
可以看到左边除题目和答案外，还有许多其他图块，这表示选择题可配置的属性

### 例2
下面的示例
1. 选择了另一种样式
2. 配置标题为“课后练习”
3. 加入倒计时，倒计时结束后将自动关闭窗口（如果用户配置了“答题结束时”回调函数，此时函数也将被执行）
4. 加入答题结束后等待1秒关闭窗口，在用户答题完毕后等待1秒关闭窗口

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28184/raw#1689316171776image.png
  ext: png
  filename: 1689316171776image.png
  size: 521493
  isNew: true
          
```

### 例3
下面的示例
加入了朗读题目配置，配置后会自动朗读，用户也可以点击重复lang'du
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30378/raw#1698654008123image.png
  ext: png
  filename: 1698654008123image.png
  size: 576117
  isNew: true
  isExpand: true
          
```



### 例4
回调函数
模板预设了三个回调，在高级类别下。分别是“答题结束时”、“答题正确时”、“答题错误时”。只要用户配置了这些函数，这些函数就会在相应的时刻被调用。
例如配置在 答题正确时 ，显示礼花特效。模板内置了两种不同的礼花特效
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28186/raw#1689316341262image.png
  ext: png
  filename: 1689316341262image.png
  size: 448019
  isNew: true
          
```


### 例5
模板内置的三种回调可以做许多事情，例如连续答题。
下面的例子是通过发送广播和接收广播来完成连续答题的操作，在第一题的回调中加入广播来启动第二题，依此类推。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28188/raw#1689316463191image.png
  ext: png
  filename: 1689316463191image.png
  size: 118581
  isNew: true
          
```

### 例6
或者更多题目，例如自定一个题目数据集合，将这些数据通关广播`myQuestions` 发送
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28191/raw#1689316645402image.png
  ext: png
  filename: 1689316645402image.png
  size: 451948
  isNew: true
          
```

在模板方块中接收此广播，利用答题结束回调来做遍历这些题目，完成连续答题的操作。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28192/raw#1689316704647image.png
  ext: png
  filename: 1689316704647image.png
  size: 817128
  isNew: true
          
```
### 例7 HTML题目

当用户需要在题目中加入图片时，可直接使用html标记语言，支持本地图片及在线图片
例子：
题目中加入html

```html
<img style="width:300px;height:150px;" src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"/>
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28221/raw#1689322627694image.png
  ext: png
  filename: 1689322627694image.png
  size: 589499
  isNew: true
          
```