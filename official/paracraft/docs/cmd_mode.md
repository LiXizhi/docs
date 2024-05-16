<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/mode`**

**quick ref:**
> /mode [game|edit|tutorial|school|strictgame]

**description:**

```
locking game mode to the given value. 
Once locked, user will not be able to toggle unless with command line. 
@param game: in game mode, one can use /addrule command to define world rules
@param edit: in edit mode, everything is editable. 
@param tutorial: tutorial mode is same as edit mode, except that mouse picking 
is only valid if there is a ending block(id=155) below. 
e.g.
/mode game     :lock to game mode
/mode edit     :lock to edit mode
/mode          :unlock and toggle between game/edit mode. 
/mode tutorial 
/mode strictgame : no commands, no cheating. Only activated when game is readonly.
```

<!-- END_AUTOGEN-->

`/mode game` 锁定为播放模式(游戏模式)。
 一旦锁定用户将无法切换为其它模式，除非再次输入/mode。
`/mode edit` 锁定为编辑模式
`/mode` 解锁和播放/编辑模式之间切换
`/mode tutorial` 教学模式
`/mode strictgame` 锁定为强制游戏模式，这种模式下，用户没有任何方法可以切换。 除非是世界作者才能用/mode切换。


