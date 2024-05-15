# Paracraft粒子化3D地形渲染系统 v1.0

**软件用途：** Paracraft粒子化3D地形渲染系统被应用在Paracraft 3D动画与编程工具软件中。它提供了一种实时渲染无穷大基于3D粒子（方块等）的3D世界的底层算法与类库实现。3D世界可以由亿万的方块粒子构成，给定一个虚拟摄影机，系统自动高效的计算可视区域中的光照和渲染数据，并提供给3D渲染引擎（显卡）显示。
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** C++
**开发完成时间：** 2012年6月1日
**发表日期：** 2012年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 基于方块粒子的3D世界数据存储与序列化
- 基于粒子的实时3D渲染系统
- 基于粒子点光源的动态光照计算系统
- 自定义粒子形态
- 支持透明，半透明材质的粒子渲染
- 支持超大地形：32公里x32公里，粒子为1米或更小。

**源代码行数**: 15万行  [点击这里查看](Paracraft粒子化3D地形渲染系统_code)

## 《Paracraft粒子化3D地形渲染系统》使用手册

Paracraft粒子化3D地形渲染系统被应用在Paracraft 3D动画与编程工具软件中。它提供了一种实时渲染无穷大基于3D粒子（方块等）的3D世界的底层算法与类库实现。3D世界可以由亿万的方块粒子构成，给定一个虚拟摄影机，系统自动高效的计算可视区域中的光照和渲染数据，并提供给3D渲染引擎（显卡）显示。

- 基于方块粒子的3D世界数据存储与序列化
- 基于粒子的实时3D渲染系统
- 基于粒子点光源的动态光照计算系统
- 自定义粒子形态
- 支持透明，半透明材质的粒子渲染
- 支持超大地形：32公里x32公里，粒子为1米或更小。

### 方块引擎
方块世界管理器管理着所有的方块世界，每个方块世界由64 x 64（x轴，z轴）个区域组成，每个区域由32 x 16 x 32（x轴，y轴，z轴）个块组成，每个块又由16 x 16 x 16（x轴，y轴，z轴）个方块（Block）组成。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4118/raw#image.png'
  ext: png
  filename: image.png
  size: '35416'
  unit: px
  width: '350'
  alignment: left

```

方块系统可以分为4层来看，同样底层是文件，在方块系统中只有ParaX文件， 往上就是方块模型： 5种模型供选择。有了模型就可以搭建方块和方块世界， 最后便是渲染和显示。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4119/raw#image.png'
  ext: png
  filename: image.png
  size: '31479'
  unit: px
  width: '450'
  alignment: left

```

#### BlockWorldManager
用来存放和管理所有创建的CBlockWorld实例，提供添加与查找的方法，支持单例模式。该类只有一个成员变量m_mapBlockWorlds，用于存放所有CBlockWorld对象和其名字的对应关系。

#### CBlockWorld
方块世界，表示一块由64 x 64 x 1（x轴，y轴，z轴）个Block块（Chunk）组成的三维空间。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4120/raw#image.png'
  ext: png
  filename: image.png
  size: '11809'
  unit: px
  width: '340'
  alignment: left

```

它管理世界中所有的方块，负责各种参数的配置，以及相关组件的操作。它保存了当前所有可见Block块，即可渲染块（RenderableChunk）的引用，用于渲染操作。方块世界之间是独立的，引擎一次也只能渲染一个世界，也就是说方块世界是最大的三维空间了。CBlockWorld有一个子类BlockWorldClient，该类实现了更多关于方块世界渲染的操作，CBlockWorld相当于是一个借口，实际使用到的是BlockWorldClient。
重要属性：
- m_activeChunks：可渲染块（RenderableChunk）的向量保存了视点（eye position）周围n个块的渲染信息。
- m_pRegions：64 x 64固定大小的BlockRegion*数组，用于存放所有加载了的区域对象。
- m_regionCache：一个int到BlockRegion*映射，作为常操作的区域的缓存。
重要方法：
- CreateGetRegion()：获取或创建Block区域，指定区域不存在时会创建一个BlockRegion对象，并将其添加到CreateGetRegion数组和m_regionCache映射中，再调用BlockRegion->Load()加载区域。

#### Block区域
BlockRegion，表示一块由32 x 16 x 32（x轴，y轴，z轴）个Block块（Chunk）组成的三维空间。它保存了这些Block块，该区域在方块世界中的坐标，也记录了垂直于y轴的平面上每一个位置的方块高度。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4121/raw#image.png'
  ext: png
  filename: image.png
  size: '8788'
  unit: px
  width: '330'
  alignment: left

```

该类提供了对其中Block和Block块的查找、修改等操作，它可从文件中加载Block区域，以及之后对区域的更新、卸载。
重要属性：
- m_thread：线程变量，用于实现区域的异步加载。
- m_bIsLocked：布尔变量，用于实现对区域操作的加锁保护。
- m_chunkTimestamp：byte向量，表示每个Chunk列是否已加载。
- m_blockHeightMap：保存每个Chunk列的高度信息。
重要方法：
- Load()：实现Block区域的加载，它先执行加载区域前需要执行的相关脚本，然后加载区域，流程如下图。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4122/raw#image.png'
  ext: png
  filename: image.png
  size: '83836'
  unit: px
  width: 550
  alignment: left

```

- LoadFromFile()：从文件加载区域。
- SaveToFille()：将修改写入文件。

#### Block块
表示一块由16 x 16 x 16（x轴，y轴，z轴）个方块（Block）组成的三维空间。它保存了空间中的方块坐标与对应的方块（Block）对象、光线信息，以及它在方块世界中的位置。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4123/raw#image.png'
  ext: png
  filename: image.png
  size: '35019'
  unit: px
  width: 460
  alignment: left

```

方块与Block对象的对应关系存放在一个16 x 16 x 16的数组m_blockIndices中，数组下标的【0-3】【4-7】【8-11】位分别表示x，y，z轴坐标，值为该方块对应的Block在数组m_blocks中的下标，-1表示该位置不存在方块。类似的，每个方块的光线信息存放在一个16 x 16 x 16的LightData类型数组中，具有光线属性的方块坐标会放在集合m_lightBlockIdice中。
并不是空间中每个存在的方块实体都对应着一个独立的Block对象，为了节省空间，相同的方块只对应同一个Block对象。这些Block对象存在数组m_blocks中，当其中某个Block对象没有与之对应的方块实体时，系统就会把它重置，但不将其从数组中删除，而是将其放入“空槽栈”，下次需要创建新的Block对象时可以重新利用这块空间，这样节省了修改数组和对应表的时间。

#### Block
方块世界最基本的元素，包含一个方块的具体信息，结构比较简单，只有三个成员变量。
- m_pTemplate：保存方块对应的模板（BlockTemplate*），其中包含该方块绝大部分的信息
- m_blockData：int16类型，方块携带的信息，当方块为空槽（Empty Slot）时，其值表示下一个空槽在m_blocks中的下标。
- m_nInstanceCount：int16类型，记录当前方块对象对应的实体方块数目，当它为0时，表示其所在的块（BlockChunk）中已经没有对应的方块实体，即为空槽。

#### 方块模型提供形式
方块模板（BlockTemplate）包含了一个Block绝大部分的信息，主要是纹理、物理属性和渲染相关的参数信息，它还含有一个方块模型对象（BlockModel）数组，提供方块各个顶点、边界盒子、纹理坐标等更细致的几何信息。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4124/raw#image.png'
  ext: png
  filename: image.png
  size: '20624'
  unit: px
  width: '400'
  alignment: left

```

对于特定类别的方块模型，我们用IBlockModelProvider接口来构造，因此，方块模板还包含一个IBlockModelProvider对象，用于生成特定类型的方块模型。方块模板会优先通过这个对象查找方块模型，如果该对象不存在则会使用自带的模型对象。
IBlockModelProvider有5个派生类，它们的继承关系如下图所示：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4125/raw#image.png'
  ext: png
  filename: image.png
  size: '33650'
  unit: px
  width: '400'
  alignment: left

```

##### Wire
WireBlockModel类用于构造线框模型，实际用于游戏中的藤蔓方块
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4126/raw#image.png'
  ext: png
  filename: image.png
  size: '96257'
  unit: px
  width: '400'
  alignment: left

```

##### Grass
CGrassModelProvider类用于构造草地，它产生的方块会有随机的偏移，从图中可以看出。

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4127/raw#image.png'
  ext: png
  filename: image.png
  size: '103468'
  unit: px
  width: '400'
  alignment: left

```

##### Linear
CLinearModelProvider类用于构造线性模型，绝大多数方块模型都是由这个类提供，比如方块、厚板、交叉平面等。

##### Slope
CSlopeModelProvider类用于构造斜坡

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4128/raw#image.png'
  ext: png
  filename: image.png
  size: '94518'
  unit: px
  width: '400'
  alignment: left

```

##### Carpet
CCarpetModelProvider类用于构造地毯
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4129/raw#image.png'
  ext: png
  filename: image.png
  size: '92802'
  unit: px
  width: '400'
  alignment: left

```

#### ChunkVertexBuilderManager
管理可渲染块（RenderableChunk），含有两个RenderableChunk数组，分别用于存放待重构（rebuild）和待上传（upload）的可渲染块。它支持单例模式，提供了处理、上传、增删可渲染块的方法。所有对可渲染块的操作都用一个互斥量保护。
ChunkVertexBuilderManager与RenderableChunk和BlockRenderTask的关系如下：

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4130/raw#image.png'
  ext: png
  filename: image.png
  size: '16957'
  unit: px
  width: '400'
  alignment: left

```


#### RenderableChunk
可渲染块，保存了该块的所有方块渲染任务，顶点缓冲区，块的位置。它负责渲染缓冲区的更新、重构以及写入内存的操作。
重要属性：
- m_renderTasks：BlockRenderTask*的向量，保存块中所有方块渲染任务
- m_builder_tasks：BlockRenderTask*的向量，保存构建器任务
- m_vertexBuffers：ParaVertexBuffer*的向量，保存块的所有顶点缓存对象
- m_memoryBuffers：ParaVertexBuffer*的向量，保存内存缓冲

#### BlockRenderTask
它表示一个方块渲染任务，包含方块模板对象、方块信息、矩形面数、顶点偏移量、该块在方块世界的位置、渲染顺序，和顶点缓存指针。提供了新建、移除渲染任务的方法，和各种属性的get和set方法。

重要属性：
- g_renderTaskPool：静态BlockRenderTask*向量，作为全局方块渲染任务池，保存所有该类的所有实例。
- m_pVertexBuffer：指向顶点缓存的指针变量。

### 地形引擎NPL脚本层API参考手册

```@IFrame
styleID: 0
iframe:
  src: >-
    https://codedocs.xyz/LiXizhi/NPLRuntime/classParaScripting_1_1ParaTerrain.html
  width: 100%
  height: 25000px

```