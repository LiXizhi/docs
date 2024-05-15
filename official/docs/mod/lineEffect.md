# 爆炸特效模组

## 介绍
爆炸特效低代码模组。这个模组旨在帮助您快速从电影方块中的演员创建活动模型，并对应电影方块中的位置，以线形特效展开、还原。通过这个模组，您可以做一些复杂模型的拆解展示，如火箭模型各个部件的拆解。

## 下载模板
从资源商城（快捷键E）选择模板并使用。
右边方块是模板功能代码，左边是例子。启用爆炸特效模组功能只需要激活右边的方块，右边的开关默认打开。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35996/raw#1712889383044image.png
  ext: png
  filename: 1712889383044image.png
  size: 199096
  isNew: true
          
```



## 基本用法
1. 创建 -> 爆炸
点开左边代码方块，运行后可以看到创建了若干活动模型，并沿Z轴线形移动展开。 点开电影方块可以看到，这些活动模型都是从电影方块中的模型拷贝出来的。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35997/raw#1712889623086image.png
  ext: png
  filename: 1712889623086image.png
  size: 461415
  isNew: true
          
```
2. 复原
   图块“从爆炸位置回到原点”，可反向的展示特效。从散开排列的模型回到初始状态（电影方块中的位置排列）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35998/raw#1712889905152image.png
  ext: png
  filename: 1712889905152image.png
  size: 558132
  isNew: true
          
```


## 示例和高级用法

爆炸特效支持配置参数，如爆炸位置，方向（x或z），模型间距等。
`注意！！`为确保配置生效，请将配置代码语句放在“从电影方块创建特效模型之前”
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35999/raw#1712890382100image.png
  ext: png
  filename: 1712890382100image.png
  size: 465841
  isNew: true
          
```



## 常见问题解答
Q  为什么配置不生效？
A  需要将所有配置的语句图块放在最前（或确保放在“从电影方块创建特效模型之前”）才可生效

## 支持与反馈
835273072@qq.com


## 结尾
感谢您使用爆炸特效低代码模组


