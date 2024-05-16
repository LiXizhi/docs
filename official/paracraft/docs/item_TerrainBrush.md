## 地形笔刷和笔画
地形笔刷和笔画物品可批量修改地形地貌
![image](https://cloud.githubusercontent.com/assets/94537/17135090/88557b7e-5360-11e6-9bbf-8cc8eaa3fceb.png)

- 每个物品可以复制多个到下方快捷栏, 每个复制的物品可以有各自不同的参数：例如半径，材质，强度，子工具等。 
- 所有工具都有如下几个参数：
   - 半径： `+/-`键或按住`Shift键`并滚动鼠标滚轮
   - 强度：可输入数值(0,1] 默认为0.5
   - 材质：可用`Alt+左键`在场景中吸取，或在`E键`物品列表中选取
   - 原点：鼠标所在位置
- 点击左键可使用工具一次， 也可以按住左键不放拖动鼠标，此时每0.2秒使用一次
- `Ctrl+Z/Y`可撤销Undo/Redo. 注意：鼠标按下，拖动到抬起只算作一次操作，尽管期间可能执行了多次操作。
- 点击鼠标中键可瞬移
- 按住Shift键并点击鼠标，进入相反的模式，例如：地形的升/降, 平滑/锐化.

### 地形笔刷物品
更改地形，地貌，创造或消除大面积的水等等。 有几个子工具：
- 用Gaussian Filter`地形升降`制作山脉或峡谷： 按住Shift为降低。可以长按并拖动鼠标大面积操作
- 平滑和锐化地表： 用一个`4*4`的Filter取平均值。可以长按并拖动鼠标大面积操作
   - 提示：我们一般先用`地形升降`后再使用平滑工具。
- `地表铲平`: 将地表铲平到鼠标的高度. 可以长按并拖动鼠标大面积操作，高度会被锁死。
   - 提示：我们一般先用`地形升降`工具，然后`地表铲平`可以快速制造大面积的低洼河床或梯田。
- 在鼠标的高度创建湖泊：可以长按并拖动鼠标大面积操作，高度会被锁死。如果同时按住Shift键为取消湖泊。
   - 请先用`地表铲平`工具制造出低洼的地形（水坑），然后调大半径，从岸边你希望的高度开始点击并拖动鼠标，所有下面坑洼的地方会被自动填充。
   - 尽量不要在平地上直接使用这个工具，请从岸边开始。

注意事项：
- 液体如`水`不会随地形改变而改变
- 非方块物品：如：花草会随地形一同升降
- 升高地形时，其实是拉伸第二层，保留最上面一层
- 降低地形时，则是直接降低，露出下面的地貌。


### 画笔物品
- 需要先选择材质： 可用`Alt+左键`在场景中吸取，或在`E键`物品列表中选取

注意事项：
- 非方块类物品是在地面上方增加： 如：花，草
- 方块类物品是替换：如：石子路
- 按住Shift键可强制使用替换模式