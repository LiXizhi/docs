## 代码方块的中的全局变量

NPL语言中变量的作用域[请看这里](/official/docs/NPL/names)

在代码方块中定义的全局变量的作用域有一点复杂，下面说明一下情况。 

### 代码的环境
每段代码（函数）都有一个环境，也叫沙盒环境，其实这个环境也是一个table对象。 全局变量一般都是定义在这个沙盒环境（Table）中的。 
如果2段代码共用的是同一个沙盒环境，那么它们彼此都可以直接通过变量名获取或设置沙盒环境中的全局变量。 

在Paracraft中存在多个沙盒环境， 某些沙盒环境又存在嵌套关系。所谓嵌套是指当全局变量没有在当前沙盒环境中，它会向上找上一级的环境，直到顶层。 

首先Paracraft中有一个权限最大的默认沙盒环境，所有的Paracraft底层代码和所有的Paracraft MOD插件都是运行在这个环境中的，我们称之为`默认环境`。 
这里值得注意的是`commonlib.gettable`等函数是从`默认环境`中读写数据的。


在F11的NPL Console中运行的代码是一个单独的沙盒环境， 这个沙盒环境很特殊，它继承了`默认环境`。 也就是说你可以读取所有`默认环境`中的全局变量，但是你新建的全局变量是在单独的专属沙盒环境中， 不会影响或改变`默认环境`。 例如下面新建的变量a并不在`默认环境`中。
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/13540/raw#1592201426629image.png
  ext: png
  filename: 1592201426629image.png
  size: '17436'
  unit: px
  width: 500

```

代码方块中的代码更加特殊一些。 每个代码方块都有自己独立的专属的沙盒环境，并且每次重新运行，这个沙盒环境都会清空并重新构建。 
代码方块的沙盒环境100%继承了当前世界沙盒环境中的所有全局变量， 当前世界的沙盒环境只继承了一小部分默认沙盒环境的中的变量。如下图所示。

```@Board
styleID: 0
board:
  xml: >-
    https://api.keepwork.com/core/v0/repos/official%2Fdocs/files/official%2Fdocs%2F_config%2Fboard%2Fsandbox%20code%20block.xml
  svg: >-
    https://api.keepwork.com/core/v0/repos/official%2Fdocs/files/official%2Fdocs%2F_config%2Fboard%2Fsandbox%20code%20block.svg

```

这样做的好处是，避免上层沙盒环境中的全局变量或函数`污染`了下层沙盒环境的全局变量或函数。 

例如，你可以同时在多个代码方块中定义`a=1`, 彼此之间并不会相互影响，相当于有多个变量a, 分别存储在每个代码方块中的沙盒环境中， 彼此并不影响。 

那么如何在同一个世界中的多个代码方块中共享全局变量（或函数）呢？我们可以通过`当前世界的沙盒环境`.

```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/13573/raw#1592203409409image.png
  ext: png
  filename: 1592203409409image.png
  size: '28179'
  unit: px
  width: 500

```

我们可以通过代码方块提供的`set()`方法或`_G`来向`当前世界的沙盒环境`中写入新的全局变量。只要世界环境中已经存在变量`a`,那么我们就只需要通过`a`来读取它的值，而不再需要用`_G.a`。

当然如果你需要共享大量的数据或函数， 还可以通过代码方块的`获取全局表gettable`或`继承表inherit`2个方法来新建属于整个世界的全局变量。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/13574/raw#1592203595605image.png
  ext: png
  filename: 1592203595605image.png
  size: '38879'
  unit: px
  width: 500

```

注意，世界中的全局变量是一直存在的， 即便代码方块卸载了，也同样存在。 只有当你退出当前世界或重新加载世界时，这个环境才被清空。 

注意， 我们一般不建议在代码方块中修改最最底层的默认沙盒环境。 目前代码方块中也没有明显的地方允许你这样做。 这样的好处是代码方块中的错误不会影响整个Paracraft的运行。 


