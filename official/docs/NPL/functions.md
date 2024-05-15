## 函数

```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/359/raw#NPL CAD教学3.7.1.mp4
  ext: mp4
  filename: NPL CAD教学3.7.1.mp4
  size: 21894910
```
[在腾讯视频播放](https://v.qq.com/x/page/b0392s1jfxm.html)

这一节我们来讲解NPL语言中的最后一种数据类型: 函数function。

在2.2中，我们讲过程序的本质是输入和输出。而函数正是建立从输入到输出关系的方法。

其实，在之前的章节中，我们已经使用过很多系统函数例如log, moveTo, turnTo, 操作符例如`+-*/ ..　== > <`以及`=`也是函数的一种特殊形态。未来我们还会学到例如`if, else, while, for` 等内置函数。

这一节，我们重点介绍如何定义新的函数。注意：计算机语言中的函数，和数学语言中常常提到的函数不是一个概念。前者有着更宽泛的含义。

函数是代码的主要形态，甚至可以说是唯一形态。可以说代码就是由函数构成的。 如果说中文，英文是由文字和单词构成的， 那么函数就如同自然语言中的文字或单词。 只不过，自然语言中的词汇是单向串联起来的，并且文字和单词的总量是基本固定的。但是计算机语言不同，我们在解决一个问题时，需要定义许许多多新的词汇（也就是函数），再利用这些新的函数（也就是词汇）去描述某个领域中的输入和输出关系。

所以每个程序，都有大量仅属于自己的词汇。好的程序员能够更科学的定义这些词汇（也就是函数），让代码朗朗上口， 逻辑清晰，简洁而优美。 初级程序员由于不善于定义词汇，代码往往冗长，晦涩，不易阅读。

在NPL中，我们可以用关键字function去创建一个新的函数。例如：我们定义一个变量JumpForward（中文是向前跳的意思），将后面的整个函数（function）赋给它。

```lua
local JumpForward = function(distance, maxHeight)
   -- 这里是函数的内容
end
```
函数的定义是以`function()`开始，以`end`结束。`()`内为函数的输入，多个输入用`,`分开，每个输入需要指定一个局部变量名。上面的例子中就是distance（距离）和maxHeight（最大高度）。在函数被调用时这2个局部变量会被赋值。  

函数的内部可以有任意其它的函数。每个代码方块或文件中的代码都在一个我们看不见的函数内部。当代码方块被激活或文件被加载时，函数里面的代码就会被执行。

函数还可以用return（返回）来输出一个结果（我们后面会讲解）。 函数本身和字符串，数字一样是一种数据类型，存在于一个固定的存储空间，如果你定义的函数没有任何变量指向它，则函数会被释放掉。 因此我们需要将新定义的函数，马上用`=号函数`赋给一个变量，未来我们就可以用这个变量来调用函数。

下面是一种更友善的定义函数的语法，和上面是完全等价的， 但是省去了等号。写法是这样的：

```lua
local function JumpForward(distance, maxHeight)
   -- 这里是函数的内容
end
```
内部是函数内容，也就是function和end之间的代码会在`JumpForward`这个函数被调用时执行。

无论哪种写法，其实`JumpForward`都是一个本地变量，当然我们也可以用全局变量，去掉上面代码中的local，例如这样：

```lua
function JumpForward(distance, maxHeight)
end
```
或者像这样：
```lua
JumpForward = function(distance, maxHeight)
end
```
对于代码方块， 全局变量需要存放在_G表中，像下面这样
```lua
function _G.JumpForward(distance, maxHeight)
end
-- 或者
_G.JumpForward = function(distance, maxHeight)
end
```

甚至, 我们可以用多个不同的变量指向同一个函数，例如：
```lua
function JumpForward(distance, maxHeight)
end
local DoJump = JumpForward
```
但是通常我们都只用一个固定的变量名来指向一个函数。因此，这个变量名也被叫做函数名。

> 调用函数的语法为 `函数名(param1[, param2, ...])`

例如： `JumpForward(2, 1)`
我们之前使用到的系统函数moveTo, turnTo等都是用这种方式调用的。只不过这些系统函数是在系统代码中定义的, 在你的代码运行前，已经被加载了。

下面我们来看一个完整的自定义函数并调用这个函数的例子。

```lua
local function JumpForward(distance, maxHeight)
    local time = distance / 5;
    move(distance, maxHeight, 0, time)
    move(distance, -maxHeight, 0, time)
end
```
distance, maxHeight是JumpForward函数内部的局部变量，当每次JumpForward函数被调用时，它们会代表不同的输入。在函数的内部我们调用了系统函数move两次。 move函数有4个输入， 前3个是相对当前角色位置的x,y,z位移, 第4个输入为消耗的时间。所以第一个move让人物向斜上放运动， 第二次move让人物向斜下方运动。运动的距离，高度，和用的时间由distance, maxHeight决定。

下面我们来调用JumpForward函数：
```lua
local function JumpForward(distance, maxHeight)
    local time = distance / 5;
    move(distance, maxHeight, 0, time)
    move(distance, -maxHeight, 0, time)
end

JumpForward(1, 1)
JumpForward(1.5, 1.5)
JumpForward(2, 2)
```
我们运行一下上面的代码，可以看到，我们通过调用自定义的JumpForward函数让人物向前跳跃了3次，每次的距离分别为1, 1.5, 2米。   

我们看到函数隐藏了内部的输入和输出细节，并用一个变量名代替了内部看不见的逻辑关系。 好的程序员会为每一个功能写函数，并命名函数，使得代码的可读性大大增加， 并可以重复利用相同的逻辑关系。 

> 写代码有一个黄金原则是`绝对不要写重复的代码` 。

写代码的过程中，程序员会不断的将重复的逻辑封装到函数变量中，这个过程叫做代码的`重构`。 宏观上看， 函数使得代码有了层级关系， 每个层级上仿佛都有程序员自己定义出来的一套新语言（和新词汇）。 一个复杂的程序可能会定义成千上万的函数变量。

我们再来看一个有返回值的函数，叫做平方函数。
```lua
local function sq(x)
   local result = x * x;
   return result
end
```

我们在函数内部定义了一个局部变量result。它的作用域是到end结束。这里result首先被赋值为x * x。
return函数代表了函数的输出，也就是sq(x)的输出。return函数后面的代码不会被执行。

下面我们来调用这个函数：

```lua
local function sq(x)
   local result = x * x;
   return result
end

local a = sq(2)
a = a + sq(3);
log(a);  -- 13
```

因为程序是按顺序执行的，执行到这里，此时a的值已经是4+9=13。我们用log函数输出，运行一下， 可以看到此时log(a)的输出为13。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2426/raw#image.png'
  ext: png
  filename: image.png
  size: '123426'
  unit: px
  width: 450
  alignment: left

```

下一节我们讲解一些常用的系统内置函数`for, if, while, and, or`。