# 导入与导出

Paracraft支持FBX和GLTF/GLB格式的3D模型导入。 以及GLTF格式的3D模型与场景的导出。

## FBX等转成X模型文件

在发行游戏时，**我们强烈建议都导出为X文件**，X文件是Paracraft的内部默认模型格式，保证可以向前兼容和跨平台。 

例如:
/exportxfile test.fbx
/exportxfile test.bmax

## 导入FBX模型
FBX是autodesk公司的通用模型文件，FBX可以直接导入Paracraft。NPLRuntime支持FBX格式的读写，但是由于FBX存在各种SDK版本的差异，我们在产品发布时，建议使用NPLRuntime内置的X文件，保证文件可以被未来版本的NPLRuntime读取。

> [Legacy plugin: ParaEngine X-file Exporter for 3dsmax 9.0](https://github.com/LiXizhi/ParaCraftSDK/tree/master/tools/ParaEngine3dsmaxPlugin/3dsmax_9_exporter_32bits_dll)

### 导出选项
在Maya或3dsmax中选择导出..., 请注意如下导出选项：
> * 建模时注意：单位为`米`，面向`X轴`正方向.1米对应一个方格大小。 太大会导致模型不显示。
> * 导出时请选择`Up-axis`为Y轴（Y轴朝上）
> * 建模时，模型以+x轴为正前方朝向
> * 请使用`FBX 2014/2015`的版本。一般需要3dsmax/maya 2015, 2016, 2017以上的版本
> * 如果你希望FBX中内置贴图文件，请选择`Embed Media`. 否则贴图必须放在FBX的同目录下或者APP的某个子目录中
>   * 贴图必须为`png, dds, jpg`格式
> * 文件扩展名建议小写：`boy.fbx`, 不是boy.FBX
> * 每个顶点最多受到4个骨骼的影响， 超出4个权重较小的会被忽略
> * 你可以`Export Selected`, 有权重的骨骼会自动导出，但是要记得选择那些没有权重的骨骼，例如`att_lefthand`
> * 在引擎中显示的模型可能左右与Max,Maya中是反的. 
> * [注意] 由于我们无法区分0和360度的差别，所以所有骨骼的两个相邻的旋转关键帧不能`超过或等于`180度：例如不支持从0转到360度。 因为0和360都是0度最终效果是不旋转。如果要旋转一周请用多个关键帧，例如从0到179到181再到360。
> * 静态的模型，最好都删除Skin, 这样会极大的减少CPU。 有Skin的Mesh即时没有动画，引擎也会按照Skin的方式计算定点，比静态模型慢很多。 没有Skin，但是骨骼的动画依然可以有。但是一旦使用了Skin，务必保证Skin涵盖所有Mesh的定点。

### 应该导出哪些内容
- 注意导出的范围：网格，相机，灯光，动画设备等
- 应用程序通常可让您导出选定的对象或整个场景
- 确保只导出所选场景或从场景中删除不需要的数据
- 网格 
   - 删除施工历史(construction history)，Nurbs，Nurms，细分曲面必须转换为多边形 - 例如三角形
   - 注意：导出前尽量合并网格`Mesh->Combine`，一些大的场景Maya导出可能要10分钟，耐心等待
   - 注意：导出前尽量`Modify->Reset transform`
- 动画 - 选择正确的帧率，动画长度等
- 混合形状/变形 - 确保您的Blendshapes（Maya）或Morph目标（Max）分配/设置了导出网格
- 纹理 - 确保您的纹理已经存成dds或png,jpg格式。可以选择内置纹理(embedded texture)
- 平滑 - 检查是否要平滑组和/或平滑网格

### 基本制作原则

#### 放缩和单位
- 按比例缩放对照明和物理模拟都很重要。
- 将系统和项目单位设置为米(Metric)，以使软件与ParaEngine保持一致。
   - 请注意，不同的系统使用不同的单位 - 例如，Max的系统单位默认值是英寸，而Maya则是厘米。
- 动画帧率默认值可以在不同的包中有所不同。因此，最好在整个流水线中一致地设置（例如，引擎用的是30fps，推荐所有动画都用30FPS制作和导出）
#### 文件和对象
- 您的场景名称对象合理和唯一。这有助于您定位和排除项目中特定的网格。
- 避免使用特殊字符，如*（）？“＃$。
- 为对象和文件使用简单但描述性的名称，以便稍后进行复制。
- 保持层次结构尽可能简单。
- 明智的命名对象可以帮助您快速找到事物

#### 网格Mesh

- 用高效的拓扑构建。只在需要的地方使用多边形。
- 如果几何体太多，则优化几何体。许多人物模型需要被艺术家智能地优化甚至重建，特别是如果源自或建立于：3D采集数据,波塞尔,ZBrush的用于渲染的其他高密度NURBS补丁模型
- 在你能负担得起的地方，建筑物，景观和建筑物中均匀分布的多边形将有助于传播照明，避免扭曲。
- 避免很长的三角形。
- 用于构造对象的方法可能会对多边形数量产生巨大影响，特别是在未优化的情况下。600个多边形听起来可能不是很多多边形，但是如果在一个场景上使用了40次，那么就很多了。一个好的经验法则往往是从简单开始，并在需要的地方添加细节。添加多边形总是比拿走更容易。

#### 纹理Texture

- 纹理应该为2的次方（例如，512x512或256x1024）的纹理，则纹理将更加高效，不需要在构建时重新缩放。您最多可以使用4096x4096像素，但2048x2048是许多图形卡和平台上可用的最高级别。一般推荐256*256和512*512
- 在线搜索有关创建优质纹理的专家建议，但其中一些准则可以帮助您从项目中获得最有效的结果
- 在工作目录中保存高分辨率源文件（例如.psd文件）。但是导出前要替换成例如256x256优化后的.png, .jpg或dds文件。
- 请确保您的3D文件引用相同的纹理，保存或导出时保持一致。
- 利用您的纹理中的可用空间，但要注意不同材质需要同一纹理的不同部分。您最终可以多次使用或加载该纹理。
- 利用无缝重复的平铺纹理。这使您可以在空间上重复使用更好的分辨率。
- 从位图中删除容易引起注意的重复元素，并注意对比度。要添加细节，请使用贴花decals和对象来分解重复。
- 从照片创建“纹理”页面时，请将页面缩小为可重复的单个模块部分。例如，相同的窗户应该共用贴图。这意味着您可以为该窗口获得更多的像素细节。

### 多动作
#### 方案1：无需其它文件
* 所有动作在同一个文件中：并且人物所有动作时长都小于10秒
* [10*n, 10*(n+1)] 秒之间的动作代表id=n的动作。 注意动作结束的时间为10秒区间中的最后一个关键帧。

#### 方案2：需要同名的XML文件
* 所有动作在同一个文件中：对动作时长没有限制
* 需要一个同名的XML文件。例如boy.fbx和boy.xml. 

boy.xml文件格式如下

```
<?xml version="1.0" encoding="utf-8"?>
<anims neck_yaw_axis="x" neck_pitch_axis="-z">
  <anim name="standing" id="0" starttick="0" endtick="40"  looptype="0"/>
  <anim name="walk" id="4" speed="3.1" starttick="50" endtick="74"  looptype="0"/>
  <anim name="run" id="5" speed="5" starttick="80" endtick="100"  looptype="0"/>
  <anim name="back" id="6" starttick="110" endtick="120"  looptype="0"/>
</anims>
```
* anims@neck_yaw_axis: 默认的头部左右转动轴。如果没有此参数将禁止头部转动。 例如"x","y","z","-z"等。
* anims@neck_pitch_axis: 默认的头部上下转动轴。如果没有此参数将禁止头部转动。 例如"x","y","z","-z"等。
* anim@name: 表示动画名字，只是方便用户看到
* anim@id: id 是内部动作ID， 请参考[内部动作ID列表](#内部动作id列表)。0表示待机， 4是走， 5是跑
* anim@starttick， endtick: 动作区间。单位是帧tick.
* anim@speed: 人物行走速度。单位m/s. 默认速度一般是4m/s. 
* anim@looptype: 循环类型. 0 循环， 1 不循环

### 骨骼
为了让同一个项目产品中的的动画可以尽量通用，我们建议所有的人物初始绑定姿势(Initial Bone Pose)是一样的。 我们建议使用著名的Da Vinci 达芬奇姿势作为初始绑定姿势。

> 友情提示：请注意人物大小，朝向和姿势. 

如果骨骼后缀名称为：
* _b 	面向摄影机
* _u 	面向摄影机,但朝上的坐标轴固定 

### 关于插件点
手持装备等需要插件点。插件点是一些特殊命名的骨骼。一般你可以创建一个BOX对象，改名字后，连接到对应的骨骼上。 
 * att_lefthand: 左手
 * att_righthand: 右手
 * att_head: 头部，帽子
 * att_text: 文字，人物名字
 * att_ground: 地面，地面光环之类
 * att_leftshoulder: 左肩
 * att_rightshoulder: 右肩
 * att_boots: 靴子，一些汽车喷气，云彩之类的效果
 * att_neck: 脖子
 * att_mouth: 嘴
 * att_face or att_overhead: 面部，额头
 * att_leftear: 左耳
 * att_rightear: 右耳
 * att_back: 背部，书包，翅膀之类的
 * att_waist: 腰部
 * att_mount or att_shield: 默认坐骑点
 * att_mount[0-f]: att_mount0, att_mountf0, etc. 座位，车辆的化可以有最多256个座位。

### 内部动作ID列表
下面动作ID，引擎内部的自动机会自动切换。 ID<1000的动作为内部动作， 大与1000为外部动作。
```
0 	STAND 站立姿势
1 	DEATH 死亡
4 	WALK 向前走
5 	RUN 向前跑
13 	WALKBACKWARDS 向后走
37 	JUMPSTART 向上跳的起始动作
38 	JUMP 跳动中，在空中的动作
39 	JUMPEND 落地的动作
41 	SWIMIDLE 游泳（水中）的待机
42 	SWIM 向前游动
43 	SWIMLEFT向左游动
44 	SWIMRIGHT向右游动
45 	SWIMBACKWARDS 向后移动
91 	MOUNT 缺省的坐骑
153 	CUSTOM0 附加待机动作，会随机插入到0号待机动作中
154 	CUSTOM1 附加待机动作
155 	CUSTOM2 附加待机动作
156 	CUSTOM3 附加待机动作 
```

### 材质Material
注意是材质名， 不是贴图的名字
* 所有材质使用的贴图长宽必须是2的n次方
* 如果材质名字以`_r`或`_r[0-9]`结束，则为可置换贴图。可置换贴图可通过程序动态替换所在ID的贴图
* 贴图文件名： 如果文件名以`_32bits`结束，则为32位高清图片，例如`tex_32bits.png`,否则为压缩格式，会有色彩失真或模糊。

#### 贴图文件路径
对于非嵌入式贴图。如果贴图名字为: "C:\XXX\MyApp\Texture\AAA\BBB.png", FBX模型在"Model\BBB.fbx"
我们会按照下面的次序寻找贴图，直到找到贴图。 
- `Model/BBB.png` 先尝试模型所在目录
- 按照父路径(跳过最上级目录)依次寻找
  - `MyApp/Texture/AAA/BBB.png` 
  - `Texture/AAA/BBB.png` 
  - `AAA/BBB.png` 
  - `BBB.png`
- 如果没有找到，则用默认贴图，并输出warning

如果FBX导出是，使用了相对路径`..\`， 此时如果贴图名字为: ..\Texture\BBB.png", FBX模型在"Model\XXX\BBB.fbx"
我们会按照下面的次序寻找贴图，直到找到贴图。 
- `Model/XXX/BBB.png` 先尝试模型所在目录
- 用相对FBX的路径尝试一次: `Model/Texture/BBB.png`
- 按照父路径(跳过最上级目录)依次寻找
  - `Texture/BBB.png` 
  - `BBB.png`

> 所以建议美术制作时，如果是这种全局路径最好直接放在"C:\MyApp\Texture\AAA\BBB.png"，用一个尽量浅的目录，这样第一次就能找到`Texture/AAA/BBB.png`

**材质名称规范**

材质名称可以是任意名字加下面任意后缀的组合：例如: `my mat_r_b_l1`

* _r[0-9] 	可置换贴图, 如果只有一个用r, r和_r2语义是一样的。可通过程序置换皮肤贴图。
* Opacity通道：除了Diffuse通道，如果材质还有opacity通道则默认启动AlphaTesting. 当Alpha小于0.5则全透明。如果不希望有AlphaTesting而是平滑渐变的，请使用`_b`材质。
* _b 	关闭材质的Alpha Testing. 会损失一部分渲染性能，如果可以用AlphaTesting代替，尽量不要加_b. 除非是一些半透明材质。
* _a 	强制关闭物理碰撞：当模型材质没有`_p`材质时，加入`_a`可以去除普通模型的物理， 否则所有非透明面都视为有物理碰撞。 
* _p 	强制启动物理碰撞：当模型材质中有`_p`材质时，所有没有`_p`的材质都视为没有物理。 所以用户可以用`_p`和`_a`两种方式控制模型的物理，如果都没有指定则所有非透明面都视为有物理碰撞。
* _t 	关闭Z-write, 他会从远到近的渲染透明的物体。 尽量少用, 影响性能。
* _l 	强制本地渲染, 即使材质使用了_t等透明参数， 面片组也不会被从远到近的排序渲染。 但是在模型内部会排序。使用_t_l，不会造成性能影响。一些贴近地面或模型的透明面，可以使用它， 例如地表附近的特效， 人物的眼镜等。
* _u 	关闭材质的光照
* _d 	叠加贴图的颜色
* _c[0-9] category id 0-9. 在某些Shader中使用的材质ID。 例如paracraft中8代表水，9是镜子，5是火把，50是金属， 31是树叶等。
* _c 	永远面向摄影机的材质. 只对静态模型有效, 动态模型用骨骼. 材质的模型的几何中心为旋转原点. 如果有多个面，请用不同的材质命名, 例如mat0_c, mat1_c,mat2_c 注意: 模型必须朝向某个方向y
* _y 	永远面向摄影机, 但朝上轴固定的材质. 只对静态模型有效, 动态模型用骨骼. 材质的模型的几何中心为旋转原点. 如果有多个面，请用不同
的材质命名, 例如mat0_y, mat1_y,mat2_y
* 镜面反射 	选择Reflection Map, 类型是Ray Tracing. 目前只能是水平面。慎用，尽量只在Portal内景中用，影响性能的。
* 光照贴图 	选择Reflection Map, 指定Bitmap贴图为Lightmap. 单个模型, 必须全部使用Light map

**常用组合**

* _b_a_t_u_d 	透明的有叠加效果的魔法效果。 例子 model/test/material/*.*
* _b_a_t_u_d_c 	夜晚点光源的效果. 面向摄影机, 例子 model/test/material/*.*
* _a009 	序列帧动画, 例子 fire_a001.tga, ..., fire_a009.tga, 指定最后一张。
* _fps10_a009 	序列帧动画, 用每秒10帧来播放, 指定最后一张。
* 贴图名字是*_pg2.png 	比如桥的围栏呀，火焰山的路两侧的透明面， 都可以用pg2(physics group 2). 这样人物会被挡住，但是摄影机不会， 主要是不影响鼠标的点击。 

#### DDS贴图
手动导出dds格式贴图需要注意以下几点：

* DXT通道的选择，DXT是针对贴图的透明通道进行压缩，不同的压缩方式会得到不同的通道效果和贴图大小。
 * DXT1 RGB (No Alpha) 没有透明通道
 * DXT1 ARGB (1 bit Alpha) 产生的透明通道为黑白两种颜色，通道锐利，可用于树木花草等不需要半透明效果的材质。
 * DXT3 ARGB (Explicit Alpha) 1:4 使用了4Bit Alpha，可很好地用于alpha通道锐利、对比强烈的需要半透明和镂空材质。
 * DXT5 ARGB (Interpolated Alpha) 1:4 使用了线形插值的4Bit Alpha，特别适合Alpha通道柔和的材质，比如高光掩码材质。 
 * MIP Map的选择，MIP Map是根据摄影机的距离来调用不同尺寸大小的贴图以产生柔和的视觉效果。MIP Map一般生成为9张从大到小的贴图，有MIP Map和没有MIP Map的贴图效果对比如下，左边是没有MIP Map的地表贴图右边是有MIP Map的地表贴图。 

### 模型物理
有两种方式给模型添加物理材质。 一种指定`非物理面`， 一种是指定`物理`面。 两种都可以的。 
* `_a` 	强制关闭物理碰撞：当模型材质没有`_p`材质时，加入`_a`可以去除普通模型的物理， 否则所有非透明面都视为有物理碰撞。 
* `_p` 	强制启动物理碰撞：当模型材质中有`_p`材质时，所有没有`_p`的材质都视为没有物理。 所以用户可以用`_p`和`_a`两种方式控制模型的物理，如果都没有指定则所有非透明面都视为有物理碰撞。

> 如果模型大多数材质都有物理， 只有个别没有物理就用_a, 这样就不用单独做物理材质了。 但是一旦用了`_p`材质, 则模型的所有物理都需要用`_p`标注出来。 两种方式美术师可以根据模型的特点来做。 

物理 为需要产生阻挡的面，一般小花小草类植物和体积特别小的物品均不需要物理，材质后跟_a即可。比较复杂的多边行则需要简化用来阻挡的面，因为默认情况多边形就是引擎中产生物理的面。首先将需要简化物理面的材质名后加上_a,然后手动创建新的简化过的多边形即可，不需要赋予任何材质和命名。对于人物角色不可能到达的位置则可以直接去掉物理，因为一般是用来阻挡角色的。一般情况下多边形结构越复杂越密集的地方简化程度越大。

如果为一个有内外的墙加物理，内外之间要有至少几个厘米的厚度，避免物理计算时可能会有问题。

#### aabb包围盒
Axis Aligned Bounding Box(aabb) 是一个能够近似代表人物的Box区域, 可以通过建立一个Box模型并将其命名为aabb指定。 这个区域被引擎用来做渲染优化，人物高度, 物理检测等用途。如果没有指定，则是网格没有绑定前的包围盒。 

给多边形命名为aabb即可，一般为长方体(box)。 包围盒可以控制物体离摄影机多远后不被显示和控制自身被点选的区域。
* 物体过于庞大，需要手动建立相对较小的包围盒。
* 粒子等部分特殊物体默认生成包围盒过小或者没有，需要手动建立包围盒。 

### UV 动画
uv动画是指通过在程序运行时动态改变纹理坐标，实现动态效果的纹理动画，使用uv动画可以实现水流动，火焰燃烧等效果。 由于FBX并不支持保存UV 动画信息， 所以引擎是通过读取材质的附加属性来设置UV 动画的。 

给材质增加若干个名字为TexAnims_key[0-9][0-9][0-9]_r|t|s 类型为向量的附加属性即可。
其中名字TexAnims_字段， key010 表示关键帧， r|t|s 是指uv动画类型， 分别表示旋转， 坐标变换， 缩放。
* 当为r时， 向量x 表示旋转的角度， y,z 用来表示旋转的原点， 0，0 表示为纹理的左上角， 1， 1表示为纹理的右下角， 0.5， 0.5则为纹理的中心点， 默认值为0，0，0
* 当为t时， x, y为纹理的位移offset 取值为0——1。 z无意义。  默认值为 0， 0， 0
* 当为s时， x, y为纹理的uv坐标缩放值， z无意义。 默认值为 1， 1， 0

* 播放UV动画时需要关闭Z-write， 命名时参考材质名称规范

### 换装系统
如果模型的名字或路径中包含"CustomGeoset"，则默认为可换装角色。 此时我们可以用下面的Mesh命名方式来定义换装。 

我们需要将可换装人物的部分分成多个Mesh对象，并用下面的方式命名Mesh对象。 
可换装的部件的网格名称格式为`[名字|数字]_[数字]` 或 `cc_dd`, "cc" 是一个代表类别的名字或数字（名字与数字的对应关系见后文）；"dd" 是从1开始的装备序号.
如果网格名为0（也就是没有按照上面的方式命名）, 这个网格会一直显示. 每个类别下最多只能有1个网格显示.
例如名称为5_01和5_02的对象只能有一个显示. 注意多个网格对象可以共用一个编号. 

下面这些，都是合法的可换装装备名
```
"Hair_01" = "00_01" = "1",
"hair_02" = "00_02" = "2",
"Boots" = "05_01" = "5_1" = "501",
"Boots_02" = "05_02" = "502",
"Unknown name" = "0",
```

网格名字的前半部可以用内置的英文名字， 例如Hair， Head之类的， 也可以直接用数字。  名字与数字的对应关系如下

```
"hair" = 0, 头发
"facialhair" = 1, 胡子
"eyeaddon" = 2, 眼罩或眼镜 
"head" = 3, 头
"hand" = "gloves" = 4, 手或手套 
"boots" = 5, 鞋子
"ears" = 7, 耳朵
"shirt" = "armsleeves" = "sleeves" = 8,  衣服
"pants" = 9, 裤子
"wings" = 10, 翅膀
"tabard" = 12, 战袍
"robe" = 13, 袍子
"skirt" = 14, 裙子
"cape" = 15, 披风
```
一般来说，你可以自定义这些类别的含义。 类别最多16个， 每个类别下的编号小于99. 通常，你不用全部类别，可能只需要：头发， 上衣， 裤子就可以了。 

在NPL脚本中， 你可以通过SetCharacterSlot函数来选择人物的装备
```
local obj = ParaScene.GetPlayer();
obj:ToCharacter():SetCharacterSlot(slot_id, item_id);
-- 选择了编号为1的衣服(8:shirt), 其它同类编号的对象会被隐藏起来，例如8_2， 8_3都不会显示了
obj:ToCharacter():SetCharacterSlot(8, 1);  
```

### 粒子系统
跟uv 动画一样， FBX也不支持保存粒子系统信息。 所以引擎也是通过读取附加属性的方式来设置粒子系统信息。

* 粒子系统必须绑定在一个骨骼节点上。 绑定时只需在面片上面添加一个字符串类型的附加属性ps_material, 其值为材质名
* 由于粒子系统的参数非常多， 所以我们使用一段lua脚本来保存参数。 在需要生成粒子系统的材质上添加一个字符串类型的附加属性ps_param。 然后填入脚本
```
-- 粒子的颜色， 我们的粒子系统只支持3个采样， 即开始 中间 结束
-- 颜色取值范围为0-1, 分别代表r g b
color =
{
	{1, 1, 1}; -- 开始颜色
	{1, 0, 0}; -- 中间颜色
	{1, 1, 0}; -- 结束颜色
};

-- 粒子的透明度， 同颜色一样 只支持3个采样
-- 取值范围0-1
alpha =
{
	1,		-- 开始不透明
	0.5, 	-- 过度到半透明
	0,		-- 淡出中消失
};

-- 粒子大小的变化， 同上， 只支持3个采样
size =
{
	0.1,	-- 一开始很小
	1,		-- 过度到正常大小
	0.1,	-- 消失不见	
};

-- 粒子发射器的速率
rate =
{
	[0] = 1;		-- 第0帧时， 发射器一秒发射1个粒子
	[50] = 100;		-- 第50帧时， 发射器过度到一秒发射100个粒子
	[100] = 50;		-- 第100帧时， 发射器过度到一秒发射50个粒子， 然后循环到第0帧
};

-- 粒子速度
speed = 
{
	[0] = 1;		-- 第0帧时， 发射器发射出来的粒子速度为1
	[100] = 10;		-- 第100帧时， 发射器发射出来的粒子速度为100， 然后循环到第0帧
};

-- 速度的变化量， 粒子的速度为V(0) = speed + variation * rand(-1,1).
variation = 
{
	[0] = 1;
	[100] = 10;
};

-- 粒子的生命
lifeTime = 
{
	[0] = 1;
	[100] = 10;
};

-- the half length of the emitter plane
emitterWidth= 
{
	[0] = 1;
	[100] = 10;
};

-- the half width of the emitter plane
emitterHeight =
{
	[0] = 1;
	[100] = 10;
};

-- 粒子发射器的原点坐标（相对于面片的偏移量）。 
pos =
{
	x = 0;
	y = 0;
	z = 0;
};

-- how the texture blending is applied to each particle. In most cases, it is 2 ALPHA_BLEND or 4 ADDITIVE ALPHA.
-- 0 for OPAQUE; 1 ADDITIVE BLEND; 2 ALPHA_BLEND(using alpha); 3 TRANSPARENT(using alpha testing); 4 ADDITIVE ALPHA;
blend = 2;

-- this parameter is only used for sphere emitter type It is the angle between the emitting direction and downward direction in range [-Pi/2, Pi/2]. Default value is 0, which is the downward direction like the plane emitter.
rotation = 0;

-- 取值0-1 用来表示color， alpha， size的中间值， 0.5表示生命周期的一半为中间值
mid = 0.5;

-- 重力
gravity = 9.8;

-- this is 0,1,2. usually means how the particles are rendered.
-- 0 or 2 means normal particle which is centered on the particle origin with a given size.
-- 1 means that particle is rendered with origin at the particle system center and extends to the particle origin.
displayType = 0;

-- 发射器类型
-- 不设置则为plane
emitterType = "sphere";

-- it is a randome force that is applied to a particle at each frame. By default it is 0. Applying a random force will create a random path for each spawned particle.
forceRandom = 1;

-- it is a trail length of the particle, the facing of the trail is the current speed vector. 
latitude = 0;

-- it controls how fast the speed magnitude of a particle dwindles as its life is approaching the end.
-- in formula, it is V*expf(-1.0f * slowdown * p.life), where p.life is the current life of a particle in seconds.
-- if slowdown is infinitely small, there will be no slowed down; if it is big(such as 1), the particle will has no speed after just a few seconds from birth. 
slowdown = 0.01;

-- UV rotation value
texRotateSpeed = 0;

--  whether using billboard when during the particles. In most cases, this is true, because particles are usually drawn with triangle quads facing the camera.
billboard = true;

-- the texture will be evenly divided in to row * col tiles, and that ParaEngine's particle system will randomly pick one to use for each newly born particle.
row = 1;
col = 1;

-- att for rotate partice
rotate2SpeedDirection = true;
```

* 材质没有被使用是不会被导出到fbx， 为了保证材质能被导出， 可以创建一个使用这个材质的面片， 同时把他的可见性设置为不可见。 引擎遇到不可见的node， 会忽略他的所有mesh

### 常见问题
- 模型缺失或错位： 导出前请先将所有模型合并为一个mesh网格，triangulate后再导出，注意有些大的模型可能需要5-10分钟. 另外导出前最好reset transform.
- 看不见模型：注意导出的单位为米。可能是模型太大或太小
- Y方向不对：FBX导出时可选择方向
- 没有材质：FBX导出时请选择Embed Texture（只支持dds,jpg,png），或者将材质放在FBX同目录下。