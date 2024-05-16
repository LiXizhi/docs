## 多次对话和交易教学



```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/408/raw#2. 多次对话和交易教学_0.mp4
  ext: mp4
  filename: 2. 多次对话和交易教学_0.mp4
  size: 407618307
```
[在腾讯视频播放](https://v.qq.com/x/page/j0381ilcxtm.html)



- `00'02s` 通过改变主角背包中两种物品的数量，实现多次对话。以木块 id:98 和金块 id:142 为例，实现三次对话：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` 命令方块，放入2个木块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`E键`-->`机关`-->`命令行`书
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` `命令行`书1-->`编辑`对话：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /text NPC说：请将2个木块换成2个金块`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 5 /text 我说：好的`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->点击`保存并关闭`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将`命令行`书1放在命令方块中2个木块后面，即当主角背包中木块的数量≥2，会触发`命令行`书1
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将1个木块和1个金块放在`命令行`书1后面，且与`命令行`书1空一格
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` `命令行`书2-->`编辑`对话：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /text NPC说：你已经成功将1个木块换成1个金块`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 5 /text 我说：好的`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将`命令行`书2放在1个木块和1个金块后面，即当主角背包中木块和金块的数量均为1，会触发`命令行`书2
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将2个金块放在`命令行`书2后面，且与`命令行`书2空一格
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` `命令行`书3-->`编辑`对话：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /text NPC说：你已经成功将2个木块换成2个金块，任务完成`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将`命令行`书3放在2个金块后面，即当主角背包中金块的数量为2，即触发`命令行`书3
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`E键`-->`机关`-->`红石线`
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将`红石线`放入两个空格，即将三部分连起来。`红石线`为or，或者的意思。当主角背包中木块和金块的数量分别达到以上三种状态中的一种，会触发相应的对话，而不会同时全部触发
- `06'08s` 将1个木块换成1个金块，实现交易：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将1个木块放入新建的命令方块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`右键单击` `命令行`书-->`编辑`命令：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`clearbag 98 1`：清除主角背包中1个木块
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`give 142 1`：给予主角背包1个金块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->将`命令行`书放在1个木块后面，即当主角背包中木块的数量≥1，会触发`命令行`书
- `07'57s` 查看效果
- `10'22s` 给物品改名字，以金块为例：
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->在下方常用物品栏黄框选中金块
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->回车，输入`/name 金元宝`，再次回车
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`Q键`丢弃金块，用主角重新拾取，即可查看效果
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->其他刷新方法：将金块和其他方块在常用物品栏或背包中交换位置；或将金块放入箱子后再取出

### References
- [`/text`命令参考手册](cmd_text)
- [`/t`命令参考手册](cmd_t)
- [`/clearbag`命令参考手册](cmd_clearbag)
- [`/give`命令参考手册](cmd_give)
- [`/name`命令参考手册](cmd_name)
- [多次对话和交易教学论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=84)