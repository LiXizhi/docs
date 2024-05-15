# 英文单词模板

## 更新
  v1.2 加入结束后回调、是否展示规则界面、每组单词提问重复次数（前5次不重复）的配置

## 使用说明


从资源商城下载单词模板并放置在场景中即可使用
右边的方块是模板功能代码，左边是例子。启用模板功能只需要激活右边的方块，右边的开关默认打开。
  
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29018/raw#1691718951620image.png
  ext: png
  filename: 1691718951620image.png
  size: 206342
  isNew: true
          
```


## 模板说明
模板功能：快速搭建用户学习英文单词游戏
模板有一个内置的例子，点击左边按钮激活例子代码方块，即可看到单词游戏的界面。

首先显示本组所有单词，用户阅读记忆本组单词，完成后点击"OK"

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29020/raw#1691719049448image.png
  ext: png
  filename: 1691719049448image.png
  size: 1224051
  isNew: true
          
```

然后将跳转到选择答案的界面，答题会自动计分
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29021/raw#1691719304885image.png
  ext: png
  filename: 1691719304885image.png
  size: 728186
  isNew: true
          
```

 
## 模板配置

### 图块编程
左边的例子代码方块可以按需复制，快速建立单词游戏

首先加入 "创建单词游戏窗口"代码图块，然后内嵌"创建单词组"，在里面加入五组单词（严格规定必须是五组），然后运行代码即可开始游戏
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29019/raw#1691719039141image.png
  ext: png
  filename: 1691719039141image.png
  size: 84681
  isNew: true
          
```


多组单词的写法：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29022/raw#1691719561966image.png
  ext: png
  filename: 1691719561966image.png
  size: 97636
  isNew: true
          
```

### 代码编程
若用户有一些编程基础，或者认为图块配置太麻烦也可以直接切换到代码编程
以下示范了三组英文单词游戏的配置：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29023/raw#1691719721341image.png
  ext: png
  filename: 1691719721341image.png
  size: 71052
  isNew: true
          
```
代码（可以直接复制） ：

```javascript
local EnglishWords = {
    {
        {en = "black", zh = "黑"},
        {en = "pink", zh = "粉红"},
        {en = "purple", zh = "紫"},
        {en = "orange", zh = "橙"},
        {en = "brown", zh = "棕"}
    }, {
        {en = "singer", zh = "歌唱家"},
        {en = "writer", zh = "作家"},
        {en = "actor", zh = "男演员"},
        {en = "actress", zh = "女演员"},
        {en = "artist", zh = "画家"}
    }, {
        {en = "pear", zh = "梨"},
        {en = "tomato", zh = "西红柿"},
        {en = "potato", zh = "土豆"},
        {en = "peach", zh = "桃"},
        {en = "strawberry", zh = "草莓"}
    },
}
broadcast("showEnglishWordsWindow", EnglishWords)
```