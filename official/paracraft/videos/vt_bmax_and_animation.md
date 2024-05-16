## Bmax与骨骼系统教学



```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/421/raw#10. Bmax与骨骼系统教学_0.mp4
  ext: mp4
  filename: 10. Bmax与骨骼系统教学_0.mp4
  size: 2016590634
```
[在腾讯视频播放](https://v.qq.com/x/page/s0307ngu8tp.html)

- `00'11s` `Bmax`：`Block Max`方块模型，用来制作精致的静态和动态道具
- `00'19s` 静态道具的制作与使用：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`00'19s` 先用彩色方块搭建所需道具，大小不超过`64x64x64`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`01'50s` `Ctrl+左键`选中道具-->`保存`-->存为bmax模型
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`03'01s` 在电影方块中添加演员-->点击人物模型右侧的`省略号按钮`-->点击`blocktemplates`文件夹-->选择bmax模型文件
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`03'46s` `右键单击钥匙按钮`解锁模型-->将模型移动至场景中-->`K键`K帧记录位置
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'55s` `快捷键4`切换到大小轴-->调整视角-->拖动`红绿蓝箭头`调整大小
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`06'16s` `快捷键3`切换到转身轴-->拖动`蓝色圆环`调整转身角度
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`06'28s` `快捷键3,3`切换到三轴旋转-->拖动`红绿蓝圆环`调整旋转角度
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`07'17s` `快捷键2`切换到位置轴-->拖动`红绿蓝箭头`调整位置
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`08'13s` `Ctrl+左键`复制演员-->调整新演员位置-->`设置属性`-->取名字，用来区分演员
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`09'05s` 将新演员切换到模型轴-->`右键`编辑关键帧-->修改模型名字，更换模型
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`11'24s` 模型位置，大小和三轴旋转等也可`右键`编辑关键帧，通过数值来精确调整
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`14'36s` 演员头部运动也可通过拖动`红蓝圆环`来调整
- `15'13s` 人物骨骼与表情：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`15'19s` `快捷键1,1`切换到骨骼轴（左下方绿色提示为`全部骨骼`）-->点击`骨骼关节`，出现该关节的三轴旋转圆环（绿色提示为该关节的名字，表示进入了该关节的`专属骨骼轴`）-->拖动`红绿蓝圆环`调整骨骼旋转角度
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`16'18s` 后背`Spine`骨骼比较特殊：调整`Spine`骨骼，会在四肢骨骼轴上自动生成关键帧
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`19'11s` 使用`反向动力学`：点击`手臂末端关节`-->通过调整骨骼末端的位置，自动生成上面两根父骨骼的旋转关键帧。`浅蓝色箭头`代表`反向动力学`，拖动它可使大臂和小臂一起联动，相当于调整了大臂和小臂的两套圆环，会自动在大臂和小臂的骨骼轴上生成关键帧，在反向动力学本身的骨骼轴上没有生成帧
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`21'24s` `Esc键`退出当前关节的`专属骨骼`，回到`全部骨骼`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`22'52s` 在头部骨骼的初始位置K帧，可防止头部受编号动作的影响
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`26'50s` 演员在不同的骨骼关键帧之间平滑地运动
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`27'59s` 在某关节的专属骨骼轴上复制关键帧，只是复制了当前一个关节的骨骼状态
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`29'42s` 在`全部骨骼`轴上复制关键帧，则是复制了当前带关键帧数据的所有骨骼的状态
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`32'45s` 若要手持道具随手部一起运动，则道具相对于手部的位置要保持不变
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`34'30s` 在调整模型位置，大小和三轴旋转等之前，要先将时间轴拖动到正确的位置
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`35'57s` `/hide`：隐藏当前控制的人或物
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`36'37s` 人物表情：点击`嘴部关节`（`眼部关节`同理）-->`快捷键2,2`切换到骨骼位移-->K帧记录初始骨骼-->拖动时间轴-->拖动`红绿蓝箭头`调整嘴部骨骼
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`38'10s` 若骨骼轴初始位置无关键帧，在中途位置K帧，初始位置会自动生成相同的关键帧
- `41'18s` 动态道具的制作与使用：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`41'33s` `E键`-->`电影`-->骨骼方块 id:253
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`41'57s` 每个骨骼方块可以控制与它相连的方块，尖头的一端除外；被控制的方块默认不动
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`42'43s` `Ctrl+右键`选中骨骼方块-->骨骼方块之间出现红色连线-->`右键单击`骨骼方块中心的圆圈-->进入该骨骼方块的背包-->输入特定的骨骼名字，如`wheel`-->点击任意位置退出骨骼选择
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`43'20s` 将整个道具（包括其中的骨骼方块）选中，存为bmax模型
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`44'05s` 将模型添加至电影方块，并移动到场景中
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`45'25s` `快捷键1`切换到动作轴-->添加动作编号`4`（走路）-->`wheel`骨骼会带动模型转起来
- `57'20s` `/hide player`：隐藏主角
- `57'33s` `/show player`：显示主角
- `58'56s` `/setblock 17956 11 18712 50 2439`：通过`/setblock`命令生成带有颜色的金属方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`17956 11 18712`：位置坐标
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`50`：金属方块id
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`2439`：颜色数值，可在`F3键`下找到
- `1:00'08s` `/setblock`等命令使用的是方块坐标，演员位置使用的是实数坐标，可在`F3键`下查看