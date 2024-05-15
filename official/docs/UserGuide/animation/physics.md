## 物理仿真

### 活动模型

任意活动模型都支持刚体物理仿真，请看下面视频。paracraft内部使用的是bullet物理引擎。 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26256/raw#1681717764392physics_demo_small.mp4
  ext: mp4
  filename: 1681717764392physics_demo_small.mp4
  size: 5054541
          
```

DEMO网址： https://webparacraft.keepwork.com/?pid=1091155
```@Project
styleID: 1
project:
  projectId: '1091155'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```


通过代码创建包含物理仿真的活动模型。 需要调用`EnableDynamicPhysics`方法。

```lua
-- run as many times as you like
hide()

local cx, cy, cz = getX(), getY(), getZ()
local modelfile = GetEntity():GetModelFile();

for dz=-math.random(0,3), math.random(0,3) do
    for dx=-math.random(0,3), math.random(0,3) do
        if(dx~=0 or dz~=0) then
            local entity = GameLogic.EntityManager.EntityLiveModel:Create({
                bx = cx + dx, by=cy, bz = cz+dz
            })
            entity:Attach()
            entity:SetModelFile(modelfile)
            entity:SetPersistent(false)
            entity:EnableDynamicPhysics(true)
        end
    end
end
```

刚体物理支持多种内置形状，默认尺寸为使用资源模型的AABB包围盒。
还支持球体或自定义形状，如下：
```
entity:SetPhysicsShape("sphere")
entity:SetPhysicsShape("box")
```

也可以使用UI来添加活动物理模型，如下图。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26257/raw#1681718131246image.png
  ext: png
  filename: 1681718131246image.png
  size: '95683'
  unit: px
  alignment: left
  width: 220

```

添加后，选中模型，然后点击属性，真实物理， 可以改变模型的物理属性。 
 
```@BigFile
bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/26258/raw#1681718263106image.png
  ext: png
  filename: 1681718263106image.png
  size: '320621'
  unit: px
  width: '800'
  alignment: left

```
### 设置动态物理属性

可以用 **Entity:SetPhysicalProperty(name, value)** 设置动态物理属性， 见下面的参数。

```
-- properties that are preserved during saving
local staticPhysicsProperties = {"Mass", "LinearDamping", "AngularDamping", "GravityX", "GravityY", "GravityZ", "Friction", "RollingFriction", "SpinningFriction"}
-- @param name: it can be name like "Mass" or a table containing name, value pairs like {LinearVelocityX=1, LinearVelocityY=0, LinearVelocityZ=0}.
-- if name is nil, we will restore all static physics properties in current self.physicsProps
-- All property names and default values:
--   Mass: 1, set to 0 to make this kinematic (static) character
--   LinearDamping, AngularDamping:0, 0
--   GravityX, GravityY, GravityZ:-10
--   LinearFactorX, LinearFactorY, LinearFactorZ:1,1
--   AngularFactorX, AngularFactorY, AngularFactorZ:1
--   LinearVelocityX, LinearVelocityY, LinearVelocityZ: 0,0,0
--   AngularVelocityX, AngularVelocityY, AngularVelocityZ:0,0,0
--   LocalInertiaX,LocalInertiaY, LocalInertiaZ: 0.03, 0.03, 0.03, etc
--   Flags: 8
--   ActivationState: 2
--   DeactivationTime: 2.01667
--   Restitution: 0
--   Friction: 0.5
--   RollingFriction, SpinningFriction: 0, 0
--   ContactStiffness, ContactDamping: 10000, 0.1
--   IslandTag, CompanionId: 2, -1
--   HitFraction: 1
--   CollisionFlags: 0
--   CcdSweptSphereRadius, CcdMotionThreshold: 0, 0
-- @param value: all values should be number. default values are
function Entity:SetPhysicalProperty(name, value)
end
```