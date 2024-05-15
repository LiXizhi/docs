## 光源
Paracraft中有3种光源：1. 太阳光 2. 发光方块 3. 动态光源
### 1 太阳光
太阳光默认只有一个, 随时间改变而改变位置。 可以通过/time命令改变，或通过/sun 命令改颜色。

### 2. 发光方块
发光方块是一种点光源，某些方块可以发光，每种方块的发光距离不一样（在1-16格之间）。所有方块发出的光是同一种颜色。可以通过/light 命令统一改颜色。其中隐形光源很有用，你可以在场景中放置任意数量的光源。

### 3. 动态光源
动态光源是一种实体，有点光源，聚光灯和平行光三种子类型。动态光源采用延迟渲染技术实现，所以只有/shader 2 以上才生效。每个光源的运算开销相当于渲染一个半径和光源的最大半径一样的球体。如果球体很大会影响很多像素，fillrate是主要的性能瓶颈。 总的来说，动态光源和普通3D模型的开销类似，可以有任意多个。 

![](https://api.keepwork.com/ts-storage/siteFiles/24704/raw#1669892259697image.png)

有三种方式可以创建动态光源：
1. 通过E键菜单下的动态光源物体，像方块一样摆放在场景中。 
2. 在电影方块中，点击添加角色，并选择光源角色。
3. 通过在有光源角色的电影方块旁边放置一个代码方块可以用代码生成点光源。 

- :arrow_forward: 教学视频1：[在场景中加入点光源](https://keepwork.com/official/tips/s1/1_59)
- :arrow_forward: 教学视频2：[电影方块中加入光源](https://keepwork.com/official/tips/s1/1_60)
- :arrow_forward: 教学视频3：[代码方块中加入光源](https://keepwork.com/official/tips/s1/1_61)

#### 3.1 代码生成点光源

首先我们需要在电影方块中创建一个光源角色：
![](https://api.keepwork.com/ts-storage/siteFiles/24705/raw#1669892580225image.png)

然后在旁边的代码方块中控制这个角色运动或改变属性。
```
cmd("/shader 2")
hide();

registerCloneEvent(function(color)
    setActorValue("color", color)
    while (true) do
        moveForward(0.5, 0.01)
        turn(10)
    end
end)

clone("myself", "#ffff00")
wait(1)
clone("myself", "#ff00ff")
wait(1)
clone("myself", "#00ffff")
wait(1)

```

- :arrow_forward: 教学视频4：[绑定光源到骨骼](https://keepwork.com/official/tips/s1/1_62)
- :arrow_forward: 教学视频5：[主角手中的光源](https://keepwork.com/official/tips/s1/1_63)

### 3.2 动态光源的类型
 
有点光源，聚光灯和平行光三种子类型。
 
![](https://api.keepwork.com/ts-storage/siteFiles/24706/raw#1669892850485image.png)
 

- :arrow_forward: 教学视频6：[在场景中加入聚光灯](https://keepwork.com/official/tips/s1/1_64)


 
## 反射
 
水方块、金属方块、[方块材质](https://keepwork.com/official/docs/UserGuide/scene/block_material)都支持反射效果。 反射效果也是通过延时渲染技术实现的， 所以需要/shader 2以上才能显示。 如下图中的白天和夜晚的反射效果。 
- 反射支持fresnel菲尼尔效应，就是入射角越大反射越模糊。
- 反射支持高光效果。其中点光源和发光方块的高光位置永远在法线的延长线上（这是一个假设，因为无法计算真实的点光源位置）。太阳光的高光位置则是根据真实的太阳位置计算的。 


![](https://api.keepwork.com/ts-storage/siteFiles/24707/raw#1669893314053image.png)
图1：白天：水方块，金属方块，发光方块，点光源

![](https://api.keepwork.com/ts-storage/siteFiles/24708/raw#1669893406560image.png)
图2：夜晚：水方块，金属方块，发光方块，点光源

- :arrow_forward: 教学视频7：[光影水反的细节详解。镜子方块与金属方块。](https://keepwork.com/official/tips/s1/1_29)
