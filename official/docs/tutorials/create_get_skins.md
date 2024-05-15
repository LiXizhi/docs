## 如何获得和制作皮肤贴图文件?

有些3D模型允许你自己绘制人物皮肤，比如主角和电影角色。一般来说，模型的皮肤会使用1张或多张图片（贴图），每张图有自己的皮肤编号。

在电影方块中，你可以通过替换这些贴图，改变角色的皮肤，如下图。 注意：我们建议使用有透明通道的贴图，比如png格式的图片。 

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10025/raw#1581529358595image.png
  ext: png
  filename: 1581529358595image.png
  size: '43054'
  alignment: left
  unit: px
  width: 510

```

贴图是通过[UV坐标](https://baike.baidu.com/item/UV%E5%9D%90%E6%A0%87/971620)映射到3D模型上的，但是并不是所有模型都有UV坐标，比如BMAX模型没有UV坐标映射，所以无法换皮肤，只能改顶点颜色。 


下面是一些Paracraft中常用的可换皮肤的模型说明

### 电影通用角色（方块人）
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10023/raw#1581529085829image.png
  ext: png
  filename: 1581529085829image.png
  size: '37083'
  alignment: left
  unit: px

```

- 皮肤编号2： 可换全身贴图， 下图为示例

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/10022/raw#1581528941785red.png'
  ext: png
  filename: 1581528941785red.png
  size: '20804'
  alignment: left
  unit: px
  width: 256

```

由于方块人模型的贴图UV坐标兼容minecraft的主角，所以你可以使用第三方开发的mcskin编辑工具制作贴图，点击下方下载。 

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10027/raw#1581530410369Skin3D_1.6.0.603.zip
  ext: zip
  filename: Skin3D安装包_1.6.0.603.zip
  size: 2572431
          
```

---

### 主角（纸盒人）
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10024/raw#1581529220638image.png
  ext: png
  filename: 1581529220638image.png
  size: '69568'
  alignment: left
  unit: px
  width: 128

```

- 皮肤编号2： 上衣
- 皮肤编号3： 眼睛
- 皮肤编号4： 嘴巴

眼睛和嘴巴贴图下载：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10089/raw#1581699321450表情贴图.zip
  ext: zip
  filename: 表情贴图.zip
  size: 1033652
          
```


```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10019/raw#1581528546627image.png
  ext: png
  filename: 1581528546627image.png
  size: '87730'
  alignment: left
  unit: px
  width: 500

```

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/10020/raw#1581528591937image.png
  ext: png
  filename: 1581528591937image.png
  size: '20622'
  alignment: left
  unit: px
  width: 500

```