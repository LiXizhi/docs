# 高级渲染
- 支持跨平台DirectX/OpenGL渲染，支持多个级别的渲染管线, 兼容最古老的固定管线渲染。
- 支持实时阴影，延迟渲染管线(Deferred shading pipeline)和大量后期特效。
- 支持异步多线程资源加载，支持远程异步资源。
- 支持多视图与左右眼立体输出。
- 支持多线程异步地图生成，加载，与光照计算。 
- 支持BMAX方块模型自动LOD与面合并。
- 支持任意格式的音视频流媒体录制与导出。

关于图形渲染的更多内容请参考[NPL语言](NPL)中的ParaEngine引擎部分。 

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/6598/raw#image.png'
  ext: png
  filename: image.png
  size: '1649629'
  unit: '%'
  percent: '60'
  alignment: left

```


# 引擎性能
Paracraft是使用NPL语言编写的。NPL运行环境内置了ParaEngine3D引擎，引擎底层使用针对各个平台的C/C++代码完成，因此具有优越的性能。 

- 通过命令行，用户可控制Paracraft对内存和显存的使用上限，避免资源过渡消耗。
- 可随时查看当前系统的资源使用情况。


