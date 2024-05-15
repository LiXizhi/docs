```lua

--[[
Title: Attention base class
Author(s): LiXizhi
Date: 2017/6/3
Desc: attention is a meta object in the vision context. It is not the object itself, 
but contains a snapshot of recent events of a single object. 
This class is the base class for all kinds of concepts that can have attention in the vision. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/AttentionBase.lua");
local AttentionBase = commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBase");
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Core/ToolBase.lua");
local AttentionBase = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBase"));
AttentionBase:Property("Name", "AttentionBase");

-- how much attention this object has in the vision context. 
-- the higher the more attention the object get. This value also decays when no memory clip matches it in recent vision context
AttentionBase:Property({"power", 0});
-- maximum power that an object can get. 
AttentionBase:Property({"max_power", 100});
-- power value to add when activated
AttentionBase:Property({"activation_power", 7});

function AttentionBase:ctor()
end

function AttentionBase:HasAttention()
	return self.power >= 0;
end

function AttentionBase:Activate()
	self:AddPower(self.activation_power);
end


function AttentionBase:AddPower(power)
	self.power = math.min(self.max_power, self.power + power);
end

function AttentionBase:SetPower(power)
	self.power = math.min(self.max_power, power);
end

-- grayscale-to-red-green-blue-color 
-- This produces to the "cold-to-hot" color ramp.
-- @param v: any value v in range vmin, vmax.
-- @param vmin, vmax:  range of v
-- return r,g,b in 0,1 ranges
function AttentionBase:ConvertFloatToColor(v, vmin, vmax)
	local r, g, b = 1.0, 1.0, 1.0; -- white
	local dv;
	if(v < vmin) then
		v = vmin;
	end
	if(v > vmax) then
		v = vmax;
	end
	dv = vmax - vmin;

	if(v <(vmin + 0.25 * dv)) then
		r = 0;
		g = 4*(v - vmin) / dv;
	elseif(v <(vmin + 0.5 * dv))then
		r = 0;
		b = 1 + 4*(vmin + 0.25 * dv - v) / dv;
	elseif(v <(vmin + 0.75 * dv)) then
		r = 4*(v - vmin - 0.5 * dv) / dv;
		b = 0;
	else
		g = 1 + 4*(vmin + 0.75 * dv - v) / dv;
		b = 0;
	end
	return r, g, b;
end

-- @return DWORD of RGB
function AttentionBase:GetPowerColor()
	local r, g, b = self:ConvertFloatToColor(self.power, 0, self.max_power);
	return math.floor(r * 0xff0000 + g * 0xff00 + b + 0xff000000);
end


-- virtual function
function AttentionBase:Draw(painter, visionContext)
end

--[[
Title: Attention Block
Author(s): LiXizhi
Date: 2017/6/3
Desc: A single block that caught our attention in the vision context. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/AttentionBlock.lua");
local AttentionBlock = commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBlock");
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Scene/Overlays/ShapesDrawer.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/AttentionBase.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/PatternBlockEdge.lua");
local PatternBlockEdge = commonlib.gettable("MyCompany.Aries.Game.Memory.PatternBlockEdge");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local ShapesDrawer = commonlib.gettable("System.Scene.Overlays.ShapesDrawer");
local AttentionBlock = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBlock"));
AttentionBlock:Property("Name", "AttentionBlock");
AttentionBlock:Property({"render_size", 0.2});

function AttentionBlock:ctor()
	-- self.edges = {}
	-- self.view_direction
end

function AttentionBlock:init(bx, by, bz)
	self.bx, self.by, self.bz = bx, by, bz;
	return self;
end

-- quick longest distance to 
function AttentionBlock:DistanceTo(x, y, z)
	return math.max(self.bx-x, self.by-y, self.bz-z);
end


-- virtual function
function AttentionBlock:Draw(painter, visionContext)
	local rx, ry, rz = visionContext:GetRenderOrigin();
	local x, y, z = self.bx-rx, self.by-ry, self.bz-rz;
	painter:SetBrush(self:GetPowerColor());
	ShapesDrawer.DrawCube(painter, x * BlockEngine.blocksize, y * BlockEngine.blocksize, z * BlockEngine.blocksize, self.render_size)

	if(self.edges) then
		for _, edge in ipairs(self.edges) do
			if(edge == PatternBlockEdge.face_bottom) then
				
			end
		end
	end
end

--[[
Title: Memory Actor
Author(s): LiXizhi
Date: 2017/6/2
Desc: Actor is the base class for a tightly related group of time-series-based concept(entity) in memory.
A memory clip may contain one or more memory actors. Actor is like an abstract concept in the brain that never separates.

When an actor is activated, it will play-back the time-series into the virtual world inside the brain by incarnation. 

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActor.lua");
local MemoryActor = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActor");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/TimeSeries.lua");
local TimeSeries = commonlib.gettable("MyCompany.Aries.Game.Common.TimeSeries");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local Actor = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActor"));
Actor:Property("Name", "MemoryActor");
-- the itemstack(TimeSeries) is changed
Actor:Signal("dataSourceChanged");
-- frame move interval in milliseconds
Actor:Property({"frameMoveInterval", 30, "GetFrameMoveInterval", "SetFrameMoveInterval", auto=true});
Actor:Property({"time", 0, "GetTime", "SetTime", auto=true});
Actor:Property({"lastTime", nil, "GetLastTime",});
Actor:Property({"active", false, "IsActive", "SetActive"});
Actor:Property({"offset_facing", 0, "GetOffsetFacing", "SetOffsetFacing", auto=true});

function Actor:ctor()
	self.TimeSeries = TimeSeries:new{name = "Actor",};
end

-- @param itemStack: movie block actor's item stack where time series data source of this entity is stored. 
-- @param entity: the world entity that this actor is controlling, such as EntityPlayer, EntityNPC, EntityModel, etc. 
function Actor:Init(itemStack, entity)
	self:SetEntity(entity);
	self:SetItemStack(itemStack);
	return self;
end

-- get the last time of all time series of this actor. 
-- this is calculated on demand on first call and cached the result. 
function Actor:GetLastTime()
	if(not self.lastTime) then
		self.lastTime = self:GetTimeSeries():GetLastTime()
	end
	return self.lastTime;
end

function Actor:SetItemStack(itemStack)
	self.lastTime = nil;
	self.itemStack = itemStack;
	self:BindItemStackToTimeSeries();
end

function Actor:GetItemStack()
	return self.itemStack;
end

function Actor:GetTimeSeries()
	return self.TimeSeries;
end

function Actor:BindItemStackToTimeSeries()
	-- needs to clear all multi variable, otherwise undo function will not work properly. 
	self.custom_vars = {};
	local timeseries = self.itemStack:GetDataField("timeseries");
	if(not timeseries) then
		timeseries = {};
		self.itemStack:SetDataField("timeseries", timeseries);
	end
	self.TimeSeries:LoadFromTable(timeseries);
	self:dataSourceChanged();
	self:SetModified();
end

function Actor:SetModified()
	-- self:valueChanged();
	-- self:keyChanged();
end

-- the world entity that this actor is controlling
function Actor:GetEntity()
	return self.entity;
end

-- the world entity that this actor is controlling
function Actor:SetEntity(entity)
	self.entity = entity;
end

-- @return the entity position if any
function Actor:GetPosition()
	if(self.entity) then
		return self.entity:GetPosition();
	end
end

function Actor:GetVariable(keyname)
	return self.TimeSeries:GetVariable(keyname);
end

-- @param keypath: keyname or key local path. such as "x", "bones::root" 
function Actor:GetChildVariableByPath(keypath)
	if(keypath) then
		local subkey;
		keypath, subkey = keypath:match("^([^:]+):*(.*)"); 
		local var = self.TimeSeries:GetChild(keypath);
		if(var) then
			if(subkey and subkey~="" and var.GetChild) then
				return var:GetChild(subkey);
			end
		end
	end
	return;
end

-- @param bStartFromFirstKeyFrame: whether we will only value after the time of first key frame. default to false.
function Actor:GetValue(keyname, time, bStartFromFirstKeyFrame)
	local v = self:GetVariable(keyname);
	if(v and time) then
		if(not bStartFromFirstKeyFrame) then
			-- default to animId = 1
			return v:getValue(1, time);
		else
			local firstTime = v:GetFirstTime();
			if(firstTime and firstTime <= time) then
				return v:getValue(1, time);
			end
		end
	end
end

-- from data source coordinate to entity coordinate according to CalculateRelativeParams()
function Actor:TransformToEntityPosition(x, y, z)
	x = x + (self.offset_x or 0);
	y = y + (self.offset_y or 0);
	z = z + (self.offset_z or 0);
	
	if(self.offset_facing ~= 0) then
		local dx, _, dz = math3d.vec3Rotate(x - self.origin_x, 0, z - self.origin_z, 0, self.offset_facing, 0);
		x = dx + self.origin_x;
		z = dz + self.origin_z;
	end
	return x,y,z;
end

-- from data source coordinate to entity coordinate according to CalculateRelativeParams()
function Actor:TransformToEntityFacing(facing)
	return facing and (facing + (self.offset_facing or 0));
end

-- return the animation instance. 
function Actor:GetAnimInstance()
	local entity = self:GetEntity();
	if(entity) then
		local obj = entity:GetInnerObject();
		if(obj) then
			local animInstance = obj:GetAttributeObject():GetChildAt(1,1);
			if(animInstance and animInstance:IsValid()) then
				return animInstance;
			end
		end
	end
end


function Actor:IsActive()
	return self.active;
end

function Actor:SetActive(bActive)
	self.active = bActive;
end

-- virtual function: 
function Actor:Activate()
	self:SetActive(true);
	self:SetTime(0);
end

-- virtual function: 
function Actor:Deactivate()
	self:SetActive(false);
end

-- start calling FrameMove() function
function Actor:BeginFrameMove()
	self.mytimer = self.mytimer or commonlib.Timer:new({callbackFunc = function(timer)
		self:FrameMove(timer:GetDelta());
	end})
	self.mytimer:Change(10, self:GetFrameMoveInterval());
end

-- end calling FrameMove() function, usually called when actor is deactivated. 
function Actor:EndFrameMove()
	if(self.mytimer) then
		self.mytimer:Change();
	end
end

-- virtual function: called every framemove. 
-- @param deltaTime: in millisecond ticks
function Actor:FrameMove(deltaTime)
end

--[[
Title: Memory Actor Block Model 
Author(s): LiXizhi
Date: 2017/6/11
Desc: Actor Entities that is usually a static block model. 
block model does not move outside of a block, but it can be animated with bones. 

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActorBlockModel.lua");
local MemoryActorBlockModel = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorBlockModel");
local actor = MemoryActorBlockModel:new():Init(itemStack, entity);
actor:Activate();
actor:Deactivate();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/BonesVariable.lua");
local math3d = commonlib.gettable("mathlib.math3d");
local BonesVariable = commonlib.gettable("MyCompany.Aries.Game.Movie.BonesVariable");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")


local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActor"), commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorBlockModel"));
Actor:Property("Name", "MemoryActorBlockModel");
-- whether to retain last bone pose after memory clip is finished. 
Actor:Property({"isRetainPose", true, "IsRetainPose", "SetRetainPose", auto=true});

function Actor:ctor()
end

-- called when enter block world. 
function Actor:Init(itemStack, entity)
	-- base class must be called last, so that child actors have created their own variables on itemStack. 
	if(not Actor._super.Init(self, itemStack, entity)) then
		return;
	end
	local timeseries = self.TimeSeries;
	timeseries:CreateVariableIfNotExist("facing", "LinearAngle");
	timeseries:CreateVariableIfNotExist("scaling", "Linear");
	self:CheckLoadBonesAnims();
	return self;
end

function Actor:GetBonesVariable()
	if(not self.bones_variable) then
		self.bones_variable = BonesVariable:new():init(self);
	end
	return self.bones_variable;
end

-- load bone animations if not loaded before, this function does nothing if no bones are in the time series. 
function Actor:CheckLoadBonesAnims()
	if(not self.bones_variable) then
		local bones = self:GetTimeSeries():GetChild("bones");
		if(bones) then
			self:GetBonesVariable();
		end
	end
end

-- make sure that the low level C++ attributes contains the latest value.
function Actor:UpdateAnimInstance()
	if(self:GetTime() ~= self.lastPlayTime) then
		self:FrameMovePlaying(0);
	end
	local bones = self:GetBonesVariable();
	if(bones) then
		bones:UpdateAnimInstance();
	end
end


-- advance the animation by deltaTime;
function Actor:FrameMovePlaying(deltaTime)
	local curTime = self:GetTime();
	self.lastPlayTime = curTime;
	curTime = curTime + (deltaTime or 0);
	if(self:GetLastTime() < curTime and self.lastPlayTime < self:GetLastTime()) then
		-- ensure the last frame is always played
		curTime = self:GetLastTime();
	end
	self:SetTime(curTime);
	local entity = self:GetEntity();
	if(not entity or not curTime or self:GetLastTime() < curTime) then
		self:Deactivate();
		return		
	end

	local obj = entity:GetInnerObject();

	local yaw,scaling;
	yaw = self:TransformToEntityFacing(self:GetValue("facing", curTime));
	scaling = self:GetValue("scaling", curTime);

	if(obj) then
		-- in case of explicit animation
		obj:SetField("Time", curTime); 
		obj:SetField("EnableAnim", false);
		obj:SetField("yaw", yaw or 0);
		obj:SetScale(scaling or 1);
	end
end

-- apply time series to entity 
function Actor:LoadBoneAnimationsToEntity()
	local boneVars = self:GetBonesVariable();
	if(boneVars) then
		boneVars:LoadFromActor();
		return true;
	end
end

function Actor:Activate()
	self:SetActive(true);
	self:SetTime(0);
	self:LoadBoneAnimationsToEntity();
	self:FrameMovePlaying(0);
	self:BeginFrameMove();
end

-- when deactivated we will release the control to human player with this function.
function Actor:ReleaseEntityControl()
	if(self:IsRetainPose()) then
		-- Do not release animation, but retaining the last bone pose in the memory clip.
	else
		local entity = self:GetEntity();
		if(entity) then
			local obj = entity:GetInnerObject();
			if(obj) then
				obj:SetField("EnableAnim", true);
			end
		end

		if(self.bones_variable) then
			self.bones_variable:UnbindAnimInstance();
		end
	end
end

-- deactivate and release entity animation control. 
function Actor:Deactivate()
	self:SetActive(false);
	self:EndFrameMove();
	self:ReleaseEntityControl();
end

function Actor:FrameMove(deltaTime)
	self:FrameMovePlaying(deltaTime);
end


--[[
Title: Memory Actor NPC
Author(s): LiXizhi
Date: 2017/6/2
Desc: Actor Entities that is NOT the current player. 

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActorNPC.lua");
local MemoryActorNPC = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorNPC");
local actor = MemoryActorNPC:new():Init(itemStack, entity);
actor:Activate();
actor:Deactivate();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/BonesVariable.lua");
local math3d = commonlib.gettable("mathlib.math3d");
local BonesVariable = commonlib.gettable("MyCompany.Aries.Game.Movie.BonesVariable");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local PlayerAssetFile = commonlib.gettable("MyCompany.Aries.Game.EntityManager.PlayerAssetFile")


local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActor"), commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorNPC"));
Actor:Property("Name", "MemoryActorNPC");
-- ignore any skin parameter set in the movie block. 
Actor:Property({"IgnoreSkin", true, "IsIgnoreSkin", "SetIgnoreSkin", auto=true,});

function Actor:ctor()
end

-- called when enter block world. 
function Actor:Init(itemStack, entity)
	-- base class must be called last, so that child actors have created their own variables on itemStack. 
	if(not Actor._super.Init(self, itemStack, entity)) then
		return;
	end
	local timeseries = self.TimeSeries;
	timeseries:CreateVariableIfNotExist("x", "Linear");
	timeseries:CreateVariableIfNotExist("y", "Linear");
	timeseries:CreateVariableIfNotExist("z", "Linear");
	timeseries:CreateVariableIfNotExist("facing", "LinearAngle");
	timeseries:CreateVariableIfNotExist("pitch", "LinearAngle");
	timeseries:CreateVariableIfNotExist("roll", "LinearAngle");
	timeseries:CreateVariableIfNotExist("HeadUpdownAngle", "Linear");
	timeseries:CreateVariableIfNotExist("HeadTurningAngle", "Linear");
	timeseries:CreateVariableIfNotExist("anim", "Discrete");
	timeseries:CreateVariableIfNotExist("assetfile", "Discrete");
	timeseries:CreateVariableIfNotExist("speedscale", "Discrete");
	timeseries:CreateVariableIfNotExist("scaling", "Linear");
	timeseries:CreateVariableIfNotExist("skin", "Discrete");
	timeseries:CreateVariableIfNotExist("blockinhand", "Discrete");

	self:CheckLoadBonesAnims();
	return self;
end

function Actor:GetBonesVariable()
	if(not self.bones_variable) then
		self.bones_variable = BonesVariable:new():init(self);
	end
	return self.bones_variable;
end

-- load bone animations if not loaded before, this function does nothing if no bones are in the time series. 
function Actor:CheckLoadBonesAnims()
	if(not self.bones_variable) then
		local bones = self:GetTimeSeries():GetChild("bones");
		if(bones) then
			self:GetBonesVariable();
		end
	end
end

-- make sure that the low level C++ attributes contains the latest value.
function Actor:UpdateAnimInstance()
	if(self:GetTime() ~= self.lastPlayTime) then
		local bIsUserControlled = self:IsUserControlled();
		self:FrameMovePlaying(0);
		if(bIsUserControlled) then
			self:SetControllable(bIsUserControlled);
		end
	end
	local bones = self:GetBonesVariable();
	if(bones) then
		bones:UpdateAnimInstance();
	end
end


-- advance the animation by deltaTime;
function Actor:FrameMovePlaying(deltaTime)
	local curTime = self:GetTime();
	self.lastPlayTime = curTime;
	curTime = curTime + (deltaTime or 0);
	if(self:GetLastTime() < curTime and self.lastPlayTime < self:GetLastTime()) then
		-- ensure the last frame is always played
		curTime = self:GetLastTime();
	end
	self:SetTime(curTime);
	local entity = self:GetEntity();
	if(not entity or not curTime or self:GetLastTime() < curTime) then
		self:Deactivate();
		return		
	end

	local obj = entity:GetInnerObject();
	local new_x = self:GetValue("x", curTime);
	local new_y = self:GetValue("y", curTime);
	local new_z = self:GetValue("z", curTime);
	new_x, new_y, new_z = self:TransformToEntityPosition(new_x, new_y, new_z);
	entity:SetPosition(new_x, new_y, new_z);

	local HeadUpdownAngle, HeadTurningAngle, anim, yaw, roll, pitch, skin, speedscale, scaling, gravity, opacity, blockinhand, assetfile;
	HeadUpdownAngle = self:GetValue("HeadUpdownAngle", curTime);
	HeadTurningAngle = self:GetValue("HeadTurningAngle", curTime);
	anim = self:GetValue("anim", curTime);
	yaw = self:TransformToEntityFacing(self:GetValue("facing", curTime));
	roll = self:GetValue("roll", curTime);
	pitch = self:GetValue("pitch", curTime);
	skin = self:GetValue("skin", curTime);
	speedscale = self:GetValue("speedscale", curTime);
	scaling = self:GetValue("scaling", curTime);
	gravity = self:GetValue("gravity", curTime);
	opacity = self:GetValue("opacity", curTime);
	assetfile = self:GetValue("assetfile", curTime);
	blockinhand = self:GetValue("blockinhand", curTime);

	if(obj) then
		-- in case of explicit animation
		obj:SetField("Time", curTime); 
		obj:SetField("IsControlledExternally", true);
		entity:SetCheckCollision(false);
		obj:SetField("EnableAnim", false);

		obj:SetField("yaw", yaw or 0);
		obj:SetField("roll", roll or 0);
		obj:SetField("pitch", pitch or 0);
		
		local bNeedRefreshModel;
		if(entity:SetMainAssetPath(PlayerAssetFile:GetFilenameByName(assetfile))) then
			bNeedRefreshModel = true;
		end
		
		if(skin and not self:IsIgnoreSkin()) then
			entity:SetSkin(skin);
		end
		entity:SetBlockInRightHand(blockinhand);

		if(bNeedRefreshModel) then
			entity:RefreshClientModel();
		end
		
		if(anim) then
			if(anim~=obj:GetField("AnimID", 0)) then
				obj:SetField("AnimID", anim);
			end
			local var = self:GetVariable("anim");
			if(var) then
				-- get the time when model assetfile just takes effect. 
				local start_time = 0;
				local varAssetFile = self:GetVariable("assetfile");
				if(varAssetFile and varAssetFile:GetKeyNum()>1) then
					start_time = varAssetFile:getStartTime(1, curTime);
					if(varAssetFile:GetFirstTime() == start_time) then
						start_time = 0;
					end
				end
				-- get the time, when the animation is first started
				local fromTime = var:getStartTime(1, curTime);
				local localTime = curTime;
				if(var:GetFirstTime() == fromTime) then
					-- force looping from first frame
					fromTime = start_time;
				elseif(fromTime < start_time) then
					-- in case the asset model is changed, the start time is relative to the asset model. 
					fromTime = start_time;
				end

				localTime = curTime - fromTime;
				-- calculate speedscale? 
				local varSpeed = self:GetVariable("speedscale");
				if(varSpeed and varSpeed:GetKeyNum()>1) then
					local fromTimeSpeed, toTimeSpeed = varSpeed:getTimeRange(1, fromTime);
					if(toTimeSpeed >= curTime) then
						localTime = localTime * (speedscale or 1);
					else
						-- we need more calculations, here:  localtime = Sigma_sum{delta_time*speedscale(time)}
						local totalScaledTime = 0;
						local calculatedTime = fromTime;
						local lastTime, lastValue;
						for time, v in varSpeed:GetKeys_Iter(1, fromTimeSpeed-1, curTime) do
							local dt = time - calculatedTime;
							if(dt > 0) then
								totalScaledTime = totalScaledTime + dt * (lastValue or v);
								calculatedTime = time;
							end
							lastTime = time;
							lastValue = v;
						end
						if(curTime > calculatedTime) then
							totalScaledTime = totalScaledTime + (curTime - calculatedTime) * speedscale;
						end
						localTime = totalScaledTime;
					end
				else
					localTime = localTime * (speedscale or 1);
				end
				obj:SetField("AnimFrame", localTime);
				local default_blending_time = 250;
				if( localTime < default_blending_time and 
					-- if this the first animation, set it without using a blending factor. 
					fromTime ~= 0) then
					obj:SetField("BlendingFactor", 1 - localTime / default_blending_time);
				else
					-- this is actually already set in obj:SetField("AnimFrame", localTime); so no need to set again. 
					-- obj:SetField("BlendingFactor", 0);
				end
			end
		end
		obj:SetField("HeadUpdownAngle", HeadUpdownAngle or 0);
		obj:SetField("HeadTurningAngle", HeadTurningAngle or 0);
		
		entity:SetSpeedScale(speedscale or 1);
		obj:SetField("Speed Scale", speedscale or 1);
		obj:SetScale(scaling or 1);
	end
end

-- apply time series to entity 
function Actor:LoadBoneAnimationsToEntity()
	local boneVars = self:GetBonesVariable();
	if(boneVars) then
		boneVars:LoadFromActor();
		return true;
	end
end

-- from data source coordinate to entity coordinate according to CalculateRelativeParams()
function Actor:TransformToEntityPosition(x, y, z)
	x = x + (self.offset_x or 0);
	y = y + (self.offset_y or 0);
	z = z + (self.offset_z or 0);
	
	if(self.offset_facing ~= 0) then
		local dx, _, dz = math3d.vec3Rotate(x - self.origin_x, 0, z - self.origin_z, 0, self.offset_facing, 0);
		x = dx + self.origin_x;
		z = dz + self.origin_z;
	end
	return x,y,z;
end

-- from data source coordinate to entity coordinate according to CalculateRelativeParams()
function Actor:TransformToEntityFacing(facing)
	return facing + (self.offset_facing or 0);
end

-- calculate relative params at time 0 according to the current entity's parameters
-- so that all time series values are relative to time 0, instead of absolute values in data source. 
-- currently, only entity position and facing are taking in to account and snapped to block position and 4 direction. 
-- calculated values in self.offset_x, self.offset_y, self.offset_z, self.offset_facing
function Actor:CalculateRelativeParams()
	local entity = self:GetEntity();
	if(entity) then
		local obj = entity:GetInnerObject();
		if(not obj) then
			return
		end	
		-- relative position
		local entity_bx, entity_by, entity_bz = entity:GetBlockPos();
		local entity_x, entity_y, entity_z = entity:GetPosition();
		local entity_facing = entity:GetFacing() or 0;
		
		local memory_x, memory_y, memory_z = self:GetValue("x", 0), self:GetValue("y", 0), self:GetValue("z", 0);
		local memory_bx, memory_by, memory_bz = BlockEngine:block(memory_x, memory_y+0.1, memory_z);
		local memory_facing = self:GetValue("facing", 0) or 0;
		
		self.offset_x = (entity_bx - memory_bx)*BlockEngine.blocksize;
		self.offset_y = (entity_by - memory_by)*BlockEngine.blocksize;
		self.offset_z = (entity_bz - memory_bz)*BlockEngine.blocksize;
		self.origin_x, self.origin_y, self.origin_z = BlockEngine:real(entity_bx, entity_by, entity_bz);

		-- relative facing
		local memory_dir_facing = Direction.NormalizeFacing(memory_facing)
		local entity_dir_facing = Direction.NormalizeFacing(entity_facing)
		self.offset_facing = mathlib.ToStandardAngle(entity_dir_facing - memory_dir_facing);

		-- echo({self.offset_x, self.offset_y, self.offset_z, self.offset_facing})
	end
end

function Actor:Activate()
	self:SetActive(true);
	self:SetTime(0);
	self:CalculateRelativeParams();
	self:LoadBoneAnimationsToEntity();
	self:FrameMovePlaying(0);
	self:BeginFrameMove();
end

-- when deactivated we will release the control to human player with this function.
function Actor:ReleaseEntityControl()
	local entity = self:GetEntity();
	if(entity) then
		
		local obj = entity:GetInnerObject();
		if(obj) then
			obj:SetField("IsControlledExternally", false);
			entity:SetCheckCollision(true);
			obj:SetField("EnableAnim", true);
		end
	end

	if(self.bones_variable) then
		self.bones_variable:UnbindAnimInstance();
	end
end

-- deactivate and release entity animation control. 
function Actor:Deactivate()
	self:SetActive(false);
	self:EndFrameMove();
	self:ReleaseEntityControl();
end


function Actor:FrameMove(deltaTime)
	self:FrameMovePlaying(deltaTime);
end

--[[
Title: Memory Clip
Author(s): LiXizhi
Date: 2017/6/2
Desc: It represents a long term memory with multiple actors over a short time period, usually less than 2 seconds. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryClip.lua");
local MemoryClip = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryClip");
local clip = MemoryClip:new():Init(context)
clip:SetMovieBlockEntity(movieClipEntity);
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActor.lua");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local PlayerAssetFile = commonlib.gettable("MyCompany.Aries.Game.EntityManager.PlayerAssetFile")

local MemoryClip = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryClip"));
MemoryClip:Property("Name", "MemoryClip");
MemoryClip:Property({"time", 0, "GetTime", "SetTime", auto=true});

function MemoryClip:ctor()
end

-- @param context: memory context that this memory clip belongs to
function MemoryClip:Init(context)
	self.context = context;
	return self;
end

function MemoryClip:GetContext()
	return self.context;
end

-- set the movie block entity as the time series data source. 
-- please note movieClipEntity is readonly and may be shared by mutiple memory context.
-- @param movieClipEntity: EntityMovieClip
function MemoryClip:SetMovieBlockEntity(movieClipEntity)
	self.movieEntity = movieClipEntity;
end

function MemoryClip:CalculateDeviation(context)
	context = context or self:GetContext();
end

-- get initial value of a given variable in timeSeries
local function GetValueAtTime0(timeSeries, name)
	local ts = timeSeries[name];
	if(ts and ts.data) then
		return ts.data[1];
	end
end

-- get the time series itemStack that matches the given player entity
-- We will return a match if the size, skin and asset in time 0 all matched. 
function MemoryClip:FindActorByStartFrame(playerContext)
	if(not playerContext) then
		return 
	end
	local inventory = self:GetActorInventory()
	local actorStack;
	local score = 0;
	for i=1, inventory:GetSlotCount() do
		local itemStack = inventory:GetItem(i);
		if(itemStack and itemStack.count > 0 and itemStack.serverdata) then
			if(itemStack.id == block_types.names.TimeSeriesNPC) then
				local timeSeries = itemStack.serverdata.timeseries;
				local v = GetValueAtTime0(timeSeries, "assetfile");
				if(v and PlayerAssetFile:GetFilenameByName(v) == playerContext.assetfile) then
					-- asset file must always match
					local candidate_score = 1;
					v = GetValueAtTime0(timeSeries, "skin");
					if(v and v == playerContext.skin) then
						candidate_score = candidate_score + 1;
					end
					v = GetValueAtTime0(timeSeries, "scaling");
					if(v and v == playerContext.scaling) then
						candidate_score = candidate_score + 1;
					end
					if(candidate_score > score) then
						score = candidate_score;
						actorStack = itemStack;
					end
				end
			end
		end
	end
	return actorStack;
end

function MemoryClip:GetActorInventory()
	if(self.movieEntity) then
		return self.movieEntity.inventory;
	end
end

function MemoryClip:TransformStartTime()
	local actorStack = self:FindActorByStartFrame();
end

function MemoryClip:Activate(context)
	context = context or self:GetContext();
	context:AddToWorkingMemory(self);
	local playerContext = context:GetPlayerContext();
	local inventory = self:GetActorInventory()
	if(not context or not inventory or not playerContext) then
		return;
	end

	-- check if there is player entity
	local playerStack = self:FindActorByStartFrame(playerContext);
	local playerActor;
	if(playerStack) then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActorNPC.lua");
		local MemoryActorNPC = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorNPC");
		playerActor = MemoryActorNPC:new():Init(playerStack, playerContext:GetEntity());
		if(playerActor) then
			playerActor:Activate();
		end
	end

	-- check other entities
	if(playerActor) then
		for i=1, inventory:GetSlotCount() do
			local itemStack = inventory:GetItem(i);
			if(itemStack and itemStack~=playerStack and itemStack.count > 0 and itemStack.serverdata) then
				if(itemStack.id == block_types.names.TimeSeriesNPC) then
					local timeSeries = itemStack.serverdata.timeseries;
				
					local v = GetValueAtTime0(timeSeries, "assetfile");
					if(v and v:match("bmax$")) then
						-- this is an block max model, it could be a Block Model.	
						local x, y, z = GetValueAtTime0(timeSeries, "x"), GetValueAtTime0(timeSeries, "y"), GetValueAtTime0(timeSeries, "z");
						x, y, z = playerActor:TransformToEntityPosition(x, y, z)
						local bx, by, bz = BlockEngine:block(x, y+0.1, z);
						local entity = EntityManager.GetBlockEntity(bx, by, bz);
						if(entity and entity.class_name == "EntityBlockModel") then
							-- asset file also match
							if(entity:GetModelFile() == v) then
								NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryActorBlockModel.lua");
								local MemoryActorBlockModel = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryActorBlockModel");
								local actor = MemoryActorBlockModel:new():Init(itemStack, entity);
								if(actor) then
									actor:SetOffsetFacing(playerActor:GetOffsetFacing())
									actor:Activate();
								end
							end
						end
					end
				elseif(itemStack.id == block_types.names.TimeSeriesCamera) then

				elseif(itemStack.id == block_types.names.TimeSeriesCommands) then
				
				end
			end
		end
	end
end

function MemoryClip:AddToWorkingMemory()
	self:GetContext():AddToWorkingMemory(self);
end

-- called every framemove. 
-- @param deltaTime: in millisecond ticks
function MemoryClip:FrameMove(deltaTime)
end


--[[
Title: Memory Context
Author(s): LiXizhi
Date: 2017/5/19
Desc: Memory context of a given player entity. This is like the AI brain of the player entity. 
Memory is stored in memory clips which is a form of distributed data representation. 
Memory clips can be played in parallel but always in one direction.
EmotionContext is used to control the replay threshold of memory clips. Without emotion, working memory tends
to disappear until new input arrives. Emotion is the driving power when there is not much external inputs. 

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryContext.lua");
local MemoryContext = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryContext");
local context = MemoryContext:new():Init();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/PlayerContext.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/MemoryClip.lua");
local MemoryClip = commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryClip");
local PlayerContext = commonlib.gettable("MyCompany.Aries.Game.Memory.PlayerContext");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local MemoryContext = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.MemoryContext"));
MemoryContext:Property("Name", "MemoryContext");
-- show/hide memory vision in 3d scene mostly for debugging purposes
MemoryContext:Property({"visible", false, "IsVisible", "SetVisible"});

MemoryContext:Signal("activeMemoryClipChanged", function(clip) end);

function MemoryContext:ctor()
	-- clips that is being played
	self.active_clips = commonlib.UnorderedArraySet:new();
	-- working memory is memory that has just been played back into the virtual world
	-- it is sentient and ready to elicit other long term memory to become new memory. 
	self.working_memory = commonlib.UnorderedArraySet:new();
	-- mapping from 3d position key to all long term memory clips
	self.longterm_memory = {};
end

-- called when enter block world. 
function MemoryContext:Init(playerEntity)
	GameLogic:Connect("WorldUnloaded", self, self.Reset, "UniqueConnection")
	if(playerEntity) then
		self:SetPlayer(playerEntity);
	end
	return self;
end

function MemoryContext:GetPosIndex(bX, bY, bZ)
	return BlockEngine:GetSparseIndex(bX, bY, bZ);
end

-- add a memory clip to working memory set. 
function MemoryContext:AddToWorkingMemory(memoryClip)
	if(self.working_memory:contains(memoryClip)) then
		self.working_memory:removeByValue(memoryClip)
	end
	-- this ensures that the memory is at the last 
	self.working_memory:push_back(memoryClip);
end

-- add memory clip to long term memory
function MemoryContext:AddMemoryClip(bX, bY, bZ, memoryClip)
	self.longterm_memory[self:GetPosIndex(bX, bY, bZ)] = memoryClip;
end

function MemoryContext:CreateMemoryClip()
	return MemoryClip:new():Init(self);
end

-- get memory clip from long term memory
function MemoryContext:GetMemoryClip(bX, bY, bZ)
	local nIndex = self:GetPosIndex(bX, bY, bZ);
	return self.longterm_memory[nIndex];
end

function MemoryContext:Reset()
	self.active_clips:clear();
	self.working_memory:clear();
	self.longterm_memory = {};
	GameLogic:Disconnect("WorldUnloaded", self, self.Reset)
end

-- if there are active memory clips that is being played back into the working memory. work 
function MemoryContext:HasAttention()
	return not self.active_clips:empty();
end

-- set the host player entity that this memory manager belongs to 
function MemoryContext:SetPlayer(player_entity)
	self.player = player_entity;
end

-- get the host player
function MemoryContext:GetPlayer()
	return self.player;
end

-- update context from 3d scene into this context
function MemoryContext:UpdateContext()
	-- update player
	self:UpdatePlayerContext();
	-- update vision according to player position
	self:GetVisionContext():Update(self:GetPlayerContext());
	self:GetVisionContext():SetVisible(self:IsVisible());
end

function MemoryContext:UpdatePlayerContext()
	local ctx = self.playerContext;
	if(not ctx) then
		ctx = PlayerContext:new();
		self.playerContext = ctx;
	end
	ctx:Update(self:GetPlayer());
	return ctx;
end

function MemoryContext:GetPlayerContext()
	if(not self.playerContext) then
		self:UpdatePlayerContext();
	end
	return self.playerContext;
end

function MemoryContext:GetVisionContext()
	if(not self.visionContext) then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/VisionContext.lua");
		local VisionContext = commonlib.gettable("MyCompany.Aries.Game.Memory.VisionContext");
		self.visionContext = VisionContext:new();
	end
	return self.visionContext;
end

-- only used for debugging to repeat the last working memory clip
function MemoryContext:ActivateRecentWorkingMemoryClip()
	local lastMemoryClip = self.working_memory:last();
	if(lastMemoryClip) then
		lastMemoryClip:Activate(self);
	end
end

-- show/hide debug draw
function MemoryContext:SetVisible(bVisible)
	self.visible = bVisible;
end

-- show/hide debug draw
function MemoryContext:IsVisible(bVisible)
	return self.visible;
end

-- called every framemove by the containing entity. 
-- @param deltaTime: in millisecond ticks
-- @return true if the entity is controlled by memory context
function MemoryContext:FrameMove(deltaTime)
	self:UpdateContext();
end

--[[
Title: Pattern generator for blocks
Author(s): LiXizhi
Date: 2017/12/25
Desc: generate patterns from a given set of attention blocks and a viewpoint and direction.
because attention blocks are mostly static, we will also save edge information into attention blocks.
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/PatternGenBlocks.lua");
local PatternGenBlocks = commonlib.gettable("MyCompany.Aries.Game.Memory.PatternGenBlocks");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/Pattern.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Direction.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/PatternBlockEdge.lua");
local PatternBlockEdge = commonlib.gettable("MyCompany.Aries.Game.Memory.PatternBlockEdge");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local Pattern = commonlib.gettable("MyCompany.Aries.Game.Memory.Pattern");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine");

local PatternGenBlocks = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.PatternGenBlocks"));
PatternGenBlocks:Property("Name", "PatternGenBlocks");

-- how many patterns to generate for per block. 
PatternGenBlocks:Property({"compression_rate", 0.1});
-- max block range from current eye position to get pattern recognition attention.
PatternGenBlocks:Property({"maxRadius", 10});

function PatternGenBlocks:ctor()
end


local function GetOffsetBySideAndView(view_direction, side1, side2)
	if(not side2) then
		return Direction.GetOffsetBySideAndView(side1, view_direction);
	else
		local dx, dy, dz = Direction.GetOffsetBySideAndView(side1, view_direction);
		local dx2, dy2, dz2 = Direction.GetOffsetBySideAndView(side2, view_direction);
		return dx+dx2, dy+dy2, dz+dz2;
	end
end

local neighborBlocks = {};

local function ComputeBlockEdge(block, blocks, view_direction)
	if(block.view_direction == view_direction and block.edges) then
		return;
	elseif(block.view_direction ~= view_direction and block.edges) then
		table.clear(block.edges);
	end
	block.edges = block.edges or {};
	local edges = block.edges;
	
	local dx, dy, dz;
	local x,y,z = block.bx, block.by, block.bz;
	for side = 0, 5 do
		local dx, dy, dz = GetOffsetBySideAndView(view_direction, side);
		neighborBlocks[side] = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
	end
	local edge;
	if(not neighborBlocks[5]) then
		edges[#edges+1] = PatternBlockEdge.face_top;

		if(not neighborBlocks[0]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_top_left;
		elseif(not neighborBlocks[1]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_top_right;
		elseif(not neighborBlocks[2]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_top_front;
		elseif(not neighborBlocks[3]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_top_back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 0, 5);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_top_right;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 1, 5);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_top_left;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 2, 5);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_top_back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 3, 5);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_top_front;
		end
	end
	if(not neighborBlocks[4]) then
		edges[#edges+1] = PatternBlockEdge.face_bottom;
		if(not neighborBlocks[0]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_bottom_left;
		elseif(not neighborBlocks[1]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_bottom__right;
		elseif(not neighborBlocks[2]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_bottom__front;
		elseif(not neighborBlocks[3]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_bottom__back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 0, 4);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_bottom_right;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 1, 4);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_bottom_left;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 2, 4);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_bottom_back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 3, 4);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_bottom_front;
		end
	end
	if(not neighborBlocks[0]) then
		if(not neighborBlocks[2]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_left_front;
		elseif(not neighborBlocks[3]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_left_back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 0, 3);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_left_front;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 0, 2);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_left_back;
		end
	end
	if(not neighborBlocks[1]) then
		if(not neighborBlocks[2]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_right_front;
		elseif(not neighborBlocks[3]) then
			edges[#edges+1] = PatternBlockEdge.edge_out_right_back;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 1, 3);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_right_front;
		end

		dx, dy, dz = GetOffsetBySideAndView(view_direction, 1, 2);
		block = blocks[BlockEngine:GetSparseIndex(x+dx, y+dy, z+dz)];
		if(block) then
			edges[#edges+1] = PatternBlockEdge.edge_in_right_back;
		end
	end
end

-- generate raw pattern near the given viewpoint. 
-- @param blocks: attentioned blocks map
-- @param view_direction: 0 is x:-1 	1 is x:+1 	2 is z:-1	3 is z:+1
-- @param cx,cy,cz: current view position, this could be the player or eye position. 
-- @param maxRadius: max block range from current eye position to get pattern recognition attention. default to 10. 
function PatternGenBlocks:Generate(blocks, cx,cy,cz, view_direction, maxRadius)
	local index = BlockEngine:GetSparseIndex(cx,cy,cz)
	
	maxRadius = maxRadius or self.maxRadius;
	local radiusSq = maxRadius * maxRadius;

	for index, block in pairs(blocks) do
		local x,y,z = block.bx, block.by, block.bz;
		-- ignore the negative half space of view direction.
		if( (view_direction == 0 and (x-cx) <= 0) or (view_direction == 1 and (x-cx) >= 0) or 
			(view_direction == 2 and (z-cz) <= 0) or (view_direction == 3 and (z-cz) >= 0)) then
			-- make sure we are only processing a small region around the current view(eye or player) pos.
			local distSq = (x-cx)^2 + (y-cy)^2 + (z-cz)^2;
			if(  distSq < radiusSq ) then
				ComputeBlockEdge(block, blocks, view_direction);
			end
		end
	end
end


-- generate all edges to the attention blocks
function PatternGenBlocks:GenerateEdges(blocks)
end

--[[
Title: Vision Context
Author(s): LiXizhi
Date: 2017/6/3
Desc: 
The vision context contains: blocks(including physical blocks) and NPC entities.
Each object in the vision context has an attention value, the more memory matches the more attention object gets.
But attention value of objects also decays fast and only last a few frames if no matched. 
Each object is also linked with matching memory clips. 

The following things will affect block attention in decreasing order:
- the player position and facing: block faces and edges close to the player viewpoint has greater attention.
- Eye attention: any activated movie clip that has recently applied to the vision context get the eye attention. Eye attention will usually last 1 or 2 seconds
- Block pattern recognition: block patterns that has more valid matches to memory movie clips get higher attention. 
- Entity pattern: Some block with bmax, or scene entities may have more attentions that others in the vision context. 
- Blocks near the mouse cursor usually have more attention, but it is not menditoray. 

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/VisionContext.lua");
local VisionContext = commonlib.gettable("MyCompany.Aries.Game.Memory.VisionContext");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Direction.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/AttentionBlock.lua");
local AttentionBlock = commonlib.gettable("MyCompany.Aries.Game.Memory.AttentionBlock");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local VisionContext = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Memory.VisionContext"));
VisionContext:Property("Name", "VisionContext");
-- default view distance is 10 blocks
VisionContext:Property({"ViewDist", 10, auto=true});
-- value to decrease attention when the object is out of view distance. 
VisionContext:Property({"InvisibleDecay", 10});
-- object decay
VisionContext:Property({"NaturalDecay", 2});
-- color to use to draw attention
VisionContext:Property({"color", "#0000ff"});
-- whether to debug draw
VisionContext:Property({"visible", false, "IsVisible", "SetVisible"});

function VisionContext:ctor()
	self.frameCount = 0;
	-- attentioned objects 
	self.attention_blocks = {};
	self.attention_entites = {};

	NPL.load("(gl)script/apps/Aries/Creator/Game/Memory/PatternGenBlocks.lua");
	local PatternGenBlocks = commonlib.gettable("MyCompany.Aries.Game.Memory.PatternGenBlocks");
	self.pattern_genBlocks = PatternGenBlocks:new();
end

-- this should be called every frame to decay attention values. 
-- @param playerContext: update from a player Context ( this is actually only used to read player position). If nil, we will use current player's block position.
function VisionContext:Update(playerContext)
	self.frameCount = self.frameCount + 1;
	
	playerContext = playerContext or EntityManager.GetPlayer();
	local eye_x, eye_y, eye_z = playerContext:GetBlockPos();
	local facing = playerContext:GetFacing();
	local lookat_dir = Direction.GetDirectionFromFacing(facing);
	local viewDist = self:GetViewDist();

	if(self:IsVisible()) then
		-- update render origin of overlay if it is visible.
		self:SetRenderOrigin(eye_x, eye_y, eye_z);
		local x, y, z = BlockEngine:real(eye_x, eye_y, eye_z)
		self.overlay:SetPosition(x, y, z);
	end

	-- update the attention weight by eye position. 
	self:DecreaseOutOfViewPower(eye_x, eye_y, eye_z, viewDist)
	self:AddPowerToVisibleObject(eye_x, eye_y, eye_z, lookat_dir, viewDist)
	self:CleanUnusedAttentionBlocks();

	self.pattern_genBlocks:Generate(self.attention_blocks, eye_x, eye_y, eye_z, lookat_dir, viewDist-2);
end

function VisionContext:DecreaseOutOfViewPower(eye_x, eye_y, eye_z, viewDist)
	for index, obj in pairs(self.attention_blocks) do
		
		if(obj:DistanceTo(eye_x, eye_y, eye_z) > viewDist) then
			obj:AddPower(-self.InvisibleDecay);
		else
			obj:AddPower(-self.NaturalDecay);
		end
	end
end

-- get the attention block
function VisionContext:CreateGetAttentionBlock(x,y,z)
	local index = BlockEngine:GetSparseIndex(x,y,z)
	local attentionBlock = self.attention_blocks[index];
	if(not attentionBlock) then
		attentionBlock = AttentionBlock:new():init(x,y,z);
		self.attention_blocks[index] = attentionBlock;
	end
	return attentionBlock;
end

function VisionContext:AddPowerToVisibleObject(eye_x, eye_y, eye_z, lookat_dir, viewDist)
	local radius = 3;
	for dx = -radius, radius do
		for dz = -radius, radius do
			local x = eye_x + dx
			local z = eye_z + dz
			local block_id, y = BlockEngine:GetNextBlockOfTypeInColumn(x,eye_y,z, 0xffffff, radius)
			if(block_id) then
				local attentionBlock = self:CreateGetAttentionBlock(x,y,z);
				if(attentionBlock) then
					attentionBlock:Activate();
				end
			end
		end
	end
end

-- remove unused attentions if any
function VisionContext:CleanUnusedAttentionBlocks()
	local removed;
	for index, obj in pairs(self.attention_blocks) do
		if(not obj:HasAttention()) then
			removed = removed or {};
			removed[#removed+1] = index;
		end
	end
	if(removed) then
		for _, index in ipairs(removed) do
			self.attention_blocks[index] = nil;
		end
	end
end

-- show/hide debug draw
function VisionContext:SetVisible(bVisible)
	if(bVisible and not self.overlay) then
		NPL.load("(gl)script/ide/System/Scene/Overlays/Overlay.lua");
		local Overlay = commonlib.gettable("System.Scene.Overlays.Overlay");
		self.overlay = Overlay:new():init();
		
		self.overlay.paintEvent = function(overlay, painter)
			self:Draw(painter);
		end

	elseif(not bVisible and self.overlay) then
		self.overlay:Destroy()
		self.overlay = nil;
	end
end

-- show/hide debug draw
function VisionContext:IsVisible()
	return self.overlay ~= nil;
end


function VisionContext:WorldToLocalBlockPos()
	
end

-- in block coordinate
function VisionContext:SetRenderOrigin(bx, by, bz)
	self.renderOriginX, self.renderOriginY, self.renderOriginZ = bx, by, bz;
end

-- in block coordinate
function VisionContext:GetRenderOrigin()
	return self.renderOriginX, self.renderOriginY, self.renderOriginZ;
end

-- draw vision mostly for debugging purposes
function VisionContext:Draw(painter)
	
	painter:SetBrush(self.color);
	for index, obj in pairs(self.attention_blocks) do
		if(obj:HasAttention()) then
			obj:Draw(painter, self);
		end
	end
end


--[[
Title: a container of multiple animblock
Author(s): LiXizhi
Date: 2014/8/7
Desc: It has the same interface of AnimBlock, except that it is a container or multiple variables.
mapping from key to values{value1, value2, ...}

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/MultiAnimBlock.lua");
local MultiAnimBlock = commonlib.gettable("MyCompany.Aries.Game.Common.MultiAnimBlock");
local anims = MultiAnimBlock:new();
anims:AddMultiAnimBlock(anim)
-------------------------------------------------------
]]
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");


local MultiAnimBlock = commonlib.inherit(nil, commonlib.gettable("MyCompany.Aries.Game.Common.MultiAnimBlock"));

function MultiAnimBlock:ctor()
	self.variables = commonlib.OrderedArraySet:new();
end

function MultiAnimBlock:GetChild()
end

-- @param anim: the AnimBlock instance. 
function MultiAnimBlock:AddVariable(variable)
	self.variables:add(variable);
end

function MultiAnimBlock:GetVariable(nIndex)
	return self.variables[nIndex];
end

-- variable is returned as an array of individual variable value at the given time. 
function MultiAnimBlock:getValue(anim, time)
	local o = {};
	for i=1, #(self.variables) do
		o[i] = self.variables[i]:getValue(anim, time);
	end
	return o;
end

function MultiAnimBlock:AddKey(time, data)
	local res;
	for i=1, #(self.variables) do
		res = self.variables[i]:AddKey(time, data[i]) or res;
	end
	return res;
end

function  MultiAnimBlock:GetLastTime()
	local max_last_time = 0;
	for i=1, #(self.variables) do
		local last_time = self.variables[i]:GetLastTime();
		if(last_time and max_last_time < last_time) then
			max_last_time = last_time;
		end 
	end
	return max_last_time;
end

function MultiAnimBlock:MoveKeyFrame(key_time, from_keytime)
	for i=1, #(self.variables) do
		self.variables[i]:MoveKeyFrame(key_time, from_keytime);
	end
end

function MultiAnimBlock:CopyKeyFrame(key_time, from_keytime)
	for i=1, #(self.variables) do
		self.variables[i]:CopyKeyFrame(key_time, from_keytime);
	end
end

-- Update or insert (Upsert) a key frame at given time.
-- @param data: data is cloned before updating. 
function MultiAnimBlock:UpsertKeyFrame(key_time, data)
	for i=1, #(self.variables) do
		if(data[i]) then
			self.variables[i]:UpsertKeyFrame(key_time, data[i]);
		end
	end
end

function MultiAnimBlock:RemoveKeyFrame(key_time)
	for i=1, #(self.variables) do
		self.variables[i]:RemoveKeyFrame(key_time);
	end
end

function MultiAnimBlock:ShiftKeyFrame(shift_begin_time, offset_time)
	for i=1, #(self.variables) do
		self.variables[i]:ShiftKeyFrame(shift_begin_time, offset_time);
	end
end

function MultiAnimBlock:RemoveKeysInTimeRange(fromTime, toTime)
	for i=1, #(self.variables) do
		self.variables[i]:RemoveKeysInTimeRange(fromTime, toTime);
	end
end

-- paste all key frames between [fromTime, toTime] to time
function MultiAnimBlock:PasteKeyFramesInRange(time, fromTime, toTime)
	for i=1, #(self.variables) do
		self.variables[i]:PasteKeyFramesInRange(time, fromTime, toTime)
	end
end

function MultiAnimBlock:TrimEnd(time)
	for i=1, #(self.variables) do
		self.variables[i]:TrimEnd(time);
	end
end

-- iterator that returns, all (time, values) pairs between (TimeFrom, TimeTo].  
-- the iterator works fine when there are identical time keys in the animation, like times={0,1,1,2,2,2,3,4}.  for time keys in range (0,2], 1,1,2,2,2, are returned. 
function  MultiAnimBlock:GetKeys_Iter(anim, TimeFrom, TimeTo)
	local iters = {};
	for i=1, #(self.variables) do
		iters[i] = self.variables[i]:GetKeys_Iter(anim, TimeFrom, TimeTo);
	end
	local times = {};
	local values = {};
	local last_values = {};

	return function ()
		local count = #(self.variables);
		local min_time, min_index;
		for i=1, count do
			local iter = iters[i]
			if(iter) then
				local time = times[i];
				if(not time) then
					time, value = iter();
					if(time == nil) then
						iters[i] = nil;
						times[i] = nil;
						values[i] = nil;
					else
						times[i] = time;
						values[i] = value;
					end
				end
				if(time and (not min_time or time<min_time)) then
					min_time = time;
					min_index = i;
				end
			end
		end
		if(min_time) then
			for i=1, count do
				local time = times[i];
				if(time == min_time) then
					times[i] = nil;
					last_values[i] = values[i];
				end
			end
			return min_time, last_values;
		end
	end
end

--[[
Title: A single anim block
Author(s): LiXizhi
Date: 2007/11/10
Use Lib:
-------------------------------------------------------
NPL.load("(gl)script/ide/TimeSeries/AnimBlock.lua");

local ctl = AnimBlock:new{
	name = "AnimBlock1",
	type = "Linear", "Discrete", or "Hermite"
};
ctl:getValue2(1, 400);
-------------------------------------------------------
]]

NPL.load("(gl)script/ide/commonlib.lua");
NPL.load("(gl)script/ide/mathlib.lua");
local mathlib = commonlib.gettable("mathlib");

if(not AnimBlock) then AnimBlock = {}; end

local type = type;
AnimBlock.tableType = "AnimBlock";
-- "Linear "or "Hermite" or "Discrete" or "LinearAngle"
AnimBlock.type = "Linear";
AnimBlock.used = true;

function AnimBlock:new(o)
	o = o or {};
	setmetatable(o, self);
	self.__index = self;
	
	---------------------------
	-- data keeping and init
	---------------------------
	-- "linear "or "Hermite" or "Discrete"

	o.ranges = o.ranges or {};
	o.times = o.times or {};
	o.data = o.data or {};
	return o;
end


function AnimBlock:Reset()
	self.ranges = {};
	self.times = {};
	self.data = {};
end

-- if all animated values equals to the key, this animation will be set unused
function AnimBlock:SetConstantKey(key)
	if(self.data) then
		local nSize = #(self.data);
		local i;
		for i = 1, nSize do
			if(self.data[i] ~= key) then
				return;
			end
		end
		self.used = false;
	end
end

-- if all animated values are very close to a given key, this animation will be set unused
function AnimBlock:SetConstantKey(key, fEpsilon)
	if(self.data) then
		local nSize = #(self.data);
		local i;
		for i = 1, nSize do
			if(commonlib.Absolute(self.data[i] - key) > fEpsilon) then
				return;
			end
		end
		self.used = false;
	end
end

-- default value
function AnimBlock:getDefaultValue()
	return self.data[1];
end

-- get value with motion blending with a specified blending frame.
-- @param nCurrentAnim: current animation sequence ID
-- @param currentFrame: an absolute ParaX frame number denoting the current animation frame. It is always within
--		the range of the current animation sequence's start and end frame number.
-- @param nBlendingAnim: the animation sequence with which the current animation should be blended.
-- @param blendingFrame: an absolute ParaX frame number denoting the blending animation frame. It is always within
--		the range of the blending animation sequence's start and end frame number.
-- @param blendingFactor: by how much the blending frame should be blended with the current frame. 
--		1.0 will use solely the blending frame, whereas 0.0 will use only the current frame.
--		[0,1), blendingFrame*(blendingFactor)+(1-blendingFactor)*currentFrame
function AnimBlock:getValue5(nCurrentAnim, currentFrame, nBlendingAnim, blendingFrame, blendingFactor)
	if(blendingFactor == 0) then
		return self:getValue2(nCurrentAnim, currentFrame);
	elseif(blendingFactor == 1) then
		return self:getValue2(nBlendingAnim, blendingFrame);
	else
		local v1 = self:getValue2(nCurrentAnim, currentFrame);
		local v2 = self:getValue2(nBlendingAnim, blendingFrame);
		
		return self:InterpolateLinear(blendingFactor, v1, v2);
	end
end

-- it accept anim index of both local and external animation
-- rangeID: Index.nIndex
-- time: Index.nCurrentFrame
function AnimBlock:getValue1(Index)
	return self:getValue2(Index.nIndex, Index.nCurrentFrame);
end

-- it accept anim index of both local and external animation
-- rangeID: CurrentAnim.nIndex, BlendingAnim.nIndex
-- time: CurrentAnim.nCurrentFrame, BlendingAnim.nCurrentFrame
function AnimBlock:getValue3(CurrentAnim, BlendingAnim, blendingFactor)
	
	if(blendingFactor == 0) then
		return self:getValue1(CurrentAnim);
	elseif(blendingFactor == 1) then
		return self:getValue1(BlendingAnim);
	else
		local v1 = self:getValue1(CurrentAnim);
		local v2 = self:getValue1(BlendingAnim);

		return self:InterpolateLinear(blendingFactor, v1, v2);
	end
end

-- iterator that returns, all (time, value) pairs between (TimeFrom, TimeTo].  
-- the iterator works fine when there are identical time keys in the animation, like times={0,1,1,2,2,2,3,4}.  for time keys in range (0,2], 1,1,2,2,2, are returned. 
function  AnimBlock:GetKeys_Iter(anim, TimeFrom, TimeTo)
	local i = self:GetNextKeyIndex(anim, TimeFrom);
	--log(tostring(i).." from "..TimeFrom.." to "..TimeTo.."\n")
	return function ()
		if(i~=nil) then
			local time = self.times[i];
			if(time==nil) then
				return
			end
			-- tricky: this skipped equal or smaller key since GetNextKeyIndex() returns the first equal or smaller ones
			while(time<=TimeFrom) do
				i=i+1;
				time = self.times[i];
				if(time==nil) then
					return
				end
			end
			--log(tostring(i).." "..time.."\n")
			if(time>TimeFrom and time<=TimeTo) then
				i = i + 1
				return time, self.data[i-1];
			end	
		end
	end
end

-- private: return the index of the first key whose time is larger than or equal to time. 
-- function may return nil if no suitable index is found. 
function  AnimBlock:GetNextKeyIndex(anim, time)
	local rangesCount = #(self.ranges);
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	if(self.type ~= "NONE" and dataCount > 1) then
		
		local range;

		-- obtain a time value and a data range, and get the range according to the current animation.
		if(anim > 0 and anim <= rangesCount) then
			range = self.ranges[anim];
		else
			return;
		end
		
		if(range[1] ~= range[2]) then
			local pos = range[1]; -- this can be 0.
			
			local nStart = range[1];
			local nEnd = range[2];
			
			if(time > self.times[nEnd]) then
				return nEnd;
			end
			
			while(true) do
				if(nStart >= nEnd) then
					-- if no item left.
					pos = nStart;
					break;
				end
				
				local nMid;
				if( ((nStart + nEnd)%2) == 1 ) then
					nMid = (nStart + nEnd - 1)/2;
				else
					nMid = (nStart + nEnd)/2;
				end
				
				local startP = (self.times[nMid]);
				local endP = (self.times[nMid + 1]);

				if(startP <= time and time < endP ) then
					-- if (middle item is target)
					pos = nMid;
					break;
				elseif(time < startP ) then
					-- if (target < middle item)
					nEnd = nMid;
				elseif(time >= endP) then
					-- if (target >= middle item)
					nStart = nMid+1;
				end
			end -- while(nStart<=nEnd)
			
			for i=pos-1, range[1], -1 do
				if(self.times[i]>=time) then
					pos = i;
				else
					break;
				end
			end
			return pos;
		else
			if(self.times[range[1]]>=time) then
				return range[1];
			end	
		end
		
	else
		-- default value
		if(self.times[1]~=nil and self.times[1]>=time) then
			return 1;
		end	
	end
end

-- get the first key time containing the time, 
-- @Note duplicated values are merged.  for example, if key1 and key2 both have the same value, their start time is merged key1's time is returned. 
function AnimBlock:getStartTime(anim, time)
	local index = self:GetNextKeyIndex(anim, time);
	if(index) then
		local start_time = self.times[index] or 0;
		if(start_time > time) then
			if(index > 1) then
				index = index - 1;
			end
		end
		local value = self.data[index]
		for i = index-1, 1, -1 do
			if(self.data[i] == value) then
				index = i;
			else
				break;
			end
		end
		return self.times[index] or 0;
	else
		return 0;
	end
end

-- return the key time range that best contains input time. 
-- @return timeFrom, timeTo: so that timeFrom<=time<=timeTo, and that there are key frames at the two ends. 
function AnimBlock:getTimeRange(anim, time)
	local rangesCount = #(self.ranges);
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	if(self.type ~= "NONE" and dataCount > 1) then
		local range;

		-- obtain a time value and a data range, and get the range according to the current animation.
		if(anim > 0 and anim <= rangesCount) then
			range = self.ranges[anim];
		else
			-- default value
			return 0, time;
		end
		
		if(range[1] ~= range[2]) then
			local pos = range[1]; -- this can be 0.
			
			local nStart = range[1];
			local nEnd = range[2];
			
			if(time >= self.times[nEnd]) then
				return self.times[nEnd], time;
			elseif(time <= self.times[nStart]) then --modified 2007.11.13
				return time, self.times[nStart];
			end
			
			while(true) do
			
				if(nStart >= nEnd) then
					-- if no item left.
					pos = nStart;
					break;
				end
				
				local nMid;
				if( ((nStart + nEnd)%2) == 1 ) then
					nMid = (nStart + nEnd - 1)/2;
				else
					nMid = (nStart + nEnd)/2;
				end
				
				local startP = (self.times[nMid]);
				local endP = (self.times[nMid + 1]);

				if(startP <= time and time < endP ) then
					-- if (middle item is target)
					pos = nMid;
					break;
				elseif(time < startP ) then
					-- if (target < middle item)
					nEnd = nMid;
				elseif(time >= endP) then
					-- if (target >= middle item)
					nStart = nMid+1;
				end
			end -- while(nStart<=nEnd)
			
			local t1 = self.times[pos];
			local t2 = self.times[pos + 1];
			
			return t1, t2;
		else
			return 0, time;
		end
		
	else
		if(dataCount == 1) then
			local keyframe = self.times[1];
			if(keyframe) then
				return keyframe, keyframe;
			else
				-- default value
				return 0, time;
			end
		else
			-- default value
			return 0, time;
		end
	end
end
	
-- this function will return the interpolated animation vector at the specified anim id and frame number
-- anim: RangeID
-- time: frame number,  1 milsec = 1 frame
function AnimBlock:getValue2(anim, time)
	local rangesCount = #(self.ranges);
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	if(self.type ~= "NONE" and dataCount > 1) then
		
		local range;

		-- obtain a time value and a data range, and get the range according to the current animation.
		if(anim > 0 and anim <= rangesCount) then
			range = self.ranges[anim];
		else
			-- default value
			return self.data[1];
		end
		
		if(range[1] ~= range[2]) then
			local pos = range[1]; -- this can be 0.
			
			local nStart = range[1];
			local nEnd = range[2];
			
			if(time >= self.times[nEnd]) then
				return self.data[nEnd];
			elseif(time <= self.times[nStart]) then --modified 2007.11.13
				return self.data[nStart];
			end
			
			while(true) do
			
				if(nStart >= nEnd) then
					-- if no item left.
					pos = nStart;
					break;
				end
				
				local nMid;
				if( ((nStart + nEnd)%2) == 1 ) then
					nMid = (nStart + nEnd - 1)/2;
				else
					nMid = (nStart + nEnd)/2;
				end
				
				local startP = (self.times[nMid]);
				local endP = (self.times[nMid + 1]);

				if(startP <= time and time < endP ) then
					-- if (middle item is target)
					pos = nMid;
					break;
				elseif(time < startP ) then
					-- if (target < middle item)
					nEnd = nMid;
				elseif(time >= endP) then
					-- if (target >= middle item)
					nStart = nMid+1;
				end
			end -- while(nStart<=nEnd)
			
			
			local t1 = self.times[pos];
			local t2 = self.times[pos + 1];
			
			local r = (time-t1)/(t2-t1);

			local vType = self.type;
			if (vType == "Linear") then
				-- interpolate linear
				return self:InterpolateLinear(r, self.data[pos], self.data[pos+1]);
			elseif (vType == "Discrete") then
				-- the first one is used. 
				return self.data[pos];	
			elseif (vType == "LinearAngle") then
				-- angle values -pi, pi
				return self:InterpolateLinearAngle(r, self.data[pos], self.data[pos+1]);
			elseif (vType == "LinearTable") then
				return self:InterpolateLinearTable(r, self.data[pos], self.data[pos+1]);
			elseif (vType == "Hermite") then
				-- HERMITE
				log("error: Caution inVal and outVal table are empty right now\r\n");
				return self:InterpolateHermite(r, self.data[pos], self.data[pos+1], self.inVal[pos], self.outVal[pos]);
			end
		else
			return self.data[range[1]];
		end
		
	else
		-- default value
		return self.data[1];
	end
end

AnimBlock.getValue = AnimBlock.getValue2;

-- linear interpolation
function AnimBlock:InterpolateLinear(range, v1, v2)
	return  (v1 * (1.0 - range) + v2 * range);
end

-- linear interpolation
function AnimBlock:InterpolateLinearAngle(range, v1, v2)
	local delta = mathlib.ToStandardAngle(v2-v1);
	return mathlib.ToStandardAngle(v1 + delta * range);
end

-- linear interpolation between two tables recursively. For string subfield, we will use value from fromT, 
-- for number sub fields, we will use linear interpolation, or if the key name begins with "rot", we will use linear angle for its child data field.
function AnimBlock:InterpolateLinearTable(range, fromT, toT, isAngleData)
	if(type(fromT) == "table" and type(toT) == "table") then
		local thisT = {};
		
		for name, value in pairs(toT) do
			if(fromT[name] == nil) then
				thisT[name] = value;
			end
		end

		for name, value in pairs(fromT) do
			local dataType = type(value);
			if(dataType == "number") then
				if(not isAngleData) then
					thisT[name] = self:InterpolateLinear(range, value, toT[name] or value);
				else
					thisT[name] = self:InterpolateLinearAngle(range, value, toT[name] or value);
				end
			elseif(dataType == "table") then
				local isAngleData = name:match("^rot")~=nil;
				thisT[name] = self:InterpolateLinearTable(range, value, toT[name] or value, isAngleData)
			else
				thisT[name] = value;
			end
		end

		return thisT;
	end
	return fromT or toT;
end

-- blend the two values use linear interpolation
function AnimBlock:BlendValues(currentValue, blendingValue, blendingFactor)
	if(blendingFactor == 0) then
		return currentValue;
	elseif(blendingFactor == 1) then
		return blendingValue;
	else
		return self:InterpolateLinear(blendingFactor, currentValue, blendingValue);
	end
end

-- hermite interpolation
function AnimBlock:InterpolateHermite(range, v1, v2, inVal, outVal)

	local h1 = 2.0*range*range*range - 3.0*range*range + 1.0;
	local h2 = -2.0*range*range*range + 3.0*range*range;
	local h3 = range*range*range - 2.0*range*range + range;
	local h4 = range*range*range - range*range;
	
	return (v1*h1 + v2*h2 + inVal*h3 + outVal*h4);
end

function AnimBlock:SetRangeByIndex(index, rangeFirst, rangeSecond)
	if(not self.ranges[index]) then
		self.ranges[index] = {};
	end
	self.ranges[index] = {rangeFirst, rangeSecond};
end

-- trim end, so that there are no time value that is smaller than time.
-- currently, it will automatically update animation range for 1 
function AnimBlock:TrimEnd(time)
	local timesCount = #(self.times);
	
	if(timesCount == 1) then
		if(self.times[timesCount]>time) then
			commonlib.resize(self.times, 0);
			commonlib.resize(self.data, 0);
			self.ranges[1] = {};
		end
	elseif(timesCount>1) then	
		if(self.times[timesCount]>time) then
			local i;
			for i=timesCount, 1, -1 do 
				if(self.times[i]<=time) then
					commonlib.resize(self.times, i);
					commonlib.resize(self.data, i);
					self:SetRangeByIndex(1, 1, i);
					return
				end
			end
			commonlib.resize(self.times, 0);
			commonlib.resize(self.data, 0);
			self.ranges[1] = {};
		end	
	end
end

-- append a key intelligently without introducing keys, it will automatically update the range if necessary.
-- currently it only works for range 0. 
-- if type is Linear, it will create a new key only if the last key, the last last key and the new key are all the same. 
-- if type is Discrete, it will always create a new key. 
-- @param time: if time is smaller than the last time, previous time, value will be removed. 
-- @param bForceAppend: always append no matter what. 
-- @return true if appended.
function AnimBlock:AutoAppendKey(time, data, bForceAppend)
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	
	if(not bForceAppend) then
		if(timesCount == 0) then
			self:AppendKey(time, data);
			self:SetRangeByIndex(1, 1, 1);
		elseif(timesCount == 1) then
			if(self.data[dataCount] ~= data) then
				self:AppendKey(time, data);
				self:SetRangeByIndex(1, 1, 2);	
			else
				self.times[timesCount] = time;
				self.data[timesCount] = data;
			end
		else -- if(timesCount >= 2) then	
			if( (self.data[dataCount] == self.data[dataCount-1]) and (self.data[dataCount]==data)) then
				self.times[timesCount] = time;
				self.data[timesCount] = data;
			else
				self:AppendKey(time, data);
				self:SetRangeByIndex(1, 1, timesCount+1);	
			end
		end
	else
		self:AppendKey(time, data);
		self:SetRangeByIndex(1, 1, timesCount+1);	
	end	
	return true;
end

function AnimBlock:AppendKey(time, data)
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	self.times[timesCount + 1] = time;
	self.data[dataCount + 1] = data;
end

-- add a key intelligently, it will automatically update the range if necessary.
-- currently it only works for range 0. 
-- if type is Linear, it will create a new key only if the last key, the last last key and the new key are all the same. 
-- if type is Discrete, it will always create a new key. 
-- @return true if key is modified
function AnimBlock:AutoAddKey(time, data)
	local index = self:GetNextKeyIndex(1, time);
	index = (index or 1);
	local next_time = self.times[index];
	-- local next_data = self.data[index];
	if(next_time) then
		if(next_time == time) then
			if(self.data[index]~=data) then
				self.data[index] = data;
				return true;
			end
		else
			if(next_time < time) then
				index = index + 1;
			end
			if( (index >=3) and (self.data[index-1] == self.data[index-2]) and (self.data[index-1]==data)) then
				-- do nothing, since it is linear
				return;
			else
				-- insert before next_time;
				commonlib.insertArrayItem(self.times, index, time);
				commonlib.insertArrayItem(self.data, index, data);
				self:SetRangeByIndex(1, 1, #(self.times));	
				return true;
			end
		end
	else
		return self:AutoAppendKey(time, data, true);
	end
end

-- add new key at time, data. if there is already a key at the time, we will replace it. 
-- @return true if new key is modified or existing data is modified. 
function AnimBlock:AddKey(time, data)
	local index = self:GetNextKeyIndex(1, time);
	index = (index or 1);
	local next_time = self.times[index];
	if(next_time) then
		if(next_time == time) then
			if(self.data[index]~=data) then
				self.data[index] = data;
				return true;
			end
		else
			if(next_time < time) then
				index = index + 1;
			end
			-- insert before next_time;
			commonlib.insertArrayItem(self.times, index, time);
			commonlib.insertArrayItem(self.data, index, data);
			self:SetRangeByIndex(1, 1, #(self.times));	
			return true;
		end
	else
		return self:AutoAppendKey(time, data, true);
	end
end

-- shifting keyframes from shift_begin_time to end by the amount of offset_time. 
function AnimBlock:ShiftKeyFrame(shift_begin_time, offset_time)
	local begin_index = self:GetNextKeyIndex(1, shift_begin_time) or 1;
	local begin_time = self.times[begin_index];
	if(not begin_time) then
		return
	elseif(begin_time < shift_begin_time) then
		begin_index = begin_index + 1;
		begin_time = self.times[begin_index];
		if(not begin_time) then
			return begin_time;
		end
	end
	if(offset_time < 0) then
		-- check to see if we need to remove some keys first. 
		local to_index = self:GetNextKeyIndex(1, shift_begin_time+offset_time);
		if(to_index) then
			local to_time = self.times[to_index];
			if(not to_time) then
			
			elseif(to_time < (shift_begin_time+offset_time)) then
				to_index = to_index + 1;
			end
		else
			to_index = 1;
		end

		if(to_index < begin_index) then
			for i = to_index, begin_index-1 do
				commonlib.removeArrayItem(self.times, i);
				commonlib.removeArrayItem(self.data, i);
			end
			self:SetRangeByIndex(1, 1, #(self.times));	

			begin_index = to_index;
		end
	end
	-- now offset the time. 
	for i = begin_index, #(self.times) do
		local time = self.times[i] + offset_time;
		self.times[i] = math.max(0, time);
	end
end

-- move keyframe from from_keytime to keytime
function AnimBlock:MoveKeyFrame(key_time, from_keytime)
	local from_index = self:GetNextKeyIndex(1, from_keytime);
	if(from_index) then
		local from_time = self.times[from_index];
		if(from_time == from_keytime) then
			local index = self:GetNextKeyIndex(1, key_time) or 1;
			local time = self.times[index];
			self.times[from_index] = key_time;
			if(index ~= from_index) then
				if(time<key_time and index < #(self.times)) then
					index = index + 1;
				end
				if(index ~= from_index) then
					commonlib.moveArrayItem(self.times, from_index, index);
					commonlib.moveArrayItem(self.data, from_index, index);
				end
			end
			return true;
		end
	end
end

-- move keyframe from from_keytime to keytime
function AnimBlock:CopyKeyFrame(key_time, from_keytime)
	local from_index = self:GetNextKeyIndex(1, from_keytime);
	if(from_index) then
		local from_time = self.times[from_index];
		if(from_time == from_keytime) then
			local index = self:GetNextKeyIndex(1, key_time) or 1;
			local time = self.times[index];
			
			if(time~=key_time and key_time ~= from_keytime) then
				if(time and time<key_time) then
					index = index + 1;
				end
				commonlib.insertArrayItem(self.times, index, key_time);
				commonlib.insertArrayItem(self.data, index, commonlib.clone(self.data[from_index]));
				self:SetRangeByIndex(1, 1, #(self.times));	
			end
			return true;
		end
	end
end

-- Update or insert (Upsert) a key frame at given time.
-- @param data: data is cloned before updating. 
function AnimBlock:UpsertKeyFrame(key_time, data)
	if(key_time and data) then
		local index = self:GetNextKeyIndex(1, key_time) or 1;
		local time = self.times[index];
		if(time~=key_time) then
			-- insert a new one. 
			if(time and time<key_time) then
				index = index + 1;
			end
			commonlib.insertArrayItem(self.times, index, key_time);
			commonlib.insertArrayItem(self.data, index, commonlib.clone(data));
			self:SetRangeByIndex(1, 1, #(self.times));	
		elseif(time) then
			-- update existing one
			self.data[time] = commonlib.clone(data);
		end
		return true;
	end
end

-- remove the key frame at key_time if there is a key frame. 
-- return true if deleted. 
function AnimBlock:RemoveKeyFrame(key_time)
	local index = self:GetNextKeyIndex(1, key_time) or 1;
	local time = self.times[index];
	if(time == key_time) then
		commonlib.removeArrayItem(self.times, index);
		commonlib.removeArrayItem(self.data, index);
		self:SetRangeByIndex(1, 1, #(self.times));	
		return true;
	end
end

-- remove all keys in the [fromTime, toTime]
function AnimBlock:RemoveKeysInTimeRange(fromTime, toTime)
	local from_index = self:GetNextKeyIndex(1, fromTime) or 1;
	local time = self.times[index];
	if(time) then
		if(time == fromTime) then
		elseif(time<fromTime) then
			from_index = from_index + 1;
		end
		local to_index = self:GetNextKeyIndex(1, toTime) or 1;
		time = self.times[index];
		if(not time) then
			-- TODO: not implemented yet
		end
	end
end
-- return the last data in the animation. 
function AnimBlock:GetLastData()
	local dataCount = #(self.data);
	if(dataCount>0) then
		return self.data[dataCount];
	end
end

function AnimBlock:GetLastTime()
	local timesCount = #(self.data);
	if(timesCount>0) then
		return self.times[timesCount];
	end
end

function AnimBlock:GetFirstTime()
	local timesCount = #(self.data);
	if(timesCount>0) then
		return self.times[1];
	end
end

function AnimBlock:UpdateLastKey(time, data)

	local timesCount = #(self.times);
	local dataCount = #(self.data);
	if(timesCount == dataCount) then
		if(timesCount > 0) then
			self.times[timesCount] = time;
			self.data[timesCount] = data;
		else
			self:AppendKey(time, data)
		end
	else
		log("error: Caution times and data table counts are not equal.\r\n");
	end
end

function AnimBlock:SetKeyValueAt(nIndex, time, data)
	self.times[nIndex] = time;
	self.data[nIndex] = data;
end

function AnimBlock:GetKeyNum()
	local timesCount = #(self.times);
	local dataCount = #(self.data);
	if(timesCount == dataCount) then
		return dataCount;
	else
		log("error: Caution times and data table counts are not equal.\r\n");
	end
	return 0;
end

function AnimBlock:SetKeyNum(num)
	num = num or 0;
	commonlib.resize(self.times, num);
	commonlib.resize(self.data, num);
	self:SetRangeByIndex(1, 1, num);
end


function AnimBlock:GetRangeTimeInterval(index)
	if(not self.ranges[index]) then
		return 0;
	end
	--log("timetag1: "..self.ranges[index][2].." timetag2:"..self.ranges[index][1].."\r\n");
	--log("time1: "..self.times[self.ranges[index][2]].." time2:"..self.times[self.ranges[index][1]].."\r\n");
	return self.times[self.ranges[index][2]] - self.times[self.ranges[index][1]];
end

-- append a new pair of (time, value) at the end of a specified animation range (rangeIndex).
-- if there is no range at rangeIndex, a new one will be created. Please note that after calling this, one can no longer append new pairs to previous ranges
-- @param rangeIndex: range index. if nil, it will default to 1. 
-- function AnimBlock:AppendPairInRange(time, value, rangeIndex)
-- end



-- test function:
function AnimBlock:BuildBasicAnimTable()
	local UIAnimFile = {};
	UIAnimFile = {
		["UIAnimation"] = {
			[1] = {
				["ScaleX"] = {
					["ranges"] = {
						[1] = {		1,			2},
						[2] = {					2,			3},
					},
					["times"] = {  [1] = 0,	   [2] = 7,	   [3]= 15,
								 ---|-----------|-----------|-----------|
					},
					["data"] = {   [1] = 0,	   [2] = 1,	   [3]= 0,
								 ---|-----------|-----------|-----------|
					},
				},
				["ScaleY"] = {
					["ranges"] = {
						[1] = {		1,			2},
						[2] = {					2,			3},
					},
					["times"] = {  [1] = 0,	   [2] = 7,	   [3]= 15,
								 ---|-----------|-----------|-----------|
					},
					["data"] = {   [1] = 0,	   [2] = 1,	   [3]= 0,
								 ---|-----------|-----------|-----------|
					},
				},
				["TranslationX"] = {
					["ranges"] = {
						[3] = {		1,			2},
						[4] = {					2,			3},
					},
					["times"] = {  [1] = 0,	   [2] = 7,	   [3]= 15,
								 ---|-----------|-----------|-----------|
					},
					["data"] = {   [1] = 0,	   [2] = 0,    [3]= 0,
								 ---|-----------|-----------|-----------|
					},
				},
				["TranslationY"] = {
					["ranges"] = {
						[3] = {		1,			2},
						[4] = {					2,			3},
					},
					["times"] = {  [1] = 0,	   [2] = 7,	   [3]= 15,
								 ---|-----------|-----------|-----------|
					},
					["data"] = {   [1] = 0,	   [2] = -20,  [3]= 0,
								 ---|-----------|-----------|-----------|
					},
				},
				["Rotation"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
				["RotateOriginX"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
				["RotateOriginY"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
				["Alpha"] = {
					["ranges"] = {
						[1] = {		1,			2},
						[2] = {					2,			3},
					},
					["times"] = {  [1] = 0,	   [2] = 7,	   [3]= 15,
								 ---|-----------|-----------|-----------|
					},
					["data"] = {   [1] = 16,   [2] = 200,  [3]= 16,
								 ---|-----------|-----------|-----------|
					},
				},
				["ColorR"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
				["ColorG"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
				["ColorB"] = {
					["ranges"] = {
					},
					["times"] = {
					},
					["data"] = {
					},
				},
			},
		},
		["UIAnimSeq"] = {
			[1] = {
				["Show"] = {
					[1] = 1,
				},
				["Hide"] = {
					[1] = 2,
				},
				["Up"] = {
					[1] = 3,
				},
				["Down"] = {
					[1] = 4,
				},
			},
		},
	};
	
	NPL.load("(gl)script/ide/commonlib.lua");
	local NewTable = commonlib.LoadTableFromFile("script/UIAnimation/Test_UIAnimFile.lua.table");
end

-- paste all key frames between [fromTime, toTime] to time
function AnimBlock:PasteKeyFramesInRange(pasteAtTime, fromTime, toTime)
	local from_index = self:GetNextKeyIndex(1, fromTime) or 1;
	local time = self.times[from_index];
	if(time and fromTime > time) then
		from_index = from_index + 1;
		time = self.times[from_index];
	end
	if(time and fromTime<=time and time<=toTime) then
		local to_index = self:GetNextKeyIndex(1, toTime) or 1;
		time = self.times[to_index];
		if(time) then
			local times = {}
			local data = {}
			for i = from_index, to_index do
				times[#times+1] = self.times[i]
				data[#data+1] = commonlib.clone(self.data[i])
			end
			
			local pasteAt_index = self:GetNextKeyIndex(1, pasteAtTime) or 1;
			time = self.times[pasteAt_index];
			if(time < pasteAtTime) then
				pasteAt_index = pasteAt_index + 1;
			end
			local pasteEndTime = pasteAtTime + toTime - fromTime;
			local offsetTime = pasteAtTime - fromTime;
			for i = 1, #times do
				time = self.times[pasteAt_index];	
				if(not time or (time<=pasteEndTime)) then
					self.times[pasteAt_index] = times[i] + offsetTime;
					self.data[pasteAt_index] = data[i]
				else
					commonlib.insertArrayItem(self.times, pasteAt_index, times[i] + offsetTime);
					commonlib.insertArrayItem(self.data, pasteAt_index, data[i]);
				end
				pasteAt_index = pasteAt_index + 1;
			end
			self:SetRangeByIndex(1, 1, #(self.times));	
		end
	end
end

--[[
Title: time series is a group of variables
Author(s): LiXizhi
Date: 2014/3/16
Desc: time series can have child time series. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/TimeSeries.lua");
local TimeSeries = commonlib.gettable("MyCompany.Aries.Game.Common.TimeSeries");
local ts = TimeSeries:new();
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/TimeSeries/AnimBlock.lua");
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local AnimBlock = commonlib.gettable("AnimBlock");

local type = type;

local TimeSeries = commonlib.inherit(nil, commonlib.gettable("MyCompany.Aries.Game.Common.TimeSeries"));

function TimeSeries:ctor()
	self.data = {};
	self.key_array = {};
	self.key_index_map = {};
end

-- load time series from a given file or table. It does not clear existing ones in the current time series, but will overwrite if name are the same as in the file. 
-- @param filename: data or the filename
function TimeSeries:LoadFromTable(data)
	if(not data) then
		return;
	end
	self.children = nil;
	self.data = data;
	
	for varName, v in pairs(data) do
		if(type(v) == "table") then
			if(v.isContainer) then
				self.children = self.children or {};
				local child = TimeSeries:new();
				child:LoadFromTable(v);
				self.children[varName] = child;
			else
				self:CreateVariable(v);
			end
		end
	end
end

-- get child timeseries
function TimeSeries:GetChild(name)
	if(self.children) then
		return self.children[name];
	end
end

-- remove a child time series object. 
function TimeSeries:RemoveChild(name)
	local child = self:GetChild(name)
	if(child) then
		self.children[name] = nil;
		self.data[name] = nil;
	end
end

-- create child timeseries
function TimeSeries:CreateChild(name)
	local child = self:GetChild(name);
	if(child) then
		return child;
	end
	self.children = self.children or {};
	local child = TimeSeries:new();
	local data = {isContainer = true, };
	child:LoadFromTable(data);
	self.data[name] = data;
	self.children[name] = child;
	return child;
end

-- save time series to a given file. 
-- @param filename: the filename 
function TimeSeries:GetData()
	return self.data;
end

-- Applies to all variables: trim end, so that there are no time value that is smaller than time.
function TimeSeries:TrimEnd(time)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:TrimEnd(time);
		end	
	end
end

-- shifting keyframes from shift_begin_time to end by the amount of offset_time. 
function TimeSeries:ShiftKeyFrame(shift_begin_time, offset_time)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:ShiftKeyFrame(shift_begin_time, offset_time);
		end	
	end
end

-- remove the key frame at key_time if there is a key frame. 
function TimeSeries:RemoveKeyFrame(keytime)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:RemoveKeyFrame(keytime);
		end	
	end
end

-- copy keyframe from from_keytime to keytime
function TimeSeries:CopyKeyFrame(keytime, from_keytime)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:CopyKeyFrame(keytime, from_keytime);
		end	
	end
end

-- Update or insert (Upsert) a key frame at given time.
-- @param data: data is cloned before updating. 
function TimeSeries:UpsertKeyFrame(key_time, data)
	for k,v in pairs(self.data) do
		v:UpsertKeyFrame(keytime, data);
	end
end

-- move keyframe from from_keytime to keytime
function TimeSeries:MoveKeyFrame(keytime, from_keytime)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:MoveKeyFrame(keytime, from_keytime);
		end	
	end
end

-- remove all keys in the [fromTime, toTime]
function TimeSeries:RemoveKeysInTimeRange(fromTime, toTime)
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.tableType == "AnimBlock") then
			v:RemoveKeysInTimeRange(fromTime, toTime);
		end	
	end
end

-- add a new variable to the time series. It there is an existing variable, the old one will be replaced. 
-- @param params: {name="", type="Linear"|"Discrete"}. It is actually passed to the new function of AnimBlock. More info see AnimBlock. 
function TimeSeries:CreateVariable(params)
	if(params.name == nil) then return end
	self.data[params.name] = AnimBlock:new(params);
	self.key_array[#(self.key_array)+1] = params.name;
	self.key_index_map[params.name] = #(self.key_array);
end

function TimeSeries:CreateVariableIfNotExist(name, type_)
	if(not self.data[name]) then
		self.data[name] = AnimBlock:new({name=name, type=type_});
		self.key_array[#(self.key_array)+1] = name;
		self.key_index_map[name] = #(self.key_array);
	end
	return self.data[name];
end

-- remove variable, the internal key index of child variables after the removed one may be changed
function TimeSeries:RemoveVariable(name)
	local var = self:GetVariable(name)
	if(var) then
		self.data[name] = nil;
		local lastIndex = self.key_index_map[name];
		commonlib.removeArrayItem(self.key_array, lastIndex);
		self.key_index_map[name] = nil;
		for i=lastIndex, #(self.key_array) do
			self.key_index_map[self.key_array[i]] = i;
		end
	end
end

-- get timeseries variable.
function TimeSeries:GetVariable(name)
	if(self.key_index_map[name]) then
		return self.data[name];
	end
end

function TimeSeries:GetVariableCount()
	return #(self.key_array);
end

function TimeSeries:GetVariableName(nIndex)
	return self.key_array[nIndex];
end

function TimeSeries:GetVariableByIndex(nIndex)
	local name = self:GetVariableName(nIndex);
	if(name) then
		return self:GetVariable(name);
	end
end

function TimeSeries:GetVariableIndex(name)
	return self.key_index_map[name];
end

-- @param varName: variable name
-- @param animID: range index
function TimeSeries:GetStartFrame(varName, animID)
	local timesID = self.data[varName].ranges[animID][1];
	return self.data[varName].times[timesID];
end

-- @param varName: variable name
-- @param animID: range index
function TimeSeries:GetEndFrame(varName, animID)
	local timesID = self.data[varName].ranges[animID][2];
	return self.data[varName].times[timesID];
end

-- get the last time in all time series and child time series
function TimeSeries:GetLastTime()
	local lastTime = 0;
	for k,v in pairs(self.data) do
		if(type(v) == "table" and v.GetLastTime) then
			local lastTime_  = v:GetLastTime() or 0;
			if(lastTime_ > lastTime) then
				lastTime = lastTime_;
			end
		end
	end
	if(self.children) then
		for k,v in pairs(self.children) do
			if(type(v) == "table" and v.GetLastTime) then
				local lastTime_  = v:GetLastTime() or 0;
				if(lastTime_ > lastTime) then
					lastTime = lastTime_;
				end
			end
		end
	end
	return lastTime;
end

-- paste all key frames between [fromTime, toTime] to time
function TimeSeries:PasteKeyFramesInRange(time, fromTime, toTime)
	for k,v in pairs(self.data) do
		v:PasteKeyFramesInRange(time, fromTime, toTime);
	end
end

--[[
Title: Direction Helper class
Author(s): LiXizhi
Date: 2012/12/1
Desc: 
	0 is x:-1 	1 is x:+1 	2 is z:-1	3 is z:+1
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Direction.lua");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/math/math3d.lua");
local math3d = commonlib.gettable("mathlib.math3d");

local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction");

-- see also : Direction.GetOffsetBySide
Direction.offsetX = {[0]=-1, 1, 0, 0, 0, 0};
Direction.offsetY = {[0]=0, 0, 0, 0, -1, 1,};
Direction.offsetZ = {[0]=0, 0, -1, 1, 0, 0};

-- mapping to Direction.GetDirection2DFromCamera()'s return value. 
Direction.directions = {[0]="negX", "posX", "negZ", "posZ", };


-- Maps a Direction value (2D) to a Facing value. This is not necessary since direction is same as facing. 
Direction.directionToFacing = { [0]=0, 1, 2, 3};

Direction.directionTo3DFacing = { [0]=0, 3.14, -1.57, 1.57};

-- direction to opposite side(facing)
Direction.directionToOpFacing = { [0]=1, 0, 3, 2, 5, 4};

-- Maps a Facing value (3D) to a Direction value (2D). 
Direction.facingToDirection = { [0]=0, 1, 2, 3, -1,-1};

-- Maps a direction to that opposite of it. */
Direction.rotateOpposite = {[0]=1, 0, 2, 3};

-- Maps a direction to that to the right of it. */
Direction.rotateRight = {[0]=3, 2, 0, 1};

-- Maps a direction to that to the left of it. */
Direction.rotateLeft = {[0]=2, 3, 1, 0};


local facing_to_dir = {
	[0] = 0, [1] = 3, [2] = 1, [3] = 2,
}

function Direction.GetOffsetBySide(side)
	local dx, dy, dz = 0,0,0;
	if(side == 0) then
		dx = -1;
	elseif(side == 1) then
		dx = 1;
	elseif(side == 2) then
		dz = -1;
	elseif(side == 3) then
		dz = 1;
	elseif(side == 4) then
		dy = -1;
	elseif(side == 5) then
		dy = 1;
	end
	return dx, dy, dz;
end

-- @param view_direction: default to 3, which is viewing to positive z axis
function Direction.GetOffsetBySideAndView(side, view_direction)
	local dx, dy, dz = 0,0,0;
	if(side == 0) then
		if(view_direction == 0) then
			dz = -1;
		elseif(view_direction == 1) then
			dz = 1;
		elseif(view_direction == 2) then
			dx = 1;
		else
			dx = -1;	
		end
	elseif(side == 1) then
		if(view_direction == 0) then
			dz = 1;
		elseif(view_direction == 1) then
			dz = -1;
		elseif(view_direction == 2) then
			dx = -1;
		else
			dx = 1;	
		end
	elseif(side == 2) then
		if(view_direction == 0) then
			dx = 1;
		elseif(view_direction == 1) then
			dx = -1;
		elseif(view_direction == 2) then
			dz = 1;
		else
			dz = -1;	
		end
	elseif(side == 3) then
		if(view_direction == 0) then
			dx = -1;
		elseif(view_direction == 1) then
			dx = 1;
		elseif(view_direction == 2) then
			dz = -1;
		else
			dz = 1;	
		end
	elseif(side == 4) then
		dy = -1;
	elseif(side == 5) then
		dy = 1;
	end
	return dx, dy, dz;
end

-- convert from facing to closest direction id. 
-- such that 0 to 0, 3.14 to 1, -1.57 to 2, 1.57 to 3
function Direction.GetDirectionFromFacing(facing)
	if(facing <0) then
		facing = facing + 6.28;
	end
	return facing_to_dir[math.floor(facing/1.57+0.5) % 4];
end

-- nomalize facing to 0, 1.57, 3.14, -1.57
function Direction.NormalizeFacing(facing)
	if(facing <0) then
		facing = facing + 6.28;
	end
	return math.floor(facing/1.57+0.5)*1.57 - 3.14;
end

-- @param camx,camy,camz: camera eye position  if nil current camera is used
-- @param lookat_x,lookat_y,lookat_z: camera lookat position. if nil current camera lookat is used. 
function Direction.GetDirectionFromCamera(camx,camy,camz, lookat_x,lookat_y,lookat_z)
	local dx, dy, dz = math3d.CameraToWorldSpace(0, 0 ,1, camx,camy,camz, lookat_x,lookat_y,lookat_z);
	if(math.abs(dz) > math.abs(dx)) then
		if(dz>0) then
			return 2;
		else
			return 3;
		end
	else
		if(dx>0) then
			return 1;
		else
			return 4;
		end
	end
end

-- @param camx,camy,camz: camera eye position  if nil current camera is used
-- @param lookat_x,lookat_y,lookat_z: camera lookat position. if nil current camera lookat is used. 
function Direction.GetDirection2DFromCamera(camx,camy,camz, lookat_x,lookat_y,lookat_z)
	local dx, dy, dz = math3d.CameraToWorldSpace(0, 0 ,1, camx,camy,camz, lookat_x,lookat_y,lookat_z);
	if(math.abs(dz) > math.abs(dx)) then
		if(dz>0) then
			return 3;
		else
			return 2;
		end
	else
		if(dx>0) then
			return 1;
		else
			return 0;
		end
	end
end

function Direction.GetFacingFromCamera(camx,camy,camz, lookat_x,lookat_y,lookat_z)
	local dx, dy, dz = math3d.CameraToWorldSpace(0, 0 ,1, camx,camy,camz, lookat_x,lookat_y,lookat_z);
	local len = dx^2+dz^2;
	if(len>0.01) then
		len = math.sqrt(len)
		local facing = math.acos(dx/len);
		if(dz>0) then	
			facing = -facing;
		end
		return facing;
	else
		return 0;
	end
end

function Direction.GetFacingFromOffset(dx, dy, dz)
	local len = dx^2+dz^2;
	if(len>0.0000001) then
		len = math.sqrt(len)
		local facing = math.acos(dx/len);
		if(dz>0) then	
			facing = -facing;
		end
		return facing;
	else
		return 0;
	end
end

function Direction.GetPitchFromOffset(dx, dy, dz)
	local len = dx^2+dy^2+dz^2;
	if(len>0.0000001) then
		len = math.sqrt(len)
		local pitch = math.asin(dy/len);
		return pitch;
	else
		return 0;
	end
end

-- @return [0,5] based on camera position
function Direction.GetDirection3DFromCamera(camx,camy,camz, lookat_x,lookat_y,lookat_z)
	local dx, dy, dz = math3d.CameraToWorldSpace(0, 0 ,1, camx,camy,camz, lookat_x,lookat_y,lookat_z);
	if(dy>0.4) then
		return 5;
	elseif(dy < -0.8) then
		return 4;
	elseif(math.abs(dz) > math.abs(dx)) then
		if(dz>0) then
			return 3;
		else
			return 2;
		end
	else
		if(dx>0) then
			return 1;
		else
			return 0;
		end
	end
end


-- local quat = mathlib.QuatFromAxisAngle(0, 0, 1, 1.57);
-- echo(quat);
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, 3.14), quat));
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, -1.57), quat));
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, 1.57), quat));

-- local quat = mathlib.QuatFromAxisAngle(0, 0, 1, -1.57);
-- echo(quat);
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, 3.14), quat));
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, -1.57), quat));
-- echo(mathlib.QuaternionMultiply(mathlib.QuatFromAxisAngle(0, 1, 0, 1.57), quat));
local quats = {
	[1] = {y=0,x=0,w=1,z=0,},
	[4] = {y=0,x=0,w=0.70739,z=0.70683,},
	[5] = {y=0.70739,x=0.70683,w=0.00057,z=0.00057,},
	[6] = {y=-0.5,x=-0.4996,w=0.5004,z=0.5,},
	[7] = {y=0.5,x=0.4996,w=0.5004,z=0.5,},
	[8] = {y=0,x=0,w=0.70739,z=-0.70683,},
	[9] = {y=0.70739,x=-0.70683,w=0.00057,z=-0.00057,},
	[10] = {y=-0.5,x=0.4996,w=0.5004,z=-0.5,},
	[11] = {y=0.5,x=-0.4996,w=0.5004,z=-0.5,},
}

-- @param data: [4,11]
function Direction.GetQuaternionByData(data)
	return (data and data>=4 and data<=11) and quats[data] or quats[1];
end

--[[
Title: Tool Base
Author(s): LiXizhi
Date: 2014/11/25
Desc: base class for a tool. I have referenced the qobject class in QT framework. I remodeled it with NPL terms:
   * object is modeled as a neuron
   * a object can define any number signal functions. A signal function is an output axon connection. 
   * with Connect method, a signal(axon) can be dynamically connected to one or more objects' slot functions, like multiple synapses. 
   * object knows Nothing about which other objects are connected to it. 
   * object fire signals via axon connections to other objects. 

Signals and slots:	
	Slots can be used for receiving signals, but they are also normal member functions. 
	An object does not know if anything receives its signals, and a slot does not know if it has any signals connected to it. 
	This ensures truly independent components.
	You can connect as many signals as you want to a single slot, and a signal can be connected to as many slots as you need. 
	It is even possible to connect a signal directly to another signal. (This will emit the second signal immediately whenever the first is emitted.)
	If several slots are connected to one signal, the slots will be executed one after the other, in the order they have been connected, when the signal is emitted.

Coding style and internals: 
	Unlike QT, signals do not need to be defined explicitly. Any function on object can be used as a signal or a slot. 
	There is no meta class for class object, instead the object itself is used as the meta object and axon connections are instantiated on first use.  
	This allows more dynamic connection programming.
 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/ide/System/Core/ToolBase.lua");
local MyTool = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("System.Core.MyTool"));
-- define property
MyTool:Property({"Enabled", true, "isEnabled", auto=true});
MyTool:Property("Value", nil, nil, nil, "ValueChanged");
MyTool:Property("Tag");
MyTool:Property({"Visible"});
MyTool:Property({"BackgroundColor", "#cccccc", auto=true});
MyTool:Property({"down", nil, "isDown", "setDown"});
MyTool:Property({"size", type="double"});

-- define signal
MyTool:Signal("XXXChanged", function(only_for_doc)  end);
-- create instance
local tool1 = MyTool:new();
local tool2 = MyTool:new();
tool1:Connect("ValueChanged", tool2, "SetValue", "UniqueConnection");
-- disconnect 
tool1:Disconnect("ValueChanged", tool2, "SetTag");
-- invoke signals
tool1:Connect("XXXChanged", tool2, "SetTag");
tool1:XXXChanged("XXXChanged");
assert(tool2:GetTag() == "XXXChanged");
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Core/ToolBase_p.lua");
local EventTickFunc = commonlib.gettable("System.Core.EventTickFunc");
local ConnectionSynapse = commonlib.gettable("System.Core.ConnectionSynapse");
local SignalConnections = commonlib.gettable("System.Core.SignalConnections");
local type = type;
local ToolBase = commonlib.inherit(nil, commonlib.gettable("System.Core.ToolBase"));

ToolBase:Property({"Name", "ToolBase", auto=true});

-- all outgoing signals 
ToolBase.signal_connections = nil;
-- all incoming connections to this receiver. mapping from ConnectionSynapse to true. 
ToolBase.senders = nil;

function ToolBase:ctor()
	
end

function ToolBase:Destroy()
	self.wasDeleted = true;
	-- disconnect all receivers
	self:Disconnect();
	-- disconnect from all senders
	self:DisconnectSenders();

	self.currentSender = nil;

	self:deleteChildren();

	-- remove it from parent object
	if (self.parent) then
        self:setParent_helper(nil);
	end
end

-- call constructure recursively, however without assigning metatable. This is only for singleton init with self. 
-- so that new function is no longer called. 
local function ctor_recursive(o, current_class)
	current_class = current_class or o;
	if(current_class._super) then
		ctor_recursive(o, current_class._super);
	end
	local ctor = rawget(current_class, "ctor");
	if(type(ctor) == "function") then
		ctor(o);
	end
end

-- Returns true if this object is a parent, (or grandparent and so on
-- to any level), of the given child; otherwise returns false.
function ToolBase:isAncestorOf(child)
    while (child) do
        if (child == self) then
            return true;
        elseif (not child.parent) then
            return false;
		end
        child = child.parent;
    end
    return false;
end

function ToolBase:GetParent(name)
	if(name==nil) then
		return self.parent
	end
	local parent = self.parent;
	while (parent~=nil) do
		if(parent:GetField("Name",nil) == name) then
			return parent;
		end
		parent = parent.parent;
	end
end

-- static function: to use the class itself as a singleton object. 
-- this function can be called many times, only the first time succeed. 
-- Once called, it will disable new() method for object instantiation.  
function ToolBase:InitSingleton()
	if(not rawget(self, "singletonInited")) then
		self.singletonInited = true;
		ctor_recursive(self);
		-- disable new function. 
		self.new = nil;
	end
	return self;
end

-- get event system. 
function ToolBase:GetEvents()
	if(not self.events) then
		self.events = commonlib.EventSystem:new();
	end
	return self.events;
end

-- change the timer
-- @param dueTime The amount of time to delay before the invoking the callback method specified in milliseconds
--	Specify zero (0) to restart the timer immediately. Specify nil to prevent the timer from restarting. 
-- @param period The time interval between invocations of the callback method in milliseconds. 
--	Specify nil to disable periodic signaling. 
function ToolBase:ChangeTimer(dueTime, period)
	self.timer = self.timer or commonlib.Timer:new({callbackFunc = function(timer)
		self:OnTick();	
	end});
	self.timer:Change(dueTime, period);
end

function ToolBase:KillTimer()
	if(self.timer) then
		self.timer:Change();
	end
end

-- get event list. 
function ToolBase:GetEventList()
	if(self.eventCache) then
		return self.eventCache;
	else
		self.eventCache = commonlib.List:new();
		return self.eventCache;
	end
end

-- @param ms_delay_time: in ms seconds.
-- @param sender: nil or a class object or anonymous function. 
-- @param slot: the slot function. if nil, the sender can be an anonymous function. 
function ToolBase:ScheduleFunctionCall(ms_delay_time, sender, slot)
	if(slot) then
		self:GetEventList():add(EventTickFunc:new():init(ms_delay_time, sender, slot))
	elseif(type(sender) == "function") then
		self:GetEventList():add(EventTickFunc:new():init(ms_delay_time, nil, sender))
	else
		return;
	end

	self.event_timer = self.event_timer or commonlib.Timer:new({callbackFunc = function(timer)
		self:OnTickEvents(timer:GetDelta());
	end});
	if(not self.event_timer:IsEnabled()) then
		self.event_timer:Change(100,100);
	end
end

-- private function:
function ToolBase:OnTickEvents(deltaTime_ms)
	if(self.eventCache) then
		local eventCache = self.eventCache;
		local event = eventCache:first();
		while (event) do
			if(event:OnTick(deltaTime_ms)) then
				event = eventCache:remove(event);
			else
				event = eventCache:next(event);
			end
		end
		if(eventCache:size() == 0 and self.event_timer) then
			self.event_timer:Change(nil);
		end
	end
end

-- timer function callback:
function ToolBase:OnTick()
	
end

-- getting connection list of a signal function. 
-- this is like axon in human brain. 
-- @param signal: function or string of function name. 
-- @param bCreateIfNotExist: default to nil. 
-- @return a list of synapses on the signal(axon).
function ToolBase:GetConnection(signal, bCreateIfNotExist)
	if(type(signal) ~= "function") then
		local signal_func = self[signal];
		if(not signal_func)  then
			if(bCreateIfNotExist) then
				-- dynamically create the signal function and install to its meta table. 
				signal_func = function(self, ...)
					self:Activate(signal_func, ...);
				end
				local metatable = getmetatable(self) or self;
				metatable.__index[signal] = signal_func;
			else
				return;
			end
		end
		signal = signal_func;
	end
	if(not self.signal_connections) then
		self.signal_connections = SignalConnections:new();
	end
	local axon_connection = self.signal_connections:Get(signal);
	if(not axon_connection and bCreateIfNotExist) then
		axon_connection = commonlib.List:new();
		axon_connection.signal = signal;
		self.signal_connections:Set(signal, axon_connection);
	end
	return axon_connection;
end

-- static function: make automatic connection. If the sender is self pointer, it can be used as member function. 
-- @param connection_type: such as "UniqueConnection", if nil, default to "AutoConnection"
-- @param sender: the sender class object. 
-- @param signal: a member function (or name) on the sender. 
-- @param receiver:the receiver class object. it can also be anonymous function in which case this should be the last parameter. 
-- @param slot: a member function (or name) on the receiver to connect to. 
function ToolBase.Connect(sender, signal, receiver, slot, connection_type)
	if(not slot and type(receiver) == "function") then
		slot = receiver;
		receiver = nil;
	end
	if(not signal) then
		LOG.std(nil, "warn", "ToolBase:Connect", "invalid null parameter");
		return;
	end
	
	if(type(slot) == "string" and receiver) then
		slot = receiver[slot];
	end
	if(type(slot)~="function") then
		LOG.std(nil, "warn", "ToolBase:Connect", "slot not found in %s", commonlib.debugstack());
		return;
	end
	return ToolBase.ConnectImp(sender, signal, receiver, slot, connection_type);
end

-- implementation without parameter validation. 
function ToolBase.ConnectImp(sender, signal, receiver, slot, connection_type)
	if(not sender or not signal or (not receiver and not slot)) then
		LOG.std(nil, "warn", "ToolBase:Connect", "invalid null parameter");
		return;
	end
	local connection = sender:GetConnection(signal, true);
	if(connection) then
		if(connection_type == "UniqueConnection") then
			local synapse = connection:first();
			while (synapse) do
				if(synapse:IsConnectedTo(receiver, slot)) then
					-- connection already exist
					return;
				end
				synapse = connection:next(synapse);
			end
		end
		local signal = connection.signal;
		local synapse = ConnectionSynapse:new({
			sender = sender,
			signal = signal,
			receiver = receiver,
			slot = slot,
			connection_type = connection_type, 
		});
		connection:add(synapse);
		if(receiver) then
			receiver.senders = receiver.senders or {};
			receiver.senders[synapse] = true;
		end

		sender:ConnectNotify(signal);
	end
end

-- remove synapse from connection. 
function ToolBase:DisconnectHelper(connection, receiver, slot, disconnectType)
	local success;
	local synapse = connection:first();
	while (synapse) do
		if(not receiver or (synapse.receiver == receiver and (not slot or synapse.slot == slot))) then
			if(synapse.receiver and synapse.receiver.senders) then
				synapse.receiver.senders[synapse] = nil;
			end
			synapse = connection:remove(synapse);
			success = true;
			if(disconnectType == "DisconnectOne") then
				return success;
			end
		else
			synapse = connection:next(synapse);
		end
	end
	return success;
end

-- @param signal: if nil, it will remove all signal connections.
-- @param disconnectType: "DisconnectOne" or "DisconnectAll", default to all. 
function ToolBase.Disconnect(sender, signal, receiver, slot, disconnectType)
	if(not sender) then
		LOG.std(nil, "warn", "ToolBase:Connect", "invalid null parameter");
		return;
	end
	if(type(slot) == "string") then
		slot = receiver[slot];
	end
	local success; 
	if(not signal) then
		if(sender.signal_connections) then
			for signal, connection in sender.signal_connections:pairs() do
				if(sender:DisconnectHelper(connection, receiver, slot, disconnectType)) then
					success = true;
				end
			end
		end
	else
		local connection = sender:GetConnection(signal);
		if(connection) then
			if(sender:DisconnectHelper(connection, receiver, slot, disconnectType)) then
				success = true;
			end
		end
	end

	if (success) then
		sender:DisconnectNotify(signal);
	end
	return success;
end

-- disconnect from all senders
-- this function is mostly used in destructor to automatically break incoming connections.
function ToolBase:DisconnectSenders()
	if(self.senders) then
		for synapse, _ in pairs(self.senders) do
			local sender = synapse.sender;
			if(sender) then
				local connection = sender:GetConnection(synapse.signal);
				if(connection) then
					connection:remove(synapse);	
					sender:DisconnectNotify(synapse.signal);
				end
			end
		end
		self.senders = nil;
	end
end

-- disconnect all connections from a given sender
function ToolBase:DisconnectSender(srcSender)
	if(self.senders) then
		for synapse, _ in pairs(self.senders) do
			local sender = synapse.sender;
			if(sender == srcSender) then
				local connection = sender:GetConnection(synapse.signal);
				if(connection) then
					connection:remove(synapse);	
					sender:DisconnectNotify(synapse.signal);
				end
			end
		end
	end
end

-- Returns a pointer to the object that sent the signal, if called in
-- a slot activated by a signal; otherwise it returns 0. The pointer
-- is valid only during the execution of the slot that calls this
-- function from this object's thread context.
-- 
-- The pointer returned by this function becomes invalid if the
-- sender is destroyed, or if the slot is disconnected from the
-- sender's signal.
-- @warning This function violates the object-oriented principle of
-- modularity. However, getting access to the sender might be useful
-- when many signals are connected to a single slot.
function ToolBase:sender()
	--if (not self.currentSender) then
        --return;
	--end
	return self.currentSender;
end

-- static or member function: activate a given signal, all connected slots will be called. 
-- @param sender: usually self. if used as a member function. 
function ToolBase.Activate(sender, signal, ...)
	local connection = sender:GetConnection(signal);
	if(connection) then
		local synapse = connection:first();
		local synapse_next;
		while (synapse) do
			-- fixed: this will allow synapse:Activate() to remove the current signal
			-- however, it does not prevent other deletion cases inside activate call
			-- it is not recommended to call Disconnect inside current signal. 
			synapse_next = connection:next(synapse);
			synapse:Activate(...);
			synapse = synapse_next;
		end
	end
end

-- This virtual function is called when something has been connected
-- to a signal in this object. 
-- warning This function violates the object-oriented principle of
-- modularity. However, it might be useful for optimizing access to expensive resources.
function ToolBase:ConnectNotify(signal)
end

-- This virtual function is called when something has been disconnected from a signal in this object.
-- warning This function violates the object-oriented principle of
-- modularity. However, it might be useful for optimizing access to expensive resources.
function ToolBase:DisconnectNotify(signal)
end

function ToolBase:GetChildren()
	if(not self.children) then
		self.children = commonlib.List:new();
	end
	return self.children;
end

function ToolBase:SetParent(parent)
	self:setParent_helper(parent);
end

function ToolBase:setParent_helper(parent)
	local oldParent = self.parent;
	if (parent == oldParent) then
        return;
	end
	if (oldParent) then
		if(oldParent.isDeletingChildren) then
			-- don't do anything since deleteChildren() already cleared our entry in self.children.
		else
			oldParent.children:remove(self);
		end
	end
	self.parent = parent;
    if (parent) then
		local children = parent:GetChildren();
		children:add(self);
	end
end

function ToolBase:deleteChildren()
	local children = self.children;
	if(children) then
		self.isDeletingChildren = true;
		
		local child = children:first();
		while (child) do
			child:Destroy();
			child = children:remove(child)
		end
		children:clear();

		self.isDeletingChildren = false;
	end
end

-- search function name by func object, in all class hierachy and meta table index.
-- only used for debugging. 
local function FindFunctionName(obj, func)
	if(type(func) == "function" and obj) then
		for name, value in pairs(obj) do
			if(func == value) then
				return tostring(name);
			end
		end
		local meta = getmetatable(obj);
		if(type(meta) == "table" and meta.__index) then
			if(meta.__index ~= obj._super) then
				for name, value in pairs(meta.__index) do
					if(func == value) then
						return tostring(name);
					end
				end
			end
		end

		if(obj._super) then
			return FindFunctionName(obj._super, func);
		end
	end
	return tostring(func);
end

 -- Dumps information about signal connections, etc. for this object to the log.
function ToolBase:dumpObjectInfo()
    log(format("OBJECT %s\n", self:GetName()));
    -- first, look for connections where this object is the sender
    log("  SIGNALS OUT\n");

    if (self.signal_connections) then
        for signal, connections in self.signal_connections:pairs() do 
            log(format("        signal: %s\n", FindFunctionName(self, signal)));

            -- receivers
            local c = connections:first();
			while (c) do
				
			    if (not c.receiver) then
                    log("          <Disconnected receiver>\n");
                else
					log(format("          --> %s %s\n", c.receiver:GetName(), FindFunctionName(c.receiver, c.slot)));
                end
				c= connections:next(c);
            end
        end
    else
        log( "        <None>\n");
    end

    -- now look for connections where this object is the receiver
    log("  SIGNALS IN\n");
    if (self.senders) then
		for s, _ in pairs(self.senders) do
            log(format("          <-- %s  %s\n", s.sender:GetName(), FindFunctionName(s.sender, s.signal)));
        end
    else
        log("        <None>\n");
	end
end


-- Installs an event filter obj on this object. filter is like the hook chain
-- An event filter is an object that receives all events that are
-- sent to this object. The filter can either stop the event or
-- forward it to this object. The event filter obj receives
-- events via its eventFilter() function. The eventFilter() function
-- must return true if the event should be filtered, (i.e. stopped);
-- otherwise it must return false.
-- If multiple event filters are installed on a single object, the
-- filter that was installed last is activated first.
function ToolBase:installEventFilter(obj)
    if (not obj) then
        return;
	end
    if (not self.eventFilters) then
		self.eventFilters = commonlib.Array:new();
	end
    -- clean up unused items in the list
	self:removeEventFilter(obj);
    self.eventFilters:push_front(obj);
end

-- Removes an event filter object obj from this object. The
-- request is ignored if such an event filter has not been installed.
-- All event filters for this object are automatically removed when
-- this object is destroyed.
-- It is always safe to remove an event filter, even during event
-- filter activation (i.e. from the eventFilter() function).
function ToolBase:removeEventFilter(obj)
    if (self.eventFilters) then
        local finished = false;
		while (not finished) do
			finished = true;
			for i, filterObj in ipairs(self.eventFilters) do
				-- also clean up unused items in the list
				if(filterObj.wasDeleted or obj == filterObj) then
					self.eventFilters:remove(i);
					finished = false;
					break;
				end
			end
		end
    end
end

-- filter the event
-- @return true if event is stopped by one of the filtered objects. 
function ToolBase:filterEvent(object, event)
	if (self.eventFilters) then
		local filters = self.eventFilters;
		for i = 1, #filters do
			local filterObj = filters[i];
			if(not filterObj.wasDeleted) then
				if(filterObj:eventFilter(obj, event)) then
					return true;
				end
			end
		end
	end
end

-- virtual function: 
-- Filters events if this object has been installed as an event
-- filter for the watched object.
-- In your reimplementation of this function, if you want to filter
-- the event out, i.e. stop it being handled further, return
-- true; otherwise return false.
-- @sa installEventFilter()
function ToolBase:eventFilter(object, event)
	-- return true; -- return true to stop the event
end
```