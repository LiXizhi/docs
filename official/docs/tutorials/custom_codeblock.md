## 自定义代码方块

我们可以在某个代码方块中自定义属于自己的图形化编程的函数，这些函数可以被复制粘贴到其它代码方块，并自动出现在扩展栏目，或者用户指定的分类下。如下图， 点击`+`可以编辑或从其它场景中的代码方块添加自定义图块。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/37379/raw#1715314502443image.png
  ext: png
  filename: 1715314502443image.png
  size: 32054
  isNew: true
          
```
你也可以选择代码方块的属性并点击定制图块，如下图
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/37380/raw#1715314718446image.png
  ext: png
  filename: 1715314718446image.png
  size: 20533
  isNew: true
          
```
我们支持定制图块，和定制工具栏。

1. 点击`定制图块`。你可以在当前代码方块，当前世界， 或全局3个地方定义属于自己的图块（函数）。 
2. （可选）点击`定制工具栏图块`，选择你希望在代码方块中显示哪些定义好的图块。

### 定制图块

在代码方块的设置UI中点击`定制图块`。按照图中数字顺序操作：

1. 选择在哪里定义图块：小技巧 :point_right: 你可以先选择全局的NPL图块，然后选择一个已有的图块点击编辑，然后再切换到当前图块，这样你就可以从一个已知的图块，派生你需要的图块了。 
2. 定义好后， 点击保存， 可以看到右下角出现了刚刚的图块。 
3. 你可以通过选择编辑，去编辑任意的图块。 编辑后记得点击保存
4. 可以通过上面4区域的工具栏测试刚刚添加的图块。注意这里的工具栏只是测试用的， 并不会显示到真实的代码方块中。 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26901/raw#1685440773763image.png
  ext: png
  filename: 1685440773763image.png
  size: 72074
          
```

我们推荐你选择在当前代码方块定义图块，这样你可以复制这个代码方块到不同的世界，并实现复用。 
有时，你希望在同一个世界中复用一套自定义的图块， 也可以选择在世界目录下定义图块。


### 定制工具栏
在代码方块的设置UI中点击`定制工具栏图块`。

你可以复制定制图块右侧的工具栏中的代码到这里。 这里你可以混合全局NPL图块和你自定义的图块，并DIY属于自己的图块工具栏。 定义好后，你的图块会显示在当前的代码方块中。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26902/raw#1685441098403image.png
  ext: png
  filename: 1685441098403image.png
  size: '38522'
  unit: px
  width: '500'
  alignment: left

```
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26903/raw#1685441146806image.png
  ext: png
  filename: 1685441146806image.png
  size: '13312'
  unit: px
  width: '400'
  alignment: left

```


最后的效果为：
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26904/raw#1685441182715image.png
  ext: png
  filename: 1685441182715image.png
  size: '10005'
  unit: px
  width: '500'
  alignment: left

```


### 添加头部唯一性代码

有些语言例如python, C++ 需要在代码头部添加例如**import**或**#include或者某些预制函数**。此时我们可以使用下面的图块，第二个参数代表优先级。数值越小，越靠前。如果多个图块定义了统一个头部引用，只生成一份引用。 一个图块可以定义多个头部引用，每隔都是独立唯一的。

![1715315096249image.png](https://api.keepwork.com/ts-storage/siteFiles/37382/raw)

### 关于缩进

对于python语言， 我们会自动添加缩进，如果一些非常特殊的情况，你也可以使用${INDENT}代表当前的缩进值。 更特殊的情况， 你也可以直接用下面高级代码（不推荐）。
### 自定义图块代码生成（高级，不推荐）

图块代码生成通常使用模板串方式: 如上图NPL_broadcase图块的代码模板broadcase($(msg), $(params))语法类似shell字符串. 其中${fieldname}代表字段名为fieldname字段值. 这是常规生成代码方式, 但对于python这种生成代码比较特殊时就需要使用图块自定义代码, 这时可以直接输入代码如:

```javascript
NPL_boradcase.ToPython = function(block)
  local msg_value = block:GetFieldValue("msg");
  local params_value = block:GetFieldValue("params");
  return string.format('broadcase("%s", "%s")', msg_value, params_value):
end
```
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29008/raw#1691648767665image.png
  ext: png
  filename: 1691648767665image.png
  size: 50031
  isNew: true
          
```
### 定义折叠起来的图块

我们还可以通过 `输入-语句`将很多图块以折叠的方式显示。 这种做法类似code snippet(代码片段)，可以让我们封装大量复杂的图块到1行图块中，同时高级用户展开图块还可以DIY内部的代码。如下图所示，如果我们展开，会看到内部的实现。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35550/raw#1709725307648image.png
  ext: png
  filename: 1709725307648image.png
  size: 26688
  isNew: true
          
```

在DIY图块界面中， 我们可以使用如下的语句实现这个功能。 

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35551/raw#1709725395145image.png
  ext: png
  filename: 1709725395145image.png
  size: 37674
  isNew: true
          
```

上面例子中xmlCode变量的内容， 可以通过右键任意图块，保存XML获得。如下，就保存了2行语句的XML内容。 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35553/raw#1709725776578image.png
  ext: png
  filename: 1709725776578image.png
  size: 13561
  isNew: true
          
```
在代码格式中，我们可以直接复制粘贴变量，甚至可以通过变量（例如例子中的t），影响折叠部分的代码。
```
do
   local t = ${dist} 
   ${xmlCode}
end
```

例如前面例子的代码会产生如下的代码。
```
do
    local t = 10
    moveForward(t, 0.5);
    turn(15);
end
```

#### 自定义折叠图块(简易模式)

还有一种更简单的定义多行代码的方式如下：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35554/raw#1709726245540image.png
  ext: png
  filename: 1709726245540image.png
  size: 26847
  isNew: true
          
```
对应的DIY图块代码为：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35555/raw#1709726290551image.png
  ext: png
  filename: 1709726290551image.png
  size: 18366
  isNew: true
          
```