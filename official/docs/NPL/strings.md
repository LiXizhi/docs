## 字符串与文字
```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/357/raw#NPL CAD教学3.5.mp4
  ext: mp4
  filename: NPL CAD教学3.5.mp4
  size: 19233357
```
[在腾讯视频播放](https://v.qq.com/x/page/x03691lh7vr.html)


在计算机语言中，字符串(string)是一种最常用的存储单元的类型。例如`log("123")`中 双引号中的`123`代表一个长度为3的字符串。

> 字符串是一定长度的二进制数据。 

NPL语言中，字符串的长度单位是字节（Byte）。一个Byte包含8个Bit，也就是8个0或1的组合，因此一个Byte最多可代表2的8次方256种不同的组合。长度为1024的字符串就代表1KB的数据，1024KB=1MB（也就是1兆），1024MB=1GB

字符串的一个最大用途是用来代表自然语言中的文字。 字符串的每个Byte对应到文字的映射规则叫做编码。NPL中默认的编码规则叫做UTF8，UTF8是全世界使用最广泛的编码规则，几乎互联网上所有的文字都是这种编码。这种编码将每个英文字母或数字映射到一个Byte，将中文或其它特殊字符映射到2个或多个Byte。例如字符串"123"中每个数字字符都对应一个Byte，也就是对应256种0,1组合中的一种。

我们看到，代码本身就是由文字组成的。 在NPL中，所有在`""`或`''`的中的文字都是utf8编码的字符串。变量可以指向字符串，例如：
```lua
local a = "Hello"
local b = 'World'
```
这里介绍一个特殊的内置函数`..`, 例如`log(a..b)`：
```lua
local a = "Hello"
local b = 'World'
log(a..b)  
```
`..`函数可以将左右两侧输入的字符串合并，并输出一个新的合并后的字符串。`..`的作用类似`+号`函数，只不过输入是字符串。所以我们看到`log(a..b)`在左下角的输出为Hello与World合并后的新字符串，也就是"HelloWorld"。

除了`..`函数，NPL中还有很多其它操作字符串的函数。例如，在一个字符串中查找或匹配另外一组字符串。 但是这里我只介绍如何用大家熟悉的log函数来操作字符串。

log其实是一个多输入的函数。如果它的第一个输入是字符串，并且字符串中包含`%d,%s`等特殊占位符的文字，则它后面的输入会依次替换前面对应的占位符，并输出替换后的字符串结果。例如：
```lua
local a = "Hello"
local b = 'World'
log(a..b)
log("x=%d, y=%s, z=%d", 1, "hello", 2)
```
这里log的第一个输入是字符串，内容是`"x=%d,逗号空格 y=%s, 逗号空格z=%d"`。这里双引号中的所有文字，例如空格，等号，逗号都不是代码，而是字符串中的数据,　占一个Byte。log的第二个输入1会替换字符串中的第一个%d，第三个输入"hello"会替换%s，第4个输入2会替换后面的%d, 所以最后的输出为`"x=1, y=hello, z=2"`。　

`%d`代表替换的对象是一个十进制的整数(decimal)，也就是1和2; `%s`代表替换的对象是字符串, 也就是"hello"。注意这种替换规则只是log函数内部的逻辑，和字符串本身和NPL语言无关。只不过在很多语言中都有类似规则的函数。

下面我来随意练习一下，先注释掉之前的例子。我们敲入
```lua
local a = "Hello"
local b = 'World'
-- log(a..b)
-- log("x=%d, y=%s, z=%d", 1, "hello", 2)
log("pos:%f %f %f", 1.1, 1.2, 1.3)
```

`"pos:%f 空格%f空格 %f"`是一个字符串，%f之外的内容可以随意输入，中英文都可以，这里pos的中文意思是位置。
`%f`和`%d`一样，也是特殊占位符，只不过`%d`代表整数，`%f`代表浮点数(float)，默认会显示小数点后6个有效数字。我们再继续敲入：

```lua
local a = "Hello"
local b = 'World'
-- log(a..b)
-- log("x=%d, y=%s, z=%d", 1, "hello", 2)
log("pos:%f %f %f", 1.1, 1.2, 1.3)
log("Say %s ~ %s ~ \nSay%s", a, b, a..b) 
```
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2420/raw#image.png'
  ext: png
  filename: image.png
  size: '162752'
  unit: px
  width: '550'
  alignment: left

```

这里`"Say %s ~ %s ~ \nSay%s"`是一个字符串，其中`\n`是换行字符, 占一个Byte，也是字符串的一部分，`\n`会使log在屏幕上的输出另起一行。变量a代表字符串"Hello"，它会替换第一个%s; 变量b代表字符串'World'，它会替换第二个%s; `a..b`的输出是字符串"HelloWorld"，它会替换第三个%s, 所以log函数最后输出的是`Say Hello ~ World ~`，第二行就直接是`SayHelloWorld`, 中间没有空格。对于不清楚的内容，请大家自己写一些代码，进行大量的练习。　

这里再介绍一个非常用的操作字符串的函数format。format函数的输入和log函数非常类似，只不过它的输出为一个字符串。例如下面的代码和之前的结果是一样的。

```
local a = "Hello"
local b = 'World'
-- log(a..b)
-- log("x=%d, y=%s, z=%d", 1, "hello", 2)
local msg = format("pos:%f %f %f", 1.1, 1.2, 1.3)
log(msg)
msg = format("Say %s ~ %s ~ \nSay%s", a, b, a..b)
log(msg) 
```

字符串在计算机语言中使用十分广泛。 字符串中的文字可以用来代表文件名，变量的名字，屏幕上的文字或任何2进制数据。这些字符串的用法我会在后面的章节中继续讲解。