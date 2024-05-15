```lua

--[[
Title: TerrainBrush
Author(s): LiXizhi
Date: 2009/1/31
Desc: terrain form brush data structure only. Keeping the dafault brush settings. 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Env/TerrainBrush.lua");
brush = MyCompany.Aries.Creator.TerrainBrush:new({})
-- well known brushes
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["GaussionHill"]
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["Flatten"]
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["RadialScale"]
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["Roughen_Smooth"]
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["SetHole"]
brush = MyCompany.Aries.Creator.TerrainBrush.Brushes["Ramp"]
------------------------------------------------------------
]]

NPL.load("(gl)script/apps/Aries/Creator/Env/TerrainBrushMarker.lua");
local TerrainBrushMarker = commonlib.gettable("MyCompany.Aries.Creator.TerrainBrushMarker");

local TerrainBrush = {
	filtername = nil,
	BrushSize = 10, 
	BrushStrength = 0.1,
	BrushSoftness = 0.5,
	
	FlattenOperation = 2,
	Elevation = 0,
	gaussian_deviation = 0.9,
	HeightScale = 3,
};
commonlib.setfield("MyCompany.Aries.Creator.TerrainBrush", TerrainBrush)

function TerrainBrush:new (o)
	o = o or {}   -- create object if user does not provide one
	setmetatable(o, self)
	self.__index = self
	return o
end

-- refresh the terrain marker
function TerrainBrush:RefreshMarker()
	if(self.filtername ~= nil) then
		TerrainBrushMarker.DrawBrush({x=self.x,y=self.y,z=self.z,radius=self.BrushSize});
	end	
end

-- clear the terrain marker
function TerrainBrush:ClearMarker()
	TerrainBrushMarker.Clear();
end

-- some known brushes
TerrainBrush.Brushes= {
	["GaussionHill"] = TerrainBrush:new({
			filtername = "GaussianHill",
			BrushSize = 10, 
			BrushStrength = 0.1,
			BrushSoftness = 0.5,
			gaussian_deviation = 0.9,
			HeightScale = 3,
		}),
	["Flatten"] = TerrainBrush:new({
			filtername = "Flatten",
			BrushSize = 5, 
			BrushStrength = 0.1,
			BrushSoftness = 0.5,
			
			FlattenOperation = 2,
			Elevation = 0,
		}),
	["Roughen_Smooth"] = TerrainBrush:new({
			filtername = "Roughen_Smooth",
			BrushSize = 4, 
			BrushStrength = 0.1,
			BrushSoftness = 0.5,
		}),
	["RadialScale"] = TerrainBrush:new({
			filtername = "RadialScale",
			BrushSize = 20, 
			BrushStrength = 0.1,
			BrushSoftness = 0.5,
			HeightScale = 3,
		}),
	["SetHole"] = TerrainBrush:new({
			filtername = "SetHole",
			BrushSize = 2, 
			BrushStrength = 0.1,
			BrushSoftness = 0.5,
		}),
	["Ramp"] = TerrainBrush:new({
			filtername = "SetHole",
			filtername = "Ramp",
			BrushSize = 5, 
			BrushStrength = 0.3,
			BrushSoftness = 0.1,
		}),	
}

-- overwrite the marker function
function TerrainBrush.Brushes.Ramp:RefreshMarker()
	if(self.filtername ~= nil) then
		TerrainBrushMarker.DrawRamp({x1=self.x1,z1=self.z1,x=self.x,z=self.z,radius=self.BrushSize});
	end	
end


--[[
Title: Terrain Brush Manipulator
Author(s): LiXizhi@yeah.net
Date: 2016/7/15
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushManipContainer.lua");
local TerrainBrushManipContainer = commonlib.gettable("MyCompany.Aries.Game.Manipulators.TerrainBrushManipContainer");
local manipCont = TerrainBrushManipContainer:new();
manipCont:init();
self:AddManipulator(manipCont);
manipCont:connectToDependNode(entity);
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Scene/Manipulators/ManipContainer.lua");
local Plane = commonlib.gettable("mathlib.Plane");
local vector3d = commonlib.gettable("mathlib.vector3d");
local ShapesDrawer = commonlib.gettable("System.Scene.Overlays.ShapesDrawer");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine");
local TerrainBrushManipContainer = commonlib.inherit(commonlib.gettable("System.Scene.Manipulators.ManipContainer"), commonlib.gettable("MyCompany.Aries.Game.Manipulators.TerrainBrushManipContainer"));
TerrainBrushManipContainer:Property({"Name", "TerrainBrushManipContainer", auto=true});
TerrainBrushManipContainer:Property({"EnablePicking", false});
TerrainBrushManipContainer:Property({"PenWidth", 0.01});
TerrainBrushManipContainer:Property({"showGrid", true, "IsShowGrid", "SetShowGrid", auto=true});
TerrainBrushManipContainer:Property({"mainColor", "#ffff00"});
-- attribute name for position on the dependent node that we will bound to. it should be vector3d type like {0,0,0}
TerrainBrushManipContainer:Property({"PositionPlugName", "position", auto=true});
TerrainBrushManipContainer:Property({"RadiusPlugName", "pen_radius", auto=true});

function TerrainBrushManipContainer:ctor()
	self:AddValue("position", {0,0,0});
end

function TerrainBrushManipContainer:createChildren()
	-- self.scaleManip = self:AddScaleManip();
	-- self.translateManip = self:AddTranslateManip();
end

function TerrainBrushManipContainer:paintEvent(painter)
	TerrainBrushManipContainer._super.paintEvent(self, painter);
	
	local isDrawingPickable = self:IsPickingPass();
	if(isDrawingPickable) then
		return;
	end

	painter:SetPen(self.pen);

	self:SetColorAndName(painter, self.mainColor);

	local x,y,z = self:GetPosition();
	local radius = self:GetRadius();
	ShapesDrawer.DrawCircle(painter, 0, 0, 0, radius * BlockEngine.blocksize, "y", false, 8);

	-- TODO: draw more accurate border & hint according to terrain blocks.
	local cx, cy, cz = BlockEngine:block(x,y-0.1,z);

	-- show grid line
	if(self:IsShowGrid()) then
		-- self:SetColorAndName(painter, self.gridColor);
		local moveDir = self:GetMoveDirByAxis();
		for i=0, radius do
			local gx = moveDir[1]*i*BlockEngine.blocksize;
			local gy = moveDir[2]*i*BlockEngine.blocksize;
			local gz = moveDir[3]*i*BlockEngine.blocksize;
			ShapesDrawer.DrawCube(painter, gx, gy, gz, 0.02, true);
		end
		if(self.isDrawRadiusText) then
			painter:PushMatrix();
			painter:TranslateMatrix(0,1,0);
			painter:LoadBillboardMatrix();
			painter:DrawTextScaled(0, 0, format("r=%s",radius), self.textScale*2);
			painter:PopMatrix();
		end
	end
end

local axis_dirs = {
	x = vector3d:new({-1,0,0}),
	y = vector3d:new({0,1,0}),
	z = vector3d:new({0,0,1}),
}
-- @param axis: "x|y|z". default to x
-- @return vector3d
function TerrainBrushManipContainer:GetMoveDirByAxis(axis)
	return axis_dirs[axis or "x"];
end


function TerrainBrushManipContainer:GetRadius()
	local radius;
	if(self.node and self.node.GetPenRadius) then
		radius = self.node:GetPenRadius();
	end
	return radius or 1;
end

function TerrainBrushManipContainer:OnValueChange(name, value)
	TerrainBrushManipContainer._super.OnValueChange(self);
	if(name == "position") then
		self:SetPosition(unpack(value));
	end
end

-- @param node: it should be ItemTerrainBrush object. 
function TerrainBrushManipContainer:connectToDependNode(node)
	local plugPos = node:findPlug(self.PositionPlugName);
	local plugScale = node:findPlug(self.RadiusPlugName);

	self.node = node;

	if(plugPos and plugScale) then
		-- one way binding 
		local manipPosPlug = self:findPlug("position");
		self:addPlugToManipConversionCallback(manipPosPlug, function(self, manipPlug)
			return plugPos:GetValue():clone();
		end);

		-- two-way binding for scaling(pen_radius) conversion:
		--local manipScalePlug = self.scaleManip:findPlug("scaling");
		--self:addManipToPlugConversionCallback(plugScale, function(self, plug)
			--return manipScalePlug:GetValue();
		--end);
		--self:addPlugToManipConversionCallback(manipScalePlug, function(self, manipPlug)
			--local scaling = plugScale:GetValue() or 1;
			--if(type(scaling) == "number") then
				--scaling = {scaling, scaling, scaling};
			--end
			--return scaling;
		--end);
	end
	-- should be called only once after all conversion callbacks to setup real connections
	self:finishAddingManips();
	TerrainBrushManipContainer._super.connectToDependNode(self, node);
end

--[[
Title: TerrainBrush Task/Command
Author(s): LiXizhi
Date: 2016/7/16
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushTask.lua");
local TerrainBrushTask = commonlib.gettable("MyCompany.Aries.Game.Tasks.TerrainBrushTask");
local task = TerrainBrushTask:new();
task:Run();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/UndoManager.lua");
NPL.load("(gl)script/ide/math/vector.lua");
NPL.load("(gl)script/ide/System/Windows/Keyboard.lua");
local Keyboard = commonlib.gettable("System.Windows.Keyboard");
local UndoManager = commonlib.gettable("MyCompany.Aries.Game.UndoManager");
local vector3d = commonlib.gettable("mathlib.vector3d");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")

local TerrainBrushTask = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Task"), commonlib.gettable("MyCompany.Aries.Game.Tasks.TerrainBrushTask"));

local groupindex_hint = 6; 

local curInstance;

-- this is always a top level task. 
TerrainBrushTask.is_top_level = true;

TerrainBrushTask.default_toolname = "raise";

TerrainBrushTask.tools = {
    {name="raise", tooltip=L"提升地形, 按住Shift点击为下降", icon="Texture/blocks/items/raise.png"},
    {name="smooth", tooltip=L"平滑地形, 按住Shift点击为锐化", icon="Texture/blocks/items/rough.png"},
    {name="flatten", tooltip=L"铲平地形", icon="Texture/blocks/items/flatten.png"},
	{name="flood", tooltip=L"按住左键并拖动填充水, 按住Shift可移除水", icon="Texture/blocks/items/waterfeet.png"},
	{name="remove", tooltip=L"删除表层方块", icon="Texture/blocks/items/wood_axe.png"},
}

function TerrainBrushTask:ctor()
	self.position = vector3d:new(0,0,0);
end

function TerrainBrushTask:Init(item)
	self.item = item;
	return self;
end

local page;
function TerrainBrushTask.InitPage(Page)
	page = Page;
end

-- get current instance
function TerrainBrushTask.GetInstance()
	return curInstance;
end

function TerrainBrushTask.OnClickTool(name)
	local self = curInstance;
	self:SelectToolByName(name);
	if(page) then
		page:Refresh(0.01);
	end
end

function TerrainBrushTask.OnChangeStrength(actualText)
	local self = curInstance;
    actualText = tonumber(actualText);
    self:SetBrushStrength(actualText);
end

function TerrainBrushTask:SelectToolByName(name)
	local self = curInstance;
	self.item:SetToolName(name);
end

function TerrainBrushTask:GetRadius()
	return self.item:GetPenRadius();
end

function TerrainBrushTask:GetBrushStrength()
	return self.item and self.item:GetBrushStrength() or 0.5;
end

function TerrainBrushTask:SetBrushStrength(value)
	value = tonumber(value);
	if(value and value>=0 and value<=1) then
		return self.item and self.item:SetBrushStrength(value);
	end
end


function TerrainBrushTask.GetTools()
	return (curInstance or TerrainBrushTask).tools;
end

function TerrainBrushTask:GetCurrentToolIcon()
	local name = self:GetToolName();
	for i, tool in self.GetTools() do
		if(tool.name == name) then
			return tool.icon;
		end
	end
end

function TerrainBrushTask:GetToolName()
	return self.item:GetToolName() or self.default_toolname;
end

function TerrainBrushTask:CreateToolTask()
	NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainFilterTask.lua");
	local task = MyCompany.Aries.Game.Tasks.TerrainFilter:new()
	-- TODO: get TerrainFilterTask object and initialize with current tool settings
	return task;
end

function TerrainBrushTask:GetToolTask()
	return self.tool_task;
end

-- do operation at given block position with current selected tool
function TerrainBrushTask:BeginOperation()
	self:EndOperation();
	self.tool_task = self:CreateToolTask();
	self.last_step_time = 0;
	self.begin_x, self.begin_y, self.begin_z = self:GetCenterBlockPos();
	self.begin_side = self.last_side;
	self.timer = self.timer or commonlib.Timer:new({callbackFunc = function(timer)
		if(self:GetToolTask()) then
			if(self:UpdateCenterPosition()) then
				self:StepOperation();
			end
		end
	end})
	self.timer:Change(200,200);
end

function TerrainBrushTask:GetCenterBlockPos()
	local x, y, z = unpack(self.item:GetPosition());
	x,y,z = BlockEngine:block(x, y-0.1, z);
	return x,y,z;
end

-- Must be called between BeginOperation and EndOperation to perform one step of the operation. 
function TerrainBrushTask:StepOperation()
	local task = self:GetToolTask();
	if(not task or not self.item) then return end

	local x, y, z = self:GetCenterBlockPos();

	local block_template = BlockEngine:GetBlock(x,y,z);
	if(not block_template) then
		return;
	end

	local curTime = ParaGlobal.timeGetTime();
	if(curTime > (self.last_step_time or 0) + (task.step_duration or 300)) then
		self.last_step_time = curTime;
	else
		return;
	end

	local toolname = self:GetToolName();
	if(toolname == "flatten") then
		if(Keyboard:IsShiftKeyPressed()) then
			task:Flatten(task.FlattenOperation.ShaveTop_Op, self.begin_y or y, x, z, self:GetRadius(), self:GetBrushStrength());
		else
			task:Flatten(task.FlattenOperation.Fill_Op, self.begin_y or y, x, z, self:GetRadius(), self:GetBrushStrength());
		end
	elseif(toolname == "raise") then
		if(Keyboard:IsShiftKeyPressed()) then
			-- lower
			task:GaussianHill(y, x, z, self:GetRadius(), -0.5, self:GetBrushStrength(), 0.6);
		else
			-- raise
			task:GaussianHill(y, x, z, self:GetRadius(), 0.5, self:GetBrushStrength(), 0.6);
		end
	elseif(toolname == "smooth") then
		if(Keyboard:IsShiftKeyPressed()) then
			-- roughen
			task:Roughen_Smooth(y, x, z, self:GetRadius(), true, 4, self:GetBrushStrength());
		else
			-- smooth
			task:Roughen_Smooth(y, x, z, self:GetRadius(), false, 4, self:GetBrushStrength());
		end
	elseif(toolname == "paint") then
		local block_id = self:GetSelectedBlockId();
		local block_template = block_types.get(block_id);
		if(block_template and block_template:isNormalCube()) then
			task:PaintBlocks(task.PaintOperation.Replace_Op, self:GetSelectedBlockId(), self:GetSelectedBlockData(), x, y, z, self:GetRadius(), self:GetBrushStrength());
		else
			task:PaintBlocks(task.PaintOperation.Ontop_Op, self:GetSelectedBlockId(), self:GetSelectedBlockData(), x, y, z, self:GetRadius(), self:GetBrushStrength());
		end
	elseif(toolname == "remove") then
		task:PaintBlocks(task.PaintOperation.Replace_Op, 0, nil, x, y, z, self:GetRadius(), 1);
	elseif(toolname == "flood") then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/WaterFloodTask.lua");
		x,y,z = BlockEngine:GetBlockIndexBySide(x, self.begin_y or y, z, self.begin_side)
		if(Keyboard:IsShiftKeyPressed()) then
			-- unflood
			local task = MyCompany.Aries.Game.Tasks.WaterFlood:new({blockX = x,blockY = y, blockZ = z, fill_id = 0, radius = self:GetRadius()})
			task:Run();
		else
			-- flood
			local task = MyCompany.Aries.Game.Tasks.WaterFlood:new({blockX = x,blockY = y, blockZ = z, fill_id = nil, radius = self:GetRadius()})
			task:Run();
		end
	elseif(toolname == "flood_paint") then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/WaterFloodTask.lua");
		x,y,z = BlockEngine:GetBlockIndexBySide(x, self.begin_y or y, z, self.begin_side)
		local task = MyCompany.Aries.Game.Tasks.WaterFlood:new({blockX = x,blockY = y, blockZ = z, fill_id = self:GetSelectedBlockId(), radius = self:GetRadius()})
		task:Run();
	end
end

function TerrainBrushTask:GetSelectedBlockId()
	return self.item and self.item:GetSelectedBlockId();
end

function TerrainBrushTask:GetSelectedBlockData()
	return self.item and self.item:GetSelectedBlockData();
end

function TerrainBrushTask:EndOperation()
	if(self.timer) then
		self.timer:Change();
	end
	if(self.tool_task) then
		self.tool_task:AddToUndoManager();
		self.tool_task = nil;
	end
	self.begin_x, self.begin_y, self.begin_z = nil, nil, nil;
	self.begin_side = nil;
end

function TerrainBrushTask:Run()
	curInstance = self;
	GameLogic.SetStatus(L"+/-键或Shift+滚轮改变半径");
	self.finished = false;
	self:LoadSceneContext();
	self:GetSceneContext():setMouseTracking(true);
	self:GetSceneContext():setCaptureMouse(true);
	self:SelectToolByName(self:GetToolName());
	self:ShowPage();
end

function TerrainBrushTask:OnExit()
	self:EndOperation();
	GameLogic.SetStatus(nil);
	self:SetFinished();
	ParaTerrain.DeselectAllBlock();
	self:UnloadSceneContext();
	self:CloseWindow();
	curInstance = nil;
end

function TerrainBrushTask:UpdateManipulators()
	self:DeleteManipulators();

	NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushManipContainer.lua");
	local TerrainBrushManipContainer = commonlib.gettable("MyCompany.Aries.Game.Manipulators.TerrainBrushManipContainer");
	local manipCont = TerrainBrushManipContainer:new();
	manipCont:init();
	self:AddManipulator(manipCont);
	manipCont:connectToDependNode(self.item);
end

function TerrainBrushTask:Redo()
end

function TerrainBrushTask:Undo()
end

function TerrainBrushTask:ShowPage()
	local window = self:CreateGetToolWindow();
	window:Show({
		name="TerrainBrushTask", 
		url="script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushTask.html",
		alignment="_ctb", left=0, top=-55, width = 256, height = 64,
	});
end

function TerrainBrushTask:PickBlockAtMouse(result)
	local result = result or Game.SelectionManager:MousePickBlock(true, false, false);
	if(result.blockX) then
		local x,y,z = result.blockX,result.blockY,result.blockZ;
		local block_id, block_data = BlockEngine:GetBlockFull(x,y,z);
		if(block_id and block_id>0) then
			self.item:SetSelectedBlockId(block_id);
			self.item:SetSelectedBlockData(block_data);
		end
	end
end

function TerrainBrushTask:mousePressEvent(event)
	if(not GameLogic.GameMode:IsEditor()) then
		return;
	end
	if(event:button() == "left") then
		if(self:UpdateCenterPosition()) then
			if(event.alt_pressed and not event.shift_pressed) then
				self:PickBlockAtMouse();
			else
				self:BeginOperation();
				self:StepOperation(x,y,z);
			end
		end
		event:accept();
	else
		self:GetSceneContext():mousePressEvent(event);
	end
end

-- return true if position is set at current mouse position. 
function TerrainBrushTask:UpdateCenterPosition()
	local result = Game.SelectionManager:MousePickBlock(true, false, false);
	if(result.blockX) then
		local x,y,z = result.blockX,result.blockY,result.blockZ;
		local rx, ry, yz = BlockEngine:real_top(x,y,z);
		self.position:set(rx, ry, yz);
		self.item:SetPosition(self.position);
		self.last_side = result.side;
		return true;
	end
end

function TerrainBrushTask:mouseReleaseEvent(event)
	if(event:button() == "left") then
		self:EndOperation();
		event:accept();
	else
		self:GetSceneContext():mouseReleaseEvent(event);
	end
end

function TerrainBrushTask:mouseMoveEvent(event)
	if(self:UpdateCenterPosition()) then
		event:accept();
	else
		self:GetSceneContext():mouseMoveEvent(event);
	end
end

function TerrainBrushTask:mouseWheelEvent(event)
	if(event.shift_pressed) then
		-- shift+mousewheel to change radius size
		local delta = event:GetDelta();
		-- radius
		self.item:SetPenRadius(self.item:GetPenRadius()*(delta>0 and 1.1 or 0.9));
		event:accept();
	else
		self:GetSceneContext():mouseWheelEvent(event);
	end
end

function TerrainBrushTask:keyPressEvent(event)
	local dik_key = event.keyname;
	if(dik_key == "DIK_ADD" or dik_key == "DIK_EQUALS") then
		-- increase radius
		self.item:SetPenRadius(self.item:GetPenRadius()*1.1);
	elseif(dik_key == "DIK_SUBTRACT" or dik_key == "DIK_MINUS") then
		-- decrease radius
		self.item:SetPenRadius(self.item:GetPenRadius()*0.9);
	elseif(dik_key == "DIK_Z")then
		UndoManager.Undo();
	elseif(dik_key == "DIK_Y")then
		UndoManager.Redo();
	elseif(dik_key == "DIK_ESCAPE")then
		self:OnExit();
		return;
	end
	self:GetSceneContext():keyPressEvent(event);
end

--[[
Title: ItemPaintBrush
Author(s): LiXizhi
Date: 2017/7/20
Desc: paint with current selected pen.

Usage:
   * alt + left mouse click: pick the current mouse block.
   * +/- key or shift+mousewheel: change radius size

use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemPaintBrush.lua");
local ItemPaintBrush = commonlib.gettable("MyCompany.Aries.Game.Items.ItemPaintBrush");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemTerrainBrush.lua");
local ItemTerrainBrush = commonlib.gettable("MyCompany.Aries.Game.Items.ItemTerrainBrush");
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")

local ItemPaintBrush = commonlib.inherit(ItemTerrainBrush, commonlib.gettable("MyCompany.Aries.Game.Items.ItemPaintBrush"));

block_types.RegisterItemClass("ItemPaintBrush", ItemPaintBrush);

-- initial pen radius
ItemPaintBrush.min_radius = 0.5;
ItemPaintBrush.max_radius = 32;

function ItemPaintBrush:ctor()
end

function ItemPaintBrush:CreateTask(itemStack)
	NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/PaintBrushTask.lua");
	local PaintBrushTask = commonlib.gettable("MyCompany.Aries.Game.Tasks.PaintBrushTask");
	return PaintBrushTask:new():Init(self);
end

-- virtual: draw icon with given size at current position (0,0)
-- @param width, height: size of the icon
-- @param itemStack: this may be nil. or itemStack instance. 
function ItemPaintBrush:DrawIcon(painter, width, height, itemStack)
	local icon = self:GetSelectedBlockIcon(itemStack);
	if(icon) then
		painter:SetPen("#ffffff");
		painter:DrawRectTexture(0, 0, width, height, icon);
	end
	ItemPaintBrush._super.DrawIcon(self, painter, width, height, itemStack);
end

--[[
Title: TerrainBrushMarker
Author(s): LiXizhi
Company: ParaEnging Co. & Taomee Inc.
Date: 2010/1/26
Desc: miniscenegraph for rendering terrain brush. 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Env/TerrainBrushMarker.lua");
local TerrainBrushMarker = MyCompany.Aries.Creator.TerrainBrushMarker;
TerrainBrushMarker.DrawBrush({x,z,radius});
TerrainBrushMarker.Clear()
------------------------------------------------------------
]]

local TerrainBrushMarker = commonlib.gettable("MyCompany.Aries.Creator.TerrainBrushMarker")

TerrainBrushMarker.Assets = {
	["center"] = "model/common/editor/z.x",
	["point"] = "model/common/editor/scalebox.x",
	["cell_region"] = "model/06props/v5/03quest/AchievementBrand/AchievementBrand.x",
	--["cell_region"] = "model/common/editor/z.x",
}
-- how many point to draw for the circle 
TerrainBrushMarker.CirclePointCount = 12;
TerrainBrushMarker.MinCirclePointCount = 12;
TerrainBrushMarker.MaxCirclePointCount = 36;
-- distance between markers in meters
TerrainBrushMarker.MakerSpacing = 1.0;

TerrainBrushMarker.CellSize = 64;
TerrainBrushMarker.CellCenterX = 0;
TerrainBrushMarker.CellCenterY = 0;

local brush = {
	x=nil,
	y=nil,
	z=nil,
	radius=nil,
}

local elapsedTime=0;
local mytimer = commonlib.Timer:new({callbackFunc = function(timer)
	local miniscene = ParaScene.GetMiniSceneGraph("TerrainBrushMarker");
	if(miniscene:IsVisible()) then
		-- move an object
		local obj = miniscene:GetObject("cell_region");
		if(obj:IsValid() and obj:IsVisible()) then
			-- move a particle around a border. 
			elapsedTime = elapsedTime + 0.05;
			--local x = TerrainBrushMarker.CellCenterX+math.cos(elapsedTime)*6;
			--local z = TerrainBrushMarker.CellCenterY+math.sin(elapsedTime)*6;
			local x, z = TerrainBrushMarker.CellCenterX, TerrainBrushMarker.CellCenterY
			local y = ParaTerrain.GetElevation(x, z)+math.sin(2*elapsedTime)*2+2;
			obj:SetPosition(x, y, z);
		else
			-- kill the timer
			timer:Change(nil,nil)
		end
	else
		-- kill the timer
		timer:Change(nil,nil)
	end
end})

-- show texture cell region by location. It will highlight the closest cell region near point(x,y)
-- @param bShow: if true to show. false to hide. 
-- @param x: x position in world unit. if nil, current player location is used. 
-- @param y: y position in world unit. 
function TerrainBrushMarker.ShowTextureCellRegion(bShow, x,y,z)
	local miniscene = ParaScene.GetMiniSceneGraph("TerrainBrushMarker");
	if(bShow) then
		miniscene:SetVisible(true);
	end
	
	if(x == nil or z ==nil) then
		x,y,z = ParaScene.GetPlayer():GetPosition();
	end	
	
	local obj = ParaTerrain.GetAttributeObjectAt(x,z);
	if(obj:IsValid()) then
		local cell_size = obj:GetField("Size", 500)/8;
		TerrainBrushMarker.CellSize = cell_size;
		x = math.floor(x/cell_size)*cell_size + cell_size/2;
		z = math.floor(z/cell_size)*cell_size + cell_size/2;
		TerrainBrushMarker.CellCenterX = x;
		TerrainBrushMarker.CellCenterY = z;
	end
	y = ParaTerrain.GetElevation(x, z);
	
	local obj = miniscene:GetObject("cell_region");
	if(not obj:IsValid()) then
		local _asset = ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["cell_region"]);
		obj = ParaScene.CreateMeshPhysicsObject("cell_region", _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
		obj:SetFacing(0);
		obj:GetAttributeObject():SetField("progress", 1);
		obj:SetPosition(x,y,z);
		miniscene:AddChild(obj);
	else
		obj:SetPosition(x,y,z);
	end
	if(obj:IsValid()) then
		obj:SetVisible(bShow);
		if(bShow) then
			mytimer:Change(0,30)
		else
			mytimer:Change(nil,nil)
		end
	end	
end

-- called to init page
-- @param brush: {x,z,radius}, all fields are optional. it will partial copy to brush struct
function TerrainBrushMarker.DrawBrush(newBrush)
	commonlib.partialcopy(brush, newBrush);
	
	local miniscene = ParaScene.GetMiniSceneGraph("TerrainBrushMarker");
	miniscene:SetVisible(true);
	if(brush.x and brush.z and brush.radius) then
		local y = ParaTerrain.GetElevation(brush.x, brush.z)
		local obj = miniscene:GetObject("center");
		if(obj:IsValid() == false) then
			local _asset = ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["center"]);
			obj = ParaScene.CreateMeshPhysicsObject("center", _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
			obj:SetFacing(0);
			obj:GetAttributeObject():SetField("progress", 1);
			obj:SetPosition(brush.x, y, brush.z);
			miniscene:AddChild(obj);
		else
			obj:SetPosition(brush.x, y, brush.z);
		end
		
		-- automatically determine how many maker to use. 
		local markerCount = math.floor(brush.radius*6.28/TerrainBrushMarker.MakerSpacing)
		if(markerCount>TerrainBrushMarker.MaxCirclePointCount) then
			markerCount = TerrainBrushMarker.MaxCirclePointCount
		elseif(markerCount<TerrainBrushMarker.MinCirclePointCount) then
			markerCount = TerrainBrushMarker.MinCirclePointCount
		end	
		TerrainBrushMarker.CirclePointCount = markerCount;
		
		local i;
		local _asset;
		for i=1,TerrainBrushMarker.CirclePointCount do
			local angle = (i/TerrainBrushMarker.CirclePointCount)*6.28;
			local x = brush.x + brush.radius * math.sin(angle);
			local z = brush.z + brush.radius * math.cos(angle);
			local y = ParaTerrain.GetElevation(x, z)
			
			local obj = miniscene:GetObject(tostring(i));
			if(obj:IsValid() == false) then
				_asset = _asset or ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["point"]);
				obj = ParaScene.CreateMeshPhysicsObject(tostring(i), _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
				obj:SetFacing(0);
				obj:GetAttributeObject():SetField("progress", 1);
				obj:SetPosition(x, y, z);
				miniscene:AddChild(obj);
			else
				obj:SetVisible(true);
				obj:SetPosition(x, y, z);
			end
		end
		if(TerrainBrushMarker.CirclePointCount < TerrainBrushMarker.MaxCirclePointCount ) then
			for i=TerrainBrushMarker.CirclePointCount+1,TerrainBrushMarker.MaxCirclePointCount do
				local obj = miniscene:GetObject(tostring(i));
				if(obj:IsValid()) then
					obj:SetVisible(false);
				else
					break;
				end
			end
		end
	end	
end

-- brush line and circle from (x1,z1) to (x,z)
function TerrainBrushMarker.DrawRamp(brush)
	local miniscene = ParaScene.GetMiniSceneGraph("TerrainBrushMarker");
	miniscene:SetVisible(true);
	if(brush.x1 and brush.z1 and brush.x and brush.z and brush.radius) then
		local y = ParaTerrain.GetElevation(brush.x, brush.z)
		local obj = miniscene:GetObject("center");
		if(obj:IsValid() == false) then
			local _asset = ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["center"]);
			obj = ParaScene.CreateMeshPhysicsObject("center", _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
			obj:SetFacing(0);
			obj:GetAttributeObject():SetField("progress", 1);
			obj:SetPosition(brush.x, y, brush.z);
			miniscene:AddChild(obj);
		else
			obj:SetPosition(brush.x, y, brush.z);
		end
		
		-- automatically determine how many maker to use. 
		local markerCount = math.floor(brush.radius*6.28/TerrainBrushMarker.MakerSpacing)
		if(markerCount>TerrainBrushMarker.MaxCirclePointCount/2) then
			markerCount = TerrainBrushMarker.MaxCirclePointCount/2
		elseif(markerCount<TerrainBrushMarker.MinCirclePointCount) then
			markerCount = TerrainBrushMarker.MinCirclePointCount
		end	
		TerrainBrushMarker.CirclePointCount = markerCount;
		
		local i;
		local _asset;
		for i=1,markerCount do
			local angle = (i/markerCount)*6.28;
			local x = brush.x + brush.radius * math.sin(angle);
			local z = brush.z + brush.radius * math.cos(angle);
			local y = ParaTerrain.GetElevation(x, z)
			
			local obj = miniscene:GetObject(tostring(i));
			if(obj:IsValid() == false) then
				_asset = _asset or ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["point"]);
				obj = ParaScene.CreateMeshPhysicsObject(tostring(i), _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
				obj:SetFacing(0);
				obj:GetAttributeObject():SetField("progress", 1);
				obj:SetPosition(x, y, z);
				miniscene:AddChild(obj);
			else
				obj:SetVisible(true);
				obj:SetPosition(x, y, z);
			end
		end
		if(TerrainBrushMarker.CirclePointCount < TerrainBrushMarker.MaxCirclePointCount ) then
			if(brush.x1~=brush.x or brush.z1~=brush.z) then
				-- now draw a line
				local lineLength = math.sqrt((brush.x1-brush.x)*(brush.x1-brush.x)+(brush.z1-brush.z)*(brush.z1-brush.z))
				
				local markerLeftCount = TerrainBrushMarker.MaxCirclePointCount - TerrainBrushMarker.CirclePointCount-1;
				local markerCount = math.floor(lineLength/TerrainBrushMarker.MakerSpacing)
				if(markerCount>markerLeftCount) then
					markerCount = markerLeftCount
				end	
				for i=1,markerCount do
					local k = (i-1)/markerCount;
					local x = brush.x1 + (brush.x-brush.x1) * k;
					local z = brush.z1 + (brush.z-brush.z1) * k;
					local y = ParaTerrain.GetElevation(x, z)
			
					local objname = tostring(i+TerrainBrushMarker.CirclePointCount);
					local obj = miniscene:GetObject(objname);
					if(obj:IsValid() == false) then
						_asset = _asset or ParaAsset.LoadStaticMesh("", TerrainBrushMarker.Assets["point"]);
						obj = ParaScene.CreateMeshPhysicsObject(objname, _asset, 1,1,1,false, "1,0,0,0,1,0,0,0,1,0,0,0");
						obj:SetFacing(0);
						obj:GetAttributeObject():SetField("progress", 1);
						obj:SetPosition(x, y, z);
						miniscene:AddChild(obj);
					else
						obj:SetVisible(true);
						obj:SetPosition(x, y, z);
					end
				end
				TerrainBrushMarker.CirclePointCount = TerrainBrushMarker.CirclePointCount + markerCount;
			end
			
			-- make remaining invisible
			for i=TerrainBrushMarker.CirclePointCount+1,TerrainBrushMarker.MaxCirclePointCount do
				local obj = miniscene:GetObject(tostring(i));
				if(obj:IsValid()) then
					obj:SetVisible(false);
				else
					break;
				end
			end
		end
	else
		TerrainBrushMarker.DrawBrush(brush);
	end	
end

-- clear everything. 
function TerrainBrushMarker.Clear()
	local miniscene = ParaScene.GetMiniSceneGraph("TerrainBrushMarker");
	miniscene:SetVisible(false);
end


--[[
Title: TerrainBrush Task/Command
Author(s): LiXizhi
Date: 2016/7/16
Desc: 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/PaintBrushTask.lua");
local PaintBrushTask = commonlib.gettable("MyCompany.Aries.Game.Tasks.PaintBrushTask");
local task = PaintBrushTask:new();
task:Run();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushTask.lua");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")

local PaintBrushTask = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Tasks.TerrainBrushTask"), commonlib.gettable("MyCompany.Aries.Game.Tasks.PaintBrushTask"));

PaintBrushTask.default_toolname = "paint";
PaintBrushTask.last_blockid = 56;

PaintBrushTask.tools = {
    {name="paint", tooltip=L"添加随机地表, 按住Shift使用替换模式", icon="Texture/blocks/items/brush.png"},
	{name="flood_paint", tooltip=L"按住左键并拖动填充方块", icon="Texture/blocks/items/waterfeet.png"},
}

function PaintBrushTask:ctor()
end

function PaintBrushTask:ShowPage()
	local window = self:CreateGetToolWindow();
	window:Show({
		name="PaintBrushTask", 
		url="script/apps/Aries/Creator/Game/Tasks/TerrainBrush/PaintBrushTask.html",
		alignment="_ctb", left=0, top=-55, width = 256, height = 64,
	});
end


--[[
Title: Block terrain filters
Author(s): LiXizhi
Date: 2013/11/27
Desc: apply filters to block terrain 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainFilterTask.lua");
local task = MyCompany.Aries.Game.Tasks.TerrainFilter:new()
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/blocks/block_types.lua");
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local names = commonlib.gettable("MyCompany.Aries.Game.block_types.names")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local TaskManager = commonlib.gettable("MyCompany.Aries.Game.TaskManager")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")

local TerrainFilter = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Task"), commonlib.gettable("MyCompany.Aries.Game.Tasks.TerrainFilter"));

TerrainFilter.radius = 5;
-- this can be "flatten" or ""
TerrainFilter.operation = "flatten";
-- when user keeps holding the mouse button, the task may be run repeatedly every 1000ms. 
TerrainFilter.step_duration = 200;


-- Perform filtering on a terrain height field.
-- set or get the terrain data by calling GetTerrainData() function.

TerrainFilter.MergeOperation = {
		Addition = 0,
		Subtract = 1,
		Multiplication = 2,
		Division = 3,
		Minimum = 4,
		Maximum = 5,
};

TerrainFilter.FlattenOperation = {
		-- Flatten the terrain up to the specified elevation 
		Fill_Op = 1,
		-- Flatten the terrain down to the specified elevation
		ShaveTop_Op = 2,
		-- Flatten the terrain up and down to the specified elevation 
		Flatten_Op = 3
};

TerrainFilter.PaintOperation = {
		-- replace blocks
		Replace_Op = 1,
		-- overlay on top of existing blocks
		Ontop_Op = 2,
};

local FlattenOperation = TerrainFilter.FlattenOperation;

function TerrainFilter:ctor()
	self.history = {};
	self.TTerrain = {};
	self.add_to_history = true;
end

-- @param paint_op: TerrainFilter.PaintOperation, default to Replace. 
-- @param x,y,z: center of the paint brush
-- @param block_id: the block to paint. can be 0
-- @param radius: the block radius, default to 5 
-- @param strength: (0, 1] the average probability to paint on each of the specified paint location.
-- @param side: the side to paint on default to 5 (which is the top block)
-- 1 means all blocks in the ciruclar region will be painted. default 0.3. 
function TerrainFilter:PaintBlocks(paint_op, block_id, block_data, xcent,ycent,zcent, radius, strength, side)
	paint_op = paint_op or TerrainFilter.PaintOperation.Replace_Op;
	radius = radius or 5;
	strength = strength or 0.3;
	side = side or 5;
	local xmin, xmax, ymin, ymax, zmin, zmax;
	
	xmin = xcent - radius;
	xmax = xcent + radius;
	ymin = math.max(1, ycent - radius);
	ymax = ycent + radius;
	zmin = zcent - radius;
	zmax = zcent + radius;
	local radiusSq = (radius-0.5)^2;
	if(side == 5) then
		for x = xmin, xmax do
			for z = zmin, zmax do
				local r_sq = ((x - xcent)^2+(z - zcent)^2);
				if(r_sq <= radiusSq) then
					for y = self:GetHeight(x, z, ymax), ymin, -1 do
						local block_template = BlockEngine:GetBlock(x,y,z);
						if(block_template and (block_id == 0 or block_template:isNormalCube())) then
							if( math.random() <= strength) then
								if(paint_op == self.PaintOperation.Ontop_Op) then
									self:SetBlock(x, y+1, z, block_id, block_data, 3);
								else
									-- default to replace operation
									self:SetBlock(x, y, z, block_id, block_data);
								end
							end
							break;
						end
					end
				end
			end
		end 
	end
end


--  Flatten the terrain both up and down to the specified elevation, using using the 
-- tightness parameter to determine how much the altered points are allowed 
-- to deviate from the specified elevation. 
-- @param flatten_op: nil default to FlattenOperation.Fill_Op
-- @param elevation: the desired height
-- @param factor: value is between [0,1]. 1 means fully transformed; 0 means nothing is changed
-- @param xcent: the center of the affected circle.
-- @param ycent: the center of the affected circle.
-- @param radius: the radius of the affected circle. 
-- @param min_thickness: at least blocks thick of the terrain shell
function TerrainFilter:Flatten(flatten_op, elevation, xcent, ycent, radius, factor)
	flatten_op = flatten_op or FlattenOperation.Flatten_Op;
	radius = radius or 5;
	factor = factor or 0.8;

	local max_height = elevation + radius*2;
	local xmin, xmax, ymin, ymax;
	xmin = xcent - radius;
	xmax = xcent + radius;
	ymin = ycent - radius;
	ymax = ycent + radius;
	
	local inner_radius = radius * factor;
	local thinkness = math.max(radius - inner_radius,1);

	for y = ymin, ymax do
		for x = xmin, xmax do
			local distance = (xcent+0.5 - x)^2 + (ycent+0.5 - y)^2;
			if(distance>0.001) then
				distance = math.sqrt(distance);
			end
			if (distance <= radius) then
				local factor_ = 1;
				if (distance <= inner_radius) then
					factor_ = 1;
				else
					factor_ = math.max(0, math.min(1, (radius-distance)/thinkness));
				end
				if(factor_ > 0 ) then
					local old_height = self:GetHeight(x, y, max_height, 5);
					local new_height = math.floor(elevation - (elevation - old_height) * (1 - factor_) + 0.5);
					self:MorphTerrainHeight(x, y, new_height, old_height, max_height);
				end
			end
		end
	end
end

-- @param filters: 5 for solid ones, or it will match all blocks.
function TerrainFilter:GetHeight(x, y, max_height, filters)
	max_height = max_height or 255;
	local dist = ParaTerrain.FindFirstBlock(x, max_height, y, 5, max_height, filters);
	if(dist<0) then
		return 0;
	else
		return max_height - dist;
	end
end


--  This creates a Gaussian hill at the specified location with the specified parameters.
--  it actually adds the hill to the original terrain surface.
--  Here ElevNew(x,y) = 
--		|(x,y)-(center_x,center_y)| < radius*smooth_factor,	ElevOld(x,y)+height_scale*exp(-[(x-center_x)^2+(y-center_y)^2]/(2*standard_deviation^2) ),
--		|(x,y)-(center_x,center_y)| > radius*smooth_factor, minimize hill effect.
-- @param xcent: the center of the affected circle. value in the range [0,1]
-- @param ycent: the center of the affected circle.value in the range [0,1]
-- @param radius: the radius of the affected circle.value in the range [0,0.5]
-- @param height_scale: scale factor. One can think of it as the maximum height of the Gaussian Hill. this value can be negative
-- @param standard_deviation: standard deviation of the unit height value. should be in the range (0,1). 
--  0.5 is common value. larger than that will just make a flat hill with smoothing.
-- @param smooth_factor: value is between [0,1]. 1 means fully transformed; 0 means nothing is changed
function TerrainFilter:GaussianHill(elevation, xcent, ycent, radius, height_scale, standard_deviation, smooth_factor)
	radius = radius or 8;
	standard_deviation = standard_deviation or 0.1;
	standard_deviation = 2*(standard_deviation^2);
	height_scale = height_scale or 0.5;
	smooth_factor = smooth_factor or 0.6;

	local xmin, xmax, ymin, ymax;
	xmin = xcent - radius;
	xmax = xcent + radius;
	ymin = ycent - radius;
	ymax = ycent + radius;
	height_scale = radius * height_scale;
	local smooth_radius = radius * smooth_factor;
	local max_height = elevation + radius*2;

	for y = ymin, ymax do
		for x = xmin, xmax do
			local distance = (xcent+0.5 - x)^2 + (ycent+0.5 - y)^2;
			if(distance>0.001) then
				distance = math.sqrt(distance);
			end
			if (distance <= radius) then
				local old_height = self:GetHeight(x, y, max_height, 5);
				local deltaHeight = height_scale * math.exp(-((distance/radius)^2)*standard_deviation);
				-- see if we should be smoothing
				if (distance > smooth_radius) then
					deltaHeight = deltaHeight*(1.0 - (distance-smooth_radius) / smooth_radius);
				end
				local new_height = math.max(1, old_height + math.floor(deltaHeight+0.5));
			
				self:MorphTerrainHeight(x, y, new_height, old_height, max_height);
			end
		end
	end
end

-- @param size: default to 5. 
-- @param max_height: if nil, it is max world height
-- return the average of the neighboring cells in a square size with 
function TerrainFilter:GetNeighbourAverageHeight(xcent, ycent, size, max_height)
	size = size or 5;
	local minx = math.floor(xcent-(size-1)/2+0.5);
	local miny = math.floor(ycent-(size-1)/2+0.5);
	local sum_height = 0;
	local count = 0;
	for y = miny, miny+size do
		for x = minx, minx+size do
			local height = self:GetHeight(x, y, max_height);
			if(height>0) then
				count = count + 1;
				sum_height = sum_height + height;
			end
		end
	end
	if(count > 0) then
		return math.floor(sum_height/count+0.5);
	end
	return 0;
end

-- changing terrain from old height to new height, it will use existing terrain blocks for morphing
-- we will maintain the top layer and extend using second layer.
-- @param x,y: block world horizontal coordinate. 
-- @param old_height: if nil, we will find max terrain height at x,y. 
function TerrainFilter:MorphTerrainHeight(x, y, new_height, old_height, max_height)
	old_height = old_height or self:GetHeight(x, y, max_height, 5);

	if(new_height ~= old_height) then
		local block_id_top, block_data_top, block_entity_top = BlockEngine:GetBlockFull(x, old_height, y);
		local block_id_second, block_data_second, block_entitydata_second = BlockEngine:GetBlockFull(x, old_height-1, y);
		if(block_id_top == 0) then
			block_id_top = names.Bedrock or 123;
		end
		if(block_id_second == 0) then
			block_id_second = block_id_top;
		end
		if(new_height > old_height) then
			for height = old_height+1, new_height do 
				local block_id_up, block_data_up, block_entitydata_up = BlockEngine:GetBlockFull(x, height, y);
				if(block_id_up > 0) then
					-- shifting non-solid blocks upwards
					local block_template = block_types.get(block_id_up);
					if(block_template and not block_template.liquid) then
						-- ignore liquid like water
						self:SetBlock(x, new_height+(height-old_height), y, block_id_up, block_data_up, nil, block_entitydata_up);	
					end
				end
				if(height <new_height) then
					self:SetBlock(x, height, y, block_id_second, block_data_second, nil, block_entitydata_second);
				else
					self:SetBlock(x, new_height, y, block_id_top, block_data_top, nil, block_entity_top);
				end
			end
		else
			for height = old_height, (new_height+1), -1 do 
				local block_id_up, block_data_up, block_entitydata_up = BlockEngine:GetBlockFull(x, old_height+(height-new_height), y);
				if(block_id_up > 0) then
					-- shifting non-solid blocks downwards
					self:SetBlock(x, height, y, block_id_up, block_data_up, nil, block_entitydata_up);	
					local block_template = block_types.get(block_id_up);
					if(block_template and not block_template.liquid) then
						-- ignore liquid like water
						self:SetBlock(x, old_height+(height-new_height), y, 0);	
					end
				else
					self:SetBlock(x, height, y, 0);
				end
			end
		end
	end
end

-- 	square filter for sharpening and smoothing. 
-- Use neighbour-averaging to roughen or smooth the height field. The factor 
-- determines how much of the computed roughening is actually applied to the 
-- height field. In it's default invocation, the 4 directly neighboring 
-- squares are used to calculate the roughening. If you select big sampling grid, 
-- all 8 neighboring cells will be used. 
-- @param elevation: if nil the max terrain height is used. 
-- @param roughen: true for sharpening, false for smoothing.
-- @param filter_size: default to 4 neighboring cells
-- @param factor: value is between [0,1]. 1 means fully transformed; 0 means nothing is changed
function TerrainFilter:Roughen_Smooth(elevation, xcent, ycent, radius, roughen, filter_size, factor)
	radius = radius or 8;
	filter_size = filter_size or 4;
	factor = factor or 0.5;

	local xmin, xmax, ymin, ymax;
	xmin = xcent - radius;
	xmax = xcent + radius;
	ymin = ycent - radius;
	ymax = ycent + radius;
	max_height = elevation;
	if(max_height) then
		max_height = elevation + radius*2;
	end

	local new_grid = {};
	for y = ymin, ymax do
		new_grid[y] = {};
		for x = xmin, xmax do
			local distance = (xcent+0.5 - x)^2 + (ycent+0.5 - y)^2;
			if(distance>0.001) then
				distance = math.sqrt(distance);
			end
			if (distance <= radius) then
				local originalHeight = self:GetHeight(x, y, max_height, 5);
				
				if(not max_height or originalHeight < max_height) then
					local averageHeight = self:GetNeighbourAverageHeight(x, y, 5, max_height);
					local value;
					if (roughen) then
						value = originalHeight - factor * (averageHeight - originalHeight);
					else
						value = originalHeight + factor * (averageHeight - originalHeight);
					end
					new_grid[y][x] = math.floor(value+0.5);
				end
			end
		end
	end
	for y = ymin, ymax do
		for x = xmin, xmax do
			if(new_grid[y][x]) then
				self:MorphTerrainHeight(x, y, new_grid[y][x], nil, max_height);
			end
		end
	end
end


-- Note: terrain data should be in normalized space with height in the range [0,1]. 
-- Picks a point and scales the surrounding terrain in a circular manner. 
-- Can be used to make all sorts of circular shapes. Still needs some work. 
--  radial_scale: pick a point (center_x, center_y) and scale the points 
--      where distance is mindist<=distance<=maxdist linearly.  The formula
--      we'll use for a nice sloping smoothing factor is (-cos(x*3)/2)+0.5.
function TerrainFilter:RadialScale(center_x, center_y, scale_factor, min_dist,max_dist, smooth_factor, frequency)
end

-- offset in a spherical region
function TerrainFilter:Spherical( offset)
end

function TerrainFilter:grid_neighbour_sum_size(terrain,x, y,size)
end

--  create a ramp (inclined slope) from height(x1,y1) to height(x2,y2). The ramp's half width is radius. 
-- this is usually used to created a slope path connecting a high land with a low land. 
-- @param radius: The ramp's half width
-- @param borderpercentage: borderpercentage*radius is how long the ramp boarder is to linearly interpolate with the original terrain. specify 0 for sharp ramp border.
-- @param factor: in range[0,1]. it is the smoothness to merge with other border heights.Specify 1.0 for a complete merge
function TerrainFilter:Ramp(x1, y1, height1, x2, y2, height2, radius, borderpercentage, factor)
	borderpercentage=borderpercentage or 0.5;
	factor=factor or 1.0;
end
		
-- 
-- load height field from file
-- @param fHeight : height of the edge 
-- @param nSmoothPixels:  the number of pixels to smooth from the edge of the height field. 
-- if this is 0, the original height field will be loaded unmodified. if it is greater than 0, the loaded height field 
-- will be smoothed for nSmoothPixels from the edge, where the edge is always fHeight. The smooth function is linear. For example,
-- - 0% of original height  for the first pixel from the edge 
-- - 1/nSmoothPixels of original height for the second pixel from the edge. Lerp(1/nSmoothPixels, fheight, currentHeight)
-- - 2/nSmoothPixels of original height for the third.Lerp(2/nSmoothPixels, fheight, currentHeight )
-- - 100% for the nSmoothPixels-1 pixel 
	
function TerrainFilter:SetConstEdgeHeight(fHeight, nSmoothPixels)
	fHeight= fHeight or 0;
	nSmoothPixels= nSmoothPixels or 7;
end

-- merge two terrains, and save the result to the current terrain. The three terrains are aligned by their center. 
-- the input terrain can be the current terrain. The two input terrain must not be normalized.
function TerrainFilter:Merge (terrain_1, terrain_2,weight_1, weight_2,operation)
end

function TerrainFilter:AddToUndoManager()
	self:SetFinished();
	if(next(self.history)) then
		TerrainFilter._super.AddToUndoManager(self);
	end
end

-- set block and add changed data to history
function TerrainFilter:SetBlock(x, y, z, block_id, block_data, flag, block_entitydata)
	if(self.add_to_history) then
		local index = BlockEngine:GetSparseIndex(x, y, z);
		if(not self.history[index]) then
			local from_id, from_data, from_entity_data = BlockEngine:GetBlockFull(x,y,z)
			if(from_id == block_id and (from_data or 0) == (block_data or 0)) then
				return;
			else
				BlockEngine:SetBlock(x, y, z, block_id, block_data, flag, block_entitydata);
				self.history[index] = {x,y,z, block_id, block_data, block_entitydata, from_id, from_data, from_entity_data};	
			end
		end
	end
end

function TerrainFilter:Redo()
	if(next(self.history)) then
		for _, b in pairs(self.history) do
			BlockEngine:SetBlock(b[1],b[2],b[3], b[4] or 0, b[5], nil, b[6]);
		end
	end
end

function TerrainFilter:Undo()
	if(next(self.history)) then
		for i, b in pairs(self.history) do
			BlockEngine:SetBlock(b[1],b[2],b[3], b[7] or 0, b[8], nil, b[9]);
		end
	end
end

--[[
Title: ItemTerrainBrush
Author(s): LiXizhi
Date: 2016/7/16
Desc: paint with current selected pen.

Usage:
   * alt + left mouse click: pick the current mouse block.
   * +/- key or shift+mousewheel: change radius size

use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemTerrainBrush.lua");
local ItemTerrainBrush = commonlib.gettable("MyCompany.Aries.Game.Items.ItemTerrainBrush");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Items/ItemToolBase.lua");
local ItemToolBase = commonlib.gettable("MyCompany.Aries.Game.Items.ItemToolBase");
local ItemClient = commonlib.gettable("MyCompany.Aries.Game.Items.ItemClient");
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")

local ItemTerrainBrush = commonlib.inherit(ItemToolBase, commonlib.gettable("MyCompany.Aries.Game.Items.ItemTerrainBrush"));

ItemTerrainBrush:Property({"pen_radius", 5, "GetPenRadius", "SetPenRadius"})
ItemTerrainBrush:Property({"brush_strength", nil, "GetBrushStrength", "SetBrushStrength"})
ItemTerrainBrush:Property({"selected_blockid", 56, "GetSelectedBlockId", "SetSelectedBlockId"})
ItemTerrainBrush:Property({"selected_blockdata", nil, "GetSelectedBlockData", "SetSelectedBlockData"})

block_types.RegisterItemClass("ItemTerrainBrush", ItemTerrainBrush);

-- initial pen radius
ItemTerrainBrush.min_radius = 2;
ItemTerrainBrush.max_radius = 32;

-- @param template: icon
-- @param radius: the half radius of the object. 
function ItemTerrainBrush:ctor()
	self:SetOwnerDrawIcon(true);
end

-- @param itemStack: if nil it is current selected one
function ItemTerrainBrush:GetSelectedBlockIcon(itemStack)
	local block_id = self:GetSelectedBlockId(itemStack) or 56;
	local item = ItemClient.GetItem(block_id);
	if(item) then
		return item:GetIcon();
	end
end

-- @param itemStack: if nil it is current selected one
function ItemTerrainBrush:GetSelectedBlockId(itemStack)
	itemStack = itemStack or self:GetCurrentItemStack()
	return itemStack and itemStack:GetDataField("selected_blockid") or self.selected_blockid;
end

function ItemTerrainBrush:SetSelectedBlockId(selected_blockid)
	local itemStack = self:GetCurrentItemStack()
	return itemStack and itemStack:SetDataField("selected_blockid", selected_blockid);
end

function ItemTerrainBrush:GetBrushStrength()
	local itemStack = self:GetCurrentItemStack()
	return itemStack and itemStack:GetDataField("brush_strength") or self.brush_strength;
end

function ItemTerrainBrush:SetBrushStrength(brush_strength)
	local itemStack = self:GetCurrentItemStack()
	return itemStack and itemStack:SetDataField("brush_strength", brush_strength);
end

function ItemTerrainBrush:GetSelectedBlockData()
	local itemStack = self:GetCurrentItemStack()
	return itemStack and itemStack:GetDataField("selected_blockdata") or self.selected_blockdata;
end

function ItemTerrainBrush:SetSelectedBlockData(selected_blockdata)
	local itemStack = self:GetCurrentItemStack()
	return itemStack and itemStack:SetDataField("selected_blockdata", selected_blockdata);
end

function ItemTerrainBrush:GetPenRadiusInItem(itemStack)
	if(itemStack) then
		local pen_radius = itemStack:GetDataField("pen_radius") or self.pen_radius;
		return math.floor(pen_radius+0.5);
	else
		return self.pen_radius;
	end
end

function ItemTerrainBrush:GetPenRadius()
	local itemStack = self:GetCurrentItemStack()
	return self:GetPenRadiusInItem(itemStack);
end

function ItemTerrainBrush:SetPenRadius(radius)
	local pen_radius = self:GetPenRadius();
	if(radius~=pen_radius) then
		radius = (radius > pen_radius) and (pen_radius+1) or (pen_radius - 1);
	end
	if(radius~=pen_radius) then
		local itemStack = self:GetCurrentItemStack()
		if(itemStack) then
			local pen_radius = math.max(math.min(radius, self.max_radius), self.min_radius);
			itemStack:SetDataField("pen_radius", pen_radius);
			self:valueChanged();
		end
	end
end

-- virtual function: called when user clicked some other item while holding this item in hand.
-- @return true will cause other item to ignore the click event. This is useful when the hand block needs to process click event itself
function ItemTerrainBrush:HandleClickOtherItem(other_item_id)
	if(other_item_id) then
		local block_template = block_types.get(other_item_id);
		if(block_template and (block_template.solid or block_template.liquid or block_template.cubeMode)) then
			self:SetSelectedBlockId(other_item_id);
			return true;
		end
	end
end

-- virtual: draw icon with given size at current position (0,0)
-- @param width, height: size of the icon
-- @param itemStack: this may be nil. or itemStack instance. 
function ItemTerrainBrush:DrawIcon(painter, width, height, itemStack)
	ItemTerrainBrush._super.DrawIcon(self, painter, width, height, itemStack);
	painter:SetPen("#ffff00");
	painter:DrawText(1,1, tostring(self:GetPenRadiusInItem(itemStack)));
end

-- virtual function: 
function ItemTerrainBrush:CreateTask(itemStack)
	NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/TerrainBrush/TerrainBrushTask.lua");
	local TerrainBrushTask = commonlib.gettable("MyCompany.Aries.Game.Tasks.TerrainBrushTask");
	return TerrainBrushTask:new():Init(self);
end


--[[
Title: TerraPaintPage
Author(s): LiXizhi
Company: ParaEnging Co. & Taomee Inc.
Date: 2010/1/26
Desc: Instructions:
	- click texture to paint on terrain
	- click set texture to replace or assign new detail texture brush
	- press esc key to exit editing mode
	- use -/+ key to scale brush size
	- hold and click/drag on terrain surface to repeatedly apply terrain paint. 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Env/TerraPaintPage.lua");
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/timer.lua");

local TerraPaintPage = commonlib.gettable("MyCompany.Aries.Creator.TerraPaintPage")

NPL.load("(gl)script/apps/Aries/Creator/Env/TerrainBrushMarker.lua");
local TerrainBrushMarker = MyCompany.Aries.Creator.TerrainBrushMarker;

-- singleton page instance. 
local page;

-- image to display when detail texture slot is empty. 
TerraPaintPage.EmptyDetailTex = "Texture/Aries/Creator/eraser.png;0 0 48 48"; -- "Texture/tileset/generic/GridMarker.dds";

-- Terrain texture db table
TerraPaintPage.terrainTexList = {
	{filename = TerraPaintPage.EmptyDetailTex},
};
-- selected index. 
TerraPaintPage.SelectedIndex = nil;
-- max number of textures to display. although the engine support unlimited textures, we will only allow the user to use 8 at most. 
TerraPaintPage.MaxDetailTexCount = 32;
-- how many milliseconds to paint repeatedly when user hold the key. 
TerraPaintPage.PaintTimerInterval = 100;
-- default brushes
local defaultBrushes = {
	{
		BrushSize = 1, 
		BrushStrength = 0.25,
		BrushSoftness = 1,
	},
	{
		BrushSize = 2, 
		BrushStrength = 0.25,
		BrushSoftness = 1,
	},
	{
		BrushSize = 3, 
		BrushStrength = 0.25,
		BrushSoftness = 1,
	},
};
-- current brush
TerraPaintPage.CurBrush = {
	filename = nil,
	BrushSize = 1, 
	BrushStrength = 0.25,
	BrushSoftness = 1,
}

function TerraPaintPage.DS_TerrainTex_Func(index)
	if(index == nil) then
		return #(TerraPaintPage.terrainTexList);
	else
		return TerraPaintPage.terrainTexList[index];
	end	
end

-- default textures for people to use. 
local terrainTexList = {
	TerraPaintPage.EmptyDetailTex,
	"Texture/tileset/generic/env_landroad_deco_yellow.dds",
	"Texture/tileset/generic/c_grass_light_green.dds",
	"Texture/tileset/generic/env_snowhill_blue.dds",
	"Texture/tileset/generic/c_grassdeco_light_green.dds",
	
	"Texture/tileset/generic/env_landroad_light_yellow.dds",
	"Texture/tileset/generic/env_beachsand_dark_yellow.dds",
	"Texture/tileset/generic/c_rockroad_light_pink.dds",
	"Texture/tileset/generic/c_garssbackdeco_light_green.dds",
	
	"Texture/tileset/generic/c_mudroad_light_yellow.dds",
	"Texture/tileset/generic/env_cliff_dark_yellow.dds",

	"Texture/tileset/generic/c_bigroad_dark_blue.dds",
	"Texture/tileset/generic/c_bigroad_light_blue.dds",
	"Texture/tileset/generic/c_rockroad_dark_pink.dds",
	"Texture/tileset/generic/Darkforest/ground01.dds",
	"Texture/tileset/generic/Darkforest/ground02.dds",
	"Texture/tileset/generic/Darkforest/ground03.dds",
	"Texture/tileset/generic/Darkforest/huoshan01.dds",
	"Texture/tileset/generic/Darkforest/huoshan02.dds",
	"Texture/tileset/generic/Darkforest/huoshan03.dds",
	"Texture/tileset/generic/Darkforest/huoshan04.dds",
	"Texture/tileset/generic/Darkforest/riverstone04.dds",
	"Texture/tileset/generic/firebirdland/a_11.dds",
	"Texture/tileset/generic/firebirdland/a_10.dds",
};
local max_textures = #terrainTexList;
TerraPaintPage.MaxDetailTexCount = max_textures;

local function GetNextUnUsedTextures(used_textures)
	local _, filename
	for _, filename  in ipairs(terrainTexList) do
		if(not used_textures[filename] and filename~="") then
			used_textures[filename] = true;
			return filename;
		end
	end
end

-- called to init page
function TerraPaintPage.OnInit()
	page = document:GetPageCtrl();
	local used_textures = {};
	local x,y,z = ParaScene.GetPlayer():GetPosition();
	local nCount = ParaTerrain.GetTextureCount(x,z);
	local i;
	local HasEmpty;
	for i = 1,TerraPaintPage.MaxDetailTexCount do 
		TerraPaintPage.terrainTexList[i] = TerraPaintPage.terrainTexList[i] or {};
		if(i<=nCount) then
			local filename = ParaTerrain.GetTexture(x, z, i-1):GetKeyName();
			TerraPaintPage.terrainTexList[i].filename = filename;	
			used_textures[filename] = true;
		else
			-- fill in some predefined textures. 
			TerraPaintPage.terrainTexList[i].filename = GetNextUnUsedTextures(used_textures) or TerraPaintPage.EmptyDetailTex;
			
			if(TerraPaintPage.terrainTexList[i].filename == TerraPaintPage.EmptyDetailTex) then
				if(not HasEmpty) then
					HasEmpty = true;
				else
					TerraPaintPage.terrainTexList[i].filename = "";
				end	
			end
		end
		TerraPaintPage.terrainTexList[i].InCell = nil;
	end
	
	local cell_texs = {};
	ParaTerrain.GetTexturesInCell(x,z,cell_texs);
	local index;
	for i, index in pairs(cell_texs) do
		local tex = TerraPaintPage.terrainTexList[index+1];
		if(tex) then
			tex.InCell = true;
		end
	end
	
	page:SetNodeValue("BrushSize", TerraPaintPage.CurBrush.BrushSize);
	page:SetNodeValue("BrushStrength", TerraPaintPage.CurBrush.BrushStrength);
	page:SetNodeValue("BrushSoftness", TerraPaintPage.CurBrush.BrushSoftness);
	
	NPL.load("(gl)script/apps/Aries/Creator/Env/SwitchEnvEditorMode.lua");
	MyCompany.Aries.Creator.SwitchEnvEditorMode("TerraPaintPage");
	
	TerrainBrushMarker.ShowTextureCellRegion(true);
	
	if(TerraPaintPage.SelectedIndex~=nil) then
		TerraPaintPage.BeginEditing();
	end
end

------------------------
-- page events
------------------------

-- Close the page
function TerraPaintPage.OnClose()
	TerraPaintPage.EndEditing()
end

-- reset the page
function TerraPaintPage.OnReset()
	TerraPaintPage.EndEditing();
	page:Refresh(0);
end

-- display a dialog to select or replace currently selected textures.
function TerraPaintPage.OnSetTexture()
	if(TerraPaintPage.SelectedIndex == nil) then
		_guihelper.MessageBox("请先选择一个图层通道, 来设置它的贴图");
		return
	end
	NPL.load("(gl)script/ide/OpenFileDialog.lua");
	local ctl = CommonCtrl.OpenFileDialog:new{
		name = "OpenFileDialog1",
		alignment = "_ct",
		left=-256, top=-150,
		width = 512,
		height = 380,
		parent = nil,
		fileextensions = {"images(*.jpg; *.png; *.dds)",},
		folderlinks = {
			{path = "Texture/tileset/generic/", text = "Texture"},
			{path = "worlds/", text = "worlds"},
		},
		onopen = function(ctrlName, filename)
			if(TerraPaintPage.SelectedIndex) then
				TerraPaintPage.ReplaceTexture(TerraPaintPage.SelectedIndex-1, filename)
			end
		end
	};
	ctl:Show(true);
end

-- delete the currently selected texture layer. 
function TerraPaintPage.OnDeleteTexture()
	if(TerraPaintPage.SelectedIndex == nil) then
		_guihelper.MessageBox([[<div style="margin-top:32px;">请先选择你想要删除的地表贴图</div>]]);
		return
	end
	
	_guihelper.MessageBox(string.format([[<div style="margin-top:32px;">你确定要将选择的地表贴图 全部删除吗？</div>]]), function(res)
			if(TerraPaintPage.SelectedIndex) then
				if(res and res == _guihelper.DialogResult.Yes) then
					TerraPaintPage.ReplaceTexture(TerraPaintPage.SelectedIndex-1, nil)
				elseif(res and res == _guihelper.DialogResult.No) then
					-- This is too advanced for kids, so we removed it. 
					-- TerraPaintPage.ReplaceTexture(TerraPaintPage.SelectedIndex-1, nil, true)
				else
					-- cancel	
				end
			end
		end, _guihelper.MessageBoxButtons.YesNo)
end

-- selected a detail terrain to paint.
-- @param index: if nil, it will select nothing
function TerraPaintPage.OnSelectTexture(index)
	if(TerraPaintPage.SelectedIndex ~= index or index~=nil) then
		TerraPaintPage.SelectedIndex = index;
		if(index) then
			local tex = TerraPaintPage.terrainTexList[index];
			if(tex) then
				local filename = tex.filename;
				if(filename) then
					TerraPaintPage.UpdateCurrentBrush({filename = filename});
					TerraPaintPage.BeginEditing()
				end	
			end	
		else
			TerraPaintPage.EndEditing()
		end
		page:Refresh(0);
	end	
end

-- select an empty eraser. 
function TerraPaintPage.OnSelectEraser()
	local nEraserIndex;
	for i = 1,TerraPaintPage.MaxDetailTexCount do 
		local tex = TerraPaintPage.terrainTexList[i] or {};
		if(tex and tex.filename == TerraPaintPage.EmptyDetailTex) then
			nEraserIndex = i;
			break;
		end
	end
	if(nEraserIndex) then
		TerraPaintPage.OnSelectTexture(nEraserIndex)
	end	
end

-- deselect current one 
function TerraPaintPage.OnDeselectTexture()
	TerraPaintPage.OnSelectTexture(nil);
end

function TerraPaintPage.OnSetBrushSoftness(value)
	TerraPaintPage.UpdateCurrentBrush({BrushSoftness = value});
end

function TerraPaintPage.OnSetBrushStrength(value)
	TerraPaintPage.UpdateCurrentBrush({BrushStrength = value});
end

function TerraPaintPage.OnSetBrushSize(value)
	TerraPaintPage.UpdateCurrentBrush({BrushSize = value});
end

function TerraPaintPage.OnClickBrush(btnName)
	local brushIndex = tonumber(btnName)
	if(brushIndex~=nil) then
		local brush = defaultBrushes[brushIndex];
		TerraPaintPage.UpdateCurrentBrush(brush, true);
	end
end

function TerraPaintPage.OnSetBrushRepeatInterval(value)
	TerraPaintPage.PaintTimerInterval = math.floor((1-value)*1000);
end

------------------------
-- public methods
------------------------

-- replace a given texture in texture cell set specified at position x,z
-- @param OldIndex: the old texture index to replace, this is zero based index. if nil, new detail texture will be added. 
-- @param newfilename: the new texture to replace with. If nil, texture will be deleted at the given index.  
-- @param bCellOnly: if true, texture is only removed from the texture cell, instead of the entire terrain tile. 
-- @param x,y,z: if nil, the current player location is used. 
function TerraPaintPage.ReplaceTexture(OldIndex, newfilename, bCellOnly, x,y,z)
	if(x == nil or z ==nil) then
		x,y,z = ParaScene.GetPlayer():GetPosition();
	end	
	local nCount = ParaTerrain.GetTextureCount(x,z);
	if(OldIndex == nil) then 
		OldIndex = nCount;
	end
	if(OldIndex >= 0) then
		if(not bCellOnly) then
			ParaTerrain.ReplaceTexture(x, z, OldIndex, newfilename);
		else
			if(newfilename == nil) then
				ParaTerrain.RemoveTextureInCell(x, z, OldIndex);
			else
				_guihelper.MessageBox("replacing in the cell is not supported. Please delete in the cell and paint again.");
			end
		end
	end
	TerraPaintPage.OnReset();
end

-- when user select a tool it will enter 3d editing mode, where the miniscenegraph should draw markers
function TerraPaintPage.BeginEditing()
	TerraPaintPage.mytimer = TerraPaintPage.mytimer or commonlib.Timer:new({callbackFunc = TerraPaintPage.OnBrushTimer})
	ParaCamera.GetAttributeObject():SetField("EnableMouseLeftButton", false)
	TerraPaintPage.RegisterHooks()
end
-- when user pressed esc key, it will quit the 3d editing mode. and the mini scenegraph should be deleted. 
function TerraPaintPage.EndEditing()
	ParaCamera.GetAttributeObject():SetField("EnableMouseLeftButton", true)
	TerraPaintPage.UnregisterHooks()
	TerraPaintPage.OnSelectTexture(nil);
	TerrainBrushMarker.Clear()
	if(TerraPaintPage.mytimer) then
		-- kill timer
		TerraPaintPage.mytimer:Change();
	end
end

-- update the terrain brush. 
-- @param brush: {x,y,z,BrushSize,BrushSoftness, BrushStrength}, all fields can be nil. 
-- @param bRefreshUI: if true the UI will be updated according to input
function TerraPaintPage.UpdateCurrentBrush(brush, bRefreshUI)
	if(brush) then
		commonlib.partialcopy(TerraPaintPage.CurBrush, brush);
	end
	-- validate data
	if(TerraPaintPage.CurBrush.BrushSize < 0.1) then
		TerraPaintPage.CurBrush.BrushSize = 0.1;
	end
	
	if(bRefreshUI) then
		page:SetUIValue("BrushSize", TerraPaintPage.CurBrush.BrushSize);
		page:SetUIValue("BrushStrength", TerraPaintPage.CurBrush.BrushStrength);
		page:SetUIValue("BrushSoftness", TerraPaintPage.CurBrush.BrushSoftness);
	end	
	
	if(TerraPaintPage.SelectedIndex~=nil) then
		TerrainBrushMarker.DrawBrush({x=TerraPaintPage.CurBrush.x,y=TerraPaintPage.CurBrush.y,z=TerraPaintPage.CurBrush.z,radius = TerraPaintPage.CurBrush.BrushSize});
	end	
end

function TerraPaintPage.RegisterHooks()
	local hookType = CommonCtrl.os.hook.HookType.WH_CALLWNDPROC;
	CommonCtrl.os.hook.SetWindowsHook({hookType = hookType, 		 
		hookName = "TerraPaint_mouse_down_hook", appName = "input", wndName = "mouse_down", 
		callback = TerraPaintPage.OnMouseDown});
	CommonCtrl.os.hook.SetWindowsHook({hookType = hookType, 		 
		hookName = "TerraPaint_mouse_move_hook", appName = "input", wndName = "mouse_move",
		callback = TerraPaintPage.OnMouseMove});
	CommonCtrl.os.hook.SetWindowsHook({hookType = hookType, 		 
		hookName = "TerraPaint_mouse_up_hook", appName = "input", wndName = "mouse_up",
		callback = TerraPaintPage.OnMouseUp});
	CommonCtrl.os.hook.SetWindowsHook({hookType = hookType, 		 
		hookName = "TerraPaint_key_down_hook", appName = "input", wndName = "key_down",
		callback = TerraPaintPage.OnKeyDown});
end

function TerraPaintPage.UnregisterHooks()
	local hookType = CommonCtrl.os.hook.HookType.WH_CALLWNDPROC;
	CommonCtrl.os.hook.UnhookWindowsHook({hookName = "TerraPaint_mouse_down_hook", hookType = hookType});
	CommonCtrl.os.hook.UnhookWindowsHook({hookName = "TerraPaint_mouse_move_hook", hookType = hookType});
	CommonCtrl.os.hook.UnhookWindowsHook({hookName = "TerraPaint_mouse_up_hook", hookType = hookType});
	CommonCtrl.os.hook.UnhookWindowsHook({hookName = "TerraPaint_key_down_hook", hookType = hookType});
end

------------------------
-- input hooked event handler
------------------------
function TerraPaintPage.OnMouseDown(nCode, appName, msg)
	if(nCode==nil) then return end
	local input = Map3DSystem.InputMsg;
	
	if(input.mouse_button == "left") then
		if(TerraPaintPage.mytimer) then
			TerraPaintPage.mytimer:Change(0, TerraPaintPage.PaintTimerInterval)
		end
		return;
	end
	
	return nCode; 
end
function TerraPaintPage.OnMouseMove(nCode, appName, msg)
	if(nCode==nil) then return end
	local input = Map3DSystem.InputMsg;
	
	local pt = ParaScene.MousePick(70, "walkpoint"); -- pick a object
	if(pt:IsValid())then
		local x,y,z = pt:GetPosition();
		TerraPaintPage.UpdateCurrentBrush({x=x,y=y,z=z});
		return;
	end	
	return nCode; 
end
function TerraPaintPage.OnMouseUp(nCode, appName, msg)
	if(nCode==nil) then return end
	local input = Map3DSystem.InputMsg;
	
	if(input.mouse_button == "left") then
		if(TerraPaintPage.mytimer) then
			TerraPaintPage.mytimer:Change()
		end
		return;
	elseif(input.mouse_button == "right") then	
		if(input.dragDist<=5) then 
			-- exit editing mode. 
			TerraPaintPage.EndEditing();
			return;
		end
	end	
	return nCode; 
end
function TerraPaintPage.OnKeyDown(nCode, appName, msg)
	if(nCode==nil) then return end
	if(ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_ESCAPE))then
		-- exit editing mode. 
		TerraPaintPage.EndEditing();
		return
	elseif(ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_EQUALS))then
		-- DoScaling +
		TerraPaintPage.UpdateCurrentBrush({BrushSize = TerraPaintPage.CurBrush.BrushSize + 0.2});
		return
	elseif(ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_MINUS))then
		-- DoScaling -
		TerraPaintPage.UpdateCurrentBrush({BrushSize = TerraPaintPage.CurBrush.BrushSize - 0.2});
		return
	end	
	return nCode; 
end

-- called every few milliseconds when user click and hold the left mouse button 
function TerraPaintPage.OnBrushTimer(timer)
	local filename = TerraPaintPage.CurBrush.filename;
	if(filename == nil or filename == TerraPaintPage.EmptyDetailTex) then
		filename = ""; -- it means painting the base layer, erasing other textures. 
	end
	Map3DSystem.SendMessage_env({type = Map3DSystem.msg.TERRAIN_SET_PaintBrush, brush = {
			filename = filename,
			x=TerraPaintPage.CurBrush.x,
			y=TerraPaintPage.CurBrush.y,
			z=TerraPaintPage.CurBrush.z,
			radius = TerraPaintPage.CurBrush.BrushSize,
			BrushStrength = TerraPaintPage.CurBrush.BrushStrength,
			BrushSoftness = TerraPaintPage.CurBrush.BrushSoftness,
			bErase = nil,
		},})
	Map3DSystem.SendMessage_env({type = Map3DSystem.msg.TERRAIN_Paint, 
		forcelocal = true, disableSound = true,
		})
end

--[[
Title: A wrapper to the low level block terrain engine
Author(s): LiXizhi
Date: 2012/10/20
Desc: It contains various block generation, searching functions. And it provide simulation to ensure a closed space block world. 
Please note that the block engine it self does not keep the data for block level data. instead all static block data is loaded and saved
by the low level game engine. 

GameLogic filters:
 OnBeforeLoadBlockRegion(bContinue, x, y): false to disable loading region from file
 OnLoadBlockRegion(bContinue, x, y)
 OnUnLoadBlockRegion(bContinue, x, y)

use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/block_engine.lua");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
BlockEngine:Connect();
BlockEngine:SetGameLogic(GameLogic);
-- your game goes inbetween connect and disconnect
BlockEngine:Disconnect();
-------------------------------------------------------
]]

NPL.load("(gl)script/apps/Aries/Creator/Game/blocks/block_types.lua");
NPL.load("(gl)script/apps/Aries/Creator/WorldCommon.lua");
local WorldCommon = commonlib.gettable("MyCompany.Aries.Creator.WorldCommon")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types");
local npl_profiler = commonlib.gettable("commonlib.npl_profiler");
local block = commonlib.gettable("MyCompany.Aries.Game.block")
local Materials = commonlib.gettable("MyCompany.Aries.Game.Materials");
local GameLogic;

local math_floor= math.floor;

---------------------------
-- create class
---------------------------
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")

-- current eye position
BlockEngine.eye = {0,0,0};
BlockEngine.eye_block = {0,0,0};
-- simulation interval in ms
BlockEngine.sim_interval = 300;

-- block size in meters
-- width in metters
BlockEngine.region_width = 512;
BlockEngine.blocksize = BlockEngine.region_width/512;
BlockEngine.blocksize_inverse = 1/BlockEngine.blocksize;
BlockEngine.half_blocksize = BlockEngine.blocksize/2;
-- terrain region is usually 512*512 blocks
BlockEngine.region_size = 512;
-- height is usually (+128,-128)
BlockEngine.region_height = 128;
-- the block's origin in real world.
BlockEngine.offset_y = 0;
-- only used for debugggin purposes. 
BlockEngine.block_cache = {};
BlockEngine.tick_count = 0;

local block_framemove_count = 0;
-- framemove coroutine will yield if simulation step is bigger than block_sim_per_frame
local block_sim_per_frame = 100;
-- whether we will call all nearby block template's frame move function in a coroutine 
BlockEngine.is_do_per_block_framemove = false;

local blocksize = BlockEngine.blocksize;
local blocksize_inverse = BlockEngine.blocksize_inverse;
local region_size = BlockEngine.region_size;
local region_width = BlockEngine.region_width;
local region_height = BlockEngine.region_height;
local offset_y = BlockEngine.offset_y;

local custom_model_load_map = {};
local eye_pos = {};

-- set the current game logic to use. 
function BlockEngine:SetGameLogic(game_logic)
	GameLogic = game_logic;
end

-- call this function to connect the block engine with the current low level game engine's block terrain world. 
-- call this function when one enters the block based game.
function BlockEngine:Connect()
	-- clear the block cache
	self.block_cache = {};
	custom_model_load_map = {};

	local x, y, z = ParaScene.GetPlayer():GetPosition();
	ParaScene.GetPlayer():SetField("IsAlwaysAboveTerrain", false);

	local attr = ParaTerrain.GetAttributeObjectAt(x,z);
	
	if(ParaTerrain.GetBlockAttributeObject) then
		ParaTerrain.GetBlockAttributeObject():SetField("GeneratorScript", ";MyCompany.Aries.Game.BlockEngine.OnGeneratorScript();")
		ParaTerrain.GetBlockAttributeObject():SetField("OnBeforeLoadBlockRegion", ";return MyCompany.Aries.Game.BlockEngine.OnBeforeLoadBlockRegion();")
		ParaTerrain.GetBlockAttributeObject():SetField("OnSaveRegionCallbackScript", ";MyCompany.Aries.Game.BlockEngine.OnSaveBlockRegion();" )
		ParaTerrain.GetBlockAttributeObject():SetField("OnLoadBlockRegion", ";MyCompany.Aries.Game.BlockEngine.OnLoadBlockRegion();")
		ParaTerrain.GetBlockAttributeObject():SetField("OnUnLoadBlockRegion", ";MyCompany.Aries.Game.BlockEngine.OnUnLoadBlockRegion();")
	end
	

	self.region_width = attr:GetField("size", 533.3333); 
	region_width = BlockEngine.region_width;
	self.blocksize = self.region_width / self.region_size;
	blocksize = BlockEngine.blocksize;

	self.blocksize_inverse = self.region_size / self.region_width;
	blocksize_inverse = BlockEngine.blocksize_inverse;

	self.half_blocksize = blocksize / 2;


	-- default to offset 200 meters below the ground.
	--self:SetOffsetY(-200);
	self:SetOffsetY(-self.blocksize*128); -- just for debugging. 

	block_types:OnWorldLoaded();

	-- enter the block world with rendering.
    ParaTerrain.EnterBlockWorld(x,y,z);

	self:UpdateEyePosition(x, y, z);

	if(self.is_do_per_block_framemove) then
		self.framemove_co = self.framemove_co or coroutine.create(function ()
			self:FrameMove_Coroutine();
		end)
	end

	self.mytimer = self.mytimer or commonlib.Timer:new({callbackFunc = function(timer)
		self:OnFrameMove();
	end})
	self.mytimer:Change(self.sim_interval, self.sim_interval);
end

local results = {};

-- @return 0 or nil to proceed loading the region in async mode. 
-- return 1 to prevent the region from loaded
function BlockEngine.OnBeforeLoadBlockRegion()
	-- LOG.std(nil, "system", "BlockEngine", "before load block region %d %d", msg.x, msg.y);
	-- return 1 prevent the region from loaded, just in case you have your own load world logics. 
	if(GameLogic) then
		if(not GameLogic.GetFilters():apply_filters("OnBeforeLoadBlockRegion", true, msg.x, msg.y)) then
			return 1;
		end
	end
        return 0;
end

function BlockEngine.OnSaveBlockRegion()
	if(GameLogic) then
		GameLogic.GetFilters():apply_filters("OnSaveBlockRegion", true, msg.x, msg.y, msg.type);
	end
end

function BlockEngine.OnLoadBlockRegion()
	if(GameLogic) then
		if(not GameLogic.GetFilters():apply_filters("OnLoadBlockRegion", true, msg.x, msg.y)) then
			return;
		end
	end
	if(BlockEngine:IsRemote()) then
		return;
	end
	LOG.std(nil, "system", "BlockEngine", "loading block region %d %d", msg.x, msg.y);
	local region_id = msg.x*100000+msg.y;
	if(custom_model_load_map[region_id]) then
		return;
	end
	custom_model_load_map[region_id] = true;
	
	local startChunkX, startChunkY, startChunkZ = msg.x*32, 0, msg.y*32;
	local endChunkX, endChunkY, endChunkZ = startChunkX+32-1, 15, startChunkZ+32-1;

	ParaTerrain.GetBlocksInRegion(startChunkX, startChunkY, startChunkZ, endChunkX, endChunkY, endChunkZ, block.attributes.onload, results);
	
	if(results.count and results.count>0) then
		local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
		local region = EntityManager.GetRegionContainer(msg.x*512, msg.y*512);
		LOG.std(nil, "system", "BlockEngine", "calling onload for %d blocks in region %d %d", results.count, msg.x, msg.y);

		local results_x, results_y, results_z, results_tempId, results_data = results.x, results.y, results.z, results.tempId, results.data;
		for i = 1, results.count do
			local x,y,z,block_id, block_data = results_x[i], results_y[i], results_z[i], results_tempId[i], results_data[i];
			if(x and block_id) then
				local block_template = block_types.get(block_id);
				-- exclude cubeModel
				if(block_template) then
					block_template:OnBlockLoaded(x,y,z, block_data);
				end
			end
		end
	end
end

function BlockEngine.OnUnLoadBlockRegion()
	if(GameLogic) then
		if(not GameLogic.GetFilters():apply_filters("OnUnLoadBlockRegion", true, msg.x, msg.y)) then
			return;
		end
	end
	if(not BlockEngine:IsRemote()) then
		LOG.std(nil, "system", "BlockEngine", "unloading block region %d %d", msg.x, msg.y);
	end
end

function BlockEngine.OnGeneratorScript()
	if(GameLogic and not GameLogic.isRemote) then
		local block_generator = GameLogic.GetBlockGenerator();
		if(block_generator) then
			local region_x, region_y = msg.region_x, msg.region_y;
			if(not msg.chunk_x or msg.chunk_x<0) then
				block_generator:AddPendingRegion(region_x, region_y);
			else
				block_generator:AddPendingChunk(region_x, region_y, msg.chunk_x, msg.chunk_z);
			end
		end
	end
end

-- disconnect the block engine, so that no computation occurs afterwards. 
-- call this function when one exit the block based game
function BlockEngine:Disconnect()
	if(self.mytimer) then
		self.mytimer:Change();
	end
	-- call this to prevent block simultion.
	ParaTerrain.LeaveBlockWorld();
end

function BlockEngine:SetOffsetY(y)
	self.offset_y = y;
	self.max_y = y + self.blocksize*BlockEngine.region_height;
	self.min_y = y - self.blocksize*BlockEngine.region_height;
	offset_y = self.offset_y;
	ParaTerrain.SetBlockWorldYOffset(offset_y);
end

-- used to cache some game data per block
-- @return -1 means nil, 0 means empty, 1 means opaque block, 2 means deco, etc. 
function BlockEngine:GetBlockTypeInCache(x, y, z)
	local block = self:GetBlockInCache(x, y, z)
	if(block) then
		return block.type or 0;
	else
		return -1;
	end
end

-- used to cache some game data per block
-- @return -1 means nil, 0 means empty, 1 means opaque block, 2 means deco, etc. 
function BlockEngine:GetBlockTypeInCacheIdx(bx, by, bz)
	local block = self:GetBlockInCacheIdx(bx, by, bz)
	if(block) then
		return block.type or 0;
	else
		return -1;
	end
end

-- similar to GetBlockType except that index is block coordinates is uint16
-- @param bx,by,bz: block index
function BlockEngine:SetBlockAttributeInCache(x,y,z, name, value)
	local block = self:GetBlockInCache(x, y, z, true)
	if(block) then
		block[name] = value;
	end
end


-- one can set the block attribute at the given position
-- supported attributes are like "type", "texture", ...
function BlockEngine:GetBlockAttributeInCache(x,y,z, name)
	local block = self:GetBlockInCache(x, y, z)
	if(block) then
		return block[name];
	end
end

-- create/get block at given world position. 
function BlockEngine:GetBlockInCacheIdx(bx, by, bz, bCreateIfNotExist)
	local sparse_index = by*900000000+bx*30000+bz;
	local block = self.block_cache[sparse_index];
	if(block) then
		return block;
	elseif(bCreateIfNotExist) then
		-- create a default block
		block = {};
		self.block_cache[sparse_index] = block;
		return block;
	end
end

-- create/get block at given world position. 
-- @param x, y, z: real world position.
function BlockEngine:GetBlockInCache(x,y,z, bCreateIfNotExist)
	local bX, bY, bZ = self:block(x, y, z);
	local sparse_index = self:GetSparseIndex(bX, bY, bZ);
	local block = self.block_cache[sparse_index];
	if(block) then
		return block;
	elseif(bCreateIfNotExist) then
		-- create a default block
		block = {};
		self.block_cache[sparse_index] = block;
		return block;
	end
end

-- whether this block is freespace. 
function BlockEngine:IsBlockFreeSpace(bx, by, bz)
	local block_id = ParaTerrain.GetBlockTemplateByIdx(bx, by, bz);
	local block = block_types.get(block_id)
	if(not block or (not block.solid and block.obstruction)) then
		return true;
	end
end

-- get the region pos that contains x, z
function BlockEngine:GetRegionPos(x,z)
	local idx_x, idx_z;
	
	idx_x = math_floor(x / region_width);
	idx_z = math_floor(z / region_width);
	
	return idx_x, idx_z;
end

-- convert from block index to real world coordinate. use floating point operations. 
-- @param note: the returned position is always the center of the block.
function BlockEngine:ConvertToRealPosition_float(x,y,z)
	local real_x, real_y, real_z;
	
	real_x = math_floor(x / region_size);
	real_z = math_floor(z / region_size);
	local x_orgin = real_x * region_size;
	local z_orgin = real_z * region_size;
	-- local index
	local bx = (x - x_orgin + 0.5) * blocksize;
	local bz = (z - z_orgin + 0.5) * blocksize;

	real_x = real_x * region_width + bx
	real_y = (y + 0.5)*blocksize + offset_y
	real_z = real_z * region_width + bz

	return real_x, real_y, real_z;
end

-- only call this function when math is in 64 bits double, otherwise use the 32bits float version above, which is compatible with C++
function BlockEngine:ConvertToRealPosition(x,y,z)
	return (x+0.5)*blocksize, (y+0.5)*blocksize+offset_y, (z+0.5)*blocksize;
end
BlockEngine.real = BlockEngine.ConvertToRealPosition;

-- this is 64bits version. convert from block index position to real world bottom center position. 
-- @param x,y,z: block index (may be floating point index). y, z can be nil. x must be number. 
function BlockEngine:real_bottom(x,y,z)
	return (x+0.5)*blocksize, (y)*blocksize+offset_y, (z+0.5)*blocksize;
end

-- top center position of given block in real coordinate
function BlockEngine:real_top(x,y,z)
	return (x+0.5)*blocksize, (y+1)*blocksize+offset_y, (z+0.5)*blocksize;
end

-- this is 64bits version. convert from block index position to real world min position. 
-- @param x,y,z: block index (may be floating point index). y, z can be nil. x must be number. 
function BlockEngine:real_min(x,y,z)
	if(y) then
		return x*blocksize, y*blocksize+offset_y, z*blocksize;
	else
		return x*blocksize;
	end
end

-- return the real y. returned value is at the bottom of the y block.
function BlockEngine:realY(y)
	return y*blocksize + offset_y;
end

-- convert real world coordinate x,y,z to block index. use floating point operations.  
function BlockEngine:ConvertToBlockIndex_float(x,y,z)
	local idx_x, idx_y, idx_z;
	
	idx_x = math_floor(x / region_width);
	idx_z = math_floor(z / region_width);
	local x_orgin = idx_x * region_width;
	local z_orgin = idx_z * region_width;
	-- local index
	local bx = math_floor((x - x_orgin)/blocksize);
	local bz = math_floor((z - z_orgin)/blocksize);

	idx_x = idx_x*region_size + bx
	idx_y = math_floor((y-offset_y)/blocksize)
	idx_z = idx_z*region_size + bz

	local sparse_index = idx_y*900000000+idx_x*30000+bz;
	return idx_x, idx_y, idx_z, sparse_index;
end

-- only call this function when math is in 64 bits double, otherwise use the 32bits float version above, which is compatible with C++
function BlockEngine:ConvertToBlockIndex(x,y,z)
	return math_floor(x*blocksize_inverse), math_floor((y-offset_y)*blocksize_inverse), math_floor(z*blocksize_inverse);
end
BlockEngine.block = BlockEngine.ConvertToBlockIndex;

-- convert to block floating point index. 
-- @param x,y,z: real world cooridnate. y z can be nil. 
-- @return block index but NOT math.floored. 
function BlockEngine:block_float(x,y,z)
	if(y) then
		return x*blocksize_inverse, (y-offset_y)*blocksize_inverse, z*blocksize_inverse;
	else
		return x*blocksize_inverse;
	end
end

-- get the block center, based on a real world position.
function BlockEngine:GetBlockCenter(x,y,z)
	return BlockEngine:real(BlockEngine:block(x,y,z));
end
BlockEngine.center = BlockEngine.GetBlockCenter;

-- get sparse index
function BlockEngine:GetSparseIndex(x, y, z)
	return y*900000000+x*30000+z;
end

-- convert from sparse index to block x,y,z
-- @return x,y,z
function BlockEngine:FromSparseIndex(index)
	local x, y, z;
	y = math.floor(index / (900000000));
	index = index - y*900000000;
	x = math.floor(index / (30000));
	z = index - x*30000;
	return x,y,z;
end


local opposite_sides = {
	[0] = 1,[1] = 0,[2] = 3,[3] = 2,[4] = 5,[5] = 4,
}

function BlockEngine:GetOppositeSide(side)
	return opposite_sides[side];
end

-- @param x, y, z: block index
-- @return: x,y,z nearby block index. 
function BlockEngine:GetBlockIndexBySide(x,y,z,side)
	if(side == 0) then
		x = x - 1;
	elseif(side == 1) then
		x = x + 1;
	elseif(side == 2) then
		z = z - 1;
	elseif(side == 3) then
		z = z + 1;
	elseif(side == 4) then
		y = y - 1;
	elseif(side == 5) then
		y = y + 1;
	end
	return x,y,z
end

-- update eye position
function BlockEngine:UpdateEyePosition(x, y, z)
	if(y < self.min_y or y > self.max_y) then
		self.is_eye_outside = true;
	else
		self.is_eye_outside = false;
	end

	self.eye_block[1], self.eye_block[2], self.eye_block[3] = self:GetBlockCenter(x,y,z);
	self.eye[1], self.eye[2], self.eye[3] = x,y,z;
end


-- increase the block_framemove_count by one and yield coroutine if block_sim_per_frame has reached. 
-- call this function when some computation has just finished. 
local function block_compute_inc()
	block_framemove_count = block_framemove_count + 1;
	if(block_framemove_count > block_sim_per_frame) then
		block_framemove_count = 1;
		coroutine.yield(true);
	end
end

-- get the next dynamic object type in the block column x,z. It will start from the high y-1 and search downward, until one is found. 
-- @param max_dist: max dist to search downward. default to y. 
-- @return block_id, block_y: nil if no dynamic type is found downward. 
function BlockEngine:GetNextDynamicTypeInColumn(x,y,z, max_dist)
	local dist = ParaTerrain.FindFirstBlock(x,y,z, 5, max_dist or y, block.attributes.framemove);
	if(dist > 0) then
		y = y-dist;
		local block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
		return block_id, y;
	else
		return nil;
	end
end

-- @param attr: bitwise field. default to block.attributes.onload (which is usually entity block)
-- @return block_id, block_y: nil if no dynamic type is found downward. 
function BlockEngine:GetNextBlockOfTypeInColumn(x,y,z, attr, max_dist)
	attr = attr or block.attributes.onload;
	local dist = ParaTerrain.FindFirstBlock(x,y,z, 5, max_dist or y, attr);
	if(dist > 0) then
		y = y-dist;
		local block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
		return block_id, y;
	else
		return nil, nil;
	end
end

-- get the y pos of the first block of nBlockID, start searching from x, y, z in the side direction
-- @param x,y,z: y default to 0
-- @param nBlockId: the block id to search for
-- @param nSide: default to 5, which is downward, 4 if upward.
-- @param max_dist: default to 255
-- @return -1 if not found
function BlockEngine:GetFirstBlock(x, y, z, nBlockId, nSide, max_dist)
	return ParaTerrain.GetFirstBlock(x, y or 0, z, nBlockId, nSide or 5, max_dist or 255);
end

-- this is a coroutine and may yield every block_sim_per_frame framemove. 
function BlockEngine:FrameMove_Coroutine()
	-- inner radius, framemove all dynamic block near the eye position. 
	while(true) do
		local tick_count = BlockEngine.tick_count +1;

		BlockEngine.tick_count = tick_count;
		LOG.std(nil, "debug", "FrameMove_Coroutine",  "tick_count %d", tick_count)

		-- block index;
		local eye_x, eye_y, eye_z = self:block(self.eye_block[1], self.eye_block[2], self.eye_block[3]);
	
		if(tick_count%19 == 1) then
			self:FrameMoveRegion(eye_x, eye_y, eye_z, 50, 41);
		elseif(tick_count%10 == 1) then
			self:FrameMoveRegion(eye_x, eye_y, eye_z, 40, 31);
		elseif(tick_count%3 == 1) then
			self:FrameMoveRegion(eye_x, eye_y, eye_z, 30, 21);
		else
			self:FrameMoveRegion(eye_x, eye_y, eye_z, 20, 0);
		end
		coroutine.yield(true);
	end
end

-- main loop of the block engine.
function BlockEngine:OnFrameMove()
	local x, y, z = ParaScene.GetPlayer():GetPosition();
	self:UpdateEyePosition(x, y, z);

	-- resume per block framemove coroutine
	if(self.is_do_per_block_framemove) then
		if(coroutine.status(self.framemove_co) == "suspended") then
			local status, result = coroutine.resume(self.framemove_co);
			if not status then
				LOG.std(nil, "error", "BlockEngine", "framemove error in coroutine");
				echo(debug.traceback(self.framemove_co));
			end
		end
	end

	-- do per nearby game entity framemove
	-- TODO:
end


-- frame move all dynamic block in given square region.
-- @param x, y, z: the block index. y can be nil.
-- @param radius:  the square region radius
-- @param radius_from: default to nil or 0. if larger than 0, we will not simulate blocks which is in radius_from square. 
-- this allow us the framemove block with different interval according to distance to eye position. 
function BlockEngine:FrameMoveRegion(x, y, z, radius, radius_from)
	y = 255;
	local framemove_col = self.FrameMoveColumn;

	if(not radius_from or radius_from == 0) then
		local bx, by, bz;
		for bx = -radius, radius do
			for bz = -radius, radius do
				framemove_col(self, x+bx, y, z+bz);
			end
		end
	elseif(radius >= radius_from) then
		local thickness = radius - radius_from;
		local bx, by, bz;
		for bx = -radius, radius do
			for bz = -radius, -radius + thickness do
				framemove_col(self, x+bx, y, z+bz);
			end
			for bz = radius-thickness, radius do
				framemove_col(self, x+bx, y, z+bz);
			end
		end
		for bz = -radius_from+1, radius_from-1 do
			for bx = -radius, -radius + thickness do
				framemove_col(self, x+bx, y, z+bz);
			end
			for bx = radius-thickness, radius do
				framemove_col(self, x+bx, y, z+bz);
			end
		end
	else
		LOG.std(nil, "error", "BlockEngine", "error framemove region");
	end
	
end

-- framemove all blocks below y, in the x, z columns from top to bottom. 
-- @param x, y, z: the block index. y can be nil.
function BlockEngine:FrameMoveColumn(x,y,z)
	local block_id;
	-- column itself count as one. 
	block_compute_inc();

	block_id, y = self:GetNextDynamicTypeInColumn(x,y,z)
	while(block_id) do
		local block_template = block_types.create_get_type(block_id);
		if(block_template) then
			block_template:updateTick(x, y, z);
		end
		block_compute_inc();

		block_id, y = self:GetNextDynamicTypeInColumn(x,y,z);
	end
end

-- same as: BlockEngine:SetBlock(x,y,z,0, nil, flag)
function BlockEngine:SetBlockToAir(x,y,z, flag)
	BlockEngine:SetBlock(x,y,z,0,0, flag);
end

function BlockEngine:MarkBlockForUpdate(x, y, z)
	if(GameLogic) then
		GameLogic.world:MarkBlockForUpdate(x, y, z);
	end
end

function BlockEngine:IsRemote()
	if(GameLogic) then
		return GameLogic.isRemote;
	end
end


-- Sets the block ID and metadata at a given location. 
-- @param flag: bitwise field. 1 will notify neighbor blocks. 2 or nil will be the default. 3 is update with notification to nearby blocks. 
--  0 will just set block without calling the block callback func. 
-- @param entity_data: table of xml node as entity_data
-- @return true if a new block is created. 
function BlockEngine:SetBlock(x,y,z,block_id, block_data, flag, entity_data)
	local last_block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
	local last_block_data = ParaTerrain.GetBlockUserDataByIdx(x,y,z);
	block_id = block_id or last_block_id;
	block_data = block_data or 0;
	if(last_block_id==block_id and last_block_data == block_data and not entity_data) then
		return false
	else
		self:MarkBlockForUpdate(x, y, z);

		local cur_block_data = last_block_id;
		if(block_id ~= last_block_id) then
			ParaTerrain.SetBlockTemplateByIdx(x,y,z,block_id);
			cur_block_data = 0;
		end
		
		if(last_block_id > 0) then
			local last_block = block_types.get(last_block_id);
			if(last_block) then
				if(not last_block.cubeMode and last_block.customModel) then
					last_block:DeleteModel(x,y,z);
				end
				if(flag ~= 0) then
					last_block:OnBlockRemoved(x,y,z,last_block_id, last_block_data);
				end
			end
		end
		
		if(block_id > 0) then
			local block = block_types.get(block_id);
			if(block) then
				if(block_data ~= cur_block_data) then
					ParaTerrain.SetBlockUserDataByIdx(x,y,z, block_data);
				end
				if(not block.cubeMode and block.customModel) then
					block:UpdateModel(x,y,z, block_data)
				end
				if(flag ~= 0) then
					block:OnBlockAdded(x,y,z, block_data, entity_data);
				end
			end
		end

		if(flag and flag >= 3) then
			BlockEngine:NotifyNeighborBlocksChange(x, y, z, block_id);
		end
		return true;
	end
end

-- Sets the block metadata at a given location. 
-- @param flag: bitwise field. 1 will notify neighbor blocks. 2 or nil will be the default
function BlockEngine:SetBlockData(x,y,z,block_data, flag)
	local block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
	local block = block_types.get(block_id);
	if(block and block_data) then
		local last_data = ParaTerrain.GetBlockUserDataByIdx(x,y,z);
		if(last_data ~= block_data) then
			self:MarkBlockForUpdate(x, y, z);
			ParaTerrain.SetBlockUserDataByIdx(x,y,z, block_data);
			if(not block.cubeMode and block.customModel) then
				block:UpdateModel(x,y,z, block_data)
			end

			if(flag and flag>=3) then
				BlockEngine:NotifyNeighborBlocksChange(x,y,z, block.id);
			end
		end
	end
end

function BlockEngine:SetBlockDataForced(x,y,z,block_data)
	ParaTerrain.SetBlockUserDataByIdx(x,y,z, block_data);
	self:MarkBlockForUpdate(x, y, z);
end

function BlockEngine:GetBlockData(x,y,z)
	return ParaTerrain.GetBlockUserDataByIdx(x,y,z);
end

function BlockEngine:GetBlockId(x,y,z)
	return ParaTerrain.GetBlockTemplateByIdx(x,y,z);
end

function BlockEngine:GetBlockIdAndData(x, y, z)
	return ParaTerrain.GetBlockFullData(x, y, z);
end

-- get full info about a given block
-- @return block_id, block_data, entity_data
function BlockEngine:GetBlockFull(x,y,z)
	local block_id, user_data = ParaTerrain.GetBlockFullData(x, y, z);
	
	if block_id > 0 then
		local block = block_types.get(block_id);
		local node;
		if(block) then
			local entity = block:GetBlockEntity(x,y,z);
			if(entity) then
				node = entity:SaveToXMLNode();
			end
		end

		return block_id, user_data, node;
	else
		return block_id;
	end 

end

function BlockEngine:GetBlockEntityData(x,y,z)
	local block = self:GetBlock(x,y,z)
	if(block) then
		local entity = block:GetBlockEntity(x,y,z);
		if(entity) then
			return entity:SaveToXMLNode();
		end
	end
end

function BlockEngine:GetBlockEntity(x,y,z)
	local block = self:GetBlock(x,y,z)
	if(block) then
		return block:GetBlockEntity(x,y,z);
	end
end

function BlockEngine:GetBlockEntityList(from_x,from_y,from_z, to_x, to_y, to_z)
	local entityList;
	for x=from_x, to_x do
		for z=from_z, to_z do
			local block_id, y = self:GetNextBlockOfTypeInColumn(x,to_y+1,z)
			while(block_id and y >= from_y) do
				local entity = self:GetBlockEntity(x,y,z);
				if(entity) then
					entityList = entityList or {};
					entityList[#entityList+1] = entity;
				end
				block_id, y = self:GetNextBlockOfTypeInColumn(x,y,z)
			end
		end
	end 
	return entityList;
end

-- get full info about a given block
-- @return block_id, block_data, entity_data
function BlockEngine:GetBlockFull(x,y,z)
	local block_id, user_data = ParaTerrain.GetBlockFullData(x, y, z);
	
	if block_id > 0 then
		local block = block_types.get(block_id);
		local node;
		if(block) then
			local entity = block:GetBlockEntity(x,y,z);
			if(entity) then
				node = entity:SaveToXMLNode();
			end
		end

		return block_id, user_data, node;
	else
		return block_id;
	end 

end

-- return array of {x,y,z, id, data, entity_data}
function BlockEngine:GetAllBlocksInfoInAABB(aabb)
	local blocks = {};
	local min_x,min_y, min_z = aabb:GetMinValues();
	local max_x,max_y, max_z = aabb:GetMaxValues();
	for i=min_x, max_x do
		for j=min_y, max_y do
			for k=min_z, max_z do
				local id, data, entity_data = BlockEngine:GetBlockFull(i,j,k);
				if(id and id>0) then
					blocks[#blocks+1] = {i,j,k, id, data, entity_data};
				end
			end
		end
	end
	return blocks;
end


-- return the block template object. 
function BlockEngine:GetBlock(x,y,z)
	local block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
	if(block_id>0) then
		return block_types.get(block_id);
	end
end

-- return the block template table. 
function BlockEngine:GetBlockTemplateByIdx(bX, bY, bZ)
	local block_id = ParaTerrain.GetBlockTemplateByIdx(bX, bY, bZ);
	if(block_id > 0) then
		return block_types.get(block_id);
	end
end

-- Obsoleted: use BlockEngine:SetBlock
-- @param x, y, z: the block index. 
function BlockEngine.SetBlockTemplateByIdx(x,y,z,block_id, block_data)
	BlockEngine:SetBlock(x,y,z,block_id, block_data);
end

-- Obsoleted: use BlockEngine:SetBlockData
function BlockEngine.SetBlockUserDataByIdx(x,y,z,block_data)
	BlockEngine:SetBlockData(x,y,z,block_data);
end

-- is point under water
-- @param bX, bY, bZ: if nil, we will use the camera eye position. 
function BlockEngine:IsInLiquid(bX, bY, bZ)
	if(not bX) then
		eye_pos = ParaCamera.GetAttributeObject():GetField("Eye position", eye_pos);
		bX, bY, bZ = BlockEngine:block(eye_pos[1],eye_pos[2],eye_pos[3]); 
	end
	local block_id = ParaTerrain.GetBlockTemplateByIdx(bX, bY, bZ);
	if(block_id > 0) then
		local block = block_types.get(block_id);
		if(block and block.liquid) then
			return true;
		end
	end
end

-- if all 6 neighbour are empty. 
function BlockEngine:IsInAir(x,y,z)
	return ( ParaTerrain.GetBlockTemplateByIdx(x-1,y,z)==0 and  
		ParaTerrain.GetBlockTemplateByIdx(x+1,y,z)==0 and
		ParaTerrain.GetBlockTemplateByIdx(x,y-1,z)==0 and
		ParaTerrain.GetBlockTemplateByIdx(x,y+1,z)==0 and
		ParaTerrain.GetBlockTemplateByIdx(x,y,z-1)==0 and
		ParaTerrain.GetBlockTemplateByIdx(x,y,z+1)==0 );
end


-- TODO: is point under water
-- @param realX, realY, realZ: if nil, we will use the camera eye position. 
function BlockEngine:IsInLiquidReal(realX, realY, realZ)
	if(not realX) then
		eye_pos = ParaCamera.GetAttributeObject():GetField("Eye position", eye_pos);
		realX, realY, realZ = eye_pos[1],eye_pos[2],eye_pos[3]
	end
	local bX, bY, bZ = BlockEngine:block(realX, realY, realZ);
	if(not self:IsInLiquid(bX, bY, bZ)) then
		local cx, cy, cz = BlockEngine:real(bX, bY, bZ);
		if(realX<cx) then
			if(not self:IsInLiquid(bX-1, bY, bZ)) then
				if(realY<cy) then
					if(not self:IsInLiquid(bX-1, bY-1, bZ) and not self:IsInLiquid(bX, bY-1, bZ)) then
						-- TODO:
					end
				else
					if(not self:IsInLiquid(bX-1, bY+1, bZ) and not self:IsInLiquid(bX, bY-1, bZ)) then
						-- TODO:
					end
				end
			end
		else
			if(not self:IsInLiquid(bX+1, bY, bZ)) then
				if(realY<cy) then
					if(not self:IsInLiquid(bX+1, bY-1, bZ) and not self:IsInLiquid(bX, bY-1, bZ)) then
						-- TODO:
					end
				else
					if(not self:IsInLiquid(bX+1, bY+1, bZ) and not self:IsInLiquid(bX, bY-1, bZ)) then
						-- TODO:
					end
				end
			end
		end
	end
	return true;
end


-- Notifies all six neighboring blocks that from_block_id changed  
function BlockEngine:NotifyNeighborBlocksChange(x, y, z, from_block_id)
	self:OnNeighborBlockChange(x - 1, y, z, from_block_id);
	self:OnNeighborBlockChange(x + 1, y, z, from_block_id);
	self:OnNeighborBlockChange(x, y - 1, z, from_block_id);
	self:OnNeighborBlockChange(x, y + 1, z, from_block_id);
	self:OnNeighborBlockChange(x, y, z - 1, from_block_id);
	self:OnNeighborBlockChange(x, y, z + 1, from_block_id);
end

-- Notifies all six neighboring blocks that from_block_id changed, except the one on the given side. 
-- @param side: the block on this side is not notified. 
function BlockEngine:NotifyNeighborBlocksChangeNoSide(x, y, z, from_block_id, side)
    if (side ~= 0) then
        self:OnNeighborBlockChange(x - 1, y, z, from_block_id);
    end

    if (side ~= 1) then
        self:OnNeighborBlockChange(x + 1, y, z, from_block_id);
    end

    if (side ~= 4) then
        self:OnNeighborBlockChange(x, y - 1, z, from_block_id);
    end

    if (side ~= 5) then
        self:OnNeighborBlockChange(x, y + 1, z, from_block_id);
    end

    if (side ~= 2) then
        self:OnNeighborBlockChange(x, y, z - 1, from_block_id);
    end

    if (side ~= 3) then
        self:OnNeighborBlockChange(x, y, z + 1, from_block_id);
    end
end


-- Notifies a block that one of its neighbor change to the specified type
-- @param from_block_id: the block id that has changed
function BlockEngine:OnNeighborBlockChange(x, y, z, from_block_id)
    local block_id = ParaTerrain.GetBlockTemplateByIdx(x, y, z);
	if(block_id > 0) then
		local block = block_types.get(block_id)
		if (block) then
			block:OnNeighborChanged(x, y, z, from_block_id);
		end
	end
end

-- get block material
function BlockEngine:GetBlockMaterial(x,y,z)
	local block_id = ParaTerrain.GetBlockTemplateByIdx(x, y, z);
	if(block_id > 0) then
		local block = block_types.get(block_id)
		if (block) then
			return block.material;
		end
	end
	return Materials.air;
end



-- Is this block powering in the specified direction 
function BlockEngine:isBlockProvidingStrongPowerTo(x, y, z, direction)
    local block_id = ParaTerrain.GetBlockTemplateByIdx(x,y,z);
	if(block_id == 0) then
		return 0
	else
		local block_template = block_types.get(block_id);
		if(block_template) then
			return block_template:isProvidingStrongPower(x, y, z, direction);
		else
			return 0;
		end
	end
end

-- Returns the highest strong power input from this block's six neighbors. 
function BlockEngine:getBlockStrongPowerInput(x,y,z)
    local max_power = math.max(0, self:isBlockProvidingStrongPowerTo(x, y - 1, z, 5));

    if (max_power >= 15) then
        return max_power;
    else
        max_power = math.max(max_power, self:isBlockProvidingStrongPowerTo(x, y + 1, z, 4));

        if (max_power >= 15) then
            return max_power;
        else
            max_power = math.max(max_power, self:isBlockProvidingStrongPowerTo(x, y, z - 1, 3));

            if (max_power >= 15) then
                return max_power;
            else
                max_power = math.max(max_power, self:isBlockProvidingStrongPowerTo(x, y, z + 1, 2));

                if (max_power >= 15) then
                    return max_power;
                else
                    max_power = math.max(max_power, self:isBlockProvidingStrongPowerTo(x - 1, y, z, 1));

                    if (max_power >= 15) then
                        return max_power;
                    else
                        max_power = math.max(max_power, self:isBlockProvidingStrongPowerTo(x + 1, y, z, 0));
                        return max_power;
                    end
                end
            end
        end
    end
end


-- Returns the weak power being outputted by the given block to the given direction.
function BlockEngine:hasWeakPowerOutputTo(x,y,z,dir)
    return self:getWeakPowerOutputTo(x,y,z,dir) > 0;
end

-- Indicate if a material is a normal solid opaque cube.
function BlockEngine:isBlockNormalCube(x,y,z)
	local block = BlockEngine:GetBlockTemplateByIdx(x,y,z);
	return block and block:isBlockNormalCube();
end

-- Gets the indirect(weak) power level of this block to a given side. 
-- Normal cube block will output the highest strong power input as weak output to all of its six faces. 
function BlockEngine:getWeakPowerOutputTo(x,y,z,dir)
    if (BlockEngine:isBlockNormalCube(x, y, z)) then
        return self:getBlockStrongPowerInput(x, y, z);
    else
        local block = BlockEngine:GetBlockTemplateByIdx(x,y,z);
		if(block) then
			return block:isProvidingWeakPower(x, y, z, dir);
		else
			return 0;
		end
    end
end

-- Used to see if one of the blocks next to you or your block is getting power from a neighboring block. Used by
-- items like TNT or Doors so they don't have going straight into them.  
function BlockEngine:isBlockIndirectlyGettingPowered(x, y, z)
	if( self:getWeakPowerOutputTo(x, y - 1, z, 5) > 0 or self:getWeakPowerOutputTo(x, y + 1, z, 4) > 0 or 
		self:getWeakPowerOutputTo(x, y, z - 1, 3) > 0 or self:getWeakPowerOutputTo(x, y, z + 1, 2) > 0 or 
		self:getWeakPowerOutputTo(x - 1, y, z, 1) > 0 or self:getWeakPowerOutputTo(x + 1, y, z, 0) > 0 ) then
		return true;
	else
		return false;
	end
end

-- get strongest indirect power from the neighboring 6 blocks. wires will transmit indirect power to its neighbor
function BlockEngine:getStrongestIndirectPower(x, y, z)
    local max_power = 0;

    for dir = 0, 5 do
		local x1,y1,z1 = BlockEngine:GetBlockIndexBySide(x,y,z,dir)
        local power = self:getWeakPowerOutputTo(x1,y1,z1, BlockEngine:GetOppositeSide(dir));

        if (power >= 15) then
            return 15;
        elseif (power > max_power) then
            max_power = power;
        end
    end

    return max_power;
end

-- Performs check to see if the block is a normal, solid block, or if the metadata of the block indicates that its
-- facing puts its solid side upwards. (inverted stairs, for example)
-- Returns true if the block at the given coordinate has a solid (buildable) top surface.
function BlockEngine:DoesBlockHaveSolidTopSurface(x,y,z)
	local block = self:GetBlock(x,y,z);
    if(block and block:isNormalCube()) then
		return true;
	end
end    



-- dump the current state of the block engine
function BlockEngine:Dump()
	echo("----------------------dumping block engine -------------------");
	echo({eye_block = self.eye_block, eye = self.eye, min_y = self.min_y, max_y = self.max_y});
end

--[[
Title: Chunk column
Author(s): LiXizhi
Date: 2013/8/27
Desc: This is in-memory implementation of Chunk column. 
A chunk column contains 16*16(*256) blocks. 
Each vertical section contains 16^3 blocks. 
-----------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/World/Chunk.lua");
local Chunk = commonlib.gettable("MyCompany.Aries.Game.World.Chunk");

chunkData = Chunk:new():InitFromChunkData(chunkData);
for worldX, worldY, worldZ, block_id in chunkData:EachBlockW() do
	ParaTerrain.SetBlockTemplateByIdx(worldX, worldY, worldZ, block_id);
end
-----------------------------------------------
]]
NPL.load("(gl)script/ide/timer.lua");
NPL.load("(gl)script/ide/math/bit.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/World/Section.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/UniversalCoords.lua");
local UniversalCoords = commonlib.gettable("MyCompany.Aries.Game.Common.UniversalCoords");
local Section = commonlib.gettable("MyCompany.Aries.Game.World.Section");

local rshift = mathlib.bit.rshift;
local lshift = mathlib.bit.lshift;
local band = mathlib.bit.band;
local bor = mathlib.bit.bor;

local tostring = tostring;
local format = format;
local type = type;

-- for performance testing
--ParaTerrain_SetBlockTemplateByIdx = function() end
--ParaTerrain_GetBlockTemplateByIdx = function() return 0 end

local Chunk = commonlib.inherit(nil, commonlib.gettable("MyCompany.Aries.Game.World.Chunk"))

local HALFSIZE = 16 * 16 * 128;

Chunk.Persistent = true;

-- containing world manager
Chunk.World = nil;
-- universal coords
Chunk.Coords = nil;

function Chunk:ctor()
	self._Sections = {};
	self._BiomesArray = {};
	self.elapsedTime= 0;
end

function Chunk:Init(world, chunkX, chunkZ)
	self.World = world;
	self.Coords = UniversalCoords:new():FromChunk(chunkX, chunkZ);
	self.chunkX = chunkX;
	self.chunkZ = chunkZ;
	self.elapsedTime= 0;
	return self;
end

-- @param data: is actually another chunk without meta tables. 
function Chunk:InitFromChunkData(data)
	self.chunkX = data.chunkX;
	self.chunkZ = data.chunkZ;
	self.elapsedTime = data.elapsedTime;
	self._Sections = data._Sections;
	self._BiomesArray = data._BiomesArray;
	return self;
end

-- @param index: [0, 4096)  16*16*16
local function UnpackBlockIndex(index)
	local cy = rshift(index, 8);
	index = band(index, 0xff);
	local cz = rshift(index, 4);
	local cx = band(index, 0xf);
	return cx, cy, cz;
end

-- iterator (worldX, worldY, worldZ, block_id) of all blocks in the chunk
-- block pos is in world coordinate system
function Chunk:EachBlockW()
	local iSection, section = next(self._Sections, nil)
	local packedIndex, block_id;
	
	local worldXOffset = self.chunkX*16;
	local worldYOffset = (iSection or 0)*16;
	local worldZOffset = self.chunkZ*16;
	return function()
		if(section) then
			packedIndex, block_id = next(section, packedIndex);
			if(not packedIndex) then
				iSection, section = next(self._Sections, iSection);
				if(section) then
					worldYOffset = iSection*16;
					packedIndex, block_id = next(section, packedIndex);
				end
			end
		end
		if(packedIndex) then
			local worldX, worldY, worldZ = UnpackBlockIndex(packedIndex);
			return worldXOffset+worldX, worldYOffset+worldY, worldZOffset+worldZ, block_id;
		end
	end
end

-- @param x,y,z: in world coordinates
-- @param side: 4 upward, 5 downward
-- @return the distance to first block.
function Chunk:FindFirstBlock(x, y, z, side, max_dist)
	x = x - self.chunkX*16;
	z = z - self.chunkZ*16;
	max_dist = max_dist or 256;
	local dist = 0;

	-- skip first block when dist==0
	dist = dist + 1;
	if(side == 4) then
		y = y + 1;
	elseif(side == 5) then
		y = y - 1;
	else
		return -1;
	end

	while(y>=0 and y <= 256 and dist <= max_dist) do
		local section = self._Sections[rshift(y, 4)];
		if (not section) then
			if(side == 4) then
				local new_y = band(y, 0xff0) + 16;
				dist = dist + (new_y - y);
				y = new_y;
			elseif(side == 5) then
				new_y = band(y, 0xff0) - 1;
				dist = dist + (y-new_y);
				y = new_y;
			else
				return -1;
			end
		else
			local block_id = section[bor(lshift(band(y,0xF), 8),  bor(lshift(z, 4), x))] or 0;
			if(block_id == 0) then
				dist = dist + 1;
				if(side == 4) then
					y = y + 1;
				elseif(side == 5) then
					y = y - 1;
				else
					return -1;
				end
			else
				return dist;
			end
		end
	end
	return -1;
end

function Chunk:InitBlockChangesTimer()
end

function Chunk:Dispose()
end

function Chunk:MarkToSave()
	
end

function Chunk:GetBlockId(coords)
	local section = self._Sections[rshift(coords:GetBlockY(), 4)];
	if (not section) then
		return 0; -- empty
	end
	return section[coords.SectionPackedCoords] or 0;
end

-- @param blockX: X or coords. if coords Y,Z should be nil.
function Chunk:GetType(blockX, blockY, blockZ)
	if(not blockY) then
		return self:GetBlockId(blockX)
	else
		return self:GetBlockIdByPos(blockX, blockY, blockZ)
	end
end

function Chunk:SetTimeStamp(time_stamp)
	self.timeStamp = time_stamp or 1;
end

function Chunk:GetTimeStamp()
	-- cache result in self.timeStamp to accelerate for next call. 
	return self.timeStamp or 0;
end

function Chunk:GetBlockIdByPos(blockX, blockY, blockZ)
	local section = self._Sections[rshift(blockY, 4)];
	if (not section) then
		return 0; -- empty
	end
	return section[bor(lshift(band(blockY,0xF), 8),  bor(lshift(blockZ, 4), blockX))] or 0;
end

function Chunk:GetData(coords)
	-- TODO:
	return 0;
end

-- alias: SetData(coords, data)
-- @param blockX: coordinates or int
function Chunk:SetData(blockX, blockY, blockZ, data)
	-- TODO:
end

-- @param pos: section_id
function Chunk:AddNewSection(pos)
	-- local section = Section.Load(self, pos);
	local section = {};
	self._Sections[pos] = section;
	return section;
end

function Chunk:SetBiomeColumn(x, z, biomeId)
    self._BiomesArray[z*16 + x] = biomeId;
end

function Chunk:OnSetType(blockX, blockY, blockZ, block_id)
end

function Chunk:OnSetTypeByCoords(coords, block_id)
end

function Chunk:SetType(blockX, blockY, blockZ, block_id, needsUpdate)
	
	local sectionId = rshift(blockY, 4);
	local section = self._Sections[sectionId];

	if (not section ) then
		if (block_id ~= 0) then
			section = self:AddNewSection(sectionId);
		else
			return;
		end
	end
	section[bor(lshift(band(blockY, 0xF), 8), bor(lshift(blockZ, 4),  blockX)) ] = block_id;
	self:OnSetType(blockX, blockY, blockZ, block_id);
	if (needsUpdate~=false) then
		self:BlockNeedsUpdate(blockX, blockY, blockZ);
	end
end

-- @param needsUpdate: default to true
function Chunk:SetTypeByCoords(coords, block_id, needsUpdate)
	local sectionId = rshift(coords.WorldY, 4);
	local section = self._Sections[sectionId];

	if (not section ) then
		if (block_id ~= 0) then
			section = self:AddNewSection(sectionId);
		else
			return;
		end
	end
	section[coords.SectionPackedCoords] = block_id;
	self:OnSetTypeByCoords(coords, block_id);

	if (needsUpdate~=false) then
		self:BlockNeedsUpdate(coords:GetBlockX(), coords:GetBlockY(), coords:GetBlockZ());
	end
end

function Chunk:BlockNeedsUpdate(blockX, blockY, blockZ)
	-- LOG.std(nil, "debug", "Chunk", "BlockNeedsUpdate Chunk(%d, %d) %d, %d, %d", self.Coords:GetChunkX(), self.Coords:GetChunkZ(), blockX, blockY, blockZ);
end


-- this function matches exactly with the C++ implementation of same function. 
function Chunk:GetMapChunkData(bIncludeInit, verticalSectionFilter)
	verticalSectionFilter = verticalSectionFilter or 0xffff;
	NPL.load("(gl)script/apps/Aries/Creator/Game/Common/BlockDataCodec.lua");
	local SameIntegerEncoder = commonlib.gettable("MyCompany.Aries.Game.Common.SameIntegerEncoder");
	local outputStream = ParaIO.open("<memory>", "w");

	-- append version format
	outputStream:WriteString("chunkV1");
	local nChunkSize = 0;
	local nChunkSizeLocation = outputStream:GetFileSize();
	outputStream:WriteInt(nChunkSize);
		
	local blockIdEncoder = SameIntegerEncoder:new():init(outputStream);
	local blockDataEncoder = SameIntegerEncoder:new():init(outputStream);

	for y = 0, 15 do
		if ( band(verticalSectionFilter, lshift(1,y)) ~= 0) then
			outputStream:WriteInt(y);
			local nBlockCount = 0;
			local nBlockCountIndex = outputStream:GetFileSize();
			outputStream:WriteInt(nBlockCount);
			local pChunk = self._Sections[y];
			if (pChunk and next(pChunk)) then
				blockIdEncoder:Reset();
				local nCount = 4096;
				for i = 0, nCount-1 do
					local blockId = pChunk[i];
					if (blockId) then
						blockIdEncoder:Append(blockId);
						nBlockCount = nBlockCount + 1;
					else
						blockIdEncoder:Append(0);
					end
				end
				blockIdEncoder:Finalize();
				-- TODO: data not supported at the moment. 
				blockDataEncoder:Reset();
				blockDataEncoder:Append(0, 4096);
				blockDataEncoder:Finalize();
			else
				blockIdEncoder:Reset();
				blockIdEncoder:Append(0, 4096);
				blockIdEncoder:Finalize();
				blockDataEncoder:Reset();
				blockDataEncoder:Append(0, 4096);
				blockDataEncoder:Finalize();
			end
			outputStream:seek(nBlockCountIndex);
			outputStream:WriteInt(nBlockCount);
			outputStream:SetFilePointer(0, 2); -- 2 is relative to end of file
		end
	end
	outputStream:seek(nChunkSizeLocation);
	outputStream:WriteInt(outputStream:GetFileSize() - nChunkSizeLocation - 4);
	outputStream:SetFilePointer(0, 2); -- 2 is relative to end of file
	local data = outputStream:GetText(0, -1);
	outputStream:close();
	return data;
end

function Chunk:ApplyMapChunkData(chunkData, verticalSectionFilter)
end

function Chunk:FillChunk(chunkData, verticalSectionFilter, hasAdditionalData)
end

function Chunk:ResetRelightChecks()
end

function Chunk:IsEmpty()
	return true;
end

function Chunk:OnChunkUnload()
end

--[[
Title: Chunk keep data both on Lua and C++
Author(s): LiXizhi
Date: 2013/8/27
Desc: 16*16(*256) block columns
Since LuaJit is very fast. we will keep data on lua as well, to eliminate all ParaTerrain.GetBlockTemplateByIdx calls. 
ParaTerrain.SetBlockTemplateByIdx is still the performance bottle neck. 
-----------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/World/ChunkCpp.lua");
local ChunkCpp = commonlib.gettable("MyCompany.Aries.Game.World.ChunkCpp");
-----------------------------------------------
]]
NPL.load("(gl)script/ide/timer.lua");
NPL.load("(gl)script/ide/math/bit.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/World/Section.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/UniversalCoords.lua");
local UniversalCoords = commonlib.gettable("MyCompany.Aries.Game.Common.UniversalCoords");
local Section = commonlib.gettable("MyCompany.Aries.Game.World.Section");
local block = commonlib.gettable("MyCompany.Aries.Game.block")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types");

local rshift = mathlib.bit.rshift;
local lshift = mathlib.bit.lshift;
local band = mathlib.bit.band;
local bor = mathlib.bit.bor;

local tostring = tostring;
local format = format;
local type = type;

if(not ParaTerrain) then
	return;
end
local ParaTerrain_SetBlockTemplateByIdx = ParaTerrain.SetBlockTemplateByIdx;
local ParaTerrain_GetBlockTemplateByIdx = ParaTerrain.GetBlockTemplateByIdx;
local ParaTerrain_SetBlockUserDataByIdx = ParaTerrain.SetBlockUserDataByIdx;
local ParaTerrain_GetBlockUserDataByIdx = ParaTerrain.GetBlockUserDataByIdx;

-- for performance testing
--ParaTerrain_SetBlockTemplateByIdx = function() end
--ParaTerrain_GetBlockTemplateByIdx = function() return 0 end

local Chunk = commonlib.inherit(nil, commonlib.gettable("MyCompany.Aries.Game.World.ChunkCpp"))

local HALFSIZE = 16 * 16 * 128;

Chunk.Persistent = true;

-- containing world manager
Chunk.World = nil;
-- universal coords
Chunk.Coords = nil;

function Chunk:ctor()
	self._BiomesArray = {};
end

function Chunk:Init(world, chunkX, chunkZ)
	self.World = world;
	self.Coords = UniversalCoords:new():FromChunk(chunkX, chunkZ);
	self.chunkX = chunkX;
	self.chunkZ = chunkZ;
	self.elapsedTime= 0;
	return self;
end

function Chunk:InitBlockChangesTimer()
end

function Chunk:Dispose()
end

function Chunk:MarkToSave()
	
end

-- clear up all data during world generation. 
function Chunk:Clear()
	-- self._BiomesArray = {};
end


function Chunk:GetBlockId(coords)
	return ParaTerrain_GetBlockTemplateByIdx(coords.WorldX, coords.WorldY, coords.WorldZ);
end

-- @param blockX: X or coords. if coords Y,Z should be nil.
function Chunk:GetType(blockX, blockY, blockZ)
	if(not blockY) then
		return self:GetBlockId(blockX)
	else
		return self:GetBlockIdByPos(blockX, blockY, blockZ)
	end
end

function Chunk:SetTimeStamp(time_stamp)
	self.timeStamp = time_stamp or 1;
	ParaTerrain.SetChunkColumnTimeStamp(self.Coords.WorldX, self.Coords.WorldZ, self.timeStamp);
end

function Chunk:GetTimeStamp()
	-- cache result in self.timeStamp to accelerate for next call. 
	if(not self.timeStamp or self.timeStamp<0) then
		self.timeStamp = ParaTerrain.GetChunkColumnTimeStamp(self.Coords.WorldX, self.Coords.WorldZ);
	end
	return self.timeStamp;
end

function Chunk:GetBlockIdByPos(blockX, blockY, blockZ)
	return ParaTerrain_GetBlockTemplateByIdx(self.Coords.WorldX+blockX, self.Coords.WorldY+blockY, self.Coords.WorldZ+blockZ);
end

function Chunk:GetData(coords)
	return ParaTerrain_GetBlockUserDataByIdx(coords.WorldX, coords.WorldY, coords.WorldZ);
end

-- alias: SetData(coords, data)
-- @param blockX: coordinates or int
function Chunk:SetData(blockX, blockY, blockZ, data)
	if(blockZ) then
		ParaTerrain_SetBlockUserDataByIdx(self.Coords.WorldX+blockX, self.Coords.WorldY+blockY, self.Coords.WorldZ+blockZ, data or 0);
	elseif(blockY) then
		local coords = blockX;
		data = blockY;
		ParaTerrain_SetBlockUserDataByIdx(coords.WorldX, coords.WorldY, coords.WorldZ, data or 0);
	end
end

-- @param pos: section_id
function Chunk:AddNewSection(pos)
	local section = {};
	self._Sections[pos] = section;
	return section;
end

function Chunk:SetBiomeColumn(x, z, biomeId)
    self._BiomesArray[z*16 + x] = biomeId;
end

function Chunk:OnSetType(blockX, blockY, blockZ, block_id)
end

function Chunk:OnSetTypeByCoords(coords, block_id)
end

function Chunk:SetType(blockX, blockY, blockZ, block_id, needsUpdate)
	-- echo({"SetBlock", self.Coords.WorldX+blockX, self.Coords.WorldY+blockY, self.Coords.WorldZ+blockZ, block_id});
	ParaTerrain_SetBlockTemplateByIdx(self.Coords.WorldX+blockX, self.Coords.WorldY+blockY, self.Coords.WorldZ+blockZ, block_id or 0);
end

-- @param needsUpdate: default to true
function Chunk:SetTypeByCoords(coords, block_id, needsUpdate)
	ParaTerrain_SetBlockTemplateByIdx(coords.WorldX, coords.WorldY, coords.WorldZ, block_id or 0);
end

function Chunk:BlockNeedsUpdate(blockX, blockY, blockZ)
	-- LOG.std(nil, "debug", "Chunk", "BlockNeedsUpdate Chunk(%d, %d) %d, %d, %d", self.Coords:GetChunkX(), self.Coords:GetChunkZ(), blockX, blockY, blockZ);
end

function Chunk:GetMapChunkData(bIncludeInit, verticalSectionFilter)
	return ParaTerrain.GetMapChunkData(self.Coords:GetChunkX(), self.Coords:GetChunkZ(), bIncludeInit, verticalSectionFilter);
end

-- @param index: [0, 4096)  16*16*16
local function UnpackBlockIndex(index)
	local cy = rshift(index, 8);
	index = band(index, 0xff);
	local cz = rshift(index, 4);
	local cx = band(index, 0xf);
	return cx, cy, cz;
end

function Chunk:ApplyMapChunkData(chunkData, verticalSectionFilter)
	local modified_blocks = {};
	
	ParaTerrain.ApplyMapChunkData(self.chunkX, self.chunkZ, verticalSectionFilter, chunkData, modified_blocks);
	-- echo({"Chunk:ApplyMapChunkData", modified_blocks, self.chunkX, self.chunkZ,})

	local removeList = modified_blocks["remove"];
	local addList = modified_blocks["add"];
	local addDataList = modified_blocks["addData"];
	local modDataList = modified_blocks["modData"];

	local worldX = self.Coords.WorldX;
	local worldZ = self.Coords.WorldZ;
	
	-- a block is deleted or replaced
	if(removeList) then
		local packedIndex, block_id;
		packedIndex, block_id = next(removeList, packedIndex)
		while(packedIndex) do
			local chunkY = band(packedIndex, 0xf);
			local x, y, z = UnpackBlockIndex(rshift(packedIndex,4));
			x = worldX+x;
			y = chunkY*16+y;
			z = worldZ+z;
			local block_template = block_types.get(block_id);
			if(block_template) then
				if(not block_template.cubeMode and block_template.customModel) then
					block_template:DeleteModel(x,y,z);
				end
				block_template:OnBlockRemoved(x,y,z,block_id, 0);
			end

			packedIndex, block_id = next(removeList, packedIndex)
		end
	end

	-- new block is added
	if(addList) then
		local packedIndex, block_id;
		packedIndex, block_id = next(addList, packedIndex);
		while(packedIndex) do
			local chunkY = band(packedIndex, 0xf);
			local x, y, z = UnpackBlockIndex(rshift(packedIndex,4));
			x = worldX+x;
			y = chunkY*16+y;
			z = worldZ+z;
			local block_template = block_types.get(block_id);
			if(block_template) then
				local block_data = addDataList[packedIndex] or 0;
				if(not block_template.cubeMode and block_template.customModel) then
					block_template:UpdateModel(x,y,z, block_data)
				end
				block_template:OnBlockAdded(x,y,z, block_data);
			end

			packedIndex, block_id = next(addList, packedIndex)
		end
	end
	-- only data field is changed, block id is not changed
	if(modDataList) then
		local packedIndex, block_data;
		packedIndex, block_data = next(modDataList, packedIndex);
		while(packedIndex) do
			local chunkY = band(packedIndex, 0xf);
			local x, y, z = UnpackBlockIndex(rshift(packedIndex,4));
			x = worldX+x;
			y = chunkY*16+y;
			z = worldZ+z;
			local block_template = block_types.get(block_id);
			if(block_template) then
				if(not block_template.cubeMode and block_template.customModel) then
					block_template:UpdateModel(x,y,z, block_data)
				end
			end
			packedIndex, block_data = next(modDataList, packedIndex);
		end
	end

	local timeStamp = self:GetTimeStamp();
	if(timeStamp <= 0) then
		self:SetTimeStamp(1);
		-- LOG.std(nil, "debug", "Chunk", "chunk %d %d loaded from ApplyMapChunkData. last time stamp: %d", self.chunkX, self.chunkZ, timeStamp);
	end
end


function Chunk:FillChunk(chunkData, verticalSectionFilter, hasAdditionalData)
	self:ApplyMapChunkData(chunkData, verticalSectionFilter)
	local results = {};
	-- tricky negative chunkY is actually verticalSectionFilter.
	ParaTerrain.GetBlocksInRegion(self.chunkX, -verticalSectionFilter, self.chunkZ, self.chunkX, -verticalSectionFilter, self.chunkZ, block.attributes.onload, results);
	if(results.count and results.count>0) then
		local results_x, results_y, results_z, results_tempId, results_data = results.x, results.y, results.z, results.tempId, results.data;
		for i = 1, results.count do
			local x,y,z,block_id, block_data = results_x[i], results_y[i], results_z[i], results_tempId[i], results_data[i];
			if(x and block_id) then
				local block_template = block_types.get(block_id);
				-- exclude cubeModel
				if(block_template) then
					block_template:OnBlockLoaded(x,y,z, block_data);
				end
			end
		end
	end
end

function Chunk:ResetRelightChecks()
end

function Chunk:IsEmpty()
	return false;
end

function Chunk:OnChunkUnload()
	-- TODO:
end

--[[
Title: World
Author(s): LiXizhi
Date: 2014/6/30
Desc: the base world class
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/World/World.lua");
local World = commonlib.gettable("MyCompany.Aries.Game.World.World")
local world = World:new():Init(server_manager);
world:FrameMove();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/World/WorldBlockAccess.lua")
NPL.load("(gl)script/apps/Aries/Creator/Game/Physics/PhysicsWorld.lua");
local PhysicsWorld = commonlib.gettable("MyCompany.Aries.Game.PhysicsWorld");
local GameRules = commonlib.gettable("MyCompany.Aries.Game.GameRules");
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types");
local block = commonlib.gettable("MyCompany.Aries.Game.block")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local WorldCommon = commonlib.gettable("MyCompany.Aries.Creator.WorldCommon")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

---------------------------
-- create class
---------------------------
local World = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.World.WorldBlockAccess"), commonlib.gettable("MyCompany.Aries.Game.World.World"))

World.class_name = "World";

function World:ctor()
	self.worldTrackers = commonlib.UnorderedArray:new();
	if(self.cpp_chunk == nil) then
		self.cpp_chunk = true;
	end
end

-- @param server_manager: can be nil for client or standalone
-- @param saveHandler: can be nil for WorldClient
function World:Init(server_manager, saveHandler)
	self:SetSeed(WorldCommon.GetWorldTag("seed") or GameLogic.options.world_seed);
	if(not saveHandler) then
		-- create a null handler if no one is specified. 
		NPL.load("(gl)script/apps/Aries/Creator/Game/World/SaveWorldHandler.lua");
		local SaveWorldHandler = commonlib.gettable("MyCompany.Aries.Game.SaveWorldHandler")
		saveHandler = SaveWorldHandler:new():Init("");
	end
	self.saveHandler = saveHandler;
	self.options = GameLogic.options;
	self.chunkProvider = self:CreateChunkProvider();
	self:InitBlockGenerator();
	return self;
end

-- virtual function: Creates the chunk provider for this world. Called in the constructor. 
function World:CreateChunkProvider()
    NPL.load("(gl)script/apps/Aries/Creator/Game/World/ChunkProviderServer.lua");
	local ChunkProviderServer = commonlib.gettable("MyCompany.Aries.Game.World.ChunkProviderServer");
	return ChunkProviderServer:new():Init(self);
end

function World:GetChunkProvider()
	return self.chunkProvider;
end

function World:GetServerManager()
	return nil;
end

function World:GetPlayer()
	return EntityManager.GetPlayer();
end

function World:OnPreloadWorld()
	GameLogic.SetIsRemoteWorld(false, false);
end

function World:GetWorldPath()
	if(not self.worldpath) then
		self.worldpath = ParaWorld.GetWorldDirectory();
	end
	return self.worldpath;
end

-- world tag "world_generator", "seed"
function World:InitBlockGenerator()
	-- load block generator
	local block = commonlib.gettable("MyCompany.Aries.Game.block")
	local world_generator = WorldCommon.GetWorldTag("world_generator");
	local seed = WorldCommon.GetWorldTag("seed");
	
	block.auto_gen_terrain_block = true;

	local block_generator;
	if(world_generator and world_generator~="") then
		if(world_generator == "flat") then
			-- only used in haqi, Not in paracraft
			block.auto_gen_terrain_block = true;
			block_generator = self:GetChunkProvider():CreateGenerator("flat");
			block_generator:SetFlatLayers({
				{y = 126, block_id = block_types.names.underground_shell},
			});
		else
			-- generators in paracraft
			block.auto_gen_terrain_block = false;
			if(world_generator == "superflat") then
				block_generator = self:GetChunkProvider():CreateGenerator("flat");
			elseif(world_generator:match("^flat%d*")) then
				local land_y = world_generator:match("^flat(%d*)");
				land_y = tonumber(land_y) or 4;
				block_generator = self:GetChunkProvider():CreateGenerator("flat");
				local layers = {};
				layers[1] = {y = 0, block_id = block_types.names.Bedrock}
				for i = 1, land_y do
					layers[i+1] = {y = i, block_id = block_types.names.underground_shell}
				end
				block_generator:SetFlatLayers(layers);

			elseif(world_generator == "empty" or 
				-- Disable complex generator on mobile platform for the moment, since performance is really bad with current implementation. 
				System.options.IsMobilePlatform) then
				block_generator = self:GetChunkProvider():CreateGenerator("empty");
			else
				-- any custom generator by name. 
				block_generator = self:GetChunkProvider():CreateGenerator(world_generator);
			end
		end
		-- disable real world terrain 
		ParaTerrain.GetAttributeObject():SetField("RenderTerrain",false);
	else
		block_generator = self:GetChunkProvider():CreateGenerator("empty");
		-- enable real world terrain 
		ParaTerrain.GetAttributeObject():SetField("RenderTerrain",true);
	end
	self:GetChunkProvider():SetGenerator(block_generator);
	GameLogic.options.has_real_terrain = ParaTerrain.GetAttributeObject():GetField("RenderTerrain",true);
end

function World:ReplaceWorld(oldWorld)
	if(oldWorld) then
		oldWorld:OnWeaklyDestroyWorld();
	end
end

-- this function is called when the world is possibly replaced by another world object
-- thus as toggling from client world to server world, without leaving the world.
function World:OnWeaklyDestroyWorld()
	self:GetChunkProvider():OnExit();
end

function World:OnExit()
	self:OnWeaklyDestroyWorld();
end

-- world trackers may be temporily disabled and then enabled again, for example when client receives
-- block change packet and updates the local world. The updated blocks should not be tracked. 
function World:EnableWorldTracker(bEnabled)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:EnableTracker(bEnabled);
	end
end


function World:IsClient()
	return false;
end


function World:AddWorldTracker(worldTracker)
	if(not self.worldTrackers:contains(worldTracker)) then
		self.worldTrackers:add(worldTracker);
	end
end

function World:RemoveWorldTracker(worldTracker)
	self.worldTrackers:removeByValue(worldTracker);
end

function World:ClearWorldTrackers()
	self.worldTrackers:clear();
end

function World:FrameMove(deltaTime)
end

-- set world size by center and extend. 
-- mostly used on 32/64bits server to prevent running out of memory. 
function World:SetWorldSize(x, y, z, dx, dy, dz)
	if(not x) then
		x, y, z = self:GetSpawnPoint();
		x, y, z = BlockEngine:block(x, y, z);
	end
	dx = dx or 256;
	dy = dy or 128;
	dz = dz or 256;
	-- set attribute to low level block engine. 
	local attr = ParaTerrain.GetBlockAttributeObject();
	attr:SetField("MinWorldPos", {x-dx, y-dy, z-dz});
	attr:SetField("MaxWorldPos", {x+dx, y+dy, z+dz});
end

-- get player home spawn position. 
function World:GetSpawnPoint()
	local x, y, z;
	local entity = EntityManager.GetEntity("player_spawn_point") or EntityManager.GetEntity("player_spawn");
	if(entity) then
		x, y, z = entity:GetPosition()
	end
	if(not x) then
		x, y, z = unpack(self.options.login_pos); 
	end
	return x, y, z;
end

-- set player home position. 
-- @param x, y, z: if nil, the current player position is used. 
function World:SetSpawnPoint(x,y,z)
	local pos = GameLogic.GetFilters():apply_filters("BeforeSetSpawnPoint", {x,y,z});
	if(pos) then
		x,y,z = unpack(pos);
		local entity = EntityManager.GetEntity("player_spawn_point")
		if(not entity) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/CreateBlockTask.lua");
			local task = MyCompany.Aries.Game.Tasks.CreateBlock:new({block_id = block_types.names.player_spawn_point, blockX=x, blockY=y, blockZ=z})
			task:Run();
			entity = EntityManager.GetEntity("player_spawn_point")
		end
		if(entity) then
			if(not x) then
				x,y,z = ParaScene.GetPlayer():GetPosition();
			end
			entity:SetPosition(x,y,z);
		end
	end
	GameLogic.GetFilters():apply_filters("SetSpawnPoint", nil, x,y,z);
	return x,y,z;
end

function World:GetWorldInfo()
	return WorldCommon:GetWorldInfo();
end

-- Called to place all entities as part of a world
function World:SpawnEntityInWorld(entity)
	entity:Attach();
end

function World:GetTotalWorldTime()
	return 10;
end

function World:GetWorldTime()
	return 10;
end

function World:GetGameRules()
	return GameRules;
end

-- Returns this world's current save handler
function World:GetSaveHandler()
	return self.saveHandler;
end

-- get player
-- @param name: if nil or "player", the current player is returned. 
function World:GetPlayer(name)
	return EntityManager.GetPlayer(name);
end

function World:GetEntityByID(id)
	return EntityManager.GetEntityById(id);
end

-- On the client, re-renders the block. On the server, sends the block to the client (which will re-render it),
-- including the tile entity description packet if applicable. 
function World:MarkBlockForUpdate(x, y, z)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:MarkBlockForUpdate(x,y,z);
	end
end

-- on client does nothing, on server broadcase to observing client
function World:OnChunkGenerated(chunkX, chunkZ)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:OnChunkGenerated(chunkX, chunkZ);
	end
end

-- On the client, re-renders this block. On the server, does nothing. 
function World:MarkBlockForRenderUpdate(x,y,z)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:MarkBlockForRenderUpdate(x,y,z);
	end
end

-- On the client, re-renders all blocks in this range, inclusive. On the server, does nothing.
function World:MarkBlockRangeForRenderUpdate(min_x, min_y, min_z, max_x, max_y, max_z)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:MarkBlockRangeForRenderUpdate(min_x, min_y, min_z, max_x, max_y, max_z);
	end
end

function World:OnEntityAdded(entity)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:OnEntityCreate(entity);
	end
end

function World:OnEntityRemoved(entity)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:OnEntityDestroy(entity);
	end
end

function World:OnPlaySound(soundName, x, y, z, volume, pitch)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:PlaySound(soundName, x, y, z, volume, pitch);
	end
end

-- virtual: set new damage to a given block
-- @param damage: [1-10), other values will remove it. 
function World:DestroyBlockPartially(entityId, x,y,z, damage)
	for i=1, #(self.worldTrackers) do
		self.worldTrackers[i]:DestroyBlockPartially(entityId, x,y,z, damage);
	end
end

function World:GetChunkFromChunkCoords(chunkX, chunkZ)
	return self.chunkProvider:ProvideChunk(chunkX, chunkZ);
end

-- total number of world ticks since the world is created. 
function World:GetTotalWorldTime()
    return self:GetWorldInfo():GetWorldTotalTime();
end

-- current world time in day-light cycle (repeat in a day).
function World:GetWorldTime()
    return self:GetWorldInfo():GetWorldTime();
end

function World:Tick()
	self:GetWorldInfo():SetTotalWorldTime(self:GetWorldInfo():GetWorldTotalTime() + 1);
end

-- update the entity in the world
-- @param bForceUpdate: default to true. if true, the entity's framemove function will be called.
function World:UpdateEntity(entity, bForceUpdate)
	if(not bForceUpdate) then
		bForceUpdate = true;
	end
    
    entity.lastTickPosX = entity.x;
    entity.lastTickPosY = entity.y;
    entity.lastTickPosZ = entity.z;
    entity.prevRotationYaw = entity.facing;
    entity.prevRotationPitch = entity.rotationPitch;

    if (bForceUpdate) then
        entity.ticksExisted = (entity.ticksExisted or 0) + 1;

        if (entity.ridingEntity) then
            entity:FrameMoveRidding(0);
        else
            entity:FrameMove(0);
        end
    end
    
    if (bForceUpdate and entity.riddenByEntity) then
        if (not entity.riddenByEntity:IsDead() and entity.riddenByEntity.ridingEntity == entity) then
            self:UpdateEntity(entity.riddenByEntity);
        else
            entity.riddenByEntity.ridingEntity = nil;
            entity.riddenByEntity = nil;
        end
    end
end


-- Returns a list of bounding boxes that collide with aabb including the passed in entity's collision. 
-- @param aabb: 
-- return array list of bounding box (all bounding box is read-only), modifications will lead to unexpected result. 
function World:GetCollidingBoundingBoxes(aabb, entity)
	return PhysicsWorld:GetCollidingBoundingBoxes(aabb, entity);
end

function World:RemoveEntity(entity)
	entity:Destroy();
end

-- Do NOT use this method to remove normal entities- use normal RemoveEntity
function World:RemovePlayerEntityDangerously(entity)
	entity:Destroy();
end

function World:GetBlockEntityList(from_x,from_y,from_z, to_x, to_y, to_z)
	return BlockEngine:GetBlockEntityList(from_x,from_y,from_z, to_x, to_y, to_z);
end

-- this is a faster way to interate all entities in the chunk. please note that it may contain non-block entities. 
function World:GetEntityListInChunk(chunkX, chunkZ)
	return EntityManager.GetEntitiesInChunkColumn(chunkX, chunkZ);
end


-- @param granularity: (0-1), 1 will generate 27 pieces, 0 will generate 0 pieces, default to 1. 
-- @param cx, cy, cz: center of break point. 
function World:CreateBlockPieces(block_template, blockX, blockY, blockZ, granularity, texture_filename, cx, cy, cz, color)
	if(block_template) then
		block_template:CreateBlockPieces(blockX, blockY, blockZ, granularity, texture_filename, cx, cy, cz, color);
	end
end

-- this function is called when chunk is loaded or unloaded for the first time. 
-- @param bLoad: true to create, false to unload
function World:DoPreChunk(chunkX, chunkZ, bLoad)
	-- TODO:
	if(bLoad) then
        self:GetChunkProvider():LoadChunk(chunkX, chunkZ);
    else
        self:GetChunkProvider():UnloadChunk(chunkX, chunkZ);
    end
end

-- this function is called before we apply new chunk data over existing chunks
function World:InvalidateBlockReceiveRegion(from_x,from_y,from_z, to_x, to_y, to_z)
	-- TODO: we need to call OnBlockRemoved for all blocks with entities, such as BlockSign, etc. 
	-- see also Chunk:FillChunk()
end


```