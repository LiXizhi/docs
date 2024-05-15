# 视频播放模组


## 更新
1.1 加入了关闭视频图块和关闭视频窗口的回调
1.2 加入3D视频播放图块
1.3 支持图片 + mp4 URL。 场景中可以支持播放多个不同的视频但同时只能播放1个视频。（播放当前视频时其它视频会自动暂停，并显示相应图片）。详细见示例4

## 介绍
视频播放低代码模组，用于在客户端内播放外部链接视频


## 下载模板
打开资源商城（快捷键R） -> 代码区 -> 视频播放模组
单击下载模组并放置在场景中即可使用。右边的方块是模板功能代码，左边是例子。启用模板功能只需要激活右边的方块，右边的开关默认打开。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30275/raw#1698220115250image.png
  ext: png
  filename: 1698220115250image.png
  size: 506419
  isNew: true
  isExpand: true
          
```



## 基本用法

输入视频（MP4文件）链接后运行即可播放。也可以选择添加视频标题
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29886/raw#1695368970453image.png
  ext: png
  filename: 1695368970453image.png
  size: 798078
  isNew: true
          
```


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29887/raw#1695369043807image.png
  ext: png
  filename: 1695369043807image.png
  size: 783096
  isNew: true
          
```


## 示例和高级用法
1. 图块“关闭视频”可以由用户配置，用来在指定的时候关闭视频窗口
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30276/raw#1698220211101image.png
  ext: png
  filename: 1698220211101image.png
  size: 46271
  isNew: true
  isExpand: true
          
```

2. 图块“视频关闭后”是回调函数，也可以由用户配置
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30277/raw#1698220242300image.png
  ext: png
  filename: 1698220242300image.png
  size: 48829
  isNew: true
  isExpand: true
          
```

3. 播放3D视频
首先打开背包（E键）新建一个相册（id 218）作为视频播放容器
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35427/raw#1709100795261image.png
  ext: png
  filename: 1709100795261image.png
  size: 125324
  isNew: true
          
```
可以添加多个相册，扩大播放容器
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35428/raw#1709100879968image.png
  ext: png
  filename: 1709100879968image.png
  size: 249618
  isNew: true
          
```

 在相册第一格右键点击打开 输入_textureDynamicDefault;0 0 300 200
 其中300为宽 200为高
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35429/raw#1709100947651image.png
  ext: png
  filename: 1709100947651image.png
  size: 660020
  isNew: true
          
```

 

拖拽图块“播放3D视频”输入长宽，点击运行即可在相册容器上播放视频
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35426/raw#1709100663248image.png
  ext: png
  filename: 1709100663248image.png
  size: 49108
  isNew: true
```

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35430/raw#1709101140262image.png
  ext: png
  filename: 1709101140262image.png
  size: 245206
  isNew: true
          
```

4. 播放3D视频(同世界播放多个)
   执行图块“创建视频活动模型”将自动创建一个视频板模型，可由用户放在场景中任意位置。默认显示封面图片，点击可播放视频。注意视频比例固定4：3，视频链接必须配置，封面可以不配置，默认显示黑底白字的封面图。
   场景中可以支持播放多个不同的视频但同时只能播放1个视频。（播放当前视频时其它视频会自动暂停，并显示相应图片）
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/36000/raw#1712890841813image.png
  ext: png
  filename: 1712890841813image.png
  size: 713107
  isNew: true
          
```



## 结尾
感谢您使用视频播放低代码模组