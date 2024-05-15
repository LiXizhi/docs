# 数字气象站

## 更新
v1.1 显示优化：加入了展示板和控制板的标题命名，控制板的图标最多可支持输入8个字。

## 介绍
低代码的数字气象站遥控界面。此模板用于快速配置气象站的数据，只需要配置相对应的变量和事件名称，点击运行后可以实时显示数值在面板上。

## 下载模板
从资源商城选择模板并使用。
右边三个方块是模板功能代码，左边是一些例子。启用选择题模板功能只需要激活右边的三个方块，右边的开关默认打开。
 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34635/raw#1703215220559image.png
  ext: png
  filename: 1703215220559image.png
  size: 190602
  isNew: true
          
```




## 基本用法
模板左边默认预设了左侧展示板数据配置，打开左边的代码方块可以看到功能图块。
### 展示板（左侧）用法
下图的示例是配置左侧展示板的用法。我们需要做的就是配置标题和相应的变量名。相应的变量名会通过查找当前世界中的全局变量名来进行实时数据展示。
如：

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34647/raw#1703224546339image.png
  ext: png
  filename: 1703224546339image.png
  size: 60601
  isNew: true
          
```

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34648/raw#1703224604323image.png
  ext: png
  filename: 1703224604323image.png
  size: 1438465
  isNew: true
          
```
### 展示板（底部）用法
“标题”的配置表示显示在按钮上的文字，目前支持输入最多8个文字。
“事件名”是指点击按钮时会发送广播来执行相应的操作。
所以，我们需要配置显示在按钮上的名字，以及相应的广播命名，如图：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34653/raw#1703228129410image.png
  ext: png
  filename: 1703228129410image.png
  size: 579928
  isNew: true
          
```

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34652/raw#1703228098902image.png
  ext: png
  filename: 1703228098902image.png
  size: 82600
  isNew: true
          
```


每次按下按钮(收到广播后)会去执行相应的操作。如图：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34651/raw#1703228062953image.png
  ext: png
  filename: 1703228062953image.png
  size: 89749
  isNew: true
          
```



### 注意事项
如图所示，使用该模组进行左侧展示板的配置时，需注意“显示展示板(左侧)”的图块需要放在左侧展示板的结尾，以及“显示展示板(底部)”的图块也需要放在底部展示板的结尾。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34649/raw#1703224763178image.png
  ext: png
  filename: 1703224763178image.png
  size: 256347
  isNew: true
          
```
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34650/raw#1703224789738image.png
  ext: png
  filename: 1703224789738image.png
  size: 221142
  isNew: true
          
```

## 支持与反馈

835273072@qq.com


## 结尾
感谢您使用数字气象站模组
