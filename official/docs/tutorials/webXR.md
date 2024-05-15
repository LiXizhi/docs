## 如何用Paracraft创造虚拟展厅？

使用paracraft可以非常方便的创建数字展馆，可以是自己的数字作品，也可以是NFT作品。常用的功能包括：

- 方便的创造属于自己的展厅（3D场景）
- 每个数字作品都可以点击交互
- 为展厅制作漫游电影或动画
- 添加智能导游NPC
- 多人联网，邀请朋友到你的虚拟世界
- 多人联网文字、弹幕、3D角色动作交互
- 丰富的主角形象任你选择
- 支持所有设备：Windows/MAC/Android/iOS/Linux/Web浏览器
- 随时随地在任意设备上编辑虚拟世界，支持多人编辑和权限管理。
- 动态实时生成左右眼，红蓝，交替光栅等格式的VR图像。
- 可生成360度VR全景视频，通过PICO, VIVE, OCULUS等VR设备宣传你的作品。

> 点击观看360VR全景画展短片演示：[Jingji的画展](https://www.bilibili.com/video/BV1BG4y1k711)

注意： bilibili, youtube等大部分视频平台都支持360全景视频，如果你有VR眼镜可以直接观看，如果没有VR眼镜，也可以在电脑上通过鼠标拖动视频窗口模拟头部的运动来观看。

### 如何添加和创建数字藏品？
```@Project
styleID: 1
project:
  projectId: '75309'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/25245/raw#1674239698853image.png
  ext: png
  filename: 1674239698853image.png
  size: '484504'
  unit: px
  width: '600'
  alignment: left
  custom: false

```
- 对于图片类的数字作品，方法如下：

> 点击观看教学视频 [相册的使用](https://keepwork.com/official/tips/s1/1_211)

我们到E键装饰项下，找到相册，ID是218。我们将相册放到墙上，像这样。根据我们需要的图片大小来摆放。

- 对于3D模型类的数字作品，请看
- [如何使用活动模型](https://keepwork.com/official/docs/UserGuide/animation/ActivityModel)
- [如何导入FBX和GLTF模型文件](https://keepwork.com/official/docs/UserGuide/scene/import_export)

### 如何为相册添加交互？

这里需要用到代码方块。

> 点击观看教学视频 [可点击的相册](https://keepwork.com/official/tips/s1/1_197)

### 如何限制观众的参观顺序？

> 点击观看教学视频 [密室解锁逻辑（上）](https://keepwork.com/official/tips/s1/1_198)

> 点击观看教学视频 [密室解锁逻辑（下）](https://keepwork.com/official/tips/s1/1_199)

### 如何优化超大型展馆的性能？

如果你的展馆十分巨大，例如有成千上万的作品，建议放置到不同的房间中动态加载资源。

> 点击观看教学视频 [用代码方块自动加载房间内景](https://keepwork.com/official/tips/s1/1_189)

### 如何制作展厅漫游动画？

paracraft提供了强大的摄影机、动画、字幕、自动配音等系统。你需要用到电影方块。详情[点击这里](https://keepwork.com/official/docs/UserGuide/animation/movie_block)

### 如何开启多人联网？

> 点击观看教学视频 [多人联网ggs命令](https://keepwork.com/official/tips/s1/1_146)

### 如何可以多人一起维护3D世界？

> 点击观看教学视频 [设置世界的多人编辑权限](https://keepwork.com/official/tips/s1/1_202)

### 即将上线：Web VR全景示教系统！

通过VR设备：眼镜+手柄，完成在PC端所有课程的示教操作。
宏示教课程只需制作1次， 就可实现PC/Web/Mobile/VR的自适应发布。

### 如何提升展厅的画面效果？

材质和灯光可以提升整个展馆的画面效果。

- [点击这里查看材质的文档](https://keepwork.com/official/docs/UserGuide/scene/block_material)
- [点击这里查看动态光源的文档](https://keepwork.com/official/docs/UserGuide/scene/lighting)

### 如何输出VR视频

- [导出360度VR全景视频](https://keepwork.com/official/docs/tutorials/vr360)
- 支持传统的红蓝、左右眼立体、交替光栅等立体实时输出。

> 点击观看教学视频 [立体输出](https://keepwork.com/official/tips/s1/1_74)

### 总结

Paracraft是一款简单易用的元宇宙创作工具。
更多介绍，请[点击这里查看虚拟现实解决方案](https://keepwork.com/official/open/vr/index)