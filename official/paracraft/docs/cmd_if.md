<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/if`**

**quick ref:**
> /if var1==var2 [/othercommand|then]

**description:**

```
do a command if var1==var2, also support operators like < <= >= >
To embed other commands in variables use $(other command text), such as $(rand)
Examples: 
/if %name% == 0 /tip your name is 0
/if %name% == "0" /tip your name is 0
/if "%name%" == "0" /tip your name is 0
/if 2 >= 1 /tip 2>=1
/if 1 < 2 /tip 1 < 2
if $(rand)>=0.5 then
	echo ">=0.5"
else
	echo "else"
fi
```

<!-- END_AUTOGEN-->
