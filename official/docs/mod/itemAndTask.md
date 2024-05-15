# 物品与任务模组

## 介绍
物品与任务低代码模组。这个模组旨在帮助您快速而灵活地配置任务系统，从而简化任务的添加、修改、检查和分数计算过程。通过这个模组，您可以将任务条件直观地关联到玩家的背包中的物品，使得任务的完成与否直接依赖于玩家背包中是否拥有特定的物品。

## 下载模板
从资源商城选择模板并使用。
右边三个方块是模板功能代码，左边是一些例子。启用物品与任务模组功能只需要激活右边的三个方块，右边的开关默认打开。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35294/raw#1706523327572image.png
  ext: png
  filename: 1706523327572image.png
  size: 285225
  isNew: true
          
```


## 基本用法
以下是一个简单例子，表示添加了一个名为“任务一”的任务到系统任务列表中。并显示任务窗口。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35299/raw#1706582020556image.png
  ext: png
  filename: 1706582020556image.png
  size: 77344
  isNew: true
          
```

点击运行后，此任务就被添加到待办任务列表中。此时左上角也显示了任务界面。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35300/raw#1706582378998image.png
  ext: png
  filename: 1706582378998image.png
  size: 80792
  isNew: true
          
```
此任务配置了时间，需要注意如果配置了时间，结束时间不能早于当前时间（服务器时间）。也就是说，不可以添加已过期的任务。
任务添加完毕之后，即可发送获得物品的广播事件，事件名为`ItemAndTask.obtainItem`，参数为物品的名字，如：`物品1`。数量默认为1。
获得物品也可直接调用图块“获得物品”，2种方式效果相同。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35301/raw#1706582674753image.png
  ext: png
  filename: 1706582674753image.png
  size: 29740
  isNew: true
          
```


执行“获得物品”的操作后，如果通过验证（验证详细规则见后文），物品将会放入背包中。
多次发送广播（或调用图块），物品将叠加放在背包内。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35302/raw#1706582707680image.png
  ext: png
  filename: 1706582707680image.png
  size: 28692
  isNew: true
          
```

现在用相同方法添加一个`物品2`。


## 示例和高级用法

图块“显示任务窗口”可以在左上角显示一个界面。可选择是否折叠
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35296/raw#1706523828230image.png
  ext: png
  filename: 1706523828230image.png
  size: 60600
  isNew: true
          
```



## 常见问题解答
Q  
A  

## 支持与反馈

835273072@qq.com


## 结尾
感谢您使用物品与任务低代码模组
