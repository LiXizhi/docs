<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/mount`**

**quick ref:**
> /mount [@entityname] -target [targetname] [-radius number]

**description:**

```
mount player or the given entity to another entity. 
@param entityname: name of the entity, if nil, it means the calling entity, such as inside the entity's inventory.  
@param targetname: if not specified, it will automatically find a nearby mountable target. 
@param radius: default to 2, only mount if the distance between two target is smaller than this. 
e.g.
/mount      :mount the player or calling entity to nearby railcars if any
/mount @p   :mount the last trigger entity or player to nearby railcars if any
/mount @test    :mount the "test" NPC to nearby railcars if any
```

<!-- END_AUTOGEN-->
