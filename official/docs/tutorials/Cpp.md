# C++ 代码方块

Paracraft支持两种C/C++代码方块： 一种采用NPL编译器，一种采用Clang编译器。

- NPL/C++编译器： 将C++代码转化成NPL代码，最终执行的是NPL代码。优点是你可以和paracraft中的一切进行交互，相当于你只是换了一种语法写paracraft；缺点是他并不支持全部C++语法。
- Clang/C++编译器：将C++通过开源的clang编译器，编译为web assembly,并在内置浏览器中运行。优点是它支持全部C++最新的语法，缺点是它无法直接调用paracraft API，而是一个独立的应用。 

## NPL/C++编译器
我们可以在代码下，选择C++创建一个NPL/C++编译器的C++代码方块， 这也是默认的C++代码方块。你也可以在代码方块设置中选择cpp(NPL/C++编译器),将任意普通代码方块变成C++代码方块。 cpp编译器会将C++代码转化成NPL代码，最终执行的也是NPL代码。优点是你可以和paracraft中的一切进行交互，相当于你只是换了一种语法写paracraft；缺点是他并不支持全部C++语法。

C++方块的主要用途为：
1. 提供了arduino C硬件编程的仿真环境
2. 为信息奥赛提供更友好的教学环境：例如支持C++图块， 宏示教， 以及将文本的输入、输出和3D场景互动起来。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34872/raw#1704798528699image.png
  ext: png
  filename: 1704798528699image.png
  size: 49876
  isNew: true
          
```
例如输入下面的代码，你可以在console窗口中看到输出
```c
#include <bits/stdc++.h> 
int main(){ 
    int a[20][20]={0};
    int n;
    cin>>n; 
    
    for(int i=0;i<n;i++){ 
        for(int j=0;j<n-i;j++){ 
            a[i][j+i]=i+1; 
            a[j+i][i]=i+1; 
        } 
    } 
    for(int i=0;i<n;i++){ 
        for(int j=0;j<n;j++){ 
            cout<<a[i][j]; 
        } 
        cout<<endl; 
    } 
    return 0; 
}
```
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34874/raw#1704800016187image.png
  ext: png
  filename: 1704800016187image.png
  size: 299178
  isNew: true
          
```

### NPL/C++ 支持的类库
print, cin, cout, setw, setprecision, lamda匿名函数, 多维数组等。未来可能会支持更多，但是主要为了支持ACM，NOIP等信息奥赛和arduino C语法的虚拟仿真。你也可以自己在3D世界中实现属于自己的类库，然后通过C++语法调用。

### main函数
如果代码中定义了main函数，它会在代码方块首次加载时执行一次。 因为C++语言不允许在函数外调用函数，我们建议您将所有的调用都写到main函数中。 

### 调用NPL函数

```
int main(){ 
    char* text = "Hi";
    registerClickEvent([](){
        say(text);
    });

    registerBroadcastEvent("sayHi", [](){
        say(text);
    });

    wait(1);
    broadcast("sayHi");
}
```


## Clang/C++编译器
由于我们不推荐这种方式的代码方块，它没有直接的创建方式，你需要先新建一个普通的代码方块，然后在代码方块设置中选择clang.  Clang/C++编译器将C++通过开源的clang编译器，编译为web assembly,并在内置浏览器中运行。优点是它支持全部C++最新的语法，程序的执行速度基本等同其他C++编译环境；缺点是它无法直接调用paracraft API，而是一个独立的应用。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/34873/raw#1704799506486image.png
  ext: png
  filename: 1704799506486image.png
  size: 39079
  isNew: true
          
```