## 代码测评
我们可以将1个或多个代码块串联。 当用户点击任意一个代码块时，串联的代码块都会顺序执行， 并且log会输出到被点击的代码块中。 同时，我们还可以在浏览模式隐藏代码块。 这样我们可以：
- 在第一个代码块，设立setup测试环境，（可设置为隐藏）
- 在第二个代码块，让用户答题，写代码。
- 在第三个代码块，检查答题的结果，并输出是否正确，并上报 （可设置为隐藏）。

下面是一些例子，你可以将本网页切换到编辑模式，看下是如何实现的。

### 编程题机器测评模板
3个代码块+1个测评模块。支持测试用例。

#### 题目：1加到100等于多少？
请用NPL或Python编写程序，计算`1加到100等于多少`
请用`output(result)`函数打印出1加到100的结果，点击运行并提交结果。

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |-
    -- 这里的代码是隐藏的，可以定义一些用户会使用到的函数
    function _G.output(value)
        _G.lastOutput = value
        print(lastOutput)
    end
  outputMode: hideParacraft
  output: ''
  output_image: ''
  serialBatchExecution: false
  hideInNonEditMode: true

```

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

```@CodeBlock
styleID: 0
codeblock:
  projectId: ''
  title: ''
  name: ''
  language: npl
  code: |
    -- 下面是一个判断用户是否回答正确的检测代码，会串行执行。
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

```@Quiz
styleID: 0
quiz:
  data:
    - id: 8f5062e0-e764-11ee-881d-77cd898f0ed8
      type: '4'
      title: quiz title
      score: 1
      desc: desc
      answer:
        - A
      options:
        - item: option 1
        - item: option 2
      nums: 1
      testCode: ''
      isShare: true

```

### 单选题测评模板

#### 题目 1+1真的等于2么？
请根据你的理解选择正确的答案。
```@Quiz
styleID: 0
quiz:
  data:
    - id: 1cd1dc60-e766-11ee-881d-77cd898f0ed8
      type: '0'
      title: 1 + 1 = ?
      score: 1
      desc: 这里是回答错误时的解释
      answer:
        - B
      options:
        - item: '2'
        - item: '3'
      nums: 2
      testCode: ''
      isShare: false

```