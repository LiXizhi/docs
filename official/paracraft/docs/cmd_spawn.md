<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/spawn`**

**quick ref:**
> /spawn [@entityname] [item_id] [-radius number] [-p x y z (dx dy dz)] [-s|persistent] [-name string]

**description:**

```
 spawn the given item. 
The max number of objects that can be spawned is the same as the total item count in the containing command block
Entities that are farther way are destroyed when new entity is spawned. 
@param entityname: if [-p] is not specified, it means near which player to spawn (default to current player). 
@param item_id: the item_id to spawn, if not specified, we will randomly find one from the containing command block. 
@param [-radius 3]: specify a radius, default to 1.
@param [-p x y z (dx dy dz)]: specify a location or cubic region to spawn (may be relative to containing block). if not specified, it uses entityname's position.
@param [-s|persistent]: if the spawned object is persistent, default to false.
@param [-name string]: give a name to the entity
Examples:
/spawn    : spawn randomly near the current player using items in the command block.
/spawn -p ~ ~1 ~     : spawn on top of the command block.
/spawn -p ~5 ~-1 ~-8 (3 0 4)	: in a cubic region relative to the command block.
```

<!-- END_AUTOGEN-->
