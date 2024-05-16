<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**item: `模型`**

| name | id | description |
|---|---|---|
| BlockModel | 254 | X |

<!-- END_AUTOGEN-->

```
/setblock ~-1 ~0 ~-2 254 0 {attr={filename="blocktemplates/111.bmax", scale=2, facing=3.14}}
```

输入保存好的bmax、x或fbx文件的相对路径，即可导入模型。

- [FBX格式参考文档](https://github.com/LiXizhi/ParaCraftSDK/wiki/FBXModel)
- [骨骼方块](item_Bone)
- [物理模型](item_PhysicsModel)

## BMAX添加插件点
你可以用BMAX做一个椅子，将其中一个骨骼命名为`mount`,那么当你右键点击这个bmax模型时， 人物会自动移动到骨骼位置。 

![image](https://cloud.githubusercontent.com/assets/94537/18039502/44626a68-6dd6-11e6-881a-2c6ce483f116.png)

> 也可以使用[物理模型](item_PhysicsModel) (面数不要太多)

![image](https://cloud.githubusercontent.com/assets/94537/18075582/9b3c06dc-6ea8-11e6-948f-3d378298066b.png)


### 参考文档
> [FBX格式参考文档](https://github.com/LiXizhi/ParaCraftSDK/wiki/FBXModel)


