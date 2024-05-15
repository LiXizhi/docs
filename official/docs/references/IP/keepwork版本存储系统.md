# keepwork版本存储系统 v1.0

**软件用途：** 该系统用于高速存储、读取文件、文档等数据。且该系统对数据具有版本控制功能，系统对同一数据的所有历史版本都会留下记录，用户可以回溯、取回数据的任意历史版本。
**运行环境:** Windows/Mac/Linux/Android/IOS
**编程语言：** Node.js(JavaScript)
**开发完成时间：** 2018年9月30日
**发表日期：** 2018年9月30日
**技术特点：** 该产品在技术方面支持以下功能
- 高速存储、读取、管理文件、文档数据
- 回溯数据的任意版本

**源代码行数**: 1万行  [点击这里查看](keepwork版本存储系统_code)

# 《支持版本管理的数据存储系统》使用手册
- 根据各接口参数格式调用系统的http接口写入/读取数据。
- 调用接口获取历史版本列表，根据版本号取回历史数据。
- 接口文档如下


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/4238/raw#image.png
  ext: png
  filename: image.png
  size: 1437194
```