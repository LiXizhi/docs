<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/clone`**

**quick ref:**
> /clone [-update] from_x from_y from_z (dx dy dz) to to_x to_y to_z (dx dy dz) [where sameblock]

**description:**

```
 clone a region of blocks to another region
@param dx,dy,dz: can be negative
e.g.
/clone ~ ~-1 ~ (2 2 2) to ~5 ~ ~
/clone ~ ~-1 ~ to ~5 ~ ~
/clone ~ ~-1 ~ to ~-5 ~ ~ (3 0 3)
-- if sameblock is specified, we will only copy if dest and src id are the same.
/clone ~ ~-1 ~ to ~-5 ~-1 ~ (3 0 3) where sameblock
```

<!-- END_AUTOGEN-->
复制一个块到另一个区域，数值可以是负数。
如果指定相同的方块,我们只会复制选择的对象和id都是相同的。

> 点击观看[clone命令教学视频](vt_clone)
