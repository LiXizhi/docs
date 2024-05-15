Paracraft 生成IOS App 使用说明
- 前置条件：
   + 硬件要求：
       MAC电脑一台 （系统版本：macOS 11.6以上）

   + 软件要求：
       Paracraft (Version: 1.0.131及以上，推荐使用最新版）
       Xcode   （Version: 13.2.1及以上)
       Terminal （Version: 2.11及以上）

   + 网络要求：
       正常联网

-  整体流程说明：
1. 打开paracraft，找到“生成独立应用程序”功能
2. 点击“一键生成”，生成IOS 工程项目文件
3. 直接打开工程项目文件或者打开XCode引入（前提：已经安装Xcode）
4. 选择生成目标paracraft进行应用名称/应用版本号/应用图标及签名设置
5. 设置完毕后，连接上真机或者启用模拟器进行构建
6. 将构建的文件通过应用商店进行发布

-  详细步骤： 
1. 打开paracraft，登录后找到“生成独立应用程序”功能   
登录账号：
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21486/raw#1646114892373image.png
  ext: png
  filename: 1646114892373image.png
  size: '508116'
  alignment: left
  unit: '%'
  percent: 80

```
进入你想生成App的世界， 打开菜单栏-文件-生成独立应用程序
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21487/raw#1646114923207image.png
  ext: png
  filename: 1646114923207image.png
  size: '3361653'
  alignment: left
  unit: '%'
  percent: 80

```

2. “生成独立应用程序”功能：点击iOS图标 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21503/raw#1646115483448image.png
  ext: png
  filename: 1646115483448image.png
  size: '3325007'
  alignment: left
  unit: '%'
  percent: 80

```


3. 使用“一键生成”生成IOS 工程文件 （预计等待时长为20～30分左右，具体视机器及网络情况而定,可喝个coffee，稍后再来）

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21491/raw#1646115207381image.png
  ext: png
  filename: 1646115207381image.png
  size: '3137597'
  alignment: left
  unit: '%'
  percent: 80

```


4. 当出现terminal弹窗时，请手动输入：
sh build.sh (可直接拷贝复制使用）
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21492/raw#1646115237506image.png
  ext: png
  filename: 1646115237506image.png
  size: '183513'
  alignment: left
  unit: '%'
  percent: 80

```
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21493/raw#1646115266529image.png
  ext: png
  filename: 1646115266529image.png
  size: '213509'
  alignment: left
  unit: '%'
  percent: 80

```


5. 打开生成的IOS工程项目文件，打开Xcode->Preferences ->Accounts 里添加苹果开发者账号。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21494/raw#1646115281568image.png
  ext: png
  filename: 1646115281568image.png
  size: '3146438'
  alignment: left
  unit: '%'
  percent: 80

```
6. 输入加入开发权限组的AppleID
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21495/raw#1646115292025image.png
  ext: png
  filename: 1646115292025image.png
  size: '46521'
  alignment: left
  unit: '%'
  percent: 80

```
7. 修改配置

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21496/raw#1646115307951image.png
  ext: png
  filename: 1646115307951image.png
  size: '106310'
  alignment: left
  unit: '%'
  percent: 80

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21497/raw#1646115324333image.png
  ext: png
  filename: 1646115324333image.png
  size: '100245'
  alignment: left
  unit: '%'
  percent: 80

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21498/raw#1646115335612image.png
  ext: png
  filename: 1646115335612image.png
  size: '81289'
  alignment: left
  unit: '%'
  percent: 80

```

8. 已生成项目归档 product- archive
 

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21499/raw#1646115382643image.png
  ext: png
  filename: 1646115382643image.png
  size: '1057773'
  unit: '%'
  percent: '80'
  alignment: left

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21500/raw#1646115394318image.png
  ext: png
  filename: 1646115394318image.png
  size: '281353'
  alignment: left
  unit: '%'
  percent: 80

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21501/raw#1646115406063image.png
  ext: png
  filename: 1646115406063image.png
  size: '484887'
  alignment: left
  unit: '%'
  percent: 80

```


```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/21502/raw#1646115425869image.png
  ext: png
  filename: 1646115425869image.png
  size: '437784'
  alignment: left
  unit: '%'
  percent: 80

```