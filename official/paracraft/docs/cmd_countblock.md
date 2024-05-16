<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/countblock`**

**quick ref:**
> /countblock x y z (dx dy dz) [blockid] [data]

**description:**

```
return the number of blocks in the cube region specified. 
@param blockid: the block id, if not specified it will match all blocks
/countblock ~-1 ~1 ~ (-1 2 ~)
/countblock ~-1 ~1 ~ (-1 2 ~) 62
/if $(countblock ~-1 ~1 ~ (-1 2 ~))==2 then
	/tip there are 2 blocks 
/fi
```

<!-- END_AUTOGEN-->
在指定区域内的方块进行操作。
如：此区域内的方块要指定某ID方块或方块数量激活。