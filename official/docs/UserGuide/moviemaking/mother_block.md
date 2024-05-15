 

## 子母电影方块


**1. 理论**
>思考：当电影场景中如何精确的控制多个电影方块播放的次序和时间？

我们可以用一个电影方块去控制其它电影方块的播放和终止时间。此时那个控制其它电影方块的方块叫做母电影方块。 
而被控制的电影方块叫做子电影方块。 我们可以在母电影方块的时间轴上添加子电影方块，达到对大量电影方块播放的精确控制。
这种方法比用中继器和导线连接多个电影方块的方法更加精确，尤其是当我们需要跨域多个电影方块去精确配音时。

**2.实践**
> 一般我们需要先删除母电影方块中的摄影机。
> 将母电影方块切换到子电影方块轴后，按Ctrl+左键选中子电影方块，按+号添加关键帧。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2984/raw#image.png'
  ext: png
  filename: image.png
  size: '131000'
  unit: px
  alignment: left
  percent: '50'
  width: 550

```

<div style="float:right;margin-left:10px;width:250px">
  
![图 1.3.7](https://api.keepwork.com/storage/v0/siteFiles/2988/raw#gol_block.png)
  
</div>

**步骤1：在场景中放入几个电影方块，分别制作里面的电影片段**

**步骤2：在母电影方块中插入背景音乐**

> 将母电影方块切换到背景音乐轴，按+号添加xxx.mp3/ogg


**步骤3：通过在母电影方块中手工输入/修改子电影方块坐标，快速批量添加子电影方块**

> 在母电影方块中连续查看子电影方块：右键切换到命令序列–>点击播放/暂停–>右键单击时间轴的任意时刻，音乐停止

<div style="clear:both"/>
<div style="float:right;margin-left:10px;width:250px">
  
![图 1.3.8](https://api.keepwork.com/storage/v0/siteFiles/2990/raw#gol_block.png)
  
</div>

**步骤4：播放母电影方块即可看到全部子电影方块**