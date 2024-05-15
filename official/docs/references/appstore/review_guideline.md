# 帕拉卡 App Store 审核指南

不管是开发新手，还是由经验丰富的程序员所组成的大型团队，我们都非常欢迎您为 Paracraft 开发 app，并希望能够帮助您了解我们的准则，以确保您的 app 能够快速通过审核流程。


## 简介

## 提交之前

- 项目ID：`123` 
- 项目目录名：`MyGame`  必须英文
- 项目名：`我的中文名`
- 世界类型：`128模板` 、2in1课程、超平坦、自然随机地形、空、并行世界
- 分类标签：`跑酷`、过山车、动画、解谜、单人游戏、射击、教学、多人游戏
- 预览图：`preview.jpg` 必须为世界目录下的文件，100KB左右， 提供截图 + url地址

https://api.keepwork.com/storage/v0/siteFiles/12720/raw#%E8%B1%A1%E5%BD%A2%E4%B9%8B%E7%BE%8E.jpg

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20729/raw#1624953380824image.png
  ext: png
  filename: 1624953380824image.png
  size: '119810'
  unit: px
  width: '300'
  alignment: left

```
> 个人推荐作品截图参考

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20735/raw#1624961255863image.png
  ext: png
  filename: 1624961255863image.png
  size: '138603'
  unit: px
  width: '300'
  alignment: left

```

> 128模板类的， 建议统一上面的截图模式：45图俯视图 + 中心主形象 （用来体现差异和特征的图标或文字）
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/20746/raw#1625016627928preview.jpg
  ext: jpg
  filename: 1625016627928preview.jpg
  size: '77213'
  unit: px
  width: '300'
  alignment: left

```

> 课程类或2in1世界的截图参考

---

## 1. 安全

## 2. 性能
是否可以流畅运行

- png图片是否长宽都为`2的N次方`，否则iOS无法显示。 jpg可以不是，但是建议长宽中`最长边`为`2的N次方`。
- png图片建议都用tinypng等工具压缩下，平均可以节省60%的空间。jpg也需要有损压缩。 
- 确定没有FBX， 都转成了x
- 确定所有bmax等， 没有引用绝对路径
- 确定代码里面没有while(true).  有的必须要添加角色或代码的感知半径
- 确保没有超过1024 pixel的图片。
- 一张32位的1024x1024x32/8=4MB贴图占用内存+显存=4MB以上。 场景中512以上的图不要超多10张。 
- 进程在win32下`占用内存在1GB以下`为佳, 峰值1.4GB为警戒线。32位操作系统或手机一般只有2GB可用内存。[点击看如何动态加载卸载场景资源]()


### 2.1 App 完成度

### 2.2 Beta 测试

### 2.3 准确的元数据
- preview.jpg 封面截图： 100KB左右， 16:9
- 年龄与用户群
- 中文或英文
- 包大小，推荐20MB以下。最好5MB。
- 目录名必须英文
- 项目名可为中文

### 2.4 硬件兼容性
- Windows/Mac/Android/iOS/Pad/2in1外接键盘

### 2.5 软件要求
- 是否默认开启ggs服务器. [点击看教程]()
- 最小可视距离：64-96米为好
- 是否依赖服务器物品系统: 目前需要单独申请
- 是否有第三方服务器：

## 3. 商务
- 会员与激活码的提供方式, [点击看教程]()
- 世界定价
- 是否外链
- 是否开源，并可以另存为
- 是否VIP世界, [点击看教程]()
- 是否机构

## 4. 设计
- 需要提供玩家进度存储 （可本地或依赖物品系统，[点击看教程]()）
- 是否可独立运行， 是否有依赖
- 是否有AI课程, [点击看教程]()
- 是否可离线访问， 运行过程中断网
- 自动加载和卸载的设计， 详见文档。

### 4.1 抄袭者

### 4.2 最低功能要求
- 开发时用的Paracraft版本号

### 4.3 重复 App

### 4.4 扩展
- 是否支持外接键盘输入
- 是否支持全触屏模式
- 是否支持多人聊天
- 是否需要额外的Agent模块和版本号：宏示教舞台，等, [点击看教程]()
- http外部贴图与美术资源

### 4.5 服务
- 客服连接

### 4.6 App 图标
一般如果单独发布Android/iOS, 需要提供128x128以及更高清的PNG Icon图片

### 4.7 通过帕拉卡登录

## 5 关于codeblock_mod的规范
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26774/raw#1684738007587image.png
  ext: png
  filename: 1684738007587image.png
  size: 62595
  unit: px
  width: '900'
  alignment: left
          
```

### 5.1 命名规则
供针对类库中的模板命名类型规则：
按钮功能父栏目以功能类型英文来命名，如button
下级子栏目以父栏目开头_来命名，如button_01

其中,字母统一全部小写。

### 5.2 类型设计
第一期上线的类型主要有：按钮类、对话框类、以及一个语文小游戏模板。
预计上线时间6月上旬第一版模块内容

### 5.3 用户使用指南
模板中内置通俗易懂的注释，用户一看就会。
具体参考：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26773/raw#1684737636394image.png
  ext: png
  filename: 1684737636394image.png
  size: 432134
  unit: px
  width: '900'
  alignment: left
          
```

### 5.4 用户体验模拟
##### 用户按R键调出商城资源库，点击交互模板按钮。如图：
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26822/raw#1684896843273image.png
  ext: png
  filename: 1684896843273image.png
  size: 656809
 
          
```
##### 在界面中点击想下载的模板类型。如图： 
 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26832/raw#1684901338932image.png
  ext: png
  filename: 1684901338932image.png
  size: 329068
          
```



##### 在场景中把下载好的模板放在场景中，第一次使用可以点击NPC查看用户指南：
 


 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26829/raw#1684900706833image.png
  ext: png
  filename: 1684900706833image.png
  size: 197152
          
```


 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26827/raw#1684900391681image.png
  ext: png
  filename: 1684900391681image.png
  size: 165832
          
```

 
 ##### 观看完用户指南后，我们打开对应的代码方块，根据注释来进行内容上的配置：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26825/raw#1684900079788image.png
  ext: png
  filename: 1684900079788image.png
  size: 137247

          
```




##### 最后，运行配置好的代码方块，看下实际效果：
   
   
   
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26826/raw#1684900151245image.png
  ext: png
  filename: 1684900151245image.png
  size: 424683
 
          
```


## 6. 法律
- 隐私
- 知识产权

---

## 提交之后

审核后，会出现在玩学课堂，锁定commit id。 


## 参考资料
- [apple review guidline](https://developer.apple.com/cn/app-store/review/guidelines/)