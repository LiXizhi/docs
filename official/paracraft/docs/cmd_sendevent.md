<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/sendevent`**

**quick ref:**
> /sendevent [@entityname] event_name [cmd_text]

**description:**

```
 send a custom event to given entity
@param entityname: if not specified, it means a global event, which is handled by home point entity. 
@param cmd_text: additional parameter saved to event.cmd_text. 
Examples:
/sendevent HelloEvent 
/sendevent @test HelloEvent {data=1}
```

<!-- END_AUTOGEN-->
