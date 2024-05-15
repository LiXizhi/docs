```c++

#pragma once
#include "MeshEntity.h"
#include "ParaXEntity.h"
#include "TileObject.h"
namespace ParaEngine
{
	class CParaXModel;
	class BMaxModel;
	struct SceneState;
	struct IParaPhysicsActor;
	class CPhysicsWorld;

	/* render with color and material. */
	class BMaxObject : public CTileObject
	{
	public:
		BMaxObject(void);
		virtual ~BMaxObject(void);

		ATTRIBUTE_DEFINE_CLASS(BMaxObject);
		ATTRIBUTE_SUPPORT_CREATE_FACTORY(BMaxObject);

		/** this class should be implemented if one wants to add new attribute. This function is always called internally.*/
		virtual int InstallFields(CAttributeClass* pClass, bool bOverride);

		/** get the number of child objects (row count) in the given column. please note different columns can have different row count. */
		virtual int GetChildAttributeObjectCount(int nColumnIndex = 0);
		/** we support multi-dimensional child object. by default objects have only one column. */
		virtual int GetChildAttributeColumnCount();
		virtual IAttributeFields* GetChildAttributeObject(int nRowIndex, int nColumnIndex = 0);

		ATTRIBUTE_METHOD(BMaxObject, UpdateModel_s) { cls->UpdateModel(); return S_OK; }
	public:
		IAttributeFields* GetAnimInstanceFields();

		virtual HRESULT Draw(SceneState * sceneState);

		void ApplyBlockLighting(SceneState * sceneState);

		virtual AssetEntity* GetPrimaryAsset();
		virtual void SetAssetFileName(const std::string& sFilename);

		virtual Matrix4* GetAttachmentMatrix(Matrix4& pOut, int nAttachmentID = 0, int nRenderNumber = 0);

		virtual void GetLocalTransform(Matrix4* localTransform);
		virtual void UpdateGeometry();

		/** set the scale of the object. This function takes effects on both character object and mesh object.
		* @param s: scaling applied to all axis.1.0 means original size. */
		virtual void SetScaling(float s);

		/** get the scaling. */
		virtual float GetScaling();
		
		/** rotation related */
		virtual float GetPitch();
		virtual void SetPitch(float fValue);

		virtual float GetRoll();
		virtual void SetRoll(float fValue);

		/**
		* return the world matrix of the object for rendering
		* @param out: the output.
		* @param nRenderNumber: if it is bigger than current calculated render number, the value will be recalculated. If 0, it will not recalculate
		* @return: same as out. or NULL if not exists.
		*/
		virtual Matrix4* GetRenderMatrix(Matrix4& out, int nRenderNumber = 0);
		
		/** if the object may contain physics*/
		virtual bool CanHasPhysics();
		virtual void LoadPhysics();
		/** by default physics is lazy-load when player walk into its bounding box, setting this to false will always load the physics.
		* Please note, one must EnablePhysics(true) before this one takes effect.
		*/
		virtual void SetAlwaysLoadPhysics(bool bEnable);
		virtual void UnloadPhysics();
		virtual void SetPhysicsGroup(int nGroup);
		virtual int GetPhysicsGroup();
		virtual void EnablePhysics(bool bEnable);
		virtual bool IsPhysicsEnabled();
		virtual TextureEntity* GetReplaceableTexture(int ReplaceableTextureID)override;
		virtual bool  SetReplaceableTexture(int ReplaceableTextureID,TextureEntity* pTextureEntity)override;

		/** whether animation is enabled. by default this is true. During movie editing, we may disable animation, set animation frame explicitly by editor logics. */
		virtual void EnableAnim(bool bAnimated);
		virtual bool IsAnimEnabled();

		/** get the current local time in case it is animated in milli seconds frames. */
		virtual int GetTime();
		virtual void SetTime(int nTime);

		/** set the current animation frame number relative to the beginning of current animation.
		* @param nFrame: 0 means beginning. if nFrame is longer than the current animation length, it will wrap (modulate the length).
		*/
		virtual void SetAnimFrame(int nFrame);

		/** get the current animation frame number relative to the beginning of current animation.  */
		virtual int GetAnimFrame();

		/** get the number of physics actors. If physics is not loaded, the returned value is 0. */
		int GetStaticActorCount();
		
		/** update model according to current animation data and time*/
		bool UpdateModel(SceneState * sceneState = NULL);

		/** ignore selected state for bmaxobject
		virtual void OnSelect(int nGroupID)override{}
		virtual void OnDeSelect()override{}
		*/
	private:
		/** size scale */
		float	m_fScale;

		/** rotation parameters */
		float m_fPitch;
		float m_fRoll;

		AnimIndex m_CurrentAnim;
		ref_ptr<ParaXEntity>      m_pAnimatedMesh;

		/** all static physics actors in physics engine */ 
		vector<IParaPhysicsActor*> m_staticActors;

		// any bit wise combination of PHYSICS_METHOD
		DWORD m_dwPhysicsMethod;
		uint32 m_nPhysicsGroup;

		/** a value between [0,1). last block light. */
		float m_fLastBlockLight;
		/** a hash to detect if the containing block position of this biped changed. */
		DWORD m_dwLastBlockHash;

		/** current time for dynamic fields. */
		int m_curTime;
		/** whether to enable animation in asset file. */
		bool m_bEnableAnim;

		std::map<uint32, TextureEntity*> mReplaceTextures;
	};
}


//-----------------------------------------------------------------------------
// Class:	
// Authors:	Leio, LiXizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine Co.
// Date:	2015.5.19
// Desc: 
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BMaxObject.h"
#include "ParaWorldAsset.h"
#include "SceneState.h"
#include "EffectManager.h"
#include "BlockEngine/BlockCommon.h"
#include "BlockEngine/BlockWorldClient.h"
#include "BlockEngine/BlockModel.h"
#include "ParaXModel/ParaXModel.h"
#include "PhysicsWorld.h"
#include "ShapeOBB.h"
#include "ShapeAABB.h"
#include "IScene.h"
#include <vector>
#include "ParaXModel/ParaXModelExporter.h"
namespace ParaEngine
{
	BMaxObject::BMaxObject()
		:m_fScale(1.0f), m_fPitch(0.f), m_fRoll(0.f), m_fLastBlockLight(0.f), m_dwLastBlockHash(0), m_bEnableAnim(true), m_curTime(0),
		m_nPhysicsGroup(0), m_dwPhysicsMethod(PHYSICS_FORCE_NO_PHYSICS)
	{
		SetAttribute(OBJ_VOLUMN_FREESPACE);
	}

	BMaxObject::~BMaxObject()
	{
		UnloadPhysics();
	}

	int BMaxObject::GetChildAttributeObjectCount(int nColumnIndex /*= 0*/)
	{
		if (nColumnIndex == 0)
			return CBaseObject::GetChildAttributeObjectCount(nColumnIndex);
		else if (nColumnIndex == 1)
			// exposing primary asset and animation instance
			return 2;
		else
			return 0;
	}

	int BMaxObject::GetChildAttributeColumnCount()
	{
		return 2;
	}

	ParaEngine::IAttributeFields* BMaxObject::GetChildAttributeObject(int nRowIndex, int nColumnIndex /*= 0*/)
	{
		if (nColumnIndex == 0)
			return CBaseObject::GetChildAttributeObject(nRowIndex, nColumnIndex);
		else if (nColumnIndex == 1)
		{
			// exposing primary asset and animation instance
			if (nRowIndex == 0)
				return GetPrimaryAsset();
			else if (nRowIndex == 1)
				return GetAnimInstanceFields();
		}
		return NULL;
	}

	ParaEngine::IAttributeFields* BMaxObject::GetAnimInstanceFields()
	{
		return this;
	}

	float BMaxObject::GetScaling()
	{
		return m_fScale;
	}

	Matrix4* BMaxObject::GetRenderMatrix(Matrix4& mxWorld, int nRenderNumber /*= 0*/)
	{
		mxWorld.identity();

		// order of rotation: roll * pitch * yaw , where roll is applied first. 
		bool bIsIdentity = true;

		float fScaling = GetScaling();
		if (fScaling != 1.f)
		{
			Matrix4 matScale;
			ParaMatrixScaling((Matrix4*)&matScale, fScaling, fScaling, fScaling);
			mxWorld = (bIsIdentity) ? matScale : matScale.Multiply4x3(mxWorld);
			bIsIdentity = false;
		}

		float fYaw = GetYaw();
		if (fYaw != 0.f)
		{
			Matrix4 matYaw;
			ParaMatrixRotationY((Matrix4*)&matYaw, fYaw);
			mxWorld = (bIsIdentity) ? matYaw : matYaw.Multiply4x3(mxWorld);
			bIsIdentity = false;
		}

		if (GetPitch() != 0.f)
		{
			Matrix4 matPitch;
			ParaMatrixRotationX(&matPitch, GetPitch());
			mxWorld = (bIsIdentity) ? matPitch : matPitch.Multiply4x3(mxWorld);
			bIsIdentity = false;
		}

		if (GetRoll() != 0.f)
		{
			Matrix4 matRoll;
			ParaMatrixRotationZ(&matRoll, GetRoll());
			mxWorld = (bIsIdentity) ? matRoll : matRoll.Multiply4x3(mxWorld);
			bIsIdentity = false;
		}

		// world translation
		Vector3 vPos = GetRenderOffset();
		mxWorld._41 += vPos.x;
		mxWorld._42 += vPos.y;
		mxWorld._43 += vPos.z;

		return &mxWorld;
	}

	bool BMaxObject::CanHasPhysics()
	{
		return IsPhysicsEnabled();
	}

	void BMaxObject::SetScaling(float fScale)
	{
		if (m_fScale != fScale)
		{
			m_fScale = fScale;
			SetGeometryDirty(true);
		}
	}

	float BMaxObject::GetPitch()
	{
		return m_fPitch;
	};

	void BMaxObject::SetPitch(float fValue)
	{
		if (m_fPitch != fValue)
		{
			m_fPitch = fValue;
			SetGeometryDirty(true);
		}
	};

	float BMaxObject::GetRoll()
	{
		return m_fRoll;
	};

	void BMaxObject::SetRoll(float fValue)
	{
		if (m_fRoll != fValue)
		{
			m_fRoll = fValue;
			SetGeometryDirty(true);
		}
	};

	void BMaxObject::SetAssetFileName(const std::string& sFilename)
	{
		auto pNewModel = CGlobals::GetAssetManager()->LoadParaX("", sFilename);
		if (m_pAnimatedMesh != pNewModel)
		{
			UnloadPhysics();
			m_pAnimatedMesh = pNewModel;
			m_CurrentAnim.MakeInvalid();
			SetGeometryDirty(true);
		}
	}

	Matrix4* BMaxObject::GetAttachmentMatrix(Matrix4& matOut, int nAttachmentID /*= 0*/, int nRenderNumber /*= 0*/)
	{
		if (m_pAnimatedMesh && m_pAnimatedMesh->IsLoaded())
		{
			CParaXModel* pModel = m_pAnimatedMesh->GetModel();
			if (pModel)
			{
				Matrix4* pOut = &matOut;
				if (pModel->GetAttachmentMatrix(pOut, nAttachmentID, m_CurrentAnim, AnimIndex(), 0.f, m_CurrentAnim, AnimIndex(), 0.f))
				{
					Matrix4 matScale;
					float fScaling = GetScaling();
					if (fabs(fScaling - 1.0f) > FLT_TOLERANCE)
					{
						ParaMatrixScaling(&matScale, fScaling, fScaling, fScaling);
						(*pOut) = (*pOut)*matScale;
					}
					return pOut;
				}
			}
		}
		return NULL;
	}

	AssetEntity* BMaxObject::GetPrimaryAsset()
	{
		return m_pAnimatedMesh.get();
	}

	void BMaxObject::UpdateGeometry()
	{
		SetGeometryDirty(false);
		if (m_pAnimatedMesh && m_pAnimatedMesh->IsLoaded())
		{
			Vector3 vMin, vMax;
			if (m_pAnimatedMesh->GetBoundingBox(&vMin, &vMax))
			{
				Matrix4 mat;
				GetLocalTransform(&mat);
				CShapeOBB obb(CShapeBox(vMin, vMax), mat);
				CShapeBox minmaxBox;
				minmaxBox.Extend(obb);
				if (GetScaling()!= 1.0){
					minmaxBox.SetMinMax(minmaxBox.GetMin() * GetScaling(), minmaxBox.GetMax() * GetScaling());
				}
				SetAABB(&minmaxBox.GetMin(), &minmaxBox.GetMax());
			}

			UnloadPhysics();
			if (m_dwPhysicsMethod == 0)
				m_dwPhysicsMethod = PHYSICS_LAZY_LOAD;
			else if (IsPhysicsEnabled() && ((m_dwPhysicsMethod&PHYSICS_ALWAYS_LOAD)>0))
			{
				LoadPhysics();
			}
		}
	}

	void BMaxObject::ApplyBlockLighting(SceneState * sceneState)
	{
		BlockWorldClient* pBlockWorldClient = BlockWorldClient::GetInstance();
		if (pBlockWorldClient && pBlockWorldClient->IsInBlockWorld())
		{
			uint8_t brightness[2];
			Uint16x3 blockId_ws(0, 0, 0);
			Vector3 vPos = GetPosition();
			BlockCommon::ConvertToBlockIndex(vPos.x, vPos.y + 0.1f, vPos.z, blockId_ws.x, blockId_ws.y, blockId_ws.z);
			float fLightness;

			pBlockWorldClient->GetBlockMeshBrightness(blockId_ws, brightness);
			// block light
			float fBlockLightness = Math::Max(pBlockWorldClient->GetLightBrightnessFloat(brightness[0]), 0.1f);
			sceneState->GetCurrentLightStrength().y = fBlockLightness;
			// sun light
			fLightness = Math::Max(pBlockWorldClient->GetLightBrightnessFloat(brightness[1]), 0.1f);
			sceneState->GetCurrentLightStrength().x = fLightness;
			fLightness *= pBlockWorldClient->GetSunIntensity();
			fLightness = Math::Max(fLightness, fBlockLightness);

			if (!sceneState->IsDeferredShading())
			{
				sceneState->GetLocalMaterial().Ambient = (LinearColor(fLightness*0.7f, fLightness*0.7f, fLightness*0.7f, 1.f));
				sceneState->GetLocalMaterial().Diffuse = (LinearColor(fLightness*0.4f, fLightness*0.4f, fLightness*0.4f, 1.f));
			}
			else
			{
				sceneState->GetLocalMaterial().Diffuse = LinearColor::White;
			}

			sceneState->EnableLocalMaterial(true);
		}
	}

	void BMaxObject::GetLocalTransform(Matrix4* localTransform)
	{
		if (localTransform)
		{
			float yaw = GetFacing();
			float pitch = GetPitch();
			float roll = GetRoll();

			Matrix4 transform = Matrix4::IDENTITY;
			Matrix4 rot;

			if (yaw != 0)
			{
				ParaMatrixRotationY(&rot, yaw);
				transform = rot.Multiply4x3(transform);
			}
			if (pitch != 0)
			{
				ParaMatrixRotationX(&rot, pitch);
				transform = rot.Multiply4x3(transform);
			}
			if (roll != 0)
			{
				ParaMatrixRotationZ(&rot, roll);
				transform = rot.Multiply4x3(transform);
			}

			*localTransform = transform;
		}
	}

	bool BMaxObject::UpdateModel(SceneState * sceneState /*= NULL*/)
	{
		if (!m_pAnimatedMesh)
			return false;
		int nIndex = (sceneState && IsLODEnabled()) ? m_pAnimatedMesh->GetLodIndex(sceneState->GetCameraToCurObjectDistance()/*, GetScaling()*/) : 0;
		CParaXModel* pModel = m_pAnimatedMesh->GetModel(nIndex);
		
		if (pModel == NULL)
			return false;
		// just a single standing animation is supported now and looped. 
		if (!m_CurrentAnim.IsValid())
			m_CurrentAnim = pModel->GetAnimIndexByID(0);
		if (m_CurrentAnim.IsValid() && IsAnimEnabled())
		{
			int nAnimLength = std::max(1, m_CurrentAnim.nEndFrame - m_CurrentAnim.nStartFrame);
			int nToDoFrame = (m_CurrentAnim.nCurrentFrame + (int)(sceneState->dTimeDelta * 1000)) % nAnimLength;
			m_CurrentAnim.nCurrentFrame = nToDoFrame;
		}
		pModel->m_CurrentAnim = m_CurrentAnim;
		pModel->m_NextAnim.nIndex = 0;
		pModel->m_BlendingAnim.MakeInvalid();
		pModel->blendingFactor = 0;
		pModel->animate(sceneState, NULL, GetAnimInstanceFields());
		return true;
	}

	HRESULT BMaxObject::Draw(SceneState * sceneState)
	{
		if (!m_pAnimatedMesh)
			return E_FAIL;
		if (GetPrimaryTechniqueHandle() < 0)
		{
			// try loading the asset if it has not been done before. 
			m_pAnimatedMesh->LoadAsset();
			if (m_pAnimatedMesh->IsLoaded())
			{
				SetPrimaryTechniqueHandle(m_pAnimatedMesh->GetPrimaryTechniqueHandle());
				UpdateGeometry();
			}
			return E_FAIL;
		}

		if (!CGlobals::GetEffectManager()->IsCurrentEffectValid())
		{
			return E_FAIL;
		}
		sceneState->SetCurrentSceneObject(this);

		int nIndex = (sceneState && sceneState->IsLODEnabled()) ?
			m_pAnimatedMesh->GetLodIndex(sceneState->GetCameraToCurObjectDistance()/*, GetScaling()*/) : 0;
		CParaXModel* pModel = m_pAnimatedMesh->GetModel(nIndex);
		if (pModel == NULL)
			return E_FAIL;
		
		int nRestoreSpecialTextures = -1;
		for (auto const & tex : mReplaceTextures)
		{
			if(pModel->specialTextures[tex.first] >= 0)
				pModel->replaceTextures[pModel->specialTextures[tex.first]] = tex.second;
			else
			{
				// if there is only one texture, we will force replace it even there is no special replaceable id redefined.
				if (pModel->GetObjectNum().nTextures <= 1 && nRestoreSpecialTextures<0)
				{
					nRestoreSpecialTextures = tex.first;
					pModel->specialTextures[tex.first] = tex.first;
					pModel->replaceTextures[pModel->specialTextures[tex.first]] = tex.second;
					break;
				}
			}
		}

		sceneState->SetCurrentSceneObject(this);
		SetFrameNumber(sceneState->m_nRenderCount);
		// get world transform matrix
		Matrix4 mxWorld;
		GetRenderMatrix(mxWorld);


		RenderDevicePtr pd3dDevice = sceneState->m_pd3dDevice;
		EffectManager* pEffectManager = CGlobals::GetEffectManager();
		pEffectManager->applyObjectLocalLighting(this);

		CEffectFile* pEffectFile = pEffectManager->GetCurrentEffectFile();
		CGlobals::GetWorldMatrixStack().push(mxWorld);

		// ApplyBlockLighting(sceneState);

		
		CApplyObjectLevelParamBlock p(GetEffectParamBlock());

		if (pEffectFile == 0)
		{
			// TODO: Fixed Function. 
		}
		else
		{
			bool bUsePointTextureFilter = false;

			// apply block space lighting for object whose size is comparable to a single block size
			if (CheckAttribute(MESH_USE_LIGHT) && !(sceneState->IsShadowPass()))
			{
				BlockWorldClient* pBlockWorldClient = BlockWorldClient::GetInstance();
				if (pBlockWorldClient && pBlockWorldClient->IsInBlockWorld())
				{
					Vector3 vPos = GetPosition();
					vPos.y += 0.1f;
					Uint16x3 blockId_ws(0, 0, 0);
					BlockCommon::ConvertToBlockIndex(vPos.x, vPos.y, vPos.z, blockId_ws.x, blockId_ws.y, blockId_ws.z);
					DWORD dwPositionHash = blockId_ws.GetHashCode();
					uint8_t brightness[2];
					pBlockWorldClient->GetBlockMeshBrightness(blockId_ws, brightness, 2);
					// block light
					float fBlockLightness = Math::Max(pBlockWorldClient->GetLightBrightnessLinearFloat(brightness[0]), 0.1f);
					sceneState->GetCurrentLightStrength().y = fBlockLightness;
					// sun light
					float fSunLightness = Math::Max(pBlockWorldClient->GetLightBrightnessLinearFloat(brightness[1]), 0.1f);
					sceneState->GetCurrentLightStrength().x = fSunLightness;

					float fLightness = Math::Max(fBlockLightness, fSunLightness*pBlockWorldClient->GetSunIntensity());
					if (m_fLastBlockLight != fLightness)
					{
						float fMaxStep = (float)(sceneState->dTimeDelta*0.5f);
						if (dwPositionHash == m_dwLastBlockHash || m_dwLastBlockHash == 0)
							m_fLastBlockLight = fLightness;
						else
							Math::SmoothMoveFloat1(m_fLastBlockLight, fLightness, fMaxStep);

						fLightness = m_fLastBlockLight;
					}
					else
					{
						m_dwLastBlockHash = dwPositionHash;
					}
					if (!sceneState->IsDeferredShading())
					{
						sceneState->GetLocalMaterial().Ambient = (LinearColor(fLightness*0.7f, fLightness*0.7f, fLightness*0.7f, 1.f));
						sceneState->GetLocalMaterial().Diffuse = (LinearColor(fLightness*0.4f, fLightness*0.4f, fLightness*0.4f, 1.f));
					}
					else
					{
						sceneState->GetLocalMaterial().Diffuse = LinearColor::White;
					}

					sceneState->EnableLocalMaterial(true);
					bUsePointTextureFilter = bUsePointTextureFilter || pBlockWorldClient->GetUsePointTextureFiltering();
				}
			}

			if (bUsePointTextureFilter)
			{
				pEffectManager->SetSamplerState(0, D3DSAMP_MINFILTER, D3DTEXF_POINT);
				pEffectManager->SetSamplerState(0, D3DSAMP_MAGFILTER, D3DTEXF_POINT);
			}
			else
			{
				pEffectManager->SetSamplerState(0, D3DSAMP_MINFILTER, pEffectManager->GetDefaultSamplerState(0, D3DSAMP_MINFILTER));
				pEffectManager->SetSamplerState(0, D3DSAMP_MAGFILTER, pEffectManager->GetDefaultSamplerState(0, D3DSAMP_MAGFILTER));
			}

			// just a single standing animation is supported now and looped. 
			UpdateModel(sceneState);
			pModel->draw(sceneState, p.GetParamsBlock()); 
		}

		if (nRestoreSpecialTextures >= 0)
		{
			pModel->specialTextures[nRestoreSpecialTextures] = -1;
			pModel->replaceTextures[nRestoreSpecialTextures] = nullptr;
		}

		CGlobals::GetWorldMatrixStack().pop();
		return S_OK;
	}

	void BMaxObject::LoadPhysics()
	{
		if (m_dwPhysicsMethod > 0 && IsPhysicsEnabled() && (GetStaticActorCount() == 0))
		{
			if (m_pAnimatedMesh && m_pAnimatedMesh->IsLoaded())
			{
				CParaXModel* ppMesh = m_pAnimatedMesh->GetModel();
				if (ppMesh == 0 || ppMesh->GetHeader().maxExtent.x <= 0.f)
				{
					EnablePhysics(false); // disable physics forever, if failed loading physics data
					return;
				}
				// get world transform matrix
				Matrix4 mxWorld;
				GetWorldTransform(mxWorld);
				IParaPhysicsActor* pActor = CGlobals::GetPhysicsWorld()->CreateStaticMesh(m_pAnimatedMesh.get(), mxWorld, m_nPhysicsGroup, &m_staticActors, this);
				if (m_staticActors.empty())
				{
					// disable physics forever, if no physics actors are loaded. 
					EnablePhysics(false);
				}
			}
		}
	}

	void BMaxObject::SetAlwaysLoadPhysics(bool bEnable)
	{
		if (bEnable)
		{
			m_dwPhysicsMethod |= PHYSICS_ALWAYS_LOAD;
		}
		else
		{
			m_dwPhysicsMethod &= (~PHYSICS_ALWAYS_LOAD);
		}
	}

	void BMaxObject::UnloadPhysics()
	{
		int nSize = (int)m_staticActors.size();
		if (nSize > 0)
		{
			for (int i = 0; i < nSize; ++i)
			{
				CGlobals::GetPhysicsWorld()->ReleaseActor(m_staticActors[i]);
			}
			m_staticActors.clear();
		}
	}

	void BMaxObject::SetPhysicsGroup(int nGroup)
	{
		PE_ASSERT(0 <= nGroup && nGroup < 32);
		if (m_nPhysicsGroup != nGroup)
		{
			m_nPhysicsGroup = nGroup;
			UnloadPhysics();
		}
	}

	int BMaxObject::GetPhysicsGroup()
	{
		return m_nPhysicsGroup;
	}

	void BMaxObject::EnablePhysics(bool bEnable)
	{
		if (!bEnable){
			UnloadPhysics();
			m_dwPhysicsMethod |= PHYSICS_FORCE_NO_PHYSICS;
		}
		else
		{
			m_dwPhysicsMethod &= (~PHYSICS_FORCE_NO_PHYSICS);
			if ((m_dwPhysicsMethod&PHYSICS_ALWAYS_LOAD)>0)
				LoadPhysics();
		}
	}

	bool BMaxObject::IsPhysicsEnabled()
	{
		return !((m_dwPhysicsMethod & PHYSICS_FORCE_NO_PHYSICS)>0);
	}

	void BMaxObject::EnableAnim(bool bAnimated)
	{
		m_bEnableAnim = bAnimated;
	}

	bool BMaxObject::IsAnimEnabled()
	{
		return m_bEnableAnim;
	}

	int BMaxObject::GetTime()
	{
		return m_curTime;
	}

	void BMaxObject::SetTime(int nTime)
	{
		m_curTime = nTime;
	}

	void BMaxObject::SetAnimFrame(int nFrame)
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
			}
		}
	}

	int BMaxObject::GetAnimFrame()
	{
		return m_CurrentAnim.IsValid() ? (m_CurrentAnim.nCurrentFrame - m_CurrentAnim.nStartFrame) : 0;
	}

	TextureEntity* BMaxObject::GetReplaceableTexture(int ReplaceableTextureID)
	{
		auto iter=mReplaceTextures.find(ReplaceableTextureID);
		return (mReplaceTextures.end()==iter)?nullptr:iter->second;
	}

	bool BMaxObject::SetReplaceableTexture(int ReplaceableTextureID,TextureEntity* pTextureEntity)
	{
		mReplaceTextures[ReplaceableTextureID]=pTextureEntity;
		return true;
	}

	int BMaxObject::GetStaticActorCount()
	{
		return (int)m_staticActors.size();
	}

	int BMaxObject::InstallFields(CAttributeClass* pClass, bool bOverride)
	{
		CTileObject::InstallFields(pClass, bOverride);
		pClass->AddField("UpdateModel", FieldType_void, (void*)UpdateModel_s, (void*)0, NULL, "", bOverride);
		return S_OK;
	}
}

#pragma once
#include "NPLHelper.h"
#include "NPLTable.h"
#include "ParaXModel/ParaXModel.h"

namespace ParaEngine
{
	class Bone;
	class BMaxParser;

	//typedef int BoneIndex;
	typedef string BoneName;
	typedef string BoneFlag;

	struct BoneRotState
	{
		BoneRotState(float time,float angle){
			this->time = time;
			this->angle = angle;
		}
		//rot state
		float angle;
		float time;
	};

	//struct BoneTransState
	//{
	//	BoneTransState(float time, float angle){
	//		this->time = time;
	//		this->angle = angle;
	//	}
	//	//trans state
	//	float angle;
	//	float time;
	//};

	//struct BoneScaleState
	//{
	//	BoneScaleState(float time, float angle){
	//		this->time = time;
	//		this->angle = angle;
	//	}
	//	//scale state
	//	float angle;
	//	float time;
	//};

	struct BoneState
	{
	public:
		BoneState(){}
		//rot state
		vector<BoneRotState> boneRot;
		//vector<BoneTransState> boneTrans;
		//vector<BoneScaleState> boneScale;
	};

	struct BoneInfo
	{
		BoneInfo(){}
		// the bone is "leg","arm","wing","wheel"
		string name;
		// the flag of bone.
		string flag;
		//the bone position,"right","left","center"
		string position;
		int index;
		float bx;
		float by;
		float bz;
	};

	/** BMax Animation generator
	1. x+ is the front, z+ right, z- left
	2. z axis's bone blocks should face inward
	3. x axis's bone block should face x+ direction.
	*/
	class BMaxAnimGenerator
	{
	public:
		BMaxAnimGenerator();
		BMaxAnimGenerator(BMaxParser *pParser);
		~BMaxAnimGenerator();
	public:
		/**
		* @param boneName: output bone name
		*/
		void ParseParameters(NPL::NPLObjectProxy& boneInfo, int boneIndex, string& boneName);
		void FillAnimations();
		ModelAnimation* FillWalkAnimation();
		void FillAnimation(int nAnimID, int nStartTime, int nEndTime, float fMoveSpeed, bool bMoveForward);
		void CountBonePosition(string boneName, BoneFlag boneFlag, const std::vector<BoneInfo>& boneInfos);
		void UpdateBonePositionInfo();
		
	private:

		void InitBoneState();
		bool CompareBonePosition(BoneInfo firstBone,BoneInfo secondBone);
		bool GetBonePosition(int boneIndex);

		void AddBoneState(const string& boneName,const string& boneFlag,int animID,BoneState boneState);
		void AddWheelBoneState();
		void AddWalkBoneState();
		void AddFlyBoneState();

		//Vector3 GetRotAxis(string boneName, string boneFlag, int animID, Vector3 boneAxis);
		float GetBoneRotSign(const string& boneName, const string& boneFlag, const string& bonePosition, int animID, float boneAxisZ);

	private:
		static std::map<pair<BoneName, BoneFlag>, std::map<int, BoneState>> s_boneStates;
		static bool s_bInitedBoneState;

		BMaxParser *m_pParser;
		
		std::map<pair<BoneName, BoneFlag>, std::vector<BoneInfo>> m_boneInfoMap;
		std::map<pair<BoneName, BoneFlag>, std::vector<int>> m_bonePositionInfoMap;

		bool m_bHasSetMaxMinPosition;
		Vector3 m_vRightBonePosition;
		Vector3 m_vLeftBonePosition;
	};
}

//-----------------------------------------------------------------------------
// Class:Block max animation generator
// Authors:	LiXizhi,LiPeng
// Emails:	lixizhi@yeah.net
// Date:	2015.12.4
// Desc: 
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BMaxParser.h"
#include "ParaXModel/AnimTable.h"
#include "ParaXModel/ParaXBone.h"
#include "BMaxAnimGenerator.h"

namespace ParaEngine
{
	bool BMaxAnimGenerator::s_bInitedBoneState = false;
	std::map<pair<BoneName, BoneFlag>, std::map<int, BoneState>> BMaxAnimGenerator::s_boneStates = std::map<pair<BoneName, BoneFlag>, std::map<int, BoneState>>();

	BMaxAnimGenerator::BMaxAnimGenerator() : 
		m_pParser(NULL), m_bHasSetMaxMinPosition(false),
		m_vLeftBonePosition(0, 0, 0), m_vRightBonePosition(0,0,0) 
	{
		InitBoneState();
	}

	BMaxAnimGenerator::BMaxAnimGenerator(BMaxParser *pParser) : 
		m_pParser(pParser), m_bHasSetMaxMinPosition(false), 
		m_vLeftBonePosition(0, 0, 0), m_vRightBonePosition(0, 0, 0)
	{
		InitBoneState();
	}

	BMaxAnimGenerator::~BMaxAnimGenerator()
	{

	}

	void BMaxAnimGenerator::AddBoneState(const string& boneName, const string& boneFlag, int animID, BoneState boneState)
	{
		auto iter = s_boneStates.find(pair<string, string>(boneName, boneFlag));
		if (iter != s_boneStates.end())
		{
			auto &boneStates = iter->second;
			auto boneStatesIter = boneStates.find(animID);
			if (boneStatesIter != boneStates.end())
			{
				boneStatesIter->second = boneState;
			}
			else
			{
				boneStates.insert(make_pair(animID, boneState));
			}
		}
		else
		{
			std::map<int, BoneState> boneStates;
			boneStates.insert(make_pair(animID, boneState));

			s_boneStates.insert(make_pair(pair<string, string>(boneName, boneFlag), boneStates));
		}
	}

	void BMaxAnimGenerator::AddWheelBoneState()
	{
		string boneName("wheel");
		string boneFlag("default");
		int animID = ANIM_WALK;
		BoneState boneState;
		boneState.boneRot.push_back(BoneRotState(0, 0));
		boneState.boneRot.push_back(BoneRotState(0.5f, 3.14f));
		boneState.boneRot.push_back(BoneRotState(1.0f, 6.28f));

		AddBoneState(boneName, boneFlag, animID, boneState);
	}

	void BMaxAnimGenerator::AddWalkBoneState()
	{
		string boneName("leg");
		string boneFlag("biped");
		int animID = int(ANIM_WALK);

		BoneState legBoneState;
		legBoneState.boneRot.push_back(BoneRotState(0, 0.942f));
		legBoneState.boneRot.push_back(BoneRotState(0.5f, -0.942f));
		legBoneState.boneRot.push_back(BoneRotState(1.0f, 0.942f));

		AddBoneState(boneName, boneFlag, animID, legBoneState);

		AddBoneState(boneName, "multiple", animID, legBoneState);

		BoneState armBoneState;
		armBoneState.boneRot.push_back(BoneRotState(0, -0.942f));
		armBoneState.boneRot.push_back(BoneRotState(0.5f, 0.942f));
		armBoneState.boneRot.push_back(BoneRotState(1.0f, -0.942f));

		AddBoneState("arm", "default", animID, armBoneState);
	}

	void BMaxAnimGenerator::AddFlyBoneState()
	{
		string boneName("wing");
		string boneFlag("default");
		int animID = ANIM_WALK;

		BoneState boneState;
		boneState.boneRot.push_back(BoneRotState(0, 0.942f));
		boneState.boneRot.push_back(BoneRotState(0.5f, -0.942f));
		boneState.boneRot.push_back(BoneRotState(1.0f, 0.942f));

		AddBoneState(boneName, boneFlag, animID, boneState);
	}

	void BMaxAnimGenerator::InitBoneState()
	{
		if (s_bInitedBoneState)
			return;
		s_bInitedBoneState = true;
		AddWheelBoneState();
		AddWalkBoneState();
		AddFlyBoneState();
	}

	void BMaxAnimGenerator::ParseParameters(NPL::NPLObjectProxy& boneInfo, int boneIndex, string& boneName)
	{
		if (boneInfo[1].GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
		{
			NPL::NPLObjectProxy& cmd = boneInfo[1];

			float bx, by, bz;
			if (boneInfo["attr"].GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
			{
				bx = (float)((double)boneInfo["attr"]["bx"]);
				by = (float)((double)boneInfo["attr"]["by"]);
				bz = (float)((double)boneInfo["attr"]["bz"]);

				Vector3 position(bx, by, bz);
				if (!m_bHasSetMaxMinPosition)
				{
					m_bHasSetMaxMinPosition = true;
					m_vRightBonePosition = position;
					m_vLeftBonePosition = position;
				}
				else
				{
					if (m_vRightBonePosition.z > bz)
					{
						m_vRightBonePosition = position;
					}
					if (m_vLeftBonePosition.z < bz)
					{
						m_vLeftBonePosition = position;
					}
				}
			}

			BoneInfo boneInfo;
			if (cmd[1].GetType() == NPL::NPLObjectBase::NPLObjectType_String)
			{
				const std::string& cmdcontent = cmd[1];
				string _boneName = cmdcontent;

				string boneFlag = "default";

				string::size_type addFlag = cmdcontent.find_first_of("-");
				if (addFlag != string::npos)
				{
					_boneName = string(cmdcontent, 0, addFlag);
					string _boneFlag(cmdcontent, addFlag + 1);
					boneFlag = _boneFlag;
				}

				addFlag = cmdcontent.find_first_of("|");
				if (addFlag != string::npos)
				{
					_boneName = string(cmdcontent, 0, addFlag);
					string boneAddInfo(cmdcontent, addFlag + 1);
					NPL::NPLObjectProxy addMsg = NPL::NPLHelper::StringToNPLTable(boneAddInfo.c_str());

					for (NPL::NPLTable::IndexIterator_Type animIter = addMsg.index_begin(); animIter != addMsg.index_end(); ++animIter)
					{
						NPL::NPLObjectProxy& anim = animIter->second;
						int animID = (int)((double)anim[1]);
						NPL::NPLObjectProxy& rotMsg = anim[2];

						BoneState boneState;
						for (NPL::NPLTable::IndexIterator_Type rotIter = rotMsg.index_begin(); rotIter != rotMsg.index_end(); ++rotIter)
						{
							NPL::NPLObjectProxy& rotState = rotIter->second;
							boneState.boneRot.push_back(BoneRotState((float)((double)rotState[1]), (float)((double)rotState[2])));
						}

						//string _boneFlag("default");
						AddBoneState(_boneName, boneFlag, animID, boneState);
					}
				}

				if (_boneName.empty())
				{
					return;
				}
				boneName += _boneName;

				boneInfo.name = _boneName;
				boneInfo.flag = boneFlag;
				boneInfo.index = boneIndex;

				boneInfo.position = "";

				boneInfo.bx = bx;
				boneInfo.by = by;
				boneInfo.bz = bz;

				auto iter = m_boneInfoMap.find(pair<BoneName, BoneFlag>(_boneName, boneFlag));
				if (iter == m_boneInfoMap.end())
				{
					vector<BoneInfo> boneInfos;
					boneInfos.push_back(boneInfo);
					m_boneInfoMap.insert(make_pair(pair<BoneName, BoneFlag>(_boneName, boneFlag), boneInfos));
					/*vector<int> bonePositionInfo;
					bonePositionInfo.push_back(boneIndex);
					m_bonePositionInfoMap.insert(make_pair(pair<string, string>(_boneName, boneInfo.flag), bonePositionInfo));*/
				}
				else
				{
					vector<BoneInfo> &boneInfos = iter->second;
					boneInfos.push_back(boneInfo);
					//CountBonePosition(_boneName,boneFlag,boneInfos);
				}

			}
		}
	}

	void BMaxAnimGenerator::UpdateBonePositionInfo()
	{
		Vector3 centerBonePosition;
		if (m_vRightBonePosition == m_vLeftBonePosition)
		{
			return;
		}
		else
		{
			centerBonePosition.x = (m_vLeftBonePosition.x - m_vRightBonePosition.x) / 2 + m_vRightBonePosition.x;
			centerBonePosition.y = (m_vLeftBonePosition.y - m_vRightBonePosition.y) / 2 + m_vRightBonePosition.y;
			centerBonePosition.z = (m_vLeftBonePosition.z - m_vRightBonePosition.z) / 2 + m_vRightBonePosition.z;
		}
		for (auto &boneInfosIter : m_boneInfoMap)
		{
			auto &boneInfos = boneInfosIter.second;
			for (auto &boneInfo : boneInfos)
			{
				if (boneInfo.bz > centerBonePosition.z)
				{
					boneInfo.position = "left";
				}
				else if (boneInfo.bz == centerBonePosition.z)
				{
					boneInfo.position = "center";
				}
				else if (boneInfo.bz < centerBonePosition.z)
				{
					boneInfo.position = "right";
				}
			}

		}
	}

	void BMaxAnimGenerator::FillAnimations()
	{

		UpdateBonePositionInfo();
		//m_bHasAnimation = true;

		// static animation 0
		ModelAnimation anim;
		memset(&anim, 0, sizeof(ModelAnimation));
		anim.timeStart = 0;
		anim.timeEnd = 0;
		anim.animID = 0;
		m_pParser->AddAnimation(anim);

		FillAnimation(ANIM_WALK, 4000, 5000, 4.0f, true);
		FillAnimation(ANIM_FLY, 4000, 5000, 4.0f, true);


		// walk animations 
		/*AutoAddWalkAnimation(ANIM_WALK, 4000, 5000, 4.0f, true);
		AutoAddWalkAnimation(ANIM_WALKBACKWARDS, 13000, 14000, 4.0f, false);*/
	}


	bool BMaxAnimGenerator::CompareBonePosition(BoneInfo firstBone, BoneInfo secondBone)
	{
		if (firstBone.by > secondBone.by)
		{
			return true;
		}

		if (firstBone.by == secondBone.by)
		{
			if (firstBone.bx > secondBone.bx)
			{
				return true;
			}

			if (firstBone.bx == secondBone.bx && firstBone.bz > secondBone.bz)
			{
				return true;
			}
		}
		return false;
	}

	void BMaxAnimGenerator::CountBonePosition(string boneName, BoneFlag boneFlag, const std::vector<BoneInfo>& boneInfos)
	{
		BoneInfo newBoneInfo = boneInfos[boneInfos.size() - 1];
		auto bonePositionInfoIter = m_bonePositionInfoMap.find(pair<BoneName, BoneFlag>(boneName, boneFlag));
		if (bonePositionInfoIter != m_bonePositionInfoMap.end())
		{
			std::vector<int> &bonePositionInfo = bonePositionInfoIter->second;
			for (auto boneInfoIter : boneInfos)
			{
				BoneInfo &boneInfo = boneInfoIter;
				if (CompareBonePosition(newBoneInfo, boneInfo))
				{
					for (auto bonePositionIter = bonePositionInfo.begin(); bonePositionIter != bonePositionInfo.end(); bonePositionIter++)
					{
						int &BoneIndex = *bonePositionIter;
						if (BoneIndex == boneInfo.index)
						{
							bonePositionInfo.insert(bonePositionIter, newBoneInfo.index);
							break;
						}
					}
				}
			}
		}
		else
			return;
	}

	float BMaxAnimGenerator::GetBoneRotSign(const string& boneName, const string& boneFlag, const string& bonePosition, int animID, float boneAxisZ)
	{
		if (boneName == "wheel")
		{
			return boneAxisZ > 0 ? 1.f : -1.f;
		}
		if (boneName == "wing")
		{
			if (bonePosition == "left")
			{
				return -1.f;
			}
		}
		return 1.f;
	}

	void BMaxAnimGenerator::FillAnimation(int nAnimID, int nStartTime, int nEndTime, float fMoveSpeed, bool bMoveForward)
	{
		ModelAnimation anim;
		anim.timeStart = nStartTime;
		anim.timeEnd = nEndTime;
		anim.animID = nAnimID;
		anim.moveSpeed = fMoveSpeed;
		int animIndex = m_pParser->GetAnimationsCount();
		int nAnimLength = anim.timeEnd - anim.timeStart;

		for (auto boneInfos : m_boneInfoMap)
		{
			string boneName = boneInfos.first.first;
			string boneFlag = boneInfos.first.second;
			auto boneStatesIter = s_boneStates.find(pair<BoneName, BoneFlag>(boneName, boneFlag));
			if (boneStatesIter != s_boneStates.end())
			{
				auto boneStates = boneStatesIter->second;
				auto boneState = boneStates.find(nAnimID);
				if (boneState != boneStates.end())
				{
					for (auto boneInfo : boneInfos.second)
					{
						auto &bone = m_pParser->m_bones[boneInfo.index];
						Bone* pBone = bone->GetBone();

						Vector3 vAxis = bone->GetAxis();
						Quaternion q;
						pBone->rot.used = true;
						int nFirstRotSize = (int)pBone->rot.times.size();

						float fRotSign = GetBoneRotSign(boneName, boneFlag, boneInfo.position, nAnimID, vAxis.z);
						/*float fRotSign = (vAxis.z > 0) ? 1.f : -1.f;
						if (!bMoveForward)
						fRotSign = -fRotSign;*/

						//Vector3 rotAxis = GetRotAxis(boneName, boneFlag, nAnimID, vAxis);

						BoneState &_boneState = boneState->second;

						for (auto rotState : _boneState.boneRot)
						{
							q.FromAngleAxis(Radian(rotState.angle * fRotSign), vAxis);
							pBone->rot.times.push_back(anim.timeStart + (int)(nAnimLength * rotState.time));
							pBone->rot.data.push_back(q);
						}


						pBone->rot.ranges.resize(animIndex + 1, AnimRange(0, 0));
						pBone->rot.ranges[animIndex] = AnimRange(nFirstRotSize, max(nFirstRotSize, (int)pBone->rot.times.size() - 1));
					}
				}
			}
		}
		m_pParser->m_anims.push_back(anim);
	}
}

#pragma once

#include "BlockEngine/BlockCoordinate.h"
#include "BlockEngine/BlockDirection.h"

namespace ParaEngine
{
	class Bone;
	class BMaxParser;
	class BlockModel;
	struct BMaxFrameNode;

	/** base class for a block in bmax model */
	struct BMaxNode : public CRefCounted
	{
	public:
		BMaxNode(BMaxParser* pParser, int16 x_, int16 y_, int16 z_, int32 template_id_, int32 block_data_);
		virtual ~BMaxNode();

		enum FaceStatus
		{
			faceInvisible = 0,
			faceVisibleNotSign,
			faceVisibleSigned
		};

	public:
		inline uint64 GetIndex()
		{
			return (uint64)x + ((uint64)z << 16) + ((uint64)y << 32);
		}
		virtual DWORD GetColor();
		BlockModel *GetBlockModel();
		/** set block model weak reference. */
		void SetBlockModel(BlockModel* pModel);
		virtual void SetColor(DWORD val);
		/** get the bone node interface if it is*/
		virtual BMaxFrameNode* ToBoneNode();
		/** if there are any bone associated with this node at the moment. */
		bool HasBoneWeight();
		/** return the index of first bone, return -1 if no bone is binded to this node*/
		virtual int GetBoneIndex();
		virtual void SetBoneIndex(int nIndex);

		/** get neighbor block by side id
		* @param nSize:
		*/
		BMaxNode* GetNeighbour(BlockDirection::Side nSize);
		BMaxNode* GetNeighbourByOffset(Vector3 offset);
		virtual bool isSolid();

		/** 
		* @param tessellatedModel: generate block model vertices
		* @return vertices count
		*/
		virtual int TessellateBlock(BlockModel* tessellatedModel);

		void QueryNeighborBlockData(BMaxNode** pBlockData, int nFrom /*= 0*/, int nTo /*= 26*/);

		uint32 CalculateCubeAO(BMaxNode** neighborBlocks);

		int32_t GetAvgVertexLight(int32_t v1, int32_t v2, int32_t v3, int32_t v4);

		void SetFaceVisible(int nIndex);
		void SetFaceUsed(int nIndex);
		bool IsFaceNotUse(int nIndex);
	public:
		int16 x;
		int16 y;
		int16 z;
		int32 template_id;
		int32 block_data;
		int m_nBoneIndex;
	protected:
		BMaxParser* m_pParser;
		DWORD m_color;
		/* weak reference to block model*/
		BlockModel * m_pBlockModel;
		FaceStatus m_facesStatus[6];
	};
	typedef ref_ptr<BMaxNode> BMaxNodePtr;
}

//-----------------------------------------------------------------------------
// Class:Block max frame node
// Authors:	LiXizhi
// Emails:	lixizhi@yeah.net
// Date:	2015.9.26
// Desc: 
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "ParaXModel/ParaXModel.h"
#include "ParaXModel/ParaXBone.h"
#include "BlockEngine/BlockCommon.h"
#include "BlockEngine/BlockDirection.h"
#include "BlockEngine/BlockWorldClient.h"
#include "BMaxParser.h"
#include "BMaxNode.h"
using namespace ParaEngine;

ParaEngine::BMaxNode::BMaxNode(BMaxParser* pParser, int16 x_, int16 y_, int16 z_, int32 template_id_, int32 block_data_) :
m_pParser(pParser), x(x_), y(y_), z(z_), template_id(template_id_), block_data(block_data_), m_color(0), m_nBoneIndex(-1), m_pBlockModel(nullptr)
{
	memset(m_facesStatus, faceInvisible, sizeof(m_facesStatus));
}

ParaEngine::BMaxNode::~BMaxNode()
{

}

void ParaEngine::BMaxNode::SetColor(DWORD val)
{
	m_color = val;
}

DWORD ParaEngine::BMaxNode::GetColor()
{
	if (m_color == 0)
	{
		auto node_template = BlockWorldClient::GetInstance()->GetBlockTemplate((uint16)template_id);
		if (node_template && node_template->isSolidBlock())
			SetColor(node_template->GetBlockColor(block_data));
		else
			SetColor(Color::White);
	}
	return m_color;
}

BlockModel * ParaEngine::BMaxNode::GetBlockModel()
{
	return m_pBlockModel;
}

void ParaEngine::BMaxNode::SetBlockModel(BlockModel* pModel)
{
	m_pBlockModel = pModel;
}

BMaxFrameNode* ParaEngine::BMaxNode::ToBoneNode()
{
	return NULL;
}

bool ParaEngine::BMaxNode::HasBoneWeight()
{
	return m_nBoneIndex>=0;
}

int ParaEngine::BMaxNode::GetBoneIndex()
{
	return m_nBoneIndex;
}

void ParaEngine::BMaxNode::SetBoneIndex(int nIndex)
{
	m_nBoneIndex = nIndex;
}

BMaxNode* ParaEngine::BMaxNode::GetNeighbour(BlockDirection::Side side)
{
	Int32x3 offset = BlockDirection::GetOffsetBySide(side);
	int nX = x + offset.x;
	int nY = y + offset.y;
	int nZ = z + offset.z;
	return m_pParser->GetBMaxNode(nX, nY, nZ);
}

BMaxNode* ParaEngine::BMaxNode::GetNeighbourByOffset(Vector3 offset)
{
	int nX = x + (int)offset.x;
	int nY = y + (int)offset.y;
	int nZ = z + (int)offset.z;
	return m_pParser->GetBMaxNode(nX, nY, nZ);
}

bool ParaEngine::BMaxNode::isSolid()
{
	return true;
}

void ParaEngine::BMaxNode::QueryNeighborBlockData(BMaxNode** pBlockData, int nFrom /*= 0*/, int nTo /*= 26*/)
{
	const Int16x3* neighborOfsTable = BlockCommon::NeighborOfsTable;
	for (int i = nFrom; i <= nTo; ++i)
	{
		Int16x3 curBlockId;
		curBlockId.x = x + neighborOfsTable[i].x;
		curBlockId.y = y + neighborOfsTable[i].y;
		curBlockId.z = z + neighborOfsTable[i].z;

		BMaxNode* pBlock = m_pParser->GetBMaxNode(curBlockId.x, curBlockId.y, curBlockId.z);
		pBlockData[i - nFrom] = pBlock;
	}
}

uint32 ParaEngine::BMaxNode::CalculateCubeAO(BMaxNode** neighborBlocks)
{
	uint32 aoFlags = 0;

	BMaxNode* pCurBlock = neighborBlocks[rbp_pXpYpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_xyz;
	}

	pCurBlock = neighborBlocks[rbp_nXpYpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_Nxyz;
	}

	pCurBlock = neighborBlocks[rbp_pXpYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_xyNz;
	}

	pCurBlock = neighborBlocks[rbp_nXpYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_NxyNz;
	}

	pCurBlock = neighborBlocks[rbp_pYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_topFront;
	}

	pCurBlock = neighborBlocks[rbp_nXpY];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_topLeft;
	}

	pCurBlock = neighborBlocks[rbp_pXpY];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_topRight;
	}

	pCurBlock = neighborBlocks[rbp_pYpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_topBack;
	}

	pCurBlock = neighborBlocks[rbp_nXnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_LeftFront;
	}

	pCurBlock = neighborBlocks[rbp_nXpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_leftBack;
	}

	pCurBlock = neighborBlocks[rbp_pXnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_rightFont;
	}

	pCurBlock = neighborBlocks[rbp_pXpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_rightBack;
	}

	pCurBlock = neighborBlocks[rbp_pXnYPz];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_xNyz;
	}

	pCurBlock = neighborBlocks[rbp_pXnYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_xNyNz;
	}

	pCurBlock = neighborBlocks[rbp_nXnYPz];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_NxNyz;
	}

	pCurBlock = neighborBlocks[rbp_nXnYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_NxNyNz;
	}

	pCurBlock = neighborBlocks[rbp_nYnZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_bottomFront;
	}

	pCurBlock = neighborBlocks[rbp_nXnY];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_bottomLeft;
	}

	pCurBlock = neighborBlocks[rbp_pXnY];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_bottomRight;
	}

	pCurBlock = neighborBlocks[rbp_nYpZ];
	if (pCurBlock)
	{
		aoFlags |= BlockModel::evf_bottomBack;
	}
	return aoFlags;
}

int32_t ParaEngine::BMaxNode::GetAvgVertexLight(int32_t v1, int32_t v2, int32_t v3, int32_t v4)
{
	if ((v2 > 0 || v3 > 0))
	{
		int32_t max1 = Math::Max(v1, v2);
		int32_t max2 = Math::Max(v3, v4);
		return Math::Max(max1, max2);
	}
	else
	{
		return v1;
	}
}

void BMaxNode::SetFaceVisible(int nIndex)
{
	m_facesStatus[nIndex] = faceVisibleNotSign;
}

void BMaxNode::SetFaceUsed(int nIndex)
{
	m_facesStatus[nIndex] = faceVisibleSigned;
}

bool BMaxNode::IsFaceNotUse(int nIndex)
{
	return m_facesStatus[nIndex] == faceVisibleNotSign;
}

int ParaEngine::BMaxNode::TessellateBlock(BlockModel* tessellatedModel)
{
	int bone_index = GetBoneIndex();
	// we will assume tessellatedModel is cube model. 
	// tessellatedModel->LoadCubeModel();

	BlockTemplate* block_template = BlockWorldClient::GetInstance()->GetBlockTemplate((uint16)template_id);
	DWORD dwBlockColor = GetColor();

	//neighbor blocks
	const int nNearbyBlockCount = 27;
	BMaxNode* neighborBlocks[nNearbyBlockCount];
	neighborBlocks[rbp_center] = this;
	memset(neighborBlocks + 1, 0, sizeof(BMaxNode*) * (nNearbyBlockCount - 1));
	QueryNeighborBlockData(neighborBlocks + 1, 1, nNearbyBlockCount - 1);

	//ao
	uint32 aoFlags = CalculateCubeAO(neighborBlocks);

	// model position offset
	BlockVertexCompressed* pVertices = tessellatedModel->GetVertices();
	int count = tessellatedModel->GetVerticesCount();
	const Vector3& vCenter = m_pParser->GetCenterPos();
	Vector3 vOffset((float)x - vCenter.x, (float)y, (float)z - vCenter.z);
	for (int k = 0; k < count; k++)
	{
		pVertices[k].OffsetPosition(vOffset);
		pVertices[k].SetBlockColor(dwBlockColor);
	}

	for (int face = 0; face < 6; ++face)
	{
		int nFirstVertex = face * 4;

		BMaxNode* pCurBlock = neighborBlocks[BlockCommon::RBP_SixNeighbors[face]];

		// we will preserve the face when two bones does not belong to the same bone
		if (!pCurBlock || (pCurBlock->GetBoneIndex() != bone_index || !pCurBlock->isSolid()))
		{
			for (int v = 0; v < 4; ++v)
			{
				int i = nFirstVertex + v;
				
				int nShadowLevel = 0;
				if (aoFlags > 0 && (nShadowLevel = tessellatedModel->CalculateCubeVertexAOShadowLevel(i, aoFlags)) != 0)
				{
					Color color(dwBlockColor);
					float fShadow = (255 - nShadowLevel) / 255.f;
					color.r = (uint8)(color.r * fShadow);
					color.g = (uint8)(color.g * fShadow);
					color.b = (uint8)(color.b * fShadow);
					tessellatedModel->SetVertexColor(i, (DWORD)color);
				}
			}
			SetFaceVisible(face);
		}
	}
	return tessellatedModel->GetVerticesCount();
}


#pragma once
#include "BMaxNode.h"

namespace ParaEngine
{
	class Bone;

	/** bone node in bmax */
	struct BMaxFrameNode : public BMaxNode
	{
	public:
		BMaxFrameNode(BMaxParser* pParser, int16 x_, int16 y_, int16 z_, int32 template_id_, int32 block_data_, int32 boneIndex);
		virtual ~BMaxFrameNode();
	public:
		BMaxFrameNode* GetParent();
		int64 GetParentIndex() const;
		void SetParentIndex(int64 val);
		bool HasParent();
		/** we will automatically set the bone name according to topology, if it is not set before. */
		void AutoSetBoneName();
		ParaEngine::Bone* GetBone();
		/** @param bRefresh: if true, we will refresh */
		ParaEngine::Bone* GetParentBone(bool bRefresh = true);
		virtual int GetBoneIndex();
		virtual void SetBoneIndex(int nIndex);
		/** get the bone node interface if it is*/
		virtual BMaxFrameNode* ToBoneNode();

		int GetParentBoneIndex();
		void SetIndex(int nIndex);
		
		 /** Returns true if this object is a parent, (or grandparent and so on to any level), of the given child. */
		bool IsAncestorOf(BMaxFrameNode* pChild);

		/** if bone chain is recursive, we will break it. return true if cycles is found broken*/
		bool BreakCycles();

		/** get the bone color */
		virtual DWORD GetColor();
		virtual void SetColor(DWORD val);

		/** get child bone count */
		int GetChildCount();
		BMaxFrameNode* GetChild(int nIndex);
		/** -1 if not found. */
		int64 GetChildIndexOf(BMaxFrameNode* pChild);
		int64 GetChildIndex();
		/** add child node */
		void AddChild(BMaxFrameNode* pNode);

		void UpdatePivot();

		/** get the bone axis. 6 possible directions */
		Vector3 GetAxis();
	protected:
		/** the bone's color if not calculated before. */
		DWORD CalculateBoneColor();

	public:
		int64 m_nParentIndex;
		ref_ptr<ParaEngine::Bone> m_pBone;
		/** child node position index*/
		vector<int64> m_children;
	};
	typedef ref_ptr<BMaxFrameNode> BMaxFrameNodePtr;
}


//-----------------------------------------------------------------------------
// Class:Block max frame node
// Authors:	LiXizhi
// Emails:	lixizhi@yeah.net
// Date:	2015.9.26
// Desc: 
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "ParaXModel/ParaXModel.h"
#include "ParaXModel/ParaXBone.h"
#include "BlockEngine/BlockCommon.h"
#include "BlockEngine/BlockDirection.h"
#include "BlockEngine/BlockWorldClient.h"
#include "BMaxParser.h"
#include "BMaxFrameNode.h"
using namespace ParaEngine;


BMaxFrameNode::BMaxFrameNode(BMaxParser* pParser, int16 x_, int16 y_, int16 z_, int32 template_id_, int32 block_data_, int32 boneIndex)
	:BMaxNode(pParser, x_, y_, z_, template_id_, block_data_), m_nParentIndex(-1)
{
	m_pBone.reset(new ParaEngine::Bone());
	m_pBone->nIndex = boneIndex;
}

void ParaEngine::BMaxFrameNode::UpdatePivot()
{
	Vector3 pivot(x - m_pParser->m_centerPos.x + BlockConfig::g_blockSize * 0.5f, y + BlockConfig::g_blockSize * 0.5f, z - m_pParser->m_centerPos.z + BlockConfig::g_blockSize * 0.5f);
	m_pBone->bUsePivot = true;
	m_pBone->pivot = pivot * m_pParser->m_fScale;
	m_pBone->flags = ParaEngine::Bone::BONE_USE_PIVOT;
}

Vector3 ParaEngine::BMaxFrameNode::GetAxis()
{
	BlockDirection::Side mySide = BlockDirection::GetBlockSide(block_data);
	Int32x3 offset = BlockDirection::GetOffsetBySide(BlockDirection::GetOpSide(mySide));
	return Vector3((float)offset.x, (float)offset.y, (float)offset.z);
}

int BMaxFrameNode::GetBoneIndex()
{
	return GetBone()->GetBoneIndex();
}

int BMaxFrameNode::GetParentBoneIndex()
{
	auto pParent = GetParent();
	return (pParent) ? pParent->GetBoneIndex() : -1;
}

void ParaEngine::BMaxFrameNode::SetIndex(int nIndex)
{
	m_pBone->nIndex = nIndex;
}

BMaxFrameNode* BMaxFrameNode::GetParent()
{
	auto iter = m_pParser->m_nodes.find(m_nParentIndex);
	if (m_nParentIndex >= 0 && iter != m_pParser->m_nodes.end())
	{
		auto pParent = iter->second;
		if (pParent)
			return pParent->ToBoneNode();
	}
	return NULL;
}

ParaEngine::BMaxFrameNode::~BMaxFrameNode()
{

}

int64 ParaEngine::BMaxFrameNode::GetParentIndex() const
{
	return m_nParentIndex;
}

void ParaEngine::BMaxFrameNode::SetParentIndex(int64 val)
{
	m_nParentIndex = val;
	auto pParent = GetParent();
	if (pParent)
	{
		pParent->AddChild(this);
		m_pBone->parent = pParent->GetBoneIndex();
	}
	else
		m_pBone->parent = -1;
}

bool ParaEngine::BMaxFrameNode::HasParent()
{
	return m_nParentIndex >= 0;
}

void ParaEngine::BMaxFrameNode::AutoSetBoneName()
{
	Bone* pBone = GetBone();
	if (pBone->GetName().empty())
	{
		std::ostringstream stream;
		stream << "bone";
		BMaxFrameNode* pChild = this;
		int nSide = -1; // left or right bone
		int nMultiChildParentCount = 0;
		int nParentCount = 0;
		while (pChild)
		{
			BMaxFrameNode* pParent = pChild->GetParent();
			if (pParent && pParent->GetChildCount()>1)
			{
				nMultiChildParentCount++;
				if (pParent->z > pChild->z)
					nSide = 1;
				else if (pParent->z < pChild->z)
					nSide = 0;
			}
			pChild = pParent;
			++nParentCount;
		}
		if (nParentCount > 0)
			nParentCount --;
		// left or right side
		if (nSide == 0)
			stream << "_left";
		else if (nSide == 1)
			stream << "_right";
		if (nSide >= 0 && nMultiChildParentCount>1)
		{
			// how many multi child parent to distinguish hand and feet, etc. 
			stream << "_mp" << nMultiChildParentCount;
		}
		// how many parent levels
		stream << "_p" << nParentCount;
		
		// check for hand and feet and apply inverse IK
		auto parent = GetParent();
		if (parent && parent->GetChildCount() == 1)
		{
			parent = parent->GetParent();
			if (parent && parent->GetChildCount() == 1)
			{
				parent = parent->GetParent();
				if (parent && parent->GetChildCount() > 1)
				{
					stream << "_IK";
				}
			}
		}
		std::string sName = stream.str();
		int nCount = m_pParser->GetNameAppearanceCount(sName, true);
		if (nCount > 0){
			stream << "_" << nCount;
			sName = stream.str();
		}
		pBone->SetName(sName);
	}
}



ParaEngine::Bone* ParaEngine::BMaxFrameNode::GetBone()
{
	return m_pBone.get();
}

void ParaEngine::BMaxFrameNode::SetBoneIndex(int nIndex)
{
	BMaxNode::SetBoneIndex(nIndex);
}

BMaxFrameNode* ParaEngine::BMaxFrameNode::ToBoneNode()
{
	return this;
}

bool ParaEngine::BMaxFrameNode::IsAncestorOf(BMaxFrameNode* pChild)
{
	while (pChild)
	{
		if (pChild == this)
			return true;
		else if (!pChild->HasParent())
			return false;
		else
			pChild = pChild->GetParent();
	}
    return false;
}

bool ParaEngine::BMaxFrameNode::BreakCycles()
{
	if (HasParent())
	{
		if (IsAncestorOf(GetParent()))
		{
			SetParentIndex(-1);
		}
	}
	return true;
}

DWORD ParaEngine::BMaxFrameNode::CalculateBoneColor()
{
	if (m_color != 0)
		return m_color;
	DWORD color = Color::White;
	auto pBlockWorld = BlockWorldClient::GetInstance();
	BlockDirection::Side mySide = BlockDirection::GetBlockSide(block_data);

	auto index = GetIndex();
	BMaxFrameNode* pParentNode = GetParent();
	
	// always start from the opposite side
	int myOppositeSide = (int)BlockDirection::GetOpSide(mySide);
	
	for (int i = 0; i < 6; i++)
	{
		BlockDirection::Side side = BlockDirection::GetBlockSide((myOppositeSide + i) % 6);

		if (side != mySide || pParentNode == NULL)
		{
			BMaxNode* neighbourNode = GetNeighbour(side);
			if (neighbourNode && !neighbourNode->HasBoneWeight())
			{
				auto next_node_template = pBlockWorld->GetBlockTemplate((uint16)(neighbourNode->template_id));
				if (next_node_template && next_node_template->isSolidBlock() && neighbourNode->template_id != BMaxParser::BoneBlockId)
				{
					color = next_node_template->GetBlockColor(neighbourNode->block_data);
					SetColor(color);
					return color;
				}
			}
		}
	}

	if (pParentNode!=NULL)
	{
		color = pParentNode->GetColor();
	}
	SetColor(color);
	return color;
}

DWORD ParaEngine::BMaxFrameNode::GetColor()
{
	if (m_color == 0)
	{
		CalculateBoneColor();
	}
	return m_color;
}


void ParaEngine::BMaxFrameNode::SetColor(DWORD val)
{
	BMaxNode::SetColor(val);
}

int ParaEngine::BMaxFrameNode::GetChildCount()
{
	return (int)m_children.size();
}

BMaxFrameNode* ParaEngine::BMaxFrameNode::GetChild(int nIndex)
{
	if ((int)(m_children.size()) > nIndex)
	{
		return m_pParser->m_bones[(int)m_children[nIndex]].get();
	}
	return NULL;
}

int64 ParaEngine::BMaxFrameNode::GetChildIndexOf(BMaxFrameNode* pChild)
{
	auto nIndex = pChild->GetIndex();
	for (int i = 0; i < (int)m_children.size(); ++i)
	{
		if (m_children[i] == nIndex)
			return i;
	}
	return -1;
}

int64 ParaEngine::BMaxFrameNode::GetChildIndex()
{
	auto parent = GetParent();
	return (parent) ? parent->GetChildIndexOf(this) : -1;
}

void ParaEngine::BMaxFrameNode::AddChild(BMaxFrameNode* pNode)
{
	auto nIndex = pNode->GetIndex();
	for (auto childIndex: m_children)
	{
		if (childIndex == nIndex)
			return;
	}
	m_children.push_back(nIndex);
}

ParaEngine::Bone* BMaxFrameNode::GetParentBone(bool bRefresh)
{
	if (bRefresh)
	{
		SetParentIndex(-1);
		int cx = x;
		int cy = y;
		int cz = z;
		BlockDirection::Side side = BlockDirection::GetBlockSide(block_data);
		Int32x3 offset = BlockDirection::GetOffsetBySide(side);
		int dx = offset.x;
		int dy = offset.y;
		int dz = offset.z;
		int maxBoneLength = BMaxParser::MaxBoneLengthHorizontal;
		if (dy != 0){
			maxBoneLength = BMaxParser::MaxBoneLengthVertical;
		}
		for (int i = 1; i <= maxBoneLength; i++)
		{
			int x = cx + dx*i;
			int y = cy + dy*i;
			int z = cz + dz*i;
			BMaxFrameNode* parent_node = m_pParser->GetFrameNode(x, y, z);
			if (parent_node)
			{
				BlockDirection::Side parentSide = BlockDirection::GetBlockSide(parent_node->block_data);
				BlockDirection::Side opSide = BlockDirection::GetOpSide(parentSide);
				if (opSide != side || (dx + dy + dz) < 0)
				{
					// prevent acyclic links
					if (!IsAncestorOf(parent_node))
					{
						SetParentIndex(parent_node->GetIndex());
					}
				}
				break;
			}
		}
	}
	auto pParent = GetParent();
	return (pParent) ? pParent->GetBone() : NULL;
}

#pragma once
#include "BlockEngine/BlockCoordinate.h"
#include "math/ShapeAABB.h"
#include "BMaxFrameNode.h"
#include "ParaXModel/ParaXModel.h"
#include "Rectangle.h"

#include <unordered_map>


class TiXmlDocument;
class TiXmlElement;
class TiXmlNode;
typedef TiXmlDocument BMaxXMLDocument;
typedef TiXmlElement BMaxXMLElement;
typedef TiXmlNode BMaxXMLNode;

namespace ParaEngine
{
	class CParaXModel;
	class BlockModel;
	class Bone;
	class BMaxParser;
	struct ModelAnimation;
	struct ModelVertex;
	class BMaxAnimGenerator;

	/** Block Max file format parser. For *.bmax
	*/
	class BMaxParser
	{
	public:
		/** block id */
		enum BlockIDNum
		{
			// transparent block (cob web) will transmit bone weight, but will not be rendered. 
			TransparentBlockId = 118,
			// bones
			BoneBlockId = 253,
			// block model are extracted. 
			BlockModelBlockId = 254,
		};

		BMaxParser( const char* filename = NULL, BMaxParser* pParent = NULL);
		virtual ~BMaxParser(void);
		CParaXModel* ParseParaXModel();
		CParaXModel* ParseParaXModel(uint32 nMaxTriangleCount);
		
		const std::string& GetFilename() const;
		void SetFilename(const std::string& val);

		void SetMergeCoplanerBlockFace(bool val);

		void Load(const char* pBuffer, int32 nSize);
	protected:
		/** check if the given filename belongs to one of its parent's filename*/
		bool IsFileNameRecursiveLoaded(const std::string& filename);
		void AddAnimation(const ModelAnimation& anim);
		int GetAnimationsCount();
		BMaxParser* GetParent() const { return m_pParent; }
		void SetParent(BMaxParser* val) { m_pParent = val; }

		void SetAutoScale(bool value);
		bool IsAutoScale();
		const Vector3& GetCenterPos() const;

		/** It will create 6 recangles from cube (centered later node's x, y, z) for each bmax node without merging coplaner block faces. */
		void CreatRectanglesFromBlocks();
		void MergeCoplanerBlockFace();
		bool IsCoplaneNode(BMaxNode* node1, BMaxNode* node2, int nFaceIndex);
		void FindCoplanerFace(BMaxNode* node, uint32 nFaceIndex);
		void FindNeighbourFace(Rectangle *rectangle, uint32 i, uint32 nFaceIndex);

		void CalculateLod(uint32 nMaxTriangleCount);
		void GetLodTable(uint32 faceCount, vector<uint32>&lodTable);
		void PerformLod();
		void CalculateAABB(vector<BMaxNodePtr>&nodes);
		void CalculateLodNode(map<int64, BMaxNodePtr> &nodeMap, int x, int y, int z);
	
		inline uint64 GetNodeIndex(uint16 x, uint16 y, uint16 z)
		{
			return (uint64)x + ((uint64)z << 16) + ((uint64)y << 32);
		}
		/* same as GetNode except that it checks for boundary condition. */
		BMaxNode* GetBMaxNode(int x, int y, int z);

		inline BMaxNode* GetNode(uint16 x, uint16 y, uint16 z)
		{
			uint64 index = GetNodeIndex(x, y, z);
			auto iter = m_nodes.find(index);
			return (iter != m_nodes.end()) ? iter->second.get() : NULL;
		}
		inline BMaxNode* GetNodeByIndex(int64 index)
		{
			auto iter = m_nodes.find(index);
			return (iter != m_nodes.end()) ? iter->second.get() : NULL;
		}
		/** return node index*/
		int64 InsertNode(BMaxNodePtr& nodePtr);

		void ParseBlocks(BMaxXMLDocument& doc);
		void ParseBlocks_Internal(const char* value);
		
		void ParseVisibleBlocks();
		void ParseHead(BMaxXMLDocument& doc);
		// parse bones
		void ParseBlockFrames();

		void CreateDefaultAnimations();

		void AutoAddWalkAnimation(int nAnimID, int nStartTime, int nEndTime, float fMoveSpeed=4.f, bool bMoveForward = true);

		BMaxFrameNode* GetFrameNode(int16 x, int16 y, int16 z);

		// bone kins
		void CalculateBoneWeights();

		void CalculateBoneWeightFromNeighbours(BMaxNode* node);

		void CalculateBoneSkin(BMaxFrameNode* pBoneNode);
		/**
		* @param bMustBeSameColor: if true we will only add bone if color is the same as the bone. 
		*/
		void CalculateBoneWeightForBlock(BMaxFrameNode* pBoneNode, BMaxNode* node, bool bMustBeSameColor = true);
		/** find the first root bone index. In most cases it is 0.
		* the first bone without parent is the root bone
		*/
		int FindRootBoneIndex();
		// animations 
		void ParseBlockAnimations(BMaxXMLDocument& doc);
		void ParseBlockAnimationSet(BMaxXMLElement* node);
		void ParseBlockAnimation(BMaxXMLElement* node);
		void ParseBlockAnimationKeys(uint16 x, uint16 y, uint16 z, BMaxXMLElement* node, int nIndex);
		void ParseBlockAnimationKey(BMaxXMLElement* node,Bone* bone,const std::string propertyType);

		void ClearModel();
		void FillParaXModelData(CParaXModel *pMesh);
		void FillVerticesAndIndices();
		//void ProcessBoneNodes();
		//int CreateBoneIndex(uint16 x, uint16 y, uint16 z, int parentIndex);
		int GetBoneIndex(uint16 x, uint16 y, uint16 z);
		void ScaleModels();
		float CalculateScale(float length);
		int64 GetIndexFromXmlElement(BMaxXMLElement* node, const char* name, int& x, int& y, int& z);

		bool ReadValue(BMaxXMLElement* node, const char* name, int32_t& value);
		bool ReadValue(BMaxXMLElement* node, const char* name, float& value);
		bool ReadValue(BMaxXMLElement* node, const char* name, Vector3& value);
		bool ReadValue(BMaxXMLElement* node, const char* name, std::string& value);
		bool ReadValue(BMaxXMLElement* node, const char* name, Vector4& value);

		/** how many times that a given name has appeared. */
		int GetNameAppearanceCount(const std::string& name, bool bAdd = true);

		/** filename is relative to current world directory. */
		CParaXModel* CreateGetRefModel(const std::string& sFilename);

		ModelGeoset* AddGeoset();
		ModelRenderPass* AddRenderPass();

		/* create or get the default animation generator */
		BMaxAnimGenerator* GetAnimGenerator();
	protected:
		BMaxParser* m_pParent;
		std::string m_filename;
		std::vector<BlockModel*> m_blockModels;
		std::unordered_map<uint64, BMaxNodePtr> m_nodes;
		//std::map<uint64, BMaxNodePtr> m_nodes;
		std::map<std::string, ref_ptr<CParaXModel> > m_refModels;
		/*std::vector<RectanglePtr>m_originRectangles;
		std::map<uint16, vector<RectanglePtr>>m_lodRectangles;*/

		/// array of bone nodes, array index is the bone index. 
		vector<BMaxFrameNodePtr> m_bones;
		// how many times that a given name has appeared. 
		std::map<std::string, int> m_name_occurances;
		bool m_bAutoScale;
		bool m_bHasBoneBlock;
		float m_fScale;
		map<BlockModel*, BMaxNode*> m_blockModelsMapping;
		vector<ModelAnimation> m_anims;
		bool m_bHasAnimation;

		vector<ModelVertex> m_vertices;
		vector<RectanglePtr>m_rectangles;
		vector<uint16> m_indices;
		std::vector<ModelGeoset> m_geosets;
		std::vector<ModelRenderPass> m_renderPasses;
		/** aabb in block world coordinate */
		CShapeBox m_blockAABB;
		/** the center point in block world coordinate */
		Vector3 m_centerPos;
		// AABB in model space
		Vector3 m_minExtent;
		Vector3 m_maxExtent;

		/** the block id used to extend AABB. */
		int m_nHelperBlockId;
		int m_nLodLevel;
		BMaxAnimGenerator* m_pAnimGenerator;

		bool m_bMergeCoplanerBlockFace;

		static const int  MaxBoneLengthHorizontal;
		static const int  MaxBoneLengthVertical;
		friend struct BMaxNode;
		friend struct BMaxFrameNode;
		friend struct BMaxBlockModelNode;
		friend class BMaxAnimGenerator;
	};
}

//-----------------------------------------------------------------------------
// Class:Block max model parser	
// Authors:	leio, LiXizhi, wujiajun(winless)
// Emails:	lixizhi@yeah.net
// Date:	2015.6.29
// Desc: at most 65535*65535*65535 blocks can be loaded
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BlockEngine/BlockModel.h"
#include "BlockEngine/BlockCommon.h"
#include "BlockEngine/BlockWorldClient.h"
#include "BlockEngine/BlockTemplate.h"
#include "BlockEngine/BlockWorldClient.h"
#include "ParaXModel/ParaXModel.h"
#include "ParaXModel/ParaXBone.h"
#include "StringHelper.h"
#include "NPLHelper.h"
#include "NPLTable.h"
#include "ParaXModel/AnimTable.h"
#include "ParaXModel/XFileHelper.h"
#include "BMaxBlockModelNode.h"
#include <tinyxml.h>
#include "BlockEngine/BlockDirection.h"
#include "BMaxAnimGenerator.h"
#include "BMaxParser.h"

#include "ZipArchive.h"

/** @def define this to use algorithm that is not recursive for merging coplanar faces. */
#define USE_COPLANER_ALGORITHM_NON_RECURSIVE

namespace ParaEngine
{
	const int BMaxParser::MaxBoneLengthHorizontal = 50;
	const int BMaxParser::MaxBoneLengthVertical = 100;

	BMaxParser::BMaxParser(const char* filename, BMaxParser* pParent)
		: m_bAutoScale(true)
		, m_nHelperBlockId(90)
		, m_pAnimGenerator(NULL)
		, m_pParent(pParent)
		, m_bHasAnimation(false)
		, m_centerPos(0, 0, 0)
		, m_fScale(1.f)
		, m_nLodLevel(0)
		, m_bMergeCoplanerBlockFace(true)
	{
		m_bHasBoneBlock = false;
		if (filename)
			SetFilename(filename);
		//Load(pBuffer, nSize);
	}

	BMaxParser::~BMaxParser(void)
	{
		for (uint32 i = 0; i < m_blockModels.size(); i++)
		{
			SAFE_DELETE(m_blockModels[i]);
		}
		m_blockModels.clear();
		m_nodes.clear();
		SAFE_DELETE(m_pAnimGenerator);
	}

	void BMaxParser::Load(const char* pBuffer, int32 nSize)
	{
		m_nLodLevel = 0;

		BMaxXMLDocument doc;

		std::string uncompressedData;
		
		if (IsZipData(pBuffer, nSize))
		{
			if (GetFirstFileData(pBuffer, uncompressedData))
			{
				pBuffer = uncompressedData.c_str();
			}
		}


		doc.Parse(pBuffer);
		ParseHead(doc);
		ParseBlocks(doc);
	}

	void BMaxParser::ParseBlocks(BMaxXMLDocument& doc)
	{
		BMaxXMLElement* element = doc.FirstChildElement("pe:blocktemplate");
		if (element != NULL)
		{
			BMaxXMLElement* blocks_element = element->FirstChildElement("pe:blocks");
			if (blocks_element != NULL)
			{

				const char* value = blocks_element->GetText();
				ParseBlocks_Internal(value);
				ParseBlockFrames();
				CalculateBoneWeights();
				if (m_bMergeCoplanerBlockFace) {
					MergeCoplanerBlockFace();
				}else {
					CreatRectanglesFromBlocks();
				}
			}
		}
	}

	void BMaxParser::ParseBlocks_Internal(const char* value)
	{
		auto pBlockWorld = BlockWorldClient::GetInstance();
		vector<BMaxNodePtr> nodes;
		CShapeBox aabb;
		NPL::NPLObjectProxy msg = NPL::NPLHelper::StringToNPLTable(value);
		for (NPL::NPLTable::IndexIterator_Type itCur = msg.index_begin(); itCur != msg.index_end(); ++itCur)
		{
			NPL::NPLObjectProxy& block = itCur->second;
			int x = (int)((double)block[1]);
			int y = (int)((double)block[2]);
			int z = (int)((double)block[3]);
			int template_id = (int)((double)block[4]);
			int block_data = (int)((double)block[5]);
			
			aabb.Extend(Vector3((float)x, (float)y, (float)z));
			auto pBlockTemplate = pBlockWorld->GetBlockTemplate(template_id);
			
			if (pBlockTemplate && m_nHelperBlockId != template_id)
			{
				if (template_id == BlockModelBlockId)
				{
					if (block[6].GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
					{
						NPL::NPLObjectProxy& entityData = block[6];
						NPL::NPLObjectProxy& attr = entityData["attr"];
						if (attr.GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
						{
							std::string sFilename = attr["filename"];
							if (!sFilename.empty())
							{
								if (IsFileNameRecursiveLoaded(sFilename))
								{
									OUTPUT_LOG("warning: bmax models reference the file %s recursively\n", sFilename.c_str());
								}
								else
								{
									BMaxBlockModelNodePtr node(new BMaxBlockModelNode(this, x, y, z, template_id, block_data));
									node->SetFilename(sFilename);
									node->SetFacing((float)((double)attr["facing"]));
									nodes.push_back(BMaxNodePtr(node.get()));
								}
							}
						}
					}
				}
				else if (template_id == BoneBlockId)
				{
					
					m_bHasBoneBlock = true;
					int nBoneIndex = (int)m_bones.size();
					BMaxFrameNodePtr pFrameNode(new BMaxFrameNode(this, x, y, z, template_id, block_data, nBoneIndex));
					m_bones.push_back(pFrameNode);
					nodes.push_back(BMaxNodePtr(pFrameNode.get()));
					
					if (block[6].GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
					{
						NPL::NPLObjectProxy& entityData = block[6];

						std::string sBoneName = "";
						GetAnimGenerator()->ParseParameters(entityData, nBoneIndex, sBoneName);

						if (entityData[1].GetType() == NPL::NPLObjectBase::NPLObjectType_Table)
						{
							NPL::NPLObjectProxy& cmd = entityData[1];
							if (cmd[1].GetType() == NPL::NPLObjectBase::NPLObjectType_String)
							{
								if (!sBoneName.empty())
								{
									int nCount = GetNameAppearanceCount(sBoneName, true);
									if (nCount > 0){
										std::ostringstream stream;
										stream << sBoneName << nCount;
										pFrameNode->GetBone()->SetName(stream.str());
									}
									else
										pFrameNode->GetBone()->SetName(sBoneName);

									pFrameNode->GetBone()->AutoSetBoneInfoFromName();
								}

								/*const std::string& sBoneName = cmd[1];
								if (!sBoneName.empty())
								{
									int nCount = GetNameAppearanceCount(sBoneName, true);
									if (nCount > 0){
										std::ostringstream stream;
										stream << sBoneName << nCount;
										pFrameNode->GetBone()->SetName(stream.str());
									}
									else
										pFrameNode->GetBone()->SetName(sBoneName);
								}*/

							}
						}
					}
				}
				else if (!pBlockTemplate->isSolidBlock())
				{
					// other non-solid blocks will not be rendered. but can be used to connect bones
					template_id = TransparentBlockId;
					BMaxBlockModelNodePtr node(new BMaxBlockModelNode(this, x, y, z, template_id, block_data));
					nodes.push_back(BMaxNodePtr(node.get()));
				}
				else
				{
					BMaxNodePtr node(new BMaxNode(this, x, y, z, template_id, block_data));
					nodes.push_back(node);
				}
			}
		}

		CalculateAABB(nodes);
		// set AABB and center
		/*m_blockAABB = aabb;
		m_centerPos = m_blockAABB.GetCenter();
		m_centerPos.y = 0;
		m_centerPos.x = (m_blockAABB.GetWidth() + 1.f) * 0.5f;
		m_centerPos.z = (m_blockAABB.GetDepth() + 1.f) * 0.5f;

		int offset_x = (int)m_blockAABB.GetMin().x;
		int offset_y = (int)m_blockAABB.GetMin().y;
		int offset_z = (int)m_blockAABB.GetMin().z;
		
		for (auto node : nodes)
		{
			node->x -= offset_x;
			node->y -= offset_y;
			node->z -= offset_z;
			InsertNode(node);
		}*/

		// set scaling;
		
	}

	void BMaxParser::ParseVisibleBlocks()
	{
		m_blockModels.clear();
		for (auto& item : m_nodes)
		{
			BMaxNode* node = item.second.get();
			if (node != NULL)
			{
				if (node->template_id == TransparentBlockId)
				{
					// total skipped for cobweb
				}
				else 
				{
					BlockModel* tessellatedModel = new BlockModel();
					if (node->TessellateBlock(tessellatedModel) > 0)
					{
						node->SetBlockModel(tessellatedModel);
						m_blockModels.push_back(tessellatedModel);
						m_blockModelsMapping[tessellatedModel] = node;
					}
					else
					{
						node->SetBlockModel(NULL);
						delete tessellatedModel;
					}
				}
			}
		}
	}
	void BMaxParser::ScaleModels()
	{
		if (m_blockModels.size() == 0)
			return;
		float scale = m_fScale;

		int nSize = (int)m_blockModels.size();
		for (int i = 0; i < nSize; i++)
		{
			BlockModel* model = m_blockModels.at(i);
			int nVertices = model->GetVerticesCount();
			BlockVertexCompressed* pVertices = model->GetVertices();
			for (int k = 0; k < nVertices; k++)
			{
				pVertices[k].position[0] *= scale;
				pVertices[k].position[1] *= scale;
				pVertices[k].position[2] *= scale;
			}
		}
	}

	float BMaxParser::CalculateScale(float length)
	{
		int nPowerOf2Length = Math::NextPowerOf2((int)(length + 0.1f));
		return (float)(BlockConfig::g_blockSize / nPowerOf2Length);
	}

	int64 BMaxParser::GetIndexFromXmlElement(BMaxXMLElement* node, const char* name, int& x, int& y, int& z)
	{
		if (node == NULL)
		{
			return -1;
		}
		const char* id = node->Attribute(name);
		std::string id_str;
		if (id)
		{
			id_str = id;
			std::vector<std::string> ids;
			StringHelper::split(id_str, ",", ids);
			if (ids.size() > 2)
			{
				x = atoi(ids[0].c_str());
				y = atoi(ids[1].c_str());
				z = atoi(ids[2].c_str());
				x -= (int)m_blockAABB.GetMin().x;
				y -= (int)m_blockAABB.GetMin().y;
				z -= (int)m_blockAABB.GetMin().z;

				int64 index = (int64)GetNodeIndex(x, y, z);
				return index;
			}
		}
		return -1;
	}

	BMaxNode* BMaxParser::GetBMaxNode(int x, int y, int z)
	{
		if (x >= 0 && y >= 0 && z >= 0 ) // && x < 256 && y < 256 && z < 256
			return GetNode((uint16)x, (uint16)y, (uint16)z);
		else
			return NULL;
	}

	int64 BMaxParser::InsertNode(BMaxNodePtr& nodePtr)
	{
		auto index = nodePtr->GetIndex();
		if (GetNode(nodePtr->x, nodePtr->y, nodePtr->z) == NULL)
		{
			m_nodes[index] = nodePtr;
		}
		return index;
	}
	void BMaxParser::ParseHead(BMaxXMLDocument& doc)
	{
		BMaxXMLElement* element = doc.FirstChildElement("pe:blocktemplate");
		if (element != NULL)
		{
			std::string auto_scale;
			ReadValue(element, "auto_scale", auto_scale);
			if (auto_scale == "false" || auto_scale == "False")
			{
				m_bAutoScale = false;
			}
		}
	}

	CParaXModel* BMaxParser::ParseParaXModel()
	{
		ClearModel();
		CParaXModel* pMesh = NULL;
		ParaXHeaderDef m_xheader;
		pMesh = new CParaXModel(m_xheader);
		FillParaXModelData(pMesh);
		pMesh->SetBmaxModel();
		return pMesh;
	}

	CParaXModel * BMaxParser::ParseParaXModel(uint32 nMaxTriangleCount)
	{
		ClearModel();
		CalculateLod(nMaxTriangleCount);

		CParaXModel* pMesh = NULL;
		ParaXHeaderDef m_xheader;
		pMesh = new CParaXModel(m_xheader);
		pMesh->SetBmaxModel();
		if (m_rectangles.size() == 0)
			return pMesh;
		FillParaXModelData(pMesh);
		return pMesh;
	}

	const std::string& BMaxParser::GetFilename() const
	{
		return m_filename;
	}

	void BMaxParser::SetFilename(const std::string& val)
	{
		m_filename = val;
	}

	void BMaxParser::SetAutoScale(bool value)
	{
		m_bAutoScale = value;
	}

	bool BMaxParser::IsAutoScale()
	{
		return m_bAutoScale;
	}

	const Vector3& BMaxParser::GetCenterPos() const
	{
		return m_centerPos;
	}



	void BMaxParser::MergeCoplanerBlockFace()
	{
		ParseVisibleBlocks();

		m_rectangles.clear();
		for (auto& item : m_nodes)
		{
			BMaxNode *node = item.second.get();
			if (node->GetBlockModel())
			{
				for (int i = 0; i < 6; i++)
				{
					if (node->IsFaceNotUse(i))
					{
						FindCoplanerFace(node, i);
					}
				}
			}
		}

		float fScale = m_fScale;
		if (m_nLodLevel > 0) {
			fScale *= (float)pow(2, m_nLodLevel);
		}

		for (RectanglePtr& rectangle : m_rectangles)
		{
			rectangle->ScaleVertices(fScale);
		}
		// OUTPUT_LOG("rect count %d \n", m_rectangles.size());
	}

	void BMaxParser::CreatRectanglesFromBlocks()
	{
		ParseVisibleBlocks();

		m_rectangles.clear();
		for (auto& item : m_nodes)
		{
			BMaxNode *node = item.second.get();
			if (node->GetBlockModel())
			{
				for (int i = 0; i < 6; i++)
				{
					RectanglePtr rectangle(new Rectangle(node, i));
					rectangle->CloneNodes();
					m_rectangles.push_back(rectangle);
				}
			}
		}

		float fScale = m_fScale;
		if (m_nLodLevel > 0) {
			fScale *= (float)pow(2, m_nLodLevel);
		}

		for (RectanglePtr& rectangle : m_rectangles)
		{
			rectangle->ScaleVertices(fScale);
		}
	}


	bool BMaxParser::IsCoplaneNode(BMaxNode* node1, BMaxNode* node2, int nFaceIndex)
	{
		return (node1 && node2 && node1->isSolid() && node2->isSolid() && 
			node2->IsFaceNotUse(nFaceIndex) &&
			node1->GetColor() == node2->GetColor() && 
			node1->GetBoneIndex() == node2->GetBoneIndex() &&
			node2->GetBlockModel() && node2->GetBlockModel()->GetVerticesCount() > 0);
	}

	void BMaxParser::FindCoplanerFace(BMaxNode* node, uint32 nFaceIndex)
	{
#ifdef USE_COPLANER_ALGORITHM_NON_RECURSIVE
		const Vector3 *directionOffsetTable = Rectangle::DirectionOffsetTable;
		int nIndex = nFaceIndex * 4;
		BMaxNode* coplanar_node = node;

		const Vector3& offset = directionOffsetTable[nIndex];
		int nLength = 0;
		for (nLength = 0; IsCoplaneNode(node, node->GetNeighbourByOffset(offset*(nLength + 1.f)), nFaceIndex); ++nLength)
		{
		}
		int nLength2 = 0;
		for (nLength2 = 0; IsCoplaneNode(node, node->GetNeighbourByOffset(-offset*(nLength2 + 1.f)), nFaceIndex); ++nLength2)
		{
		}

		const Vector3& offset2 = directionOffsetTable[nIndex + 1];
		int nLength1 = 0; 
		bool bBreak = false;
		for (nLength1 = 0; !bBreak; ++nLength1)
		{
			for (int i = -nLength2; i <= nLength; i++)
			{
				if (!IsCoplaneNode(node, node->GetNeighbourByOffset(offset2*(nLength1 + 1.f) + offset * (float)i), nFaceIndex))
				{
					nLength1 = nLength1 - 1;
					bBreak = true;
					break;
				}
			}
		}
		int nLength3 = 0;
		bBreak = false;
		for (nLength3 = 0; !bBreak; ++nLength3)
		{
			for (int i = -nLength2; i <= nLength; i++)
			{
				if (!IsCoplaneNode(node, node->GetNeighbourByOffset(-offset2*(nLength3 + 1.f) + offset * (float)i), nFaceIndex))
				{
					nLength3 = nLength3 - 1;
					bBreak = true;
					break;
				}
			}
		}
		// mark all faces as used
		node->SetFaceUsed(nFaceIndex);
		for (int i = -nLength2; i <= nLength; i++)
		{
			for (int j = -nLength3; j <= nLength1; j++)
			{
				auto node_ = node->GetNeighbourByOffset(offset * (float)i + offset2 * (float)j);
				if(node_)
					node_->SetFaceUsed(nFaceIndex);
			}
		}
		
		RectanglePtr rectangle(new Rectangle(node, nFaceIndex));
		m_rectangles.push_back(rectangle);
		rectangle->SetCornerNode(node->GetNeighbourByOffset(offset * (float)nLength - offset2 * (float)nLength3), 1);
		rectangle->SetCornerNode(node->GetNeighbourByOffset(offset2 * (float)nLength1 + offset * (float)nLength), 2);
		rectangle->SetCornerNode(node->GetNeighbourByOffset(-offset * (float)nLength2 + offset2 * (float)nLength1), 3);
		rectangle->SetCornerNode(node->GetNeighbourByOffset(-offset2 * (float)nLength3 - offset * (float)nLength2), 0);
		
#else
		const uint16 nVertexCount = 4;

		BMaxNodePtr nodes[nVertexCount] =
		{
			BMaxNodePtr(node), BMaxNodePtr(node), BMaxNodePtr(node), BMaxNodePtr(node)
		};

		RectanglePtr rectangle(new Rectangle(nodes, nFaceIndex));
		for (uint32 i = 0; i < nVertexCount; i++)
		{
			FindNeighbourFace(rectangle.get(), i, nFaceIndex);
			node->SetFaceUsed(nFaceIndex);
		}

		rectangle->CloneNodes();
		m_rectangles.push_back(rectangle);
#endif
	}

	void BMaxParser::FindNeighbourFace(Rectangle *rectangle, uint32 i, uint32 nFaceIndex)
	{
		const Vector3 *directionOffsetTable = Rectangle::DirectionOffsetTable;
		int nIndex = nFaceIndex * 4 + i;
		PE_ASSERT(nIndex < 24);
		const Vector3& offset = directionOffsetTable[nIndex];

		int nextI = nIndex + ((i == 3) ? -3 : 1);	
		
		PE_ASSERT(nextI < 24);
		BMaxNode *fromNode = rectangle->GetFromNode(nextI);
		BMaxNode *toNode = rectangle->GetToNode(nextI);

		const Vector3& nextOffset = directionOffsetTable[nextI];
		BMaxNode *currentNode = fromNode;

		vector<BMaxNodePtr>nodes;
		
		if (fromNode)
		{
			do
			{
				BMaxNode *neighbourNode = currentNode->GetNeighbourByOffset(offset);
				if (!currentNode->isSolid() || neighbourNode == NULL || !neighbourNode->isSolid() || currentNode->GetColor() != neighbourNode->GetColor() || currentNode->GetBoneIndex() != neighbourNode->GetBoneIndex())
					return;
				BlockModel* neighbourCube = neighbourNode->GetBlockModel();

				if (neighbourCube && neighbourCube->GetVerticesCount() > 0 && neighbourNode->IsFaceNotUse(nFaceIndex))
					nodes.push_back(BMaxNodePtr(neighbourNode));
				else
					return;

				if (currentNode == toNode)
					break;
				currentNode = currentNode->GetNeighbourByOffset(nextOffset);
			} while (currentNode);
		}

		BMaxNode *newFromNode = fromNode->GetNeighbourByOffset(offset);
		BMaxNode *newToNode = toNode->GetNeighbourByOffset(offset);

		for (BMaxNodePtr nodePtr : nodes)
		{
			nodePtr->SetFaceUsed(nFaceIndex);
		}
		rectangle->UpdateNode(newFromNode, newToNode, nextI);
		FindNeighbourFace(rectangle, i, nFaceIndex);
	}

	void BMaxParser::CalculateLod(uint32 nMaxTriangleCount)
	{
		/*
		MergeCoplanerBlockFace(m_rectangles);
		//m_originRectangles = rectangles;

		if (fabs(m_fScale - 1.0f) > FLT_EPSILON)
		{
			for (RectanglePtr& rectangle : rectangles)
			{
				rectangle->ScaleVertices(m_fScale);
			}
		}

		vector<uint32> lodTable;
		GetLodTable(rectangles.size(), lodTable);
		for (uint16 i = 0;i < lodTable.size();i++)
		{
			uint32 nextFaceCount = lodTable[i];
			while (rectangles.size() > nextFaceCount)
			{
				PerformLod();
				rectangles.clear();
				MergeCoplanerBlockFace(rectangles);
			}
			if (fabs(m_fScale - 1.0f) > FLT_EPSILON)
			{
				for (RectanglePtr& rectangle : rectangles)
				{
					rectangle->ScaleVertices(m_fScale);
				}
			}
			m_lodRectangles[i] = rectangles;
		}
		*/

		//a rectangle generate two triangles
		while (m_rectangles.size() * 2 > nMaxTriangleCount)
		{
			PerformLod();
			MergeCoplanerBlockFace();
		}

	}

	void BMaxParser::GetLodTable(uint32 faceCount, vector<uint32>&lodTable)
	{
		if (faceCount >= 4000)
			lodTable.push_back(4000);
		if (faceCount >= 2000)
			lodTable.push_back(2000);
		if (faceCount >= 500)
			lodTable.push_back(500);
	}

	void BMaxParser::PerformLod()
	{
		m_nLodLevel ++;

		CShapeAABB aabb;
		map<int64, BMaxNodePtr> nodesMap;
		
		int width = (int)m_blockAABB.GetWidth();
		int height = (int)m_blockAABB.GetHeight();
		int depth = (int)m_blockAABB.GetDepth();

		for (int direction = 0; direction <= 3; direction++)
		{
			int x = (int)m_centerPos[0];
			while (x >= -1 && x <= width)
			{
				for (int y = 0; y <= height; y += 2)
				{
					int z = (int)m_centerPos[2];
					while (z >= -1 && z <= depth)
					{
						CalculateLodNode(nodesMap, x, y, z);
						(direction & 1) == 0 ? z += 2 : z -= 2;
					}
				}
				if (direction >= 2)
					x += 2;
				else
					x -= 2;
			}
		}
		vector<BMaxNodePtr>nodes;

		for (auto iter = nodesMap.begin();iter != nodesMap.end();iter++)
		{
			nodes.push_back(iter->second);
		}
		CalculateAABB(nodes);
	}

	void BMaxParser::CalculateAABB(vector<BMaxNodePtr>&nodes)
	{
		m_blockAABB.SetEmpty();
		for (auto item : nodes)
		{
			BMaxNode *node = item.get();
			m_blockAABB.Extend(Vector3((float)node->x, (float)node->y, (float)node->z));
		}

		m_centerPos = m_blockAABB.GetCenter();
		m_centerPos.y = 0;
		m_centerPos.x = (m_blockAABB.GetWidth() + 1.f) * 0.5f;
		m_centerPos.z = (m_blockAABB.GetDepth() + 1.f) * 0.5f;

		// OUTPUT_LOG("center %f %f %f\n", m_centerPos[0], m_centerPos[1], m_centerPos[2]);
		const auto& vMin = m_blockAABB.GetMin();
		int offset_x = (int)vMin.x;
		int offset_y = (int)vMin.y;
		int offset_z = (int)vMin.z;

		m_nodes.clear();
		for (auto node : nodes)
		{
			node->x -= offset_x;
			node->y -= offset_y;
			node->z -= offset_z;
			InsertNode(node);
		}

		// OUTPUT_LOG("nodes count %d\n", m_nodes.size());
		if (m_bAutoScale && m_nLodLevel == 0)
		{
			float fMaxLength = Math::Max(Math::Max(m_blockAABB.GetHeight(), m_blockAABB.GetWidth()), m_blockAABB.GetDepth()) + 1.f;
			m_fScale = CalculateScale(fMaxLength);
			if (m_bHasBoneBlock)
			{
				// for animated models, it is by default 1-2 blocks high, for static models, it is 0-1 block high. 
				m_fScale *= 2.f;
			}
		}
	}

	void BMaxParser::CalculateLodNode(map<int64, BMaxNodePtr> &nodeMap, int x, int y, int z)
	{
		int32 cnt = 0;

		map<int32, int32> colorMap;
		map<int32, int32> boneMap;

		for (int16 dx = 0; dx <= 1; dx++)
		{
			for (int16 dy = 0; dy <= 1; dy++)
			{
				for (int16 dz = 0; dz <= 1; dz++)
				{
					int16 cx = x + dx;
					int16 cy = y + dy;
					int16 cz = z + dz;

					if (cx >= 0 && cy >= 0 && cz >= 0)
					{
						BMaxNode *node = GetNode(cx, cy, cz);
						if (node)
						{
							cnt++;
							bool hasFind = false;
							int boneIndex = node->GetBoneIndex();
							if (boneIndex >= 0)
							{
								BMaxFrameNode *myBone = m_bones[boneIndex].get();
								for (auto iter = boneMap.begin(); iter != boneMap.end(); iter++)
								{
									BMaxFrameNode *bone = m_bones[iter->first].get();
									if (boneIndex == iter->first || bone->IsAncestorOf(myBone))
									{
										iter->second++;
										hasFind = true;
										break;
									}
									else if (myBone->IsAncestorOf(bone))
									{
										boneMap.insert(make_pair(boneIndex, iter->second + 1));
										boneMap.erase(iter);
										hasFind = true;
										break;
									}
								}
								if (!hasFind)
								{
									boneMap.insert(make_pair(boneIndex, 1));
								}
							}

							int32 myColor = node->GetColor();
							auto iter = colorMap.find(myColor);
							if (iter != colorMap.end())
							{
								iter->second++;
							}
							else
							{
								colorMap.insert(make_pair(myColor, 1));
							}
						}
					}
				}
			}
		}

		if (cnt >= 4)
		{
			uint16 newX = (x + 1) / 2;
			uint16 newY = y / 2;
			uint16 newZ = (z + 1) / 2;
			uint64 index = GetNodeIndex(newX, newY, newZ);

			BMaxNodePtr node(new BMaxNode(this, newX, newY, newZ, 0, 0));

			int32 color = 0;
			auto itColor = std::max_element(colorMap.begin(), colorMap.end(), [](const std::pair<int32, int32>& a, const std::pair<int32, int32>& b)
			{
				return a.second < b.second;
			});

			if (itColor != colorMap.end())
				color = itColor->first;
			node->SetColor(color);

			int32 boneIndex = -1;
			auto itBone = std::max_element(boneMap.begin(), boneMap.end(), [](const std::pair<int32, int32>& a, const std::pair<int32, int32>& b)
			{
				return a.second < b.second;
			});
			if (itBone != boneMap.end())
				boneIndex = itBone->first;
			node->SetBoneIndex(boneIndex);

			if (nodeMap.find(index) == nodeMap.end())
			{
				nodeMap.insert(make_pair(index, node));
			}
		}
	}

	ModelGeoset* BMaxParser::AddGeoset()
	{
		ModelGeoset geoset;
		memset(&geoset, 0, sizeof(geoset));
		geoset.id = (uint16_t)m_geosets.size();
		m_geosets.push_back(geoset);
		return &(m_geosets.back());
	}

	ModelRenderPass* BMaxParser::AddRenderPass()
	{
		ModelRenderPass pass;
		pass.cull = true;
		pass.texanim = -1;
		pass.color = -1;
		pass.opacity = -1;
		m_renderPasses.push_back(pass);
		return &(m_renderPasses.back());
	}

	BMaxAnimGenerator* BMaxParser::GetAnimGenerator()
	{
		if (!m_pAnimGenerator)
			m_pAnimGenerator = new BMaxAnimGenerator(this);
		return m_pAnimGenerator;
	}

	void BMaxParser::FillVerticesAndIndices()
	{
		if (m_blockModels.size() == 0)
		{
			return;
		}

		ModelGeoset* geoset = AddGeoset();
		ModelRenderPass* pass = AddRenderPass();
		pass->geoset = geoset->id;

		int32 nStartIndex = 0;

		CShapeAABB aabb;
		int total_count = 0;
		int nStartVertex = 0;

		int nRootBoneIndex = 0;
		for (uint32 i = 0; i < m_rectangles.size(); i++)
		{
			Rectangle *rectangle = m_rectangles[i].get();
			BlockVertexCompressed* pVertices = rectangle->GetVertices();

			int nVertices = 4;
			int nIndexCount = 6;

			if ((nIndexCount + geoset->icount) >= 0xffff)
			{
				// break geoset, if it is too big
				nStartIndex = (int32)m_indices.size();
				geoset = AddGeoset();
				pass = AddRenderPass();
				pass->geoset = geoset->id;
				pass->SetStartIndex(nStartIndex);
				geoset->SetVertexStart(total_count);
				nStartVertex = 0;
			}

			geoset->icount += nIndexCount;
			pass->indexCount += nIndexCount;

			uint8 vertex_weight = 0xff;

			for (int k = 0; k < nVertices; k++, pVertices++)
			{
				ModelVertex modelVertex;
				memset(&modelVertex, 0, sizeof(ModelVertex));
				pVertices->GetPosition(modelVertex.pos);
				pVertices->GetNormal(modelVertex.normal);
		
				modelVertex.color0 = pVertices->color2;
				//set bone and weight, only a single bone
				int nBoneIndex = rectangle->GetBoneIndexAt(k);
				// if no bone is found, use the default root bone
				modelVertex.bones[0] = (nBoneIndex != -1) ? nBoneIndex : nRootBoneIndex;
				modelVertex.weights[0] = vertex_weight;

				m_vertices.push_back(modelVertex);
				aabb.Extend(modelVertex.pos);
			}

			int start_index = nStartVertex;
			m_indices.push_back(start_index + 0);
			m_indices.push_back(start_index + 1);
			m_indices.push_back(start_index + 2);
			m_indices.push_back(start_index + 0);
			m_indices.push_back(start_index + 2);
			m_indices.push_back(start_index + 3);
			total_count += nVertices;
			nStartVertex += nVertices;
		}

		for (uint32 i = 0; i < m_blockModels.size(); i++)
		{
			BlockModel* model = m_blockModels.at(i);
			BMaxNode* node = m_blockModelsMapping[model];
			if (!node || node->isSolid())
				continue;

			int nVertices = model->GetVerticesCount();
			BlockVertexCompressed* pVertices = model->GetVertices();
			int nFace = model->GetFaceCount();

			int nIndexCount = nFace * 6;

			if ((nIndexCount + geoset->icount) >= 0xffff)
			{
				// break geoset, if it is too big
				nStartIndex = (int32)m_indices.size();
				geoset = AddGeoset();
				pass = AddRenderPass();
				pass->geoset = geoset->id;
				pass->SetStartIndex(nStartIndex);
				geoset->SetVertexStart(total_count);
				nStartVertex = 0;
			}

			geoset->icount += nIndexCount;
			pass->indexCount += nIndexCount;

			int nBoneIndex = node->GetBoneIndex();
			// if no bone is found, use the default root bone
			if (nBoneIndex == -1)
				nBoneIndex = nRootBoneIndex;
			uint8 vertex_weight = 0xff;

			for (int k = 0; k < nVertices; k++, pVertices++)
			{
				ModelVertex modelVertex;
				memset(&modelVertex, 0, sizeof(ModelVertex));
				pVertices->GetPosition(modelVertex.pos);
				modelVertex.pos *= m_fScale;
				pVertices->GetNormal(modelVertex.normal);
				modelVertex.color0 = pVertices->color2;
				//set bone and weight, only a single bone
				modelVertex.bones[0] = nBoneIndex;
				modelVertex.weights[0] = vertex_weight;

				m_vertices.push_back(modelVertex);
				aabb.Extend(modelVertex.pos);
			}

			for (int k = 0; k < nFace; k++)
			{
				int start_index = k * 4 + nStartVertex;
				m_indices.push_back(start_index + 0);
				m_indices.push_back(start_index + 1);
				m_indices.push_back(start_index + 2);
				m_indices.push_back(start_index + 0);
				m_indices.push_back(start_index + 2);
				m_indices.push_back(start_index + 3);
			}
			total_count += nVertices;
			nStartVertex += nVertices;
		}
		
		aabb.GetMin(m_minExtent);
		aabb.GetMax(m_maxExtent);
	}

	void BMaxParser::ClearModel()
	{
		m_geosets.clear();
		m_renderPasses.clear();
		m_indices.clear();
		m_vertices.clear();
	}

	void BMaxParser::FillParaXModelData(CParaXModel *pMesh)
	{
		if (pMesh == NULL)
		{
			return;
		}
		FillVerticesAndIndices();
		pMesh->m_objNum.nVertices = m_vertices.size();
		pMesh->m_objNum.nBones = m_bones.size();
		pMesh->m_objNum.nAnimations = m_bones.size() > 0 ? m_anims.size() : 0;
		pMesh->m_objNum.nIndices = m_indices.size();
		pMesh->m_header.minExtent = m_minExtent;
		pMesh->m_header.maxExtent = m_maxExtent;

		if (m_vertices.size() == 0)
			return;
		//pMesh->m_RenderMethod = CParaXModel::BMAX_MODEL;
		pMesh->SetRenderMethod(CParaXModel::BMAX_MODEL);
		pMesh->initVertices(m_vertices.size(), &(m_vertices[0]));
		pMesh->initIndices(m_indices.size(), &(m_indices[0]));

		if (m_bones.size() > 0)
		{
			pMesh->bones = new ParaEngine::Bone[m_bones.size()];
			for (int i = 0; i < (int)m_bones.size(); ++i)
			{
				Bone* pBone = m_bones[i]->GetBone();
				if (!pBone->rot.used && !pBone->scale.used && !pBone->trans.used)
				{
					pBone->SetStaticTransform(Matrix4::IDENTITY);
					pBone->bUsePivot = true;
				}
				pMesh->bones[i] = *pBone;
				if (pBone->nBoneID > 0)
					pMesh->m_boneLookup[pBone->nBoneID] = i;
				else if (pBone->IsAttachment())
				{
					pMesh->NewAttachment(true, pBone->GetAttachmentId(), i, pBone->bUsePivot ? pBone->pivot : Vector3::ZERO);
				}
			}
		}

		if (m_bones.size() > 0)
		{
			if (m_anims.size() > 0)
			{
				pMesh->anims = new ModelAnimation[m_anims.size()];
				memcpy(pMesh->anims, &(m_anims[0]), sizeof(ModelAnimation)*m_anims.size());
			}
			pMesh->animBones = true;
			pMesh->animated = true;
		}
		else
		{
			pMesh->animBones = false;
			pMesh->animated = false;
		}

		// add geoset (faces & indices)
		{
			pMesh->geosets = m_geosets;
			pMesh->passes = m_renderPasses;
		}

		if (pMesh->geosets.size() > 0)
		{
			pMesh->showGeosets = new bool[pMesh->geosets.size()];
			memset(pMesh->showGeosets, true, pMesh->geosets.size()*sizeof(bool));
		}
	}

	int BMaxParser::GetBoneIndex(uint16 x, uint16 y, uint16 z)
	{
		int nBoneIndex = -1;
		BMaxNode* pBone = GetNode(x,y,z);
		if (pBone && pBone->ToBoneNode())
		{
			nBoneIndex = pBone->GetBoneIndex();
		}
		return nBoneIndex;
	}

	bool BMaxParser::ReadValue(BMaxXMLElement* node, const char* name, int32_t& value)
	{
		if (node)
		{
			const char* attr = node->Attribute(name);
			if (attr)
			{
				value = atoi(attr);
				return true;
			}
		}
		return false;
	}
	bool BMaxParser::ReadValue(BMaxXMLElement* node, const char* name, float& value)
	{
		if (node)
		{
			const char* attr = node->Attribute(name);
			if (attr)
			{
				value = (float)atof(attr);
				return true;
			}
		}
		return false;
	}
	bool BMaxParser::ReadValue(BMaxXMLElement* node, const char* name, Vector3& value)
	{
		if (node)
		{
			const char* attr = node->Attribute(name);
			std::string attr_str;
			if (attr)
			{
				attr_str = attr;
				std::vector<std::string> ids;
				StringHelper::split(attr_str, ",", ids);
				if (ids.size() > 2)
				{
					value.x = (float)atof(ids[0].c_str());
					value.y = (float)atof(ids[1].c_str());
					value.z = (float)atof(ids[2].c_str());
					return true;
				}
			}
		}
		return false;
	}
	bool BMaxParser::ReadValue(BMaxXMLElement* node, const char* name, std::string& value)
	{
		if (node)
		{
			const char* attr = node->Attribute(name);
			if (attr)
			{
				value = attr;
				return true;
			}
		}
		return false;
	}
	bool BMaxParser::ReadValue(BMaxXMLElement* node, const char* name, Vector4& value)
	{
		if (node)
		{
			const char* attr = node->Attribute(name);
			std::string attr_str;
			if (attr)
			{
				attr_str = attr;
				std::vector<std::string> ids;
				StringHelper::split(attr_str, ",", ids);
				if (ids.size() > 3)
				{
					value.x = (float)atof(ids[0].c_str());
					value.y = (float)atof(ids[1].c_str());
					value.z = (float)atof(ids[2].c_str());
					value.w = (float)atof(ids[3].c_str());
					return true;
				}
			}
		}
		return false;
	}

	int BMaxParser::GetNameAppearanceCount(const std::string& name, bool bAdd /*= true*/)
	{
		int nLastAppearance = 0;
		auto iter = m_name_occurances.find(name);
		if (iter != m_name_occurances.end())
		{
			nLastAppearance = iter->second;
		}
		if (bAdd)
		{
			m_name_occurances[name] = nLastAppearance + 1;
		}
		return nLastAppearance;
	}

	void BMaxParser::ParseBlockAnimations(BMaxXMLDocument& doc)
	{
		BMaxXMLElement* element = doc.FirstChildElement("pe:blocktemplate");
		if (element != NULL)
		{
			BMaxXMLElement* blockanimations_element = element->FirstChildElement("pe:blockanimations");
			if (blockanimations_element != NULL)
			{
				for (BMaxXMLNode* pChild = blockanimations_element->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
				{
					BMaxXMLElement* pElement = pChild->ToElement();
					if (pElement)
					{
						ParseBlockAnimationSet(pElement);
					}
				}
			}
		}
	}
	void BMaxParser::ParseBlockAnimationSet(BMaxXMLElement* node)
	{
		if (node == NULL)
		{
			return;
		}
		ModelAnimation anim;
		memset(&anim, 0, sizeof(ModelAnimation));
		anim.timeStart = 0;
		int32_t duration;
		if (ReadValue(node, "duration", duration))
		{
			anim.timeEnd = duration;

			m_bHasAnimation = true;
		}
		anim.animID = m_anims.size();
		m_anims.push_back(anim);

		for (BMaxXMLNode* pChild = node->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
		{
			BMaxXMLElement* pElement = pChild->ToElement();
			if (pElement)
			{
				ParseBlockAnimation(pElement);
			}
		}

	}
	void BMaxParser::ParseBlockAnimation(BMaxXMLElement* node)
	{
		if (node == NULL)
		{
			return;
		}
		int x;
		int y;
		int z;
		auto index = GetIndexFromXmlElement(node, "frame_id", x, y, z);
		if (index > -1)
		{
			int nIndex = 0;
			for (BMaxXMLNode* pChild = node->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
			{
				BMaxXMLElement* pElement = pChild->ToElement();
				if (pElement)
				{
					ParseBlockAnimationKeys(x, y, z, pElement, nIndex);
					nIndex++;
				}
			}
		}
	}
	void BMaxParser::ParseBlockAnimationKeys(uint16 x, uint16 y, uint16 z, BMaxXMLElement* node, int nIndex)
	{
		int bone_index = GetBoneIndex(x, y, z);
		if (bone_index > -1)
		{
			ParaEngine::Bone & bone = *(m_bones[bone_index]->GetBone());
			bone.flags = ParaEngine::Bone::BONE_USE_PIVOT;
			bone.calc = true;
			std::string value;
			if (ReadValue(node, "property", value))
			{
				for (BMaxXMLNode* pChild = node->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
				{
					BMaxXMLElement* pElement = pChild->ToElement();
					if (pElement)
					{
						ParseBlockAnimationKey(pElement, &bone, value);
					}
				}
				int nAnimId = nIndex;
				bone.scale.ranges.resize(nAnimId + 1, AnimRange(0, 0));
				bone.trans.ranges.resize(nAnimId + 1, AnimRange(0, 0));
				bone.rot.ranges.resize(nAnimId + 1, AnimRange(0, 0));
				bone.scale.ranges[nAnimId] = AnimRange(0, bone.scale.times.size() - 1);
				bone.trans.ranges[nAnimId] = AnimRange(0, bone.trans.times.size() - 1);
				bone.rot.ranges[nAnimId] = AnimRange(0, bone.rot.times.size() - 1);
			}
		}
	}
	void BMaxParser::ParseBlockAnimationKey(BMaxXMLElement* node, Bone* bone, const std::string propertyType)
	{
		if (node == NULL || bone == NULL)
		{
			return;
		}
		if (propertyType == "position")
		{
			bone->trans.used = true;
			int time;
			Vector3 value;
			if (ReadValue(node, "time", time) && ReadValue(node, "value", value))
			{
				bone->trans.times.push_back(time);
				bone->trans.data.push_back(value);
			}
		}
		if (propertyType == "rotation")
		{
			bone->rot.used = true;
			int time;
			Vector4 value;
			if (ReadValue(node, "time", time) && ReadValue(node, "value", value))
			{
				bone->rot.times.push_back(time);
				Quaternion rot(value.x, value.y, value.z, value.w);
				bone->rot.data.push_back(rot);
			}
		}
		if (propertyType == "scale")
		{
			bone->scale.used = true;
			int time;
			Vector3 value;
			if (ReadValue(node, "time", time) && ReadValue(node, "value", value))
			{
				bone->scale.times.push_back(time);
				bone->scale.data.push_back(value);
			}
		}
	}

	BMaxFrameNode* BMaxParser::GetFrameNode(int16 x, int16 y, int16 z)
	{
		BMaxNode* pNode = GetBMaxNode(x, y, z);
		if (pNode)
			return pNode->ToBoneNode();
		else
			return NULL;
	}

	void BMaxParser::ParseBlockFrames()
	{
		// calculate parent bones
		for (auto bone : m_bones)
			bone->UpdatePivot();
		// calculate parent bones
		for (auto bone : m_bones)
			bone->GetParentBone(true);
		// set bone name
		for (auto bone : m_bones)
			bone->AutoSetBoneName();

		GetAnimGenerator()->FillAnimations();

		// create animation
		//CreateDefaultAnimations();
	}

	void BMaxParser::CalculateBoneWeightForBlock(BMaxFrameNode* pBoneNode, BMaxNode* node, bool bMustBeSameColor)
	{
#if 0
		if (node && !node->HasBoneWeight())
		{
			if (node->template_id != BoneBlockId)
			{
				if (!bMustBeSameColor || (node->GetColor() == pBoneNode->GetColor()))
				{
					node->SetBoneIndex(pBoneNode->GetBoneIndex());
					for (int i = 0; i < 6; i++)
					{
						CalculateBoneWeightForBlock(pBoneNode, node->GetNeighbour((BlockDirection::Side)i), bMustBeSameColor);
					}
				}
			}
		}
#else
		std::stack<BMaxNode*> nodeStack;
		if (node)
			nodeStack.push(node);

		while (!nodeStack.empty())
		{
			auto cur = nodeStack.top();
			nodeStack.pop();

			if (!cur->HasBoneWeight()
				&& cur->template_id != BoneBlockId
				&& (!bMustBeSameColor || cur->GetColor() == pBoneNode->GetColor()))
			{
				cur->SetBoneIndex(pBoneNode->GetBoneIndex());
				for (int i = 0; i < 6; i++)
				{
					auto neighbour = cur->GetNeighbour((BlockDirection::Side)i);
					if (neighbour)
						nodeStack.push(neighbour);
				}

			}

		}
#endif
	}

	void BMaxParser::CalculateBoneSkin(BMaxFrameNode* pBoneNode)
	{
		if (pBoneNode->HasBoneWeight())
			return;
		// ensures that parent bone node is always calculated before child node. 
		BMaxFrameNode* pParentBoneNode = pBoneNode->GetParent();
		if (pParentBoneNode && !pParentBoneNode->HasBoneWeight())
			CalculateBoneSkin(pParentBoneNode);

		// add current bone to skin.
		pBoneNode->SetBoneIndex(pBoneNode->GetBoneIndex());

		// calculate bone color if not. 
		DWORD bone_color = pBoneNode->GetColor();

		// add other blocks connected to the bone recursively. 
		BlockDirection::Side mySide = BlockDirection::GetBlockSide(pBoneNode->block_data);
		for (int i = 0; i < 6; i++)
		{
			BlockDirection::Side side = BlockDirection::GetBlockSide(i);
			if (mySide != side)
			{
				CalculateBoneWeightForBlock(pBoneNode, pBoneNode->GetNeighbour(side));
			}
		}
	}
	
	int BMaxParser::FindRootBoneIndex()
	{
		for (auto pBone : m_bones)
		{
			if (!pBone->HasParent())
				return pBone->GetBoneIndex();
		}
		return 0;
	}


	void BMaxParser::CalculateBoneWeightFromNeighbours(BMaxNode* node)
	{
		if (node != NULL && !node->HasBoneWeight())
		{
			bool bFoundBone = false;
			for (int i = 0; i < 6 && !bFoundBone; i++)
			{
				BlockDirection::Side side = BlockDirection::GetBlockSide(i);
				BMaxNode* pNeighbourNode = node->GetNeighbour(side);
				if (pNeighbourNode && pNeighbourNode->HasBoneWeight())
				{
					node->SetBoneIndex(pNeighbourNode->GetBoneIndex());
					bFoundBone = true;
				}
			}
			if (bFoundBone)
			{
				for (int i = 0; i < 6; i++)
				{
					BlockDirection::Side side = BlockDirection::GetBlockSide(i);
					BMaxNode* pNeighbourNode = node->GetNeighbour(side);
					if (pNeighbourNode && !pNeighbourNode->HasBoneWeight())
					{
						CalculateBoneWeightFromNeighbours(pNeighbourNode);
					}
				}
			}
		}
	}

	void BMaxParser::CalculateBoneWeights()
	{
		// pass 1: calculate all blocks directly connected to bone block and share the same bone color
		for (auto bone: m_bones)
		{
			CalculateBoneSkin(bone.get());
		}

		// pass 2: from remaining blocks, calculate blocks which are connected to bones, but with different colors to those bones. 
		for (auto bone : m_bones)
		{
			BlockDirection::Side mySide = BlockDirection::GetBlockSide(bone->block_data);
			for (int i = 0; i < 6; i++)
			{
				BlockDirection::Side side = BlockDirection::GetBlockSide(i);
				if (mySide != side)
				{
					CalculateBoneWeightForBlock(bone.get(), bone->GetNeighbour(side), false);
				}
			}
		}

		// pass 3: from remaining blocks, calculate blocks which are connected to other binded blocks, but with different colors to those blocks.
		for (auto& item : m_nodes)
		{
			CalculateBoneWeightFromNeighbours(item.second.get());
		}
	}

	void BMaxParser::CreateDefaultAnimations()
	{
		m_bHasAnimation = true;

		// static animation 0
		ModelAnimation anim;
		memset(&anim, 0, sizeof(ModelAnimation));
		anim.timeStart = 0;
		anim.timeEnd = 0;
		anim.animID = 0;
		m_anims.push_back(anim);

		// walk animations 
		AutoAddWalkAnimation(ANIM_WALK, 4000, 5000, 4.0f, true);
		AutoAddWalkAnimation(ANIM_WALKBACKWARDS, 13000, 14000, 4.0f, false);
	}

	bool BMaxParser::IsFileNameRecursiveLoaded(const std::string& filename)
	{
		if (!filename.empty())
		{
			if (GetFilename() == filename)
				return true;
			else if (GetParent())
			{
				return GetParent()->IsFileNameRecursiveLoaded(filename);
			}
		}
		return false;
	}

	void BMaxParser::AddAnimation(const ModelAnimation& anim)
	{
		m_anims.push_back(anim);
	}

	int BMaxParser::GetAnimationsCount()
	{
		return (int)m_anims.size();
	}

	void BMaxParser::AutoAddWalkAnimation(int nAnimID, int nStartTime, int nEndTime, float fMoveSpeed, bool bMoveForward)
	{
		ModelAnimation anim;
		anim.timeStart = nStartTime;
		anim.timeEnd = nEndTime;
		anim.animID = nAnimID;
		anim.moveSpeed = fMoveSpeed;
		int animIndex = (int)m_anims.size();
		int nAnimLength = anim.timeEnd - anim.timeStart;
		for (auto bone : m_bones)
		{
			Bone* pBone = bone->GetBone();
			if (pBone->GetName().find("wheel") != string::npos)
			{
				Vector3 vAxis = bone->GetAxis();
				Quaternion q;
				pBone->rot.used = true;
				int nFirstRotSize = (int)pBone->rot.times.size();

				// for wheels, add rotation animation. 
				q.FromAngleAxis(Radian(0.f), vAxis);
				pBone->rot.times.push_back(anim.timeStart);
				pBone->rot.data.push_back(q);

				float fRotSign = (vAxis.z > 0) ? 1.f : -1.f;
				if (!bMoveForward)
					fRotSign = -fRotSign;
				q.FromAngleAxis(Radian(3.14f*fRotSign), vAxis);
				pBone->rot.times.push_back(anim.timeStart + nAnimLength / 2);
				pBone->rot.data.push_back(q);

				q.FromAngleAxis(Radian(6.28f*fRotSign), vAxis);
				pBone->rot.times.push_back(anim.timeStart + nAnimLength);
				pBone->rot.data.push_back(q);

				pBone->rot.ranges.resize(animIndex + 1, AnimRange(0, 0));
				pBone->rot.ranges[animIndex] = AnimRange(nFirstRotSize, max(nFirstRotSize, (int)pBone->rot.times.size() - 1));
			}
		}
		m_anims.push_back(anim);
	}

	CParaXModel* BMaxParser::CreateGetRefModel(const std::string& sFilename)
	{
		auto it = m_refModels.find(sFilename);
		if (it != m_refModels.end())
		{
			return it->second.get();
		}
		if (CParaFile::GetFileExtension(sFilename) == "bmax")
		{
			ref_ptr<CParaXModel> pModel;

			std::string sFullFilename = CGlobals::GetWorldInfo()->GetWorldDirectory() + sFilename;
			CParaFile file;
			if (file.OpenFile(sFullFilename.c_str()))
			{
				BMaxParser parser(sFilename.c_str(), this);
				parser.Load(file.getBuffer(), file.getSize());
				pModel.reset(parser.ParseParaXModel());
			}
			else
			{
				OUTPUT_LOG("warn: can not find referenced bmax file %s \n", sFilename.c_str());
			}

			m_refModels[sFilename] = pModel;
			return pModel.get();
		}
		return NULL;
	}

	void BMaxParser::SetMergeCoplanerBlockFace(bool val)
	{
		m_bMergeCoplanerBlockFace = val;
	}


}


```