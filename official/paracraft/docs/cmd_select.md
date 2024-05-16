<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/select`**

**quick ref:**
> /select [-add|clear|below|all|pivot|move] x y z [(dx dy dz)]

**description:**

```
select blocks in a region.
-- select all blocks in AABB region
/select x y z [(dx dy dz)]
-- select all block below the current player's feet
/select -below [radius] [height]
-- add a single block to current selection. one needs to make a selection first. 
/select -add x y z
-- clear selection
/select -clear
-- select all blocks connected with current selection but not below current selection. 
/select -all x y z [(dx dy dz)]
-- set pivot point
/select -pivot x y z
-- move to a new position
/select -move x y z
```

<!-- END_AUTOGEN-->
