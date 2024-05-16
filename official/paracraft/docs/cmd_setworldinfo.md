## /setworldinfo

/setworldinfo [-isVipWorld true|false]
命令描述
set a given world tag
--this will make world accessible to only vip users
/setworldinfo -isVipWorld true    
/setworldinfo -selectWater true    
/setworldinfo -assetUrl "https://some_cdn_url.zip"



### 设置世界外部美术资源路径 
可以是另外一个世界的存档连接。 必须是zip文件。 

```
/setworldinfo -assetUrl "https://api.keepwork.com/ts-storage/siteFiles/27082/raw#1686815518839CodeBlockTest_20220627_693.zip"
```

也可以通过F11，选择WorldCommon 然后选择world_info, toolbase的AssetUrl，如下图所示。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/27083/raw#1686815732769image.png
  ext: png
  filename: 1686815732769image.png
  size: 62123
          
```

在E键菜单的模板中可以看到外部的bmax模型。 