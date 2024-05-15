## 内置函数
```@BigFile
styleID: 0
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/360/raw#NPL CAD教学3.7.2.mp4
  ext: mp4
  filename: NPL CAD教学3.7.2.mp4
  size: 36568707
```
[在腾讯视频播放](https://v.qq.com/x/page/s0537tzyib2.html)


这一节我们来看一些常用的系统内置函数，包括`and, or,  if, for, while `。这些内置函数与我们自己定义的函数本质是一样的，只是语法不同.
它们有一个共同的特点就是在一定条件下改变代码的执行路径，代码不再是顺序执行。 

下面我们分别来看下。

先来看and（和）函数。 
```lua
local result = (left) and (right)
```
它将代码分成了左右两个部分 (left) and (right)。
它会先执行左侧的代码，如果左侧的代码的返回值为false或nil, 则整个and函数返回左侧代码的输出，右侧代码不会执行。
如果左侧代码的返回值不是false或nil, 则右侧的代码会执行，并且整个and函数返回右侧代码的输出。

我们看个例子
```lua
local function left_code(a)
   log("左侧执行了")
   return a > 10;
end
local function right_code(a)
   log("右侧执行了")
   return a > 5;
end
```
我们先来定义一个左侧函数left_code。这个函数会输出`左侧执行了`，它会返回一个值，如果输入大于10的话，它会返回true，否则会返回false。我们再来定义一个右侧函数(right_code)，它会输出`右侧执行了`。如果右侧输入大于5的话，它会返回true，否则返回false。现在我们来使用and函数：

```lua
local t = left_code(10) and right_code(10);
log(t); -- false
```

and函数左侧代码为left_code(10)，然后是and和right_code(10)。此时我们输出t，我们运行一下，可以看到执行的结果为`左侧执行了`。由于左侧10并不大于10，所以返回了false。因此整个and函数会返回左侧代码的执行结果，也就是t为false，而右侧代码并没有执行。

下面我们将左侧输入变成11，右侧输入为10不变。

```lua
local function left_code(a)
   log("左侧执行了")
   return a > 10;
end
local function right_code(a)
   log("右侧执行了")
   return a > 5;
end

local t = left_code(11) and right_code(10);
log(t); -- true
```

此时我们再次运行，我们可以看到左侧代码的输入11是大于10的，所以返回了true。左侧代码执行了，此时and函数会继续执行右侧的代码。因为右侧代码的输入是大于5的，所以右侧代码返回了true。因此整个and函数返回true。

其实and函数左侧的代码永远会执行，只不过根据它的返回值的不同，决定了是否执行右侧代码，进而决定整个and函数的返回值。

如果我们将右侧代码的输入改成0，我们再次执行。
```lua
local t = left_code(11) and right_code(0);
log(t); -- false
```
可以看到左侧代码和右侧代码都执行了，但是右侧代码的返回值为false，因为0没有大于5。 如图：

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2427/raw#image.png'
  ext: png
  filename: image.png
  size: '155003'
  unit: px
  width: '500'
  alignment: left

```

----

下面我们来看or（或）函数，它也是将代码分成左右两个部分，但它与and函数的执行结果基本相反。也就是如果左侧代码的返回值不是false或nil，则整个or函数返回左侧代码的输出，右侧代码不会执行。如果左侧代码的返回值是false或nil，则右侧代码会执行，并且整个or函数返回右侧代码的输出。

下面我们来看一个例子，同样还是这两个函数，我们这里改为了or函数。我们运行一下，可以看到左侧的输入，同样是10，左侧代码返回了false，因为是or函数，所以右侧代码会执行。右侧的输入10大于5，右侧代码返回了true，所以左右代码都执行了，并且整个or函数返回了true。

```lua
local function left_code(a)
   log("左侧执行了")
   return a > 10;
end
local function right_code(a)
   log("右侧执行了")
   return a > 5;
end

local t = left_code(10) or right_code(10);
log(t); -- true
```

那么我们现在将左侧的输入改为11，右侧的输入改为0。 

```lua
local t = left_code(11) or right_code(0);
log(t); -- true
```
再来运行一下。我们看到只有左侧的代码执行了，并且因为11大于10返回了true，而右侧的代码并没有执行。如图：
  
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2429/raw#image.png'
  ext: png
  filename: image.png
  size: '164624'
  unit: px
  width: '450'
  alignment: left

```

----
下面来看if函数。 if中文是如果的意思, 它需要配合then和end来使用，也就是如果(if)那么(then)的意思，我们用一个例子来说明它的用法。

```lua
function testword(a)
     if (a=="hello") then
          log("a是hello")
     end
end
testword("hello")
testword("xxx")
```

我们先来定义一个函数textword，如果（if） a等于hello，也就是a和字符串hello完全相同; 那没(then)我们输出`a是hello`。下面我们来调用testword函数两次，输入分别是hello和xxx。

```lua
function testword(a)
     if (a=="hello") then
          log("a是hello")
     end
end
testword("hello")
testword("xxx")
```
我们运行一下，可以看到它只输出了`a是hello`，也就是说if函数会根据括号中函数的返回值来决定是否会执行then和end之间的代码。
比如上面的代码中，如果a等于hello，那么中间的代码才会执行，log才有输出。否则输入是xxx那么log这行代码并不会执行。

我们同样还可以使用else关键字。else是否则的意思。我们在它后面加上`log("a不是hello")`。

```lua
function testword(a)
    if (a == "hello") then
        log("a是hello")
    else
        log("a不是hello")
    end
end
testword("hello") -- a是hello
testword("xxx") -- a不是hello
```

那么这段代码的意思是: 如果a和字符串hello完全相同，则执行then和else之间的代码，否则将执行else和end之间的代码。 

此时我们再运行，可以看到输出了两行:
- `testword("hello")`输出了`a是hello`。
- `testword("xxx")`输出了`a不是hello`。

我们看到if函数是编程语言中唯一一个有多种形态的特殊函数，它可以由多个像`then end else`这样的关键字构成。

比如它还可以加入elseif关键字，如下面：
```lua
function testword(a)
    if (a == "hello") then
         log("a是hello")
    elseif(a == "world") then
         log("a是world")
    else
         log("a不是hello, 也不是world")
    end
end
```
`elseif`(否则如果)a`==等于等于`world, 那么输出`a是world`; 再用else关键字，也就是否则输出`a不是hello，也不是world`。也就是前两个括号中的函数返回false时才会执行最后一个else和end之间的代码。 

整体来说，if函数中至少要有then和end, 同时还可以有任意多个elseif和一个else。if函数最终的实现效果是依次执行括号中的代码，直到有一行代码返回真则执行后面的代码。换句话说，上述由关键字隔开的三段代码永远只有一段会执行。

下面我们再加一行`testword("world")`，运行一下，可以看到输出了三行结果。
```lua
function testword(a)
  if (a == "hello") then
     log("a是hello")
  elseif(a == "world") then
     log("a是world")
  else
     log("a不是hello, 也不是world")
  end
end
testword("hello")
testword("world")
testword("xxx")
```
- `testword("hello")`输出了`a是hello`。
- `testword("world")`输出了`a是world`。
- `testword("xxx")`输出了`A不是hello也不是word`。

当然我们也可以不使用elseif，用两个if函数来写。例如在第一个if函数的else和end之间再加入另一个if函数，那么结果也是一样的。 如下：
 
```lua
function testword(a)
  if (a == "hello") then
     log("a是hello")
  else
     if(a == "world") then
          log("a是world")
     else
          log("a不是hello, 也不是world")
     end
  end
end
testword("hello")
testword("world")
testword("xxx")
```

为了避免嵌套，让逻辑更清晰，我们还是用第一种写法。if, then, elseif, else, end 是系统内置的`关键字`，他们可以共同的十分灵活的定义若干输入和输出之间的条件触发关系。if函数在计算机语言中十分的常见，但是它也会破坏代码的可读性。在自然语言中，例如我们在用中文讲课或写文章时，我们很少用：如果怎么样, 那没怎么样。即使我们平时说话时使用了`如果`, 在如果和那么之间的文字也不会很长，也很少嵌套。同样的原则对于计算机语言同样适用，我们应该尽可能的让我们的代码看上去是顺序执行的。

初级程序员的代码到处都是冗长和嵌套的if函数。下面我们介绍一些降低if函数复杂度的方法。
- 第一种方法是将then和end之间的代码放到一个新的函数中。
- 第二种方法是将各种输入和输出都放入一个table表中。

下面我们来看一个例子，首先我们先将then和end之间的代码放到一个函数中，这里我们需要创建三个新函数，它们分别`a_is_hello, a_is_world, a_is_others`，分别对应我们之前if,end中间的代码。在实际使用中，这里面的代码可能是很多行的。 

```lua
local function a_is_hello()
   log("a是hello")
end
local function a_is_world()
   log("a是world")
end
local function a_is_others()
   log("a不是hello, 也不是world")
end
```
然后我们会创建一个table，比如叫wordtable，它建立了多个字符串和函数之间的对应关系，也就是字符串hello到a_is_hello这个函数的映射；以及字符串world到a_is_world函数的映射。如下面所示：

```lua
local function a_is_hello()
   log("a是hello")
end
local function a_is_world()
   log("a是world")
end
local function a_is_others()
   log("a不是hello, 也不是world")
end

local wordtable = {
   hello = a_is_hello,
   world = a_is_world,
}

function testword2(a)
     local result = wordtable[a] or a_is_others
     result()
end
```

这时我们再定义一个testword2函数，此时我们就可以避免出现if和end,这样来写：我们将对条件的判断改为对table对象的查询。那么如果没有查询到的话，我们则返回`a_is_others`变量。此时result是一个函数变量，我们用`result()`调用这个函数。 

现在我们来测试一下。
```lua
local function a_is_hello()
   log("a是hello")
end
local function a_is_world()
   log("a是world")
end
local function a_is_others()
   log("a不是hello, 也不是world")
end

local wordtable = {
   hello = a_is_hello,
   world = a_is_world,
}

function testword2(a)
     local result = wordtable[a] or a_is_others
     result()
end
testword2("hello")
testword2("world")
testword2("xxx")
```
调用testword2函数3次。第一次的输入为hello，第二次的输入为world，第三次的输入为xxx。运行一下，可以看到输出同样是这三个。通过这样的方法，我们避免了使用if函数。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2431/raw#image.png'
  ext: png
  filename: image.png
  size: '178457'
  unit: px
  width: 500
  alignment: left

```

----

下面我们来看while函数，它是一个循环函数，while是循环的意思，它同样需要配合do和end两个关键字来使用。我们来举个例子。
while函数会不停的执行while和end之间的代码， 直到（）中的代码输出不是false或nil。

```lua
local a=0
while(a<3) do
   a = a + 1;
   log(a)
end
```
如上面的代码中，第一次执行时a等于0。0小于3，括号中的代码返回true。所以它下面的代码继续执行。那么0+1等于1，log(a)输出结果是1，那么do和end之间的代码会执行三次，会有三个输出结果。
我们运行一下，可以看到输出结果为123，也就是当a大于3时，后面的代码将不再执行。

最后我们再来看另外一个循环函数for，它的语法是这样的。 我们用一个例子来说明：
```lua
for a = 1, 3, 1 do
   a = a + 1
   log(a)
end
```
for和while类似，只不过它会定义一个局部变量a并设置一个初始值1 一个结束值3和一个递增值1，并重复执行do和end之间的代码，也就是第一次执行时a等于1，然后a会不停的加1。 最后一次执行时a等于3, 每次log(a)会输出不同的a的数值。我们运行一下，可以看到输出结果为234。当然如果递增的值是1的话，我们也可以不写，例如这样
```lua
for a = 1, 3 do
   a = a + 1
   log(a)
end
```
我们再运行，结果是一样的。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/2432/raw#image.png'
  ext: png
  filename: image.png
  size: '122298'
  unit: px
  width: 450
  alignment: left

```

好了， 到今天为止， 我们就讲完了NPL语言中的全部语法。 无论多么复杂的程序都是由我们学到的这些最基本的函数构成的。 可见， 目前的高级计算机语言相比自然语言要简单很多， 一般只有十几个最基本的函数构成， 但是如何运用这些函数去创造成千上万更复杂的函数却需要大量的读写练习。NPL/Paracraft提供了一个很好的练习环境。你可以通过代码方块学习计算机编程， 最终编写出和Paracraft一样复杂的程序。 