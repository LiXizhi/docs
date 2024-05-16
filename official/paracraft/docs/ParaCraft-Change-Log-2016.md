# ParaCraft Change Log 2016

2016.12.28
- updated download page and installer on official website
- updated projects wiki page with all sponsored projects.
- becomes a lagou vip.
- released NPL CAD 3.2 video tutorial.
- /sound command now support url as well.

2016.12.26
- fix fly using camera direction
- add sendemail addresser
- Fixed jumping from slab block

2016.12.15-2016.12.23
- NPL meta compiler v0.1 finished, v0.2 is on its way.
- various GIS projection is studied, a coding project is started.
- 3D printing service is developed using NPL web server by third-party teams, 3D printing service integration is added to STL exporter.
- distributed git (or Spokes in github) are thoroughly studied and coding project planned.
- CephFS distributed file system as used in gitlab is studied.
- chrome embedded framework plugin v0.1 for paracraft is finished.
- fixed dll dependency when dll is loaded from a different folder than the main executable.  Security warning is added.

2016.12.14
- ace.js editor is upgraded to latest version, and support Chinese IME
- requirejs added for wikicraft mod interface.

2016.12.10-2016.12.13
- wikicraft mod command interface 30%.
- force physics added for mesh and bmax model.

2016.12.5-2016.12.9
- fixed working directory path under linux
- paracraft lecture for 3 days.
- finished NPLCAD tutorial and course  works
- updated paracraft website and upgraded server.
- Chrome Embedded Framework Mod for paracraft (80%)
- suppressed warning NPL.FromJson with empty data
- certificate supported via options in NPL.AppendUrlRequest();
- discussed possible augmented reality application for existing text books.
- json decode is os.geturl is now automatic
- added two filters for load and share world.

2016.12.3-2016.12.4
- /music command now support http url file
- /voice command added to support free text to speech service provided by baidu.
- NPL CAD video tutorial part 3 finished.
- Paracraft course work refined and uploaded all videos to baidu yun pan.
- fixed step block sound for slab block
- WorldShare mod 10%

2016.12.1-2016.12.2
- System.os.run now uses mktemp under linux for temporary files
- paracraft course work written.
- NPL's activate function may be extended to support multi-threaded callback via meta programming.
- ParaEngine attribute "ProcessId" added.  and System.os.GetCurrentProcessId added.
- Paracraft Rebranding project and docs are added to github
- HttpFiles added for paracraft

2016.11.30
- System.os.run now support linux bash shell script
- System.os.runAsync added
- Gitlab.com studied which is an open source github implementation.

2016.11.23-2016.11.29
- GIS studied with beijing university professors: geographic information system research center.
- wikicraft mod interface designed and implemented (50%).
- send email now support utf8 encoding by default.
- NPLCAD tutorial 1 published.
- fixed default log level in dev mode in paracraft.
- NPL Meta-programming project started (10% designed doc done).
- NPL CAD 3D algorithms project started (10% requirement done) .
- popen and window resposition test case added.

2016.11.23
- refined NPL wikipedia article
- BipedObject now supports polygon-level physics
- Physics can be turned on for all Entity object in paracraft.
- Embedding NPLRuntime wiki doc added

2016.11.19-2016.11.22
- NPL CAD performance improved.
- NPL CAD uses copy on write policy.
- NPL voxelizer performance improved.
- NPL CAD video tutorial part 1.
- Adding parameterized examples to NPL CAD
- NPL CAD added axis, log, coordinate system and mouse input conforms to paracraft.

2016.11.18
- added NPL to wikipedia, and paracraft to baidu wiki.

2016.11.14-2016.11.17
- refined package manager user interface for npl packages.
- NPL package manager final version is published.
- NPL world uploader project opened for recruitment on coding.net
- NPL cad project opened for recruitment on coding.net
- added baidu wiki for npl.
- paraengine dll can now be loaded from zip archive with a security warning.
- added mc importer to paracraft mod web site.

2016.11.9-2016.11.13
- plugin loader can avoid duplicated versions
- refined settings page and shader effect is now persistent between application restarts
- fix mcml v2 window esc key logic
- paracraft package manager released updated documentation and refined plugin UI
- wiki doc for NPL is improved, fixed doxygen error added some new topics like attribute system and async loading.
- NPL CAD project is refined and published to paracraft mod site.

2016.11.8
- fixed json reader
- implemented json writer in NPLRuntime NPL.ToJson

2016.11.4-2016.11.7
- NPL CAD refined, added block item, fixed utf8 file names, etc.
- NPL package merged.
- asset monitor autorefresh added in world folder.
- jquery interface is changed for both mcml v1 and v2 to make them compatible with standard.
- NPL debugger now support debugging files in dev folder.

2016.11.2-2016.11.3
- fixed @p for entity block.
- wikicraft project discussion.
- mcml v1 and v2 jquery interface is unified and support node creation using the Page or mcmlNode object. Added `.value()` for setting ang getting value.
- An example of two-way databinding is written in wiki doc and test file.
- System.window now supports esc key to close attribute when showing with mcml v2 params.
- /open mcml2://filepath  is supported to create window with mcml v2

2016.10.31-2016.11.1
- CParaFile now support pure memory file for binary data serialization.
- chunk generator now support async mode.
- in memory chunk class implemented.
- Physics Model now support inventory like command block and triggered when user clicked the model.
- packetClickEntity implemented for all block entity
- EntityBlockModel now support onclick event and inventory bag

2016.10.28-2016.10.29
- Entity Block Model (bmax) can be synced in server mode.
- mac OSX server version is done.
- fixing warnings and minor typo on OSX clang compiler
- added async chunk generation interface

2016.10.26-2016.10.27
- smtp protocol supported and System.os.SendEmail added.
- fixed command manager bug.
- sky submesh now support alpha blending, etc.
- FBX material now supports render order via _l[0-999] material name.
- tableDB now support replaceOne method. db_manager can now remove fields.
- block model supports relative to root directory.
- npl package manager merged into wiki mod.

2016.10.25
- fixed /tip channel
- added filters for "PlayerHasLoginPosition", nil, x,y,z:
- fbx material class now support unlit, no z write attribute just like parax file format.
- sky sub mesh with unlit material will be rendered as it is
- added wiki doc for filters and events

2016.10.23-2016.10.24
- fixed plugin loader for pre-installed namespace.
- CS GUI wiki doc.
- merged localinstall and npl package manager.
- /runat @p supported for last trigger entity
- fixed RunCommand not honoring server side code
- fixed /clearbag not clearing block in hand
- fixed window frame autosize property with _ct alignment
- /open url now support open mcml page at the center.

2016.10.20-2016.10.22
- fixed username on client side.
- fixed @playername for a dozen of player related commands like /scaling /facing, /velocity, /gravity, /take, /give, /clearbag, /say, /set, /walk, /lookat, /disableinput ...
- a trip to beijing open university.
- item block color is now saved to item stack
- /tip now support color and duration.

2016.10.19
- *.FBX is supported in addition to *.fbx
- fixed win32 window style changed but screen size not updated
- Added documentation for paracraft filters
- added new attribute IgnoreEyeBlockCollisionInSunlight to camera attribute. or `/property set -camera IgnoreEyeBlockCollisionInSunlight false`
- fixed neighbor chunk update for vertical chunk borders.
- Added filters for GUI desktop, mod interface now also use filters

2016.10.18
- remote texture now support https in additional to http.
- postfields supported in NPL url request to send any binary data in http request
- os.GetUrl now supports json as content type, refined wiki doc.
- merged mac osx build for all platforms.

2016.10.17
- NPL package manager v1 finished.
- fbx material class now support category id.

2016.10.15-2016.10.16
- fixed binary data in NPL's http body
- NPL web server now support multi-part post, such as for uploading binary file.
- File uploader example added to NPL web server.
- assimp is now built with CMAKE and integrated to NPLRuntime and client.

2016.10.14
- added filter for default context, added demo in paracraft test mod.
- documentation for mcml layout and scene context is written.
- tabledb now support delete method.
- paracraft android version fixed and rebuilt.
- fixed page resume called when page is still running

2016.10.13
- all query fields in tableDB will automatically create index keys.
- deleteOne now support empty query field
- fixed a number of warnings for clang MAC compiler.
- listened to a lecture for n-dimensional meditation.

2016.10.11-2016.10.12
- the global log function now except non-text as well
- non client area test is supported in GUI engine and windows title can be hidden under windows platform.
- ShowWindowTitleBar attribute added to toggle title bar
- mcml v1 and v2 now supports inline css-like style, updated wiki document

2016.10.9-2016.10.10
- rqlite & raft planned for tabledb
- lots of refactoring of NPL packages: moved localserver to system folder
- NPL wiki doc mcml related documentation done.
- NPL package site 60%
- paracraft MAC version stage 1 complete
- paracraft mod can now generate visual studio solution file.

2016.10.7-2016.10.8
- video tutorial for ParacraftMod: part1
- 3d printing sales company
- fixed npl file monitor for multi-website and multiple root directories.
- fixed teleport stone with neuron transmission and wiki doc

2016.10.6
- console.page is refined to avoid page refresh and embedded log window.
- log.page refined to support filtering and more text options.

2016.10.4-2016.10.5
- count function implemented in tableDB
- id set intersection and union helper class added to tableDB
- compound key in TableDB now supports ascending and descending order.
- fixed line ending of script solutions for hundreds of files.
- Plugin manager are fully implemented and added in main package
- all kinds of queries in tableDB now support multiple keys with intersection.
- ignored access log for localhost

2016.10.2-2016.10.3
- TableDB index now uses BLOB data as primary key for fast ranged query on secondary key indices.
- TableDB full table scan now support ranged filter.
- TableDB refined and supported Compound keys and updated wiki documentation.

2016.10.1
- TableDB manager page added in NPL code wiki
- fixed file system watcher bug in scripting interface
- upgraded C++ file system watcher interface to support win/linux/macOS
- fixed asio steadyTimer not called under linux

2016.9.28-2016.9.30
- NPL luasql module now support postgresql if it is available on the system during compiling.
- Table database now support ranged query and pagination with offset and limit.
- refined NPL wiki doc.
- NPL package manager (40%), Table DBManager (50%)
- Deferred shading light geometry pipeline added.

2016.9.27
- MAC OSX supported for server version
- "dev" command line now supports using current directory.
- "loadpackage" command line parameter supported

2016.9.24-2016.9.25
- fixed relative wiki web root path
- fixed npl web page first line must begin with <?npl
- refined rendermatrix api and refined light object

2016.9.22-2016.9.23
- refined NPL doc
- started NPL package manager project on coding platform
- fixed low-level singleton classes destroy order.
- B2 SOHO doc reviewed
- NPL for MAC OSX reviewed with two candidates.
- ParaEngineAPP is now reference counted.
- Fixed /goto command @target
- Add /runat command: /runat @all /tip hi, everyone

2016.9.21
- Redirect IO refined, and added interpreter mode for NPL runtime.
- Fixed some crash bug in command line mode.

2016.9.20
- Fixed table database index rebuild bug
- deferred light geometry implementation started with partners
- NPL package manager design doc written and project started.

2016.9.19
- fixed block physics reload bug
- recruiting and education for programmer
- deferred shading of light geometry studied.

2016.9.18
- audio midi api volume can now be changed with global audio settings
- fixed replaceblock task recursion bug

2016.9.17
- Fixed a haqi startup bug
- Write NPL Web Dev Tutorial Doc, making a 46 mins  SDK tutorial video.
- Refined web development toolchain pipeline.
- Reviewed design doc on wikicraft web site.

2016.9.16
- NPL vs extension fix: breakpoint set is now async. Changing default server from localhost to 127.0.0.1.
- ParacraftSDK removed src folder and added NPL web server example with code wiki.
- NPL package main added NPL web page documentation for vs extension.

2016.9.15
- fixed web server virtual host, so that we can host multiple website on the same port.
- "npl_code_wiki" can be used as internal rule_id, such as in 127.0.0.1
- web server test web site refined.

2016.9.9-2016.9.14
- wikicraft website team building and initial project commit.
- BlockModel now supports fbx file, fixed coplanar index.
- opened MAC version project on Coding project.

2016.9.8
- deferred shading for custom light geometry is discussed with partners
- ParaXModel now supports `_p` to explicitly specify physics in additional to `_a` to explicitly remove physics from model material.

2016.9.7
- fix bug: hand tool is now deselected when leaving the world
- wiki web site stress tested with loadimpact and loader.io. Minor fix a host name issue.
- done some recruiting from coding.net
- space key or jump to get off rail car. fixed rail bug when mounted client player is off when going down a slope

2016.9.5-2016.9.6
- fixed "table" field type in table DB.  Fixed a minor bug in row validation.
- added stats model to wiki site.
- design doc of wiki site 20%
- published project to coding.net for recruiting.

2016.9.3-2016.9.4
- log level added to NPL runtime. NPL web server will use lower log level
- log_service added to NPL web server
- npl web server browser cache control configuration added

2016.9.2
- ParaIO.GetFileInfo api is added to replace lfs library. The new api takes all search path and dev folder in to consideration.
- npl http file handler now support memory caching and auto compression with gzip

2016.8.31-2016.9.1
- officially start project for wiki site, initial design doc and team building.
- NPL summer of Code is finished, three projects reviewed
- `beautiful mind` 3d animation is refined and published to all platforms.

2016.8.30
- `/show physics` command added.
- BMAXObject now support full physics, ParaXModel added reading physics API.
- Added new block item `PhysicsModel` which uses physics from the bmax model. wiki doc updated.
- improved image/model item icon to show filename
- EditModel Task and manipulator added for BlockModel editing
- EntityModel accurate polygon-level physical 3d picking supported.
- bmax model now support scaling with physics

2016.8.29
- fix bmax attachment pivot attachment position.
- bmax BlockModel now support click to move to mount position.
- fixed block piece object animate() function not called when window is minimizied.
- fixed neuron manager event ignoring trigger entity
- fixed TeleportBlock logic in network mode.
- fixed ItemCommandLine can not save two consecutive empty space characters
- fixed /loadtemplate command's relative or abs path
- Movie clip start time can now be saved.

2016.8.26-2016.8.28
- fix bmax mount position and bone attachment name mapping.
- Ansible IT management deployed and studied
- Anhui University Summer Project: <beautiful mind> published.

2016.8.25
- fix EntityImage expansion in network mode.
- command /home /goto can now run on the server side

2016.8.24
- wiki site 65%: support multiple domain config for external authentication. wikicraft domain name registered.
- fix HTTP headers normalization for some old browsers.

2016.8.23
- wiki site 60%: user profile page added, page and site model added.
- profile image angular-identicon implemented

2016.8.20-2016.8.22
- NPL Summer Of Code: HTML5 monitor: 70%.  GitUploader:50%. NPLCAD:50%
- wiki site 50%: subscribers logics done with pagination.

2016.8.19
- red/blue stereo view added in addition to left/right eye view. `/stereo red` to enable it.
- viewport now support custom renderer and render target.
- fixed entity mount sync in server mode
- TakeScreenShot API now support async mode for HTML5Monitor project.

2016.8.18
- designed NPL cad language reference
- fixed reflection rendering with multiple viewport
- fix viewport change when render target is changed. fix alpha block rendering in multiple viewport.
- added /sky black command
- added red/blue stereo shader

2016.8.17
- Fast Approximate Anti-Aliasing (FXAA) added for shader 2, 3 or 4 (merged from papercraft code)
- Merged a number shader related changes from papercraft project
- shadow map improved with percentage-closer filtering

2016.8.16
- Fixed a tricky bug that: boost::asio::async_write may crash
- NPL.reject now support gracefully disconnect

2016.8.15
- merged pull request to add connection reason and file remove api.
- merged pull request to fix server nid on private server.
- all references to change logs has been moved to github.

2016.8.5
- /teleport command are made local
- /move command is now handled by entity function so that server can set client player's position regardless of client reset.
- Server can now handle commands entered on the client's console with proper fromEntity set.
- auto sky color is off after /sun command
- server side remote player teleport logic is done. A new packet PacketEntityMove is added.

2016.8.4
- fixed networking issues for ridding entities
- fixed riding entity rotation animation syncing.
- Entity manager now supports active chunks, all chunks with players on the server side is also active.  This will frame move entities like rail cars even it is far from main server actor.
- fixed numerous small bugs in pos/rot syncing
- fixing teleport packet pitching in railcar

2016.8.2-2016.8.3
- object with custom renderer will also call view touch method.
- model multi user base is implemented.
- wiki site 20%: project manager and loader
- fixed player unmount rail car on server side during log out.

2016.8.1
- added history button to paracraft.
- fixed apply chunk API with different meta data field.
- Fixed page yielding with concurrent calls

2016.7.30- 2016.7.31
- table db now support multiple indices with non-unique key values
- wiki site 10%: new project page

2016.7.29
- merge load block with unknown id bug fix
- fixed table db unset indexed field bug
- refactored model api for wiki site.
- fixed biped blockworld physics when there is ceiling blocks

2016.7.27-2016.7.28
- ItemToolBase implemented to support task command based item.
- Fixed rendering: sky texture gaps
- wiki site 10%: user model and github access tokens
- haqi 3v3 logics changed.
- HTML5 monitor: 20%.

2016.7.26
- added flood/remove pen to Paint brush filter.
- Terrain filters will take water into consideration and automatically snap non-solid block to surface.
- Fixed a low level rendering bug when neighboring blocks are set dirty in the same frame, causing one or two blocks not updated.

2016.7.23-2016.7.25
- new mcml editbox refined
- Task system refined to support UI and scenecontext in base class
- Terrain Filter Task now supports guassion, smooth, flatten, paint blocks.
- Terrain filter now support undo/redo and mouse dragging.
- TerrainPaintBrush and TexturePaintBrush fully implemented.
- All movie-related video tutorials are moved to wiki and properly annotated.

2016.7.22
- refined NPL wiki's networking section
- new mcml added pe_repeat tag
- fixed railblock with empty data.
- fixed im server check text limit, fixed empty name display, fixed random team login time in haqi
- movie background music can now have empty filename to stop music

2016.7.21
- serialization will now check for recusive tables by default to prevent stack overflow.
- fixed EntityImage tiling size
- fix actor recording when it is referenced by a parent link.
- fix actor recording when its movie block contains child movie clips.
- fixed scrollbar dragging without setting mouse capture.
- fixed client player entity not attached to entity manager
- fixed a crash if bmax model reference other models recursively.
- block stair implemented mirror operation.

2016.7.16-2016.7.20
- a trip to beijing for middle school teachers
- added TerrainBrush implementation
- fixed line ending of source code.

2016.7.15
- fixed a query position bug in haqi
- refactored Task base class to fully support SceneContext
- Added TerranBrush demo tool.

2016.7.14
- /anim can play any fbx or x file in current world directory
- NPL language service: fix goto function with underscore. Added `NPL Set Breakpoint here` in context menu.
- NPL HTTP Debugger now support list breakpoint, and add/remove bp even when debugger is not attached.
- /uiscaling command added.

2016.7.13
- fixed undo/redo of block creation or block fill line task with entity data.
- NPL language service now support function name with underscore _

2016.7.11-2016.7.12
- internal Hudson CI toolchain moved to VM server
- NPL runtime added MaxPendingConnections attribute.
- NPL Web Server now support dozens of configurations via XML file.
- NPL Web Server supports method HEAD
- log level change is printed to log.
- BlockImage and BlockItemFrame now support all six directions.

2016.7.7-2016.7.10
- Released recommended work: Chronicles of Mountains and Rivers.
- HTTP non-keep-alive is fully supported in NPL web server.
- NPL.reject now supports gracefully closing connection after all pending data is flushed.
- NPL.Compress/Decompress method added with gzip/zlib support.
- NPL web server will automatically compress text data when data is plain text and over a given size.
- Fixed NPL web server headers case insensitive.
- handles "If-Modified-Since" HTTP header to prevent duplicated resources.
- NPL web server fixed modifed date in zip or npl_package files
- NPL page file and response object added no cache header function.
- Apache Benchmark(ab) tool is tested with NPL server.

2016.7.5-2016.7.6
- Concurrency.Parallel class added for table db testing.
- Fixed under water selection effect
- TableDatabase now uses write ahead log. Wiki page updated.

2016.7.2-2016.7.4
- router model in wiki web implemented and designed. Refined ajax architecture for NPL code wiki.
- table database is reviewed with other people. documentation is refined.
- table database fixed sync mode message waiting. Added a few commands for sync mode API.
- BlockSlope is fully implemented with other people.
- db manager NPL code wiki page added.
- fixed world.page ajax call.
- fixed a possible crash when filename is null in NPL does file exist API.

2016.7.1
- refined NPL architecture wiki
- NPL for vs now support documentation folder, *.npl file and F12 to goto file.
- NPL main package added intelli-sense documentation for visual studio.

2016.6.29-2016.6.30
- web server model routing example created.
- Fixed npl_script handler with url parameter.

2016.6.28
- NPL web server will honor dev directory in its file system watcher.
- BlockSlope and model provider added.
- npl packages in dev folder are always loaded first.

2016.6.27
- NPL summer of code is started and gitter is added. 3 students enrolled.
- Paracraft wiki site is designed.
- NPL web debugger support reading source from npl_packages folder

2016.6.25-2016.6.26
- NPL preemptive activation file fully implemented (with debugger, configuration, etc) and documentation is written.
- This is Major breakthrough in concurrent programming for NPL.

2016.6.24
- HTTPS SSL server doc added for NPL
- NPL now support per neuron file message queue and preemptive neuron file activation. This give you the same  concurrency model as in Erlang.

2016.6.21-2016.6.23
- added /clearcache command and a button in setting page
- fixed EntityImage does not support url image.
- fixed C++ url image loading.
- NPL planning to add per-file message queue size.
- Get blocks in region now support verticalSectionFilter
- blockSign, blockImage, blockItemFrame can now be synced in remote world. Both client and server can edit these entities

2016.6.18-2016.6.20
- fix mouse release event not fired when two mouse button are both down
- fixed a block attribute not honor xml attribute
- fixed int overflow in haqi's db server API.
- studied concurrent programming model in web programming.

2016.6.17
- NPL performance compare wiki page is added
- math.bit is now always 32bits under lua and luajit.

2016.6.15-2016.6.16
- opening/closing zip archives are now thread-safe.
- all particle element will now keep a reference to its spawner object, rather than keeping raw pointers.
- Fixed batched element draw not cleared when scene is reset

2016.6.14
- fix: local chunk changes are commited to server before applying server patch
- fixed remote world block setting bug

2016.6.12-2016.6.13
- wiki site deployed hudson ci added
- fixed a animation crash bug when model without animation is animated.
- Music block can be toggled by power. When destoryed, music is stopped.
- Fixed entity portrait scaling
- removed save world tips when user is in remote world
- fixed fill line task does not inform neighbor changes

2016.6.9-2016.6.11
- wiki site support basic login/register/change password/change profile
- wiki home page demo added.

2016.6.8
- Fixed auto ci for packages/main
- jwt lib and hmac encoding implemented.

2016.6.7
- mini loader for wp-web site framework is done.
- private project paracraftwiki is added to github.
- site_config() can now return custom WebServer. config from server configuration files.
- fixed daemon mode without async module.

2016.6.3-2016.6.6
- wiki page architecture for NPL code wiki is done.
- fixed zip file comment reading.
- fixed css mine type for NPL web server.
- added nocache support for NPL web server.
- refined npl documentation.
- login/register page of npl code wiki is done.

2016.6.1-2016.6.2
- haqi: iptables limit 5 connections per IP
- waitflush command added to table database.
- improved overall documentation.
- CNAME studied and added for our wiki site.

2016.5.29-2016.5.30
- personal wiki site is supported with registration and basic github-binding.

2016.5.26-2016.5.28
- fixed ray tacing of blocks at rare conditions and improved algorithm performance.
- fixed /time command not changing time immediately. Update world sim update performance a little.
- investigated a lot about out of memory file corruption when saving to xml files, but without success.
- unified all async call interfaces of NPL web server framework. add a few functions to make making json response/request easier.
- fix extra space in actor overlay is lost
- fix actor overlay does not show up for the first time when its origin is not in camera.

2016.5.23-2016.5.25
- Remote NPC,mob sync in world client: spawn, delete, position, move, facing, scaling, asset, skin, handblock,  dropped item, and player inventory of modified items.
- LinkManip now supports undo/redo. Fixed render update dependencies.
- fix rail car and NPC position yaw not updated correctly in remote client
- /say command will work over the network for all kinds of entities.

2016.5.22
- NPL Runtime build travis-ci, will build latest boost from source and statically link to it.
- Added parent link to Actor NPC.
- ParentLinkManipContainer implemented.
- actor asset can now be "" or "0" again.

2016.5.21
- NPL Runtime (linux version) is now automatically built and deployed using travis-ci to github releases.
- `npl_packages/main` is created and packaged as sub module to NPL Runtime.

2016.5.20
- log.txt can be changed via command line or at runtime.
- all archive files can also be loaded from search paths.
- npl.load can also handle pkg or zip file.
- NPL runtime now use static boost by default.

2016.5.19
- search path is fully implemented.
- NPL.load now support automatically load npl_packages and add search path.

2016.5.18
- Fixed sql statement cache rebuild when sql schema is changed.
- sqlite db is opened with readonly tag when disk file is readonly under win32
- sqlite3 module is upgraded to 3.12
- Table database test case refined
- Table database support raw SQL operation in addition to CRUD command.

2016.5.17
- Table database optimization
- Sqllite statement will automatically garbage collect itself.
- commonlib.enable__gc added to oo.lua for table based garbage collection.
- NPL acceptor delayed loading network socket object.

2016.5.13-2016.5.16
- Table database implementation (100%) with test cases, performance test, etc.
- fixed NPL.activate custom queue priority.

2016.5.12
- Table database implementation (20%).
- fix headon display GUI order with alpha-blended blocks
- disabled all item events when redirect context is selected, such as during block selection.
- fixed head rotation and facing for player on the main server.
- fixed redo operation for block data when replacing block

2016.5.10-2016.5.11
- Fix writing to empty world client causing world template errors.
- fix url encoder on C++ side,
- NPL get url now support custom http headers.
- added Ctrl+S in npl console
- fix actor NPC roll,pitch recording keys.
- Table database initial implementation.
- Added NPL code wiki oauth2 login module for github, google, and facebook account.

2016.5.7-2016.5.9
- studied various programming courses such as: freecodecamp, udacity, edx(MIT,harvard), code, codeacademy, etc.
- added HasClosingRequest attribute for debugger. A debugging process can now always end itself.
- npl code wiki now support search by text
- npl console window now support multi-tab code cache

2016.5.6
- fixed url protocol install with utf8 file path. fix os.run with utf8 file path.
- refined npl debugger, added color theme, added F5 shortcut key, added close but this button. Ctrl+Alt+I to start debugger.
- camera's sub variable is now on the timeline
- day of time actor variable can be changed via GUI

2016.5.5
- Apply chunk refresh bug fixed.
- Server side chunk generator is enabled.
- fix zip writer forget to trunk file size bug.
- camera roll added for camera actor. Manipulators can be used for actor camera.

2016.5.4
- NPL debugger for visual studio code is finished.
- NPL code editor can now open absolute path.

2016.5.3
- fixed network client player's gravity
- fixed actor editor when position key is deleted
- fix 3d rotation undo key displaying wrong.
- refactored custom variable for all actors, making undo operation auto-working.
- fix scene context dragging operation interpreted as clicking.
- Fix transmanipulator with null input, runtime error.
- texture pack is now synced in remote server.

2016.4.30-2016.5.2
- NPLRuntime github project can now build full directX based client, with only boost and directX external dependency.
- fixed chunk lighting in remote client world.
- fixed chunk lighting bugs in certain cave situations.

2016.4.29
- improved apply chunk column data performance for initial update
- fixed url protocol install path error
- fixed search file api for NPL runtime under linux
- fix global template sub folder can not be opened bug
- fix multiline text aabb in actor overlay
- fix sun light calculation bug at the chunk border when calling applyMapChunk.

2016.4.27-2016.4.28
- fix month time display in zip archive.
- code editor now support run code
- fix apply chunk lighting not refreshed. Remote client lighting fixed.

2016.4.23-2016.4.26
- a trip to beijing for Chinese language forum
- NPL runtime can now be built under win32 without external dependencies but boost.
- fixed libcurl crossplatform building.
- Zip writer added, CreateZip api is supported on all platforms. Dropping dependencies on old windows-only ziplib.

2016.4.22
- Fixed adding wrong camera keyframe when paused
- ItemCode now uses NPL code wiki's code editor, and will auto detect file changes
- Fix GameLogic's file watcher interface to monitor all file changes in world directory. Added a filter and signal for file changes.
- NPL code editor support code syncing and context menu on its tabs. File context menu support, open externally, close, save, etc.
- added `prevent duplicate tabs` plugin in chromes.

2016.4.21
-  fix anim sequence with standing animation
- fix static fbx import with invalid static transform matrix
- NPL HTTP debugger now support context menu, set in readonly mode.
- NPL code editor will remember last edit position.

2016.4.19-2016.4.20
- fix disk priority when opening zip world file
- fix fbx skin weight
- NPL admin site upgrade from bootstrap 2 to 3
- sensitive theme improved and rewritten using bootstrap 3. Sidebar can now be hidden.
- NPL code wiki add code editor page, supporting filters and will ask user confirm before closing a file.

2016.4.18
- NPL Debugger in Code wiki is released.
- fixed fbx attachment matrix calculations
- fix FBX importer with embedded empty texture.

2016.4.16-2016.4.17
- NPL web server added local storage for angular as buildin.
- Haqi server is virtualized and moved to new server farm.

2016.4.15
- jquery ui resizable added to NPL web site framework
- NPL http debugger UI suppports source browser and setting breakpoints by clicking on the line.

2016.4.14
- fix synchronous msg queue pop error
- breakpoints, watch, call stack implemented in NPL web debugger UI

2016.4.13
- HTTP debugger implemented and NPL code wiki debugger.page added.
- synchronous NPL message function is added for HTTP debugger

2016.4.11
- Heat beat will reset msg global variable to nil.
- fixed saving actor static appearance. Fixed a default avatar skin texture.
- cmakefile for luajit is added to npl runtime. NPLRuntime uses luajit by default
- fixed wire block rendering potential crash.
- fix a crashing issue when applying chunks.

2016.4.9-10
- added some NPL documentation
- FFI is planned for CSG implementation.

2016.4.8
- DialogItem is added and published with editors written in HTML5/angularjs/NPL.
- NPL wiki added Client/Server demo code.

2016.4.7
- fixed nested double brackets long string in NPL HTTP post request
- fixed IPC debugger stack walk with C function
- allow json encode with empty array.

2016.4.5-2016.4.6
- EditDialog page fully implemented
- Head rotation packet is correctly handled by the client.
- fix dragging block template file to window lost block meta data
- block model item now supports standard block template file
- bmax model in block model item can now be unpacked and edited

2016.4.1-2016.4.4
- NPL language service: added support for code snippets.
- added new command: /virtualitem [@playername] [add|remove|get] [item_id]  add, remove or get a certain virtual item to a given player
               /virtualitem add quest1111
- Dialog rule now fully support triggers
- angluarJs added to webserver framework for MVC web pages.

2016.3.30
- Write NPL Server Page Wiki
- NPL mysql plugin added to github and added related wiki page.
- CAD plugin(10%): CSG (constructive solid geometry) implementation in NPL.
- NPCDialogPage added for displaying dialog
- ItemDialog added which will trigger dialog when activated.

2016.3.29
- NPL debugger 2.0 released: call stack implemented, attach UI and dll registration improved.
- NPL IPC debugger now fully support luajit by fixing stack level when stepping over functions. One no longer needs to switch to standard lua dll for debugging.

2016.3.28
- basic dialog rule item added
- NPL language service: support goto definition for all opened files and those defined in xml conf.
- /doygen command now supports exporting all source code file name and line number to be used by NPL language service

2016.3.25-2016.3.27
- fixed url protocol install bug. Run as admin io redirection fixed.
- NPL language service: using nuget packages to manage dependencies.

2016.3.24
- NPL cad plugin design doc done. Project is started.
- NPL language service: fixed hex number display, added highlighting for functions and self identifier, fixed some lua 5.1 syntax.

2016.3.23
- a trip to Beijing to meet some university teachers.
- updated NPL wiki for basic concept.

2016.3.22
- fix unable to list world when tag.xml is missing.
- fix file system watcher causing app not exit completely bug
- added NPL web server demo to SDK
- fix an include bug with NPL web server
- NPL language service published with version 1.8, updated documentation.

2016.3.20-2016.3.21
- NPL language service: HTML/page mixed mode highlighting added.
- NPL language service: fixed idle parsing and outlining support for NPL code.
- NPL language service: function navigation window implemented.
- NPL language service: parsing errors will be highlighted in code.
- NPL language service: quick info added.

2016.3.18-2016.3.19
- fixed player physics on server
- NPL page highlighting supported in NPL language service for visual studio

2016.3.17
- Writing NPLRuntime Wiki (25%)
- Published a trailer video for education and introduction of Paracraft.
- NPL web server's include() now support refresh.
- fixed FFI binding in NPLRuntime.

2016.3.16
- added open.page in code wiki
- Quest system implemented: an item based quest system with advanced data item exchange rules.
- ItemRule and editor added.

2016.3.15
- EntityItem has physics again
- ItemTool： 方块硬度，工具，多方块Damage缓存， 掉落，掉落物理仿真

2016.3.14
- picking result added
- BlockDamageProgress added , WorldSim support damage block partially function.
- ItemTool demo code added

2016.3.11-2016.3.13
- Writing NPLRuntime Wiki (10%)
- 制作剪辑了一个3Mins宣传视频 for course works.

2016.3.10
- CI to automatically sync svn to git
- fixed NPLRuntime install on ParacraftSDK

2016.3.9
- fix AABB calculation of FBX file.
- fix fbx animation importer for splitted animations.

2016.3.8
- Patent for camera shooting reviewed.
- fix NPL runtime CI with higher boost 1.58 version
- fixed terrain generator with empty chunks when teleported to a new location.

2016.3.3-2016.3.7
- a trip to shanghai taomee.
- finished tunnel service: a proxy server/client that allows private client to communicate with private server
- added command: /tunnelserver and improved startserver and connect command to allow tunnel proxy.

2016.3.1
- fixed tiled image in image entity.
- fix shader shadow display after porting to linux
- service mode is by default disabled under linux, log append is only on for service mode under linux
- fix NPLRuntime bootstrapping under linux
- /blockimages command support 65535 colors with color blocks.
- NPL code wiki console.page now runs in a sandbox environment.
- request from localhost is always regarded as admin in default npl web server.

2016.2.28-2016.2.29
- NPLRuntime is now fully compatible with ParaEngineServer. Fixing mono dll, added IsServerMode attribute.
- NPLRuntime will automatically find and build NPLMono2 and MySQL plugins under windows and linux.

2016.2.27
- fixed singleton delete of file watcher
- NPLRuntime can now be compiled under win32 with cmake.

2016.2.21-2016.2.26
- merged paraengine server into client code, NPLRuntime can now be compiled automatically on any linux/win machine.
- NPLRuntime linux cmake (100%):  project is now built automatically on third-party travis tool on github.
- NPLRuntime now has no warnings on gcc 4.9 and boost 1.55

2016.2.20
- NPLRuntime linux cmake (10%)

2016.2.19
- fix camera AABB display in play mode
- command editor is beautified when display in readonly mode.
- changed entity selection display method
- all movable entity will fire onclick event, which can be captured by command or code

2016.2.18
- fix camera AABB display in play mode
- fix haqi's transform maker display and fix sign item with modou.
- fixed publish script on linux CI server, installed latested vm for debian8/hudson, etc.
- backup and moved C++ svn server to central server.

2016.2.17
- study a number of cad software
- fix npl code wiki theme menu bug in narrow screen mode.
- ace editor added to NPL console

2016.2.16
- fix /gravity commands

2016.2.15
- curl 32/64bits client updated to ver 1.47.1, fixing a out of memory bug when downloading files from https site.
- AB is fully upgraded to perforce.
- 2016 new year planned: we should focus more on helping users to publish their works as many different formats and track their activities and provide directory services.
- removed Users.Delete API from haqi web server

2016.2.6-2016.2.14
- setup stunnel+squid server in hongkong server farm.
- fixing lots of CI scripts to use perforce instead of AB and external svn directly. Line endings and file modification times are preserved on perforce.
- a three day trip to guilin after Chinese new year.

2016.2.5
- fixed /velocity and /speedscale command
- fixed entity collision with non-physical block entity like detector block.

2016.1.29-2016.2.4
- our office is moved to a new place
- alianbrain 1000GB data moved to perforce

2016.1.28
- added actor selector manipulator, to highlight current selected actor
- added wiki contribute page with how to upload images, etc.
- added help button on command tooltip.

2016.1.27
- FBX model info class refactored, now support <anims neck_yaw_axis="x" neck_pitch_axis="-z"> attributes
- FBX wiki page refined, Paracraft WIKI page refined, removed master branch.
- refined old multiline edit control in NPL:  delete and backspace key logics are fixed.
- pe_block removed all dragging code, pe_slot is the only possible dragging item.
- pe_block added tooltip2 attribute.  In builder window, right click a block to open its wiki page.
- add command /wiki  item_id
- fixed line ending \r\n for all wiki pages

2016.1.26
- FBX parser now support attachment points. FBX model wiki page added.
- fix bone manipulator trans handle's coordinate system (from local to parent).
- all predefined FBX bone names are mapped to their ids.

2016.1.25
- fix System.os long directory name with special characters.
- HourOfCode v1 world finished.
- /wikigen will also generate table of content
- NPL.AppendURLRequest support -I option which is headers only.
- System.os.GetUrl() function added, which support HTTP(s) get headers only with redirection.
- /loadworld url command will automatically compare file length before downloading a file again.

2016.1.23
- /open -d option added.
- /wikigen command added. all wiki page place holders are added.

2016.1.22
- middle teleport key will ignore transparent block
- bone directions are automatically determined by searching its parent bone. Some animation is shown to aid the user.
- HourOfCode with Paracraft v0.1 is released.

2016.1.21
- refined personal website and paracraft website on github. fixed several code bug.
- write company info page for tatfook.
- fix pe_slot invisible drag receiver bug, causing item drag to lost.

2016.1.20
- refined help menu
- added /menu help.help.xxx.yyy command, such as /menu help.help.tutorial.newusertutorial
- url protocol is force installed when paracraft start. it is the primary way of communication between apps for all platforms.
- fix saving template to directory with unicode char.
- fix run as admin command error with unicode char in file path.
- fix different browser works differently for url protocol text encoding

2016.1.19
- added Paracraft project web page on github.
- added command /hasurlprotocol to check for command
- refined loadworld and url protocol

2016.1.18
- NPL's curl interface now support https, SSL and url redirection, so that we can download content from https://github.com/XXX
- added /registerurlprotocol command to register url protocol for Paracraft.
- support url protocol: paracraft://cmd/loadworld https://github.com/LiXizhi/HourOfCode/archive/master.zip

2016.1.16
- Web tutorials are all linked to paracraft github wiki, including every command, block and several other user actions.
- fix wire model display.
- alt+left click bone block to rotate it.

2016.1.15
- Added arrow block having 24 possible directions. id=255.
- lua_pcall now support reading back lua return value in C++.
- BlockEngine added "OnBeforeLoadBlockRegion" callback with return values

2016.1.14
- fix group id and sentient fields for network players
- overlay support relative position when saving as template file
- TimeSeriesCommand.blocks support relative position.
- /select -pivot x y z can be used to set pivot point by command
- /select -move x y z can be used to move selection to a given location.

2016.1.13
- tab key is disabled for tutorial mode.
- load world will mix zip and folder directory by time.

2016.1.12
- fix /sethome command and delete entity with same name.
- blocks actor can now remember entity data.
- multiple inline command $() can appear in a single command line
- $() support inline command with nested () brackets
- added new command /countblock x y z (dx dy dz) [blockid] [data]

2016.1.11
- can_jump rule will automatically affect can_fly rule
- /take and /give command now support server data
- block id in any commands can now use name in addition to id.
- added two filters for chunk generation.
- when export bmax file, an item model block will be taken in hand
- bmax and template files can be loaded via the template browser panel

2016.1.10
- some transient game rule are reset when a new world is loaded.
- refactored game mode logics to inherit properties from scene context

2016.1.8-2016.1.9
- added System.os class in NPL, which support ShellExecuteEx
- NPLRuntime installer script added to ParacraftSDK.
- updated nplproject.com website to add download links.

2016.1.7
- added /show mod command to show the plugin window. (also added to desktop menu)
- mod page has link to public wiki to allow user to download/publish mod online.
- /rule command refined.

2016.1.6
- fix event loading when calling /sendevent
- sync SDK src with full source code
- Entity allow force local property
- updated official website links and images

2016.1.5
- ShapeBox added to NPL math lib.
- ActorOverlay is fully implemented, supporting text, image, color, rect functions and text, scale, opacity, etc, properties.
- Bounding box and selection effect added for ActorOverlay.
- fix /spawn command total item count

2016.1.1-2016.1.4
- fix world.page file display
- added EntityOverlay, ActorOverlay, ItemTimeseriesOverlay to allow owner draw of 3D actors.
- NPL code wiki will serve files starting with ./www/ from current world directory.
- expose System.Core.Event table to creator API sandbox env
- fix painter context opacity when drawing text and textures
- protected call is used for item code.
- /spawn command will only spawn spawnable items in the inventory.

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

Older Change logs:
- [ParaCraft Change Log 2015](http://www.evernote.com/l/ALEEi65XWyJJt74x0QfDO5wZ4jk4R-nfuKw/)
- [ParaCraft Change Log 2014](http://www.evernote.com/l/ALHh68tIAJpBiYyDRKsUQLwqJRbmij2BN-4/)