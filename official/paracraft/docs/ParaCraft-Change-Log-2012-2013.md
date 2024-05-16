[ParaCraft Change Log 2012-2013]

[Editor Mode Only]:
1. Mini Map (Using Block world Heightmap, dynamic texture is fine)
2. Block Location Display + Checkpoint + /teleport command
[General]:
3. If teleport stone is adjacent to a light block, when the user steps on the teleport stone, it will automatically go to the next teleport stone in the direction of the character facing. 
4. water block light refresh is not perfect. Dynamically removing water block is buggy 
      1. Optimize block position struct 
      2. Height map change 
5. MC wiki site


- 家族Flag  (Done)
- MC Rendering under 英特尔 G33/G31 Express Chipset Family  and 945GM （Done）
- Image to 3D Model （Done）
- /makeasset 功能 (Done)
- Cache目录怎么删 （Done）
- Terrain Hole删不掉 (Done)
- 水面的人物动作（Ignored）
- 大世界运动不卡(Done)
- 栅栏的问题(Done)
- 选择好了材质包 怎么没出现在积木那一栏？ （Done）
- [ItemManager] (done)
- 选择Block (Ctrl+Z) (done)
- 第一视角摄像机能够引入创意空间么？ （Done）
- 材质包替换 外网是错误的（done）
- 实数水的渐变（BlockWorld中）（done）
- 加入了很多命令行,请看F1帮助(Done)
- Mod和材质替换Bug修复
- 鲜花榜Fix(Done)
- 增加世界另存为的功能（一个世界的多个存档）(done)
- MiniMap(Done)
- Ctrl+F12 隐藏UI （Done）
- 中键可以瞬移了（Done）
- 生成小地图后地图会维持上次的放缩状态（Done）
- 修复了下降100米后会死机的Bug（Done）
- 可以直接在Mod自定义材质包中将物品创造出来了（Done）
- 修复了/tp指令末尾有空格的Bug（Done）
- 增加了全新的任务目标捡金币（Done）
- 转动视角，新版鼠标右击转动视角，有时候手抽了，会出现积木： 提供新的物品类型（如抢之类的）（Done）
- TPS game (done)
- 下载其他人的世界没有Loading条。 （partly Done）
2013.8.8: 
- 出生点(Done)
- 选择方块后增加了复制与粘贴 Select Blocks: Ctrl+C,Ctrl+V (Done)
2013.8.15: 
- 所有进入创意空间的人都不骑坐骑了(Done)
- 旧版创意空间也可以离线进入（不要发布）(Done)
- 进入其他人的创意空间默认为游戏模式， 而不是编辑模式。(Done)
- 可以用来 播放声音， 字母， 传送， 等等功能。(Done)
2013.8.16
- 创意空间中可以点击其他玩家并与之交流了。 (Done)
- 怪物加入了掉血的动画
- 狙击枪可以向任意位置射击并有震动效果。
- 怪物可以被击杀，并且获得金币
- 加入Show/Hide指令
- 可以输入米米号进入空间了
- 增加了积木沙盒编程环境：Command Block inside sandbox environment
- 方块增加远处雾化效果
- 白天，夜晚自动变化雾的颜色，
- 可以设置每天的时间长度 一天20分钟。命令行/day mins  
- 没有设置出生点时， 会从上次存档点出生
- 积木可以用脚本语言编程了. 引入和沙盒编程模式
- 第一批积木API(包括创建，删除方块，播放声音，字幕)
- 增加时间函数/time

2013.8.30
- 增加全积木初始模板
- 修复了部分积木模型在夜晚的光照
- 调整了积木排序和名称。 即将取消和新增一批积木。 
- 夜晚灯光颜色可调

2013.9.8
- 夜晚的积木光照更柔和了
- 修复了积木光照有时发黑的Bug
- 人物的头会自动旋转
- 重力加速度增加了一些。 
- 人物的光照会更加场景坏境变化。 

2013.9.15
- 可以改变积木光照颜色
- 双击空格可飞行，飞行时速度为平时1.6倍
- 修复了光照Bug
- 增加了人物走动的摇摆

2013.9.26
- 增加动态改积木光照的命令行和API
- 每个积木可以存储1个16位的额外字段。 解决火把等可以放在任意一个面上，位置不会乱动。


2013.9.27
- publish List中加入新资源 (Done)
- 楼梯， 火把，地铁， 梯子，窗， 按钮， 按钮2 增加面属性以及存盘功能 （Done）
- 增加梯子的Corner （Done）
- 增加围墙， 楼梯 (Done)

2013.9.28
- 2个积木组成的门和天窗的实现(done)
- 双击并按住W键可加速奔跑，摄影机视角变大。 (done)
- 角色运动和减速有加速度和减速度。 (done)
- 增加OnNeighbour Change: 门和围墙 (done)
- 所有积木模型像素画。 (done)
- 玻璃， 冰块增加击碎声音

2013.9.29
- 用线框代表选择的积木（Done) 
- 搭建积木的测试环境(Done)
- 替换建星做好的blockworld/目录下可用的所有模型积木
- 用线框代表选择的积木： 

2013.9.30
- 新增了2个材质的梯子积木，并且允许使用倒过来的梯子
- 跑动中停止下来，转头有一个平滑效果了
- 编辑地形， 多块选择等，采用了线框代表鼠标当前的选择。 
- 编辑人物时，可使用线框效果。 
- 可以通过点击面的上部和下部来决定梯子是正放，还是倒着放。

2013.10.1
- 十字片， 薄板的模型。 

2013.10.3
- 增加了对任意形状的方块告诉渲染接口
- 增加了草等5种植物
- 增加了随机偏移位置和放大的植物模型

2013.10.5
- 增加了物品分类ID用于渲染和仿真
- 增加了会随风动的植物
- 增加了会随风动的水块

2013.10.6 - 2013.10.9
- reconstructing world position from view space depth value is fully implemented.
- fixed render several render bugs in block engine when device is lost or leaving the scene.

- Effect object now support SetParam to set a number of camera matrix in scripting interface
- Multiple render target framework is working now
- Block Engine now support fancy graphic mode which uses deferred shading.
- shadow map is refactored and can be accessed from the scripting interface.
- block can cast shadows
- fancy block effects HLSL is added to composite.fx and mrt_blocks.fx.

- block category id added.
- render task sorting is added for category id, so that similar id are rendered next to each other.
- multiple render target shader added for block engine.
- fixing a bug for chunk distance render order.

2013.10.9
- 高级MRT & deferred shading 渲染流水线完成
- 增加了真实积木太阳光阴影渲染

2013.10.10
- 增加了shader 2,  shadow, reflection 指令用来控制高级的渲染。 

2013.10.11
- 光影水反1期 ：所有物体的真实阴影与自阴影渲染
- 所有模型引入法线，阴影渲染使用法线

2013.10.12-2013.10.13
- 光影水反2期 ：（水的反射）

2013.10.14
- 新版UI 皮肤
- 新版UI （登录)

2013.10.15
- 水的反射加入了Bump mapping. 
- shadow pass improved performance

2013.10.16
- ParaServer立项讨论
- 完成创造UI 1期 （UI布局）
- 3D人物面向鼠标位置

2013.10.17
- 物品Icon的拖动类库. pe:mc_block pe:mc_player 类库
- 完成创造UI  2期 （人物背包部分，拖拽与存盘）
- 血条与当前选择UI

2013.10.18-2013.10.20
- 新版UI （主界面）
- 新版UI （选择世界）

2013.10.21
- A、D键应该是左右移动   （ Done）
- 选择新块加入背包的时候，优先的是自己手上的块，这逻辑很难理解 （ Done）
- Shirt+右键建出来的块数量太多了 （ Done 改为 3个了）
- 登录和选择世界禁用了全部不能用的按钮（所有可见功能都可以用了）
- 修复选中效果不更新的 Bug (Done)
- AA 效果和特效的冲突问题解决，强制取消AA
-  Shift+右键：使用手中的块， 而不是接触的块。 

2013.10.22
- 摄影机锁定距离滚轮可以切换块。 （insert/delete或Ctrl+滚轮）可以改摄影机距离
- 击碎效果（多张序列帧）
2013.10.23
- 每次关闭E键， 我刚刚加了一次全局的内存垃圾回收。
- 所有的积木配置和分类都从XML中读取
- 加入了若干人物类型
- 人物的粒子贴图渲染
- 放置水块会流动

2013.10.24
- MC 安装包 Launcher (Done)
- 新建世界支持中文名字
- 加入爱拍的电影拍摄功能Demo按钮
- 背包UI优化
- Shader 2的光照范围
- 登录世界的背景图

2013.10.26
- Bug Fix: Left/Right 按钮恢复了
- E键强制为背包 而不是恢复桌面
- 哈奇版的中键逻辑恢复了
- 模板功能加入了哈奇的创作模式
- 创作模式下取消了背包, 可以异步操作，并且点击方块自动放入手中， 生存与游戏模式逻辑不变。
- 增加了高品质下的UI自动放缩
- 画面效果中可以设置摄影机摇摆，UI放缩，锁定鼠标滚轮
- 增加了ESC键和系统设置
- 水块的流动逻辑优化了， 更容易填平水面
- 空手，然后Ctrl+右键水块， 可以批量消除水块

2013.10.27
- 所有特效文件预先编译。 光影水泛可以在各种机器上运行了。（笔记本电脑也OK了） 

2013.10.28
- Bug Fix：出生点踩上去的时候自动被破坏掉
- 修复了狙击抢模式下无法使用E键， 以及选择块失效的Bug
- 进入游戏模式后， 自动取消飞行
- 修复加载世界多次， 物品栏物品重复的Bug

2013.10.30
- 飞行模式落地后会自动变为行走模式
- 修复某些时刻飞行速度很慢的Bug
 - Z键可以快速的返回上一步操作（Done）
 - Q键可以切换上一个使用的方块（Done）

2013.10.31 
- Fixed 首次跳跃， 人物可能消失的Bug
- Y方向的第三人称摄影机瞬移加入了平滑. 当超过1.2格时平滑摄影机（效果不是很理想， 暂时禁用了）
- 优化和世界加载时的光照渲染，提高了光照计算速度。
- 摄影机与物理碰撞时的距离放缩加入了自动加速功能
- 默认建议开启特效
- 摄像机的缩放与太阳有关，当有太阳时，摄像机前面被方块阻挡后会自动透明方块

2013.11.1-2013.11.3
-  完成随机初始地形基本算法
-  积木地形文件优化, 压缩率提高4倍, 兼容所有旧版本. 
-  积木类型整理block_types.xml 加入了程序名称和mc_id

2013.11.4   
   - 方块饱和度颜色的修正 （全部使用32bits贴图）
- 叶子的mipmapping ==1, 其他是4
- 修复了双面材质光照Bug
- 修复水块的渲染：当上方为积木时会正确渲染。 
- 随机地形Profiler后优化 性能提高50%

2013.11.5
- 整理了mc_id, 修复了一批贴图问题
- 更新了MCImporter， 支持meta data的导出， 以及修复叶子导出问题。 
- MC 3期计划的PPT
-  新手指引相关工具和UI设计（Review ）
- 建立了GitHub的ParaCraft项目，并分配了权限

2013.11.6 
- 随机地形加入了timestamp用来记录哪些区域被生成或修改了
- 加入了半格高的slab类型，同ID，不用data和模型的显示与存储。
- 加入了甘蔗模型reed,  id=161
- 新教程的初始世界模板v0.1

2013.11.7 
- 楼梯和台阶在创建时会根据摄影机的位置自动变向
- 增加了block_types_template, 简化了block_types.xml的书写。 
- 优化了默认模式下的太阳光的渲染。
- 讨论了农场类的经济：加入淡水资源，作为每天的精力值（例如50滴水）.
- 模型类的积木很远会消失的Bug解决了

2013.11.8
- 所有的模型支持可置换贴图
- 加入了Vine 
- 添加水滴Block（农场用） 
- 修复窗， 房顶，火把等材质问题。
- 加入了小麦的4种状态

2013.11.9
- 加入了仙人掌cactus模型
- 加入了"seed_plant" template： 种子阶段是地上的一个面而不是Cross。 
- 加入了没有物理的梯子：梯子和藤蔓都可以爬上去
- 逻辑更改：栅栏不可攀爬了, 只有梯子可以。 
- 爬梯子时， 会自动锁定在梯子上， 不会容易掉下午
- GitHub已经包年付费

2013.11.11
- 切换到LuaJit2, Linux/Win32编译了LuaJit2. 性能提升3倍， 随机地形算法提升20倍。 
- 修复大量Escape Character造成的版本不兼容
- 内网Client/Server全部升级到LuaJit 包括CI（PublishList）

2013.11.12
- 优化Set/GetBlock函数。 性能提高3X
- 性能优化: chunk, blocks,
- 主角用PNG可置换贴图。 

2013.11.13     
-  性能优化:  m_lightBlockIndices. /PROFILE 性能分析
-  Fix: 右侧iFrame应该无法点击，否则会误操作删除。

2013.11.14-2013.11.17
-  径琦：农场玩法UI设计
-  径琦：农场玩法数值Excel
-  阿水：核心创造玩法UI设计（新手， 主角， 建造类任务）
-  建造类任务系统Demo
-  建星：添加所有种类的楼梯， Slab， 墙壁，栅栏，铁轨， 玻璃 等 （程序100%, 美术50%）
-  贴图： 红色，绿色， 白色的类似窗棱的贴图， 用于任务指引 
-  luajit2 导致外网哈1，哈2都要发新的PKG完整包， 之前所有PKG作废。Server端由于1GB的64Bits的原因， 还是采用原版Lua
- NPL Compiler will not report syntax error count. All syntax errors of main_full.pkg is now removed. 
- taole's engine optimization. 

2013.11.18
- 加入了反向选择的SelectionGroup 
- fixed slab model incorrect face removal
- 调整建造任务体验
- 恢复VMServer ： MySQL

2013.11.19
- 联通多Step创造模式。 
- 建造系统的BOM文件格式的自动生成。 多元点对齐。(放弃：暂时不做了，只用一个Step)。 

2013.11.20
- 本机服务器模拟API：登录, EXP, 资源，物品，统计等系统的API模拟接口
- 创建世界：随机初始地形 完成，修复光照， 以及跟随玩家自动生成 (但是性能还是不佳)
- 修复一些积木的显示
- 1级UI美术优化

2013.11.21
- 完整的任务系统UI，1级UI
- 初始地形性能优化

2013.11.22-2013.11.24
- 大量的随机地形算法优化。以及Block引擎优化。 引入FFI，性能提升20x.
- 人物出生时，出现在地表上. 增加GetFirstBlock方法. 
- FillLine复制接触的块(id)和块的方向（data）

2013.11.25
  - 修复了第二次进入世界， 会选择到自己人物的Bug
    - 模板文件名是中文了，支持积木方向
- 所有模型操作Copy， Paste， Transform都支持了积木方向
- 需允许在水或空气上开始建造任务
- 增加了建造获得进度的动画。 
- 合并积木文件（增加了几十个MC的材质块）

2013.11.26
- 完整的任务系统UI和配置联通可批量生产。新手指引UI.  增加任务Command: /quest [id]
- 增加各种反馈：成功创造，获得EXP
- 30个块获得5EXP， 消耗1点体力

2013.11.27
- 角色Camera上移一点 (DONE)
- 画面颜色饱和度临时提高下。 (DONE)
- FIX任务链(DONE)
- 物品获得用抛物线， 并增加+X  EXP。（Done）
- 不对的地方， 不允许放不正确的块。 自动消除块
- 将草类加入可允许建造的范围内，如果和块冲突自动删除
- 人物贴图命令行: /skin [filename]
     - 无绿色框时， 箭头提示最佳的块 （如果没有最佳块， 则自动出现在手中）。 
     - 建造提示去掉白色框，只保留绿色框（optional 看体验）

2013.11.28
-  TerrainFilterTask: 把地面铲平，强制海拔64米，并向下填充到没水为止，向上删除到看到天空为止
-  加入了NPCItem
-  世界根据世界名字为Seed
-  工具条会显示物品名称
-  创建任务会自动修正方向不对的块。 

2013.11.29
- 重新将产品定位成沙盒游戏sandbox游戏。 一切数值和逻辑还给Sandbox.  允许高自由度。 
- 仿真一期完成：每个Block可定义自己的类逻辑文件。 
          举例：半格高的Slab会自动变成1格高的Slab；
                    草上不可以再放草了， 也不可以悬空放置草了。
2013.11.30
- 加入了点击继续游戏。很少多开， 所以默认打开，避免玩家误点
- GameLogic部分代码重构
- F5切换摄影机：支持3种模式

2013.12.1
     -积木仿真逻辑架构完成
- 加入了水块的仿真

2013.12.2-2013.12.3
- 红石电路的渲染 ： 重构了积木渲染
- 红石开关 ： 重构了Block类

2013.12.4
- 教学任务相关优化： 新建世界， 自动忽略水等模块， UI指引优化，新手教程做了2个。
- 水块上放实心积木为替换。
- Alt+左键：迅速获得方块
- Shift+左键：逻辑改为消除同类块
- 存模板：恢复自动原点。 或/UsePlayerPivotY
- 右键和左键都可以触发开关
- 红石电路的仿真： 红石按钮，导线，开关，铁窗等

2013.12.5
- 创建任务完善加入了auto_create invert_create, offset_x,y,z等模式
- Fix 水无限下降的Bug
- 加入了响应红石电路的铁窗
- 长按左键会消除方块

2013.12.6-2013.12.8
- 红石电路： 中继器，红石火把
- 重构了BlockEngine API
- 火把亮度降为14
- Entity 接口优化： 
- 加入了红石铁门， 压力板， 红石灯

2013.12.9
- 积木逻辑： 活塞， 粘性活塞

2013.12.10
- 渲染引擎优化：内存占用减少， 加载过的区域，渲染速度大幅提升
- 修复F键无法飞行
- BuildTask支持offset_x属性
- 修复栅栏在建造模型中的Bug
- 加入了红石进阶教学， 加入了更多建筑教学

2013.12.11
- 加入了一直开的灯
- 加入了能量源红石块，并修复一个Wire渲染配置。 
- 重构了光照缓存系统： 当人物在一定范围内活动时， 保证画面绝对的流畅。 

2013.12.13-2013.12.14
- 重构了可视化区域缓存代码： 性能和内存占用大幅优化     
- 可以动态调整可视距离，并增加对应的command  /renderdist
- 修复光照Bug和导线渲染Bug

2013.12.15
- 重构了Entity接口: 加入碰撞检测。
- 所有人物都会被活塞推动， 或由于创建积木而移动到积木上方。 
- 所有人物都可以触发压力板等
- 传送石和Plant采用新的Block接口实现。
- MCImporter不再使用offset_y. 
- 动物移动时， 有基本的物理了。 自动爬高1格（栅栏除外）， 会向下掉落
- 栅栏会连接到周围的块上。 BlockFence and BlockStair added. 
- Cody在切换模式时自动消失。 

2013.12.16
- Block模型预加载: 开关， 中继器等 不会再闪一下了
- 增加了铁栅栏。 修复了玻璃的自动模型匹配
- 修复了红石中继器仿真优先级的Bug
- 修复了实数地表人物FallDown的Bug
- 修复了哈奇版中积木不显示的Bug
- 创造任务加入了快速完成按钮（只有SDK有效）
- 水不可销毁， 不可拾取
- 重构Item接口
- 修复出生点Bug， 可重复放置出生点. 

2013.12.17
- 动物加入了自动寻路， 可以触发开关等。 例如动物会优先走草地， 不走入有水的地方， 
          尽量避免爬坡，有时会掉下去。
- 动物的运动能加平滑了
- 重构派生关系：NPC >Mob >Movable>Entity
- 增加了走路的声音接口， 音量可调

2013.12.18
- glass 贴图改变。改了灯的贴图， 区别于红石灯。 

2013.12.19
- 实现了Block Entity接口
- 加入了吸水方块
