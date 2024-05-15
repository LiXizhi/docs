## 制作 Chat GPT 聊天机器人

- :point_right: **目标1**：制作一个3D虚拟人， 点击人物时，输入对话，通过ChatGPT大语言模型API返回语音+文字的结果。
- :star: **目标2**：给虚拟人增加预设的知识，让它按照我们的要求进行对话。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/27317/raw#1688010477697image.png
  ext: png
  filename: 1688010477697image.png
  size: 211933
  isNew: true
          
```

### 第一步：申请ChatGPT API key
你需要到 https://openai.com 免费申请一个API KEY。我们也即将支持国内和我们自己的类ChatGPT算力服务，不过目前ChatGPT的效果是最好的。由于注册方法比较繁琐， 这里我们直接提供一个注册好的key. 我们将它写到一个我们定义的表变量`openai`中。

```lua
local openai = gettable("openai")
openai.api_url = "https://open2.aiproxy.xyz"
-- 在这里输入openai的密钥，以及代理服务器地址
openai.api_key = "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"
```

### 第二步：实现对话API
我们创建一个openai.ask函数， 调用openai的http api接口，选择`gpt-3.5-turbo`作为LLM的大语言模型，当然我们也可以用其他openai提供的模型。 

```@CodeBlock
styleID: 0
codeblock:
  projectId: '1205777'
  title: ''
  name: openai
  language: npl
  code: |-
    local openai = gettable("openai")
    openai.api_url = "https://open2.aiproxy.xyz"
    openai.api_key = "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"

    function openai.ask(content)
        local input = {
            url = openai.api_url.."/v1/chat/completions",
            options = {CURLOPT_PROXY = openai.http_proxy, CURLOPT_ALLOW_SLOW_REQUEST=1},
            form={
                messages={ { content=(openai.preKnowledge or "")..content, role="user" } },
                model="gpt-3.5-turbo" 
            },
            headers={ Authorization="Bearer "..openai.api_key },
            json=true,
        }
        local reply;
        
        System.os.GetUrl(input, co:MakeCallbackFunc(function(err, msg, data)
            echo({err, msg})
            if err == 200 then
                reply = data.choices and data.choices[1].message.content
                reply = string.gsub(reply, "\n\n", "")
            end
            resume();
        end))
        yield()
        
        return reply;
    end    
  outputMode: autoParacraft
  output: ''

```

### 第三步：创建虚拟角色并调用openai.ask
我们需要创建一个电影方块，在电影方块中添加我们希望的角色，这里我们选择帕帕的人物形象。然后创建另外一个代码方块，添加下面的逻辑：当角色被点击时，调用openai.ask函数，将结果阅读出来`playText`，以及在人物头顶显示出来`say`。现在，点击运行试试看吧！

```@CodeBlock
styleID: 0
codeblock:
  projectId: '1205777'
  title: ''
  name: test chat GPT
  language: codeblock
  code: |
    say('点击我提问');
    registerClickEvent(function()
      ask('请输入问题', true);
      say('思考中...');
      result = openai.ask(get("answer"));
      say(result);
      playText(result, nil, tonumber('0'));
    end)
  outputMode: autoParacraft
  output: ''

```


### 提高：给虚拟人增加预设的知识

ChatGPT是预先训练好的模型， 它使用互联网上1T左右的文字数据进行训练，所以他并不知道这1T数据之外的信息。
> 那么如何让它知道额外的信息呢？

其实我们只要写prompt, 也就是给他一些提示文字。 目前提示文字最长2000字，未来会支持更多。 但是如果你要支持更多的预设知识，就需要训练你自己的大语言模型了， 你还记得么， 前面我们用的是`gpt-3.5-turbo`模型。

训练模型需要几天时间，并且需要很好的GPU显卡， 这里我们先用prompt的方式， 告诉虚拟人一些知识，例如：

```@CodeBlock
styleID: 0
codeblock:
  projectId: '1205777'
  title: ''
  name: openaiknowledge
  language: codeblock
  code: |
    text = [[
    paracraft is 帕拉卡. 
    你的名字叫帕帕。
    你出生在中国。
    ]]
    local openai = gettable("openai")
    openai.preKnowledge =  text
  outputMode: autoParacraft
  output: ''

```

你可以随意修改上面的知识，然后点击运行。此时你可以通过任何语言（例如中文或英文）以任何方式问它相关的问题， 看看它是否可以正确的回答出来, 例如：`what is your name? 你在哪里出生的？`。 每次运行结果会不太一样， 不过很可能它会回答下面的内容：

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/27318/raw#1688012456734image.png
  ext: png
  filename: 1688012456734image.png
  size: 110664
  isNew: true
          
```