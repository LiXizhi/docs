# 仿真与SDK开发包
NPL语言起源于2004年的一个人工智能研究项目。 ParaEngine引擎和Paracraft从诞生那一天，就首先被定位为研究人工智能算法的3D仿真平台。因此Paracraft PC版本身包含了完整的NPL语言运行与开发环境。 用户可以使用Paracraft开发和调试NPL代码，写基于Paracraft的插件或独立的App应用程序。

- Paracraft作为一个3D编辑器，更注重创作的便捷性和扩展性，一定程度上放弃了写实，原因是我们希望降低故事创作的成本和周期，同时方便世界的数据作为人工智能或仿真算法的输入和输出，降低算法的计算量。
- 用户可以在3个层次上对世界进行仿真： 1. 通过物品的UI界面  2. 通过命令行  3. 通过NPL语言。 我们希望用户的学习可以越来越深入，直到接触NPL语言。 
- 世界中的每个方块都支持记忆学习和编程。


# 插件库 & NPL开源社区
NPL/Paracraft是开源的， 任何人都可以上传插件到keepwork网络平台。 用户可以方便的加载，卸载插件。 所有只使用NPL语言的插件都是跨平台的。Paracraft安装包内置了几个常用的开源系统插件，例如NPL CAD, ParaX导出工具等。
请注意，插件通常具有很高的文件访问权限，请谨慎安装。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/12627/raw#1588753463177image.png
  ext: png
  filename: 1588753463177image.png
  size: 90951
          
```

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/12628/raw#1588753499089image.png
  ext: png
  filename: 1588753499089image.png
  size: 94836
          
```


## 如何参与开发？

请阅读： https://github.com/LiXizhi/ParaCraftSDK

NPL开源类库：
- https://github.com/nplpackages
- https://github.com/tatfook
- https://github.com/lixizhi