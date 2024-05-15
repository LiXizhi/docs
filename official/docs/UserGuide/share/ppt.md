

## 内嵌3D世界到PPT文件

我们支持内嵌paracraft世界或keepwork可计算文档到PPT演示文件。 目前支持最新版的WPS和Microsoft Office。

- :heart: `浏览者无需安装任何插件`，可以直接查看PPT（支持Web、PC和MAC端）
- 下面指南仅针对PPT的作者

### WPS作者指南
- 安装WPS Office PC客户端
- 如果没有看到**安装**按钮, 请刷新网页并允许用WPS打开。

```@IFrame
styleID: 0
iframe:
  src: 'https://wps.keepwork.com/publish.html'
  width: 100%
  height: 450px
```

```@IFrame
styleID: 0
iframe:
  src: 'https://wps.keepwork.com/word_publish/publish.html'
  width: 100%
  height: 450px
```

安装完成后， 可以看到Paracraft菜单。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35799/raw#1711712285915image.png
  ext: png
  filename: 1711712285915image.png
  size: 813123
  isNew: true
          
```

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35801/raw#1711713531916可计算文档paracraft in WPS.mp4
  ext: mp4
  filename: 1711713531916可计算文档paracraft in WPS.mp4
  size: 14503711
  isNew: true
          
```


### Microsoft Office用户
- 开发者请安装 Webviewer Addin.


### 已知问题
-  WPS的F5播放模式下，鼠标右键和键盘不可用。 但是ms office没有这个问题。 请在非F5模式下使用，直到官方修复。
-  WPS webview做了24.5FPS的限制， ms office是可以60FPS的。
-  WPS webview不能缓存web paracraft的文件，首次打开比较慢。 ms Office没有这个问题，第二次打开速度很快。
-  WPS和MsOffice相互的webview不兼容。
-  WPS手机版暂时无法使用
-  WPS webview不支持预览图，在手机和ms office中显示为空图片。 ms office则会显示为世界的最近一次的预览图，但是没有3D交互。

### DEMO演示文档 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35800/raw#1711712618989可计算文档paracraft in WPS.pptx
  ext: pptx
  filename: paracraft in WPS.pptx
  size: 418631
  isNew: true
          
```