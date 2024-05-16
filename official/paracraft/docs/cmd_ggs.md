**command: `/ggs`**

**quick ref:**
> /ggs subcmd [options] args...

**description:**

general game server  = 通用游戏服务器，是我们用NPL写的一个通用联机服务器。 
ggs一般用于同步多名在线玩家虚拟角色的实时位置、动作和外观，也可以在玩家间发送消息，同步数据。
ggs是无状态服务器，或者说至少有1名用户连接时才保存内存状态。 当玩家下线时，服务器数据可能会被自动回收。 

```
subcmd: 
connect 连接联机世界
	/ggs connect [options] [worldId] [worldName]
	/ggs connect -isSyncBlock -isSyncCmd -areaSize=64 -silent -editable 12706
disconnect 断开连接
	/ggs disconnect
cmd 执行软件内置命令
	/ggs cmd [options] cmdname cmdtext
	/ggs cmd tip hello world	
setSyncForceBlock 强制同步指定位置方块(机关类方块状态等信息默认是不同步, 可使用该指令强制去同步):
	/ggs setSyncForceBlock x y z on|off
	/ggs setSyncForceBlock 19200 5 19200 on   强制同步位置19200 5 19200的方块信息
	/ggs setSyncForceBlock 19200 5 19200 off  取消强制同步位置19200 5 19200的方块信息
user 用户命令
	/ggs user visible           显示所有用户 不包含主玩家
	/ggs user hidden            隐藏所有用户 不包含主玩家
	/ggs user enableclick       玩家可点击
	/ggs user disableclick      玩家不可点击
offlineuser 离线用户命令
	/ggs offlineuser visible    显示离线用户
	/ggs offlineuser hidden     隐藏离线用户
setNewLiveModelAutoSync 新增活动模型是否同步(默认为 on)
	/ggs setNewLiveModelAutoSync on    允许新增活动模型同步
	/ggs setNewLiveModelAutoSync off   禁止新增活动模型同步
setLiveModelAutoSync            所有活动模型是否同步(默认为 on)
	/ggs setLiveModelAutoSync on    允许活动模型同步
	/ggs setLiveModelAutoSync off   禁止活动模型同步
showuserinfo                     显示用户信息
	/ggs showuserinfo [username]
debug 调试命令 
	/ggs debug [action]
	/ggs debug debug module 开启或关闭指定客户端模块日志
	/ggs debug serverdebug module 开启或关闭指定服务端模块日志
	/ggs debug options       显示客户端选项信息
	/ggs debug playerinfo    显示客户端所在世界的玩家信息
	/ggs debug worldinfo     显示客户端所在世界的信息
	/ggs debug serverinfo    显示客户端所在服务器信息	
	/ggs debug serverlist    显示全网服务器列表
	/ggs debug statistics    显示全网统计信息
	/ggs debug ping          验证是否是有效联机玩家
	/ggs debug syncForceBlockList 显示强制同步块列表
filesync
	/ggs filesync            同步所有文件
	/ggs filesync filepath   同步指定文件
blockly 图块编程	
developer                    GGS 开发者模式
```


## 关于自动分流
默认情况下GGS单个服务器最大人数配置是100人（可配置），梯度为20人（不可配置）。 自动分流原则如下。

- 当服务器人数小于(100-20)时，服务器优先级为math.ceil(（userCount-20）/ 20)
- 当服务器人数大于(100-20)时，服务器优先级为 0 
- 用户总会进入服务器优先级最高的服务器；优先级相同时，会用最先创建的服务器。 
- 单个服务器超过最大人数100时，会自动开启一个新的服务器。
- 当服务器人数为0一段时间后会自动销毁。 


举例：
- 第1-100个用户登录时进入S1服务器（S1由于超过80人，优先级从4降为0）
- 第101个用户会进入S2. 假设S1的用户都没有离开世界，则后来102-180个用户都会流入S2. 
- 此时假设原来S1中的100个用户逐渐离开，在线降到了60人，而S2中还省70人。 这时S2的优先级（4）会高于S1（3）. 后来的用户会持续的进入S2，直到S2的人数也到达了80人，优先级变成了0. 后面的用户又会流入S1. 

总之，就是用户总是优先装满80人，让服务期尽量的热闹，而不是平均分配人数。 这样做可以应对家长会这样的高峰流量，让人少的服务器尽快人数降为0，新人总是去人多的服务器。 










