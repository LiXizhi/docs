# 虚拟仿真课程制作入门

## 什么是帕拉卡？(10分钟)
帕拉卡Paracraft是一款面向老师和学生的3D虚拟现实创作工具。
- 帕拉卡是完全中国**自主原创**和开源的工具，对标unity等专业3D引擎。
- 内置3D建模、3D动画、沉浸式编程与调试、CAD建模、虚拟仿真、GIT云端版本控制、多人协作等功能。
- 可以研发从**青少年个人编程项目**到百万行代码的**大型商业化APP**。


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/24456/raw#1668601345209image.png
  ext: png
  filename: 1668601345209image.png
  size: 301380
          
```

### 下载安装Paracraft
推荐使用Paracraft社区版(家庭版)。:heart: [点击这里下载](https://paracraft.cn)

### 如何自学Paracraft
- 成人用户可阅读我们的:heart:[官方文档](https://keepwork.com/official/docs/index), 观看里面的新手教学视频。
- 如果你希望培7-14岁的孩子一起学习，可以[报名线上培训班](https://papa.palaka.cn/download)。

### 使用帕拉卡可以做出什么作品？

你可以发布如下类型的作品：
- 在浏览器或微信上直接运行的[Web3D网页:《深圳荔园小学》](https://webparacraft.keepwork.com/?pid=23540)
- PC/Android/iOS等[独立APP:《圣诞树》](https://keepwork.com/official/paralife/app/christmastree)
- 在VR设备上可播放的[360度全景视频:《画展》](https://www.bilibili.com/video/BV1BG4y1k711/)或立体电影

:heart:这里有[更多技术演示](https://keepwork.com/official/open/showcase/index)

## 基于可计算文档的虚拟仿真课程介绍 (10分钟)

- 过去的教材课件是**静态的，没有反馈的，不可编辑的**。 
- 过去的虚拟仿真是**非线性的，缺少说明，不可搜索和难以编辑的**。 

有没有一种数字教材的形式可以同时具备
1. 文本的易于阅读、编辑、搜索、总结的特性
2. 虚拟仿真的沉浸式、操作性、和强交互的特性

:dart:答案是`可计算文档`。

可计算文档原型是jupyter notebook。我们将WPS文档和Paracraft的元宇宙技术通过互联网浏览器结合起来，从而让原本静态的文档成为了可以运算的计算机程序。我们可以利用可计算文档制作出面向各个年龄段的数字教材和交互课件；提供教、学、练、测、评为一体的以文档为中心的互联网数字资源。

- 案例：[深圳人工智能数字丛书](https://keepwork.com/official/open/lessons/AI/index)
   - 可以看第1/3/4学段的第一课: 人工智能概述。 

## 从0开始制作一个课件 (30分钟)

### 准备工作
1. 下载并注册paracraft账号。
2. 登录[keepwork.com](https://keepwork.com)可计算文档的编辑器
3. 创建个人网站、选择页面布局、建立多人编辑权限。

### 开始制作课程
- 添加文字、标题、**加粗**、`高亮`
> 重点提示
- 添加[超链接](#), 代码
- 上传并添加自制图片
- 上传并添加自制视频，添加B站和腾讯视频
- 添加可折叠部件
- 使用表情`:smile:`:smile::dart::point_right::heart:
- 使用绘图板

### 添加第一个可计算模块
- AI对话模块

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: AI
  code: 介绍一下智慧农场
  outputMode: autoParacraft
  output: >-
    智慧农场是一种以物联网为基础，通过物联化、互联化、智能化的方式，综合无线传感技术、自动控制技术、网络技术和数据库技术实现现代化、智能化管理的农场。它可以通过云计算、5G、物联网等技术，部署于农业生产现场的各种传感节点和通信网络，实现农业生产环境的智能感知、智能预警、智能决策、智能分析等功能。在这个过程中，学生可以参与农业发展知识讲述、农业生产技术展示和农业科技动手体验，从而对传统农业和未来农业产生初步的理解和浓厚的兴趣。
  output_image: ''

```

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: AI
  code: 概括它的主要特点， 每行50字
  outputMode: autoParacraft
  output: |-
    智慧农场的主要特点包括：

    1. 智能感知：通过传感器和物联网技术，实现对农业生产环境的实时监测和数据采集。
    2. 智能预警：通过对数据的分析，及时发现异常情况并发出预警，减少损失。
    3. 智能决策：通过云计算和人工智能技术，实现自动化决策，提高农业生产效率。
    4. 智能分析：通过对农业生产数据的分析，发现规律和趋势，为决策提供数据支持。
    5. 参与性强：可以让学生参与农业发展知识讲述、农业生产技术展示和农业科技动手体验，增强对传统农业和未来农业的理解和兴趣。
  output_image: ''

```

### 添加第一个虚拟仿真世界
- 先打开paracraft, 创建一个人新世界
- 制作世界内容
   - 添加代码和电影方块
- 分享世界并添加到文档中

### 添加第一个低代码模组
- 填空题模组

### 录制一个宏示教
- 录制宏示教
- 在文档中引用宏示教

### 用文档驱动虚拟世界
- 文档中添加codeblock，并与世界中的代码方块关联起来
- 改变codeblock中的文档参数
- 运行，并在虚拟世界中观看结果
- 制作包含多个步骤的交互讲解

### 制作动手练习题目
- 用代码判断是否正确

---
:dart: 参考项目：自己动手做出下面的项目

## 智慧农场