<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**item: `物理模型`**

| name | id | description |
|---|---|---|
| PhysicsModel | 22 | X |

<!-- END_AUTOGEN-->

### 物理模型
支持所有`ParaXModel(*.bmax, *.x, *.fbx, ...)` 目前模型中所有非透明的面都会认为有物理碰撞.

> 如果不希望有精确的多边形物理请使用[模型](item_BlockModel)


### 调试物理模型
使用命令`/show physics`可显示物理面（即绿色的多边形和法线），如下图所示。 

![image](https://cloud.githubusercontent.com/assets/94537/18075582/9b3c06dc-6ea8-11e6-948f-3d378298066b.png)

### 模型编辑
- 支持单轴任意大小统一放缩
- 支持Y轴旋转

![image](https://cloud.githubusercontent.com/assets/94537/18092503/1711ca52-6eff-11e6-9003-e0cb174e8196.png)

当人物手中选择`物理模型`工具时, 在下方可以选择两种模式。 一种是`模型创造`模式， 一种是`模型编辑`模式。
在编辑模式下， 你需要先点击选中场景中任何一个物理模型或模型，然后可对其旋转或放缩。 

### 注意事项：
- 模型的选择： 模型没有限制大小， 用户可以点击物理模型的任意位置删除或选择。 也可以点击所属方块的位置
- 模型的物理仅对主角生效，并且仅当主角走到物体附近时才加载
- 模型物理底层使用了`PhysicsBT`物理引擎


### 模型点击事件
右键点击模型可以编辑模型背包。 原理相当于命令方块，但仅当模型被点击时才执行。 如下图：

![image](https://cloud.githubusercontent.com/assets/94537/19898112/afe292d0-a095-11e6-872b-fcec7b5aab76.png)