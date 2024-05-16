<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/walk`**

**quick ref:**
> /walk [@entityname] [x y z] [-random 5] [-speed 1.0] [-finishanim 0] [-to|away @entityname] [-dist 10] [-fly]

**description:**

```
let the given entity walk to a given position. 
@param entityname: name of the entity, if nil, it means the calling entity, such as inside the entity's inventory.  
@param x, y, z: the target position. if not specified it means the current entity's position. 
@param -random: if specified we will find add a random number to the target position, so that it walks to a random position within this radius
@param -speed: if specified it will modify the entity's walk speed. 
@param -finishanim: if specified, it will play the given animation once the player has reached the given position. 
@param -to|away: if specified, the player will walk to or away from the specified entity
@param -dist: only used when -to/away is specified.  How close to stop when walk to (default to 1). or how far to stop when walk away, default to 20. 
@param -fly: force flying
e.g.
/walk 19200 4 19200 -random 10   walk randomly to any position within 10 meters of the specified point. 
/walk -to @a -dist 1  walk towards nearby player until distance is 1. 
/walk -away @a -dist 10 walk away from nearby player until distance is 10. 
```

<!-- END_AUTOGEN-->
