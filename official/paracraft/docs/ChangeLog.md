## ParaCraft Change Log 2017
> Click [here](http://www.evernote.com/l/ALGymMtcwlJDT5c6frUlCQPzTAbHn8LqLwE/) for most recent daily log

2017.7.15-2017.7.16
- NPL Debugger watch window can now view table object in details.
- added commonlib.serialize_in_length()
- added calling log API example in nplruntime c++ plugin samples.
- kanban discussion for leaders
- /replace -all command support from_data and to_data
- NPL http debugger allow examine variables with namespaces like a.b.c
- changed command block response time so that it can detect fast rail detector.
- fix picking buffer render frame when there are multiple manipulators and not all are visible.

2017.7.9-2017.7.14
- haqi pay and login backend (30%)
- mc exporter 1.1 published to support new mc blocks
- fix offsetworld and add reset light method
- bmax model will now merge coplanar faces
- bmax model will now use lod by default
- several engine fix like editbox middle align
- region xml file uses compressed format when file size is bigger than 10kb.
- keepwork private project is ready to use.
- git.keepwork.com now support github login.

2017.7.6-2017.7.8
- fixed rail detector bug when car and player are top of it.
- kanban tutorial improved.
- git.keepwork.com now support keepwork.com account with github account binded.
- pov ray project started
- /show vision command added for debugging AI vision object.

2017.7.1-2017.7.5
- oauth interface for keepwork
- block region now support zip compression when file is bigger.
- Para XML reader now support reading from zip compressed file.
- attribute fields now support hash look up.
- training for kanban of project management and refined kanban.
- keep work payment interface and certifications.
- fbx particle system deployed
- numerous bug fixes in keepwork

2017.6.18-2017.7.1
- vision context in AI module
- tatfook wiki site
- keepwork now support private project
- haqi change operation company

2017.6.15-2017.6.17
- improved /end 1 command to allow a movie block to end immediately
- [1%] ModelShare mod designed and reviewed.
- Summer of Code 2017 begins and 4 students enrolled.

2017.6.12-2017.6.14
- TableDB feature complete alpha 1 finished. Review in progress
- Fixed enter text multiline
- fixed movie clip last frame not played bug.
- Android paracraft design goal complete.

2017.6.2-2017.6.11
- keepwork major release
- memory block added and implemented with a demo
- BMaxObject now support bone animations.
- Fix haqi onclose method of mcml v1 page not called
- Attended AI forum and monthly report
- Shanghai department is operational
- URL protocol is implemented on android.
- World Share stable version is online.

2017.6.1
- AI report 50% written on keepwork
- Chinese file name on gitlab
- enabled core dump on keepwork and improved CDN settings on git data source.
- refined issue pipeline and fixed several view issues on keepwork.

2017.5.26-2017.5.31
- fixed crash on visiting physics entity
- fixed world share with pagination on git source.
- added tab key in GUIContainer
- ParaX writer fully implemented

2017.5.18-2017.5.25
- fixed worldshare line ending
- CDN for keepwork tested and deployed
- cname and mx conflict and uses mail.keepwork.com for mail address.
- X file binary exporter in C++ alpha 1
- [10%] memory block file added and designed
- dozens of memory block test animations are made.
- New office design fixed
- Shanghai Studio for mobile and community edition.
- keepwork website editor redesign.
- world share fixed many bugs and uses commit id for CDN download.
- docker and mesos deployed for future operations.

2017.5.15-2017.5.17
- added __LINE__ to page file
- added ShowExitDialog filter
- edit box default empty text color changed.
- paracraft buildin mod released
- WorldShare Mod released and fixed many bugs.
- fixed esc key causing Page.OnClose called multiple times.
- fix stl exporter can not export bmax
- ParaX exporter mod fixed bug: merge coplanar faces and bone animations.
- reviewed block tower project.
- fixed crash on freeimage io reader
- CDN for keepwork reviewed and tested

2017.5.9-2017.5.14
- fixed ParaIO read/write
- lj_GC64 enabled by default in linux with luajit2.1 beta3
- added base32
- WorldShare and Keepwork project refined.
- ParaX exporter mod v1.0 finished
- Table DB raft phase 2
- paracraft buildin mod project done.
- added search zip file demo.
- MovieAI 10%: designed movieclip used as character AI for real world movement.

2017.5.4-2017.5.8
- NPL web socket merged to svn
- fixed block piece particle auto release.
- new office building

2017.4.24-2017.5.3
- console will inherit paraent console if any.
- fixed teleport to unloaded chunks
- NPL TCP connection support upgrade to web socket protocol defined in RFC6455

2017.4.23
- drag and drop zip file now automatically recognizes world,mod,blocktextures types
- build-in mod supported in paracraft.  System mod supported by pluginloader
- mod select page refined and shows total number of active plugins.

2017.4.20-2017.4.21
- NPL.load now support absolute file path in windows system.
- NPL.load folder now support zip package file and package.npl configuration inside package file is honored
- paracraft now support preinstalled npl package.

2017.4.19
- ShareWorldPage refactored
- Autonomous character animation project planned.
- ActorNPC's Animation list is read from parax file

2017.4.17-2017.4.18
- NPLRuntime sqlite3 support online backup API.
- /blockfilemonitor [x y z] [filename] added for monitor external bmax file

2017.4.3-2017.4.16
- paraxmodel animations exposed
- NPLRuntime support PCH under windows
- NPL.load now support package.npl with main script.
- NPL dc/os architecture doc written
- WSL(Windows subsystem for linux) is tested with NPLRuntime build process.
- vs 2017 can be used as compiler for NPLRuntime

2017.4.8-2017.4.12
- refined all help page tutorials and fixed tutorial progress bug
- custom buffer picking system done and tested
- NPL dockerfile added
- update documentation for 9-tile image
- update doc for buffer picking and encoding, update ask question section in NPL wiki.
- NPLCAD 3.7.1 video tutorial published

2017.3.29-2017.4.6
- report and meeting at anhui
- keepwork website pre-alpha online
- git data source implemented for keepwork
- fixed crash on some animated fbx model
- buffer picking api fully exposed and implemented
- CAD algorithm further studied.
- fixed mine-type for svg and a few other files.
- TableDB raft implementation stage 1
- paracraft build-in tutorials refined.
- Mesh without skin is static costing little CPU.
- added Encoding.Utf16ToUtf8 and Encoding.Utf8ToUtf16

2017.3.22-2017.3.28
- fixed physics mesh index error and uses 32bits indices for paraxmodel.
- wikicraft project tech demo released with gitlab datasource and a number of wiki mods.
- studied mesos+marathon+chronos for distributed operating system.
- studied docker containers in addition to vm
- New NPL Tools 30%
- Paracraft tutorial annotations for dozens of videos.
- fixed build-in tutorial task sorting by filename instead of date time.
- fixed png image reader with single colors.
- BMaxToParaXExporter 80%

2016.3.20-2016.3.21
- fixed epsilon in moving entity
- fixed shift key when creating blocks.
- fixed NPL.load return value with npl extension
- fbx diffuse color is exported.

2016.3.17-2016.3.19
- fix luajit 5.2 compat in script
- Async resource queue can now automatically grow when full
- Set/GetFieldCData supported for accessing big C++ data structure via ffi.
- ParaXModelAttr implemented for accessing parax file details via NPL

2016.3.15-2016.3.16
- paper world project reviews
- guid class added.
- std::thread crash with static boost in ubuntu and gcc 4.8.4

2017.3.8-2017.3.14
- NPL docs site implemented and published with attachable third-parties
- merged NPL MAC build to master
- enable_file_monitor attribute for npl_script_handler in web framework.
- reviewed third-party MVC web framework developed for NPL
- wikicraft renamed to keepwork.com, deployed and reviewed for dev.
- NPL Cluster Site reviewed
- mem_cache in web framework now support expire time
- `./build_linux.sh 6` now supports parallel build to decrease build time on dev machine.

2017.3.4-2017.3.7
- fixed mod open folder
- wikicraft editor refined
- NPLCAD 3,4 opened
- NPLCAD support include command
- fixed a crash when render queue overflow
- NPLRuntime appveyor now uses build-matrix
- RenderOrder attribute added and implemented to pipeline
- "zwrite" and "ztest" effect params added to ParaObject.
- updated pipeline wiki doc

2017.3.3
- ParaIO.GetText automatically does utf16 conversion according to byte order.
- NPL.load now hooks into require.

2017.3.2
- NPL vs plugin update 2.8 released with formatter
- NPLRuntime 32bits/64bits installer finished with appveyor auto deploy
- NPL.load now support file based module name and doc updated.
- new command: /pointtexture off

2017.2.28
- Fix NPL.load with relative path with coroutine threads.
- Starting Shenzhen ACM animation contest for youth.
- NPL.filename added.
- NPL delayed export supported.
- require function now support NPL.load

2017.2.25-2017.2.27
- NPL.export implemented with test cases that support cyclic dependency.
- filename attribute added for NPL runtime state.
- NPL runtime nsis installer finished. AppVeyor added for NPL Runtime.
- published NPL CAD 3.6 tutorial.
- NPL CAD stage 2 almost complete with performance optimization.

2017.2.24
- NPL.load will return cached file module.
- openstreet and bing map studied.
- file based module system designed on wiki.

2017.2.22-2017.2.23
- open image with 8 bits png indexed color supported. updated test file and wiki doc.
- XFile parser is supported on server version.

2017.2.18-2017.2.20
- fixed FBX with too many indices
- wikicraft project team building
- NPLRuntime appveyor ci added
- git sync auto pullback script

2017.2.10-2017.2.17
- rpc now support timeout in NPL DSL.
- fixed fbx with too many vertices
- NPLRuntime now supports dll build
- NPLRuntime now support appveyor ci under windows.
- github ci backup done
- NPLCAD 2 bug fix
- wikicraft project refined and merged, fully support github data source.
- lots of recruiting
- NPL project planned

2017.2.5-2017.2.9
- fixed comments in npl def statement.
- npl language service for vs 2017 published and uploaded
- NPLCAD stage 2 finished and published alpha version.
- rpc class added and added for NPL dsl, now support multiple thread and remote thread
- fixed block types id 81
- wikicraft group meeting and team rebuilding
- crc32 added to core npl package

2017.1.27-2017.2.3
- NPL meta compiler several bug fixes
- NPL language service fixed several bugs
- NPL dgit stage 2 finished.
- implemented and tested rsa lib in NPL
- started Chinese language project on coding

2017.1.26
- fixed nested NPL.load with *.npl files.

2017.1.21-2017.1.25

- FBX parser now support unlimited vertices provided they are in increasing order.
- fixed transparency of static fbx model
- NPL language service now support formatter and new meta-programming syntax
- release NPLCAD 3.5 tutorial video
- npl compiler now support meta compiler as well
- *.npl file can be used as startup file.

2017.1.1-2017.1.20
- NPL meta compiler integrated
- rsa and bigint added to NPL
- worldshare mod added
- fixed physics engine in block world
- NPL cad extended with meta programming
- STL exporter refined.
- fixed NPL c++ plugin samples and build file and documentation
- a trip to Beijing about education in applied math
- chrome embeded framework is refined.
- released NPL CAD 3.3 and 3.4 tutorial video
