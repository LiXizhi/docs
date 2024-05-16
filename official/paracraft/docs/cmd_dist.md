<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/dist`**

**quick ref:**
> /dist [@entityname]

**description:**

```
return the block distance from current player to given player.
This command is usually run from NPC or command block to obtain distance to a nearby player. 
@param entityname: name of the entity.
@return the block distance. if entity is not found, it will return a very large number
e.g.
/if $(dist @a) <= 2 /tip hello  : when the distance to closest nearby player is less than 2 meters, say hello
```

<!-- END_AUTOGEN-->
实行把物体或方块从这个人物分配给另外一个人物。