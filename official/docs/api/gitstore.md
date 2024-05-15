## Git Store API

### zip包生成逻辑

用户上传更新世界，后台会异步的将用户世界打成zip包上传至七牛云的对象存储中，文件名以 `repoPath-commitId.zip`的方式命名，
保留规则：每个世界至少会保留最新的commitId的zip包，同时后台会定时删除超过七天且不是最新commitId的zip包。

### 客户端下载世界逻辑

第一步： 先从七牛云对象存储中获取zip包，链接为`https://qiniu-gitzip.keepwork.com/repoPath-commitId.zip`
返回200，则成功，return；
返回404，则说明zip包不存在，需要调用后端api接口去获取zip包，跳转至第二步

第二步：客户端调用 `https://apicdn.keepwork.com/core/v0/repos/:repoPath/download?ref=xxx`
获取zip包，其中`apicdn.keepwork.com`是对 `api.keepwork.com`域名做的CDN，仅用于zip包下载优化
如果未命中CDN缓存，则会从源站取，对于私有世界，并且用户无权限，则会返回403。
由于是回源机制， 对源站压力较大，CDN过期策略由CDN提供商决定，配置上是1年才过期。

### 客户端下载世界跳过私有判断

在第二步增加 `signature` 参数
生成规则为：`md5('repoPath:projectId')`