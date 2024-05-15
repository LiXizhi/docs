# 键盘

## 代码方块中的键盘事件

#### key down 和key up 事件

我们可以用下面的方式侦听按键按下和抬起时的消息。  

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35101/raw#1706018225336image.png
  ext: png
  filename: 1706018225336image.png
  size: 18087
  isNew: true
          
```
run是并行执行的意思
```javascript
registerKeyPressedEvent('space', function(msg)
    tip('space down');
    run(function()
        while (isKeyPressed('space')) do
            wait(0.1);
        end
        tip('space up');
    end)
end)
```