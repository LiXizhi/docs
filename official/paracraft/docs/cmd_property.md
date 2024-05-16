<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/property`**

**quick ref:**
> /property [set|get] [-objPath] name value

**description:**

```
set engine attribute value by name. 
@param set|get: default to set property. 
@param objPath: attribute model path. if not specified, we will search for name in major places. 
please see NPL code wiki (F11)->View Menu->Object Browser for possible obj paths.
for security reasons, only all, scene, gui, asset, npl can be modified
Examples: 
/property -scene-1_1 MaxBufferRebuildPerTick_FarChunk  100
/tip $(property get -all WindowText)
/property set -all WindowText helloworld
/property WindowText helloworld short cut
/property AsyncChunkMode false
/property UseAsyncLoadWorld false
/property MaxCacheRegionCount 16
/property set -camera IgnoreEyeBlockCollisionInSunlight false
/property -scene MaxCharTriangles 50000
/property -scene MinPopUpDistance 100
```

<!-- END_AUTOGEN-->

## 设置远处物体出现的最小距离
/property -scene MinPopUpDistance 100
100米内的所有物体都会显示， 不会自动隐藏。 超过这个距离， 引擎会根据物体的大小自动隐藏。 注意有些异步或远程加载的模型， 事先不知道大小， 可能需要至少到这个距离才会显示。 

## 缓存多少region的block数据
/property MaxCacheRegionCount 16
一个region等于512x512米。 一般会缓存9或16个大型地块。 超过这个数量，引擎会卸载地块以节约内存。 如果你是64位系统并且内存很大， 可以加大这个数值。 

## 设置最大显示的多边形数量
/property -scene MaxCharTriangles 50000
例如最多显示5万个多边形， 超过这个数量，模型会根据渲染次序自动隐藏。注意这个数值只影响角色，方块地形的多边形数量不算在内。 