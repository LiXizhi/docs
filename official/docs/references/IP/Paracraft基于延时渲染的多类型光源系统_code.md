```lua

--[[
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/EditLight/EditLightTask.lua");
local EditLightTask = commonlib.gettable("MyCompany.Aries.Game.Tasks.EditLightTask");
local task = EditLightTask:new();
task:Run();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/UndoManager.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/CreateBlockTask.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/DestroyBlockTask.lua");
NPL.load("(gl)script/ide/math/vector.lua");
NPL.load("(gl)script/ide/System/Windows/Keyboard.lua");
NPL.load("(gl)script/ide/System/Util/Binding/Bindings.lua");
local Binding = commonlib.gettable("System.Util.Binding");
local Keyboard = commonlib.gettable("System.Windows.Keyboard");
local UndoManager = commonlib.gettable("MyCompany.Aries.Game.UndoManager");
local vector3d = commonlib.gettable("mathlib.vector3d");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local EditLightTask = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Task"), commonlib.gettable("MyCompany.Aries.Game.Tasks.EditLightTask"));

local curInstance;
local light;

-- this is always a top level task. 
EditLightTask.is_top_level = true;

function EditLightTask:ctor()
end

local page;
function EditLightTask.InitPage(Page)
	page = Page;
end

-- get current instance
function EditLightTask.GetInstance()
	return curInstance;
end

function EditLightTask:Run()
	curInstance = self;

	self:LoadSceneContext();
	self:GetSceneContext():setMouseTracking(true);
	self:GetSceneContext():setCaptureMouse(true);
end

function EditLightTask:OnExit()
	self:ShowPage(false);

	self:SetFinished();
	self:UnloadSceneContext();
	self:CloseWindow();

	curInstance = nil;
	light = nil;
end

function EditLightTask:RefreshPage()
	if(page) then
		page:Refresh(0.01);
	end
end

function EditLightTask:UpdateManipulators()
	self:DeleteManipulators();

	if(light) then
		local x, y, z = light:GetPosition();

		NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/EditLight/EditLightModelManipContainer.lua");
		local EditLightModelManipContainer = commonlib.gettable("MyCompany.Aries.Game.Manipulators.EditLightModelManipContainer");
		local lightModelManipCont = EditLightModelManipContainer:new();
		lightModelManipCont:init(light);

		self:AddManipulator(lightModelManipCont);
		lightModelManipCont:connectToDependNode(light);

		NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/EditLight/EditLightManipContainer.lua");
		local EditLightManipContainer = commonlib.gettable("MyCompany.Aries.Game.Manipulators.EditLightManipContainer");
		local manipCont = EditLightManipContainer:new();
		manipCont:init(light);

		self:AddManipulator(manipCont);
		manipCont:connectToDependNode(light);

		self:RefreshPage();
	end
end

function EditLightTask:Redo()
end

function EditLightTask:Undo()
end

function EditLightTask:ShowPage(bShow)
	if(not page) then
		local width,height = 200, 600;
		local params = {
				url = "script/apps/Aries/Creator/Game/Tasks/EditLight/EditLightTask.html", 
				name = "EditLightTask.ShowPage", 
				isShowTitleBar = false,
				DestroyOnClose = true,
				bToggleShowHide=false, 
				style = CommonCtrl.WindowFrame.ContainerStyle,
				allowDrag = true,
				enable_esc_key = false,
				bShow = bShow,
				click_through = false, 
				app_key = MyCompany.Aries.Creator.Game.Desktop.App.app_key, 
				directPosition = true,
					align = "_lt",
					x = 0,
					y = 60,
					width = width,
					height = height,
			};
		System.App.Commands.Call("File.MCMLWindowFrame", params);
		if(params._page) then
			params._page.OnClose = function()
				page = nil;
			end
		end
	else
		if(bShow == false) then
			page:CloseWindow();
		else
			page:Refresh(0.1);
		end
	end
end

function EditLightTask:GetSelectedLight()
	return light;
end

function EditLightTask:SelectLight(entityLight)
	self:ShowPage(true);

	if(light~=entityLight) then
		if(light) then
			light:Disconnect("valueChanged", EditLightTask, EditLightTask.OnLightValueChange);	
		end

		light = entityLight;
		light:Connect("valueChanged", EditLightTask, EditLightTask.OnLightValueChange, "UniqueConnection");

		self.UpdatePageFromLight();
		self:UpdateManipulators();
	end
end

function EditLightTask.OnLightValueChange()
	local self = EditLightTask.GetInstance();
	self:UpdatePageFromLight();
end


function EditLightTask:PickLightAtMouse(result)
	local result = result or Game.SelectionManager:MousePickBlock(true, true, false);
	if(result.blockX) then
		local x,y,z = result.blockX,result.blockY,result.blockZ;
		local lightEntity = BlockEngine:GetBlockEntity(x,y,z) or result.entity;
		if(lightEntity and lightEntity:isa(EntityManager.EntityLight)) then
			return lightEntity;
		end
	end
end

function EditLightTask.CancelSelection()
	local self = EditLightTask.GetInstance();

	self:ShowPage(false);
	self:DeleteManipulators();
	if(light) then
		light:Disconnect("valueChanged", EditLightTask, EditLightTask.OnLightValueChange);	
		light = nil;
	end
end

function EditLightTask:handleLeftClickScene(event, result)
	local lightEntity = self:PickLightAtMouse();
	if(lightEntity) then
		self:SelectLight(lightEntity);
	else
		EditLightTask.CancelSelection()
	end
end

function EditLightTask:handleRightClickScene(event, result)
	if(not GameLogic.GameMode:IsEditor()) then
		return;
	end

	local result = result or Game.SelectionManager:MousePickBlock(true, false, false);
	local x,y,z = BlockEngine:GetBlockIndexBySide(result.blockX, result.blockY, result.blockZ, result.side);

	local task = MyCompany.Aries.Game.Tasks.CreateBlock:new({blockX = x, blockY = y, blockZ = z, entityPlayer = EntityManager.GetPlayer(), block_id = 264, side = result.side, from_block_id = result.block_id, side_region=side_region })
	task:Run();
end

function EditLightTask:mouseMoveEvent(event)
	self:GetSceneContext():mouseMoveEvent(event);
end

function EditLightTask:mouseWheelEvent(event)
	self:GetSceneContext():mouseWheelEvent(event);
end

function EditLightTask:keyPressEvent(event)
	local dik_key = event.keyname;
	if(dik_key == "DIK_Z")then
		UndoManager.Undo();
	elseif(dik_key == "DIK_Y")then
		UndoManager.Redo();
	end
	self:GetSceneContext():keyPressEvent(event);
end

function EditLightTask:SetItemInHand(itemStack)
	self.itemInHand = itemStack;
end

function EditLightTask:GetModelFileInHand()
	if(self.itemInHand) then
		return self.itemInHand:GetDataField("tooltip");
	end
end

function EditLightTask:UpdateValueToPage()
	self:RefreshPage()
end

function EditLightTask:UpdatePageFromLight()
	local self = EditLightTask.GetInstance();
	if(self and page) then
		if(light) then
			local lightModel = light:GetField("modelFilepath", "");
			page:SetValue("modelFilepath", string.gsub(lightModel, ".*/", ""));

			Binding.NumberToString(light, "LightType", 0, page, "LightType", "0", nil, "int");

			Binding.PosVec3ToString(light, "Diffuse", {1, 1, 1}, page, "Diffuse", {1, 1, 1}, 0.001, "int");
			Binding.PosVec3ToString(light, "Specular", {1, 1, 1}, page, "Specular", {1, 1, 1}, 0.001, "int");
			Binding.PosVec3ToString(light, "Ambient", {1, 1, 1}, page, "Ambient", {1, 1, 1}, 0.001, "int");

			Binding.PosVec3ToString(light, "Position", {1, 1, 1}, page, "Position", {1, 1, 1}, 0.001, "float");
			Binding.XYZToString(light, "Yaw", "Pitch", "Roll", 0, page, "Rotation", "0,0,0", 0.001, "int");

			Binding.NumberToString(light, "Range", 0, page, "Range", "0", 0.001, "float");
			Binding.NumberToString(light, "Falloff", 0, page, "Falloff", "0", 0.001, "float");

			Binding.NumberToString(light, "Attenuation0", 0, page, "Attenuation0", "0", 0.001, "float");
			Binding.NumberToString(light, "Attenuation1", 0, page, "Attenuation1", "0", 0.001, "float");
			Binding.NumberToString(light, "Attenuation2", 0, page, "Attenuation2", "0", 0.001, "float");

			Binding.NumberToString(light, "Theta", 0, page, "Theta", "0", 0.001, "int");
			Binding.NumberToString(light, "Phi", 0, page, "Phi", "0", 0.001, "int");
		else
			page:SetValue("modelFilepath", "")
			page:SetValue("LightType", "")
			page:SetValue("Diffuse", "")
			page:SetValue("Specular", "")
			page:SetValue("Ambient", "")
			page:SetValue("Position", "")
			page:SetValue("Rotation", "")
			page:SetValue("Range", "")
			page:SetValue("Falloff", "")
			page:SetValue("Attenuation0", "")
			page:SetValue("Attenuation1", "")
			page:SetValue("Attenuation2", "")
			page:SetValue("Theta", "")
			page:SetValue("Phi", "")
		end
	end
end

function EditLightTask.ChangeLightModel()
	local self = EditLightTask.GetInstance();
	if(self and page and light) then
		local local_filename = light:GetField("modelFilepath", "");

		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/OpenAssetFileDialog.lua");
		local OpenAssetFileDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.OpenAssetFileDialog");
		OpenAssetFileDialog.ShowPage(
			L"请输入bmax, x或fbx文件的相对路径, <br/>你也可以随时将外部文件拖入窗口中",
			function(result)
				if(result and result~="" and result~=local_filename) then
					light:SetField("modelFilepath", result);
				end
			end,
			local_filename,
			L"选择模型文件",
			"model",
			nil,
			nil
		)
	end
end

function EditLightTask.ChangeLightType()
	local self = EditLightTask.GetInstance();
	if(self and page and light) then
		Binding.StringToNumber(page, "LightType", "0", light, "LightType", 0, nil, "int");
		self:UpdateManipulators();
	end
end

function EditLightTask.ChangeDiffuseColor(r, g, b)
	local color = {r, g, b};

	if light then
		light:SetField("Diffuse", color)
	end
end

function EditLightTask.ChangeSpecularColor(r, g, b)
	local color = {r, g, b};

	if light then
		light:SetField("Specular", color)
	end
end

function EditLightTask.ChangeAmbientColor(r, g, b)
	local color = {r, g, b};

	if light then
		light:SetField("Ambient", color)
	end
end

function EditLightTask.UpdateLightFromPage()
	local self = EditLightTask.GetInstance();
	if(self and page and light) then
		Binding.StringToPosVec3(page, "Position", {1, 1, 1}, light, "Position",  {1, 1, 1}, 0.001, "float");
		Binding.StringToXYZ(page, "Rotation", "0,0,0", light, "Yaw", "Pitch", "Roll", 0, 0.001, "int");

		Binding.StringToNumber(page, "Range", "0", light, "Range", 0, 0.001, "float");
		Binding.StringToNumber(page, "Falloff", "0", light, "Falloff", 0, 0.001, "float");

		Binding.StringToNumber(page, "Attenuation0", "0", light, "Attenuation0", 0, 0.001, "float");
		Binding.StringToNumber(page, "Attenuation1", "0", light, "Attenuation1", 0, 0.001, "float");
		Binding.StringToNumber(page, "Attenuation2", "0", light, "Attenuation2", 0, 0.001, "float");

		Binding.StringToNumber(page, "Theta", "0", light, "Theta", 0, 0.001, "int");
		Binding.StringToNumber(page, "Phi", "0", light, "Phi", 0, 0.001, "int");
	end
end


--[[
Title: EntityLight
Author(s): LiXizhi
Date: 2016/9/21
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Entity/EntityLight.lua");
local EntityLight = commonlib.gettable("MyCompany.Aries.Game.EntityManager.EntityLight")
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Entity/EntityBlockBase.lua");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local Entity = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.EntityManager.EntityBlockBase"), commonlib.gettable("MyCompany.Aries.Game.EntityManager.EntityLight"));

-- light properties
Entity:Property({"LightType", 1});

Entity:Property({"Diffuse", {0, 0, 0}});
Entity:Property({"Specular", {0, 0, 0}});
Entity:Property({"Ambient", {0, 0, 0}});

Entity:Property({"Position", {0, 0, 0}});
Entity:Property({"Direction", {0, 0, 0}});

Entity:Property({"Yaw", 0});
Entity:Property({"Pitch", 0});
Entity:Property({"Roll", 0});

Entity:Property({"Range", 1});
Entity:Property({"Falloff", 0});

Entity:Property({"Attenuation0", 1});
Entity:Property({"Attenuation1", 1});
Entity:Property({"Attenuation2", 1});

Entity:Property({"Theta", 0});
Entity:Property({"Phi", 0});

-- light model properties
Entity:Property({"modelInitPos", {0,0,0}});
Entity:Property({"modelOffsetPos", {0,0,0}});
Entity:Property({"modelScale", 1});
Entity:Property({"modelYaw", 0});
Entity:Property({"modelPitch", 0});
Entity:Property({"modelRoll", 0});
Entity:Property({"modelFilepath", ""});

-- class name
Entity.class_name = "EntityLight";
EntityManager.RegisterEntityClass(Entity.class_name, Entity);
Entity.is_persistent = true;
-- always serialize to 512*512 regional entity file
Entity.is_regional = true;

function Entity:ctor()
	self.modelInitPos = {0, 0, 0};
	self.modelOffsetPos = {0, 0, 0};
	self.modelFilepath = "model/blockworld/BlockModel/block_model_one.x";
end

function Entity:init()
	if(not Entity._super.init(self)) then
		return
	end
	self:CreateInnerObject();
	return self;
end

function Entity:isPointLight()
	local t = self:GetField("LightType");
	return t == 1;
end

function Entity:isSpotLight()
	local t = self:GetField("LightType");
	return t == 2;
end

function Entity:isDirectionalLight()
	local t = self:GetField("LightType");
	return t == 3;
end

function Entity:SetOffsetPos(offset)
	local p = self:GetField("modelInitPos");
	local x, y, z = p[1], p[2], p[3];

	offset[1] = math.min(math.max(-BlockEngine.half_blocksize, offset[1]), BlockEngine.half_blocksize);
	offset[2] = math.min(math.max(0, offset[2]), BlockEngine.blocksize);
	offset[3] = math.min(math.max(-BlockEngine.half_blocksize, offset[3]), BlockEngine.half_blocksize);
	self.modelOffsetPos = offset;

	local lightModel = self.lightModel;
	if(lightModel) then
		lightModel:SetPosition(x + offset[1], y + offset[2], z + offset[3]);
	end
	self:valueChanged();
end

function Entity:Clamp(v, min, max)
	if v < min then
		return min;
	end
	if v > max then
		return max;
	end
	return v;
end

function Entity:GetField(field, default_value)
	-- hand light model properties first
	if field == "modelInitPos" then
		return self.modelInitPos
	end
	if field == "modelOffsetPos" then
		return self.modelOffsetPos
	end
	if field == "modelScale" then
		return self.modelScale or 1
	end
	if field == "modelYaw" then
		return self.modelYaw or 0
	end
	if field == "modelPitch" then
		return self.modelPitch or 0
	end
	if field == "modelRoll" then
		return self.modelRoll or 0
	end
	if field == "modelFilepath" then
		return self.modelFilepath
	end

	-- properties belong to the C++ world's light object
	default_value = 0;
	if field == "Position" or
	   field == "Direction" or
	   field == "Diffuse" or
	   field == "Specular" or
	   field == "Ambient" then
		default_value = {0, 0, 0};
	end

	local lightObject = self:GetInnerObject();

	local value = lightObject:GetField(field, default_value);

	-- radian to degree
	if field == "Yaw"   or 
	   field == "Pitch" or 
	   field == "Roll"  or 
	   field == "Theta" or 
	   field == "Phi"   then
		value = value * 180 / 3.14;
	end

	-- color from float(0.f - 1.f) to int(0 - 255) 
	if field == "Diffuse" or
	   field == "Specular" or
	   field == "Ambient" then
		value = {
				self:Clamp(value[1] * 255, 0, 255),
				self:Clamp(value[2] * 255, 0, 255),
				self:Clamp(value[3] * 255, 0, 255),
				}
	end

	return value;
end

function Entity:SetField(field, value)
	local oldValue = self:GetField(field);

	-- ATTENTION: skip approximate values, because the multiple manips update values to plugs asynchronously
	if(type(oldValue) == "table") then
		if(commonlib.partialcompare(oldValue, value, 0.01)) then
			return;
		end
	elseif(type(oldValue) == "number") then
		if(math.abs(oldValue - value) < 0.01) then
			return;
		end
	end
	
	-- handle light model properties first
	if field == "modelOffsetPos" then
		self:SetOffsetPos(value)
		return;
	end
	if field == "modelScale" then
		self.modelScale = value

		local lightModel = self.lightModel;
		if(lightModel) then
			lightModel:SetScale(value);
		end
		self:valueChanged();

		return;
	end
	if field == "modelYaw" then
		self.modelYaw = value

		local lightModel = self.lightModel;
		if(lightModel) then
			lightModel:SetField("yaw", value);
		end
		self:valueChanged();

		return;
	end
	if field == "modelPitch" then
		self.modelPitch = value

		local lightModel = self.lightModel;
		if(lightModel) then
			lightModel:SetField("pitch", value);
		end
		self:valueChanged();

		return;
	end
	if field == "modelRoll" then
		self.modelRoll = value

		local lightModel = self.lightModel;
		if(lightModel) then
			lightModel:SetField("roll", value);
		end
		self:valueChanged();

		return;
	end
	if field == "modelFilepath" then
		self.modelFilepath = value

		local lightModel = self.lightModel;
		if(lightModel) then
			lightModel:SetField("assetfile", value);
		end
		self:valueChanged();

		return;
	end


	-- handle properties of C++ world's light object
	local lightObject = self:GetInnerObject();

	if field == "Phi" then
		if value < 0 or value > 179 then
			return;
		end

		local theta = self:GetField("Theta");
		if value < theta then
			lightObject:SetField("Theta", value * 3.14 / 180);
		end
	end
	if field == "Theta" then
		if value < 0 or value > 179 then
			return;
		end

		local phi = self:GetField("Phi");
		if value > phi then
			lightObject:SetField("Phi", value * 3.14 / 180);
		end
	end

	-- degree to radian
	if field == "Yaw"   or 
	   field == "Pitch" or 
	   field == "Roll" or 
	   field == "Theta" or 
	   field == "Phi"  then
		value = value * 3.14 / 180;
	end

	-- color from int(0 - 255) to float(0.f - 1.f)
	if field == "Diffuse" or
	   field == "Specular" or
	   field == "Ambient" then
		value = {
				self:Clamp(value[1] / 255, 0, 1),
				self:Clamp(value[2] / 255, 0, 1),
				self:Clamp(value[3] / 255, 0, 1),
				}
	end

	local result = lightObject:SetField(field, value);

	self:valueChanged();

	return result;
end

function Entity:CreateInnerObject()
	local x, y, z = self:GetPosition();

	local lightObject = ParaScene.CreateObject("CLightObject", self:GetBlockEntityName(), x,y,z);

	lightObject:SetAttribute(0x8000, true);
	lightObject:SetField("RenderDistance", 100);
	lightObject:SetField("IsDeferredLightOnly", true);

	self:SetInnerObject(lightObject);
	ParaScene.Attach(lightObject);


	local lightModel = ParaScene.CreateObject("BMaxObject", self:GetBlockEntityName(), x,y,z);

	lightModel:SetField("assetfile", self.modelFilepath);
	lightModel:SetAttribute(0x8080, true);
	lightModel:SetField("RenderDistance", 100);

	self.lightModel = lightModel;
	ParaScene.Attach(lightModel);

	self.modelInitPos = {x,y,z};

	return lightObject;
end

function Entity:Destroy()
	ParaScene.Delete(self.lightModel);

	self:DestroyInnerObject();
	Entity._super.Destroy(self);
end

function Entity:LoadFromXMLNode(node)
	Entity._super.LoadFromXMLNode(self, node);
	local attr = node.attr;
	if(attr) then
	end
end

function Entity:SaveToXMLNode(node, bSort)
	node = Entity._super.SaveToXMLNode(self, node, bSort);
	return node;
end

--[[
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/EditLight/EditLightManipContainer.lua");
local EditLightManipContainer = commonlib.gettable("MyCompany.Aries.Game.Manipulators.EditLightManipContainer");
local manipCont = EditLightManipContainer:new();
manipCont:init();
self:AddManipulator(manipCont);
manipCont:connectToDependNode(entity);
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Scene/Manipulators/ManipContainer.lua");
local Color = commonlib.gettable("System.Core.Color");
local Plane = commonlib.gettable("mathlib.Plane");
local vector3d = commonlib.gettable("mathlib.vector3d");
local ShapesDrawer = commonlib.gettable("System.Scene.Overlays.ShapesDrawer");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine");
local EditLightManipContainer = commonlib.inherit(commonlib.gettable("System.Scene.Manipulators.ManipContainer"), commonlib.gettable("MyCompany.Aries.Game.Manipulators.EditLightManipContainer"));
EditLightManipContainer:Property({"Name", "EditLightManipContainer", auto=true});
EditLightManipContainer:Property({"PenWidth", 0.01});
EditLightManipContainer:Property({"showGrid", true, "IsShowGrid", "SetShowGrid", auto=true});
EditLightManipContainer:Property({"mainColor", "#ffff00"});

function EditLightManipContainer:ctor()
	self:AddValue("position", {0,0,0});
end

function EditLightManipContainer:init(node)
	self.node = node;
	EditLightManipContainer._super.init(self);
	return self;
end

function EditLightManipContainer:createChildren()
	self.translateManip = self:AddTranslateManip();
	self.translateManip:SetFixOrigin(true);
	self.translateManip:SetRealTimeUpdate(false);
	self.translateManip:SetUpdatePosition(false);

	if self.node:isPointLight() or self.node:isSpotLight() then
		self.scaleManip = self:AddScaleManip();
		self.scaleManip:SetRealTimeUpdate(true);
		self.scaleManip.radius = 0.7;
		self.scaleManip:SetUniformScaling(true);
	end

	if self.node:isSpotLight() or self.node:isDirectionalLight() then
		self.rotateManip = self:AddRotateManip();
		self.rotateManip:SetRealTimeUpdate(true);
		self.rotateManip.radius = 1.2;
		self.rotateManip:SetYawPitchRollMode(true);
		self.rotateManip:SetYawEnabled(true);
		self.rotateManip:SetPitchEnabled(true);
		self.rotateManip:SetRollEnabled(true);
	end

	if self.node:isSpotLight() then
		self.thetaManip = self:AddRotateManip();
		self.thetaManip:SetRealTimeUpdate(true);
		self.thetaManip.radius = 0.4;
		self.thetaManip.yColor = "#ffffff";
		self.thetaManip:SetYawPitchRollMode(true);
		self.thetaManip:SetYawEnabled(true);
		self.thetaManip:SetPitchEnabled(false);
		self.thetaManip:SetRollEnabled(false);

		self.phiManip = self:AddRotateManip();
		self.phiManip:SetRealTimeUpdate(true);
		self.phiManip.radius = 0.7;
		self.phiManip.yColor = "#666666";
		self.phiManip:SetYawPitchRollMode(true);
		self.phiManip:SetYawEnabled(true);
		self.phiManip:SetPitchEnabled(false);
		self.phiManip:SetRollEnabled(false);
	end
end

function EditLightManipContainer:paintEvent(painter)
	EditLightManipContainer._super.paintEvent(self, painter);
	self.pen.width = self.PenWidth;
	painter:SetPen(self.pen);

	local node = self.node;
	if node then
		local nodeRangePlug = node:findPlug("Range");
		local range = nodeRangePlug:GetValue();

		local nodeDirPlug = node:findPlug("Direction");
		local dir = nodeDirPlug:GetValue();

		local nodePosPlug = node:findPlug("Position");
		local worldPos = nodePosPlug:GetValue();
		local camx,camy,camz = ParaCamera.GetPosition();
		local toCam = {camx - worldPos[1], camy - worldPos[2] - 0.5, camz - worldPos[3]}

		-- yellow color
		self:SetColorAndName(painter, "#ffff00");
		-- draw sphere edge facing to camera
		if self.node:isPointLight() then
			ShapesDrawer.DrawCircleEdge(painter, range, toCam[1], toCam[2], toCam[3], 0, 0, 0);
		end

		-- draw directional line
		if self.node:isSpotLight() or self.node:isDirectionalLight() then
			ShapesDrawer.DrawLine(painter, 0, 0, 0, dir[1] * range, dir[2] * range, dir[3] * range);
		end

		-- draw cone edge
		if self.node:isSpotLight() then
			local nodeThetaPlug = node:findPlug("Theta");
			local nodePhiPlug = node:findPlug("Phi");
			local theta = nodeThetaPlug:GetValue();
			local phi = nodePhiPlug:GetValue();
			theta = theta * 3.14 / 180;
			phi = phi * 3.14 / 180;

			local dirVec = vector3d:new(dir);
			local toCamVec = vector3d:new(toCam);
			local normal = toCamVec:cross(dirVec);
			normal:normalize();

			-- theta edge
			local sin_half_theta = math.sin(theta/2);
			local cos_half_theta = math.cos(theta/2);

			local first_edge = (dirVec * cos_half_theta + normal * sin_half_theta) * range;
			local second_edge = (dirVec * cos_half_theta - normal * sin_half_theta) * range;

			self:SetColorAndName(painter, "#ffffff");
			ShapesDrawer.DrawLine(painter, 0, 0, 0, first_edge[1], first_edge[2], first_edge[3]);
			ShapesDrawer.DrawLine(painter, 0, 0, 0, second_edge[1], second_edge[2], second_edge[3]);

			self:SetColorAndName(painter, "#ffff00");
			-- draw cone bottom circle of theta
			ShapesDrawer.DrawCircleEdge(painter, range * sin_half_theta, dir[1], dir[2], dir[3], dir[1] * cos_half_theta * range, dir[2] * cos_half_theta * range, dir[3] * cos_half_theta * range)

			-- phi edge
			local sin_half_phi = math.sin(phi/2);
			local cos_half_phi = math.cos(phi/2);

			local first_edge = (dirVec * cos_half_phi + normal * sin_half_phi) * range;
			local second_edge = (dirVec * cos_half_phi - normal * sin_half_phi) * range;

			self:SetColorAndName(painter, "#666666");
			ShapesDrawer.DrawLine(painter, 0, 0, 0, first_edge[1], first_edge[2], first_edge[3]);
			ShapesDrawer.DrawLine(painter, 0, 0, 0, second_edge[1], second_edge[2], second_edge[3]);

			self:SetColorAndName(painter, "#ffff00");
			-- draw cone bottom circle of phi
			ShapesDrawer.DrawCircleEdge(painter, range * sin_half_phi, dir[1], dir[2], dir[3], dir[1] * cos_half_phi * range, dir[2] * cos_half_phi * range, dir[3] * cos_half_phi * range)
		end
	end

end

function EditLightManipContainer:OnValueChange(name, value)
	EditLightManipContainer._super.OnValueChange(self);
	if(name == "position") then
		self:SetPosition(unpack(value));
	end
end

function EditLightManipContainer:connectToDependNode(node)
	self.node = node;

	local nodePosPlug = node:findPlug("Position");
	local parentManipPosPlug = self:findPlug("position");
	self:addPlugToManipConversionCallback(parentManipPosPlug, function(self, manipPlug)
		local p = nodePosPlug:GetValue();
		return {p[1], p[2]+0.5, p[3]};
	end);

	-- ATTENTION: trick part about position
	local manipPosPlug = self.translateManip:findPlug("position");

	self:addManipToPlugConversionCallback(nodePosPlug, function(self, nodePlug)
		local pos = nodePosPlug:GetValue();
		local offsetPos = manipPosPlug:GetValue();
		self.translateManip:SetField("position", {0, 0, 0});
		return {pos[1]+offsetPos[1], pos[2]+offsetPos[2], pos[3]+offsetPos[3]};
	end);


	if self.node:isPointLight() or self.node:isSpotLight() then
		local nodeRangePlug = node:findPlug("Range");
		local manipScalePlug = self.scaleManip:findPlug("scaling");

		self:addManipToPlugConversionCallback(nodeRangePlug, function(self, plug)
			return manipScalePlug:GetValue()[1] or 1;
		end);
		self:addPlugToManipConversionCallback(manipScalePlug, function(self, manipPlug)
			local scaling = nodeRangePlug:GetValue() or 1;
			if(type(scaling) == "number") then
				scaling = {scaling, scaling, scaling};
			end
			return scaling;
		end);
	end
	

	local degToRad = function(deg)
		return deg * 3.14 / 180;
	end
	local radToDeg = function(rad)
		return rad * 180 / 3.14;
	end

	if self.node:isSpotLight() or self.node:isDirectionalLight() then
		local nodeYawPlug = node:findPlug("Yaw");
		local manipYawPlug = self.rotateManip:findPlug("yaw");

		self:addManipToPlugConversionCallback(nodeYawPlug, function(self, plug)
			return radToDeg(manipYawPlug:GetValue() or 0);
		end);
		self:addPlugToManipConversionCallback(manipYawPlug, function(self, manipPlug)
			return degToRad(nodeYawPlug:GetValue() or 0);
		end);

		local nodePitchPlug = node:findPlug("Pitch");
		local manipPitchPlug = self.rotateManip:findPlug("pitch");

		self:addManipToPlugConversionCallback(nodePitchPlug, function(self, plug)
			return radToDeg(manipPitchPlug:GetValue() or 0);
		end);
		self:addPlugToManipConversionCallback(manipPitchPlug, function(self, manipPlug)
			return degToRad(nodePitchPlug:GetValue() or 0);
		end);

		local nodeRollPlug = node:findPlug("Roll");
		local manipRollPlug = self.rotateManip:findPlug("roll");

		self:addManipToPlugConversionCallback(nodeRollPlug, function(self, plug)
			return radToDeg(manipRollPlug:GetValue() or 0);
		end);
		self:addPlugToManipConversionCallback(manipRollPlug, function(self, manipPlug)
			return degToRad(nodeRollPlug:GetValue() or 0);
		end);
	end

	if self.node:isSpotLight() then
		local nodeThetaPlug = node:findPlug("Theta");
		local manipThetaPlug = self.thetaManip:findPlug("yaw");

		self:addManipToPlugConversionCallback(nodeThetaPlug, function(self, plug)
			return radToDeg(manipThetaPlug:GetValue() or 0);
		end);
		self:addPlugToManipConversionCallback(manipThetaPlug, function(self, manipPlug)
			return degToRad(nodeThetaPlug:GetValue() or 0);
		end);

		local nodePhiPlug = node:findPlug("Phi");
		local manipPhiPlug = self.phiManip:findPlug("yaw");

		self:addManipToPlugConversionCallback(nodePhiPlug, function(self, plug)
			return radToDeg(manipPhiPlug:GetValue() or 0);
		end);
		self:addPlugToManipConversionCallback(manipPhiPlug, function(self, manipPlug)
			return degToRad(nodePhiPlug:GetValue() or 0);
		end);
	end

	self:finishAddingManips();
	EditLightManipContainer._super.connectToDependNode(self, node);
end



```


```hlsl

// Spot light

float ViewAspect;
float TanHalfFOV;
float2 screenParam;

float4x4 matWorld;
float4x4 matView;
float4x4 matProj;


float4 light_diffuse;
float4 light_specular;
float4 light_ambient;

float3 light_position;
float3 light_direction;

float light_range;
float light_falloff;

float light_attenuation0;
float light_attenuation1;
float light_attenuation2;

float light_theta;
float light_phi;


texture sourceTexture0;
sampler diffuseSampler : register(s0) = sampler_state
{
    Texture = <sourceTexture0>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

// TODO: specular texture surface 1

texture sourceTexture2;
sampler depthSampler : register(s2) = sampler_state
{
    Texture = <sourceTexture2>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

texture sourceTexture3;
sampler normalSampler : register(s3) = sampler_state
{
    Texture = <sourceTexture3>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};


struct VSInput
{
    float4 pos : POSITION;
};

struct VSOut
{
    float4 pos : POSITION;
    float2 texCoord : TEXCOORD0;
    float3 cameraEye : TEXCOORD1;
};

struct PSOut
{
    float4 color : COLOR0;
};

VSOut MainVS(VSInput input)
{
    VSOut output;

    float4 local_pos = input.pos;
    float4x4 matWorldViewProj = mul(mul(matWorld, matView), matProj);
    float4 proj_pos = mul(local_pos, matWorldViewProj);

    output.pos = proj_pos;

    float4 norm_proj_pos = proj_pos / proj_pos.w;
    output.cameraEye = float3(norm_proj_pos.x * TanHalfFOV * ViewAspect, norm_proj_pos.y * TanHalfFOV, 1);

    
    // -0.5, because the tex coord and proj screen coord are opposite
    // 0.5 / screenParam
    // ref https://docs.microsoft.com/en-us/windows/desktop/direct3d10/d3d10-graphics-programming-guide-resources-coordinates
    // and https://docs.microsoft.com/en-us/windows/desktop/direct3d9/directly-mapping-texels-to-pixels

    float2 texCoord = (proj_pos.xy * float2(0.5, -0.5) + float2(0.5, 0.5) * proj_pos.w) / proj_pos.w + 0.5 / screenParam;
    output.texCoord = texCoord;


    return output;
}

float dist_factor(float3 object_pos)
{
    float4 light_pos = mul(float4(light_position, 1), matView);
    float dist = distance(object_pos, light_pos.xyz / light_pos.w);

    float dist_att;
    if (dist > light_range)
    {
        dist_att = 0;
    }
    else
    {
        dist_att = 1 / (light_attenuation0 + light_attenuation1 * dist + light_attenuation2 * dist * dist);
    }

    return dist_att;
}

/*
 * diffuse: object material diffuse color
 * normal: object normal vector in camera space
 * position: object position in camera space
 */
float3 lighting(float4 diffuse, float3 normal, float3 position)
{
    float3 I_diff, I_spec, I_total;
    float3 l, v, n, h;
    float att;

    n = normalize(normal);
    v = normalize(-position);

    // FIXME: two test value
    float m_shi = 1;
    float4 m_spec = float4(1, 1, 1, 1);

    att = dist_factor(position);

    // spot light factor reference
    // https://docs.microsoft.com/en-us/windows/desktop/direct3d9/attenuation-and-spotlight-factor#spotlight-factor

    float cos_half_theta = cos(light_theta / 2);
    float cos_half_phi = cos(light_phi / 2);

    // tranform light direction from wolrd into camera space
    float4 light_dir = mul(float4(light_direction, 0), matView);
    float3 norm_light_dir = normalize(light_dir.xyz);

    float4 light_pos = mul(float4(light_position, 1), matView);
    l = normalize(light_pos.xyz / light_pos.w - position);

    // alpha is the angle between light direction vector and light-to-object vector
    float cos_alpha = dot(norm_light_dir, -l);
    float spotlight_factor;

    if (cos_alpha > cos_half_theta)
    {
        spotlight_factor = 1;
    }
    else if (cos_alpha < cos_half_phi)
    {
        spotlight_factor = 0;
    }
    else
    {
        float p = (cos_alpha - cos_half_phi) / (cos_half_theta - cos_half_phi);
        // p is always between 0 and 1, but hlsl compiler doesn't know
        // use abs() here to avoid the hlsl compiler's warning
        spotlight_factor = pow(abs(p), light_falloff);
    }

    att = att * spotlight_factor;

    I_diff = saturate(dot(l, n)) * (diffuse.xyz * light_diffuse.xyz);

    h = normalize(l + v);

    I_spec = saturate(dot(l, n)) * pow(saturate(dot(h, n)), m_shi) * (m_spec.xyz * light_specular.xyz);

    I_total = att * (I_diff + I_spec);
    return I_total;
}

PSOut MainPS(VSOut input)
{
    PSOut output;

    float2 texCoord = input.texCoord;
    float4 color = tex2D(diffuseSampler, texCoord);
    float alpha = color.a;
	
    // if the normal is world space normal value
    float4 norm = tex2D(normalSampler, texCoord);
    float4 normal_in_camera = mul(float4(norm.rgb * 2.0 - 1.0, 0), matView);
    float3 normal = normalize(normal_in_camera.xyz);

	// screen space depth value. 
    float depth = tex2D(depthSampler, texCoord).x;

    // position in camera space
    float4 position = float4(input.cameraEye * depth, 1);

    float3 total_color = color.rgb;
    total_color = total_color + lighting(color, normal.xyz, position.xyz);

    output.color = float4(total_color, alpha);

    return output;
}



struct VS1_IN
{
    float4 pos : POSITION;
};

struct VS1_OUT
{
	float4 pos : POSITION;
};

struct PS1_OUT
{
	float4 Color : COLOR0;
};

VS1_OUT VS1(VS1_IN input)
{
	VS1_OUT output;

    float4 p = input.pos;

    float4x4 matWorldViewProj = mul(mul(matWorld, matView), matProj);
    p = mul(p, matWorldViewProj);

    output.pos = p;

	return output;
}


PS1_OUT PS1(VS1_OUT input)
{
	PS1_OUT output;
    output.Color = float4(1, 0, 0, 1);

	return output;
}

technique LightVolumeMask
{
    pass FrontFace
    {
        VertexShader = compile vs_3_0 VS1();
        PixelShader = compile ps_3_0 PS1();

        ColorWriteEnable = 0;
        //ColorWriteEnable = 0xFFFFFFFF;
        ZWriteEnable = 0;
        ZFunc = LESS;
        StencilEnable = true;
        StencilFunc = ALWAYS;
        StencilZFail = REPLACE;
        StencilPass = KEEP;
        StencilRef = 1;
        StencilMask = 0xFFFFFFFF;
        CullMode = CCW;
    }
    pass BackFace
    {
        VertexShader = compile vs_3_0 MainVS();
        PixelShader = compile ps_3_0 MainPS();

        ColorWriteEnable = 0xFFFFFFFF;
        ZWriteEnable = 0;
        ZFunc = GREATEREQUAL;
        StencilEnable = true;
        StencilFunc = EQUAL;
        StencilPass = KEEP;
        StencilRef = 0;
        StencilMask = 0xFFFFFFFF;
        CullMode = CW;
    }
}


// Point light
float ViewAspect;
float TanHalfFOV;
float2 screenParam;

float4x4 matWorld;
float4x4 matView;
float4x4 matProj;


float4 light_diffuse;
float4 light_specular;
float4 light_ambient;

float3 light_position;
float3 light_direction;

float light_range;
float light_falloff;

float light_attenuation0;
float light_attenuation1;
float light_attenuation2;

float light_theta;
float light_phi;


texture sourceTexture0;
sampler diffuseSampler : register(s0) = sampler_state
{
    Texture = <sourceTexture0>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

// TODO: specular texture surface 1

texture sourceTexture2;
sampler depthSampler : register(s2) = sampler_state
{
    Texture = <sourceTexture2>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

texture sourceTexture3;
sampler normalSampler : register(s3) = sampler_state
{
    Texture = <sourceTexture3>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};


struct VSInput
{
    float4 pos : POSITION;
};

struct VSOut
{
    float4 pos : POSITION;
    float2 texCoord : TEXCOORD0;
    float3 cameraEye : TEXCOORD1;
};

struct PSOut
{
    float4 color : COLOR0;
};

VSOut MainVS(VSInput input)
{
    VSOut output;

    float4 local_pos = input.pos;
    float4x4 matWorldViewProj = mul(mul(matWorld, matView), matProj);
    float4 proj_pos = mul(local_pos, matWorldViewProj);

    output.pos = proj_pos;

    float4 norm_proj_pos = proj_pos / proj_pos.w;
    output.cameraEye = float3(norm_proj_pos.x * TanHalfFOV * ViewAspect, norm_proj_pos.y * TanHalfFOV, 1);

    
    // -0.5, because the tex coord and proj screen coord are opposite
    // 0.5 / screenParam
    // ref https://docs.microsoft.com/en-us/windows/desktop/direct3d10/d3d10-graphics-programming-guide-resources-coordinates
    // and https://docs.microsoft.com/en-us/windows/desktop/direct3d9/directly-mapping-texels-to-pixels

    float2 texCoord = (proj_pos.xy * float2(0.5, -0.5) + float2(0.5, 0.5) * proj_pos.w) / proj_pos.w + 0.5 / screenParam;
    output.texCoord = texCoord;


    return output;
}

float dist_factor(float3 object_pos)
{
    float4 light_pos = mul(float4(light_position, 1), matView);
    float dist = distance(object_pos, light_pos.xyz / light_pos.w);

    float dist_att;
    if (dist > light_range)
    {
        dist_att = 0;
    }
    else
    {
        dist_att = 1 / (light_attenuation0 + light_attenuation1 * dist + light_attenuation2 * dist * dist);
    }

    return dist_att;
}

/*
 * diffuse: object material diffuse color
 * normal: object normal vector in camera space
 * position: object position in camera space
 */
float3 lighting(float4 diffuse, float3 normal, float3 position)
{
    float3 I_diff, I_spec, I_total;
    float3 l, v, n, h;
    float att;

    n = normalize(normal);
    v = normalize(-position);

    // FIXME: two test value
    float m_shi = 1;
    float4 m_spec = float4(1, 1, 1, 1);

    att = dist_factor(position);

    float4 light_pos = mul(float4(light_position, 1), matView);
    l = normalize(light_pos.xyz / light_pos.w - position);

    I_diff = saturate(dot(l, n)) * (diffuse.xyz * light_diffuse.xyz);

    h = normalize(l + v);

    I_spec = saturate(dot(l, n)) * pow(saturate(dot(h, n)), m_shi) * (m_spec.xyz * light_specular.xyz);

    I_total = att * (I_diff + I_spec);
    return I_total;
}

PSOut MainPS(VSOut input)
{
    PSOut output;

    float2 texCoord = input.texCoord;
    float4 color = tex2D(diffuseSampler, texCoord);
    float alpha = color.a;
	
    // if the normal is world space normal value
    float4 norm = tex2D(normalSampler, texCoord);
    float4 normal_in_camera = mul(float4(norm.rgb * 2.0 - 1.0, 0), matView);
    float3 normal = normalize(normal_in_camera.xyz);

	// screen space depth value. 
    float depth = tex2D(depthSampler, texCoord).x;

    // position in camera space
    float4 position = float4(input.cameraEye * depth, 1);

    // TODO: loop the light in here
    float3 total_color = color.rgb;

        total_color = total_color + lighting(color, normal.xyz, position.xyz);

    output.color = float4(total_color, alpha);

    return output;
}






struct VS1_IN
{
    float4 pos : POSITION;
};

struct VS1_OUT
{
	float4 pos : POSITION;
};

struct PS1_OUT
{
	float4 Color : COLOR0;
};

VS1_OUT VS1(VS1_IN input)
{
	VS1_OUT output;

    float4 p = input.pos;

    float4x4 matWorldViewProj = mul(mul(matWorld, matView), matProj);
    p = mul(p, matWorldViewProj);

    output.pos = p;

	return output;
}


PS1_OUT PS1(VS1_OUT input)
{
	PS1_OUT output;
    output.Color = float4(1, 0, 0, 1);

	return output;
}

// This algorithm is inspired by
// https://kayru.org/articles/deferred-stencil/
// stencil buffer make the light shading more efficient
technique LightVolumeMask
{
    pass FrontFace
    {
        VertexShader = compile vs_3_0 VS1();
        PixelShader = compile ps_3_0 PS1();

        ColorWriteEnable = 0;
        //ColorWriteEnable = 0xFFFFFFFF;
        ZWriteEnable = 0;
        ZFunc = LESS;
        StencilEnable = true;
        StencilFunc = ALWAYS;
        StencilZFail = REPLACE;
        StencilPass = KEEP;
        StencilRef = 1;
        StencilMask = 0xFFFFFFFF;
        CullMode = CCW;
    }
    pass BackFace
    {
        VertexShader = compile vs_3_0 MainVS();
        PixelShader = compile ps_3_0 MainPS();

        ColorWriteEnable = 0xFFFFFFFF;
        ZWriteEnable = 0;
        ZFunc = GREATEREQUAL;
        StencilEnable = true;
        StencilFunc = EQUAL;
        StencilPass = KEEP;
        StencilRef = 0;
        StencilMask = 0xFFFFFFFF;
        CullMode = CW;
    }
}


// Directional light

float ViewAspect;
float TanHalfFOV;
float2 screenParam;

float4x4 matWorld;
float4x4 matView;
float4x4 matProj;

float4 light_diffuse;
float4 light_specular;
float4 light_ambient;

float3 light_position;
float3 light_direction;

float light_range;
float light_falloff;

float light_attenuation0;
float light_attenuation1;
float light_attenuation2;

float light_theta;
float light_phi;


texture sourceTexture0;
sampler diffuseSampler : register(s0) = sampler_state
{
    Texture = <sourceTexture0>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

// TODO: specular texture surface 1

texture sourceTexture2;
sampler depthSampler : register(s2) = sampler_state
{
    Texture = <sourceTexture2>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};

texture sourceTexture3;
sampler normalSampler : register(s3) = sampler_state
{
    Texture = <sourceTexture3>;
    MinFilter = Linear;
    MagFilter = Linear;
    MipFilter = None;
    AddressU = clamp;
    AddressV = clamp;
};


struct VSInput
{
    float3 pos : POSITION;
    float2 texCoord : TEXCOORD0;
};

struct VSOut
{
    float4 pos : POSITION;
    float2 texCoord : TEXCOORD0;
    float3 cameraEye : TEXCOORD1;
};

struct PSOut
{
    float4 color : COLOR0;
};

VSOut MainVS(VSInput input)
{
    VSOut output;

    output.pos = float4(input.pos, 1);
    output.texCoord = input.texCoord;
    output.cameraEye = float3(input.pos.x * TanHalfFOV * ViewAspect, input.pos.y * TanHalfFOV, 1);

    return output;
}

float dist_factor(float3 object_pos)
{
    float4 light_pos = mul(float4(light_position, 1), matView);
    float dist = distance(object_pos, light_pos.xyz / light_pos.w);

    float dist_att;
    if (dist > light_range)
    {
        dist_att = 0;
    }
    else
    {
        dist_att = 1 / (light_attenuation0 + light_attenuation1 * dist + light_attenuation2 * dist * dist);
    }

    return dist_att;
}

/*
 * diffuse: object material diffuse color
 * normal: object normal vector in camera space
 * position: object position in camera space
 */
float3 lighting(float4 diffuse, float3 normal, float3 position)
{
    float3 I_diff, I_spec, I_total;
    float3 l, v, n, h;
    float att;

    n = normalize(normal);
    v = normalize(-position);

    // FIXME: two test value
    float m_shi = 1;
    float4 m_spec = float4(1, 1, 1, 1);

    att = 1;

    // tranform light direction from wolrd space to camera space
    float4 light_dir = mul(float4(light_direction, 0), matView);
    l = normalize(-light_dir.xyz);

    I_diff = saturate(dot(l, n)) * (diffuse.xyz * light_diffuse.xyz);

    h = normalize(l + v);

    I_spec = saturate(dot(l, n)) * pow(saturate(dot(h, n)), m_shi) * (m_spec.xyz * light_specular.xyz);

    I_total = att * (I_diff + I_spec);
    return I_total;
}

PSOut MainPS(VSOut input)
{
    PSOut output;

    float2 texCoord = input.texCoord;
    float4 color = tex2D(diffuseSampler, texCoord);
    float alpha = color.a;
	
    // if the normal is world space normal value
    float4 norm = tex2D(normalSampler, texCoord);
    float4 normal_in_camera = mul(float4(norm.rgb * 2.0 - 1.0, 0), matView);
    float3 normal = normalize(normal_in_camera.xyz);

	// screen space depth value. 
    float depth = tex2D(depthSampler, texCoord).x;

    // position in camera space
    float4 position = float4(input.cameraEye * depth, 1);

    float3 total_color = color.rgb;
    total_color = total_color + lighting(color, normal.xyz, position.xyz);

    output.color = float4(total_color, alpha);

    return output;
}


technique DirectionalLight
{
    pass P0
    {
        VertexShader = compile vs_3_0 MainVS();
        PixelShader = compile ps_3_0 MainPS();

        CullMode = None;
        ZEnable = false;
        ZWriteEnable = false;
    }
}



```

```c++

#pragma once
#include "ParaXEntity.h"
#include "SphereObject.h"
#include <string>
namespace ParaEngine
{
	class CParaXModel;
	class CLightParam;

	/** this is an independent local light scene object.
	* local lights are mostly contained in the mesh object. But an independent light object like this
	* is useful, when we want to manipulate the light object at runtime. */
	class CLightObject : public CSphereObject
	{
	public:
		virtual CBaseObject::_SceneObjectType GetType() { return CBaseObject::LightObject; };
		CLightObject(void);
		virtual ~CLightObject(void);

	public:
		//////////////////////////////////////////////////////////////////////////
		// implementation of IAttributeFields
		ATTRIBUTE_DEFINE_CLASS(CLightObject);
		ATTRIBUTE_SUPPORT_CREATE_FACTORY(CLightObject);

		/** this class should be implemented if one wants to add new attribute. This function is always called internally.*/
		virtual int InstallFields(CAttributeClass* pClass, bool bOverride);

		ATTRIBUTE_METHOD1(CLightObject, GetLightType_s, int*) { *p1 = cls->GetLightType(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetLightType_s, int) { cls->SetLightType(p1); return S_OK; }

		ATTRIBUTE_METHOD1(CLightObject, GetDiffuse_s, Vector3*) { *p1 = *(Vector3*)(&cls->GetDiffuse()); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetDiffuse_s, Vector3) { LinearColor c(p1.x, p1.y, p1.z, 1); cls->SetDiffuse(c); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetSpecular_s, Vector3*) { *p1 = *(Vector3*)(&cls->GetSpecular()); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetSpecular_s, Vector3) { LinearColor c(p1.x, p1.y, p1.z, 1); cls->SetSpecular(c); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetAmbient_s, Vector3*) { *p1 = *(Vector3*)(&cls->GetAmbient()); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetAmbient_s, Vector3) { LinearColor c(p1.x, p1.y, p1.z, 1); cls->SetAmbient(c); return S_OK; }

		ATTRIBUTE_METHOD1(CLightObject, GetPosition_s, DVector3*) { *p1 = DVector3(cls->GetPosition()); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetPosition_s, DVector3) { DVector3 c(p1.x, p1.y, p1.z); cls->SetPosition(c); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetDirection_s, Vector3*) { *p1 = *(Vector3*)(&cls->GetDirection()); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetDirection_s, Vector3) { Vector3 c(p1.x, p1.y, p1.z); cls->SetDirection(c); return S_OK; }

		/** Yaw Pitch Roll inherit from BaseObject */

		ATTRIBUTE_METHOD1(CLightObject, GetRange_s, float*) { *p1 = cls->GetRange(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetRange_s, float) { cls->SetRange(p1); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetFalloff_s, float*) { *p1 = cls->GetFalloff(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetFalloff_s, float) { cls->SetFalloff(p1); return S_OK; }

		ATTRIBUTE_METHOD1(CLightObject, GetAttenuation0_s, float*) { *p1 = cls->GetAttenuation0(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetAttenuation0_s, float) { cls->SetAttenuation0(p1); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetAttenuation1_s, float*) { *p1 = cls->GetAttenuation1(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetAttenuation1_s, float) { cls->SetAttenuation1(p1); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetAttenuation2_s, float*) { *p1 = cls->GetAttenuation2(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetAttenuation2_s, float) { cls->SetAttenuation2(p1); return S_OK; }

		ATTRIBUTE_METHOD1(CLightObject, GetTheta_s, float*) { *p1 = cls->GetTheta(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetTheta_s, float) { cls->SetTheta(p1); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, GetPhi_s, float*) { *p1 = cls->GetPhi(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetPhi_s, float) { cls->SetPhi(p1); return S_OK; }

		ATTRIBUTE_METHOD1(CLightObject, IsDeferredLightOnly_s, bool*) { *p1 = cls->IsDeferredLightOnly(); return S_OK; }
		ATTRIBUTE_METHOD1(CLightObject, SetDeferredLightOnly_s, bool) { cls->SetDeferredLightOnly(p1); return S_OK; }

	public:
		virtual std::string ToString(DWORD nMethod);

		/** Rotate the object.This only takes effects on objects having 3D orientation, such as
		* static mesh and physics mesh. The orientation is computed in the following way: first rotate around x axis,
		* then around y, finally z axis.
		* @param x: rotation around the x axis.
		* @param y: rotation around the y axis.
		* @param z: rotation around the z axis.
		*/
		virtual void Rotate(float x, float y, float z);

		/** set the scale of the object. This function takes effects on both character object and mesh object.
		* @param s: scaling applied to all axis.1.0 means original size. */
		virtual void SetScaling(float s);

		/** reset the object to its default settings.*/
		virtual void Reset();

		int GetPrimaryTechniqueHandle();

		/**
		* Init from light struct.
		* @param pLight the initial light parameter, if NULL, a default white spot light will be created.
		* @param ppMesh: the mesh used to draw the object
		* @param vCenter: center world position.
		* @param mat: local transformation matrix
		* @param bCopyParams if true, the light object will make an internal copy of the light parameters.
		*	if not, it will only keep a reference to the light parameter. Only set this to false, when one
		*	need to manipulate it through the GUI.
		* @return S_OK if succeeds.
		*/
		HRESULT InitObject(CLightParam* pLight, MeshEntity* ppMesh, const Vector3& vCenter, const Matrix4& mat, bool bCopyParams = true);

		/** derived class can override this function to place the object in to the render pipeline.
		* if this function return -1, the SceneObject will automatically place the object into the render pipeline.
		* if return 0, it means the object has already placed the object and the scene object should skip this object.
		*/
		virtual int PrepareRender(CBaseCamera* pCamera, SceneState * sceneState);

		/** it only draws an arrow, when the scene's show local light parameter is true. */
		virtual HRESULT Draw(SceneState * sceneState);

		virtual void Cleanup();

		/** set local transform directly */
		void SetLocalTransform(const Matrix4& mXForm);
		/** set local transform by first uniform scale, then rotate around Z, X, Y axis sequentially. */
		void SetLocalTransform(float fScale, float fRotX, float fRotY, float fRotZ);
		/** set local transform by first uniform scale, then rotate using a quaternion. */
		void SetLocalTransform(float fScale, const Quaternion& quat);
		/** get local transform*/
		void GetLocalTransform(Matrix4* localTransform);

		/** return the global light in render coordinate system. */
		CLightParam* GetLightParams();

		virtual AssetEntity* GetPrimaryAsset();
		virtual void SetAssetFileName(const std::string& sFilename);
		virtual Matrix4* GetAttachmentMatrix(Matrix4& pOut, int nAttachmentID = 0, int nRenderNumber = 0);

		/**
		* return the world matrix of the object for rendering
		* @param out: the output.
		* @param nRenderNumber: if it is bigger than current calculated render number, the value will be recalculated. If 0, it will not recalculate
		* @return: same as out. or NULL if not exists.
		*/
		virtual Matrix4* GetRenderMatrix(Matrix4& out, int nRenderNumber = 0);
		virtual void RenderDeferredLightMesh(SceneState * sceneState);
	public:
		/**
		* Set type
		* @param nType D3DLIGHTTYPE
		*  - D3DLIGHT_POINT          = 1,
		*  - D3DLIGHT_SPOT           = 2,
		*  - D3DLIGHT_DIRECTIONAL    = 3,
		*/
		void SetLightType(int nType);
		int GetLightType();

		void SetDiffuse(const LinearColor& color);
		const LinearColor& GetDiffuse();
		void SetSpecular(const LinearColor& color);
		const LinearColor& GetSpecular();
		void SetAmbient(const LinearColor& color);
		const LinearColor& GetAmbient();

		/*
		 * ATTENTION:
		 * why no void SetPosition(const DVector3& pos) and DVector3 GetPosition()?
		 *
		 * e.g.
		 *   coord (19999.234, -128, 20000.1) is not world pos of light/block,
		 *   because the world center is (20000, -128, 20000)[I guess],
		 *   so the world pos should be (19999.234, -128, 20000.1) - (20000, -128, 20000) = (-0.766, 0, 0.1)
		 *
		 * we calculate light in shader using world pos, (-0.766, 0, 0.1), and that is calculated in function
		 * GetLightParams(), GetRenderMatrix(). 
		 * 
		 * this class store the position in parent class SphereObject, and calculate the light world pos as needed.
		 */
		void SetDirection(const Vector3& dir);
		const Vector3& GetDirection();

		virtual void SetYaw(float yaw);
		virtual float GetYaw();
		virtual void SetPitch(float pitch);
		virtual float GetPitch();
		virtual void SetRoll(float roll);
		virtual float GetRoll();

		void SetRange(float range);
		float GetRange();
		void SetFalloff(float falloff);
		float GetFalloff();

		void SetAttenuation0(float Attenuation0);
		float GetAttenuation0();
		void SetAttenuation1(float Attenuation1);
		float GetAttenuation1();
		void SetAttenuation2(float Attenuation2);
		float GetAttenuation2();

		void SetTheta(float theta);
		float GetTheta();
		void SetPhi(float phi);
		float GetPhi();

		void AutoSetAttenation();

		/** whether the light is enabled for deferred render pipeline only. */
		bool IsDeferredLightOnly() const;
		void SetDeferredLightOnly(bool val);

		/** whether rotation has happened */
		bool IsRotationDirty() const;
		void SetRotationDirty(bool val);
	protected:
		/** current position in the map */
		//Vector3           m_vPos;
		/** local transform. usually a rotation with scaling.  */
		//Matrix4            m_mxLocalTransform;
		Matrix4            m_mxLocalTransform;

		AnimIndex m_CurrentAnim;

		/** mesh geometry */
		ref_ptr<ParaXEntity>      m_pAnimatedMesh;
		ref_ptr<MeshEntity>		  m_pDeferredShadingMesh;

		/** light parameters. */
		CLightParam* m_pLightParams;

		/** if true, the light object will delete the m_pLightParams object at destruction time. */
		bool m_bDeleteLightParams;

		/** whether the light is enabled for deferred render pipeline only. */
		bool m_bDeferredLightOnly;

		/** if true, auto set attenuation{0-2} as the range changes. */
		bool m_bAutoSetAttenuation;

		/** if rotation has happened */
		bool m_bRotationDirty;
	};
}


//-----------------------------------------------------------------------------
// Class: CLightObject
// Authors:	LiXizhi, devilwalk
// Emails:	LiXizhi@yeah.net
// Date:	2006.6
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "ParaWorldAsset.h"
#include "SceneState.h"
#include "SceneObject.h"
#include "LightParam.h"
#include "BlockEngine/BlockWorldClient.h"
#include "LightManager.h"
#include "LightObject.h"
#include "LightGeoUtil.h"

using namespace ParaEngine;

/**@def whether to automatically adjust light parameters by range. */
#define AUTO_LIGHT_PARAMS_BY_RANGE

CLightObject::CLightObject(void)
	:m_bDeleteLightParams(true), m_pLightParams(NULL), m_bAutoSetAttenuation(true), m_bRotationDirty(false)
{

	m_pLightParams = new CLightParam();

	m_pLightParams->MakeRedPointLight();
	//m_pLightParams->MakeRedSpotLight();
	//m_pLightParams->MakeRedDirectionalLight();

	m_mxLocalTransform = Matrix4::IDENTITY;
	SetMyType(_LocalLight);
	SetShadowCaster(false);
}

CLightObject::~CLightObject(void)
{
	if (m_bDeleteLightParams)
		SAFE_DELETE(m_pLightParams);
}

void CLightObject::Cleanup()
{
}

std::string CLightObject::ToString(DWORD nMethod)
{
#ifndef MAX_LINE
#define MAX_LINE	500
#endif
	string sScript;
	char line[MAX_LINE + 1];

	Matrix4 mat;
	GetLocalTransform(&mat);
	Vector3 vPos = GetObjectCenter();
	const char* sLightParams = "";
	if (m_pLightParams != 0)
	{
		sLightParams = m_pLightParams->ToString();
	}
	if (SUCCEEDED(snprintf(line, MAX_LINE, "player = ParaScene.CreateLightObject(\"\", %f,%f,%f, \"%s\",\"%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\");\n",
		vPos.x, vPos.y, vPos.z, sLightParams,
		mat._11, mat._12, mat._13, mat._21, mat._22, mat._23, mat._31, mat._32, mat._33, mat._41, mat._42, mat._43)))
	{
		sScript.append(line);
		sScript.append("ParaScene.Attach(player);\n");
	}
	else
	{
		OUTPUT_LOG("error writing light objects.\r\n");
	}
	return sScript;
}

CLightParam* CLightObject::GetLightParams()
{
	// get position in the render coordinate system
	Vector3 vPos = GetRenderOffset();
	// render at the center
	vPos.y += GetHeight() / 2;

	if (m_pLightParams != 0)
	{
		m_pLightParams->Position = vPos;
	}
	return m_pLightParams;
}

void CLightObject::SetLocalTransform(const Matrix4& mXForm)
{
	m_mxLocalTransform = mXForm;
}

void CLightObject::SetLocalTransform(float fScale, float fRotX, float fRotY, float fRotZ)
{
	Matrix4 mx;
	ParaMatrixScaling(&m_mxLocalTransform, fScale, fScale, fScale);
	ParaMatrixRotationZ(&mx, fRotZ);
	m_mxLocalTransform = m_mxLocalTransform * mx;
	ParaMatrixRotationX(&mx, fRotX);
	m_mxLocalTransform = m_mxLocalTransform * mx;
	ParaMatrixRotationY(&mx, fRotY);
	m_mxLocalTransform = m_mxLocalTransform * mx;
}

void CLightObject::SetLocalTransform(float fScale, const Quaternion& quat)
{
	Matrix4 mx;
	ParaMatrixScaling(&m_mxLocalTransform, fScale, fScale, fScale);
	quat.ToRotationMatrix(mx, Vector3::ZERO);
	m_mxLocalTransform = m_mxLocalTransform * mx;
}

void CLightObject::GetLocalTransform(Matrix4* localTransform)
{
	*localTransform = m_mxLocalTransform;
}

void CLightObject::Rotate(float x, float y, float z)
{
	Matrix4 mat;
	GetLocalTransform(&mat);
	Matrix4 mat1;
	if (x != 0.f)
		mat = (*ParaMatrixRotationX(&mat1, x))*mat;
	if (y != 0.f)
		mat = (*ParaMatrixRotationY(&mat1, y))*mat;
	if (z != 0.f)
		mat = (*ParaMatrixRotationZ(&mat1, z))*mat;

	SetLocalTransform(mat);
}

void CLightObject::SetScaling(float s)
{
	Matrix4 mat;
	GetLocalTransform(&mat);
	Matrix4 mat1;
	ParaMatrixScaling(&mat1, s, s, s);
	mat = mat1 * mat;
	SetLocalTransform(mat);
}

void CLightObject::Reset()
{
	SetLocalTransform(*CGlobals::GetIdentityMatrix());
}

HRESULT CLightObject::InitObject(CLightParam* pLight, MeshEntity* ppMesh, const Vector3& vCenter, const Matrix4& mat, bool bCopyParams)
{
	// set position
	SetObjectCenter(vCenter);

	if (m_bDeleteLightParams)
		SAFE_DELETE(m_pLightParams);

	if (pLight == NULL)
	{
		m_pLightParams = new CLightParam();
		m_pLightParams->MakeRedPointLight();
		m_bDeleteLightParams = true;
	}
	else
	{
		if (bCopyParams) {
			m_pLightParams = new CLightParam();
			*m_pLightParams = *pLight;
			m_bDeleteLightParams = true;
		}
		else {
			m_pLightParams = pLight;
			m_bDeleteLightParams = false;
		}
	}

	// set the radius, this is for view clipping object calculation and scene attachment . 
	// TODO: we should over write the view clipping object to calculate the light region's bounding box. 
	SetRadius(m_pLightParams->Range);
	return S_OK;
}

void CLightObject::SetLightType(int nType)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Type = (D3DLIGHTTYPE)nType;
	}
}

int CLightObject::GetLightType()
{
	return (int)((m_pLightParams != 0) ? m_pLightParams->Type : D3DLIGHT_POINT);
}

void CLightObject::SetDiffuse(const LinearColor& color)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Diffuse = color;
	}
}

const LinearColor& CLightObject::GetDiffuse()
{
	static const LinearColor g_default = { 1, 1, 1, 1 };
	return (m_pLightParams != 0) ? m_pLightParams->Diffuse : g_default;
}

void CLightObject::SetSpecular(const LinearColor& color)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Specular = color;
	}
}

const LinearColor& CLightObject::GetSpecular()
{
	static const LinearColor g_default = { 1, 1, 1, 1 };
	return (m_pLightParams != 0) ? m_pLightParams->Specular : g_default;
}

void CLightObject::SetAmbient(const LinearColor& color)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Ambient = color;
	}
}

const LinearColor& CLightObject::GetAmbient()
{
	static const LinearColor g_default = { 1, 1, 1, 1 };
	return (m_pLightParams != 0) ? m_pLightParams->Ambient : g_default;
}

void CLightObject::SetDirection(const Vector3& dir)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Direction = dir;
	}
}

const Vector3& CLightObject::GetDirection()
{
	static const Vector3 g_default = { 1, 1, 1 };

	if (IsRotationDirty()) {
		m_pLightParams->RecalculateDirection();
		SetRotationDirty(false);
	}

	return (m_pLightParams != 0) ? m_pLightParams->Direction : g_default;
}

void CLightObject::SetYaw(float yaw)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Yaw = yaw;
		m_bRotationDirty = true;
	}
}

float CLightObject::GetYaw()
{
	return (m_pLightParams != 0) ? m_pLightParams->Yaw : 0.f;
}

void CLightObject::SetPitch(float pitch)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Pitch = pitch;
		m_bRotationDirty = true;
	}
}

float CLightObject::GetPitch()
{
	return (m_pLightParams != 0) ? m_pLightParams->Pitch : 0.f;
}

void CLightObject::SetRoll(float roll)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Roll = roll;
		m_bRotationDirty = true;
	}
}

float CLightObject::GetRoll()
{
	return (m_pLightParams != 0) ? m_pLightParams->Roll : 0.f;
}

void CLightObject::SetRange(float range)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Range = range;
	}

	AutoSetAttenation();
}

float CLightObject::GetRange()
{
	return (m_pLightParams != 0) ? m_pLightParams->Range : 0.f;
}

void CLightObject::SetFalloff(float falloff)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Falloff = falloff;
	}
}

float CLightObject::GetFalloff()
{
	return (m_pLightParams != 0) ? m_pLightParams->Falloff : 0.f;
}

void CLightObject::SetAttenuation0(float Attenuation0)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Attenuation0 = Attenuation0;
	}
}

float CLightObject::GetAttenuation0()
{
	return (m_pLightParams != 0) ? m_pLightParams->Attenuation0 : 0.f;
}

void CLightObject::SetAttenuation1(float Attenuation1)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Attenuation1 = Attenuation1;
	}
}

float CLightObject::GetAttenuation1()
{
	return (m_pLightParams != 0) ? m_pLightParams->Attenuation1 : 0.f;
}

void CLightObject::SetAttenuation2(float Attenuation2)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Attenuation2 = Attenuation2;
	}
}

float CLightObject::GetAttenuation2()
{
	return (m_pLightParams != 0) ? m_pLightParams->Attenuation2 : 0.f;
}

void CLightObject::SetTheta(float theta)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Theta = theta;
	}
}

float CLightObject::GetTheta()
{
	return (m_pLightParams != 0) ? m_pLightParams->Theta : 0.f;
}

void CLightObject::SetPhi(float phi)
{
	if (m_pLightParams != 0)
	{
		m_pLightParams->Phi = phi;
	}
}

float CLightObject::GetPhi()
{
	return (m_pLightParams != 0) ? m_pLightParams->Phi : 0.f;
}

int ParaEngine::CLightObject::GetPrimaryTechniqueHandle()
{
	switch (m_pLightParams->Type) {
	case D3DLIGHT_POINT:
		return TECH_LIGHT_POINT;
	case D3DLIGHT_SPOT:
		return TECH_LIGHT_SPOT;
	case D3DLIGHT_DIRECTIONAL:
		return TECH_LIGHT_DIRECTIONAL;
	}
}

int ParaEngine::CLightObject::PrepareRender(CBaseCamera* pCamera, SceneState * sceneState)
{
	if (sceneState->GetScene()->PrepareRenderObject(this, pCamera, *sceneState))
	{
#ifdef USE_DIRECTX_RENDERER
		if (IsDeferredLightOnly())
		{
			sceneState->AddToDeferredLightPool(this);
		}
		else
		{
			CGlobals::GetLightManager()->RegisterLight(GetLightParams());
		}
#endif
	}
	return 0;
}

HRESULT CLightObject::Draw(SceneState * sceneState)
{
	return S_OK;
	if (IsDeferredLightOnly() && sceneState->IsDeferredShading())
	{
		RenderDeferredLightMesh(sceneState);
	}
	return S_OK;
}

AssetEntity* ParaEngine::CLightObject::GetPrimaryAsset()
{
	return (m_pAnimatedMesh.get());
}

void ParaEngine::CLightObject::SetAssetFileName(const std::string& sFilename)
{
	auto pNewModel = CGlobals::GetAssetManager()->LoadParaX("", sFilename);
	if (m_pAnimatedMesh != pNewModel)
	{
		m_pAnimatedMesh = pNewModel;
		m_CurrentAnim.MakeInvalid();
		SetGeometryDirty(true);
	}
}

Matrix4* ParaEngine::CLightObject::GetAttachmentMatrix(Matrix4& matOut, int nAttachmentID /*= 0*/, int nRenderNumber /*= 0*/)
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

Matrix4* ParaEngine::CLightObject::GetRenderMatrix(Matrix4& out, int nRenderNumber /*= 0*/)
{
	// world translation
	Vector3 vPos = GetRenderOffset();
	// render at the center
	vPos.y += GetHeight() / 2;

	out = m_mxLocalTransform;
	out._41 += vPos.x;
	out._42 += vPos.y;
	out._43 += vPos.z;
	return &out;
}

void ParaEngine::CLightObject::RenderDeferredLightMesh(SceneState * sceneState)
{
	if (sceneState->IsShadowPass())
		return;

#ifdef USE_DIRECTX_RENDERER
	sceneState->SetCurrentSceneObject(this);
	SetFrameNumber(sceneState->m_nRenderCount);

	// get world transform matrix
	Matrix4 mxWorld;
	GetRenderMatrix(mxWorld);
	mxWorld = m_mxLocalTransform * mxWorld;
	CGlobals::GetWorldMatrixStack().push(mxWorld);

	struct LightVertex
	{
	public:
		LightVertex() :normal(1, 0, 0), color(0xffffffff) {};
		Vector3 position;  //4byte
		Vector3 normal;  //4byte
		DWORD color;	//4byte;
	};
	std::vector<LightVertex> m_Vertices;
	m_Vertices.resize(8);
	m_Vertices[0].position = Vector3(0, 1, 0);
	m_Vertices[1].position = Vector3(0, 1, 1);
	m_Vertices[2].position = Vector3(1, 1, 1);
	m_Vertices[3].position = Vector3(1, 1, 0);
	uint16 m_indices[6] = { 0,1,2,   0,2,3 };

	LightVertex* vb_vertices = NULL;
	LightVertex *ov = NULL;
	LightVertex *m_origVertices = &(m_Vertices[0]);

	DynamicVertexBufferEntity* pBufEntity = CGlobals::GetAssetManager()->GetDynamicBuffer(DVB_XYZ_NORM_DIF);

	auto pDevice = sceneState->GetRenderDevice();
	pDevice->SetStreamSource(0, pBufEntity->GetBuffer(), 0, sizeof(LightVertex));

	int nNumLockedVertice;
	int nNumFinishedVertice = 0;
	int indexCount = (int)m_Vertices.size();
	do
	{
		if ((nNumLockedVertice = pBufEntity->Lock(indexCount - nNumFinishedVertice, (void**)(&vb_vertices))) > 0)
		{
			int nLockedNum = nNumLockedVertice / 3;

			int nIndexOffset = nNumFinishedVertice;
			for (int i = 0; i < nLockedNum; ++i)
			{
				int nVB = 3 * i;
				for (int k = 0; k < 3; ++k, ++nVB)
				{
					int a = m_indices[nIndexOffset + nVB];
					LightVertex& out_vertex = vb_vertices[nVB];
					// weighted vertex
					ov = m_origVertices + a;
					out_vertex.position = ov->position;
					out_vertex.normal = ov->normal;
					out_vertex.color = 0xffffffff;
				}
			}
			pBufEntity->Unlock();

			if (pBufEntity->IsMemoryBuffer())
				RenderDevice::DrawPrimitiveUP(pDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, nLockedNum, pBufEntity->GetBaseVertexPointer(), pBufEntity->m_nUnitSize);
			else
				RenderDevice::DrawPrimitive(pDevice, RenderDevice::DRAW_PERF_TRIANGLES_CHARACTER, D3DPT_TRIANGLELIST, pBufEntity->GetBaseVertex(), nLockedNum);
		}
		if ((indexCount - nNumFinishedVertice) > nNumLockedVertice)
		{
			nNumFinishedVertice += nNumLockedVertice;
		}
		else
			break;

	} while (1);


	CGlobals::GetWorldMatrixStack().pop();
#endif
}


void ParaEngine::CLightObject::AutoSetAttenation()
{
	/*
	 * att = 1 / (a0 + a1*r + a2*r*r)
	 *
	 * if att at the maximum range edge is 0.1, then
	 *    a0 + a1*r + a2*r*r = 1 / att = 10
	 *
	 * we prefer a0,a1,a2 acting in range [0, 1],
	 * so we use a greedy way to calculate the a0, a1, a2
	 */
	if (m_bAutoSetAttenuation) {
		float edge_att = 0.1f;
		float one_over_att = 1 / edge_att;
		float range = m_pLightParams->Range;

		SetAttenuation0(1.0f);
		one_over_att = one_over_att - 1;

		if (range > one_over_att) {
			SetAttenuation1(one_over_att / range);
			one_over_att = 0.f;
		}
		else {
			SetAttenuation1(1.0f);
			one_over_att = one_over_att - range;
		}

		SetAttenuation2(one_over_att / (range * range));
		one_over_att = 0.f;
	}
}

bool ParaEngine::CLightObject::IsDeferredLightOnly() const
{
	return m_bDeferredLightOnly;
}

void ParaEngine::CLightObject::SetDeferredLightOnly(bool val)
{
	m_bDeferredLightOnly = val;
}


bool ParaEngine::CLightObject::IsRotationDirty() const
{
	return m_bRotationDirty;
}

void ParaEngine::CLightObject::SetRotationDirty(bool val)
{
	m_bRotationDirty = val;
}

int CLightObject::InstallFields(CAttributeClass* pClass, bool bOverride)
{
	CSphereObject::InstallFields(pClass, bOverride);

	pClass->AddField("LightType", FieldType_Int, (void*)SetLightType_s, (void*)GetLightType_s, NULL, NULL, bOverride);

	pClass->AddField("Diffuse", FieldType_Vector3, (void*)SetDiffuse_s, (void*)GetDiffuse_s, CAttributeField::GetSimpleSchemaOfRGB(), NULL, bOverride);
	pClass->AddField("Specular", FieldType_Vector3, (void*)SetSpecular_s, (void*)GetSpecular_s, CAttributeField::GetSimpleSchemaOfRGB(), NULL, bOverride);
	pClass->AddField("Ambient", FieldType_Vector3, (void*)SetAmbient_s, (void*)GetAmbient_s, CAttributeField::GetSimpleSchemaOfRGB(), NULL, bOverride);

	pClass->AddField("Position", FieldType_DVector3, (void*)SetPosition_s, (void*)GetPosition_s, NULL, NULL, bOverride);
	pClass->AddField("Direction", FieldType_Vector3, (void*)SetDirection_s, (void*)GetDirection_s, NULL, NULL, bOverride);
	pClass->AddField("Yaw", FieldType_Float, (void*)SetYaw_s, (void*)GetYaw_s, NULL, NULL, bOverride);
	pClass->AddField("Pitch", FieldType_Float, (void*)SetPitch_s, (void*)GetPitch_s, NULL, NULL, bOverride);
	pClass->AddField("Roll", FieldType_Float, (void*)SetRoll_s, (void*)GetRoll_s, NULL, NULL, bOverride);

	pClass->AddField("Range", FieldType_Float, (void*)SetRange_s, (void*)GetRange_s, NULL, NULL, bOverride);
	pClass->AddField("Falloff", FieldType_Float, (void*)SetFalloff_s, (void*)GetFalloff_s, NULL, NULL, bOverride);

	pClass->AddField("Attenuation0", FieldType_Float, (void*)SetAttenuation0_s, (void*)GetAttenuation0_s, NULL, NULL, bOverride);
	pClass->AddField("Attenuation1", FieldType_Float, (void*)SetAttenuation1_s, (void*)GetAttenuation1_s, NULL, NULL, bOverride);
	pClass->AddField("Attenuation2", FieldType_Float, (void*)SetAttenuation2_s, (void*)GetAttenuation2_s, NULL, NULL, bOverride);

	pClass->AddField("Theta", FieldType_Float, (void*)SetTheta_s, (void*)GetTheta_s, NULL, NULL, bOverride);
	pClass->AddField("Phi", FieldType_Float, (void*)SetPhi_s, (void*)GetPhi_s, NULL, NULL, bOverride);

	pClass->AddField("IsDeferredLightOnly", FieldType_Bool, (void*)SetDeferredLightOnly_s, (void*)IsDeferredLightOnly_s, NULL, NULL, bOverride);
	return S_OK;
}

#pragma once

namespace ParaEngine
{
	/** a single light in ParaEngine. */
	class CLightParam : public Para3DLight
	{
	public:
		CLightParam(void);
		~CLightParam(void);
	public:

		// Return whether first element is greater than the second
		bool static IsGreater(const CLightParam& elem1, const CLightParam& elem2)
		{
			return elem1.m_nScore > elem2.m_nScore;
		}
		bool static IsGreaterPt(const CLightParam* elem1, const CLightParam* elem2)
		{
			return elem1->m_nScore > elem2->m_nScore;
		}

		/** make the current light a white point light with default value. */
		void MakeRedPointLight();
		void MakeRedSpotLight();
		void MakeRedDirectionalLight();

		// calculate direction base on yaw/pitch/roll
		void RecalculateDirection();

		/**
		* return the parameters as a string. This is usually used for serialization.
		* format is "Type Range (r g b a) att0 att1 att2"
		* D3DLIGHTTYPE    Type;            Type of light source
		* 						- D3DLIGHT_POINT          = 1,
		* 						- D3DLIGHT_SPOT           = 2,
		* 						- D3DLIGHT_DIRECTIONAL    = 3,
		* float           Range;           Cutoff range
		* D3DCOLORVALUE   Diffuse;         Diffuse color of light
		* float           Attenuation0;    Constant attenuation
		* float           Attenuation1;    Linear attenuation
		* float           Attenuation2;    Quadratic attenuation
		* e.g. "1 7.0 (1 1 0 1) 0.3 0.1 1"
		* light intensity is calculated as 1/(Attenuation0+d*Attenuation1+d*d*Attenuation2), where d is the distance from the light to object center.
		* @return see above
		*/
		const char* ToString();
		/** convert a string returned by ToString() to this object.
		* @see ToString() */
		void FromString(const char* str);

	public:
		// yaw, pitch, roll for recording the rotation
		// radian system
		float Yaw;
		float Pitch;
		float Roll;

	private:
		int m_nScore;
		friend class CLightManager;

		Vector3 InitDirection = { 0, 0, 1 };
	};
}

//-----------------------------------------------------------------------------
// Class:	CLightParam
// Authors:	LiXizhi
// Emails:	LiXizhi@yeah.net
// Company: ParaEngine
// Date:	2006.4.17
//
// d3d light model reference:
// https://docs.microsoft.com/en-us/windows/desktop/direct3d9/d3dlight9
//-----------------------------------------------------------------------------
#include "ParaEngine.h"
#include "LightParam.h"

/** @def max length of string in CLightParam::ToString()*/
#define MAX_LIGHT_PARAM_STRING_LENGTH	512

using namespace ParaEngine;

CLightParam::CLightParam(void)
{
}

CLightParam::~CLightParam(void)
{
}

void CLightParam::MakeRedPointLight()
{
	Type = D3DLIGHT_POINT;

	Diffuse = LinearColor(1.0f, 0, 1.f, 1.0f);
	Specular = LinearColor(1.0f, 0, 0, 1.0f);
	Ambient = LinearColor(1.0f, 0, 0, 1.0f);

	Position = Vector3(0, 0, 0);
	/* no Direction */
	Direction = Vector3(0, 0, 1);
	/* no Yaw Pitch Roll */
	Yaw = 0;
	Pitch = 0;
	Roll = 0;

	Range = 3.f;
	/* no Falloff */
	Falloff = 1.f;

	Attenuation0 = 0.3f;
	Attenuation1 = 0.1f;
	Attenuation2 = 1.f;

	/* no Theta */
	Theta = 0.8f;
	/* no Phi */
	Phi = 1.0f;
}

void ParaEngine::CLightParam::MakeRedSpotLight()
{
	Type = D3DLIGHT_SPOT;

	Diffuse = LinearColor(1.0f, 1.0f, 0, 1.0f);
	Specular = LinearColor(1.0f, 0, 0, 1.0f);
	Ambient = LinearColor(1.0f, 0, 0, 1.0f);

	Position = Vector3(0, 0, 0);
	Direction = Vector3(0, 0, 1);
	Yaw = 0;
	Pitch = 0;
	Roll = 0;

	Range = 3.0f;
	Falloff = 1.f;

	Attenuation0 = 0.3f;
	Attenuation1 = 0.1f;
	Attenuation2 = 1.f;

	Theta = 0.8f;
	Phi = 1.0f;
}

void ParaEngine::CLightParam::MakeRedDirectionalLight()
{
	Type = D3DLIGHT_DIRECTIONAL;

	Diffuse = LinearColor(1.0f, 0, 0, 1.0f);
	Specular = LinearColor(1.0f, 0, 0, 1.0f);
	Ambient = LinearColor(1.0f, 0, 0, 1.0f);

	/* no Position */
	Position = Vector3(0, 0, 0);
	Direction = Vector3(0, 0, 1);
	Yaw = 0;
	Pitch = 0;
	Roll = 0;

	/* no Range */
	Range = 3.f;
	/* no Falloff */
	Falloff = 1.f;

	/* no Attenuation0 */
	Attenuation0 = 0.3f;
	/* no Attenuation1 */
	Attenuation1 = 0.1f;
	/* no Attenuation2 */
	Attenuation2 = 1.0f;

	/* no Theta */
	Theta = 0.8f;
	/* no Phi */
	Phi = 1.0f;
}

void ParaEngine::CLightParam::RecalculateDirection()
{
	// Yaw - around axis y
	// Pitch - around axis x
	// Roll - around axis z
	Matrix4 mat = Matrix4::IDENTITY;
	Matrix4 transform;

	// the order is roll -> pitch -> yaw
	// calculate the direction using extrinsic rotation
	// TODO: refer to blog - extrinsic and intrinsic
	if (Roll != 0.f)
		mat = (*ParaMatrixRotationZ(&transform, Roll))*mat;
	if (Pitch != 0.f)
		mat = (*ParaMatrixRotationX(&transform, Pitch))*mat;
	if (Yaw != 0.f)
		mat = (*ParaMatrixRotationY(&transform, Yaw))*mat;

	Direction = InitDirection.TransformNormal(mat);
}

const char* CLightParam::ToString()
{
	static char sParams[MAX_LIGHT_PARAM_STRING_LENGTH + 1];
	memset(sParams, 0, sizeof(sParams));

	snprintf(sParams, MAX_LIGHT_PARAM_STRING_LENGTH, "%d %f (%f %f %f %f) %f %f %f",
		Type, Range, Diffuse.r, Diffuse.g, Diffuse.b, Diffuse.a, Attenuation0, Attenuation1, Attenuation2);
	return sParams;
}

void CLightParam::FromString(const char* str)
{
	try
	{
		int nType = 0;
		sscanf(str, "%d %f (%f %f %f %f) %f %f %f",
			&nType, &Range, &Diffuse.r, &Diffuse.g, &Diffuse.b, &Diffuse.a, &Attenuation0, &Attenuation1, &Attenuation2);
		Type = (D3DLIGHTTYPE)nType;
		// just assume these values. 
		Ambient = LinearColor(0, 0, 0, 0);
		Position = Vector3(0, 0, 0);
	}
	catch (...)
	{
		MakeRedPointLight();
	}
}

	void BlockWorldClient::RenderDeferredLighting()
	{
#ifdef USE_DIRECTX_RENDERER
		SceneState* sceneState = CGlobals::GetSceneState();
		if (!sceneState->IsDeferredShading() || sceneState->listDeferredLightObjects.empty())
			return;

		CGlobals::GetEffectManager()->EndEffect();


		auto pDevice = sceneState->GetRenderDevice();

		ParaScripting::ParaAsset::LoadEffectFile("deferred_point_lighting", "script/apps/Aries/Creator/Game/Shaders/DeferredShadingPointLighting.fxo");
		ParaScripting::ParaAsset::LoadEffectFile("deferred_spot_lighting", "script/apps/Aries/Creator/Game/Shaders/DeferredShadingSpotLighting.fxo");
		ParaScripting::ParaAsset::LoadEffectFile("deferred_directional_lighting", "script/apps/Aries/Creator/Game/Shaders/DeferredShadingDirectionalLighting.fxo");

		ParaScripting::ParaAssetObject effect = NULL;

		VertexDeclarationPtr pDecl = NULL;

		ID3DXMesh * pObject = NULL;
		for (CLightObject* lightObject : sceneState->listDeferredLightObjects) {
			auto light_param = lightObject->GetLightParams();

			auto light_type = light_param->Type;

			auto light_diffuse = light_param->Diffuse;
			auto light_specular = light_param->Specular;
			auto light_ambient = light_param->Ambient;

			auto light_position = light_param->Position;
			auto light_direction = lightObject->GetDirection();

			auto light_range = light_param->Range;
			auto light_falloff = light_param->Falloff;

			auto light_attenuation0 = light_param->Attenuation0;
			auto light_attenuation1 = light_param->Attenuation1;
			auto light_attenuation2 = light_param->Attenuation2;

			auto light_theta = light_param->Theta;
			auto light_phi = light_param->Phi;

			// how complicated the mesh is
			int mesh_slice_num = 50;

			switch (light_type) {
			case D3DLIGHT_POINT:
				effect = ParaScripting::ParaAsset::GetEffectFile("deferred_point_lighting");
				D3DXCreateSphere(pDevice, light_range, mesh_slice_num, mesh_slice_num, &pObject, 0);

				pDecl = CGlobals::GetEffectManager()->GetVertexDeclaration(EffectManager::S0_POS);
				break;
			case D3DLIGHT_SPOT:
				effect = ParaScripting::ParaAsset::GetEffectFile("deferred_spot_lighting");
				// FIXME: how to draw a spherical cone but a normal cone
				//D3DXCreateCylinder(pDevice, 0.0f, 2.0f, 5.0f, 100, 100, &pObject, 0);
				D3DXCreateSphere(pDevice, light_range, mesh_slice_num, mesh_slice_num, &pObject, 0);

				pDecl = CGlobals::GetEffectManager()->GetVertexDeclaration(EffectManager::S0_POS);
				break;
			case D3DLIGHT_DIRECTIONAL:
				effect = ParaScripting::ParaAsset::GetEffectFile("deferred_directional_lighting");
				pDecl = CGlobals::GetEffectManager()->GetVertexDeclaration(EffectManager::S0_POS_TEX0);
				break;
			}

			if (pDecl)
				pDevice->SetVertexDeclaration(pDecl);

			effect.Begin();

			auto params = effect.GetParamBlock();
			params.SetParam("ViewAspect", "floatViewAspect");
			params.SetParam("TanHalfFOV", "floatTanHalfFOV");
			params.SetParam("screenParam", "vec2ScreenSize");

			Matrix4 mxWorld;
			lightObject->GetRenderMatrix(mxWorld);
			CGlobals::GetWorldMatrixStack().push(mxWorld);
			params.SetParam("matWorld", "mat4World");
			CGlobals::GetWorldMatrixStack().pop();

			params.SetParam("matView", "mat4View");
			params.SetParam("matProj", "mat4Projection");

			params.SetVector4("light_diffuse", light_diffuse.r, light_diffuse.g, light_diffuse.b, light_diffuse.a);
			params.SetVector4("light_specular", light_specular.r, light_specular.g, light_specular.b, light_specular.a);
			params.SetVector4("light_ambient", light_ambient.r, light_ambient.g, light_ambient.b, light_ambient.a);

			params.SetVector3("light_position", light_position.x, light_position.y, light_position.z);
			params.SetVector3("light_direction", light_direction.x, light_direction.y, light_direction.z);

			params.SetFloat("light_range", light_range);
			params.SetFloat("light_falloff", light_falloff);

			params.SetFloat("light_attenuation0", light_attenuation0);
			params.SetFloat("light_attenuation1", light_attenuation1);
			params.SetFloat("light_attenuation2", light_attenuation2);

			params.SetFloat("light_theta", light_theta);
			params.SetFloat("light_phi", light_phi);


			auto _ColorRT = ParaScripting::ParaAsset::LoadTexture("_ColorRT", "_ColorRT", 0);
			auto originRT = ParaScripting::CParaEngine::GetRenderTarget();
			ParaScripting::CParaEngine::StretchRect(originRT, _ColorRT);
			ParaScripting::CParaEngine::SetRenderTarget(originRT);
			params.SetTextureObj(0, _ColorRT);
			params.SetTextureObj(2, ParaScripting::ParaAsset::LoadTexture("_DepthTexRT_R32F", "_DepthTexRT_R32F", 0));
			params.SetTextureObj(3, ParaScripting::ParaAsset::LoadTexture("_NormalRT", "_NormalRT", 0));

			effect.CommitChanges();

			pDevice->Clear(0, 0, D3DCLEAR_STENCIL, 0, 1.0f, 0);

			switch (light_type) {
			case D3DLIGHT_POINT:
			case D3DLIGHT_SPOT:
				for (int pass = 0; pass < 2; pass++) {
					if (effect.BeginPass(pass)) {
						pObject->DrawSubset(0);
						effect.EndPass();
					}
				}
				pObject->Release();
				break;
			case D3DLIGHT_DIRECTIONAL:
				if (effect.BeginPass(0)) {
					ParaScripting::CParaEngine::DrawQuad();
					effect.EndPass();
				}
				break;
			}
			effect.End();
		}
#endif
	}

/**
Author: LiXizhi
Company: ParaEngine
Date: 2015.5.10
Desc: Deferred shading post processing: 4 passes as below
pass0 (lightmap + shadow + HDR + nighteye + sunspot + torch glow) + (TODO:ssao, underwater, specularity)
pass1 (reflection) + (TODO:sunspot in water)
pass2 (bloom textures) + (TODO:average luminance)
final (DepthOfView + Bloom + RainFog + Vignette + ToneMap)  + (TODO: motionBlur + luminanceToneMap)

References:
http://www.gamedev.net/topic/506573-reconstructing-position-from-depth-data/
http://www.crytek.com/cryengine/presentations/real-time-atmospheric-effects-in-games-revisited
SUES v10.1: Sonic Ether's unbelievable shader
CustomBuild:"$(DXSDK_DIR)/Utilities/bin/x86/fxc.exe" /Tfx_2_0 /Gfp /nologo /Fo %(RelativeDir)/%(Filename).fxo %(FullPath)
OUTPUT:%(RelativeDir)%(Filename).fxo
*/
/** whether to enable debug view. lt:bloom textures, lr:bloom sum, lb:original, rb:final. */
// #define SHOW_DEBUG_VIEW

#include "CommonFunction.fx"

float4x4 matView;
float4x4 matViewInverse;
float4x4 matProjection;
float4x4 mShadowMapTex;
float4x4 mShadowMapViewProj;
float2	viewportOffset;
float2	viewportScale;

float3   g_FogColor;

// x is shadow map size(such as 2048), y = 1/x
float2  ShadowMapSize;
// usually 40 meters
float	ShadowRadius; 

/** whether to desaturate and apply blue tint at dark night. */
#define NIGHT_EYE_EFFECT

// x>0 use sun shadow map, y>0 use water reflection, z>=1 bloom, z>=2 depth of view. 
float3 RenderOptions;


float2 screenParam;
float centerDepthSmooth = 15.f;
// between [0,1]
float rainStrength = 0.f;
float EyeBrightness = 0.5;
float ViewAspect;
float TanHalfFOV;
float cameraFarPlane;
float3 cameraPosition;
float3 sunDirection;
float3 SunColor;
float3 TorchLightColor;
float timeNoon = 1.0; // 1 is noon. 0 is night
float timeMidnight = 0.0; // 1 is midnight.
float DepthOfViewFactor = 0.15;	//aperture - bigger values for shallower depth of field
float FogStart = 100.0;
float FogEnd = 140.0;
float CloudThickness = 0.0;

static const float bloom_threshold = 0.7;
// offset_x, offset_y, scale_factor
static const float3 offsets[16] = {
	float3(0.008, 0.0, 1.0), float3(0.006, 0.0, 1.2), float3(0.004, 0.0, 1.3), float3(0.002, 0.0, 1.5),
	float3(0.0, 0.008, 1.0), float3(0.0, 0.006, 1.2), float3(0.0, 0.004, 1.3), float3(0.0, 0.002, 1.5),
	-float3(0.008, 0.0, 1.0), -float3(0.006, 0.0, 1.2), -float3(0.004, 0.0, 1.3), -float3(0.002, 0.0, 1.5),
	-float3(0.0, 0.008, 1.0), -float3(0.0, 0.006, 1.2), -float3(0.0, 0.004, 1.3), -float3(0.0, 0.002, 1.5)
};

texture sourceTexture0;
sampler colorSampler:register(s0) = sampler_state
{
	Texture = <sourceTexture0>;
	MinFilter = Linear;
	MagFilter = Linear;
	AddressU = clamp;
	AddressV = clamp;
};

texture sourceTexture1;
sampler matInfoSampler:register(s1) = sampler_state
{
	Texture = <sourceTexture1>;
	MinFilter = Linear;
	MagFilter = Linear;
	AddressU = clamp;
	AddressV = clamp;
};

texture sourceTexture2 : TEXTURE;
sampler ShadowMapSampler: register(s2) = sampler_state
{
	texture = <sourceTexture2>;
	MinFilter = Linear;
	MagFilter = Linear;
	MipFilter = None;
	AddressU = BORDER;
	AddressV = BORDER;
	BorderColor = 0x0;
};

texture sourceTexture3;
sampler depthSampler:register(s3) = sampler_state
{
	Texture = <sourceTexture3>;
	MinFilter = Linear;
	MagFilter = Linear;
	AddressU = clamp;
	AddressV = clamp;
};

texture sourceTexture4;
sampler normalSampler:register(s4) = sampler_state
{
	Texture = <sourceTexture4>;
	MinFilter = Linear;
	MagFilter = Linear;
	AddressU = clamp;
	AddressV = clamp;
};
texture sourceTexture5;
sampler compositeSampler:register(s5) = sampler_state
{
	Texture = <sourceTexture5>;
	MinFilter = Linear;
	MagFilter = Linear;
	AddressU = clamp;
	AddressV = clamp;
};
struct VSOutput
{
	float4 pos			: POSITION;         // Screen space position
	float2 texCoord		: TEXCOORD0;        // texture coordinates
	float3 CameraEye		: TEXCOORD2;      // texture coordinates
};

//All sky shading attributes
struct SkyStruct {
	float3 	albedo;				//Diffuse texture aka "color texture" of the sky
	float3 sunSpot;
	float sunProximity;
};

// Surface shading properties
struct SurfaceStruct
{
	int category_id;
	float3 	albedo;					// Diffuse texture "color texture" in linear color space (gamma decoded)
	float3 	normal;					// Screen-space surface normals
	float3	cameraSpacePos;
	float3	CameraEye;
	float2	texCoord;
	float 	depth;					// scene depth
	float 	NdotL; 					// dot(normal, lightVector). used for direct lighting calculation
	float 	shadow;
	SkyStruct sky;
	bool mask_sky;
	bool mask_water;
	bool mask_torch;
};

// Surface shading properties
struct SurfaceStruct2
{
	int category_id;
	float3 	color;					// Diffuse texture "color texture" in linear color space (gamma decoded)
	float	sunlightVisibility;
	float	torch_light_strength;
	float3 	normal;					// Screen-space surface normals
	float3	cameraSpacePos;
	float3	CameraEye;
	float2	texCoord;
	float 	depth;					// scene depth
	float 	NdotL; 					// dot(normal, lightVector). used for direct lighting calculation
	float 	shadow;
	float	specularity;
	bool mask_sky;
	bool mask_water;
	bool mask_metal;
};

// Lightmaps directly from C++ engine
struct RawLightmapStruct
{
	float torch;				//Light emitted from torches and other emissive blocks
	float sky;					//Light coming from the sky
};

//Lighting information to light the scene. These are untextured colored lightmaps to be multiplied with albedo to get the final lit and textured image.
struct LightmapStruct
{
	float3 sunlight;				//Direct light from the sun
	float3 skylight;				//Ambient light from the sky
	float3 bouncedSunlight;		//Fake bounced light, coming from opposite of sun direction and adding to ambient light
	float3 scatteredSunlight;		//Fake scattered sunlight, coming from same direction as sun and adding to ambient light
	float3 torchlight;			//Light emitted from torches and other emissive blocks
	float3 nolight;				//Base ambient light added to everything. For lighting caves so that the player can barely see even when no lights are present
	float3 sky;					//Color and brightness of the sky itself
};

// Result of shading calculation variables
struct ShadingStruct
{
	float   direct;
	float 	bounced; 			//Fake bounced sunlight
	float 	skylight; 			//Light coming from sky
	float 	scattered; 			//Fake scattered sunlight
	float 	sunlightVisibility; //Shadows
};

//Final textured and lit images sorted by what is illuminating them.
struct FinalStruct {
	float3 sunlight;				//Direct light from the sun
	float3 skylight;				//Ambient light from the sky
	float3 torchlight;			//Light emitted from torches and other emissive blocks
	float3 nolight;				//Base ambient light added to everything. For lighting caves so that the player can barely see even when no lights are present
	float3 sky;					//Color and brightness of the sky itself
	float3 glow_torch;
};

struct PSOut
{
	// HDR color
	float4 Color	: COLOR0;
	// 32bits additional information. 
	half4 Color2	: COLOR1;
};

VSOutput CompositeQuadVS(float3 iPosition:POSITION,
	float2 texCoord : TEXCOORD0)
{
	VSOutput o;
	o.pos = float4(iPosition, 1);
	o.texCoord = texCoord + 0.5 / screenParam;

	// for reconstructing world position from depth value
	float3 outCameraEye = float3(iPosition.x*TanHalfFOV*ViewAspect, iPosition.y*TanHalfFOV, 1);
	o.CameraEye = outCameraEye;

	return o;
}

//Function that retrieves the diffuse texture and convert it into linear space.
float3  GetAlbedoLinear(float2 texCoord)
{
	// decode gama correction, so that we work in original linear space
	return pow(tex2D(colorSampler, texCoord).rgb, 2.2f);
}

//Desaturates any color input at night, simulating the rods in the human eye
// @param amount: How much will the new desaturated and tinted image be mixed with the original image
void DoNightEye(inout float3 color, float amount)
{
	float3 rodColor = float3(0.2, 0.5, 1.0); 	//Cyan color that humans percieve when viewing extremely low light levels via rod cells in the eye
	float colorDesat = dot(color, float3(1, 1, 1)); 	//Desaturated color
	color = lerp(color, rodColor*colorDesat, amount);
}

float2 convertCameraSpaceToScreenSpace(float3 cameraSpace)
{
	float4 clipSpace = mul(float4(cameraSpace, 1.0), matProjection);
	float2 NDCSpace = clipSpace.xy / clipSpace.w;
	float2 ScreenPos = 0.5 * NDCSpace + 0.5;
	return float2(ScreenPos.x, 1 - ScreenPos.y) * viewportScale + viewportOffset;
}


// compute water reflection by sampling along the reflected eye ray until a pixel is found. 
float4 	ComputeRayTraceReflection(float3 cameraSpacePosition, float3 cameraSpaceNormal)
{
	float initialStepAmount = 1;
	//float stepRefinementAmount = 0.1;
	//int maxRefinements = 0;

	float3 cameraSpaceViewDir = normalize(cameraSpacePosition);
	float3 cameraSpaceVector = normalize(reflect(cameraSpaceViewDir, cameraSpaceNormal)) * initialStepAmount;
	float3 oldPosition = cameraSpacePosition;
	float3 cameraSpaceVectorPosition = oldPosition + cameraSpaceVector;
	float2 currentPosition = convertCameraSpaceToScreenSpace(cameraSpaceVectorPosition);
	float4 color = float4(0, 0, 0, 0);
	float2 finalSamplePos = float2(0, 0);
	float ray_length = initialStepAmount;
	int numSteps = 0;
	int max_step = 12; // cameraFarPlane/initialStepAmount; 4 * (1.5^10) = 230
	while (numSteps < max_step &&
		(currentPosition.x > 0 && currentPosition.x < 1 &&
			currentPosition.y > 0 && currentPosition.y < 1))
	{
		float2 samplePos = currentPosition.xy;
		float sampleDepth = tex2Dlod(depthSampler, float4(samplePos, 0, 0)).r;

		float currentDepth = cameraSpaceVectorPosition.z;
		float diff = currentDepth - sampleDepth;

		if (diff >= 0 && sampleDepth > 0 && diff <= ray_length)
		{
			// found it, exit the loop
			finalSamplePos.xy = samplePos;
			numSteps = max_step;
		}
		else
		{
			ray_length *= 1.5;
			cameraSpaceVector *= 1.5;	//Each step gets bigger
			cameraSpaceVectorPosition += cameraSpaceVector;

			currentPosition = convertCameraSpaceToScreenSpace(cameraSpaceVectorPosition);
		}
		numSteps++;
	}

	if (finalSamplePos.x != 0 && finalSamplePos.y != 0)
	{
		// compute point color
		float2 texCoord = finalSamplePos.xy;
		color.rgb = GetAlbedoLinear(texCoord);
		color.a = clamp(1 - pow(distance(float2(0.5, 0.5), finalSamplePos.xy)*2.0, 2.0), 0.0, 1.0);
	}
	return color;
}

float CalculateSkylight(in SurfaceStruct surface)
{
	if (surface.category_id == 31)
	{
		// grass 
		return 1.0f;
	}
	else
	{
		const float3 upVector = float3(0, 1.0, 0);
		float skylight = dot(surface.normal, upVector);
		skylight = skylight * 0.4f + 0.6f;
		return skylight;
	}
}

//Calculates direct sunlight without visibility check. mainly depends on surface normal. 
float 	CalculateDirectLighting(in SurfaceStruct surface)
{
	if (surface.category_id == 31)
	{
		// grass 
		return 1.0f;
	}
	else if (surface.category_id == 18)
	{
		// leaves
		// if(NdotL > -0.01)
		// 	return max(0, NdotL);
		// else
		// 	return abs(NdotL) * 0.25;
		return 1.0f;
	}
	else
	{
		// default sun light 
		return max(0, surface.NdotL*0.99 + 0.01);
	}
}

// @return [0,1]: 1 is no shadow(fully visible), 0 is completely in shadow(dark, unvisible)
float 	CalculateSunlightVisibility(inout SurfaceStruct surface, in ShadingStruct shading)
{
	if (RenderOptions.x < 0.99f || rainStrength >= 0.99f) {
		// no shadow when raining
		surface.shadow = 1.0; 
		return 1.0f;
	}
	
	// only apply global sun shadows when there is enough sun light on the material
	if (shading.direct > 0.0f)
	{
		// reconstruct world space vector
		float4 vWorldPosition = float4(surface.cameraSpacePos, 1);
		vWorldPosition = mul(vWorldPosition, matViewInverse);

		surface.shadow = calculateShadowFactor(ShadowMapSampler, vWorldPosition, surface.depth, mShadowMapTex, mShadowMapViewProj, ShadowMapSize.x, ShadowMapSize.y, ShadowRadius);
		return surface.shadow;
	}
	else
	{
		surface.shadow = 0.0;
		return 0.0f;
	}
}

// Function that retrieves the lightmap of light emitted by emissive blocks like torches
// Apply inverse square law and normalize for natural light falloff
// return value is also [0, 1] but applied inverse square law. 
// Note: the precomputed lightmap is fine. if you want to change lightmap of torch yourself, call 
// ParaTerrain.GetBlockAttributeObject():SetField("UseLinearTorchBrightness", shader_method >=3);
float GetLightmapTorch(float lightmap)
{
	lightmap = 1.0f - lightmap;
	lightmap = pow(lightmap, 2.0f);
	lightmap = 1.0f / pow((lightmap * 6 + 0.2f), 2.0f);
	lightmap -= 0.0260; // = 1.0f / pow((1 * 6 + 0.2f), 2.0f);
	lightmap = max(0.0f, lightmap);
	lightmap *= 0.04f;
	return lightmap;
}

//Function that retrieves the lightmap of light emitted by the sky. This is a raw value from 0 (fully dark) to 1 (fully lit) regardless of time of day
float 	GetLightmapSky(float skylight) {
	return pow(skylight, 4.3f);
}

//Function that retrieves the screen space surface normals. Used for lighting calculations
float4  GetNormal(float2 texCoord) {
	float4 norm = tex2D(normalSampler, texCoord);
	return float4(norm.rgb * 2.0 - 1.0, norm.w);
}

/* linear depth in camera space. [0, cameraFarPlane] */
float  GetDepth(float2 texCoord) {
	return tex2D(depthSampler, texCoord).x;
}

float GetSunlightVisibility(float2 coord)
{
	return tex2D(ShadowMapSampler, coord).g;
}

// @param vec2Seed: normally this is texture coordinate.
float noise(float offset, float2 vec2Seed)
{
	float2 coord = vec2Seed + offset.xx;
	float noise = clamp(frac(sin(dot(coord, float2(12.9898f, 78.233f))) * 43758.5453f), 0.0f, 1.0f)*2.0f - 1.0f;
	return noise;
}

//Calculates direct sunlight without visibility check
void CalculateNdotL(inout SurfaceStruct surface)
{
	surface.NdotL = dot(sunDirection, surface.normal);
}

//Mask
void 	CalculateMasks(inout SurfaceStruct surface)
{
	surface.mask_sky = surface.depth < 0.01;
	surface.mask_water = (surface.category_id == 8 || surface.category_id == 9);
	surface.mask_torch = (surface.category_id == 5);
}

//circular sun
// return 1 is sun, 0 is not sun. 
bool CalculateSunspot(inout SurfaceStruct surface)
{
	float3 npos = normalize(surface.CameraEye);
	float3 halfVector2 = normalize(-mul(sunDirection, (float3x3)matView).xyz + npos);
	float sunProximity = 1.0f - dot(halfVector2, npos);
	surface.sky.sunProximity = sunProximity;
	return (sunProximity > 0.96f);
}

void AddSunglow(inout SurfaceStruct surface)
{
	float sunglowFactor = pow(surface.sky.sunProximity, 4.4);
	surface.sky.albedo *= 1.0f + sunglowFactor * (7.0f);
}

// this is not fog, but a very low frequency scattering of fog color over the entire scene. 
void CalculateAtmosphericScattering(inout float3 color, in SurfaceStruct surface)
{
	float3 fogColor = g_FogColor.rgb;
	float fogFactor = pow(surface.depth / 1500.0f, 2.0f);
	// only paint on non-sky area
	fogFactor *= lerp(1.0f, 0.0f, float(surface.mask_sky));
	//add scattered low frequency light
	color += fogColor * fogFactor * 2.0f;
}

// apply fog effect from FogStart to cameraFarPlane
// NOT used: really bad effect. with depth of view, distance fog is not needed. 
void ApplyDistanceFog(inout float3 color, in SurfaceStruct surface)
{
	float3 fogColor = g_FogColor.rgb;
	float fogFactor = clamp((surface.depth - FogStart) / (cameraFarPlane - 16) * 6.0, 0.0, 1.0);
	// only paint on non-sky area
	fogFactor *= lerp(1.0f, 0.0f, float(surface.mask_sky));
	color = lerp(color, fogColor, fogFactor);
}

// do basic surface color calculation here (without reflection)
PSOut CompositePS0(VSOutput input)
{
	//Initialize surface properties required for lighting calculation for any surface that is not part of the sky
	SurfaceStruct surface = (SurfaceStruct)0;
	float2 texCoord = input.texCoord;
	surface.texCoord = texCoord;
	surface.albedo = GetAlbedoLinear(texCoord);
	surface.sky.albedo = surface.albedo;
	surface.albedo = pow(surface.albedo, 1.4f);
	surface.albedo = lerp(surface.albedo, dot(surface.albedo, float1(0.3333f).xxx), 0.035f);
	surface.normal = GetNormal(texCoord);
	surface.depth = GetDepth(texCoord);
	surface.CameraEye = input.CameraEye;
	surface.cameraSpacePos = input.CameraEye * surface.depth;
	// r:category id,  g: sun light value, b: torch light value
	float4 block_info = tex2D(matInfoSampler, texCoord);
	surface.category_id = (int)(block_info.r * 255.0 + 0.4);
	float sun_light_strength = block_info.g;
	float torch_light_strength = block_info.b;

	CalculateMasks(surface);

	//Remove the sky from surface albedo, because sky will be handled separately
	surface.albedo *= 1.0f - float(surface.mask_sky);
	//Initialize sky surface properties
	surface.sky.albedo = surface.sky.albedo * float(surface.mask_sky); //Gets the albedo texture for the sky
	surface.sky.sunSpot = SunColor * (float(CalculateSunspot(surface)) * float(surface.mask_sky));
	surface.sky.sunSpot *= 1.0f - rainStrength;
	surface.sky.sunSpot *= 1.0f - timeMidnight;
	surface.sky.sunSpot *= 100.0f;
	AddSunglow(surface);

	//Initialize original Lightmap values
	RawLightmapStruct rawLightmap;
	rawLightmap.torch = GetLightmapTorch(torch_light_strength);
	rawLightmap.sky = GetLightmapSky(sun_light_strength);

	//Calculate surface shading
	ShadingStruct shading;
	CalculateNdotL(surface);
	float directSunShading = CalculateDirectLighting(surface); //Calculate direct sunlight without visibility check (shadows)
	shading.direct = lerp(CloudThickness, 1.0, directSunShading);
	shading.sunlightVisibility = CalculateSunlightVisibility(surface, shading);
	shading.direct *= lerp(CloudThickness, 1.0, shading.sunlightVisibility);
	shading.direct *= 1.0f - rainStrength;
	shading.direct *= 1.0f - CloudThickness;
	shading.direct *= pow(rawLightmap.sky, 0.1f);
	shading.skylight = CalculateSkylight(surface);

	//Colorize surface shading and store in lightmaps
	LightmapStruct lightmap;
	lightmap.sunlight = SunColor.rgb * shading.direct;
	lightmap.skylight = rawLightmap.sky;
	lightmap.skylight *= shading.skylight;
	//give some ambient sunlight plus some base ambient at night. 
	lightmap.skylight *= (SunColor.rgb*(1.0f - CloudThickness)*2.0 + lerp(1.0, 0.1f, pow(timeMidnight, 0.6)));
	// lightmap.nolight = float3(0.05f, 0.05f, 0.05f);
	// also give torch light some fake shading to make custom model look more dimentional at night. 
	float fakeTorchShading = 1.0;
	if (surface.category_id == 255) {
		fakeTorchShading = (directSunShading * 0.6 + 0.4);
		lightmap.skylight *= fakeTorchShading;
	}
	lightmap.torchlight = (rawLightmap.torch * fakeTorchShading) * TorchLightColor;

	//Apply lightmaps to albedo and generate final shaded surface
	FinalStruct final;
	//final.nolight = surface.albedo * lightmap.nolight;
	final.sunlight = surface.albedo * lightmap.sunlight;
	final.skylight = surface.albedo * lightmap.skylight;
	final.torchlight = surface.albedo * lightmap.torchlight;
	final.glow_torch = surface.albedo * (float(surface.mask_torch) * TorchLightColor);
	// final.glow_torch = pow(final.glow_torch, 2.0);

#ifdef NIGHT_EYE_EFFECT
	float nightEyeAmount = timeMidnight*0.8;
	DoNightEye(final.sunlight, nightEyeAmount);
	DoNightEye(final.skylight, nightEyeAmount);
	DoNightEye(surface.sky.albedo, nightEyeAmount);
	// DoNightEye(final.nolight, 0.8);
#endif

	float3 finalComposite;
	finalComposite = final.sunlight	    * 1.0f					//Add direct sunlight
		+ final.skylight     * 0.05f					//Add ambient skylight
														// + final.nolight	    * 0.03f					//Add base ambient light
		+ final.torchlight   * 2.0					//Add light coming from emissive blocks
		+ final.glow_torch   * 3.0f					// add torch, lamp, lava glow
		;
	//Apply sky to final composite
	// surface.sky.albedo *= lerp(1.0f, 3.0f, timeNoon);
	surface.sky.albedo += surface.sky.sunSpot;
	finalComposite += surface.sky.albedo;

	CalculateAtmosphericScattering(finalComposite, surface);
	// ApplyDistanceFog(finalComposite, surface);

	// Convert final image back into gamma 0.45 space
	finalComposite.rgb = pow(finalComposite.rgb, (1.0f / 2.2f));

	// Scale image down for HDR, only required for integer16, not floating16. 
	// finalComposite.rgb *= 0.01f;

	PSOut o;
	o.Color = float4(finalComposite.rgb, 1.0);
	o.Color2 = float4(0, surface.shadow * pow(rawLightmap.sky, 0.2f), rawLightmap.sky, 1.0);
	return o;
}

float4 ComputeFakeSkyReflection(inout SurfaceStruct2 surface)
{
	// TODO
	return float4(0, 0, 0, 1.0);
}

void CalculateSpecularReflections(inout SurfaceStruct2 surface)
{
	int category_id = surface.category_id;

	surface.mask_sky = surface.depth < 0.01;
	surface.mask_water = (category_id == 8 || category_id == 9);
	surface.mask_metal = (category_id == 50);

	if (surface.mask_water || surface.mask_metal)
	{
		// water is 1 (full), metal is has a week reflective color. 
		float specularity = lerp(1.0, surface.specularity, surface.mask_metal);
		float3 cameraSpaceNormal = mul(surface.normal, (float3x3)matView);
		float4 reflection = ComputeRayTraceReflection(surface.cameraSpacePos, cameraSpaceNormal);
		float4 fakeSkyReflection = ComputeFakeSkyReflection(surface);
		reflection.a = reflection.a * fakeSkyReflection.a * specularity;
		surface.color.xyz = lerp(surface.color.xyz, reflection.rgb, reflection.a);
	}
}


/** sunlight specularity based on sun and eye half vector, and the normal */
void CalculateSpecularHighlight(inout SurfaceStruct2 surface)
{
	if (!surface.mask_sky && !surface.mask_water)
	{
		// everything has some specular light, metal block has more
		// float roughness = lerp(1, 0.5, surface.mask_metal);
		// float gloss = pow(1.01f - roughness, 4.5f);
		float gloss = lerp(0, surface.specularity*0.05, surface.mask_metal);

		float3 cameraSpaceViewDir = -normalize(surface.cameraSpacePos);
		float3 cameraSpaceNormal = mul(surface.normal, (float3x3)matView);
		float3 halfVector = normalize(mul(sunDirection, (float3x3)matView).xyz + cameraSpaceViewDir);
		float HdotN = saturate(dot(halfVector, cameraSpaceNormal));

		const float fresnelPower = 6.0;
		float fresnel = pow(saturate(1.0 - dot(cameraSpaceViewDir, cameraSpaceNormal)), fresnelPower) * 0.98 + 0.02;
		float spec = pow(HdotN, gloss * 5000 + 10.0);
		spec *= fresnel;
		spec *= gloss * 600 + 0.02; // 0.02 is base specular for all blocks.
		spec *= surface.sunlightVisibility;
		spec *= 1.0 - rainStrength;
		float3 specularHighlight = spec * SunColor;

		// For fake torch specular light, we will assume torch light and eye are on the same point, so half vector is actually viewDir.
		if (surface.mask_metal)
		{
			float spec = pow(saturate(dot(cameraSpaceViewDir, cameraSpaceNormal)), 60.0);
			specularHighlight += (TorchLightColor.rgb*pow(surface.torch_light_strength*spec, 3.0));
		}
		surface.color.xyz += specularHighlight;
	}
}

// do water reflection here
float4 CompositePS1(VSOutput input) :COLOR
{
	SurfaceStruct2 surface = (SurfaceStruct2)0;
float2 texCoord = input.texCoord;
surface.texCoord = texCoord;
surface.color = GetAlbedoLinear(texCoord);
surface.sunlightVisibility = GetSunlightVisibility(texCoord);
// get world space normal
float4 normal_ = GetNormal(texCoord);
surface.normal = normal_.xyz;
surface.specularity = 1.0 - normal_.w;
surface.depth = GetDepth(texCoord);
surface.CameraEye = input.CameraEye;
surface.cameraSpacePos = input.CameraEye * surface.depth;
// r:category id,  g: sun light value, b: torch light value
float4 block_info = tex2D(matInfoSampler, texCoord);
surface.category_id = (int)(block_info.r * 255.0 + 0.4);
// float sun_light_strength = block_info.g;
surface.torch_light_strength = block_info.b;

CalculateSpecularReflections(surface);
CalculateSpecularHighlight(surface);

return float4(surface.color.rgb, 1.0);
}

// calculate bloom at given level of detail and write it to a given offset position
float3 CalculateBloom(float2 texcoord, int LOD, float2 offset)
{
	float scale = pow(2.0f, float(LOD));

	float padding = 0.02f;

	if (texcoord.x - offset.x + padding < 1.0f / scale + (padding * 2.0f)
		&& texcoord.y - offset.y + padding < 1.0f / scale + (padding * 2.0f)
		&& texcoord.x - offset.x + padding > 0.0f
		&&  texcoord.y - offset.y + padding > 0.0f) {

		float3 bloom = float1(0.0f).xxx;
		float allWeights = 0.0f;
		const float3 glowThreshold = float3(1.0, 1.0, 1.0);
		for (int i = 0; i < 6; i++) {
			for (int j = 0; j < 6; j++) {
				float weight = 1.0f - distance(float2(i, j), float2(2.5f, 2.5f)) / 3.5; // 3.5 = 0.25*1.414
				weight = 1.0f - cos(weight * 3.1416f / 2.0f);
				weight = pow(weight, 2.0f);
				float2 coord = float2(i - 2.5, j - 2.5);
				coord /= screenParam;

				float2 finalCoord = (texcoord.xy + coord.xy - offset.xy) * scale;
				// glow threshold is set to 
				bloom += max(float3(0, 0, 0), tex2D(colorSampler, finalCoord).rgb - glowThreshold) * weight;
				allWeights += weight;
			}
		}
		bloom /= allWeights;
		return bloom;
	}
	else {
		return float1(0.0f).xxx;
	}

}

// calculate bloom texture (several bloom texture resolutions are calculated in one pass in different locations of the texture) 
float4 CompositePS2(VSOutput input) :COLOR
{
	float2 texCoord = input.texCoord;

	float3 bloom = CalculateBloom(texCoord, 2, float2(0.0f, 0.0f) + float2(0.000f, 0.000f));
	bloom += CalculateBloom(texCoord, 3, float2(0.0f, 0.25f) + float2(0.000f, 0.025f));
	bloom += CalculateBloom(texCoord, 4, float2(0.125f, 0.25f) + float2(0.025f, 0.025f));
	bloom += CalculateBloom(texCoord, 5, float2(0.1875f, 0.25f) + float2(0.050f, 0.025f));
	bloom += CalculateBloom(texCoord, 6, float2(0.21875f, 0.25f) + float2(0.075f, 0.025f));
	bloom += CalculateBloom(texCoord, 7, float2(0.25f, 0.25f) + float2(0.100f, 0.025f));
	bloom += CalculateBloom(texCoord, 8, float2(0.28f, 0.25f) + float2(0.125f, 0.025f));

	return float4(bloom.rgb, 1.0f);
}


// down size to 1/4 of original size. Calculate average color.
float4 GlowDownsizePS(VSOutput input) :COLOR
{
	float2 texcoord = input.texCoord;
	float2 texStep = float2(1.0, 1.0) / screenParam;
	float3 bloom = float3(0.0, 0.0, 0.0);
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			float2 coord = float2(i, j) * texStep;
			float2 finalCoord = (texcoord.xy + coord.xy);
			bloom += tex2D(colorSampler, finalCoord).rgb;
		}
	}
	return float4(bloom.rgb / 16.0, 1.0f);
}


/* the final composition step to tonemap to monitor resolution.
*/
struct VSOutputFinal
{
	float4 pos			: POSITION;         // Screen space position
	float2 texCoord		: TEXCOORD0;        // texture coordinates
};

VSOutputFinal FinalQuadVS(float3 iPosition:POSITION,
	float2 texCoord : TEXCOORD0)
{
	VSOutputFinal o;
	o.pos = float4(iPosition, 1);
	o.texCoord = texCoord + 0.5 / screenParam;
	return o;
}

// get and convert to linear color space (decode gamma)
float3 	GetColorTexture(float2 coord)
{
	return tex2D(compositeSampler, coord).rgb;
}

// value based on SEUS v10.0
float3 DepthOfField(float2 pos)
{
	float cursorDepth = centerDepthSmooth;
	if (cursorDepth == 0.0) {
		// just in case it is first person view. 
		cursorDepth = tex2D(depthSampler, float2(0.5, 0.5)).x;
	}

	const float blurclamp = 0.014;  // max blur amount

	float2 aspectcorrect = float2(1.0, ViewAspect) * 1.5;

	float depth = tex2D(depthSampler, pos).x;
	// depth += float(isHand) * 0.36f;

	float factor = (depth - cursorDepth) / cameraFarPlane;

	float2 dofblur = clamp(factor * DepthOfViewFactor, -blurclamp, blurclamp).xx;

	float3 col = float3(0.0, 0.0, 0.0);
	col += GetColorTexture(pos);

	col += GetColorTexture(pos + (float2(0.0, 0.4)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.15, 0.37)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.29, 0.29)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.37, 0.15)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.4, 0.0)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.37, -0.15)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.29, -0.29)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.15, -0.37)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.0, -0.4)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.15, 0.37)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.29, 0.29)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.37, 0.15)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.4, 0.0)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.37, -0.15)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(-0.29, -0.29)*aspectcorrect) * dofblur);
	col += GetColorTexture(pos + (float2(0.15, -0.37)*aspectcorrect) * dofblur);

	col += GetColorTexture(pos + (float2(0.15, 0.37)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(-0.37, 0.15)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(0.37, -0.15)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(-0.15, -0.37)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(-0.15, 0.37)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(0.37, 0.15)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(-0.37, -0.15)*aspectcorrect) * dofblur*0.9);
	col += GetColorTexture(pos + (float2(0.15, -0.37)*aspectcorrect) * dofblur*0.9);

	col += GetColorTexture(pos + (float2(0.29, 0.29)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(0.4, 0.0)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(0.29, -0.29)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(0.0, -0.4)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(-0.29, 0.29)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(-0.4, 0.0)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(-0.29, -0.29)*aspectcorrect) * dofblur*0.7);
	col += GetColorTexture(pos + (float2(0.0, 0.4)*aspectcorrect) * dofblur*0.7);

	col += GetColorTexture(pos + (float2(0.29, 0.29)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(0.4, 0.0)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(0.29, -0.29)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(0.0, -0.4)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(-0.29, 0.29)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(-0.4, 0.0)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(-0.29, -0.29)*aspectcorrect) * dofblur*0.4);
	col += GetColorTexture(pos + (float2(0.0, 0.4)*aspectcorrect) * dofblur*0.4);

	float3 color = col / 41;
	return color;
}

struct BloomDataStruct
{
	float3 blur0;
	float3 blur1;
	float3 blur2;
	float3 blur3;
	float3 blur4;
	float3 blur5;
	float3 blur6;
	float3 bloom;
};

// Retrieve previously calculated bloom textures
void GetBloom(float2 texcoord, inout BloomDataStruct bloomData) {
	//constants for bloom bloomSlant
	const float    bloomSlant = 0.25f;
	const float bloomWeight[7] = { pow(7.0f, bloomSlant),
		pow(6.0f, bloomSlant),
		pow(5.0f, bloomSlant),
		pow(4.0f, bloomSlant),
		pow(3.0f, bloomSlant),
		pow(2.0f, bloomSlant),
		1.0f
	};

	float2 recipres = float2(1.0, 1.0) / screenParam;
	texcoord -= recipres;

	bloomData.blur0 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 2.0f)) + float2(0.0f, 0.0f) + float2(0.000f, 0.000f)).rgb;
	bloomData.blur1 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 3.0f)) + float2(0.0f, 0.25f) + float2(0.000f, 0.025f)).rgb;
	bloomData.blur2 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 4.0f)) + float2(0.125f, 0.25f) + float2(0.025f, 0.025f)).rgb;
	bloomData.blur3 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 5.0f)) + float2(0.1875f, 0.25f) + float2(0.050f, 0.025f)).rgb;
	bloomData.blur4 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 6.0f)) + float2(0.21875f, 0.25f) + float2(0.075f, 0.025f)).rgb;
	bloomData.blur5 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 7.0f)) + float2(0.25f, 0.25f) + float2(0.100f, 0.025f)).rgb;
	bloomData.blur6 = tex2D(colorSampler, (texcoord.xy) * (1.0f / pow(2.0f, 8.0f)) + float2(0.28f, 0.25f) + float2(0.125f, 0.025f)).rgb;

	bloomData.bloom = bloomData.blur0 * bloomWeight[0];
	bloomData.bloom += bloomData.blur1 * bloomWeight[1];
	bloomData.bloom += bloomData.blur2 * bloomWeight[2];
	bloomData.bloom += bloomData.blur3 * bloomWeight[3];
	bloomData.bloom += bloomData.blur4 * bloomWeight[4];
	bloomData.bloom += bloomData.blur5 * bloomWeight[5];
	bloomData.bloom += bloomData.blur6 * bloomWeight[6];
}

/** blur distance scene if raining. */
void AddRainFogScatter(float2 texcoord, inout float3 color, in BloomDataStruct bloomData)
{
	const float    bloomSlant = 0.0f;
	const float bloomWeight[7] = { pow(7.0f, bloomSlant),
		pow(6.0f, bloomSlant),
		pow(5.0f, bloomSlant),
		pow(4.0f, bloomSlant),
		pow(3.0f, bloomSlant),
		pow(2.0f, bloomSlant),
		1.0f
	};

	float3 fogBlur = bloomData.blur0 * bloomWeight[6] +
		bloomData.blur1 * bloomWeight[5] +
		bloomData.blur2 * bloomWeight[4] +
		bloomData.blur3 * bloomWeight[3] +
		bloomData.blur4 * bloomWeight[2] +
		bloomData.blur5 * bloomWeight[1] +
		bloomData.blur6 * bloomWeight[0];

	float fogTotalWeight = 1.0f * bloomWeight[0] +
		1.0f * bloomWeight[1] +
		1.0f * bloomWeight[2] +
		1.0f * bloomWeight[3] +
		1.0f * bloomWeight[4] +
		1.0f * bloomWeight[5] +
		1.0f * bloomWeight[6];

	fogBlur /= fogTotalWeight;

	float linearDepth = GetDepth(texcoord);

	float fogDensity = 0.023f * (rainStrength);
	float visibility = 1.0f / exp(linearDepth * fogDensity);
	float fogFactor = 1.0f - visibility;
	fogFactor = clamp(fogFactor, 0.0f, 1.0f);
	color = lerp(color, fogBlur, fogFactor);
}

float3 TonemapReinhard_Good(float3 color)
{
	const float averageLuminance = 0.00003f;
	const float contrast = 0.9f;
	float3 value = pow(color.rgb, contrast);
	value = value / (value + EyeBrightness.xxx);
	color.rgb = value;
	return color;
}

void Vignette(inout float3 color, float2 pos)
{
	float dist = distance(pos, float2(0.5, 0.5)) * 2.0f / 1.5142;
	dist = pow(dist, 1.1f);
	color.rgb *= 1.0 - dist;
}

float4 FinalPS(VSOutput input) :COLOR
{
	float2 texCoord = input.texCoord;
	float3 color;
	if (RenderOptions.z >= 2)
		color = DepthOfField(texCoord);
	else
		color = GetColorTexture(texCoord);

	// add bloom 
	BloomDataStruct bloomData;
	GetBloom(texCoord, bloomData);			//Gather bloom textures
	color += bloomData.bloom*0.006f;

	if (rainStrength > 0.01f)
		AddRainFogScatter(texCoord, color, bloomData);

	// apply user defined fog
	float eyeDist = length(input.CameraEye * GetDepth(texCoord));
	if (FogStart < FogEnd)
		color.xyz = lerp(color.xyz, pow(g_FogColor.xyz, 2.2f), 1.0 - clamp((FogEnd - eyeDist) / (FogEnd - FogStart), 0.0, 1.0));

	// vignette effect: darken edges
	Vignette(color, texCoord);

#ifdef SHOW_DEBUG_VIEW
	color = lerp(lerp(bloomData.bloom.rgb, color, float(texCoord.y<0.5)), lerp(tex2D(compositeSampler, texCoord).rgb, tex2D(colorSampler, texCoord).rgb, float(texCoord.y<0.5)), float(texCoord.x<0.5)); // DEBUG: show bloom texture and result
#endif

	color = TonemapReinhard_Good(color);
	//Put color back into gamma space for correct display
	color.rgb = pow(color.rgb, (1.0f / 2.2f));

	return float4(color, 1.0f);
}

float4 CompositeFXAA(VSOutput input) :COLOR
{
	return FxaaPixelShader(
	input.texCoord,							// FxaaFloat2 pos,
		FxaaFloat4(0.0f, 0.0f, 0.0f, 0.0f),		// FxaaFloat4 fxaaConsolePosPos,
		colorSampler,							// FxaaTex tex,
		colorSampler,							// FxaaTex fxaaConsole360TexExpBiasNegOne,
		colorSampler,							// FxaaTex fxaaConsole360TexExpBiasNegTwo,
		1.0 / screenParam,							// FxaaFloat2 fxaaQualityRcpFrame,
		FxaaFloat4(0.0f, 0.0f, 0.0f, 0.0f),		// FxaaFloat4 fxaaConsoleRcpFrameOpt,
		FxaaFloat4(0.0f, 0.0f, 0.0f, 0.0f),		// FxaaFloat4 fxaaConsoleRcpFrameOpt2,
		FxaaFloat4(0.0f, 0.0f, 0.0f, 0.0f),		// FxaaFloat4 fxaaConsole360RcpFrameOpt2,
		0.75f,									// FxaaFloat fxaaQualitySubpix,
		0.166f,									// FxaaFloat fxaaQualityEdgeThreshold,
		0.0833f,								// FxaaFloat fxaaQualityEdgeThresholdMin,
		0.0f,									// FxaaFloat fxaaConsoleEdgeSharpness,
		0.0f,									// FxaaFloat fxaaConsoleEdgeThreshold,
		0.0f,									// FxaaFloat fxaaConsoleEdgeThresholdMin,
		FxaaFloat4(0.0f, 0.0f, 0.0f, 0.0f)		// FxaaFloat fxaaConsole360ConstDir,
		);
}

technique Default_Normal
{
	pass P0
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		VertexShader = compile vs_3_0 CompositeQuadVS();
		PixelShader = compile ps_3_0 CompositePS0();
	}
	pass P1
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		VertexShader = compile vs_3_0 CompositeQuadVS();
		PixelShader = compile ps_3_0 CompositePS1();
	}
	pass P2
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		VertexShader = compile vs_3_0 CompositeQuadVS();
		PixelShader = compile ps_3_0 CompositePS2();
	}
	pass P3
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		VertexShader = compile vs_3_0 CompositeQuadVS();
		PixelShader = compile ps_3_0 FinalPS();
	}
	pass P4
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		VertexShader = compile vs_3_0 FinalQuadVS();
		PixelShader = compile ps_3_0 GlowDownsizePS();
	}
	pass P5
	{
		cullmode = none;
		ZEnable = false;
		ZWriteEnable = false;
		FogEnable = False;
		AlphaBlendEnable = false;
		VertexShader = compile vs_3_0 CompositeQuadVS();
		PixelShader = compile ps_3_0 CompositeFXAA();
	}
}

```