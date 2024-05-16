## Setblock命令教学


```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/398/raw#2. Setblock命令教学_0.mp4
  ext: mp4
  filename: 2. Setblock命令教学_0.mp4
  size: 427732318
```

[在腾讯视频播放](https://v.qq.com/x/page/u0386dwsyff.html)
*注：视频中的黄色羊毛，红色羊毛在当前版本的Pararcraft的名字是彩色方块。*
- `00'11s` [`/setblock x y z id`](cmd_setblock)：在指定位置生成和消除方块
- `00'44s` 绝对坐标：`F3键`-->查看当前鼠标所在方块或所选区域的坐标-->`Ctrl+T`复制绝对坐标
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock 19260 63 19134 (2 0 1) 27`：在该区域生成黄色羊毛
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock 19263 64 19136 23`：在该位置生成红色羊毛
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock x y z 0`：消除方块（即在指定位置生成空气`0`）
- `06'09s` 相对坐标：`F3键`-->先`右键单击``命令方块`-->再查看当前鼠标所在方块或所选区域的坐标-->`Ctrl+R`复制相对坐标（即相对最近选择的对象(`命令方块`)的坐标）
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->注意：相对坐标在执行时，会随执行该命令的对象(`命令方块`)的坐标而动态变化
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock ~-3 ~-1 ~1 (2 0 1) 27`：在相对区域生成黄色羊毛
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock ~0 ~0 ~3 23`：在相对位置生成红色羊毛
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock ~x ~y ~z 0`：消除方块 
- `11'00s` `/setblock x y z id [方块数据data]`：data一般是数字0-6，代表物品方向
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock ~0 ~1 ~3 100 3`：生成方向为3的火把
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock ~0 ~1 ~2 188 6`：生成方向为6的楼梯
  
### References
- [`/setblock`命令参考手册](/official/paracraft/docs/cmd_setblock)
- [`/setblock`命令论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=77)