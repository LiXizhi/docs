## 程序的本质

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/354/raw#NPL CAD教学3.2.mp4
  ext: mp4
  filename: NPL CAD教学3.2.mp4
  size: 10164210
```
[在腾讯视频播放](https://v.qq.com/x/page/n0360pikfm0.html)


> 程序的本质就是输入和输出。

每一行语句就是将输入和输出连接起来，程序都是按一定顺序执行的，只有在上一行的输入和输出执行完毕后，才会启动下一行的输入和输出，也就是行与行之间是一种隐性的连接关系。


下面我们来看一个例子
```lua
-- 程序的本质
a = 3 + 4
log(a)
```
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2409/raw#image.png'
  ext: png
  filename: image.png
  size: '171422'
  unit: px
  width: '600'
  alignment: left

```

`a=3+4; log(a)` 运行后可以看到日志窗口中显示出了7。我们将右侧代码输入输出的连接关系以图形的方式展现出来。如下方左图:

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2411/raw#image.png'
  ext: png
  filename: image.png
  size: '144137'
  unit: px
  width: 500
  alignment: left

```


在这里3和4是输入，加号`+`是一个运算函数。关于函数的概念，我会在`2.7节`中给大家详细讲解。这里大家先简单地理解为对输入3和4进行加法运算并输出结果。等号`=`与加号`+`类似，也是一个运算函数，它的作用是将等号右侧的输入，也就是加号函数的输出，赋给等号左侧的输入，也就是将右侧3+4的输出结果7再作为输入赋给左侧的变量a。如上方右图，等号的左右两侧都是等号函数的输入，等号函数并没有任何输出。有些语言中例如C语言中，等号函数还会输出赋值后的结果，但是NPL语言中是不输出的。所以我们看到一行很简单的，看上去很像数学表达式的代码`a = 3 + 4`，其实是加号和等号两个函数输入和输出链接的结果，如下方左图。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2412/raw#image.png'
  ext: png
  filename: image.png
  size: '112780'
  unit: px
  width: '500'
  alignment: left

```

`a`是一个变量，在程序中没有加双引号的文字基本都是变量，纯数字和符号除外。更确切地说，由字母以及下划线组成的任意单词都是变量。如果在`log(a)`中将a的前后加上双引号`log("a")`，那么a就变成了字符串，左下角的日志窗口就会显示字母a而不是数字7。
```lua
a = 3 + 4
log(a)
log("a")  -- 显示字符串a
```
关于变量我会在`2.4节`中详细讲解。这里大家先简单地理解为变量就是某个存储单元的名字，变量默认会输出它所代表的存储单元，等号赋值除外。例如在`log(a)`中变量a会输出数字7，7又成为了log函数的输入。log函数最终在日志窗口中输出数字7，`log(3+4)`也会在左下角输出数字7，所不同的是3+4输出的结果7输入到log函数后会马上被系统释放掉。但是在`log(a)`中变量a始终指向7，所以a对应的存储单元中的7不会被马上释放。

一般来说，所有没有被变量命名的输出结果都会很快被系统自动释放掉，这样就不会占用计算机的内存了。内存是计算机的存储单元，程序在执行时，所有的代码，也就是输入输出函数等都会变成内存中的存储单元。也就是说上图中所有的圆圈都对应着内存中的存储单元，我们写的程序建立了这些存储单元之间的输入输出关系。

对于初学者来说，从这种视角看程序，会有些繁琐和复杂，但是它的确可以帮助初学者真正的理解代码的结构，等你阅读了大量代码后，你的大脑会自动的去理解这些输入输出的关系，你甚至感觉不到它们的存在。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2415/raw#image.png'
  ext: png
  filename: image.png
  size: '585525'
  unit: px
  width: '600'
  alignment: left

```

程序就如同我们的大脑。人类的大脑有上百亿的神经元细胞组成，每个神经元细胞有上万个来自其它神经元的输入和一个到其他神经元的输出，总共有百万亿的链接。如下图。


<div style="float:left;width:40%">
  
![图 2.2.1](https://api.keepwork.com/storage/v0/siteFiles/2413/raw#image.png)
  
</div>
<div style="float:left;margin-left:30px;width:40%">
  
![图 2.2.2](https://api.keepwork.com/storage/v0/siteFiles/2414/raw#image.png)
  
</div>
<div style="clear:both" />

所以人脑就像一台超级计算机，神经元的输入和输出的连接关系就如同我们的代码。NPL是一种高级语言，上面代码中的`log(a)`其实经历了很多你看不见的底层代码的输入和输出，最终才到达屏幕上你看见的由像素组成的数字7。

---

> 思考1： 上图中的代码和人脑有哪些相似的地方？

单项异步的输入输出连接

> 思考2： 什么是存储单元？

> 思考3： 计算机硬件中哪些是输入，哪些是输出？

> 思考4： 人体哪些是输入，哪些是输出？ 程序的本质是什么？