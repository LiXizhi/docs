## 批量编辑命令教学


```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/395/raw#6. 批量编辑命令教学_0.mp4
  ext: mp4
  filename: 6. 批量编辑命令教学_0.mp4
  size: 378571285
```
[在腾讯视频播放](https://v.qq.com/x/page/o03867v9wf0.html)
- `00'08s` `Shift+Alt+右键`：批量换色
- `00'57s` `/replace -all 原id 新id 半径`：替换区域内指定类型的所有方块（方块可以不相邻）
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/replace -all 23 87 50`：在半径50的范围内，将23红色羊毛换成87萤石
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/replace -all 86 92 50`：在半径50的范围内，将86橡树叶换成92樱花
- `03'48s` `/fill`：区域填充，另外可参考[地形笔刷工具](item_TerrainBrush)
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->首先，选中要替换成的方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->然后，`Ctrl+左键`点击边缘，选取要填充的区域
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->最后，输入`/fill`，使用选中的方块填充该区域
- `05'40s` `/del -below 半径`：删除人物当前高度以下的所有方块，常用于修整地图
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->注意：命令执行需要一定时间，且不可撤销，建议提前备份世界
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/del -below 30`：将人物下方，半径30以内的所有方块删除
- `07'52s` `/setblock 目标区域 方块id`：替换立方体区域内所有方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`F3键`-->`Ctrl+左键`选取区域-->`Ctrl+T`复制区域坐标
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock 20423 59 19384 (15 4 31) 0`：删除区域内所有水和其它方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/setblock 20423 59 19384 (15 4 31) 62`：将区域内所有方块替换为`62草方块`
- `10'05s` `Alt+左键`：吸取材质

### References
- [电影场景教学](vt_movie_scene_building)
- [`/fill`命令参考手册](cmd_fill)
- [`/replace`命令参考手册](cmd_replace)
- [`/del`命令参考手册](cmd_del)
- [`/setblock`命令参考手册](cmd_setblock)
- [批量编辑命令教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=75)
- [地形笔刷工具](item_TerrainBrush)