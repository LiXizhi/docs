```c++
//-----------------------------------------------------------------------------
// Class:	CParaXModel
// Authors:	Li, Xizhi
// Emails:	LiXizhi@yeah.net
// Date:	2005.10.8
// Revised: 2005.10.8
// Note: some logics is based on the open source code of WOWMAPVIEW
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include <algorithm>
#include "ParaWorldAsset.h"
#include "SceneObject.h"
#include "effect_file.h"
#ifdef USE_DIRECTX_RENDERER
#include "ShadowVolume.h"
#include "EdgeBuilder.h"
#endif
#include "SortedFaceGroups.h"
#include "CustomCharCommon.h"
#include "particle.h"
#include "ParaXBone.h"
#include "ParaXModel.h"
#include "BoneChain.h"
#include "memdebug.h"
#include "XFileCharModelExporter.h"
#include "./IO/FileUtils.h"
#include "ViewportManager.h"


/** def this, if one wants the animation to be very accurate. */
//#define	ONLY_REMOVE_EQUAL_KEYS

/** @def if this macro is defined, then vertices and normals of the animated mesh will be precalculated.
* uncomment this macro, if you believe that the reuse of model vertices is not much and that the model
* has many hidden meshes. */
// #define PRECALCULATE_VERTICES_NORMALS

namespace ParaEngine
{
	int globalTime = 0;
	VertexDeclarationPtr CParaXModel::m_pVertexDeclaration = NULL;
	CEffectFile* CParaXModel::m_pEffectFile = NULL;
}
using namespace ParaEngine;

size_t CParaXModel::m_uUsedVB = 0;

void CParaXModel::SetHeader(const ParaXHeaderDef& xheader)
{
	// for xheader
	m_header = xheader;

	//check rotation property first since it's not really a "animation" property
	//clear it after we get value                  -- clayman 2012.7.23
	uint32 mask = (1 << 5);
	rotatePartice2SpeedVector = (m_header.IsAnimated & (1 << 5)) > 0;
	m_header.IsAnimated &= ~mask;

	animated = m_header.IsAnimated > 0;
	animGeometry = (m_header.IsAnimated&(1 << 0)) > 0;
	animTextures = (m_header.IsAnimated&(1 << 1)) > 0;
	animBones = (m_header.IsAnimated&(1 << 2)) > 0;
	//to support arg channel only texture animation  -clayman 2011.8.5
	animTexRGB = (m_header.IsAnimated&(1 << 4)) > 0;

	if (IsBmaxModel())
		m_RenderMethod = BMAX_MODEL;
	else if (animated)
		m_RenderMethod = SOFT_ANIM;
	else
		m_RenderMethod = NO_ANIM;
}

CParaXModel::CParaXModel(const ParaXHeaderDef& xheader)
	: m_bIsValid(true), m_nCurrentFrameNumber(0), m_nHasAlphaBlendedRenderPass(-1), m_bTextureLoaded(false)
	, m_vNeckYawAxis(Vector3::UNIT_Y), m_vNeckPitchAxis(Vector3::UNIT_Z)
	, m_vbState(NOT_SET)
{
	SetHeader(xheader);
	
	// set to default for all others.
	memset(&m_objNum, 0, sizeof(m_objNum));
	m_trans = 1.0f;
	m_radius = 1.0f;

	int i = 0;
	for (i = 0; i < MAX_MODEL_TEXTURES; ++i)
	{
		specialTextures[i] = -1;
		replaceTextures[i] = 0;
		useReplaceTextures[i] = false;
	}
	for (i = 0; i < MAX_MODEL_ATTACHMENTS; ++i)
		m_attLookup[i] = -1;

	for (i = 0; i < MAX_KNOWN_BONE_NODE; ++i)
		m_boneLookup[i] = -1;
	bounds = 0;
	boundTris = 0;
	showGeosets = 0;

	hasCamera = false;
	m_origVertices = NULL;
	m_frame_number_vertices = NULL;
	m_vertices = NULL;
	m_normals = NULL;
	texcoords1 = NULL;
	m_indices = NULL;
	anims = NULL;
	bones = NULL;
	texanims = NULL;
	globalSequences = NULL;
	colors = NULL;
	lights = NULL;
	transparency = NULL;
	particleSystems = NULL;
	ribbons = NULL;
	globalSequences = NULL;

	// animation states
	m_CurrentAnim.Reset();
	m_NextAnim.MakeInvalid();
	m_BlendingAnim.Reset();
	blendingFactor = 0;

	mUpperAnim.Reset();
	mUpperBlendingAnim.Reset();
	mUpperBlendingFactor = 0;

	fBlendingTime = 0.25f;	// this is the default value.
}

CParaXModel::~CParaXModel(void)
{
	if (m_bIsValid)
	{
		if (m_vbState == INITED)
		{
			m_uUsedVB -= m_pVertexBuffer.GetBufferSize();
		}

		m_pIndexBuffer.ReleaseBuffer();
		m_pVertexBuffer.ReleaseBuffer();


		//gLog("Unloading model %s\n", name.c_str());

		if (GetObjectNum().nTextures) {
			for (size_t i = 0; i < GetObjectNum().nTextures; i++) {
				if (textures[i]) {
					textures[i].reset();
				}
			}
			SAFE_DELETE_ARRAY(textures);
		}

		SAFE_DELETE_ARRAY(globalSequences);

		SAFE_DELETE_ARRAY(bounds);
		SAFE_DELETE_ARRAY(boundTris);
		SAFE_DELETE_ARRAY(showGeosets);


		// unload all sorts of crap
		SAFE_DELETE_ARRAY(m_vertices);
		SAFE_DELETE_ARRAY(m_normals);
		SAFE_DELETE_ARRAY(texcoords1);
		SAFE_DELETE_ARRAY(m_indices);
		SAFE_DELETE_ARRAY(anims);
		SAFE_DELETE_ARRAY(m_origVertices);
		SAFE_DELETE_ARRAY(m_frame_number_vertices);

		if (animBones)
			SAFE_DELETE_ARRAY(bones);
		if (!animGeometry) {
		}

		if (animTextures)
			SAFE_DELETE_ARRAY(texanims);
		SAFE_DELETE_ARRAY(colors);
		SAFE_DELETE_ARRAY(transparency);
		SAFE_DELETE_ARRAY(lights);

		SAFE_DELETE_ARRAY(particleSystems);
		SAFE_DELETE_ARRAY(ribbons);

		ClearFaceGroups();
	}
}

void CParaXModel::SetVertexBufferDirty()
{
	if (m_vbState == INITED)
	{
		m_uUsedVB -= m_pVertexBuffer.GetBufferSize();
		m_pVertexBuffer.ReleaseBuffer();
		m_pIndexBuffer.ReleaseBuffer();

		m_vbState = NEED_INIT;
	}
}

void CParaXModel::SetRenderMethod(RENDER_METHOD method)
{
	m_RenderMethod = method;
}

bool CParaXModel::CheckMinVersion(int v0, int v1/*=0*/, int v2/*=0*/, int v3/*=0*/)
{
	return (GetHeader().version[0] >= v0) && (GetHeader().version[1] >= v1) && (GetHeader().version[2] >= v2) && (GetHeader().version[3] >= v3);
}

bool CParaXModel::InitDeviceObjects()
{
	LoadTextures();

	return true;
}

bool CParaXModel::DeleteDeviceObjects()
{
	return true;
}

void CParaXModel::LoadTextures()
{
	if (m_bTextureLoaded)
		return;
	m_bTextureLoaded = true;
	auto& texManager = CGlobals::GetAssetManager()->GetTextureManager();
	for (int i = 0; i < (int)m_objNum.nTextures; ++i)
	{
		asset_ptr<TextureEntity> pTexture = textures[i];
		if (pTexture)
		{
			textures[i] = CGlobals::GetAssetManager()->LoadTexture("", pTexture->GetKey(), TextureEntity::StaticTexture);
			if (pTexture != textures[i] && pTexture->GetRawData())
			{
				textures[i]->SetRawData(pTexture->GetRawData(), pTexture->GetRawDataSize());
				// OUTPUT_LOG("%s assigned buffer from raw data \n", pTexture->GetKey().c_str());
				pTexture->GiveupRawDataOwnership();
			}
		}
	}

	initTranslucentFaceGroups();
}

bool CParaXModel::IsBmaxModel()
{
	return m_header.type == PARAX_MODEL_BMAX;
}

void CParaXModel::SetBmaxModel()
{
	m_header.type = PARAX_MODEL_BMAX;
	SetRenderMethod(BMAX_MODEL);
}

void CParaXModel::ClearFaceGroups()
{
	//////////////////////////////////////////////////////////////////////////
	// delete all face group. 
	for (int i = 0; i < (int)m_faceGroups.size(); ++i)
	{
		SAFE_DELETE(m_faceGroups[i]);
	}
	m_faceGroups.clear();
}

bool CParaXModel::IsValid()
{
	return m_bIsValid;
}

AnimIndex CParaXModel::GetAnimIndexByID(int nAnimID)
{
	int nAnim = (int)GetObjectNum().nAnimations;
	for (int i = 0; i < nAnim; i++)
	{
		if (anims[i].animID == nAnimID)
		{
			return AnimIndex(i, 0, anims[i].timeStart, anims[i].timeEnd, (byte)(anims[i].loopType), nAnimID);
		}
	}
	return AnimIndex(-1);
}

int CParaXModel::GetAnimIDByIndex(int nAnimIndex)
{
	if (nAnimIndex < (int)GetObjectNum().nAnimations && nAnimIndex >= 0)
		return anims[nAnimIndex].animID;
	else
		return 0;
}

const ModelAnimation* CParaXModel::GetModelAnimByIndex(int nAnimIndex)
{
	if (nAnimIndex < (int)GetObjectNum().nAnimations && nAnimIndex >= 0)
		return &(anims[nAnimIndex]);
	else
		return NULL;
}

void CParaXModel::InitVertexBuffer()
{
	switch (m_RenderMethod)
	{
	case ParaEngine::CParaXModel::NO_ANIM:
		InitVertexBuffer_NOANIM();
		break;
	case ParaEngine::CParaXModel::BMAX_MODEL:
		InitVertexBuffer_BMAX();
		break;
	default:
		break;
	}
}

void CParaXModel::InitVertexBuffer_BMAX()
{
	do
	{
		if (m_pVertexBuffer.IsValid()
			|| m_pVertexBuffer.IsValid()
			|| passes.size() == 0
			|| m_origVertices == nullptr
			|| m_indices == nullptr)
		{
			break;
		}

		auto nPasses = passes.size();

		size_t count = 0;
		for (size_t i = 0; i < nPasses; i++)
		{
			auto& p = passes[i];

			if (p.geoset < 0 || !showGeosets[p.geoset])
				continue;

			count += p.indexCount;
		}

		if (!m_pVertexBuffer.CreateBuffer((uint32)(count * sizeof(bmax_vertex)), 0, D3DUSAGE_WRITEONLY))
			break;

		bmax_vertex* pBuffer;
		if (!m_pVertexBuffer.Lock((void**)&pBuffer, 0, 0))
			break;

		size_t index = 0;
		for (size_t pass = 0; pass < nPasses; pass++)
		{
			auto& p = passes[pass];

			if (p.geoset < 0 || !showGeosets[p.geoset])
				continue;

			size_t nLockedNum = p.indexCount / 3;
			int nVertexOffset = p.GetVertexStart(this);
			int nIndexOffset = p.m_nIndexStart;

			for (size_t i = 0; i < nLockedNum; ++i)
			{
				size_t nVB = 3 * i;
				for (int k = 0; k < 3; ++k, ++nVB)
				{
					int a = m_indices[nIndexOffset + nVB] + nVertexOffset;
					auto& out_vertex = pBuffer[index++];
					auto& ov = m_origVertices[a];
					out_vertex.p = ov.pos;
					out_vertex.n = ov.normal;
					out_vertex.color = ov.color0;
				}
			}
		}


		m_pVertexBuffer.Unlock();
		auto usedSize = count * sizeof(bmax_vertex);
		m_uUsedVB += usedSize;

		m_vbState = INITED;

		return;

	} while (false);

	m_pVertexBuffer.ReleaseBuffer();
	m_pIndexBuffer.ReleaseBuffer();
	m_vbState = NOT_USE;
}

void CParaXModel::InitVertexBuffer_NOANIM()
{
	do
	{
		if (m_pVertexBuffer.IsValid()
			|| m_pVertexBuffer.IsValid()
			|| passes.size() == 0
			|| m_origVertices == nullptr
			|| m_indices == nullptr)
		{
			break;
		}

		auto nPasses = passes.size();

		size_t count = 0;
		for (size_t i = 0; i < nPasses; i++)
		{
			auto& p = passes[i];

			if (p.geoset < 0 || !showGeosets[p.geoset])
				continue;

			count += p.indexCount;
		}

		if (!m_pVertexBuffer.CreateBuffer((uint32)(count * sizeof(mesh_vertex_normal)), 0, D3DUSAGE_WRITEONLY))
			break;

		mesh_vertex_normal* pBuffer;
		if (!m_pVertexBuffer.Lock((void**)&pBuffer, 0, 0))
			break;


		size_t index = 0;
		for (size_t pass = 0; pass < nPasses; pass++)
		{
			auto& p = passes[pass];

			if (p.geoset < 0 || !showGeosets[p.geoset])
				continue;

			size_t nLockedNum = p.indexCount / 3;
			int nVertexOffset = p.GetVertexStart(this);
			int nIndexOffset = p.m_nIndexStart;

			for (size_t i = 0; i < nLockedNum; ++i)
			{
				size_t nVB = 3 * i;
				for (int k = 0; k < 3; ++k, ++nVB)
				{
					int a = m_indices[nIndexOffset + nVB] + nVertexOffset;
					auto& out_vertex = pBuffer[index++];
					auto& ov = m_origVertices[a];
					out_vertex.p = ov.pos;
					out_vertex.n = ov.normal;
					out_vertex.uv = ov.texcoords;
				}
			}
		}


		m_pVertexBuffer.Unlock();
		auto usedSize = count * sizeof(mesh_vertex_normal);
		m_uUsedVB += usedSize;

		m_vbState = INITED;

		return;

	} while (false);

	m_pVertexBuffer.ReleaseBuffer();
	m_pIndexBuffer.ReleaseBuffer();
	m_vbState = NOT_USE;
}

void CParaXModel::initVertices(int nVertices, ModelVertex* pVertices)
{
	if (pVertices == NULL) return;
	// delete old
	m_objNum.nVertices = nVertices;
	SAFE_DELETE_ARRAY(m_origVertices);
	SAFE_DELETE_ARRAY(m_frame_number_vertices);

	// radius
	m_radius = (m_header.maxExtent - m_header.minExtent).length() / 2;

	/// read m_origVertices
	if (m_RenderMethod == SOFT_ANIM || m_RenderMethod == NO_ANIM || m_RenderMethod == BMAX_MODEL)
	{
		m_origVertices = new ModelVertex[nVertices];
		if (m_origVertices != 0)
			memcpy(m_origVertices, pVertices, nVertices * sizeof(ModelVertex));
		if (m_RenderMethod != BMAX_MODEL && m_RenderMethod != NO_ANIM)
		{
			m_frame_number_vertices = new int[nVertices];
			memset(m_frame_number_vertices, 0, sizeof(int)*nVertices);
			m_vertices = new Vector3[nVertices];
			m_normals = new Vector3[nVertices];
		}
		else
		{
			SAFE_DELETE_ARRAY(m_frame_number_vertices);
			SAFE_DELETE_ARRAY(m_vertices);
			SAFE_DELETE_ARRAY(m_normals);
		}
	}
	else if (m_RenderMethod == SHADER_ANIM)
	{
		/**
		* Create vertex buffer with skinning information
		*/
		if (!m_pVertexBuffer.IsValid())
		{
			if (m_pVertexBuffer.CreateBuffer(nVertices * sizeof(ModelVertex), 0, D3DUSAGE_WRITEONLY))
			{
				ModelVertex* pBuffer = NULL;
				if (m_pVertexBuffer.Lock((void**)&pBuffer, 0, 0))
				{
					memcpy(pBuffer, pVertices, nVertices * sizeof(ModelVertex));
					m_pVertexBuffer.Unlock();
				}
			}
		}
	}
	else if (m_RenderMethod == NO_ANIM) // NOT USED
	{
		/**
		* NOT USED: Create vertex buffer with only vertex information
		*/
		if (!m_pVertexBuffer.IsValid())
		{
			if (m_pVertexBuffer.CreateBuffer(nVertices * sizeof(mesh_vertex_normal), 0, D3DUSAGE_WRITEONLY))
			{
				mesh_vertex_normal* pBuffer = NULL;
				if (m_pVertexBuffer.Lock((void**)&pBuffer, 0, 0))
				{
					for (int i = 0; i < nVertices; i++) {
						pBuffer[i].p = (Vector3)pVertices[i].pos;
						pBuffer[i].n = (Vector3)pVertices[i].normal;
						pBuffer[i].uv = (Vector2)pVertices[i].texcoords;
					}
					m_pVertexBuffer.Unlock();
				}
			}
		}
	}
}

void CParaXModel::initIndices(int nIndices, uint16* pIndices)
{
	if (pIndices == 0) return;

	RenderDevicePtr pD3dDevice = CGlobals::GetRenderDevice();
	// delete old
	m_objNum.nIndices = nIndices;
	SAFE_DELETE_ARRAY(m_indices);
	if (m_RenderMethod == SOFT_ANIM || m_RenderMethod == NO_ANIM || m_RenderMethod == BMAX_MODEL)
	{
		m_indices = new uint16[nIndices];
		if (m_indices != 0)
			memcpy(m_indices, pIndices, sizeof(uint16)*nIndices);
	}
	else
	{
		if (!m_pIndexBuffer.IsValid())
		{
			if (m_pIndexBuffer.CreateIndexBuffer(sizeof(uint16)*(UINT)nIndices, D3DFMT_INDEX16, D3DUSAGE_WRITEONLY))
			{
				uint16* pIndexValues = NULL;
				if (m_pIndexBuffer.Lock((void**)&pIndexValues, 0, 0))
				{
					memcpy(pIndexValues, pIndices, sizeof(uint16)*nIndices);
					m_pIndexBuffer.Unlock();
				}
			}
		}
	}
}

void CParaXModel::initTranslucentFaceGroups()
{
	int nPasses = (int)passes.size();
	if (nPasses <= 0 || m_origVertices == 0)
		return;

	for (int nPass = 0; nPass < nPasses; nPass++)
	{
		ModelRenderPass &p = passes[nPass];
		// this is an transparent pass.
		if (p.blendmode != BM_OPAQUE && p.nozwrite && !p.force_local_tranparency)
		{
			CFaceGroup * pFaceGroup = new CFaceGroup();
			m_faceGroups.push_back(pFaceGroup);

			m_TranslucentPassIndice.resize(nPass + 1, -1);
			m_TranslucentPassIndice[nPass] = (int)(m_faceGroups.size() - 1);

			// copy data from mesh and material to face group.

			/// Set the texture
			TextureEntity* bindtex = NULL;
			if (specialTextures[p.tex] == -1)
				bindtex = textures[p.tex].get();
			else
			{
				bindtex = replaceTextures[specialTextures[p.tex]];
				// use default texture if replaceable texture is not specified. 
				if (bindtex == 0)
					bindtex = textures[p.tex].get();
			}
			pFaceGroup->m_pTexture = bindtex;
			pFaceGroup->m_alphaBlending = true;
			pFaceGroup->m_alphaTesting = false;
			pFaceGroup->m_bHasLighting = !(p.unlit);
			pFaceGroup->m_disableZWrite = p.nozwrite;
			pFaceGroup->m_bAdditive = (p.blendmode == BM_ADDITIVE) || (p.blendmode == BM_ADDITIVE_ALPHA);
			pFaceGroup->m_stripLength = p.m_fStripLength;
			pFaceGroup->m_bSkinningAni = p.skinningAni;
			// any material is ok. 
			ParaMaterial mat = CGlobals::GetSceneState()->GetCurrentMaterial();
			mat.Ambient = LinearColor(0.6f, 0.6f, 0.6f, 1.f);
			mat.Diffuse = LinearColor(1.f, 1.f, 1.f, 1.f);
			pFaceGroup->m_material = mat;

			// this gives zwrite enabled face a high priority to be rendered higher.
			if (!pFaceGroup->m_disableZWrite)
				pFaceGroup->m_order = 0;
			else
				pFaceGroup->m_order = 1;

			pFaceGroup->m_nNumTriangles = p.indexCount / 3;;

			for (int k = 0; k < pFaceGroup->m_nNumTriangles; ++k)
			{
				for (int j = 0; j < 3; j++)
				{
					ModelVertex& v = m_origVertices[m_indices[p.m_nIndexStart + k * 3 + j]];
					pFaceGroup->m_vertices.push_back((Vector3)(v.pos));
					pFaceGroup->m_normals.push_back((Vector3)(v.normal));
					pFaceGroup->m_UVs.push_back(v.texcoords);

					if (pFaceGroup->m_bSkinningAni)
					{
						uint32 packedValue = *((int32*)v.bones);
						pFaceGroup->m_boneIndices.push_back(packedValue);

						packedValue = *((int32*)v.weights);
						pFaceGroup->m_vertexWeights.push_back(packedValue);
					}
				}
			}
			pFaceGroup->UpdateCenterPos();
		}
	}
}

ModelAttachment& CParaXModel::NewAttachment(bool bOverwrite, int nAttachmentID, int nBoneIndex, const Vector3&  pivotPoint)
{
	if (m_attLookup[nAttachmentID] >= 0 && !bOverwrite)
	{
		return m_atts[m_attLookup[nAttachmentID]];
	}
	else
	{
		if (m_attLookup[nAttachmentID] >= 0 && bOverwrite)
		{
			ModelAttachment& att = m_atts[m_attLookup[nAttachmentID]];
			att.bone = nBoneIndex;
			att.pos = pivotPoint;
			return att;
		}
		else
		{
			m_atts.push_back(ModelAttachment());
			int nAttachmentIndex = (int)m_atts.size() - 1;
			ModelAttachment& att = m_atts[nAttachmentIndex];
			att.id = nAttachmentID;
			m_attLookup[nAttachmentID] = nAttachmentIndex;

			att.bone = nBoneIndex;
			att.pos = pivotPoint;
			m_objNum.nAttachments = (int)m_atts.size();

			if((int)m_objNum.nAttachLookup <= nAttachmentID)
				m_objNum.nAttachLookup = nAttachmentID + 1;
			return att;
		}
	}
}

bool CParaXModel::SetupTransformByID(int nID)
{
	int nAttachmentIndex = m_attLookup[nID];
	if (nAttachmentIndex >= 0)
	{
		m_atts[nAttachmentIndex].setup(this);
		return true;
	}
	else
		return false;
}


Matrix4* CParaXModel::GetAttachmentMatrix(Matrix4* pOut, int nAttachmentID, const AnimIndex& CurrentAnim, const AnimIndex& BlendingAnim, float blendingFactor, const AnimIndex & upperAnim, const AnimIndex & upperBlendingAnim, float upperBlendingFactor, bool bRecalcBone, IAttributeFields* pAnimInstance)
{
	int nAttachmentIndex = m_attLookup[nAttachmentID];
	if (nAttachmentIndex >= 0)
	{
		// the bone index at this attachment
		int nBoneIndex = m_atts[nAttachmentIndex].bone;
		Vector3 pos = m_atts[nAttachmentIndex].pos;

		uint32 nBones = (uint32)GetObjectNum().nBones;
		if (nBoneIndex < (int)nBones)
		{
			if (bRecalcBone)
			{
				/** calculate the bone and its parent bones */
				for (uint32 i = 0; i < nBones; i++)
				{
					bones[i].MakeDirty();
				}
			}
			if (bones[nBoneIndex].calcMatrix(bones, (bones[nBoneIndex].mIsUpper&&upperAnim.IsValid())?upperAnim:CurrentAnim, (bones[nBoneIndex].mIsUpper&&upperAnim.IsValid()) ? upperBlendingAnim : BlendingAnim, (bones[nBoneIndex].mIsUpper&&upperAnim.IsValid()) ? upperBlendingFactor : blendingFactor, pAnimInstance))
			{
				Matrix4 mat, mat1;
				mat1 = (bones[nBoneIndex].mat);
				mat.makeTrans(pos.x, pos.y, pos.z);
				mat1 = mat.Multiply4x3(mat1);
				*pOut = mat1;
				return pOut;
			}
		}
	}
	return NULL;
}


bool CParaXModel::HasAttachmentMatrix(int nAttachmentID)
{
	return (m_attLookup[nAttachmentID] >= 0);
}

void CParaXModel::PostCalculateBoneMatrix(uint32 nBones)
{
	for (uint32 i = 0; i < nBones; i++)
	{
		bones[i].PostCalculateBoneMatrix();
	}
}

void CParaXModel::calcBones()
{
	uint32 nBones = (uint32)GetObjectNum().nBones;
	for (uint32 i = 0; i < nBones; i++)
	{
		bones[i].MakeDirty();
	}

	for (uint32 i = 0; i < nBones; i++) {
		bones[i].calcMatrix(bones);
	}
	PostCalculateBoneMatrix(nBones);
}

void CParaXModel::calcBones(CharacterPose* pPose, const AnimIndex& CurrentAnim, const AnimIndex& BlendingAnim, float blendingFactor, const AnimIndex & upperAnim, const AnimIndex & upperBlendingAnim, float upperBlendingFactor, IAttributeFields* pAnimInstance)
{
	uint32 nBones = (uint32)GetObjectNum().nBones;

	// uncomment to fine tune performances for this part of code. 
	//#define PERFOAMRNCE_TEST_calcBones
#ifdef PERFOAMRNCE_TEST_calcBones
	if (nBones < 30)
		return;
	// PERF1("calcBones");

#endif

	for (uint32 i = 0; i < nBones; i++) {
		bones[i].MakeDirty();
	}

	if (pPose)
	{
		// TODO: check if this is an valid character model.
		if (pPose->m_fUpperBodyFacingAngle != 0.f && m_vNeckYawAxis != Vector3::ZERO)
		{
			int nHeadAttachmentIndex = m_attLookup[ATT_ID_HEAD];
			if (nHeadAttachmentIndex >= 0)
			{
				int nParent = m_atts[nHeadAttachmentIndex].bone;
				int nSpine = m_boneLookup[Bone_Spine];
				if (nParent >= 0 && nSpine >= 0)
				{
					int nStart = nParent;

					// tricky code: try to find if there are at least 4 spline bones from head to spine, in most cases, it is head, neck, spline1, spline
					int i = 4;
					for (; i >= 0 && nStart >= 0 && (nSpine != nStart); i--)
					{
						nStart = bones[nStart].parent;
					}
					bool bHasEnoughSpineBones = (i == 0);

					// just in case, some animator connect Thigh bones to spine and we have limited bones, we will ignore rotation
					if (bHasEnoughSpineBones && (nSpine == nStart) && m_boneLookup[Bone_L_Thigh] > 0 && bones[m_boneLookup[Bone_L_Thigh]].parent == nSpine) {
						bHasEnoughSpineBones = false;
					}

					if (!bHasEnoughSpineBones)
					{
						// rotate only head
						int nHead = m_boneLookup[Bone_Head];
						CBoneChain UpperBodyBoneChain(1);
						UpperBodyBoneChain.SetStartBone(bones, nHead, m_boneLookup);
						UpperBodyBoneChain.RotateBoneChain(m_vNeckYawAxis, bones, nBones, pPose->m_fUpperBodyFacingAngle, CurrentAnim, BlendingAnim, blendingFactor, upperAnim, upperBlendingAnim, upperBlendingFactor, pAnimInstance);
					}
					else
					{
						int nNeck = bones[nParent].parent; // get the NECK bone index
						int nRotateSpineBoneCount = 4;
						
						CBoneChain UpperBodyBoneChain(nRotateSpineBoneCount);
						UpperBodyBoneChain.SetStartBone(bones, nNeck, m_boneLookup);
						UpperBodyBoneChain.RotateBoneChain(m_vNeckYawAxis, bones, nBones, pPose->m_fUpperBodyFacingAngle, CurrentAnim, BlendingAnim, blendingFactor, upperAnim, upperBlendingAnim, upperBlendingFactor, pAnimInstance);
					}
				}
			}
			else
			{
				int nHeadIndex = m_boneLookup[Bone_Head];
				if (nHeadIndex >= 0)
				{
					CBoneChain UpperBodyBoneChain(1);
					UpperBodyBoneChain.SetStartBone(bones, nHeadIndex, m_boneLookup);
					UpperBodyBoneChain.RotateBoneChain(m_vNeckYawAxis, bones, nBones, pPose->m_fUpperBodyFacingAngle, CurrentAnim, BlendingAnim, blendingFactor, upperAnim, upperBlendingAnim, upperBlendingFactor, pAnimInstance);
				}
			}
		}
		if (pPose->m_fUpperBodyUpDownAngle != 0.f  && m_vNeckPitchAxis != Vector3::ZERO)
		{
			int nHeadIndex = m_boneLookup[Bone_Head];
			if (nHeadIndex >= 0)
			{
				CBoneChain UpperBodyBoneChain(1);
				UpperBodyBoneChain.SetStartBone(bones, nHeadIndex);
				UpperBodyBoneChain.RotateBoneChain(m_vNeckPitchAxis, bones, nBones, pPose->m_fUpperBodyUpDownAngle, CurrentAnim, BlendingAnim, blendingFactor, upperAnim, upperBlendingAnim, upperBlendingFactor, pAnimInstance);
			}
		}
	}
#ifdef PERFOAMRNCE_TEST_calcBones
	PERF1("calcBones");
#endif
	vector<Matrix4> lower_mats;
	vector<Matrix4> upper_mats;
	lower_mats.reserve(nBones);
	for (uint32 i = 0; i < nBones; i++) {
		bones[i].calcMatrix(bones, CurrentAnim, BlendingAnim, blendingFactor, pAnimInstance);
		lower_mats.push_back(bones[i].mat);
	}
	if (upperAnim.IsValid())
	{
		for (uint32 i = 0; i < nBones; i++) {
			bones[i].MakeDirty();
		}
		for (uint32 i = 0; i < nBones; i++) {
			bones[i].calcMatrix(bones, upperAnim, upperBlendingAnim, upperBlendingFactor, pAnimInstance);
			upper_mats.push_back(bones[i].mat);
		}
		for (uint32 i = 0; i < nBones; i++) {
			if (bones[i].mIsUpper)
				bones[i].mat = upper_mats[i];
			else
				bones[i].mat = lower_mats[i];
		}
	}
	PostCalculateBoneMatrix(nBones);
}

bool CParaXModel::HasAnimation()
{
	return animated;
}

void CParaXModel::animate(SceneState * pSceneState, CharacterPose* pPose, IAttributeFields* pAnimInstance)
{
	if (animated == false || !m_CurrentAnim.IsValid())
		return;

	if (animBones) {
		calcBones(pPose, m_CurrentAnim, m_BlendingAnim, blendingFactor, mUpperAnim, mUpperBlendingAnim, mUpperBlendingFactor, pAnimInstance);
	}

	uint32 nLights = GetObjectNum().nLights;
	for (size_t i = 0; i < nLights; i++) {
		if (lights[i].parent >= 0) {
			lights[i].tpos = bones[lights[i].parent].mat * lights[i].pos;
			lights[i].tdir = bones[lights[i].parent].mrot * lights[i].dir;
		}
	}

	if (m_CurrentAnim.Provider == 0)
	{
		if (pSceneState)
		{
			// TODO: non-local provider?	
			uint32 nParticleEmitters = GetObjectNum().nParticleEmitters;
			for (size_t i = 0; i < nParticleEmitters; i++) {
				// TODO:random time distribution
				// int pt = a.timeStart + (currentFrame + (int)(tmax*particleSystems[i].tofs)) % tmax;
				particleSystems[i].setup(pSceneState, m_CurrentAnim.nIndex, m_CurrentAnim.nCurrentFrame);
			}

			uint32 nRibbonEmitters = GetObjectNum().nRibbonEmitters;
			for (size_t i = 0; i < nRibbonEmitters; i++) {
				ribbons[i].setup(pSceneState, m_CurrentAnim.nIndex, m_CurrentAnim.nCurrentFrame);
			}

			if (animTextures) {
				uint32 nTexAnims = GetObjectNum().nTexAnims;
				for (size_t i = 0; i < nTexAnims; i++) {
					texanims[i].calc(m_CurrentAnim.nIndex, m_CurrentAnim.nCurrentFrame);
				}
			}
		}
	}
	else
	{
		// TODO: what happens when animating textures during external animation, such as the blink of eyes.
	}
}

// not used
void CParaXModel::RenderNoAnim(SceneState* pSceneState)
{
	int nPasses = (int)passes.size();
	if (nPasses <= 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	pd3dDevice->SetStreamSource(0, m_pVertexBuffer.GetDevicePointer(), 0, sizeof(mesh_vertex_normal));
	pd3dDevice->SetIndices(m_pIndexBuffer.GetDevicePointer());

	CEffectFile* pEffect = CGlobals::GetEffectManager()->GetCurrentEffectFile();
	if (pEffect == 0)
	{
#ifdef USE_DIRECTX_RENDERER
		///////////////////////////////////////////////////////////////////////////
		// fixed function pipeline
		for (int i = 0; i < nPasses; i++)
		{
			ModelRenderPass &p = passes[i];
			if (p.init(this, pSceneState))
			{
				// we don't want to render completely transparent parts
				RenderDevice::DrawIndexedPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, 0, 0, m_objNum.nVertices, p.m_nIndexStart, p.indexCount / 3);
				p.deinit();
			}
		}
#endif
	}
	else
	{
		//////////////////////////////////////////////////////////////////////////
		// programmable pipeline
		if (pEffect->begin())
		{
			if (pEffect->BeginPass(0))
			{
				for (int i = 0; i < nPasses; i++)
				{
					ModelRenderPass &p = passes[i];
					if (p.init_FX(this, pSceneState))
					{
						// we don't want to render completely transparent parts
						pEffect->CommitChanges();
						RenderDevice::DrawIndexedPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, 0, 0, m_objNum.nVertices, p.m_nIndexStart, p.indexCount / 3);
						p.deinit_FX(pSceneState);
					}
				}
				pEffect->EndPass(0);
			}
			pEffect->end();
		}
	}
	pd3dDevice->SetIndices(0);
}



void CParaXModel::RenderSoftNoAnim(SceneState* pSceneState, CParameterBlock* pMaterialParams)
{
	int nPasses = (int)passes.size();
	if (nPasses <= 0)
		return;


	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();

	if (m_vbState == INITED)
	{
		pd3dDevice->SetStreamSource(0, m_pVertexBuffer.GetDevicePointer(), 0, sizeof(mesh_vertex_normal));
	}
	else
	{
		DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_TEX1_NORM);
		pd3dDevice->SetStreamSource(0, pBufEntity->GetBuffer(), 0, sizeof(mesh_vertex_normal));
	}


	CEffectFile* pEffect = CGlobals::GetEffectManager()->GetCurrentEffectFile();
	size_t startVB = 0;
	if (pEffect == 0)
	{
		///////////////////////////////////////////////////////////////////////////
		// fixed function pipeline
		for (int nPass = 0; nPass < nPasses; nPass++)
		{
			ModelRenderPass &p = passes[nPass];

			if (p.geoset >= 0 && showGeosets[p.geoset])
			{
				// skip and build for translucent pass
				if (pSceneState->m_bEnableTranslucentFaceSorting &&
					((int)m_TranslucentPassIndice.size()) > nPass && m_TranslucentPassIndice[nPass] >= 0)
				{
					if (!pSceneState->IsIgnoreTransparent())
					{
						const Matrix4& mat = CGlobals::GetWorldMatrixStack().top();

						const ModelVertex& ov = m_origVertices[m_indices[p.m_nIndexStart]];
						CFaceGroupInstance faceGroup(&mat, m_faceGroups[m_TranslucentPassIndice[nPass]]);
						if (p.texanim != -1) {
							const TextureAnim& texAnim = texanims[p.texanim];
							faceGroup.m_vUVOffset.x = texAnim.tval.x;
							faceGroup.m_vUVOffset.y = texAnim.tval.y;

							faceGroup.m_vUVRotate = texAnim.rval;

							if (texAnim.scale.used)
							{
								faceGroup.m_vUVScale.x = texAnim.sval.x;
								faceGroup.m_vUVScale.y = texAnim.sval.y;
							}
						}
						pSceneState->GetFaceGroups()->AddFaceGroup(faceGroup);
					}

					continue;
				}

				if (p.init(this, pSceneState))
				{
					//DrawPass_NoAnim(p);
					DrawPass_NoAnim_VB(p, startVB);
					p.deinit();
				}
				startVB += p.indexCount;
			}
		}
	}
	else
	{
		//////////////////////////////////////////////////////////////////////////
		// programmable pipeline
		if (pEffect->begin())
		{
			if (pEffect->BeginPass(0))
			{
				/* if this is defined, we will combine render pass with similar textures and attributes.
				It is very strange that combining render pass is slower. */
				// #define COMBINE_RENDER_PASS

#ifdef COMBINE_RENDER_PASS
				ModelRenderPass* pLastPass = NULL;
#endif
				for (int nPass = 0; nPass < nPasses; nPass++)
				{
					ModelRenderPass &p = passes[nPass];

					if (p.geoset >= 0 && showGeosets[p.geoset])
					{
						// skip and build for translucent pass
						if (pSceneState->m_bEnableTranslucentFaceSorting &&
							((int)m_TranslucentPassIndice.size()) > nPass && m_TranslucentPassIndice[nPass] >= 0)
						{
							if (!pSceneState->IsIgnoreTransparent())
							{
								const Matrix4& mat = CGlobals::GetWorldMatrixStack().top();

								const ModelVertex& ov = m_origVertices[m_indices[p.m_nIndexStart]];
								CFaceGroupInstance faceGroup(&mat, m_faceGroups[m_TranslucentPassIndice[nPass]]);
								if (p.texanim != -1) {
									const TextureAnim& texAnim = texanims[p.texanim];
									faceGroup.m_vUVOffset.x = texAnim.tval.x;
									faceGroup.m_vUVOffset.y = texAnim.tval.y;

									faceGroup.m_vUVRotate = texAnim.rval;

									if (texAnim.scale.used)
									{
										faceGroup.m_vUVScale.x = texAnim.sval.x;
										faceGroup.m_vUVScale.y = texAnim.sval.y;
									}


									//support texture uv rgb animation --clayman 2011.8.8
									if (animTexRGB)
										faceGroup.m_UVRgbAnim = true;

								}
								pSceneState->GetFaceGroups()->AddFaceGroup(faceGroup);
							}

							continue;
						}
#ifdef COMBINE_RENDER_PASS
						// we shall combine render pass if current one is same as previous, using the overloaded p.operator == 
						if (pLastPass == NULL)
						{
							if (p.init_FX(this))
							{
								pLastPass = &p;
								pEffect->CommitChanges();
								//DrawPass_NoAnim(p);
								DrawPass_NoAnim_VB(p, startVB);
							}

							startVB += p.indexCount;
						}
						else
						{
							if ((*pLastPass == p))
							{
								DrawPass_NoAnim_VB(p, startVB);
								startVB += p.indexCount;
							}
							else
							{
								pLastPass->deinit_FX(pSceneState, pMaterialParams);
								if (p.init_FX(this, pMaterialParams))
								{
									pLastPass = &p;
									pEffect->CommitChanges();
									DrawPass_NoAnim_VB(p, startVB);
								}
								startVB += p.indexCount;
							}
						}
#else
						// do not combine render pass. this appears to be faster than combined render passes. 
						if (p.init_FX(this, pSceneState, pMaterialParams))
						{
							pEffect->CommitChanges();
							DrawPass_NoAnim_VB(p, startVB);
							p.deinit_FX(pSceneState, pMaterialParams);
						}
						startVB += p.indexCount;
#endif

					}
				}
#ifdef COMBINE_RENDER_PASS
				if (pLastPass != NULL)
				{
					pLastPass->deinit_FX(pSceneState, pMaterialParams);
				}
#endif
				pEffect->EndPass(0);
			}
			pEffect->end();
		}
	}

}


void CParaXModel::RenderBMaxModel(SceneState* pSceneState, CParameterBlock* pMaterialParams)
{
	int nPasses = (int)passes.size();
	if (nPasses <= 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();

	if (m_vbState == INITED)
	{
		pd3dDevice->SetStreamSource(0, m_pVertexBuffer.GetDevicePointer(), 0, sizeof(bmax_vertex));
	}
	else
	{
		DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_NORM_DIF);
		pd3dDevice->SetStreamSource(0, pBufEntity->GetBuffer(), 0, sizeof(bmax_vertex));
	}

	CEffectFile* pEffect = CGlobals::GetEffectManager()->GetCurrentEffectFile();
	size_t startVB = 0;
	if (pEffect == 0)
	{
#ifdef USE_DIRECTX_RENDERER
		///////////////////////////////////////////////////////////////////////////
		// fixed function pipeline
		for (int nPass = 0; nPass < nPasses; nPass++)
		{
			ModelRenderPass &p = passes[nPass];
			if (p.geoset >= 0 && showGeosets[p.geoset])
			{
				if (p.init_bmax_FX(this, pSceneState))
				{
					//DrawPass_BMax(p);
					DrawPass_BMax_VB(p, startVB);
					p.deinit_bmax_FX(pSceneState);
				}

				startVB += p.indexCount;
			}
		}
#endif
	}
	else
	{
		//////////////////////////////////////////////////////////////////////////
		// programmable pipeline
		if (pEffect->begin())
		{
			if (pEffect->BeginPass(0))
			{
				for (int nPass = 0; nPass < nPasses; nPass++)
				{
					ModelRenderPass &p = passes[nPass];

					if (p.geoset >=0 && showGeosets[p.geoset])
					{
						// do not combine render pass. this appears to be faster than combined render passes. 
						if (p.init_bmax_FX(this, pSceneState, pMaterialParams))
						{
							pEffect->CommitChanges();
							DrawPass_BMax_VB(p, startVB);
							p.deinit_bmax_FX(pSceneState);
						}
						startVB += p.indexCount;
					}
				}
				pEffect->EndPass(0);
			}
			pEffect->end();
		}
	}
}

void CParaXModel::RenderSoftAnim(SceneState* pSceneState, CParameterBlock* pMaterialParams)
{
	int nPasses = (int)passes.size();
	if (nPasses <= 0)
		return;
	// define this to generate performance report
	//#define RenderSoftAnim_PERFORMANCE_TEST
#ifdef RenderSoftAnim_PERFORMANCE_TEST
	PERF1("RenderSoftAnim");
#endif


	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_TEX1_NORM);
	pd3dDevice->SetStreamSource(0, pBufEntity->GetBuffer(), 0, sizeof(mesh_vertex_normal));

	CEffectFile* pEffect = CGlobals::GetEffectManager()->GetCurrentEffectFile();
	if (pEffect == 0)
	{
#ifdef USE_DIRECTX_RENDERER
		///////////////////////////////////////////////////////////////////////////
		// fixed function pipeline
		for (int nPass = 0; nPass < nPasses; nPass++)
		{
			ModelRenderPass &p = passes[nPass];

			if (p.geoset >= 0 && showGeosets[p.geoset])
			{
				// skip and build for translucent pass
				if (pSceneState->m_bEnableTranslucentFaceSorting &&
					((int)m_TranslucentPassIndice.size()) > nPass && m_TranslucentPassIndice[nPass] >= 0)
				{
					if (!pSceneState->IsIgnoreTransparent())
					{
						Matrix4 mat = CGlobals::GetWorldMatrixStack().top();

						const ModelVertex& ov = m_origVertices[m_indices[p.m_nIndexStart]];
						// use the four bone matrix. 
						if (ov.weights[0] > 0)
						{
							Matrix4 matLocal = bones[ov.bones[0]].mat*((float)ov.weights[0] * (1 / 255.0f));
							for (int b = 1; b < 4 && ov.weights[b]>0; b++) {
								matLocal += bones[ov.bones[b]].mat*((float)ov.weights[b] * (1 / 255.0f));
							}
							mat = matLocal * mat;
						}
						CFaceGroupInstance faceGroup(&mat, m_faceGroups[m_TranslucentPassIndice[nPass]]);
						if (p.texanim != -1) {
							const TextureAnim& texAnim = texanims[p.texanim];
							faceGroup.m_vUVOffset.x = texAnim.tval.x;
							faceGroup.m_vUVOffset.y = texAnim.tval.y;

							faceGroup.m_vUVRotate = texAnim.rval;

							if (texAnim.scale.used)
							{
								faceGroup.m_vUVScale.x = texAnim.sval.x;
								faceGroup.m_vUVScale.y = texAnim.sval.y;
							}
						}
						pSceneState->GetFaceGroups()->AddFaceGroup(faceGroup);
					}

					continue;
				}

				if (p.init(this, pSceneState))
				{
					DrawPass(p);
					p.deinit();
				}
			}
		}
#endif
	}
	else
	{
		//////////////////////////////////////////////////////////////////////////
		// programmable pipeline
		if (pEffect->begin())
		{
			if (pEffect->BeginPass(0))
			{
				/* if this is defined, we will combine render pass with similar textures and attributes.
				It is very strange that combining render pass is slower. */
				// #define COMBINE_RENDER_PASS

#ifdef COMBINE_RENDER_PASS
				ModelRenderPass* pLastPass = NULL;
#endif
				for (int nPass = 0; nPass < nPasses; nPass++)
				{
					ModelRenderPass &p = passes[nPass];

					if (p.geoset >= 0 && showGeosets[p.geoset])
					{
						// skip and build for translucent pass
						if (pSceneState->m_bEnableTranslucentFaceSorting &&
							((int)m_TranslucentPassIndice.size()) > nPass && m_TranslucentPassIndice[nPass] >= 0)
						{
							if (!pSceneState->IsIgnoreTransparent())
							{
								float alpha = 1.f;
								if (p.opacity != -1)
								{
									//typing error,m_CurrentAnim.nIndex is always 0?? 
									//change m_CurrentAnim.nIndex to m_CurrentAnim  --clayman 2012.8.21
									//alpha = transparency[p.opacity].trans.getValue(m_CurrentAnim.nIndex);
									alpha = transparency[p.opacity].trans.getValue(m_CurrentAnim);
									if (alpha < 0)
										continue;
								}

								Matrix4 mat = CGlobals::GetWorldMatrixStack().top();

								const ModelVertex& ov = m_origVertices[m_indices[p.m_nIndexStart]];
								// use four bone matrix. 
								if (ov.weights[0] > 0 && m_faceGroups[m_TranslucentPassIndice[nPass]]->m_bSkinningAni == false)
								{
									Matrix4 matLocal = bones[ov.bones[0]].mat*((float)ov.weights[0] * (1 / 255.0f));
									for (int b = 1; b < 4 && ov.weights[b]>0; b++) {
										matLocal += bones[ov.bones[b]].mat*((float)ov.weights[b] * (1 / 255.0f));
									}
									mat = matLocal * mat;
								}
								CFaceGroupInstance faceGroup(&mat, m_faceGroups[m_TranslucentPassIndice[nPass]]);
								if (p.texanim != -1) {
									const TextureAnim& texAnim = texanims[p.texanim];
									faceGroup.m_vUVOffset.x = texAnim.tval.x;
									faceGroup.m_vUVOffset.y = texAnim.tval.y;

									faceGroup.m_vUVRotate = texAnim.rval;

									if (texAnim.scale.used)
									{
										faceGroup.m_vUVScale.x = texAnim.sval.x;
										faceGroup.m_vUVScale.y = texAnim.sval.y;
									}

									//support texture uv rgb animation --clayman 2011.8.8
									if (animTexRGB)
										faceGroup.m_UVRgbAnim = true;
								}
								// opacity
								faceGroup.m_fAlpha = alpha;
								faceGroup.m_bones = bones;
								pSceneState->GetFaceGroups()->AddFaceGroup(faceGroup);
							}

							continue;
						}
#ifdef COMBINE_RENDER_PASS
						// we shall combine render pass if current one is same as previous, using the overloaded p.operator == 
						if (pLastPass == NULL)
						{
							if (p.init_FX(this))
							{
								pLastPass = &p;
								pEffect->CommitChanges();
								DrawPass(p);
							}
						}
						else
						{
							if ((*pLastPass == p))
							{
								DrawPass(p);
							}
							else
							{
								pLastPass->deinit_FX(pSceneState, pMaterialParams);
								if (p.init_FX(this))
								{
									pLastPass = &p;
									pEffect->CommitChanges();
									DrawPass(p);
								}
							}
						}
#else
						// do not combine render pass. this appears to be faster than combined render passes. 
						if (p.init_FX(this, pSceneState, pMaterialParams))
						{
							pEffect->onDrawPass(pMaterialParams, nPass);
							pEffect->CommitChanges();
							DrawPass(p);
							p.deinit_FX(pSceneState, pMaterialParams);
						}
#endif
					}
				}
#ifdef COMBINE_RENDER_PASS
				if (pLastPass != NULL)
				{
					pLastPass->deinit_FX(pSceneState, pMaterialParams);
				}
#endif
				pEffect->EndPass(0);
			}
			pEffect->end();
		}
	}
}

void CParaXModel::DrawPass_BMax_VB(ModelRenderPass &p, size_t start)
{
	if (m_vbState != INITED)
	{
		DrawPass_BMax(p);
		return;
	}

	if (p.indexCount == 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	RenderDevice::DrawPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, (UINT)start, p.indexCount / 3);
}

void CParaXModel::DrawPass_NoAnim_VB(ModelRenderPass &p, size_t start)
{
	if (m_vbState != INITED)
	{
		DrawPass_NoAnim(p);
		return;
	}

	if (p.indexCount == 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	RenderDevice::DrawPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, (UINT)start, p.indexCount / 3);
}


void CParaXModel::DrawPass_NoAnim(ModelRenderPass &p)
{
	if (p.indexCount == 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();

	{
		mesh_vertex_normal* vb_vertices = NULL;
		int nVertexOffset = p.GetVertexStart(this);
		ModelVertex *ov = m_origVertices;
		int nNumLockedVertice;
		int nNumFinishedVertice = 0;

		int nIndexOffset = p.m_nIndexStart;

		DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_TEX1_NORM);
		do
		{
			if ((nNumLockedVertice = pBufEntity->Lock((p.indexCount - nNumFinishedVertice),
				(void**)(&vb_vertices))) > 0)
			{
				int nLockedNum = nNumLockedVertice / 3;

				int nIndexOffset = p.m_nIndexStart + nNumFinishedVertice;
				for (int i = 0; i < nLockedNum; ++i)
				{
					int nVB = 3 * i;
					for (int k = 0; k < 3; ++k, ++nVB)
					{
						int a = m_indices[nIndexOffset + nVB] + nVertexOffset;
						mesh_vertex_normal& out_vertex = vb_vertices[nVB];
						// weighted vertex
						ov = m_origVertices + a;
						out_vertex.p = ov->pos;
						out_vertex.n = ov->normal;
						out_vertex.uv = ov->texcoords;
					}
				}
				pBufEntity->Unlock();

				if (pBufEntity->IsMemoryBuffer())
					RenderDevice::DrawPrimitiveUP(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, nLockedNum, pBufEntity->GetBaseVertexPointer(), pBufEntity->m_nUnitSize);
				else
					RenderDevice::DrawPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, pBufEntity->GetBaseVertex(), nLockedNum);

				if ((p.indexCount - nNumFinishedVertice) > nNumLockedVertice)
				{
					nNumFinishedVertice += nNumLockedVertice;
				}
				else
					break;
			}
			else
				break;
		} while (1);
	}
}


void CParaXModel::DrawPass_BMax(ModelRenderPass &p)
{
	if (p.indexCount == 0)
		return;

	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	bmax_vertex* vb_vertices = NULL;
	ModelVertex *ov = m_origVertices;
	int nNumLockedVertice;
	int nNumFinishedVertice = 0;
	DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_NORM_DIF);
	do
	{
		if ((nNumLockedVertice = pBufEntity->Lock((p.indexCount - nNumFinishedVertice),
			(void**)(&vb_vertices))) > 0)
		{
			int nLockedNum = nNumLockedVertice / 3;

			bmax_vertex  vertex;
			int nIndexOffset = p.m_nIndexStart + nNumFinishedVertice;
			int nVertexOffset = p.GetVertexStart(this);
			ModelVertex* origVertices = m_origVertices + nVertexOffset;
			if (HasAnimation())
			{
				for (int i = 0; i < nLockedNum; ++i)
				{
					int nVB = 3 * i;
					for (int k = 0; k < 3; ++k, ++nVB)
					{
						int a = m_indices[nIndexOffset + nVB];
						bmax_vertex& out_vertex = vb_vertices[nVB];
						// weighted vertex
						ov = origVertices + a;

						float weight = ov->weights[0] * (1 / 255.0f);
						Bone& bone = bones[ov->bones[0]];
						Vector3 v = (ov->pos * bone.mat)*weight;
						Vector3 n = ov->normal.TransformNormal(bone.mrot) * weight;
						for (int b = 1; b < 4 && ov->weights[b]>0; b++) {
							weight = ov->weights[b] * (1 / 255.0f);
							Bone& bone = bones[ov->bones[b]];
							v += (ov->pos * bone.mat) * weight;
							n += ov->normal.TransformNormal(bone.mrot) * weight;
						}
						out_vertex.p = v;
						out_vertex.n = n;
						out_vertex.color = ov->color0;
					}
				}
			}
			else
			{
				for (int i = 0; i < nLockedNum; ++i)
				{
					int nVB = 3 * i;
					for (int k = 0; k < 3; ++k, ++nVB)
					{
						uint16 a = m_indices[nIndexOffset + nVB];
						bmax_vertex& out_vertex = vb_vertices[nVB];
						ov = origVertices + a;
						out_vertex.p = ov->pos;
						out_vertex.n = ov->normal;
						out_vertex.color = ov->color0;
					}
				}
			}

			pBufEntity->Unlock();

			if (pBufEntity->IsMemoryBuffer())
				RenderDevice::DrawPrimitiveUP(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, nLockedNum, pBufEntity->GetBaseVertexPointer(), pBufEntity->m_nUnitSize);
			else
				RenderDevice::DrawPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, pBufEntity->GetBaseVertex(), nLockedNum);

			if ((p.indexCount - nNumFinishedVertice) > nNumLockedVertice)
			{
				nNumFinishedVertice += nNumLockedVertice;
			}
			else
				break;
		}
		else
			break;
	} while (1);
}

void CParaXModel::DrawPass(ModelRenderPass &p)
{
	// uncomment to generate performance result in order to fine tune optimizations.  
	// #define DO_PERFORMANCE_TEST
	if (p.indexCount == 0)
		return;
	if (p.is_rigid_body)
	{
		// for rigid body with many vertices, do skinning on GPU instead of CPU. 
		DrawPass_NoAnim(p);
		return;
	}

#ifdef DO_PERFORMANCE_TEST
	if (p.indexCount < 500)
		return;
	PERF1("SoftSkinningDrawPass");
#endif
	RenderDevicePtr pd3dDevice = CGlobals::GetRenderDevice();
	mesh_vertex_normal* vb_vertices = NULL;
	ModelVertex *ov = m_origVertices;
	int nVertexOffset = p.GetVertexStart(this);
	int nNumLockedVertice;
	int nNumFinishedVertice = 0;
	DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_TEX1_NORM);

	do
	{
		if ((nNumLockedVertice = pBufEntity->Lock((p.indexCount - nNumFinishedVertice),
			(void**)(&vb_vertices))) > 0)
		{
			int nLockedNum = nNumLockedVertice / 3;

#ifdef DO_PERFORMANCE_TEST
			if (nLockedNum > 200)
			{
				PERF1("SoftSkinning");
#endif
				mesh_vertex_normal  vertex;
				int nIndexOffset = p.m_nIndexStart + nNumFinishedVertice;
				for (int i = 0; i < nLockedNum; ++i)
				{
					int nVB = 3 * i;
					for (int k = 0; k < 3; ++k, ++nVB)
					{
						int a = m_indices[nIndexOffset + nVB] + nVertexOffset;
						mesh_vertex_normal& out_vertex = vb_vertices[nVB];
						// weighted vertex
						ov = m_origVertices + a;

						// uncomment to detect incorrect index. 
						// assert(a < m_objNum.nVertices, "index overflow");

						// TODO: m_nCurrentFrameNumber can not be replaced by CGlobals::GetViewportManager()->getCurrentFrameNumber()
						if (m_frame_number_vertices[a] != m_nCurrentFrameNumber)
						{
							m_frame_number_vertices[a] = m_nCurrentFrameNumber;

							float weight = ov->weights[0] * (1 / 255.0f);
							Bone& bone = bones[ov->bones[0]];
							Vector3 v = (ov->pos * bone.mat)*weight;
							Vector3 n = ov->normal.TransformNormal(bone.mrot) * weight;
							for (int b = 1; b < 4 && ov->weights[b]>0; b++) {
								weight = ov->weights[b] * (1 / 255.0f);
								Bone& bone = bones[ov->bones[b]];
								v += (ov->pos * bone.mat) * weight;
								n += ov->normal.TransformNormal(bone.mrot) * weight;
							}
							out_vertex.p = v;
							out_vertex.n = n;

							// save the animated vertex in case it is reused in the same frame. 
							m_vertices[a] = v;
							m_normals[a] = n;
						}
						else
						{
							out_vertex.p = m_vertices[a];
							out_vertex.n = m_normals[a];
						}
						out_vertex.uv = ov->texcoords;
					}
				}
#ifdef DO_PERFORMANCE_TEST
			}
#endif
			pBufEntity->Unlock();

			if (pBufEntity->IsMemoryBuffer())
				RenderDevice::DrawPrimitiveUP(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, nLockedNum, pBufEntity->GetBaseVertexPointer(), pBufEntity->m_nUnitSize);
			else
				RenderDevice::DrawPrimitive(pd3dDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, pBufEntity->GetBaseVertex(), nLockedNum);

			if ((p.indexCount - nNumFinishedVertice) > nNumLockedVertice)
			{
				nNumFinishedVertice += nNumLockedVertice;
			}
			else
				break;
		}
		else
			break;
	} while (1);
}

void CParaXModel::RenderShaderAnim(SceneState* pSceneState)
{

}

void CParaXModel::drawModel(SceneState * pSceneState, CParameterBlock* pMaterialParam, int nRenderMethod)
{
	if (passes.size() == 0)
		return;
	CEffectFile* pEffect = CGlobals::GetEffectManager()->GetCurrentEffectFile();
	if (pEffect == 0)
		CGlobals::GetRenderDevice()->SetTransform(D3DTS_WORLD, CGlobals::GetWorldMatrixStack().SafeGetTop().GetConstPointer());
	else
	{
		/// apply surface materials
		bool bEnableLight = pSceneState->GetScene()->IsLightEnabled();
		if (bEnableLight)
		{
			ParaMaterial mat = pSceneState->GetCurrentMaterial();
			if (!pSceneState->HasLocalMaterial())
				mat.Diffuse = LinearColor(1.f, 1.f, 1.f, 1.f);
			pEffect->applySurfaceMaterial(&mat);
		}
		else
		{
			ParaMaterial mat = pSceneState->GetCurrentMaterial();
			if (!pSceneState->HasLocalMaterial())
			{
				mat.Ambient = LinearColor(0.6f, 0.6f, 0.6f, 1.f); // shall we use ambient to simulate lighting, when lighting is disabled.
				mat.Diffuse = LinearColor(1.f, 1.f, 1.f, 1.f);
			}
			pEffect->applySurfaceMaterial(&mat);
		}
	}



	if (nRenderMethod < 0)
		nRenderMethod = m_RenderMethod;

	if (m_vbState == NOT_SET)
	{
		if (nRenderMethod == NO_ANIM
			|| (nRenderMethod == BMAX_MODEL && !HasAnimation()))
		{
			if (m_uUsedVB < MAX_USE_VERTEX_BUFFER_SIZE)
			{
				m_vbState = NEED_INIT;
				InitVertexBuffer();
			}
		}
		else
		{
			m_vbState = NOT_USE;
		}
	}

	switch (nRenderMethod)
	{
	case SHADER_ANIM:
		RenderShaderAnim(pSceneState);
		break;
	case SOFT_ANIM:
		RenderSoftAnim(pSceneState, pMaterialParam);
		break;
	case NO_ANIM:
	{
		RenderSoftNoAnim(pSceneState, pMaterialParam);
	}
	break;
	case BMAX_MODEL:
	{
		RenderBMaxModel(pSceneState, pMaterialParam);
	}

	break;
	default:
		break;
	}
}

void CParaXModel::BuildShadowVolume(ShadowVolume * pShadowVolume, LightParams* pLight, Matrix4* mxWorld)
{
	// TODO: for animation, the m_indices are null. figure out how.
	if (m_RenderMethod == NO_ANIM)
	{
		return;
	}
#ifdef USE_DIRECTX_RENDERER
#ifdef SHADOW_ZFAIL_WITHOUTCAPS
	pShadowVolume->m_shadowMethod = ShadowVolume::SHADOW_Z_PASS;
	//geosets.BuildShadowVolume(this,currentAnimInfo, pShadowVolume, pLight, mxWorld);
	pShadowVolume->m_shadowMethod = ShadowVolume::SHADOW_Z_FAIL;
#else
	// get the bounding box and check which shadow rendering method we use.
	const Vector3& mMinimum = m_header.minExtent;
	const Vector3& mMaximum = m_header.maxExtent;

	/** check if object is too small, if so its shadow will not be rendered */
	{
		Vector3 bottom, top;
		bottom = (mMinimum + mMaximum) / 2.0f;
		bottom.y = mMinimum.y;
		top = bottom;
		top.y = mMaximum.y;
		Vector3 screenTop, screenBottom;
		pShadowVolume->ProjectPoint(&screenBottom, &bottom, mxWorld);
		pShadowVolume->ProjectPoint(&screenTop, &top, mxWorld);

		float screenDistX = (float)fabs(screenTop.x - screenBottom.x);
		float screenDistY = (float)fabs(screenTop.y - screenBottom.y);
		if (screenDistX < pShadowVolume->m_fMinShadowCastDistance && screenDistY < pShadowVolume->m_fMinShadowCastDistance)
		{
			pShadowVolume->m_shadowMethod = ShadowVolume::SHADOW_NONE;
			return;
		}
	}
	/** check to see if object may be in shadow. We only performance this test if object does not
	enforce capping */
	// if(not capping)
	{
		Vector3 mCorners[8];
		mCorners[0] = mMinimum;
		mCorners[1].x = mMinimum.x; mCorners[1].y = mMaximum.y; mCorners[1].z = mMinimum.z;
		mCorners[2].x = mMaximum.x; mCorners[2].y = mMaximum.y; mCorners[2].z = mMinimum.z;
		mCorners[3].x = mMaximum.x; mCorners[3].y = mMinimum.y; mCorners[3].z = mMinimum.z;

		mCorners[4] = mMaximum;
		mCorners[5].x = mMinimum.x; mCorners[5].y = mMaximum.y; mCorners[5].z = mMaximum.z;
		mCorners[6].x = mMinimum.x; mCorners[6].y = mMinimum.y; mCorners[6].z = mMaximum.z;
		mCorners[7].x = mMaximum.x; mCorners[7].y = mMinimum.y; mCorners[7].z = mMaximum.z;

		for (int i = 0; i < 8; i++)
		{
			ParaVec3TransformCoord(&mCorners[i], &mCorners[i], mxWorld);
		}

		if (pShadowVolume->PointsInsideOcclusionPyramid(mCorners, 8))
		{
			/** we use z-fail algorithm, if camera may be in the shadow or the object does not
			performance screen distance testing */
			pShadowVolume->m_shadowMethod = ShadowVolume::SHADOW_Z_FAIL;
		}
		else
			pShadowVolume->m_shadowMethod = ShadowVolume::SHADOW_Z_PASS;
	}
	/** build the shadow volume */

	// TODO: light's direction relative to the object.
	// here we assume the light is a directional light.
	Vector3 vLight = pLight->Direction;
	float fRange = pLight->Range;
	vLight = -vLight;

	int nUseCap = ((pShadowVolume->m_shadowMethod == ShadowVolume::SHADOW_Z_FAIL) ? 1 : 0);
	bool bBaseModelRendered = false;
	for (size_t i = 0; i < passes.size(); i++) {
		ModelRenderPass &p = passes[i];

		/**
		* TODO: although, we don't want to render completely transparent parts,
		* we will render it anyway if the geoset is 0, which is usually the base model.
		* this is just a work around. In future, I will specify a certain geoset ID as the shadow model and render it only.
		*/
		if ((p.geoset >= 0 && showGeosets[p.geoset]) && (p.blendmode == BM_OPAQUE || (p.geoset == 0 && !bBaseModelRendered)))
		{
			if (p.geoset == 0)
				bBaseModelRendered = true;
			ModelVertex *ov = m_origVertices;
			int nNumFaces = p.indexCount / 3;
			Vector3 * pVertices = NULL;
			DWORD dwNumVertices = 0;
			DWORD dwNumEdges = 0;

			// Allocate a temporary edge list
			std::unordered_set <EdgeHash, hash_compare_edge> m_edgeTable;
			if (nUseCap > 0)
				pShadowVolume->ReserveNewBlock(&pVertices, nNumFaces * 3);

			// the three vertices of each face
			Vector3 FaceV[3];
			WORD wFace[3]; // index of the three vertices of each face
			for (int i = 0; i < nNumFaces; ++i)
			{
				// compute the three vertices of each face
				for (int k = 0; k < 3; ++k)
				{
					int nVB = 3 * i + k;
					wFace[k] = m_indices[p.m_nIndexStart + nVB];
					// weighted vertex
					ParaVec3TransformCoord(&(FaceV[k]), &GetWeightedVertexByIndex(wFace[k]), mxWorld);
				}
				// Transform vertices or transform light?
				// we use vertex transform, it may be more accurate to use light transform
				Vector3 vCross1(FaceV[2] - FaceV[1]);
				Vector3 vCross2(FaceV[1] - FaceV[0]);
				Vector3 vNormal;
				vNormal = vCross1.crossProduct(vCross2);

				if (vNormal.dotProduct(vLight) >= 0.0f)
				{
					CEdgeBuilder::AddEdge(m_edgeTable, dwNumEdges, wFace[0], wFace[1]);
					CEdgeBuilder::AddEdge(m_edgeTable, dwNumEdges, wFace[1], wFace[2]);
					CEdgeBuilder::AddEdge(m_edgeTable, dwNumEdges, wFace[2], wFace[0]);

					if (nUseCap > 0)
					{
						pVertices[dwNumVertices++] = FaceV[0];
						pVertices[dwNumVertices++] = FaceV[2];
						pVertices[dwNumVertices++] = FaceV[1];
					}
				}
			} // for(int i=0;i<nNumFaces;++i)

			if (nUseCap > 0)
			{
				// commit shadow volume front cap vertices
				pShadowVolume->CommitBlock(dwNumVertices);
				dwNumVertices = 0;
				pVertices = NULL;
			}
			/**
			build shadow volume for the edge array
			Interestingly, the extrusion of geometries for point light sources and
			infinite directional light sources are different. see below.
			*/
			if (pLight->bIsDirectional)
			{
				/**
				infinite directional light sources would extrude all silhouette edges to
				a single point at infinity.
				*/
				pShadowVolume->ReserveNewBlock(&pVertices, dwNumEdges * 3);
				Vector3 v3 = Vector3(mxWorld->_41, mxWorld->_42, mxWorld->_43) + pLight->Direction * pLight->Range;

				std::unordered_set <EdgeHash, hash_compare_edge>::iterator itCurCP, itEndCP = m_edgeTable.end();

				// first shutdown all connections
				for (itCurCP = m_edgeTable.begin(); itCurCP != itEndCP; ++itCurCP)
				{
					int index1 = (*itCurCP).m_v0;
					int index2 = (*itCurCP).m_v1;

					Vector3 v1 = GetWeightedVertexByIndex(index1);
					Vector3 v2 = GetWeightedVertexByIndex(index2);
					ParaVec3TransformCoord(&v1, &v1, mxWorld);
					ParaVec3TransformCoord(&v2, &v2, mxWorld);

					// Add a quad (two triangles) to the vertex list
					pVertices[dwNumVertices++] = v1;
					pVertices[dwNumVertices++] = v2;
					pVertices[dwNumVertices++] = v3;
				}
				pShadowVolume->CommitBlock(dwNumVertices);
			}
		}
	}
#endif
#endif
}

Vector3 CParaXModel::GetWeightedVertexByIndex(unsigned short nIndex)
{
	ModelVertex* ov = m_origVertices + nIndex;
	Vector3 v = bones[ov->bones[0]].mat * ov->pos * ((float)ov->weights[0] * (1 / 255.0f));
	for (int b = 1; b < 4 && ov->weights[b]>0; b++) {
		v += bones[ov->bones[b]].mat * ov->pos * ((float)ov->weights[b] * (1 / 255.0f));
	}
	return (Vector3)v;
}


void CParaXModel::draw(SceneState * pSceneState, CParameterBlock* materialParams, int nRenderMethod)
{
	if (!m_bIsValid) return;

	m_nCurrentFrameNumber++;

	if (!animated) {
		// TODO: maybe a faster way to render using Static mesh interface
		// so there is no need to go with render passes
		drawModel(pSceneState, materialParams, nRenderMethod);
	}
	else {
		/// assume that the animate() function has already been called to set the bone matrices

		drawModel(pSceneState, materialParams, nRenderMethod);

		if (!pSceneState->IsIgnoreTransparent())
		{
			// update particles
			float fDeltaTime = (float)pSceneState->dTimeDelta;
			if (fDeltaTime > 0)
			{
				updateEmitters(pSceneState, fDeltaTime);
			}
			// draw particle systems
			uint32 nParticleEmitters = GetObjectNum().nParticleEmitters;
			for (size_t i = 0; i < nParticleEmitters; i++) {
				particleSystems[i].draw(pSceneState);
			}

			// draw ribbons
			uint32 nRibbonEmitters = GetObjectNum().nRibbonEmitters;
			for (size_t i = 0; i < nRibbonEmitters; i++) {
				ribbons[i].draw(pSceneState);
			}
		}
	}
}

void CParaXModel::lightsOn(uint32 lbase)
{
	// setup lights
	uint32 nLights = GetObjectNum().nLights;
	for (uint32 i = 0, l = lbase; i < nLights; i++)
		lights[i].setup(m_CurrentAnim.nCurrentFrame, l++);
}

void CParaXModel::lightsOff(uint32 lbase)
{
}

void CParaXModel::updateEmitters(SceneState * pSceneState, float dt)
{
	if (!m_bIsValid) return;
	uint32 nParticleEmitters = GetObjectNum().nParticleEmitters;
	for (size_t i = 0; i < nParticleEmitters; i++) {
		particleSystems[i].update(pSceneState, dt);
	}
}

float CParaXModel::GetBoundingRadius()
{
	return m_radius;
};

void CParaXModel::drawBones()
{

}

void CParaXModel::drawBoundingVolume()
{

}
bool CParaXModel::canAttach(int id)
{
	return ((int)GetObjectNum().nAttachLookup > id) && (m_attLookup[id] != -1);
}

int CParaXModel::GetPolyCount()
{
	int nCount = 0;
	int nPasses = (int)passes.size();
	for (int nPass = 0; nPass < nPasses; nPass++)
	{
		ModelRenderPass &p = passes[nPass];
		nCount += p.indexCount / 3;
	}
	return nCount;
}

int CParaXModel::GetPhysicsCount()
{
	return 0;
}

const char* CParaXModel::DumpTextureUsage()
{
	static string g_output;
	g_output.clear();

	char temp[200];
	snprintf(temp, 200, "cnt:%d;", GetObjectNum().nTextures);
	g_output.append(temp);

	for (size_t i = 0; i < GetObjectNum().nTextures; i++)
	{
		if (textures[i])
		{
			const TextureEntity::TextureInfo * pInfo = textures[i]->GetTextureInfo();
			if (pInfo)
			{
				char temp[200];
				snprintf(temp, 200, "%d*%d(%d)", pInfo->m_width, pInfo->m_height, pInfo->m_format);
				g_output.append(temp);
			}
			g_output.append(textures[i]->GetKey());
			g_output.append(";");
		}
	}
	return g_output.c_str();
}

bool CParaXModel::HasAlphaBlendedObjects()
{
	if (m_nHasAlphaBlendedRenderPass >= 0)
		return m_nHasAlphaBlendedRenderPass > 0;
	else
	{
		for (ModelRenderPass &p : passes)
		{
			if (p.blendmode != BM_OPAQUE && p.blendmode != BM_TRANSPARENT)
			{
				m_nHasAlphaBlendedRenderPass = 1;
				return true;
			}
		}
		m_nHasAlphaBlendedRenderPass = 0;
		return false;
	}
}

int CParaXModel::GetChildAttributeObjectCount(int nColumnIndex /*= 0*/)
{
	if (nColumnIndex == 0) {
		return (int)GetObjectNum().nBones;
	}
	else if (nColumnIndex == 1) {
		return (int)GetObjectNum().nTextures;
	}
	return 0;
}

IAttributeFields* CParaXModel::GetChildAttributeObject(int nRowIndex, int nColumnIndex /*= 0*/)
{
	if (nColumnIndex == 0)
	{
		if (nRowIndex < (int)GetObjectNum().nBones)
			return &(bones[nRowIndex]);
	}
	else if (nColumnIndex == 1)
	{
		if (nRowIndex < (int)GetObjectNum().nTextures)
		{
			if (textures[nRowIndex])
			{
				return textures[nRowIndex].get();
			}
		}
	}
	return 0;
}

IAttributeFields* CParaXModel::GetChildAttributeObject(const std::string& sName)
{
	return 0;
}

int CParaXModel::GetChildAttributeColumnCount()
{
	return 2;
}

int CParaXModel::GetNextPhysicsGroupID(int nPhysicsGroup)
{
	int nNextID = -1;
	for (ModelRenderPass& pass : passes)
	{
		if (pass.hasPhysics() && pass.GetPhysicsGroup() > nPhysicsGroup)
		{
			if (nNextID > pass.GetPhysicsGroup() || nNextID == -1)
			{
				nNextID = pass.GetPhysicsGroup();
			}
		}
	}
	return nNextID;
}

HRESULT CParaXModel::RendererRecreated()
{
	m_pIndexBuffer.RendererRecreated();
	m_pVertexBuffer.RendererRecreated();

	this->SetVertexBufferDirty();

	return S_OK;
}

HRESULT CParaXModel::ClonePhysicsMesh(DWORD* pNumVertices, Vector3 ** ppVerts, DWORD* pNumTriangles, DWORD** ppIndices, int* pnMeshPhysicsGroup /*= NULL*/, int* pnTotalMeshGroupCount /*= NULL*/)
{
	if (m_objNum.nVertices == 0 || !m_indices)
		return E_FAIL;

	if (pnTotalMeshGroupCount)
	{
		int nTotalMeshGroupCount = 0;
		int nPhysicsGroup = -1;
		while ((nPhysicsGroup = GetNextPhysicsGroupID(nPhysicsGroup)) >= 0)
		{
			nTotalMeshGroupCount++;
		}
		*pnTotalMeshGroupCount = nTotalMeshGroupCount;
	}

	for (ModelRenderPass& pass : passes)
	{
		if (pass.force_physics)
		{
			for (ModelRenderPass& pass : passes)
			{
				if (!pass.force_physics)
				{
					pass.disable_physics = true;
				}
			}
			break;
		}
	}

	DWORD dwNumFaces = 0;
	int nVertexCount = 0;
	for (ModelRenderPass& pass : passes)
	{
		if (pass.hasPhysics() && (pnMeshPhysicsGroup == 0 || ((*pnMeshPhysicsGroup) == pass.GetPhysicsGroup())))
		{
			dwNumFaces += pass.indexCount / 3;
		}
	}

	if (dwNumFaces == 0)
	{
		// in case, there is no physics faces in the mesh, return immediately.
		if (pNumVertices != 0)
			*pNumVertices = 0;
		if (pNumTriangles != 0)
			*pNumTriangles = 0;
		return S_OK;
	}

	//////////////////////////////////////////////////////////////////////////
	// read the vertex buffer
	//////////////////////////////////////////////////////////////////////////
	DWORD dwNumVx = 0;
	Vector3 * verts = NULL;
	if (ppVerts != NULL)
	{
		dwNumVx = m_objNum.nVertices;
		verts = new Vector3[dwNumVx];
		auto pVertices = &(m_origVertices[0]);

		for (DWORD i = 0; i < dwNumVx; ++i)
		{
			verts[i] = pVertices->pos;
			pVertices++;
		}
		if (m_RenderMethod == SOFT_ANIM)
		{
			if (m_frame_number_vertices == 0)
				m_frame_number_vertices = new int[dwNumVx];
			memset(m_frame_number_vertices, 0, sizeof(int)*dwNumVx);
		}
	}


	//////////////////////////////////////////////////////////////////////////
	// read the index buffer
	//////////////////////////////////////////////////////////////////////////
	DWORD* indices = NULL;
	if (ppIndices)
	{
		indices = new DWORD[dwNumFaces * 3];
		int nD = 0; // destination indices index

		for (ModelRenderPass& pass : passes)
		{
			if (pass.hasPhysics() && (pnMeshPhysicsGroup == 0 || ((*pnMeshPhysicsGroup) == pass.GetPhysicsGroup())))
			{
				int nVertexOffset = pass.GetVertexStart(this);
				if (m_RenderMethod == SOFT_ANIM)
				{
					int nIndexOffset = pass.m_nIndexStart;
					for (int i = 0; i < pass.indexCount; ++i)
					{
						int a = m_indices[nIndexOffset + i] + nVertexOffset;
						if (m_frame_number_vertices[a] != 1)
						{
							m_frame_number_vertices[a] = 1;
							auto ov = m_origVertices + a;
							float weight = ov->weights[0] * (1 / 255.0f);
							Bone& bone = bones[ov->bones[0]];
							Vector3 v = (ov->pos * bone.mat)*weight;
							for (int b = 1; b < 4 && ov->weights[b]>0; b++)
							{
								weight = ov->weights[b] * (1 / 255.0f);
								Bone& bone = bones[ov->bones[b]];
								v += (ov->pos * bone.mat) * weight;
							}
							verts[a] = v;
						}
					}
				}

#ifdef INVERT_PHYSICS_FACE_WINDING
				int32* dest = (int32*)&(indices[nD]);
				int16* src;
				if (pass.indexStart == 0xffff)
					src = &(m_indices[pass.m_nIndexStart]);
				else
					src = &(m_indices[pass.indexStart]);
				int nFaceCount = pass.indexCount / 3;
				for (int i = 0; i < nFaceCount; ++i)
				{
					// change the triangle winding order
					*dest = *src + nVertexOffset; ++src;
					*(dest + 2) = *src + nVertexOffset; ++src;
					*(dest + 1) = *src + nVertexOffset; ++src;
					dest += 3;
				}
#else
				if (pass.indexStart == 0xffff)
				{
					for (int i = 0; i < pass.indexCount; ++i)
					{
						indices[nD + i] = m_indices[pass.m_nIndexStart + i] + nVertexOffset;
					}
				}
				else
				{
					for (int i = 0; i < pass.indexCount; ++i)
					{
						indices[nD + i] = m_indices[pass.indexStart + i] + nVertexOffset;
					}
				}

#endif
				nD += pass.indexCount;
			}
		}
	}
	// output result
	if (pNumVertices != 0) {
		*pNumVertices = dwNumVx;
	}
	if (ppVerts != 0) {
		*ppVerts = verts;
	}
	if (pNumTriangles != 0) {
		*pNumTriangles = dwNumFaces;
	}
	if (ppIndices != 0) {
		*ppIndices = indices;
	}
	return S_OK;
}

int CParaXModel::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	// install parent fields if there are any. Please replace __super with your parent class name.
	IAttributeFields::InstallFields(pClass, bOverride);

	PE_ASSERT(pClass != NULL);
	pClass->AddField("TextureUsage", FieldType_String, (void*)0, (void*)DumpTextureUsage_s, NULL, NULL, bOverride);
	pClass->AddField("PolyCount", FieldType_Int, (void*)0, (void*)GetPolyCount_s, NULL, NULL, bOverride);
	pClass->AddField("PhysicsCount", FieldType_Int, (void*)0, (void*)GetPhysicsCount_s, NULL, NULL, bOverride);

	pClass->AddField("GeosetsCount", FieldType_Int, (void*)0, (void*)GetGeosetsCount_s, NULL, NULL, bOverride);
	pClass->AddField("RenderPassesCount", FieldType_Int, (void*)0, (void*)GetRenderPassesCount_s, NULL, NULL, bOverride);

	pClass->AddField("ObjectNum", FieldType_void_pointer, (void*)0, (void*)GetObjectNum_s, NULL, NULL, bOverride);
	pClass->AddField("Vertices", FieldType_void_pointer, (void*)0, (void*)GetVertices_s, NULL, NULL, bOverride);
	pClass->AddField("RenderPasses", FieldType_void_pointer, (void*)0, (void*)GetRenderPasses_s, NULL, NULL, bOverride);
	pClass->AddField("Geosets", FieldType_void_pointer, (void*)0, (void*)GetGeosets_s, NULL, NULL, bOverride);
	pClass->AddField("Indices", FieldType_void_pointer, (void*)0, (void*)GetIndices_s, NULL, NULL, bOverride);
	pClass->AddField("Animations", FieldType_void_pointer, (void*)0, (void*)GetAnimations_s, NULL, NULL, bOverride);
	pClass->AddField("SaveToDisk", FieldType_String, (void*)SaveToDisk_s, NULL, NULL, NULL, bOverride);

	return S_OK;
}

void CParaXModel::SaveToDisk(const char* path)
{
	string filepath(path);
	XFileCharModelExporter::Export(filepath, this);
}

//-----------------------------------------------------------------------------
// Class:	CParaXAnimInstance
// Authors:	Li, Xizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2005.9.18
// Revised: 2005.10.8
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "ParaWorldAsset.h"
#include "ParaXModel/ParaXModel.h"
#include "ParaXModel/AnimTable.h"
#include "ParaXModel/BoneAnimProvider.h"
#include "EffectManager.h"
#include "SceneState.h"
#include "CustomCharSettings.h"
#include "CustomCharModelInstance.h"
#include "ParaXModelCanvas.h"
#include "ParaXAnimInstance.h"

/** @def default walking animation speed if model does not exist or does not contain a walk animation. */
#define DEFAULT_WALK_SPEED 4.0f

namespace ParaEngine
{
	// global time for global sequences
	extern int globalTime;
}

using namespace ParaEngine;


CParaXAnimInstance::CParaXAnimInstance(void)
	:m_modelType(CharacterModel), m_bUseGlobalTime(false), m_curTime(0), m_fBlendingFactor(0), m_nCurrentIdleAnimationID(ANIM_STAND), m_nCustomStandingAnimCount(-1), mUpperBlendingFactor(0)
{
	// Maybe init from a another function, instead of constructor
	if (m_modelType == CharacterModel)
	{
		m_pCharModel.reset(new CharModelInstance());
	}
}

CParaXAnimInstance::~CParaXAnimInstance(void)
{
}

int CParaXAnimInstance::GetTime()
{
	return m_curTime;
}

void CParaXAnimInstance::SetTime(int nTime)
{
	m_curTime = nTime;
}

void CParaXAnimInstance::SetBlendingFactor(float fBlendingFactor)
{
	m_fBlendingFactor = fBlendingFactor;
}


void CParaXAnimInstance::SetUseGlobalTime(bool bUseGlobalTime)
{
	m_bUseGlobalTime = bUseGlobalTime;
}

bool CParaXAnimInstance::IsUseGlobalTime()
{
	return m_bUseGlobalTime;
}

void CParaXAnimInstance::SetAnimFrame(int nFrame)
{
	if (m_CurrentAnim.IsValid() && !m_CurrentAnim.IsUndetermined())
	{
		int nLength = m_CurrentAnim.nEndFrame - m_CurrentAnim.nStartFrame;
		if (nLength > 0 && nFrame >= 0)
		{
			if (nFrame <= nLength)
			{
				m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nStartFrame + nFrame;
			}
			else
			{
				m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nStartFrame + nFrame % nLength;
			}
			m_fBlendingFactor = 0.f;
		}
	}

}

int CParaXAnimInstance::GetAnimFrame()
{
	return m_CurrentAnim.nCurrentFrame - m_CurrentAnim.nStartFrame;
}

int CParaXAnimInstance::GetIdleAnimationID()
{
	return m_nCurrentIdleAnimationID;

}

void CParaXAnimInstance::SetIdleAnimationID(int nID)
{
	m_nCurrentIdleAnimationID = nID;
}

bool CParaXAnimInstance::HasMountPoint(int nMountPointID /*= 0*/)
{
	return HasAttachmentMatrix(nMountPointID);
}

CharModelInstance * CParaXAnimInstance::GetCharModel()
{
	if (m_modelType == CharacterModel)
	{
		return m_pCharModel.get();
	}
	return NULL;
}

void CParaXAnimInstance::Init(ParaXEntity * pModel)
{
	ResetBaseModel(pModel);
}

int CParaXAnimInstance::GetValidAnimID(int nAnimID)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel)
		{
			int nAnimIndex = 0;
			do {
				nAnimIndex = pModel->GetAnimIndexByID(nAnimID).nIndex;
				if (nAnimIndex >= 0 || nAnimID == 0)
					break;
				nAnimID = CAnimTable::GetDefaultAnimIDof(nAnimID);
			} while (true);
			return nAnimID;
		}
	}
	return -1;
}

void ParaEngine::CParaXAnimInstance::SetUpperAnimation(int nAnimID)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
		{
			return;
		}

		if (IsAnimIDMapEnabled())
		{
			map<int, int>::iterator it = GetAnimIDMap()->find(nAnimID);
			if (it != GetAnimIDMap()->end())
			{
				nAnimID = (*it).second;
			}
		}

		if (nAnimID < 0)
		{
			mUpperAnim.MakeInvalid();
			mUpperBlendingAnim.MakeInvalid();
			mUpperBlendingFactor = 0;
		}
		else
		{
			AnimIndex IndexAnim(0);
			bool bHasWalkAnim = false;
			if (nAnimID < 1000)
			{
				// load local model animation
				do {
					if (nAnimID == ANIM_WALK)
						bHasWalkAnim = true;
					IndexAnim = pModel->GetAnimIndexByID(nAnimID);
					if (IndexAnim.IsValid() || nAnimID == 0)
						break;
					nAnimID = CAnimTable::GetDefaultAnimIDof(nAnimID);
				} while (true);
			}
			else
			{
				// load an external animation.
				CBoneAnimProvider* pProvider = CBoneAnimProvider::GetProviderByID(nAnimID);
				if (pProvider)
				{
					IndexAnim = pProvider->GetAnimIndex(pProvider->GetSubAnimID());
				}
			}
			if (IndexAnim.IsValid() && IndexAnim.Provider == 0)
			{
				// scale speed properly
				auto pModelAnim = pModel->GetModelAnimByIndex(IndexAnim.nIndex);
				if (pModelAnim)
				{
					float moveSpeed = pModelAnim->moveSpeed;
					if (bHasWalkAnim && moveSpeed == 0.f)
					{
						// default to 4 meters/seconds in case walk animation is not inside the file. 
						moveSpeed = DEFAULT_WALK_SPEED;
					}
				}
			}
			IndexAnim.nAnimID = nAnimID; // enforce the same ID

			if (mUpperAnim != IndexAnim)
			{
				/// If the current animation is looping and bAppend is false, play immediately from the beginning of the new animation.
				// turn on motion warping

				mUpperBlendingAnim = mUpperAnim;
				if (!mUpperBlendingAnim.IsValid())
					mUpperBlendingAnim = m_CurrentAnim;
				mUpperBlendingFactor = 1.0;

				mUpperAnim = IndexAnim;
				mUpperAnim.Reset();
			}
			else
			{
				mUpperAnim.Reset();
				mUpperBlendingFactor = 0;
			}
		}
	}
	else
	{
		// TODO: other model type goes here
	}
}

int ParaEngine::CParaXAnimInstance::GetUpperAnimation()
{
	return mUpperAnim.IsValid()?mUpperAnim.nAnimID:-1;
}

bool CParaXAnimInstance::HasAnimId(int nAnimID)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel)
		{
			return pModel->GetAnimIndexByID(nAnimID).IsValid();
		}
	}
	return false;
}

void CParaXAnimInstance::ResetAnimation()
{
	m_CurrentAnim.MakeInvalid();
	m_NextAnim.MakeInvalid();
	m_BlendingAnim.MakeInvalid();
	m_fBlendingFactor = 0;
	m_nCurrentIdleAnimationID = ANIM_STAND;
	m_nCustomStandingAnimCount = -1;
	m_AttachmentMatrices.clear();
	// external animation are stored in dynamic fields using bone names as key. 
	RemoveAllDynamicFields();
	m_curTime = 0;

	mUpperAnim.MakeInvalid();
}

bool CParaXAnimInstance::ResetBaseModel(ParaXEntity * pModel)
{
	if (m_modelType == CharacterModel)
	{
		// animation info are preserved, so never call ResetAnimation() here. 
		// ResetAnimation();
		m_pCharModel->InitBaseModel(pModel);
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel)
			m_CurrentAnim = pModel->GetAnimIndexByID(GetIdleAnimationID());
		else
			m_CurrentAnim.MakeInvalid();
		m_NextAnim.MakeInvalid();
		m_BlendingAnim.MakeInvalid();
		m_fBlendingFactor = 0;
		m_nCurrentIdleAnimationID = ANIM_STAND;
		m_nCustomStandingAnimCount = -1;

		mUpperAnim.MakeInvalid();
		return true;
	}
	return false;
}

void CParaXAnimInstance::LoadAnimationByIndex(const AnimIndex& IndexAnim, bool bAppend)
{
	if (!IndexAnim.IsValid())
		return;
	if (m_modelType == CharacterModel)
	{
		if (m_CurrentAnim != IndexAnim)
		{
			/// if the animation is different, we will play a new one.

			if ((!bAppend) || m_CurrentAnim.IsLooping())
			{
				/// If the current animation is looping and bAppend is false, play immediately from the beginning of the new animation.
				// turn on motion warping

				m_BlendingAnim = m_CurrentAnim;
				m_fBlendingFactor = 1.0;

				m_CurrentAnim = IndexAnim;
				m_CurrentAnim.Reset();

				/// set the next animation to default
				m_NextAnim.MakeInvalid();
			}
			else
			{
				/// if the current animation is non-looping, we will set the next animation to play to the new animation.
				m_NextAnim = IndexAnim;
				m_NextAnim.Reset();
			}
		}
		else
		{
			m_NextAnim = IndexAnim;
		}
	}
	else
	{
		// TODO: other model type goes here
	}
}

/** get the ID of the current animation.*/
int CParaXAnimInstance::GetCurrentAnimation()
{
	int nID = 0;
	if (m_modelType == CharacterModel)
	{
		nID = m_CurrentAnim.nAnimID;
		if (nID < 0)
			nID = 0;
	}
	else
	{
		// TODO: other model type goes here
	}
	return nID;
}

bool CParaXAnimInstance::HasAlphaBlendedObjects()
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel)
		{
			return pModel->HasAlphaBlendedObjects();
		}
	}
	return false;
}

bool CParaXAnimInstance::HasAnimation(int nAnimID)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
			return false;

		if (IsAnimIDMapEnabled())
		{
			map<int, int>::iterator it = GetAnimIDMap()->find(nAnimID);
			if (it != GetAnimIDMap()->end())
			{
				nAnimID = (*it).second;
			}
		}

		if (nAnimID < 0)
			return false;

		AnimIndex IndexAnim(0);

		if (nAnimID < 1000)
		{
			// load local model animation
			IndexAnim = pModel->GetAnimIndexByID(nAnimID);
			if (IndexAnim.IsValid() || nAnimID == 0)
				return true;
		}
		else
		{
			// load an external animation.
			CBoneAnimProvider* pProvider = CBoneAnimProvider::GetProviderByID(nAnimID);
			if (pProvider)
			{
				IndexAnim = pProvider->GetAnimIndex(pProvider->GetSubAnimID());
				if (IndexAnim.IsValid())
				{
					return true;
				}
			}
		}
	}
	else
	{
		// TODO: other model type goes here
	}
	return false;
}

///////////////////////////////////////////////////////////////////////////
// major implementation of loading a given animation ID.
void CParaXAnimInstance::LoadAnimation(int nNextAnimID, float * fSpeed, bool bAppend)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
		{
			if (fSpeed)
			{
				if (CAnimTable::IsWalkAnimation(nNextAnimID))
					*fSpeed = m_fSpeedScale* m_fSizeScale * DEFAULT_WALK_SPEED;
				else
					*fSpeed = 0.f;
			}
			return;
		}

		if (IsAnimIDMapEnabled())
		{
			map<int, int>::iterator it = GetAnimIDMap()->find(nNextAnimID);
			if (it != GetAnimIDMap()->end())
			{
				nNextAnimID = (*it).second;
			}
		}

		if (nNextAnimID < 0)
			return;

		AnimIndex IndexAnim(0);
		bool bHasWalkAnim = false;
		if (nNextAnimID < 1000)
		{
			// load local model animation
			do {
				if (nNextAnimID == ANIM_WALK)
					bHasWalkAnim = true;
				IndexAnim = pModel->GetAnimIndexByID(nNextAnimID);
				if (IndexAnim.IsValid() || nNextAnimID == 0)
					break;
				nNextAnimID = CAnimTable::GetDefaultAnimIDof(nNextAnimID);
			} while (true);
		}
		else
		{
			// load an external animation.
			CBoneAnimProvider* pProvider = CBoneAnimProvider::GetProviderByID(nNextAnimID);
			if (pProvider)
			{
				IndexAnim = pProvider->GetAnimIndex(pProvider->GetSubAnimID());
				if (IndexAnim.IsValid())
				{
					pProvider->GetAnimMoveSpeed(fSpeed, pProvider->GetSubAnimID());
					*fSpeed *= m_fSpeedScale* m_fSizeScale;
				}
			}
		}
		if (IndexAnim.IsValid() && IndexAnim.Provider == 0)
		{
			// scale speed properly
			auto pModelAnim = pModel->GetModelAnimByIndex(IndexAnim.nIndex);
			if (pModelAnim)
			{
				float moveSpeed = pModelAnim->moveSpeed;
				if (bHasWalkAnim && moveSpeed == 0.f)
				{
					// default to 4 meters/seconds in case walk animation is not inside the file. 
					moveSpeed = DEFAULT_WALK_SPEED;
				}
				if (fSpeed)
					*fSpeed = m_fSpeedScale* m_fSizeScale * moveSpeed;
			}
			else
			{
				if (fSpeed)
					*fSpeed = (bHasWalkAnim) ? m_fSpeedScale* m_fSizeScale * DEFAULT_WALK_SPEED : 0.f;
			}
		}
		else
		{
			if (fSpeed)
				*fSpeed = (bHasWalkAnim) ? m_fSpeedScale* m_fSizeScale * DEFAULT_WALK_SPEED : 0.f;
		}
		IndexAnim.nAnimID = nNextAnimID; // enforce the same ID
		LoadAnimationByIndex(IndexAnim, bAppend);
	}
	else
	{
		// TODO: other model type goes here
	}
}

void CParaXAnimInstance::LoadAnimation(const char * sName, float * fSpeed, bool bAppend)
{
	LoadAnimation(CAnimTable::GetAnimIDByName(sName), fSpeed, bAppend);
}

void CParaXAnimInstance::LoadDefaultStandAnim(float * fSpeed)
{
	LoadAnimation(ANIM_STAND, fSpeed);
}
void CParaXAnimInstance::LoadDefaultWalkAnim(float * fSpeed)
{
	LoadAnimation(ANIM_RUN, fSpeed);
}

Matrix4*  CParaXAnimInstance::GetAttachmentMatrix(Matrix4* pOut, int nAttachmentID, int nRenderNumber)
{
	ParaXEntity* pModelEnity = GetAnimModel();
	CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
	if (pModel == NULL)
		return NULL;

	ATTACHMENT_MATRIX_POOL_TYPE::iterator iter = m_AttachmentMatrices.find(nAttachmentID);

	if (iter != m_AttachmentMatrices.end())
	{
		// return the pre-calculated matrix. 
		if (nRenderNumber == 0 || iter->second.m_nRenderNumber == nRenderNumber)
		{
			(*pOut) = iter->second.m_mat;
			return pOut;
		}
	}
	if (pModel->GetAttachmentMatrix(pOut, nAttachmentID, m_CurrentAnim, m_BlendingAnim, m_fBlendingFactor, mUpperAnim, mUpperBlendingAnim, mUpperBlendingFactor))
	{
		Matrix4 matScale;
		if (fabs(m_fSizeScale - 1.0f) > FLT_TOLERANCE)
		{
			ParaMatrixScaling(&matScale, m_fSizeScale, m_fSizeScale, m_fSizeScale);
			(*pOut) = (*pOut)*matScale;
		}
		// save the attachment matrix. 
		AttachmentMat mat;
		mat.m_mat = *pOut;
		mat.m_nRenderNumber = nRenderNumber;
		m_AttachmentMatrices[nAttachmentID] = mat;
	}
	else
		return NULL;
	return pOut;
}

bool CParaXAnimInstance::HasAttachmentMatrix(int nAttachmentID)
{
	ParaXEntity* pModelEnity = GetAnimModel();
	CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
	if (pModel == NULL)
		return false;
	return (pModel->HasAttachmentMatrix(nAttachmentID));
}

void CParaXAnimInstance::AdvanceTime(double dTimeDelta)
{
	//if(dTimeDelta<0.000001)
	//	return;
	/// Speed up the animation rendering by a factor of m_fSpeedScale
	dTimeDelta *= m_fSpeedScale;

	if (m_modelType == CharacterModel)
	{
		CharModelInstance* pChar = GetCharModel();
		if (pChar)
			pChar->AdvanceTime(float(dTimeDelta));
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
			return;
		if (m_CurrentAnim.IsValid())
		{
			if (m_CurrentAnim.nCurrentFrame<(int)m_CurrentAnim.nStartFrame)
				m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nStartFrame;
			if (m_CurrentAnim.nCurrentFrame>(int)m_CurrentAnim.nEndFrame)
				m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nEndFrame;
			int nToDoFrame = m_CurrentAnim.nCurrentFrame + (int)(dTimeDelta * 1000);
			if (m_bUseGlobalTime)
			{
				nToDoFrame = m_CurrentAnim.nStartFrame + ParaEngine::globalTime % (m_CurrentAnim.nEndFrame - m_CurrentAnim.nStartFrame);
				if (m_CurrentAnim.nCurrentFrame > nToDoFrame)
				{
					// looping
					if (m_CurrentAnim.IsUndetermined())
					{
						// if current animation is undetermined, possibly because it is still being loaded, we shall try loading it again. 
						float fSpeed;
						LoadAnimation(m_CurrentAnim.nAnimID, &fSpeed);
					}
				}
			}
			//int nSegLength = m_CurrentAnim.nEndFrame - m_CurrentAnim.nStartFrame;

			// blending factor is decreased
			if (m_fBlendingFactor > 0)
			{
#ifdef _DEBUG
				if (dTimeDelta > 0.033)
				{
					dTimeDelta = 0.033;
				}
#endif
				m_fBlendingFactor -= (float)(dTimeDelta / pModel->fBlendingTime); // BLENDING_TIME blending time
				if (m_fBlendingFactor < 0)
					m_fBlendingFactor = 0;
			}
			// check if we have reached the end frame of the current animation
			if (nToDoFrame > (int)m_CurrentAnim.nEndFrame)
			{
				nToDoFrame = (nToDoFrame - m_CurrentAnim.nStartFrame) % (m_CurrentAnim.nEndFrame - m_CurrentAnim.nStartFrame + 1) + m_CurrentAnim.nStartFrame; // wrap to the beginning

				if (m_NextAnim.IsValid())
				{///  if there is a queued animation, we will play that one.
					if (m_NextAnim == m_CurrentAnim)
					{// if the next animation is the same as the current one,force looping on the current animation
						m_CurrentAnim.nCurrentFrame = nToDoFrame;
					}
					else
					{// play the next animation with motion blending with the current one.
						if (!m_CurrentAnim.IsLooping())
						{
							m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nEndFrame; // this is not necessary ?
						}
						LoadAnimationByIndex(m_NextAnim);
						// m_CurrentAnim.nCurrentFrame = m_CurrentAnim.nStartFrame;// this is not necessary ?
					}
					/// empty the queue
					m_NextAnim.MakeInvalid();
				}
				else
				{///  if there is NO queued animation, we will play the default one.
					if (!m_CurrentAnim.IsLooping())
					{/// non-looping, play the default idle animation
						if (!m_CurrentAnim.IsUndetermined())
						{
							AnimIndex IdleAnimIndex = pModel->GetAnimIndexByID(GetIdleAnimationID());
							if (m_CurrentAnim == IdleAnimIndex)
							{
								m_CurrentAnim.nCurrentFrame = nToDoFrame;
								m_CurrentAnim.AddCycle();
							}
							else
							{
								LoadAnimationByIndex(IdleAnimIndex);
							}
						}
						else
						{
							// if current animation is undetermined, possibly because it is still being loaded, we shall try loading it again. 
							float fSpeed;
							LoadAnimation(m_CurrentAnim.nAnimID, &fSpeed);
						}
					}
					else
					{/// looping on the current animation
						m_CurrentAnim.nCurrentFrame = nToDoFrame;
						m_CurrentAnim.AddCycle();
						if (m_nCustomStandingAnimCount != 0)
						{
							// the character may have alternative standing animations. A character must have the standing animation ANIM_STAND(0), 
							// it may also have up to 4 custom standing animations, in the id range ANIM_CUSTOM0-ANIM_CUSTOM3
							// we will play the custom animations, if any, randomly after the default standing animation is played after some set time(such as 10 seconds).
							if ((m_CurrentAnim.nAnimID == ANIM_STAND && m_CurrentAnim.nFramePlayed > 7000) || (m_CurrentAnim.nAnimID >= ANIM_CUSTOM0 && m_CurrentAnim.nAnimID <= ANIM_CUSTOM3))
							{
								// if it has played over 10 seconds. we will choose one of the custom animations if any.
								if (m_nCustomStandingAnimCount == -1)
								{
									m_nCustomStandingAnimCount = 0;
									for (int k = 0; k < 3; k++)
									{
										AnimIndex IdleAnimIndex = pModel->GetAnimIndexByID(ANIM_CUSTOM0 + k);
										if (IdleAnimIndex.IsValid())
											++m_nCustomStandingAnimCount;
										else
											break;
									}
								}
								if (m_nCustomStandingAnimCount > 0)
								{
									// select a random number [0,m_nCustomStandingAnimCount]
									int nCustomIndex = 0;
									if (pChar == 0 || fabs(pChar->GetCurrrentUpperBodyTurningAngle()) < 0.01)
									{
										nCustomIndex = (rand()) % (m_nCustomStandingAnimCount + 1);
										if (nCustomIndex == m_nCustomStandingAnimCount)
											nCustomIndex = ANIM_STAND;
										else
										{
											nCustomIndex = ANIM_CUSTOM0 + nCustomIndex;
											if (m_CurrentAnim.nAnimID == nCustomIndex)
												nCustomIndex = ANIM_STAND;
										}
									}
									else
									{
										nCustomIndex = ANIM_STAND;
									}

									if (m_CurrentAnim.nAnimID != nCustomIndex)
									{
										AnimIndex IdleAnimIndex = pModel->GetAnimIndexByID(nCustomIndex);
										if (IdleAnimIndex.IsValid())
										{
											LoadAnimationByIndex(IdleAnimIndex);
										}
									}
								}
							}
						}
					}
				}
			}
			else
			{
				m_CurrentAnim.nCurrentFrame = nToDoFrame;
			}
		}

		if (mUpperAnim.IsValid())
		{
			if (mUpperAnim.nCurrentFrame<(int)mUpperAnim.nStartFrame)
				mUpperAnim.nCurrentFrame = mUpperAnim.nStartFrame;
			if (mUpperAnim.nCurrentFrame>(int)mUpperAnim.nEndFrame)
				mUpperAnim.nCurrentFrame = mUpperAnim.nEndFrame;
			int nToDoFrame = mUpperAnim.nCurrentFrame + (int)(dTimeDelta * 1000);
			if (m_bUseGlobalTime)
			{
				nToDoFrame = mUpperAnim.nStartFrame + ParaEngine::globalTime % (mUpperAnim.nEndFrame - mUpperAnim.nStartFrame);
				if (mUpperAnim.nCurrentFrame > nToDoFrame)
				{
					// looping
					if (mUpperAnim.IsUndetermined())
					{
						// if current animation is undetermined, possibly because it is still being loaded, we shall try loading it again. 
						assert(false);
					}
				}
			}
			if (mUpperBlendingFactor > 0)
			{
#ifdef _DEBUG
				if (dTimeDelta > 0.033)
				{
					dTimeDelta = 0.033;
				}
#endif
				mUpperBlendingFactor -= (float)(dTimeDelta / pModel->fBlendingTime); // BLENDING_TIME blending time
				if (mUpperBlendingFactor < 0)
					mUpperBlendingFactor = 0;
			}
			// check if we have reached the end frame of the current animation
			if (nToDoFrame > (int)mUpperAnim.nEndFrame)
			{
				nToDoFrame -= (mUpperAnim.nEndFrame - mUpperAnim.nStartFrame); // wrap to the beginning

				///  if there is NO queued animation, we will play the default one.
				if (!mUpperAnim.IsLooping())
				{/// non-looping, play the default idle animation
					mUpperAnim.MakeInvalid();
				}
				else
				{/// looping on the current animation
					mUpperAnim.nCurrentFrame = nToDoFrame;
					mUpperAnim.AddCycle();
				}
			}
			else
			{
				mUpperAnim.nCurrentFrame = nToDoFrame;
			}
		}
	}
	else
	{
		// TODO: other model type goes here
	}
}

void CParaXAnimInstance::BuildShadowVolume(SceneState * sceneState, ShadowVolume * pShadowVolume, LightParams* pLight, Matrix4* mxWorld)
{
#ifdef USE_DIRECTX_RENDERER
	LPDIRECT3DDEVICE9  pd3dDevice = CGlobals::GetRenderDevice();

	// scale the model
	Matrix4 mat, matScale;
	ParaMatrixScaling(&matScale, m_fSizeScale, m_fSizeScale, m_fSizeScale);
	mat = matScale * (*mxWorld);
	CGlobals::GetWorldMatrixStack().push(mat);

	// draw model
	m_pCharModel->AnimateModel(sceneState, m_CurrentAnim, m_NextAnim, m_BlendingAnim, m_fBlendingFactor, mUpperAnim, mUpperBlendingAnim, mUpperBlendingFactor, NULL);
	m_pCharModel->BuildShadowVolume(sceneState, pShadowVolume, pLight, &mat); 

	// pop matrix
	CGlobals::GetWorldMatrixStack().pop();
#endif
}

void CParaXAnimInstance::Animate(double dTimeDelta, int nRenderNumber/*=0 */)
{
	if (GetRenderCount() < nRenderNumber || nRenderNumber == 0)
	{
		if (nRenderNumber != 0)
			SetRenderCount(nRenderNumber);
		if (IsAnimationEnabled())
			AdvanceTime(dTimeDelta);
	}
}

bool CParaXAnimInstance::UpdateModel(SceneState * sceneState)
{
	if (m_modelType == CharacterModel)
	{
		// draw model
		if (m_pCharModel->AnimateModel(sceneState, m_CurrentAnim, m_NextAnim, m_BlendingAnim, m_fBlendingFactor, mUpperAnim, mUpperBlendingAnim, mUpperBlendingFactor, this))
		{
			// update the attachment matrix
			if (!m_AttachmentMatrices.empty() && sceneState)
			{
				int nRenderNumber = sceneState->GetRenderFrameCount();

				ParaXEntity * pModelAsset = m_pCharModel->GetBaseModel();
				if (pModelAsset)
				{
					int nIndex = sceneState->IsLODEnabled() ? pModelAsset->GetLodIndex(sceneState->GetCameraToCurObjectDistance()) : 0;
					CParaXModel* pModel = pModelAsset->GetModel(nIndex);

					if (pModel)
					{
						// update attachment matrix. 
						ATTACHMENT_MATRIX_POOL_TYPE::iterator itCur, itEnd = m_AttachmentMatrices.end();
						for (itCur = m_AttachmentMatrices.begin(); itCur != itEnd; ++itCur)
						{
							Matrix4 maxOut;
							if (itCur->second.m_nRenderNumber != nRenderNumber &&
								pModel->GetAttachmentMatrix(&maxOut, itCur->first, m_CurrentAnim, m_BlendingAnim, m_fBlendingFactor, mUpperAnim, mUpperBlendingAnim, mUpperBlendingFactor, false))
							{
								Matrix4 matScale;
								if (fabs(m_fSizeScale - 1.0f) > FLT_TOLERANCE)
								{
									ParaMatrixScaling(&matScale, m_fSizeScale, m_fSizeScale, m_fSizeScale);
									maxOut = maxOut * matScale;
								}
								// save the attachment matrix. 
								itCur->second.m_mat = maxOut;
								itCur->second.m_nRenderNumber = nRenderNumber;
							}
						}
					}
				}
			}
			return true;
		}
	}
	return false;
}


bool CParaXAnimInstance::UpdateWorldTransform(SceneState * sceneState, Matrix4& out, const Matrix4& mxWorld)
{
	if (m_modelType == CharacterModel)
	{
		if (UpdateModel(sceneState))
		{
			// scale the model
			if (fabs(m_fSizeScale - 1.0f) > FLT_TOLERANCE)
			{
				Matrix4 matScale;
				ParaMatrixScaling(&matScale, m_fSizeScale, m_fSizeScale, m_fSizeScale);
				out = matScale * mxWorld;
			}
			else
				out = mxWorld;
			return true;
		}
	}
	return false;
}

HRESULT CParaXAnimInstance::Draw(SceneState * sceneState, const Matrix4* mxWorld, CParameterBlock* materialParams)
{
	if (m_modelType == CharacterModel)
	{
		Matrix4 mat;
		if(UpdateWorldTransform(sceneState, mat, *mxWorld))
		{
			CGlobals::GetWorldMatrixStack().push(mat);
			m_pCharModel->Draw(sceneState, materialParams);
			CGlobals::GetWorldMatrixStack().pop();
		}
	}
	else
	{
		// TODO: other model type goes here
	}
	return S_OK;
}

/// normally this will read the radius of the current animation
/// and calculate the correct size after scaling
void CParaXAnimInstance::GetCurrentRadius(float* fRadius)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
			return;
		int nIndex = (m_CurrentAnim.Provider == 0 && (int)(pModel->GetObjectNum().nAnimations) > m_CurrentAnim.nIndex) ? m_CurrentAnim.nIndex : 0;
		auto pModelAnim = pModel->GetModelAnimByIndex(nIndex);
		if (pModelAnim){
			float boundsRadius = pModelAnim->rad;
			*fRadius = m_fSizeScale* boundsRadius;
		}
	}
	else
	{
		// TODO: other type goes here
	}
}
/// normally this will read the radius of the current animation
/// and calculate the correct size after scaling
void CParaXAnimInstance::GetCurrentSize(float * fWidth, float * fDepth)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
			return;
		int nIndex = (m_CurrentAnim.Provider == 0 && (int)(pModel->GetObjectNum().nAnimations) > m_CurrentAnim.nIndex) ? m_CurrentAnim.nIndex : 0;
		auto pModelAnim = pModel->GetModelAnimByIndex(nIndex);
		if (pModelAnim){
			Vector3 box = pModelAnim->boxA - pModelAnim->boxB;
			*fWidth = fabs(m_fSizeScale* box.x);
			*fDepth = fabs(m_fSizeScale* box.y);
		}
	}
	else
	{
		// TODO: other type goes here
	}
}

/// normally this will read the move speed of the current animation
/// and calculate the correct(scaled) speed
void CParaXAnimInstance::GetCurrentSpeed(float* fSpeed)
{
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
			return;
		int nIndex = (m_CurrentAnim.Provider == 0 && (int)(pModel->GetObjectNum().nAnimations) > m_CurrentAnim.nIndex) ? m_CurrentAnim.nIndex : 0;
		auto pModelAnim = pModel->GetModelAnimByIndex(nIndex);
		if (pModelAnim)
		{
			float moveSpeed = pModelAnim->moveSpeed;
			if (fSpeed)
				*fSpeed = m_fSpeedScale* m_fSizeScale* moveSpeed;
		}
	}
	else
	{
		// TODO: other type goes here
	}
}

/// normally this will read the move speed of the specified animation
/// and calculate the correct(scaled) speed
void CParaXAnimInstance::GetSpeedOf(const char * sName, float * fSpeed)
{
	// TODO: find a way to get it by name from database.
	int nAnimID = CAnimTable::GetAnimIDByName(sName);
	if (m_modelType == CharacterModel)
	{
		ParaXEntity* pModelEnity = GetAnimModel();
		CParaXModel* pModel = (pModelEnity != NULL) ? pModelEnity->GetModel() : NULL;
		if (pModel == NULL)
		{
			if (fSpeed)
			{
				if (CAnimTable::IsWalkAnimation(nAnimID))
					*fSpeed = m_fSpeedScale* m_fSizeScale * DEFAULT_WALK_SPEED;
				else
					*fSpeed = 0.f;
			}
			return;
		}
			

		int nAnimIndex = -1;
		bool bHasWalkAnim = false;
		do {
			if (nAnimID == ANIM_WALK)
				bHasWalkAnim = true;
			nAnimIndex = pModel->GetAnimIndexByID(nAnimID).nIndex;
			if (nAnimIndex >= 0 || nAnimID == 0)
				break;
			nAnimID = CAnimTable::GetDefaultAnimIDof(nAnimID);
		} while (true);

		if (nAnimIndex >= 0)
		{
			auto pModelAnim = pModel->GetModelAnimByIndex(nAnimIndex);
			if (pModelAnim)
			{
				float moveSpeed = pModelAnim->moveSpeed;
				if (bHasWalkAnim && moveSpeed == 0.f)
				{
					// default to 4 meters/seconds in case walk animation is not inside the file. 
					moveSpeed = DEFAULT_WALK_SPEED;
				}
				if (fSpeed)
					*fSpeed = m_fSpeedScale* m_fSizeScale* moveSpeed;
			}
		}
		else
		{
			if (fSpeed)
				*fSpeed = (bHasWalkAnim) ? m_fSpeedScale* m_fSizeScale * DEFAULT_WALK_SPEED : 0.f;
		}
	}
	else
	{
		// TODO: other type goes here
	}

}

ParaXEntity* CParaXAnimInstance::GetAnimModel()
{
	CharModelInstance * pCharInst = GetCharModel();
	return (pCharInst != NULL) ? pCharInst->GetAnimModel() : NULL;
}


IAttributeFields* CParaXAnimInstance::GetChildAttributeObject(const std::string& sName)
{
	return GetCharModel();
}

IAttributeFields* CParaXAnimInstance::GetChildAttributeObject(int nRowIndex, int nColumnIndex /*= 0*/)
{
	if (nRowIndex == 0 && nColumnIndex == 0)
		return GetCharModel();
	else if (nColumnIndex == 1)
	{
		// bones 
		ParaXEntity* pModel = GetAnimModel();
		if (pModel)
		{
			CParaXModel* pXModel = pModel->GetModel();
			if (pXModel && nRowIndex < (int)pXModel->GetObjectNum().nBones)
			{
				return &(pXModel->bones[nRowIndex]);
			}
		}
	}
	return NULL;
}

int CParaXAnimInstance::GetChildAttributeObjectCount(int nColumnIndex /*= 0*/)
{
	if (nColumnIndex == 0)
	{
		// animation instance
		return 1;
	}
	else if (nColumnIndex == 1)
	{
		// bones
		ParaXEntity* pModel = GetAnimModel();
		if (pModel && pModel->GetModel())
		{
			return pModel->GetModel()->GetObjectNum().nBones;
		}
	}
	return 0;
}

int CParaXAnimInstance::GetChildAttributeColumnCount()
{
	return 2;
}

int CParaXAnimInstance::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	CAnimInstanceBase::InstallFields(pClass, bOverride);

	pClass->AddField("IdleAnimationID", FieldType_Int, (void*)SetIdleAnimationID_s, (void*)GetIdleAnimationID_s, NULL, "", bOverride);
	pClass->AddField("UpdateModel", FieldType_void, (void*)UpdateModel_s, (void*)0, NULL, "", bOverride);
	
	return S_OK;
}

//-----------------------------------------------------------------------------
// Class:	ParaXBone
// Authors:	Li, Xizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2005.10.8
// Revised: 2005.10.8, 2014.8
// Note: some logics is based on the open source code of WOWMAPVIEW
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "FileManager.h"
#include "BoneAnimProvider.h"
#include "DynamicAttributeField.h"
#include "CustomCharCommon.h"
#include "ParaXModel.h"
#include "StringHelper.h"
#include "ParaXBone.h"

using namespace ParaEngine;

Bone::Bone()
	:bUsePivot(true), nBoneID(0), nIndex(0), parent(-1), flags(0), calc(false), pivot(0.f, 0.f, 0.f), matTransform(Matrix4::IDENTITY), matOffset(Matrix4::IDENTITY), m_finalTrans(0, 0, 0), m_finalScaling(1.f, 1.f, 1.f), mIsUpper(false)
{
}

void Bone::RemoveRedundentKeys()
{
	if (IsPivotBone())
		bUsePivot = (pivot != Vector3(0, 0, 0));

#ifdef ONLY_REMOVE_EQUAL_KEYS
	scale.SetConstantKey(Vector3(1.f, 1.f, 1.f));
	trans.SetConstantKey(Vector3(0, 0, 0));
#else
	scale.SetConstantKey(Vector3(1.f, 1.f, 1.f), 0.0001f);
	trans.SetConstantKey(Vector3(0, 0, 0), 0.00001f);
#endif

}
void Bone::calcMatrix(Bone *allbones)
{
	if (calc)
		return;

	if (parent >= 0) {
		allbones[parent].calcMatrix(allbones);
		mat = allbones[parent].mat;
	}
	else
		mat.identity();

	// compute transformation matrix (mrot) for normal vectors 
	if (parent >= 0)
		mrot = allbones[parent].mrot;
	else
		mrot.identity();
}

/**
for shared animations to take effect,bones must be named properly in 3dsmax (the default biped naming of character studio in 3dsmax 7,8,9 is compatible with us).
Here is the list of known bone names (case insensitive, maybe prefixed with any characters like biped01,but not suffixed):
Root(any name which is parent of pelvis), Pelvis,Spine,	L Thigh,L Calf,	L Foot,	R Thigh,R Calf,	R Foot,	L Clavicle,	L UpperArm,	L Forearm,	L Hand,	R Clavicle,	R UpperArm,	R Forearm,R Hand,Head,Neck,	L Toe0,	R Toe0,		R Finger0,	L Finger0,	Spine1,	Spine2,	Spine3,
The parent of the pelvis bone is always regarded as the root bone (Root).  All predefined bones must have pivot points,otherwise external animation will not be applied.
only the Bone_Root and facial bone's translation animation (which is also scaled automatically according to the local model) will be applied to the local model, for all other predefined bones, only rotation is applied.
This conforms to the BVH file format, where only the root node has translation and rotation animation, where all other nodes contains only rotation animation.
This allows the same animation data to be applied to different models with different bone lengths, but the same topology.
*/
bool Bone::calcMatrix(Bone *allbones, const AnimIndex & CurrentAnim, const AnimIndex & BlendingAnim, float blendingFactor, IAttributeFields* pAnimInstance)
{
	if (calc)
		return true;
	calc = true;
	if (!CurrentAnim.IsValid())
	{
		if (rot.used || scale.used || trans.used)
			return false;
	}
	if (IsStaticTransform() && IsTransformationNode())
	{
		if (parent >= 0) {
			allbones[parent].calcMatrix(allbones, CurrentAnim, BlendingAnim, blendingFactor, pAnimInstance);
			mat = matTransform * allbones[parent].mat;
		}
		else
			mat = matTransform;
		return true;
	}

	if (!BlendingAnim.IsValid())
		blendingFactor = 0.f;

	auto current_blending_factor = blendingFactor;
	auto & current_anim = CurrentAnim;
	auto & current_blending_anim = BlendingAnim;

	CBoneAnimProvider* pCurProvider = NULL;
	// the bone in the external bone provider that corresponding to the current bone. 
	Bone* pCurBone = NULL;
	if (current_anim.Provider != 0)
	{
		pCurProvider = CBoneAnimProvider::GetProviderByID(current_anim.nIndex);
		if (pCurProvider)
		{
			if (nBoneID > 0)
			{
				// if the bone is one of the known biped bones, we will find in the external provider.
				// if no such a bone in the provider, we will use the default value (0). 
				pCurBone = pCurProvider->GetBone((KNOWN_BONE_NODES)nBoneID);
			}
			else
			{
				// if the bone is one of the unknown biped bones, both locally and externally. we will try to use external animation by matching bone index. 
				// if no unknown bone in the external provider with the same index and parent index, we will use the default animation (0). 
				Bone* bone_ = pCurProvider->GetBoneByIndex(this->nIndex);
				if (bone_ != 0 && bone_->nBoneID <= 0 && parent == bone_->parent)
				{
					pCurBone = bone_;
				}
			}
		}
	}
	CBoneAnimProvider* pBlendingProvider = NULL;
	// the bone in the external bone provider that corresponding to the current bone. 
	Bone* pBlendBone = NULL;
	if (current_blending_anim.Provider != 0 && current_blending_anim.IsValid())
	{
		pBlendingProvider = CBoneAnimProvider::GetProviderByID(current_blending_anim.nIndex);
		if (pBlendingProvider)
		{
			if (nBoneID > 0)
			{
				// if the bone is one of the known biped bones, we will find in the external provider.
				// if no such a bone in the provider, we will use the default value (0). 
				pBlendBone = pBlendingProvider->GetBone((KNOWN_BONE_NODES)nBoneID);
			}
			else
			{
				// if the bone is one of the unknown biped bones, both locally and externally. we will try to use external animation by matching bone index. 
				// if no unknown bone in the external provider with the same index and parent index, we will use the default animation (0). 
				Bone* bone_ = pBlendingProvider->GetBoneByIndex(this->nIndex);
				if (bone_ != 0 && bone_->nBoneID <= 0 && parent == bone_->parent)
				{
					pBlendBone = bone_;
				}
			}
		}
	}
	Quaternion q;
	Vector3 tr(0, 0, 0);
	Vector3 sc(1.f, 1.f, 1.f);


	if (pCurBone == NULL && pBlendBone == NULL)
	{
		//////////////////////////////////////////////////////////////////////////
		// Both current and blending anim are local
		Matrix4 m, mLocalRot;
		int nCurrentAnim = current_anim.nIndex;
		int currentFrame = current_anim.nCurrentFrame;
		int nBlendingAnim = current_blending_anim.nIndex;
		int blendingFrame = current_blending_anim.nCurrentFrame;

		if (IsStaticTransform())
		{
			if (GetExternalRot(pAnimInstance, q))
			{
				// use pivot point
				if (IsPivotBone())
				{
					m.makeTrans(pivot*-1.0f);
					if (GetExternalScaling(pAnimInstance, sc))
					{
						m.m[0][0] = sc.x;
						m.m[1][1] = sc.y;
						m.m[2][2] = sc.z;
						m.m[3][0] *= sc.x;
						m.m[3][1] *= sc.y;
						m.m[3][2] *= sc.z;
					}
					mLocalRot = Matrix4(q);
					m = m.Multiply4x3(mLocalRot);
					m.offsetTrans(pivot);
				}
				else
				{
					if (GetExternalScaling(pAnimInstance, sc))
					{
						m.makeScale(sc);
						mLocalRot = Matrix4(q);
						m *= mLocalRot;
					}
					else
					{
						mLocalRot = Matrix4(q);
						m = mLocalRot;
					}
				}
				if (GetExternalTranslation(pAnimInstance, tr))
				{
					m.offsetTrans(tr);
				}
				m = m * matTransform;
			}
			else
			{
				if (GetExternalScaling(pAnimInstance, sc))
				{
					m.makeScale(sc);
					if (GetExternalTranslation(pAnimInstance, tr))
					{
						m.offsetTrans(tr);
					}
					m = m * matTransform;
				}
				else if (GetExternalTranslation(pAnimInstance, tr))
				{
					m.makeTrans(tr);
					m = m * matTransform;
				}
				else
					m = matTransform;
			}
		}
		else if (rot.used || scale.used || trans.used || IsBillBoarded())
		{
			// #define PERFOAMRNCE_TEST_calcMatrix
#ifdef PERFOAMRNCE_TEST_calcMatrix
			PERF1("calcMatrix");
#endif
			// Compute transform matrix from SRT keys and the pivot point. m[column] = (pivot)*T*R*S*(-pivot)
			if (bUsePivot)
			{
				// use pivot point
				m.makeTrans(pivot*-1.0f);

				if (GetExternalScaling(pAnimInstance, sc) ||
					(scale.used && (sc = scale.getValue(nCurrentAnim, currentFrame/*, nBlendingAnim, blendingFrame, blendingFactor*/)) != Vector3::UNIT_SCALE))
				{
					m.m[0][0] = sc.x;
					m.m[1][1] = sc.y;
					m.m[2][2] = sc.z;
					m.m[3][0] *= sc.x;
					m.m[3][1] *= sc.y;
					m.m[3][2] *= sc.z;
				}
				if (GetExternalRot(pAnimInstance, q))
				{
					mLocalRot = Matrix4(q);
					m = m.Multiply4x3(mLocalRot);
				}
				else if (rot.used) {
					q = rot.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
					mLocalRot = Matrix4(q.invertWinding());
					m = m.Multiply4x3(mLocalRot);
				}

				if (GetExternalTranslation(pAnimInstance, tr))
				{
					m.offsetTrans(tr);
				}
				else if (trans.used) {
					tr = trans.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
					m.offsetTrans(tr);
				}
				m.offsetTrans(pivot);
			}
			else
			{
				// no pivot point is used.
				if (GetExternalScaling(pAnimInstance, sc) ||
					(scale.used && (sc = scale.getValue(nCurrentAnim, currentFrame/*, nBlendingAnim, blendingFrame, blendingFactor*/)) != Vector3::UNIT_SCALE))

				{
					m.makeScale(sc);
					if (GetExternalRot(pAnimInstance, q))
					{
						mLocalRot = Matrix4(q);
						m = m.Multiply4x3(mLocalRot);
					}
					else if (rot.used) {
						q = rot.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
						mLocalRot = Matrix4(q.invertWinding());
						m = m.Multiply4x3(mLocalRot);
					}
				}
				else
				{
					if (GetExternalRot(pAnimInstance, q))
					{
						mLocalRot = Matrix4(q);
						m = mLocalRot;
					}
					else if (rot.used) {
						q = rot.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
						mLocalRot = Matrix4(q.invertWinding());
						m = mLocalRot;
					}
					else
						m.identity();
				}

				if (GetExternalTranslation(pAnimInstance, tr))
				{
					m.offsetTrans(tr);
				}
				else if (trans.used) {
					tr = trans.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
					m.offsetTrans(tr);
				}
			}
		}
		else
		{
			m.identity();
		}

		if (parent >= 0) {
			allbones[parent].calcMatrix(allbones, CurrentAnim, BlendingAnim, blendingFactor, pAnimInstance);
			mat = m * allbones[parent].mat;
		}
		else
			mat = m;
	}
	else
	{
		//////////////////////////////////////////////////////////////////////////
		// either current anim or the blending animation references an external animation provider.
		Matrix4 m, mLocalRot;
		mLocalRot.identity();
		m.identity();
		int nCurrentAnim = current_anim.nIndex;
		int currentFrame = current_anim.nCurrentFrame;
		int nBlendingAnim = current_blending_anim.nIndex;
		int blendingFrame = current_blending_anim.nCurrentFrame;

		// Compute transform matrix from SRT keys and the pivot point. m[column] = (pivot)*T*R*S*(-pivot)
		if (bUsePivot)
		{
			// use pivot point
			m.makeTrans(pivot*-1.0f);
			if (scale.used)
			{
				// always uses local scale
				sc = scale.getValue(current_anim);

				m.m[0][0] = sc.x;
				m.m[1][1] = sc.y;
				m.m[2][2] = sc.z;
				m.m[3][0] *= sc.x;
				m.m[3][1] *= sc.y;
				m.m[3][2] *= sc.z;
			}
			//if (rot.used) 
			if (GetExternalRot(pAnimInstance, q))
			{
				mLocalRot = Matrix4(q);
				m = m.Multiply4x3(mLocalRot);
			}
			else
			{
				//////////////////////////////////////////////////////////////////////////
				// external animation may affect the rotations, but not scale or translation, except the root and facial bone.
				Quaternion currentValue;
				Quaternion blendValue;
				if (pCurBone != NULL)
				{
					currentValue = pCurBone->rot.getValue(pCurProvider->GetSubAnimID(), current_anim.nCurrentFrame);
				}
				else
				{
					if (current_anim.Provider == 0)
						currentValue = rot.getValue(current_anim);
					else
						currentValue = rot.getDefaultValue();
				}
				if (current_blending_factor != 0.f)
				{
					if (pBlendBone != NULL)
					{
						blendValue = pBlendBone->rot.getValue(pBlendingProvider->GetSubAnimID(), current_blending_anim.nCurrentFrame);
					}
					else
					{
						if (current_blending_anim.Provider == 0)
							blendValue = rot.getValue(current_blending_anim);
						else
							blendValue = currentValue;
					}
					if (pCurBone == NULL && current_anim.Provider != 0)
					{
						currentValue = blendValue;
					}
				}
				q = rot.BlendValues(currentValue, blendValue, current_blending_factor);
				mLocalRot = Matrix4(q.invertWinding());
				m = m * mLocalRot;
			}
			//if (trans.used) 
			{
				if (!(nBoneID == Bone_Root || (nBoneID >= Bone_forehand && nBoneID <= Bone_chin)))
				{
					// this is any other bone, except the root bone and facial animation bone.
					tr = trans.getValue(current_anim, current_blending_anim, current_blending_factor);
					m.offsetTrans(tr);
				}
				else
				{
					// only root node and facial animation may contain translation animation, in shared animation mode? such as BVH files.
					// more over, translation animation is scaled uniformly according to the pivot point Y values in the external animation file vs local file.
					Vector3 currentValue;
					Vector3 blendValue;

					if (pCurBone != NULL)
					{
						currentValue = pCurBone->trans.getValue(pCurProvider->GetSubAnimID(), current_anim.nCurrentFrame);
						if (nBoneID == Bone_Root)
						{
							// translation animation is scaled uniformly according to the pivot point Y values in the external animation file vs local file.
							currentValue *= (pivot.y / pCurBone->pivot.y);
						}
					}
					else
					{
						if (current_anim.Provider == 0)
							currentValue = trans.getValue(current_anim);
						else
							currentValue = trans.getDefaultValue();
					}

					if (current_blending_factor != 0.f)
					{
						if (pBlendBone != NULL)
						{
							blendValue = pBlendBone->trans.getValue(pBlendingProvider->GetSubAnimID(), current_blending_anim.nCurrentFrame);
							if (nBoneID == Bone_Root)
							{
								// translation animation is scaled uniformly according to the pivot point Y values in the external animation file vs local file.
								blendValue *= (pivot.y / pBlendBone->pivot.y);
							}
						}
						else
						{
							if (current_blending_anim.Provider == 0)
								blendValue = trans.getValue(current_blending_anim);
							else
								blendValue = currentValue;
						}
						if (pCurBone == NULL && current_anim.Provider != 0)
						{
							currentValue = blendValue;
						}
					}

					tr = trans.BlendValues(currentValue, blendValue, current_blending_factor);
					m.offsetTrans(tr);
				}
			}
			m.offsetTrans(pivot);
		}
		else if (IsStaticTransform())
		{
			if (GetExternalRot(pAnimInstance, q))
			{
				// use pivot point
				if (IsPivotBone())
				{
					m.makeTrans(pivot*-1.0f);
					mLocalRot = Matrix4(q);
					m = m.Multiply4x3(mLocalRot);
					m.offsetTrans(pivot);
				}
				else
				{
					mLocalRot = Matrix4(q);
					m = mLocalRot;
				}
			}
			else
			{
				m = matTransform;
			}
		}
		else
		{
			// external animation is not applied when there is no pivot point in the bone
			// no pivot point is used; 
			if (scale.used)
			{
				// always uses local scale
				sc = scale.getValue(current_anim);

				m.makeScale(sc);
				if (GetExternalRot(pAnimInstance, q))
				{
					mLocalRot = Matrix4(q);
					m = m.Multiply4x3(mLocalRot);
				}
				else if (rot.used) {
					q = rot.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
					mLocalRot = Matrix4(q.invertWinding());
					m = m.Multiply4x3(mLocalRot);
				}
			}
			else
			{
				if (GetExternalRot(pAnimInstance, q))
				{
					mLocalRot = Matrix4(q);
					m = mLocalRot;
				}
				else if (rot.used) {
					q = rot.getValue(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, current_blending_factor);
					mLocalRot = Matrix4(q.invertWinding());
					m = mLocalRot;
				}
				else
					m.identity();
			}
			if (trans.used) {
				tr = trans.getValue(current_anim, current_blending_anim, current_blending_factor);
				m.offsetTrans(tr);
			}
		}


		if (parent >= 0) {
			allbones[parent].calcMatrix(allbones, CurrentAnim, BlendingAnim, blendingFactor, pAnimInstance);
			mat = m * allbones[parent].mat;
		}
		else
			mat = m;
	}

	if (IsBillBoarded())
	{
		//////////////////////////////////////////////////////////////////////////
		// billboarding should be applied after the entire bone transformation is done.

		Matrix4 mtrans = CGlobals::GetViewMatrixStack().SafeGetTop();
		Matrix4 mtransWorld = CGlobals::GetWorldMatrixStack().SafeGetTop();
		mtransWorld = mat * mtransWorld; // added 

		// convert everything to model space, so that we have look, up, right vector in model space.  
		mtrans = mtransWorld * mtrans;
		mtrans.invert();
		Vector3 camera = Vector3(0, 0, 0) * mtrans;
		Vector3 look = (camera - pivot).normalisedCopy();
		Vector3 up = ((mtrans * Vector3(0, 1, 0)) - camera).normalisedCopy();
		Vector3 right = (up % look).normalisedCopy();
		up = (look % right).normalisedCopy();

		// calculate a billboard matrix
		Matrix4 mbb;
		mbb.identity();

		mbb.m[2][0] = right.x;
		mbb.m[2][1] = right.y;
		mbb.m[2][2] = right.z;
		mbb.m[1][0] = up.x;
		mbb.m[1][1] = up.y;
		mbb.m[1][2] = up.z;
		mbb.m[0][0] = look.x;
		mbb.m[0][1] = look.y;
		mbb.m[0][2] = look.z;

		// fixed pivot LXZ 2008.12.3. 
		if (bUsePivot)
		{
			mtrans.makeTrans(pivot*-1.0f);
			mtrans = mtrans * mbb;
			mtrans.offsetTrans(pivot);
			mbb = mtrans;
		}

		mat = mbb * mat;
	}
	SetFinalRot(q);
	SetFinalTrans(tr);
	SetFinalScaling(sc);
	return true;
}

ParaEngine::Bone::~Bone()
{

}

const std::string& ParaEngine::Bone::GetIdentifier()
{
	if (m_sIdentifer.empty())
	{
		if (GetBoneID() > 0)
		{
			KNOWN_BONE_NODES boneNames = (KNOWN_BONE_NODES)GetBoneID();
			switch (boneNames)
			{
			case ParaEngine::Bone_Root:
				SetName("Root");
				break;
			case ParaEngine::Bone_Pelvis:
				SetName("Pelvis");
				break;
			case ParaEngine::Bone_Spine:
				SetName("Spine");
				break;
			case ParaEngine::Bone_L_Thigh:
				SetName("L_Thigh");
				break;
			case ParaEngine::Bone_L_Calf:
				SetName("L_Calf");
				break;
			case ParaEngine::Bone_L_Foot:
				SetName("L_Foot");
				break;
			case ParaEngine::Bone_R_Thigh:
				SetName("R_Thigh");
				break;
			case ParaEngine::Bone_R_Calf:
				SetName("R_Calf");
				break;
			case ParaEngine::Bone_R_Foot:
				SetName("R_Foot");
				break;
			case ParaEngine::Bone_L_Clavicle:
				SetName("L_Clavicle");
				break;
			case ParaEngine::Bone_L_UpperArm:
				SetName("L_UpperArm");
				break;
			case ParaEngine::Bone_L_Forearm:
				SetName("L_Forearm");
				break;
			case ParaEngine::Bone_L_Hand:
				SetName("L_Hand");
				break;
			case ParaEngine::Bone_R_Clavicle:
				SetName("R_Clavicle");
				break;
			case ParaEngine::Bone_R_UpperArm:
				SetName("R_UpperArm");
				break;
			case ParaEngine::Bone_R_Forearm:
				SetName("R_Forearm");
				break;
			case ParaEngine::Bone_R_Hand:
				SetName("R_Hand");
				break;
			case ParaEngine::Bone_Head:
				SetName("Head");
				break;
			case ParaEngine::Bone_Neck:
				SetName("Neck");
				break;
			case ParaEngine::Bone_L_Toe0:
				SetName("L_Toe0");
				break;
			case ParaEngine::Bone_R_Toe0:
				SetName("R_Toe0");
				break;
			case ParaEngine::Bone_R_Finger0:
				SetName("R_Finger0");
				break;
			case ParaEngine::Bone_L_Finger0:
				SetName("L_Finger0");
				break;
			case ParaEngine::Bone_Spine1:
				SetName("Spine1");
				break;
			case ParaEngine::Bone_Spine2:
				SetName("Spine2");
				break;
			case ParaEngine::Bone_Spine3:
				SetName("Spine3");
				break;
			case ParaEngine::Bone_forehand:
				SetName("forehand");
				break;
			case ParaEngine::Bone_L_eyelid:
				SetName("L_eyelid");
				break;
			case ParaEngine::Bone_R_eyelid:
				SetName("R_eyelid");
				break;
			case ParaEngine::Bone_L_eye:
				SetName("L_eye");
				break;
			case ParaEngine::Bone_R_eye:
				SetName("R_eye");
				break;
			case ParaEngine::Bone_B_eyelid:
				SetName("B_eyelid");
				break;
			case ParaEngine::Bone_upper_lip:
				SetName("upper_lip");
				break;
			case ParaEngine::Bone_L_lip:
				SetName("L_lip");
				break;
			case ParaEngine::Bone_R_lip:
				SetName("R_lip");
				break;
			case ParaEngine::Bone_B_lip:
				SetName("B_lip");
				break;
			case ParaEngine::Bone_chin:
				SetName("chin");
				break;
			case ParaEngine::Bone_R_Finger01:
				SetName("R_Finger01");
				break;
			case ParaEngine::Bone_L_Finger01:
				SetName("RL_Finger01oot");
				break;
			case ParaEngine::Bone_R_Finger1:
				SetName("R_Finger1");
				break;
			case ParaEngine::Bone_L_Finger1:
				SetName("L_Finger1");
				break;
			case ParaEngine::Bone_R_Finger11:
				SetName("R_Finger11");
				break;
			case ParaEngine::Bone_L_Finger11:
				SetName("L_Finger11");
				break;
			case ParaEngine::Bone_R_Finger2:
				SetName("R_Finger2");
				break;
			case ParaEngine::Bone_L_Finger2:
				SetName("L_Finger2");
				break;
			case ParaEngine::Bone_R_Finger21:
				SetName("R_Finger21");
				break;
			case ParaEngine::Bone_L_Finger21:
				SetName("L_Finger21");
				break;
			default:
			{
				CVariable var;
				var = nIndex;
				SetName(std::string("Unknown") + (const std::string&)var);
				break;
			}
			}
		}
		else
		{
			CVariable var;
			var = nIndex;
			SetName((const std::string&)var);
		}
	}
	return GetName();
}

void ParaEngine::Bone::SetName(const std::string& val)
{
	m_sIdentifer = val;
}

void ParaEngine::Bone::AutoSetBoneInfoFromName()
{
	if (m_sIdentifer.empty() || GetBoneID() > 0)
		return;
	std::string sName = m_sIdentifer;
	StringHelper::make_lower(sName);

	// check special meaning ending names
	{
		int nSize = sName.size();
		int nMarkIndex = nSize - 2;// Index of the character '_'

		while (nMarkIndex >= 0 && sName[nMarkIndex] == '_')
		{
			char symbol = sName[nMarkIndex + 1];
			if (symbol == 'b')
			{
				// the bone is billboarded. always facing the camera. 
				flags |= 0x8;
			}
			else if (symbol == 'u')
			{
				// the bone is billboarded, but up axis is fixed. always facing the camera. 
				flags |= 0x4;
			}
			nMarkIndex -= 2;
		}
	}
	// Check the bone name for some predefined attachment points
	if ((int)sName.length() > 4 && sName[0] == 'a' && sName[1] == 't' && sName[2] == 't' && sName[3] == '_')
	{
		// if the name begins with "att". 
		string sAttName = sName.substr(4);
		if (sAttName == "lefthand")
		{
			SetBoneID(-ATT_ID_HAND_LEFT);
			mIsUpper = true;
		}
		else if (sAttName == "righthand")
		{
			SetBoneID(-ATT_ID_HAND_RIGHT);
			mIsUpper = true;
		}
		else if (sAttName == "head")
		{
			SetBoneID(-ATT_ID_HEAD);
			mIsUpper = true;
		}
		else if (sAttName == "text")
		{
			SetBoneID(-ATT_ID_TEXT);
		}
		else if (sAttName == "ground")
		{
			SetBoneID(-ATT_ID_GROUND);
		}
		else if (sAttName == "leftshoulder")
		{
			SetBoneID(-ATT_ID_SHOULDER_LEFT);
		}
		else if (sAttName == "rightshoulder")
		{
			SetBoneID(-ATT_ID_SHOULDER_RIGHT);
		}
		else if (sAttName == "boots")
		{
			SetBoneID(-ATT_ID_BOOTS);
			mIsUpper = true;
		}
		else if (sAttName == "neck")
		{
			SetBoneID(-ATT_ID_NECK);
			mIsUpper = true;
		}
		else if (sAttName == "mouth")
		{
			SetBoneID(-ATT_ID_MOUTH);
		}
		else if (sAttName == "face" || sAttName == "overhead")
		{
			SetBoneID(-ATT_ID_FACE_ADDON);
		}
		else if (sAttName == "leftear")
		{
			SetBoneID(-ATT_ID_EAR_LEFT_ADDON);
		}
		else if (sAttName == "rightear")
		{
			SetBoneID(-ATT_ID_EAR_RIGHT_ADDON);
		}
		else if (sAttName == "back")
		{
			SetBoneID(-ATT_ID_BACK_ADDON);
		}
		else if (sAttName == "waist")
		{
			SetBoneID(-ATT_ID_WAIST);
		}
	}
	else if (StringHelper::StrEndsWithWord(sName, "mount") || StringHelper::StrEndsWithWord(sName, "shield"))
	{
		// Default Mount or shield position
		SetBoneID(-ATT_ID_MOUNT00);
	}
	else if (StringHelper::StrEndsWithWord(sName, "mount?") || StringHelper::StrEndsWithWord(sName, "mount??"))
	{
		// additional mount position
		int nMountBoneIndex = 0;
		char c = sName[sName.size() - 1];
		if (c >= '0' && c <= '9')
			nMountBoneIndex = c - '0';
		c = sName[sName.size() - 2];
		if (c >= '0' && c <= '9')
			nMountBoneIndex = (c - '0') * 10 + nMountBoneIndex;

		int nAttID = ATT_ID_MOUNT00;
		if (nMountBoneIndex >= 1 && nMountBoneIndex <= 99)
		{
			nAttID = ATT_ID_MOUNT1 + (nMountBoneIndex - 1);
		}
		SetBoneID(-nAttID);

		if (nMountBoneIndex >= 1 && nMountBoneIndex <= 7)
			mIsUpper = true;
	}
	else
	{
		std::string::size_type nPos = -1;
		if (StringHelper::StrEndsWithWord(sName, "r?hand"))
		{
			SetBoneID(Bone_R_Hand);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?hand"))
		{
			SetBoneID(Bone_L_Hand);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?foot"))
		{
			SetBoneID(Bone_L_Foot);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?foot"))
		{
			SetBoneID(Bone_R_Foot);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?upperarm"))
		{
			SetBoneID(Bone_L_UpperArm);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?upperarm"))
		{
			SetBoneID(Bone_R_UpperArm);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "pelvis"))
		{
			SetBoneID(Bone_Pelvis);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "spine"))
		{
			SetBoneID(Bone_Spine);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "spine1"))
		{
			SetBoneID(Bone_Spine1);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "spine2"))
		{
			SetBoneID(Bone_Spine2);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "spine3"))
		{
			SetBoneID(Bone_Spine3);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?thigh"))
		{
			SetBoneID(Bone_L_Thigh);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?thigh"))
		{
			SetBoneID(Bone_R_Thigh);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?calf"))
		{
			SetBoneID(Bone_L_Calf);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?calf"))
		{
			SetBoneID(Bone_R_Calf);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?forearm"))
		{
			SetBoneID(Bone_L_Forearm);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?forearm"))
		{
			SetBoneID(Bone_R_Forearm);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?clavicle"))
		{
			SetBoneID(Bone_L_Clavicle);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?clavicle"))
		{
			SetBoneID(Bone_R_Clavicle);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?toe0"))
		{
			SetBoneID(Bone_L_Toe0);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?toe0"))
		{
			SetBoneID(Bone_R_Toe0);
			SetIdentifier("");
		}
		else if (StringHelper::StrEndsWithWord(sName, "neck"))
		{
			SetBoneID(Bone_Neck);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?finger0"))
		{
			SetBoneID(Bone_L_Finger0);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?finger0"))
		{
			SetBoneID(Bone_R_Finger0);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "l?finger1"))
		{
			SetBoneID(Bone_L_Finger1);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if (StringHelper::StrEndsWithWord(sName, "r?finger1"))
		{
			SetBoneID(Bone_R_Finger1);
			SetIdentifier("");
			mIsUpper = true;
		}
		else if ((nPos = sName.find("head")) != string::npos)
		{
			if ((nPos == (sName.size() - 4)) &&
				(nPos == 0 || sName[nPos - 1] == ' ' || sName[nPos - 1] == '_'))
			{
				SetBoneID(Bone_Head);
				SetIdentifier("");
				mIsUpper = true;
			}
		}
		else if (StringHelper::StrEndsWithWord(sName, "upper"))
		{
			mIsUpper = true;
		}
	}
}

void ParaEngine::Bone::SetIdentifier(const std::string& sID)
{
	m_sIdentifer = sID;
}

void ParaEngine::Bone::SetOffsetMatrix(const Matrix4& mat)
{
	matOffset = mat;
	flags |= BONE_OFFSET_MATRIX;
	bUsePivot = false;
}

const std::string& ParaEngine::Bone::GetName() const
{
	return m_sIdentifer;
}

void ParaEngine::Bone::SetStaticTransform(const Matrix4& mat)
{
	matTransform = mat;
	flags |= BONE_STATIC_TRANSFORM;
	bUsePivot = false;
}

bool ParaEngine::Bone::CheckHasAnimation()
{
	return !(IsStaticTransform() || (!scale.CheckIsAnimated() && !trans.CheckIsAnimated() && !rot.CheckIsAnimated()));
}

bool ParaEngine::Bone::IsAnimated()
{
	return !(IsStaticTransform() || (!scale.used && !trans.used && !rot.used));
}

bool ParaEngine::Bone::GetExternalRot(IAttributeFields* pAnimInstance, Quaternion& outQuat)
{
	if (pAnimInstance && pAnimInstance->GetDynamicFieldCount() > 0)
	{
		CDynamicAttributeField* pVarField = pAnimInstance->GetDynamicField(GetRotName());
		if (pVarField)
		{
			int nTime = pAnimInstance->GetTime();
			CDynamicAttributeField* pTimeField = pAnimInstance->GetDynamicField(GetTimeName());
			if (pTimeField != 0) {
				nTime = (int)((double)(*pTimeField));
				if(nTime < 0)
					nTime = pAnimInstance->GetTime();
			}
			return pVarField->GetValueByTime(nTime, outQuat);
		}
	}
	return false;
}

bool ParaEngine::Bone::GetExternalTranslation(IAttributeFields* pAnimInstance, Vector3& outTrans)
{
	if (pAnimInstance && pAnimInstance->GetDynamicFieldCount() > 0)
	{
		CDynamicAttributeField* pVarField = pAnimInstance->GetDynamicField(GetTransName());
		if (pVarField)
		{
			int nTime = pAnimInstance->GetTime();
			CDynamicAttributeField* pTimeField = pAnimInstance->GetDynamicField(GetTimeName());
			if (pTimeField != 0) {
				nTime = (int)((double)(*pTimeField));
				if (nTime < 0)
					nTime = pAnimInstance->GetTime();
			}
			return pVarField->GetValueByTime(nTime, outTrans);
		}
	}
	return false;
}

bool ParaEngine::Bone::GetExternalScaling(IAttributeFields* pAnimInstance, Vector3& outScaling)
{
	if (pAnimInstance && pAnimInstance->GetDynamicFieldCount() > 0)
	{
		CDynamicAttributeField* pVarField = pAnimInstance->GetDynamicField(GetScaleName());
		if (pVarField)
		{
			int nTime = pAnimInstance->GetTime();
			CDynamicAttributeField* pTimeField = pAnimInstance->GetDynamicField(GetTimeName());
			if (pTimeField != 0) {
				nTime = (int)((double)(*pTimeField));
				if (nTime < 0)
					nTime = pAnimInstance->GetTime();
			}
			return pVarField->GetValueByTime(nTime, outScaling);
		}
	}
	return false;
}

void ParaEngine::Bone::PostCalculateBoneMatrix()
{
	if (IsOffsetMatrixBone() && !IsAttachment())
	{
		mat = matOffset * mat;
	}
	// compute transformation matrix (mrot) for normal vectors 
	{
		// Quaternion q = mat.extractQuaternion();
		// q.ToRotationMatrix(mrot, Vector3::ZERO);
		mrot = mat.RemoveTranslation();
		mrot.RemoveScaling();
	}
}

const ParaEngine::Matrix4& ParaEngine::Bone::GetFinalMatrix()
{
	return mat;
}

const Vector3& ParaEngine::Bone::GetPivotPoint()
{
	return pivot;
}


ParaEngine::Vector3 ParaEngine::Bone::GetAnimatedPivotPoint()
{
	if (IsOffsetMatrixBone() || IsPivotBone())
	{
		Vector3 vPivot = pivot * mat;
		return vPivot;
	}
	else
	{
		return Vector3(mat._41, mat._42, mat._43);
	}
}

int ParaEngine::Bone::IsAttachment() const
{
	return nBoneID < 0;
}

int ParaEngine::Bone::GetAttachmentId() const
{
	return nBoneID < 0 ? ((-nBoneID == ATT_ID_MOUNT00) ? 0 : -nBoneID) : -1;
}

const ParaEngine::Quaternion& ParaEngine::Bone::GetFinalRot() const
{
	return m_finalRot;
}

void ParaEngine::Bone::SetFinalRot(const ParaEngine::Quaternion& val)
{
	m_finalRot = val;
}

const Vector3 & ParaEngine::Bone::GetFinalTrans() const
{
	return m_finalTrans;
}

void ParaEngine::Bone::SetFinalTrans(const Vector3 &val)
{
	m_finalTrans = val;
}

const Vector3& ParaEngine::Bone::GetFinalScaling() const
{
	return m_finalScaling;
}

void ParaEngine::Bone::SetFinalScaling(const Vector3& val)
{
	m_finalScaling = val;
}

const ParaEngine::Matrix4& ParaEngine::Bone::GetFinalRotMatrix() const
{
	return mrot;
}

ParaEngine::Matrix4 ParaEngine::Bone::GetPivotRotMatrix()
{
	if (IsOffsetMatrixBone())
	{
		Matrix4 mat = matOffset.RemoveTranslation();
		mat.RemoveScaling();
		mat.invert();
		mat = mat * GetFinalRotMatrix();
		return mat;
	}
	else
	{
		return GetFinalRotMatrix();
	}
}

void ParaEngine::Bone::MakeDirty(bool bForce)
{
	calc = false;
}

const std::string& ParaEngine::Bone::GetRotName()
{

	if (m_sRotName.empty())
	{
		m_sRotName = GetIdentifier() + "_rot";
	}
	return m_sRotName;
}

const std::string& ParaEngine::Bone::GetTransName()
{
	if (m_sTransName.empty())
	{
		m_sTransName = GetIdentifier() + "_trans";
	}
	return m_sTransName;
}

const std::string& ParaEngine::Bone::GetScaleName()
{
	if (m_sScaleName.empty())
	{
		m_sScaleName = GetIdentifier() + "_scale";
	}
	return m_sScaleName;
}

const std::string& ParaEngine::Bone::GetTimeName()
{
	if (m_sTimeName.empty())
	{
		m_sTimeName = GetIdentifier() + "_time";
	}
	return m_sTimeName;
}

int ParaEngine::Bone::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	IAttributeFields::InstallFields(pClass, bOverride);

	pClass->AddField("RotName", FieldType_String, (void*)0, (void*)GetRotName_s, NULL, "", bOverride);
	pClass->AddField("TransName", FieldType_String, (void*)0, (void*)GetTransName_s, NULL, "", bOverride);
	pClass->AddField("ScaleName", FieldType_String, (void*)0, (void*)GetScaleName_s, NULL, "", bOverride);
	pClass->AddField("TimeName", FieldType_String, (void*)0, (void*)GetTimeName_s, NULL, "", bOverride);

	pClass->AddField("IsBillBoarded", FieldType_Bool, (void*)0, (void*)IsBillBoarded_s, NULL, "", bOverride);
	pClass->AddField("IsPivotBone", FieldType_Bool, (void*)0, (void*)IsPivotBone_s, NULL, "", bOverride);
	pClass->AddField("IsOffsetMatrixBone", FieldType_Bool, (void*)0, (void*)IsOffsetMatrixBone_s, NULL, "", bOverride);
	pClass->AddField("IsStaticTransform", FieldType_Bool, (void*)0, (void*)IsStaticTransform_s, NULL, "", bOverride);
	pClass->AddField("IsTransformationNode", FieldType_Bool, (void*)0, (void*)IsTransformationNode_s, NULL, "", bOverride);

	pClass->AddField("IsAnimated", FieldType_Bool, (void*)0, (void*)IsAnimated_s, NULL, "", bOverride);
	pClass->AddField("OffsetMatrix", FieldType_Matrix4, (void*)SetOffsetMatrix_s, (void*)0, NULL, "", bOverride);
	pClass->AddField("SetStaticTransform", FieldType_Matrix4, (void*)SetStaticTransform_s, (void*)0, NULL, "", bOverride);
	pClass->AddField("FinalMatrix", FieldType_Matrix4, (void*)0, (void*)GetFinalMatrix_s, NULL, "", bOverride);
	pClass->AddField("FinalRotMatrix", FieldType_Matrix4, (void*)0, (void*)GetFinalRotMatrix_s, NULL, "", bOverride);
	pClass->AddField("PivotRotMatrix", FieldType_Matrix4, (void*)0, (void*)GetPivotRotMatrix_s, NULL, "", bOverride);

	pClass->AddField("PivotPoint", FieldType_Vector3, (void*)0, (void*)GetPivotPoint_s, NULL, "", bOverride);
	pClass->AddField("AnimatedPivotPoint", FieldType_Vector3, (void*)0, (void*)GetAnimatedPivotPoint_s, NULL, "", bOverride);
	pClass->AddField("FinalRot", FieldType_Quaternion, (void*)SetFinalRot_s, (void*)GetFinalRot_s, NULL, "", bOverride);
	pClass->AddField("FinalTrans", FieldType_Vector3, (void*)SetFinalTrans_s, (void*)GetFinalTrans_s, NULL, "", bOverride);
	pClass->AddField("FinalScaling", FieldType_Vector3, (void*)SetFinalScaling_s, (void*)GetFinalScaling_s, NULL, "", bOverride);

	pClass->AddField("ParentIndex", FieldType_Int, (void*)0, (void*)GetParentIndex_s, NULL, "", bOverride);
	pClass->AddField("BoneIndex", FieldType_Int, (void*)0, (void*)GetBoneIndex_s, NULL, "", bOverride);
	pClass->AddField("BoneID", FieldType_Int, (void*)SetBoneID_s, (void*)GetBoneID_s, NULL, "", bOverride);

	return S_OK;
}

Bone& ParaEngine::Bone::operator=(const Bone& other)
{
	m_sIdentifer = other.m_sIdentifer;
	m_sRotName = other.m_sRotName;
	m_sTransName = other.m_sTransName;
	m_sScaleName = other.m_sScaleName;

	trans = other.trans;
	rot = other.rot;
	scale = other.scale;

	pivot = other.pivot;
	matOffset = other.matOffset;
	matTransform = other.matTransform;

	parent = other.parent;
	nBoneID = other.nBoneID;
	nIndex = other.nIndex;

	flags = other.flags;

	mat = other.mat;

	mrot = other.mrot;

	m_finalRot = other.m_finalRot;

	m_finalTrans = other.m_finalTrans;

	m_finalScaling = other.m_finalScaling;

	calc = other.calc;
	bUsePivot = other.bUsePivot;

	mIsUpper=other.mIsUpper;

	return *this;
}

#pragma once
#include "animated.h"
#include "IAttributeFields.h"

namespace ParaEngine
{
	class CBVHSerializer;

	/** a single animated bone,  it contains both the bone instance data and all animation data of the bone. 
	There are three ways to calculate final bone matrix. 
	1. using each bone's pivot point and SRT transforms relative to the current bone
	2. using offset matrix (which transform from mesh to local bone space) and SRT transforms relative to the parent bone
	3. the bone has no animation and a static transform is used to transform from current bone space to its parent bone space. 
	*/
	class Bone : public IAttributeFields
	{
	public:
		Bone();
		virtual ~Bone();

		ATTRIBUTE_DEFINE_CLASS(Bone);

		/** this class should be implemented if one wants to add new attribute. This function is always called internally.*/
		virtual int InstallFields(CAttributeClass* pClass, bool bOverride);
		
		ATTRIBUTE_METHOD1(Bone, GetRotName_s, const char**)		{ *p1 = cls->GetRotName().c_str(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetTransName_s, const char**)		{ *p1 = cls->GetTransName().c_str(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetScaleName_s, const char**)		{ *p1 = cls->GetScaleName().c_str(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetTimeName_s, const char**) { *p1 = cls->GetTimeName().c_str(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, IsBillBoarded_s, bool*)		{ *p1 = cls->IsBillBoarded(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, IsPivotBone_s, bool*)		{ *p1 = cls->IsPivotBone(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, IsOffsetMatrixBone_s, bool*){ *p1 = cls->IsOffsetMatrixBone(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, IsTransformationNode_s, bool*)	{ *p1 = cls->IsTransformationNode(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, IsStaticTransform_s, bool*) { *p1 = cls->IsStaticTransform(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, IsAnimated_s, bool*)		{ *p1 = cls->IsAnimated(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, SetOffsetMatrix_s, const Matrix4&)		{ cls->SetOffsetMatrix(p1); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, SetStaticTransform_s, const Matrix4&)		{ cls->SetStaticTransform(p1); return S_OK; }
		
		ATTRIBUTE_METHOD(Bone, RemoveRedundentKeys_s)		{ cls->RemoveRedundentKeys(); return S_OK; }
		
		ATTRIBUTE_METHOD1(Bone, GetFinalMatrix_s, Matrix4*)		{ *p1 = cls->GetFinalMatrix(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetFinalRotMatrix_s, Matrix4*)		{ *p1 = cls->GetFinalRotMatrix(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetPivotRotMatrix_s, Matrix4*)		{ *p1 = cls->GetPivotRotMatrix(); return S_OK; }
		
		ATTRIBUTE_METHOD1(Bone, GetPivotPoint_s, Vector3*)		{ *p1 = cls->GetPivotPoint(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetAnimatedPivotPoint_s, Vector3*)		{ *p1 = cls->GetAnimatedPivotPoint(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, SetFinalRot_s, Quaternion)		{ cls->SetFinalRot(p1); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetFinalRot_s, Quaternion*)		{ *p1 = cls->GetFinalRot(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, SetFinalTrans_s, Vector3)		{ cls->SetFinalTrans(p1); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetFinalTrans_s, Vector3*)		{ *p1 = cls->GetFinalTrans(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, SetFinalScaling_s, Vector3)		{ cls->SetFinalScaling(p1); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetFinalScaling_s, Vector3*)		{ *p1 = cls->GetFinalScaling(); return S_OK; }

		ATTRIBUTE_METHOD1(Bone, GetParentIndex_s, int*)		{ *p1 = cls->GetParentIndex(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, GetBoneIndex_s, int*)		{ *p1 = cls->GetBoneIndex(); return S_OK; }
		
		ATTRIBUTE_METHOD1(Bone, GetBoneID_s, int*)		{ *p1 = cls->GetBoneID(); return S_OK; }
		ATTRIBUTE_METHOD1(Bone, SetBoneID_s, int)		{ cls->SetBoneID(p1); return S_OK; }
		
	public:
		/** get the name or identifier. */
		virtual const std::string& GetIdentifier();
		virtual void SetIdentifier(const std::string& sID);

		/** whether the bone is billboarded*/
		bool IsBillBoarded() const { return (flags & BONE_BILLBOARDED) != 0; };
		/** whether calculate bone matrix using each bone's pivot point and SRT transforms relative to the current bone.*/
		bool IsPivotBone() const { return (flags & BONE_OFFSET_MATRIX) == 0; };
		/** whether calculate bone matrix using offset matrix (which transform from mesh to local bone space) and SRT transforms relative to the parent bone */
		bool IsOffsetMatrixBone() const { return (flags & BONE_OFFSET_MATRIX) != 0; };
		/** whether the bone has no animation and a static transform is used to transform from current bone space to its parent bone space. */
		bool IsStaticTransform() const { return (flags & BONE_STATIC_TRANSFORM) != 0; };
		/** whether the bone is transformation node */
		bool IsTransformationNode() const { return (flags & BONE_TRANSFORMATION_NODE) != 0; };

		/** calling this function means that you want to use BONE_OFFSET_MATRIX for final bone matrix calculation. */
		void SetOffsetMatrix(const Matrix4& mat);
		
		/** calling this function means that you want to use BONE_STATIC_TRANSFORM for final bone matrix calculation. */
		void SetStaticTransform(const Matrix4& mat);

		/** whether the bone contains animation data. */
		bool CheckHasAnimation();

		const std::string& GetName() const;
		void SetName(const std::string& val);

		/** automatically set bone id from bone name. */
		void AutoSetBoneInfoFromName();

		/** whether bone is animated. */
		bool IsAnimated();
		/**
		* calc bone matrix and all of its parent bones.
		* @param nCurrentAnim: current animation sequence ID
		* @param currentFrame: an absolute ParaX frame number denoting the current animation frame. It is always within
		* the range of the current animation sequence's start and end frame number.
		* @param nBlendingAnim: the animation sequence with which the current animation should be blended.
		* @param blendingFrame: an absolute ParaX frame number denoting the blending animation frame. It is always within
		* the range of the blending animation sequence's start and end frame number.
		* @param blendingFactor: by how much the blending frame should be blended with the current frame.
		* 1.0 will use solely the blending frame, whereas 0.0 will use only the current frame.
		* [0,1), blendingFrame*(blendingFactor)+(1-blendingFactor)*currentFrame
		* @param pAnimInstance: if specified, we will use rotation variable in the animation instance if any.
		*/
		bool calcMatrix(Bone* allbones, const AnimIndex & CurrentAnim, const AnimIndex & BlendingAnim, float blendingFactor, IAttributeFields* pAnimInstance = NULL);
		/** for static bones */
		void calcMatrix(Bone* allbones);

		/** get external rot quaternion from animation instance. 
		* @return true, if rotation is found, otherwise the one in the bone should be used. 
		*/
		bool GetExternalRot(IAttributeFields* pAnimInstance, Quaternion& outQuat);
		bool GetExternalTranslation(IAttributeFields* pAnimInstance, Vector3& outTrans);
		bool GetExternalScaling(IAttributeFields* pAnimInstance, Vector3& outScaling);

		/**  Always call this function after loading data from files.*/
		void RemoveRedundentKeys();

		/* rotation and offset matrix are processed */
		void PostCalculateBoneMatrix();
		
		const ParaEngine::Matrix4& GetFinalMatrix();
		/** return the pivot point in binding space */
		const Vector3& GetPivotPoint();

		/** return the current pivot point */
		Vector3 GetAnimatedPivotPoint();

		int GetParentIndex() const { return parent; }
		int GetBoneIndex() const { return nIndex; }
		int GetBoneID() const { return nBoneID; }
		int IsAttachment() const;
		/** return -1 if it is not attachment id. of it is non-negative attachment id */
		int GetAttachmentId() const;
		void SetBoneID(int val) { nBoneID = val; }

		const ParaEngine::Quaternion& GetFinalRot() const;
		void SetFinalRot(const ParaEngine::Quaternion& val);

		const Vector3 & GetFinalTrans() const;
		void SetFinalTrans(const Vector3 &val);

		const Vector3& GetFinalScaling() const;
		void SetFinalScaling(const Vector3& val);

		const ParaEngine::Matrix4& GetFinalRotMatrix() const;
		/** similar to GetFinalRotMatrix(), except that it will remove rotation in its offset matrix. */
		Matrix4 GetPivotRotMatrix();
		
		/** mark this bone as un-calculated bone. 
		* @param bForce: if false(default), Static and transformation node are never dirty. 
		*/
		void MakeDirty(bool bForce = false);

		friend class CBVHSerializer;

		Bone& operator=(const Bone& other);
	
	public:
		enum BONE_FLAGS
		{
			/** calculate bone matrix using each bone's pivot point and SRT transforms relative to the current bone.
			* offset matrix is not used.
			*/
			BONE_USE_PIVOT = 0,
			/** whether the bone is billboarded */
			BONE_BILLBOARDED = (0x1 << 3),
			/** calculate bone matrix using offset matrix (which transform from mesh to local bone space) and SRT transforms relative to the parent bone
			* pivot point is not used.
			*/
			BONE_OFFSET_MATRIX = (0x1 << 4),
			/** the bone has no animation and a static transform is used to transform from current bone space to its parent bone space.  */
			BONE_STATIC_TRANSFORM = (0x1 << 5),
			/* the bone is the transformation node */
			BONE_TRANSFORMATION_NODE = (0x1 << 6),
		};
		std::string	m_sIdentifer;
		std::string	m_sRotName;
		std::string	m_sTransName;
		std::string	m_sScaleName;
		std::string	m_sTimeName;
		const std::string& GetRotName();
		const std::string& GetTransName();
		const std::string& GetScaleName();
		const std::string& GetTimeName();

		Animated<Vector3> trans;
		Animated<Quaternion> rot;
		Animated<Vector3> scale;

		// pivot point in binding pos
		Vector3 pivot;
		
		// offset matrix that transforms from mesh space to the current bone space. 
		Matrix4 matOffset;
		// the bone has no animation and a static transform is used to transform from current bone space to its parent bone space. 
		Matrix4 matTransform;

		// index of the parent bone
		int parent;
		
		// the predefined bone ID. it is 0 for unknown bones, positive for known bones. one of the KNOWN_BONE_NODES
		int nBoneID;

		// index of this bone
		int nIndex;
		
		// bitwise fields of bone attributes. BONE_BILLBOARDED for bill boarded. 
		DWORD flags;
	
		// temporary final matrix
		Matrix4 mat;
		
		// temporary final rotation matrix
		Matrix4 mrot;
		
		// temporary final m_finalRot used in composing the final mat
		Quaternion m_finalRot;

		// temporary final m_finalTrans used in composing the final mat
		Vector3 m_finalTrans;

		// temporary final m_finalScaling used in composing the final mat
		Vector3 m_finalScaling;
		
		bool calc;
		bool bUsePivot;

		bool mIsUpper;

		/** max number of bones per vertex, currently this is 4. */
		const static int s_MaxBonesPerVertex = 4;
	};
}

#pragma once

#include "MeshEntity.h"

namespace ParaEngine
{
	class CParaXModel;

	struct ParaXEntity : public AssetEntity
	{
	public:
		ParaXEntity(const AssetKey& key);
		ParaXEntity();
		virtual ~ParaXEntity();
		ATTRIBUTE_DEFINE_CLASS(ParaXEntity);

		/** this class should be implemented if one wants to add new attribute. This function is always called internally.*/
		virtual int InstallFields(CAttributeClass* pClass, bool bOverride);

		/** get the number of child objects (row count) in the given column. please note different columns can have different row count. */
		virtual int GetChildAttributeObjectCount(int nColumnIndex = 0);
		virtual IAttributeFields* GetChildAttributeObject(int nRowIndex, int nColumnIndex = 0);
		
		ATTRIBUTE_METHOD1(ParaXEntity, GetFileName_s, const char**)	{ *p1 = cls->GetFileName().c_str(); return S_OK; }

		ATTRIBUTE_METHOD1(ParaXEntity, DumpTextureUsage_s, const char**)	{ *p1 = cls->DumpTextureUsage(); return S_OK; }
		ATTRIBUTE_METHOD1(ParaXEntity, GetPolyCount_s, int*)	{ *p1 = cls->GetPolyCount(); return S_OK; }
		ATTRIBUTE_METHOD1(ParaXEntity, GetPhysicsCount_s, int*)	{ *p1 = cls->GetPhysicsCount(); return S_OK; }
		

	public:
		friend class CParaXProcessor;

		virtual void Cleanup();
		virtual AssetEntity::AssetType GetType(){ return AssetEntity::parax; };

		CAnimInstanceBase* CreateAnimInstance();

		virtual HRESULT InitDeviceObjects();
		virtual HRESULT DeleteDeviceObjects();

		/**
		* most assets are loaded asynchronously. This allows us to check if an asset is loaded. 
		* For example, we can LoadAsset() for a number of assets that need preloading. and then use a timer to check if they are initialized and remove from the uninialized list.  
		*/
		virtual bool IsLoaded();

		/** name of the model file(*.x) name holding the parax object
		get the mesh file name of the lowest level mesh. */
		const std::string& GetFileName();

		virtual IAttributeFields* GetAttributeObject();

		/**
		* refresh this texture surface with a local file. 
		* @param sFilename: if NULL or empty the old texture file(sTextureFileName) will be used. 
		* @param bLazyLoad if true it will be lazy loaded.
		*/
		void Refresh(const char* sFilename=NULL,bool bLazyLoad = false);

		/** get polycount of this mesh object */
		int GetPolyCount();
		/** get physics polycount of this mesh object */
		int GetPhysicsCount();
		/** get texture usage such as the number of textures and their sizes. */
		const char* DumpTextureUsage();

		/** Adds a new level-of-detail entry to this Mesh.
		@remarks
		As an alternative to generating lower level of detail versions of a mesh, you can
		use your own manually modeled meshes as lower level versions. This lets you 
		have complete control over the LOD, and in addition lets you scale down other
		aspects of the model which cannot be done using the generated method; for example, 
		you could use less detailed materials and / or use less bones in the skeleton if
		this is an animated mesh. Therefore for complex models you are likely to be better off
		modeling your LODs yourself and using this method, whilst for models with fairly
		simple materials and no animation you can just use the generateLodLevels method.
		@param fromDepth The z value from which this Lod will apply.
		@param meshName The name of the mesh which will be the lower level detail version.
		*/
		void CreateMeshLODLevel(float fromDepth, const std::string& sFilename);

		/** Changes the alternate mesh to use as a manual LOD at the given index.
		@remarks
		Note that the index of a LOD may change if you insert other LODs. If in doubt,
		use getLodIndex().
		@param index: The index of the level to be changed
		@param sFilename: The name of the mesh which will be the lower level detail version.
		*/
		void UpdateManualLodLevel(int index, const std::string& sFilename);

		/** Retrieves the level of detail index for the given depth value. 
		*/
		int GetLodIndex(float fCameraObjectDist, float fScaling = 1.f) const;

		/** Retrieves the level of detail index for the given squared depth value. 
		@remarks
		Internally, the LODs are stored at squared depths to avoid having to perform
		square roots when determining the lod. This method allows you to provide a
		squared length depth value to avoid having to do your own square roots.
		*/
		int GetLodIndexSquaredDepth(float squaredDepth, float fScaling = 1.f) const;

		/** Removes all LOD data from this Mesh. only the lowest level remains */
		void RemoveLodLevels(void);

		/** get the highest level mesh if LOD is enabled. 
		* @param nLODIndex: default to 0, where the lowest LOD level mesh is returned.
		*/
		CParaXModel* GetModel(int nLODIndex=0);

		/** try to get the highest level mesh if LOD is enabled without calling LoadAsset().
		* It can be called from other thread safely.
		* @param nLODIndex: default to 0, where the lowest LOD level mesh is returned.
		*/
		CParaXModel* TryGetModel(int nLODIndex = 0);
		
		/** init the parax model. */
		void Init(const char* filename=NULL);

		/** this function is mostly used internally. It will load the mesh from disk, unpack it and init the entity. 
		* when this function returns, the texture will be already loaded to device pool. 
		* @param pDev: if NULL, the default render device is used 
		* @param sFileName: if NULL, m_asset->GetLocalFileName() is used. 
		*/
		HRESULT CreateModelFromFile_Serial(RenderDevicePtr pDev=NULL, const char* sFileName=NULL);

		/** this function is mostly used internally. 
		* this function will return immediately. It will append the texture request to AsyncLoaders's IO queue. 
		* @param pContext: this should be a pointer to CAsyncLoader
		* @param pDev: if NULL, the default render device is used 
		* @param sFileName: if NULL, m_asset->GetLocalFileName() is used. 
		*/
		HRESULT CreateModelFromFile_Async(void* pContext, RenderDevicePtr pDev = NULL, const char* sFileName = NULL);
		
		void SetPrimaryTechniqueHandle(int nHandle);
		int GetPrimaryTechniqueHandle();

		/** Get AABB bounding box of the asset object. if the asset contains an OOB, it will return true. */
		virtual bool GetBoundingBox(Vector3* pMin, Vector3* pMax);

		void SetMergeCoplanerBlockFace(bool val);
		bool GetMergeCoplanerBlockFace();

		/** callback of listening the event that renderer was recreated on Android/WP8
		all opengl related id has already become invalid at this time, no need to release them, just recreate them all in this function.
		*/
		virtual HRESULT RendererRecreated();
	private:
		/// mesh objects in LOD list. each mesh may contain materials and textures, but you can simply 
		/// ignore them. The default setting is rendering with materials. See CParaXStaticMesh for more details
		std::vector<MeshLOD> m_MeshLODs;

		/** the primary technique handle*/
		int m_nTechniqueHandle;

		/** an option whether merge coplaner block faces when loading a bmax model*/
		bool m_bMergeCoplanerBlockFace;
	};

	typedef AssetManager<ParaXEntity>  ParaXEntityManager;
}

//-----------------------------------------------------------------------------
// Class:	ParaXEntity
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2004.3.8
// Revised: 2006.7.12
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BipedObject.h"
#include "ParaMeshXMLFile.h"
#include "ParaXAnimInstance.h"
#include "ParaXSerializer.h"
#include "ContentLoaders.h"
#include "AsyncLoader.h"
#include "ParaXEntity.h"

#include "memdebug.h"

using namespace ParaEngine;

/** place holder for being loaded parax models */
#define DEFAULT_PARAX_MODEL			"character/common/tag/tag.x"

ParaEngine::ParaXEntity::ParaXEntity(const AssetKey& key)
	: AssetEntity(key)
	, m_nTechniqueHandle(-1)
	, m_bMergeCoplanerBlockFace(true)
{

}

ParaEngine::ParaXEntity::ParaXEntity()
{

}

ParaEngine::ParaXEntity::~ParaXEntity()
{

}

int ParaXEntity::GetPrimaryTechniqueHandle()
{
	return m_nTechniqueHandle;
}

void ParaXEntity::SetPrimaryTechniqueHandle(int nHandle)
{
	m_nTechniqueHandle = nHandle;
}

HRESULT ParaXEntity::InitDeviceObjects()
{
	if(m_bIsInitialized)
		return S_OK;

	m_bIsInitialized = true;
	CreateModelFromFile_Async(NULL, NULL, NULL);
	return S_OK;
}

HRESULT ParaXEntity::DeleteDeviceObjects()
{
	m_bIsInitialized = false;

	std::vector<MeshLOD>::iterator iCur, iEnd = m_MeshLODs.end();
	for (iCur = m_MeshLODs.begin(); iCur != iEnd; ++iCur)
	{
		MeshLOD& lod = (*iCur);
		if(lod.m_pParaXMesh)
		{
			lod.m_pParaXMesh->DeleteDeviceObjects();
			lod.m_pParaXMesh.reset();
		}
	}
	return S_OK;
}

CAnimInstanceBase* ParaXEntity::CreateAnimInstance()
{
	CParaXAnimInstance* pAI = new CParaXAnimInstance();
	pAI->Init(this);
	return pAI;
}


void ParaXEntity::Refresh( const char* sFilename/*=NULL*/,bool bLazyLoad /*= false*/ )
{
	// TODO: not implemented yet. ParaX does not support remote sync at the moment
	m_bIsValid = true;
	if(sFilename != NULL && sFilename[0] != '\0')
	{
		SetLocalFileName(sFilename);
	}

	UnloadAsset();
	Cleanup(); // clean up LODs
	Init();
	if(!bLazyLoad)
		LoadAsset();
}

HRESULT ParaXEntity::CreateModelFromFile_Serial(RenderDevicePtr pDev, const char* sFileName)
{
	// Load Texture sequentially
	asset_ptr<ParaXEntity> my_asset(this);
	CParaXLoader loader_( my_asset, sFileName );
	CParaXLoader* pLoader = &loader_;
	CParaXProcessor processor_( my_asset );
	CParaXProcessor* pProcessor = &processor_;

	pProcessor->m_pDevice = pDev;

	void* pLocalData;
	int Bytes;
	if( SUCCEEDED(pLoader->Load()) && 
		SUCCEEDED(pLoader->Decompress( &pLocalData, &Bytes )) && 
		SUCCEEDED(pProcessor->Process( pLocalData, Bytes )) && 
		SUCCEEDED(pProcessor->LockDeviceObject()) && 
		SUCCEEDED(pProcessor->CopyToResource()) && 
		SUCCEEDED(pProcessor->UnLockDeviceObject()) )
	{
	}
	else
	{
		pProcessor->SetResourceError();
	}
	pProcessor->Destroy();
	pLoader->Destroy();
	return S_OK;
}

HRESULT ParaXEntity::CreateModelFromFile_Async(void* pContext, RenderDevicePtr pDev, const char* sFileName)
{
	// Load Texture asynchronously
	asset_ptr<ParaXEntity> my_asset(this);
	if(pContext == 0)
		pContext = &(CAsyncLoader::GetSingleton());
	CAsyncLoader* pAsyncLoader = ( CAsyncLoader* )pContext;
	if( pAsyncLoader )
	{
		CParaXLoader* pLoader = new CParaXLoader( my_asset, sFileName);
		CParaXProcessor* pProcessor = new CParaXProcessor( my_asset );
		pProcessor->m_pDevice = pDev;

		pAsyncLoader->AddWorkItem( pLoader, pProcessor, NULL, NULL );
	}
	return S_OK;
}

void ParaXEntity::Init(const char* sFilename)
{
	if(sFilename)
		SetLocalFileName(sFilename);
}

const string& ParaXEntity::GetFileName()
{
	if(m_MeshLODs.size()>0)
	{
		return m_MeshLODs[0].m_sMeshFileName;
	}
	else
	{
		return GetLocalFileName();
	}
}

CParaXModel* ParaXEntity::GetModel( int nLODIndex/*=0*/ )
{
	LoadAsset();
	if(IsValid() && ((int)m_MeshLODs.size())>nLODIndex && nLODIndex>=0)
		return m_MeshLODs[nLODIndex].m_pParaXMesh.get();
	else
		return nullptr;
}

CParaXModel* ParaXEntity::TryGetModel(int nLODIndex)
{
	if (IsValid() && ((int)m_MeshLODs.size())>nLODIndex && nLODIndex >= 0)
		return m_MeshLODs[nLODIndex].m_pParaXMesh.get();
	else
		return nullptr;
}


bool ParaXEntity::IsLoaded()
{
	return TryGetModel()!=0;
}

void ParaXEntity::CreateMeshLODLevel( float fromDepth, const string& sFilename )
{
	MeshLOD meshLOD;
	meshLOD.m_fromDepthSquared = fromDepth*fromDepth;
	meshLOD.m_sMeshFileName = sFilename;
	
	m_MeshLODs.push_back(meshLOD);

	std::sort(m_MeshLODs.begin(), m_MeshLODs.end(), MeshLodSortLess());
}

void ParaXEntity::UpdateManualLodLevel( int index, const string& sFilename )
{
	if((int)m_MeshLODs.size()>index)
	{
		MeshLOD& lod = m_MeshLODs[index];
		if(lod.m_sMeshFileName != sFilename)
		{
			lod.m_sMeshFileName = sFilename;
			lod.m_pParaXMesh.reset();
		}
	}
}

int ParaXEntity::GetLodIndex( float fCameraObjectDist, float fScaling) const
{
	return GetLodIndexSquaredDepth(fCameraObjectDist * fCameraObjectDist, fScaling);
}

int ParaXEntity::GetLodIndexSquaredDepth( float squaredDepth, float fScaling) const
{
	if(m_MeshLODs.size()>1)
	{
		std::vector<MeshLOD>::const_iterator i, iend = m_MeshLODs.end();
		int index = 0;
		if (fScaling == 1.0f)
		{
			for (i = m_MeshLODs.begin(); i != iend; ++i, ++index)
			{
				if (i->m_fromDepthSquared > squaredDepth)
				{
					return index;
				}
			}
		}
		else
		{
			float fScalingSq = fScaling* fScaling;
			for (i = m_MeshLODs.begin(); i != iend; ++i, ++index)
			{
				if (i->m_fromDepthSquared * fScalingSq > squaredDepth)
				{
					return index;
				}
			}
		}
	}
	// If we fall all the way through, use the lowest lod
	return (int)(m_MeshLODs.size() - 1);
}

void ParaXEntity::RemoveLodLevels( void )
{
	if(m_MeshLODs.size()>1)
	{
		m_MeshLODs.resize(1);
	}
}

void ParaXEntity::Cleanup()
{
	m_MeshLODs.clear();
};


IAttributeFields* ParaXEntity::GetAttributeObject()
{
	return this;
}

HRESULT ParaXEntity::RendererRecreated()
{
	std::vector<MeshLOD>::iterator iCur, iEnd = m_MeshLODs.end();
	for (iCur = m_MeshLODs.begin(); iCur != iEnd; ++iCur)
	{
		MeshLOD& lod = (*iCur);
		if (lod.m_pParaXMesh)
		{
			lod.m_pParaXMesh->RendererRecreated();
		}
	}
	return S_OK;
}

bool ParaEngine::ParaXEntity::GetBoundingBox(Vector3* pMin, Vector3* pMax)
{
	CParaXModel* pMesh = GetModel();
	if (pMesh != NULL)
	{
		*pMin = pMesh->GetHeader().minExtent;
		*pMax = pMesh->GetHeader().maxExtent;
		return true;
	}
	return false;
}

int ParaEngine::ParaXEntity::GetChildAttributeObjectCount(int nColumnIndex /*= 0*/)
{
	return (int)m_MeshLODs.size();
}

IAttributeFields* ParaEngine::ParaXEntity::GetChildAttributeObject(int nRowIndex, int nColumnIndex /*= 0*/)
{
	return GetModel(nRowIndex);
}

int ParaEngine::ParaXEntity::GetPolyCount()
{
	CParaXModel* pModel = GetModel();
	return (pModel) ? pModel->GetPolyCount() : 0;
}

int ParaEngine::ParaXEntity::GetPhysicsCount()
{
	CParaXModel* pModel = GetModel();
	return (pModel) ? pModel->GetPhysicsCount() : 0;
}

const char* ParaEngine::ParaXEntity::DumpTextureUsage()
{
	CParaXModel* pModel = GetModel();
	return (pModel) ? pModel->DumpTextureUsage() : CGlobals::GetString().c_str();
}

int ParaEngine::ParaXEntity::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	// install parent fields if there are any. Please replace __super with your parent class name.
	AssetEntity::InstallFields(pClass, bOverride);

	pClass->AddField("FileName", FieldType_String, NULL, (void*)GetFileName_s, NULL, NULL, bOverride);
	pClass->AddField("TextureUsage", FieldType_String, NULL, (void*)DumpTextureUsage_s, NULL, NULL, bOverride);
	pClass->AddField("PolyCount", FieldType_Int, NULL, (void*)GetPolyCount_s, NULL, NULL, bOverride);
	pClass->AddField("PhysicsCount", FieldType_Int, NULL, (void*)GetPhysicsCount_s, NULL, NULL, bOverride);
	return S_OK;
}

void ParaEngine::ParaXEntity::SetMergeCoplanerBlockFace(bool val)
{
	m_bMergeCoplanerBlockFace = val;
}

bool ParaEngine::ParaXEntity::GetMergeCoplanerBlockFace()
{
	return m_bMergeCoplanerBlockFace;
}





```