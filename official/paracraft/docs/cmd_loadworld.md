<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/loadworld`**

**quick ref:**
> /loadworld [worldname|url|filepath]

**description:**

```
oad a world by worldname or url or filepath relative to parent directory
@param -i: interactive mode, which will ask the user whether to use existing world or not. 
@param -e: always use existing world if it exist without checking if it is up to date.  
@param -s: slient load.
@param -d: download the world without loading it. Upon finish, it will /sendevent download_offline_world_finish project_id
@param -forcedownload: always download(again) online world without checking if it is different to local. 
@param -auto|-force: it will check local world revision with remote world, and download ONLY-if remote world is newer. 
@param -inplace: if the entered world is equal to the current world, the subsequent /sendevent command will be executed directly. otherwise, the command will be executed after entering the world. For security reasons, only event that begins with "global" can be sent
@param -personal: login required. always sync online world to local folder, then enter.
e.g.
/loadworld 530
/loadworld https://github.com/xxx/xxx.zip
/loadworld -i https://github.com/xxx/xxx.zip
/loadworld -e https://github.com/xxx/xxx.zip
/loadworld -force 530
/loadworld -personal 530
/loadworld home
/loadworld back
/loadworld -s -inplace 530 | /sendevent globalSetPos  {x, y, z}
/loadworld -d 530

```

<!-- END_AUTOGEN-->
加载一个世界的名称或压缩文件或文件相对路径目录。