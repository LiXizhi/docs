# 3D电影制作

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8270/raw#动画电影.mp4
  ext: mp4
  filename: sunclock.mp4
  size: 11528698
          
```


#### 电影方块
电影方块是paracraft的核心功能，我们利用电影方块中的摄影机、演员、字幕、声音、特效等，制作从简单到复杂的3D电影动画。
注：
按钮：id:105，用于启动电影方块
中继器：id:197，指示信号输出方向，连接多部电影的工具
红石线：id:189，传递能量，可选择使用。

 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8343/raw#1574751809542image.png
  ext: png
  filename: 1574751809542image.png
  size: '146999'
  unit: '%'
  percent: '60'
  alignment: left

```



#### 电影演员
添加各式各样的演员，如可爱的卡通人物、交通工具、魔法特效等。通过角色扮演录制动画，使演员在电影动画中动起来。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8341/raw#1574751726029image.png
  ext: png
  filename: 1574751726029image.png
  size: '64723'
  unit: '%'
  percent: '60'
  alignment: left

```


#### 时间轴
在电影方块界面的屏幕底部有一段长条的蓝色时间线，它就是电影方块的时间轴。
时间轴的右边显示的是时间轴的总长度，是以秒为单位的（数值默认30即代表30秒），我们可以输入数字更改时长。
拖动时间轴上的灰色按钮用来调整当前所在时间，灰色按钮上面的时间是以毫秒为单位，比如现在我们在 1000 （毫秒）的位置，也就是当前时刻在 1 秒。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8344/raw#1574751842055image.png
  ext: png
  filename: 1574751842055image.png
  size: '9126'
  unit: '%'
  percent: 80
  alignment: left

```


#### 摄影机与关键帧
摄像机主要功能是记录演员以及镜头发生的一切静、动态，形成镜头语言展现出最终的电影画面。
在键盘上按WASD移动摄像机。
`注：建议先学习基本的镜头语言（中，近，远景镜头，与蒙太奇等）。
如果我们想让摄影机沿着一定的轨迹移动，那么这条轨迹的起点和终点就是关键帧。换句话说，摄影机总是在两个关键帧之间移动的。我们调整好摄影机起点和终点的位置角度，在时间轴上分别添加两个关键帧（快捷键 K 键）。然后摄影机会在两个关键帧之间自动匀速平滑地移动，记录两个关键帧之间的镜头语言。`

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8340/raw#1574751666188image.png
  ext: png
  filename: 1574751666188image.png
  size: '989190'
  unit: '%'
  percent: '60'
  alignment: left

```



#### 多个电影方块链接与子母电影方块
一部视频的创作往往需多个镜头和场景进行拍摄，用中继器链接多个电影方块，退出电影方块编辑页面可以使用按钮来播放电影。当电影方块需要跨多个电影方块去精确配音以及需要用到很多演员时，我们可以用一个电影方块去控制其它电影方块的播放和终止时间。此时那个控制其它电影方块的方块叫做母电影方块。而被控制的电影方块叫做子电影方块。 我们可以在母电影方块的时间轴上添加子电影方块，达到对大量电影方块播放的精确控制。

 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8339/raw#1574751471939image.png
  ext: png
  filename: 1574751471939image.png
  size: '480473'
  unit: '%'
  percent: '60'
  alignment: left

```



#### 支持1080p 多格式电影导出
首次导出电影需要下载官方插件，按F9录制完成后即可导出。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8337/raw#1574751234700image.png
  ext: png
  filename: 1574751234700image.png
  size: '90197'
  unit: '%'
  percent: '60'
  alignment: left

```


```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/8338/raw#1574751315596image.png
  ext: png
  filename: 1574751315596image.png
  size: '80342'
  unit: '%'
  percent: 40
  alignment: left

```


- 支持360度VR全景实时输出
   - 支持所有VR设备，例如PICO, VIVE, OCULUS等
- 也支持传统的红蓝、左右眼立体输出。
   - 详情请见：https://keepwork.com/official/tips/s1/1_74
   
   