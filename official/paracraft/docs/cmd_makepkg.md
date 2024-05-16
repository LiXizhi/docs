<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/makepkg`**

**quick ref:**
> /makepkg zip_src|package.txt [pkg_dest]

**description:**

```
make src zip file to dest pkg file. If dest is not provided, the src zip file extension is changed to pkg. 
pkg is an encrpted zip file and can be used interchangably with zip file in paracraft. 
e.g.
/makepkg test.zip  -- generate test.pkg
/makepkg main_mobile_res   -- internally used

It also takes a text file name, whose content is same as .gitignore, but has the reverse meaning. 
e.g. the following generate paracraft-mini.pkg and paracraft-mini.zip according to package list file
/makepkg packages/redist/paracraft-mini.txt 
```

<!-- END_AUTOGEN-->

/makepkg命令可以根据text文件打包生成pkg（zip）文件。
文件的格式和.gitignore很像，但是为相反的意思。 
> script目录下的脚本文件会被自动去掉注释，编译为bin/目录下的.o后缀文件。

例如: packages/redist/paracraft-mini.txt 文件内容如下：
```
config/
!config/*.xml
script/test/*.lua
Texture/kidui/main/cursor.tga
_emptyworld/_emptyworld.worldconfig.txt
_emptyworld/flat.raw
_emptyworld/flat.txt
/_emptyworld/*.db
script/apps/Aries/Creator/Game/Commands/CommandInstall.lua
```
文件名支持`*`通配符。 如果!开头则表示去除掉的文件。 如果/开头表示绝对路径。 

