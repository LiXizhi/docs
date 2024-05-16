## Compareblocks命令教学


```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/397/raw#4. Compareblocks命令教学_0.mp4
  ext: mp4
  filename: 4. Compareblocks命令教学_0.mp4
  size: 373747832
```
[在腾讯视频播放](https://v.qq.com/x/page/q0386wf1v19.html)

- `00'02s` `/compareblocks 区域坐标1 to 区域坐标2`：比较2个区域内的所有方块是否一致，若一致返回true并继续执行下一行命令。主要用来制作密码机关。完整`密码墙机关`举例：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'11s` 在区域2创建正确的`密码墙`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'46s` 在区域1后方创建[`命令方块`](item_Command_block)，并放入三本[`命令书`](item_CommandLine)
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'54s` 第一本命令书`/t 2 /activate`：在命令方块被激活的第2秒再次激活命令方块，这样使得命令方块中所有命令可以每隔2秒被执行一次
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`02'56s` 第二本命令书`/compareblocks 18750 2 18856 (0 2 2) to 18750 2 18852 (0 2 2)`：比较2个区域的密码墙是否一致，若一致继续执行后面的命令
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'07s` 第三本命令书`/setblock 18731 2 18861 (0 1 0) 0`：这行命令会在密码一致时执行，用来消除指定区域的方块（门打开）
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'38s` 第三本命令书`/t`：让命令方块中所有时间命令停止，命令方块不会被再次激活
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`05'12s` 最后，用红石线连接机关和命令方块，当用户触发机关时，命令方块可被首次激活 
- `06'20s` `/compareblocks 19298 64 19161 (2 2 0) to 19292 64 19161 (2 2 0)`：再次举例
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'38s` `/tip ding`：若前面命令中的2个区域一致，则显示`ding`
- `08'08s` 对比举例：用红石电路实现`密码墙机关`（要复杂很多）

### References
- [`/compareblocks`命令参考手册](cmd_compareblocks)
- [`/compareblocks`命令论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=125)