## Tip命令教学


```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/403/raw#1. Tip命令教学_0.mp4
  ext: mp4
  filename: 1. Tip命令教学_0.mp4
  size: 124204737
```
[在腾讯视频播放](https://v.qq.com/x/page/c0386xbp99k.html)

- `00'02s` 用[`/tip`提示命令](cmd_tip)实现倒计时显示：3, 2, 1, Start!
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`00'23s` 显示多行tips提示：
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /tip 3`：第1秒显示`3`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip 2`：过1秒显示`2`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip 1`：过1秒显示`1`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip Start!`：过1秒显示`Start!`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~2 /tip`：过2秒tip结束
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`02'18s` 单行替换名称为`a`的tip：`/tip -a`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /tip -a 3`：第1秒显示`3`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip -a 2`：过1秒替换显示`2`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip -a 1`：过1秒替换显示`1`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~1 /tip -a Start!`：过1秒替换显示`Start!`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~2 /tip -a`：过2秒tip结束
  - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`04'06s` 同时显示两条不同名称的tips：在显示`/tip -a`的同时显示`/tip -b`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t 1 /tip -b this is a game`：第1秒同时显示`b`提示`this is a game`
     - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->`/t ~0.1 /tip -b`：过0.1秒`tip -b`结束   

### References
- [`/tip`命令参考手册](cmd_tip)
- [`/t`命令参考手册](cmd_t)
- [`/tip`命令论坛链接](http://bbs.paraengine.com/forum.php?mod=viewthread&tid=99)