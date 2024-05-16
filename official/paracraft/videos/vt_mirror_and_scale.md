## 镜像与缩放教学

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/291/raw#7. 镜像与缩放教学.mp4
  ext: mp4
  filename: 7. 镜像与缩放教学.mp4
  size: 469351293
```
[在腾讯视频播放](https://v.qq.com/x/page/t0386wvwjti.html)

- `00'47s` `镜像`功能可将区域方块，根据指定中心点和方向对称复制
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Ctrl+左键`选中区域方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Alt+左键`设置中心点
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->点击左侧属性框中的`镜像`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->选择`镜像的轴x y z`，即镜像方向
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`复制方式`默认为`复制`；若选择`不复制`，则只显示镜像后的区域方块，原始区域方块消失
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->点击`确定`，区域方块即被对称复制
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Ctrl+Z`可撤销操作
- `05'02s` `/circle 10`：创建半径为10的圆形 
- `06'07s` 通过`/mirror`命令实现镜像：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->复制：`/mirror 对称轴 区域坐标 to 对称轴上任一点坐标`，例如`/mirror x 19298 64 19165 (10 0 10) to 19298 64 19172`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->不复制：`/mirror -no_clone 对称轴 区域坐标 to 对称轴上任一点坐标`，例如`/mirror -no_clone x 19298 64 19165 (10 0 10) to 19298 64 19172` 
- `09'08s` `缩放`功能可将区域方块，沿指定方向任意缩放
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Ctrl+左键`选中区域方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->鼠标移至左侧属性框中的`变换`：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Shift+左键`可将选中区域复制到鼠标所在位置
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Shift+点击左侧红绿蓝箭头`可将选中区域在三个方向上拉伸
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Ctrl -/+`可将选中区域缩放2倍
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->点击`变换`：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`x y z`为位移，可手工输入，也可用`-/+`调整
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Scaling`为缩放，可手工输入在三个方向上任意缩放，也可用`-/+`整体缩放2倍
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->点击`确定`，即可查看效果

### References
- [`/mirror`命令参考手册](cmd_mirror)
- [镜像与缩放教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=126)






