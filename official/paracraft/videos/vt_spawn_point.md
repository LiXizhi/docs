## 出生点教学

<iframe frameborder="0" width="100%" height="600" src="https://v.qq.com/txp/iframe/player.html?vid=y0387l390oq"></iframe>

- `00'04s` `E键`-->`机关`-->`出生点` 上限:1 id:20002 
- `00'35s` `右键单击` `出生点`，点击`逻辑`，输入出生点命令：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/time -1`：时间为午夜
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/mode game`：游戏模式下
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/addrule Player AutoWalkupBlock false`：人物不可自动走上前方高于他一格的位置
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/speeddecay 10 10`：摩擦力。第一个10为地表摩擦力，第二个10为空气摩擦力
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/addrule Player JumpUpSpeed 5`：人物向上跳跃速度。系统默认值为6.5
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/music 5`：播放系统内部声音5
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/addrule Player CanJumpInAir false`：人物不能连跳
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/addrule Block CanPlace 190 87`：`拉杆` id:190 只能放在`萤石` id:87 上 
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/addrule Block CanPlace 105 23`：`按钮` id:105 只能放在`红色羊毛` id:23 上
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/clearbag`：清空人物背包 
- `06'33s` 多条命令可放入`命令行`书（`E键`--> `机关`下），方便复用
- `06'57s` 重新放置`出生点`，`出生点`中命令不变
- `07'39s` `右键单击` `出生点`，将其手工`删除`后，`出生点`中命令将不复存在
- `08'06s` `/home`：将人物传送回`出生点`

### References
- [`/time`命令参考手册](cmd_time)
- [`/mode`命令参考手册](cmd_mode)
- [`/addrule`命令参考手册](cmd_addrule)
- [`/speeddecay`命令参考手册](cmd_speeddecay)
- [`/music`命令参考手册](cmd_music)
- [`/clearbag`命令参考手册](cmd_clearbag)
- [`/home`命令参考手册](cmd_home)
- [出生点教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=79)