## 含羞草与含羞石教学

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/287/raw#2. 含羞草与含羞石教学.mp4
  ext: mp4
  filename: 2. 含羞草与含羞石教学.mp4
  size: 386728822
```

[在腾讯视频播放](https://v.qq.com/x/page/k03863kh5xt.html)
- `00'09s` `含羞草` id:221 相当于压力板+命令方块：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` `含羞草`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /music 5`：第1秒播放系统内部声音5
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 2 /text 文字`：第2秒显示情景字幕
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~3 /text`：过3秒字幕结束
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /move @a x y z`：过1秒将主角传送到坐标位置
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~2 /music`：过2秒音乐结束
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->人物触碰`含羞草`即触发命令
- `03'50s` 在`/addrule Player AutoWalkupBlock false`命令下（即人物不可自动走上前方高于他一格的位置），在方块前放置`含羞草`，人物可自动爬上一格
- `07'42s` `含羞石` id:227 周围相邻的六个方向上任一方块状态发生改变（生成或消除，有`可移动木箱`动态经过）即触发`含羞石`相邻的命令方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/tip ding`：在屏幕上方提示`ding`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击`推动`可移动木箱` id:83
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->黄框选中`藤蔓` id:162 或`梯子` id:166，`右键单击`拉动`可移动木箱`

### References
- [`/music`命令参考手册](cmd_music)
- [`/text`命令参考手册](cmd_text)
- [`/move`命令参考手册](cmd_move)
- 主角视角和传送教学
- 出生点教学
- [音乐教学](vt_music)
- [记忆学习教学](vt_block_memory)
- [含羞草与含羞石教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=73)
