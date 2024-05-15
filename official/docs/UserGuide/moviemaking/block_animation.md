## 方块动画


### 1.实例目标：
>今天我们要学习用电影方块中的方块制作简单的方块小动画。

- 编辑电影方块，在左下角中选中方块帧进行。

### 2.教学内容
> 如何制作一个倒数爆炸的方块小动画：

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3454/raw#image.png
  ext: png
  filename: image.png
  size: 118515
          
```

### 3.进入课程世界参考效果


```@Project
styleID: 1
project:
  projectId: '1754'
  projectTagsShow: false
  projectMembersShow: false

```


### 4.制作步骤：

#### 第一步
> 用彩色方块搭建一面墙，在空地放置一个电影方块和一个按钮。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3462/raw#image.png'
  ext: png
  filename: image.png
  size: '149082'
  unit: px
  percent: '50'
  alignment: left
  width: 500

```

#### 第二步
> 打开电影方块，在第0秒将摄像机位置固定在白墙的中心，左侧时间轴的选项从文字改为方块，并将右侧的秒数从30变为7秒，如下图：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3463/raw#image.png'
  ext: png
  filename: image.png
  size: '220345'
  unit: px
  percent: '50'
  alignment: left
  width: 600

```

#### 第三步
> 在第0秒，白墙上搭建一个数字5后全选数字的范围，然后按最右下角的“+”添加一帧。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3464/raw#image.png'
  ext: png
  filename: image.png
  size: '74219'
  unit: px
  percent: '50'
  alignment: left
  width: 600

```

#### 第四步
> 在第1秒（1000的位置），白墙上搭建一个数字4（把之前的5变成4）后全选数字的范围，然后按最右下角的“+”添加一帧。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3465/raw#image.png'
  ext: png
  filename: image.png
  size: '63988'
  unit: px
  percent: '50'
  alignment: left
  width: 600

```

#### 第五步
> 如此做，在第2000/3000/4000/5000的位置分别加上数字3/2/1/0

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3466/raw#image.png'
  ext: png
  filename: image.png
  size: '70356'
  alignment: left
  unit: px
  percent: '50'
  width: 600

```

#### 第六步
> 我们在第6000/6100/6200/6300/6400/6500/6600这七个时间轴位置加上爆炸的效果：

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3467/raw#image.png'
  ext: png
  filename: image.png
  size: '127384'
  unit: px
  width: '600'
  alignment: left

```

### 更多可能性

- 你可以用方块动画制作一扇门，这样可以很好的阻止用户通过
- 你可以用方块动画制作大面积的照明，比如将某个区域替换为会发光的方块。
- 你可以用方块动画控制拉杆。
- 你可以用方块动画控制场景中的任意方块（包括代码方块，拉杆），只不过我们很少这样做。 比如0秒某个地方出现一个代码方块， 10秒时变成一个关闭的拉杆，20秒为一个打开的拉杆。