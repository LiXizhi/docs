<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/say`**

**quick ref:**
> /say [@entityname] [-duration 10] [-2d] [any text here]

**description:**

```
let the given entity say something on top of its head. 
@param entityname: name of the entity, if nil, it means the calling entity, such as inside the entity's inventory.  
@param duration: how many seconds the head dialog last.
@param 2d: whether to render in front of all 3d objects
e.g.
/say hello there! 
/say -duration 10 hello
/say -duration -2d hello   : render as 2d
```

<!-- END_AUTOGEN-->
