## NPL/ParaEngine 技术攻坚

> **优先级评分 / 完成度%**
> 2：影响商业化的高优先级； 1：必须有但可延后；0：最好能有

### 1. 动态物理引擎
- 将C++中的PhysicsBT开源物理引擎接口开放给NPL层 2 / 60%
- 方块引擎和实体引擎的刚体动力学的融合 2 / 50%
- 刚体动力学API完善 1
- 布料仿真 1
- 轮子动力系统仿真 1
- 真实流体与粒子仿真 1
- 双足与四足动物仿真 0
- 反向动力学解算 0

### 2. 渲染与效果
- 方块材质编辑器支持全部材质层 2 / 50%
- marching cube算法将BMAX模型转化为更平滑的多边形 2 / 10%
- 手机端渲染管线重构，支持最新的渲染技术  1
- 通用材质编辑器和渲染管线优化  1
- shader 3 通用HLSL渲染管线重构  1
- 更改默认的方块渲染， 增加方块的圆角渲染 0
- /shader cartoon 卡通渲染 0
- 任意LOD编辑方块地形引擎的功能 1
- 对标unreal 5的nanite渲染管线，无限多边形Retain模式渲染 1
- 支持多scene和viewport渲染 1
- 类似unreal 5 批量树木，植物生成器，可以考虑不是方块来做。 1

### 3. NPL语言
- 支持类型标记，编译时支持部分强类型语言的特性  1
- 支持stack object  1
- visual studio NPL插件升级  1
- vs code NPL插件升级  1
- MCML v2.0升级 -> HTML5 兼容更多css 1
- Git Cloud 分布式数据库实现 1
- official/docs中文文档 1

### 4. 导入导出
- 支持GLTF/FBX中的更多材质 2 / 10%
- 电影方块动画导出X文件 2
- 全场景导出gltf 2 / 50%
- 支持VR 360全景视频和全景立体视频导出 2 / 80%
- 基于WebXR实现VR宏示教 2 / 10%
- POVRay光线追踪渲染和云渲染 1 / 10%
- mp4 电影级ray tracing导出插件 v2.0
- Calender服务器NFT数字资产自动备份 1
- BMAX， CAD模型支持生成UV文理坐标， 让用户可以画贴图 1
- CAD模型支持基本材质，类似方块ID 1
- PC支持蓝牙模块 1
- 支持红外传感器，用于VR、AR等项目 1

### 5. 跨平台
- 全场景导出gltf 2 / 50%
- 国产linux操作系统的兼容   2 / 80%
- cp_old和dev分支合并，提供全平台的统一代码分支和CI 1
- directX和openGL最新版本的抽象统一API 1
- iOS android 手机版Webview和常用第三方插件支持 2 / 20%
- 基于emscripten实现引擎到web asm的编译，实现Web版引擎  2 / 50%
- 全平台自动化编译和多环境部署CI/CD  2 / 0%
- 增强虚拟现实 AR augmented reality 对接摄像头 1

### 6. 编辑器
- 跨平台声音录制 + 声音波形编辑 2 / 50%
- 粒子系统编辑器 脚本版 2
- 电影方块的扮演模式和多轴模式 2
- E键菜单中的objects物品列表 1
- 简易版photoshop, 支持产品内绘制方块材质或x文件的皮肤 1
- /diff world 2.0  多人世界合并 2 50%
- /game interface  GI 系统 孙子兵法 + 多人联网编辑器 1
- NPL图块编辑器2.0 1
- 动画识别方块, 自动识别方块并增加骨骼动画 v2.0  1 
- 从图片生成3D模型 1
- Keepwork网站编辑器手机端优化 2 / 30%
- 摄像头对接骨骼动作识别系统 1

### 7. AI
- 基于时间序列的自主人物动画系统 1 / 10%
- 用NPL实现深度学习类库，GPU版本 1 / 10%
- AI文本到动画的自动生成系统 0
- AI文本到3D模型的自动生成系统 0
- 摄像头对接骨骼和面部识别  0
- 语音识别&LLM集成  1 / 100%
- 自动化测试中的3D搜索和相似度匹配 1 / 10%


### 8. Web端
- clang/python/npl wasm环境 1 / 100%
- 基于lexical的markdown编辑器代替现有编辑器 1 / 50%
- keepwork重新改版,强化笔记和数字教材 1
- 云平台具有制课能力，和keepwork打通 1
- 教、学、练、测、评的可计算文档  1
- 可计算文档支持在线容器 1
- 基于可计算文档的自动化测试 0 
- 抖音基于深度学习的广告投放 1
- 稳定性、Cache性能与数据库优化、监控 1
- paracraft网页版应用化：手机Chrome触控，全平台，启动优化, WebXR 1
- AIGC能力：keepwork知识库的学习，问答系统，助手 1


## 专利计划
1. 《一种基于流媒体技术的3D示教系统》 @big
2. 《一种基于流媒体技术的360度全景互动世界制作系统》 @big 1. 2D非流媒体的申请2个 2. 3D的申请2个。 编辑的申请1个。移动端+PC端适配，组合键，鼠标提示，录制等等。
3. 《一种基于流媒体的360度全景互动电影系统》 @pbb 1个交互系统 2个编辑系统3DXML打点
4. 《一种基于双向流媒体的360度全景互动游览系统》 @pbb 2-3个专利
5. 《一种基于立方体的无UV真实物理材质渲染系统》 @wxa 基于Voxel的PBR材质系统。 编辑器一些针对voxel的操作，3D内部，Fill操作， PBR的UI。 传统的UV上贴图，Voxel不需要制定UV， 但是如何自动生成可以tile的UV， 针对不同的形状和方向。对无UV的材质apply流程的保护。
6. 《一种基于共享虚拟土地的在线项目式教学系统》@pbb 2in1的3C教学法（有ppt, Copy, Create,Competition）每人一块地的共享编辑加浏览。
7. 《虚拟校园与海量个人作品的3D游览与演示系统》@pbb 抖音是2D的，我们提供一种3D的浏览方式。中间100个固定，可买卖， 周围采用AI自动根据手势方向（好友，同地区，全国，四个方向）填充，以达到最大的虚拟价值和社交体验。 128x128, 64x64. 大小要保护。
8. 《一种基于虚拟现实技术的1对多人的在线师生作品评价与教学系统》 @wxa AI导游+真人平行世界做干预的一套1对500的在线的教学系统。作品陈列的逻辑， ggs切换服务器的逻辑。
9. 《一种基于个人成长档案与AI测评的编程能力测评模型》 @lzq, jn.  课程组搞定。记录在区块链上，如何将行为变成数据，用于档案。例如所有的打字， 鼠标点击， 使用时长，代码量，阅读量，作品等。 可量化的。 在不考试的情况下， 如何通过用户在几年的电脑使用行为，自动生成量化的指标。
10. 《一种基于小数据模型的3D模型骨骼动画自动生成系统》 @lxz 
11. 《一种基于时间序列的自主人物动画系统》 @lxz
12. 《可定制代码方块的图块编程的编辑系统》 @wxa 
13. 《一种基于堆栈的强类型与弱类型混合脚本语言》 @wxa  1. 类似js到ts的类型compile time的标记。不提lua，但是所有的syntax重新定义。 type lua， meta programming, typed table和table的自动转化。提升table.key的速度，接近C++的性能，包括未来做deeplearning类库， 都可以直接用NPL， nvidia cuda显卡的支持。   2. Pin to stack的语法, 参考C#,不要再heap上分配typed table, 而是利用luajit，直接生成stack上的对象， 退出直接删除， 不经过GC。   
14. 《基于方块的3D沉浸式编程系统》 @pbb 补充代码方块的专利。 瞄着ms,minecraft. 让他们无法用codeblock的编程模式。 
15. 《方块转换为LOD和物理模型的方法》@wxa
16. 《无限LOD的地形引擎和数据存储方法》 @wxa  1 在基本比例尺附近用id来存，比例尺以外，以数组或octtree的形式存储。存储参考UTF8. 例如0-128之间就是常用方块或字母。 超过128，multibytes. 类似的原理设计Voxel的方式。 做3级。 1级ID， 2级ID+data, 3级 id+octtree.  
17. 《用NPL实现MCML》 @wxa  single pass 60FPS
18. 《空间搜索算法》 @pbb  像搜索1位文字匹配一样的，搜索3D blocks的集合。
19. 《marching cube算法将BMAX模型转化为更平滑的多边形》
20. 《Git Cloud 分布式数据库实现》@zlj 参考github, 1 writer 多 readers. 1对3.git场景的分布式数据库。 
21. 《Calender服务器NFT数字资产自动备份》 @zlj 简单，容易写。 1. 如何存 2. 如何验证数字资产
22. 《一种基于可计算文档的3D运行时环境》@lwy
    - https://github.dev/tatfook/codelab3d/blob/main/paralab_design_doc.ipynb
23. 《一种基于markdown的可计算文档交互系统》@liufengfeng
24. 《一种图形化编程的可计算文档交互系统》@lwy
25. 《一种从可计算文档自动生成3D交互场景的系统》@lwy
26. 《一种基于空间切割的3D世界的打包和存储方式》@pbb   1. 世界以4叉树的方式存储世界中的对象，包括方块与方块中的数据（普通方块，代码方块，电影方块等） 2. 每512x512方块为一个region文件，将数据内容做了空间上的区分，不同空间对应不同的文件。3. 只有一个空间区域内的内容修改时，才需要重新序列化到磁盘， 这样方便快速的做数据恢复和局部备份。 4. 支持所有文件打包到一个pkg文件（虚拟文件系统）， 可以在不同的平台下被执行，以及快速的通过CDN网络下载, 可以和NPLRuntime一起打包为独立可执行文件。 5. 空间切割后， 可以有效的做基于3D世界的多人同时编辑协作，避免文件冲突，方便merge。6. 正对每个region文件做了基于用户身份的加密, 对用户知识产权做了额外的保密。 
27. 《一种基于3D场景的机器学习训练与教学系统》 @wyx
28. 《一种基于3D场景的低代码模组》 @wyx
29. 《一种基于虚拟串口的数字孪生数控仿真模组》 @wyx  虚拟掌控板
30. 《基于视频和虚拟仿真的动态手势识别技术》 @wyx handpose + machine learning
31. 《基于视频和虚拟仿真的人体姿势识别技术》 @wyx bipedpose + machine learning
32. 《一种图形化编程复制、粘贴代码API的技术》 @wxa 多个代码方块中复制自定义代码
33. 《一种基于视频和微波炉的低成本3D扫描技术》 @lxz Nvidia AIGC的方案 + 微波炉
34. 《一种可交互3D绘本制作与交互系统》 @wyx
35. 《一种基于多点手指拖动和外部摄影机的3D多角色动画制作系统》 @wyx
36. 《一种基于电脑视频游戏的动作捕捉系统》 @lxz 显卡 + AI GC
37. 《一种基于可计算文档的文件编辑、编译和交互系统》 @lwy 串联文件， 文件和系统一一对应。 
38. 《一种基于3D动画的强化学习3D沙盒训练与仿真系统》 @lxz mindmanager
39. 《一种基于基于3D动画和沙盘的无人机编队系统》 @wyx 
40. 《一种基于大语言模型的3D沙盒语音辅助创作系统》 @wyx






## 应用层
- [帕拉卡Paracraft历史更新记录，用户看的]( https://keepwork.com/keepwork/changelog/paracraft/changelog_zh)
- [引擎层历史更新记录](https://github.com/LiXizhi/NPLRuntime/commits/dev)