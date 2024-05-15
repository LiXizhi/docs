## 智能模组

智能模组是可复用组件，通常是由一组代码方块构成的，如下图。 智能模组通常包括代码、模型、动画、美术资源等，可以打包为XML文件，上传到资源商城，被其他人使用。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26455/raw#1683265857858image.png
  ext: png
  filename: 1683265857858image.png
  size: '139032'
  unit: px
  width: '400'
  alignment: left

```

我们可以为一组相邻的方块添加一个`智能模组告示牌`，从而定义一个智能模组。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26454/raw#1683265075841image.png
  ext: png
  filename: 1683265075841image.png
  size: '50313'
  unit: px
  width: 200
  alignment: left

```

右键点击智能模组告示牌，可以编辑智能模组。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26456/raw#1683266041789image.png
  ext: png
  filename: 1683266041789image.png
  size: '65531'
  unit: px
  width: '400'
  alignment: left

```

每个智能模组有自己的名字，版本号和URL，如下图。模组支持自动升级，所以大家非必要，不要去编辑模组中的代码。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26457/raw#1683266322187image.png
  ext: png
  filename: 1683266322187image.png
  size: '176404'
  unit: px
  width: 600
  alignment: left

```
## 常用模组属性

- 文字颜色：属于自己的模组，告示牌上的文字为红色。 属于别人的模组，显示为蓝绿色。 
- 智能模块名称：建议用英文且唯一，例如：公司名.模块名。例如Paracraft.MyMod 
- 版本号：例如1.0.
- 更新方式：建议设置为手动。这样你可以随时右键告示牌并点击下载更新。 
- 外部文件：这里可以填写外部美术资源文件，详见后文。
- url地址：这个地址是自动生成的， 一般为项目id+本地路径。 

### 外部文件

有些智能模组可能会使用大量的外部文件，例如图片、bmax、声音文件等等。
格式为每行一个文件名或`filename,url`。如下

```javascript
img/test.png,https://api.keepwork.com/ts-storage/siteFiles/28975/raw#1691312622238image.png
img/filename.bmax,https://cdn.keepwork.com/username/img/filename.bmax?ver=1
```

- 如果格式为每行`文件名,url`，则代表为按需加载的美术资源。 
- 如果格式为文件名，后面没有逗号和URL，则表示这些文件需要直接从源项目世界中复制到当前世界。 

我们推荐尽量使用第一种方式，它的做法和在世界目录下增加一个assetmanifest.txt是一样的。 只有当美术文件被使用时，才会动态从CDN URL下载。

我们在保存世界时，也可以在世界目录下增加一个`.paraignore`文件, 在其中写入被忽略的文件的路径。注意对于第一种方式，引擎会先搜索当前世界目录下的文件， 如果不存在才会使用后面的URL下载。下载的URL一般会缓存在本地，所以如果你更新了同名的图片，最好也更新下URL，例如在URL后面加?ver=xxx，这样可以强制CDN重新下载。

### 世界目录下的assetmanifest.txt

有些世界需要使用很多静态的外部文件，例如图片、bmax、声音文件等等。
我们可以在世界目录下手工创建一个`assetmanifest.txt`, 内容为每行`文件名,url`， 例如：

```javascript
img/test.png,https://api.keepwork.com/ts-storage/siteFiles/28975/raw#1691312622238image.png
img/filename.bmax,https://cdn.keepwork.com/username/img/filename.bmax?ver=1
```

当世界加载时，这个映射被加载，离开世界时映射被清空。 当我们在世界中使用上述逗号左侧的文件时，引擎会先搜索当前世界目录下的同名文件， 如果不存在则会使用后面的URL下载。

下载的URL一般会缓存在本地，所以如果你更新了同名的图片，最好也更新下URL，例如在URL后面加?ver=xxx，这样可以强制CDN重新下载。

> TODO: 我们可以用`/download [assetmanifest.txt](assetmanifest.txt)` 将assetmanifest.txt中的所有文件都下载到当前世界目录下。 这种情况一般在发布离线世界安装包时有效，但是大多数情况下是不需要的。 

### 世界目录下的.paraignore文件

如果你希望分享世界时，世界目录下的某些文件不要上传，只保存在本地磁盘上，可以在世界目录下手工创建一个`.paraignore`文件， 内容为：

```javascript
img/test.png
img/filename.bmax
```

里面的内容有点类似`.gitignore`, 这样这些文件不会上传，但是在打包为p3d或离线安装包时会包含里面的文件。

### 分享智能模组

在paracraft中点击**资源库**，再点击代码可以查看别人分享的智能模组或提交自己的智能模组。智能模组需要通过**官方审核**才能被搜索到。

![1713252963788image.png](https://api.keepwork.com/ts-storage/siteFiles/36176/raw)



## 参考资料

- 如何发布官方Agent智能模组: [https://github.com/NPLPackages/Agents/wiki](https://github.com/NPLPackages/Agents/wiki)
- 《宏示教舞台》智能模组教学视频：https://keepwork.com/official/tips/s1/1_160

```javascript
```