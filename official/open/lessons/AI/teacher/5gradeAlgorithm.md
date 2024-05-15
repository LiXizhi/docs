# 教材章节案例：体验算法控制

信息科技5年级, 2022浙教版

## 你将学习

1. 用关键信息分析问题。
2. 综合应用算法控制结构解决生活问题。

## :dart: 讨论

火车站进站时凭身份证检票、办公楼宇通过刷指纹进出大门、购物支持刷脸支付、登录学习平台需要验证身份……这些应用的背后蕴含着怎样的算法结构？
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34704/raw#1703950907057image.png
  ext: png
  filename: 1703950907057image.png
  size: 144385
  isNew: true
          
```

## 建构
用算法解决问题首先需要从问题中提取关键信息，进而分析问题、设计算法、验证算法。计算机根据人们设定的算法自动执行并输出结果。

### 一 分析问题
根据问题中的关键信息来分析需要解决的问题。比如购买火车票的问题，根据乘车人的年龄特征来区分是否需要购买车票；如果需要购买车票，还可以根据“是否满 14 周岁”这个特征来区分购买全票还是优惠票。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34705/raw#1703951025034image.png
  ext: png
  filename: 1703951025034image.png
  size: 23273
  isNew: true
          
```
### :dart: 想一想

> 在购买火车票的过程中有哪些关键信息？这些关键信息和购票的结果有什么关联？

如果要用计算机来实现“购票”的过程，就需要设计合适的算法。

### 二 设计算法 

设计算法时，通常把一些复杂的问题根据关键信息分成几个小问题，再将每个小问题的解决过程用流程图表示，最后完成整个算法的设计。比如，购买火车票的问题可以使用如下顺序结构：

- 步骤 1：选择起点、终点。
- 步骤 2：选择时间、车次。
- 步骤 3：输入乘车人信息。
- 步骤 4：确定车票类型。
- 步骤 5：支付票额并出票。

“确定车票类型”这个步骤可以使用分支结构，用如下流程图来表示。
```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2Fticket.svg

```
### 三 验证算法

根据算法流程图，在计算机中编写代码并运行，对设计的算法进行验证。如“确定车票类型”这个算法，可以编写以下程序代码进行验证。


```@Project
styleID: 1
project:
  projectId: '2098864'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
```@CodeBlock
styleID: 0
codeblock:
  projectId: '2098864'
  title: ticketCode
  name: ticketCode
  language: codeblock
  code: |-
    say('点我咨询购票');
    registerClickEvent(function()
        nianling = tonumber(ask('请输入您的年龄：'));
        if (nianling < 6) then
            say('免票');
        else
            if (nianling < 14) then
                say('优惠票');
            else
                say('全价票');
            end
        end
    end)
  outputMode: autoParacraft
  output: >
    2024-01-02 09:32:07 5941|main|warn|Entity:SetSkin|skin files does not exist
    80001;84089;81005;88020;85109;83202
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: false

```

### :dart: 想一想

> 用分支结构解决“确定车票类型”的算法中，编写的程序代码是否与算法流程图一一对应？

## 练习

根据本课的算法流程图，尝试画出先判断“14 周岁及以上”这一条件的算法流程图。

---

## 参考
- [浙教版2022信息科技5上](https://api.keepwork.com/ts-storage/siteFiles/34753/raw#1704159351949信息科技5上.pdf) 

### 提出基于相似原理的数字课程设计模型

基于相似原理，知识的本质是思维对动画的控制力，或者叫`重要体验`。针对新课标，我们可以分成下面5个步骤去设计数字课程。

1. 寻找生活中的相似情景
2. 定义1-2个重要体验：重要体验一般由动画片段（记忆）和对动画的控制力(思维)构成的。我们需要寻找或制作能清晰表达重要体验的短动画。
3. 设计课堂动手实验：心理学研究表明，当学生有肢体行为时，更容易形成重要体验。因此，我们要设计在课堂上让学生动手的实验，目标是帮助学生形成重要体验。 
4. 课后继续迭代：基于课堂项目，鼓励学生课后继续动手迭代项目。
5. 通过翻转课堂获得反馈：提供让学生展示个人作品的场所。 
```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2FPBL.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fopen/files/official%2Fopen%2F_config%2Fboard%2FPBL.svg

```
其中

- 针对2：我们制作了500个针对3-9年级的2022新课标的3D动画和虚拟仿真实验。 
- 针对3：我们提供了基于可计算文档的在数字教材中直接进行3D虚拟仿真和动手实验的工具，让老师可以成为教材的创造者，让学生可以自由探索并创造属于自己的作品，形成重要体验。

参考数字教材章节案例： [https://keepwork.com/official/open/lessons/AI/teacher/5gradeAlgorithm](https://keepwork.com/official/open/lessons/AI/teacher/5gradeAlgorithm)