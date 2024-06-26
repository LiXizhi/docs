# 编程教育的测评系统

这里我们设计一种评价学生综合编程能力的`自我在线测评系统`。 用户可以随时随地在家中对自己的编程能力进行测评，在不同的阶段可颁发相关的证书。

## 测评的用途与目标
首先评估的用途有3种：
1. 为了学生更好的自学
2. 为了老师更好的教学
3. 为了用人单位的评估

由于测评系统是被设计成用户可随时随地在家完成的，所以我们的主要用途应该是前2点。但是如果用户选择`购买证书`，我们也提供有一定公信力的针对第三点的测评服务。 

## 基本原则
测评系统的目标是为了让学生在学习的过程中，可以随时进行自我评估，并且可以帮助老师了解每个学生的学习进展和需求。

## 背景调研
- [美国高中联盟MTC](https://mastery.org/a-new-model/)将于2019年应用全新“高考”成绩考核标准,颠覆GPA。中文报道[点击这里](https://www.jiemodui.com/N/94552)
  - 相比高考，MTC强调学生的项目和能力，它将评估者从授课老师或国家教育部门，变成了高中的学校。对于联盟内的成员学校，MTC提供教师培训、工具、资源等支持，每个学校有2至5人团队负责“新模式”落地，每年MTC举办四次工作坊，由学校负责人、教育专家共同讨论落地过程中出现的问题。

- 欧洲的[CAS](https://www.computingatschool.org.uk/)提供了一套白皮书: 
  - 点击查看[CASPrimaryComputing.pdf](https://api.keepwork.com/storage/v0/siteFiles/3930/raw#CASPrimaryComputing.pdf)
  - 里面提到的形成性评估（Formative assessment）手段包括：自评，他评，讨论，项目，笔记, KWL列表等。 其中`自评`是主体：包括让学生制作教学视频，或视频博客。 

人在创作时，比如写笔记，制作教学视频，创作作品时，才会真正的自我审视；所以应该要求学生建立自己的个人学习的笔记网站或博客或视频博客。这些自评的记录同时也是`他评`的重要依据。 最后我们还可以每个月使用例如[知识清单](/official/docs/teach/lessons/paracraft_exams)的方式让学生定期比较下老师的学习笔记：已经掌握了什么，希望学习什么，还有哪些没有学(KWL列表)。

- github, stackoverflow, linkedin, wiki, 百度知道: 在专业领域，这3个产品或工具分别从某些方面符合教育评估的需求。但是需要降低使用门槛，让小学生和大众也能参与。

## 测评系统鼓励的行为
- 自主学习
- 创造个人作品
- 写笔记，写博客
- 做教学视频和教别人
- 多人协作，帮助别人
- 公开和发布自己的成果（作品，笔记，视频，出版物）
- 做长周期的大项目
- 与行业专家交流
- 发散学习，不限定学科
- 自我总结

## 测评系统不鼓励的行为
- 刷题
- 研究题库
- 背诵考点
- 重复做题，以提高考试反应速度

## KeepWork在线测评系统设计
测评应该包含下面的几方面的内容
- 个人作品的存储
  - 提交个人编程作品
  - 提交个人视频作品
  - 提交个人学习笔记
- 个人知识引擎
  - 让学生和老师将自己的知识数字化的系统
  - 编辑KWL列表：已经掌握了什么（Know），希望学习什么(Want)，还有哪些需要去学(Learn)
  - 提供一些领域专家的标准化个人知识样本。可以量化，并将学生的个人知识和专家的进行对比评分。
- 一个班级或学校的师生可以方便的看到彼此的作品，笔记，个人知识，KWL，并可以相互点评
- 全国范围的个人作品自动排行系统
- 一个可呈现给用人单位的标准化的个人网页首页
- 提供教师培训、工具、资源等支持

## 第三方创作工具的推荐标准
好的测评系统需要推荐好的创作工具给用户使用。 好的创作工具应该符合下面特征
- 用户拥有数据，可自行备份
- 可记录历史和时间戳
- 不限制用户的创造力

## 如何实施测评系统的新模式？
1. 在中小学和高中形成联盟： 让成百上千的中小学校加盟， 这样就有非常多的学生首页
2. 推荐给一流大学的自主招生平台：让更多的国家知名大学采纳，最终替代奥赛，成为高校自主招生的主要途径。 

## 为何高校愿意使用新模式？
目前高校的自主招生只针对奥赛获奖的学生开放。 这其实是不得已为之的，因为招生筛选简历很花时间。
但是如果我们允许高校的自主招生专家组从一个学生**小学开始**就开始关注他的成果，这样学生和招生专家都有更多的时间提供和了解更多的学生信息：比如学生的个人视频博客，个人学习笔记，计算机作品，中小学老师的评语，范围更广的各种技能的掌握程度等。每个高校可以动员学校**所有的老师**对7-20岁的学生主页进行标记和打分，形成高校的备选学生资源库。

让高校（包括企业）和优秀的学生之间形成长期的**双向选择**，而不用等到高考前的1-2个月内匆忙完成。未来的高考在教育评估中的比重会降低，而且也不需要集中考试，学生可以随时参加某个高校需求的专科考试即可，而且只要通过即可。 

## 终身制的评估系统在社会协作中的作用
评估系统可以是终身制的，类似linkedin。最终的目的是希望促成人与人之间的合作。 比如你在寻找科研伙伴， 创业合伙人， 企业在招员工等，都是社会协作。 在中小学阶段的评估以学校老师和专家的他评为主， 到了大学和成年则以自评为主要手段，以促成人与人的合作为目标。比如你可以通过文字标签，搜索你附近有哪些学生或成人对人工智能感兴趣，并且精通编程和心理学。 

很多社会上优秀的人，并没有在互联网上公开自己过去的笔记和作品，也许很久都没有更新过自己的简历。如果以创作为基础的评估系统在小学时就一直被使用，使用了15年就会成为习惯，对于推动个人知识的数字化和社会协作是非常重要的一步。





