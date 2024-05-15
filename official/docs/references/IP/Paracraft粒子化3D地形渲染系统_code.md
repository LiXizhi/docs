```cpp
//-----------------------------------------------------------------------------
// Class:	Block World Provider
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Date:	2014.2.6
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "ShapeAABB.h"
#include "ShapeSphere.h"
#ifdef USE_TINYXML2
#include <tinyxml2.h>
#else
#include <tinyxml.h>
#endif
#include "BlockModel.h"
#include "BlockConfig.h"
#include "BlockCommon.h"
#include "BlockRegion.h"
#include "BlockLightGridBase.h"
#include "TextureEntity.h"
#include "BlockWorld.h"
#include "SceneObject.h"
#include "BipedObject.h"

using namespace ParaEngine;

/** default render distance in blocks */
#define DEFAULT_RENDER_BLOCK_DISTANCE	96

namespace ParaEngine
{
	float CBlockWorld::g_verticalOffset = 0;

	inline int64_t GetBlockSparseIndex(int64_t bx, int64_t by, int64_t bz)
	{
		return by * 30000 * 30000 + bx * 30000 + bz;
	}
}

CBlockWorld::CBlockWorld()
	:m_curChunkIdW(-1), m_activeChunkDim(0), m_lastChunkIdW(-1), m_lastChunkIdW_RegionCache(-1), m_lastViewCheckIdW(0), m_dwBlockRenderMethod(BLOCK_RENDER_FAST_SHADER), m_sunIntensity(1), m_isVisibleChunkDirty(true), m_curRegionIdX(0), m_curRegionIdZ(0),
m_pLightGrid(new CBlockLightGridBase(this)), m_bReadOnlyWorld(false), m_bIsRemote(false), m_bIsServerWorld(false), m_bCubeModePicking(false), m_isInWorld(false), m_bSaveLightMap(false), 
m_bUseAsyncLoadWorld(true), m_bRenderBlocks(true), m_group_by_chunk_before_texture(false), m_is_linear_torch_brightness(false), m_maxCacheRegionCount(0),
m_minWorldPos(0, 0, 0), m_maxWorldPos(0xffff, 0xffff, 0xffff), m_minRegionX(0), m_minRegionZ(0), m_maxRegionX(63), m_maxRegionZ(63)
{
	// 256 blocks, so that it never wraps
	m_activeChunkDimY = 16; 
	SetActiveChunkRadius(12);
	m_blockTemplatesArray.resize(256, 0);

	GenerateLightBrightnessTable(m_is_linear_torch_brightness);
	// resize region
	m_pRegions = new BlockRegionPtr[64 * 64];
	memset(m_pRegions, 0, sizeof(BlockRegionPtr) * 64 * 64);

	SetRenderDist(DEFAULT_RENDER_BLOCK_DISTANCE);

	m_selectedBlockMap.resize(10);
	for (unsigned int i = 0; i < m_selectedBlockMap.size(); ++i)
	{
		auto& select_group = m_selectedBlockMap[i];
		select_group.m_color = LinearColor(0.3f, 0.3f, 0.3f, 0.4f);

		if (i % 2 == 1)
		{
			select_group.m_fScaling = 1.01f;
			select_group.m_bEnableBling = true;
		}
		else
		{
			select_group.m_fScaling = 1.f;
		}
		if (i == 4 || i == 5)
		{
			select_group.m_bOnlyRenderClickableArea = true;
			select_group.m_fScaling = 0.99f;
			select_group.m_bEnableBling = false;
		}
		if (i == BLOCK_GROUP_ID_WIREFRAME)
		{
			select_group.m_bWireFrame = true;
			select_group.m_color = LinearColor(0.2f, 0.2f, 0.2f, 0.7f);
			select_group.m_fScaling = 1.01f;
		}
		else if (i == BLOCK_GROUP_ID_HIGHLIGHT)
		{
			select_group.m_bEnableBling = true;
			select_group.m_fScaling = 1.01f;
		}
	}

	RenderableChunk::StaticInit();
}

CBlockWorld::~CBlockWorld()
{
	m_isInWorld = false;
	SAFE_DELETE(m_pLightGrid);
	ClearAllBlockTemplates();
	SAFE_DELETE_ARRAY(m_pRegions);
}

void ParaEngine::CBlockWorld::EnterWorld(const string& sWorldDir, float x, float y, float z)
{
	if (m_isInWorld)
		return;

	if (!sWorldDir.empty())
		m_worldInfo.ResetWorldName(sWorldDir);
	else
		m_worldInfo.ResetWorldName(CWorldInfo::GetSingleton().GetDefaultWorldConfigName());

	//init data
	// only use more region cache on 64 bits system.
	m_maxCacheRegionCount = (sizeof(void*) > 4) ? 16 : 9;

	/** only cache 4 region for networked world*/
	if(IsRemote())
		m_maxCacheRegionCount = 4;

	m_minActiveChunkId_ws.SetValue(0);

	// LoadBlockTemplateData();

	OUTPUT_LOG("Enter Block World %s : max region cache %d\n", m_worldInfo.GetWorldName().c_str(), m_maxCacheRegionCount);
	GetLightGrid().OnEnterWorld();

	OnViewCenterMove(x, y, z);

	m_isInWorld = true;
}

void CBlockWorld::SaveToFile(bool saveToTemp)
{
	// SaveBlockTemplateData();

	for (std::map<int, BlockRegion*>::iterator iter = m_regionCache.begin(); iter != m_regionCache.end(); iter++)
	{
		iter->second->SaveToFile();
	}
#ifdef PARAENGINE_CLIENT
	if (!saveToTemp)
	{
		HANDLE hFind = INVALID_HANDLE_VALUE;
		WIN32_FIND_DATA ffd;

		std::string lastSaveDir = m_worldInfo.GetBlockGameSaveDir(true);
		lastSaveDir.append("*");
		hFind = FindFirstFile(lastSaveDir.c_str(), &ffd);
		if (hFind == INVALID_HANDLE_VALUE)
			return;

		std::string gameSaveDir = m_worldInfo.GetBlockGameSaveDir(false);
		lastSaveDir = m_worldInfo.GetBlockGameSaveDir(true);

		std::string current;
		std::string src;
		do
		{
			if (!(ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
			{
				ffd.cFileName;
				current.clear();
				current.assign(ffd.cFileName);

				int32_t size = current.size();
				if ((current[size - 3] == 'x' && current[size - 2] == 'm' && current[size - 1] == 'l')
					|| current[size - 3] == 'r' && current[size - 2] == 'a' && current[size - 1] == 'w')
				{
					current.clear();
					current.append(gameSaveDir);
					current.append(ffd.cFileName);

					src.clear();
					src.append(lastSaveDir);
					src.append(ffd.cFileName);
					CParaFile::CopyFile(src.c_str(), current.c_str(), true);
				}
			}
		} while (FindNextFile(hFind, &ffd) != 0);
	}
#endif
}

void ParaEngine::CBlockWorld::LeaveWorld()
{
	Scoped_WriteLock<BlockReadWriteLock> Lock_(GetReadWriteLock());

	m_curRegionIdX = 0;
	m_curRegionIdZ = 0;

	m_curChunkIdW.SetValue(-1);
	m_lastChunkIdW.SetValue(-1);
	m_lastChunkIdW_RegionCache.SetValue(-1);
	m_lastViewCheckIdW = Uint16x3(0);

	std::map<int, BlockRegion*>::iterator iter;
	while ((iter = m_regionCache.begin()) != m_regionCache.end())
	{
		BlockRegion* pRegion = iter->second;
		UnloadRegion(pRegion, false);
	}

	for (int i = 0; i<m_activeChunkDim; i++)
	{
		for (int j = 0; j<m_activeChunkDimY; j++)
		{
			for (int k = 0; k<m_activeChunkDim; k++)
			{
				GetActiveChunk(i, j, k).OnLeaveWorld();
			}
		}
	}

	m_visibleChunks.clear();

	ClearAllBlockTemplates();

	m_isInWorld = false;

	GetLightGrid().OnLeaveWorld();

	DeselectAllBlock(-BLOCK_GROUP_ID_MAX);
}

bool ParaEngine::CBlockWorld::MatchTemplateAttribute(uint16_t templateId, BlockTemplate::BlockAttrubiteFlag flag)
{
	BlockTemplate *pTemplate = GetBlockTemplate(templateId);
	if (pTemplate)
	{
		return pTemplate->IsMatchAttribute(flag);
	}
	return false;
}

float ParaEngine::CBlockWorld::GetLightBrightnessFloat(uint8_t brightness)
{
	return m_lightBrightnessTableFloat[brightness];
}

uint8_t ParaEngine::CBlockWorld::GetLightBrightnessInt(uint8_t brightness)
{
	return m_lightBrightnessTableInt[brightness];
}

float ParaEngine::CBlockWorld::GetLightBrightnessLinearFloat(uint8_t brightness)
{
	return m_lightBrightnessLinearTableFloat[brightness];
}

float ParaEngine::CBlockWorld::GetSunIntensity()
{
	return m_sunIntensity;
}

void ParaEngine::CBlockWorld::UpdateAllActiveChunks()
{
	m_lastChunkIdW.SetValue(-1);
	m_lastChunkIdW_RegionCache.SetValue(-1);
	m_lastViewCheckIdW = Uint16x3(0);
	UpdateActiveChunk();
}

void ParaEngine::CBlockWorld::SetActiveChunkRadius(int nActiveChunkRadius)
{
	if (nActiveChunkRadius >= 3 && nActiveChunkRadius <= 64)
	{
		// m_activeChunkDim must be a odd value
		int nActiveChunkDim = 2 * (nActiveChunkRadius + 1) + 1;
		if (nActiveChunkDim != m_activeChunkDim)
		{
			if (nActiveChunkDim>m_activeChunkDim)
			{
				m_activeChunks.resize(nActiveChunkDim * m_activeChunkDimY * nActiveChunkDim, NULL);
				for (int i = 0; i < (int)(m_activeChunks.size()); ++i)
				{
					if (m_activeChunks[i] == NULL)
					{
						m_activeChunks[i] = new RenderableChunk();
					}
				}
				m_activeChunkDim = nActiveChunkDim;

				if (IsInBlockWorld())
					UpdateAllActiveChunks();
			}
		}
	}
	else
	{
		OUTPUT_LOG("warning: SetActiveChunkRadius %d is too big or too small\n", nActiveChunkRadius);
	}
}

void CBlockWorld::SetRenderDist(int nValue)
{
	SetActiveChunkRadius((int)((float)nValue / (float)BlockConfig::g_chunkBlockDim + 0.5f));
	m_nRenderDistance = min(nValue, m_activeChunkDim*BlockConfig::g_chunkBlockDim / 2);
	GetLightGrid().SetLightGridSize((int)(m_nRenderDistance * 2 / BlockConfig::g_chunkBlockDim) + 2);

	int nMinRegionCount = ((int)(m_nRenderDistance / 512) + 2) ^ 2;

	if (m_maxCacheRegionCount < nMinRegionCount)
		m_maxCacheRegionCount = nMinRegionCount;
}

int ParaEngine::CBlockWorld::GetRenderDist()
{
	return m_nRenderDistance;
}

const Uint16x3& ParaEngine::CBlockWorld::GetEyeBlockId()
{
	return m_curCamBlockId;
}


void ParaEngine::CBlockWorld::SetEyeBlockId(const Uint16x3& eyePos)
{
	m_curCamBlockId = eyePos;
	m_curCamChunkId.x = m_curCamBlockId.x / 16;
	m_curCamChunkId.y = m_curCamBlockId.y / 16;
	m_curCamChunkId.z = m_curCamBlockId.z / 16;
}

const Uint16x3& ParaEngine::CBlockWorld::GetEyeChunkId()
{
	return m_curCamChunkId;
}

const Int16x3 ParaEngine::CBlockWorld::GetMinActiveChunkId()
{
	return m_minActiveChunkId_ws;
}

void ParaEngine::CBlockWorld::GetCurrentCenterChunkId(Int16x3& oResult)
{
	oResult = m_curChunkIdW;
}

CBlockLightGridBase& ParaEngine::CBlockWorld::GetLightGrid()
{
	return *m_pLightGrid;
}

void ParaEngine::CBlockWorld::SetBlockRenderMethod(BlockRenderMethod method)
{
}


BlockRegion* ParaEngine::CBlockWorld::CreateGetRegion(uint16_t x, uint16_t y, uint16_t z)
{
	if (!m_isInWorld || y >= BlockConfig::g_regionBlockDimY)
		return NULL;

	uint16_t region_x = x >> 9;
	uint16_t region_z = z >> 9;
	return CreateGetRegion(region_x, region_z);
}

BlockRegion* CBlockWorld::CreateGetRegion(uint16_t region_x, uint16_t region_z)
{
	BlockRegion* pRegion = GetRegion(region_x, region_z);
	if (pRegion)
	{
		return pRegion;
	}
	else if (region_x <= m_maxRegionX && region_z <= m_maxRegionZ && region_x>=m_minRegionX && region_z>=m_minRegionZ)
	{
		pRegion = new BlockRegion(region_x, region_z, this);
		if (pRegion)
		{
			char name[128];
			snprintf(name, 128, "region_%d_%d", pRegion->GetRegionX(), pRegion->GetRegionZ());
			pRegion->SetIdentifier(name);
			OUTPUT_LOG("Load region: %d %d, total regions: %d\n", pRegion->GetRegionX(), pRegion->GetRegionZ(), (int)(m_regionCache.size()));
			{
				Scoped_WriteLock<BlockReadWriteLock> Lock_(GetReadWriteLock());
				m_pRegions[pRegion->GetPackedRegionIndex()] = pRegion;
				m_regionCache[pRegion->GetPackedRegionIndex()] = pRegion;
			}
			pRegion->Load();
		}
		return pRegion;
	}
	else
		return NULL;
}

void ParaEngine::CBlockWorld::ResetAllLight()
{
	for (auto& item : m_regionCache)
	{
		item.second->ClearAllLight();
	}

	auto& lightGrid = GetLightGrid();

	lightGrid.OnEnterWorld();
}

bool ParaEngine::CBlockWorld::UnloadRegion(uint16_t block_x, uint16_t block_y, uint16_t block_z, bool bAutoSave /*= true*/)
{
	uint16_t rx, ry, rz;
	BlockRegion* pRegion = GetRegion(block_x, block_y, block_z, rx, ry, rz);
	if (pRegion){
		UnloadRegion(pRegion, bAutoSave);
		return true;
	}
	return false;
}

void CBlockWorld::UnloadRegion(BlockRegion* pRegion, bool bAutoSave)
{
	if (pRegion)
	{
		if (m_pRegions[pRegion->GetPackedRegionIndex()] == pRegion)
		{
			if (!IsRemote() && bAutoSave && !IsReadOnly() && pRegion->IsModified())
				pRegion->SaveToFile();
			OnUnLoadBlockRegion(pRegion->GetRegionX(), pRegion->GetRegionZ());
			Scoped_WriteLock<BlockReadWriteLock> Lock_(GetReadWriteLock());
			m_pRegions[pRegion->GetPackedRegionIndex()] = NULL;
			m_regionCache.erase(pRegion->GetPackedRegionIndex());
			pRegion->OnUnloadWorld();
		}
		else
		{
			OUTPUT_LOG("error: invalid UnloadRegion\n");
		}
		delete pRegion;
	}
}

BlockRegion* CBlockWorld::GetRegion(uint16_t x, uint16_t y, uint16_t z, uint16_t& rs_x, uint16_t& rs_y, uint16_t& rs_z)
{
	if (m_isInWorld && y < BlockConfig::g_regionBlockDimY)
	{
		uint16_t region_x = x >> 9;
		uint16_t region_z = z >> 9;

		if (region_x < 64 && region_z < 64)
		{
			BlockRegion* pRegion = m_pRegions[region_x + (region_z << 6)];
			if (pRegion)
			{
				rs_x = x & 0x1ff;
				rs_y = y & 0xff;
				rs_z = z & 0x1ff;
				return pRegion;
			}
		}
	}
	return NULL;
}

BlockRegion* CBlockWorld::GetRegion(uint16_t region_x, uint16_t region_z)
{
	if (region_x < 64 && region_z < 64)
		return m_pRegions[region_x + (region_z << 6)];
	else
		return NULL;
}

float CBlockWorld::GetVerticalOffset()
{
	return g_verticalOffset;
}

void CBlockWorld::SetVerticalOffset(float offset)
{
	g_verticalOffset = offset;
}

int32_t CBlockWorld::GetActiveChunkDim()
{
	return m_activeChunkDim;
}

int32_t CBlockWorld::GetActiveChunkDimY()
{
	return m_activeChunkDimY;
}


bool CBlockWorld::IsInBlockWorld()
{
	return m_isInWorld;
}

void CBlockWorld::SetReadOnly(bool bValue)
{
	m_bReadOnlyWorld = bValue;
}

bool CBlockWorld::IsReadOnly()
{
	return m_bReadOnlyWorld;
}


void ParaEngine::CBlockWorld::ClearAllBlockTemplates()
{
	for (auto& it : m_blockTemplates)
	{
		if (it.first < 256){
			m_blockTemplatesArray[it.first] = NULL;
		}
		SAFE_DELETE(it.second);
	}
	m_blockTemplates.clear();
}


void CBlockWorld::SaveBlockTemplateData()
{
#ifdef USE_TINYXML2
	using namespace tinyxml2;
	tinyxml2::XMLDocument doc;

	XMLDeclaration* decl = doc.NewDeclaration(nullptr);
	doc.LinkEndChild(decl);

	XMLElement* root = doc.NewElement("BlockTemplates");
	doc.LinkEndChild(root);
	for (std::map<uint16_t, BlockTemplate*>::iterator it = m_blockTemplates.begin(); it != m_blockTemplates.end(); it++)
	{
		BlockTemplate* pTemplate = it->second;

		XMLElement* pNewItem = doc.NewElement("Template");
		pNewItem->SetAttribute("Id", pTemplate->GetID());
		pNewItem->SetAttribute("Att", pTemplate->GetAttFlag());
		pNewItem->SetAttribute("Priority", pTemplate->GetRenderPriority());
		TextureEntity* pTex = pTemplate->GetTexture0();
		if (pTex)
		{
			pNewItem->SetAttribute("Tex0", pTex->GetLocalFileName().c_str());

			pTex = pTemplate->GetTexture1();
			if (pTex)
			{
				pNewItem->SetAttribute("Tex1", pTex->GetLocalFileName().c_str());
			}

			pTex = pTemplate->GetNormalMap();
			if (pTex)
			{
				pNewItem->SetAttribute("NorMap", pTex->GetLocalFileName().c_str());
			}
		}
		root->LinkEndChild(pNewItem);
	}
	std::string fileName = m_worldInfo.GetBlockTemplateFileName(true);
	doc.SaveFile(fileName.c_str());
#else
	TiXmlDocument doc;

	TiXmlDeclaration* decl = new TiXmlDeclaration("1.0", "", "");
	doc.LinkEndChild(decl);

	TiXmlElement* root = new TiXmlElement("BlockTemplates");
	doc.LinkEndChild(root);
	for (std::map<uint16_t, BlockTemplate*>::iterator it = m_blockTemplates.begin(); it != m_blockTemplates.end(); it++)
	{
		BlockTemplate* pTemplate = it->second;

		TiXmlElement* pNewItem = new TiXmlElement("Template");
		pNewItem->SetAttribute("Id", pTemplate->GetID());
		pNewItem->SetAttribute("Att", pTemplate->GetAttFlag());
		pNewItem->SetAttribute("Priority", pTemplate->GetRenderPriority());
		TextureEntity* pTex = pTemplate->GetTexture0();
		if (pTex)
		{
			pNewItem->SetAttribute("Tex0", pTex->GetLocalFileName());

			pTex = pTemplate->GetTexture1();
			if (pTex)
			{
				pNewItem->SetAttribute("Tex1", pTex->GetLocalFileName());
			}

			pTex = pTemplate->GetNormalMap();
			if (pTex)
			{
				pNewItem->SetAttribute("NorMap", pTex->GetLocalFileName());
			}
		}
		root->LinkEndChild(pNewItem);
	}
	std::string fileName = m_worldInfo.GetBlockTemplateFileName(true);
	doc.SaveFile(fileName);
#endif
}

void CBlockWorld::LoadBlockTemplateData()
{
	CParaFile* pFile = NULL;

	std::string tempXml = m_worldInfo.GetBlockTemplateFileName(true);
	CParaFile file(tempXml.c_str());

	std::string gameSaveXml = m_worldInfo.GetBlockTemplateFileName(false);
	CParaFile gameSaveFile(gameSaveXml.c_str());

	if (file.isEof())
	{
		if (!gameSaveFile.isEof())
			pFile = &gameSaveFile;
	}
	else
	{
		pFile = &file;
	}

	if (pFile == NULL)
		return;

	try
	{
#ifdef USE_TINYXML2
		using namespace tinyxml2;
		tinyxml2::XMLDocument doc(true, COLLAPSE_WHITESPACE);
		doc.Parse(pFile->getBuffer(), (int)(pFile->getSize()));
		XMLElement* pRoot = doc.RootElement();

		if (pRoot)
		{
			for (XMLNode* pChild = pRoot->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
			{
				if (pChild->ToElement())
				{
					XMLElement* pElement = pChild->ToElement();
					if (pElement)
					{
						int32_t templateID = 0;
						int32_t categoryID = 0;
						pElement->QueryIntAttribute("Category", &categoryID);

						if (pElement->QueryIntAttribute("Id", &templateID) == XMLError::XML_SUCCESS)
						{
							uint32_t templateAtt = 0;
							if (pElement->QueryIntAttribute("Att", (int32_t*)&templateAtt) == XMLError::XML_SUCCESS)
							{
								int32_t priority = 0;
								pElement->QueryIntAttribute("Priority", &priority);

								const char* tex0 = pElement->Attribute("Tex0");
								const char* tex1 = pElement->Attribute("Tex1");
								const char* normalMap = pElement->Attribute("NorMap");

								BlockTemplate* pTemplate = RegisterTemplate(templateID & 0xffff, templateAtt, categoryID);
								if (pTemplate)
								{
									pTemplate->SetRenderPriority(priority & 0xf);
									if (tex0)
										pTemplate->SetTexture0(tex0);
									if (tex1)
										pTemplate->SetTexture1(tex1);
									if (normalMap)
										pTemplate->SetNormalMap(normalMap);
								}
							}
						}
					}
				}
			}
		}
#else
		TiXmlDocument doc;
		doc.Parse(pFile->getBuffer(), 0, TIXML_DEFAULT_ENCODING);
		TiXmlElement* pRoot = doc.RootElement();

		if (pRoot)
		{
			for (TiXmlNode* pChild = pRoot->FirstChild(); pChild != 0; pChild = pChild->NextSibling())
			{
				if (pChild->Type() == TiXmlNode::ELEMENT)
				{
					TiXmlElement* pElement = pChild->ToElement();
					if (pElement)
					{
						int32_t templateID = 0;
						int32_t categoryID = 0;
						pElement->QueryIntAttribute("Category", &categoryID);

						if (pElement->QueryIntAttribute("Id", &templateID) == TIXML_SUCCESS)
						{
							uint32_t templateAtt = 0;
							if (pElement->QueryIntAttribute("Att", (int32_t*)&templateAtt) == TIXML_SUCCESS)
							{
								int32_t priority = 0;
								pElement->QueryIntAttribute("Priority", &priority);

								int32_t temp;
								const char* tex0 = pElement->Attribute("Tex0", &temp);
								const char* tex1 = pElement->Attribute("Tex1", &temp);
								const char* normalMap = pElement->Attribute("NorMap", &temp);

								BlockTemplate* pTemplate = RegisterTemplate(templateID & 0xffff, templateAtt, categoryID);
								if (pTemplate)
								{
									pTemplate->SetRenderPriority(priority & 0xf);
									if (tex0)
										pTemplate->SetTexture0(tex0);
									if (tex1)
										pTemplate->SetTexture1(tex1);
									if (normalMap)
										pTemplate->SetNormalMap(normalMap);
								}
							}
						}
					}
				}
			}

		}
#endif
	}
	catch (...)
	{
		OUTPUT_LOG("error parsing block template file \n");
	}

}

RenderableChunk& CBlockWorld::GetActiveChunk(uint16_t curChunkWX, uint16_t curChunkWY, uint16_t curChunkWZ)
{
	curChunkWX = curChunkWX % m_activeChunkDim;
	curChunkWY = curChunkWY % m_activeChunkDimY;
	curChunkWZ = curChunkWZ % m_activeChunkDim;
	uint32_t index = curChunkWZ + curChunkWX * m_activeChunkDim + curChunkWY * m_activeChunkDim * m_activeChunkDim;
	return *(m_activeChunks[index]);
}


bool CBlockWorld::ReuseActiveChunk(int16_t curChunkWX, int16_t curChunkWY, int16_t curChunkWZ, BlockRegion* pRegion)
{
	if (curChunkWX >= 0 && curChunkWY >= 0 && curChunkWY < 16 && curChunkWZ >= 0 && pRegion)
	{
		int16_t localChunkX = curChunkWX & 0x1f;
		int16_t localChunkY = curChunkWY & 0xf;
		int16_t localChunkZ = curChunkWZ & 0x1f;

		uint16_t chunkIndex = PackChunkIndex(localChunkX, localChunkY, localChunkZ);
		GetActiveChunk(curChunkWX, curChunkWY, curChunkWZ).ReuseChunk(pRegion, chunkIndex);
		return true;
	}
	else
	{
		GetActiveChunk(curChunkWX, curChunkWY, curChunkWZ).ReuseChunk(NULL, -1);
		return false;
	}
}

BlockTemplate* CBlockWorld::GetBlockTemplate(uint16_t id)
{
	if (id < 256)
		return m_blockTemplatesArray[id];
	else
	{
		std::map<uint16_t, BlockTemplate*>::iterator it = m_blockTemplates.find(id);
		if (it == m_blockTemplates.end())
			return NULL;

		return (*it).second;
	}
}

BlockTemplate* CBlockWorld::RegisterTemplate(uint16_t id, uint32_t attFlag, uint16_t category_id)
{
	if (GetBlockTemplate(id))
		return NULL;

	BlockTemplate *newTemplate = new BlockTemplate(id, attFlag, category_id);
	m_blockTemplates.insert(std::pair<uint16_t, BlockTemplate*>(id, newTemplate));
	if (id < 256)
		m_blockTemplatesArray[id] = newTemplate;
	return newTemplate;
}

void CBlockWorld::SetBlockTemplateId(float x, float y, float z, uint16_t templateId)
{
	Uint16x3 blockIdx;
	BlockCommon::ConvertToBlockIndex(x, y, z, blockIdx.x, blockIdx.y, blockIdx.z);
	SetBlockId(blockIdx.x, blockIdx.y, blockIdx.z, templateId);
}

void CBlockWorld::SetBlockTemplateIdByIdx(uint16_t x, uint16_t y, uint16_t z, uint16_t templateId)
{
	SetBlockId(x, y, z, templateId);
}

uint16_t CBlockWorld::GetBlockTemplateId(float x, float y, float z)
{
	Uint16x3 blockIdx;
	BlockCommon::ConvertToBlockIndex(x, y, z, blockIdx.x, blockIdx.y, blockIdx.z);
	return GetBlockId(blockIdx.x, blockIdx.y, blockIdx.z);
}

uint16_t CBlockWorld::GetBlockTemplateIdByIdx(uint16_t x, uint16_t y, uint16_t z)
{
	return GetBlockId(x, y, z);
}

void CBlockWorld::SetBlockUserData(float x, float y, float z, uint32_t data)
{
	Uint16x3 blockIdx;
	BlockCommon::ConvertToBlockIndex(x, y, z, blockIdx.x, blockIdx.y, blockIdx.z);
	SetBlockData(blockIdx.x, blockIdx.y, blockIdx.z, data);
}

void CBlockWorld::SetBlockUserDataByIdx(uint16_t x, uint16_t y, uint16_t z, uint32_t data)
{
	SetBlockData(x, y, z, data);
}

uint32_t CBlockWorld::GetBlockUserData(float x, float y, float z)
{
	Uint16x3 blockIdx;
	BlockCommon::ConvertToBlockIndex(x, y, z, blockIdx.x, blockIdx.y, blockIdx.z);
	return GetBlockData(blockIdx.x, blockIdx.y, blockIdx.z);
}

uint32_t CBlockWorld::GetBlockUserDataByIdx(uint16_t x, uint16_t y, uint16_t z)
{
	return GetBlockData(x, y, z);
}

bool CBlockWorld::SetBlockVisible(uint16_t templateId, bool value, bool bRefreshWorld)
{
	BlockTemplate* pTemp = GetBlockTemplate(templateId);

	if (pTemp)
	{
		if (!value == pTemp->IsMatchAttribute(BlockTemplate::batt_invisible))
			return false;

		if (!value)
		{
			BlockTemplateVisibleData visibleData;
			visibleData.lightOpyValue = pTemp->GetLightOpacity();
			visibleData.isTransparent = pTemp->IsMatchAttribute(BlockTemplate::batt_transparent);
			visibleData.torchLight = pTemp->GetTorchLight();

			m_blockTemplateVisibleDatas[templateId] = visibleData;

			pTemp->SetAttribute(BlockTemplate::batt_transparent, true);
			pTemp->SetAttribute(BlockTemplate::batt_invisible, true);
			pTemp->SetLightOpacity(0);
			pTemp->SetTorchLight(0);
		}
		else
		{
			pTemp->SetAttribute(BlockTemplate::batt_invisible, false);
			auto visibleDataItr = m_blockTemplateVisibleDatas.find(templateId);
			if (visibleDataItr != m_blockTemplateVisibleDatas.end())
			{
				pTemp->SetAttribute(BlockTemplate::batt_transparent, visibleDataItr->second.isTransparent);
				pTemp->SetLightOpacity(visibleDataItr->second.lightOpyValue);
				pTemp->SetTorchLight(visibleDataItr->second.torchLight);

				m_blockTemplateVisibleDatas.erase(templateId);
			}
		}
		if (bRefreshWorld) {
			RefreshBlockTemplate(templateId);
			return false;
		}
		return true;
	}
	return false;
}

void ParaEngine::CBlockWorld::RefreshBlockTemplate(uint16_t templateId)
{
	for (auto& iter : m_regionCache)
	{
		iter.second->SetChunksDirtyByBlockTemplate(templateId);
	}
}

uint32_t ParaEngine::CBlockWorld::SetBlockId(uint16_t x, uint16_t y, uint16_t z, uint32_t nBlockID)
{
	if (y >= 256)
		return 0;
	
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		BlockTemplate* pTemplate = (nBlockID > 0) ? GetBlockTemplate(nBlockID) : NULL;
		pRegion->SetBlockTemplateByIndex(lx, ly, lz, pTemplate);
		m_isVisibleChunkDirty = true;
		return 0;
	}
	return 0;
}

uint32_t ParaEngine::CBlockWorld::GetBlockId(uint16_t x, uint16_t y, uint16_t z)
{
	if (y >= 256)
		return 0;

	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		return pRegion->GetBlockTemplateIdByIndex(lx, ly, lz);
	}
	return 0;
}

uint32_t ParaEngine::CBlockWorld::SetBlockData(uint16_t x, uint16_t y, uint16_t z, uint32_t nBlockData)
{
	if (y >= 256)
		return 0;

	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		pRegion->SetBlockUserDataByIndex(lx, ly, lz, nBlockData);
		m_isVisibleChunkDirty = true;
		return 0;
	}
	return 0;
}

uint32_t ParaEngine::CBlockWorld::GetBlockData(uint16_t x, uint16_t y, uint16_t z)
{
	if (y >= 256)
		return 0;

	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		return pRegion->GetBlockUserDataByIndex(lx, ly, lz);
	}
	return 0;
}

Block* CBlockWorld::GetBlock(uint16_t x_ws, uint16_t y_ws, uint16_t z_ws)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x_ws, y_ws, z_ws, lx, ly, lz);

	if (pRegion)
	{
		return pRegion->GetBlock(lx, ly, lz);
	}
	return NULL;
}


Block* CBlockWorld::GetUnlockBlock(uint16_t x, uint16_t y, uint16_t z)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion && !pRegion->IsLocked())
	{
		return pRegion->GetBlock(lx, ly, lz);
	}
	return nullptr;
}

BlockTemplate* CBlockWorld::GetBlockTemplate(uint16_t x, uint16_t y, uint16_t z)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		return pRegion->GetBlockTemplateByIndex(lx, ly, lz);
	}
	return NULL;
}

BlockTemplate* CBlockWorld::GetBlockTemplate(Uint16x3& blockId)
{
	return GetBlockTemplate(blockId.x, blockId.y, blockId.z);
}

void CBlockWorld::SetChunkDirty(Uint16x3& chunkId_ws, bool isDirty)
{
	int16_t regionX = chunkId_ws.x >> 5;
	int16_t regionZ = chunkId_ws.z >> 5;

	BlockRegion* pRegion = GetRegion(regionX, regionZ);
	if (pRegion)
	{
		int16_t chunkX_rs = chunkId_ws.x & 0x1f;
		int16_t chunkZ_rs = chunkId_ws.z & 0x1f;

		uint16_t packedChunkId_rs = PackChunkIndex(chunkX_rs, chunkId_ws.y, chunkZ_rs);
		pRegion->SetChunkDirty(packedChunkId_rs, isDirty);
	}
}

void ParaEngine::CBlockWorld::SetChunkLightDirty(Uint16x3& chunkId_ws)
{
	int16_t regionX = chunkId_ws.x >> 5;
	int16_t regionZ = chunkId_ws.z >> 5;

	BlockRegion* pRegion = GetRegion(regionX, regionZ);
	if (pRegion)
	{
		int16_t chunkX_rs = chunkId_ws.x & 0x1f;
		int16_t chunkZ_rs = chunkId_ws.z & 0x1f;

		uint16_t packedChunkId_rs = PackChunkIndex(chunkX_rs, chunkId_ws.y, chunkZ_rs);
		pRegion->SetChunkLightDirty(packedChunkId_rs);
	}
}


ChunkMaxHeight* CBlockWorld::GetHighestBlock(uint16_t blockX_ws, uint16_t blockZ_ws)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(blockX_ws, 0, blockZ_ws, lx, ly, lz);
	if (pRegion)
	{
		return pRegion->GetHighestBlock(lx, lz);
	}
	return NULL;
}

void CBlockWorld::GetMaxBlockHeightWatchingSky(uint16_t blockX_ws, uint16_t blockZ_ws, ChunkMaxHeight* pResult)
{
	ChunkMaxHeight* pBlockHeight = NULL;
	pBlockHeight = GetHighestBlock(blockX_ws, blockZ_ws);
	if (pBlockHeight)
		pResult[0] = *pBlockHeight;

	pBlockHeight = GetHighestBlock(blockX_ws + 1, blockZ_ws);
	if (pBlockHeight)
		pResult[1] = *pBlockHeight;

	pBlockHeight = GetHighestBlock(blockX_ws - 1, blockZ_ws);
	if (pBlockHeight)
		pResult[2] = *pBlockHeight;

	pBlockHeight = GetHighestBlock(blockX_ws, blockZ_ws + 1);
	if (pBlockHeight)
		pResult[3] = *pBlockHeight;

	pBlockHeight = GetHighestBlock(blockX_ws, blockZ_ws - 1);
	if (pBlockHeight)
		pResult[4] = *pBlockHeight;
}

bool ParaEngine::CBlockWorld::IsChunkColumnInActiveRange(int16_t curChunkWX, int16_t curChunkWZ)
{
	return (curChunkWX >= m_minActiveChunkId_ws.x && curChunkWX < (m_minActiveChunkId_ws.x + m_activeChunkDim) &&
		curChunkWZ >= m_minActiveChunkId_ws.z && curChunkWZ < (m_minActiveChunkId_ws.z + m_activeChunkDim));
}

bool CBlockWorld::RefreshChunkColumn(int16_t curChunkWX, int16_t curChunkWZ)
{
	if (IsChunkColumnInActiveRange(curChunkWX, curChunkWZ))
	{
		int16_t regionX = curChunkWX >> 5;
		int16_t regionZ = curChunkWZ >> 5;
		BlockRegion *pRegion = GetRegion(regionX, regionZ);

		for (int16_t curChunkWY = 0; curChunkWY < 16; curChunkWY++)
		{
			ReuseActiveChunk(curChunkWX, curChunkWY, curChunkWZ, pRegion);
		}
		GetLightGrid().AddDirtyColumn(curChunkWX, curChunkWZ);
		m_isVisibleChunkDirty = true;
		return true;
	}
	return false;
}

void CBlockWorld::UpdateActiveChunk()
{
	Int16x3 curMinActiveChunkId(m_minActiveChunkId_ws);

	Int16x3 deltaOfs;
	Int16x3::Subtract(m_curChunkIdW, m_lastChunkIdW, deltaOfs);
	m_minActiveChunkId_ws.x = m_curChunkIdW.x - (int)((m_activeChunkDim) / 2);
	m_minActiveChunkId_ws.y = m_curChunkIdW.y - (int)((m_activeChunkDimY) / 2);
	m_minActiveChunkId_ws.z = m_curChunkIdW.z - (int)((m_activeChunkDim) / 2);


	// tricky: this will be set to fixed value, since we want to cache for all chunks vertically. 
	m_minActiveChunkId_ws.y = 0;
	curMinActiveChunkId.y = 0;
	deltaOfs.y = 0;

	if (deltaOfs.x == 0 && deltaOfs.y == 0 && deltaOfs.z == 0)
		return;


	Int16x3 deltaAbs(deltaOfs);
	deltaAbs.Abs();

	if (m_lastChunkIdW.x < 0 || deltaAbs.x >= m_activeChunkDim ||
		deltaAbs.y >= m_activeChunkDimY ||
		deltaAbs.z >= m_activeChunkDim)
	{
		for (int y = 0; y < m_activeChunkDimY; y++)
		{
			int16_t curChunkWY = m_minActiveChunkId_ws.y + y;

			for (int z = 0; z < m_activeChunkDim; z++)
			{
				int16_t curChunkWZ = m_minActiveChunkId_ws.z + z;
				for (int x = 0; x < m_activeChunkDim; x++)
				{
					int16_t curChunkWX = m_minActiveChunkId_ws.x + x;
					int16_t regionX = curChunkWX >> 5;
					int16_t regionZ = curChunkWZ >> 5;
					// check load regions
					BlockRegion *pRegion = CreateGetRegion(regionX, regionZ);

					if (pRegion)
					{
						ReuseActiveChunk(curChunkWX, curChunkWY, curChunkWZ, pRegion);
					}
					else
					{
						// OUTPUT_DEBUG("warning: no region at visible chunk\r\n");
					}
				}
			}
		}
	}
	else
	{
		Int16x3 startChunkId(m_minActiveChunkId_ws);

		if (deltaOfs.x >= 0)
			startChunkId.x = startChunkId.x + m_activeChunkDim - deltaOfs.x;

		if (deltaOfs.y >= 0)
			startChunkId.y = startChunkId.y + m_activeChunkDimY - deltaOfs.y;

		if (deltaOfs.z >= 0)
			startChunkId.z = startChunkId.z + m_activeChunkDim - deltaOfs.z;

		//update 3D ring array, try to simplify the update logic here 
		// x direction
		for (int16_t x = 0; x < deltaAbs.x; x++)
		{
			int16_t curChunkWX = startChunkId.x + x;

			for (int16_t z = 0; z < m_activeChunkDim; z++)
			{
				int16_t curChunkWZ = curMinActiveChunkId.z + z;

				int16_t regionX = curChunkWX >> 5;
				int16_t regionZ = curChunkWZ >> 5;
				BlockRegion* pRegion = CreateGetRegion(regionX, regionZ);

				for (int16_t y = 0; y < m_activeChunkDimY; y++)
				{
					int16_t curChunkWY = curMinActiveChunkId.y + y;

					ReuseActiveChunk(curChunkWX, curChunkWY, curChunkWZ, pRegion);
					if (!pRegion)
					{
						// OUTPUT_DEBUG("warning: no region at visible chunk\r\n");
					}
				}
			}
		}

		curMinActiveChunkId.x = m_minActiveChunkId_ws.x;

		// y direction
		for (int16_t y = 0; y < deltaAbs.y; y++)
		{
			int16_t curChunkWY = startChunkId.y + y;

			for (int z = 0; z < m_activeChunkDim; z++)
			{
				int16_t curChunkWZ = curMinActiveChunkId.z + z;

				for (int x = 0; x < m_activeChunkDim; x++)
				{
					int16_t curChunkWX = curMinActiveChunkId.x + x;

					int16_t regionX = curChunkWX >> 5;
					int16_t regionZ = curChunkWZ >> 5;
					BlockRegion *pRegion = CreateGetRegion(regionX, regionZ);
					ReuseActiveChunk(curChunkWX, curChunkWY, curChunkWZ, pRegion);
					if (!pRegion)
					{
						// OUTPUT_DEBUG("warning: no region at visible chunk\r\n");
					}
				}
			}
		}

		curMinActiveChunkId.y = m_minActiveChunkId_ws.y;

		// z direction
		for (int16_t z = 0; z < deltaAbs.z; z++)
		{
			int16_t curChunkWZ = startChunkId.z + z;

			for (int16_t x = 0; x < m_activeChunkDim; x++)
			{
				int16_t curChunkWX = curMinActiveChunkId.x + x;

				int16_t regionX = curChunkWX >> 5;
				int16_t regionZ = curChunkWZ >> 5;
				BlockRegion* pRegion = CreateGetRegion(regionX, regionZ);

				for (int16_t y = 0; y < m_activeChunkDimY; y++)
				{
					int16_t curChunkWY = curMinActiveChunkId.y + y;
					ReuseActiveChunk(curChunkWX, curChunkWY, curChunkWZ, pRegion);
					if (!pRegion)
					{
						// OUTPUT_DEBUG("warning: no region at visible chunk\r\n");
					}
				}
			}
		}
	}
}

void CBlockWorld::RefreshAllLightsInColumn(uint16_t chunkX_ws, uint16_t chunkZ_ws)
{
	uint16_t regionX = chunkX_ws / BlockConfig::g_regionChunkDimX;
	uint16_t regionZ = chunkZ_ws / BlockConfig::g_regionChunkDimZ;

	BlockRegion* pRegion = GetRegion(regionX, regionZ);
	if (pRegion)
	{
		pRegion->RefreshAllLightsInColumn(chunkX_ws, chunkZ_ws);
	}
}

void CBlockWorld::NotifyBlockHeightMapChanged(uint16_t blockIdX_ws, uint16_t blockIdZ_ws, ChunkMaxHeight& prevBlockHeight)
{
	GetLightGrid().NotifyBlockHeightChanged(blockIdX_ws, blockIdZ_ws, prevBlockHeight);
}


bool CBlockWorld::GetBlockBrightness(Uint16x3& blockId_ws, uint8_t* brightness, int nSize, int nLightType)
{
	return GetLightGrid().GetBrightness(blockId_ws, brightness, nSize, nLightType);
}

bool CBlockWorld::GetBlockMeshBrightness(Uint16x3& blockId_ws, uint8_t* brightness, int nLightType)
{
	BlockTemplate* pBlock = GetBlockTemplate(blockId_ws);
	if (pBlock && !pBlock->IsTransparent())
	{
		// if the block is solid, we will return the max brightness of the block's 6 neighbors. 
		uint8_t brightnesses[14];
		int nSize = 7;
		if (GetBlockBrightness(blockId_ws, brightnesses, nSize, nLightType))
		{
			uint8_t max_value = brightnesses[1];
			for (int i = 2; i < nSize; i++)
			{
				if (max_value < brightnesses[i])
					max_value = brightnesses[i];
			}
			brightness[0] = max_value;
			if (nLightType == 2)
			{
				max_value = brightnesses[1 + nSize];
				for (int i = 2; i < nSize; i++)
				{
					if (max_value < brightnesses[i + nSize])
						max_value = brightnesses[i + nSize];
				}
				brightness[1] = max_value;
			}
			return true;
		}
		else
			return false;
	}
	else
	{
		// if the block in Not solid, we will simply return the block's brightness. 
		return (GetBlockBrightness(blockId_ws, brightness, 1, nLightType));
	}
}


float CBlockWorld::GetBlockBrightnessReal(Uint16x3& blockId_ws, float* pBrightness)
{
	uint8_t brightness = 0;
	GetBlockMeshBrightness(blockId_ws, &brightness, -1);
	float fBrightness = GetLightBrightnessFloat(brightness);
	if (pBrightness != NULL)
		pBrightness[0] = fBrightness;
	return fBrightness;
}

float CBlockWorld::GetBlockBrightnessReal(const Vector3& vPos, float* pBrightness)
{
	Uint16x3 blockId_ws(0, 0, 0);
	BlockCommon::ConvertToBlockIndex(vPos.x, vPos.y, vPos.z, blockId_ws.x, blockId_ws.y, blockId_ws.z);
	return GetBlockBrightnessReal(blockId_ws, pBrightness);
}

void CBlockWorld::SetLightBlockDirty(Uint16x3& blockId_ws, bool isSunLight)
{
	GetLightGrid().SetLightDirty(blockId_ws, isSunLight, 1);
}

int32_t CBlockWorld::GetBlocksInRegion(Uint16x3& startChunk_ws, Uint16x3& endChunk_ws, uint32_t matchType, const luabind::adl::object& result, uint32_t verticalSectionFilter)
{
	int32_t blockCount = 0;
	for (uint16_t x = startChunk_ws.x; x <= endChunk_ws.x; x++)
	{
		uint16_t regionX = x >> 5;
		for (uint16_t z = startChunk_ws.z; z <= endChunk_ws.z; z++)
		{
			uint16_t regionZ = z >> 5;

			BlockRegion* pRegion = GetRegion(regionX, regionZ);
			if (pRegion)
			{
				if (verticalSectionFilter==0)
					pRegion->GetBlocksInChunk(x, z, startChunk_ws.y, endChunk_ws.y, matchType, result, blockCount);
				else
					pRegion->GetBlocksInChunk(x, z, verticalSectionFilter, matchType, result, blockCount);
			}
		}
	}
	return blockCount;
}


void CBlockWorld::SetCubeModePicking(bool bIsCubeModePicking)
{
	m_bCubeModePicking = bIsCubeModePicking;
}

bool CBlockWorld::IsCubeModePicking()
{
	return m_bCubeModePicking;
}

bool CBlockWorld::Pick(const Vector3& rayOrig, const Vector3& dir, float length, PickResult& result, uint32_t filter)
{
	if (!m_isInWorld)
		return false;
	//////////////////////////////////////////////////////////////
	//
	// use 3D DDA algorithm to find hit block more detail see 
	// http://www.flipcode.com/archives/Raytracing_Topics_Techniques-Part_4_Spatial_Subdivisions.shtml
	//
	//////////////////////////////////////////////////////////////

	Uint16x3 tempBlockId;
	BlockCommon::ConvertToBlockIndex(rayOrig.x, rayOrig.y, rayOrig.z, tempBlockId.x, tempBlockId.y, tempBlockId.z);
	int32_t startBlockIdX = tempBlockId.x;
	int32_t startBlockIdY = tempBlockId.y;
	int32_t startBlockIdZ = tempBlockId.z;

	int32_t curBlockIdX = startBlockIdX;
	int32_t curBlockIdY = startBlockIdY;
	int32_t curBlockIdZ = startBlockIdZ;

	//ray tracing direction
	int32_t blockStepX;
	int32_t blockStepY;
	int32_t blockStepZ;

	//setup 3d dda init value
	Vector3 nextBlockPos;
	if (dir.x > 0)
	{
		blockStepX = 1;
		nextBlockPos.x = (curBlockIdX + 1) * BlockConfig::g_blockSize;
	}
	else
	{
		blockStepX = -1;
		nextBlockPos.x = curBlockIdX * BlockConfig::g_blockSize;
	}

	if (dir.y > 0)
	{
		blockStepY = 1;
		nextBlockPos.y = (curBlockIdY + 1) * BlockConfig::g_blockSize;
	}
	else
	{
		blockStepY = -1;
		nextBlockPos.y = curBlockIdY * BlockConfig::g_blockSize;
	}

	if (dir.z > 0)
	{
		blockStepZ = 1;
		nextBlockPos.z = (curBlockIdZ + 1) * BlockConfig::g_blockSize;
	}
	else
	{
		blockStepZ = -1;
		nextBlockPos.z = curBlockIdZ * BlockConfig::g_blockSize;
	}

	// distance we can travel along the ray before hitting a block boundary, in either of the three axis.
	Vector3 errDist;
	// the delta distance to travel in the three axis, before we move to next block. This is a constant;
	Vector3 delta;

	float maxRayDist = 100000;
	if (dir.x != 0)
	{
		float invX = 1.0f / dir.x;
		errDist.x = (nextBlockPos.x - rayOrig.x) * invX;
		delta.x = BlockConfig::g_blockSize * blockStepX * invX;
	}
	else
		errDist.x = maxRayDist;

	if (dir.y != 0)
	{
		float invY = 1.0f / dir.y;
		errDist.y = (nextBlockPos.y - rayOrig.y + GetVerticalOffset()) * invY;
		delta.y = BlockConfig::g_blockSize * blockStepY * invY;
	}
	else
		errDist.y = maxRayDist;

	if (dir.z != 0)
	{
		float invZ = 1.0f / dir.z;
		errDist.z = (nextBlockPos.z - rayOrig.z) * invZ;
		delta.z = BlockConfig::g_blockSize * blockStepZ * invZ;
	}
	else
		errDist.z = maxRayDist;
	
	int16_t curRegionX = -1;
	int16_t curRegionZ = -1;
	BlockRegion* curRegion = NULL;
	int32_t side;
	while (true)
	{
		//find the smallest value of traveledDist and going alone that direction
		float distTraveled = 0;
		if (errDist.x < errDist.y)
		{
			if (errDist.x < errDist.z)
			{
				distTraveled = errDist.x;
				curBlockIdX += blockStepX;
				errDist.x += delta.x;
				side = 0;
			}
			else
			{
				distTraveled = errDist.z;
				curBlockIdZ += blockStepZ;
				errDist.z += delta.z;
				side = 2;
			}
		}
		else
		{
			if (errDist.y < errDist.z)
			{
				distTraveled = errDist.y;
				curBlockIdY += blockStepY;
				errDist.y += delta.y;
				side = 4;
			}
			else
			{
				distTraveled = errDist.z;
				curBlockIdZ += blockStepZ;
				errDist.z += delta.z;
				side = 2;
			}
		}

		uint16_t regionX = curBlockIdX >> 9;
		uint16_t regionZ = curBlockIdZ >> 9;
		if (regionX != curRegionX || regionZ != curRegionZ)
		{
			curRegionX = regionX;
			curRegionZ = regionZ;
			curRegion = GetRegion(curRegionX, curRegionZ);
		}

		if (curRegion == NULL || curBlockIdX < 0 || curBlockIdY < 0 || curBlockIdZ < 0)
			return false;

		Block* pBlock = curRegion->GetBlock(curBlockIdX & 0x1ff, curBlockIdY & 0xff, curBlockIdZ & 0x1ff);
		BlockTemplate* pBlockTemplate = NULL;
		if (pBlock != 0 && (pBlockTemplate = pBlock->GetTemplate()) != 0 && ((pBlockTemplate->GetAttFlag() & filter) > 0))
		{
			const double blockSize = BlockConfig::g_blockSize;
			float rayLength = -1;

			if (side == 0 && blockStepX <= 0)
				side = 1;
			if (side == 2 && blockStepZ <= 0)
				side = 3;
			if (side == 4 && blockStepY <= 0)
				side = 5;

			if (pBlockTemplate->GetBlockModel().IsCubeAABB() || IsCubeModePicking())
			{
				rayLength = distTraveled;
			}
			else
			{
				// use AABB for non-cube model
				CShapeAABB aabb;
				pBlockTemplate->GetAABB(this, curBlockIdX, curBlockIdY, curBlockIdZ, &aabb);
				Vector3 vOrig = rayOrig - Vector3((float)(blockSize*curBlockIdX), (float)(blockSize*curBlockIdY + GetVerticalOffset()), (float)(blockSize*curBlockIdZ));

				float fHitDist = -1;
				int nHitSide = 0;
				if (aabb.IntersectOutside(&fHitDist, &vOrig, &dir, &nHitSide))
				{
					rayLength = fHitDist;
					side = nHitSide;
				}
			}

			if (rayLength >= 0)
			{
				m_selectBlockIdW.x = curBlockIdX;
				m_selectBlockIdW.y = curBlockIdY;
				m_selectBlockIdW.z = curBlockIdZ;

				float collsionX = rayOrig.x + rayLength * dir.x;
				float collsionY = rayOrig.y + rayLength * dir.y;
				float collsionZ = rayOrig.z + rayLength * dir.z;

				result.X = collsionX;
				result.Y = collsionY;
				result.Z = collsionZ;

				result.BlockX = curBlockIdX;
				result.BlockY = curBlockIdY;
				result.BlockZ = curBlockIdZ;

				result.Side = side;
				result.Distance = rayLength;
				return true;
			}
		}
		if (distTraveled > length)
			return false;
	}
	return false;
}

bool CBlockWorld::IsObstructionBlock(uint16_t x, uint16_t y, uint16_t z)
{
	if (!m_isInWorld)
		return 0;

	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);

	if (pRegion)
	{
		uint32_t templateId = pRegion->GetBlockTemplateIdByIndex(lx, ly, lz);
		if (templateId > 0)
		{
			BlockTemplate* temp = GetBlockTemplate(templateId);
			if (temp && temp->IsMatchAttribute(BlockTemplate::batt_obstruction))
				return true;
		}
	}
	return false;
}


void CBlockWorld::SetTemplateTexture(uint16_t id, const char* textureName)
{
	BlockTemplate* pTemplate = GetBlockTemplate(id);
	if (pTemplate)
	{
		std::string sTextureName = textureName;

		if (sTextureName.find("_three") != std::string::npos)
		{
			if (pTemplate->IsMatchAttribute(BlockTemplate::batt_singleSideTex))
			{
				pTemplate->SetAttribute(BlockTemplate::batt_singleSideTex, false);
				pTemplate->SetAttribute(BlockTemplate::batt_threeSideTex, true);
				pTemplate->SetAttribute(BlockTemplate::batt_fourSideTex, false);
				pTemplate->GetBlockModel().LoadModelByTexture(3);
				ClearBlockRenderCache();
			}
		}
		else if (sTextureName.find("_four") != std::string::npos)
		{
			if (pTemplate->IsMatchAttribute(BlockTemplate::batt_singleSideTex))
			{
				pTemplate->SetAttribute(BlockTemplate::batt_singleSideTex, false);
				pTemplate->SetAttribute(BlockTemplate::batt_threeSideTex, false);
				pTemplate->SetAttribute(BlockTemplate::batt_fourSideTex, true);
				pTemplate->GetBlockModel().LoadModelByTexture(4);
				ClearBlockRenderCache();
			}
		}
		else
		{
			if (pTemplate->IsMatchAttribute(BlockTemplate::batt_threeSideTex))
			{
				pTemplate->SetAttribute(BlockTemplate::batt_singleSideTex, true);
				pTemplate->SetAttribute(BlockTemplate::batt_threeSideTex, false);
				pTemplate->SetAttribute(BlockTemplate::batt_fourSideTex, false);
				pTemplate->GetBlockModel().LoadModelByTexture(0);
				ClearBlockRenderCache();
			}
		}
		pTemplate->SetTexture0(textureName);
	}
}

void CBlockWorld::SuspendLightUpdate()
{
	GetLightGrid().SuspendLightUpdate();
}

void CBlockWorld::ResumeLightUpdate()
{
	GetLightGrid().ResumeLightUpdate();
}

bool CBlockWorld::IsLightUpdateSuspended()
{
	return GetLightGrid().IsLightUpdateSuspended();
}

void CBlockWorld::SetChunkColumnTimeStamp(uint16_t x, uint16_t z, uint16_t nTimeStamp)
{
	uint16_t y = 0;
	BlockRegion* pRegion = GetRegion(x, y, z, x, y, z);
	if (pRegion)
	{
		pRegion->SetChunkColumnTimeStamp(x, z, nTimeStamp);
	}
}

int32_t CBlockWorld::GetChunkColumnTimeStamp(uint16_t x, uint16_t z)
{
	uint16_t y = 0;
	BlockRegion* pRegion = GetRegion(x, y, z, x, y, z);
	if (pRegion)
	{
		return pRegion->GetChunkColumnTimeStamp(x, z);
	}
	return -1;
}



int CBlockWorld::FindFirstBlock(uint16_t x, uint16_t y, uint16_t z, uint16_t nSide /*= 4*/, uint32_t max_dist /*= 32*/, uint32_t filter /*= 0xffffffff*/, int nCategoryID)
{
	int bx = x;
	int by = y;
	int dist_offset = 0;
	int bz = z;

	if (nSide == 5)
	{
		// if we are finding downward, we can accelerate by using the heightmap;
		auto pHeightPair = GetHighestBlock(x, z);
		if (pHeightPair)
		{
			int nMaxY = pHeightPair->GetMaxHeight();
			if (y > nMaxY)
			{
				if (filter != 0)
				{
					// start searching from highest block.
					by = nMaxY + 1;
					dist_offset = y - by;
				}
				else
				{
					return 1;
				}
			}
		}
		else
		{
			// all column is air. 
			if (filter == 0)
				return 1;
			else
				return -1;
		}
	}
	for (uint32_t nDist = 1; nDist <= max_dist; ++nDist)
	{
		BlockCommon::GetBlockPosBySide(bx, by, bz, nSide);
		if (by >= 0 && by <= 256)
		{
			BlockTemplate* pTemplate = GetBlockTemplate(bx, by, bz);
			if (pTemplate)
			{
				if (pTemplate->IsMatchAttribute(filter) && (nCategoryID < 0 || pTemplate->GetCategoryID() == nCategoryID))
				{
					return nDist + dist_offset;
				}
			}
			else if (filter == 0)
			{
				return nDist + dist_offset;
			}
		}
	}
	return -1;
}


int CBlockWorld::GetFirstBlock(uint16_t x, uint16_t y, uint16_t z, int nBlockId, uint16_t nSide /*= 4*/, uint32_t max_dist /*= 32*/)
{
	int bx = x;
	int by = y;
	int dist_offset = 0;
	int bz = z;

	if (nSide == 5)
	{
		// if we are finding downward, we can accelerate by using the heightmap;
		BlockTemplate* pBlock = GetBlockTemplate(nBlockId);
		if (pBlock && pBlock->IsMatchAttribute(BlockTemplate::batt_solid))
		{
			auto pHeightPair = GetHighestBlock(x, z);
			if (pHeightPair && pHeightPair->GetMaxHeight() > 0)
			{
				if (y > pHeightPair->GetMaxHeight())
				{
					// start searching from highest block.
					by = pHeightPair->GetMaxHeight() + 1;
					dist_offset = y - by;
				}
			}
			else
			{
				// all column is air. 
				return -1;
			}
		}
	}
	for (uint32_t nDist = 1; nDist <= max_dist; ++nDist)
	{
		BlockCommon::GetBlockPosBySide(bx, by, bz, nSide);
		if (by >= 0 && by <= 256)
		{
			BlockTemplate* pTemplate = GetBlockTemplate(bx, by, bz);
			if (pTemplate && pTemplate->GetID() == nBlockId)
			{
				return nDist + dist_offset;
			}
		}
	}
	return -1;
}


BlockIndex CBlockWorld::GetBlockIndex(uint16_t x, uint16_t y, uint16_t z, bool bCreateIfNotExist)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);
	if (pRegion)
	{
		BlockChunk* pChunk = pRegion->GetChunk(CalcPackedChunkID(lx, ly, lz), bCreateIfNotExist);
		if (pChunk)
		{
			return BlockIndex(pChunk, CalcPackedBlockID(lx, ly, lz));
		}
	}
	return BlockIndex((BlockChunk*)NULL, 0);
}

BlockChunk* CBlockWorld::GetChunk(uint16_t x, uint16_t y, uint16_t z, bool bCreateIfNotExist)
{
	uint16_t lx, ly, lz;
	BlockRegion* pRegion = GetRegion(x, y, z, lx, ly, lz);
	if (pRegion)
	{
		return pRegion->GetChunk(CalcPackedChunkID(lx, ly, lz), bCreateIfNotExist);
	}
	return NULL;
}

LightData* CBlockWorld::GetLightData(uint16_t x, uint16_t y, uint16_t z, bool bCreateIfNotExist)
{
	BlockIndex index = GetBlockIndex(x, y, z, bCreateIfNotExist);
	if (index.m_pChunk != NULL)
		return index.m_pChunk->GetLightData(index.m_nChunkBlockIndex);
	else
		return NULL;
}

int CBlockWorld::GetDirtyColumnCount()
{
	return GetLightGrid().GetDirtyColumnCount();
}

int ParaEngine::CBlockWorld::GetDirtyBlockCount()
{
	return GetLightGrid().GetDirtyBlockCount();
}

void CBlockWorld::GenerateLightBrightnessTable(bool bUseLinearBrightness)
{
	float fLight = 0.0f;

	for (int nIntensity = 0; nIntensity <= 15; ++nIntensity)
	{
		float fLightDist = 1.0f - nIntensity / 15.0f;
		if (bUseLinearBrightness)
			m_lightBrightnessTableFloat[nIntensity] = nIntensity / 15.0f;
		else
			m_lightBrightnessTableFloat[nIntensity] = (1.0f - fLightDist) / (fLightDist * 3.0f + 1.0f) * (1.0f - fLight) + fLight;
		m_lightBrightnessTableInt[nIntensity] = min((int)(m_lightBrightnessTableFloat[nIntensity] * 255), 255);
		m_lightBrightnessLinearTableFloat[nIntensity] = nIntensity / 15.0f;
	}
	for (int nIntensity = 16; nIntensity < sizeof(m_lightBrightnessTableInt); ++nIntensity)
	{
		m_lightBrightnessTableFloat[nIntensity] = 1.f;
		m_lightBrightnessTableInt[nIntensity] = 255;
		m_lightBrightnessLinearTableFloat[nIntensity] = 1.f;
	}
	if (m_is_linear_torch_brightness != bUseLinearBrightness)
	{
		ClearBlockRenderCache();
		m_is_linear_torch_brightness = bUseLinearBrightness;
	}
}

void CBlockWorld::UpdateRegionCache()
{
	if (!IsServerWorld())
	{
		int nDeltaChunkMoved = Math::Max(abs(m_curChunkIdW.x - m_lastChunkIdW_RegionCache.x), abs(m_curChunkIdW.z - m_lastChunkIdW_RegionCache.z));
		// at least walk cross one chunk to update region cache. 
		if (nDeltaChunkMoved >= 2)
		{
			m_lastChunkIdW_RegionCache = m_curChunkIdW;

			std::map<int, BlockRegion*>::iterator iter;

			bool bHasUnloadedRegion = true;
			int nRegionUnloaded = 0;
			while (m_regionCache.size() > m_maxCacheRegionCount && bHasUnloadedRegion)
			{
				BlockRegion* pFarthestRegion = NULL;
				int nFarthestRegionDist = 0;
				bHasUnloadedRegion = false;
				for (iter = m_regionCache.begin(); iter != m_regionCache.end(); iter++)
				{
					BlockRegion* pRegion = iter->second;
					if (pRegion)
					{
						// int nDistToCurrent = Math::Max(abs(m_curRegionIdX - pRegion->GetRegionX()), abs(m_curRegionIdZ - pRegion->GetRegionZ()));
						// all nine regions need to be in cache, regardless of m_maxCacheRegionCount
						// if (nDistToCurrent > 1)

						Uint16x3 center;
						pRegion->GetCenterBlockWs(&center);
						int nDistToCurrent = Math::Max(abs((int)m_curCenterBlockId.x - (int)center.x), abs((int)m_curCenterBlockId.z - (int)center.z));
						if (nDistToCurrent >= 256 + GetRenderDist())
						{
							// only remove unmodified region or remote region. 
							if (IsRemote() || !(pRegion->IsModified()))
							{
								if (nDistToCurrent > nFarthestRegionDist)
								{
									nFarthestRegionDist = nDistToCurrent;
									pFarthestRegion = pRegion;
								}
							}
						}
					}
				}
				if (pFarthestRegion)
				{
					OUTPUT_LOG("unload out of range region: %d %d\n", pFarthestRegion->GetRegionX(), pFarthestRegion->GetRegionZ());
					UnloadRegion(pFarthestRegion);
					bHasUnloadedRegion = true;
					nRegionUnloaded++;
				}
			}

			if (nRegionUnloaded > 0)
			{
				OUTPUT_LOG("%d region unloaded. Current region in memory: %d\n", nRegionUnloaded, (int)m_regionCache.size());
			}
		}
	}
	else
	{
		
	}
}

void CBlockWorld::OnViewCenterMove(float viewCenterX, float viewCenterY, float viewCenterZ)
{
	if (!m_isInWorld)
		return;

	BlockCommon::ConvertToBlockIndex(viewCenterX, viewCenterY, viewCenterZ, m_curCenterBlockId.x, m_curCenterBlockId.y, m_curCenterBlockId.z);

	m_curRegionIdX = m_curCenterBlockId.x >> 9;
	m_curRegionIdZ = m_curCenterBlockId.z >> 9;

	m_lastChunkIdW = m_curChunkIdW;

	m_curChunkIdW.x = m_curCenterBlockId.x >> 4;
	m_curChunkIdW.y = m_curCenterBlockId.y >> 4;
	m_curChunkIdW.z = m_curCenterBlockId.z >> 4;


	if (m_curChunkIdW.x != m_lastChunkIdW.x || m_curChunkIdW.y != m_lastChunkIdW.y || m_curChunkIdW.z != m_lastChunkIdW.z)
	{
		UpdateRegionCache();
		UpdateActiveChunk();
		GetLightGrid().OnWorldMove(m_curChunkIdW.x, m_curChunkIdW.z);
	}

	int nDeltaBlocksMoved = Math::Max(abs((int)m_curCenterBlockId.x - (int)m_lastViewCheckIdW.x), abs((int)m_curCenterBlockId.z - (int)m_lastViewCheckIdW.z));
	// at least walk cross one chunk to update region cache. 
	if (nDeltaBlocksMoved >= 16)
	{
		m_lastViewCheckIdW = m_curCenterBlockId;
		// ClearOutOfRangeActiveChunkData();
	}

	m_isVisibleChunkDirty = true;
}

void CBlockWorld::UpdateVisibleChunks(bool bIsShadowPass)
{
	
}

void CBlockWorld::SetSunIntensity(float intensity)
{
	if (intensity < 0) intensity = 0;
	if (intensity > 1) intensity = 1;

	float fDelta = m_sunIntensity - intensity;
	if (fDelta!=0.f)
	{
		m_sunIntensity = intensity;

		if (!IsInBlockWorld())
		{
			return;
		}

		// it will cause all buffer to rebuild, we will only change if light value changed a lot. 
		if (fDelta > 0.15f && GetBlockRenderMethod() == BLOCK_RENDER_FIXED_FUNCTION)
		{
			for (int x = 0; x < m_activeChunkDim; x++)
			{
				for (int z = 0; z < m_activeChunkDim; z++)
				{
					for (int y = 0; y < m_activeChunkDimY; y++)
					{
						RenderableChunk& chunk = GetActiveChunk(x, y, z);
						BlockChunk* pChunk = chunk.GetChunk();
						if (pChunk && pChunk->IsInfluenceBySunLight())
						{
							chunk.SetChunkDirty(true);
						}
					}
				}
			}
		}
	}
}


void CBlockWorld::SelectBlock(uint16_t x, uint16_t y, uint16_t z, int nGroupID)
{
	if (nGroupID >= 0 && nGroupID < BLOCK_GROUP_ID_MAX)
	{
		int64_t	nIndex = GetBlockSparseIndex(x, y, z);

		if (m_selectedBlockMap[nGroupID].GetBlocks().find(nIndex) == m_selectedBlockMap[nGroupID].GetBlocks().end())
		{
			m_selectedBlockMap[nGroupID].GetBlocks()[nIndex] = Uint16x3(x, y, z);
		}
	}
}

void CBlockWorld::DeselectBlock(uint16_t x, uint16_t y, uint16_t z, int nGroupID)
{
	if (nGroupID >= 0 && nGroupID < BLOCK_GROUP_ID_MAX)
	{
		int64_t	nIndex = GetBlockSparseIndex(x, y, z);

		std::map<int64_t, Uint16x3>::iterator itCur = m_selectedBlockMap[nGroupID].GetBlocks().find(nIndex);
		if (itCur != m_selectedBlockMap[nGroupID].GetBlocks().end())
		{
			m_selectedBlockMap[nGroupID].GetBlocks().erase(itCur);
		}
	}
}

void CBlockWorld::DeselectAllBlock(int nGroupID)
{
	if (nGroupID < 0)
	{
		nGroupID = min(-nGroupID, BLOCK_GROUP_ID_MAX - 1);
		for (int i = 0; i <= nGroupID; i++)
		{
			m_selectedBlockMap[i].GetBlocks().clear();
		}
	}
	else if (nGroupID < BLOCK_GROUP_ID_MAX)
	{
		m_selectedBlockMap[nGroupID].GetBlocks().clear();
	}
}

ParaEngine::BlockRenderMethod ParaEngine::CBlockWorld::GetBlockRenderMethod()
{
	return m_dwBlockRenderMethod;
}

void CBlockWorld::OnGenerateTerrain(int nRegionX, int nRegionY, int nChunkX, int nChunkZ)
{
	ScriptCallback* pCallback = GetScriptCallback(Type_GeneratorScript);
	if (pCallback){
		char sMsg[512];
		snprintf(sMsg, 512, "msg={region_x=%d, region_y=%d,chunk_x=%d, chunk_z=%d};", nRegionX, nRegionY, nChunkX, nChunkZ);
		std::string script = sMsg;
		script += pCallback->GetCode();
		pCallback->ActivateLocalNow(script);
	}
}


int ParaEngine::CBlockWorld::OnBeforeLoadBlockRegion(int x, int y)
{
	ScriptCallback* pCallback = GetScriptCallback(Type_BeforeLoadBlockRegion);
	if (pCallback){
		char sMsg[100];
		snprintf(sMsg, 100, "msg={x=%d,y=%d};", x, y);
		std::string script = sMsg;
		script += pCallback->GetCode();
		return pCallback->ActivateLocalNow(script);
	}
	return S_OK;
}


int CBlockWorld::OnLoadBlockRegion(int x, int y)
{
	ScriptCallback* pCallback = GetScriptCallback(Type_LoadBlockRegion);
	if (pCallback){
		char sMsg[100];
		snprintf(sMsg, 100, "msg={x=%d,y=%d};", x, y);
		std::string script = sMsg;
		script += pCallback->GetCode();
		pCallback->ActivateLocalNow(script);
	}
	return S_OK;
}

int CBlockWorld::OnUnLoadBlockRegion(int x, int y)
{
	ScriptCallback* pCallback = GetScriptCallback(Type_UnLoadBlockRegion);
	if (pCallback){
		char sMsg[100];
		snprintf(sMsg, 100, "msg={x=%d,y=%d};", x, y);
		std::string script = sMsg;
		script += pCallback->GetCode();
		pCallback->ActivateAsync(script);
	}
	return S_OK;
}

int ParaEngine::CBlockWorld::OnSaveBlockRegion(int x, int y)
{
	ScriptCallback* pCallback = GetScriptCallback(Type_SaveRegionCallbackScript);
	if (pCallback){
		char sMsg[100];
		snprintf(sMsg, 100, "msg={x=%d,y=%d,type=\"raw\"};", x, y);
		std::string script = sMsg;
		script += pCallback->GetCode();
		pCallback->ActivateLocalNow(script);
	}
	return S_OK;
}


void ParaEngine::CBlockWorld::AddRenderTask(BlockRenderTask* pRenderTask)
{

}

CWorldInfo& ParaEngine::CBlockWorld::GetWorldInfo()
{
	return m_worldInfo;
}

bool ParaEngine::CBlockWorld::IsSaveLightMap() const
{
	return m_bSaveLightMap;
}

void ParaEngine::CBlockWorld::SaveLightMap(bool val)
{
	m_bSaveLightMap = val;
}


ParaEngine::mutex& ParaEngine::CBlockWorld::GetBlockWorldMutex()
{
	return m_blockworld_mutex;
}

void ParaEngine::CBlockWorld::LockWorld()
{
	m_blockworld_mutex.lock();
}

void ParaEngine::CBlockWorld::UnlockWorld()
{
	m_blockworld_mutex.unlock();
}

void ParaEngine::CBlockWorld::ClearBlockRenderCache()
{

}

bool ParaEngine::CBlockWorld::DoChunksNearChunkExist(uint16_t x, uint16_t y, uint16_t z, uint16_t radius)
{
	return CheckChunkColumnsExist(x - radius, y - radius, z - radius, x + radius, y + radius, z + radius);
}

bool ParaEngine::CBlockWorld::CheckChunkColumnsExist(int minX, int minY, int minZ, int maxX, int maxY, int maxZ)
{
	if (maxY >= 0 && minY < 256)
	{
		minX >>= 4;
		minZ >>= 4;
		maxX >>= 4;
		maxZ >>= 4;

		for (int cx = minX; cx <= maxX; ++cx)
		{
			for (int cz = minZ; cz <= maxZ; ++cz)
			{
				if (!ChunkColumnExists(cx, cz))
				{
					return false;
				}
			}
		}

		return true;
	}
	else
	{
		return false;
	}
}

bool ParaEngine::CBlockWorld::ChunkColumnExists(uint16_t chunkX, uint16_t chunkZ)
{
	ChunkLocation chunkPos(chunkX, chunkZ);
	uint16_t y = 0;
	uint16_t x = chunkPos.GetCenterWorldX();
	uint16_t z = chunkPos.GetCenterWorldZ();
	
	BlockRegion* pRegion = GetRegion(x, y, z, x, y, z);
	if (pRegion && ! pRegion->IsLocked())
	{
		return pRegion->GetChunkColumnTimeStamp(x, z)>0;
	}
	return false;
}


bool ParaEngine::CBlockWorld::IsChunkLocked(uint32 worldX, uint32 worldZ)
{
	int16_t regionX = (int16_t)(worldX >> 9);
	int16_t regionZ = (int16_t)(worldZ >> 9);

	BlockRegion* pRegion = GetRegion(regionX, regionZ);
	if (pRegion && !pRegion->IsLocked())
	{
		return false;
	}
	return true;
}

bool ParaEngine::CBlockWorld::IsRemote()
{
	return m_bIsRemote;
}

void ParaEngine::CBlockWorld::SetIsRemote(bool bValue)
{
	m_bIsRemote = bValue;
}


void ParaEngine::CBlockWorld::SetIsServerWorld(bool bValue)
{
	m_bIsServerWorld = bValue;
}

bool ParaEngine::CBlockWorld::IsServerWorld()
{
	return m_bIsServerWorld;
}

void ParaEngine::CBlockWorld::SetLightCalculationStep(uint32 nTicks)
{
	GetLightGrid().SetLightCalculationStep(nTicks);
}

uint32 ParaEngine::CBlockWorld::GetLightCalculationStep()
{
	return GetLightGrid().GetLightCalculationStep();
}

void ParaEngine::CBlockWorld::SetRenderBlocks(bool bValue)
{
	if (m_bRenderBlocks != bValue)
	{
		m_bRenderBlocks = bValue;
		SetVisibleChunkDirty(true);
	}
}

bool ParaEngine::CBlockWorld::IsRenderBlocks()
{
	return m_bRenderBlocks;
}

bool ParaEngine::CBlockWorld::IsUseAsyncLoadWorld() const
{
	return m_bUseAsyncLoadWorld;
}

void ParaEngine::CBlockWorld::SetUseAsyncLoadWorld(bool val)
{
	m_bUseAsyncLoadWorld = val;
}

void ParaEngine::CBlockWorld::OnFrameMove()
{
	for (auto& iter : m_regionCache)
	{
		iter.second->OnFrameMove();
	}
}

int ParaEngine::CBlockWorld::GetNumOfLockedBlockRegion()
{
	int nCount = 0;
	for (auto& iter : m_regionCache)
	{
		if(iter.second->IsLocked())
			nCount++;
	}
	return nCount;
}


int ParaEngine::CBlockWorld::GetNumOfBlockRegion()
{
	return (int)m_regionCache.size();
}

int ParaEngine::CBlockWorld::GetTotalNumOfLoadedChunksInLockedBlockRegion()
{
	int nCount = 0;
	for (auto& iter : m_regionCache)
	{
		if (iter.second->IsLocked())
			nCount += iter.second->GetChunksLoaded();
	}
	return nCount;
}

bool ParaEngine::CBlockWorld::IsVisibleChunkDirty() const
{
	return m_isVisibleChunkDirty;
}

void ParaEngine::CBlockWorld::SetVisibleChunkDirty(bool val)
{
	m_isVisibleChunkDirty = val;
}

BlockReadWriteLock& ParaEngine::CBlockWorld::GetReadWriteLock()
{
	return m_readWriteLock;
}


bool ParaEngine::CBlockWorld::IsGroupByChunkBeforeTexture() const
{
	return m_group_by_chunk_before_texture;
}

void ParaEngine::CBlockWorld::SetGroupByChunkBeforeTexture(bool val)
{
	m_group_by_chunk_before_texture = val;
}

const ParaEngine::Int32x3& ParaEngine::CBlockWorld::GetMinWorldPos() const
{
	return m_minWorldPos;
}

void ParaEngine::CBlockWorld::SetMinWorldPos(const ParaEngine::Int32x3& val)
{
	m_minWorldPos = val;
	m_minRegionX = (std::max)((int32)0, m_minWorldPos.x >> 9);
	m_minRegionZ = (std::max)((int32)0, m_minWorldPos.z >> 9);
}

const ParaEngine::Int32x3& ParaEngine::CBlockWorld::GetMaxWorldPos() const
{
	return m_maxWorldPos;
}

void ParaEngine::CBlockWorld::SetMaxWorldPos(const ParaEngine::Int32x3& val)
{
	m_maxWorldPos = val;
	m_maxRegionX = (std::min)((int32)63, m_maxWorldPos.x >> 9);
	m_maxRegionZ = (std::min)((int32)63, m_maxWorldPos.z >> 9);
}

uint16_t ParaEngine::CBlockWorld::GetMaxCacheRegionCount() const
{
	return m_maxCacheRegionCount;
}

void ParaEngine::CBlockWorld::SetMaxCacheRegionCount(uint16_t val)
{
	if (val >= 4)
	{
		m_maxCacheRegionCount = val;
	}
}


RenderableChunk* ParaEngine::CBlockWorld::GetRenderableChunk(const Int16x3& chunkPos)
{
	if (IsChunkColumnInActiveRange(chunkPos.x, chunkPos.z))
	{
		RenderableChunk* pChunk = &GetActiveChunk(chunkPos.x, chunkPos.y, chunkPos.z);
		if (pChunk->IsDirty() || pChunk->GetChunkPosWs() != chunkPos)
			pChunk = NULL;
		return pChunk;
	}
	return NULL;
}


void ParaEngine::CBlockWorld::ClearOutOfRangeActiveChunkData()
{
	int nChunkColumnRemoved = 0;
	int32 centerX = m_curCamBlockId.x;
	int32 centerZ = m_curCamBlockId.z;

	for (int z = 0; z < m_activeChunkDim; z++)
	{
		int16_t curChunkWZ = m_minActiveChunkId_ws.z + z;
		for (int x = 0; x < m_activeChunkDim; x++)
		{
			int16_t curChunkWX = m_minActiveChunkId_ws.x + x;
			int32 nDist = (int32)(pow(centerX - (curChunkWX * 16 + 8), 2) + pow(centerZ - (curChunkWZ * 16 + 8), 2));

			if (nDist > 0)
				nDist = (int)((Math::Sqrt((float)nDist) + 12)); // 16/2 * 1.414 = 12
			if (nDist > GetRenderDist())
			{
				//if (!GetActiveChunk(curChunkWX, 0, curChunkWZ).IsDirty())
				{
					for (int y = 0; y < m_activeChunkDimY; y++)
					{
						int16_t curChunkWY = m_minActiveChunkId_ws.y + y;

						GetActiveChunk(curChunkWX, curChunkWY, curChunkWZ).ClearChunkData();
					}
					nChunkColumnRemoved++;
				}
			}
		}
	}
	if (nChunkColumnRemoved > 0)
	{
		// OUTPUT_LOG1("nChunkColumnRemoved: %d\n", nChunkColumnRemoved);
	}
}

IAttributeFields* ParaEngine::CBlockWorld::GetChildAttributeObject(const std::string& sName)
{
	for (auto& iter : m_regionCache)
	{
		if (iter.second->GetIdentifier() == sName)
			return iter.second;
	}
	return NULL;
}

IAttributeFields* ParaEngine::CBlockWorld::GetChildAttributeObject(int nRowIndex, int nColumnIndex /*= 0*/)
{
	if (nRowIndex < (int)m_regionCache.size())
	{
		auto iter = m_regionCache.begin();
		std::advance(iter, nRowIndex);
		return iter->second;
	}
	return NULL;
}

int ParaEngine::CBlockWorld::GetChildAttributeObjectCount(int nColumnIndex /*= 0*/)
{
	return (int)m_regionCache.size();
}

const std::string& ParaEngine::CBlockWorld::GetIdentifier()
{
	return m_sName;
}

void ParaEngine::CBlockWorld::SetIdentifier(const std::string& sID)
{
	m_sName = sID;
}

int ParaEngine::CBlockWorld::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	// install parent fields if there are any. Please replace __super with your parent class name.
	IAttributeFields::InstallFields(pClass, bOverride);

	PE_ASSERT(pClass != NULL);
	
	pClass->AddField("BlockRenderMethod", FieldType_Int, (void*)SetBlockRenderMethod_s, (void*)GetBlockRenderMethod_s, NULL, NULL, bOverride);

	pClass->AddField("ResumeLightUpdate", FieldType_void, (void*)ResumeLightUpdate_s, NULL, NULL, "", bOverride);
	pClass->AddField("SuspendLightUpdate", FieldType_void, (void*)SuspendLightUpdate_s, NULL, NULL, "", bOverride);

	pClass->AddField("ResetAllLight", FieldType_void, (void*)ResetAllLight_s, NULL, NULL, "", bOverride);

	pClass->AddField("LockWorld", FieldType_void, (void*)LockWorld_s, NULL, NULL, "", bOverride);
	pClass->AddField("UnlockWorld", FieldType_void, (void*)UnlockWorld_s, NULL, NULL, "", bOverride);

	pClass->AddField("IsLightUpdateSuspended", FieldType_Bool, NULL, (void*)IsLightUpdateSuspended_s, NULL, NULL, bOverride);
	
	pClass->AddField("SetChunkColumnTimeStamp", FieldType_Float_Float_Float, (void*)SetChunkColumnTimeStamp_s, NULL, NULL, NULL, bOverride);

	pClass->AddField("RenderDist", FieldType_Int, (void*)SetRenderDist_s, (void*)GetRenderDist_s, NULL, NULL, bOverride);
	
	pClass->AddField("DirtyColumnCount", FieldType_Int, NULL, (void*)GetDirtyColumnCount_s, NULL, NULL, bOverride);
	pClass->AddField("DirtyBlockCount", FieldType_Int, NULL, (void*)GetDirtyBlockCount_s, NULL, NULL, bOverride);
	pClass->AddField("IsReadOnly", FieldType_Bool, (void*)SetReadOnly_s, (void*)IsReadOnly_s, NULL, NULL, bOverride);
	pClass->AddField("IsRemote", FieldType_Bool, (void*)SetIsRemote_s, (void*)IsRemote_s, NULL, NULL, bOverride);
	pClass->AddField("IsServerWorld", FieldType_Bool, (void*)SetIsServerWorld_s, (void*)IsServerWorld_s, NULL, NULL, bOverride);
	pClass->AddField("SaveLightMap", FieldType_Bool, (void*)SetSaveLightMap_s, (void*)IsSaveLightMap_s, NULL, NULL, bOverride);
	pClass->AddField("UseAsyncLoadWorld", FieldType_Bool, (void*)SetUseAsyncLoadWorld_s, (void*)IsUseAsyncLoadWorld_s, NULL, NULL, bOverride);
	pClass->AddField("UseLinearTorchBrightness", FieldType_Bool, (void*)UseLinearTorchBrightness_s, (void*)0, NULL, NULL, bOverride);
	pClass->AddField("GeneratorScript", FieldType_String, (void*)SetGeneratorScript_s, (void*)GetGeneratorScript_s, NULL, NULL, bOverride);
	
	pClass->AddField("OnBeforeLoadBlockRegion", FieldType_String, (void*)SetBeforeLoadBlockRegion_s, (void*)GetBeforeLoadBlockRegion_s, CAttributeField::GetSimpleSchemaOfScript(), "", bOverride);
	pClass->AddField("OnLoadBlockRegion", FieldType_String, (void*)SetLoadBlockRegion_s, (void*)GetLoadBlockRegion_s, CAttributeField::GetSimpleSchemaOfScript(), "", bOverride);
	pClass->AddField("OnUnLoadBlockRegion", FieldType_String, (void*)SetUnLoadBlockRegion_s, (void*)GetUnLoadBlockRegion_s, CAttributeField::GetSimpleSchemaOfScript(), "", bOverride);
	pClass->AddField("OnSaveRegionCallbackScript", FieldType_String, (void*)SetSaveRegionCallbackScript_s, (void*)GetSaveRegionCallbackScript_s, NULL, NULL, bOverride);

	pClass->AddField("LightCalculationStep", FieldType_Int, (void*)SetLightCalculationStep_s, (void*)GetLightCalculationStep_s, NULL, NULL, bOverride);
	pClass->AddField("RenderBlocks", FieldType_Bool, (void*)SetRenderBlocks_s, (void*)IsRenderBlocks_s, NULL, NULL, bOverride);
	pClass->AddField("NumOfLockedBlockRegion", FieldType_Int, (void*)NULL, (void*)GetNumOfLockedBlockRegion_s, NULL, NULL, bOverride);
	pClass->AddField("NumOfBlockRegion", FieldType_Int, (void*)NULL, (void*)GetNumOfBlockRegion_s, NULL, NULL, bOverride);
	pClass->AddField("MaxCacheRegionCount", FieldType_Int, (void*)SetMaxCacheRegionCount_s, (void*)GetMaxCacheRegionCount_s, NULL, NULL, bOverride);
	pClass->AddField("TotalNumOfLoadedChunksInLockedBlockRegion", FieldType_Int, (void*)NULL, (void*)GetTotalNumOfLoadedChunksInLockedBlockRegion_s, NULL, NULL, bOverride);
	pClass->AddField("SunIntensity", FieldType_Float, (void*)SetSunIntensity_s, (void*)GetSunIntensity_s, NULL, NULL, bOverride);

	pClass->AddField("MinWorldPos", FieldType_Vector3, (void*)SetMinWorldPos_s, (void*)GetMinWorldPos_s, NULL, NULL, bOverride);
	pClass->AddField("MaxWorldPos", FieldType_Vector3, (void*)SetMaxWorldPos_s, (void*)GetMaxWorldPos_s, NULL, NULL, bOverride);
	pClass->AddField("TotalChunksInMemory", FieldType_Int, (void*)0, (void*)GetTotalChunksInMemory_s, NULL, NULL, bOverride);
	pClass->AddField("TotalRenderableChunksInMemory", FieldType_Int, (void*)0, (void*)GetTotalRenderableChunksInMemory_s, NULL, NULL, bOverride);

	
	return S_OK;
}

//-----------------------------------------------------------------------------
// Class:	Client side light data calculation
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2012.11.26
/*  performance note:
The RefreshLight() function for a single block of second pass can take as long as
10-90ms about (1000 to 15000 queued block to recalculate)
*/
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BlockWorld.h"
#include "BlockRegion.h"
#include "BlockFacing.h"
#include "BlockCommon.h"
#include "SceneState.h"
#include <boost/bind.hpp>
#include "ParaTime.h"
#include "BlockLightGridClient.h"
#include "BlockFacing.h"

/** whether to use separate thread for light calculation. */
#define ASYNC_LIGHT_CALCULATION

/** define this to enable debug performance log output. */
//#define PRINT_PERF_LOG

namespace ParaEngine
{
	CBlockLightGridClient::CBlockLightGridClient(int32_t chunkCacheDim, CBlockWorld* pBlockWorld)
		: CBlockLightGridBase(pBlockWorld), m_bIsLightThreadStarted(false), m_bIsAsyncLightCalculation(true),
		m_minChunkIdX_ws(-1000), m_minChunkIdZ_ws(-1000), m_maxChunkIdX_ws(-1), m_maxChunkIdZ_ws(-1), m_minLightBlockIdX(-1000), m_maxLightBlockIdX(-1),
		m_minLightBlockIdZ(-1000), m_maxLightBlockIdZ(-1), m_centerChunkIdX_ws(-1), m_centerChunkIdZ_ws(-1), m_max_cells_per_frame(500), m_max_cells_left_per_frame(5000), m_nDirtyBlocksCount(0)
	{
		SetLightGridSize(chunkCacheDim);
	}

	CBlockLightGridClient::~CBlockLightGridClient()
	{
		OnLeaveWorld();
		if (m_light_thread.joinable())
		{
			OUTPUT_LOG("begin exiting light thread ...\n");
			m_light_thread.join();
			OUTPUT_LOG("light thread exited \n");
		}
	}

	void CBlockLightGridClient::OnEnterWorld()
	{
		std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
		m_minChunkIdX_ws = -1000;
		m_minChunkIdZ_ws = -1000;
		m_maxChunkIdX_ws = -1;
		m_maxChunkIdZ_ws = -1;
		m_minLightBlockIdX = -1000;
		m_maxLightBlockIdX = -1;
		m_minLightBlockIdZ = -1000;
		m_maxLightBlockIdZ = -1;
		m_centerChunkIdX_ws = -1;
		m_centerChunkIdZ_ws = -1;
		m_nDirtyBlocksCount = 0;

		m_dirtyColumns.clear();
		m_loaded_columns.clear();
		m_forced_chunks.clear();
		m_quick_loaded_columns.clear();
		m_blocksNeedLightRecalcuation.resize(32 * 32 * 32);
	}

	void CBlockLightGridClient::OnLeaveWorld()
	{
		//release memory used by stl
		{
			std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
			m_loaded_columns.clear();
			m_forced_chunks.clear();
			m_quick_loaded_columns.clear();
			m_dirtyColumns.clear();
			m_nDirtyBlocksCount = 0;
		}

		if (m_pBlockWorld && m_bIsLightThreadStarted && m_light_thread.joinable())
		{
			if (!m_pBlockWorld->GetReadWriteLock().HasWriterLock())
			{
				m_light_thread.join();
			}
			else
			{
				// this code must be called from the main thread which owns the writer lock
				PE_ASSERT(m_pBlockWorld->GetReadWriteLock().IsCurrentThreadHasWriterLock());
				Scoped_WriterUnlock<>  unlock_(m_pBlockWorld->GetReadWriteLock());
				m_light_thread.join();
			}
		}
		{
			std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
			m_dirtyCells.clear();
		}
	}

	void CBlockLightGridClient::OnWorldMove(uint16_t centerChunkX, uint16_t centerChunkZ)
	{
		m_centerChunkIdX_ws = centerChunkX;
		m_centerChunkIdZ_ws = centerChunkZ;
		int32_t chunkCacheRadius = m_nLightGridChunkSize / 2;
		int32_t newChunkStartX = centerChunkX - chunkCacheRadius;
		int32_t newChunkStartZ = centerChunkZ - chunkCacheRadius;

		int32_t deltaChunkX = newChunkStartX - m_minChunkIdX_ws;
		int32_t deltaChunkZ = newChunkStartZ - m_minChunkIdZ_ws;

		if (deltaChunkX == 0 && deltaChunkZ == 0)
			return;

		m_minChunkIdX_ws = newChunkStartX;
		m_minChunkIdZ_ws = newChunkStartZ;
		m_maxChunkIdX_ws = m_minChunkIdX_ws + m_nLightGridChunkSize;
		m_maxChunkIdZ_ws = m_minChunkIdZ_ws + m_nLightGridChunkSize;

		m_minLightBlockIdX = m_minChunkIdX_ws * BlockConfig::g_chunkBlockDim;
		m_minLightBlockIdZ = m_minChunkIdZ_ws * BlockConfig::g_chunkBlockDim;

		m_maxLightBlockIdX = m_minLightBlockIdX + m_nLightGridChunkSize * BlockConfig::g_chunkBlockDim;
		m_maxLightBlockIdZ = m_minLightBlockIdZ + m_nLightGridChunkSize * BlockConfig::g_chunkBlockDim;

		if (abs(deltaChunkX) >= m_nLightGridChunkSize || abs(deltaChunkZ) >= m_nLightGridChunkSize)
		{
			for (int32_t x = 0; x < m_nLightGridChunkSize; x++)
			{
				for (int32_t z = 0; z < m_nLightGridChunkSize; z++)
				{
					int32_t curChunkIdX_ws = m_minChunkIdX_ws + x;
					int32_t curChunkIdZ_ws = m_minChunkIdZ_ws + z;

					if (curChunkIdX_ws >= 0 && curChunkIdX_ws < 0xffff
						&& curChunkIdZ_ws >= 0 && curChunkIdZ_ws < 0xffff)
					{
						if (!IsChunkColumnLoaded(curChunkIdX_ws, curChunkIdZ_ws))
							AddDirtyColumn(curChunkIdX_ws, curChunkIdZ_ws);
					}
				}
			}
		}
		else
		{
			int32_t startChunkX_ws = m_minChunkIdX_ws;
			if (deltaChunkX >= 0)
				startChunkX_ws = startChunkX_ws + m_nLightGridChunkSize - deltaChunkX;

			int32_t startChunkZ_ws = m_minChunkIdZ_ws;
			if (deltaChunkZ >= 0)
				startChunkZ_ws = startChunkZ_ws + m_nLightGridChunkSize - deltaChunkZ;

			//-------update light chunks alone x axis-------------
			for (int16_t x = 0; x < abs(deltaChunkX); x++)
			{
				uint32_t curChunkX_ws = startChunkX_ws + x;

				for (int16_t z = 0; z < m_nLightGridChunkSize; z++)
				{
					int32_t curChunkZ_ws = m_minChunkIdZ_ws + z;
					if (!IsChunkColumnLoaded(curChunkX_ws, curChunkZ_ws))
						AddDirtyColumn(curChunkX_ws, curChunkZ_ws);
				}
			}
			startChunkX_ws = m_minChunkIdX_ws;

			//--------update light chunks alone z axis------------
			for (int16_t z = 0; z < abs(deltaChunkZ); z++)
			{
				int32_t curChunkZ_ws = startChunkZ_ws + z;
				for (int x = 0; x < m_nLightGridChunkSize; x++)
				{
					int32_t curChunkX_ws = m_minChunkIdX_ws + x;
					if (!IsChunkColumnLoaded(curChunkX_ws, curChunkZ_ws))
						AddDirtyColumn(curChunkX_ws, curChunkZ_ws);
				}
			}
		}
	}

	bool CBlockLightGridClient::GetBrightness(Uint16x3& blockId_ws, uint8_t* brightness, int nSize, int nLightType)
	{
		if (brightness == nullptr)
			return false;

		Uint16x3 curBlockId_ws;
		for (int i = 0; i < nSize; i++)
		{
			curBlockId_ws.x = blockId_ws.x + BlockCommon::NeighborOfsTable[i].x;
			curBlockId_ws.y = blockId_ws.y + BlockCommon::NeighborOfsTable[i].y;
			// fix curBlockId_ws.y may be 65535, since it is unsigned and that 0 -1 = 65535, not used since will only check curBlockId_ws.y >= 256 immediately afterward. 
			// curBlockId_ws.y = curBlockId_ws.y == 0xffff ? 0 : curBlockId_ws.y; 
			curBlockId_ws.z = blockId_ws.z + BlockCommon::NeighborOfsTable[i].z;

			if (nLightType == 0)
			{
				brightness[i] = 0;
			}
			uint8 nSunLight = 0;
			uint8 nBlockLight = 0;

			BlockIndex blockIndex = CalcLightDataIndex(curBlockId_ws, false);
			if (blockIndex.m_pChunk)
			{
				LightData* pLightData = GetLightData(blockIndex);
				if (nLightType != 1)
					nBlockLight = pLightData->GetBrightness(false);
				if (nLightType != 0)
				{
					if (blockIndex.m_pChunk->CanBlockSeeTheSkyWS(curBlockId_ws.x, curBlockId_ws.y, curBlockId_ws.z)) 
					{
						if (pLightData->GetBrightness(true) != 15)
							pLightData->SetBrightness(15, true);
						nSunLight = 15;
					}
					else
						nSunLight = pLightData->GetBrightness(true);
				}
			}
			else
			{
				if (nLightType != 0)
					nSunLight = CanBlockSeeTheSky(curBlockId_ws.x, curBlockId_ws.y, curBlockId_ws.z) ? 15 : 0;
			}

			if (nLightType == -1)
			{
				nSunLight = (uint8_t)(nSunLight * m_pBlockWorld->GetSunIntensity());
				brightness[i] = (nBlockLight > nSunLight ? nBlockLight : nSunLight);
			}
			else if (nLightType == 2)
			{
				brightness[i] = nBlockLight;
				brightness[i + nSize] = nSunLight;
			}
			else if (nLightType == 3)
			{
				brightness[i + nSize] = nBlockLight;
				brightness[i + nSize * 2] = nSunLight;
				nSunLight = (uint8_t)(nSunLight * m_pBlockWorld->GetSunIntensity());
				brightness[i] = (nBlockLight > nSunLight ? nBlockLight : nSunLight);
			}
			else
				brightness[i] = (nLightType == 1) ? nSunLight : nBlockLight;
		}
		return true;
	}

	bool CBlockLightGridClient::IsLightDirty(Uint16x3& blockId_ws)
	{
		uint16_t chunk_ws_x = blockId_ws.x >> 4;
		uint16_t chunk_ws_y = blockId_ws.y >> 4;
		uint16_t chunk_ws_z = blockId_ws.z >> 4;

		uint16_t cx = blockId_ws.x & 0xf;
		uint16_t cy = blockId_ws.y & 0xf;
		uint16_t cz = blockId_ws.z & 0xf;
		uint16_t packedBlockId_cs = cx + (cz << 4) + (cy << 8); // y in higher bits

		uint64_t key = (((uint64_t)chunk_ws_y) << 48) + (((uint64_t)chunk_ws_x) << 32) + (((uint64_t)chunk_ws_z) << 16) + packedBlockId_cs; // chuck y in higher bits. 

		return (m_dirtyCells.find(key) != m_dirtyCells.end());
	}

	void CBlockLightGridClient::SetLightDirty(Uint16x3& blockId_ws, bool isSunLight, int8 nUpdateRange)
	{
		if (m_suspendLightUpdate)
			return;

		// uint64_t key = ((uint64_t)blockId_ws.x<<32) + ((uint64_t)blockId_ws.y<<16) + blockId_ws.z;

		// make a key: where blocks inside the same 16*16*16 chunk are grouped together. and the higher chunk (y) is sorted in front. 

		uint16_t chunk_ws_x = blockId_ws.x >> 4;
		uint16_t chunk_ws_y = blockId_ws.y >> 4;
		uint16_t chunk_ws_z = blockId_ws.z >> 4;

		uint16_t cx = blockId_ws.x & 0xf;
		uint16_t cy = blockId_ws.y & 0xf;
		uint16_t cz = blockId_ws.z & 0xf;
		uint16_t packedBlockId_cs = cx + (cz << 4) + (cy << 8); // y in higher bits

		uint64_t key = (((uint64_t)chunk_ws_y) << 48) + (((uint64_t)chunk_ws_x) << 32) + (((uint64_t)chunk_ws_z) << 16) + packedBlockId_cs; // chuck y in higher bits. 


		auto got = m_dirtyCells.find(key);
		if (got == m_dirtyCells.end())
		{
			uint8_t sunLightRange, pointLightRange;
			if (isSunLight)
			{
				sunLightRange = nUpdateRange;
				pointLightRange = -1;
			}
			else
			{
				sunLightRange = -1;
				pointLightRange = nUpdateRange;
			}
			m_dirtyCells.insert(std::make_pair(key, Light(blockId_ws, sunLightRange, pointLightRange)));
		}
		else
		{
			if (isSunLight && nUpdateRange > got->second.sunlightUpdateRange)
				got->second.sunlightUpdateRange = nUpdateRange;
			else if (!isSunLight && nUpdateRange > got->second.pointLightUpdateRange)
				got->second.pointLightUpdateRange = nUpdateRange;
		}
	}

	void CBlockLightGridClient::NotifyBlockHeightChanged(uint16_t blockIdX_ws, uint16_t blockIdZ_ws, ChunkMaxHeight& prevBlockHeight)
	{
		if (IsChunkColumnLoadedWorldPos(blockIdX_ws, 0, blockIdZ_ws))
		{
			ChunkMaxHeight heightMap[6];
			m_pBlockWorld->GetMaxBlockHeightWatchingSky(blockIdX_ws, blockIdZ_ws, heightMap);

			Uint16x3 curBlockId_ws(blockIdX_ws, 0, blockIdZ_ws);
			if (heightMap[0].GetMaxHeight() > prevBlockHeight.GetMaxSolidHeight() && prevBlockHeight.GetMaxSolidHeight() > 0)
			{
				for (int y = prevBlockHeight.GetMaxSolidHeight() + 1; y <= heightMap[0].GetMaxHeight(); y++)
				{
					curBlockId_ws.y = y;
					SetLightDirty(curBlockId_ws, true, 1);
				}
			}

			int max = heightMap[0].GetMaxHeight();
			for (int i = 1; i<5; i++)
			{
				if (heightMap[i].GetMaxHeight() > max)
					max = heightMap[i].GetMaxHeight();
			}

			if (max >= heightMap[0].GetMaxSolidHeight())
			{
				EmitSunLight(blockIdX_ws, blockIdZ_ws);

				if (IsChunkColumnLoadedWorldPos(blockIdX_ws - 1, 0, blockIdZ_ws))
					EmitSunLight(blockIdX_ws - 1, blockIdZ_ws);
				if (IsChunkColumnLoadedWorldPos(blockIdX_ws + 1, 0, blockIdZ_ws))
					EmitSunLight(blockIdX_ws + 1, blockIdZ_ws);
				if (IsChunkColumnLoadedWorldPos(blockIdX_ws, 0, blockIdZ_ws - 1))
					EmitSunLight(blockIdX_ws, blockIdZ_ws - 1);
				if (IsChunkColumnLoadedWorldPos(blockIdX_ws, 0, blockIdZ_ws + 1))
					EmitSunLight(blockIdX_ws, blockIdZ_ws + 1);
			}
		}
	}

	void CBlockLightGridClient::StartLightThread()
	{
		if (!m_bIsLightThreadStarted)
		{
			m_bIsLightThreadStarted = true;
			try
			{
				m_light_thread = std::thread(std::bind(&CBlockLightGridClient::LightThreadProc, this));
			}
			catch (...)
			{
				m_bIsLightThreadStarted = false;
				// some other exception (print a diagnostic!)
				OUTPUT_LOG("error: m_light_thread unknown error\n");
			}
		}
	}

	void CBlockLightGridClient::LightThreadProc()
	{
		Scoped_ReadLock<BlockReadWriteLock> lock_(m_pBlockWorld->GetReadWriteLock());

		m_bIsLightThreadStarted = true;
		unsigned int nStartTime = GetTickCount();
		unsigned int nLightCalculationTimeLeft = GetLightCalculationStep();

		int32_t processedCount = 0;
		m_nDirtyBlocksCount = (int)m_dirtyCells.size();

		// #define DISABLE_LIGHTING_CALCULATION_TEST_ONLY
#ifdef DISABLE_LIGHTING_CALCULATION_TEST_ONLY
		m_dirtyColumns.clear();
		m_dirtyCells.clear();
#endif
		// call this function regularly to yield CPU to writer thread only if they are waiting to write data. 
#define CHECK_YIELD_CPU_TO_WRITER   if(m_pBlockWorld->GetReadWriteLock().HasWaitingWritersAndSingleReader()){ \
	m_nDirtyBlocksCount = (int)(m_dirtyCells.size() + processedCount); \
	++nYieldCPUTimes;\
	lock_.unlock(); \
	lock_.lock(); \
	if(!m_pBlockWorld->IsInBlockWorld()){\
		m_bIsLightThreadStarted = false;\
		return;\
				}\
						}

		while (m_pBlockWorld->IsInBlockWorld())
		{
			// this function is called on each pre-render frame move to update light values if necessary. 
			processedCount = 0;

			int max_cells_left_per_frame = 999999;// m_max_cells_left_per_frame;
			int max_cells_per_frame = 50;//  m_max_cells_per_frame;
			int32_t maxColumnPerFrame = 1;
			int nYieldCPUTimes = 0;
			// how many chunk columns to update every frame move. 

			if ((int)m_dirtyCells.size() < max_cells_per_frame * 2 && (m_dirtyColumns.size() > 0 || !m_forced_chunks.empty()))
			{
				m_closest_chunks.clear();
				ChunkLocation chunkEye((m_minChunkIdX_ws + m_maxChunkIdX_ws) / 2, (m_minChunkIdZ_ws + m_maxChunkIdZ_ws) / 2);

				{
					std::unique_lock<std::recursive_mutex> DirtyColumnLock_(m_mutex);
					for (auto it = m_dirtyColumns.begin(); it != m_dirtyColumns.end();)
					{
						const ChunkLocation& curChunkId_ws = *it;
						uint16_t chunkX_ws = curChunkId_ws.m_chunkX;
						uint16_t chunkZ_ws = curChunkId_ws.m_chunkZ;
						if (chunkX_ws >= m_minChunkIdX_ws && chunkX_ws < m_maxChunkIdX_ws
							&& chunkZ_ws >= m_minChunkIdZ_ws && chunkZ_ws < m_maxChunkIdZ_ws)
						{
							if (m_pBlockWorld->DoChunksNearChunkExist(curChunkId_ws.GetCenterWorldX(), 0, curChunkId_ws.GetCenterWorldZ(), 16))
							{
								// only fully executed insertions may happen, so iterators are still valid. 
								int nDist = curChunkId_ws.DistanceToSquared(chunkEye);
								int nSize = (int)(m_closest_chunks.size());
								if (nSize < maxColumnPerFrame)
									m_closest_chunks.push_back(std::pair<ChunkLocation, int32_t>(curChunkId_ws, nDist));
								else
								{

									for (int i = 0; i < nSize; ++i)
									{
										if (m_closest_chunks[i].second > nDist)
										{
											m_closest_chunks[i] = std::pair<ChunkLocation, int32_t>(curChunkId_ws, nDist);
											break;
										}
									}
								}
								it++;
							}
							else
							{
								it++;
							}
						}
						else
						{
							it = m_dirtyColumns.erase(it);
						}
					}

					int nNumOfForceChunk = 0;
					while (!m_forced_chunks.empty() && (nNumOfForceChunk < maxColumnPerFrame))
					{
						m_closest_chunks.push_back(std::pair<ChunkLocation, int32_t>(m_forced_chunks.back(), 0));
						m_forced_chunks.pop_back();
						nNumOfForceChunk++;
					}

					int nSize = (int)(m_closest_chunks.size());
					for (int i = 0; i < nSize; ++i)
					{
						const ChunkLocation& curChunkId_ws = m_closest_chunks[i].first;
						RemoveDirtyColumn(curChunkId_ws);
					}
				}

				int nSize = (int)(m_closest_chunks.size());
				for (int i = 0; i < nSize; ++i)
				{
					processedCount++;
					const ChunkLocation& curChunkId_ws = m_closest_chunks[i].first;
					uint16_t chunkX_ws = curChunkId_ws.m_chunkX;
					uint16_t chunkZ_ws = curChunkId_ws.m_chunkZ;

					m_pBlockWorld->RefreshAllLightsInColumn(chunkX_ws, chunkZ_ws);

					CHECK_YIELD_CPU_TO_WRITER;

					uint16_t chunkBlockX = chunkX_ws * BlockConfig::g_chunkBlockDim;
					uint16_t chunkBlockZ = chunkZ_ws * BlockConfig::g_chunkBlockDim;
					for (int x = 0; x < BlockConfig::g_chunkBlockDim; x++)
					{
						for (int z = 0; z < BlockConfig::g_chunkBlockDim; z++)
						{
							EmitSunLight(chunkBlockX + x, chunkBlockZ + z);
							CHECK_YIELD_CPU_TO_WRITER;
						}
					}
					SetLightingInChunkColumnInitialized(chunkX_ws, chunkZ_ws);

					SetColumnPreloaded(chunkX_ws, chunkZ_ws);
					// RemoveDirtyColumn(curChunkId_ws);
				}
				m_closest_chunks.clear();
			}

			int nDirtyCellCount = (int)m_dirtyCells.size();
			if (nDirtyCellCount > 0)
			{
				processedCount++;
				m_nDirtyBlocksCount = nDirtyCellCount;
				int nBlocksToCalculateThisFrame = max_cells_per_frame;
				if ((nDirtyCellCount - max_cells_left_per_frame) > max_cells_per_frame)
				{
					nBlocksToCalculateThisFrame = nDirtyCellCount - max_cells_left_per_frame;
				}

				for (auto it = m_dirtyCells.begin(); it != m_dirtyCells.end() && nBlocksToCalculateThisFrame > 0;)
				{
					Light& light_data = it->second;
					if (!IsLightUpdateSuspended())
					{
						--nBlocksToCalculateThisFrame;
						if (light_data.sunlightUpdateRange >= 0){
							if (!RefreshLight(light_data.blockId, true, light_data.sunlightUpdateRange, &lock_, &nYieldCPUTimes))
							{
								m_bIsLightThreadStarted = false;
								return;
							}
						}
						if (light_data.pointLightUpdateRange >= 0){
							if (!RefreshLight(light_data.blockId, false, light_data.pointLightUpdateRange, &lock_, &nYieldCPUTimes))
							{
								m_bIsLightThreadStarted = false;
								return;
							}
						}
						it = m_dirtyCells.erase(it);
					}
					else
						nBlocksToCalculateThisFrame = 0;
				}
			}

			unsigned int nFinishTime = GetTickCount();
			unsigned int nStepDurationTicks = Math::Max(nFinishTime - nStartTime, (unsigned int)1);

			if (nLightCalculationTimeLeft < nStepDurationTicks)
			{
				nLightCalculationTimeLeft = GetLightCalculationStep();
				// since read/write lock is used, this function will try to notify any waiting writers. 

				lock_.unlock();

				if (m_dirtyCells.size() == 0 && processedCount == 0){
					m_nDirtyBlocksCount = 0;
					SLEEP(10);
				}
				while (IsLightUpdateSuspended() && m_pBlockWorld->IsInBlockWorld()){
					SLEEP(1);
				}
				// since we are using our own read/write lock, this function will block until writers are freed. 
				// in most cases when no writer request, it will lock immediately again, thus utilizing more CPU to process remaining light cells.  
				lock_.lock();
				nStartTime = GetTickCount();
			}
			else
			{
				// sometimes GetTickCount will wrap around INT32, so this prevents it. 
				nStartTime = nFinishTime;
				nLightCalculationTimeLeft = Math::Min(nLightCalculationTimeLeft - nStepDurationTicks, (unsigned int)GetLightCalculationStep());

				if (m_dirtyCells.size() == 0 && processedCount == 0){
					m_nDirtyBlocksCount = 0;
					lock_.unlock();
					SLEEP(10);
					lock_.lock();
				}
			}
		}
		m_nDirtyBlocksCount = 0;
		m_bIsLightThreadStarted = false;
	}

	void CBlockLightGridClient::UpdateLighting()
	{
		if (!(m_pBlockWorld->IsInBlockWorld()))
		{
			return;
		}

		if (IsAsyncLightCalculation())
		{
			StartLightThread();
		}
		else
		{
#ifndef	ASYNC_LIGHT_CALCULATION
			if (m_dirtyColumns.size() == 0 && m_dirtyCells.size() == 0)
				return;
			// this function is called on each pre-render frame move to update light values if necessary. 
			int32_t processedCount = 0;

			bool bIsCameraMoved = CGlobals::GetSceneState()->m_bCameraMoved;

			int max_cells_left_per_frame = m_max_cells_left_per_frame;
			int max_cells_per_frame = m_max_cells_per_frame;
			int32_t maxColumnPerFrame = 1;

			if (bIsCameraMoved)
			{
				max_cells_per_frame = 50;
				max_cells_left_per_frame = 999999999;

				if ((int)m_dirtyCells.size() > max_cells_per_frame)
					maxColumnPerFrame = 0;
				else
					maxColumnPerFrame = 1;
			}
			else
			{
				/*if((int)m_dirtyCells.size() > max_cells_per_frame)
				{
				maxColumnPerFrame = 0;
				}*/
			}

			// how many chunk columns to update every frame move. 
			// TODO: shall we calculate from near to far. 
			// m_dirtyColumns should use a hash function to sort by distance. 
			// TODO: shall we only calculate when m_dirtyCells is empty. 

			for (auto it = m_dirtyColumns.begin(); it != m_dirtyColumns.end(); )
			{
				const ChunkLocation& curChunkId_ws = *it;
				uint16_t chunkX_ws = curChunkId_ws.m_chunkX;
				uint16_t chunkZ_ws = curChunkId_ws.m_chunkZ;
				if (chunkX_ws >= m_minChunkIdX_ws && chunkX_ws < m_maxChunkIdX_ws
					&& chunkZ_ws >= m_minChunkIdZ_ws && chunkZ_ws < m_maxChunkIdZ_ws)
				{
					if (m_pBlockWorld->DoChunksNearChunkExist(curChunkId_ws.GetCenterWorldX(), 0, curChunkId_ws.GetCenterWorldZ(), 16))
					{
						if (processedCount < maxColumnPerFrame)
						{
							SetColumnPreloaded(chunkX_ws, chunkZ_ws);

							m_pBlockWorld->RefreshAllLightsInColumn(chunkX_ws, chunkZ_ws);

							uint16_t chunkBlockX = chunkX_ws * BlockConfig::g_chunkBlockDim;
							uint16_t chunkBlockZ = chunkZ_ws * BlockConfig::g_chunkBlockDim;
							for (int x = 0; x < BlockConfig::g_chunkBlockDim; x++)
							{
								for (int z = 0; z < BlockConfig::g_chunkBlockDim; z++)
								{
									EmitSunLight(chunkBlockX + x, chunkBlockZ + z);
								}
							}
							processedCount++;
							it = m_dirtyColumns.erase(it);
						}
						else
							it++;
					}
					else
					{
						it++;
					}
				}
				else
				{
					it = m_dirtyColumns.erase(it);
				}
			}


			int nDirtyCellCount = (int)m_dirtyCells.size();
			if (nDirtyCellCount > 0)
			{
				int nBlocksToCalculateThisFrame = max_cells_per_frame;
				if ((nDirtyCellCount - max_cells_left_per_frame) > max_cells_per_frame)
				{
					nBlocksToCalculateThisFrame = nDirtyCellCount - max_cells_left_per_frame;
				}
				// pass 1: first calculate those near the eye center
				/*for(auto it = m_dirtyCells.begin();it != m_dirtyCells.end() && nBlocksToCalculateThisFrame>0;)
				{
				Light& light_data = it->second;
				if(light_data.blockId.x >= m_minLightBlockIdX && light_data.blockId.x <= m_maxLightBlockIdX && light_data.blockId.z >= m_minLightBlockIdZ && light_data.blockId.z <= m_maxLightBlockIdZ)
				{
				-- nBlocksToCalculateThisFrame;
				if(light_data.sunLightValue > 0)
				EmitLight(light_data.blockId,light_data.sunLightValue,true);
				else if(light_data.sunLightValue == 0)
				RefreshLight(light_data.blockId, true);

				if(light_data.pointLightValue > 0)
				EmitLight(light_data.blockId,light_data.pointLightValue, false);
				else if(light_data.pointLightValue == 0)
				RefreshLight(light_data.blockId, false);
				}

				it = m_dirtyCells.erase(it);
				}*/

				// pass 2: calculate everything else in any order. 
				for (auto it = m_dirtyCells.begin(); it != m_dirtyCells.end() && nBlocksToCalculateThisFrame > 0;)
				{
					Light& light_data = it->second;
					if (light_data.blockId.x >= m_minLightBlockIdX && light_data.blockId.x <= m_maxLightBlockIdX && light_data.blockId.z >= m_minLightBlockIdZ && light_data.blockId.z <= m_maxLightBlockIdZ)
					{
						--nBlocksToCalculateThisFrame;
						if (light_data.sunlightUpdateRange > 0)
							EmitLight(light_data.blockId, light_data.sunlightUpdateRange, true);
						else if (light_data.sunlightUpdateRange == 0)
							RefreshLight(light_data.blockId, true);

						if (light_data.pointLightUpdateRange > 0)
							EmitLight(light_data.blockId, light_data.pointLightUpdateRange, false);
						else if (light_data.pointLightUpdateRange == 0)
							RefreshLight(light_data.blockId, false);
					}

					it = m_dirtyCells.erase(it);
				}
			}
#endif
		}
	}

	int CBlockLightGridClient::ForceAddChunkColumn(int chunkX_ws, int chunkZ_ws)
	{
		std::unique_lock<std::recursive_mutex> Lock_(m_mutex);

		if (IsChunkColumnLoaded(chunkX_ws, chunkZ_ws))
			return 0;
		if (!m_pBlockWorld->DoChunksNearChunkExist(chunkX_ws * 16, 0, chunkZ_ws * 16, 16))
		{
			return -1;
		}

		for (const ChunkLocation& chunkPos : m_forced_chunks)
		{
			if (chunkPos.m_chunkX == chunkX_ws && chunkPos.m_chunkZ == chunkZ_ws)
				return 2;
		}
		m_forced_chunks.push_back(ChunkLocation(chunkX_ws, chunkZ_ws));

		return 2;
	}

	int CBlockLightGridClient::GetForcedChunkColumnCount()
	{
		std::unique_lock<std::recursive_mutex> Lock_(m_mutex);
		return m_forced_chunks.size();
	}

	// blocks higher than the highest solid block in the height map can sky. Note, the top most opaque block can not see the sky. 
	bool CBlockLightGridClient::CanBlockSeeTheSky(uint16 x, uint16 y, uint16 z)
	{
		ChunkMaxHeight* pHeight = m_pBlockWorld->GetHighestBlock(x, z);
		if (pHeight)
			return pHeight->GetMaxSolidHeight() < y;
		else
			return true;
	}

	int32 CBlockLightGridClient::GetSavedLightValue(int32 x, int32 y, int32 z, bool isSunLight)
	{
		if (y >= 0 && y < BlockConfig::g_regionBlockDimY && x >= 0 && z >= 0)
		{
			Uint16x3 curBlockId_ws((uint16)x, (uint16)y, (uint16)z);

			BlockIndex blockIndex = CalcLightDataIndex(curBlockId_ws);
			if (blockIndex.m_pChunk)
			{
				auto lightData = GetLightData(blockIndex);
				if (isSunLight)
				{
					if (blockIndex.m_pChunk->CanBlockSeeTheSkyWS(curBlockId_ws.x, curBlockId_ws.y, curBlockId_ws.z)) 
					{
						if (lightData->GetBrightness(true) != 15)
							lightData->SetBrightness(15, true);
						return 15;
					}
					else
						return lightData->GetBrightness(true);
				}
				else
				{
					return lightData->GetBrightness(false);
				}
			}
			else
			{
				return (isSunLight && CanBlockSeeTheSky(curBlockId_ws.x, curBlockId_ws.y, curBlockId_ws.z)) ? 15 : 0;
			}
		}
		return 0;
	}

	int32 CBlockLightGridClient::GetBlockOpacity(int32 x, int32 y, int32 z)
	{
		if (y >= 0 && y < BlockConfig::g_regionBlockDimY && x >= 0 && z >= 0)
		{
			BlockTemplate* pTemplate = m_pBlockWorld->GetBlockTemplate((uint16)x, (uint16)y, (uint16)z);
			return pTemplate ? pTemplate->GetLightOpacity() : 1;
		}
		return 1;
	}

	void CBlockLightGridClient::SetLightValue(uint16_t x, uint16_t y, uint16_t z, int nLightValue, bool isSunLight)
	{
		Uint16x3 neighborId(x, y, z);
		auto lightIndex = CalcLightDataIndex(neighborId);
		if (lightIndex.m_pChunk)
		{
			GetLightData(lightIndex)->SetBrightness((uint8)nLightValue, isSunLight);
		}
	}

	int32 CBlockLightGridClient::ComputeLightValue(uint16 x, uint16 y, uint16 z, bool isSunLight /*= false*/)
	{
		if (isSunLight && CanBlockSeeTheSky(x, y, z))
			return 15;
		else
		{
			BlockTemplate* pTemplate = m_pBlockWorld->GetBlockTemplate(x, y, z);
			int block_lightvalue = pTemplate ? pTemplate->GetLightValue() : 0;
			int lightvalue = isSunLight ? 0 : block_lightvalue;
			int block_lightopacity = pTemplate ? pTemplate->GetLightOpacity() : 1;

			if (block_lightopacity >= 15 && block_lightvalue > 0)
			{
				block_lightopacity = 1;
			}

			if (block_lightopacity < 1)
			{
				block_lightopacity = 1;
			}

			if (block_lightopacity >= 15)
			{
				return 0;
			}
			else if (lightvalue >= 14)
			{
				return lightvalue;
			}
			else
			{
				for (int nFaceIndex = 0; nFaceIndex < 6; ++nFaceIndex)
				{
					int32 neighborX = x + BlockFacing::offsetsXForSide[nFaceIndex];
					int32 neighborY = y + BlockFacing::offsetsYForSide[nFaceIndex];
					int32 neighborZ = z + BlockFacing::offsetsZForSide[nFaceIndex];
					int32 newLightValue = GetSavedLightValue(neighborX, neighborY, neighborZ, isSunLight) - block_lightopacity;

					if (newLightValue > lightvalue)
					{
						lightvalue = newLightValue;
					}

					if (lightvalue >= 14)
					{
						return lightvalue;
					}
				}
				return lightvalue;
			}
		}
	}

	// call this function when the block's light value is no longer valid and need to recalculated. 
	// the old light value of the current cell is used to decide which blocks needs to be recalculated. 
	bool CBlockLightGridClient::RefreshLight(const Uint16x3& blockId_ws, bool isSunLight, int32 nUpdateRange, Scoped_ReadLock<BlockReadWriteLock>* Lock_, int* pnCpuYieldCount)
	{
		// call this function regularly to yield CPU to writer thread only if they are waiting to write data. 
#define REFRESH_LIGHT_CHECK_YIELD_CPU_TO_WRITER   if(Lock_ && Lock_->mutex().HasWaitingWritersAndSingleReader()){ \
	++nYieldCPUTimes;\
	Lock_->unlock(); \
	Lock_->lock(); \
	if(!m_pBlockWorld->IsInBlockWorld())\
		return false;\
			}

		// pass 1, invalidate all dirty blocks light value to 0
		// add all blocks whose light value is equal to current source's light value and its affected area to the queue.
		int nQueuedCount = 0;
		int nYieldCPUTimes = 0;
		int lastLightValue = GetSavedLightValue(blockId_ws.x, blockId_ws.y, blockId_ws.z, isSunLight);
		int newLightValue = ComputeLightValue(blockId_ws.x, blockId_ws.y, blockId_ws.z, isSunLight);
		// we will start refresh from second one in the queue, since the first one is already valid. 
		int nStartRefreshIndex = (newLightValue == lastLightValue && nUpdateRange == 1) ? 1 : 0;

		if (newLightValue > lastLightValue)
		{
			m_blocksNeedLightRecalcuation[nQueuedCount++] = LightBlock(blockId_ws, lastLightValue);
		}
		else if (newLightValue == lastLightValue && nUpdateRange == 0)
		{
			// no need to update when light value is not changed and update range is 0. 
			REFRESH_LIGHT_CHECK_YIELD_CPU_TO_WRITER;
			return true;
		}
		else
		{
			m_blocksNeedLightRecalcuation[nQueuedCount++] = LightBlock(blockId_ws, lastLightValue);

			int nIndex = 0;
			while (nIndex < nQueuedCount)
			{
				LightBlock& current = m_blocksNeedLightRecalcuation[nIndex++];
				Uint16x3& curBlockPos = current.blockId;

				int32 lightvalue = GetSavedLightValue(curBlockPos.x, curBlockPos.y, curBlockPos.z, isSunLight);
				if (lightvalue == current.brightness)
				{
					// invalidate the light value to 0
					if (lightvalue > 0 && nIndex > nStartRefreshIndex)
						SetLightValue(curBlockPos.x, curBlockPos.y, curBlockPos.z, 0, isSunLight);

					if (lightvalue > 0 && curBlockPos.AbsDistanceTo(blockId_ws) < 17)
					{
						for (int nFaceIndex = 0; nFaceIndex < 6; ++nFaceIndex)
						{
							int32 neighborX = curBlockPos.x + BlockFacing::offsetsXForSide[nFaceIndex];
							int32 neighborY = curBlockPos.y + BlockFacing::offsetsYForSide[nFaceIndex];
							int32 neighborZ = curBlockPos.z + BlockFacing::offsetsZForSide[nFaceIndex];

							int32 blockOpacity = Math::Max((int32)1, GetBlockOpacity(neighborX, neighborY, neighborZ));
							int32 lastLightValue = GetSavedLightValue(neighborX, neighborY, neighborZ, isSunLight);

							if ((lastLightValue == (lightvalue - blockOpacity)) && !(lastLightValue == 0 && blockOpacity == 15) && nQueuedCount < (int)m_blocksNeedLightRecalcuation.size())
							{
								Uint16x3 neighborPos((uint16)neighborX, (uint16)neighborY, (uint16)neighborZ);
								if (!isSunLight || !IsLightDirty(neighborPos))
									m_blocksNeedLightRecalcuation[nQueuedCount++] = LightBlock(neighborPos, (uint8)lastLightValue);
							}
						}
					}
				}
				else
				{
					current.brightness = (int8)lightvalue;
				}
			}
			REFRESH_LIGHT_CHECK_YIELD_CPU_TO_WRITER;
		}

		//pass 2: relight all blocks in the queue generated above. 
		// recalculate all dirty blocks in pass1(m_blocksNeedLightRecalcuation), by setting each block's new light value to be the largest of its 6 neighbors
		// And if its neighbors needs update, also recalculate recursively. 

		Int32x3 minDirtyBlockId_ws(0x7FFF);
		Int32x3 maxDirtyBlockId_ws;

#ifdef PRINT_PERF_LOG
		int64 nFromTime = GetTimeUS();
#endif

		int nIndex = 0;
		while (nIndex < nQueuedCount)
		{
			LightBlock& current = m_blocksNeedLightRecalcuation[nIndex++];
			Uint16x3& curBlockPos = current.blockId;

			int32 lightvalue, newLightValue;

			bool bUpdateNeighbor = false;
			if (nIndex <= nStartRefreshIndex)
			{
				newLightValue = lightvalue = current.brightness;
				bUpdateNeighbor = true;
			}
			else
			{
				lightvalue = GetSavedLightValue(curBlockPos.x, curBlockPos.y, curBlockPos.z, isSunLight);
				newLightValue = ComputeLightValue(curBlockPos.x, curBlockPos.y, curBlockPos.z, isSunLight);
				if (newLightValue != lightvalue)
				{
					SetLightValue(curBlockPos.x, curBlockPos.y, curBlockPos.z, newLightValue, isSunLight);
					AddPointToAABB(curBlockPos, minDirtyBlockId_ws, maxDirtyBlockId_ws);
					bUpdateNeighbor = (newLightValue > lightvalue) && curBlockPos.AbsDistanceTo(blockId_ws) < 17;
				}
				else if (current.brightness != newLightValue)
				{
					// this is required for light value(invalidated to 0, but computed light is also 0) in the first pass. 
					// in such cases, the light value is changed so add to AABB to rebuild the render buffer. 
					AddPointToAABB(curBlockPos, minDirtyBlockId_ws, maxDirtyBlockId_ws);
				}
			}

			if (bUpdateNeighbor && nQueuedCount < (int)(m_blocksNeedLightRecalcuation.size() - 6))
			{
				for (int nFaceIndex = 0; nFaceIndex < 6; ++nFaceIndex)
				{
					int32 neighborX = curBlockPos.x + BlockFacing::offsetsXForSide[nFaceIndex];
					int32 neighborY = curBlockPos.y + BlockFacing::offsetsYForSide[nFaceIndex];
					int32 neighborZ = curBlockPos.z + BlockFacing::offsetsZForSide[nFaceIndex];
					int32 lastLightValue = GetSavedLightValue(neighborX, neighborY, neighborZ, isSunLight);
					if (lastLightValue < newLightValue)
					{
						Uint16x3 neighborPos((uint16)neighborX, (uint16)neighborY, (uint16)neighborZ);
						if(!isSunLight || !IsLightDirty(neighborPos))
							m_blocksNeedLightRecalcuation[nQueuedCount++] = LightBlock(neighborPos, (uint8)lastLightValue);
					}
				}
			}
			REFRESH_LIGHT_CHECK_YIELD_CPU_TO_WRITER;
		}
		SetChunksDirtyInAABB(minDirtyBlockId_ws, maxDirtyBlockId_ws);
		REFRESH_LIGHT_CHECK_YIELD_CPU_TO_WRITER;
		if (pnCpuYieldCount)
		{
			*pnCpuYieldCount += nYieldCPUTimes;
		}
#ifdef PRINT_PERF_LOG
		int64 nCurTime = GetTimeUS();
		if ((nCurTime - nFromTime) > 1000)
		{
			OUTPUT_LOG("Refresh light big duration: %d us QueueCount: %d isSunLight:%d YieldCPUCount:%d\n", (int)(nCurTime - nFromTime), nQueuedCount, isSunLight ? 1 : 0, nYieldCPUTimes);
		}
#endif
		return true;
	}

	void CBlockLightGridClient::EmitSunLight(uint16_t blockIdX_ws, uint16_t blockIdZ_ws, bool bInitialSet)
	{
		ChunkMaxHeight heightMap[6];
		m_pBlockWorld->GetMaxBlockHeightWatchingSky(blockIdX_ws, blockIdZ_ws, heightMap);

		//no block exist
		if (heightMap[5].GetMaxHeight() == 31)
		{
			/*
			// if no block exists, all light values are set to max sunlight values.
			Uint16x3 curBlockId_ws(blockIdX_ws, 0, blockIdZ_ws);
			auto curLightIdx = CalcLightDataIndex(curBlockId_ws);
			if(curLightIdx.m_pChunk != 0)
			{
			for(int y=0;y<BlockConfig::g_regionBlockDimY;y++)
			{
			curBlockId_ws.y = y;
			curLightIdx = CalcLightDataIndex(curBlockId_ws);
			if(curLightIdx.m_pChunk != 0)
			{
			GetLightData(curLightIdx)->SetBrightness(BlockConfig::g_sunLightValue,true);
			}
			}
			}
			*/
			return;
		}

		Uint16x3 curBlockId_ws(blockIdX_ws, 0, blockIdZ_ws);

		int16 max_height = 0;
		for (int i = 0; i<5; i++)
		{
			if (heightMap[i].GetMaxHeight() > max_height)
				max_height = heightMap[i].GetMaxHeight();
		}

		// update all blocks vertically from the highest visible neighboring block to the current max solid block height. 
		if (max_height > 0)
		{
			int16 min_height = heightMap[0].GetMaxSolidHeight();
			if ((heightMap[5].GetMaxHeight() & 1) == 0){
				min_height += 1;
				max_height += 1;
			}

			if (max_height >= BlockConfig::g_regionBlockDimY)
				max_height = BlockConfig::g_regionBlockDimY - 1;

			if (!bInitialSet)
			{
				for (uint16 y = min_height; y <= max_height; y++)
				{
					curBlockId_ws.y = y;
					SetLightDirty(curBlockId_ws, true, 1);
				}
			}
			else
			{
				/*
				// do we really need to add 16 to height?
				max_height += BlockConfig::g_sunLightValue;
				if (max_height >= BlockConfig::g_regionBlockDimY)
				max_height = BlockConfig::g_regionBlockDimY-1;
				else
				max_height = ((max_height >> 4) << 4) + 0xf;
				*/

				for (uint16 y = min_height; y <= max_height; y++)
				{
					curBlockId_ws.y = y;
					auto curLightIdx = CalcLightDataIndex(curBlockId_ws);
					LightData* pData = GetLightData(curLightIdx);
					if (pData)
						pData->SetBrightness(BlockConfig::g_sunLightValue, true);
				}
			}
		}
		else
		{
			// if no block exists, all light values are set to max sunlight values. 
			Uint16x3 curBlockId_ws(blockIdX_ws, 0, blockIdZ_ws);
			int nMaxChunkY = BlockConfig::g_regionBlockDimY >> 4;
			for (int y = 0; y < nMaxChunkY; y++)
			{
				curBlockId_ws.y = (y << 4);
				auto curLightIdx = CalcLightDataIndex(curBlockId_ws, false);
				if (curLightIdx.m_pChunk != 0)
				{
					GetLightData(curLightIdx)->SetBrightness(BlockConfig::g_sunLightValue, true);
					for (int i = 1; i < 16; ++i)
					{
						curBlockId_ws.y++;
						auto curLightIdx = CalcLightDataIndex(curBlockId_ws, false);
						if (curLightIdx.m_pChunk != 0)
							GetLightData(curLightIdx)->SetBrightness(BlockConfig::g_sunLightValue, true);
					}
				}
			}
		}
	}

	// obsoleted function, no pre-calculation required. 
	void CBlockLightGridClient::CheckDoQuickSunLightValues(int chunkX_ws, int chunkZ_ws)
	{
		ChunkLocation chunkPos(chunkX_ws, chunkZ_ws);
		std::unique_lock<std::recursive_mutex> Lock_(m_mutex);
		if (m_quick_loaded_columns.find(chunkPos) == m_quick_loaded_columns.end())
		{
			Lock_.unlock();
			if (m_pBlockWorld->ChunkColumnExists(chunkX_ws, chunkZ_ws))
			{
				if (chunkX_ws >= m_minChunkIdX_ws && chunkX_ws < m_maxChunkIdX_ws && chunkZ_ws >= m_minChunkIdZ_ws && chunkZ_ws < m_maxChunkIdZ_ws)
				{
					Lock_.lock();
					m_quick_loaded_columns.insert(chunkPos);
					Lock_.unlock();
					DoQuickSunLightValues(chunkX_ws, chunkZ_ws);
				}
			}
		}
	}

	void CBlockLightGridClient::DoQuickSunLightValues(int chunkX_ws, int chunkZ_ws)
	{
		uint16_t chunkBlockX = chunkX_ws * BlockConfig::g_chunkBlockDim;
		uint16_t chunkBlockZ = chunkZ_ws * BlockConfig::g_chunkBlockDim;
		for (int x = 0; x < BlockConfig::g_chunkBlockDim; x++)
		{
			for (int z = 0; z < BlockConfig::g_chunkBlockDim; z++)
			{
				uint16_t blockIdX_ws = chunkBlockX + x;
				uint16_t blockIdZ_ws = chunkBlockZ + z;
				Uint16x3 curBlockId_ws(blockIdX_ws, 0, blockIdZ_ws);

				EmitSunLight(blockIdX_ws, blockIdZ_ws, true);
			}
		}
	}

	void CBlockLightGridClient::AddDirtyColumn(uint16_t chunkX_ws, uint16_t chunkZ_ws)
	{
		ChunkLocation chunkPos(chunkX_ws, chunkZ_ws);
		std::unique_lock<std::recursive_mutex> Lock_(m_mutex);
		if (m_dirtyColumns.find(chunkPos) == m_dirtyColumns.end())
		{
			m_dirtyColumns.insert(chunkPos);
			Lock_.unlock();
		}
	}

	void CBlockLightGridClient::RemoveDirtyColumn(const ChunkLocation& curChunkId_ws)
	{
		std::unique_lock<std::recursive_mutex> DirtyColumnLock_(m_mutex);
		m_dirtyColumns.erase(curChunkId_ws);
	}

	int CBlockLightGridClient::GetDirtyColumnCount()
	{
		std::unique_lock<std::recursive_mutex> Lock_(m_mutex);
		return (int)(m_dirtyColumns.size());
	}

	void CBlockLightGridClient::SetColumnPreloaded(uint16_t chunkX_ws, uint16_t chunkZ_ws)
	{
		if (!IsChunkColumnLoaded(chunkX_ws, chunkZ_ws))
		{
			std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
			m_loaded_columns.insert((chunkX_ws << 16) + chunkZ_ws);
		}
	}

	void CBlockLightGridClient::SetColumnUnloaded(uint16_t chunkX_ws, uint16_t chunkZ_ws)
	{
		std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
		{
			auto iter = m_loaded_columns.find((chunkX_ws << 16) + chunkZ_ws);
			if (iter != m_loaded_columns.end())
			{
				m_loaded_columns.erase(iter);
			}
		}
		ChunkLocation chunkPos(chunkX_ws, chunkZ_ws);
		{
			auto iter = m_quick_loaded_columns.find(chunkPos);
			if (iter != m_quick_loaded_columns.end())
			{
				m_quick_loaded_columns.erase(iter);
			}
		}
		{
			auto iter = m_dirtyColumns.find(chunkPos);
			if (iter != m_dirtyColumns.end())
			{
				m_dirtyColumns.erase(iter);
			}
		}
	}

	void CBlockLightGridClient::SetLightingInChunkColumnInitialized(uint16_t chunkX_ws, uint16_t chunkZ_ws)
	{
		for (int y = 0; y < BlockConfig::g_regionChunkDimY; y++)
		{
			BlockChunk* pChunk = m_pBlockWorld->GetChunk(chunkX_ws * 16, y * 16, chunkZ_ws * 16, false);
			if (pChunk)
				pChunk->SetLightingInitialized(true);
		}
	}

	bool CBlockLightGridClient::IsChunkColumnLoadedWorldPos(int nWorldX, int nWorldY, int nWorldZ)
	{
		std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
		return m_loaded_columns.find(((nWorldX >> 4) << 16) + (nWorldZ >> 4)) != m_loaded_columns.end();
	}

	bool CBlockLightGridClient::IsChunkColumnLoaded(int nChunkX, int nChunkZ)
	{
		std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
		return m_loaded_columns.find((nChunkX << 16) + nChunkZ) != m_loaded_columns.end();
	}

	

	bool CBlockLightGridClient::IsAsyncLightCalculation() const
	{
		return m_bIsAsyncLightCalculation;
	}

	void CBlockLightGridClient::SetAsyncLightCalculation(bool val)
	{
		m_bIsAsyncLightCalculation = val;
	}

	void CBlockLightGridClient::SetLightGridSize(int nSize)
	{
		std::lock_guard<std::recursive_mutex> Lock_(m_mutex);
		if (GetLightGridSize() != nSize)
		{
			CBlockLightGridBase::SetLightGridSize(nSize);

			m_minChunkIdX_ws = -1000;
			m_minChunkIdZ_ws = -1000;
			m_maxChunkIdX_ws = -1;
			m_maxChunkIdZ_ws = -1;
			m_minLightBlockIdX = -1000;
			m_minLightBlockIdZ = -1000;
			m_maxLightBlockIdX = -1;
			m_maxLightBlockIdZ = -1;
			if (m_centerChunkIdX_ws > 0 && m_centerChunkIdZ_ws > 0)
			{
				OnWorldMove(m_centerChunkIdX_ws, m_centerChunkIdZ_ws);
			}
		}
	}

	int CBlockLightGridClient::GetDirtyBlockCount()
	{
		return m_nDirtyBlocksCount;
	}

	void CBlockLightGridClient::SetChunksDirtyInAABB(Int32x3 & minDirtyBlockId_ws, Int32x3 & maxDirtyBlockId_ws)
	{
		if (minDirtyBlockId_ws.x > maxDirtyBlockId_ws.x)
			return;
		//extend 1 block in case block happen at the boundary of two chunks
		minDirtyBlockId_ws.x -= 1;
		minDirtyBlockId_ws.y -= 1;
		minDirtyBlockId_ws.z -= 1;
		maxDirtyBlockId_ws.x += 1;
		maxDirtyBlockId_ws.y += 1;
		maxDirtyBlockId_ws.z += 1;

		if (minDirtyBlockId_ws.x < 0)
			minDirtyBlockId_ws.x = 0;
		if (minDirtyBlockId_ws.z < 0)
			minDirtyBlockId_ws.z = 0;
		if (minDirtyBlockId_ws.y < 0)
			minDirtyBlockId_ws.y = 0;
		if (minDirtyBlockId_ws.y >= BlockConfig::g_regionBlockDimY)
			minDirtyBlockId_ws.y = BlockConfig::g_regionBlockDimY - 1;
		if (maxDirtyBlockId_ws.x >= 0xffff)
			maxDirtyBlockId_ws.x = 0xffff - 1;
		if (maxDirtyBlockId_ws.z >= 0xffff)
			maxDirtyBlockId_ws.z = 0xffff - 1;
		if (maxDirtyBlockId_ws.y < 0)
			maxDirtyBlockId_ws.y = 0;
		if (maxDirtyBlockId_ws.y >= BlockConfig::g_regionBlockDimY)
			maxDirtyBlockId_ws.y = BlockConfig::g_regionBlockDimY - 1;

		Uint16x3 startDirtyChunk_ws;
		startDirtyChunk_ws.x = (uint16)(minDirtyBlockId_ws.x >> 4);
		startDirtyChunk_ws.y = (uint16)(minDirtyBlockId_ws.y >> 4);
		startDirtyChunk_ws.z = (uint16)(minDirtyBlockId_ws.z >> 4);

		Uint16x3 endDirtyChunk_ws;
		endDirtyChunk_ws.x = (uint16)(maxDirtyBlockId_ws.x >> 4);
		endDirtyChunk_ws.y = (uint16)(maxDirtyBlockId_ws.y >> 4);
		endDirtyChunk_ws.z = (uint16)(maxDirtyBlockId_ws.z >> 4);

		Uint16x3 curChunk_ws;
		for (uint32_t x = startDirtyChunk_ws.x; x <= endDirtyChunk_ws.x; x++)
		{
			for (uint32_t y = startDirtyChunk_ws.y; y <= endDirtyChunk_ws.y; y++)
			{
				for (uint32_t z = startDirtyChunk_ws.z; z <= endDirtyChunk_ws.z; z++)
				{
					Uint16x3 curChunk_ws(x, y, z);
					m_pBlockWorld->SetChunkLightDirty(curChunk_ws);
				}
			}
		}
	}

	void CBlockLightGridClient::AddPointToAABB(const Uint16x3 &curBlockPos, Int32x3 &minDirtyBlockId_ws, Int32x3 &maxDirtyBlockId_ws)
	{
		if (curBlockPos.x > maxDirtyBlockId_ws.x)
			maxDirtyBlockId_ws.x = curBlockPos.x;
		if (curBlockPos.x < minDirtyBlockId_ws.x)
			minDirtyBlockId_ws.x = curBlockPos.x;
		if (curBlockPos.y > maxDirtyBlockId_ws.y)
			maxDirtyBlockId_ws.y = curBlockPos.y;
		if (curBlockPos.y < minDirtyBlockId_ws.y)
			minDirtyBlockId_ws.y = curBlockPos.y;
		if (curBlockPos.z > maxDirtyBlockId_ws.z)
			maxDirtyBlockId_ws.z = curBlockPos.z;
		if (curBlockPos.z < minDirtyBlockId_ws.z)
			minDirtyBlockId_ws.z = curBlockPos.z;
	}

}

//-----------------------------------------------------------------------------
// Class:	All kinds of block tessellation 
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2014.12.22
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BlockModel.h"
#include "BlockCommon.h"
#include "VertexFVF.h"
#include "BlockChunk.h"
#include "BlockRegion.h"
#include "BlockWorld.h"
#include "VertexFVF.h"
#include "BlockTessellators.h"

using namespace ParaEngine;

ParaEngine::BlockTessellatorBase::BlockTessellatorBase(CBlockWorld* pWorld)
	: m_pWorld(pWorld), m_pCurBlockTemplate(0), m_pCurBlockModel(0), m_blockId_ws(0, 0, 0), m_nBlockData(0), m_pChunk(0), m_blockId_cs(0, 0, 0)
{
	memset(neighborBlocks, 0, sizeof(neighborBlocks));
}

void ParaEngine::BlockTessellatorBase::SetWorld(CBlockWorld* pWorld)
{
	if (m_pWorld != pWorld)
	{
		m_pWorld = pWorld;
	}
}

int32 ParaEngine::BlockTessellatorBase::TessellateBlock(BlockChunk* pChunk, uint16 packedBlockId, BlockRenderMethod dwShaderID, BlockVertexCompressed** pOutputData)
{
	return 0;
}

int32_t ParaEngine::BlockTessellatorBase::GetMaxVertexLight(int32_t v1, int32_t v2, int32_t v3, int32_t v4)
{
	int32_t max1 = Math::Max(v1, v2);
	int32_t max2 = Math::Max(v3, v4);
	return Math::Max(max1, max2);
}

uint8 ParaEngine::BlockTessellatorBase::GetMeshBrightness(BlockTemplate * pBlockTemplate, uint8* blockBrightness)
{
	uint8 centerLightness = blockBrightness[rbp_center];
	if (centerLightness > 0 && pBlockTemplate->GetLightOpacity() > 1)
		return Math::Min(centerLightness + pBlockTemplate->GetLightOpacity(), 15);
	else
		return Math::Max(Math::Max(Math::Max(Math::Max(Math::Max(Math::Max(centerLightness, blockBrightness[rbp_nX]), blockBrightness[rbp_pX]), blockBrightness[rbp_nZ]), blockBrightness[rbp_pZ]), blockBrightness[rbp_pY]), blockBrightness[rbp_nY]);
}

int32_t ParaEngine::BlockTessellatorBase::GetAvgVertexLight(int32_t v1, int32_t v2, int32_t v3, int32_t v4)
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


bool ParaEngine::BlockTessellatorBase::UpdateCurrentBlock(BlockChunk* pChunk, uint16 packedBlockId)
{
	Block* pCurBlock = pChunk->GetBlock(packedBlockId);
	if (pCurBlock)
	{
		m_pCurBlockTemplate = pCurBlock->GetTemplate();
		if (m_pCurBlockTemplate)
		{
			m_pChunk = pChunk;
			UnpackBlockIndex(packedBlockId, m_blockId_cs.x, m_blockId_cs.y, m_blockId_cs.z);
			m_blockId_ws.x = pChunk->m_minBlockId_ws.x + m_blockId_cs.x;
			m_blockId_ws.y = pChunk->m_minBlockId_ws.y + m_blockId_cs.y;
			m_blockId_ws.z = pChunk->m_minBlockId_ws.z + m_blockId_cs.z;

			neighborBlocks[rbp_center] = pCurBlock;
			m_nBlockData = pCurBlock->GetUserData();
			m_pCurBlockModel = &(m_pCurBlockTemplate->GetBlockModel(m_pWorld, m_blockId_ws.x, m_blockId_ws.y, m_blockId_ws.z, (uint16)m_nBlockData, neighborBlocks));
			tessellatedModel.ClearVertices();
			return true;
		}
	}
	return false;
}

void ParaEngine::BlockTessellatorBase::FetchNearbyBlockInfo(BlockChunk* pChunk, const Uint16x3& blockId_cs, int nNearbyBlockCount, int nNearbyLightCount)
{
	//neighbor block info: excluding the first (center) block, since it has already been fetched. 
	if (nNearbyBlockCount > 1)
	{
		memset(neighborBlocks + 1, 0, sizeof(Block*) * (nNearbyBlockCount - 1));
		pChunk->QueryNeighborBlockData(blockId_cs, neighborBlocks + 1, 1, nNearbyBlockCount - 1);
	}
	//neighbor light info
	if (!m_pCurBlockModel->IsUsingSelfLighting())
	{
		nNearbyLightCount = nNearbyLightCount < 0 ? nNearbyBlockCount : nNearbyLightCount;
		memset(blockBrightness, 0, sizeof(uint8_t) * nNearbyLightCount * 3);
		m_pWorld->GetBlockBrightness(m_blockId_ws, blockBrightness, nNearbyLightCount, 3);
	}
}

uint32_t ParaEngine::BlockTessellatorBase::CalculateCubeAO()
{
	uint32_t aoFlags = 0;

	if (m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_invisible))
		return aoFlags;

	Block* pCurBlock = neighborBlocks[rbp_pXpYpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_xyz;
	}

	pCurBlock = neighborBlocks[rbp_nXpYpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_Nxyz;
	}

	pCurBlock = neighborBlocks[rbp_pXpYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_xyNz;
	}

	pCurBlock = neighborBlocks[rbp_nXpYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_NxyNz;
	}

	pCurBlock = neighborBlocks[rbp_pYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_topFront;
	}

	pCurBlock = neighborBlocks[rbp_nXpY];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_topLeft;
	}

	pCurBlock = neighborBlocks[rbp_pXpY];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_topRight;
	}

	pCurBlock = neighborBlocks[rbp_pYpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_topBack;
	}

	pCurBlock = neighborBlocks[rbp_nXnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_LeftFront;
	}

	pCurBlock = neighborBlocks[rbp_nXpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_leftBack;
	}

	pCurBlock = neighborBlocks[rbp_pXnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_rightFont;
	}

	pCurBlock = neighborBlocks[rbp_pXpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_rightBack;
	}

	pCurBlock = neighborBlocks[rbp_pXnYPz];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_xNyz;
	}

	pCurBlock = neighborBlocks[rbp_pXnYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_xNyNz;
	}

	pCurBlock = neighborBlocks[rbp_nXnYPz];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_NxNyz;
	}

	pCurBlock = neighborBlocks[rbp_nXnYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_NxNyNz;
	}

	pCurBlock = neighborBlocks[rbp_nYnZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_bottomFront;
	}

	pCurBlock = neighborBlocks[rbp_nXnY];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_bottomLeft;
	}

	pCurBlock = neighborBlocks[rbp_pXnY];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_bottomRight;
	}

	pCurBlock = neighborBlocks[rbp_nYpZ];
	if (pCurBlock)
	{
		if (pCurBlock->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
			aoFlags |= BlockModel::evf_bottomBack;
	}
	return aoFlags;
}

//////////////////////////////////////////////////////////
//
// BlockGeneralTessellator
//
//////////////////////////////////////////////////////////

ParaEngine::BlockGeneralTessellator::BlockGeneralTessellator(CBlockWorld* pWorld) : BlockTessellatorBase(pWorld)
{
}

int32 ParaEngine::BlockGeneralTessellator::TessellateBlock(BlockChunk* pChunk, uint16 packedBlockId, BlockRenderMethod dwShaderID, BlockVertexCompressed** pOutputData)
{
	if (!UpdateCurrentBlock(pChunk, packedBlockId))
		return 0;

	if (m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_liquid))
	{
		// water, ice or other transparent cube blocks
		// adjacent faces of the same liquid type will be removed. 
		TessellateLiquidOrIce(dwShaderID);
	}
	else
	{
		if (m_pCurBlockModel->IsUsingSelfLighting())
		{
			// like wires, etc. 
			TessellateSelfLightingCustomModel(dwShaderID);
		}
		else if (m_pCurBlockModel->IsUniformLighting())
		{
			// custom models like stairs, slabs, button, torch light, grass, etc. 
			TessellateUniformLightingCustomModel(dwShaderID);
		}
		else
		{
			// standard cube including tree leaves. 
			TessellateStdCube(dwShaderID);
		}
	}
	int nFaceCount = tessellatedModel.GetFaceCount();
	if (nFaceCount > 0)
	{
		tessellatedModel.TranslateVertices(m_blockId_cs.x, m_blockId_cs.y, m_blockId_cs.z);
		*pOutputData = tessellatedModel.GetVertices();
	}
	return nFaceCount;
}


void ParaEngine::BlockGeneralTessellator::TessellateUniformLightingCustomModel(BlockRenderMethod dwShaderID)
{
	int nFetchNearybyCount = 7; //  m_pCurBlockTemplate->IsTransparent() ? 7 : 1;
	FetchNearbyBlockInfo(m_pChunk, m_blockId_cs, nFetchNearybyCount);

	tessellatedModel.CloneVertices(m_pCurBlockTemplate->GetBlockModel(m_pWorld, m_blockId_ws.x, m_blockId_ws.y, m_blockId_ws.z, (uint16)m_nBlockData, neighborBlocks));

	const uint16_t nFaceCount = m_pCurBlockModel->GetFaceCount();

	// custom model does not use AO and does not remove any invisible faces. 
	int32_t max_light = 0;
	int32_t max_sun_light = 0;
	int32_t max_block_light = 0;

	DWORD dwBlockColor = m_pCurBlockTemplate->GetDiffuseColor(m_nBlockData);
	const bool bHasColorData = dwBlockColor != Color::White;

	if (dwShaderID == BLOCK_RENDER_FIXED_FUNCTION)
	{
		max_light = GetMeshBrightness(m_pCurBlockTemplate, &(blockBrightness[rbp_center]));

		// not render completely dark
		max_light = Math::Max(max_light, 2);
		float fLightValue = m_pWorld->GetLightBrightnessLinearFloat(max_light);

		for (int face = 0; face < nFaceCount; ++face)
		{
			int nFirstVertex = face * 4;
			for (int v = 0; v < 4; ++v)
			{
				int nIndex = nFirstVertex + v;
				tessellatedModel.SetLightIntensity(nIndex, fLightValue);

				if (bHasColorData)
				{
					tessellatedModel.SetVertexColor(nIndex, dwBlockColor);
				}
			}
		}
	}
	else
	{
		max_sun_light = GetMeshBrightness(m_pCurBlockTemplate, &(blockBrightness[rbp_center + nFetchNearybyCount * 2]));
		max_block_light = GetMeshBrightness(m_pCurBlockTemplate, &(blockBrightness[rbp_center + nFetchNearybyCount]));

		uint8 block_lightvalue = m_pWorld->GetLightBrightnessInt(max_block_light);
		uint8 sun_lightvalue = max_sun_light << 4;
		for (int face = 0; face < nFaceCount; ++face)
		{
			int nFirstVertex = face * 4;
			for (int v = 0; v < 4; ++v)
			{
				int nIndex = nFirstVertex + v;
				tessellatedModel.SetVertexLight(nIndex, block_lightvalue, sun_lightvalue);
				if (bHasColorData)
				{
					tessellatedModel.SetVertexColor(nIndex, dwBlockColor);
				}
			}
		}
	}
}

void ParaEngine::BlockGeneralTessellator::TessellateSelfLightingCustomModel(BlockRenderMethod dwShaderID)
{
	FetchNearbyBlockInfo(m_pChunk, m_blockId_cs, 19, 0);
	tessellatedModel.CloneVertices(m_pCurBlockTemplate->GetBlockModel(m_pWorld, m_blockId_ws.x, m_blockId_ws.y, m_blockId_ws.z, (uint16)m_nBlockData, neighborBlocks));

	DWORD dwBlockColor = m_pCurBlockTemplate->GetDiffuseColor(m_nBlockData);
	const bool bHasColorData = dwBlockColor != Color::White;

	if (m_pCurBlockModel->IsUseAmbientOcclusion())
	{
		uint32 aoFlags = CalculateCubeAO();
		const uint16_t nFaceCount = tessellatedModel.GetFaceCount();
		for (int face = 0; face < nFaceCount; ++face)
		{
			int nIndex = face * 4;
			tessellatedModel.SetVertexShadowFromAOFlags(nIndex, nIndex, aoFlags);
			if (bHasColorData)
			{
				tessellatedModel.SetVertexColor(nIndex, dwBlockColor);
			}
		}
	}
}

int32 VertexVerticalScaleMaskMap[] = {
	3, // evf_NxyNz, //g_topLB 
	1, // evf_Nxyz, //g_topLT 
	0, // evf_xyz, //g_topRT 
	2, // evf_xyNz, //g_topRB 
	-1, //g_frtLB 
	3, // evf_NxyNz, //g_frtLT 
	2, // evf_xyNz, //g_frtRT 
	-1, //g_frtRB 
	-1, //g_btmLB 
	-1, //g_btmLT 
	-1, //g_btmRT 
	-1, //g_btmRB 
	-1, // g_leftLB 
	1, // evf_Nxyz, // g_leftLT 
	3, // evf_NxyNz, // g_leftRT 
	-1, // g_leftRB 
	-1, // g_rightLB
	2, // evf_xyNz, // g_rightLT
	0, // evf_xyz, // g_rightRT
	-1, // g_rightRB
	-1, // g_bkLB 
	0, // evf_xyz, // g_bkLT 
	1, // evf_Nxyz, // g_bkRT 
	-1, // g_bkRB 
};

void ParaEngine::BlockGeneralTessellator::TessellateLiquidOrIce(BlockRenderMethod dwShaderID)
{
	FetchNearbyBlockInfo(m_pChunk, m_blockId_cs, 27);

	uint32 aoFlags = 0;
	if (m_pCurBlockModel->IsUseAmbientOcclusion())
	{
		aoFlags = CalculateCubeAO();
	}

	const uint16_t nFaceCount = m_pCurBlockModel->GetFaceCount();
	PE_ASSERT(nFaceCount <= 6);

	bool bHasTopScale = false;
	float TopFaceVerticalScales[] = { 1.f, 1.f, 1.f, 1.f };

	DWORD dwBlockColor = m_pCurBlockTemplate->GetDiffuseColor(m_nBlockData);
	const bool bHasColorData = dwBlockColor != Color::White;

	//----------calc vertex lighting----------------
	for (int face = 0; face < nFaceCount; ++face)
	{
		int nFirstVertex = face * 4;

		Block* pCurBlock = neighborBlocks[BlockCommon::RBP_SixNeighbors[face]];

		if (!(pCurBlock &&
			((pCurBlock->GetTemplate()->IsAssociatedBlockID(m_pCurBlockTemplate->GetID())
				// TODO: we should show the face when two transparent color blocks with different color are side by side.
				// However, since we are not doing face sorting anyway, this feature is turned off at the moment. 
				// && pCurBlock->GetTemplate()->GetDiffuseColor(pCurBlock->GetUserData()) == dwBlockColor
				)
				|| (face != 0 && pCurBlock->GetTemplate()->IsFullyOpaque()))))
		{
			int32_t baseIdx = nFirstVertex * 4;
			int32_t v1 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx]];
			int32_t max_light = Math::Max(v1, 2);
			bool bHideFace = false;


			if (face == 0 && !m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_solid))
			{

				// check top face, just in case we need to scale edge water block according to gravity. 
				for (int v = 0; v < 4; ++v)
				{
					int i = nFirstVertex + v;
					int32_t baseIdx = i * 4;

					// if both of the two adjacent blocks to the edge vertex are empty, we will scale that edge vertex to 0 height.  
					Block* b2;
					Block* b3;
					if (v == 0) {
						b2 = neighborBlocks[rbp_nX];
						b3 = neighborBlocks[rbp_nZ];
						if (!((b2 && b2->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid)) ||
							(b3 && b3->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid))))
						{
							// BlockModel::evf_NxyNz
							TopFaceVerticalScales[3] = 0.4f;
							bHasTopScale = true;
						}
						else
						{
							if (!((neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]]->GetTemplate() == m_pCurBlockTemplate)))
							{
								// BlockModel::evf_NxyNz
								TopFaceVerticalScales[3] = 0.8f; // surface block is always a little lower
								bHasTopScale = true;
							}
						}
					}
					else if (v == 1) {
						b2 = neighborBlocks[rbp_nX];
						b3 = neighborBlocks[rbp_pZ];
						if (!((b2 && b2->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid)) ||
							(b3 && b3->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid))))
						{
							// BlockModel::evf_Nxyz
							TopFaceVerticalScales[1] = 0.4f;
							bHasTopScale = true;
						}
						else
						{
							if (!((neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]]->GetTemplate() == m_pCurBlockTemplate)))
							{
								// BlockModel::evf_Nxyz
								TopFaceVerticalScales[1] = 0.8f;
								bHasTopScale = true;
							}
						}
					}
					else if (v == 2) {
						b2 = neighborBlocks[rbp_pX];
						b3 = neighborBlocks[rbp_pZ];
						if (!((b2 && b2->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid)) ||
							(b3 && b3->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid))))
						{
							// BlockModel::evf_xyz
							TopFaceVerticalScales[0] = 0.4f;
							bHasTopScale = true;
						}
						else
						{
							if (!((neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]]->GetTemplate() == m_pCurBlockTemplate)))
							{
								// BlockModel::evf_xyz
								TopFaceVerticalScales[0] = 0.8f;
								bHasTopScale = true;
							}
						}
					}
					else if (v == 3) {
						b2 = neighborBlocks[rbp_pX];
						b3 = neighborBlocks[rbp_nZ];
						if (!((b2 && b2->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid)) ||
							(b3 && b3->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid | BlockTemplate::batt_obstruction | BlockTemplate::batt_liquid))))
						{
							// BlockModel::evf_xyNz
							TopFaceVerticalScales[2] = 0.4f;
							bHasTopScale = true;
						}
						else
						{
							if (!((neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 1]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 2]]->GetTemplate() == m_pCurBlockTemplate) ||
								(neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]] && neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx + 3]]->GetTemplate() == m_pCurBlockTemplate)))
							{
								// BlockModel::evf_xyNz
								TopFaceVerticalScales[2] = 0.8f;
								bHasTopScale = true;
							}
						}
					}
				}

				if (!bHasTopScale && (pCurBlock && pCurBlock->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_solid)))
				{
					bHideFace = true;
				}
			}

			if (!bHideFace)
			{
				for (int v = 0; v < 4; ++v)
				{
					int i = nFirstVertex + v;

					int nIndex = tessellatedModel.AddVertex(*m_pCurBlockModel, i);
					if (bHasTopScale && VertexVerticalScaleMaskMap[i] >= 0)
					{
						float fScale = TopFaceVerticalScales[VertexVerticalScaleMaskMap[i]];
						if (fScale != 1.f)
						{
							tessellatedModel.SetVertexHeightScale(nIndex, fScale);
						}
					}

					if (dwShaderID == BLOCK_RENDER_FIXED_FUNCTION)
					{
						tessellatedModel.SetLightIntensity(nIndex, m_pWorld->GetLightBrightnessLinearFloat(max_light));
					}
					else
					{
						if (m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_solid))
							tessellatedModel.SetVertexLight(nIndex, m_pWorld->GetLightBrightnessInt(blockBrightness[BlockCommon::NeighborLightOrder[baseIdx] + 27]), blockBrightness[BlockCommon::NeighborLightOrder[baseIdx] + 27 * 2] << 4);
						else
							tessellatedModel.SetVertexLight(nIndex, m_pWorld->GetLightBrightnessInt(blockBrightness[27]), blockBrightness[27 * 2] << 4);
					}

					tessellatedModel.SetVertexShadowFromAOFlags(nIndex, i, aoFlags);
					if (bHasColorData)
					{
						tessellatedModel.SetVertexColor(nIndex, dwBlockColor);
					}
				}
				tessellatedModel.IncrementFaceCount(1);
			}
		}
	}
}

void ParaEngine::BlockGeneralTessellator::TessellateStdCube(BlockRenderMethod dwShaderID)
{
	FetchNearbyBlockInfo(m_pChunk, m_blockId_cs, 27);

	uint32 aoFlags = 0;
	if (m_pCurBlockModel->IsUseAmbientOcclusion())
	{
		aoFlags = CalculateCubeAO();
	}

	const uint16_t nFaceCount = m_pCurBlockModel->GetFaceCount();
	PE_ASSERT(nFaceCount <= 6);

	DWORD dwBlockColor = m_pCurBlockTemplate->GetDiffuseColor(m_nBlockData);
	const bool bHasColorData = dwBlockColor != Color::White;

	int tileSize = m_pCurBlockTemplate->getTileSize();
	float uvScale = (tileSize == 1) ? 1.0f : (1.0f / tileSize);

	for (int face = 0; face < nFaceCount; ++face)
	{
		int nFirstVertex = face * 4;

		Block* pCurBlock = neighborBlocks[BlockCommon::RBP_SixNeighbors[face]];

		if (!pCurBlock || (pCurBlock->GetTemplate()->GetLightOpacity() < 15))
		{
			for (int v = 0; v < 4; ++v)
			{
				int i = nFirstVertex + v;
				int32_t baseIdx = i * 4;

				int32_t max_light = 0;
				int32_t max_sun_light = 0;
				int32_t max_block_light = 0;

				if (dwShaderID == BLOCK_RENDER_FIXED_FUNCTION)
				{
					int32_t v1 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx]];
					int32_t v2 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 1]];
					int32_t v3 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 2]];
					int32_t v4 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 3]];
					max_light = GetAvgVertexLight(v1, v2, v3, v4);
				}
				else
				{
					int32_t v1 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx] + 27];
					int32_t v2 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 1] + 27];
					int32_t v3 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 2] + 27];
					int32_t v4 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 3] + 27];
					max_block_light = GetAvgVertexLight(v1, v2, v3, v4);

					v1 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx] + 27 * 2];
					v2 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 1] + 27 * 2];
					v3 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 2] + 27 * 2];
					v4 = blockBrightness[BlockCommon::NeighborLightOrder[baseIdx + 3] + 27 * 2];

					max_sun_light = GetAvgVertexLight(v1, v2, v3, v4);
				}

				Block* pCurBlock1 = neighborBlocks[BlockCommon::NeighborLightOrder[baseIdx]];
				if (pCurBlock1 && pCurBlock1->GetTemplate()->IsMatchAttributes(BlockTemplate::batt_solid | BlockTemplate::batt_invisible, BlockTemplate::batt_solid))
				{
					// simulate ao but not render completely dark. 
					max_light -= 3;
					max_sun_light -= 3;
					max_block_light -= 3;
				}

				int nIndex = tessellatedModel.AddVertex(*m_pCurBlockModel, i);
				if (dwShaderID == BLOCK_RENDER_FIXED_FUNCTION)
				{
					max_light = Math::Max(max_light, 2);
					tessellatedModel.SetLightIntensity(nIndex, m_pWorld->GetLightBrightnessLinearFloat(max_light));
				}
				else
				{
					max_sun_light = Math::Max(max_sun_light, 0);
					max_block_light = Math::Max(max_block_light, 0);
					tessellatedModel.SetVertexLight(nIndex, m_pWorld->GetLightBrightnessInt(max_block_light), max_sun_light << 4);
				}

				tessellatedModel.SetVertexShadowFromAOFlags(nIndex, i, aoFlags);
				if (bHasColorData)
				{
					tessellatedModel.SetVertexColor(nIndex, dwBlockColor);
				}

				if (m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_pos_tiling) || m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_random_tiling))
				{
					BlockVertexCompressed* vert = tessellatedModel.GetVertices() + nIndex;
					Vector2 tran;
					if (m_pCurBlockTemplate->IsMatchAttribute(BlockTemplate::batt_pos_tiling))
						tran = Vector2((float)(m_blockId_cs.x % tileSize), (float)(m_blockId_cs.z % tileSize));
					else
						tran = Vector2((float)(m_nBlockData % tileSize), (float)(m_nBlockData / tileSize));
					float u, v;
					vert->GetTexcoord(u, v);
					vert->SetTexcoord((tran.x + u) * uvScale, (tran.y + v) * uvScale);
				}
			}
			tessellatedModel.IncrementFaceCount(1);
		}
	}
}

//-----------------------------------------------------------------------------
// Class: BlockTemplate
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Date:	2012.12
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "BlockTemplate.h"
#include "ParaWorldAsset.h"
#include "BlockModelProvider.h"
#include "WireModelProvider.h"
#include "CarpetModelProvider.h"
#include "SlopeModelProvider.h"
#include "BlockWorld.h"
#include "SceneObject.h"
#include "util/regularexpression.h"
#include "StringHelper.h"

namespace ParaEngine
{
	const uint16_t BlockTemplate::g_maxRenderPriority = 0xf;

	BlockTemplate::BlockTemplate( uint16_t id,uint32_t attFlag, uint16_t category_id) :m_id(id),m_attFlag(attFlag), m_category_id(category_id), m_fPhysicalHeight(1.f), m_nTileSize(1),
		m_pNormalMap(nullptr), m_renderPriority(0), m_lightScatterStep(1), m_lightOpacity(1), m_pBlockModelFilter(NULL), m_bIsShadowCaster(true), m_associated_blockid(0), 
		m_bProvidePower(false), m_nLightValue(0xf), m_fSpeedReductionPercent(1.f), m_renderPass(BlockRenderPass_Opaque), m_dwMapColor(Color::White), m_UnderWaterColor(0)
	{
		Init(attFlag, category_id);
	}

	BlockTemplate::~BlockTemplate()
	{
		SAFE_DELETE(m_pBlockModelFilter);
	}

	void BlockTemplate::Init(uint32_t attFlag, uint16_t category_id)
	{
		m_attFlag = attFlag;
		m_category_id = category_id;

		// init default parameters
		m_fPhysicalHeight = 1.f;
		m_renderPriority = 0;
		m_lightScatterStep = 1;
		m_lightOpacity = 1;
		m_associated_blockid = 0;
		m_bProvidePower = false;
		m_nLightValue = 0xf;
		m_fSpeedReductionPercent = 1.f;
		m_renderPass = BlockRenderPass_Opaque;

		m_textures0.resize(1, NULL);
		m_textures1.resize(1, NULL);

		// render priority: opaque object, alpha tested object, and then alpha blended object. 
		if (IsAlphaBlendedTexture() && !IsAlphaTestTexture())
			SetRenderPass(BlockRenderPass_AlphaBlended);
		else if (IsAlphaTestTexture())
			SetRenderPass(BlockRenderPass_AlphaTest);
		else
			SetRenderPass(BlockRenderPass_Opaque);

		if (IsMatchAttribute(batt_transparent))
		{
			if (GetRenderPass() == BlockRenderPass_AlphaBlended)
			{
				if (IsMatchAttribute(batt_liquid) && !IsMatchAttribute(batt_solid))
				{
					// liquid water has higher priority to render first among all alpha blending pass.
					m_renderPriority += 1;
					SetRenderPass(BlockRenderPass_ReflectedWater);
				}
			}
			else
			{
				// making liquid with lowest render priority so that it is rendered last, and more opaque objects have higher priority. 
				if (IsMatchAttribute(batt_liquid))
				{
					if (!IsMatchAttribute(batt_solid))
					{
						m_renderPriority += 1;
						// light in water scattered more than in air. 
						SetLightOpacity(2);
						// disable shadow for water
						m_bIsShadowCaster = false;
						SetRenderPass(BlockRenderPass_ReflectedWater);
					}
					else
					{
						// ice (solid liquid) is rendered after water. 
						// ice scatters light. 
						SetLightOpacity(2);
					}
				}
				else
				{
					m_renderPriority += 2;

					if (IsMatchAttribute(batt_solid))
					{
						m_renderPriority++;
					}
					if (IsMatchAttribute(batt_obstruction))
						m_renderPriority++;
					if (IsMatchAttribute(batt_customModel) && !IsMatchAttribute(batt_cubeModel))
						m_renderPriority++;
				}
			}
		}
		else
		{
			if (IsMatchAttribute(batt_solid))
				SetLightOpacity(15);
		}

		int32_t uvPattern = 0;

		m_nLightValue = IsMatchAttribute(batt_light) ? 0xf : 0;

		if (IsMatchAttribute(BlockTemplate::batt_threeSideTex))
			uvPattern = 3;
		else if (IsMatchAttribute(BlockTemplate::batt_fourSideTex))
			uvPattern = 4;
		else if (IsMatchAttribute(BlockTemplate::batt_sixSideTex))
			uvPattern = 6;

		if (IsMatchAttribute(BlockTemplate::batt_obstruction))
		{
			if (IsMatchAttribute(BlockTemplate::batt_climbable))
				SetPhysicalHeight(0.f);
			else
			{
				SetPhysicalHeight(1.f);
			}
		}
		else
		{
			SetPhysicalHeight(-1.f);
		}

		m_block_models.resize(1);
		SAFE_DELETE(m_pBlockModelFilter);

		GetBlockModel().LoadModelByTexture(uvPattern);
		GetBlockModel().SetCategoryID(GetCategoryID());
		if (!IsMatchAttribute(BlockTemplate::batt_cubeModel) && IsMatchAttribute(BlockTemplate::batt_customModel))
		{
			GetBlockModel().SetUniformLighting(true);
			GetBlockModel().SetIsCubeAABB(false);
		}
	}

	void BlockTemplate::SetTexture0(const char* texName, int nIndex)
	{
		if(texName)
		{
			if (nIndex == 0 && (IsMatchAttribute(BlockTemplate::batt_pos_tiling) || IsMatchAttribute(BlockTemplate::batt_random_tiling)))
			{
				regex r("^.+_x(\\d+)\\..+$");

				cmatch num;
				if (regex_search(texName, num, r))
				{
					std::string str(num[1].first, num[1].second - num[1].first);
					setTileSize(StringHelper::StrToInt(str.c_str()));
				}
			}

			if ((int)m_textures0.size() <= nIndex)
				m_textures0.resize(nIndex + 1, NULL);
			m_textures0[nIndex] = CGlobals::GetAssetManager()->LoadTexture("", texName, TextureEntity::StaticTexture);
		}
		else
		{
			if (nIndex < (int)m_textures0.size())
				m_textures0[nIndex] = nullptr;
		}
	}

	void BlockTemplate::SetTexture1(const char* texName)
	{
		if(texName)
		{
			m_secondTexName = texName;
			m_textures1[0] = CGlobals::GetAssetManager()->LoadTexture("", m_secondTexName, TextureEntity::StaticTexture);
		}
		else
		{
			m_secondTexName.clear();
			m_textures1[0] = nullptr;
		}
	}

	void BlockTemplate::SetNormalMap(const char* texName)
	{
		if(texName)
		{
			m_normalMapName = texName;
			m_pNormalMap = CGlobals::GetAssetManager()->LoadTexture("",m_normalMapName,TextureEntity::StaticTexture);
		}
		else
		{
			m_pNormalMap = nullptr;
		}
	}

	void BlockTemplate::GetBoundingBoxVertices( Vector3 * pVertices, int* pNumber )
	{
		GetBlockModel().GetBoundingBoxVertices(pVertices, pNumber);
	}

	BlockModel& BlockTemplate::CreateGetBlockModel(int nIndex /*= 0*/)
	{
		if (m_pBlockModelFilter != 0)
			return m_pBlockModelFilter->GetBlockModel(nIndex);
		else
		{
			if (nIndex >= (int)m_block_models.size())
				m_block_models.resize(nIndex + 1);
			return m_block_models[nIndex];
		}
	}

	BlockModel& BlockTemplate::GetBlockModelByData(uint32 nData)
	{
		if (m_pBlockModelFilter != 0)
			return m_pBlockModelFilter->GetBlockModelByData(nData & 0xff);
		else
			return m_block_models[0];
	}


	BlockModel& BlockTemplate::GetBlockModel(int nIndex)
	{
		if(m_pBlockModelFilter!=0)
			return m_pBlockModelFilter->GetBlockModel(nIndex);
		else
			return m_block_models[nIndex];
	}

	BlockModel& BlockTemplate::GetBlockModel(CBlockWorld* pBlockManager, uint16_t bx, uint16_t by, uint16_t bz, uint16_t nBlockData /*= 0*/, Block** neighborBlocks)
	{
		if(m_pBlockModelFilter!=0)
			return m_pBlockModelFilter->GetBlockModel(pBlockManager, GetID(), bx, by, bz, nBlockData, neighborBlocks);
		else{
			return m_block_models[0];
		}
	}

	void BlockTemplate::LoadModel( const std::string& sModelName )
	{
		GetBlockModel().LoadModel(sModelName);
		
		if (IsMatchAttribute(BlockTemplate::batt_customModel))
			GetBlockModel().SetUniformLighting(true);

		if(sModelName == "wire")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CWireModelProvider(this);
		}
		else if (sModelName == "slope")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CSlopeModelProvider(this);
		}
		else if(sModelName == "grass")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CGrassModelProvider(this);

			// modify 16 different scaling and 
			m_block_models.resize(16, GetBlockModel());

			const float random_numbers [] = {1.f,0.3f,0.8f, 0.5f,0.2f,0.9f, 0.1f, 0.15f, 0.4f, 0.55f, 0.8f, 0.95f, 0.25f, 0.05f, 0.75f, 0.65f, 0.25f, 0.85f, 1.f, 0.6f, 0.9f, };
			for (int i=0; i<16; i++)
			{
				BlockModel& block_model = m_block_models[i];
				float fScaling = 0.8f + random_numbers[i]*0.2f;
				Vector3 vOffset((random_numbers[i]-0.5f)*0.5f, 0, (random_numbers[16-i]-0.5f)*0.5f);
				block_model.Transform(vOffset, fScaling);
			}
		}
		else if(sModelName == "stairs")
		{
			// TODO: in future: currently it is not a cubeModel yet
			// SetLightOpacity(15);
		}
		else if(sModelName == "slab")
		{
			SetLightOpacity(5);
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this,2);

			// modify 16 different scaling and 
			m_block_models.resize(2, GetBlockModel());
			m_block_models[0].LoadModel("slab_top");
			m_block_models[1].LoadModel("slab_bottom");

			SetPhysicalHeight(0.5f);
		}
		else if(sModelName == "vine")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this, 24);

			// modify 
			m_block_models.resize(24, GetBlockModel());
			for (int dir = 0; dir < 4; dir++)
			{
				char sName[] = "vine00";
				sName[5] = '0' + dir;
				for (int i = 0; i < 6; i++)
				{
					sName[4] = '0' + i;
					m_block_models[i+dir*6].LoadModel(sName);
				}
			}
		}
		else if(sModelName == "halfvine")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this,6);

			// modify 
			m_block_models.resize(6, GetBlockModel());
			char sName[] = "halfvine0";
			for(int i=0;i<6;i++)
			{
				sName[8] = '0' + i;
				m_block_models[i].LoadModel(sName);
			}
		}
		else if (sModelName == "plate")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this, 6);

			// modify 
			m_block_models.resize(6, GetBlockModel());
			char sName[] = "plate0";
			for (int i = 0; i < 6; i++)
			{
				sName[5] = '0' + i;
				m_block_models[i].LoadModel(sName);
			}
		}
		else if (sModelName == "carpet")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CCarpetModelProvider(this);
		}
		else if(sModelName.find("plant") == 0)
		{
			// four state plant: 128*32 textures: mature,  growing, tiny, withered
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this,4);

			// modify 
			m_block_models.resize(4, GetBlockModel());
			char sName[] = "cross0/4";
			for(int i=0;i<4;i++)
			{
				sName[5] = '0' + i;
				m_block_models[i].LoadModel(sName);
			}
		}
		else if(sModelName.find("seed_plant") == 0)
		{
			// four state plant: 128*32 textures: mature,  growing, seed, withered
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			m_pBlockModelFilter = new CLinearModelProvider(this,4);

			// modify 
			m_block_models.resize(4, GetBlockModel());
			m_block_models[0].LoadModel("cross0/4");
			m_block_models[1].LoadModel("cross1/4");
			m_block_models[2].LoadModel("cross2/4");
			m_block_models[3].LoadModel("seed3/4"); // this is flat seed here
		}
		else if (sModelName == "codeblock")
		{
			// set model filter
			SAFE_DELETE(m_pBlockModelFilter);
			const int nDataCount = 16;
			m_pBlockModelFilter = new CLinearModelProvider(this, nDataCount);
			m_block_models.resize(nDataCount, GetBlockModel());
			m_block_models[0].SetTextureIndex(2);
		}
	}

	void BlockTemplate::SetAssociatedBlock( uint16_t associated_blockid )
	{
		m_associated_blockid = associated_blockid;
	}

	bool BlockTemplate::IsAssociatedBlockID( uint16_t block_id )
	{
		return (GetID() == block_id) || ((m_associated_blockid == block_id) && (m_associated_blockid>0));
	}

	void BlockTemplate::setProvidePower( bool bValue )
	{
		m_bProvidePower = bValue;
	}

	bool BlockTemplate::isBlockNormalCube()
	{
		return IsMatchAttribute(batt_solid | batt_cubeModel) && !m_bProvidePower;
	}

	void BlockTemplate::SetTorchLight( uint8_t value )
	{
		if(value>=0 && value<=15)
			m_nLightValue = value;
	}

	void BlockTemplate::GetAABB( CBlockWorld* pBlockManager, uint16_t bx, uint16_t by, uint16_t bz, CShapeAABB* pOutAABB )
	{
		if(GetBlockModel().IsCubeAABB())
		{
			GetBlockModel().GetAABB(pOutAABB);
		}
		else
		{
			Block* pBlock = pBlockManager->GetBlock(bx,by,bz);
			if(pBlock)
			{
				if(IsMatchAttribute(BlockTemplate::batt_cubeModel))
				{
					GetBlockModel(pBlockManager, bx,by,bz, pBlock->GetUserData()).GetAABB(pOutAABB);
				}
				else if(IsMatchAttribute(BlockTemplate::batt_customModel))
				{
					const double blockSize = BlockConfig::g_blockSize;
					const double fHalfBlockSize = blockSize /2;
					Vector3 vPos(Vector3((float)(blockSize*bx+fHalfBlockSize), (float)(blockSize*by + pBlockManager->GetVerticalOffset()+fHalfBlockSize), (float)(blockSize*bz+fHalfBlockSize)));

					char tmp[256];
					snprintf(tmp, 255, "%d,%d,%d", bx,by,bz);
					CBaseObject* pObject = CGlobals::GetScene()->GetObject(tmp, vPos, false);
					if(pObject)
					{
						pObject->GetViewClippingObject()->GetAABB(pOutAABB);
						pOutAABB->GetCenter() -= (vPos - Vector3((float)(fHalfBlockSize), (float)(fHalfBlockSize), (float)(fHalfBlockSize)));
					}
					else
					{
						GetBlockModel().GetAABB(pOutAABB);
					}
				}
				else
				{
					GetBlockModel().GetAABB(pOutAABB);
				}
			}
			else
				GetBlockModel().GetAABB(pOutAABB);
		}
	}

	float BlockTemplate::GetPhysicalHeight()
	{
		return m_fPhysicalHeight;
	}

	float BlockTemplate::GetPhysicalHeight( CBlockWorld* pBlockManager, uint16_t bx, uint16_t by, uint16_t bz )
	{
		if (m_fPhysicalHeight>0.f && IsMatchAttribute(BlockTemplate::batt_cubeModel) && (m_pBlockModelFilter || m_block_models.size()>1))
		{
			Block* pBlock = pBlockManager->GetBlock(bx,by,bz);
			if(pBlock)
			{
				CShapeAABB aabb;
				GetBlockModel(pBlockManager, bx,by,bz, pBlock->GetUserData()).GetAABB(&aabb);
				// get max y height value.
				return aabb.GetMax(1);
			}
		}
		return m_fPhysicalHeight;
	}

	void BlockTemplate::SetPhysicalHeight( float fHeight )
	{
		m_fPhysicalHeight = fHeight;
	}

	void BlockTemplate::SetAttribute(DWORD dwAtt, bool bTurnOn /*= true*/)
	{
		if (bTurnOn)
			m_attFlag |= dwAtt;
		else
			m_attFlag &= (~dwAtt);
	}

	float BlockTemplate::GetSpeedReductionPercent() const
	{
		return m_fSpeedReductionPercent;
	}

	void BlockTemplate::SetSpeedReductionPercent(float val)
	{
		m_fSpeedReductionPercent = val;
	}

	void BlockTemplate::SetLightOpacity(int32 nValue)
	{
		m_lightOpacity = nValue;
		m_lightScatterStep = nValue;
	}

	void BlockTemplate::MakeCustomLinearModelProvider(int nModelCount)
	{
		// set model filter
		SAFE_DELETE(m_pBlockModelFilter);
		m_pBlockModelFilter = new CLinearModelProvider(this, nModelCount);
	}

	TextureEntity* BlockTemplate::GetTexture0(uint32 nUserData)
	{
		int nIndex = GetBlockModelByData(nUserData).GetTextureIndex();
		return nIndex < (int32)(m_textures0.size()) ? m_textures0[nIndex] : m_textures0[0];
	}

	TextureEntity* BlockTemplate::GetTexture1()
	{
		return m_textures1[0];
	}

	void BlockTemplate::SetMapColor(Color val)
	{
		m_dwMapColor = val;
	}

	Color BlockTemplate::GetMapColor() const
	{
		return m_dwMapColor;
	}

	DWORD BlockTemplate::GetBlockColor(int32_t blockData)
	{
		DWORD dwBlockColor = Color::White;
		if (HasColorData())
		{
			dwBlockColor = 0xff000000 | Color::convert16_32((uint16)blockData);
		}
		else if (IsColorData8Bits())
		{
			dwBlockColor = 0xff000000 | (~ Color::convert8_32((uint8)(blockData >> 8)));
		}
		else
		{
			dwBlockColor = GetMapColor();
		}
		return dwBlockColor;
	}

	DWORD BlockTemplate::GetDiffuseColor(int32_t blockData)
	{
		DWORD dwBlockColor = Color::White;
		if (HasColorData())
		{
			dwBlockColor = 0xff000000 | Color::convert16_32((uint16)blockData);
		}
		else if (IsColorData8Bits())
		{
			dwBlockColor = 0xff000000 | (~Color::convert8_32((uint8)(blockData >> 8)));
		}
		return dwBlockColor;
	}

	bool BlockTemplate::isSolidBlock()
	{
		return IsMatchAttribute(batt_solid);
	}

	void BlockTemplate::setUnderWaterColor(const Color & val)
	{
		m_UnderWaterColor = val;
	}

	const Color & BlockTemplate::getUnderWaterColor()const
	{
		return m_UnderWaterColor;
	}

	int BlockTemplate::getTileSize() const
	{
		return m_nTileSize;
	}

	void BlockTemplate::setTileSize(int nTile)
	{
		if (m_nTileSize != nTile)
		{
			m_nTileSize = nTile;
			if (IsMatchAttribute(BlockTemplate::batt_pos_tiling))
			{
				SetAttribute(batt_pos_tiling, m_nTileSize > 1);
				SetAttribute(batt_random_tiling, false);
			}
			else if(IsMatchAttribute(BlockTemplate::batt_random_tiling))
			{
				SetAttribute(batt_pos_tiling, false);
				SetAttribute(batt_random_tiling, m_nTileSize > 1);
			}
			else
			{
				//any case should this happen?
				SetAttribute(batt_pos_tiling, false);
				SetAttribute(batt_random_tiling, false);			    
			}
		}
	}

}

//-----------------------------------------------------------------------------
// Class:	Renderable chunks
// Authors:	LiXizhi, Clayman
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2012.11.26
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include <boost/thread/tss.hpp>
#include "RenderableChunk.h"
#include "ParaVertexBufferPool.h"
#include "BlockRegion.h"
#include "BlockModel.h"
#include "BlockChunk.h"
#include "BlockWorld.h"
#include "BlockCommon.h"
#include "BlockTessellators.h"
#include "VertexFVF.h"
#include "ChunkVertexBuilderManager.h"


namespace ParaEngine
{
	int RenderableChunk::s_nTotalRenderableChunks = 0;

	RenderableChunk::RenderableChunk()
		:m_pWorld(NULL), m_chunkBuildState(ChunkBuild_empty), m_nDelayedRebuildTick(0), m_nChunkViewDistance(0), m_nViewIndex(0), m_nRenderFrameCount(0), m_nLastVertexBufferBytes(0), m_dwShaderID(-1), m_bIsMainRenderer(true), m_bIsDirtyByBlockChange(true)
	{
		m_isDirty = true;
		m_regionX = -1;
		m_regionZ = -1;
		m_packedChunkID = 0;
		m_totalFaceCount = 0;
		s_nTotalRenderableChunks++;
	}

	RenderableChunk::~RenderableChunk()
	{
		WaitUntilChunkReady();
		ClearBuilderBuffer();
		DeleteDeviceObjects();
		--s_nTotalRenderableChunks;
	}


	bool RenderableChunk::ShouldRebuildRenderBuffer(CBlockWorld* pWorld, bool bNewBuffer /*= true*/, bool bUpdatedBuffer /*= true*/)
	{
		BlockRegion * pOwnerBlockRegion = pWorld->GetRegion(m_regionX, m_regionZ);
		if (!pOwnerBlockRegion || pOwnerBlockRegion->IsLocked())
			return false;
		else
			m_pWorld = pOwnerBlockRegion->GetBlockWorld();

		return ((bNewBuffer && m_isDirty) ||
			(bUpdatedBuffer && pOwnerBlockRegion->IsChunkDirty(m_packedChunkID))) && !IsBuildingBuffer();
	}

	bool RenderableChunk::RebuildRenderBuffer(CBlockWorld* pWorld, bool bAsyncMode)
	{
		BlockRegion * pOwnerBlockRegion = pWorld->GetRegion(m_regionX, m_regionZ);
		if (pOwnerBlockRegion && !pOwnerBlockRegion->IsLocked())
		{
			if (bAsyncMode)
			{
				return ChunkVertexBuilderManager::GetInstance().AddChunk(this);
			}
			else
			{
				BuildRenderGroup();
				m_isDirty = false;
				if (IsMainRenderer())
					pOwnerBlockRegion->SetChunkDirty(m_packedChunkID, false);
				SetChunkBuildState(RenderableChunk::ChunkBuild_Ready);

				// transfer ownership from builder task to render task. 
				m_renderTasks = m_builder_tasks;
				m_builder_tasks.clear();
				ClearBuilderBuffer();
				return true;
			}
		}
		return true;
	}


	void RenderableChunk::FillRenderQueue(CBlockWorld* pWorld, Vector3& renderOfs, float verticalOffset)
	{
		// do not render dirty ones. 
		if (m_isDirty || m_renderTasks.size() == 0)
			return;

		BlockRegion * pOwnerBlockRegion = pWorld->GetRegion(m_regionX, m_regionZ);
		if (!pOwnerBlockRegion || pOwnerBlockRegion->IsLocked())
			return;
		else
			m_pWorld = pOwnerBlockRegion->GetBlockWorld();


		uint16_t maxDistValue = 0xfff;
		uint16_t dist = 0;
		bool bGroupByChunk = m_pWorld->IsGroupByChunkBeforeTexture();
		if (bGroupByChunk)
		{
			dist = (uint16_t)GetViewIndex();
		}
		else
		{
			Uint16x3 eyeChunk = pWorld->GetEyeChunkId();
			Uint16x3 curChunk;
			UnpackChunkIndex(m_packedChunkID, curChunk.x, curChunk.y, curChunk.z);

			curChunk.x += pOwnerBlockRegion->m_minChunkId_ws.x;
			curChunk.y += pOwnerBlockRegion->m_minChunkId_ws.y;
			curChunk.z += pOwnerBlockRegion->m_minChunkId_ws.z;

			int16_t deltaX = (int16)eyeChunk.x - (int16)curChunk.x;
			int16_t deltaY = (int16)eyeChunk.y - (int16)curChunk.y;
			int16_t deltaZ = (int16)eyeChunk.z - (int16)curChunk.z;

			//pack distance as 12 bit value
			int32_t dist2 = deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ;
			
			int32_t maxDist2 = pWorld->GetActiveChunkDim() * pWorld->GetActiveChunkDim() * 3;
			float r = (float)dist2 / maxDist2;
			if (r > 1)
				r = 1;

			dist = (uint16_t)(r * maxDistValue);
		}
	
		for(size_t i=0;i< m_renderTasks.size();i++)
		{
			BlockRenderTask *task = m_renderTasks[i];
			uint16_t priority = BlockTemplate::g_maxRenderPriority - task->GetTemplate()->GetRenderPriority();
			
			if (task->GetTemplate()->GetRenderPass() == BlockRenderPass_AlphaBlended)
			{
				//invert distant for alpha blended object
				uint32_t renderOrder = ((maxDistValue - dist) << 16);
				renderOrder += (task->GetTemplateId() + (task->GetTemplate()->GetCategoryID()<<8));
				renderOrder += (priority << 28);
				task->SetRenderOrder(renderOrder);
			}
			else
			{
				uint32_t renderOrder = (priority << 28);
				if (bGroupByChunk)
				{
					renderOrder += (dist << 16);
					renderOrder += (task->GetTemplateId() + (task->GetTemplate()->GetCategoryID() << 8));
				}
				else
				{
					renderOrder += ((task->GetTemplateId() + (task->GetTemplate()->GetCategoryID() << 8)) << 12);
					renderOrder += dist;
				}
				task->SetRenderOrder(renderOrder);
			}
			
			pWorld->AddRenderTask(task);
		}
	}

	int32 RenderableChunk::GetTotalFaceCount() const
	{
		return m_totalFaceCount;
	}

	void RenderableChunk::BuildRenderGroup()
	{
		if (!m_pWorld)
			return;

		BlockRegion * pOwnerBlockRegion = m_pWorld->GetRegion(m_regionX, m_regionZ);
		if(!pOwnerBlockRegion)
			return;

		ClearRenderTasks();
		ReleaseVertexBuffers();
		BlockChunk* pChunk = pOwnerBlockRegion->GetChunk(m_packedChunkID, false);
		if(!pChunk)
		{
			return;
		}

		//------------------------------------------------------------------------
		//fill instance group
		ResetInstanceGroups();
		int32 totalFaceCount = BuildInstanceGroupsByIdAndData(pChunk);

		if (totalFaceCount <= 0)
		{
			m_totalFaceCount = totalFaceCount;
			return;
		}

		SortAndMergeInstanceGroupsByTexture();
		
		//----------------------------------------------------------
		//2.create a big buffer to hold all blocks

		uint32_t bufferSize = sizeof(BlockVertexCompressed) * (totalFaceCount * 4);

		BlockRenderMethod dwShaderID = (BlockRenderMethod)GetShaderID();

		m_totalFaceCount = totalFaceCount;
		int32 nFaceCountCompleted = 0;
		
		const int32 maxFaceCountPerBatch = BlockConfig::g_maxFaceCountPerBatch;

		BlockGeneralTessellator& tessellator = GetBlockTessellator();
		//-------------------------------------------------------------
		//3.fill buffer

		int32 nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
		ParaVertexBuffer* pVertexBuffer = RequestVertexBuffer(nFreeFaceCountInVertexBuffer);
		if (!pVertexBuffer)
			return;
		BlockVertexCompressed* pVertices;
		pVertexBuffer->Lock((void**)&pVertices);
		uint32_t vertexOffset = 0;

		std::vector<InstanceGroup* >& instanceGroups = GetInstanceGroups();

		int nSize = (int)instanceGroups.size();
		InstanceGroup* pInstGroup = NULL;
		InstanceGroup* pLastInstGroup = NULL;
		BlockRenderTask *pTask = NULL;
		for (int i = 0; (i < nSize && (pInstGroup = instanceGroups[i])->instances.size()>0); i++)
		{
			BlockTemplate* pTemplate = pInstGroup->m_pTemplate;
			uint32_t nBlockData = pInstGroup->m_blockData;
			std::vector<uint16_t>& instanceGroup = pInstGroup->instances;
			uint32 groupSize = instanceGroup.size();
			uint32 instCount = groupSize;
			int nMaxFaceCountPerInstance = pTemplate->GetBlockModelByData(nBlockData).GetFaceCount();

			if (nFreeFaceCountInVertexBuffer < (int32)pInstGroup->GetFaceCount())
			{
				if (nFreeFaceCountInVertexBuffer < (maxFaceCountPerBatch*0.1) )
				{
					pVertexBuffer->Unlock();
					nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
					pVertexBuffer = RequestVertexBuffer(nFreeFaceCountInVertexBuffer);
					if (!pVertexBuffer)
						return;
					pVertexBuffer->Lock((void**)&pVertices);
					vertexOffset = 0;
					pLastInstGroup = NULL;
				}
				if (nFreeFaceCountInVertexBuffer < (int32)pInstGroup->GetFaceCount())
				{
					instCount = nFreeFaceCountInVertexBuffer / nMaxFaceCountPerInstance;
				}
				else
				{
					instCount = groupSize;
				}
			}

			//add render task
			if (!pTask || !(pInstGroup->CanShareRenderBufferWith(pLastInstGroup)))
			{
				pTask = BlockRenderTask::CreateTask();
				pTask->Init(pTemplate, nBlockData, vertexOffset, pVertexBuffer->GetDevicePointer(), pChunk->m_minBlockId_ws);
				m_builder_tasks.push_back(pTask);
				pLastInstGroup = pInstGroup;
			}

			int32 batchInstCount = 0;
			int32 unprocessedInstCount = groupSize;
			for(int inst = 0;inst < (int)groupSize;inst++)
			{
				//start a new one if instances can't fit into one batch
				batchInstCount++;
				if (nFreeFaceCountInVertexBuffer < nMaxFaceCountPerInstance)
				{
					pVertexBuffer->Unlock();
					nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
					pVertexBuffer = RequestVertexBuffer(nFreeFaceCountInVertexBuffer);
					if (!pVertexBuffer)
						return;
					pVertexBuffer->Lock((void**)&pVertices);
					vertexOffset = 0;
						
					if (nFreeFaceCountInVertexBuffer < unprocessedInstCount*nMaxFaceCountPerInstance)
					{
						instCount = nFreeFaceCountInVertexBuffer / nMaxFaceCountPerInstance;
					}
					else
					{
						instCount = unprocessedInstCount;
					}
					pTask = BlockRenderTask::CreateTask();
					pTask->Init(pTemplate, nBlockData, vertexOffset, pVertexBuffer->GetDevicePointer(), pChunk->m_minBlockId_ws);
					m_builder_tasks.push_back(pTask);
					pLastInstGroup = pInstGroup;
					
					batchInstCount = 1;
				}
				
				//--------------------------------------------------------------
				// assemble block model data
				//--------------------------------------------------------------
				BlockVertexCompressed* pBlockModelVertices = NULL;
				unprocessedInstCount--;
				int32 nFaceCount = tessellator.TessellateBlock(pChunk, instanceGroup[inst], dwShaderID, &pBlockModelVertices);
				if (nFaceCount > 0)
				{
					int32 nVertexCount = nFaceCount * 4;
					if (nFreeFaceCountInVertexBuffer >= nFaceCount)
					{
						memcpy(pVertices, pBlockModelVertices, sizeof(BlockVertexCompressed)*nVertexCount);
						pVertices += nVertexCount;
						vertexOffset += nVertexCount;

						nFaceCountCompleted += nFaceCount;
						pTask->AddRectFace(nFaceCount);
						nFreeFaceCountInVertexBuffer -= nFaceCount;
					}
					else
					{
						// this could happen when block changes when we are still processing it
						OUTPUT_LOG("fatal error: not enough face count in vertex buffer. \n");
					}
				}
			}
		}
		pVertexBuffer->Unlock();

	}

	void RenderableChunk::OnLeaveWorld()
	{
		DeleteDeviceObjects();
		ClearBuilderBuffer();
		Reset();
	}

	void RenderableChunk::DeleteDeviceObjects()
	{
		ClearRenderTasks();
		ReleaseVertexBuffers();
	}

	void RenderableChunk::RendererRecreated()
	{
		ClearRenderTasks();
		m_vertexBuffers.clear();
	}

	void RenderableChunk::ReuseChunk(BlockRegion* pOwnerBlockRegion,int16_t packedChunkId_rs)
	{
		ClearChunkData();
		m_nLastVertexBufferBytes = 0;
		if(pOwnerBlockRegion)
		{
			m_regionX = pOwnerBlockRegion->GetRegionX();
			m_regionZ = pOwnerBlockRegion->GetRegionZ();
			m_pWorld = pOwnerBlockRegion->GetBlockWorld();
		}
		else
		{
			m_regionX = -1;
			m_regionZ = -1;
			m_pWorld = NULL;
		}
		m_packedChunkID = packedChunkId_rs;

		if(pOwnerBlockRegion == nullptr || packedChunkId_rs == -1)
		{
			return;
		}

		Uint16x3 chunkId_rs;
		UnpackChunkIndex(m_packedChunkID,chunkId_rs.x,chunkId_rs.y,chunkId_rs.z);

		Uint16x3 minRegionBlockId = pOwnerBlockRegion->m_minBlockId_ws;
		float blockSize = BlockConfig::g_blockSize;
		
		Vector3 vMinWorld, vMaxWorld;
		vMinWorld.x = minRegionBlockId.x * blockSize;
		vMinWorld.x += chunkId_rs.x * BlockConfig::g_chunkSize;

		vMinWorld.y = minRegionBlockId.y * blockSize;
		vMinWorld.y += chunkId_rs.y * BlockConfig::g_chunkSize + pOwnerBlockRegion->GetBlockWorld()->GetVerticalOffset();
		
		vMinWorld.z = minRegionBlockId.z  * blockSize;
		vMinWorld.z += chunkId_rs.z * BlockConfig::g_chunkSize;

		vMaxWorld = vMinWorld + Vector3::UNIT_SCALE * (blockSize * BlockConfig::g_chunkBlockDim);

		m_pShapeAABB.SetMinMax(vMinWorld, vMaxWorld);
	}

	void RenderableChunk::Reset()
	{
		m_regionX = -1;
		m_regionZ = -1;
		m_isDirty = false;
		m_nDelayedRebuildTick = 0;
	}

	bool RenderableChunk::IsEmptyChunk()
	{
		return GetChunk() == NULL;
	}

	bool RenderableChunk::IsDirtyByNeighbor()
	{
		auto pChunk = GetChunk();
		return pChunk && pChunk->IsDirtyByNeighbor();
	}

	bool RenderableChunk::GetIsDirtyByBlockChange()
	{
		auto pChunk = GetChunk();
		return pChunk && pChunk->IsDirtyByBlockChange();
	}

	bool RenderableChunk::IsIntersect(CShapeSphere& sphere)
	{
		return !IsEmptyChunk() && m_pShapeAABB.Intersect(sphere);
	}

	void RenderableChunk::StaticInit()
	{

	}

	void RenderableChunk::StaticRelease()
	{
		BlockRenderTask::ReleaseTaskPool();
	}

	BlockChunk* RenderableChunk::GetChunk()
	{
		if (m_regionX >= 0 && m_pWorld)
		{
			BlockRegion * pOwnerBlockRegion = m_pWorld->GetRegion(m_regionX, m_regionZ);
			if(pOwnerBlockRegion)
				return pOwnerBlockRegion->GetChunk(m_packedChunkID, false);
		}
		return NULL;
	}

	bool RenderableChunk::IsNearbyChunksLoaded()
	{
		BlockChunk* pChunk = GetChunk();
		return pChunk && pChunk->IsNearbyChunksLoaded();
	}


	void RenderableChunk::ClearBuilderBuffer()
	{
		for (auto& task : m_builder_tasks)
			BlockRenderTask::ReleaseTask(task);
		m_builder_tasks.clear();

		for (auto& buf : m_memoryBuffers)
		{
			buf.ReleaseBuffer();
		}
		m_memoryBuffers.clear();
	}

	void RenderableChunk::ClearRenderTasks()
	{
		for (uint32_t i = 0; i < m_renderTasks.size(); i++)
			BlockRenderTask::ReleaseTask(m_renderTasks[i]);
		m_renderTasks.clear();
	}

	void RenderableChunk::ReleaseVertexBuffers()
	{
		ParaVertexBufferPool* pPool = GetVertexBufferPool();

		for (auto vertexBuffer : m_vertexBuffers)
		{
			pPool->ReleaseBuffer(vertexBuffer);
		}
		m_vertexBuffers.clear();
	}

	ParaVertexBufferPool* RenderableChunk::GetVertexBufferPool()
	{
		static std::string s_pool_name = "chunk";
		return CVertexBufferPoolManager::GetInstance().CreateGetPool(s_pool_name);
	}

	ParaVertexBuffer* RenderableChunk::RequestVertexBuffer(int32 nFreeFaceCountInVertexBuffer)
	{
		ParaVertexBuffer* pVertexBuffer = GetVertexBufferPool()->CreateBuffer(nFreeFaceCountInVertexBuffer*sizeof(BlockVertexCompressed) * 4, block_vertex::FVF, D3DUSAGE_WRITEONLY);
		if (pVertexBuffer && pVertexBuffer->IsValid())
		{
			m_vertexBuffers.push_back(pVertexBuffer);
			return pVertexBuffer;
		}
		else
		{
			OUTPUT_LOG("warn: failed to CreateVertexBuffer of size %d for renderable chunk\n", nFreeFaceCountInVertexBuffer);
			return NULL;
		}
	}

	void RenderableChunk::StaticReleaseInstGroup(std::vector<RenderableChunk::InstanceGroup* >* pInstances)
	{
		for (int i = 0; i < (int)pInstances->size(); i++)
		{
			SAFE_DELETE((*pInstances)[i]);
		}
		pInstances->clear();
		delete pInstances;
	}

	BlockGeneralTessellator& RenderableChunk::GetBlockTessellator()
	{
		static boost::thread_specific_ptr <BlockGeneralTessellator> tls_tessellator;
		if (!tls_tessellator.get())
			tls_tessellator.reset(new BlockGeneralTessellator(m_pWorld));
		BlockGeneralTessellator& tessellator = *tls_tessellator;
		tessellator.SetWorld(m_pWorld);
		return tessellator;
	}

	bool RenderableChunk::IsDirtyByBlockChange() const
	{
		return m_bIsDirtyByBlockChange;
	}

	void RenderableChunk::IsDirtyByBlockChange(bool val)
	{
		m_bIsDirtyByBlockChange = val;
	}

	std::vector<RenderableChunk::InstanceGroup* >& RenderableChunk::GetInstanceGroups()
	{
		static boost::thread_specific_ptr <std::vector<InstanceGroup*>> tls_instanceGroups(StaticReleaseInstGroup);
		if (!tls_instanceGroups.get())
			tls_instanceGroups.reset(new std::vector<InstanceGroup*>());
		return *tls_instanceGroups;
	}

	std::map<int32_t, int>& RenderableChunk::GetInstanceMap()
	{
		static boost::thread_specific_ptr <std::map<int32_t, int>> tls_instance_map;
		if (!tls_instance_map.get())
			tls_instance_map.reset(new std::map<int32_t, int>());
		return *tls_instance_map;
	}

	void RenderableChunk::ResetInstanceGroups()
	{
		std::vector<InstanceGroup* >& instanceGroups = GetInstanceGroups();
		int nInstanceSize = (int)instanceGroups.size();
		for (int i = 0; i < nInstanceSize; i++)
		{
			InstanceGroup* group = (instanceGroups[i]);
			if (!group->isEmpty())
				group->reset();
			else
				break;
		}
		if (nInstanceSize == 0)
			instanceGroups.push_back(new InstanceGroup());

		GetInstanceMap().clear();
	}

	int32 RenderableChunk::BuildInstanceGroupsByIdAndData(BlockChunk* pChunk)
	{
		int32 totalFaceCount = 0;
		int32 cachedGroupIdx = 0;
		uint16_t nSize = (uint16_t)pChunk->m_blockIndices.size();
		std::map < int32_t, int > & instance_map = GetInstanceMap();
		std::vector<InstanceGroup* >& instanceGroups = GetInstanceGroups();

		for (uint16_t i = 0; i < nSize; i++)
		{
			Block* pBlock = pChunk->GetBlock(i);
			if (!pBlock)
				continue;

			if (pBlock->GetTemplate()->IsMatchAttribute(BlockTemplate::batt_cubeModel)
				&& pChunk->IsVisibleBlock(i, pBlock))
			{
				//find correct group,nearby blocks may use the same template,so we 
				//compare it with current group first.
				uint32 nBlockID = pBlock->GetTemplate()->GetID();
				uint32 nBlockData = pBlock->GetTemplate()->HasColorData() ? 0 : pBlock->GetUserData();
				BlockModel& blockmodel = pBlock->GetTemplate()->GetBlockModelByData(nBlockData);
				if (nBlockData > 0)
					nBlockID = ((nBlockData << 12) | nBlockID);
				auto curIndex = instance_map.find(nBlockID);
				if (curIndex != instance_map.end())
				{
					cachedGroupIdx = curIndex->second;
				}
				else // if(m_instanceGroups[cachedGroupIdx].m_pTemplate != pBlock->GetTemplate())
				{
					for (uint32_t j = 0; j < instanceGroups.size(); j++)
					{
						if (instanceGroups[j]->m_pTemplate == pBlock->GetTemplate() && instanceGroups[j]->m_blockData == nBlockData)
						{
							cachedGroupIdx = j;
							break;
						}
						else if (instanceGroups[j]->m_pTemplate == 0)
						{
							//template doesn't match any group 
							instanceGroups[j]->m_pTemplate = pBlock->GetTemplate();
							instanceGroups[j]->m_blockData = nBlockData;
							cachedGroupIdx = j;
							break;
						}
					}

					if (instanceGroups[cachedGroupIdx]->m_pTemplate != pBlock->GetTemplate() || instanceGroups[cachedGroupIdx]->m_blockData != nBlockData)
					{
						instanceGroups.push_back(new InstanceGroup());
						cachedGroupIdx = instanceGroups.size() - 1;
						instanceGroups[cachedGroupIdx]->m_pTemplate = pBlock->GetTemplate();
						instanceGroups[cachedGroupIdx]->m_blockData = nBlockData;
					}
					instance_map[nBlockID] = cachedGroupIdx;
				}

				uint32 nFaceCount = blockmodel.GetFaceCount();
				instanceGroups[cachedGroupIdx]->AddInstance(i, nFaceCount);
				totalFaceCount += nFaceCount;
			}
		}	
		return totalFaceCount;
	}

	RenderableChunk::ChunkBuildState RenderableChunk::GetChunkBuildState() const
	{
		return m_chunkBuildState;
	}

	void RenderableChunk::SetChunkBuildState(RenderableChunk::ChunkBuildState val)
	{
		m_chunkBuildState = val;
		if (m_chunkBuildState == ChunkBuild_Ready)
			SetDelayedRebuildTick(0);
	}

	void RenderableChunk::WaitUntilChunkReady()
	{
		while (m_chunkBuildState == ChunkBuild_Rebuilding || m_chunkBuildState == ChunkBuild_RequestRebuild)
		{
			SLEEP(1);
		}
	}


	void RenderableChunk::RebuildRenderBufferToMemory(Scoped_ReadLock<BlockReadWriteLock>* Lock_, int* pnCpuYieldCount)
	{
		// call this function regularly to yield CPU to writer thread only if they are waiting to write data. 
#define CHECK_YIELD_CPU_TO_WRITER   if(Lock_ && Lock_->mutex().HasWaitingWriters()){ \
	nCpuYieldCount++;\
	Lock_->unlock(); \
	Lock_->lock(); \
	if(!m_pWorld->IsInBlockWorld() || m_isDirty)\
		return;\
}

		if (GetChunkBuildState() != ChunkBuild_Rebuilding)
			return;
		if (!m_pWorld)
			return;
		BlockRegion * pOwnerBlockRegion = m_pWorld->GetRegion(m_regionX, m_regionZ);
		if (!pOwnerBlockRegion)
			return;

		// make chunk not dirty anymore, safe to call, since main thread has write lock that will 
		// not modify the block world when this function is being executed. 
		m_isDirty = false;

		if (IsMainRenderer())
			pOwnerBlockRegion->SetChunkDirty(m_packedChunkID, false);

		ClearBuilderBuffer();

		BlockChunk* pChunk = pOwnerBlockRegion->GetChunk(m_packedChunkID, false);
		if (!pChunk)
		{
			return;
		}
		int nCpuYieldCount = 0;
		//------------------------------------------------------------------------
		//fill instance group
		ResetInstanceGroups();
		CHECK_YIELD_CPU_TO_WRITER;
		int32 totalFaceCount = BuildInstanceGroupsByIdAndData(pChunk);
		CHECK_YIELD_CPU_TO_WRITER;
		if (totalFaceCount <= 0)
		{
			m_totalFaceCount = totalFaceCount;
			return;
		}

		SortAndMergeInstanceGroupsByTexture();
		CHECK_YIELD_CPU_TO_WRITER;
		//----------------------------------------------------------
		//2.create a big buffer to hold all blocks
		
		uint32_t bufferSize = sizeof(BlockVertexCompressed) * (totalFaceCount * 4);

		BlockRenderMethod dwShaderID = (BlockRenderMethod)GetShaderID();

		m_totalFaceCount = totalFaceCount;
		int32 nFaceCountCompleted = 0;

		const int32 maxFaceCountPerBatch = BlockConfig::g_maxFaceCountPerBatch;
		//-------------------------------------------------------------
		//3.fill buffer
		BlockGeneralTessellator& tessellator = GetBlockTessellator();
		int32 nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
		int32 nMemoryBufferIndex = 0;
		ParaVertexBuffer memoryBuffer = RequestMemoryBuffer(nFreeFaceCountInVertexBuffer, &nMemoryBufferIndex);
		
		BlockVertexCompressed* pVertices;
		memoryBuffer.Lock((void**)&pVertices);
		uint32_t vertexOffset = 0;
		std::vector<InstanceGroup* >& instanceGroups = GetInstanceGroups();
		int nSize = (int)instanceGroups.size();
		InstanceGroup* pInstGroup = NULL;
		InstanceGroup* pLastInstGroup = NULL;
		BlockRenderTask *pTask = NULL;
		for (int i = 0; (i < nSize && (pInstGroup = instanceGroups[i])->instances.size()>0); i++)
		{
			BlockTemplate* pTemplate = pInstGroup->m_pTemplate;
			uint32_t nBlockData = pInstGroup->m_blockData;
			std::vector<uint16_t>& instanceGroup = pInstGroup->instances;
			uint32 groupSize = instanceGroup.size();
			uint32 instCount = groupSize;
			int nMaxFaceCountPerInstance = pTemplate->GetBlockModelByData(nBlockData).GetFaceCount();

			if (nFreeFaceCountInVertexBuffer < (int32)pInstGroup->GetFaceCount())
			{
				if (nFreeFaceCountInVertexBuffer < (maxFaceCountPerBatch*0.1))
				{
					memoryBuffer.Unlock();
					nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
					memoryBuffer = RequestMemoryBuffer(nFreeFaceCountInVertexBuffer, &nMemoryBufferIndex);
					memoryBuffer.Lock((void**)&pVertices);
					vertexOffset = 0;
					pLastInstGroup = NULL;
				}
				if (nFreeFaceCountInVertexBuffer < (int32)pInstGroup->GetFaceCount())
				{
					instCount = nFreeFaceCountInVertexBuffer / nMaxFaceCountPerInstance;
				}
				else
				{
					instCount = groupSize;
				}
			}

			//add render task
			if (!pTask || !(pInstGroup->CanShareRenderBufferWith(pLastInstGroup)))
			{
				pTask = BlockRenderTask::CreateTask();
				pTask->Init(pTemplate, nBlockData, vertexOffset, pChunk->m_minBlockId_ws, nMemoryBufferIndex);
				m_builder_tasks.push_back(pTask);
				pLastInstGroup = pInstGroup;
			}

			int32 batchInstCount = 0;
			int32 unprocessedInstCount = groupSize;
			for (int inst = 0; inst < (int)groupSize; inst++)
			{
				//start a new one if instances can't fit into one batch
				batchInstCount++;
				if (nFreeFaceCountInVertexBuffer < nMaxFaceCountPerInstance)
				{
					memoryBuffer.Unlock();
					nFreeFaceCountInVertexBuffer = Math::Min(maxFaceCountPerBatch, m_totalFaceCount - nFaceCountCompleted);
					memoryBuffer = RequestMemoryBuffer(nFreeFaceCountInVertexBuffer, &nMemoryBufferIndex);
					memoryBuffer.Lock((void**)&pVertices);
					vertexOffset = 0;

					if (nFreeFaceCountInVertexBuffer < unprocessedInstCount*nMaxFaceCountPerInstance)
					{
						instCount = nFreeFaceCountInVertexBuffer / nMaxFaceCountPerInstance;
					}
					else
					{
						instCount = unprocessedInstCount;
					}
					pTask = BlockRenderTask::CreateTask();
					pTask->Init(pTemplate, nBlockData, vertexOffset, pChunk->m_minBlockId_ws, nMemoryBufferIndex);
					m_builder_tasks.push_back(pTask);
					pLastInstGroup = pInstGroup;

					batchInstCount = 1;
				}

				//--------------------------------------------------------------
				// assemble block model data
				//--------------------------------------------------------------
				BlockVertexCompressed* pBlockModelVertices = NULL;
				unprocessedInstCount--;
				int32 nFaceCount = tessellator.TessellateBlock(pChunk, instanceGroup[inst], dwShaderID, &pBlockModelVertices);
				if (nFaceCount > 0)
				{
					int32 nVertexCount = nFaceCount * 4;
					if (nFreeFaceCountInVertexBuffer >= nFaceCount)
					{
						memcpy(pVertices, pBlockModelVertices, sizeof(BlockVertexCompressed)*nVertexCount);
						pVertices += nVertexCount;
						vertexOffset += nVertexCount;

						nFaceCountCompleted += nFaceCount;
						pTask->AddRectFace(nFaceCount);
						nFreeFaceCountInVertexBuffer -= nFaceCount;
					}
					else
					{
						// this could happen when block changes when we are still processing it. 
						OUTPUT_LOG("fatal error: not enough face count in vertex buffer. \n");
					}
				}
				CHECK_YIELD_CPU_TO_WRITER;
			}
		}
		memoryBuffer.Unlock();
		if (pnCpuYieldCount)
			*pnCpuYieldCount = nCpuYieldCount;
	}
	
	ParaMemoryBuffer RenderableChunk::RequestMemoryBuffer(int32 nFaceCountInVertexBuffer, int32* pBufferIndex)
	{
		ParaMemoryBuffer memBuffer;
		if (memBuffer.CreateBuffer(nFaceCountInVertexBuffer*sizeof(BlockVertexCompressed) * 4))
		{
			if (pBufferIndex)
				*pBufferIndex = m_memoryBuffers.size();
			m_memoryBuffers.push_back(memBuffer);
		}
		else
		{
			OUTPUT_LOG("warn: failed to RequestMemoryBuffer of size %d for renderable chunk\n", nFaceCountInVertexBuffer);
		}
		return memBuffer;
	}

	void RenderableChunk::UploadFromMemoryToDeviceBuffer()
	{
		ReleaseVertexBuffers();
		ClearRenderTasks();
		
		if (!m_memoryBuffers.empty())
		{
			for (ParaMemoryBuffer& memBuffer : m_memoryBuffers)
			{
				ParaVertexBuffer* pBuffer = RequestVertexBuffer(memBuffer.GetBufferSize() / (sizeof(BlockVertexCompressed) * 4));
				if (pBuffer)
					pBuffer->UploadMemoryBuffer(memBuffer.GetMemoryPointer());
			}

			m_renderTasks.clear();
			m_renderTasks.reserve(m_builder_tasks.size());
			for (BlockRenderTask* pTask : m_builder_tasks)
			{
				if ((int)m_vertexBuffers.size() > pTask->GetBufferIndex())
				{
					// transfer render task ownership from builder task to render task. 
					pTask->SetVertexBuffer(m_vertexBuffers[pTask->GetBufferIndex()]->GetDevicePointer());
					m_renderTasks.push_back(pTask);
				}
				else
				{
					BlockRenderTask::ReleaseTask(pTask);
				}
			}
			m_builder_tasks.clear();
			ClearBuilderBuffer();
		}
	}

	bool RenderableChunk::IsBuildingBuffer() const
	{
		return m_chunkBuildState == ChunkBuild_Rebuilding || m_chunkBuildState == ChunkBuild_RequestRebuild;
	}

	bool RenderableChunk::IsReadyOrEmpty() const
	{
		return m_chunkBuildState == ChunkBuild_Ready || m_chunkBuildState == ChunkBuild_empty;
	}

	Int16x3 RenderableChunk::GetChunkPosWs()
	{
		Uint16x3 curChunk;
		UnpackChunkIndex(m_packedChunkID, curChunk.x, curChunk.y, curChunk.z);
		return Int16x3(((m_regionX << 5) + curChunk.x), curChunk.y, ((m_regionZ << 5) + curChunk.z));
	}

	int32 RenderableChunk::GetDelayedRebuildTick() const
	{
		return m_nDelayedRebuildTick;
	}

	void RenderableChunk::SetDelayedRebuildTick(int32 val)
	{
		m_nDelayedRebuildTick = val;
	}

	int16 RenderableChunk::GetChunkViewDistance() const
	{
		return m_nChunkViewDistance;
	}

	void RenderableChunk::SetChunkViewDistance(int16 val)
	{
		m_nChunkViewDistance = val;
	}

	int16 RenderableChunk::GetViewIndex() const
	{
		return m_nViewIndex;
	}

	void RenderableChunk::SetViewIndex(int16 val)
	{
		m_nViewIndex = val;
	}

	void RenderableChunk::SortAndMergeInstanceGroupsByTexture()
	{
		std::vector<InstanceGroup* >& instanceGroups = GetInstanceGroups();
		auto itEnd = std::find_if(instanceGroups.begin(), instanceGroups.end(), [](InstanceGroup * pInst){
			return pInst->GetFaceCount() == 0;
		});
		// sort by id and then by texture and then by face count. 
		std::sort(instanceGroups.begin(), itEnd, [](InstanceGroup* l, InstanceGroup* r){
			if (l->m_pTemplate != r->m_pTemplate)
			{
				int nOrder1 = l->m_pTemplate->GetRenderPriority();
				int nOrder2 = r->m_pTemplate->GetRenderPriority();
				if (nOrder1 != nOrder2)
					return nOrder1 < nOrder2;
				else
				{
					return l->m_pTemplate->GetID() < r->m_pTemplate->GetID();
				}
			}
			else
			{
				return l->m_blockData < r->m_blockData;
			}
		});
		
		/* not needed any more, since we are already merging it during render task rebuild.
		// merge groups with identical textures. 
		int nSize = (int)m_instanceGroups.size() - 1;
		for (int i = 0; i < nSize && m_instanceGroups[i]->GetFaceCount()>0; i++)
		{
			InstanceGroup* curInstance = m_instanceGroups[i];
			InstanceGroup* nextInstance = m_instanceGroups[i + 1];
			if (nextInstance->GetFaceCount() > 0)
			{
				if (curInstance->m_pTemplate == nextInstance->m_pTemplate &&
					curInstance->m_pTemplate->GetBlockModelByData(curInstance->m_blockData).GetTextureIndex() == nextInstance->m_pTemplate->GetBlockModelByData(nextInstance->m_blockData).GetTextureIndex())
				{
					// now merge the two instance group. 
					// use the block data with larger face count for buffer size estimation. 
					curInstance->m_blockData = nextInstance->m_blockData;
					(*curInstance) += (*nextInstance);
					nextInstance->reset();
					for (int j = i + 1; j < nSize; j++)
					{
						m_instanceGroups[j] = m_instanceGroups[j + 1];
						m_instanceGroups[j + 1] = nextInstance;
					}
					i--;
				}
			}
		}
		*/
	}

	int RenderableChunk::GetTotalRenderableChunks()
	{
		return s_nTotalRenderableChunks;
	}

	std::vector<BlockRenderTask*> RenderableChunk::GetRenderTasks()
	{
		return m_renderTasks;
	}

	const CShapeBox& RenderableChunk::GetShapeAABB() const
	{
		return m_pShapeAABB;
	}

	int RenderableChunk::GetShaderID() const
	{
		return (m_dwShaderID < 0) ? m_pWorld->GetBlockRenderMethod() : m_dwShaderID;
	}

	void RenderableChunk::SetShaderID(int val)
	{
		m_dwShaderID = val;
	}

	bool RenderableChunk::IsMainRenderer() const
	{
		return m_bIsMainRenderer;
	}

	void RenderableChunk::SetIsMainRenderer(bool val)
	{
		m_bIsMainRenderer = val;
	}

	void RenderableChunk::ClearChunkData()
	{
		SetChunkDirty(true);
		m_nDelayedRebuildTick = 0;

		if (!IsBuildingBuffer())
		{
			// clear all buffers
			ClearRenderTasks();
			ClearBuilderBuffer();
		}
		else
		{
			OUTPUT_LOG("warn: chunk is rebuilding when clearing it\n");
		}
		ReleaseVertexBuffers();
		m_chunkBuildState = ChunkBuild_empty;
	}

	int RenderableChunk::GetRenderFrameCount() const
	{
		return m_nRenderFrameCount;
	}

	void RenderableChunk::SetRenderFrameCount(int val)
	{
		m_nRenderFrameCount = val;
	}

	int RenderableChunk::GetVertexBufferBytes()
	{
		int nTotalBytes = 0;
		for (auto vertexBuffer : m_vertexBuffers)
		{
			nTotalBytes += (int)vertexBuffer->GetBufferSize();
		}
		return nTotalBytes;
	}

	int RenderableChunk::GetLastBufferBytes()
	{
		int nTotalBytes = GetVertexBufferBytes();
		if (nTotalBytes > 0)
		{
			m_nLastVertexBufferBytes = nTotalBytes;
		}
		return m_nLastVertexBufferBytes;
	}

	bool RenderableChunk::InstanceGroup::CanShareRenderBufferWith(InstanceGroup* pOther /*= NULL*/)
	{
		if (pOther == NULL)
			return false;
		else
		{
			if (m_pTemplate->GetRenderPass() != pOther->m_pTemplate->GetRenderPass())
				return false;
			else
			{
				// TODO: further test textures and categories, etc. 
				return (m_pTemplate->GetTexture0(m_blockData) == pOther->m_pTemplate->GetTexture0(pOther->m_blockData))
					&& (m_pTemplate->GetNormalMap() == pOther->m_pTemplate->GetNormalMap());
			}
		}
	}

	
}




```