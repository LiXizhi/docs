[ParaCraft Change Log 2015]

2015.12.31
- desktop can use command to show a given builder tab, via show filters.
          /show desktop and  /show desktop.builder.env
- added command: /show desktop.builder.[static|movie|character|playerbag|gear|deco|tool|template|env]
- added command: /show movie.controller

2015.12.30
- new post added to personal website on github template
- submit my wiki theme to jekyll theme org. 
- fix attach to 3d API with empty object names does not show up.
- fix depth testing for GUI object attached to 3d object.
- /say command now supports -2d option.
- update command: /export [-silent] [filename] 
- added show/hide command filters

2015.12.27-2015.12.29
- Personal website framework made with github+jekyll. 
- Initial version automatic animation done in C++. 
- 新增命令: /avatar [@playername] [filename] 改变主角或人物的模型. such as 
          /avatar test.fbx
- 优化命令: /skin [@playername] [filename] 改变主角或人物的皮肤

2015.12.26
- update paracraft website framework to word press 4.4
- Right click actor icon to focus to its free camera position if it is editing bones. 
- fix auto camera biped states and fly mode speed direction when multiple walking keys are pressed.

2015.12.25
- /mode tutorial command added.
- Edit marker block is implemented in tutorial context
- fix a animation bug when changing biped asset file in async mode
- pe:slot support background2 and onclick_empty attribute
- click slot to create items via GUI and added filter integration points. 
- movie block can also create camera, NPC via GUI. 

2015.12.24
- removed shadow for fully transparent object.
- fixed biped animation speed and IK bone names for FBX files. 
- fix replaceable texture in FBX and default skin in movie block.
- if fbx and bmax model bone is named "L Hand" "R Foot" "Head", etc. these bone names are recognized. 

2015.12.22
- optimized world saving: real world terrain are no longer saved.
- attribute.db and npc.db are closed after world loading. 
- it is possible to delete current world, file watcher is disabled. 
- 新增命令:/mount  /unmount 让指定人物驾驶周围的可驾驶物品例如矿车。 

2015.12.20
- fixed a bug in NPL/HTTP protocol when url contains '('

2015.12.18
- ctrl+z/y is suppresed in editbox control to prevent it leaking to scripting interface. 
- /mode command is refined to work more robust. 
- fix rotation of blocks runtime error
- fix loading zip file twice when searching files from zip files.

2015.12.16-2015.12.17
- fix /walk to command target position
- ItemCode will catch runtime error in code. 

2015.12.15
- zip archive files are exposed via attribute interface. 
- zip file can has a base directory for ease of human packaging and use github clone zip file directly as plugin. 
- the plugin systems will automatically search zip file in Mod/ folder for main.lua. The Mod folder can be a sub folder, making it easier to download from github. 
- hudson CI for android APK generation is done: this includes filtering asset files, building dll with NDK, and final packaging. 

2015.12.12-2015.12.14
- Plugin loader optimized to support non-standard named zip file and folder in ./Mod directory. 

2015.12.11
- 修复旧版实数空间的各种兼容性问题
- create new CI for android deployment
- fixed NPLDebuggerPackage for visual studio having to press twice. 

2015.12.10
- /walk command and entity support -speed parameter. 

2015.12.6-2015.12.9
- ParaCraftSDK wiki updated. with new plugin tutorials.
- ./config.txt will overwrite existing command line parameters. 
- basic rebranding supported in ParacraftSDK. 
- 新增命令: /togglefly [@entityname] [on|off]  让物体可以飞行。 
- added entity simulation when fly mode is on. 

2015.12.5
- optimized select module page with better UI
- Plugin: STLExporter added, fully refactored and added to git. 
- fix initial value of ShapeAABB in NPL.
- fix same file dialog can not open non-existing file bug.

2015.12.4
- fix serialization bug when loading entity in motion.
- 发布推荐作品《Invisible Love》
- 发布推荐作品《永生的雪人》

2015.12.3
- fix a transformation bug in painter, causing transforms not updated. 
- multi-frame block renderer is supported on mobile client and can be turned on via GUI setting. 
- updated doc of NPL debugger to include vs redist
- cloudness can be adjusted from GUI. 云的多少决定影子的颜色和明暗面色差
- ExporterTask now supports plugins

2015.12.2
- fix a crashing bug with multi-frame renderer when used in opengl mode. 

2015.12.1
- fix z-fighting skybox and block rendering on mobile client. 
- fix z-fighting for multi-frame block rendering. 
- fix chat window in mobile edition
- added superrender to mobile edition
- Fix transparent texture rendering in fbx file. 

2015.11.30
- fix falling down when entity is in fly mode
- MultiFrameBlockWorldRenderer increased performance
- added command /superrender
- eye brightness and super render distance can now be changed via GUI in environment page. 
- fix fog rendering in block world

2015.11.27-2015.11.29
- multi-frame block world renderer for super large world (100%): supporting all render method
- block rendering helper classes are made thread-safe
- fixed GUI viewport size, allow rendering with unit space coordinate.
- finished English translation of a bmax tutorial (1 hour of manual subtitles)
- fixed /fog command which support any shader method.

2015.11.26
- multi-frame block world renderer for super large world (20%)

2015.11.24
- fixed sentient radius for entity

2015.11.23
- ParacraftSDK and website optimized to add visit count, some documentation, etc. 

2015.11.22
- fixed NPL url form upload for binary file format. Internally it will made a copy of the data for async calls.

2015.11.21
- added web stats and published paracraft full to cloud
- by default, full version is downloaded. Added credits to launcher.
- cloud auto sync folder set for baidu and one drive.  

2015.11.20
- fixing cursor not displayed when application first load.
- credits, terms of use and privacy policy page added in website and software
- "desktop_menu" filter added for plugins
- mcimporter released v1.0 on github
- fixed paracraft full version distribution file name case sensitive for plugin files. 

2015.11.19
- fix color_data attribute when inheriting data.
- added opacity attribute of block type.
- added spawn point to importer

2015.11.18
- NPL table serialization now support number key.
- NPL interface now supports synchronous call in addition to asynchronous NPL.activate.
- NPL importer/world generator examine added ParacraftSDK. MCImporter added. 
- 如果安装了第三方的mcimporter插件: added /mcimport command to import mc world directory. Please note, it does not import at once, instead it uses the ChunkGenerator interface to load the world dynamically according to current player position.

2015.11.17
- chunk generator interface are virtualized. Custom generators can be integrated more easily.  
- FlatChunkGenerator and NatureV1ChunkGenerator refactored from old source. 
- a github based personal website server is setup.
- ParacraftSDK is made English by default.
- update NPL debugger to visual studio gallery, added some screen shots.
- plugin init is called as soon as user selected login mode. 

2015.11.16
- main player asset and skin is now read from block_types.xml file. 

2015.11.14-2015.11.15
- NPL debugger for visual studio 2015 is supported in addition to vs 2013.

2015.11.13
- 新增命令: function, functionend, callfunction 允许用命令行定义函数或事件了.  
- 帮助模版增加programming分类和SendEntityEvent

2015.11.12
- fixed /say -duration 10 hello

2015.11.11
- Back from PAX, write several diaries. 发布新闻《Paracraft 归来》
- upgrade NPL language service to vs 2015.

2015.10.28-2015.11.10
- 我们去PAX Australia了

2015.10.27
- BMAX教学视频Part1 (46分钟) by Qizai

2015.10.25-2015.10.26
- Fix Block Sign description packet
- Fix chat system in paracraft
- 发布推荐作品《TheClown》
- 发布推荐作品《ToMars》
- 发布新闻《PAX 2015》， 发布教学视频《BasicIntroduction》
- 录制了20分钟的英文教学视频并发布Youtube

2015.10.24
- 内置模版教程(100%): BoneBlock
- removed unused load file in paracraft
- paracraft full edition pkg CI implemented.
- paracraft English version is published to upload.com.

2015.10.23
- paracraft download page with click count and history view implemented. 
- paracraft CI implemented, which can upload to FTP automatically. 
- fix movie block adding text key frame the first time. 
- Fix 3d scene context mouse capture. 
- support disable shader effect in settings page

2015.10.22
- fix UI scaling in finger size, fix touch to click translation bug. 

2015.10.21
- window version also support cmdline in config.txt. 
- texture package now displays file path and author.
- fix texture atlas model loading
- Paracraft full package CI ans script is tested and ready for release
- cleaned up several unused paracraft models and wrong texture reference. 
- touch click is optimized to auto extending click area
- source code merged with mobile edition. 

2015.10.20
- www.nplproject.com refined for PAX, download, donation, and about us page.
- pe_editor fixed button width with textscale
- mobile edition translation and front page done. 
- fixed empty string as key can not be de-serialized in NPL
- Paracraft donation license key can now be purchased via shareit website. 

2015.10.19
- fixed camera dragging issue. 

2015.10.18
- Paracraft code is completely separated from haqi code. full PKG size is shrunk to 5MB.
- Paracraft clean installer CI configuration refined and tested. 
- Newly created world will use a new mixed texture pack. 

2015.10.17
- 增加透明彩色方块(彩虹方块)
- 压缩默认材质包
- 清理材质Icon目录
- fix liquid block rendering with different block color
- paracraft dropped dependency on major haqi files

2015.10.16
- ItemCarpet added, 地毯支持22种不同的方向, 支持旋转. 
- 增加物品玻璃地毯： 半透明显示.  支持不同方向的物理碰撞。

2015.10.15
- optimized copy block operation in selectblock task
- 修复movieblock 清除所有关键帧后人物不复位的Bug
- 修复movieblock 添加全局关键帧导致人物突然运动的bug. 
- 修复movieblock actorNPC无法显示用户创建的blocks的关键帧. 
- 修复movieblock actorNPC无法录制block data的bug. 
- 演员方块录制支持相对位移
- Windows x64 支持声音播放, 重新编译caudioengine and soft openAL. 更新64位安装包
- 内置模版教程(80%): UsingColorBlock, RecordAnimation
- Ctrl+Shift+左键选择全部相连的方块
- 修复电影方块字幕等undo后， 无法添加关键帧的Bug

2015.10.14
- 内置模版教程(70%): Create Character
- fix scene context event error with multiple manipulator containers
- 选择方块界面支持拖动坐标轴来位移了

2015.10.13
- 方块选择增加了智能全选功能ctrl+a, 方块选择bmax模版
- 优化命令/select -all   增加智能选择命令
- add close button to chat window. fix zorder of texture package. fixed wrong block icons in default texture pack.
- 电影方块存为模版时演员和摄影机支持相对坐标。 方便电影方块的重用. 
- 内置模版教程(50%):  bmax model creator, using movie block

2015.10.12
- 新增命令/select x y z [(dx dy dz)]  选择指定区域的方块
- 电影方块支持运行相对命令. 例如 /select ~-1 ~1 ~-8 (4 6 4)
- Banner page added for facebook/youtube/PAX page. 
- 优化/setblock 支持entity data, such as 
          /setblock ~-1 ~0 ~-2 254 0 {attr={filename="blocktemplates/demo.bmax"}}
- 新增命令/editblock [x y z] [editorname]

2015.10.11
- many block icons are automatically rendered according to current texture at runtime on first display. 
- miniscenegraph automatically redrawn when device is lost. Added IsPersistentRenderTarget attribute.
- merged code with ParaEngine mobile edition.

2015.10.10
- bmax model now supports over 65535 indices / vertex per geometry. 
- manip UI size can be changed by [ and ] key
- optimized texture package, fixed a number of packages and added a new default package
- finished making poster page for PAX Aus 2015. 

2015.10.9
- bmax model can be nested, i.e. you can save blocks with BlockModel blocks.  They must be under the same world directory. 
- designed PAX 2015 posters. 
- A new hudson CI task is created to support making full paracraft 32bits window installer. 

2015.10.8
- actor audio file now uses native windows open dialog
- actor skin now use native open file dialog
- no-solid block is skipped during bmax rendering but will connect skins. 
- designed paracraft donation cards

2015.10.7
- refined Help page and templates folders. template folder now support ordering
- added /xgettext command to generate poedit file in current world
- added /language command to change translations for the current world.
- /show|hide player command added
- fix new mcml margin and min-width calculations
- donation page added and generated some donor keys
- fix new mcml page close window, fix new mcml editbox's getvalue function. 
- when movie block contains any text subtitles, it will prevent all subtitles of its child movie block
- 发布推荐作品<致匠心>: bmax里程碑的作品

2015.10.6
- fix delete world directory in win32
- Webtutorial support dismiss/close mode. Tutorial is automatically shown for newly created world.
- block template page refined, fixed pe_select SetValue

2015.10.5
- toolbase now support event filtering, the application object uses the event filtering mechanism.
- mcml now support word break
- web/video tutorials window fully implemented.  refined translations and UI in a number of places. 

2015.10.3-2015.10.4
- Window class now support dragging and auto size
- mcml pe_identicon added
- WebTutorial interface added. 
- fix draw utf8 text api in directX based painter
- tooltip implemented to new UI framework.

2015.10.1-2015.10.2
- md5 support binary output
- fix bone weight in bmax model
- booked all tickets and hotels for PAX Australia. 

2015.9.30
- BMax's Wheel Bones support automatic moving forward and backward animation
- Identicon class added, generating github like user icons

2015.9.29
- support delete local world, and fix local world not displayed for newly created ones.
- refined data structure in BMAX
- preparing trip to PAX.
- bone name can be read from bmax model.

2015.9.28
- multi color rules applied for bone binding. 
- fix AO shadow color of bone blocks in bmax model.
- refined Bone variable selection logics and sub variable display
- 新增命令/export, 增加export task
- save file dialog added

2015.9.26-2015.9.27
- refactored BMaxParser and BMaxFrameNode, acyclic links are removed. 
- bone names are automatically set and unique, IK bones are automatically discovered for hand and feet.
- bmax model now support opacity in animation channel.
- fix pure texture cleanup code. 
- fix hidden surface removal in bmax model. 
- fix bmax model rendering in deferred shading. Lighting is wrong. 

2015.9.25
- Optimized movie related item category and tool tips once selected. 
- skin blocks connecting to the ground (lowest bone) is ignored during block bone editing
- fix world sharing and saving pages in English version.
- Bone entity can be edited, such as bone names

2015.9.24
- BMax now supports color and skin editing in addition to bones. 骨骼与蒙蔽制作完成. 
- Block bone support rotation and mirror
- 支持torch, stairs梯子, 中继器, sign, item sign, image, button, vine, ladder, lever,door, window, fence的旋转
- refactored block image and block item frame's loading scheme
- Fix searchkey of blocks for English version.

2015.9.23
- fix asset height of camera look at position
- Block Bone editing added
- Automatically find parent block bones and allowing editing pivot point. 
- fix attribute model identifier display in asset manager

2015.9.22
- fix lilipad placement on water
- 修复shift+WASD无法走动
- added change language page at front page. 
- donation page and paied membership pro plugins studied
- Fix metal block rendering as black when shown with a color block. 
- fix runtime error when removing empty bone animations.
- added BlockBoneContext, EntityBlockBone, BlockBoneManipContainer, BlockBoneManip

2015.9.21
- when manipulator is used, we will automatically enter lock mode. 
- fix buffer picking crash bug by using weak_ptr for all headon display objects.
- rotation and position hierarchy of biped bones are fixed
- bone rotation key can now be edited via GUI
- config/language.txt can be used to change UI language

2015.9.19-2015.9.20
- added command /poedit for translations of xml files
- all major translations of paracraft is done.
- OpenFileDialog_win32 now fully support file filtering.
- Actor and model key frame support loading from file using standard window dialog. 

2015.9.18
- fix line width calculation in painter for 3d lines
- bone color scheme optimized
- Paracraft is preparing its debut in PAX Australia
- shader 1-4 can be changed via GUI
- lots of translation fix, adding movie category in builder page. 
- pe button support spacing attribute

2015.9.17
- 3d line width can be automatically adjusted according to current projection matrix.
- fix item onclick event
- fix undo operation of bone editing lead to unsaved states.
- pe_mc_slot's item_tooltip is now dynamic.
- Item class is a subclass of  ToolBase, supporting icon owner draw now via painter context.
- 彩色方块支持显示当前颜色和Tooltip.

2015.9.16
- fix first time variable key display for bones
- fix saving last editing camera position.
- last key type of bone is remembered for ease of editing
- one bone IK resolver added and used for bones without IK handle
- a key frame sound is played whenever the bone key frame is added
- replaced remove recording watermark 替换了视频录制的水印
- in bones manipulator, press K key to add a new key frame
- joint name displayed in timeline which auto size

2015.9.15
- all TileObject in C++ uses ShapeAABB internally.
- geometry are marked dirty and recalculated when yaw, pitch, roll, ... attributes changed.
- object facing is calculated into AABB, which accelerate occlusion testing when preparing the 3d scene.
- all entity in paracraft are now tool base object.
- last bone editing camera position is remembered.
- ParaX Bone external translation/scaling are added.
     -支持骨骼移动和放缩 in additional to rotation.

2015.9.14
- nplproject official website setup with ICP passed.
- Bones with IK handle such as hand/foot are automatically selected when clicked
- Fix: main player visibility is not controlled by AutoCamera. CanShowMainPlayer property added to main scene.
- 购买了Kinect动作捕捉设备

2015.9.12-2015.9.13
- +/- 键可遍历骨骼选择, ESC可取消选择
- 增加IK骨骼动画系统: PoleVector direction automatically set for Hand and Leg.

2015.9.11
- 优化命令/fog:  added command to reenable auto fog color
- fix manipulator connections for bone manip, a low level bug
- fixed bmax model display and refresh for newly saved models.
- fix free camera display.
- fix bmax model rendering for normal, AO (ambient occlusion) info are exported to color channel.
- quaternion and vector class are extended and refined in NPL.
- BoneProxy, BoneIKManip added
- Two bone IK resolver implemented
- 骨骼动画编辑 初级版本完成

2015.9.10
- Time Series can be nested.
- Bone animation can be edited and saved, including undo/redo, sub key editing, etc.
- All bones' key, value can be displayed as merged key, values on the time line and edited as a whole
- A new MoveManipContainer now support middle key to move object.
- FreeCamera has an avatar for better position in movie edit context
- Manipulator bounding radius can now be set, useful for bigger object.

2015.9.9
- bone rotation/trans/scale can be separately stored in animation instance using different names.
- FBX redundant keys are removed during loading.
- asset file and anim instances are decoupled in bipedobject in C++,allowing us to change model without changing bone animation.
- assetfile property added to base object

2015.9.8
- Fix load world screen button.
- pivot point rotation is displayed without rotation inside offset matrix.
- added BonesVariable and BoneVariable class
- C++ support key editing
- Key frames in bones can be edited in paracraft.

2015.9.7
- a trip to Beijing to present a PPT to education institute.

2015.9.6
- Fix Tips Stack zorder display
- refined LoadWorld inteface to support download status
- Paracraft's localserver run in disk mode by default instead of memory mode to support full offline browsing.

2015.9.5
- Bone rotation can be correctly edited.
- Fix static bone animation

2015.9.4
- finish ppt for education in paracraft
- Keyboard class added.
- key event is sent to all manipulators. BonesManip support esc to cancel and a few other key events.

2015.9.3
- ParaXBone now support reading animation from animation instance
- CVariable now support animated data, quaternion type added and exposed to scripting interface
- fixed SceneContext event fallback for mouse wheel.
- BoneManip now support selecting and rotating bones.
- added quaternion class in NPL.

2015.9.2
- Attribute class refactored into multiple files
- dynamic attribute set added and improved performance and reduced memory
- CVariable class implemented.

2015.9.1
- local transform and pivot exposed via attribute model, supporting both offsetMatrix and pivot based bones.
- BoneManip and BoneManipContainer added
- LoadBillboardMatrix added to painter context, and text can be rendered facing the camera.
- 电影人物支持骨骼显示

2015.8.31
- a very good movie story of 2016 is planned
- /time now command will return current time.
- Fix day light and time rendering when time is over 24 hours.
- Bones are exposed via attribute model, bone names are automatically set by bone id.
- fixed real time scaling manipulator error
- invalid-model or model without walk animation now has default walk speed.
- added BonesManip for bone displaying

2015.8.30
- Fixing typo in several translations
- refactored and removed unused animation classes.
- fix /shader 1 transparent block rendering in fog.
- fix movie timeline ending time not update as expected.
- objectbrowser in NPL code wiki now support dynamic row refreshing.

2015.8.29
- free camera added to EditMovieContext.
- 1,2,3,4,5键可以切换动作, 移动，放缩，旋转变量等Actor的子变量.
- /spawn 命令支持头顶文字并支持在指定巨型区域内生成.
          例如:  /spawn -p ~5 ~-1 ~-8 (3 0 4)     在指定立方体区域内随机生成.
- 新增命令/dist [@entityname] 返回当前人物到指定人物的距离。可以放在NPC或命令方块中运行
          例如:  /if $(dist @a) <= 2 /tip hello   当距离最近主角小于2米时，显示Hello.
- 扩充指令/walk: 接近或远离指定人物.
               /walk -to @a -dist 1  walk towards nearby player until distance is 1.
               /walk -away @a -dist 10  walk away from nearby player until distance is 10.
- fix command info display with special characters

2015.8.28
- fix actor rotation not updated when deleting key frame.
- interviewed and talked with duzhi

2015.8.27
- SetFieldInternal added to attributeobject, optimized plug to manipulator conversion.
- Replace selection with current block is now a per block action.
- 当选中一群方块时， 点击不同的Item按钮含义可以不同， 一般方块为替换选中， 彩色方块为替换为上次的颜色，模型方块为存为新模型.
- 修复彩色方块无法正确替换颜色的Bug.
- NPC人物模型支持存盘, 可以Spawn出任意模型了
- 电影模式下支持将bmax模型直接拖入窗口中新建角色.

2015.8.26
- 电影角色头部，转向等都支持用manipulator 操作
- 电影人物支持Yaw/pitch/roll的三轴旋转. 建议锁定人物后，使用Manipulator操作.

2015.8.25
- manipulators support undo/redo signals
- ScaleManipulator and ScaleManipContainer added. 支持Manip电影人物的放缩操作
- RotateManipulator and RotateManipContainer added.

2015.8.24
- Fix picking timer not started on MovieSceneContext
- Actor selection code is moved to MovieSceneContext
- refactored movie editing system, to make it more connection driven and automatic with ToolBase data binding.

2015.8.23
- 修复BMax模型自动放缩，原点位置和渲染.
- Fix ShapeAABB initial value.
- 手持模型方块右键点击选择中的方块可以保存为BMax模型
- TranslateManip now support grid size display and snapping to grid.
- BlockPivotManipContainer added as an example of data binding.

2015.8.22
- System.Core.Classes added for keeping all registerred class
- System.Core.ToolBaseAttributeObject, such that all ToolBase derived object have default attribute model.
- All classes have name property now.
- BMaxParser refactored to save memory and increase speed, at most 256*256*256 blocks are supported in size.

2015.8.21
- TranslateManip now responds to  mouse movement along selected axis with proper rendering.
- System.Core.Attribute plug class implemented.  findPlug added to AttributeObject.

2015.8.20
- 新增: System.Windows.Screen类
- ported ShapeRay, Plane class to NPL math lib.
- protocol buffer lib can be loaded from any NPL thread by calling NPL.activate("protocol/pb.cpp");

2015.8.19
- mouse event system finished in overlay and scene context.
- Matrix4 and related math is added to NPL.
- System.Scene.Cameras.AutoCamera added: several matrix attributes exposed via C++

2015.8.17
- EntitySky and related commands are refactored. Everything is managed by EntitySky object instead of WeatherEffect class. 天空与天气系统重构逻辑代码.
- 推荐列表发布作品<丰南实验学校>
- more attributes by GUI object.
- Overlay local transform matrix is supported. PushMatrix logics is fixed.

2015.8.16
- System.Util.CmdParser added.
- System.Core.ObjectPath now support set/get field by string
- 新增命令: /property [set|get] [-objPath] name value 设置或获取对象属性
- 新增命令: /property AsyncChunkMode true|false 是否异步加载场景. 部分作品可能不异步会好些.
- 新增命令: /property MaxBufferRebuildPerTick_FarChunk 2000
- 新增命令: /property WindowText string  设置窗口标题.
- NPL Code wiki: Object Browser 支持属性更改， 右键点击属性名或双击Cell, Enter键确认.

2015.8.15
- buffer picking for overlays and rendertargets are now supported.

- multiple buffer picking objects can be created using BufferPickingManager.
- Add toolbase InitSingleton class inheritance support .
- OverlayPicking class added to NPL.

2015.8.14
- Painter class is exposed via Attribute Model, applying single IO pattern.
- Painter class added dozens of attribute fields for 3d transformations.
- PainterContext provide complete 2d and 3d api with mixed coordinate system.

2015.8.13
- Fix painter Y downward coordinate when rendering 3d objects, which differs from 2d objects.
- Overlay ported to mobile with opengl support.
- Rotation/translation/scaling manipulator rendering done.
- SelectionManager/selection group and items are exposed via attribute model.
- ManipulatorContainer added, and creation logics is bound with SceneContext
- SelectBlocksTask now uses manipulators for pivot display. 更新坐标轴显示, 支持透明.
- added a couple of helper timer functions such as TimerManager.SetTimeout
- CBufferPicking added to C++ engine, supporting pixel accurate picking in ParaEngine.
- System.Scene.BufferPicking supported, wrapping the C++ interface.
- 彩色方块支持Alt+左键：像素级别拾取颜色. using the new BufferPicking interface.

2015.8.12
- 修复/addrule block命令， 增加命令说明.
- opengl renderer added zfunc API
- SceneState is now an attribute model, and exposed via NPL.
- Overlay now support two render pass: one with z fail and one with z pass.
- added ShapesDrawer class, for ease of drawing 3d shapes in NPL.

2015.8.11
- fix object space line sprite rendering in directX
- Painter class now supports drawing thick 3d lines.
- Painter class now support drawing triangle list, and draw line list.
- NPL层支持用Painter做3D Overlay绘制. See System.Scene.Overlay
- NPL and BMax related IP writing.

2015.8.10
- Fix 修复提示版方向在之前的世界中可能出错的问题.
- added System.Scene.Overlay interface for custom 3d rendering
- added placeholders for System.Scene.Manipulators
- ParaAttributeObject support QueryObject() and QueryUIObject().
- COverlayObject added in C++ engine, supporting advanced 2d/3d overlay rendering via painter context interface.
- public hudson CI: 20%: AB to svn

2015.8.9
- public hudson CI setup. all NPL script is maintained via public network. Trigger by SCM.
- fixing several scene context bug
- change \n NPL encoding behavior to make it inescapable in HTML encoding.
- Fix multiline EntitySign can not be saved to template properly
- EditMovieContext added for movie mode.
- 输入输出事件接口大量重构. 去掉了所有os.hook, 改用新的SceneContext处理所有3D事件.

2015.8.8
- 3D event refactoring using SceneContext (100%).  Removed a big file GameEventHandler.
- RedirectContext added for commands that requires user input.

2015.8.7
- ToolBase will auto delete connections when Destroy is called.
- Toolbase adding dump object info method for ease of debugging.
- Fix a cache policy error in web service wrapper causing repeated calls in haqi2's bag view.
- Refactored scene context: ItemSniper

2015.8.6
- 哈奇1，2手机版累计更新发布外网APK， 修复错误封号问题

2015.8.4-2015.8.5
- we were on a two day vocation to GuanLan Villa.
- 3D event refactoring using SceneContext (70%)
- All context, PlayContext, EditContext added.
- when control key is pressed, auto camera will not move the player.
- ParacraftScriptGit20150720.zip.pdf 软著时间戳gained.

2015.8.3
- fixed snow effect when snowing heavily exceeding pool limit.
- fixed os hook priority queue not working
- 3D event refactoring using SceneContext (50%)
- SelectionManager added.  BaseContext added for scene event handling.
- mailinglist updated to official website.
- New IM system deployed and used company-wide.

2015.8.2
- 扩充命令/sky -add filename   向天空增加动态BMax模型. 例如:
          /sky -none    不显示基层天空，但是显示submeshes
          /sky -add animated_sun.fbx   添加一个动态模型. 原点在0,0,0  半径0.5
          /sky -clear   清除所有添加的动态模型.
- NPL project mail list registered: mail us: npl@freelists.org
- subscribed to luajit maillist, it is looking for maintainer.

2015.8.1
- /memlimit -v will automatically adjust total memory as well.
- fix a distance chunk removal algorithm bug.
- FBX importer support alpha-blended texture when opacity channel is not none.
- EntitySky added, and all sky related functions are moved to EntitySky, such as changing model and textures.
- IAttributeFields now supports AddChildAttributeObject and query by class name or type.

2015.7.31
- FBX全面支持多动作导出. 支持2种方式
          1 通过同名的XML文件指定每个动作编号的起止时间
          2. 自动解析: 如果没有XML文件，则按照起始时间/10秒为动作ID, 每个动作不可超过10秒.
- 修复命令/rand  4 6   支持整数输出. 例如上面输出4,5,6.
- 修复命令/anim 支持默认为控制父物体。 EntityMovable行走后, 会恢复到上一次的AnimId.
- 修复命令/spawn 当所有生成对象都在范围内时， 不再生成新对像.  防止对象凭空消失.
- 新增命令: if then, else, elif, elseif, fi. 支持Nested嵌套. 例如
                set abc=$(rand)
if %abc%<0.3 then
     echo "1"
elif %abc%<0.6 then
     echo "2"
else
     echo "4"
fi
- 修复/fog -fogstart 雾化范围大于摄影机距离时显示Bug。 设置很大的起雾距离可取消雾化.

2015.7.30
- NPL runtime directory structure added.  Create NPL runtime as a npl command.
- NPL runtime packages can now be automatically loaded from ./packages folder.
- temp, screen shot folder is not created on startup, in order to make NPL runtime as silent as possible. perf.txt is also removed when no log to display.
- applied rule of silence to NPL runtime and paraengineclient.exe.
- NPL Runtime增加npl和npls命令: 分别以窗口和Console的模式启动npl运行环境.
- NPL runtime complete package: main_full.pkg 去掉了默认bootstrapper.
          默认的gameinterface.lua会根据命令行设定game loop file.
- NPL Runtime可以安装到系统Path Env中, 也支持side-by-side随App打包(./bin+./packages).
- NPL project: 建立外网Hudson CI. A program starts from build, not run.
- 新增命令:  /leaveworld [-f] 退出当前世界，回到登录界面.
          /leaveworld -f          :force leaving.
- Fix /spawn命令出来的根据-s参数决定是否会被存盘，默认不会被保存.
- Fix /spawn命令可以根据内部的物品数量不断生成新的物品， 当超过数量时， 离得最远的一个会被删除。

2015.7.29
- 公司内部IT部署改造: 弃用RTX， 改用开放的IM平台.
- Mobile版代码同步到最新: 包括FBX部分。

2015.7.28
- ParaEngineWebPlugin merged to lastest version with firebreath git.
- fix unicode version compile error of paraengine header files.
- Web version: fix js script for failing to AttachEvent on IE 11
- 修复物品展示等图片不显示的问题。
- 修复电影人物出现物理仿真的Bug.
- 支持Alt+左键拾取NPC, 电影角色，摄影机等。 拾取后的物品包含所有信息.
- 所有Entity, Block都有可能转变成ItemStack。至此世界中的一起都可以与ItemStack相互转化而不丢失信息.
- 修复shader 2,3,4下的雾化效果. 可以用/fog 命令控制.
- 新增命令/spawn [@entityname] [item_id] [-radius number] [-p x y z] [-s|persistent]
          根据执行者(一般是命令方块)背包中的内容随机选取一个生成物品或人物.

2015.7.27
- 规划了NPLProject, 和相关CI与开发内容。
- 申请域名nplproject.com
- NPL is going modular:  建立NPL.sln 准备整理相关类库.
- 制作FBX动态模型的Maya, Max的视频

2015.7.26
- 新增命令: /sendevent [@entityname] event_name [event_data]   用于建立Entity和Rule bag item之间的通讯
- refined Entity Editor name display
- ItemCode's sandbox environment is cleaned when loading a new world
- ItemCode's create script UI theme refined. Updated default themes for tabs, buttons, and treeview
- BlockEngine added MaxVisibleVertexBufferBytes attribute to make cache better.
- 新增命令: /memlimit [-v] [size_in_MB] change the memory limit of the block vertex buffer
               /memlimit 100   : change memory limit to 100mb
               /memlimit -v 10   : change visible chunk limit to 10mb
- Minor fix create new world UI

2015.7.25
- Refined chunk remove algorithm when memory limit is reached.
- added always in vertex buffer chunk radius to ensure really close chunks are never swapped off when video memory is tight (especially useful for shadow map)
- Chunk builder and light grid are exposed via attribute object.
- Chunk upload can now limit the total number of bytes to upload per tick, allowing smoother frame rate.
- BlockRegion memory exposed via attribute object.

2015.7.24
- Vertex Buffer usage are exposed and displayed in info window (F3) for memory debugging.
- Fix particles count exceed max allowed pool size warning.
- 内存优化: 可以设置内存上限， 保证永远不会因为内存问题Crash. 默认上限为700MB.

2015.7.23
- 当前内存使用情况可以从infoWindow中查看F3.
- 新增命令:  /docgen [filename] 从NPL Source code 生成IntelliSense XML 文件可用于NPL Language Service. 极大提升NPL编程效率.
- 生成所有常用NPL/Paracraft类库的IntelliSense文件到Documentation/paracraft.docgen.xml

2015.7.22
- 所有Slash命令支持命令嵌套: 语法与linux 命令嵌套 $() 一致. $()中的命令的输出作为下一个命令对应位置的输入
          例如: /tip $(rand 1 4)   打印1-4之间的一个随机数.
               /if $(rand) >= 0.5 /tip half chance      有1半概率执行/tip语句
- 楼梯BlockStair的物理仿真更加精确了 (仅针对NPC). 可以站在一半的高度上了，支持任意AABB.
- NPC和Mob默认不可以跳跃1格高的方块, 但是可以走楼梯或半砖.
- F3 InfoWindow中会显示选择selection的方块种类和类型,方便调试.
- 命令方块或物品中输入命令可以不必以/开始直接输入命令名字即可, 例如tip hello
- 新增命令:/say [@entityname] [-duration 10] [any text here]
          例如: /say hello there!
- 告示牌支持8种横向放置，包括上面的文字也是横向的.
- 告示牌性能优化, 只有当上面有文字时才创建UI对象.

2015.7.21
- GetLocalTransform added to base object
- Headon display now handles local transform, so that GUI can be transformed in any possible way in 3d scene.
- visual studio 2015 reviewed with many videos.
- 重构Major Changes: refactored EntityMovable physics, to move entity with NPL instead of C++.
- 修复BlockSlab的物理仿真, Mob, NPC可以在上半砖或下半砖上正确移动.

2015.7.20
- unified Entity rulebag serialization.
- EntityHomePoint now support rulebag. 出生点物品支持RuleBag.
- EntityMovable now handles all movement in NPL instead of C++, allowing more control and simulation to entities.

2015.7.19
- Fix npl code wiki packaging error for script file.
- 修复CI bash shell脚本, 支持force include by *.lua in main_script-1.0.txt
- 修复CI bash shell 生存Client PKG脚本, 性能大幅提升.
- AssetEntity, ParaXEntity, NPLRuntimeState, Viewport now exposed as attribute object.
- fix paracraft preloader that load some haqi files.
- add commonlib.add_interface to support faster multiple inheritance for pure interfaces in NPL/Lua.
- TableAttribute will display table which is AttributeObject itself in the third column.
- EntityManager is exposed via attribute objects with all of its entities.  registered entitymanager to DOM.

2015.7.18
- Dropdown list background filter added and fix drop down display in paracraft.
- added BlockVine. making it base class for all vine shape blocks like CornerStone, BloodStain, Stairs, etc.
- new command help is automatically added to help page.
- fix type error in shortcutkey.xml, fix load world input url field with empty text.
- 扩充命令: /activate @self  激活指定Entity, /activate默认为激活当期人物.
- EntityNPC增加规则背包以及激活逻辑。
- toggle desktop key E is now a global key that can be triggered at any time.
- 新增命令: /walk [@entityname] [x y z] [-random 5] [-speed 1.0] [-finishanim 0]

2015.7.17
- Fix: Carpet, Lilipad等禁止某些创建位置，replace/fillline task 也遵守相应规则。
- refined memory usage of chunks
- Regions are exposed via attribute object of block world object.

2015.7.16
- BMAX model now supports block lighting, and point texture sampler.
- Renderable chunk cache policy changed to automatically remove out of range unused device vertex buffer and memory buffer.
- 优化内存占用， 只有活跃并且在可视半径内的Chunk会被计算到内存中。 内存开销降低为之前的1/2.
- 官方论坛改造完毕， 版规，下载， 推荐，视频等大量帖子内容更新。
- 哈奇外网Rest接口限速完成并发布。

2015.7.15
- refined FBX texture path for embedded textures, fix a crash issue of assimp.
- fixed assimp FBX text format parser. by appending \0 to text format data.
- changed region cache remove algorithm to be based more precisely on render distance.
- 32 bits build only by default has 4 region cache.  region cache remove is only triggered when user has moved across 2 chunks since last cache update.
- Refactored ParaVertexBufferPool to be exposed via attribute interface.
- added a few stats fields to block engine.
- 发布推荐列表: ParacraftSDK教学视频4到6.

2015.7.14
- fix FBX with embedded textures
- refined official forum categories, merged several posts, write a list of all works.
- 发布推荐列表: <Finding Miss Xuan> 实况.

2015.7.13
- Fix NPL language service can not show code outline for external files. Updated to git and vs site.
- client rest sent rate is limited, except for global store sync.
- FBX support merge: support both embedded and external FBX texture.

2015.7.12
- rest interface now support per user message query rate control. 禁止通过Rest接口对服务器攻击.
- 外挂账号会自动冻结10分钟或更久.

2015.7.11
- PlayContext added. Refined auto camera interface.

2015.7.10
- Add SceneContext, computational model of 3d event handling is redesigned.
- NPL outliner tool window created for NPL language service.
- NPL CodeModel implemented in NPL language service.  Supporting search and go to definition in current file.
- NPL code completion now support per solution configuration
- FBX模型支持嵌入或非嵌入式材质显示.

2015.7.9
- fix: transparent faces in ParaXModel loading moved from IO thread to render thread due to texture references.
- 统一了论坛和官网的Logo

2015.7.8
- Paracraft论坛改版并合并板块：作为官网的辅助模块，收集Bug， 分享作品为主。 创意剧场改为在官网推荐列表发布。
- 联网中的Client会自动从内存中删除不用的地形， 保证内存开销降低。 修复Client在卸载地形时， 会Crash的Bug.
- 修复联网的Client卸载后的Region, 重新载入后，地形不显示的Bug.

2015.7.7
- fix byte alignment issue of StringBuilder in C++, causing map chunk data to be sent mis-aligned.
- fix empty chunk column map data format error.
- fix multiplayer mode chat GUI runtime error.
- fix block missing in remote world: 解决联网Client世界，地图偶尔缺失的问题
- design of multi-layer animation system.
2015.7.6
- 修复Paracraft Launcher GetModuleFileNameEx issue.
- refactored texture loading logics in ParaXModel, fixing a potential multi-thread crash during texture loading.

2015.7.4
- 录制ParacraftSDK视频6: NPL code wiki.
- NPL code wiki: learn.page 支持demos from lua or page files.

2015.7.3
- added dozens of command descriptions.
- fix npl code wiki security issues: NPL code wiki can only be run from writable worlds, a message box will be prompted if user attempts to run it in read-only world.
- set /clicktocontinue off when running npl code wiki.
- NPL code wiki: internal training.
- 推荐列表/微信发布: 微电影<尽头的承诺>

2015.7.2
- object_browser.page fix menu item display (click area)
- npl code wiki加入Help菜单. 增加命令 /menu help.npl_code_wiki
- fix world upload error when client data goes out of range.
- GameLogic now exposes several API code paths for ease of use by plugins.
- 修复下载世界的Tips不消失的Bug.
- Filters introduced to paracraft framework for plugin development. it is used for filtering input/output of certain functions like commands.
- 新增命令/open npl://    启动WebServer打开NPL code wiki上的页面.
- 命令提示窗优化. 未翻译的文字不再显示.  fix text overflow when scrolling.
- fix menu click area in object_browser.page.  增加DOM类型:Game, GameLogic, commonlib, System.
- TableAttribute fix meta table index display

2015.7.1
- object_browser.page will list all registered document model.
- console.page support both run as code or run as page.
- fix bmax model rendering in BipedObject. bmax is now a boolean property of parax model object.
- AttributeObject and TableAttribute class implemented. A unified interface for data access
- object_browser.page now support inspecting _G variable in lua.
- fixing a number of leaked global variables in previous code.

2015.6.30
- Learn and studied all maya api, design and sdk samples.

2015.6.29
- 修复Paracraft launcher deletefile无法删除只读文件以及自我删除的逻辑。
- NPL Website Demo:  world.page 双击文件可渲染指定page文件.
- NPL Admin Site平台正式更名为NPL Code Wiki. 可以作为一个适合高级用户自己DIY各种Web小工具Plugin&Page的场所. 类似一个支持3D编辑功能和全部NPL指令的代码WIKI网站。
- NPL Code Wiki: 网站说明
- Mod manager support handleMouseEvent
- NPL Code Wiki: 增加propertywindow.page.  支持查看ObjectPath上的所有属性.
- 修复部分C++底层Data interface 类型错误的Bug.

2015.6.28
- NPL Website Demo:  world.page 可列出当前世界中的信息和文件. 相当于每个个人服务器的世界目录都是一个WebServer目录。
- File monitor support system wide file detection. world.page: 当前世界中的文件更改会自动刷新

2015.6.27
- NPL Admin site: ajax framework implemented. documentation written.
- System.Core.DOM and System.Core.ObjectPath added. Unified interface for C++, NPL object access.
- NPL Website Demo:  object_browser.page 用ajax获取client所有DOM数据.

2015.6.26
- jeasyui framework added to NPL website.
- NPL Website: propertywindow.page implemented with datagrid control of easyui.
- fix quick select bar not shown in editing movie mode
- BMax Animation(20%): 电影方块中的演员支持bmax和fbx格式. World Files API支持Search Cache.
- fix FBX animation speed.

2015.6.25
- BMax Animation(20%): Scaling automatically by 2/4/8/16 times.  Pivot and AABB logics designed and implemented.
- fix lilypad block normal flipped.
- fix NPL web server script filter priority. fix serving files with empty base directory.
- 新增命令: /savemodel [modelname] 保存当前选中的方块为BMax模型.
- NPL Website Demo:  viewsource.page 可以查看每个页面的源代码, 并可以Rich/Raw切换显示.
          未来可以作为鼓励用户学习和实践NPL写plugin的场所.

2015.6.24
- BMax Animation(10%): 增加BlockMapColor属性
- NPL Admin Server: changed config files to serve files in Texture, model, character directory.
- NPL Website Demo:  blocklist.page: 在网页端显示所有方块的信息.  用Web的方式写代码，挺适合快速开发一些View
- 修复BMax模型中Y Axis和Transform没有生效的Bug. 修复模型AABB没有计算Transform和Animation的Bug.
- Paracraft论坛导航栏加入官网链接等.

2015.6.23
- fix ArrayMap, and Filters class.
- admin site (100%): framework is done. added js/css for drop down menu, mobile theme,  readme.txt added, index page, sidebar added.
- NPL Website Demo:  Console.page: 在网页端执行任意的NPL代码.
- NPL Website Demo:  Worldmap.page: 在网页端显示当前世界的小地图.
- 官网+微信发布: 《电影方块教学6》

2015.6.20
- admin site (70%): menu system added, data is read from XML database.
- Fix npl web page parser not outputting text behind last closing npl code tag.

2015.6.19
- assimp & FBX compiled 64bits version under win32
- 更新外网Paracraft 64bits版支持FBX和最新PKG
- 修复Paracraft登陆器在无法更新文件时，仍然显示更新成功的Bug.
- 更新外网Paracraft登陆器: 只读文件更新时会自动去掉只读属性。
- BlockWorld added MinWorldPos and MaxWorldPos attribute and prevent any C++ code to access block region outside its range.
- 增加命令: /worldsize radius [center_x center_y center_z]  限制世界的大小。
          注：已经加载的region(512*512)除外。与/loadregion配合， 可以在Server上定制任意形状的区域。
          例如: /worldsize 256  主要用于Server端防止内存泄漏， 建议加在出生点的指令中。
- 新增MaxIPAddress 属性, 获得最大的本机IP(已经排除Loopback ip range 127.XXX)

2015.6.18
- FBX支持顶替着色Vertex Color.  BMaxModel支持静态模型in additional to animated models.
- fix esc key is outputed to edit box 命令窗口中ESC可清除命令， 再次按ESC可取消输入.
- 彩色方块，模型方块, 告示牌，相册，都支持Alt键拾取为带有信息的物品
- fix crash when window size is 0. a minimum of 1*1 is ensured.
- LockWindowSize attribute added to ParaEngine object 允许锁定窗口大小，全部用程序控制.
- 支持从外部浏览器直接拖fbx, x文件到窗口中， 会自动导入并变成手中的一个模型物品。
- 模型物品不存在时会显示一个默认的模型.
- fix FieldType_DVector3 ignored in SetField call. 修复手持物品显示位移没生效的Bug.

2015.6.17
- ParaX Bone calculation now support offset matrix, and static transform in addition to pivot SRT transform.
          this is mainly for importing FBX animation directly.
- fbx->parax 骨骼动画模型导入的核心功能完成.
- Bone's rotation matrix is moved to a post step after all bone matrix is done. and calculated from final matrix.
- 彩色方块支持shift画线, alt单个替换, alt+shift批量替换等操作.
- 模型方块支持带动画的FBX, ParaX文件.
- BMaxObject now support looped standing animation and fully support loading from FBX, ParaX files.

2015.6.16
- admin site (60%): options are loaded from XmlDatabase and configurable.
- Shader 2,3,4: 增加specular light map, NormalMap中的Alpha通道表示反射贴图：0表示全反射, 1表示不反射。
- fbx动态模型导入: 骨骼与动画信息.
- fbx->parax静态模型导入完成

2015.6.15
- WebServer: menu and tree-walker system
- XmlDatabase: a simple xml based database system in pure NPL. 支持最基本的select, update, delete方法. 每个table一个XML file.

2015.6.14
- ArrayMap class added to script/ide/stl
- Filters class added to System.Core
- WebServer: plugin, cache and options system implemented
- WebServer: mem_cache implemented: single threaded memory cache

2015.6.13
- C++ Engine: fix clip area bug in old GUI system.
- Fix /savetemplate command to be able to save relative to current pivot position.
- Fix DIY block's  attributes and category are not changed when redefined.
- WebServer: default sensitive theme template added.

2015.6.12
- WebServer: fix mine types of webserver for html files
- WebServer: by default to listen to 0.0.0.0 which means all ip addresses on the computer.
- Paracraft官网: 完成所有推荐列表作品的收录和英文标题的翻译。 收录并整理了所有过去的新闻与教学视频. 近100篇图文整理.
- FBX->ParaX File importer: animation initial implementation reviewed.
- admin site (40%): theme framework.

2015.6.11
- WebServer: any files inside zip/pkg can be served by the web server.
- all files under admin server folder are packaged to all installations.
- WebServer: support relative path ./ and url request params, add api function site_url
- admin site (20%): xmlrpc.
- Paracraft官网首页在手机上可正确放缩.
- Paracraft微信: Paracraft.cn多语言官网上线. write "about us" page

2015.6.10
- WebServer: both compile and runtime error message of npl page will be returned to client.
           the line number in script matches that of the merged script. Ease for reading runtime error.
- WebServer API: add exit(), __FILE__, dirname(),  include, include_once, etc.
- WebServer API: support nested include() inside page script.
- WebServer: fix npl page redirection error.
- 新增命令:/webserver    start web server at given directory: e.g:
          /webserver                              start the default NPL/ParaEngine debug server (mostly for client debugging)
          /webserver www/my_web_site      start your own HTTP server.
- admin site (10%): NPL后台管理网站. 全部用NPL WebServer完成.
- fix conflicts between multiple instances of system file watcher

2015.6.9
- WebServer (100%): url redirect, reorganize file structure, doc refined, php-like page script.
          NPL WebServer具备Apache + PHP同样的功能, 性能更快.
- WebServer: NPL wsapi interface done. lua extension can be dropped.
- WebServer: NPL request/response now support client side cookies.
- WebServer: npl_page_env, npl_page_handler, npl_page_parser, npl_page_manager implemented.
          支持PHP-style: HTML+NPL mixed mode file. 动态编译Page + 缓存代码.
- WebServer: npl_page_manager支持文件修改监测并自动重新编译缓存代码.

2015.6.8
- Abstracted web server interface: old socket based httpd web server is deprecated. new npl_http server implementation added.
- WebServer (40%): 增加npl_request, npl_response, npl_file_handler 类.
- WebServer配置文件支持%CD%, 可从document root自动获取.
- npl_response支持chunked data.

2015.6.6-2015.6.7
- 彩色方块ColorBlock全部逻辑完成.
- 修复所有Shader中block category id 浮点数取整错误导致分类错误的Bug
- Bumpy block shader pipeline added.
- 新增方块: 彩色金属方块, 支持Normal map, specular map.
- Specular light added to HDR shader pipeline.
          Shader 2 的Specular+Bump效果使用虚假摄影机光源模拟的。
          Shader 3 HDR的Specular+Bump效果: 支持精确太阳反射+全场景Ray tracing反射+Fake torch light反射

2015.6.5
- 新增方块: 引入一种可DIY 32bits 颜色的彩色方块ColorBlock. 可用于派生其它方块
          颜色是32bits的， 不影响渲染性能.
- Add new block attribute color_data which use a data field for a 32bits color.
- 新增命令: /setcolor [x y z] [#rgb] 给指定方块着色 (未来新版Widget UI 会提供画笔上色)
          /setcolor #ff0000    当前人物脚下的方块变为红色
          /setcolor 10 10 10 #ff0000    paint block at world pos to red color
          /setcolor ~ ~1 ~ #ff0000      paint with relative to player position.
- block item class now has complete key/mouse event handlers which are fired when selected in hand
- 新增: System.Core.Color  移动部分代码. 支持16到32位颜色变换.
- Deprecate 3DMapSystem namespace. System is the default, no need to select implementation.
- 新增Item: ItemColorBlock 可通过快捷键选择场景中的Block颜色或改变饱和度和亮度.
- Fix: disabled alt key release to activate the system menu under win32. 修复Alt key event

2015.6.4
- Network: PlayerMP支持Server端的Entity物理仿真， 例如可推动矿车等.
- Network: Entity支持Mount坐骑， 例如可乘坐矿车等.
- Refined paracraft network logic design document.
- DirectX/Opengl版的Block渲染Vertex部分支持Color2.  每个Block都支持独立的32位顶点着色.

2015.6.3
- Sync/fix PC/Android C++ source.
- haqi android APK file upgraded to version 1.5
- Network: 支持EntityRailcar的基础网络同步,以及平滑位移运动同步.
- Network: 支持从Standalone到Server模式切换时, 所有已经存在的Entity自动同步.
- Entity inner object logic unified and makes faster, using week reference at all places.
- Fix visual studio 2013 npl_build_rule.targets with Exec task that can output error to console.
- Paracraft官网增加Category页面, 可自定义GridView, 优化若干外观代码.

2015.6.2
- www.paracraft.cn 官网开放. 待内容录入. 中英双语.
- C++ support "onactivate" event.
- Editbox will lose focus when window is deactivated.
- Widget UI底层(50%): Focus, and active window added.
- 新MCML:增加pe_editbox, pe_if.
- 官方推荐作品: 《电影方块教学5》发布

2015.6.1
- Cursor to X translation api added to editbox
- optimized GetTextWidth npl function to make it faster
- Fix: text size calculation is more accurate without trailing.
- Fix: painter clipping during save/restore in NPL script.
- C++ GUI object support CompositionPoint attribute for IME customization
- 修复个人Server无法显示对话消息的Bug.
- 新版Widget UI: Editbox(100%) : 支持IME输入点, text scrolling, clipping, Mouse Drag selection, Cursor blink
- 修复mouse move and release event only sent to last mouse down widget

2015.5.30-2015.5.31
- 新版Widget UI: Editbox(70%) : 支持ctrl/shift/home/end/方向键等组合键， 支持undo/redo
- Widget Editbox supports all key sequences that behaves exactly like Win32 editbox.
- Widget Editbox supports undo/redo.  support maxLength property.

2015.5.29
- Fix 切换Shader时光照错误或重复计算.
- Fix HDR shader火把的颜色不随光源颜色变化的Bug.
- Fix Shader 2 Lite: 远处影子Depth在摄影机摇摆时计算有误.
- Fix Shader 2 Lite:  太阳光照强度曲线计算错误。 取消HSV颜色修复.
- Shader HDR和普通Shader都增加了Torch light fake shading, 让夜晚模型看起来立体一些。

2015.5.28
- 新版Widget UI: Editbox(60%), 支持Cursor, selection渲染, 支持Clipboard, advanced text editing.
- Key sequence added to widget editbox: supporting all the major editing combos.
- 修复MovieTimeline 在Refresh后显示错误的Bug.

2015.5.27
- ParacraftSDK中的MyApp增加了注册NPL API的演示.  NPL Register API 函数改为Interface.
- 新版Widget UI: Editbox(50%), 支持IME和中文输入法.
- InputMethodEnabled attribute added to GuiBase
- refactored GUIIME, so that every GUIBase object can receive ime event.
- GUIBase now emit "oninputmethod" event.
- RegisterNPL file is now part of formal core interface.
- Fix: NPL files are loaded from dev folder first.
- BMax静态模型: 基本BlockList模型导入(20%), FBX导入(20%)
2015.5.26
- HDR shader: 修复透明物体的渲染在HDR中不对的Bug. 对HDR增加了Opache和Alpha Pass.
- NPL table now support field iterator

2015.5.25
- 新增命令: /movieoutputmode [on|off] 快速加载. 远处Block出现速度提升。
- 新增命令: /maxrenderdist [64-1024]  最大可视距离上限.  超过300会非常占用内存和显卡。 只建议截图或64位版.
- 优化命令: /renderdist 支持maxrenderdist
- 新增BlockModel物品:  可以制作高精度BMax模型，方法如下
右键图标可以输入fbx, x, blocktemplate文件名。 当前有选择的物体时，自动根据Pivot和AABB将其转换为接近1x1的模型。 放缩比例只支持4， 8，16. 三个分辨率。 过大的模型不允许导出。 保存时询问是否覆盖之前的模型。
击碎后自动变成图纸。

2015.5.23-2015.5.24
- DirectX/OpenGL增加BMax model的渲染Shader
- added bounding box to BMaxObject.
- BMax model now support deferred shading shader 2 and above.

2015.5.20-2015.5.22
- Paracraft官网: 中英多语. 常规内容录入完毕.
- 修复Win8平板无法点击的Bug (Intel bug report).  修复最小分辨率导致UI重叠的Bug.
- 隐藏GoalTraker UI, 左上角的问号只有当有Build任务时才显示.
- Paracraft Launcher 维护性过更新(外网paracraft/haqi2更新)
[fix]     已经下载完成的文件，会被重复下载
[fix]     更新失败后，误删version.txt
[fix]     下载进度log没有在UI线程显示
[new]  网络超时，支持重连。不间断可以尝试10次，连接成功1次，计数归0
[new]  显示下载速度
- Mobile版在win32下支持Key combo, like ctrl+v. Editbox支持方向键方便调试, 修backspace删除2个letter.
- Mobile版修复TinyXml2中的2个Bug, ParseXMLString 的COLLAPSE_WHITESPACE会改动const input string. &nbsp没有转成' '.
- Mobile版修复Appdirectory 使用writable path.

2015.5.18-2015.5.19
- Wordpress官网: 升级PHP, GD,增加常用插件. 升级Theme.
- Wordpress官网: 首页与布局
- BMax与FBX格式支持初步版.

2015.5.16-2015.5.17
- 修复部分模型UV不对的问题.
- Shader 3: 优化点光源fallout曲线.
- 新增命令: /brightness [0-1]set brightness factor (0-1) used in HDR shader 3, 4. default value is 0.5. the larger the more detail in brighter region.
          /brightness 0.1    more detail with dark colors
          /brightness 0.8    more detail with bright colors
- Shader 3: HDR增加Debug view模式.优化Bloom
- 深圳动漫创作大赛： 中小学组Paracraft作品比赛结束并颁奖.
- 官网: 多语言增加多语言配置qTranslate-X plugin. 规划官网分区.

2015.5.15
- Shader 3: 修复摄影机有特殊偏转时 ，阴影计算错误的Bug
- Shader 3: 优化ambient光照,考虑夜晚和太阳.

2015.5.14
- fix shadow map in deferred shading 修复人物自阴影shadow
- fix character sun light rendering in deferred shading.
- 新增命令: /dof [0-1]  调节景深. 越大景深越大（模糊）
               /dof 0   disable depth of view
               /dof 0.09   超级景深
- 命令: /sky -cloud 0.9  可以改变白天的影子。 支持/shader 3以上.
- HDR shader: 修复sun color,使用HDR版的sun diffuse color

2015.5.13
- Mod can add OnWorldSave event
- 优化Shader shadow, fix shadow rendering bug at night.
- 高级光影Shader: fix torch light with 0 intensity.
- 高级光影Shader: Night Eye effect added. adjusted ambient light.

2015.5.11-2015.5.12
- ParacraftSDK增加MyApp Sample. 自定义命令行的EXE.
- 高级光影Shader: 增加HDR, tone map, bloom, depth of view, sun glow,  torch glow, rain fog.
- 扩展命令: /shader [0-4]     3 为 bloom effect,  4 为bloom+ depth of view.
               /shader 1   普通渲染
               /shader 2   真实影子+水面反射
               /shader 3   真实影子+水面反射+HDR光影+Bloom泛光+RainFog雨雾+Vignette
               /shader 4   真实影子+水面反射+HDR光影+Bloom泛光+RainFog雨雾+Vignette+DepthOfView景深

2015.5.9-2015.5.10
- Block默认雾化Shader更精确
- 增加Multi-pass 高级光影Shader pipeline.

2015.5.8
- 讨论计划支持FBX格式的方案 (包括内置贴图).  同时支持STL格式.
- 全平台引入assimp开源类库, 计划支持格式导入.
- Widget UI: 支持page refresh. 支持LayoutRequest事件.
- Widget UI: optimized event with static new pattern.
- Widget UI: added application event log, added sizeEvent when geometry changed.
- Widget UI: optmized show window. mcml controls's ShowEvent is invoked after layout is done but before actually shown.
- 新增小地图物品. 可以随时动态生成周围的小地图。 采用新版Widget UI

2015.5.7
- added AutoClearBackground attribute to gui base
- Widget UI: window类增加show/hide功能.
- 修复背包物品无法保存的Bug.
- Widget UI: 增加pe:custom和测试用例. 支持自定义UIElement控件.
- 修复self painted gui crash when resize native window.
- Widget UI: 增加show/hide event, 重构window create 逻辑代码.
- 修复render target resize 后不更新，以及device设备没有更新的Bug

2015.5.6
- Mod system can replace all major UI and events in the game. Generally everything can be replaced by a mod.
- 新增命令/bloom [on|off]  开启Bloom泛光模式
- 新增命令/createmob name [x y z] [filename] [...]
          /createmob test chicken.x
- EntityMob支持相对世界路径的模型资源存盘.
- 增加6个方向的骨骼方块为将来BMax模型最准备.
- 增加小地图插件的Demo, 用新的widget UI api绘制高度彩色图.

2015.5.5
- Fix Haqi webapi dbserver integer overflow bug (serious bug fix).
- Shader effect增加final processing step.
- 新增命令/depthofview [on|off]  开启景深模式

2015.5.4
- Widget UI底层(47%): 增加pe_container, Canvas类
- fix widget UI mouse picking zorder
- fix pe_button alignment
- System.Windows.mcml:  global style with inheritance

2015.5.1-2015.5.3
- Widget UI底层(45%): pe_script added
- Widget UI: 增加pe_unknown, pe_input, pe_button
- Widget UI: 支持mcml page event
- Widget UI: pe_button label rendering and alignment added
- Widget UI: auto resizing of widget window done (mcml layout).
- Widget UI: Fix mouse/key event routing to parent control.
2015.4.30
- Widget UI底层(40%): 9 tile Texture渲染
- Widget UI: mcml支持background属性
- painter's drawTexture support 9 tile texture natively.

2015.4.29
- Widget UI底层(35%): 文字渲染
- Widget UI: 增加Label支持文字渲染
- Widget UI: 增加pe_text,pe_span, pe_font支持自动换行和放缩的文字渲染.
- 修复painter渲染utf8 string encoding bug.

2015.4.28
- Widget UI底层(30%): layout 架构
- Widget UI: add pe_div, Style, default_css类
- Widget UI: layout支持所有alignment方式, 包括之前不支持的right alignment with unspecified width.

2015.4.27
- 修复GUI底层无法显示非法UTF8字符串的Bug. 非法String采用?代替.
- Widget UI底层(20%): layout and mcml底层开发
- Widget UI: add Layout, LayoutItem, Page, PageLayout, DOM类
- Widget UI: Window类支持从url中LoadComponent.

2015.4.25-2015.4.26
- Widget UI底层(15%): Mouse Enter/leave event implemented.
- Widget UI: toolbase Property now uses a property table and supports more customizable ways to define property.
- Widget UI: ButtonBase refined. UIElement rect and geometry coordinate system fixed.
- Widget UI: layout system designed
- ParacraftSDK教学视频4.0 Mod   5.0 FAQ
- 更新ParacraftSDK/tools/ThirdParty/License  鼓励所有外部开发者使用GPL协议开发插件。
- 收录第三方开源Paracraft插件: tools/ThirdParty/TemplateCreator  模型转Block.

2015.4.24
- Widget UI底层(12%): SizeEvent now recursively sent during prepareRender added.
- Widget UI: Application:PostEvent 系统完成, 增加测试用例, 支持Event Compressing, 增加App主循环.
- Widget UI: 新增LogEvent, PostEvent, PostEventList类. Application Event支持send/post 两种模式了
- 动作系统UI设计: 时间轴部分完成.

2015.4.23
- 新IDE底层(8%): 新增类库ButtonBase, Mouse, Button
- Widget UI底层架构 readme.txt and new mcml system planned.

2015.4.22
- 新IDE底层(6%): Event, FocusEvent,  新增Global UI Application class.
- Widget UI底层(7%): focus系统, toolbase 增加爱child-parent management.

2015.4.21
- 新IDE底层(4%): KeyEvent, MouseEvent 完成.  rebased ToolBase, Action, ActionGroup class.
- NPL层加入:RingBuffer, Point, Rect的基础Math类.
- Widget UI底层(5%): 新增UIElement支持rect testing, etc.

2015.4.20
- 建立动画编辑UI的底层设计逻辑：4维空间到2维空间的变换。
- 发布创意剧场： 《蒲公英》
- 新IDE底层(2%): PainterContext, Window, ToolBase 完成.
- 4维时空编辑系统(0.1%): TimelineView place holder.

2015.4.17-2015.4.19
- 修复3D转2D坐标时由于UI scaling 造成错位的Bug.
- Mobile版haqi修复部分IO慢的机器登录时会与服务器断开的Bug
- 修复NPL Debuger和IPCDebugger, 支持dev目录下NPL文件的调试。
- 发布NPL Debuger package 1.3到VS官网.
- 录制ParacraftSDK教学 part 2 NPL & part 3 MCML:
- 发布创意剧场：ParacraftSDK教学1-3
- 官方论坛关闭评论功能；取消官方QQ群和比赛，改为用户自发组织。

2015.4.15-2015.4.16
- Mobile版修复3D文字Zorder不对的Bug.
- Mobile版调试和优化haqi1,2性能. card page performance improved
- Mobile版fix combat level loading error during login. Fixed white card can not be saved in bag.
- Mobile版Haqi1,2更新提示采用GSL_version.
- Mobile版Haqi1,2发布测试版. 哈奇1： http://www.pgyer.com/haqi   哈奇2： http://www.pgyer.com/haqi2

2015.4.14
- ParacraftSDK 增加C++ plugin的sample和相关的ParaEngine include C++ header files
- ParaXStaticModel now keeps system mesh in raw vertices and indices format, thus saving memory.
- mobile version of ParaXStaticModel now supports cloning physical mesh.
- add STATIC_LIBRARY flag for cAudioEngine and physics engine to avoid name conflict under android/ios
- Rebuild Bullet3 paraengine plugin removing triangle winding order change.
- Android版3D物理引擎集成完毕. Bullet physics as a plugin.
- Android版Haqi1,2修复物理碰撞相关的地方失效的Bug.
- Mobile版修复实数地表Base layer缺失时没有使用默认贴图造成地面出现一条线的Bug.
- Mobile版修复部分静态模型错乱的Bug.

2015.4.13
- Taurus项目增加到SDK Git上
- 3dsmax 导出插件集成进入ParacraftSDK
- Mobile版修复AudioEngine切换时，不暂停声音的Bug.
- BMax项目设计草案效果图
- Mobile版禁用Premultiplied alpha texture. 修复alpha通道颜色太黑的Bug
- 录制了ParacraftSDK教学视频1.0

2015.4.12
- ParacraftSDK: PEDN开发网对外开放部分内容
- 哈奇1,2手机版发布玩家测试
- ParacraftSDK  walkthrough 视频教程WIKI草稿.

2015.4.11
- 深圳动漫基地Paracraft培训课第一周.
- refactored and added TouchSessions manager in c++.
- added TouchGesturePinch in c++, Pinch gestured is mapped to mouse scroll to 3d scene if there is no user defined touch handler.
- Mobile版默认支持pinch放缩操作. 哈1,2可放缩摄影机.

2015.4.10
- 新增命令rsync用于发布时下载美术资源到cache目录中.
- 修复Paracraft离线版中缺失材质. 修复由于replace texture导致自动rsync失效的问题.
- Paracraft离线版中包含userdata.db (材质包信息)
- 用ParacraftSDK制作paracraft app 的win32 离线安装包 给动漫基地
- Mobile版暂时禁用了3d sound, 手机功放出来听起来怪怪的, 耳机中也许是好的.
- iOS端引擎类库可用cmake编译了
- Mobile版修复ui animation reference to unscoped stack variable, 造成数据失效的Bug. 修复Mobile上所有animated ui不显示的Bug
- Mobile版哈1,2所有底层造成的Bug类问题解决完毕

2015.4.9
- 优化ParacraftSDK: Fix desktop icon, 安装包更小, added Run.peworld。
- Mobile版: 哈1,2: refined clickthrough for quest pane in mobile version
- 使用ParacraftSDK建立了_apps/Paracraft项目. Android平台的自动打包迁移到ParacraftSDK.
- 制作Paracraft离线安装包nsi脚本, 并上传Git.
- 创造模式下右上角的问号改为激活F1百科(去掉了点我开始的提示)。 模板管理UI放入E键中的管理模块内.
- 优化了Plugin系统，增加ModManager以及几个Mod事件.
- ParacraftSDK: 增加Mod系统Demo.

2015.4.8
- ParacraftSDK 开发环境v1.0.  大量cmakelist files, 和一些基本的说明文档, 支持生成Android APK.
- ParacraftSDK nsi安装脚本制作完毕. 初步是一个80MB的exe. 需要visual studio 2013.
- PETools for visual studio is also added to ParacraftSDK.

2015.4.7
- opengl font renderer now share the same shader with the standard 2d quad renderer. No shader switch now.
- Mobile版：投影文字渲染速度提升8倍。 Multiple text can now be batch-rendered. Shadowed text now only takes 1/8 of draw calls in most cases.
- Mobile版：android端迁移了physicsBT 3D物理引擎.
- Android版：haqi1,2任务追踪区域缩小.
- BMax插件项目立项: BMax = Block 3dsMax = pronounced as Baymax
          将方块模板转变为静态或骨骼绑定的动态模型。引入特殊方块作为可编程骨骼.
          配合暑期的骨骼动画DIY系统, 可以在Paracraft内部制作任意形态的动态模型. 以及放缩静态模型比例尺。
- Entity default G changed to 9.8 from 9.18.
- Paracraft官网download page download banner 图片重新制作.
- Mobile版:实数地表增加雾化效果
- Mobile版:修复Thickline造成Alpha blending错误.

2015.4.5-2015.4.6
- added ASSET_STATE_FAILED_TO_LOAD to texture entity.
- SelfPaint UI object will correctly detect async loaded textures and repaint after asset is downloaded.
- Fix: Android版: 哈2聊天没有回车键
- Mobile版: 哈1,2的可视距离固定为很小，保证流畅。

2015.4.4
- Android版解决新版AudioEngine的Streaming路径不可读取的问题. 声音引擎彻底迁移完毕。
- Android版去掉了所有Audio Streaming, 因为sdcard太慢影响性能. 全部为in-memory audio.
- Fix: Mobile版哈2的新手教程配音只能播放前2秒的音乐。
- Mobile版默认哈1,2不播放背景音乐. 会提升一些性能.

2015.4.3
- Mobile版解决miniscene光照太暗的问题
- painter implemented all blending mode
- Mobile版放弃android自带API, 采用和Win32一样的声音引擎播放ogg,mp3等文件。
- Android版中哈2的新手教程配音只能播放前2秒。 需要切换到cAudioEngine修复。
- Android版通用子类库cmake系统完成. linux下通过NDK cross compile.  例如声音和物理引擎.

2015.4.2
- GUI层大量与Clipping, SelfPaint相关的优化和Bug Fix.
- hardware clipping moved from GUI Container to Painter class.
- both scissor rect and stencil based clipping is implemented in GPU painter engine.
- SelfPainted device now support hardware clipping for both directX and opengl.
- improved scissor rect performance with DirectX by disabling it when no clipping is used.
- GUI container no longer flush sprites, the render order is preserved, the caller is responsible to batch textures, this allows texture batching across group of ui objects.
- fix unstable transform when render self painted GUI object.
2015.4.1
- cAudioEngine added android build script.
- when the content of GUI object is changed, its SelfPaint parent will be repaint automatically without calling InvalidateRect manually.
2015.3.31
- 论坛下载区权限调整
- SelfPainted gui object will automatically add its render target to delete pool once it is destroyed.
- ContainerObject will remove dead objects from its children.
- Rendertarget now support LifeTime, SetDead attribute.
- fix asset manager's DeleteEntity call crash.
- CRenderTarget will delete device texture when itself is destroyed.
- SelfPainted GUIContainer will automatically repaint in the next frame, if any used texture is not fully loaded.
- fixed clipping region of SelfPainted GUI rendering inside the flipped opengl render target.
- add InvalidateRect() to SelfPainted UI container object. still a naive implementation that just invalidate all.
- Painter now support composition mode and auto flush previous render objects.
- SelfPainted Gui Object will auto clear clipping rect with a fully transparent color.
- 增加MCML的SelfPaint属性，一些文字和图片较多的UI，可以考虑SelfPaint， 例如聊天， 任务追踪，物品栏等。 可极大的提升UI渲染速度。
2015.3.30
- Mobile版Haqi2修复headon.speek, gossip_ai, shop, combat icon, texture overflow and typing error. Fix loop tips with mobile haqi.
- 修复新版登陆器更新失败仍可开启的Bug
- Mobile版GuiButton支持Headon Display over 3d object. 修复haqi2, 人物头顶图标不显示的Bug.
- Mobile版优化交接任务性能提升20倍. 4秒到0.2秒. N^M算法改为N+M. 基本可接受了。
- 发布创意剧场：比赛结束贴
- Android版: MainTexture.dds需要加入Preloader， 不然同步下载超过5秒， 部分系统会秒退.
- Mobile版增加CMissileObject. haqi1,2点击地面特效恢复。

2015.3.28-2015.3.29
- Mobile版Haqi2修复CCS人物UV错误, 修复Text size, 修复AutoFocus on login page.
- Mobile版修复XML parsing not skipping BOM header. 修复部分XML解析失败的Bug.
- 修复extendedcost失效的Bug. 发布外网补丁.
- Mobile版Haqi2修复Combat UI不显示的Bug.
- Mobile版Fix: CCS Skin composer uses black color as transparent color key. 修复透明CCS贴图不正确的Bug.
- Android版Haqi1, Haqi2常规功能,从登录注册到新手等都可正常运行.  性能还待优化.

2015.3.27
- Mobile版Haqi默认记住用户密码.  Fix:新手指引和出牌UI错位
- Mobile版修复全局透明多边形不显示的Bug.
- 人物头部运动的提示和编辑UI显示次序一致。
- Mobile版禁用Terrain Geo mipmapping rendering
- Android版Haqi2安装包脚本完成，可正常运行， 修复大批XML typing error.
- 深圳动漫基地5月会举行一个环保主题的基于Paracraft的动漫创作比赛, 内容同去年。
- 优化CCS换装系统的贴图加载, 没有加载的材质不会造成每帧的IO开销.
- Mobile版修复CCS换装系统材质不存在，就整体不渲染的Bug
- Mobile版修复haqi2新手教程Bug.

2015.3.26
- Mobile版修复Editbox输入后面有\r\n
- Mobile版ParaXEntity和MeshEntity采用异步加载, 支持AssetManifest.
- Globalstore.db和extendedcost.db改用加密的文本格式, 启动速度提升10倍(主要针对Mobile的哈奇版)
- Mobile版哈奇可以在手机上正常运行了.

2015.3.25
- Mobile版修复鼠标拖动事件数据模拟异常的Bug.  Mobile哈奇中所有触屏操作可正确映射.
- Mobile版ParaEngineExtension会自动加载Mobile API,  并替换一些系统默认API， 例如ShellExecute支持open url.
- Mobile哈奇中的注册会打开外部浏览器注册

2015.3.24
- Mobile版Haqi项目修复一批XML typing error.
- Mobile版Haqi项目优化GlobalStore进度显示
- Mobile版修复3D角色人物头顶文字显示错位的Bug

2015.3.23
- Mobile版Haqi项目作为ParacraftSDK的App Demo上传Git.  哈奇首个APK安装包完成 (部分功能还不完善).  See  https://github.com/LiXizhi/Haqi
- Fix ParacraftSDK license to make it fully GPL compatible. 允许用户发行自己的PC或APK包.
- 深圳动漫基地本年的环保主题的微电影创作比赛依旧采用Paracraft，已经发送海报给有关部门.
- Mobile版修复TextureSequence和assetmanifest中的md5文件名冲突的Bug
- Mobile版修复WritablePath下可用绝对路径访问而无Security Failure的Bug.
- Mobile版修复一批哈奇中XML不规范的Bug.
- UserTable can now be saved in writable path under mobile version.
- Mobile版的哈奇调整默认UI分辨率. 放大UI, 方便点击.

2015.3.20-2015.3.22
- fix terrain shader for mobile version
- asset manifest supported for mobile version
- support move file operation on mobile version
- implement auto make APK script and create a sample taurus app on mobile platform
- ParacraftSDK完成android平台发布任意APK的脚本.
- Mobile版增加Haqi和Taurus项目. 并可以独立APK打包，真机测试运行

2015.3.19
- Github上增加了GPL开源软件许可协议及其补充协议:  GPL license file for ParaEngine/NPL/ParacraftSDK  with additional permission for closed source and commercial project.
          https://raw.githubusercontent.com/LiXizhi/ParaCraftSDK/master/LICENSE
- 外网更新哈2安装包

2015.3.18
- 64bits windows version now uses luajit instead of lua to make same bytecode compatible for both 32/64bits system.
- Paracraft 64位Windows版发布并放入官网. Removed all dll dependency on MSVCRT
- Paracraft 32位Windows版外网Launcher更新.
- checked out LuaJit 2.1 dev branch, full 64bits support on memory size and iOS (interpreter mode only)
- 更新ParacraftSDK to Git: 最新的安装包, 打包脚本重写, 放入bin/目录
- 思考NPL/ParaEngine/ParacraftSDK的License形式.

2015.3.17
- ParaCraftSDK Git增加ParacraftBuild submodule
- ParaCraftSDK 目录结构优化, 修复Create Mod脚本
- 修复哈奇中家园物品不可移动的Bug
- Paracraft和haqi2 launcher最终版: 改为单线程, 可自动更新, 更新失败可继续， 可删除不用的文件，支持多国语言.
- 内网修复哈奇后台管理Pl+mysql的后台程序, 采用IIS的CGI模块.
- 增加命令行servermode="true", 使得32/64位的ParaEngineClient.exe可以以命令行模式工作，并可返回值.
- ParaCraftSDK 增加build目录, 新增64位zip包自动打包脚本

2015.3.16
- TextureComposer class and ComposerTask added. Only a single render target is created for each composer type.
- fix opengl texture reference count not zero bug.
- TextureComposer will automatically unload all component textures when there is no more composing tasks.

2015.3.14-2015.3.15
- Mobile版: RenderTarget support save to file
- Mobile版: CCS系统脸部和皮肤采用新的Painter引擎绘制.
- 增加ImageEntity类
- 发布创意剧场：原创魔幻系列电影第一部《神迹·黑塔后的大陆》

2015.3.13
- 重构人物换装系统，拆分为多个文件，代码更清晰.
- 2014寒假的Paracraft创意大赛评选工作最后阶段. 完成哈奇中的虚拟物品奖励的发放.
- 更新PC端外网Launcher
- Mobile版修复miniscene depth buffer invalid under win32.
- 人物换装系统可以在Mobile版下使用了

2015.3.12
- Mobile版修复文件选择渲染. 修复CmdToolip在小分辨率不显示的Bug.
- 修复PC版百科内容不显示的Bug.
- PC版和Mobile版统一使用main_mobile_res.pkg,内涵各种非代码资源
- asset manifest enabled for mobile version. accelerate parsing file speed, add "UseLocalFileFirst" attribute to manifest
- Paracraft新版Launcher完成，采用libcurl，支持断点续传，md5验证，有良好的更新提示

2015.3.11
- 电影演员关键帧合并头部上下，左右运动的编辑
- 电影演员关键帧增加x, y, z位置的精确关键帧编辑.
- SelfPainted gui render target support non-power of 2 region.
- Mobile版: modified low level file api source code to make it thread safe.
- Mobile版: 修复negative size texture quad rendering.
- Mobile版:  fix shader opengl error in terrain engine.
- Mobile版和paracraft PC版: 启用F12, Ctrl+F3, Ctrl+F4的内置调试工具.

2015.3.10
- 新增命令:  /sun [0,2] [0,2] [0,2]改变太阳的颜色. 目前只有在/shader 2下生效.
- 底层引擎删除数十个不用的旧版GDI文件和许多API
- added "SelfPaint","IsDirty" attribute to GUI Object. Test case added to TestGUI
- standard GUI and ownerDraw GUI can coexist on SelfPainted parent device.
- GUIContainer's "SelfPaint" can be turned on/off anytime anywhere. Once on, all its children including itself is painted using a private render target
- "SelfPaint" 一行语句, 可以让任意GUI对象变成RenderTarget Device. 子对象支持Standard和OwnerDraw混合模式渲染.

2015.3.9
- Mobile版:修复Rendertarget flip_Y的问题, 修复rendertarget viewport问题(Opengl only bug)
- Paracraft加了网页版入口 (not recommended so far, only for demo).
- 新增Github项目ParacraftWebsite 并上传了browserdemo
- http://bbs.paraengine.com/browserdemo/download.html  (not recommended)
- Mobile版更新支持断点续传和md5验证
- 添加人物皮肤时自动删除前后的空格

2015.3.8
- rendertarget (miniscenegraph) support "On_Paint" script callback.
- rendertarget can be created from script, the render pipeline will auto redraw dirty rendertarget.
- render pipeline supports a new type of render queue called owner_draw_objects, which is rendered even 3d scene is disabled.
- rendertarget attributes exposed to scripting interface. Test case added to TestGUI.lua
- removed 3DCanvas interface from NPL and C++.
- ParaObject now support SetScript function like ParaUIObject. Adding id property to ParaObject.
- 全面支持RenderTarget上的绘制

2015.3.7
- Mobile版底层打包升级到3.4, 修复字体渲染Bug
- Mobile版新增AutoUpdater类
- CPainter修复drawTexture scaling 计算错误.
- 发布创意剧场<千古剑灵>

2015.3.6
- Color can convert to and from string
- painter state(font, pen, brush, etc) are exposed to NPL.
- painter add save/restore state
- painter added set/get transform
- 旧GUI系统的全部功能都可以通过新的CPainter方式实现了
- 修复摄影机角色做后一个关键帧抖动的Bug.

2015.3.5
- MovieCodecPlugin视频输出当Encoding无法在30Frames的缓冲中结束时， 会先将FPS减半，直到恢复， 而尽量不会连续丢帧。
- 增加vectorpath, pen, brush, font class for painter
- 修复演员动作计算时间错误的bug.
- 修复以当前分辨率录制时前面几帧有窗口的Bug

2015.3.4
- Sprite渲染器增加绘制线段的底层API,并通过Painter接口开放API.
- Mobile版:android/iOS增加自动跟新模块, NPL层UI进度显示等完成.
- 增加多边形Polygon class.
- MovieCodecPlugin升级到版本3. 解决声音录制和视频录制不同步导致输出文件失效的Bug.
- MovieCodecPlugin 音频和视频，捕捉和编码分开2个线程。 Encoding线程是共用的(serialize IO write)
- 调整snow的默认大小0.1-->0.05

2015.3.3
- NPL.activate support explicitly or implicitly registered c++ file.
- 脚本层支持直接激活指定命名规则的C函数. 方便通过例如NPL.activate("helloworld.cpp", {})的方式快速开发C++层回调。

2015.3.2
- 动画系统增加EnableAnim属性， 可以全部用脚本控制动画帧数
- 人物每帧的动作全部改为脚本层控制, 包括动作的速率和动作混合Blending.  每帧的动作是精确且唯一的。
- 解决当人物首次出先在摄影机中时，动作从第0帧开始而不是正确的Timeline帧数.
- 更改人物动作编辑模式, 可精确拖动时间轴预览每帧的动作(支持速率与Blending)，动作默认不循环. 粒子系统除外。
- 电影人物默认为锁定状态, L键或点击解锁可以解除锁定，此时头部会跟随摄影机运动。 R键录制可以在上锁过程中使用，退出录制会自动上锁。
- 电影人物增加143奔跑动作.
- 修复/anim指令对9开头是指令失效的Bug
- 修复粒子无法在画板前显示的Bug: 所有3D UI前移到透明物体之前渲染。
- 修复DrawRect API coordinate system.
- 修复摄影机模型抖动的Bug
- 修复电影方块中模型有改变时， 动画时间原点计算错误的Bug.

2015.3.1
- Fixing NPL language service for hex display.
- CPainter 类增加了各种2d transforms, GUI的OwnerDraw事件默认在Client coordinate system中绘制.

2015.2.28
- Mobile版: iOS加入震动API, 增加protocol buffer. Java与NPL之间的类库改名为LocalBridgePBAPI.
- Mobile版: iOS加入memory info和open url 方法.
- CPainter类向脚本层大量连通,NPL层增加对应的ParaPainter. 整理GUI文件和类. NPL建立OwnerDraw控件的测试用例.

2015.2.26-2015.2.27
- 实现PaintEngineGPU若干方法
- 2D GUI引擎大量重构, 所有渲染全部改用新的CPainter类在PaintDevice上绘制图形和文字.
- 创意剧场发布<Paracraft下载链接合集>
- 资源管理器支持slot callback. 全部Signal类升级为signal2
- CGUIRoot成为了有效的PaintDevice.
- CPainter支持3D transform, 可以用Painter类直接渲染到3D场景中
- 重构IHeadOnDisplay 渲染， 也采用Painter渲染所有3D场景中的文字.

2015.2.25
- iOS版：AppleStore审核通过并上架， 更新官网
- 增加PaintEngineGPU和PaintEngineRaster类, GUIBase增加OwnerDraw属性

2015.2.24
- 新增2D辅助类: 2d helper struct including 2d matrix, 2d transform, lines
- 增加CPainter基类

2015.2.23
- Mobile版修复framebuffer 导致glClearColor失效的Bug.
- 修复pe:button with margin floating layout bug. 修复Mobile版人物选择UI错位的Bug.
- 新增2D辅助类: 2d helper struct including ParaPoint, ParaSize, ParaRect, ParaMargins
- 增加CPainterEngine, CPaintDevice, 基类。

2015.2.21-2015.2.22
- 新增Opengl版CRenderTarget类
- 重构MinisceneGraph类，从新的RenderTarget派生.
- Mobile版全面支持Miniscenegraph. Opengl 的frame buffer Texture增加FlipY.

2015.2.20
- Mobile版:异步IO重新启用, 但是由于用了非异步的底层IO类库, 异步效率比正常Client低一些.
- 恢复AddEvent命令, 修复哈奇中双人坐骑失效的Bug.
- 视频输出插件版本号升级, 下次更新时会自动提示下载新的插件，新版插件已经上传到了官网。
- 修复UI渲染同时有Scaling和Rotation时后者失效. 例如修复哈奇中捕鱼的UI.

2015.2.19
- 视频导出插件重构: 采用C++ 11 threading更加跨平台一些。
- 视频导出插件将截图和压缩分成了2个线程处理, 解决高清视频输出有时会卡顿的问题。
- 修复哈奇版创意空间实数地表失效的Bug.

2015.2.18
- Mobile版在iOS的TestFlight上申请了测试，邀请了若干朋友参加（最多1000人）

2015.2.17
- 所有物体位置信息从float改为double， 所有相关API调整.
- 摄影机所有数据从float改为double，优化摄影机矩阵精度.
- 一定程度上解决了摄影机缓慢移动时，会轻微抖动的Bug

2015.2.16
- 修复自定义方块的Action无效的Bug.
- Mobile版:iOS更新了ipa内测包; build for distribution, submitted to iTunes Connect for review.

2015.2.15
- Mobile版修复震动API导致删除方块或人物降落时崩溃的Bug
- Mobile版内置论坛下载链接更新
- Mobile版增加了远处的雾化效果
- 测试期间官网下载全部采用蒲公英提供的无需审核的超链接. 并向各大APPStore上传了rc7的更新.
- Mobile版： 修复部分内景世界无法在正确位置放置方块。比如桃子的轮船之谜。

2015.2.14
- Paracraft手机版v1.0发行: android/iOS.
- 重做官网下载页面：包含了所有版本的下载链接。 调整论坛的部分布局和内容。
- 创意剧场：发布《Paracraft手机版发行啦》，写了给用户的一封信。

2015.2.13
- Mobile版: 电影编辑模式下不隐藏运动按钮, 仍然可以控制人物
- Mobile版: 修复SetMousePosition(-1000,-1000)失效的Bug. 造成手指离开后， 仍然会Picking上次的位置。
- Mobile版: Android版修复totalMemory在API level < 16时crash的问题. 去掉了测试相关的activity(baidu related, and webview)
- Mobile版: Android版用testin云平台测试了200个机型，通过率90% (没有通过的大概是X86机器)
- 豌豆荚Paracraft官方App认证通过：预约了豌豆荚在2月14日首发Paracraft创意空间手机版
- Mobile版: 打包流程增加了main_mobile_res.pkg.  目前百科相关的大量XML文件都放入其中了。
- Mobile版: 修复iOS版百科模块无法正确通过文件搜索读取数据的Bug。

2015.2.12
- 导线模型支持Alpha通道：可用于部分自定义材质中
- 申请了Android AppStore发布资质: 百度91(person & company)， 腾讯应用宝(person & company)， 360助手(person)， 华为AppStore(company)， PP助手(person), 豌豆荚(person)。
- Mobile版在Win32下同样使用cAudioEngine.
- Mobile版: Android下修复/music 指令直接切换声音，第二个声音失效的Bug.

2015.2.11
- 引擎的PKG 打包系统支持Exclude选项（之前只有Linux支持， 目前全平台都支持了）安装包大小小了几兆.
- 中文名的模板文件在不同编码的操作系统间Copy时, 会尝试自动转码， 如果失败还会尝试默认路径。 解决Mobile版中文模板无法读取的Bug.
- Mobile版: 登录页加入了制作群, PC端下载链接等内容.
- 更新整理了www.paraengine.com上的官网信息，团队介绍等
- Mobile版:文件搜索功能增加上次修改日期的读取
- Mobile版: 删除默认世界， 本地世界按照修改日期排序， 并同时显示创建和修改日期。

2015.2.10
- Mobile版: 点击飞行后人物出现在空中 地形默认高度为零，造成的. 可设置地面默认高度了
- Mobile版: 修复UI放缩模式下, MouseWheel区域计算错误的Bug.
- Mobile版: 修复UI放缩模式下, SetMousePosition计算错误的Bug.
- Mobile版: 新建世界可记住世界名字
- Mobile版: 保存世界提示修改, 修复一个资源缺失问题, Mobile端版本号与PC端同步随资源发布
- Mobile版: 修复由于Attribute.db不正常， 以及EncodingConvert不支持null string导致部分世界无法正常打开的问题
- Mobile版: 支持目录递归删除, 可以删除本地世界了.
- Mobile版: 支持半透明人物动画渲染
- Mobile版: 百科目录中文不显示问题解决, 并可直接创建， 优化显示。
- Mobile版: 下载世界后会自动清除WebCache中的缓存文件
- Mobile版: 非编辑模式支持背包和从背包中扔物品.

2015.2.9
- Mobile版: 修复删除文件后文件缓存中仍然有文件的Bug
- Mobile版: 长按下载按钮可以删除指定世界（如果下载失败，提供一种重新下载的方式）
- Mobile版: 设置中可以更改材质包了
- Mobile版: Opengl Texture支持同步和异步加载, 默认为异步,可通过脚本控制。IO和解压在另外线程.
- Mobile版: 修复每当glGetError出错时， 会导致一张贴图无法加载的Bug.

2015.2.7-2015.2.8
- Mobile版: 修复android下的frand函数, 修复部分粒子系统显示范围出错的Bug
- Mobile版: 实数地形系统在BlockWorld下彻底被禁用， 减少内存开销, 加快Loading速度
- paracraft论坛取消了手机版访问.
- Mobile版: 设置中支持UI放缩, 针对一些高分辨率的视网膜屏手机.

2015.2.6
- Mobile版: fix第一人称操作出错
- Mobile版: 系统图标Logo等更新为最新版
- Mobile版: 修复某些手机天空闪烁: infinite projection matrix flicker bug: when NDC.z*0.5+0.5
- Mobile版: 内存小闪退的问题：对于小于1GB的手机在游戏登录UI内告知用户
- Mobile版: 修复部分粒子系统不显示的Bug
- 创意剧场：《魔法的重要性》
2015.2.5
- Mobile版: 长按为编辑, 如果没有可编辑才是删除.
- 修复mcml:div background-color错误显示的问题.
- Mobile版: 电影方块中的角色长按为右键， 左键单击可以拖动. 所有的pe_slot支持正常的点击拖动。
- 材质包支持模糊匹配名称, 名字只要有50%是一样的， 就会采用。 首次加载材质包列表不会造成应用材质包失败.
- 官方材质包列表与推荐列表增加了硬盘数据缓存
- Mobile版: 修复切换材质包部分材质错乱的Bug
- Mobile版: 修复小屏幕手机放缩问题， Design resolution通过脚本层设置，与PC端一致.

2015.2.3-2015.2.4
- Mobile版: 修复材质包显示，支持zip文件内容和目录的搜索功能
- Mobile版: Fix NPLCompiler 文件目录名缺失的Bug
- Mobile版: iOS打包系统优化, 资源文件和Config移动到[git]/ParacraftBuild/res目录
- Mobile版: 登陆UI: 增加官网链接， 微信号， 百度测试页增加返回按钮， 推出按钮, 增加导入按钮
- SelectionManager 采用Weak Reference Count方式管理, 修复可能导致之前版本有Crash的现象.
- 新增命令:/msg  any text   通过MessageBox显示一段文字.
- 新增mcml max-height css style属性， 修复MsgBox文字过长，无法点击确认按钮的Bug
- Mobile版: 所有世界支持动态按需材质包下载. 安装包中默认包含了几个常用材质包.
- Mobile版: 修复中文目录路径材质包在Android系统下无法读取的Bug， 修复切换世界材质不变的Bug(没卸载Zip).
- Mobile版: 优化CI脚本， Win32/Mac下都可以自动打包

2015.2.2
- Mobile版: 鼠标Touch事件重新remap， 支持右键，拖拽，Mouse Hover等操作.
- Mobile版: 增加了退出按钮， 登录UI修正，百度测试UI加入Back按钮.
- Mobile版: Android 增加API可打开外部URL
- 可搜索Zip文件中的目录, 自动删除重复文件.
- Mobile版：GUI增加scissor rect clipping，支持多Viewport.  对于不支持Stencil的机器可用. 例如iOS系统.
- 修复/hide 命令无效的Bug
- Mobile版：修复鼠标事件在多Viewport下位置错误的Bug
- Mobile版：本地世界增加导入..按钮.

2015.1.31- 2015.2.1
- Mobile版: android版删除不必要的lua文件, 重命名dll为paraenginemobile.so
- Mobile版: 跨平台的鼠标事件封装和GUI层重构. 支持所有鼠标类事件的响应。

2015.1.30
- Mobile版: 增加对LOD人物的显示的支持
- Mobile版: 可换装人物系统模型部分完成
- Mobile版: 引擎iOS, MAC全套CI一键打包发布系统完成:32/64位Mac, iOS, iPA.
2015.1.29
- Mobile版: TextureEntity支持create from memory buffer for both OpenGL and DirectX texture.
- Mobile版: 实数Terrain引擎增加OpenGL shader, 统一了Terrain Texture 和TextureEntity的接口. 支持多AlphaBlending
- Mobile版: 实数Terrain引擎支持任意多层材质混合, 支持大的非重复BaseTexture
- 用户材质包系统升级: 改为异步按需下载, 支持默认材质包, 默认路径改为英文.

2015.1.28
- Mobile版: 修复EditBox中的文字输入事件.
- Mobile版：当有键盘时， Enter和SlashKey会激活Mobile版下的命令行和发送指令。
- Mobile版：修复哈奇运行测试中的一些Bug: ParaCharacter is reference counted, DummyInstance is not reference counted, fix multi texture mesh load error.
- 不存在的模型也有默认的移动速度.
- Mobile版: 修复无法判定目录是否存在的Bug.
- Mobile版: 暂时禁用更改显示分辨率的API
- Mobile版：Static模型支持多维材质, 取消物理面的渲染。

2015.1.27
- 删除了引擎对pcre的依赖, 全部改用C++ 11的std::regex, 不支持的编译器则为boost:regex
- Mobile版迁移实数地形引擎: Terrain Engine ported to mobile version.

2015.1.26
- Terrain引擎精简, 支持Attribute Model
- 修复非仿真天空显示Bug
- 哈奇1，2手机版预告发布创意剧场
- Mobile版: 增加servermode命令行，支持无显卡的模式下以命令行运行脚本，主要用于Mac下的CI.

2015.1.24-2015.1.25
- AttributeModel 支持rows,cols的方式遍历子节点
- IRefObject 也从Attribute Model派生, 再次减少Multiple Inheritance.
- SceneObject的所有对象(15大类)全部通过AttributeModel可以访问. NPL脚本层加入对测试用例
- Asset Entity, Animation Base class are also derived from attribute model.
- GUI, Scene, AssetManager, ViewportManager都可以通过AttributeModel遍历子对象.  所有资源Texture， Shader等可遍历.
- BipedObject人物可以遍历动作,模型, 材质等
- 新增命令: /dump [scene|gui|asset|all|view|player] 打印信息到Logo文件

2015.1.23
- ParaScene.attach() 针对非TileObject, 会自动创建ContainerObject并调用AddChild.
- C++层新增CBlockDynamicObject类用于BlockWorld物理仿真的基类
- C++层新增BlockPieceParticle，使用物理类和新的Object interface, 并开放接口给脚本。 使得Block碎片渲染速度提升30倍.
- Mobile版: Mac版32/64位通用包完成
- Mobile版: iOS的命令行CI发布脚本初始版本完成.
- Paracraft最终版的Logo, Icon和登陆器UI设计完成.
- Mobile版: 修复非全屏输入法android/iOS/Win32的Editbox无法输入超过1个字的文字。另外Win32的Mobile版也可以输入中文了.
- Mobile版: 增加IME的光标渲染和文本输入光标位置的计算

2015.1.22
- 重构3dengine对象继承关系, 逻辑更清晰. CBaseObject更加轻量,节约内存开销.
- 新增TileObject类, 作为大部分Quad-Tree 对象的基类.
- 取消了CBaseObject中IViewClippingObject的Multiple Inheritance, 使其作为直接基类，逻辑更清晰.
- 删除一批不用的类:例如OPCBiped, PositionObject, etc.
- CTerrainTile QuadTree也从基类派生， 新增AttributeModelProxy可以通过脚本遍历所有QuadTree上的对象
- QuadTree数据结构改变, 改为unordered_ref_array而不是List. Quad-Tree性能提升, 代码更简洁,自动管理对象内存释放.

2015.1.21
- 调整下雨等粒子的渲染次序， 可以透过窗户， 看到外面下雨。
- 新增DefaultFactory类, 用于注册自定义Class. 引擎推荐以这种方式扩充新的类。
- 重构CEffectSystem采用了新的渲染流水线，并改为通过脚本添加到SceneObject中，相当于一个独立的Plugin系统。
- 脚本可以通过SceneObject添加新的渲染对象类型

2015.1.20
- 修复AttributeField的ClassID 重复的Bug， 解决下雨等特效失效的问题。
- 修复子电影方块第二次播放时会误播当前帧一次的Bug。例如导致某些Command重复执行一次。
- 修复下雨时房屋漏雨的Bug
- 修复MP3音频解码的Seek function 会随时间递增误差的Bug。
- 重构BaseObject的渲染流水线。 使得新定义的Object可以自定义渲染流水线。

2015.1.19
- Mobile版在iOS下采用了和Win32下同样的声音cAudioEngine底层， 修复了各种Error
          全版本都可以播放所有支持的音频文件mp4, ogg, wav， 包括3D音效， Seeking等功能。
- 底层新增CContanerObject, 去掉了早期的DummyObject对象.

2015.1.17-2015.1.18
- 修复开启光影后， 部分模型为黑色的Bug， 例如方向箭头.
- 修复编辑MP3声音文件时，Seek会错位2秒的Bug.
- Audio引擎升级为跨平台支持mp3, wav, ogg等. 主要由于iOS至今不支持ogg, 但是用户作品已经大量使用。
- IAttributeField基类支持Factory Pattern. 可以通过AttributeClass实例化对象，增加宏使得新的派生类可方便的支持FactoryPattern
- 新增API.  ParaScene.CreateObject(obj_type), 支持创建任意注册类型的对象。方便扩展。

2015.1.16
- Mobile版在Win32下增加对键盘输入的相应，比如WASD可以行走.
- 修复Chunk更新错误导致删除或添加方块后，光照或模型没有正确更新或缺少面。
- Mobile版在Mac系统下编译了32/64位通用版，初步可运行。

2015.1.15
- Mobile版在Win32下增加disk search path.
- Mobile版修复TinyXML2的AttributeName不可有_ underscore 的Bug
- Mobile版在Win32下增加对命令行的读取，
- Mobile版尝试了一下哈奇是可以运行的, 修复了所有script runtime error。
- Mobile版修复Mac系统下的编译， 为CI做准备
- 增加AddDiskSearchPath方法， 保证在Mobile版在Win32下可以从当前目录读取数据
- 修复子电影方块的摄影机在播放时仍然显示模型的Bug
- 修复Toolbase Singleton底层Bug
- 所有特效演员的材质移动到texture/effect目录，优化若干特效演员的初始大小
- 增加了PlayModeController, 在播放电影时，可以改变视角。

2015.1.14
- PKG 通过后缀可区分32位和64位版本。 保证iOS安装包可以同时运行32位和64位编译后的NPL文件。
       Windows版也可以32bits/64bits exe共享目录了. PKG以_32bits.pkg / _64bits.pkg结尾.
- iOS版修复32位系统上Bool的Byte Align导致Crash的Bug
- 修复iOS版32位系统上Luajit的FFI不Export Symbol的Bug.
- iOS版tested on iPad2/ iPad3 / iPhone5s/ iPhone6Plus.   iPad2 with 512RMB will run out of memory and crash in some world, all others are fine.
- 编辑关键帧的时间成功时会Ding一声。
- 可精确调节摄影机的关键帧: 位置，角度等。 右键点击摄影机关键帧可编辑。
- 可设置电影方块的起始时间，方便放大时间轴，编辑一部分时间片段。
- pe:slider增加单步快进， 电影时间轴支持单帧移动。

2015.1.13
- XML节点取消了.n属性, 改了数十个文件，增加了一点点XML读写速度， 代码更清晰。
- Mobile版底层增加对重力加速度感应的事件支持.
- Mobile版设置中增加重力感应控制器，主要配合立体电影可动态改视角
- iOS版在64位真机上顺利运行了, 还有一些问题如声音。

2015.1.12
- 立体分离度可存盘
- 立体模式下左右眼屏幕的UI和3D场景都支持事件输入
- PC版电影录制UI增加立体输出选项
- studied gyroscope/accelerator for android/iOS
2015.1.9-2015.1.11
- ParaEngine建立64位版, 相比32位版没有内存限制。 缺点是Luajit暂时无法启用。 主要为了iOS平台必须支持64位版。
        DirectX, libcurl, lua, 等都为64位的版本，增加Is64BitsSystem引擎属性.
- Mobile版: 迁移ParaMovie类库
- Mobile版: 支持多Viewport渲染
- Mobile版: 支持左右眼3D立体输出（可在设置中开启）

2015.1.8
- 公司荣获了一个优秀动漫影视企业的证书。
- 修复动作编辑点击关闭后，动作错误的Bug。
- 修复开光影后， 推出到没有Block的世界， 人物是黑色的Bug.
- 修复粒子系统动态换刷新资源死机的Bug。
- 修复MCML pe_font 的换行计算问题
- Mobile版修复/sky tex 指令不可直接换天空背景的Bug.
- 修复粒子系统引用计数Bug
- 修复ParaXModel在程序退出时没有被释放的Bug.

2015.1.7
- Joined iOS developer program, deploying to real iPhone device.
- 修复2个材质包之间切换时， 缺失的材质不是默认材质， 而是上次使用的材质的Bug。
- 重构光影水反的透明人物渲染流水线。 解决在Deferred Shading模式下， 半透明人物的渲染问题。
- Precompiled header ParaEngine.h added to MSVC via CMake and added /MP to turn on multiprocessor build. Compilation is 10 times faster than before. 受到iOS XCode的启发， 加入了CMake Precompiled Header ParaEngine.h 和/MP目前ParaEngineClient.dll Full Rebuild只需120秒，Mobile项目只需75秒,  比之前快了10倍左右。 极大增加开发速度。
- 所有没有4号动作的人物模型，默认有每秒4米的移动速度。解决一些特效类人物无法扮演移动的问题。

2015.1.6
- 半透明Block（例如冰块，玻璃板）在使用Deferred Shading模式渲染时可以正确渲染了，暂时不支持此类物体的反射和投影。
- 优化一批memory allocator and data object types for scene rendering.
- Paracraft iOS版编译通过, 修复一批编译器错误.
- iOS版：首个可运行版本完成。

2015.1.5
- 人物随光照距离的衰减从指数改为线性，人物会比周围Block亮一些，在黑暗中的人物更清晰一些。
- 修复使用最后一个物品后，人物手中物品模型不消失的Bug.
- 修复打开的Chest渲染会漏出周围的多边形。
- 新增EntityEditModel基类， Entity增加GetEditModel()方法， 提供了一个统一的Editor访问接口。
- 支持给电影角色起名字，方便查找多个角色
- 电影方块中的角色列表支持翻页和更多演员的显示， Tooltip中会显示演员的名字
- 修复本地世界文件排序错误
- 修复时间轴缩短时，红色标尺会消失的Bug.  C++ GUI底层UpdateRect的问题.

2015.1.4
- 修复另一个光照线程在退出世界时Crash的Bug
- Mobile版修复某些场景UI控件的ZValue不在最前端和3D场景冲突的Bug.
- 2014年Paracraft总结与2015年展望： 2015是工具研发（IDE）与产品起步的一年；开启NPL语言开源与开放化的征程。

2015.1.1-2015.1.3
- ParaEngine底层对象管理升级, 引入AutoReleasePool, 大量类文件的引用计数管理重构.
- 统一了所有底层对象基类RefObject->IObject->IAttributeObject->2D和3D base classes.
- 实现了定制版的单线程高性能WeakReference与IObject。 常用对象的底层增加了weak reference的支持.
- all tile visitors uses weak reference to keep track of bipeds.
- 所有脚本层C++对象使用WeakReference, 例如ParaObject, ParaUIObject, ParaAttributeObject. 保证脚本对象永远不会Access Violation.
          因此所有脚本层编程规则改动：不用每次用object id 验证对象有效性， 脚本中建议长久保留ParaObject, ParaUIObject等对象，通过IsValid() 可以查看对象是否存在, 即使不存在也不会出错.
- 脚本层缓存并优化几个常用的Singleton C++ API对象. 例如ParaCamera.GetAttributeObject().   每次只通过WeakReference 查看IsValid().
- Mobile版修复外部动作如坐下不加载的问题
- 修复HeadonText在某些角度不显示的Bug.
- 修复同ID多材质方块材质被错误合并的Bug. 例如有2种状态的按钮的渲染.
- 修复程序退出时可能报错的Bug(光照线程被错误终止导致)
- Mobile版修复Unicode substr错误; 修复脚本层Text自动换行脚本有时错算一个字符的Bug; 修复MCML中文字换行渲染错误.
- Mobile版修复NPOT(non-power of two) Texture显示不全的Bug。


Older Change logs:
     [ParaCraft Change Log 2014]:
     http://www.evernote.com/l/ALHh68tIAJpBiYyDRKsUQLwqJRbmij2BN-4/