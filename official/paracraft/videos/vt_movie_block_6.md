## 电影方块教学6

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/423/raw#8. 电影方块教学6_0.mp4
  ext: mp4
  filename: 8. 电影方块教学6_0.mp4
  size: 910892258
```
[在腾讯视频播放](https://v.qq.com/x/page/m0157t7jdgx.html)

- `00'10s` `/fov 1.04`：调整视角，默认值1.04，数值越大视角越扩张
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`00'53s` `/fov 1.5`：扩大，拉伸视角
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`06'49s` `/fov 1.04 10000`：第二个参数为视角变化的速度，速度越大变化过程越短
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`08'32s` `/fov 0.9`：缩进视角
- `10'10s` `/savetemplate aaa`：保存模板aaa，`Alt+左键`设置模板原点 
- `11'22s` `/loadtemplate aaa`：加载模板aaa
- `13'12s` `/savetemplate`保存的是`本地模板`（`E键`-->`模板`下），只可在当前世界中使用；通过界面操作也可存为`全局模板`，全局模板可在任意世界中共享使用
- `13'40s` `/loadtemplate -a 12 18791 70 18976 aaa`：以动画方式加载模板aaa
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`-a`：第一个参数为animation，即制作动画
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`12`：第二个参数为模板加载的时间，即12秒内
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`18791 70 18976`：第三个参数为原点坐标
- `15'19s` `/loadtemplate -r 18791 70 18976 aaa`：清除模板aaa
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`-r`：第一个参数为remove，即清除
- `18'43s` 镜子方块：`E键`-->`装饰`-->镜子 id:252，有反射效果，可DIY贴图
- `21'32s` 晃动，行进的镜头效果
- `22'42s` 演员动作与`/setblock`的配合 
- `25'03s` `/activate 19127 70 19337`：激活坐标方块
- `25'22s` 其他拍摄花絮 

### References
- [/loadtemplate命令教学视频](vt_loadtemplate)
  - [/savetemplate命令手册](cmd_savetemplate)
  - [/loadtemplate命令手册](cmd_loadtemplate)