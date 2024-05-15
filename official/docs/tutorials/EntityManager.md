# EntityManager物体管理器

我们可以在代码方块中，使用EntityManager类精确控制活动物体。 下面是一些例子。

## 创建活动模型

可以使用 GameLogic.EntityManager.EntityLiveModel:Create 创建活动模型。

```lua
local x, y, z = getX(), getY(), getZ()
local entity = GameLogic.EntityManager.EntityLiveModel:Create({bx=x,by=y+2,bz=z});
if(entity) then
  entity:Attach();
  entity:SetModelFile("blocktemplates/test.bmax");
  entity:SetScaling(1.5)
  entity:SetPersistent(false)
  entity:SetFacing(-1.57)
  entity:SetAutoTurningDuringDragging(true);
end
```

`entity:SetPersistent(false)` 可以设置模型是否被存盘。
`entity:SetModelFile("blocktemplates/test.bmax");` 设置模型的美术资源， 可以相对当前世界目录。

## 获取场景中所有角色

可以用`EntityManager.FindEntities`方法。

```lua
local entities = GameLogic.EntityManager.FindEntities({category="all", type="CodeActor"})
if(entities) then
    for _, entity in ipairs(entities) do
        becomeAgent(entity)
        say("hi")
    end
end

```

## 绘制自定义的Entity
可以使用`SetOverlayPaintFunction`函数在代码方块中自定义draw函数进行绘制

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29930/raw#1696269710694image.png
  ext: png
  filename: 1696269710694image.png
  size: 73927
  isNew: true
  isExpand: true
          
```
```javascript
NPL.load("(gl)script/ide/System/Scene/Overlays/ShapesDrawer.lua");
local ShapesDrawer = commonlib.gettable("System.Scene.Overlays.ShapesDrawer");

GetEntity():SetOverlayPaintFunction(function(entity, painter)
    painter:SetPen({width = 0.01, color="#0000ff"})
    ShapesDrawer.DrawCircle(painter, 1, 2, 0, 0.3, "z", false, 12)
    ShapesDrawer.DrawCircle(painter, 1, 2, 0, 0.3, "x", false, 12)

    -- draw text with 0.01 scaling
    painter:PushMatrix();
    painter:TranslateMatrix(1, 2, 0); -- 3d position
    painter:LoadBillboardMatrix();
    painter:DrawTextScaled(0, 0, "hello", 0.01);
    painter:PopMatrix();

    -- draw line with 0.01 width
    ShapesDrawer.DrawLine(painter, 0,0,0, 1,2,0)
end)
```