<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/goto`**

**quick ref:**
> /goto [@playername] [x y z]

**description:**

```
teleport current player to a given block position relative to given player. Similar to /tp except that it uses block position. 
format: /goto x y z  abs position
format: /goto ~ ~1 ~  relative position
format: /goto home -- teleport to home   
format: /goto [@playername] [x y z]
```

<!-- END_AUTOGEN-->
将当前角色传送指定角色的相对位置。

例如：在联网环境下:
```lua
-- 传送到用户`150634875`身边
/goto @__MP__150634875
-- 传送到管理员身边
/goto @__MP__admin
```