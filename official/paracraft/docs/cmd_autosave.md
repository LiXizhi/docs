<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/autosave`**

**quick ref:**
> /autosave [-checkModified|stage|apply|rollback] [on|off] [mins]

**description:**

```
automatically save the world every few mins. 
@param interval: how many minutes to auto save the world. 
e.g.
/autosave        :enable auto save
/autosave on     :enable auto save
/autosave off    :disable autosave
/autosave on 10  :enable auto save every 10 minutes
/autosave -stage  :stage current world changes to temp folder which can be recovered later
/autosave -apply : apply staged changes usually from auto save folder in memory.
/autosave -rollback : rollback changes, a restart is preferred over rollback.
/autosave -checkModified on :enable auto save with world modified
/autosave -checkModified on 10:enable auto save with world modified every 10 minutes
```

<!-- END_AUTOGEN-->


- `/autosave -stage` 保存世界的修改到temp/autosave/目录
- `/autosave -apply` 从temp/autosave/目录恢复世界

世界在退出时都会执行`/autosave -stage`

1. 可编辑的世界无论以什么方式退出，只要有改动， 都会存一份（diff 增量，注意不是全量，备份是是全量，比较慢）到temp/autosave/目录下。 
1. 当下次加载世界时，如果存在temp/autosave/世界名+用户名的目录， 并且2边的revision相同。 则弹出一个黄色的确认条。
1. /reload和重启世界命令下， 不会自动autosave. 
4. 默认可编辑世界，每10分钟会自动存盘/autosave -stage 一次。 

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26639/raw#1684114344519image.png
  ext: png
  filename: 1684114344519image.png
  size: 43936
          
```

无论是只读世界，还是可编辑世界，Save As另存为时，如果世界有改动， 会询问是否要在副本中包含改动的部分。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26640/raw#1684114531615image.png
  ext: png
  filename: 1684114531615image.png
  size: '92791'
  unit: px
  alignment: left
  width: 399

```