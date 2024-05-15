# Paracraft模型文件ParaX标准 v1.0

**软件用途：** Paracraft模型文件ParaX标准提供了标准化的文件方案，兼容多个广泛的文件格式，实现统一化模型管理。
**运行环境:** Windows 10, Mac OS, Andriod, iOS
**编程语言：** NPL语言, C++
**开发完成时间：** 2018年6月1日
**发表日期：** 2018年6月1日
**技术特点：** 该产品在技术方面支持以下功能
- 兼容多文件格式
- 统一化的管理模型
- 加载速度快
- 模型标准可拓展

**源代码行数**: 3 [点击这里查看](Paracraft模型文件ParaX标准_code)

## 使用手册

### 资源管理
#### 介绍 

在计算机所描绘的3D世界中，所有的物体模型（如树木，人物，山峦）都是通过多边形网格来逼近表示的。网格模型是一种将物体模型的顶点数据、纹理、材质等信息存储在一个外部文件中的3D物体模型。对于那些简单的图元描述的图形，比如点，线，三角形等等，我们可以通过写代码指定顶点数据，索引数据，法线向量，纹理和材质等等信息。但对于复杂的3D物体的话，采用这种方式显然是不现实的。因此我们需要使用网格模型的技术，从各种特定的文件格式中读取和绘制3D图形。使用网格模型最普遍的方式是从外部的3D模型文件中加载一个网格。而这些3D模型通常都是由3D建模软件生成的，比较复杂的网格数据。

#### 网格
##### 网格Mesh分析

由多边形网格构成的物体储存着不同种类的基本元素：包括顶点，边线，面片和多边形。在许多情况下，只有顶点，边线以及面片会被存储。渲染器有可能只支持三角形，这时候多边形必须得由许多三角形组成。其他情况下，一些渲染器要么可以支持四边形或更多边形，要么能把多边形转化为三角形，这时候就没必要把网格储存为三角形格式。
网格参数介绍：

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4142/raw#image.png'
  ext: png
  filename: image.png
  size: '17155'
  unit: '%'
  percent: 50

```
> 网格结构图

- 顶点Vertex：包含了诸如颜色，法线向量，纹理坐标等信息的位置因素
- 边线Edge: 连接两个顶点形成的个体
- 面Face：一套紧密相邻的边线Edge集合。一套共面的面Face构成多边形Polygon。一般情况下面Face和多边形Polygon是等价的，但是由于渲染硬件一般只支持3~4边的面-Face,所以多边形也表示为多重面。由于多边形和面的从属关系，可能会带来几何结构，形状等额外性质。
- UV坐标：用于进行顶点和像素点的映射，便于贴图。

Mesh解析流程如图：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4143/raw#image.png'
  ext: png
  filename: image.png
  size: '37355'
  unit: '%'
  percent: 50

```

> Mesh解析大致流程图

1. CMeshObject在生成各种网格对象之前进行初始化，向下层索取如网格，纹理等信息。
2. MeshEntity负责产生网格信息，它会产生一个调用下层的CMeshLoader加载器和CMeshProcessor去目录或者网络上搜寻资源文件，解析并提取资源信息，呈递给渲染器，最后将结果返回到上层的CMeshObject。
3. ContentLoader在收到上层的调用动作后会检索文件，解析文件分类提取信息更新到m_asset呈递到上层，此外还负责关于网格LOD的设置。
  - m_ppMesh: 涵盖网格的结构和基本信息               
   - m_asset:网格加载处理器将呈递给上层的资源文件


#### ParaX
ParaEngine给它自己的文件定义了一种格式叫ParaX。它是基于微软.x文件模板建立的，也因此它也被设计为可以良好兼容DirectX V9.0b D3DX API。ParaX格式定义了骨骼，皮肤网格，骨骼动画，动画序列，动画速度，骨骼alpha animations等属性。
ParaX文件的顶层部分如下图. 在图中一共有3块顶层部分被定义。前两块对于DirectX保留的模式API 可以良好兼容。第三块由ParaEngine定义。并且由于这些顶层部分并没有任何重叠，ParaX文件可以被任何支持DirectX的商业软件查看或修改

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4144/raw#image.png'
  ext: png
  filename: image.png
  size: '37280'
  unit: '%'
  percent: 50

```

>  ParaX文件层级

下表所示是一个典型的ParaX模板实例，文件结构对应着图Figure 1.包含两块骨骼部分：SCENE_ROOT和BODY，一个网格对象，一个动画设置，一个动画序列。网格对象包含三个顶点，一个面，一种材质和两块蒙皮。

```
xof 0302txt 0032
Header {
 1;
 0;
 1;
}
Frame SCENE_ROOT {
   FrameTransformMatrix {
1,0,0,0,
0,1,0,0,
0,0,1,0,
0,0,0,1;;
 }
Frame Body {
   FrameTransformMatrix { // frame’s local matrix relative to its parent
1,0,0,0,
0,1,0,0,
0,0,1,0,
2,2,2,1;;
 }
Mesh pCubeShape2 { // a static mesh object
 3; // number of vertices defined below
1.5;0;0;,
0;0;1.5;,
0;1.5;0;,
 1; // number of faces defined below
3;2,1,0;, // each face has three indexes of the previously defined vertices 
MeshMaterialList {
1; // number of materials 
1; // number of faces whose material is defined below
0;; // material index
Material { // the material 
 0.800000;0.800000;0.800000;1.000000;; // diffuse
2.000000;
 0.000000;0.000000;0.000000;;
 0.000000;0.000000;0.000000;;
TextureFilename { // texture
"Texture\\dao.bmp";
}
}
MeshNormals {
 2; // number norm values defined below
0.565854;0.233529;-0.790743;,
-0.445748;0.525722;-0.724517;,
 1; // number of faces whose norm is defined. 
3;1,1,0;, // the three norm indexes for the three vertices of the face
}
MeshTextureCoords {
 3; // number of vertices whose texture coordinates are defined.
0.709954;-0.303127;,
0.651408;-0.155958;,
0.651391;-0.334976;;
}
XSkinMeshHeader {
 2; // max number of weights per vertex
 2; // max number of weights per face
 2; // number of bones
}
SkinWeights {
   "Body";
3; // number of vertices which are bound to this bone
0, // index of the vertices in the current mesh
1,
2;
0.55; // weight of the vertex
0.78;
0.12;
1,0,0,0, // offset matrix
0,1,0,0,
0,0,1,0,
2,2,2,1;;
}
SkinWeights {
   " SCENE_ROOT";
1; // number of vertices which are bound to this bone
2,
0.89; // weight of the vertex
1,0,0,0, // offset matrix
0,1,0,0,
0,0,1,0,
0,0,0,1;;
}
} // end of mesh
}// end of frame
}// end of frame

AnimationSet {
 Animation {
  {body}
  AnimationKey {
  0; // key type (rotation, translation or scaling)
  2; // number of keys
  0; 4; -0.185982, -0.721465, -0.648574, 0.155728;;, // timed keys
  120; 4; -0.185982, -0.721465, -0.648574, 0.155728;;
 }
 Animation {
  {SCENE_ROOT}
  AnimationKey {
  1; // key type (rotation, translation or scaling)
  2;
  0; 3; 1.000000, 1.000000, 1.000000;;,
  120; 3; 1.000000, 1.000000, 1.000000;;
 }
}
ParaEngine female1{
 Sequences{
  Anim{
   "Stand"; // animation name
   0; // from
   120; // to
   -1;	// loop on its self
   0;	// no speed
   0;0;0;;
   0;0;0;;
   100.0;		//bounding sphere radius
  }
 }
}
```
> ParaX Simple File


#####  ParaX模型解析
ParaX解析流程如图：

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4145/raw#image.png'
  ext: png
  filename: image.png
  size: '50059'
  unit: '%'
  percent: 50

```

> ParaX大致解析流程

1. ParaXEntity负责向上层传递m_asset.它会调动下层的ContentLoaderParaX执行资源文件的读取加载工作进行信息收集。
2. ContentLoaderParaX在加载和处理文件的时候，会通过文件名检索种类来分配对应的解析器。对于标准ParaX格式文件，ParaXSerializer会被调动。
3. ParaXSerializer类是ParaX解析的核心部分，由ParaXSerializer(文件读写)和ParaXPraser(文件解析)两部分组成。ParaX解析结构如下列代码所示

```
void* CParaXSerializer::LoadParaXMesh(CParaFile &f, ParaXParser& p)
{
	void* pMesh=NULL;
	if(LoadParaX_Header(p)){
		pMesh = LoadParaX_Body(p);
		LoadParaX_Finalize(p);
	}
	return pMesh;
}
```

分为Header，Body，Finalize三个部分。
Hearder部分会判定文件各部分种类并执行对应操作，解析过程中Header一定得最先完成，没有完成或者失败都会终止后续操作并报错
```
bool CParaXSerializer::LoadParaX_Header(ParaXParser& Parser)
{        ……
		if(Type == TID_ParaXHeader){…}
		else if(Type == TID_ParaXBody)
		else if(Type == TID_XDWORDArray)
		else if(Type == TID_ParaXRefSection)
		else if(Type == TID_D3DRMMesh)
		else if(Type == TID_D3DRMFrame)
		else{…}
		}
	}
	return true;
}
```

Body部分会先将模型分为有动画和静态两类，对于有动画的模型会分析文件信息判定种类，分类读取文件资源，再然后进行详细的动画配置。
```
	if(Parser.m_xheader.type == PARAX_MODEL_ANIMATED || Parser.m_xheader.type == PARAX_MODEL_BMAX)
		{            ……
				if(SUCCEEDED(pSubData->GetName(szName, &nSize))){
… 
if(Type == TID_XDWORDArray){…}
				else if(Type == TID_XVertices)	{…}
				else if(Type == TID_XTextures)	{…}
				else if(Type == TID_XAttachments){…}
				else if(Type == TID_XTransparency){…}
				else if(Type == TID_XViews){…}
				else if(Type == TID_XIndices0){…}
				else if(Type == TID_XGeosets){…}
				else if(Type == TID_XRenderPass){…}
				else if(Type == TID_XBones){…}
				else if(Type == TID_XTexAnims)	{…}
				else if(Type == TID_XParticleEmitters){…}
				else if(Type == TID_XRibbonEmitters){…}
				else if(Type == TID_XColors){…}
				else if(Type == TID_XCameras){…}
				else if(Type == TID_XLights){…}
				else if(Type == TID_XAnimations){…}
				}
}
				SAFE_RELEASE(pSubData);
			}
		          …\\很大部分关于动画animation的代码
		else if(Parser.m_xheader.type == PARAX_MODEL_DX_STATIC)
		{
			// TODO: for original dx model file.
		}
```
Finailize部分负责资源释放，准备下轮解析

```
void ParaXParser::Finalize()
{   
SAFE_RELEASE(m_pParaXBody);
	SAFE_RELEASE(m_pParaXRawData);
	SAFE_RELEASE(m_pDXEnum);
	SAFE_RELEASE(m_pParaXRef);
	SAFE_RELEASE(m_pD3DMesh);
	SAFE_RELEASE(m_pD3DRootFrame);}
```

4. ParaXModel是被定义为解释人物动画信息等数据的类，在完整的ParaX解析过程中它会被许多地方所引用到，对于ParaXSerializer，它提供了动画的配置方法以及相关模型信息的读写提取。


##### ParaX静态模型

ParaXStaticModel即ParaX静态模型，Create() / ClonePhysiceMesh() / LoadToSystemBuffer() / Render() 是最主要的功能方法，侧重于整体的纹理铺设，渲染，物理相关加载和数据到内存的加载缓冲。它基本作用按照ParaEngine的作者意思应该和StaticMesh是差不多，用于辅助生成LOD，但是实际的解析过程中，ParaXStaticModel却没有被任何地方引用。


#### ParaX扩展
ParaEnigine有着自己定义的专属格式ParaX，但市面上制作3D模型的软件太多，他们的产品格式也各不相同，为了保证ParaEngine的兼容性和适用性，ParaX添加了对几种主流模型文件的扩展，例如：FBX,BMax(ParaEnigine自定义格式),CAD,MDX。具体方法就是在解析文件的过程中进行文件种类筛选，分配对应的解析器解析，流程如图：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4146/raw#image.png'
  ext: png
  filename: image.png
  size: '40588'
  unit: '%'
  percent: 80

```

>  ParaX扩展解析流程


##### FBX
FBX格式是一种被AutoDesk公司的诸如MAYA/3dsmax等软件广泛使用的文件格式，也是工业上被用得最多的文件格式之一。
ParaEnigine的FBX解析器将所有的解析方法，对象全都高度整合到一起，只声明了解析器FBXPraser和用来读取动画xml文件的FBXModelInfo这两个类。
FBXPraser承担了材质，纹理，色域，动画，骨骼分配与家属关系确立，可见性等多个方面的功能，但具体可以概括为两类：
```
XFile::Scene* ParaEngine::FBXParser::ParseFBXFile(const char* buffer, int nSize)
{
	Assimp::Importer importer;
	Reset();
	const aiScene* pFbxScene = importer.ReadFileFromMemory(buffer, nSize, aiProcess_Triangulate | aiProcess_GenSmoothNormals, "fbx");
	if (pFbxScene) {…}
	else {…}
	return m_pScene;
}
```
ParseFBXFile():会读取网格和材料信息并进行相应处理后然后返回结果，用来解析静态模型
```
CParaXModel* FBXParser::ParseParaXModel(const char* buffer, int nSize)
{
	CParaXModel* pMesh = NULL;
	Assimp::Importer importer;
	Reset();
	SetAnimSplitterFilename();
	const aiScene* pFbxScene = importer.ReadFileFromMemory(buffer, nSize, aiProcess_Triangulate | aiProcess_GenSmoothNormals | aiProcess_FlipUVs, "fbx");
	if (pFbxScene) {…}
	else {…}
	return pMesh;
}
```
PaserParaXModel():会读取材料和动画信息并进行相应处理，之后会建立骨骼间的父类子类关系，以及从entity或者库中提取必要数据。用来解析有动画的模型
几个重要方法: 
- HasMaterials():读取mNumMaterials并执行ProcessStaticMaterials()
- HasAnimations()：读取mAnimations并执行ProcessFBXAnimation()
- ProcessEBXBoneNodes()：建立骨骼家属关系，提供在必要地方的网格补加方法
- FillParaXModelData():从各个Entity或者库里提取模型解析必要的数据
- PostProcessParaXModelData():预计算处理骨骼相关参数值来优化网格

##### BMax
BMax是内置的block max文件格式。BMax即Block Max，是一种专门被用在Paracraft中来储存和交换Block数据的一种文件格式。
BMax解析器和FBX解析器不一样，BMax解析器不像FBX解析器将所有的东西集成到一块，BMax解析器只是简单的分析文件结构，分类处理部分，再交由下层对应各类处理，更加的灵活。BMax解析结构如代码所示：
```
void BMaxParser::Load(const char* pBuffer, int32 nSize)
	{
		BMaxXMLDocument doc;
		doc.Parse(pBuffer);
		ParseHead(doc);
		ParseBlocks(doc);
	}
```
其中ParseHead只是简单判定文件是否有预设参数，解析步骤置于ParseBlocks中，如下：
```
		const char* value = blocks_element->GetText();
				ParseBlocks_Internal(value);
				ParseBlockFrames();
				CalculateBoneWeights();
				ParseVisibleBlocks();
				if (m_bAutoScale)
					ScaleModels();
```
NOTE：ParseBlocks_Internal(value) / ParseVisibleBlocks()：返回节点索引
ParseBlockFrames()：解析骨骼
CalculateBoneWeights()：判定骨骼家属关系
整体基本结构如图：
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4147/raw#image.png'
  ext: png
  filename: image.png
  size: '28260'
  unit: '%'
  percent: 80

```

>  BMax解析结构类图


##### CAD
ParaEngine中对CAD的解析进行了比较细致的方法说明，但是似乎已经舍弃了对于这种模型的引用，所以这些方法并没有在任何地方被调用过，这里仅对CAD解析过程进行简单的介绍。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/4148/raw#image.png'
  ext: png
  filename: image.png
  size: '26598'
  unit: '%'
  percent: 50

```


> CAD解析结构类图

CadModelNode继承自CTileObject，后者继承于CBaseObject，负责场景，3D相关功能的集成。在处理CAD模型时：
- CadModelNode将被启用负责参数处理和渲染工作，它首先会执行InitObject()，需要向下层所要m_pModel. 
- CadModel会调用下层的加载器和处理器来解析文件提取信息，并将获取的文件呈递给渲染器，最后将结果呈递给上层。
- CadContentLoader负责最底层的文件搜寻解析，信息提取工作。

##### MDX

目前ParaEngine并未使用MDX相关文件,只是简单了预声明了一个MDXEntity类，并没有构写相关功。能方法，没有使用实例

 
## bmax简易骨骼与X文件应用



**1. 理论**
利用bmax角色制作一个包含骨骼的模型，制作简单的重复的动作，并存为X文件。
本节内容较难，建议观看教学视频。

**2. 实践**
- 学习为简单的bmax角色放置正确的骨骼
- 学习利用骨骼做一个完整的循环动作
- 存成x文件导入电影方块中，并使用这个循环动作
- bmax骨骼应用
- X文件使用方法

**步骤1：认识bmax**
- 什么是bmax？
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/3705/raw#13. 模型与动画人物教学.mp4
  ext: mp4
  filename: 13. 模型与动画人物教学.mp4
  size: 616642521
          
```

bmax就是【Block Max方块模型】，用来制作精致的静态和动态道具。无论是静态还是动态的bmax，都能用于电影或场景中。静态bmax可以没有骨骼，动态bmax需要赋予骨骼。

<div style="float:right;margin-left:10px;width:150px">
  
![图 1.2.8](https://api.keepwork.com/storage/v0/siteFiles/3256/raw#image.png)
  
</div>


- 什么是骨骼？

和人体的骨骼类似，在Paracraft中，骨骼是一种特殊的有方向的方块，骨骼总是指向它的上一级骨骼，并且可以控制与之相连的其它方块（类似人体的肌肉）运动。

骨骼A指向骨骼B，我们称骨骼A为骨骼B的子骨骼，骨骼B为骨骼A的父骨骼。 父骨骼运动，子骨骼也跟着运动。
模型中最上级的一个父骨骼，没有指向任何其它骨骼，我们称之为根骨骼，它控制了人物整体的运动。

- 骨骼权重与彩色方块
骨骼的位置和方向，会影响周围的普通方块（肌肉）。一个普通方块可能受到多个骨骼的影响，普通方块受到某个骨骼的影响大小叫做权重。数值1代表某个方块完全跟随某个骨骼运动，0代表不跟随骨骼运动。 在Bmax中，这个数值不是1就是0. 也就是所Bmax中的某个普通方块只会受到一个骨骼方块的影响。 此时我们也称这个方块绑定到了这个骨骼上。 

指定普通方块的权重是一个很复杂的过程，我们会用到`彩色方块id：10`。彩色方块可以有很多种不同的颜色，Paracraft会自动将颜色相同，并且彼此相连的一组方块看成一个肌肉群，并将他们统一绑定到与之相连的骨骼方块上。 

例如手掌与手臂相连，手臂与肩膀相连。这时手掌和手臂最好用不同颜色的彩色方块区分开，如下图。
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3249/raw#image.png'
  ext: png
  filename: image.png
  size: '94830'
  unit: px
  percent: '35'
  alignment: left
  width: 200

```

- 什么是x文件？
x文件是ParaX文件的缩写，是Paracraft中的通用模型文件格式。x文件是一种比Bmax文件更加通用的模型文件格式。X文件不仅可以记录静态的3D模型和骨骼位置关系， 还可以存储多组骨骼动画。

在Paracraft中，我们可以将一个或多个包含人物动作的电影方块，保存成一个X文件。 然后， 我们可以在任何其它地方，重复使用它，比如可以用做NPC， 电影人物或者场景模型。 当然我们也可以将其它外部软件制作的动画模型，转化为X文件。
 
 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3252/raw#image.png'
  ext: png
  filename: image.png
  size: '65446'
  unit: px
  percent: '40'
  alignment: left
  width: 350

```




**步骤2：插入正确骨骼**

> 打开菜单栏(E键)，电影分类下的骨骼方块id：253
 
- 骨骼方块箭头的方向指向它的父骨骼，没有父骨骼的方块为根骨骼
- 骨骼方块会绑定和它后部以及侧面相连的方块，这些方块会随骨骼一同运动
- 建议用彩色方块搭建骨骼以外的（肌肉）方块

注意：
- 只有正常的方块会显示出来，半透明以及非方形的方块目前还不会显示，但是可以用来连接肌肉
   - 例如可以用蜘蛛网，连接2个悬空的区域，使它们绑定到同一根骨骼上
- Bmax模型也可以连接到骨骼上，形成Bmax模型的嵌套，为模型增加更多的细节
- 在最终显示时，骨骼方块本身也会变为离它最近的一个肌肉方块
 

 如下图，各部位的骨骼最终要指向父骨骼，末端-->中间-->前端-->父骨骼-->根骨骼。

<div style="float:left;width:200px">
  
![图 1.2.9](https://api.keepwork.com/storage/v0/siteFiles/3243/raw#image.png)
  
</div>
<div style="float:left;margin-left:10px;width:250px">
  
![图 1.2.10](https://api.keepwork.com/storage/v0/siteFiles/1992/raw#image.png)
  
</div>
<div style="clear:both"/>

`当父子骨骼不在同一直线上时，可添加中间骨骼进行连接。如果希望相连的方块属于不同的骨骼，我们需要用颜色区分开。如上图绿色和深绿色，紫色和浅紫色`

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3242/raw#image.png'
  ext: png
  filename: image.png
  size: '70035'
  unit: px
  alignment: left
  width: 500

```

`先搭建蛇头部位，只需搭建一半，再放入骨骼。后搭建蛇身一半，放入蛇身骨骼。`

- 在绑定骨骼时，Ctrl+右键点击骨骼，会显示所有骨骼的状态和权重。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3246/raw#image.png'
  ext: png
  filename: image.png
  size: '203488'
  unit: px
  alignment: left
  percent: '50'
  width: 300

```


**步骤3： 存成bmax，并为各个关节K动作帧**
 



- Ctrl+左键全选模型，Alt+左键选择模型的中心轴进行镜像
- Ctrl+左键选中道具进行保存并存为bmax模型
- 在电影方块中添加演员，点击添加按钮再选择bmax模型的路径

`快捷键1,1切换到骨骼轴后点击骨骼关节，出现该关节的三轴旋转圆环（绿色提示为该关节的名字，表示进入了该关节的专属骨骼轴），拖动红绿蓝圆环调整骨骼旋转角度。`
（补充：快捷键2切换到位置轴，快捷键3切换到转身轴，按两次3可切换到三轴旋转，快捷键4切换到大小轴）

> 注意：
1、要在头部骨骼的初始位置K帧，可防止头部受编号动作的影响。
2、Esc键退出当前关节的专属骨骼，回到全部骨骼。
3、若骨骼轴初始位置无关键帧，在中途位置K帧，初始位置会自动生成相同的关键帧。

 
把骨骼动作完成后关闭电影方块，将该电影方块保存为X文件。

```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3255/raw#image.png'
  ext: png
  filename: image.png
  size: '112247'
  unit: px
  percent: '40'
  alignment: left
  width: 300

```

 
**步骤4： 将X文件导入电影方块，在动作中插入该动作编号（默认0待机）并将秒数调整为10秒左右，小蛇调整好运动的位置，它就可以循环动作了。**

 
```@BigFile
bigFile:
  src: 'https://api.keepwork.com/storage/v0/siteFiles/3254/raw#image.png'
  ext: png
  filename: image.png
  size: '74978'
  unit: px
  percent: '40'
  alignment: left
  width: 200

```