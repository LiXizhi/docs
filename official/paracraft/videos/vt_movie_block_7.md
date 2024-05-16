## 电影方块教学7：骨骼方块的原理与应用


```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/427/raw#11. 电影方块教学7_0.mp4
  ext: mp4
  filename: 11. 电影方块教学7_0.mp4
  size: 1529472920
```
[在腾讯视频播放](https://v.qq.com/x/page/r0315bgnr7x.html)

- `00'25s` 全选建筑模型：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`00'35s` `Ctrl+左键`选中建筑底部任一方块-->`全选按钮/Ctrl+A`：选中上方全部连通的方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'07s` `Ctrl+Shift+左键`：切换到单选，选中不相连的方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'30s` 全选后，直接拖动建筑上的`红绿蓝箭头`，移动建筑模型
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`02'51s` `Ctrl+Alt+左键`：过滤选中同种方块
- `03'40s` 骨骼方块的原理与应用：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`03'59s` `E键`-->`右键单击`骨骼方块-->进入它的详细帮助网页
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'06s` [骨骼的基本原理](item_Bone)
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`05'27s` 骨骼实例解析（风筝，狗链，自行车）：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`05'33s` 从任何一个子骨骼出发，沿着尖头的方向，依次指向父骨骼，最终指向根骨骼
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`06'34s` 当父子骨骼不在同一直线上时，可添加中间骨骼进行连接
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`08'44s` 在电影方块中，骨骼方块变为模型的骨骼结点。根骨骼影响所有子骨骼和整个模型，父骨骼只会影响后面的子骨骼和后面的模型
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`11'27s` 骨骼修改后，电影方块中的模型会失效，需重新添加
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`12'17s` 骨骼控制的方块，需要全部与骨骼方块相连。不相连的方块需用蜘蛛网连接
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`14'13s` 骨骼方块之间无需用方块相连，只要在同一条直线上即可
- `16'23s` 手部跟随：演员A自动跟随演员B的指定骨骼位移和旋转
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`16'47s` 添加演员A和B
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`17'02s` 选择演员B的骨骼，即要跟随的骨骼
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`17'27s` 切换到演员A的`父链接轴`-->`+`添加演员A需要跟随的父骨骼名称（系统默认为最近一次选择的骨骼）-->演员A自动来到演员B的指定骨骼-->可通过`红绿蓝箭头和圆环`调整演员A的相对位置和旋转
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`18'22s` 设置演员B的骨骼动作
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`19'05s` 拖动时间轴，演员A自动跟随演员B的骨骼一起运动
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`19'27s` 微调演员B的骨骼动作，演员A的位置和旋转也会自动随之调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`20'16s` 在父链接的模式下，调整演员A的位置和旋转，可做局部动画
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`21'05s` 演员A不会随演员B放缩，需到自己的大小轴进行放缩
- `23'58s` `快捷键2,2`：切换到骨骼位移
- `26'24s` `快捷键4`：切换到骨骼放缩，可在x,y,z三个方向上分别放缩，影响子骨骼
- `28'26s` 摄影机的位移和旋转：首先切换到摄影机，
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`28'29s` `快捷键4`：切换到摄影机大小，拖动`红绿蓝箭头`调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`29'18s` `快捷键2`：切换到摄影机位置，拖动`红绿蓝箭头`调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`29'41s` `快捷键3`：切换到摄影机三轴旋转，拖动`红绿蓝圆环`，实现摄影机的360度旋转  
- `30'31s` `/fog -color 1 1 1`：雾的颜色，默认RGB颜色1 1 1为白色，在非仿真天空下使用
- `32'49s` 图层字幕：以任意大小，角度，颜色，位置显示在电影中
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`33'26s` `左键单击`电影方块功能框中的空位-->点击`图层`-->`右键单击`切换到图层
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`33'49s` 切换到文字轴-->`+`添加文字
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`34'21s` `快捷键2,3,4`分别切换到位置，转身，大小-->拖动`红绿蓝箭头/圆环`调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`34'42s` 切换到颜色轴-->`+`添加RGB颜色，#ffffff为白色，#000000为黑色
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`36'03s` `快捷键3,3`切换到三轴旋转-->拖动`红绿蓝圆环`调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`36'46s` 切换到文字轴-->`+`添加空格空帧，字幕消失
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`37'41s` 切换到透明度轴-->`+`添加`0`透明，`1`不透明
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`38'21s` 切换到代码轴：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`38'38s` `+`添加颜色`color("#ff0000")`，文字`text("hello")`等渲染代码
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`39'33s` `+`添加文字代码`text("line2",0,16)`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`40'36s` `+`添加图片代码`image("1.png",300,200)`（世界文件夹下，鼠标移至图片，可见图片尺寸）
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`42'01s` 图层字幕可用`Ctrl+左键`复制，可保存空格缩进
- `43'13s` 通过在母电影方块中手工输入/修改子电影方块坐标，快速批量添加子电影方块
- `47'23s` 使用32位Paracraft程序时，如果编辑次数很多，建议重启客户端，防止内存不足引起死机