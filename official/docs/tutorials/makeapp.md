# 生成独立应用程序

在菜单中选择`文件|生成独立应用程序`， 我们可以将一个或多个世界发布为独立应用程序。 也可以使用`/makeapp`命令。 

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29092/raw#1692250511200image.png
  ext: png
  filename: 1692250511200image.png
  size: '81986'
  isNew: true
  unit: px
  width: 450

```


### 如何设置Loading背景图
如果世界目录下有 `frontpage.png` 或 `frontpage_32bits.png` 或 `frontpage.jpg`
则这幅图将作为启动的Loading图片，建议图片大小为512X288。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29095/raw#1692252897831image.png
  ext: png
  filename: 1692252897831image.png
  size: 113725
  isNew: true
          
```

## Windows平台
打包完成后，将生成
- `bin/` 目录包含paracraft引擎文件和临时下载的文件
- `data/` 目录包含当前世界的文件
- `start.bat` 启动文件，双击可运行
- `【世界名】.zip` 包含了上述文件的zip包，可发送给别人下载体验。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29094/raw#1692251171781image.png
  ext: png
  filename: 1692251171781image.png
  size: 5562
  isNew: true
          
```


> :point_right: 重要注意事项: 请复制上面所有文件到非中文路径下，再执行start.bat

例如:
```
c:\temp\start.bat
c:\temp\bin\
c:\temp\data\
```
如果使用zip文件，也请解压到非中文路径下。 

> :heart: 建议多运行几次start.bat, 然后再手工打包为*.zip文件（注意不要打包zip文件）， 进行发型。 这样可以保证所有在线资源都已经下载到bin/temp目录中。 


## Android平台
首次安装需要下载Android环境，格局指引打包即可

