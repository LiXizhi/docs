<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/docgen`**

**quick ref:**
> /docgen [filename]

**description:**

```
generate NPL documentation for the given file. 
@param filename: lua file name to parse. if filename matches "*.docgen.txt", we will parse all files in it. 
	if nil, it will default to ./Documentation/paracraft.docgen.txt
e.g.
/docgen script/apps/Aries/Creator/Game/block_engine.lua		:parse only this given file
/docgen     :rebuild all files in paracraft.docgen.txt
```

<!-- END_AUTOGEN-->
