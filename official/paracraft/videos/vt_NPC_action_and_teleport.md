## NPC动作和传送教学
```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/406/raw#4. NPC动作和传送教学_0.mp4
  ext: mp4
  filename: 4. NPC动作和传送教学_0.mp4
  size: 259230339
```


[在腾讯视频播放](https://v.qq.com/x/page/p0382hdxy4f.html)

- `00'06s` `/anim @NPC名字 lie`：NPC躺下 
- `00'50s` `/anim @NPC名字 sit`：NPC坐下 
- `01'26s` 将NPC传送到指定位置：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`F3键`：显示/隐藏x y z坐标
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`player`：主角所在位置的坐标。posX：主角的方向是面对x轴的正方向
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`[Ctrl+T]mouse`：鼠标黑框所在位置的坐标。side(5)：所在方块的顶面
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`[Ctrl+R]Relative to player`：鼠标黑框相对于主角的位置坐标
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->鼠标黑框选中目的地
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Ctrl+T`复制鼠标黑框的位置坐标`19255 63 19148`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->回车，输入`/move @NPC名字 19255 63 19148`  
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->再次回车，NPC即被传送到目的地
- `05'24s` `右键单击`NPC（`E键` `人物`下）-->`属性`-->可给NPC取名，换肤等
- `05'56s` `/velocity @NPC名字 0 10 0`：`0 10 0`分别代表x y z轴上的速度，x和z轴上的速度为0，y轴上的速度为10，效果为NPC高跳
- `06'45s` `/velocity @NPC名字 10 0 0`：y和z轴上的速度为0，x轴上的速度为10，效果为NPC向x轴的方向前进一段距离
- `07'04s` `/velocity @NPC名字 0 5 5`：x轴上的速度为0，y和z轴上的速度为5，效果为NPC向z轴的方向跳跃，并前进一段距离
  
### References
- [`/anim`命令参考手册](cmd_anim)
- [`/move`命令参考手册](cmd_move)
- [`/velocity`命令参考手册](cmd_velocity)
- [Setblock命令教学：绝对和相对坐标](vt_setblock)
- [人物对话教学：放置NPC](vt_dialog)
- [NPC动作和传送教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=70)
