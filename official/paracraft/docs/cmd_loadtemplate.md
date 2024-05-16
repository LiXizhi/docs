<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/loadtemplate`**

**quick ref:**
> /loadtemplate [-r] [-abspos] [-tp] [-a seconds] [x y z] [templatename]

**description:**

```
load template to the given position
@param -a seconds: animate building progress. the followed number is the number of seconds (duration) of the animation. 
@param -r: remove blocks
@param -abspos: whether load using absolute position. 
@param -tp: whether teleport player to template player's location. 
@param x,y,z: position or current player position
@param templatename: relative to current world. the file is at blocktemplates/[templatename].blocks.xml
default name is "default"
/loadtemplate ~0 ~2 ~ test
/loadtemplate -a 3 test
/loadtemplate -r test
```

<!-- END_AUTOGEN-->
加载模板到指定的位置。

> 点击观看[loadtemplate命令教学视频](vt_loadtemplate)