<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/open`**

**quick ref:**
> /open [-p] [-d] url

**description:**

```
open url in external browser
@param -p: if -p is used, it will ask user for permission. 
@param -d: url is a directory
Examples: 
/open http://www.paraengine.com
/open -p http://www.paraengine.com
/open npl://learn	open NPL code wiki pages
/open -d temp/
/open hello.html  open mcml file relative to world or root directory. Page is always center aligned and auto sized.
/open mcml://hello.html     same as above.  
```

<!-- END_AUTOGEN-->

- 如果URL以`http://`开头，则用外部浏览器打开。 
- 如果没有协议名或以`mcml://`开头, 则使用MCML v1显示一个可拖动的窗口。 窗口居中，大小根据内部MCML页面自动放缩。按ESC会自动关闭。文件路径可相对当前世界或者根目录。 例如：`/open hello.html`

例如: `hello.html`
```html
<pe:mcml>
<div style="background-color:#808080;padding:10px;max-width:500px;min-height:300px">
Please Enter Radius:<br/>
<input type="text" name="radius" value="4"/><br/>
<input type="submit" name="btnCreate" value="Create It!" /><br/>
</div>
</pe:mcml>
```

