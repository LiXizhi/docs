## 表与数组
```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/358/raw#NPL CAD教学3.6.mp4
  ext: mp4
  filename: NPL CAD教学3.6.mp4
  size: 31668775
```
[在腾讯视频播放](https://v.qq.com/x/page/t0378skh757.html)


我们之前讲过， NPL语言中的全部数据类型是： `数字，字符串，表，函数，true/false/nil`。
我们只剩下表和函数没有讲了。 本节我们讲解：表(Table)。

> 表是数据到数据的映射关系。

表就如同文件夹或字典，例如下面从中文字符串到英文字符串的映射就可以用一个表来存储。这里是从左向右映射：左侧的数据叫做关键字(key), 右侧的数据叫做数值(value)。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2422/raw#image.png'
  ext: png
  filename: image.png
  size: '91038'
  unit: px
  width: 450
  alignment: left

```


我们可以用`{}`来创建一个空的表。例如:
```lua
a = {}
```
此时变量a代表了一个空的表。 下面我们向表a中插入上述数据的映射关系。   
```lua
a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"
```
`a[key]=value`是一种特殊的函数形式, 它有3个输入，分别是a, key, value。它的作用是向表a中加入一个从关键字key到数值value的映射。关键字key可以是除了nil外的任何数据类型，所以我们也可以插入Apple到苹果的映射。

```lua
a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"

a["Apple"] = "苹果"
```

`表`最重要的功能是，输入任何一个关键字key，快速的输出对应的数值value。即使表中有成千上万的映射，也可以快速的返回结果。例如:
```lua
a = {};
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"

a["Apple"] = "苹果"

log(a["苹果"]) -- aple
```

`log(a["苹果"])` 会输出Apple

上面的`a[key]`中的`[]`其实是一个特殊的内置函数， 它有2个输入，分别是左侧的表a和方括号中的关键字key，它的输出是表中关键字所对应的数据, 如果不存在这个映射，则输出nil。例如

```lua
a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"

a["Apple"] = "苹果"

log(a["苹果"]) -- Apple
log(a["橘子"]) -- nil
```

如果关键字是字符串，并且符合变量的命名规则， 则`a[key]`以及`a[key]=value`函数在NPL中还有一种更简单的形式 `a.key`和`a.key=value`。 `.`的左右侧的输入分别是表和关键字。例如：

```lua
a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"

log(a["苹果"]) -- Apple
log(a.苹果) -- Apple
```

`log(a["苹果"])`和`log(a.苹果)` 都会输出"Apple"，这样我们可以省去`[""]`,让代码更容易阅读。 

```lua
a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"


log(a["苹果"]) -- Apple
log(a.苹果) -- Apple

a["橘子"] = "orange"
a.橘子 = "orange"
log(a.橘子) -- 橘子
```

同理 `a["橘子"]="orange"`与`a.橘子="orange"` 是等价的。`log(a.橘子)`会输出orange。

你也许会问，使用`.`函数访问数据的方式和变量很像。 没错，其实NPL中所有的变量，都是通过表来存储的。

> `变量`就是变量名(字符串)到变量所代表的对象的映射。

在NPL中所有的全局变量都存在一个全局表变量`_G`中。例如, 下面3行语句是等价的:

```lua
_G.a = {}   -- 其它地方可以用 a = {}
a["苹果"] = "Apple"
a["右侧"] = "Right"
a["正确"] = "Right"

log(a.苹果)   -- Apple
log(_G["a"]["苹果"])  -- Apple
log(_G.a.苹果)  -- Apple
```

上面三个log都输出Apple。所以访问一个全局变量a其实是调用了函数`_G["a"]`, 本地变量（local variable）情况特殊一些，但是基本原理是一样的。

> 注意：代码方块中的全局变量被存在了另外一个独立的表中，而不是默认的全局表。如果你希望表a可以在多个代码方块中使用， 你需要用`_G.a = {}`, 也就是向全局表_G中插入字符串"a"到空表{}的映射，或者调用`set("a", {})`函数。 在常规的NPL代码中，你可以直接用`a = {}`向默认全局表中写数据。

计算机如何通过变量的名字在某个表中找到它对应的对象（存储单元）是一个很比较复杂的事情。 在NPL语言中，这个过程是通过一个叫做`MetaTable`(原表)的概念实现的。通过Metatable, 程序员可以自定义`[]`和`.`函数针对某个表的输入/输出映射规则。但是这个概念对初学者太复杂了，这里就不讲解了。在代码方块中，大家并不需要知道原表，每个3D世界中所有的代码方块共用一个名字为`_G`的全局表。 最后，大家记住一个规则，就是尽量不要用全局变量。如果你一定要用，你要清楚它存在了哪个全局表中，因为全局表可能不只一张。

一个表对象中的所有关键字必须是彼此不同的， 然而数值可以相同，并且可以是任意的数据类型，包括其它表。
例如，变量_G中包含了字符串"a"到表a的映射，表a又包含了从"苹果"到"Apple"的映射。

可以说代码方块中的数据(全局变量，系统函数等等)都在_G表中， 所以计算机程序其实是保存在一个由表构成的树型结构中，类似文件夹一样；最上面的一层就是_G表。通过这张表，我们可以通过关键字，找到程序中的所有全局数据。

最后我们再介绍一种创建表的方法，它可以让你的代码更简短。
```lua
a = { ["苹果"]="Apple", Apple="苹果", 右侧 = "Right", ["正确"] = "Right" }
```
如上，我们可以直接在{}中用逗号分隔每个数据映射。这样就不用一个一个插入了。为了美观，我们也可以加入空格和回车。
```lua
a = {
  ["苹果"] = "Apple",
  Apple = "苹果",
  右侧 = "Right",
  ["正确"] = "Right"
}
```
细心的人会发现，其实如果等号左侧的关键字是符合变量命名规则的字符串，则可省去`[""]`，例如Apple和右侧我们就没有加`[""]`。

这里要注意的是， 表中的映射是不记录添加的先后顺序的。所以下面的写法也是等价的。
```lua
a = {
  右侧 = "Right",
  ["正确"] = "Right",
  ["苹果"] = "Apple",
  Apple = "苹果",
}
```
如果关键字不是字符串， 而是连续的从1开始的整数, 例如:
```lua
a = {
  [1] = "one",
  [2] = "two",
  [3] = "three",
}
log(a[2]) -- 会输出"two"
```

此时，有一个简单的写法，可以忽略前面的整数关键字,方括号以及等号, 写成
```lua
a = {"one", "two", "three"}
log(a[2]) -- 会输出"two"
```
这样的表，通常叫做数组。

我们也可以混合两种写法，例如：
```lua
a = {"one", "two", "three", Apple="苹果"}
log(a)
```

此时`log(a)`会输出整张表的内容。如下图：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2423/raw#image.png'
  ext: png
  filename: image.png
  size: '284528'
  unit: px
  width: 550
  alignment: left

```


了解了表和数组的概念，我们来看一个复杂一点的例子。

```lua
moveTo(19202, 5, 19168)
turnTo(90)
```
moveTo函数可以让人物瞬移到指定位置。它的输入是3个数字坐标， 关键字1,2,3映射的数据分别代表x,y,z的坐标。

```lua
-- moveTo(19202, 5, 19168)
local pos = {19202, 5, 19168}
moveTo(pos[1], pos[2], pos[3])

turnTo(90)
```
下面我们先注释掉moveTo这行， 换一种写法。先创建一个本地变量pos，再建立表中的3个映射，分别将1,2,3的位置映射到数据19202, 5, 19168。再输入`moveTo(pos[1], pos[2], pos[3])`。我们重新运行，可以看到人物瞬移到的位置是一样的。所以注释掉的代码和我们新加入的使用变量pos的代码效果是一样的。

下面我们看turnTo函数，它让演员转向到某个角度，代码中是90度。下面我们来用一个变量来记录角色的位置(pos)和方向(facing)

我们先注释掉之前的代码， 换一种写法。

```lua
local params = {}
params.pos = {x=19202, y=5, z=19168}
params.facing = 90

moveTo(params.pos.x, params.pos.y, params.pos.z)
turnTo(params.facing)
```
`local params = {}` 先创建一个本地变量params，让它指向一个空的表。
`params.pos = {x=19202, y=5, z=19168}`再向params中加入pos到另外一张表，也就是包含x,y,z坐标的映射。
`params.facing = 90` 我们再加入一个字符串facing到90的映射。
然后我们再使用moveTo函数，将三个坐标`params.pos.x, params.pos.y, params.pos.z` 输入给它；以及使用turnTo函数，将`params.facing`输入给它。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2424/raw#image.png'
  ext: png
  filename: image.png
  size: '173944'
  unit: px
  width: '550'
  alignment: left

```

运行后，如上图，人物瞬移到19202, 5, 19168并转向90度的方向。虽然代码变长了， 但是我们将数据和命令通过变量分离开来了。 这样做有很多好处。比如, 我们可以根据变量动态的计算人物的位置和方向，比如下图中的`params.pos.y + 1`和`params.facing + 45`。注意下面的代码我还用了一个前面讲到的更简洁的初始化表的写法。

```lua
local params = {
   pos = {x=19202, y=5, z=19168},
   facing = 90,
}
moveTo(params.pos.x, params.pos.y + 1, params.pos.z)
turnTo(params.facing + 45)
```

最后我们总结一下：表是一组有映射关系的数据的集合， 是NPL语言中唯一的复合型数据， 几乎所有复杂的概念都需要通过表来表示，例如一个3维坐标， 一组复杂的输入； 我们写的所有的代码其实都存在表中。 表可以通过关键字(一般是字符串和数字)快速的输出它对应的数据。