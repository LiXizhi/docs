<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/runat`**

**quick ref:**
> /runat @name /any_command

**description:**

```
Run a local client side command at given player's console
@param @name: @all for all connected players. @name for given player name. `__MP__` can be ignored.
@param /any_command: if command is local, it can be sent to client for execution, otherwise it can only run on server.
Examples:
/runat @all /tip hello everyone    send message to every connected user
/runat @__MP__admin /tip hi, admin   send to admin host
/runat @admin /tip hi, admin         send to admin host
/runat @username /tip hi, username   send to a given user
```

<!-- END_AUTOGEN-->

在指定用户的电脑上执行本地命令。 

```
/runat @all /tip 大家好  发给所有人
/runat @admin /tip hi, admin    发给管理员
```