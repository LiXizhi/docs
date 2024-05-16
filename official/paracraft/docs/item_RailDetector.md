<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**item: `探测铁轨`**

> * **name: ** RailDetector
> * **id: `251`**

<!-- END_AUTOGEN-->
用探测铁轨可以连接成铁路，矿车可以在上面行驶。
- 当矿车经过时，探测铁轨正下方的方块强充能。
并且
- 当矿车上无人时，经过探测铁轨周围4个方向的正下方方块不充能，也就是无法激活四周的中继器。
- 当矿车上有人时，经过探测铁轨周围4个方向的正下方方块弱充能，可以激活四周的中继器。

我们可以用这个方式来探测矿车中是否有人。 如下图：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4903/raw#image.png'
  ext: png
  filename: image.png
  size: '161112'
  unit: '%'
  percent: '40'
  alignment: left

```
当无人乘坐的矿车经过中继器时，无法激活中继器。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/5017/raw#image.png'
  ext: png
  filename: image.png
  size: '253071'
  alignment: left
  unit: '%'
  percent: 40

```

当有人乘坐的矿车经过中继器时，激活中继器。


 