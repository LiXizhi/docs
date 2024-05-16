<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/testblock`**

**quick ref:**
> /testblock x y z [(dx dy dz)] blockid [data]

**description:**

```
Used to test whether blocks in the x, y and z coordinates or cube region specified is block_id. 
return true if all blocks match a given one. relative position begins with ~
/testblock x y z blockid data
/testblock ~ ~1 ~ blockid data
/testblock ~-1 ~1 ~ (-1 2 ~) blockid data
xyz are the coordinates of the blockid
blockid is the BlockID of the blockid (includes id:0)
data is the blockid data
```

<!-- END_AUTOGEN-->
