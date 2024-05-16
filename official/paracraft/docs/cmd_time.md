<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/time`**

**quick ref:**
> /time [-1,1] [now]

**description:**

```
set current time of day. 0 or nil means noon, -0.5 is dawn, 0.5 is twilight. 1,-1 is midnight
@return: the current time in range [-1, 1]. 
Example:
/time 0		set time to mid noon
/tip $(/time now)   return current time
```

<!-- END_AUTOGEN-->
