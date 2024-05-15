# 全屏选择题模组

## 更新
v1.1 完善功能，可自定义样式
v1.2 显示优化，被右上角按钮遮挡画面
v1.3 加入多选题功能，配置正确选项大于1个时，自动变为多选题。多选题需要手动点击提交。

## 介绍
低代码全屏选择题模组。此模板用于快速搭建选择题，只需输入题目与4个选项（至少2个选项，至少一个正确选项），问题与选项可支持图片，可由用户自定义风格

## 下载模板
从资源商城选择模板并使用。
右边三个方块是模板功能代码，左边是一些例子。启用选择题模板功能只需要激活右边的三个方块，右边的开关默认打开。
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33322/raw#1701076534864image.png
  ext: png
  filename: 1701076534864image.png
  size: 797798
  isNew: true
  isExpand: true
          
```



## 基本用法
模板左边默认预设了三组例子，打开左边的代码方块可以看到功能图块。
下面的示例是一种简单用法，配置题目和答案，图片填入了外部链接，也可以将图片放入世界中。选项的顺序会自动被打乱。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33324/raw#1701076708265image.png
  ext: png
  filename: 1701076708265image.png
  size: 358764
  isNew: true
  isExpand: true
          
```

用户点击选项后会自动判断对错，并于3秒后关闭窗口（默认3秒，可修改），如
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33325/raw#1701076823429image.png
  ext: png
  filename: 1701076823429image.png
  size: 551716
  isNew: true
  isExpand: true
          
```



## 示例和高级用法

### 自定义样式
可以看到左边除题目和答案外，还有许多其他图块，这表示选择题可配置的属性
下面的例子展示了自定义界面的颜色
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33326/raw#1701076945024image.png
  ext: png
  filename: 1701076945024image.png
  size: 126262
  isNew: true
  isExpand: true
          
```

### 连续答题
通过回调函数可以配置连续答题的功能，参加示例三。或[选择题题模组文档说明](https://keepwork.com/official/docs/mod/choice)
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/33327/raw#1701077090906image.png
  ext: png
  filename: 1701077090906image.png
  size: 159277
  isNew: true
  isExpand: true
          
```

## 常见问题解答
Q  回调"答题正确时""答题结束时"的区别？
A  "答题正确时"是在用户点击选项后触发的，"答题结束时"是在点击选项后，等待相应时间，并关闭窗口后触发的。 前者不会打断后者，为避免出错跳转到下一题的代码应写在"答题结束时"回调中。

## 支持与反馈

835273072@qq.com


## 结尾
感谢您使用全屏选择题低代码模组
