## 自主人物动画系统

### AI驱动的自主动画系统
在paracraft中，我们可以通过3D视觉和人工智能算法自动生成人物动画，从而对复杂的3D场景和文字目标做出和人类相似的NPC角色行为。 第一步用户可以在电影方块中制作骨骼动画和3D环境，两者结合生成动画训练数据，也就是长期记忆，然后当人物符合某些视觉或文字条件时触发对应的动画。原理就像人脑中存储了大量的动画和记忆，当符合某些条件时去播放它们，就形成了如同人类的自主行为。详情请看演示视频： https://keepwork.com/official/tips/s1/1_80

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26360/raw#1682414754937image.png
  ext: png
  filename: 1682414754937image.png
  size: 595751
          
```

### 动画驱动的机器人控制系统

文档和演示请见：https://keepwork.com/official/docs/tutorials/robot_intro


### 用代码方块控制骨骼的参数

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29472/raw#1693827540523image.png
  ext: png
  filename: 1693827540523image.png
  size: 92665
  isNew: true
          
```

在代码方块中，你可以使用下面代码，调整某个骨骼的放缩、旋转和位移。例如，将Neck骨骼X方向做一个放缩。
如果你希望调整主角, 前面加上`becomeAgent("@p")`

```lua
-- becomeAgent("@p")
local var = actor:GetBonesVariable():GetVariables().Neck;
if(var) then
    local scale = var:GetVarByName(var:GetScaleName())
    local trans = var:GetVarByName(var:GetTransName())
    local rot = var:GetVarByName(var:GetRotName())
    
    if(scale) then
        var:SetTime(0)
        scale:AutoAppendKey(0, {1.6,1,1}, true)
        scale:LoadFromTimeVar()
    end
end
```

我们也可以用电影方块中的骨骼参数，设置某个骨骼。注意需要调用`entity:EnableAnimation(true)`才能重新激活默认动画。

```lua
becomeAgent("@p")
playBone("R_UpperArm", 0)
local entity = GetEntity()
entity:EnableAnimation(true)
```