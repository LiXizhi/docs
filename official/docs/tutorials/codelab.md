## 可计算文档使用说明

我们可以在keepwork文档中添加`代码方块`，从而直接在网页中编辑和运行各种代码。我们使用web assembly技术，使得NPL, Paracraft, Python, C/C++等代码可以直接在浏览器中运行，也支持链接外部docker容器。运行结果会输出在代码的下方。


### 快速开始：编写 Hello World 程序
点击`模块>>其他>>代码方块`, 创建一个默认的代码方块。你可以修改下面的代码，然后点击代码左侧的执行按钮反复运行代码。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: npl
  code: print("hello world")
  outputMode: autoParacraft
  output: |
    hello world

```

### 编写3D程序
点击代码右上角的下拉列表，可以切换当前代码的执行环境。 默认为npl代码，现在我们切换到CodeBlock(3D)。codeblock和npl都是使用web assembly的paracraft作为运行坏境，它们都会用paracraft创建一个对应的代码方块来执行代码， 区别是codeblock还会创建一个电影方块，并且会多一个3D输出窗。点击下面代码的运行，然后点击3D角色会转30度。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: codeblock
  code: |-
    say("Click Me to rotate!")
    registerClickEvent(function()
       turn(30)
    end)
  outputMode: autoParacraft
  output: ''

```


### 共享运行环境和3D世界
同一个页面中的所有npl和codeblock都默认共享同一个运行环境和3D世界。全局变量、函数等也是共享的。例如我们可以再创建2个代码, 你可以交替点击运行观察输出的结果。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: npl
  code: |-
    _G.count = (count or 0) + 1
    print(count)
  outputMode: autoParacraft
  output: ''

```


```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: npl
  code: |-
    _G.count = (count or 0) + 1
    print(count)
  outputMode: autoParacraft
  output: ''

```


在运行按钮的下方有个数字，每次运行代码会加1, 你可以用它搞清楚文档中代码运行的顺序。

当然，3D世界也是一样的， 我们可以在3D世界中看到全部运行过的代码方块。 代码方块在3D世界中的位置和他们在文档中的顺序是对应的。 

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: codeblock
  code: say(count or 0)
  outputMode: autoParacraft
  output: ''

```


### 输出的样式
我们支持多种输出的样式。点击代码输出窗口左上方的`...`可以查看。
默认情况下，所有codeblock类型的代码输出都会显示3D paracraft窗口，如果你不希望显示可以在菜单中选择`隐藏3D窗口`

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: codeblock
  code: 'log("3d window is hidden, click ... to enable it again")'
  outputMode: hideParacraft
  output: |
    echo:"3d window is hidden, click ... to enable it again"

```

### 支持多语言
npl, codeblock, clang, python 都默认使用基于Web assembly的web paracraft。 无需安装，直接用本地浏览器进行运算，所有语言都共享一个paracraft运行环境。 

####  C/C++ 支持
选择clang, 可以运行C/C++代码

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  language: clang
  code: |-
    #include <stdio.h>
    int main() {
        printf("hello world from C++");
        return 0;
    }
  outputMode: autoParacraft
  output: >
    Untarring sysroot.tar... done.

    Fetching and compiling clang... done.

    clang -cc1 -emit-obj -disable-free -isysroot / -internal-isystem
    /include/c++/v1 -internal-isystem /include -internal-isystem
    /lib/clang/8.0.1/include -ferror-limit 19 -fmessage-length 80
    -fcolor-diagnostics -O2 -o test.o -x c++ test.cc


    Fetching and compiling lld... done.

    wasm-ld --no-threads --export-dynamic -z stack-size=1048576
    -Llib/wasm32-wasi lib/wasm32-wasi/crt1.o test.o -lc -lc++ -lc++abi -lcanvas
    -o test.wasm


    Compiling test.wasm... done.

    test.wasm

    hello world from C++

```

####  Python(NPL)支持
选择Python(NPL), 可以运行Python代码。 我们通过将Python语言编译为NPL语言来运行，因此可以用python驱动场景中的3D角色，和3D世界无缝通讯，甚至使用NPL语言中的变量、数据和函数。


```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: python
  code: |-
    for i in range(1, 3):
       print("hello from python %d"%(i))
  outputMode: autoParacraft
  output: |
    hello from python 1
    hello from python 2

```

####  Python(Local)支持
如果你希望用原版的Python，可以使用在线容器或Python(Local)。Python(Local)支持import远程pure python类库（whl类库）。用`micropip.install(url)`命令安装本地或远程的Python类库。 

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: python_wasm
  code: |-
    import micropip
    micropip.install('numpy')
  outputMode: autoParacraft
  output: ''

```

Python(local)预先配置了一些[常用类库](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)，可以通过`import`命令， 直接下载使用，无需手工安装。例如`numpy`, `matplot`等。 其中matplot做了特殊处理，可以直接渲染到网页中。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: python_wasm
  code: |-
    import numpy as np

    x = np.arange(15, dtype=np.int64).reshape(3, 5)
    x[1:, ::2] = -99
    print(x)

    import matplotlib.pyplot as plt
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x))
    plt.plot(x, np.cos(x))
    plt.show()
  outputMode: autoParacraft
  output: |
    [[  0   1   2   3   4]
     [-99   6 -99   8 -99]
     [-99  11 -99  13 -99]]

```

### 连接http容器 (jupyter server)
我们可以通过http协议连接本地或远程容器，从而实现对整个Kernel操作系统的控制。 例如可以利用容器的GPU，硬盘等做任意复杂的运算。 

> :dart: [如何在本地搭建一个jupyter-server？](https://keepwork.com/official/docs/Resource/downloadjupyter)


```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: connect_jupyter_server
  code: |-
    !which python

    b = "hello"
  outputMode: autoParacraft
  output: ''
  output_image: ''

```

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: connect_jupyter_server
  code: print(b)
  outputMode: autoParacraft
  output: ''
  output_image: ''

```


### 连接临时容器 （敬请期待）
我们也提供临时云容器服务，敬请期待。

#### Chat GPT 大语言模型支持
选择AI对话, 可以输入中英文等自然语言, 我们通过open ai或百度文心一言的大语言模型服务提供答案。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: AI
  code: 可计算文档是Keepwork的重要功能，记住了么？
  outputMode: autoParacraft
  output: >-
    是的，可计算文档是Keepwork的一个重要功能。可计算文档是指在文档中插入数据、公式、图表等功能，使文档可以自动计算、更新、分析和呈现结果。通过可计算文档，用户可以在文档中进行数据输入、统计、计算、展示等工作，提高文档的实用性和交互性。


    在Keepwork中，可计算文档可以通过插入各种类型的表单、图表、公式等元素来实现。表单可以让用户输入数据，图表可以呈现数据，公式可以执行计算和数据分析。通过这些元素，可计算文档可以实现对数据的收集、整理、分析和展示等功能。


    使用可计算文档可以帮助用户更好地理解和利用数据，提高工作效率和准确性。同时，可计算文档还可以与其他Keepwork功能进行集成，如团队协作、数据分析和表单收集等，为用户提供更全面、便捷的解决方案。

```

一个文档中可以有多个AI对话， 他们按照前后顺序共享同一个上下文。 例如你可以继续提问。 

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: test
  language: AI
  code: 我刚刚说的，keepwork的重要功能是什么？
  outputMode: autoParacraft
  output: Keepwork的重要功能是可计算文档。

```

你可以修改任何提问，并重新执行。 回答是记录在文档中的，不点运行不会重新计算的。

:point_right: 登录才能提问，目前免费用户每天可以问10个问题，会员每天100个，未来可能调整策略。

### 自动化测试、答题系统
我们可以将1个或多个代码块串联。 当用户点击任意一个代码块时，串联的代码块都会顺序执行， 并且log会输出到被点击的代码块中。 同时，我们还可以在浏览模式隐藏代码块。 这样我们可以：
- 在第一个代码块，设立setup测试环境，（可设置为隐藏）
- 在第二个代码块，让用户答题，写代码。
- 在第三个代码块，检查答题的结果，并输出是否正确，并上报 （可设置为隐藏）。

下面是一个让用户计算`1加到100等于多少`的题目的例子

首先我们在第一个代码块中，准备下output函数（已隐藏，可切换到编辑模式查看）。
```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    function _G.output(value)
        _G.lastOutput = value
        print(lastOutput)
    end
    print("请用output(res)输出")
  outputMode: hideParacraft
  output: |
    请用output(res)输出
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: true

```


请用`output(result)`函数打印出1加到100的结果，点击运行提交结果。
```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    local r = 0
    for i=1, 101 do
       r = r + i
    end
    output(r)
  outputMode: autoParacraft
  output: |
    5151
  output_image: ''
  serialBatchExecution: true
  hideInNonEditMode: false

```

下面是一个判断用户是否回答正确的检测代码（已隐藏，可切换到编辑模式查看）。
```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |
    if(tostring(lastOutput) == "5050") then
       print("回答正确!")
    else
       print("回答错误!")
    end
  outputMode: autoParacraft
  output: |
    回答错误!
  output_image: ''
  serialBatchExecution: true
  hideInNonEditMode: true

```


### NPL CodeLab vs Jupyter CodeLab
- NPL codelab指我们研发的基于keepwork.com的可计算文档IDE。 
- Jupyter codelab指Jupyter官方notebook, 也包括很多第三方实现，例如google codelab, vs code jupyter, jupyter lite, 等。 

| |**NPL CodeLab** | **Jupyter Lab** (Google CodeLab)|
|--|----|---|
| 支持WASM的边缘计算。（适合学校离线场景，不受算力影响）| :smile: 支持 | 官方版本不支持 |
| 支持3D仿真和动画。适合K12到大学的课程呈现。 | :smile: 支持 | 不支持， 只适合大龄用户 |
| 文件存储格式 | :smile: 人类可读写markdown | ipynb为json格式，不适合人类读写 | 
| 支持单页面，多运行环境内核（云+本地）| :smile: 支持 | 不支持 |
| 支持NPL，Python， C/C++的离线计算 | :smile: 支持 | 官方版只有python |

## 参考资料
- 阿里云DSW (DataScienceWorkshop 交互建模): https://help.aliyun.com/document_detail/441723.html?spm=a2c4g.163684.0.0.3f5719e6bUqupt
- 百度飞桨(BML Notebook)：https://ai.baidu.com/bml/