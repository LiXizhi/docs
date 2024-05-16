<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/setblock`**

**quick ref:**
> /setblock x y z (dx dy dz) [block] [data] [entityDataTable] [where sameblock]

**description:**

```
 set block at given absolute or relative position. 
/setblock x y z [block] [data]
/setblock ~ ~1 ~ [block] [data]
/setblock ~-1 ~1 ~ (-1 2 ~) [block] [data] where sameblock
@param xyz are the coordinates of the block. relative position begins with ~
@param block is the BlockID of the block (includes id:0)
@param data is the block data
@param entityDataTable is xml table
@param where sameblock can be used to only modify block data of a given block in the region. 
Examples:
/setblock ~-1 ~0 ~-2 254 0 {attr={filename="blocktemplates/111.bmax", scale=2, facing=3.14}}
```
<!-- END_AUTOGEN-->

在指定位置生成和消除方块
- 点击观看[setblock教学视频](vt_setblock)

第三个参数为XMLTable, 例如：
```
/setblock ~-1 ~0 ~-2 254 0 {attr={filename="blocktemplates/111.bmax", scale=2, facing=3.14}}
```