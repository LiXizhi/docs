<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/else`**

**quick ref:**
> /else

**description:**

```
jump to the next "else", "elseif", "fi", "end" command
examples: 
if $(rand)>=0.5 then
	echo "1"
elseif $(rand)>0.5 then
	if $(rand)>0.5 then
		echo "2.1"
	else
		echo "2.2"
	fi
	echo "2.3"
else
	echo "3"
fi

set abc=$(rand)
if %abc%<0.3 then
     echo "1"
elif %abc%<0.6 then
     echo "2"
else
     echo "4"
fi
```

<!-- END_AUTOGEN-->
