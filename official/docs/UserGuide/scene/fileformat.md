# File Format
ParaEngine/NPL support several built-in file format. Some is used for 3d models, some for 3d world

## 2D Image file format
We support `dds, png, jpg, tga` image files. `dds` is the native device format and fastest to load. png is also the recommended format for 32bits lossless format. 

DirectX/OpenGL graphic drivers require textures with dimensions of order of 2, like 1, 2, 4, 8,16, 32, 64, 128, 256, 512, etc. Non-order of 2 textures are scaled and may look blurred. So it is always recommended to use an order of 2 textures. 

- if file extension is "dds", both format and mip levels are loaded from the file.
- if file extension is "png" and file name ends with "_32bits", format is D3DFMT_A8R8G8B8, mip level is 1.
- if file extension is "png" and file name does not ends with "_32bits", format is DXT3, complete mip level chain is created.
- if file extension is "png" and file path contains "blocks", we will use 32bits texture and full mipmap levels. if filename further contains "leaves" it will only has 1 mip level. 
- in all other cases, such as "tga", format is D3DFMT_UNKNOWN and mip level is D3DX_DEFAULT.
- if the file name ends with `_fps10_a009`, it is animated sequenced textures, which will be played at 10 frames per second, one can specify the last image as the file name to enable this feature.
> To use a subregion of an image, one can use `filename;left top width height`

## 3D Model file format

ParaEngine supports following built-in or standard file format. 
- ParaX format (*.x): This is our build-in file format for advanced animated characters, particles, etc. One needs to download and install ParaEngine exporter plugin for 3dsmax 9 (32bits/64bits). However, we are not supporting the latest version of 3dsmax. Please consider using FBX file format.
- FBX format (`*.fbx`): FBX is the universal file format for AutoDesk product like MAYA/3dsmax. It is one of the most supported lossless file format in the industry. Click [here for how to use FBX](https://github.com/LiXizhi/ParaCraftSDK/wiki/FBXModel). (Please note model size and embedded texture matters)

> we only support FBX version 2013 or above. Version 2014, 2015 are tested. 

- BMAX (*.bmax): This is our built-in block max file format, which is used exclusively by Paracraft application for storing static and animated blocks. 
- STL format (*.stl): This is a file format used for 3d printing.

### Attachment points
attachment points are special bones with name prefix `att_`, such as `att_lefthand` see [FBX](https://github.com/LiXizhi/ParaCraftSDK/wiki/FBXModel). One can attach ParaXModels to these attachment via NPL script at runtime. 

```
-- when we attach a model to the main character, the attached model will share the same animation id as the main character. If there is no such an animation on the attached model, the default standing animation is used. 
local player = ParaScene.CreateCharacter ("MyPlayer1", ParaAsset.LoadParaX("","character/v3/Elf/Female/ElfFemale.x"), "", true, 0.35, 0, 1.0);
local x,y,z = ParaScene.GetPlayer():GetPosition()
player:SetPosition(x,y,z);
ParaScene.Attach(player);
	
local asset = ParaAsset.LoadParaX("","character/v3/Pet/XM/XM.xml");
player:ToCharacter():AddAttachment(asset, 11);
```
It is also possible to add scaling and replaceble texture, such as 
```
player:ToCharacter():AddAttachment(meshModel, nRightHandId, -1, scaling, texReplaceable);
player:ToCharacter():RemoveAttachment(4, 1);
```
see [BlockInEntityHand.lua](https://github.com/NPLPackages/paracraft/blob/master/script/apps/Aries/Creator/Game/Entity/BlockInEntityHand.lua) for a real world example. 

The attachment id is listed below:
```
        /** attachment ID for character models */
	enum ATTACHMENT_ID
	{
		ATT_ID_SHIELD = 0,
		ATT_ID_HAND_RIGHT = 1,
		ATT_ID_HAND_LEFT = 2,
		ATT_ID_TEXT = 3,
		ATT_ID_GROUND = 4,
		ATT_ID_SHOULDER_RIGHT = 5,
		ATT_ID_SHOULDER_LEFT = 6,
		ATT_ID_HEAD = 11,
		ATT_ID_FACE_ADDON = 12,
		ATT_ID_EAR_LEFT_ADDON = 13,
		ATT_ID_EAR_RIGHT_ADDON = 14,
		ATT_ID_BACK_ADDON = 15,
		ATT_ID_WAIST = 16,
		ATT_ID_NECK = 17,
		ATT_ID_BOOTS = 18,
		ATT_ID_MOUTH = 19,
		ATT_ID_MOUNT1 = 20,
		ATT_ID_MOUNT2,
		ATT_ID_MOUNT3,
		ATT_ID_MOUNT4,
		ATT_ID_MOUNT5,
		ATT_ID_MOUNT6,
		ATT_ID_MOUNT7,
		ATT_ID_MOUNT8,
		ATT_ID_MOUNT9,
		ATT_ID_MOUNT10,
		ATT_ID_MOUNT11,
		ATT_ID_MOUNT12,
		ATT_ID_MOUNT13,
		ATT_ID_MOUNT14,
		ATT_ID_MOUNT15,
		ATT_ID_MOUNT16,
		ATT_ID_MOUNT17,
		ATT_ID_MOUNT18,
		ATT_ID_MOUNT19,
		ATT_ID_MOUNT20,
		ATT_ID_MOUNT00 = 0xffff, // this is same as ATT_ID_SHIELD or MOUNT0
	};
```

ParaObject's API interface. 
```cpp
/**
* @param ModelAsset the model to be attached. This can be both ParaX model or static mesh model.
* @param nAttachmentID to which part of the character, the effect model is attached.
	ATT_ID_SHIELD = 0,
	ATT_ID_HAND_RIGHT = 1,
	ATT_ID_HAND_LEFT = 2,
	ATT_ID_TEXT = 3,
	ATT_ID_GROUND = 4,
	ATT_ID_SHOULDER_RIGHT = 5,
	ATT_ID_SHOULDER_LEFT = 6,
	ATT_ID_HEAD = 11,
	ATT_ID_FACE_ADDON = 12,
	ATT_ID_EAR_LEFT_ADDON = 13,
	ATT_ID_EAR_RIGHT_ADDON = 14,
	ATT_ID_BACK_ADDON = 15,
	ATT_ID_WAIST = 16, 
	ATT_ID_NECK = 17, 
	ATT_ID_BOOTS = 18,
	ATT_ID_MOUTH = 19, 
	ATT_ID_MOUNT1 = 20,
* @param nSlotID the slot id of the effect. default value is -1.  if there is already an effect with the same ID
*	it will be replaced with this new one. 
* @param scaling: scaling of the texture
* @param ReplaceableTexture: replace the texture. 
*/
void AddAttachment(ParaAssetObject ModelAsset, int nAttachmentID);
void AddAttachment3(ParaAssetObject ModelAsset, int nAttachmentID, int nSlotID);
void AddAttachment4(ParaAssetObject ModelAsset, int nAttachmentID, int nSlotID, float fScaling);
void AddAttachment5(ParaAssetObject ModelAsset, int nAttachmentID, int nSlotID, float fScaling, ParaAssetObject ReplaceableTexture);

/** get the attachment object's attribute field. */
ParaAttributeObject GetAttachmentAttObj(int nAttachmentID);

/**
* the model to be detached. @see AddAttachment();
* @param nAttachmentID: this value is reserved and can be any value.  
* @param nSlotID the slot id of the effect. default value is -1.  all attachments with the SlotID will be removed.  
*/
void RemoveAttachment(int nAttachmentID);
void RemoveAttachment2(int nAttachmentID, int nSlotID);
```
### Reading ParaX file content from NPL script
It is possible to read binary data from ParaX file from NPL script. See following for details:
[[https://github.com/NPLPackages/main/blob/master/script/ide/System/Scene/Assets/ParaXModelAttr.lua]]

ParaXModelAttr can be used to get information of ParaX Model asset file. It can be used to dump textures, vertices, matrices, bones, etc. 
There are two sets of API, one is cdata API, the other is scripting API. 
- cdata API function name is like xxxCData: such as GetObjectNumCData is very fast, it uses the same data reference to internal C++ ParaXModel without any memory allocation. 
Thus providing a way to read/write big C++ data without any memory allocation on scripting environment. 
Thanks to luajit ffi, the speed of referencing cdata field is close to native C++ speed.
- the scripting API function name is like xxx: such as ParaXModelAttr:GetVertices() will copy cdata into standard lua table and cache the result, which could be slow and requires lots of memory allocations. 


```lua
-- Example 1: load from cdata into npl table objects
NPL.load("(gl)script/ide/System/Scene/Assets/ParaXModelAttr.lua");
local ParaXModelAttr = commonlib.gettable("System.Scene.Assets.ParaXModelAttr");
local attr = ParaXModelAttr:new():initFromPlayer(ParaScene.GetPlayer())
echo(attr:GetObjectNum());
echo(attr:GetRenderPasses());
echo(attr:GetGeosets());
for i=1, attr:GetObjectNum().nTextures do
	echo({texture = attr:GetTextureName(i-1)});
end
for i=1, attr:GetObjectNum().nBones do
	local bone = attr:GetBone(i-1);
	echo({bone_name = bone:GetField("name", ""), PivotPoint = bone:GetField("PivotPoint", {}), ParentIndex = bone:GetField("ParentIndex", -1) });
end
echo(attr:GetVertices());
echo(attr:GetIndices());
-- Example 2: loading from a given *.x or *.fbx file. 
NPL.load("(gl)script/ide/System/Scene/Assets/ParaXModelAttr.lua");
local ParaXModelAttr = commonlib.gettable("System.Scene.Assets.ParaXModelAttr");
local attr = ParaXModelAttr:new():initFromAssetFile("character/bmax/test_multianim.fbx", function(attr)
	attr:DrawStaticAsText()
end)
-- Example 3: using cdata directly without any memory allocation on scripting environment
NPL.load("(gl)script/ide/System/Scene/Assets/ParaXModelAttr.lua");
local ParaXModelAttr = commonlib.gettable("System.Scene.Assets.ParaXModelAttr");
local attr = ParaXModelAttr:new():initFromAssetFile("character/bmax/test_multianim.fbx", function(attr)
	local vertices = attr:GetVerticesCData();
	local nCount = attr:GetObjectNumCData().nVertices;
	for i=0, nCount-1 do
		echo({vertices[i].pos.x, vertices[i].pos.y, vertices[i].pos.z})
	end
end)
```

### BMax file format
BMAX is short for Block Max, it is a file format used exclusively in Paracraft for storing and exchanging block data. 
In paracraft, the world is made up of blocks, each block may contain `x,y,z, block_id, block_data, custom_data`
- `x,y,z` is block position
- `block_id` is type id of the block, see [block_types.xml](https://github.com/NPLPackages/paracraft/blob/master/config/Aries/creator/block_types.xml) for a complete list of block ids. 
- `block_data` is a 32bits data of the block, it usually denotes the orientation or type of the block. 
- `custom_data` can be any NPL table object that stores additional data of the block. Most static blocks does not contain custom_data, however, blocks like movie block, command blocks will save animation data and commands in this place. 

You can select some blocks in paracraft and save them to bmax file to examine a real bmax file, it should be self-explanatory. Following is an example bmax file(containing a button, 2 movie blocks, a repeater and a wire):

![image](https://cloud.githubusercontent.com/assets/94537/21293073/901298a4-c554-11e6-8967-14fbb914ff55.png)

```xml

<pe:blocktemplate>
	<pe:blocks>{
{-2,0,-3,105,5,},

{-2,0,-2,228,[6]={{name="cmd","/t 6 /end",},{{"{timeseries={lookat_z={times={0,5348,},data={20001.56125,20004.65625,},ranges={{1,2,},},type=\"Linear\",name=\"lookat_z\",},eye_liftup={times={0,5348,},data={0.28568,0.26068,},ranges={{1,2,},},type=\"Linear\",name=\"eye_liftup\",},lookat_x={times={0,5348,},data={20000.51959,20000.58203,},ranges={{1,2,},},type=\"Linear\",name=\"lookat_x\",},eye_rot_y={times={0,5348,},data={-3.11606,-3.11668,},ranges={{1,2,},},type=\"LinearAngle\",name=\"eye_rot_y\",},is_fps={times={0,5348,},data={0,0,},ranges={{1,2,},},type=\"Discrete\",name=\"is_fps\",},lookat_y={times={0,5348,},data={-127.08333,-127.08333,},ranges={{1,2,},},type=\"Linear\",name=\"lookat_y\",},eye_dist={times={0,5348,},data={8,8,},ranges={{1,2,},},type=\"Linear\",name=\"eye_dist\",},has_collision={times={0,5348,},data={1,1,},ranges={{1,2,},},type=\"Discrete\",name=\"has_collision\",},eye_roll={times={0,5348,},data={0,0,},ranges={{1,2,},},type=\"LinearAngle\",name=\"eye_roll\",},},}",name="slot",attr={count=1,id=10061,},},{"{timeseries={time={times={},data={},ranges={},type=\"Linear\",name=\"time\",},music={times={},data={},ranges={},type=\"Discrete\",name=\"music\",},tip={times={},data={},ranges={},type=\"Discrete\",name=\"tip\",},movieblock={times={},data={},ranges={},type=\"Discrete\",name=\"movieblock\",},cmd={times={},data={},ranges={},type=\"Discrete\",name=\"cmd\",},blocks={times={},data={},ranges={},type=\"Discrete\",name=\"blocks\",},text={times={},data={},ranges={},type=\"Discrete\",name=\"text\",},},}",name="slot",attr={count=1,id=10063,},},name="inventory",{"{timeseries={blockinhand={times={},data={},ranges={},type=\"Discrete\",name=\"blockinhand\",},x={times={0,},data={20000.51959,},ranges={{1,1,},},type=\"Linear\",name=\"x\",},pitch={times={},data={},ranges={},type=\"LinearAngle\",name=\"pitch\",},y={times={0,},data={-127.08333,},ranges={{1,1,},},type=\"Linear\",name=\"y\",},parent={times={},data={},ranges={},type=\"LinearTable\",name=\"parent\",},roll={times={},data={},ranges={},type=\"LinearAngle\",name=\"roll\",},block={times={},data={},ranges={},type=\"Discrete\",name=\"block\",},scaling={times={},data={},ranges={},type=\"Linear\",name=\"scaling\",},gravity={times={},data={},ranges={},type=\"Discrete\",name=\"gravity\",},HeadUpdownAngle={times={},data={},ranges={},type=\"Linear\",name=\"HeadUpdownAngle\",},anim={times={},data={},ranges={},type=\"Discrete\",name=\"anim\",},bones={R_Forearm_rot={times={0,34,1836,},data={{0.00024,0.00175,-0.01261,0.99992,},{0.00024,0.00175,-0.01261,0.99992,},{0.00022,-0.05946,0.42959,0.90107,},},ranges={{1,3,},},type=\"Discrete\",name=\"R_Forearm_rot\",},R_UpperArm_rot={times={0,34,1836,},data={{-0.01933,-0.00286,0.03036,0.99935,},{-0.01802,-0.03834,0.32796,0.94375,},{-0.0137,-0.01077,0.14324,0.98954,},},ranges={{1,3,},},type=\"Discrete\",name=\"R_UpperArm_rot\",},isContainer=true,},speedscale={times={},data={},ranges={},type=\"Discrete\",name=\"speedscale\",},assetfile={times={0,},data={\"actor\",},ranges={{1,1,},},type=\"Discrete\",name=\"assetfile\",},skin={times={},data={},ranges={},type=\"Discrete\",name=\"skin\",},z={times={0,},data={20001.56125,},ranges={{1,1,},},type=\"Linear\",name=\"z\",},facing={times={},data={},ranges={},type=\"LinearAngle\",name=\"facing\",},HeadTurningAngle={times={},data={},ranges={},type=\"Linear\",name=\"HeadTurningAngle\",},name={times={0,},data={\"actor3\",},ranges={{1,1,},},type=\"Discrete\",name=\"name\",},opacity={times={},data={},ranges={},type=\"Linear\",name=\"opacity\",},},tooltip=\"actor3\",}",name="slot",attr={count=1,id=10062,},},},name="entity",attr={bz=19201,bx=19200,class="EntityMovieClip",item_id=228,by=5,},},},

{-2,0,-1,197,3,},
{-2,0,0,189,},
{-2,0,1,228,[6]={{name="cmd","/t 30 /end",},{name="inventory",{name="slot",attr={count=1,id=10061,},},},name="entity",attr={bz=19204,bx=19200,class="EntityMovieClip",item_id=228,by=5,},},},}

	</pe:blocks>
</pe:blocktemplate>
```

For user manual of using movie blocks, please see the courses in
- http://www.paracraft.cn/learn/movieblockcourses?lang=zh

## ParaX File format
ParaX is binary file format used exclusively in NPL Runtime for animated 3D character asset.  
ParaX is like a concise version of FBX file (FBX is like BMAX file used by autodesk 3dsmax/maya, ...)
NPL Runtime also support reading FBX file and load as ParaXModel object in C++, for user guide see [FBX](https://keepwork.com/official/docs/UserGuide/scene/import_export)

- BMAX to ParaX converter in C++ (Lacking support for animation data in movie block)： https://github.com/LiXizhi/NPLRuntime/tree/master/Client/trunk/ParaEngineClient/BMaxModel
- ParaX models: 
  - https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/ParaXModel/XFileCharModelParser.h
  - https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/3dengine/ParaXSerializer.h
  - https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/3dengine/ParaXSerializer.h

#### BMAX movie blocks to ParaX File format Conversion Details
- locate all movie blocks in BMAX file and ignore all other blocks. Movie blocks needs to be in the same order of 3D space (as repeater and wires indicates)
- The first movie block is always animation id 0 (idle animation)
- The second movie block is always animation id 4 (walk animation)
- The animation id of the third or following movie blocks can be specified in its movie block command
- The BMAX model(s) in the first movie block is used for defining bones and mesh (vertices, etc), please see [this code](https://github.com/LiXizhi/NPLRuntime/tree/master/Client/trunk/ParaEngineClient/BMaxModel) for how to translate blocks into bones, vertices and sub meshes. BMAX models in all other movie blocks are ignored. 
- Animation data in movie blocks are used to generate bone animations for each animation id in the final ParaXModel. 

## ParaX File LOD
LOD is for level of detail.  We use an XML file(LOD mesh XML file) to group several `*.x` model files. So that when the camera to object distance are within a specified range, we will use a given '*.x' model as defined in the xml file. 

`LOD mesh XML file` is just a metafile referencing a collection of x files and specifying which file to use when the object is within a given radius. 

In order to generate mesh LOD file, use the following guidelines:

- Put all your LOD mesh's model files (all resolutions), textures in the same directory. Name each file as `objectName_LOD10.x`, `objectName_LOD20.x`. The number in the trailing "_LOD[number]" means within what distance in meters this file shall be used. 
- Create a xml file called `objectName.xml` in the same directory. 

E.g. in your directory, you have `chat.dds, char_LOD5.x, char_LOD10.x, char_LOD30.x`. 
The xml file should be named as `char.xml`, and the LOD setting is retrieved from this filename. 

> NOTE: it is VERY important that all LOD must have the same animation lengths for all animations. because the game engine will use LOD0's animation frame number for all its LODs.

The format of xml file is given using an example file (`ElfFemale.xml`) below. It should be intuitive to write your own. 
```xml
<?xml version="1.0" encoding="utf-8"?>
<mesh version="1" type="0">
	<boundingbox minx="-0.336675" miny="0.000000" minz="-0.366781" maxx="0.312267" maxy="1.247474" maxz="0.335574"/>
	<submesh loddist="5" filename="ElfFemale_LOD5.x"/>
	<submesh loddist="15" filename="ElfFemale_LOD15.x"/>
	<submesh loddist="30" filename="ElfFemale_LOD30.x"/>
</mesh>
```
- bounding box is optional

As a general principle, the first LOD has all the triangles, the second one has no more than 2000 triangles, and the third has no more than 500 triangles. For mesh with less than 500 triangles, there does not need any lod. For mesh with 2000 triangles, two LOD is enough, more mesh with more than 4000 triangles, three lods are recommended. But it is entirely up to the developer to decide how many lods a model has or none. 

## 3D World File Format
ParaEngine/NPL can automatically save or load 3D scene object to or from disk files. 

To create an empty world, one can use
```lua
	local worldpath = "temp/clientworld";
	ParaIO.DeleteFile(worldpath.."/");
	ParaIO.CreateDirectory(worldpath.."/");
	ParaWorld.NewEmptyWorld(worldpath, 533.3333, 64);
```
3D world is tiled. Each tile is usually 512*512 meters. For historical reasons, it is 533.3333 by default. 
You will notice three files, after calling above function. 

`temp/clientworld/worldconfig.txt` which is the entry file for 3d world, its content is like 
```
-- Auto generated by ParaEngine 
type = lattice
TileSize = 533.333313
(0,0) = temp/clientworld/flat.txt
(0,1) = temp/clientworld/flat.txt
...
```
It contains a mapping from tile (x,y) to tile configuration file. 

`temp/clientworld/flat.txt` is configuration file for a single terrain tile.
```
-- auto gen by ParaEngine
Heightmapfile = temp/clientworld/flat.raw
MainTextureFile = terrain/data/MainTexture.dds
CommonTextureFile = terrain/data/CommonTexture.dds
Size = 533.333313
ElevScale = 1.0
Swapvertical = 1
HighResRadius = 30
DetailThreshold = 50.000000
MaxBlockSize = 64
DetailTextureMatrixSize = 64
NumOfDetailTextures = 0
```

## Global Terrain Format
Global Terrain Format is a LOD triangle tile based terrain engine. The logical tile size is defined by 3d world configuration file, such as 533.333, however, its real dimension is always 512*512 and saved as a `*.raw` file. 

## Block World File Format
ParaEngine has a build-in block engine for rendering 3D blocky world. 
Block world is also tiled. The logical tile size is defined by 3d world configuration file, such as 533.333, however, its real dimension is always `512x512` and saved as a binary block region file in `*.raw` extension. Please note that block world region file `*.raw` is different from global terrain's `*.raw` file. The latter is just height maps. 

Currently, each block may contain `x,y,z, block_id, block_data[, custom_data]`, currently `custom_data` is not supported in block region `*.raw` file. Block region file is encoded (compressed) using `increase-by-integer` algorithm, which will save lots of disk space if blocks are of the same type in the tiled region. 

See [BlockRegion.cpp](https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/BlockEngine/BlockRegion.h) for details

## References
- http://www.paracraft.cn/  : see bmax model tutorial video 
- https://github.com/LiXizhi/NPLRuntime/wiki
- https://github.com/LiXizhi/STLExporter
- http://wikicraft.cn/wiki/mod/packages : see STLExporter
- BMAX to ParaX converter in C++ (Lacking support for animation data in movie block)： https://github.com/LiXizhi/NPLRuntime/tree/master/Client/trunk/ParaEngineClient/BMaxModel

- ParaX models: 
  - https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/ParaXModel/XFileCharModelParser.h
  - https://github.com/LiXizhi/NPLRuntime/blob/master/Client/trunk/ParaEngineClient/3dengine/ParaXSerializer.h
