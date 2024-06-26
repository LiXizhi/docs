# Paracraft虚拟仿真引擎项目建议书

## 项目概述

### 什么是帕拉卡Paracraft？
帕拉卡Paracraft是一款面向个人的3D虚拟现实创作工具。
- 帕拉卡是完全**自主原创**和开源的工具，对标unity等专业3D引擎。
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

### 1. 解决什么大行业和大问题（归类）
- 大类：面向个人的3D虚拟世界创作与仿真工具
- 小类：数字课件生产力工具，CAD建模与动画制作工具、人工智能仿真环境

### 2. 帕拉卡的优势
- 2-1 帕拉卡可以让用户创作任意复杂的3D动画和3D程序，非常适合开发生动的自主学习数字课件。
- 2-2 帕拉卡是完全自主知识产权的，用国产编程语言研发的虚拟现实创作平台，开源200万行代码。（取代unity，autodesk的独特定位）
- 2-3 独创互联网AI互动教学系统，基于流媒体技术让虚拟现实课程在手机微信、电脑浏览器上可以1秒打开，无需安装插件，无需漫长的加载，1秒开始学习。
- 2-4 提供文档+教材+培训服务：1-2周内，学生就可以快速掌握并开始创造属于自己的作品。
- 2-5 教学素材资源可共享。别人的作品就是最好的老师。我们用区块链技术保护所有历史版本的知识产权，并让用户永远可以站在巨人的肩膀上创作。

## 项目内容
### 1. 自主可控的虚拟仿真引擎，并支持国产操作系统

详见[功能清单](https://keepwork.com/official/docs/references/features/index)

进一步研究对国产操作系统的支持，包括
- 1 直接编译并运行在linux内核的国产操作系统上的3D引擎。
- 2 通过web assembly直接运行在浏览器的虚拟现实引擎，包括对io, 3d图形渲染，多线程等难点的技术支持。

### 2. 建设国内自主技术的虚拟现实创作社区。
基于国产云平台uengine,建立开发者社区后台或私有云，包括3d模型，cad模型，动画，代码等资源商城，用户git云端个人数据存储与多人协作权限管理。并应用到10所高职、高专、应用型大学，建立Paracraft虚拟仿真实验室，共同建设基于国内自主技术的虚拟现实创作社区和资源库。

### 3. 面向人工智能的3D虚拟仿真平台
大语言模型在强化学习和虚拟仿真环境下都需要3D仿真环境，用于训练和模拟多关节虚拟机器人。Paracraft将开发面向自主行动角色的3D虚拟仿真平台，做到完全自主可控，包括： 
1. 基于刚体动力学的可编辑3D虚拟仿真环境
2. 可编辑、可编程的多轴虚拟机器人，例如双足人型，四足动物型，无人机群体等。
3. 所见即所得的机器人与虚拟世界编辑与仿真环境。
4. 构建一个基于人工智能的基于虚拟仿真或动画的自动强化学习案例。

过去研究成果，请见：
- [paracraft可编程机器人](https://keepwork.com/official/docs/tutorials/robot_intro)
- [面向动画的自主虚拟人](https://keepwork.com/official/tips/s1/1_80)


该研究成果对于面向人工智能的机器人运动控制与仿真系统具有重大意义。


## 同行分析与背景
全球，虚拟现实技术有代表性的2个开发者生态为Unity和Roblox。Unity是通用3D引擎技术起家的国外公司，类似的还有Unreal等，2021 年，Unity应用每月的下载量超过50亿次，全球月活Unity用户超过150万人，Unity创建和运营业务所触达的全球平均月活玩家数量超28亿。国内95%以上的高职和高校的虚拟现实课件采用Unity开发完成。Roblox是更加面向青少年的创作者社区，类似的还有Minecraft等。Roblox的开发者主要为高中生和大学生，使用者以中小学生为主； 2022年3季度，每天使用Roblox的用户为5880万人，月活跃创作者超过了400万人、线上由玩家和开发者创作的地图超过了4000万款。上述Unity, Roblox, Minecraft等都有面向学校的教育版和相应的开发者社群。

## 可行性分析


帕拉卡已经在广州和江西300多所学校进行了试点，在课内和课外都取得了很好的教学成果。在1年的时间内，超过10万学生通过430课堂学习和使用了帕拉卡，学生创造了10万多个个人数字作品，创造了200多个3D虚拟校园，多名一线的信息科技老师发表了基于帕拉卡的学术论文或书籍（见参考文献1,4,5），同时获得了2022信息科技课标专家组的推荐，并进入了2022年10月教育部的信息科技的课标解读（见参考文献2）。


### 应用案例

#### 用于大富科技子公司的机器人建模与仿真
使用paracraft做CAD建模并投入物理机器人的生产。制作了50款机器人原型机，并有2款正在准备商业化。

#### 《北京开放大学》部署虚拟现实仿真与教学平台
  
北京开放大学旅游学院采购帕拉卡软件，作为**虚拟现实仿真与教学平台**，并部署到全校的计算机教学中心。学校的于平老师基于该平台自主研发了一套校本课程，并出版了图书。同时学校的Python语言课程也正在尝试放到帕拉卡3D虚拟仿真平台中进行教学。该套课程获得了获得2018年国家最美慕课3等奖


#### 《深圳职业技术学院》开设镜头语言课

深圳职业技术学院从2018年开始, 学校的镜头语言课程的教学、学生随堂练习、期末作业都采用了帕拉卡平台。学生可以在3D虚拟世界中实践镜头语言、在虚拟场景中练习电影拍摄技巧。上课老师为：深职院资深动画教师郭启晨老师。下图为深职院的学生的上课场景。


#### 《玩学世界》语数外3D交互手机APP，科大讯飞投资，百万用户
  
《玩学世界》是合作伙伴（科大讯飞投资）基于帕拉卡开发的手机APP。
- K12全学段学科教育，打造沉浸式学习
- 获客成本0.1元、月留存30%、上线3个月60万月活
- 30万用户创造的3D家园

#### 《魔法哈奇》国内首个3D儿童社区游戏，500万用户，4000万营收
  
《魔法哈奇》是创始团队基于NPL语言开发的儿童3D游戏社区

- 2009年上线，由上市公司上海淘米运营  
- 500万注册用户，4000万营收
- 百度贴吧200万+帖子

#### 学员开发的《圣诞树》儿童教育APP， iOS儿童应用付费榜前10
 
学习和使用3-5年帕拉卡的学员，可以制作商业APP，并实现盈利。


## 参考文献
1. 龚春美.《项目式学习下初中信息技术教学内容的重构》，中学教学参考，2022.6 
2. 教育部专家组.《义务教育信息科技课程标准(2022年版)》，人民教育出版社，2022.9
3. 大富网络. 帕拉卡软件虚拟现实课件平台，https://keepwork.com/official/open/vr/index，2022.10
4. 杭州上城区信息科技教研组. 《Paracraft青少年3D动画编程入门（微课版）》，清华大学出版社，2021
5. 于平，北京开放大学. 《Paracraft创意动画入门》，清华大学出版社，2018
6. 李铁才，李西峙.《相似性与相似原理》第2版，哈尔滨工业大学出版社，2020
