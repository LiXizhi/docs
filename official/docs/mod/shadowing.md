# 跟我读模板

## 介绍

跟我读低代码模组，快速搭建用户跟读练习（支持英文/中文）

影子跟读法（shadowing）
用户可播放原声->跟读->听自己的发音
学习者能够即时听到自己的发音，从而更容易发现并纠正发音或语调上的错误。通过反复跟读，学习者能够逐渐提高对于目标语言的听力理解能力。通过模仿母语者的语调和语音，学习者能够更自然地使用目标语言，避免一些显著的外语口音。影子跟读法有助于提高口语的流利度，因为学习者在模仿时会逐渐形成更自然的语音流。反复跟读可以帮助学习者养成正确的语音、语调和强调习惯，从而更容易在实际交流中运用这些语言元素。

## 下载模板
打开资源商城（快捷键R） -> 代码区 -> 跟我读低代模组
单击下载模组并放置在场景中即可使用。右边的方块是模板功能代码，左边是例子。启用模板功能只需要激活右边的方块，右边的开关默认打开。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32926/raw#1700201459079image.png
  ext: png
  filename: 1700201459079image.png
  size: 259005
  isNew: true
  isExpand: true
          
```


## 基本用法
下面是一种基础用法，拖拽图块配置一组“跟读文字”“提示文字”。点击左边按钮激活例子代码方块，即可看到跟读练习的界面。
进入跟读练习后，点击“原声”可以播放原文，点击“录音”可以跟读。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32928/raw#1700202313888image.png
  ext: png
  filename: 1700202313888image.png
  size: 524523
  isNew: true
  isExpand: true
          
```

跟读录音结束后会自动评分，共有perfect、great、good三种评分。计算方式：正确率perfect（70%以上）、great（40%以上）、good（其他）
并且错误的字会标红，正确的标绿。
此时点播放可以听到自己的发音，点击重录可以重新读
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32929/raw#1700202570480image.png
  ext: png
  filename: 1700202570480image.png
  size: 337585
  isNew: true
  isExpand: true
          
```


 

## 示例和高级用法
下面展示了多组跟读的用法（古诗 中文）
如果配置的跟读数据有2组或以上，则会显示翻页的UI，以及结算页（结算评分取平均分）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32934/raw#1700202855566image.png
  ext: png
  filename: 1700202855566image.png
  size: 557410
  isNew: true
  isExpand: true
          
```

结算页：
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32935/raw#1700203028815image.png
  ext: png
  filename: 1700203028815image.png
  size: 228948
  isNew: true
  isExpand: true
          
```


每组跟读会有一张配图，用户可以自行配置，方法是在图块加入“配置图片”，选择本地图片。图片比例为`3：4`
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32937/raw#1700203232564image.png
  ext: png
  filename: 1700203232564image.png
  size: 74053
  isNew: true
  isExpand: true
          
```


即可显示自定义图片，如不配置会显示默认图片
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29794/raw#1695027994423image.png
  ext: png
  filename: 1695027994423image.png
  size: 297938
  isNew: true
          
```

### 获取数据
回调"关闭跟读窗口后" 当跟读结束后关闭结算窗口（单组跟读是关闭当前窗口），此函数会被调用
结束后可以按需要获取数据
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29888/raw#1695371825619image.png
  ext: png
  filename: 1695371825619image.png
  size: 667590
  isNew: true
          
```

## 常见问题解答

Q 如何修改样式属性？
A 图块“属性”区域，放置了一些可配置样式和属性的图块，可根据需求自行修改。

## 支持与反馈
835273072@qq.com


## 结尾
感谢您使用跟我读低代码模组