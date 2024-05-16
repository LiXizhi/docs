<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/t`**

**quick ref:**
> /t [~][seconds] /othercmd

**description:**

```
Execute a command after a given time relative to caller entity. 
Each entity can have a list of timed event and an internal time variable. 
When the entity is active, the time variable will advance in each frame and execute any timed event
This command can be used to add or remove timed event and the internal time variable.
/t ~2 /activate     :loop and activate the calling entity every 2 seconds
/t ~1 /tip hi
/t ~0 /t 0   :set time to 0
/t			 :clear all timed event
```

<!-- END_AUTOGEN-->
