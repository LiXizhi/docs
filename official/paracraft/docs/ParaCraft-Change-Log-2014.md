[ParaCraft Change Log 2014]

2014.12.31
- 全部BaseClass的children采用了reference counted 的方式管理内存.
- upgraded to lastest build environment. executable size shrinks 2MB
- Andriod版不会在播放过程中待机了.
- 退出时d3d reference count>0不再提示非法退出而是打印error Log. 保证其他模块被正常释放.

2014.12.30
- Particle Element支持高速的材质排序通过ParticleRenderPass，提升了渲染性能。
- Particle Element支持材质的Filter等属性.  雨雪特效采用了PointFilter (消除了渲染中模糊边界). 默认为LinearFilter
- C++层的雨点特效增加了物理溅射效果
- 重构AttributeField, 支持匿名新类的扩展. 提供对C++底层对象的intrusive and unified data model. 可以访问子对象。
- 改变了所有3D对象的子对象存储结构，增加了访问速度， 支持Random Access by index.

2014.12.29
- 取消了skylight precalculation step, 单个光源获取速度有所下降， 但是整体光照性能提升，且无计算错误.
- 粒子特效支持随机动态贴图。 优化了下雪特效，修复下雨和下雪之间切换的问题。
- 底层Entity仿真速度deltaTime优化， 保证在不同渲染性能的机器上，电影播放和真实时间（Music）的同步.
- Mobile版合并WebView代码， 修复Android下log2导致Crash的Bug.
- 修复Mobile版坐下等动作资源不存在的问题
- Mobile版只读世界退出也需要用户点击确认，防止误操作.

2014.12.27-2014.12.28
- 引擎底层新增高性能的可扩展粒子系统和Billboard渲染系统
- 下雨和下雪特效用C++层实现,新增天气粒子渲染类， 效率提升50倍.  保证Mobile版中下雨场景流畅渲染.
- 下雨和下雪的每个粒子都会受到当前光照与场景中灯光的影响.
- 优化光照获取函数，彻底修复高空人物变黑的Bug

2014.12.25
- Block引擎渲染分成3个Pass了. Opaque, alpha tested, alpha blended. 其中alphatest pass禁用了mipmaping.
          alpha blended 由于禁用了discard/clip fragment shader, 速度会略有提升
- 修复PC版中fixed function pipeline 在时间改变时场景闪烁的问题.
- 修复AlphaTesting在DeferredShading光影下出现黑色边的Bug.
- 优化命令: /registeritem [-alphaTestTexture] [-blendedTexture] [-light] [block_id:2000-2999] [texture] [base_block_id]
          可以让任意自定义方块支持透明， 半透明或发光等属性. e.g.    /registeritem -light 2004 Texture/blocks/leaves_birch.png 86
- 修复AlphaBlended的distance sort算法. 基本按照由远到近渲染.

2014.12.24
- 修复Wire block tessellation bug.
- Mobile版修复背景音乐不可暂停的Bug

2014.12.23
- Block Tessellation 全面重构. 代码更加清晰, 速度更快, 显存更节约. 多边形数量最多减少到之前的1/6.
          Mobile版中体现更明显(bottleneck on bus and triangle count)
- 修复非仿真天空下12小时制天空的太阳渲染角度,保证旧世界的效果不变。
- Alpha blending is turned off during solid block rendering pass to be Early-Z friendly on modern graphics card.

2014.12.22
- Mobile版一个Chunk中的渲染会合并同材质的Block为一个DrawCall
- STL在Debug模式下太缓慢了, 取消一批用STL实现的数据结构，保证Debug模式可以较快运行. 更多内容看EASTL(EA公司的一个开源STL实现和文章)
- 修复旧版电影方块中人物坐下等动作不播放的Bug.
- Mobile版: 修复libcurl在dns timeout时可能crash的Bug.

2014.12.21
- Mobile版针对显卡Early-Z优化了AlphaTest 材质的渲染.
- GDebugger used to analyze opengl performance.  Stl contrainers in debug mode is the hot spot in win32. Draw call count is the primary hotspot on device in release mode.
- block渲染改为ChunkBuffer优先而不是材质优先, 在主流显卡的Early Z 中性能会更好一些。

2014.12.20
- 增加适合Mobile版的Checkbox_button控件
- Mobile版的Settings界面优化.
- Mobile版增加Render Stats的输出用于调试渲染性能

2014.12.19
- Mobile修复声音特效首次播放不发声的问题。
- 新增命令/createtexturepack name 生成新材质包到指定目录, 用户可以删除或替换制作自己的材质包
          重复的材质以duplicate_开头。 包含动态材质和Mobile版的材质重定向功能.
- 用新指令将默认材质包生成为SummerFieldPlus材质包, 今后作为自定义材质。 即将推出新的默认材质包代替SummerField。
- 整理了之前的一批路径错误的材质
- Skybox is rendered at precisely Z=1 修复雾化渲染错误.
- fix renderdist auto terrain generation

2014.12.18
- 修复简易shadow在shader模式下会显示的Bug
- Mobile版支持Sky仿真渲染：包括太阳， 月亮，view dependent fog light scattering.
- 创意剧场：Paracraft成为Intel2in1官方推荐的12个超级本应用之一.
- Mobile版中修复一批PC版的旧材质，将其替换为类似材质.
- 修复TrueType字体资源在部分手机中切换APP后渲染失效的Bug.

2014.12.17
- Sky时间系统从12小时，改为24小时. 白天太阳的位置略有变化(可能会影响部分影片), Block光照略有变化
- 仿真Sky模式下: 雾的颜色会根据摄影机角度自动调节, 背对太阳时雾为原始颜色。
- 仿真Sky模式下: 地平线下太阳光仍然会照亮部分天空和云彩
- Mobile版: 修复夜晚不显示的Bug
- 仿真Sky模式下: 增加月亮的渲染, 黄昏时天空会同时出现太阳和月亮
- 新增命令: /sky -moon moon_size[10-1000] moon_glow  改变月亮的大小

2014.12.16
- Sky渲染优化: Sky is rendered after solid objects but before transparent ones to avoid overdraw.
- 修复仿真天空在部分手机上不显示的Bug: z value at 0.9999 is considered outside projection space on some card.
- 修复有时仿真天空出现一条闪烁的线的Bug. fixed triangle strips adding empty triangles where necessary.

2014.12.15
- 新增slab, plate在手中的模型渲染
- 新增命令/texgen -all  -i 可以一次生成一批Block的缩略图了
- 创意剧场：《乌鸦》
- Mobile版: touch camera controller 加入了平滑， 流畅度增加，避免抖动.
- 修复高Shader模式下, 人物光照颜色不受点光源影响的Bug.
- 修复编辑模式下到世界最低处， 人物移动速度突然变快的Bug

2014.12.13-2014.12.14
- 新增命令/texgen -all  用于生成Block缩略图的texture atlas
- researched quite a few things on youtube, including c4d, qt's model/view, rsa.org, blender, etc.
- NPL based toolkit planned

2014.12.12
- 真人版Mobile Demo
- 增加Miniscene中可以渲染point filtering的内容
- TextureAtlas支持批量渲染block的portrait

2014.12.11
- Mobile版支持窗口TitleBar高度的属性.
- 针对Mobile版优化了UI方便点击：EditBookPage (加大字体和按钮)
- MCML优化background-color属性, 可直接指定背景颜色.  Mobile版中MovieText文字加大, 背景修复
- 修复中文材质包无法Drag and drop安装的Bug.
- 材质包模块增加刷新按钮: 如果本地目录发生变化可以重新刷新.
- treeview和gridview增加了ScrollToRow方法, 可以滚动到指定的行.
- 材质包模块中的列表框会自动滚动到当前选择中的材质包
- 修复BlockSign上某个方向文字闪烁的Bug due to Z-testing.
- Mobile版修复手中的命令方块无法激活的Bug.
- Mobile版的Tooltip字体加大14到20号字.

2014.12.10
- 修复带有部分透明度的Block模型光照计算有误差的Bug. 例如半砖.
- 整理了推荐列表：增加了其它分类。 例如解密地图。
- TextureAtlas优化: 50%

2014.12.9
- Mobile版修复重新登录后MobileAPI失效的Bug.
- 发布创意剧场：《喜欢你是一次冒险》
- 登录UI背景图优化, 修复ViewMode下视角灵敏度与图标.
- 修复自定义材质包中玻璃板与玻璃的材质无法分辨指定，导致相互引用混乱的Bug.
- TextureAtlas Packer implemented in NPL for dynamic block icon rendering.

2014.12.8
- Mobile版增加震动API
- 击碎物体或飞行落地会触发震动
- Mobile版设置中增加了是否开启手机震动效果的选项
- Mobile版音量可调可保存
- Mobile的slider控件点击区域修复.
- Mobile版登录界面更新支持多语言. 翻译了一批UI文字.
- submit paracraft trademark

2014.12.6-2014.12.7
- Mobile版增加反转Touch鼠标，灵敏度, 最大可视距离等设置
- 设置更改时采用delayed flush, 每3秒会Flush一次.
- 引入最大可视距离的概念，渲染距离超出时会小于这个距离. 取消了对渲染距离命令的范围限制. 导演可调节RenderDist， 但不可调节最大可视距离.
- Siggraph Asia 2014 @shenzhen meeting old friends

2014.12.5
- 新增单个URL请求下载进度的通知回调函数
- 世界下载增加了下载进度的显示: 正在下载: 96/1024KB
- Mobile版Worlds下载按钮增加状态显示.
- 修复自定义材质中流体属性无法继承的Bug
- 修复BlockPieces有时不消失的Bug

2014.12.4
- 修复首次加载光照，极少数方块有一定概率无光照的Bug
- 修复Region Unload后，光照缓存Meta信息没有清除的Bug
- 修复Region超出缓存最大值时， 没有Unload的Bug.
- 修复下载文件时网络故障导致下载失败，恢复网络后，无法再次下载的Bug
- 修复在线世界列表，快速切换不刷新的Bug。
- Mobile版在线世界列表增加了刷新按钮，并修复了功能。

2014.12.3
- Mobile版增加了选择后的工具按钮: 属性，拉伸，删除等.
- Mobile版恢复了选择后的手势， 既可以用手势， 也可以点击UI。
- Mobile版点击向下飞行键， 如果已经接近地面，则自动退出飞行模式.
- Mobile版单击创建增加了100ms延迟, 手指抬起时可以看到物体出现的过程，感觉更加真实。
2014.12.2
- 修复光影模式下CustomModel类的光照问题.
- 修复暂停的音乐， 再次用/music命令播放时， 前面会少0.5-1秒的时间。
- 击碎效果的重力G增加到2G.
- 首次加载时：出生点自动定位到地面而不是空中。
- Fix世界加载时首个同类块无光照和高度信息的Bug。
- 创意剧场：《星座直播间2》

2014.12.1
- Tool工具架构底层开发完成。
- TouchController用新的Tool工具底层重构完成. Tool对象之间松耦合了。
- Mobile版在WIN32下可以用键盘模拟大多数多点触控的效果。 方便调试。
- Andriod版多平台登录（百度云API）底层开发完成（支持百度，QQ， 手机号等）

2014.11.29-2014.11.30
- Paracraft英文版的网站模板完成: http://en.paraengine.com/
- 真人版的Paracraft简介剧本优化，后期剪辑, 并请用户配音.
- 与Disney的《冰雪奇缘》开发团队的特效组程序员交流，了解一些工具相关的制作方式.

2014.11.28
- 建立英文版的wordpress基础网站
- 真人版的产品介绍视频: 剧本和拍摄
- 创意剧场：《创意空间介绍:Mobile》等3部。
- Tool工具架构增加action, actiongroup.

2014.11.26-2014.11.27
- Tool架构底层开发，针对手机版的Touch操作拆分成了几个工具类：画笔， 选择， 拾取，橡皮等工具。
- 对论坛首页的模板做了一些编程开发

2014.11.25
- 命令输入框中: 支持tab快速选择和自动补全
- 论坛新首页: 明确了电影主题,  增加了说明， 管理会更严格.
- Tool工具类底层开发: 引入类似QT的signal/slot机制.

2014.11.24
- 修复: 反复加载世界可能光照线程出现死锁的情况.
- 修复: 实数的地形引擎加载时如果部分文件缺失可能出现Crash的Bug.
- 修复EditBox无法输入TAB的Bug.
- 修复Mobile造成PC版数字小键盘大小写错位的Bug.
- 上述问题发了外网更新包

2014.11.22-2014.11.23
- NPLgettext一个小项目用于从NPL和MCML中自动提取文本做翻译： https://github.com/LiXizhi/NPLgettext
- 建立了Paracraft的Poedit文件：用于中文和英文版的翻译.
- NPL类库支持了mo(binary), po(text)的本地化文件读取和录入.
- 代码支持多语言国际化(10%):登录页, Loading页面, 菜单等
- 新增获取系统默认语言的API
- Mobile版:采用了Native分辨率, 防止UI出现放缩的问题.

2014.11.21
- 输入命令行时支持上下键翻动
- 增加了新的System Message, 支持SlateMode UI的即时切换(such as on MS Surface Pro Tablet)

2014.11.20
- Mobile版修复返回键只有KeyUp没有KeyDown消息的Bug
- Intel的超级本可以自动侦测当前模式无需点击屏幕.
- Mobile版支持大多数键盘虚拟按键的输入.
- 修复带放缩的Text的放缩动画的渲染.  Mobile版中大量使用了这种效果， 例如ESC键。 去掉ANSI版的字体渲染API.
- Mobile版主UI优化：所有图形至少2个像素，Menu从双向展开改为单向展开，适当缩小了大小。 更加美观。
- Mobile版增加了只读模式与编辑模式间的切换。
- 发布创意剧场：《善恶共存》, 创意大赛比赛时间延后至寒假。

2014.11.19
- we are on vacation

2014.11.18
- Mobile版Touch Button加入了点击效果.并配合动作.
- Mobile版:andriod4.4以上版本增加Immersive Mode: 修复Android全屏模式下， 虚拟Nav Bar仍然显示的Bug
- Mobile版:登录界面中增加Mod插件UI, 以及更新按钮.
- studied QT Framework: at source code level.
- Mobile版:重构了键盘事件响应代码， 增加了Andriod中虚拟导航Key. mapped to ESC_KEY
- Andriod版中的返回按钮等同于ESC键， 会激活退出世界的对话框.

2014.11.17
- Mobile版修复UI点击区域与3D操作重合，造成误操作的Bug.
- Mobile版Touch UI 5秒无操作会Auto Hide.
- 重新设计了主UI, 布局更加合理.

2014.11.15-2014.11.16
- studied qt and other tool architecture.

2014.11.14
- PC版增加了可自动隐藏的菜单，具有更好的功能扩展性，1级UI放入了菜单中，默认UI更加简洁干净了。
- 发布创意剧场：《鹅卵石与宝石》

2014.11.13
- MovieCodecPlugin 增加了Symbol File, 修正了CMake文件。 做了HotSpot性能分析.
- 优化部分HeadOnTextAPI性能.
- PC版的工具栏与Mobile版布局统一了. 去掉了血量和体力值的显示。

2014.11.12
- 调整了光照Chunk加载次序的算法，引入新的权重，修复特殊的每帧变化的场景，可能永远不更新或更新太缓慢的Bug.
- Chunk Rebuild排序采用了stable_sort代替sort, 修复加载次序不固定的Bug.
- TouchControl支持注册多种手势类， 并自动取消单指的默认操作.
- 新增TouchGesturePinch手势类: 第三人称下，可以调整摄影机距离.
- Mobile版：新增Ctrl键的AABB选取

2014.11.11
- 手机版的TouchController UI被移植到了Win8中的Intel2in1Pad中。 在Touch和Mouse之间智能切换.
          如果最近的一次点击来自鼠标则隐藏TouchInterface。 如果最近的点击来自Touch设备， 就自动显示出来。
- 重构Win32下touch API接口与Mobile版共用事件.
- Intel合作:京东上的Intel高端超级本有3000个TF卡中预装了ParaCraft.

2014.11.10
- 优化画板，相册，告示牌的渲染：除了文字和图，模型部分都作为ChunkBuffer来渲染.
          极大的提升有大量重复模型的场景FPS。Mobile版FPS从8到60.
- 增加OBJ_CUSTOM_RENDERER属性, 模型可以被标记为不渲染，由外部渲染器渲染.
- 优化了登录UI中的图标. 更加清晰了.
- TreeView控件的TreeNode增加了RenderTemplate

2014.11.9
- Run lighting algorithm full function analysis: function hot spot discovered.
- 根据hotspot性能分析：优化一批数据结构. 例如之前GetBlockIndex占用了30% of total CPU time.
- 统一了所有Block运算的BlockIndex转换函数， 并且全部inline以提升性能.
- Lighting算法线程线程切换粒度调整为之前的1/1000. 增加了线程调度的流畅度.
- 修复皮肤ID显示比实际值大1的Bug
- 发布创意剧场：《侏儒的考验》, 《哈奇Vizta创意空间杂志》
2014.11.8
- 修复无法给非主角换皮肤的Bug
- NPC首次创建取消了自主运动.
- 电影方块中的命令行支持多行输入了， 可以在同一个时间点上执行多个命令.
- ChunkRebuild算法线程线程切换粒度调整为之前的1/1000. 增加了线程调度的流畅度.

2014.11.7
- ChunkRendering: 采用独立线程计算和生成RenderBuffer. 目前整个引擎有3个线程：
          主渲染线程， 光照线程， Chunk线程， 三者之间相互调度，竞争资源达到性能最优。
- Shader优化：在只有点光源的场景中， 物体也会根据法线方向，受光略有不同, 增加了立体感.

2014.11.6
- ChunkRendering: Block的顶点数据生成代码重构，拆分成更多子函数
- 新增ParaMemoryBuffer用于多线程RenderBuffer的构建
- RenderableChunk类支持同步与异步2种模式构建RenderBuffer. 异步模式下工作线程先将数据构建到内存中， 下一帧主线程再上传到显卡. 从而保证主线程的绝对流畅.
- 增加了ChunkVertexBuilderManager异步队列

2014.11.5
- 全部的模型采用ChunkRendering：例如按钮， 压力板， 活塞， 中继器， 门， 铁轨， 动力铁轨等.
- ChunkRendering: 支持不同的Block Data对应不同的材质.
- 修复WireModel overdraw with new chunk rendering algorithm.
- 修复人物皮肤在电影方块中无法用数字ID.
- ChunkRendering: 修复玻璃门双面材质用模型表示
- ChunkRendering: 优化所有Block中用到的模型都成为了正方形面的模型. 节约4倍内存开销.
- ChunkRendering: 修复BlockData 16位Overflow导致Crash的Bug. 改为32位.
- 性能优化: 在同一个Chunk内, 会合并同材质不同Data的Block. 会减少DrawCall以及SetTexture的次数.  CPU开销很小.
2014.11.4
- 增加BlockModelManager：模型类Block加载时加入了Cache, 同类模型只读一次文件.
- 对所有ChunkBuffer中的ParaX模型文件，加载时做了同面的多边形索引优化。 顶点数据内存开销缩小4倍, 多边形数目减少1倍， ChunkBuffer刷新速度也相应提升.
- 修复一批法线不同面的Block模型文件.  三角形转为四边形时，允许误差0.01. 目前100%都是BlockModel了.
- 修复BlockModel AABB点选区域.
- 修复blockmodel texture wrapping in windows version.
- 修复BlockModel中的物理面被错误显示的问题.
- ChunkRendering: 修复压力板等多状态模型的显示

2014.11.3
- 模型类的渲染非常的占用CPU， 基本都移到了ChunkBuffer中渲染。例如楼梯, 玻璃，栅栏，围墙，火把, 等。
- Mobile版静态Block模型很多的场景中FPS从8FPS增加到60FPS.
- 场景中的火把去掉了粒子效果，主要为了提升Mobile版的运行效率.

2014.11.2
- 优化命令 /loadtemplate [-r] [-abspos] [-tp] [-a seconds] [x y z] [templatename]     增加是否为绝对位置， 以及是否转送人物的属性。
- 任务模板增加click_once_deploy属性, 默认为true, 当为true时， 模板LoadingUI显示一键完成， 而不是开始建造.
- 模板可以通过UI选择使用相对或保存时的绝对位置创建.  目前电影方块的内容都是绝对位置的。

2014.11.1
- 世界BlockWorld内存优化, 重构读写算法：内存开销减少60%.  内存中同类数据采用索引方式读取. 极大压缩内存占用.
          读Block性能提升(fewer cache miss), 写性能当一个Chunk区域内的Block种类很多时有所下降.

2014.10.31
- 光照系统内存开销减少8.5%.  光照信息更精简.
- 编辑模式下，使用电影编辑的选择距离加大到正常大小， 方便动画制作.
- 修复并行模式下光照统计信息的输出，加载世界时默认计算3秒的光照.

2014.10.30
- 光照传递系统大量重写. 速度提升，代码更清晰.
- 扩充命令: /sound name [filename] [from_time:0] [volume:0-1] [pitch:0-2]
          /sound 1.mp3 10.1                              play 1.mp3 from 10.1 seconds

2014.10.29
- 光照系统重构:  重写了核心的光照算法，更加简洁和迅速，新算法修复单光源计算可能运算量非常大的Bug.
- 修复Spiral lighting queue sequence bug.

2014.10.28
- 优化性能: optimize GetBlockTemplate performance, fix a small memory leak.
- 关照计算与主线程RenderBuffer更新按照当前视点螺旋方式由近到远刷新， 主线程限制了每帧RenderBuffer的刷新率。刷新分为首次与光源更新2种，有不同的权重，在人物正常运动速度下刚好可以跟上摄影机。
- 光照线程粒度变为了之前的1/100.  保证主渲染线程有写请求时其他Reader第一时间释放锁，并消息通知主线程， 同样当主线程释放锁时，立即通过事件唤醒所有reader(光照线程)。 ReadWriteLock类通过锁与消息事件， 达到最小的锁次数和最大程度的异步。 光照线程CPU利用率高达90%(几乎等同写锁占主线程的比例)。多核处理器上，满负荷的光照线程对主线程FPS的影响小于1% (可以忽略不计).
- 取消了NPL脚本Framemove之外的所有的blockworld锁。 主线程大部分时间工作在无锁状态下。 光照更新也工作在无锁状态， 依靠Int32本身的原子性， 光照模块仅对数据结构会改变的少数函数加了异步锁。 IO线程数据首次初始化时，通过Region文件的全局Lock状态，保证其他线程（主线程和光照线程）直接跳过Chunk的处理， 而不是申请锁，造成contention。

2014.10.27
- 增加了ReadWriteLock类和实现。 用于Block运算中的多线程同步的专用Lock. 写优先的Lock.
- 关照线程锁机制重构：光照计算与主进程改为condition_variable的通知模式
- 修复:背景音乐应该从第一帧出现的位置开始播放.

2014.10.26
- 世界IO加载默认为异步, 世界首次加载时禁止世界渲染，更多CPU给加载线程。
- 重新思考光照渲染线程与主线程的同步机制, 保证Mobile版可流畅运行.

2014.10.25
- Mobile version has 4 Region Cache instead of 16 on PC. 降低Mobile版的内存开销.
- Block世界加载IO部分大量重构: 支持同步，异步2种可随时切换的模式.  提升了加载速度和渲染过程中的流畅度.
- 世界首次加载能够显示正在加载的Chunk个数. 同时防止一些手机加载大型世界时由于画面不响应，进入休眠模式.
- Mobile版暂时禁用了随机地形生产。 没有LuaJit, 目前的算法在Mobile上太慢了。

2014.10.24
- 修复EntityImage的算法， 解决在特殊情况下出现递归的Bug.
- Mobile版：推荐列表新增Tag分类。 对作品更好的分类.  不是所有世界都在手机上推荐运行的。

2014.10.23
- Mobile版：拖拽控件pe:sliderbar支持touch input. 兼容鼠标和touch操作.
- Mobile版：pe:slot支持用touch的方式拖动物品，比如移动背包中的物品，或扔到场景中等.
- GUI触屏底层逻辑修正：当控件有ontouch事件时将忽略自动生成mouse事件
- 修复Android下GUI zordering sort not stable. using std::stable_sort instead.
- 修复设置UI在手机上显示不全的Bug。
- Mobile版：编辑物品时(比如背包等), TouchController UI会自动隐藏
- Mobile版修正了一些常用的专属UI(放大版): 例如箱子, Tips, 文字面板, 命令编辑窗等 方便在手机上操作.
- 多行文本新增fontsize, lineheight属性. Mobile版的文字输入面板使用大号字体.
- 世界模板功能优化：支持相对位置与绝对位置
- Mobile版：修复Icon路径大小写导致不显示的问题。 所有Icon可正确显示了.

2014.10.22
- 新增命令参数: /sky -sun sun_size sun_glow  调节太阳大小和光晕的大小：例如
/sky -sun 500 12
- 新增命令参数: /sky -cloud density[0-1] 调节云的密度
               /sky -cloud 0.1
- 优化了命令提示的显示.
- 修复Android版中天空盒子显示错误问题.
- Mobile版: 增加了加载UI以及小提示, 并修复会弹出聊天框的Bug.
- 关照渲染线程可以通过参数调节每帧计算多少光照。
- 当加载世界时会将更多CPU分配给光照进程。 极大的提升了光照加载速度和进入世界后的流畅度。
- 加载世界时会显示当前光照计算信息, 进入世界时光照应该是基本加载完毕状态.
- Mobile版：加大了BBS Tip的字号.
- Launcher登录页面更新链接：将最新的活动与咨询链接放上了
- 加载世界加入ReserveBlocks减少Loading时内存分配次数. 解决部分世界在某些内存小的手机上不可加载的Bug.

2014.10.21
- Mobile版：仿真天空可以正常渲染了.
- 仿真天空增加了云的密度， 太阳的大小等参数: 默认情况下太阳大了一些， 云疏了一些.
- 官网发布了最新的ParaCraft登陆器, 修复之前登陆器无法启动的Bug. 支持更新与运行分开.
- 提交了Intel超级本的创作大赛作品.

2014.10.20
- Mobile版：当天空文件不存在时， 使用默认的天空文件。
- Mobile版：静态模型类天空可以正确渲染了.
- Mobile版：设计百度云Mod
- iOS版: buildboost_ios.sh脚本, 自动编译所有boost类库.

2014.10.19
- Mobile版: 新增渲染Shader: Sky和SkyDome
- iOS版: learned XCode systematically.

2014.10.18
- Mobile版: 修复Text Layout offset Y error when rendering smaller scaled font with vertical center alignment.
- Mobile版: android上修复无法使用stencil buffer的问题.
- Mobile版：fix render IO/sim tick's time delta causing biped to flicker.
- iOS版: learned MacOS systematically.

2014.10.17
- 修复新版本在某些ATI显卡中不正常渲染的Bug
- Mobile版 GUI增加了Stencil渲染， 可以正确渲染剪裁区域了Clipping Container without faster render.

2014.10.16
- 优化命令:/generatesrc [-private] [src_file_list] [dest_folder]  支持private和路径参数. 自动生成源码
          private参数表示强制移除函数实现
- 修复music对象和在movie sequence block 中错位的Bug
- 修复演员角色88，100号人物动作.
- Mobile版: 新增ParaXRefSection的解析和渲染。修复比如火把中的火苗的渲染.
- Mobile版: 物品分类电影类合并到工具类中， 手机版也可以创建电影方块等.
- Mobile版: 修复2D UI中RGB<-->BGR通道错误的Bug; 同步了一批编辑时用到的材质到发行目录.
- Mobile版: 增加人物的点选手势。点击对应鼠标左键， 长按对应鼠标右键。 矿车因此可以乘坐了。
- 摄影机双击W,将以10倍的速度运动. 方便录制过程中快速走位
- Mobile版: 人物类模型增加opacity属性,可以控制人物淡入淡出.
- 新增动态变量opacity透明度：电影人物支持编辑淡入淡出. 透明度为0，人物可以彻底消失。
- 新增API. ParaScene.CheckExists() 针对Entity优化了ParaScene.GetObject()的调用，降低内存开销，提升速度.

2014.10.15
- 修复子电影方块中人物重叠的Bug
- 重构Mobile平台下DeleteFile(s)方法, 支持文件wildcard的删除. 如清空Cache目录.
- Mobile版切换世界停掉BGM声音
- Mobile版修复部分国外的手机(如KindleFire)中文名的世界无法打开的问题
- 修复音效有时会不播放：3秒的特效长度不准确. 改为了1秒. 所有特效不会unload
- 更改了音效文件GC回收机制：先播放，先回收，从不强制回收直到超过10个.
- PC版修复声音引擎seek底层bug: 可以精确的定位声音文件到指定的播放位置
- Mobile版：创作百科与模板功能设计案 (融入了电影功能的创作百科)
- 增加ActorMusic: 可以在时间轴上编辑音轨, 拖动时间轴音轨也自动定位到指定的位置, 方便后期配音.

2014.10.14
- Mobile版简单的声音引擎实现：支持直接从zip, sdcard或安装包中播放音频.
     - 世界zip文件包中的文件， 会被先解压到sdcard中播放.
     -  iOS不支持ogg, ogg自动被替换为wav.  MP3, wav是默认支持的格式.Andriod下支持ogg.
     - 每次启动自动清空AudioCache目录下的所有文件
     - 由于API不支持Query长度，默认非循环的音效长度为3秒钟
- Mobile版的下载列表增加文件大小显示
- 跨桌面平台(Win32, MacOS)的登陆与更新器Launcher基本完成. 用了QT C++. 解决旧版登陆器不稳定的Bug.
- 发布创意剧场：《过眼云烟》.
2014.10.13
- 电影制作: 引入子电影方块时间轴的概念. 可以在一个电影方块的时间轴上编辑众多子电影方块.
     - 摄影机和字幕等自动引用子电影方块，这个对后期配音，剪辑有极大的帮助.
     - 选中场景中的电影方块，并按添加Key可自动添加选中的电影方块到父方块的关键帧中
     - 当子方块没有摄影机时，父方块的摄影机则生效。 字幕和演员等所有其他Actor是同时生效的。
     - 选择父方块中的命令序列Actor， 或播放父方块都会激活子方块中的摄影机（如果有的化）
     - 播放或编辑过程中，场景中会自动高亮当前时间轴上的电影方块.
- 右键重复点击关键帧或时间轴，会弹出ContextMenu, 可以精确编辑关键帧， 例如设置时间等多项精确操作.
- 发布创意剧场：《悲伤的巴塞罗那》中篇科幻电影.

2014.10.12
- Mobile版：removed unnecessary shader switch when rendering multiple text together.
- Mobile版：fix NPL runtime tick calling twice in app delegate.
- Mobile版：长按+点击物品栏：等于Alt拾取; 物品栏可以点击空白位置; 点击上划可以扔掉Slot中的物品;
- Mobile版：Undo/Redo共用同一个按钮。 Redo手势为向右侧滑动
- Mobile版：左侧增加shift按钮Touch模拟键盘上的Shift.
- Mobile版：修复StaticMesh被选择时，Model Transform错乱的Bug
- Mobile版：opengl effect system now uses parameter cache and only commit to device when CommitChange is called.
- Mobile版：Shader param: AlphaTesting enabled for all static and animated mesh.
- 新增角色的关键帧精确编辑UI: 转身, 头部上下, 头部左右
- 发布创意剧场：《妻子的记忆》首部中篇电影.

2014.10.11
- Mobile版：再次修复Home键，材质缺失的Bug.
- Mobile版：修复一些贴图或模型不存在的Bug.
- Mobile版：修复自定义皮肤和部分人物模型材质显示不出的Bug.
- Mobile版：texture sampler states automatically changed according to global settings.
- Mobile版：修复模型类的选择特效无效的Bug.
- Mobile版：修复3D场景中多行的文本渲染错误的Bug.
- 修复画板自动展开功能异步加载错误.

2014.10.10
- Mobile版：修复阴影文字渲染错位的Bug.
- Mobile版：修复VertextArray中Color为BGRA(Opengl)和RGBA(DirectX)不一致的问题
- Mobile版：修复EditBox输入文字后onchange Event不发送的Bug.
- Mobile版：fix ParaX file parsing crash on special files with empty object name.
- Mobile版：可以加载外部zip包中的材质资源了
- 修复自定义材质包加载的Bug
- Mobile版在观影模式下会隐藏操作UI

2014.10.9
- Mobile版：增加右键编辑手势：长按选择单个物体后，再次点击。
- Mobile版：增加GUI渲染专用Shader
- Mobile版：增加3D场景中的立体文字渲染

2014.10.7-2014.10.8
- Mobile版：ParaX动态模型解析与渲染
- Mobile版：XFile文件解析底层：大量内容.
- Mobile版：OpenGL的DynamicVertexBuffer的重构与实现.
- Mobile版：加入粒子渲染
- 修复了ParaX文件解析在Android真机上Crash的Bug. 可以在Android上渲染动态模型了

2014.10.5-2014.10.6
- Mobile版的ParaXStaticModel静态模型文件的解析
- Mobile版的渲染Shader和静态模型的渲染

2014.10.4
- 重构: ContentLoaders 异步加载资源
- 同步model, character资源目录
- Mobile版ParaX模型接口API(dummy functions): Biped, MeshObject, ParaXStaticModel, MeshEntity, etc.

2014.10.3
- 重构: refactored asset_ptr into RefCounted, RefCountedOne, and ref_ptr.
- 新增XFile相关类代替dxfile的文件解析.

2014.9.30
- 发布创意剧场：《各路人生》
- Mobile版：TouchController支持多点触控, 选择手势，批量删除手势， Extrude手势， 批量创建手势等
- Android平台发布ParaCraft技术测试APK安装包: 非方块渲染还没有加入, 电影还不能播放.

2014.9.29
- Mobile版: 加速了开机速度.
- C++底层也加入了Touch Session.
- Mobile版: GUI控件的鼠标滚轮事件可以用单指的拖动来模拟了.
- Mobile版: 第一人称视角下支持Touch操作和第三人称视角一致.

2014.9.28
- FileAPI优化：文件检测精确返回文件所在位置：如磁盘， ZIP， Search Path.
- Mobile版：提升NPL文件加载速度，避免加载时大量file not found warning.
- Mobile版登录页加入开启Jit的按钮（大部分Android手机是OK的）, NPL执行速度提升30-60倍 (尤其是地图生成算法).

2014.9.27
- 修复部分手机Release版Crash的Bug
- MinGW cross compiled LuaJit for android:  version 2.0.3 (Git Head as of the date)
- 由于LuaJit在部分主流Android手机中仍然会Crash, 只好全平台禁止了jit.

2014.9.26
- Mobile版所有包含opengl资源的对象增加RendererRecreated:包括shader, vertex buffer,  texture, pool, etc.
- 修复部分Android手机按Home键切出后，再切换回来无法渲染的Bug.
- Mobile版在线作品可以正常查看了， 部分手机可能无法下载.

2014.9.25
- Mobile版增加方块高亮与选择特效渲染， 修复Attribute Index Bug.
- Mobile版Icon设计并更新,Android下产品名字改为ParaCraft
- Mobile版用手势可以类似画画一样，一次创建一条或取消
- Mobile版修复AsyncLoader无法下载的Bug, 修复ZipArchive无法加载的Bug，
- Mobile版修复Release版光照计算死机的Bug.
- Mobile版增加14，20号2种字号，自动适配到合适的字号.

2014.9.24
- Mobile输入法: GUIEditbox，GUIIMEEditBox 实现了手机操作系统的默认系统输入法.
- 重构IME系统, EditBox支持超大字号, MCML中的input text也支持font-size属性.
- Mobile版增加：命令行输入以及世界起名字
- GUIEdit， 以及MCML的input text都加入了EmptyText属性, 用于显示无内容时的文字
- Mobile版增加了画单像素Non-AA线的功能: Debug模式下可以显示包围盒信息了，或用指令/show boundingbox
- Mobile版增加动态贴图渲染TextureSequence: 可以渲染水了.

2014.9.23
- Mobile平台的Win32 Release版配置+编译
- Mobile版修复飞行模式的默认速度并可以用Touch和代码控制飞行以及升降.
- Mobile版人物走动， 飞行，跳跃， Camera方向等功能联通.
- 飞行按钮按住上移等于tab, 下移等于shift-tab
- Mobile版新增画AA线的shader, 可渲染Block的选择效果
- Mobile版主UI联通: Menu, Toolbar, inventory, settings, save world, etc.

2014.9.22
- NPL支持bin/*.o 以及*.luac 两种读取Bytecode的方法. 后者是为了和其他程序的插件兼容.
- 常规GUI控件如按钮， 只在单点触控下生效。 多点触控必须通过ontouch事件实现。
- Mobile版禁用了文件侦听API,会导致exception.
- 修复多点触控的Bug,修复字体长度Bug, 修复duplicated Vertex Buffers release exception.
- Taurus中加入了mobile版的PKG自动生成配置和模块.  Android Release版可以编译了.
- replaced standard assert function with our own version which can print error to log file in android.
- 用adb logcat>log.txt 可以查看详细真机日志：修复Mobile版由于实数地板渲染导致闪退的Bug.

2014.9.21
- Mobile版支持File Searching in writable directory (the sdcard is preferred)
- 连通Mobile版的新建以及加载世界UI. 支持sdcard上的文件遍历.
- 修复tinyxml2使之支持attribute without quotation marks. 与tinyxml1兼容.
- world attribute database enabled for mobile version.
- Dummy人物也包含了移动速度.

2014.9.20
- Mobile版支持任意大字号, C++层渲染时将自动放缩，内部只用固定字号的texture atlas. 目前是14号字.
- Mobile版字体去掉了anti-aliasing. 通用贴图也加入了blocks_前缀，去掉anti-aliasing.
- Mobile版采用Android默认字体的中文版:DroidSansFallback.ttf
- Mobile版会自动适应设备的分辨率
- 修复tinyxml2使之可以支持mcml的<%=string%>标记. 并加入了错误Log输出.
- generated keystore file for android apk in release mode.
- 连通Mobile版的登录UI

2014.9.19
- ParaEngine底层模块化重构100%:  各项功能基本稳定的Android/Win32通用底层代码.
- 重构Event相关的类文件 ，重构TouchEvent触屏接口, win8/android等的touchevent统一接口.
- 底层加入了TouchSession类：追踪同ID的对象， 并设置了超时机制. 支持多点同时.
- 所有GUI对象和脚本层都支持ontouch事件. touchdown后追踪所有同ID的消息， 直到Timeout或touchup.
- mcml同样支持ontouch: input button, div, pe:container都支持ontouch事件.
- ParaCraft 首个内部Android apk技术预览版.  可读取任意世界.

2014.9.18
- 重写了RenderableChunk： 新的Block Rendering算法不再使用Vertex Offset， 只使用Index offset。 在Opengl ES 2.0下可以运行. 引入Static Vertex Buffer Pool. 每个Renderable Chunk可以有多个VBO. 每个VBO的最大大小为9000个面. 每个Renderable Batch的最大大小从480增加到最大9000. 渲染性能整体是略有提高的.  Draw Call的数量在大多数情况下会下降。 VBO数量略微增加.
- OpenGL ES2.0 Fix: glDrawElementsBaseVertex not supported in opengl es. Now default to glDrawElements.
- 新增人物：火特效   (所有官方可用人物可通过XML配置了: config\Aries\creator\PlayerAssetFile.xml)
- Opengl渲染器增加了Debug输出, 所有重要的Render API如果出错在Debug模式下会报错. 方便真机调试.
- GLSL编译时的错误消息包括编译和连接错误都会输出到Log中方便在真机环境下调试.

2014.9.17
- Mobile平台的BlockEngine渲染Shader 100%
- Mobile平台文件写操作自动寻找可写位置auto find writable path which is transparent to the user.
- 修复当多个电影方块同步播放时， 字幕和背景冲突的Bug.
- 优化了命令帮助提示:commandworlds

2014.9.16
- 新增命令: /show touch  显示触屏UI (用于调试Android上的操作)
- 修复opengl perspective projection matrix which differs from directX以及相关frustum算法.
- biped simulation ported to mobile platform
- 增加了Mobile的触屏主UI以及部分功能.
- ParaEngine底层模块化重构99%:  Render Device (100%)
- OpenGL renderer: 增加了depth buffer, z write, z testing, face culling等功能. Shader增加了attribute vertex location.

2014.9.15
- 修复迁移导致DB无法生成的Bug
- fix process hanging bug when exit program in mobile version.
- ParaEngine底层模块化重构98%:  Effect System(100%)

2014.9.14
- ParaEngine底层模块化重构97%:  Vertex Declaration(100%), Effect System(90%)
- 将DirectX HLSL中所有的effect parameter 映射到了Opengl GLSL中的Uniform中. 统一了DirectX中的matrix, texture, parameter handles.
- effect_file_openGL可以管理GLSL程序.

2014.9.13
- Mobile版ParaEngine拆分为3个Lib以加快编译速度， 避免command line too long during android build.
- ParaEngine底层模块化重构96%:  Effect System(80%), Vertex Declaration(50%)
- 将所有的渲染部分代码移动到Renderer目录中。 分为OpenGL和DirectX两个渲染器。
- 用OpenGL实现了DirectX API中的d3dx effect system, vertex declaration system, vertex buffer, index buffer接口.
- 发布创意微电影：战.前夜

2014.9.12
- ParaEngine底层模块化重构95%:  Effect System(70%), Render Device (70%)
- Mobile refactor: 修复全局透明材质不显示的Bug.

2014.9.11
- ParaEngine底层模块化重构95%:  Effect System(50%), Render Device (50%)
- 修复外网DB中的角色不显示的Bug.
- 增加了人物换皮肤的UI
- Mobile版UI制作(60%)
2014.9.10
- 修复rain effect中雨点太大的Bug. 修复雨和雪的模型光照Bug.
- 外网Win32上发布Mobile整合版的DLL.
- 修复当SpeedScale不是1时， 人物录制出现滑步的Bug.
- 发布创意微电影：古剑奇谭大结局

2014.9.9
- 取消entity object的感知属性, 提升性能: 修复出生点等物品不显示的Bug.
- F3 中player位置为当前操作的人物， 例如可以为演员或主角.
- 删掉了几个与MC太接近的模型
- 优化scene & tile visitor logics, improved performance of visiting biped and cleaned up the code.
- Mobile平台联通luajit2.ffi, 使得关键脚本调用C++API具有C的性能.

2014.9.8
- 电影人物和摄影机都可以在最后一个关键帧之后随意向后拖动时间轴继续录制.
- 新增指令: /show boundingbox 和/hide boundingbox 显示所有物体的包围盒。
- 新增指令: /show perf  显示性能统计performance view
- 优化命令帮助提示: 当代码和XML配置中不一样时， 显示所有的内容。 并且首次访问时只加载一次。
- 修复飞行模式下录制人物动作时运动速度每帧指数递增的Bug.
- 修复/renderdist 上限。 目前是一个变量了， 原则上可以任意大场景， 但是还是设置了上限。
- 增加EntityPool: 优化/rain   /snow 的性能10倍. 还有优化空间.

2014.9.7
- 首次创建电影角色时会自动弹出PropertyPage给用户一个初始化形象的机会， 并且会自动保存静态形象到第一帧。
- 添加电影人物的默认角色为actor(演员)
- 修复重构中3D Ray Picking Math Bug
- shift+点击扮演按钮可以清空所有人物动作.
- 右键点击关键帧Icon： 锁定/解锁所有电影人物。 在录制后期， 可以锁定人物，防止误操作或做精细化动作调整.
- 修复首个摄影机关键帧锁定模式下不生效的Bug.
- 增加演员角色：camera
- 修复演员86号动作： 新增一批演员动作：跪着，抬手，捂脸，闭眼，说话，躺着等。
- 修复飞行模式下进入电影编辑模式，演员头部方向不受控, 以及演员和摄影机动画速度变快的Bug.
- ParaEngine底层模块化重构91%:  audio engine(100%)

2014.9.6
- 修复camera worldup接近90度时会震动的Bug.
- 体验了精细化电影拍摄中的各种问题，近期内会优化
- ParaEngine Render Pipeline refactored for Mobile.

2014.9.5
- 修复由于d3dx9_43.dll不兼容导致 部分新电脑上无法运行程序的Bug. 目前强制安装
- 修复Android的Win32编译环境由于文件太多导致无法连接的Bug. Exceed 32KB link command line limit.
- 修复迁移过程中的2个UI显示Bug.
- 修复电影方块中静止的人物无法播放动作的Bug
- 全部ParaEngine底层模块可以运行在Android上了(With Null Renderer).

2014.9.4
- ParaCraft Mobile版 核心交互UI设计草案初稿.
- 修复指令: /fov angle speed, 当Speed大于100或负数时为瞬间改变.
- ParaEngine底层模块化重构90%:  block engine(100%) , scene(100%), AI(100%), biped objects (100%), physics(100%)
- 命令行输入加入了IntelliSense功能 (文档部分待完善)
- 加入了几个新的角色：云， 星光， 花瓣雨，发光特效

2014.9.3
- 修复电影方块角色满时，无法加对白的Bug.
- ParaEngine底层模块化重构85%:  base objects(100%) , global terrain(100%), viewmanager(100%), ParaXModel(100%)
- 官方论坛皮肤改版升级:www.paracraft.cn 加入了门户页

2014.9.2
- ParaCraft Mobile正式立项:建立相关开发目录. Aim alpha 1 in 21 days.
- 增加新方块: 镜面方块 (只有在shader开启模式下，才能看到效果， 测试专用，以及少数电影特效中可用)。通过替换材质来改默认颜色。
- 给出单个电影镜头超过100个角色的解决方案.

2014.9.1
- 修复android下mutex不是recursive mutex, 造成死锁的Bug
- 修复Android下无法创建目录的Bug. changed the file path conventions in linux.
- Mobile在下面三种方式都可以启动了：commonlib(light), IDE(basic UI and MCML), ParaworldCore(full-fledged app)
- 针对Mobile系统，GUI加入了基本的TouchEvent, 2D界面支持多点触控了
- ParaEngine底层模块化重构80%:  2DEngine(100%)

2014.8.31
- dropped ICDB support in ParaEngine
- log和可写文件在Android下全部默认存放到SDCard中, 如果SDCard不存在，则用默认的cache folder。
- studied various android emulator
- ParaEngine底层模块化重构75%: Writable File系统(100%)

2014.8.30
- ParaEngine底层模块化重构72%: Database系统(100%)  , XML related(100%)
- 针对Mobile平台的文件权限， 调整了本地数据库Sqlite的读写位置。
- 修复Mobile平台下的XML文件解析API
- Mobile平台全面支持MCML

2014.8.29
- ParaCraft增加一键开服设置，管理员可以通过UI添加用户。
- 增加跨平台的UTF8到UTF16的转换。
- GUI系统所有wchar_t的接口和实现都改为了u16string(char16_t).  兼容Android上unicode的处理.
- ParaEngine底层模块化重构70%: 2d rendering API (100%) , PKG系统(100%)
- 调整PKG系统，可以从Android等平台的APK安装包中加载到PKG.
- 移动平台中：调整NPL的文件加载. 默认加载main.pkg，并且会找precompiled *.o 文件.
- 修复更改RenderDist后的人物出现距离算法的Bug。 目前是精确按照AABB有10个像素高则不显示计算的。也就是说屏幕分辨率增高，默认的可视距离也会增加。
- 修复计算字体尺寸的Bug， 修复迁移过程中一些数学函数的错误.
- 创意剧场发布： 活动结束贴+1部作品
- 研究了django WebServer, 可以考虑用NPL写一个类似的。

2014.8.28
- GUI系统在Android上测试通过.  迁移了NPL的commonlib库.
- SpriteFont的OpengGL实现(100%)：加入了TTF字体的渲染. 包括各种字体的对齐方式，以及与整个GUI渲染共享同一个SpriteRenderer对象，增加渲染速度。
- 新增人物动作：85屈膝坐下   86 坐着抬手  87坐着捂脸 88  睁眼躺着 100 闭眼躺着

2014.8.27
- ParaEngine底层模块化重构65%: 2d rendering API (80%)
- 重构2dengine的所有Rendering接口. 渲染相关API独立到SpriteRenderer类中了.
- SpriteRenderer 包含了DirectX和OpenGL2个class implementation. 主要用于渲染GUI相关的2D图片.
- SpriteRenderer 的OpengGL实现(100%): 所有非文字类GUI都可以在Android上正确渲染了
- SpriteFont 的OpengGL实现(10%)
- 增加了发光特效的电子演员，可以用来拍摄一些魔法效果。
- 增加了83号人物动作: 捂脸

2014.8.26
- ParaEngine底层模块化重构60%: GUI Object System(100%)
- ParaScriptingBindings目录与Mobile全部同步
- ParaScripting UI相关的所有API全部迁移到Mobile平台.
- ParaEngineApp在Mobile项目上联通: GUI Root对象在Mobile平台启用.
- 加入了script/mobile/test/testGUI等测试用例文件, 并在Android上测试了GUI相关的API.
- 添加了script/ide/commonlib.lua文件. Mobile版和Win32版的内容完全一致了: 包括Log机制.

2014.8.25
- ParaEngine底层模块化重构50%: Asset资源管理(70%), GUI Object System(60%)
- SpriteFontEntity字体模块差分为DX, OpenGL 2个独立文件
- 重构ParaWorldAsset:目前支持font, texture 2种资源管理。
- 重构2dengine, GUI系统：无渲染，无IO版 100%

2014.8.23-2014.8.24
- ParaEngine底层模块化重构45%: Core classes(100%), Asset资源管理(50%)
- 材质管理分为TextureEntityDirectX 和TextureEntityOpenGL两个类. 重构AssetManager, 引入Implementation class的概念.
- 修复模型放缩等几个重构过程中引入的Bug.
- C++加入了PlatformConfig可以支持多平台.

2014.8.22
- 修复下雨后，无法切换回仿真天空的Bug.
- 修复反复编辑电影方块首个关键帧时间可能不是0的Bug.
- 材质包加入了中央HTTP WIKI服务器, 方便用户下载, 上传和使用材质包. 避免出现材质加载失败的问题. 尚需优化逻辑.
- 创作百科界面调整. 支持编辑模板， 编辑描述， 多目录（和材质包类似）。 方便发布免费模板。
          增加了一键完成的功能. 不需要一定完成前面的步骤.
          每个模板支持XML，用户可直接编辑. 并打包分享自己的模板或教程。
- 修复迁移全局模板时的Bug. 修复材质包非强制下载.
- ParaEngine底层模块化重构40%:  骨骼动画模块(100%)
- 重构ParaX模型类库:将所有骨骼动画的数学运算统一为Row-Major, 并改用新的跨平台数学类库, 删除不用的本地数学库文件。
- 修复所有重构带来的Bug: 引擎可以用新版类库正常运行了.

2014.8.21
- ParaEngine底层模块化重构35%:  所有Vector, Matrix, 3D算法跨平台.近万行重构。
- 新Math库重写了所有之前用到的D3DX Math的方法。
- 引擎底层全部Math调用使用了新的Math库. 除了纯3D API, 其他部分已经全部使用跨平台代码。
- 新增Files.FindFile(), 对文件搜索进行了缓存。
- 修复了电影文件引用本地材质发布后材质无法找到的Bug.
- 2014创意大赛评选活动给20多位用户寄出实物奖励，证书，衣服和感谢信. 公司内拍摄了活动照.

2014.8.20
- ParaEngine底层模块化重构25%:  util目录跨平台同步. Math, util在Android编译通过.
- FreeFileSync: Win32和Mobile版同步目录:util(100%), math(100%)

2014.8.18-2014.8.19
- ParaEngine底层模块化重构20%:  重写Math类库。 写了一个最大化兼容DirectXMath的跨平台Math类库.将之前类库中Matrix Column Major全部统一为为Row Major。  将引擎大量代码从d3dx的Math迁移到新类库。
- 新增数学类库:ParaMathUtility，补充了很多常用MathAPI. 未来会支持SIMD, SSE2(已经预留了接口). 主要为Matrix4, Vector3, LinearColor, Transform, Quaternion等常用Math方法。 更多面向对象的封装， 编译器自动检测DirectX，并Cast到各种对象。
- 引擎重构: Drop dependency on D3dxcolor, d3dcolor, macros: use the new ParaEngine::LinearColor and ParaEngine::Color class.
- GUI系统全部采用新的数学类库。 优化了每个UI的底层2D Transform性能.
- 创意大赛评比结果出台： 打印了证书等

2014.8.16-2014.8.17
- ParaEngine底层模块化重构10%:  初始版本可运行在Andriod上了.
- IO 系统重构：支持win32, boost, coco 3套跨平台接口.
- boost等用CYWWin重新编译for Android. 加入external/boost github项目
- 优化工具链:可以快速同步编译到android系统上,生成APK安装文件.
- Win32和Android底层模块公用：IO(100%), network(100%), NPL scripting&threading(100%), Binding(100%),timer(100%),curl(100%),paradebug(100%), dir_monitor(100%), ic(100%), database(100%), zip archive(100%).
- 研究了一下iOS平台的xCode编译.

2014.8.15
- ParaEngine底层模块化重构7%: NPL模块与Andriod全部同步了

2014.8.14
- ParaEngine底层模块化重构5%: 超过1000个CoreEngine文件重新安排了目录结构. CMakeList全部用*.*代替显示文件；删掉了一批不用的引擎文件. Pretty Clean Source Code Now.
- ParaCraftMobile的Andriod编译环境优化

2014.8.13
- 修复水面反射投影不对的Bug. 增加了Wave动画.
- ParaEngine Android系统编译+联调.
- Win32下Client/Server/DLL增加了/LARGEADDRESSAWARE   32位系统上可以使用最多3GB内存. 64位系统上可以使用4GB. 解决部分较大世界访问时内存不够导致Crash的问题. 之前内存到达1.6GB左右会Crash. 目前增加到了4GB.

2014.8.12
- 增加立体模式下左右眼视角的Viewport Layout管理:
- viewport is supported in GUI.
- 新增命令:/stereo [on|off] [eye_dist]开启关闭3D立体输出模式 (左右眼输出).
/stereo on 0.1               with 0.1 eye distance
/stereo 0.03               with 0.03 eye distance
/stereo off                    turn 3d off
/stereo                         toggle
- 系统设置中加入了立体输出的设置UI
- 修复3D立体输出下的影子渲染
- 底层重构AssetEntity类
- /hide desktop模式下不显示指针和选择区域.
- 导出了几个玩家的3D立体电影:shine your way 等.

2014.8.11
- 增加Viewport的脚本接口
- 特效系统支持Viewport： Deferred Shader and Post processing support viewport.
- 新增命令:/viewport [@id] [alignment:_lt|_fi|_rt] [left] [top] [width] [height] 改变视图布局,e.g.
/viewport 0 0 100 0
/viewport _lt 0 0 600 400
/viewport @0 _lt 0 0 600 400
/viewport

2014.8.9- 2014.8.10
- 增加了3DViewport类和实现, 并重构MousePicking接口.
- 重构部分底层引擎App部分的StartAPP流程以及Render流程.
- 增加了BatchedElementDraw类. 逐渐替换调部分DirectX接口.
- 增加了ThickLine的渲染类.
- 研究了DxMath类， 为多平台迁移准备.

2014.8.8
- 修复摄影机没有位移， 只变方向时关键帧不显示的问题。
- 修复/ccs指令在哈奇版中尺寸不对的Bug
- 修复NPC换装后电影录制没有动作的Bug
- 修复SetCharacterSlot会Crash的Bug(屏蔽了代码， 但没有全解决)

2014.8.7
- 更新命令: /startserver 的默认IP为0.0.0.0   这样会侦听本机的所有IP的端口(包括局域网的IP)而不仅仅是127.0.0.1
- 可编程的人物换装系统完成: 人物，动物等各种模型都可以做成能换装的了。 和哈奇的换装一样， 但全部程序控制无需生成DB文件。
- 新增命令: /ccs [-geoset|g|model|m] [@playername] [integer or hair|shirt|pant|boot|hand|wing|eye] [id]    人物换装命令，例子:
/ccs                        当前人物切换到可换装模式
/ccs filename           使用指定的人物模型:可以为当前世界目录下的文件
/ccs shirt 2              切换到上衣2号
/ccs hair 1               切换到头发1号
/ccs hair 0               隐藏头发

2014.8.6
- ParaEngineServer命令行支持不带quotation mark的参数.
- ParaEngineServer也可以运行AllInOne Server了
- 物品系统的WebServer修复Encoding, GetHashCode(在Win32,linux不一致的Bug)
- 84物品系统也从Linux迁移到到Win32下， 可以在Win32下调试运行了.  包括MemCached也提供了Win32的版本
- XSP2 WebServer的Win32运行环境和Code也放到./WebAPI下面了

2014.8.5
- there is a bug in mono's GC under win32, we can only have one embedded C++ thread
- 在Win32下DBServer目前只有单个线程会调用Mono,否则会报错。
- 修天空切换后颜色不对的Bug
- 修复Midi在没有使用时被初始化

2014.8.4
- 修复人物属性编辑器无法关闭的Bug
- 修复TmInterface 在win32下buffer overflow
- Win32下: All-In-One Server完成, 修改登陆接口, 当内网时无视密码. 无需Internet链接就可以测试了.
- 修复WebAPI的一些Bug.
2014.8.2
- 从mono源代码直接编译了GitHub上最新的版本Mono 3.4.0.  多线程的GC可以在Win32上正常运行了。
- DBServer, NPLRouter,TMInterface, IMServer从Linux迁移到了Win32，并写了AllInOne脚本可以本机运行了.

2014.8.1
- Mono 3.2.4有Bug, 目前使用了latest stable 2.10.9.  DBServer可以运行了
- NPLMono2支持WinForm了，例子在ParaCraftSDK/sample/MonoSample.net中
- NPLMono2在linux下编译通过
- NPLRouter在win32下使用了新的NPLMono2接口(可以被Client/Server共享使用了). Linux下还是旧接口.
- TMInterface使用新接口在linux/win32下编译通过.

2014.7.31
- DBServer的Win32版测试环境搭建好. 全部用.net 2.0-3.5为主.
- DBServer的WebAPI重新编译，增加NPLMonoInterface项目.
- ParaEngineServer重新编译：新版本兼容了下旧版的linux编译.
- 新增命令多人模式管理员: /register username password  注册一个新用户
          用户数据在/config/ParaCraft/password.txt文件中, 管理员可自己添加。 如果删除这个文件为可自由加入.
- 新增命令多人模式管理员: /unregister username   删除一个用户
- 输入服务器地址后：如果服务器需要验证， 会自动弹出输入用户,密码的对话框
- 修复与非当前的服务器连接断开时，显示了错误的提示信息.
- 所有点击事件根据每个Entity和Block自己决定是否在本地或Server执行.
- 所有的命令区分Client/Server. 大多数指令会传送到Server执行.
- 新增命令:/configserver 打开服务器配置目录

2014.7.30
- 修复多人创作，同时移动多个物品时方向错误的Bug
- 新版的NPLMono2完成：采用了最新的Mono 3.2.3内核。Win32下不区分Client/Server可以共享同一个DLL. Linux版也升级了， 但是没有发布.  新的NPLMono2使用了最新的SGen内存回收器，Win32下首次支持多线程。可以在Win32下支持多个NPL线程. 之前只有Linux可以多线程.
- 修复超过64个方块同时修改时， Client不更新的Bug.
- ParaCraftSDK中增加了mono模块的Sample

2014.7.29
- MonoLib接口升级到最新的版本.

2014.7.28
- 矿车到地下低于blockY== 0会自动消失
- Fix多人模式下：TNT不爆炸
- Fix多人模式下海绵无法吸水
- 新增命令: /create [id|filename] [bx] [by] [bz]  在指定位置创建一个指定ID的物品(可以为角色或方块等). 例如
          /create 20012  19207 5 19194       在坐标处生成一个矿车(注意下方必须有铁轨).
- 修复内网QQ登录的SSL签名问题
- 新增快捷方式:Ctrl+D 重复上次选择的区域. 如果在选择过程中按Ctrl+D为取消选择.   方便由于误操作需要撤销并重新选择区域的操作.
- 增加指令/hide desktop  隐藏桌面.  可以模拟出电影模式, 但是并不改变当前模式
- 增加指令/show desktop  显示桌面.
- 摄影机和演员可以进入矿车中参与电影的录制

2014.7.27
- 修复多人模式下， Client发起的批量修改导致在Server端错误仿真的Bug.
- 增加了世界文件管理类
- 新增命令: /offsetworld offsetY  将整个世界纵向移动offsetY格子(慎用) 例如: /offsetworld 10

2014.7.26
- Enter可以聊天不用输入/chat指令了。 仅针对paracraft客户端.
- 修理EntityImage的refresh机制。
- 多人优化: 写字板的方向和上面的文字的初次同步完成
- 创意剧场发布3部微电影：《告别那些事》 《木兰花令：词》等

2014.7.25
- 多人优化: 出生点同步完成
- 多人优化: 当人物所在位置的数据没有同步完成时，人物将无法移动.
- 修复反复进入服务器时， server报错的Bug
- 修复动作超过3个人时的动作不同步的问题
- /connect和/startserver命令在非编辑模式下也可用.
- 新增命令: /chat XXX  联网模式下可以聊天
- 修复：Client人物走到很远处， 再传送回来， 无法移动（Chunk不更新了）
- 修复：外网Client登录有1.5秒延迟的Bug. DB创建失败.
- 修复无法命令方块点击会创建的Bug

2014.7.24
- 多人优化: 每当Client链接上一个Server时， 都会自动进入一个新的空世界.
- 多人优化: 当用户移动超过8米, Server才刷新Chunk. 防止频繁发送地形数据.
- 多人优化: Client支持在已经链接的状态下， 去链接另外一个世界，并仅当链接建立后才切换过去。
- 多人优化: 支持在地址栏中输入IP地址或域名来进入指定Server世界。 例如:
     127.0.0.1           127.0.0.1:8099             pc://127.0.0.1:8099
- 多人优化: 登录流程中加入AuthUser的验证消息
- 多人优化: 哈奇中也支持ParaCraft的私服：但是形象全部是ParaCraft的.
- 多人优化: Server模式下底层的地形缓存不再从内存中移除不用的地形.
- 多人优化: 增加Client/Server对Disconnect的处理逻辑
- 多人优化: 管理员可以用/save 指令每隔一段时间自动保存下Server的世界.
- 多人优化: 当Client无法链接Server时， 给出错误提示.
- 多人优化: NPL网络底层的TCP链接设置按照Server的标准配置
- 多人优化: 增加了人物形象的同步

2014.7.23
- 多人优化: 首次进入世界加载性能优化
- 修复高模演员无法用UI换装， 以及初次出现没有贴图的Bug.
- 多人优化: 增加了多人模式下的退出，进入世界，保存世界逻辑
- 多人优化: Server或Client模式下都可以通过退出世界来退出网络。 并且可以反复进入Server或Client状态。
- 多人优化: 禁止Server模式下，同时为Client.
2014.7.22
- NPL底层增加2进制String的传输
- 底层增加BlockChunk的数据压缩，解压以及覆盖
- 多人创作底层100%: 首次进入世界，自动同步人物周围的世界内容

2014.7.21
- 修复railcar不可驾驭的Bug
- 官方服务器使用Hamachi建立完毕， 另外花生壳的VPN服务器也可以.
- STL增加OrderedArraySet数据类型， 优化初次加载的chunk次序， 按照角色周围螺旋加载.

2014.7.20
- 底层加入了对网络层数据的支持
- 动漫节结束: 2014.7.19-2014.7.21

2014.7.19
- 多人优化: 按钮拉杆等有action的物品的点击全部在Server端仿真了.
- 多人优化: 压力板,按钮,红石，活塞，流体等的仿真全部移到Server端了.
- 多人优化: remote world模式下禁止所有Block和Entity的仿真, 全部在Server进行.
- 重构世界访问接口:

2014.7.18
- 多人创作底层99%: client端支持高级创作的自动同步(可在多个Client上创作了)
- 可以用任意公网或局域网IP(或域名)开服务器了:例如:
          /startserver                                                         /connect           本机测试
          /startserver  192.168.0.107  8088                         /connect  192.168.0.107  8088          局域或公网IP
          /startserver  server1.paracraft.cn  12345              /connect server1.paracraft.cn  12345     域名网址
- 多人优化: 增加了击碎效果的同步
- 修复了粘性活塞前面是充能红石线导致运算错误的Bug

2014.7.17
- 修复/renderdist 命令的可视距离上线只有120的Bug. 目前可以最大512.
- 多人创作底层95%: 动态新增的方块改变的自动同步.
- 创意剧场发布微电影：《我是导演》等3部作品。
- 发布多人创作首个Demo:

2014.7.16
- 修复当一个渲染单元数目超过65535时， 方块渲染失效的Bug.
- 深圳动漫节布展：

2014.7.15
- 多人创作底层90%: 完成多用户的同步
- 创意空间文化衫印刷完毕.

2014.7.14
- 修复用户自定义贴图路径如果以/开头，无法显示的问题. 会自动帮用户更正贴图路径
- 多人创作底层90%: Client端对Server Entity的基本位置等信息的同步完成.
- 发布外网补丁.

2014.7.13
- 光照系统修复+优化： 当周围16范围内的区域没有加载时光照不会被计算。 优化部分光照数据结构用了unordered_set.
- 光照会优先计算距离摄影机近的地方.

2014.7.12
- 新增指令：/moviecamera [on|off] 开启关闭电影方块中的摄影机.  也可以通过将摄影机电影方块中扔掉关闭。
- 电影方块功能优化：没有摄影机的电影方块可以独立播放，并且不会不进入电影模式，用户可以进行其他操作。 并且可以多个同时播放。 可以用来做场景动画或布景（循环播放）。
- 创意剧场发布5个新的微电影：《肇庆市第一中学》等

2014.7.11
- 新增指令：/clicktocontinue [on|off]  开启/关闭离开窗口点击继续的设置
- 新增指令：/sound name [filename] [volume:0-1] [pitch:0-2]    播放指定的声音， 结束后自动停止.
/sound anyname break.ogg 0.2 1.2               播放break.ogg在anyname, 音量0.2,音调1.2
/sound break                                             play a predefined sound
/sound 1.mp3                                           播放音乐，自动结束
- 新增指令：/stopsound name  停止指定声音
- 修复材质包切换世界后贴图变黑，无法找到的Bug.
- 多人创作底层85%: 人物动作高频同步(位置, 方向，动作, 头部运动)，Server的物理仿真等完成

2014.7.10
- 实体方块的物理仿真AABB不精确的问题修复了. 矿车在自定义方块上无法行走的问题解决.
- 底层NPL的STL类库更新
- 支持命令行参数world="[word path]" 方便测试.  e.g. world="worlds/DesignHouse/MultiplayerTest"
- Compiled and upgraded luajit version to 2.0.3
- 多人创作底层85%

2014.7.9
- 修复积木动画无法替换之前的方块的Bug.
- 创意微电影宣传片：《我是导演》完成了.
- 完成创意TShirt文化衫设计
- 多人创作底层80%

2014.7.8
- 多人创作底层75%: Refactored PlayerController and world logics

2014.7.7
-  新增指令：/hsv [h s v] [multiply_r multiply_g multiply_b] 调节整个屏幕的色相与饱和度。 前面是3个参数是加法位移，
后面3个参数是乘法.
          例如: /hsv 0 -1 0        /hsv 0 0 0 1 1 1.5
- 修复电影方块中的命令行，天气等变量的第一个关键帧如果不在time=0处，会提前执行的Bug.
- Ctrl+左键支持区域选择：并且支持Entity类物品的选择与删除

2014.7.6
-  PETools修复并重新编译支持VS2013了并上传到了MS的官方网站.
-  修复DNS失效情况下Kids版会更新为Teen版的Bug.
- 新增指令：/selectobj   选择目前能看到的所有物体.
-  Ctrl+左键拖动：支持区域选择了. 可以框选一群物体.  解决用户的实数空间或人物无法选中删除的问题
- 多人创作底层70%

2014.7.5
-  增加了ShaderManger用于添加各种后期处理特效.
-  新增命令: /grey [r g b] [glow_r glow_g glow_b] 开启全屏灰色效果. 例如
/grey 1.2 1.2 0.9
/grey 0.85 0.79 0.74 0.27 0.14 0.03
- 新增指令： /rain 0    /snow 0 表示停止下雨和下雪， 并且会切换到正常的天空
- 切换世界时环境特效如下雨和下雪特效会被消除

2014.7.4
- 修复删除矿车,矿车声音还在的bug
- 修复第0帧的电影方块中的命令可能会被执行多次的Bug.
- 修复ctrl+z, 人物被传送到原点的Bug
- 多人创作底层68%：脚本层架构联通

2014.7.3
- 修复下雨特效内存溢出死机的Bug
- 多人创作底层65%
- 高模演员人物动作优化

2014.7.2
- 防作弊模式Demo
- 优化了/mode 指令，防止多次执行同样的Mode影响效率。 模式切换时，E键UI也会隐藏
- 所有的命令增加了可执行的模式， 目前只有少数命令可以在非编辑模式下使用. 例如/mode
- 运动中的物体（例如车）可以保存在世界中，并且在重新加载世界时保持运动.

2014.7.1
- 多人创作底层60%

2014.6.30
- 由于几名参赛选手反映，存档不够：存档槽购买限制取消，暑期首次购买创意存档，赠送2个存档槽，鼓励用户有多个作品参赛.
- 多人创作底层50%

2014.6.27-2014.6.29
- 修复切换世界后， E键背包内物品还是上个世界的Bug
- 修复箱子等非Cube, 但是Solid的模型打开后，侧面渲染露出墙壁的Bug
- 多人创作底层40%

2014.6.26
- 新增命令:/disconnect 离开当前服务器
- 个人服务器网络链接管理相关内容完成
- Undo/redo改成了Ctrl+Z/Y 防止误操作.

2014.6.25
- 电影播放时右侧的UI隐藏了
- 完成多人创作底层类库
- 新增命令:/startserver [ip_host] [port]  开启个人服务器
- 新增命令:/connect [ip] [port] [username] [password]  链接到别人的服务器
- 思考和设计了MotionPoseEditor动作编辑器
- 优化命令:/sky white|green  分别是白色和绿色的天空，方便影视后期的绿色幕布处理

2014.6.24
- 电影方块中：Ctrl+左键可以复制关键帧。Alt+左键可以移动关键帧(但不移动后面的帧)
- 优化指令： /music [filename|1~6] [from_time] 可以通过命令行指定从第几秒播放音乐. 主要在电影方块中使用。
          例如/music 1.mp3 10.5   从10.5秒的地方播放1.mp3
- C++层实数与方块坐标转化算法优化
- 修复人物在空中的光照是黑色的Bug, 优化了一些光照内存使用算法.

2014.6.23
- 当选中方块后， 用Ctrl+Alt 可以选中所选方块中与当前方块一样的方块。
- 修复摄影机摇摆在关闭情况下, Shift键不起作用的Bug
- 电影人物的速度和重力加速度可以通过UI调整了.
- 每个人物都可以有自己的速度属性了, 并且定义了飞行，跑步的默认速度值。
- 修复删掉关键帧， 字幕不刷新的Bug
- 选择Blocks的效果速度提升为原来的5倍
- 修复当电影方块文字只有1帧时， 渐入渐出效果不对的Bug（之前是必须前后有关键帧才行）
- 拖动电影中的关键帧时（例如摄影机），当一个关键帧十分靠近另外一个时， 2个关键帧会自动相连，相差1. 方便制作蒙太奇动画.

2014.6.22
- F1中增加了逻辑命令的全套帮助
- 修复箱子推动后消失的Bug
- 新增命令: /call [code with return value] 执行任意代码.
- 优化命令: /set a=/call return 1  可以将一个命令的结果赋值给一个变量.
          例如: /set mode=/call return GameLogic.GameMode:GetMode()
                    /if %mode%== "editor" /tip you are in editor mode
- 加入了Entity 3D声音管理类.
- 矿车加入了3D声音:会根据速度自动调整声调和音量。分成人在车上和不在车上2种.

2014.6.21
- 修复光影保存的默认值和/Shader 2指令
- /blockimage 指令可以Undo了
- 物品的tooltip 都包含id了.
- 发布微电影：《当下的力量》 《我从11楼跳下》

2014.6.20
- 修复/blockimage 指令 对奇数宽度的图片计算错误的Bug.

2014.6.19
- 矿车加入了爬坡倾斜，并修复了爬坡会抖动的Bug.
- C++层增加了可以读取任意图片的接口.
- 新增命令: /blockimage [-xy|-yz|-xz] [colors] filename [x y z] 将任意图片转换为方块
          /blockimage 2 preview.jpg    黑白2色
          /blockimage -xz 16 preview.jpg    在xz轴16色
          内部用虚拟线程来创建，支持任意大。 可以用来做:像素画， 地基， 艺术字等.
- 命令/blockimage 增加了1,2,3,4,16色模式
- 新增命令: /sky [-tex] [sim|filename] 改变天空或天空的贴图. 可以用命令方块保存天空状态
               /sky -tex Texture/blocks/cake_top.png   文件可以相对当前世界的目录
               /sky -tex 使用白色天空盒子
-  新增命令: /fog [-color|skycolor|fogstart|fogend] values  改变雾的颜色和距离
               /fog -color 1 1 1          /fog -skycolor 1 1 1          /fog -fogstart 80          /fog -fogend 100
- 优化了/loadtemplate -a的建造动画， 看上去基本是从下到上建造的.

2014.6.18
- 增加了可替换材质的天空盒子
- 增加了高清演员actor（测试用）：有面部表情和更多骨骼.
- 修复新的物理仿真时，浮点数Round-off error in AABB math. 矿车极少数情况下会穿越方块的Bug解决了
- 加入了伤害结算系统和伤害类型.
- 非编辑模式下， 连续点击矿车，矿车会倾斜，之后矿车会粉碎变成可拾取的物品.
- 修复人物类模型在非编辑模式下创造，数量不减少的Bug.

2014.6.17
- 新增方块：探测铁轨：当有矿车通过时会发出红石信号（效果与压力板类似）；当矿车上有人，并且人的背包中有东西时，根据东西的多少会向链接的中继器充能
- 新增命令: /loadtemplate -r [templatename] 清空场景, 配合-a 可以在电影方块中反复使用, 例如
/loadtemplate -r test
/loadtemplate -a 15 test
- 修复物体仿真系统中时间间隔导致仿真的FPS不恒定的Bug, 矿车运动得更平稳了.
- 修复电影方块中的命令行，被反复调用的Bug.
- 修复摄影机关键帧首次不显示的Bug.
- PC中设置菜单中大多数选项可以保存了：如声音，鼠标反转，摄影机摇摆等等

2014.6.16
- 电影方块的所有角色R键录制都支持undo/redo. 之前只有摄影机支持.
          并且R键的开始，结束时间也会被记录， 并且undo/redo时保存, 方便反复录制，直到满意。
- 新增命令: /savetemplate [templatename] 原点采用当前选择方块的Pivot坐标位置（比如某个特殊的方块或命令方块）并且没有方块数目的选择上限。
- 修改人物或命令的关键帧数值时，对话框中会显示上次的数值.
- 修复录制UI，文件名太长无法点击的Bug.
- 新增命令: /loadtemplate -a [seconds] [templatename]  模拟人创建场景的过程，可以指定多少秒创建完成。可以用来做一些很Cool的动画. 例如/loadtemplate -a 10 test
- 发布外网补丁

2014.6.15
- 修复Shift键无法删除关键帧的Bug
- 修复Camera状态下， 无法添加字幕关键帧的Bug
- 新增命令: /loadtemplate    /savetemplate   用了新的类来实现

2014.6.14
- 修复删除和添加动力铁轨时，周围铁轨充能状态不刷新的Bug
- ParaCraft登录器的IE窗口使用了独立线程， 但出错， 还是会Crash整个登陆器
- 加入了VectorPool 优化了性能.
- 2个矿车可以在铁轨上碰撞，并加速，逐渐获得相同的速度。
- 一名玩家保存后， 所有文件内容都变成了0， 但是文件尺寸是对的。 查了很久，原因不明

2014.6.13
- 修复上方有方块时放置物品无效的Bug
- 修复矿车无法保存方向的Bug
- 动力铁轨与普通铁轨可以连接
- 人物在矿车上按W键可以缓慢的让矿车有个初速度
- 父亲节发布3部微电影：苹果树全部内置拍摄，时光2, 父亲

2014.6.12
- 矿车的物理仿真. 以及矿车可以在轨道上运动了
- 自定义的方块可以使用替换命令了
- 人物Entity(例如矿车,mob)的鼠标带选取区域更精确了
- 坐骑系统底层完成
- 右键矿车人物可以跳上矿车， Shift键或连跳可以下来，下来后会被传送到周围的一格。人在车上也可以跳跃一次.
- 增加动力铁轨：红石信号可以传导16格。激活为加速，不激活为减速。激活方式与红石导线基本一致。当一端被其他方块挡住时， 在激活状态下会过得向另外一端的初始速度(可以用作启动矿车).

2014.6.9-2014.6.11
- 优化64位脚本浮点下为Block坐标的转化函数
- 增加基于脚本的Entity与Block之间的碰撞检测，包括新写了一系列物理运算和缓存类。 包括Discrete AABB, AABBPool, new STL vector, block collision detection, entity physical movement function, etc. 从此脚本层可以独立的运算基于AABB的物理仿真（仅限于Entity和Blocks）。
- ParaCraftMobile项目在GitHub上建立完毕

2014.6.8
- 修复加载世界时如果可视距离/renderdist 改变了， 则光照计算错误的Bug (黑色区域)
- 加入了矿车和轨道的新类
- 多人创作20%
2014.6.7
- 修复论坛中2个ABOC(key digg)的插件导致网站访问缓慢的Bug。 由于Google被墙了, 删掉了对google jquery的外部引用。
- 修复哈奇中人物走动时头部方向不对的Bug. Entity类增加了是否为方块人的函数IsBiped().

2014.6.6
- 增加命令: /flood [radius or 10] [block_id] [x] [y] [z] 用水的方式填充人物所在区域
- 增加命令: /unflood [radius or 10] [x] [y] [z] 吸干人物所在区域的水
- 电影关键帧类型选择加入了列表框，方便快速选择。
- 电影关键帧全局角色增加了命令行变量.
- 创意剧场APP开始规划

2014.6.5
- ParaCraftMobile项目从技术Demo到正式立项与分工
- 电影方块优化：左下角会显示当前正在编辑的角色, 演员也可以显示关键帧并编辑，例如人物动作，模型，手持，皮肤，大小等

2014.6.4
- 优化了画球算法，命令格式改为/sphere radius [beSolid]       radius 为半径  beSolid 为true表示是实心球，false表示是空心球，不填默认是空心球
- 增加命令/ellipsoid radiusX radiusY radiusZ beSolid  画椭圆体，radiusX 为X轴方向半径，radiusY 为Y轴方向半径，radiusZ 为Z轴方向半径  beSolid 为true表示是实心椭圆体，false表示是空心椭圆体，不填默认是空心椭圆体
- 多人创作架构代码
- 创意空间宣传片分镜头
- 创意剧场发布3个作品《挖井》《排队》《带刺的人生》

2014.6.3
- 第一人称摄影机录制不会显示中间的十字叉了
- 录制中Title中加入了当前录制时长的显示
- 修复MovieCodec中的一个卡顿时的录制异常终止的Bug，以及最多录制10000帧的Bug.

2014.6.1 - 2014.6.2
- 再次设计多人模式

2014.5.31
    - "/ring [plane] radius [thickness]", "/circle [plane] radius" 优化了画圆和环命令，再3个平面都可以画了
 - 增加命令：画球命令 /sphere radius

2014.5.30
- 修复了录制声音时有破音的Bug. 加大了声音的录制缓存.
- 加入Windows自带的文件输出目录选项.

2014.5.29
- 所有的ParaEngine插件支持不用访问调用ParaEngineClient的接口
- 所有MovieCodec Plugin的Log都会写入log.txt

2014.5.28
- 视频录制时，默认采用了真实时间的录制模式，而不是虚拟时间。 这样可以动态的捕捉声音不会与画面有差异.
          测试：960*560 25FPS 高清音视频 + 光影全开 + 动态MP4压缩 （2400KBPS）： 在多核主流计算机上是完全流畅的。
          测试：1280×780 30FPS 高清音视频 + 光影全开 + 动态MP4压缩 （5120KBPS）： 在多核主流计算机上是完全流畅的。
- 增加了720P高清分辨率30FPS的电影输出.

2014.5.27
- 修复创建的新物品，创造时只能有一个方向的Bug.
- 修复摄影机离墙很近时，会反转180度的Bug.
- 修复创建的新物品ID重复的Bug, 以及同一个贴图ID不共用的Bug.
- 录制UI加入了材质包切换和光影选项，避免录制时忘记.
- 电影输出增加3秒后开始的选项.
- 电影的默认字体从20变成了25.
- 当电影播放时，声音不会因为切换窗口而消失.
- 修复多行文本框, 用DEL键导致后一行文字消失的Bug.
- 修复可视距离调试时, 光照远处出现黑色的Bug.  修复可视距离超过256时，光照会渲染没有加载的区域.

2014.5.26
- 支持只有1格高的人物物理仿真（之前是2格高）
- 摄影机人物改为只有1格高的物理了，可以穿越窗户等.
- 替换操作支持对有内部数据的物品进行Undo操作, 如不小将电影方块替换成了其他方块， 可以Undo回来，并保存里面的内容了
- 摄影机按住Shift可以穿墙，并且这种状态可以通过关键帧保存下来。
- 当摄影机在墙中 并且眼睛的位置没有碰撞时， 自动忽略摄影机的物理。

2014.5.25
- 修复背包zorder,在书的Zorder之下了
- 增加了一些优秀的用户作品到推荐列表：如《遗忘的宝藏》等, 给用户寄的礼物和证书有很好的反馈.

2014.5.24
- 电影方块可以不用中继器，紧靠在一起摆放，这样可以避免中继器造成的0.5秒延迟。会自动识别触发的方向，但是中继器仍然是推荐方案.
- 视频输出/停止的快捷键F9. 窗口TitleBar上有录制的提示显示
- 导出设置UI中可以选3种页面边距

2014.5.23
- MP4和FLV都支持声音的Loopback录制了。 UI中可以选择是否录制声音。
- 输出视频时可以选择是否增加水印功能

2014.5.22
- 增加WSAPI的Loopback声音录制模块
- FFMPEG的视频录制用了一个独立的线程, 性能大幅提升
- 修复内存不够时，程序Crash的Bug.

2014.5.21
- FFMPEG 采用了GDI方式截图而不是DirectX Backbuffer. 大幅度提高了性能。
         录制时默认分类率提高到640×480. 帧率从20FPS, 提高到25FPS.
          支持GIF, FLV, MP4等格式的输出了。
           "RecordingFPS" and "VideoBitRate" 可以调节了
- 增加了视频输出设置UI：用户在导出时可以选择分辨率， 格式等信息了。

2014.5.20
- 修复Rain/Snow 特效面向摄影机的Bug.  以及修复投影并稍微提高了性能和优化了随机函数分布
- 修复中文材质包无法保存的Bug.
- 修复电影编辑模式下切换世界下方物品栏失效的Bug
- 电影人物默认的重力加速度和主角一致了。
- 21部创作大赛的用户作品上传了官方视频.
- 演员增加飞翔模式（F键）
- 修复电影Bug：人物坐下动作会先站起来再坐下，应该去掉前一个预备动作。
- 以上更新发布了外网：0.7.72

2014.5.19
- 修复电影人物运动距离太远人物会消失的Bug.
- 修复在哈奇中方块人物坐下躺下等的动作不对的Bug.
- 电影播放模式下，无论是否编辑模式。 都无法选择物体。 并且不会有ClickToContinue出现
- 切换游戏模式改为:Ctrl+G 避免误操作。
- 修复FFMPEG模块在不使用时也会动态加载的Bug

2014.5.17-2014.5.18
- 动漫创作大赛21部创意大赛， 创作， 评比完毕。 并颁奖

2014.5.16
- 无论编辑模式还是游戏模式， 播放电影时，按R键就自动重新播放并输出MPEG4视频
          此时会隐藏大部分UI, 禁用切换窗口FPS自动变低，并在全部电影结束后，自动结束录制，并恢复UI显示，中途可以用R键结束.
- 播放模式下电影方块的红石输出从0.5秒提升到2秒。 修复2个电影方块切换时，画面回到之前的Bug等。
- FFMPEG方式的视频录制默认使用当前分辨率输出， 并且可以设置四角的页面边距。
- 电影模式下视频输出时（即使是编辑模式），鼠标也不可以Pick任何物体。
- 电影编辑模式下， 当用按钮激活电影方块时， 有MPEG的录制按钮
- 修复材质包无法打开材质目录的Bug.
- 修复字幕淡出效果不生效的Bug。
- 修复电影正常播放过程中有很低的概率会突然暂停的Bug

2014.5.15
- 内置视频输出v1.0: 采用FFMPEG电影输出. 需要安装插件，目前不在默认安装包中。
          新版视频输出：支持了开光影的录制
- 增加命令: /record 开启关闭视频输出。
 - 下雨下雪天气效果v1.0完成:自动跟随摄影机位置， 自动识别室内与室外以及遮挡物。
 - 增加命令: 命令/rain [strength] 、 /rain [strength] 开启

2014.5.14
- 电影角色模式（或任何俯身状态下）下：B键会打开所俯身的人物的背包。 方便更改手持道具。
- 修复电影模式下：编辑摄影机时无法undo/redo摄影机关键帧的Bug。
- 修复选择多个方块时， 用Ctrl+Shift选择，物品数目不刷新的Bug.

2014.5.13
- 增加了电影字幕编辑UI:   新增功能： 支持多行文字，字体大小， 字体颜色， 文字动画（渐入渐出等），
          背景颜色， 文字位置（下方或中间） 背景动画（渐入渐出等）等
- 电影文字只从添加的关键帧处开始：无需将第一个关键帧设置为空。
- 修复电影模式下， 主角视角无法Undo的Bug.

2014.5.12
- 增加了天气系统：如下雨/雪的基本类
- 尝试了Office VPN
- 完成4个微电影世界：圆的故事 等等
- 完成一个新的擂台场景
- 统计了首届电影大赛投票结果， 征集创意短篇。
- 制作了ParaCraft海报。
- 思考： 如何组建一个微电影评审组?

2014.5.10-2014.5.11
- 动漫基地培训
- 阅读了101个小故事

2014.5.9
- 世界加载UI上增加导入/导出按钮...
- 人物属性中可以切换多个人物动物模型
- 加载世界的材质不存在时， 不弹出提示。支持中文名的材质包名称的显示。
- 修复2个皮肤缺失的Bug.
- 点击村民，手中会拿着村民。
- 去掉了只读世界，不可以点击物品Icon的限制.
- 材质包用压缩格式处理了一下. PNG缩小了50-100倍。
- 玻璃窗再次修改. 中间采用一个面片.
- 采用registeritem 指令产生的Item会随世界自动保存和恢复
- 哈奇中的材质包已经换成和PC一样的了

2014.5.8
- 活塞模型和材质重做，可以置换了.
- 所有官方人物皮肤用XML管理了, 全部重新命名.
- 增加了2个官方皮肤:老奶奶的皮肤
- 增加了3个官方动物皮肤:熊人等
- 修复玻璃窗十字模型不显示的问题. 玻璃窗重做.
- 方块置换贴图支持水等动态贴图了.  所有方块都支持用动态贴图代替之前的（动态或静态）贴图. 例如water_fps3_a009.png
- /registeritem支持同ID覆盖之前的ID并自动刷新所有的引用
- 压力板，活塞， 粘性活塞等重做并支持置换贴图.
- 增加新动物：鸟
- ParaCraft论坛图片宽度改为600了

2014.5.7
- 关闭了阿里云云盾:论坛恢复正常
- 修复多个方块的材质路径，发布后需要全面测试每个方块的模型资源
          铁轨模型重做, 所有方块材质移动到texture/blocks下面了

- 增加指令: /registeritem[block_id:2000-2999] texture [base_block_id]  创建新的物品类型。
/registeritem 2000 Texture/blocks/lapis_ore.png 234
/registeritem 2001 Texture/blocks/items/1013_Carrot.png 115
- 命令方块/registeritem中可以用画册和其他物品合成新的物品。 方块合成命令：第一个必须为画册，第2个是模板

2014.5.6
- 修改方块名字：木门-->木窗，铁门-->铁窗
- 铁窗，木窗的模型改变了，采用面片， 提供更多DIY空间
- 材质包替换时必须以数字开头
- 材质包和所有模型类方块，都支持texture2,texture3,...属性。 多模型支持texture_index属性。
- 按钮,拉杆，铁窗，木窗，铁门， 木门，红石火把，中继器采用了可替换材质。
- 创建门时， 会自动将窗户也创建出来。 2格高的木门，铁门。
- 高亮特效时也采用PointTexture filtering. 例如按钮方块的高亮.

2014.5.5
- 创意剧场2期：3个微电影发布：窗， 对岸， 对猪弹琴
- 整理了BBS的下载贴的位置. 制定了创意剧场的编辑工作流程.

2014.5.4
- 非编辑模式下播放电影不会显示人物选择框。
- C++和脚本层分别加入了针对Touch设备的角色控制函数
- 任意物品获得时会播放一个3D动画：Icon飞到人物头顶.
- 当画册被单击删除后， 会变成一个物品，物品Tooltip中包含画册图片的路径， 当再次使用这个物品创建时， 上面的图片可以保留下来。 这个功能不仅可以方便的移动图片， 还可以用于将画册与其他物品合成为新的物品。
- 增加新方块：地毯方块(16种颜色)，每种有6个方向.

2014.5.1-2014.5.3
- 增加了开源模块ffmpeg , 即将支持任意格式的内置电影输出（包括FLV, XVID, GIF, AVI等）
- 增加了C++插件: MovieCodecPlugin 采用ffmpeg 模块, 用于音频视频格式转换。

2014.4.30
- GUIBase和GUIContainer增加Point Filtering选项，用于画板等地方
- 增加玩家内置DIY画板底层API，支持Alpha通道的渲染和擦除。
- CGDIGraphics 画笔支持Alpha通道，且当Alpha=0时，自动变成Alpha擦除
- 每个GUIBase支持External Renderer
- 冰块和水都可以透光了. 例如冰和水中放入发光的块

2014.4.29
- 当有版本冲突时， 会自动备份整个世界到backups目录
- ESC 菜单以及备份时会显示当前的版本号，并可以打开备份目录
- 保存世界UI不再自动截图, 一些保存时的信息提示优化。
- 只读ZIP世界也可以打开所在目录了
- 备份数据可以保存blockworld.lastworld目录了,并且会自动忽略blockworld目录
- worlds/backups/目录会自动保留当天的3个存档， 以及之前3天每天最新的存档。
- 任何修改过并保存的世界都会在退出时自动备份

2014.4.28
- 保存世界时加入了版本号revision

2014.4.27
- 深圳罗湖区创意培训课结束了。 3周，6整天的课程。 30多位师生.

2014.4.26
- 新增指令/generatesrc   1期源代码开放
- 当人物降落到空世界的最下方时， 会自动生成一块。

2014.4.25
- 修复：哈奇中角色的创作，坐下，躺下等动作不对的Bug。
- 修复：哈奇中跑步时头的方向不对。

2014.4.24
- 修复Win8.1 触屏下, 切换窗口Crash的Bug
- 构建了C++底层的Touch触屏API接口.
- NPL脚本层和所有ParaUIObject增加了多点触控API接口和回调函数

2014.4.23
- ParaCraft论坛全面改版
- 电影人物支持换模型和模型随时间改变.
- 修复midi 可以支持任意长的Note. /midi [0-127]
- 修复ParaCraft安装包在XP下不是有效EXE的Bug.
- 重写了ParaCraft的启动器, 启动器支持离线模式, 修复了之前启动器不稳定以及网页显示不出来的Bug.

2014.4.22
- mid音乐文件可以从ZIP文件包中读取了, 目前全局只能有一个MID文件播放
- 重构了论坛版块
- 加入了MIDI的音符播放API: 例如： ParaAudio.PlayMidiMsg(0x00403C90)
- 增加指令:/midi [1-7] 播放一个Note.
          /midi 0x00403C90    play a raw note 3C with velocity 40 in channel 0.
          /midi [1-7]          do la me fa so la si
          /midi a[1-7]     lower tone
          /midi g[1-7]     higher tone
- 增加方块：音符块（相应红石信号）。 如果没有指定音调， 则由方块下方的方块材质决定音调。
          默认为C调60。石头是14， 砂子21， 木头35， 玻璃70
          每创建一个新的方块会自动将音调调高一节. 通过播放一个Note， 可以重置。
- 长按左键如果移动到其他方块，并不会消除方块.
- 长按左键并移动鼠标可以弹奏音符方块。
- 世界作者角色名字可以通过inventorypage修改，并可以保存

2014.4.21
- 录制视频时， 选择解码器的窗口会前置。 强制用户选择.  目前的录制不支持真实光影.
- 视频解码器选择框会自动记住上次用户选择的解码器类型了, 例如Microsoft Video 1。
- 首次录制会默认选择Microsoft Video 1为解码器, 但是我们推荐用户安装XVID, DIVX解码器.
- 修复B键打开背包，当背包空时会Crash的Bug
- 修复了GitHub的BAT文件的LineEnding不对, 导致无法运行的Bug.  加入.gitattributes 文件标记eol.
- ParaCraftSDK的Bin目录下我加入了7z.exe可以做自动打包用.
- ParaCraftSDK的Publish.bat可以用来自动生成完整安装包以及ZIP包.
- 本地模板保存汉字乱码bug修复
- 保存模板换了新UI
- 音乐盒与/music 指令支持mid格式的音乐了

2014.4.20
- 深圳罗湖区创作大赛2期结束
- 制作了新一批的课件.

2014.4.19
- 演员ActorNPC可以录制创建和消除方块的动画了

2014.4.18
- 修复Bug：切换到摄影机录制时， 会自动切换到摄影机的录制视角，而不是角色视角.
- 修复Bug：当摄影机上方有方块时会卡住动不了的Bug解决了.
- 加载世界的UI更大了,支持长的文件名.
- 更换材质的UI优化了， 并且可以显示预览图并自动记住上次世界的材质包.
- 修复首次切换摄影机ASD键无法行走的Bug.
- 修复摄影机在地面会从飞行模式变为陆地模式的Bug.
- ParaCraft中人物进入飞行模式， 不会因为降落到地面而自动切换到正常模式.
- 增加了方块拍摄时，当选中ActorCommand或ActorBlocks时， 会高亮所有相关的Block.

2014.4.17
- 当增加或删除电影关键帧时都会有声音提示.
- 增加了角色创建方块和消除方块的录制功能
- 编辑模式下的预览：摄影机控制器也一直存在关闭按钮和播放按钮，但是没有录制按钮.
- 只有摄影机演员无法创建方块， 其他演员都可以创造方块了
- 摄影机也支持角色扮演的录制方式了, 每5秒自动生成一个关键帧.

2014.4.16
- 修复Timeline关键帧点击区域的Bug
- NPL序列化时索引从Int32扩展到int64和Double.
- 增加电影方块角色ActorBlocks: 可以录制以创建和删除方块为关键帧的动画。

2014.4.15
- 当影片长度设置为0后， 无法通过右下角的UI设置影片时长的Bug解决了
- 修复首次打开电影方块编辑UI时，右下角TimeLine上的影片结束时间与真实时间不一样（总是10秒）的Bug
- 增加了摄影机物体的移动速度.
- 修复拖动TimeLine, 关键帧数值会跳动的Bug。 这个Bug同时修复了， 给摄影机添加关键帧时， 一拖动时间轴摄影机就复位到前一帧的Bug.
- 修复SliderBar拖动时，如果SetValue导致数字闪烁的Bug.
- 当关闭或Alt+F4等操作时， 会自动弹出一个界面，让用户确认是否保存。 小技巧：如果再次点关闭，将默认为关闭并保存
- 电影控制面板上的主角UI高亮贴图优化
- 外网火把， 门等资源发错修复

2014.4.14
- 修复Picking到未知方块时， 会有Runtime的Bug.
- 木窗的名字改回木门， 与创作百科一致。 新增的改为了封闭的木门。
- 修复创作百科模式下， 无法通过E建自由选择方块的Bug.
- 修复完整客户端，灯，中继器等材质缺失的Bug.
- 创作百科中已经解锁的任务点击经验条旁的按钮就可以一键完成了
- 增加指令: /cheat [on|off]  打开作弊模式. 目前只针对创作百科.
- 作弊模式下：所有创作百科的任务都可以接
- 百科任务，进度条旁加入了自动完成的功能。 上来就默认有1次， 每3秒补充一次（1次可完成一块，Cooldown有提示）.

2014.4.12-13
- 深圳罗湖区创意空间培训课， 教师组，小学组， 中学组，共60多人。 3个教室，全天授课.

2014.4.12
- 修复右键命令无法打开书本的Bug
- 当人物与摄影机的距离很小时（包括第一人称）， 人物的头都会面向摄影机的方向， 而不是鼠标所在的位置。
- 增加命令: /recorder 打开视频录制界面

2014.4.11
- 增加角色ActorGUIText: 可以添加游戏内的字幕了
- 修复电影播放时快捷栏不隐藏的Bug
- 修复正常播放电影时，其它UI不隐藏的Bug
- 游戏模式下正常播放电影时会隐藏全部UI， 包括TimeLine. 非游戏模式下会显示Timeline， 但不显示Controller.
- 修复电影编辑或播放过程中退出并切换世界导致一些UI失灵的Bug.
- 加入了新的方块：铁门+木门 逻辑和铁门， 铁窗一样
- 制作了创意工程师的名片
- 制作了电影教程视频.
- 创意空间动漫基地教学视频：前4个课时的视频（辛苦奇仔为我们录制数小时的精良视频）
- 精品视频： 男孩与苹果树， 爱回家。
- 建立ParaCraft百度云盘

2014.4.10
- 创建电影角色后会自动附身并选中.
- 大家共同制作了TheBoyAndAppleTree 电影:9 分钟微电影
- 修复在拖动时间轴时， 当前人物头的方向会随鼠标乱动的Bug.
- 修复960×560分辨率下电影编辑器无法点击关闭按钮的Bug.
- Ctrl+F12隐藏全部UI时：mini-scene中的特效不会隐藏， 如方块的击碎特效会出现。
- 重构Entity人物头部运动代码， 支持多人同时做头部控制， 并且可以自定义抬头和低头的角度。
- 人物的头可以更低了，每个Entity可以配置最大， 最小角度.  NPC(演员)的低头角度的默认值是主角的2倍.
- 当演员有摄影机焦点时，变为无法选择， 只能通过点击电影控制器上的设置按钮选择编辑人物属性。 这样做的目的是，让人物可以低头等运动更加方便。 不会选择到自身。
- 人物在潜行模式下（按住Shift）移动时，头部仍然会转向鼠标所在的方向。

2014.4.9
- 修复了播放模式下摄影机0.5秒后会抖动一次的Bug
- 修复强制终止播放后，无法再次打开同一个电影块的编辑UI.
- 增加快捷键R键 （开始扮演录制或暂停）
- 增加快捷键K键 （电影的编辑模式下， 增加一个摄影机或角色的关键帧）
- 增加了电影命令物品:ItemTimeSeriesCommand  和 电影命令角色ActorCommands. 支持拖拽。 Undo/redo等
- 增加了命令角色的常驻Timeline UI显示。可以通过UI切换当前正在编辑的关键帧变量：如文字,时间, 声音等
- 增加命令：/addkey [text|time] [value] 可以为电影增加关键帧（如文字,时间, 声音等）
- 角色ActorCommands的Timeline中, 右侧按钮可以添加或修改关键帧.
- 角色ActorCommands 加入了每天时间的动画变量(time)
- 角色ActorCommands 加入了字幕的动画变量(text), 增加了编辑和修改关键帧的专属UI.

2014.4.8
- 修复人物录制到最后一帧没有自动停止的Bug。
- Enter键进入命令输入方式与摄影机模块UI不重叠
- 增加快捷键P(暂停或开始)， Ctrl+P 停止当前摄影机模块
- 演员动画增加参数: 重力(决定每个演员跳跃的高度)
- 所有内置动画都有了固定的ID，并且在程序启动时会预加载， 所以演员可以正常录制外部动画了. 例如/anim sit
- 演员手中可以拿方块并切换方块了。 通过编辑人物背包中第一个格子

2014.4.7
- 修复Slider拖动会有位移误差的Bug
- Shift+左键点击关键帧， 可以删除一个关键帧
- 电影控制模块加入了背包设置按钮
- 电影拍摄过程中对关键帧的所有修改可以Undo/Redo了.
- 修复未定义EntityClass的Block导致runtime的bug
- 加入了开始于结束时间的现实
- 拖动关键帧超出最长时间会变为最长时间。
- 可以通过UI更改电影的终止时间了。自动更新/t seconds /end 命令.
- setblock 命令加入了where sameblock 参数. 可以用来批量修改一个区域中指定方块的blockdata

2014.4.6
- 摄影机模型在录制和播放时， 会面向正确的方向。
- 增加了关键帧的显示。
- 点击关键帧附近的区域会自动移动到前面或后面一帧。
- 加入了最近点击的关键帧书签
- SliderBar 拖动优化：即使鼠标移出空间， 仍然可拖动。
- 点击Keyframe可以位移一组关键帧

2014.4.5
- 增加了电影片段的编辑模式，可以加演员，可以快速切换角色
- 电影模式下可以选择主角。
- 优化了电影片段的编辑模式的UI操作。
- 电影模式下FPS模式都需要按住鼠标右键，这样保证UI可以点选。

2014.4.4
- /skin 指令增加相对当前世界目录的贴图文件
- 增加了电影模式/mode movie
- 编辑模式下， 选中电影，会自动进入电影模式。

2014.4.3
- 演员增加了皮肤， 头部方向， 动作， 朝向动画参数的录制
- 在回放演员动画时， 忽略头部的自动跟踪
- 插件Mod系统v1.0开发完毕
- 源代码导出流程开发完毕
- 人物运动行走的动作可以录制了
- 修复录制模式下的shift行走的录制
- 演员增加了行走速度的动画录制/speedscale
- 右键点击演员可以编辑演员的属性（如大小和名字）
- 演员增加了放大缩小的动画录制.
- 摄影机和演员都可以手工加入关键帧了. 可以用来录制更平滑的摄影机动画
- 支持一遍Play一遍加入关键帧。
- 点击扮演或播放， 可以暂停或继续该功能。
- 增加物品:Apple苹果
- 增加儿童到老人的几个皮肤.
- 修复：摄影机旋转动画，2个关键帧之间会优先从弧度小的方向旋转。
- 摄影机部分暂时关闭【扮演录制功能】，全部由【KeyFrame】功能代替

2014.4.2
- 修复：当人物用/hide指令后， 阴影不再显示
- 增加了MovieClip的时间轴的现实，编辑， 拖动， 设置总时长等功能。
- 修复第一人称下俯身无法选择物体的Bug
- 修复俯身拍摄时中键无法使用的Bug
- MovieClip被电路信号激活后自动切换到默认摄影机
- 摄影机会录制6个方向+是否第1人称。共7个维度的动画数据.
- 修复录制退出后人物行走模式不对的Bug
- 摄影机不会投影
- 电影增加PlayMode，PlayMode下摄影机不会显示
- 多个电影片段衔接时， 保证摄影机正确蒙太奇切换。 0.5秒没有后续电影则切换回主角。
- 支持没有摄影机的MovieClip.

2014.4.1
- shift键进入潜行模式， 速度减半， 平时按shift会弯腰
- 增加命令：/end 用于终止电影片段。 例如
         /t 30 /end  30秒后停止播放.
- 加入了录制UI, 可以中途暂停， 播放，或继续录制.
- 所有电影数据可以被保存并通过物品移动
- 摄影机默认是可以飞行的。F键对其无效.
- 通过对MovieClip写入指令/t 10 /activate 可以循环播放一个电影片段。
- 编辑MovieClip角色时， 场景内的物品会自动刷新.

2014.3.31
- 增加了角色录制功能
- 增加命令：/addactor [npc|camera] 新建演员或摄影机到当前的时间起点。
- 物品, 时间序列，等的编辑UI会自动关闭前一个打开新的。
- 播放中或当前选中的电影方块会闪烁.

2014.3.30
- 修复出生点无法放置的Bug
- 物品改名: 向上导体, 苔石墙
- 实现了电影系统相关的代码架构：包括MovieManager, MovieClip, Actor, ActorCamera, ItemTimeSeries, EntityCamera, 等.
- 增加命令：/movieclip [-stop]     暂停当前的电影片段

2014.3.29
- 增加命令：/focus [@playername]  俯身到某个角色身上. 主要用于电影拍摄。
          /focus  没有参数表示切换回主角
- 按住shift键， 人物运动速度为之前的1/5. 并且会使用Walk动作而不是Run动作.
- 修复画板有时导致世界方块无法加载的Bug

2014.3.28
- 在选择Blocks的过程中用Z,Y 可以Undo, Redo。 Ctrl+Z是Undo选择操作.
- 变换窗口支持复制与不复制. XYZ用不同的颜色字体。
- 变换窗口支持动态实时预览(绿色虚框)
- 选择Blocks时， Ctrl+V会默认显示绿色虚框和变换窗口，需要点击确认才会粘贴.
- 选择方块是：Ctrl+Shift+left click 可以选择或取消选择单个方块
- 完成MovieClip系统的设计方案v1.0

2014.3.27
- 增加指令: /disableinput [@playername] [x y z] [true|false]  禁止命令方块，含羞草，或人物等Entity的所有输入
          /disableinput
/disableinput ~ ~ ~
/disableinput @test false
/disableinput 20000 10 20000 true
          在命令行中加入，可以产生让剧情对话只能看一遍的效果。
- 增加指令: /applytexturepack [folder_or_zipfile] 应用指定文件和目录的材质包。
          /applytexturepack blocktexture_FangKuaiGaiNian_16Bits.zip
          /applytexturepack  空表示默认材质包
- 每次进入世界会恢复默认材质
- 增加了每个方块的表面滑动系数slipperiness. 默认0.25米.
- 人物在冰面会滑动100米才停下来.

2014.3.26
- 内部组织了开源讲座
- bbs板块划分
- CD-KEY插件更新

2014.3.25
- 发布ParaCraftSDK并书写了使用简介
- 修复了红石导体下方无方块时工作异常的Bug
- BBS网站开发完毕了CD-KEY插件. 所有的用户可以发行自己的CDKEY了
- ParaCraftSDK中完成了发布App的Publish脚本.
- 记忆学习的方块渲染优化。没有方块但有链接的地方会显示出来.
- 增加指令: /translate from_x from_y from_z (dx dy dz) to offset_x offset_y offset_z  移动一批方块到指定位置
          /translate ~ ~-1 ~ (1 1 1) to 0 3 0
- 增加指令: /rotate [x|y|z] from_x from_y from_z (dx dy dz) angle [to pivot_x pivot_y pivot_z] 按照某个轴旋转一组方块
          /rotate x ~ ~ ~ (3 2 3) 1.57 to ~4 ~ ~
          /rotate y ~ ~ ~ (3 2 3) 1.57

2014.3.24
- 完成ParaCraftSDK的BAT脚本
- 完成ParaCraftSDK的2个Sample:  SampleWorld, SimpleWebServer,
2014.3.23
- InfoWindow 加入了BlockData的显示
- 修复可拖动UI， 部分区域AutoSize后无法点击的Bug. 如命令方块的编辑UI。

2014.3.22
- SandboxAPI 开放了一批新的类，几乎包括所有Block相关的大类.

2014.3.21
- 论坛有了新皮肤
- 给ParaCraftSDK增加了一些Sample
- 测试了论坛的商务功能

2014.3.20
- bbs加入了悬赏模块
- 升级指令： /music 可以停止音乐
- 点击音乐盒可以播放或关闭音乐
- 出生点物品可以删除了：右键点击即可
- ParaCraft.exe安装包优化：只需一个文件即可，无需AutoUpdate.dll了
- 整理了物品列表
- 创意百科中加入了BBS的问答按钮.
- 建立开源的ParaCraftSDK项目: 对用户开放ParaEngine和NPL语言的第一步.
              下载地址： https://github.com/LiXizhi/ParaCraftSDK
               让用户可以学习和研究NPL语言，开发ParaCraft应用， 甚至独立产品.

2014.3.19
- 支持自定义物品图标的右下角的文字。只要给物品起名时，包含[XXX]. 例如:  介绍[bbs]
- 修复服务器列表下载无法支持有参数的URL的Bug
- 修复本地目录最多显示50个世界的Bug.
- ItemBook书中支持字体加粗， 加背景，以及加超链接， 格式和TWIKI一致
-- 加粗: *your phrase*
-- 背景色: =your words=
-- 超链接: [[http://www.paraengine.com][paraengine]]
- /text 命令同样支持上述TWIKI格式的文字特效
- 增加指令: /text [-p] [-w] text
          /text 指令可以通过点击鼠标左键，快速前进。
          /text -p  暂停Entity的时间， 直到用户点击鼠标左键关闭当前对话，才进入下个对话
          /text -w  用户必须等待Entity，无法通过鼠标左键快进。

2014.3.18
- 重构cmd list避免部分代码有重复，
- 缓存代码编译结果， 提高了命令行的执行效率
-  /if 命令支持>= > ==  <= < 操作符号
               /if 2 >= 1 /tip 2>=1
               /if 1 < 2 /tip 1 < 2
-  增加命令: /jumpto [line_offset|end|begin]  跳转到指定位置的代码。 例如：
                    /if %name% == "0" /jumpto 3
/tip your name is NOT 0
/jumpto end
/tip your name is 0
-  增加命令: /open [-p] url   可以打开URL地址. -p表示需要取得用户同意确认
               /open -p http://www.paraengine.com
- 增加了可自定义每个世界的桌面物品的功能（只有编辑模式可编辑）。 目前开发了左上角两个位置。
-  加入任务物品：URL地址: 可以编辑并打开URL的物品。 配合自定义桌面作者可以制作一些外部链接。
- 进入世界， 初次使用自定义桌面时， 默认左上角的链接为bbs和WIKI网址.
-  增加命令: /torchcolor [r] [g] [b] 改变光源（火把）的颜色
                    /torchcolor 1.2 0.2 0.2

2014.3.17
- 所有Command支持自定义Compiler
- /t 指令会延迟Command的编译。
- 增加命令: /set -p name [=] prompt_msg  可以提示用户输入文字。

     例如：
               /set -p password=请输入密码:
               /t ~1 /tip 你输入的密码是%password%

- 增加命令: /pause  暂停当前人物或命令方块的所有/t指令的执行
- 增加命令: /resume  继续当前人物或命令方块的所有/t指令的执行
- 增加命令: /advancetime [~][time] 快进当前人物或命令方块的时间。 无参数表示快进到下一个关键帧。 ～表示相对时间否则是绝对时间。
- 修复ParaCraft无法保存模板的Bug.
- 增加命令: /if var1==var2 /othercommand   当var1==var2 时，运行后面的指令。

     例如：
               /if %name% == 0 /tip your name is 0

2014.3.16
- 增加命令: /set [-p] [@playername] name [=] value_prompt_msg  例如：
                    /set a=hello world
                    /tip %a%
- 所有指令支持 %var%.
- 支持内部变量%name%

2014.3.15
- 完成论坛和语言的关系设计
- 增加命令:/mirror [-clone|-no_clone] [-update] [x|y|z] from_x from_y from_z (dx dy dz) to pivot_x pivot_y pivot_z

2014.3.14
- 创意空间BBS正式和玩家见面
- 增加命令:/info 可以切换Info窗口. 快捷键F3

2014.3.13
- 增加了X, Y, Z 轴的镜像复制功能，支持clone/no_clone 模式， 支持动态选择，动态改原点等功能
- 增加位置跳转的快捷键F2（切换）Ctrl+F2(添加)  Shift+Ctrl+F2全部删除 （和Visual C++的默认键位一致）
- 创意空间BBS上线了。 支持悬赏等功能。
- 增加了智能画板

2014.3.12
- 优化了代码和命令行窗口， 支持点击就编辑， 以及保存并退出的功能。
- 代码， 书，命令行窗口也可以拖动了。
- /tp 窗口支持对传送点命名了
-  选择时，加入了x,y,z的三维坐标显示。

2014.3.11
- 修复了Region Loading的Bug, 导致部分Custom模型被加载2次.
- 增加命令: /edititem [item_id]   未来会增加编辑Item属性的面板
- 命令方块的窗口可以拖动了
- 增加命令/tp和/goto  可以记录多个临时位置信息。 方便世界的编辑者记录多个位置并存盘。

2014.3.10
- 增加命令:/replacetexture from_id to_id_or_filename  动态替换积木材质， 可以为用户世界目录下的指定贴图。
- 从列表中去掉了材质转换方块。 只可以从命令行获得。
- 新增了BUD：含羞草石： 当周围6个方格改变时，会触发周围的命令方块以及自身， 注，周围的同类含羞草石无效。
 - /命令方块上次的数字形态输出的结果可以保留， 并作为中继器，红石导体等的输入（注意只能是指向性导体，不可以是红石线）。
- 临时方案：修复登陆器Crash的Bug
- 增加规则： /addrule Player AllowRunning false  是否可以跑步

2014.3.8-3.9
- 修复可移动积木上方为非Obstructionblock时无法移动的Bug。
- 建立了bbs.paraengine.com的discuz论坛
- 建立了BBS基本导航，SQL备份， 捐赠模块，分享模块，用户权限等内容
- 优化了twiki网站的权限， 去掉了一些链接， 防止Robots占用大量CPU.

2014.3.7
- 支持对选择区域在X,Y,Z轴放大缩小。方便大家制作一些大型建筑
- 含羞草在被移动的箱子或活塞删除时，会触发一次消息后消失。
- 花草类物品在被活塞或箱子压过后， 在非编辑模式下， 会产生物品。

2014.3.6
- 修复碰撞检测不准确的Bug：对含羞草的碰撞加入了DeltaTime预判， 可以检测到高速运动并反弹的物体
- 增强命令：/anim [@playername] anim_name_or_id[,anim_name_or_id ...] 加入了人物动作指令可以执行1个或多个动作 例如:
/anim sit
- 人物上次的动作/anim 可以保存了

2014.3.5
- 编辑模式下：Ctrl+右键可以直接激活命令方块
- 增加命令:  /activate [x y z]   可以激活自己或其它方块。 可以用命令方块写GameLoop了。
- 增强命令：/return number|Bool  可以返回Number了
-  增加了水和蜘蛛网等特殊方块的减速效果：可以通过BlockAttribute配置。
- 增强规则命令：/block block_id attr_name attr_value
               例如：/block 118 speedReduction 0.1   蜘蛛网减速90%
- 修复非创造模式下可以用Shift+右键等的Bug
-  重构了物品击碎事件的处理。每个Block可以自定义击碎后变成的物品
- 击碎命令方块，编辑模式下会变成含有命令的命令物品。可以用这种方式（借助命令方块的可视化工具）方便的制作命令Item物品

2014.3.4
- /t指令在无参数时可以清除目标的所有时间事件。
- Entity仿真加入了AlwaysSentient机制, 在人物很远的地方，依然可以运行FrameMove
- 重构了人物仿真的FrameMove机制。
- /clone -update 支持了update参数， 在Clone的过程中会更新仿真如电路逻辑会激活。
- 增加命令 /loadregion [x y z] [radius] 强制加载所在位置坐标的地形(512*512)范围的东西。
- 压力板， 含羞草都可以有记忆学习功能了
- 增加了物品耐久度的概念， 使用物品会损失耐久度， 直到破损
- 增加命令: /durability [value] 设置目前手中装备的耐久度
-  一些行为：如推箱子，如果使用藤蔓等， 会相应物品的损失耐久度。目前物品默认是无耐久度的。
- 增加命令:  /testblock x y z [(dx dy dz)] blockid [data]  用来判断目标或一个区域是否为指定方块。是的化返回true.
-  增加命令:  /compareblocks ~ ~-1 ~ (2 2 2) to ~5 ~ ~ 比较2个矩形区域中的方块是否完全一样。 是的化返回true.
- 命令方块背包的true/false条件反转了一下（旧逻辑是兼容的）方便理解
- Fix: shift+TAB/TAB 建的传送功能
- Help Refined flappybird game

2014.3.3
- 背包中的红石火把后面的方块代表反向逻辑， 即后面的方块不存在时才向后执行
- Ctrl+左键可以复制背包中的物品
- 名字或内容不同的物品无法合并
- 命令，书，代码物品变为可以堆叠了
- 增加命令: /fov [fieldofview:1.57] [animSpeed]  可以改变摄影机的FieldOfView（类似望远镜的效果）
-  增加指令功能： /tip [-name] 可以清除tip
- /lookat 指令会同时设置摄影机的方向
- 加入～键, 摄影机拉近的效果
- 修复了背包中物品顺序保存不正确的Bug
- 出生点物体可以保存背包中的物品了
- 增加命令: /music [filename|1~6]   播放指定ID的背景音乐或文件

2014.3.2
- 增加命令: /scaling [@playername] size 改变人物的大小
- 增加命令: /tickrate [@playername] rate 改变人物的更新刷新率，默认20. 30或60都OK
- 修复人物间碰撞导致Mob无法移动的Bug。
- 物体碰撞最大分离速度改为3m/s
- 修复含羞草中无法使用时间命令的Bug
-  箱子掉下来，会落在人的头上
- 推动箱子，人物优先排挤到侧面
- 活塞会优先水平方向推动人物，然后是垂直方向
- /text 命令没有参数时是消除字幕
- 增加命令: /loadworld [worldname|url|filepath]  可以在世界中切换世界（可以由多个世界构成一个大世界观）
- 当给人物手中的物品命名后Tooltip自动刷新， 当给命令书内容改变时，也会自动刷新。
- 修复/t 指令后有部分命令无法执行

2014.3.1

- Shift+F3 查看UI信息
- 修复pe_mc_slot中鼠标点击到没有显示的Slot的BUG
- 重力命令可以指定某个角色了 /gravity [@playername] [value|9.81]
- Fix: ParaCraft鼠标Icon加入预加载中
- Fix: 点击文本输入框无法获取输入焦点
- 登录UI整理：合并多人/单人

2014.2.28
- 物品编辑框中， Shift+点击物品会转移物品， 而不是丢弃物品
- 修复动物无法在透明类方块上行走的Bug
- 更新了WIKI中的个人页面，加入了一些不错的外网世界到推荐列表中
- 哈奇2中多人访问时人物大小问题解决了
- 增加命令 /facing [@playername] angle 可以设置人物方向
- 增加命令 /lookat [@playername] [x y z] 让当前人物看某个人物或方向（第一人称比较有效）
- /clone命令中的dx,dy,dz可以为负数了
- F3的InfoWindow 加入了相对位置的说明， 并且可以相对当前选中的块，或Player或正在编辑的物体
- F3的InfoWindow 当编辑模式下选多个块时， 会显示矩形区域的AABB。方便如/clone /setblock指令批量修改

2014.2.27
- 增加命令 /move [@playername] [x y z] 可以移动指定人物到指定位置
- 增加命令 /velocity [add|set] [@playername] x [y] [z] 增加|设置动物或人物的速度
- 增加命令 /speeddecay [@playername] [surface_decay] [air_decay] 设置动物或角色在地面和空气中的摩擦力
- 材质包支持将单面材质替换为3面材质, 命名[id]_[name]_three.png 即可
- 登录模式下进入下载的世界为默认进入当前用户的个人世界服务器
- 鼠标右键可以推动可移动的箱子，如果手里是藤蔓，则为拉动。 上方有积木时不可移动。
- 支持默认速度： /velocity set @test 1,~,~
- 修复ItemCommandLine无法多行的Bug
- CommandLine支持 -- 作为注释
- 动物不会自己掉下悬崖
- 修复命令方块复制粘贴命令丢失的Bug
- 哈奇中加入了世界列表

2014.2.26
- 增加了BlockDynamic,常规的Block可以有物理仿真了
- 动物可以被人物推动了，增加了AABB物理检测
- 加固木箱改为了可推动的箱子id:83（下面的方块敲掉会自由落体掉下来）

2014.2.25
- 水中总是可以跳跃
- /addrule Player CanJumpInWater false  增加是否在水中可以跳跃
- 加入了出生点编辑模式， 可以在进入世界后执行代码。
- 可以设置人物是否可以自主运动
- 去掉了游戏模式下左键行走的功能

2014.2.24
- 改变了默认鼠标的图标（第一人称）
- 修复了人物DeltaTime的Bug.
- 可以给人物起名字，并且/tp @[人物名字] 等指令生效
- Fix 新建世界后，加载世界目录不更新

2014.2.23
- 摄影机离很近墙壁会抖动的Bug解决了
- 动物无法走过关闭的活板门
- 增加命令 /loadtemplate [x y z] templatename   可以做动画了
- 所有命令和代码物品，游戏模式下可以通过右键来执行。玩家可以制作自己的创作工具箱了
- 增加命令 /t seconds  [/其他命令]  在seconds秒后执行后面的命令（可以做动画，支持相对时间）

2014.2.22
- 修复第一人称的飞行模式Bug
- 背包物品操作优化： Shift+左键清空（无目标时）， 左键点击拿起全部物品， 右键点击拿起一半物品。
- Entity XML存盘格式更加精简
- 书，命令行， 代码的Tooltip会显示第一行文字。
- 新增命令/name [name#tooltip1#tooltip2] 给手中的物品起名字（例如书本）。
- 方块相关的位移，粘贴，消除等操作支持EntityData（例如告示牌等也可以批量复制粘贴了）
- 修复儿童版实数地表无法变成积木地表的Bug

2014.2.21
- 人物脚在水中速度减为0.4，头在水中则为0.8
- 人物默认密度为1.2, 这样人物在水中会自动下降
- 增加命令 /density  1.2  设置人物的密度（决定在水中是否下沉）
2014.2.20
- 物品复制， 模板，创建，删除(Undo/Redo):支持对物品内部数据的保存（例如命令方块或告示牌的文字）
- 增加命令/addrule Player CanJump false  是否可以跳跃
- 增加命令/addrule Player CanJumpInAir false 是否可以连跳（在空中跳跃）
- 增加命令/addrule Player PickingDist 3 鼠标点击范围(默认是6)
- 增加命令/addrule Player JumpUpSpeed 2 鼠标点击范围(默认是6.5)
- 命令方块增加中红石块相当于Logical OR.
- 增加命令/mode [game|editor]  锁定游戏模式，无法用G切换.
- 增加命令/gravity [value|9.18] 设置重力加速度
- 增加命令/speedscale [value|1] 设置人物运动相对速度。1是默认速度
- 增加命令/viewbobbing [true|false] 摄影机摇摆
- 增加命令/addrule CanPlace from_id  to1,to2,...  可以设置1对多的放置规则
- 增加命令/clone from_x from_y from_z (dx dy dz) to to_x to_y to_z (dx dy dz) [where sameblock]

2014.2.19
- 增加命令 /goto [@playername] [x y z] :支持相对或绝对位置
- 修复了火把和导体的一个状态更新Bug
2014.2.18
- 含羞草的厚度改为0.1m, 采用精确物理
- F3加入了窗口模式
- 游戏模式下到地下会触发死亡Dialog
- 增加红石开关（类似红石火把）：可以方便的向上传递电流，并且可以被活塞推动

2014.2.17
- 命令方块支持前置条件: 例如获得XX个YY后,才触发ZZ.
- 增加命令/return true 返回true的指令
- 增加命令/clearbag [@playername] [itemid] [count] 可以从背包中清除全部或指定的方块
- 增加命令/give [@playername] [block] [count] [serverdata] 可以向背包中添加指定的方块
- 增加了方块触发器(含羞草)：可以用作6个方向的人物碰撞感知器

2014.2.16
- 修复在墙角，摄影机和鼠标无法操作的Bug。
- 摄影机摇摆可存盘了
- 统一采用60FPS摄影机了，高速的机器运行会更加流畅。
-  取消了人物数量5个的上限。
- FPS模式以及非创造模式， 人物只能够到6格以内的方块。
- 修复第一人称下鼠标乱跳的Bug。

2014.2.15
- /addrule Block CanDestroy Lever 1 规则命令：游戏模式X方块可重复回收利用
- 第一人称模式摄影机速度改变了
- 重写了摄影机头部震动的代码，更加真实了

2014.2.14
- 修复背包物品有时显示Icon消失的BUg
- 创意百科帮助只在2级前提示
- 增加了ItemCode脚本物品（Scoping和积木编程是一样的）
- 增加了ItemCommandLine命令行物品
- 脚本和命令行可以放入命令方块中了。

2014.1.24
- 联网模式：增加玩家URL输入
- 解决ESC键有时失效的问题
- 书方块在背包中不可堆叠
- 修复箱子和楼梯透光问题
- 优化在狭小房间中的摄影机
- 加入了随机皮肤
- 多人只读世界访问模式： 用户头顶名字和皮肤的显示，采用了新的CCS架构

2014.1.25
- ParaEngineGit项目更新到GitHub/ParaEngine
- 建立了可行的C++远程工作环境
- 增加了可以独立编译的SDK sample:HelloWorldPlugin
- 修复ZIP世界无法读取Entity信息的Bug
- 修复世界路径有特殊‘字符的Bug
- 修复SQLLITE DB退出Crash的Bug
- 不移动时， 人物从梯子上自动下来：
- Fix：当铁门关闭时， 如果人物在铁门里面，人物不会被传送到上方。
- Fix：人物的头卡住的Bug

2014.2.11
- 修复无法关闭Chest的Bug。

2014.2.12
- 加入了材质替换方块
- 修复第一人称操作，切换窗口时，鼠标错位的Bug

2014.2.13
- /where 命令会将坐标复制到裁剪版中
- 增加指令：/setblock ~x ~y ~z [block] [data]
- 增加指令：/give [block]
- 第一人称操作优化：例如打开宝箱后，无法用鼠标
- 选择方块时可以切换飞行模式了

2014.1.28
- 修复Slab上无法放Slab的Bug
- 修复墙角漏光的Bug
- 增加了半层高的Slab物理，以及人物可以自动走上去。（非主角Entity暂时不行）
- 修复摄影机与非CubeBlock（例如玻璃，Slab） 的碰撞不平滑的Bug

2014.1.29
- 加入了命令/text 和 /tip
- 加入了/addrule  /rule 等规则相关的命令
- 加入了/dostring 命令
- Shift Tab/Tab可以在编辑和选择积木时使用了
- 编辑时可以使用鼠标中间了

2014.2.2
- 修复半透明方块的透光问题。
- 多人创造与私服架构设计

2014.2.3-2014.2.5
- upgraded NPL language service and debugger from vs 2010 to vs 2013
- open sourced NPL mini-tools on github. Source tree is used for Git version control.
- 红石块会发光

2014.2.6-2014.2.7
- 重构BlockWorldProvider和光照部分，C++支持多线程和私服

2014.2.10
- 可以保存光照信息到世界Region文件了。 （数据还需要优化和压缩）

2014.1.27
- 增加了无法自动攀爬的属性命令
- 书籍阅读时，可以右键打开宝箱等
- 引入规则文件rule.lua
- 加入了墙角草（相当于隐形梯子）
- 命令方块上如果有神经元编程，会响应红石信号
- 加入了LilyPad，可以放水上
- 人可以行走在LilyPad上（可以作为0厚度的物理方块使用）
- 加入了RuleBlock: 玩家可以编辑例如只允许拉杆放到萤石块上

2014.1.26
- 修复活塞更新Bug

2014.1.23
- TNT会触发其他TNT 并有5 Tick延迟
- 手持插件点调整并可以配置
- ESC菜单加入了打开世界路径的功能
- 材质包中贴图替换逻辑采用同名都替换逻辑
- 加入了人物皮肤管理PlayerSkin类, 可以通过属性面板切换皮肤
- 修复了禁止他人保存模板的功能

2014.1.22
- 加入了/install url 命令， 可以通过命令行安装材质包了
- 远程世界积木消失的问题解决了。
- TNT炸弹逻辑完成
- 书的编辑UI完成
- 加入了南瓜灯：暂时没有方向
- 解决了自动保存世界的Bug

2014.1.21
- 只有修改的region才会保存， 只有没有保存的Region才会Unload. 修复Importer的Bug。
- 修复没有保存，却自动保存的Bug。
- Item Classes 全部预加载。
- Snipper变成了物品， 去掉了模型，支持Q键丢弃。
- Item 系统加入了RightClick功能
- 加入了相册功能：支持HTTP贴图，内部贴图和相对世界的路径
- 加入了Book：可以作为GUI Window

2014.1.20
- 修复KidsESC键， 背包UI，
- 游戏模式允许创建并消耗方块
- Item.count==0 视为不存在。创造模式不消耗物品
- 游戏模式下放置物品会消耗掉物品。
- /replace [-all] [from_id] [to_id] [radius]: 批量替换块

2014.1.19
- 增加了flatXX地形生成器： 儿童版的积木世界默认flat64作为生产器

2014.1.18
- 修复水里无法放方块的Bug
- 修复了最上Chunk不现实的Bug

2014.1.17
- 当箱子上方为空或水时才能打开箱子。
- 互联网模式开启， 和WIKI页面同步.
- 发布了ParaCraftV0.1: cc.paraengine.com

2014.1.16
- 所有哈奇相关的UI和功能已经与目前UI融合完毕
- 哈奇版开放了任务，新建世界默认为积木世界。
- GSL支持MC版本的人物形象

2014.1.15
- 上传，下载世界跑通，世界读取Wiki内容

2014.1.14
- QQ 登录,重写了UserLoginProcess以及相关登录UI

2014.1.13
- ParaCraft launcher页面制作完毕， WIKI登录页功能实现
- 完成QQ号外部登录
- 修复了建造任务中提示过慢的Bug
- 完成了34个新年+红石任务

2014.1.11
- 积木和人物选择操作优化
- 积木增加了6个方向的拉伸，并使用了最新的皮肤
-  alt+shift + 右键为批量替换。 去掉了Ctrl+右键（防止误操作）
- 积木多选UI优化， 以及NeuronUI, Goal UI 等的UI替换
- 点击场景也关闭对话框

2014.1.10
- 修复了SetBlock底层Bug， 导线附近中继器失效的问题解决了
- 中继器可以被侧面的对其强冲能的块锁住。
- 增加了飞行速度
- CC官网加入了dashboard
- 物品编辑UI加入了提示并隐藏了不用的版面
- 所有Entity人物，鼠标放上去会高亮显示
- 加入了左键对话， 右键编辑的逻辑

2014.1.9
    -  修复了BuildingTask不连续的Error
- 加入了Chest声音
- E键UI切换世界Bug 优化
- 积木逻辑： 唱片机
- TWIKI网站全面升级到6.0. cc和ParaEngine网站放到阿里云中了

2014.1.6-1.8
    - Entity mcml渲染底层
    - 宝箱： UI + 逻辑 + 数据存储
    - 楼梯加入了新的子模型， 改变了楼梯的缺省创建模式。
    - 修复了楼梯等模型UpdateModel后UserData没有存入模板。
    - 增加了人物71号动画：Create和Break

2014.1.3
- 人物背包： 可以丢弃和拾取物品 (采用了新的物品API和UI底层)
- 主角的形象可以保存了. /skin filename
- 人物手中拿着物品（插件点）

2014.1.2
- 32*32的物品 只要 32×4+2=130个面即可， 还可以LOD

- 构建物品系统的新UI底层(拖动，丢弃等): Slot, ContainerView, pe_mc_blocks. 所有操作通过ItemStack完成， 质量守恒。

2014.1.1
- Entity 加入了物理碰撞
- 修复了一个光照加载Bug

2013.12.31
- Q键扔东西

2013.12.30
- 世界保存时的默认路径中去掉世界的名字。
- 加入直接只读属性. *.db 采用全局名字
- 所有的主角背包采用新的API。
- 物品系统底层逻辑:InventoryPlayer

2013.12.28-2013.12.29
- 大量重构： 所有模型的鼠标点选和AABB都采用了真实模型信息而不是方块。 例如火把， 红石线等。
- 右键无法在已经存在的块上创造。

2013.12.27
- 在阿里云上建立了WIKI网站：cc.paraengine.com 并创建了2个编辑账户
- EntityItem支持动画并加入了3种类型模型的渲染。

2013.12.26
- 加入了2D UI以及场景中的3D图片的非Linear渲染模式
- EntityItem支持了3D和2D的渲染
- 物品系统底层逻辑:ItemStack
- 修复了在UI拉伸时的头顶文字出错的Bug

2013.12.25
- ClickToContinue 更加流畅
- 修复了切换世界Crash的Bug
- 加入了3D场景中的物品对象

2013.12.24
- 支持HTTP远程贴图

2013.12.23
- 修复进入世界默认位置Bug
- 修复玻璃窗贴图和告示牌模型
- 加入了物品展示框，任意图片UI可以作为3D模型显示了
- Block region cache 增加到16. 修复积木无法显示的Bug。 (发了DLL外网补丁)
- 研究了大厅服务器Plugin

2013.12.20-2013.12.22
- Entity的数据保存在了Region.xml文件中，并且是随Region动态加载的
- 针对红石优化了创建任务， 增加了几种创造属性
- 可以渲染3D UI了. 增加了告示牌
- Builder可以排序方块
- MultiLineEditBox支持默认文字
- 加入了GUI目录：Entity编辑UI占位符
- 告示牌与GUI联通： 可以编辑告示牌了
- 加入了命令方块

今天计划：
- 制作第一人称右手模型人物（一个只有手的主角）
- 人物与编辑UI： NPC对话
本周计划：
- 物品系统: NPC对话UI，合成台，NPC商店
- 现有UI梳理： Player背包，加载世界， 设置等
- 多人创作： 私服的共同创造和访问（通过IP地址）
- 块增加：画板，火苗，种子 等等
- 积木逻辑： 音符方块，比较器。

大家一起思考的问题:
- Sandbox要超越MC： 要在逻辑的方便性和可能性上超越：思考物品， Neuron, 与红石的结

核心的困难问题：合体
- 如何保存世界的多了版本， 而不被联网世界所破坏

未来激活的计划：
- 保存光照信息到世界.tmp目录
- 尽在出生点附近保存光照信息

暂时搁置计划：
- GitHub 远程开发环境构建
- 回复儿童版创意空间的右键模式
- 特殊的积木渲染读X文件
- 制作BlockCharacter：可以动态高速的渲染积木。并且支持mini-scene画中画， 未来加入骨骼。
- 反射Normal的Bug
- 初始世界加载时间长一点， 将周围的世界也加载进来，给一个加载动画。

- Entity仿真架构与API （策划/程序员可批量扩展）
- 光影水反2期 ：（泛光 & God Rays）
- 光影水反3期 ：（材质优化与HDR 效果，反射法线， Motion Blur等）
- 点击距离5格以内
- 动物的运动要有物理
- 刷地形的工具
- 加工具栏：笔刷, 地形，镜像， 植被等

-  MC Multi-User
- Client as Block Server without the saving button.

- NPL API:
基于骨骼的自定义模型人物
水下移动功能 s键触发 u上升 j下降
2.  增加平行光源块， 在大的室内， 方便照明竖线上所有的块。