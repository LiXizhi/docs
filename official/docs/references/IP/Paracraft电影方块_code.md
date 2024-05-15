```lua
--[[
Title: base actor class
Author(s): LiXizhi
Date: 2014/3/30
Desc: for recording and playing back
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
local actor = commonlib.gettable("MyCompany.Aries.Game.Movie.Actor");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/TimeSeries.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/MovieClipController.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/MovieTimeSeriesEditingTask.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/MovieClipTimeLine.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/MovieManager.lua");
local MovieManager = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieManager");
local vector3d = commonlib.gettable("mathlib.vector3d");
local MovieClipTimeLine = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieClipTimeLine");
local MovieTimeSeriesEditing = commonlib.gettable("MyCompany.Aries.Game.Tasks.MovieTimeSeriesEditing");
local MovieClipController = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieClipController");
local TimeSeries = commonlib.gettable("MyCompany.Aries.Game.Common.TimeSeries");
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local type = type;
local Actor = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Movie.Actor"));
Actor.class_name = "Actor";
Actor:Property("Name", "Actor");
Actor:Property({"isAgent", false, "IsAgent"});
-- whenever the current time is changed or any key is modified. 
Actor:Signal("valueChanged");
-- whenever any of the actor's key data is modified. 
Actor:Signal("keyChanged");
-- the current selected editable variable changed. 
Actor:Signal("currentEditVariableChanged");
-- the itemstack(TimeSeries) is changed, possibly during undo/redo operation. 
Actor:Signal("dataSourceChanged");
Actor:Signal("focusIn");
Actor:Signal("focusOut");

Actor.valueFields = commonlib.ArrayMap:new();

function Actor:ctor()
	self.TimeSeries = TimeSeries:new{name = "Actor",};
	self.valueFields = commonlib.ArrayMap:new();
	self.custom_vars = {};
end

function Actor:Init(itemStack, movieclipEntity, movieclip)
	self:SetItemStack(itemStack)
	self.movieclipEntity = movieclipEntity;
	self:SetMovieClip(movieclip or self.movieclipEntity:GetMovieClip())
	return self;
end

function Actor:SetInitParams(params)
	if(not self.initParams) then
		self.initParams = params;
	else
		commonlib.partialcompare(self.initParams, params);
	end
end

function Actor:GetInitParams()
	return self.initParams;
end

function Actor:SetInitParam(name, value)
	self.initParams = self.initParams or {};
	self.initParams[name] = value;
end

function Actor:GetInitParam(name)
	return self.initParams and self.initParams[name];
end

-- virtual:
function Actor:ApplyInitParams()
end

function Actor:SetCodeBlock(codeblock)
	self.codeblock = codeblock;
end

function Actor:GetCodeBlock()
	return self.codeblock;
end

function Actor:SetItemStack(itemStack)
	self.itemStack = itemStack;
	self:BindItemStackToTimeSeries();
end

function Actor:GetTimeSeries()
	return self.TimeSeries;
end

-- this is called right after all actors in movie clips have been created. 
function Actor:OnCreate()
end

-- find actor by its display name in containing movie entity
-- @return actor or nil.
function Actor:FindActor(name)
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		return movieClip:FindActor(name);
	end
end

function Actor:GetRootActor()
	local parent = self:GetParentActor();
	if(not parent) then
		return self;
	else
		return parent:GetRootActor();
	end
end

function Actor:SetParentActor(actor)
	self.parentActor = actor;
end

function Actor:GetParentActor()
	return self.parentActor;
end

-- virtual function
function Actor:GetChildActor(name)
end

function Actor:GetCustomVariable(name)
	return self.custom_vars[name];
end

function Actor:SetCustomVariable(name, value)
	self.custom_vars[name] = value;
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

function Actor:GetBoundRadius()
	local entity = self:GetEntity();
	if(entity) then
		return entity:GetBoundRadius();
	end
	return 0;
end

function Actor:IsAllowUserControl()
	local entity = self:GetEntity();
	if(entity) then
		return entity:HasFocus() and not self:IsPlayingMode() and self:IsPaused() and 
			not MovieClipController.IsActorsLocked() and
			not MovieClipTimeLine.IsDraggingTimeLine();
	end
end

-- user is using WASD key to control this actor now. 
function Actor:IsUserControlled()
	local entity = self:GetEntity();
	if(entity) then
		return entity:HasFocus() and not entity:IsControlledExternally();
	end
end

-- get the movie clip that contains this actor. 
function Actor:GetMovieClip()
	return self.movieclip;
end

function Actor:SetMovieClip(movieClip)
	self.movieclip = movieClip;
end

function Actor:GetMovieClipEntity()
	return self.movieclipEntity;
end

-- whether its persistent. 
function Actor:IsPersistent()
	return self.is_persistent;
end

-- whether the entity should be serialized to disk. 
function Actor:SetPersistent(bIsPersistent)
	self.is_persistent = bIsPersistent;
end


-- it is only in playing mode when activated by a circuit. 
-- any other way of triggering the movieclip is not playing mode(that is edit mode)
function Actor:IsPlayingMode()
	if(self.movieclip) then
		return self.movieclip:IsPlayingMode();
	end
end

function Actor:GetSelectionName()
	return self:GetDisplayName();
end

-- get display name
function Actor:GetDisplayName()
	if(self.itemStack) then
		return self.itemStack:GetDisplayName() or "";
	end
	return "";
end

function Actor:SetDisplayName(name)
	if(self.itemStack) then
		self.itemStack:SetDisplayName(name);
	end
end

-- @return the entity position if any
function Actor:GetPosition()
	if(self.entity) then
		return self.entity:GetPosition();
	end
end

-- @return the entity position if any
function Actor:GetRollPitchYaw()
	if(self:GetEntity()) then
		local obj = self:GetEntity():GetInnerObject();
		if(obj) then
			return obj:GetField("roll", 0), obj:GetField("pitch", 0), obj:GetField("yaw", 0);
		end
	end
	return 0,0,0;
end


function Actor:GetTime()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		return movieClip:GetTime();
	end
end

function Actor:SetTime(time)
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		return movieClip:SetTime(time);
	end
end


function Actor:GetEntity()
	return self.entity;
end

-- use BeginUpdate() and EndUpdate() to avoid entity be refreshed. 
function Actor:SaveStaticAppearance()
	--self:BeginUpdate();
	-- save code here
	--self:EndUpdate();
end

function Actor:GetItemStack()
	return self.itemStack;
end

function Actor:OpenEditor()
	MovieClipController.SetFocusToItemStack(self.itemStack);
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

-- virtual:
-- @return nil or a table of variable list. 
function Actor:GetEditableVariableList()
end

-- virtual: 
-- get editable variable by index. only used by editor for recently selected variable. 
-- @param selected_index: nil if it means the current one. 
-- @return var, cur_index
function Actor:GetEditableVariable(selected_index)
	local varList = self:GetEditableVariableList();
	if(varList) then
		selected_index = selected_index or self:GetCurrentEditVariableIndex();
		return self.TimeSeries:GetVariable(varList[selected_index]);
	end
end

function Actor:GetCurrentEditVariableIndex()
	return self.curEditVariableIndex or 1;
end

-- whether we will also show  the command actor's variables on this actor's timeline. 
function Actor:CanShowCommandVariables()
	return false;
end

-- return index by name
-- @return index
function Actor:FindEditVariableByName(name)
	local varList = self:GetEditableVariableList();
	if(varList) then
		for index, var in ipairs(varList) do
			if(var == name) then
				return index;
			end
		end
	end
end

function Actor:SetCurrentEditVariableIndex(selected_index)
	if(self.curEditVariableIndex~=selected_index) then
		self.curEditVariableIndex = selected_index;
		self:currentEditVariableChanged(selected_index);
	end
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

-- get last recorded time.
function Actor:GetLastTime(keyname)
	local v = self:GetVariable(keyname);
	if(v) then
		return v:GetLastTime() or 0;
	end
	return 0;
end

function Actor:IsSelected()
	return Game.SelectionManager:GetSelectedActor() == self;
end

-- select me: for further editing. 
function Actor:SelectMe()
	local entity = self:GetEntity();
	if(entity) then
		local obj = entity:GetInnerObject();
		if(obj) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/SelectModelTask.lua");
			local task = MyCompany.Aries.Game.Tasks.SelectModel:new({obj=obj})
			task:Run();	
		end
	end
end

-- a pair of BeginModify and EndModify will allow undo/redo of the actor's timeline. 
function Actor:BeginModify()
	self.undo_task = MovieTimeSeriesEditing:new()
	self.undo_task:BeginModify(self:GetMovieClip(), self:GetItemStack());
end

function Actor:EndModify()
	if(self.undo_task) then
		self.undo_task:EndModify();
		self.undo_task = nil;
		self:SetModified();
	end
end

-- @return true if recording. 
function Actor:SetRecording(isRecording)
	if(self:IsKeyFrameOnly()) then
		return nil;
	else
		if(isRecording~=self.isRecording) then
			self.isRecording = isRecording;

			if(isRecording) then
				self:BeginModify();
			else
				self:EndModify();
			end

			if(isRecording) then
				--self:RemoveKeysInTimeRange(self:GetTime(), self:GetCurrentRecordingEndTime());
				self:ClearRecordToTime();
			end
			
			local movieClip = self:GetMovieClip();
			if(movieClip) then
				movieClip:SetActorRecording(self, isRecording);
			end
		end
		return self.isRecording;
	end
end

function Actor:IsRecording()
	return self.isRecording == true;
end


-- add new key at time, data. if there is already a key at the time, we will replace it. 
function Actor:AddKey(keyname, time, value)
	local v = self:GetVariable(keyname);
	if(v) then
		if(v:AddKey(time, value)) then
			self:SetModified();
			return true;
		end
	end
end

-- when a group of changes takes place, such as during recording, 
-- we can put change inside BeginUpdate() and EndUpdate() pairs, so that 
-- only one keyChanged() event will be emitted. 
function Actor:BeginUpdate()
	if(not self.isBeginAddKey) then
		self.isBeginAddKey = 0;
		self.isKeyChanged = false;
	else
		self.isBeginAddKey = self.isBeginAddKey + 1;
	end
end

function Actor:EndUpdate()
	if(self.isBeginAddKey) then
		if(self.isBeginAddKey <= 0) then
			self.isBeginAddKey = false;
			if(self.isKeyChanged) then
				self.isKeyChanged = false;
				self:SetModified();
			end
		else
			self.isBeginAddKey = self.isBeginAddKey - 1;
		end
	end
end

function Actor:SetModified()
	if(self.isBeginAddKey) then
		self.isKeyChanged = true;
	else
		self:valueChanged();
		self:keyChanged();
	end
end

-- add new key at time, data. if there is already a key at the time, we will replace it. 
-- it will not add key if previous and next key is same as current. 
-- this function is ideal for recording player actions. 
function Actor:AutoAddKey(keyname, time, value)
	local v = self:GetVariable(keyname);
	if(v) then
		local res;
		if(self.is_adding_key) then
			res = v:AddKey(time, value);
		else
			-- res = v:AutoAddKey(time, value);
			res = v:AutoAppendKey(time, value);
		end
		if(res) then
			self:SetModified();
		end
	end
end

-- clear all keys after time, and add the new key. 
function Actor:AutoAppendKey(keyname, time, value)
	local v = self:GetVariable(keyname);
	if(v) then
		local res;
		if(self.is_adding_key) then
			res = v:AddKey(time, value);
		else
			res = v:AutoAppendKey(time, value);
		end
		if(res) then
			self:SetModified();
		end
	end
end

-- record and add a key frame at the current position. 
function Actor:AddKeyFrame()
	self.is_adding_key = true;
	self:FrameMoveRecording(0);
	self:SetControllable(self:IsAllowUserControl() == true);
	self.is_adding_key = nil;
end

-- virtual function: display a UI to let the user to edit this keyframe's data. 
function Actor:EditKeyFrame(keyname, time)
	time = time or self:GetTime();
end

-- add a key frame at the specified position. 
-- @param time: if nil, it is current time. 
function Actor:AddKeyFrameByName(name, time, data)
	if(data~=nil) then
		self:BeginModify();
		self.is_adding_key = true;
		time = time or self:GetTime();
		self:AutoAddKey(name, time, data);
		self.is_adding_key = nil;
		self:EndModify();
	end
end


-- get current recording end time. 
function Actor:GetCurrentRecordingEndTime()
	return self:GetMaxLength();
end

function Actor:GetMaxLength()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		return movieClip:GetLength() or 10000;
	end
	return 10000;
end

-- shifting keyframes from shift_begin_time to end by the amount of offset_time. 
function Actor:ShiftKeyFrame(shift_begin_time, offset_time)
	self:BeginModify();
	local max_length = self:GetMaxLength();
	if((shift_begin_time+offset_time) > max_length) then
		offset_time = max_length - shift_begin_time;
	end
	self.TimeSeries:ShiftKeyFrame(shift_begin_time, offset_time);
	self:SetModified();
	self:EndModify();
end

-- remove the key frame at key_time if there is a key frame. 
function Actor:RemoveKeyFrame(keytime)
	self:BeginModify();
	self.TimeSeries:RemoveKeyFrame(keytime);
	self:SetModified();
	self:EndModify();
end

-- copy keyframe from from_keytime to keytime
function Actor:CopyKeyFrame(keytime, from_keytime)
	self:BeginModify();
	self.TimeSeries:CopyKeyFrame(keytime, from_keytime);
	self:SetModified();
	self:EndModify();
end

-- Update or insert (Upsert) a key frame at given time.
-- @param data: data is cloned before updating. 
function Actor:UpsertKeyFrame(key_time, data)
	self:BeginModify();
	self.TimeSeries:UpsertKeyFrame(key_time, data);
	self:SetModified();
	self:EndModify();
end

-- paste all key frames between [fromTime, toTime] to time
function Actor:PasteKeyFramesInRange(time, fromTime, toTime)
	self:BeginModify();
	self.TimeSeries:PasteKeyFramesInRange(time, fromTime, toTime);
	self:SetModified();
	self:EndModify();
end

-- move keyframe from from_keytime to keytime
function Actor:MoveKeyFrame(keytime, from_keytime)
	self:BeginModify();
	self.TimeSeries:MoveKeyFrame(keytime, from_keytime);
	self:SetModified();
	self:EndModify();
end



function Actor:Resume()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		movieClip:Resume();
	end
end

function Actor:Pause()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		movieClip:Pause();
	end
end

function Actor:IsPaused()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		return movieClip:IsPaused();
	end
end

function Actor:Stop()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		movieClip:Stop();
	end
end

function Actor:GotoBeginFrame()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		movieClip:GotoBeginFrame();
		movieClip:Pause();
	end
end

function Actor:GotoEndFrame()
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		movieClip:GotoEndFrame();
		movieClip:Pause();
	end
end

function Actor:RestartRecording()
	self:Stop();
	self:SetRecording(true);
	self:Resume();
end

-- clear all record to a given time. if curTime is nil, it will use the current time. 
function Actor:ClearRecordToTime(curTime)
	-- trim all keys to current time
	local curTime = curTime or self:GetTime();
	if(curTime) then
		if(curTime <= 0) then
			self.TimeSeries:TrimEnd(curTime-1)
		else
			self.TimeSeries:TrimEnd(curTime);
		end	
		self:SetModified();
	end
end

-- remove all keys in the [fromTime, toTime]
-- @param fromTime: if fromTime is nil, it will use the current time. 
-- @param toTime: if nil, it will be max length. 
function Actor:RemoveKeysInTimeRange(fromTime, toTime)
	-- trim all keys to current time
	local fromTime = fromTime or self:GetTime();
	local toTime = toTime or self:GetMaxLength();
	if(fromTime and toTime) then
		self.TimeSeries:RemoveKeysInTimeRange(fromTime, toTime);
		self:SetModified();
	end
end

function Actor:SetControllable(bIsControllable)
end

-- whether the actor can create blocks. The camera actor can not create blocks
function Actor:CanCreateBlocks()
	return;
end

-- this function is called whenver the create block task is called. i.e. the user has just created some block
function Actor:OnCreateBlocks(blocks)
end

-- this function is called whenver the destroy block task is called. i.e. the user has just destroyed some blocks
function Actor:OnDestroyBlocks(blocks)
end

function Actor:SetFocus()
	local entity = self:GetEntity()
	if(entity) then
		self.lastTime = nil;
		entity:SetFocus();
	end
end

function Actor:HasFocus()
	local entity = self:GetEntity()
	if(entity) then
		return entity:HasFocus();
	end
end

function Actor:DestroyEntity()
	local entity = self:GetEntity()
	if(entity and not self:IsAgent()) then
		if(entity:HasFocus()) then
			EntityManager.SetFocus(EntityManager.GetPlayer());
		end
		entity:Destroy();
		self.entity = nil;
	end
end

-- remove the scene entity that representing this actor. 
function Actor:OnRemove()
	self:DestroyEntity();
end

function Actor:FrameMoveRecording(deltaTime)
end

function Actor:FrameMovePlaying(deltaTime)
end

-- only supporting key frames, not recording. 
function Actor:IsKeyFrameOnly()
	return false;
end

-- whether the actor is being selected in the editor
function Actor:FrameMove(deltaTime, bIsSelected)
	if(self:IsRecording())then
		self:FrameMoveRecording(deltaTime);
	else
		self:FrameMovePlaying(deltaTime, bIsSelected);
	end
	if(bIsSelected)  then
		local time = self:GetTime();
		if(self.lastTime ~= time) then
			self.lastTime = time;
			self:valueChanged();
		end
	end
end

-------------------------------------
-- reimplement attribute field 
-------------------------------------

-- @param getVar: get variable function. it is function that usually return the multivariable
-- @return attribute plug
function Actor:AddValue(name, getVar)
	self.valueFields:add(name, {name=name, getVar=getVar})
	return self:findPlug(name);
end

function Actor:GetFieldNum()
	return self.TimeSeries:GetVariableCount() + self.valueFields:size();
end

function Actor:GetFieldIndex(name)
	return self.TimeSeries:GetVariableIndex(name) 
		or ((self.valueFields:getIndex(sFieldname) or 0) + self.TimeSeries:GetVariableCount());
end

function Actor:GetFieldName(valueIndex)
	if(valueIndex <= self.TimeSeries:GetVariableCount()) then
		return self.TimeSeries:GetVariableName(valueIndex);
	else
		local field = self.valueFields:at(valueIndex - self.TimeSeries:GetVariableCount());
		if(field) then
			return field.name;
		end
	end
end

function Actor:GetFieldType(nIndex)
	return "";
end

function Actor:SetField(name, value)
	local oldValue = self:GetField(name);
	-- skip equal values
	if(type(oldValue)== "table") then
		if(commonlib.partialcompare(oldValue, value)) then
			return;
		end
	elseif(oldValue == value) then
		return;
	end

	local field = self.valueFields:get(name);
	if(field) then
		if(field.getVar(self):AddKey(self:GetTime(), value)) then
			self:SetModified();
		end
	else
		self:AddKey(name, self:GetTime(), value);	
	end
end

function Actor:GetField(name, defaultValue)
	local field = self.valueFields:get(name);
	if(field) then
		return field.getVar(self):getValue(1, self:GetTime());
	else
		return self:GetValue(name, self:GetTime()) or defaultValue;
	end
end

-- return the inner biped object
function Actor:GetInnerObject()
	local entity = self:GetEntity();
	if(entity) then
		return entity:GetInnerObject();
	end
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

-- if no camera position is found, the current actor's position is used. 
function Actor:RestoreLastFreeCameraPosition()
	local cameraEntity = GameLogic.GetFreeCamera();
	if(self.lastFreeCameraPos) then
		local dx, dy, dz = self.lastFreeCameraPos.dx, self.lastFreeCameraPos.dy, self.lastFreeCameraPos.dz;
		local ax, ay,az = self:GetPosition();
		cameraEntity:SetPosition(dx+ax, dy+ay, dz+az);
		ParaCamera.SetEyePos(self.lastFreeCameraPos.eye_dist, self.lastFreeCameraPos.eye_liftup, self.lastFreeCameraPos.eye_rot_y);
	else
		cameraEntity:SetPosition(self:GetPosition());
	end
end

-- @param bForceSave: if nil, we will only save if free camera has focus
function Actor:SaveFreeCameraPosition(bForceSave)
	local cameraEntity = GameLogic.GetFreeCamera();
	
	if(cameraEntity) then
		if(cameraEntity:HasFocus() or bForceSave) then
			if(not self.lastFreeCameraPos) then
				self.lastFreeCameraPos = {};
			end
			local x, y, z = cameraEntity:GetPosition();
			local ax, ay,az = self:GetPosition();
			self.lastFreeCameraPos.dx = x - ax;
			self.lastFreeCameraPos.dy = y - ay;
			self.lastFreeCameraPos.dz = z - az;
			self.lastFreeCameraPos.eye_dist, self.lastFreeCameraPos.eye_liftup, self.lastFreeCameraPos.eye_rot_y = ParaCamera.GetEyePos();
		end
	else
		self.lastFreeCameraPos = nil;
	end
end

function Actor:CanShowSelectManip()
	return true
end

function Actor:IsAgent()
	return self.isAgent;
end

-- taking control of the give entity. But it will not delete the entity when actor is removed.
function Actor:BecomeAgent(entity)
	if(entity) then --  and entity:isa(EntityManager.EntityMovable)
		local lastEntity = self:GetEntity();
		if(lastEntity ~= entity) then	
			self:DestroyEntity();
		end
		self.entity = entity;
		self.isAgent = true;
		MovieManager:AddActorName(entity.name or "");
	end
end

--[[
Title: camera actor
Author(s): LiXizhi
Date: 2014/3/30
Desc: for recording and playing back of camera creation and editing. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorCamera.lua");
local ActorCamera = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorCamera");
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/math/math3d.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/MultiAnimBlock.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/MovieClipTimeLine.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Commands/CmdParser.lua");
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");
local MovieClipTimeLine = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieClipTimeLine");
local MultiAnimBlock = commonlib.gettable("MyCompany.Aries.Game.Common.MultiAnimBlock");
local EntityCamera = commonlib.gettable("MyCompany.Aries.Game.EntityManager.EntityCamera")
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local CameraController = commonlib.gettable("MyCompany.Aries.Game.CameraController")

local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.Actor"), commonlib.gettable("MyCompany.Aries.Game.Movie.ActorCamera"));

Actor.class_name = "ActorCamera";
-- default to none-fps mode, the lookat position is more smooth than FPS one. 
local default_fps_mode = 0;
-- take a key frame every 5 seconds. 
Actor.auto_record_interval = 5000;

-- keyframes that can be edited from UI keyframe. 
local selectable_var_list = {
	"pos", -- multiple of x,y,z
	"rot", -- multiple of "roll", "pitch", "facing"
	"scaling",
	"static", -- multiple of "name" and "isAgent"
};


function Actor:ctor()
	self.curEditVariableIndex = -1;
end

function Actor:GetMultiVariable()
	local var = self:GetCustomVariable("multi_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new();
		var:AddVariable(self:GetVariable("lookat_x"));
		var:AddVariable(self:GetVariable("lookat_y"));
		var:AddVariable(self:GetVariable("lookat_z"));
		var:AddVariable(self:GetVariable("eye_dist"));
		var:AddVariable(self:GetVariable("eye_liftup"));
		var:AddVariable(self:GetVariable("eye_rot_y"));
		var:AddVariable(self:GetVariable("eye_roll"));
		self:SetCustomVariable("multi_variable", var);
		return var;
	end
end

-- get rotate multi variable
function Actor:GetStaticVariable()
	local var = self:GetCustomVariable("static_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="static"});
		var:AddVariable(self:GetVariable("name"));
		var:AddVariable(self:GetVariable("isAgent"));
		self:SetCustomVariable("static_variable", var);
		return var;
	end
end

-- get position multi variable
function Actor:GetPosVariable()
	local var = self:GetCustomVariable("pos_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="pos"});
		var:AddVariable(self:GetVariable("lookat_x"));
		var:AddVariable(self:GetVariable("lookat_y"));
		var:AddVariable(self:GetVariable("lookat_z"));
		self:SetCustomVariable("pos_variable", var);
		return var;
	end
end

-- get rotate multi variable
function Actor:GetRotateVariable()
	local var = self:GetCustomVariable("rot_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="rot"});
		var:AddVariable(self:GetVariable("eye_roll"));
		var:AddVariable(self:GetVariable("eye_liftup"));
		var:AddVariable(self:GetVariable("eye_rot_y"));
		self:SetCustomVariable("rot_variable", var);
		return var;
	end
end


function Actor:GetRollVariable()
	return self:GetVariable("eye_roll");
end

function Actor:GetYawVariable()
	return self:GetVariable("eye_rot_y");
end

function Actor:GetPitchVariable()
	return self:GetVariable("eye_liftup");
end

function Actor:GetScalingVariable()
	return self:GetVariable("eye_dist");
end

function Actor:Init(itemStack, movieclipEntity, isReuseActor, newName, movieclip)
	if(not Actor._super.Init(self, itemStack, movieclipEntity, movieclip)) then
		return;
	end

	local timeseries = self.TimeSeries;
	
	timeseries:CreateVariableIfNotExist("lookat_x", "Linear");
	timeseries:CreateVariableIfNotExist("lookat_y", "Linear");
	timeseries:CreateVariableIfNotExist("lookat_z", "Linear");
	timeseries:CreateVariableIfNotExist("eye_dist", "Linear");
	timeseries:CreateVariableIfNotExist("eye_liftup", "Linear");
	timeseries:CreateVariableIfNotExist("eye_rot_y", "LinearAngle");
	timeseries:CreateVariableIfNotExist("eye_roll", "LinearAngle");
	timeseries:CreateVariableIfNotExist("is_fps", "Discrete");
	timeseries:CreateVariableIfNotExist("has_collision", "Discrete");
	timeseries:CreateVariableIfNotExist("name", "Discrete");
	timeseries:CreateVariableIfNotExist("isAgent", "Discrete"); -- true, nil|false, "relative", "searchNearPlayer"
	
	self:AddValue("position", self.GetPosVariable);
	self:AddValue("roll", self.GetRollVariable);
	self:AddValue("facing", self.GetYawVariable);
	self:AddValue("pitch", self.GetPitchVariable);
	self:AddValue("scaling", self.GetScalingVariable);

	-- get initial position from itemStack, if not exist, we will use movie clip entity's block position. 
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		local x, y, z = movieClip:GetOrigin();
		y = y + BlockEngine.blocksize;

		x = self:GetValue("lookat_x", 0) or x;
		y = self:GetValue("lookat_y", 0) or y;
		z = self:GetValue("lookat_z", 0) or z;

		local att = ParaCamera.GetAttributeObject();

		self.entity = EntityCamera:Create({x=x,y=y,z=z, item_id = block_types.names.TimeSeriesCamera});
		self.entity:SetPersistent(false);
		self.entity:Attach();
		return self;
	end
end

-- this is called right after all actors in movie clips have been created. 
function Actor:OnCreate()
	local movieClip = self:GetMovieClip();
	if(movieClip:IsPlayingMode()) then
		local isAgent = self:GetValue("isAgent", 0);
		local offsetFacing;
		if(isAgent) then
			if(isAgent == "searchNearPlayer") then
				-- relative to player actor in the  movie clip
				local playerActor = movieClip:FindActor("player");
				if(playerActor) then
					self.offset_x, self.offset_y, self.offset_z =  playerActor.offset_x, playerActor.offset_y, playerActor.offset_z;
					self.offset_facing = playerActor:GetOffsetFacing();
				end
			elseif(isAgent == "relative") then
				-- relative to current camera position
				local x = self:GetValue("lookat_x", 0);
				local y = self:GetValue("lookat_y", 0);
				local z = self:GetValue("lookat_z", 0);
				if(x and y and z) then
					local cx, cy, cz = ParaCamera.GetLookAtPos()
					self.offset_x, self.offset_y, self.offset_z =  cx-x, cy-y, cz-z;
					local facing = self:GetValue("eye_rot_y", 0);
					local camobjDist, LifeupAngle, CameraRotY = ParaCamera.GetEyePos();
					self.offset_facing = CameraRotY - (facing or 0)
				end
			end
		end
	end
end

function Actor:IsKeyFrameOnly()
	return true;
end

-- @return nil or a table of variable list. 
function Actor:GetEditableVariableList()
	return selectable_var_list;
end

-- whether we will also show  the command actor's variables on this actor's timeline. 
-- self.curEditVariableIndex must be -1 in order for command actor's variable to be selected. otherwise, this actor's variable is selected.
function Actor:CanShowCommandVariables()
	return true;
end

-- @param selected_index: if nil,  default to current index
-- @return var
function Actor:GetEditableVariable(selected_index)
	selected_index = selected_index or self:GetCurrentEditVariableIndex();
	
	local name = selectable_var_list[selected_index];
	local var;
	if(name == "pos") then
		var = self:GetPosVariable();
	elseif(name == "rot") then
		var = self:GetRotateVariable();
	elseif(name == "scaling") then
		var = self:GetScalingVariable();
	elseif(name == "static") then
		var = self:GetStaticVariable();
	elseif(name) then
		var = self.TimeSeries:GetVariable(name);
	end
	return var;
end

-- @return true if recording. 
function Actor:SetRecording(isRecording)
	isRecording = isRecording == true;
	if(isRecording~=self:IsRecording()) then
		self.isRecording = isRecording;

		if(isRecording) then
			self.begin_recording_time = self:GetTime();
			--self:RemoveKeysInTimeRange(self:GetTime(), self:GetCurrentRecordingEndTime());
			self:ClearRecordToTime();
		else
			self.begin_recording_time = nil;
			self.end_recording_time = self:GetTime();
		end
			
		local movieClip = self:GetMovieClip();
		if(movieClip) then
			movieClip:SetActorRecording(self, isRecording);
		end

		-- add key frame at recording switch time. 
		self:AddKeyFrame();
	end
	return self.isRecording;
end

function Actor:OnRemove()
	Actor._super.OnRemove(self);
end

function Actor:FrameMoveRecording(deltaTime)
	local curTime = self:GetTime();
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	
	if( not entity.ridingEntity and deltaTime > 0 and self.begin_recording_time) then
		-- only take a key frame every self.auto_record_interval milliseconds. 
		if ((self.begin_recording_time+self.auto_record_interval) > curTime) then
			-- do nothing if we are not at auto recording interval. 
			return;
		else
			self.begin_recording_time = curTime;
		end
	end

	entity:UpdatePosition();
	local x,y,z = entity:GetPosition();

	self:BeginUpdate();
	self:AutoAddKey("lookat_x", curTime, x);
	self:AutoAddKey("lookat_y", curTime, y);
	self:AutoAddKey("lookat_z", curTime, z);

	local eye_dist, eye_liftup, eye_rot_y = ParaCamera.GetEyePos();
	if(eye_dist) then
		self:AutoAddKey("eye_dist", curTime, eye_dist);
		self:AutoAddKey("eye_liftup", curTime, eye_liftup);
		self:AutoAddKey("eye_rot_y", curTime, eye_rot_y);
		self:AutoAddKey("eye_roll", curTime, entity:GetCameraRoll());
	end
	self:AutoAddKey("is_fps", curTime, if_else(CameraController.IsFPSView(), 1,0));

	local has_collision = if_else(self.entity:HasCollision(), 1,0); 
	self:AutoAddKey("has_collision", curTime, has_collision);
	self:EndUpdate();
end

function Actor:IsAllowUserControl()
	local entity = self:GetEntity();
	if(entity) then
		local curTime = self:GetTime();
		return entity:HasFocus() and not self:IsPlayingMode() and self:IsPaused() and 
			-- allow user control when there is no key frames at the end
			-- using OR, we will allow dragging when no key frames. 
			(((self:GetMultiVariable():GetLastTime()+1) <= curTime) or not MovieClipTimeLine.IsDraggingTimeLine());
	end
end
local camera_params = {0,0,0}; -- yaw, pitch, roll
function Actor:FrameMovePlaying(deltaTime)
	local curTime = self:GetTime();
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	
	local eye_dist = self:GetValue("eye_dist", curTime);
	local eye_liftup = self:GetValue("eye_liftup", curTime);
	local eye_rot_y = self:GetValue("eye_rot_y", curTime);
	local eye_roll = self:GetValue("eye_roll", curTime);

	if(self.offset_facing and eye_rot_y) then
		eye_rot_y = eye_rot_y + self.offset_facing;
	end

	local allow_user_control;
	if(entity:HasFocus()) then
		local isBehindLastFrame = ((self:GetMultiVariable():GetLastTime()+1) <= curTime);
		if(isBehindLastFrame) then
			if(not self.isBehindLastFrame) then
				self.isBehindLastFrame = true;
				isBehindLastFrame = false;
			end
		else
			self.isBehindLastFrame = isBehindLastFrame;
		end
		allow_user_control = not self:IsPlayingMode() and isBehindLastFrame;
		if( not allow_user_control ) then
			ParaCamera.SetEyePos(eye_dist, eye_liftup, eye_rot_y);
			self:UpdateFPSView(curTime);
		end
		entity:SetCameraRoll(eye_roll or 0);
		if(isBehindLastFrame) then
			return;
		end
	else
		self.isBehindLastFrame = nil;
	end
	
	local obj = entity:GetInnerObject();
	if(obj) then
		obj:SetFacing(eye_rot_y or 0);
		obj:SetField("HeadUpdownAngle", 0);
		obj:SetField("HeadTurningAngle", 0);
		local nx, ny, nz = mathlib.math3d.vec3Rotate(0, 1, 0, 0, 0, -(eye_liftup or 0))
		nx, ny, nz = mathlib.math3d.vec3Rotate(nx, ny, nz, 0, eye_rot_y or 0, 0)
		obj:SetField("normal", {nx, ny, nz});
	end
	

	if(not allow_user_control) then
		local new_x = self:GetValue("lookat_x", curTime);
		local new_y = self:GetValue("lookat_y", curTime);
		local new_z = self:GetValue("lookat_z", curTime);

		if(new_x and new_y and new_z) then
			if(self.offset_x) then
				new_x = self.offset_x + new_x;
				new_y = self.offset_y + new_y;
				new_z = self.offset_z + new_z;
			end
			
			entity:SetPosition(new_x, new_y, new_z);
			-- due to floating point precision of the view matrix, slowly moved camera may jerk.
			--LOG.std(nil, "debug", "ActorCamera", "x,y,z: %f %f %f", new_x, new_y, new_z);
			--LOG.std(nil, "debug", "ActorCamera", "c pos: %f %f %f", ParaCamera.GetLookAtPos());
		end
	end

	local has_collision = self:GetValue("has_collision", curTime) or 1; 
	-- disable collision if camera is inside a solid block. 
	if(entity:IsInsideObstructedBlock() and not CameraController.HasCameraCollision()) then
		has_collision = false;
	end
	entity:SetCameraCollision(has_collision);

	if(self:IsPlayingMode()) then
		entity:HideCameraModel();
	else
		entity:ShowCameraModel();
	end
end

function Actor:UpdateFPSView(curTime)
	curTime = curTime or self:GetTime();
	local is_fps = self:GetValue("is_fps", curTime) or default_fps_mode; 
	local current_is_fps = if_else(CameraController.IsFPSView(), 1,0);
	if(current_is_fps ~= is_fps) then
		CameraController.ToggleCamera(is_fps == 1);
	end
end

function Actor:SetFocus()
	Actor._super.SetFocus(self);
	self:UpdateFPSView(curTime);
	self:FrameMovePlaying(0);
	-- always begin with nil variable, rather than remember last selection.  
	self:SetCurrentEditVariableIndex(-1);
end

-- select me: for further editing. 
function Actor:SelectMe()
	-- camera actor does not show up anything. 
	
end

-- get the camera settings before SetFocus is called. this usually stores the current player's camera settings
-- before a movie clip is played. we will usually restore the camera settings when camera is reset. 
function Actor:GetRestoreCamSettings()
	local entity = self.entity;
	if(entity) then
		return entity:GetRestoreCamSettings()
	end
end

function Actor:SetRestoreCamSettings(settings)
	local entity = self.entity;
	if(entity) then
		return entity:SetRestoreCamSettings(settings);
	end
end

function Actor:CreateKeyFromUI(keyname, callbackFunc)
	local curTime = self:GetTime();
	local h,m,s = commonlib.timehelp.SecondsToHMS(curTime/1000);
	local strTime = string.format("%.2d:%.2d", m,math.floor(s));
	local old_value = self:GetValue(keyname, curTime);
	if(keyname == nil) then
		-- multi-variable
		local title = format(L"起始时间:%s <br/>lookat_x, lookat_y, lookat_z,<br/>eye_dist, eye_liftup, eye_rot_y", strTime);
		local lookat_x = self:GetValue("lookat_x", curTime);
		local lookat_y = self:GetValue("lookat_y", curTime);
		local lookat_z = self:GetValue("lookat_z", curTime);
		if(not lookat_x) then
			return;
		end
		local eye_dist = self:GetValue("eye_dist", curTime) or 10;
		local eye_liftup = self:GetValue("eye_liftup", curTime) or 0;
		local eye_rot_y = self:GetValue("eye_rot_y", curTime) or 0;

		local old_value = string.format("%f, %f, %f,\n%f, %f, %f", lookat_x,lookat_y,lookat_z,eye_dist,eye_liftup,eye_rot_y);

		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");

				if(vars[1] == lookat_x and vars[2] == lookat_y and vars[3] == lookat_z and
					vars[4] == eye_dist and vars[5] == eye_liftup and vars[6] == eye_rot_y) then
					-- nothing has changed
				elseif(vars[6]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("lookat_x", nil, vars[1]);
					self:AddKeyFrameByName("lookat_y", nil, vars[2]);
					self:AddKeyFrameByName("lookat_z", nil, vars[3]);
					self:AddKeyFrameByName("eye_dist", nil, vars[4]);
					self:AddKeyFrameByName("eye_liftup", nil, vars[5]);
					self:AddKeyFrameByName("eye_rot_y", nil, vars[6]);
					self:EndUpdate();
					self:FrameMovePlaying(0);	
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value,true); 
	elseif(keyname == "pos") then
		local title = format(L"起始时间%s, 请输入位置x,y,z:", strTime);
		old_value = string.format("%f, %f, %f", self:GetValue("lookat_x", curTime) or 0,self:GetValue("lookat_y", curTime) or 0, self:GetValue("lookat_z", curTime) or 0);
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
				if(result and vars[1] and vars[2] and vars[3]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("lookat_x", nil, vars[1]);
					self:AddKeyFrameByName("lookat_y", nil, vars[2]);
					self:AddKeyFrameByName("lookat_z", nil, vars[3]);
					self:EndUpdate();
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end, old_value)
	elseif(keyname == "rot") then
		local title = format(L"起始时间%s, 请输入roll, pitch, yaw (-1.57, 1.57)<br/>", strTime);
		old_value = string.format("%f, %f, %f", self:GetValue("eye_roll", curTime) or 0,self:GetValue("eye_liftup", curTime) or 0,self:GetValue("eye_rot_y", curTime) or 0);
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
				if(result and vars[1] and vars[2] and vars[3]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("eye_roll", nil, vars[1]);
					self:AddKeyFrameByName("eye_liftup", nil, vars[2]);
					self:AddKeyFrameByName("eye_rot_y", nil, vars[3]);
					self:EndUpdate();
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value)
	elseif(keyname == "scaling" or keyname == "eye_dist") then
		local title = format(L"起始时间%s, 请输入放大系数(默认1)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName("eye_dist", nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "static") then
		old_value = {name = self:GetValue("name", 0) or "", isAgent = self:GetValue("isAgent", 0)}
		NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/EditStaticPropertyPage.lua");
		local EditStaticPropertyPage = commonlib.gettable("MyCompany.Aries.Game.Movie.EditStaticPropertyPage");
		EditStaticPropertyPage.ShowPage(function(values)
			if(values.name ~= old_value.name) then
				self:AddKeyFrameByName("name", 0, values.name);
				self:SetDisplayName(values.name)
			end
			if(values.isAgent ~= old_value.isAgent) then
				self:AddKeyFrameByName("isAgent", 0, values.isAgent);
			end
			if(callbackFunc) then
				callbackFunc(true);
			end
		end, old_value, {
			{value="false", text=L"默认"},
			{value="relative", text=L"相对摄影机"},
			{value="searchNearPlayer", text=L"相对主角"},
		});
	end
end

--[[
Title: a single music track on the time line
Author(s): LiXizhi
Date: 2014/10/15
Desc: playing a music file on the time line, dragging the time line will automatically seek to the music file
allowing precise editing between music and 3d scene. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorMusic.lua");
local ActorMusic = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorMusic");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/SelectBlocksTask.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Sound/BackgroundMusic.lua");
local BackgroundMusic = commonlib.gettable("MyCompany.Aries.Game.Sound.BackgroundMusic");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local MovieClip = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieClip");
local MovieManager = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieManager");

local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.Actor"), commonlib.gettable("MyCompany.Aries.Game.Movie.ActorMusic"));

function Actor:ctor()
end

function Actor:Init(itemStack, movieclipEntity, movieclip)
	if(not Actor._super.Init(self, itemStack, movieclipEntity, movieclip)) then
		return;
	end
	
	local timeseries = self.TimeSeries;
	-- location array of movie blocks on the timeline.
	timeseries:CreateVariableIfNotExist("music", "Discrete");

	return self;
end

function Actor:IsKeyFrameOnly()
	return true;
end

-- @return true if recording. 
function Actor:SetRecording(isRecording)
	-- disable recording. 
	return false;
end

-- remove all blocks
function Actor:OnRemove()
	self.last_audio_src = nil;
	self.last_start_time = nil;
	self.last_is_paused = nil;
	self.last_music_time = nil;
end


-- virtual function: display a UI to let the user to edit this keyframe's data. 
-- @param default_value: if nil, it will be the one already on the timeline. {filename, start_time}
function Actor:EditKeyFrame(keyname, time, default_value, callbackFunc)
	local curTime = time or self:GetTime();
	local h,m,s = commonlib.timehelp.SecondsToHMS(curTime/1000);
	local strTime = string.format("%.2d:%.2d", m,math.floor(s));
	local old_value = default_value or self:GetValue(keyname, curTime);
	local old_value_str;
	if(old_value and old_value[1]) then
		if(old_value[1] == "") then
			old_value_str = "";
		else
			old_value_str = string.format("%s %f", old_value[1], old_value[2] or 0);
		end
	end
	local title = format(L"起始时间%s, 请输入文件名与播放位置:<br/>xxx.mp3 [开始时间(单位秒)]", strTime);

	NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/OpenFileDialog.lua");
	local OpenFileDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.OpenFileDialog");
	OpenFileDialog.ShowPage(title, function(result)
		if(result) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Commands/CmdParser.lua");
			local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");
			local cmd_text = result;
			local filename, start_time;
			filename, cmd_text = CmdParser.ParseString(cmd_text);
			filename = filename or "";
			start_time, cmd_text = CmdParser.ParseInt(cmd_text);
			start_time = start_time or 0;

			NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Files.lua");
			local Files = commonlib.gettable("MyCompany.Aries.Game.Common.Files");
			if(filename~="" and not Files.GetWorldFilePath(filename)) then
				_guihelper.MessageBox(format(L"当前世界的目录下没有文件: %s", filename));
			else
				local value = {filename, start_time};
				self:AddKeyFrameByName(keyname, nil, value);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end
	end,old_value_str, L"声音文件", "audio")
end

function Actor:CreateKeyFromUI(keyname, callbackFunc)
	local default_value;
	self:EditKeyFrame(keyname, nil, default_value, callbackFunc);	
end

function Actor:FrameMovePlaying(deltaTime, bIsSelected)
	local curTime = self:GetTime();
	if(not curTime) then
		return
	end
	local music_pos = self:GetValue("music", curTime);
	if(not music_pos) then
		return;
	end
	local filename, start_time = music_pos[1], music_pos[2];

	-- change the current time of the movie block. 
	local var = self:GetVariable("music");
	local fromTime, toTime = var:getTimeRange(1, curTime);
	local firstTime = var:GetFirstTime();

	if(firstTime > curTime) then
		return;
	end
		
	local cur_music = BackgroundMusic:GetCurrentMusic();
	local audio_src = BackgroundMusic:GetMusic(filename);
	if(audio_src) then
		local activeMovieClip = MovieManager:GetActiveMovieClip();
		if( (math.abs(curTime - (self.last_music_time or 0)) > 500) or
			(self.last_audio_src ~= audio_src or self.last_start_time~=start_time) or 
			(deltaTime == 0 and activeMovieClip and activeMovieClip:IsPaused()) or 
			(activeMovieClip and not activeMovieClip:IsPaused() and self.last_is_paused) ) then
			audio_src:stop();
			local local_time = start_time+(curTime-fromTime)/1000;
			audio_src:seek(local_time);
			-- echo({start_time, curTime-fromTime, curTime, fromTime});
			if(cur_music ~= audio_src) then
				BackgroundMusic:SetMusic(audio_src);
			end
			if(activeMovieClip and activeMovieClip:IsPaused()) then
				if(not self.last_is_paused) then
					audio_src:pause();
					self.last_is_paused = true;
				end
			else
				if(self.last_is_paused) then
					self.last_is_paused = nil;
					audio_src:play2d();
				else
					audio_src:play2d();
				end
			end
		end
		self.last_audio_src = audio_src;
		self.last_start_time = start_time;
		self.last_music_time = curTime;
	elseif(filename=="") then
		if(cur_music) then
			BackgroundMusic:Stop();
			self.last_audio_src = nil;
			self.last_start_time = nil;
			self.last_music_time = nil;
			self.last_is_paused = nil;
		end
	end
end

--[[
Title: video recorder
Author(s): LiXizhi
Date: 2014/5/15
Desc: 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/VideoRecorder.lua");
local VideoRecorder = commonlib.gettable("MyCompany.Aries.Game.Movie.VideoRecorder");
VideoRecorder.ToggleRecording();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/VideoRecorderSettings.lua");
local VideoRecorderSettings = commonlib.gettable("MyCompany.Aries.Game.Movie.VideoRecorderSettings");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local BroadcastHelper = commonlib.gettable("CommonCtrl.BroadcastHelper");
local VideoRecorder = commonlib.gettable("MyCompany.Aries.Game.Movie.VideoRecorder");

-- this is the minimum version 
VideoRecorder.MIN_MOVIE_CODEC_PLUGIN_VERSION = 8;

local max_resolution = {4906, 2160};
local default_resolution = {640, 480};
local before_capture_resolution;
function VideoRecorder.ToggleRecording()
	if(ParaMovie.IsRecording()) then
		VideoRecorder.EndCapture();
	else
		VideoRecorder.BeginCapture();
	end
end

function VideoRecorder.OpenOutputDirectory()
	VideoRecorderSettings.OnOpenOutputFolder();
end

function VideoRecorder.GetCurrentVideoFileName()
	return VideoRecorderSettings.GetOutputFilepath(); 
end

function VideoRecorder.HasFFmpegPlugin()
	NPL.load("(gl)script/apps/Aries/Creator/Game/Mod/ModManager.lua");
	local ModManager = commonlib.gettable("Mod.ModManager");
	local plugin = ModManager:GetMod("MovieCodecPlugin");
	if(plugin and plugin:GetVersion() >= VideoRecorder.MIN_MOVIE_CODEC_PLUGIN_VERSION) then
		local attr = ParaMovie.GetAttributeObject();
		return attr:GetField("HasMoviePlugin",false);
	end
end

-- @param callbackFunc: called when started. function(bSucceed) end
function VideoRecorder.BeginCapture(callbackFunc)
	if(VideoRecorder.HasFFmpegPlugin()) then
		VideoRecorderSettings.ShowPage(function(res)
			if(res == "ok") then
				AudioEngine.SetGarbageCollectThreshold(99999);
				VideoRecorder.AdjustWindowResolution(function()
					local start_after_seconds = VideoRecorderSettings.start_after_seconds or 0;
					local elapsed_seconds = 0;
					local mytimer = commonlib.Timer:new({callbackFunc = function(timer)
						
						if(elapsed_seconds >= start_after_seconds) then
							timer:Change();
							BroadcastHelper.PushLabel({id="MovieRecord", label = "", max_duration=0, color = "255 0 0", scaling=1.1, bold=true, shadow=true,});
							GameLogic.options:SetClickToContinue(false);
							local attr = ParaMovie.GetAttributeObject();
							attr:SetField("RecordingFPS", VideoRecorderSettings.GetFPS())
							attr:SetField("VideoBitRate", VideoRecorderSettings.GetVideoBitRate())
							attr:SetField("CaptureAudio", VideoRecorderSettings.IsRecordAudio())
							local margin = VideoRecorderSettings.GetMargin() or 0;
							if(attr:GetField("StereoCaptureMode", 0)~=0) then
								margin = 0;
							elseif(VideoRecorderSettings.GetStereoMode() ~=0) then
								attr:SetField("StereoCaptureMode", VideoRecorderSettings.GetStereoMode());
								margin = 0;
							end
							attr:SetField("MarginLeft", margin);
							attr:SetField("MarginTop", margin);
							attr:SetField("MarginRight", margin);
							attr:SetField("MarginBottom", margin);
							ParaMovie.BeginCapture(VideoRecorderSettings.GetOutputFilepath())
							VideoRecorder.ShowRecordingArea(true);
							if(callbackFunc) then
								callbackFunc(true);
							end
						else
							BroadcastHelper.PushLabel({id="MovieRecord", label = format(L"%d秒后开始录制", start_after_seconds-elapsed_seconds), max_duration=2000, color = "255 0 0", scaling=1.1, bold=true, shadow=true,});
						end
						elapsed_seconds = elapsed_seconds + timer:GetDelta()/1000;
						if(elapsed_seconds >= start_after_seconds) then
							BroadcastHelper.PushLabel({id="MovieRecord", label = "", max_duration=0, color = "255 0 0", scaling=1.1, bold=true, shadow=true,});
						end
					end})
					mytimer:Change(0, 500);
				end)
			else
				if(callbackFunc) then
					callbackFunc(false);
				end
			end
		end);
	else
		_guihelper.MessageBox(L"你没有安装最新版的视频输出插件, 请到官方网站下载安装", function(res)
			if(res and res == _guihelper.DialogResult.Yes) then
				GameLogic.RunCommand("/install -mod https://keepwork.com/wiki/mod/packages/packages_install/paracraft?id=12")
			end
		end, _guihelper.MessageBoxButtons.YesNo);
		if(callbackFunc) then
			callbackFunc(false);
		end
	end
end

function VideoRecorder.FrameCapture()
end

-- adjust window resolution
-- @param callbackFunc: function is called when window size is adjusted. 
function VideoRecorder.AdjustWindowResolution(callbackFunc)
	local att = ParaEngine.GetAttributeObject();
	local cur_resolution = att:GetField("WindowResolution", {400, 300}); 
	local preferred_resolution = VideoRecorderSettings.GetResolution();
	
	-- reserve space in resolution for render borders which indicates whether the screen is being recorded or not
	local margin = VideoRecorderSettings.GetMargin();
	preferred_resolution[1] = preferred_resolution[1] + margin*2;
	preferred_resolution[2] = preferred_resolution[2] + margin*2;
	
	if(cur_resolution[1] > max_resolution[1] or cur_resolution[2] > max_resolution[2]) then
		if(not preferred_resolution or not preferred_resolution[1]) then
			preferred_resolution = max_resolution;
		end
	end

	if(preferred_resolution and preferred_resolution[1]) then
		att:SetField("ScreenResolution", preferred_resolution); 
		att:CallField("UpdateScreenMode");
		before_capture_resolution = cur_resolution;
		local mytimer = commonlib.Timer:new({callbackFunc = function(timer)
			if(callbackFunc) then
				callbackFunc();
			end
		end})
		mytimer:Change(1000, nil);
	else
		local mytimer = commonlib.Timer:new({callbackFunc = function(timer)
			if(callbackFunc) then
				callbackFunc();
			end
		end})
		mytimer:Change(100, nil);
	end
	
	-- restore resolution from margins that reserved for borders
	preferred_resolution[1] = preferred_resolution[1] - margin*2;
	preferred_resolution[2] = preferred_resolution[2] - margin*2;
	VideoRecorderSettings.SetResolution(preferred_resolution);
end

function VideoRecorder.RestoreWindowResolution()
	if(before_capture_resolution) then
		local att = ParaEngine.GetAttributeObject();
		local cur_resolution = att:GetField("ScreenResolution", {400, 300}); 
		if(cur_resolution[1] < before_capture_resolution[1] or cur_resolution[2] < before_capture_resolution[2]) then
			att:SetField("ScreenResolution", before_capture_resolution); 
			att:CallField("UpdateScreenMode");
		end
		before_capture_resolution = nil;
	end
end

function VideoRecorder.EndCapture()
	AudioEngine.SetGarbageCollectThreshold(10);
	ParaMovie.EndCapture();
	VideoRecorder.ShowRecordingArea(false);
	GameLogic.options:SetClickToContinue(true);
	VideoRecorder.RestoreWindowResolution();
end

function VideoRecorder.ShowRecordingArea(bShow)
	if(VideoRecorder.HasFFmpegPlugin()) then
		local _parent = ParaUI.GetUIObject("RecordSafeArea");
		if(not bShow) then
			if(_parent:IsValid()) then
				_parent.visible = false;
				ParaUI.Destroy(_parent.id);
			end
			if(VideoRecorder.title_timer) then
				VideoRecorder.title_timer:Change();
			end
			if(VideoRecorder.last_text) then
				ParaEngine.SetWindowText(VideoRecorder.last_text);
				VideoRecorder.last_text = nil;
			end
			return;
		else
			if(not _parent:IsValid()) then
				local attr = ParaMovie.GetAttributeObject();
				local margin_left, margin_top, margin_right, margin_bottom = attr:GetField("MarginLeft",0), attr:GetField("MarginTop",0), attr:GetField("MarginRight",0), attr:GetField("MarginBottom",0);
				local border_width = 2;
				_parent = ParaUI.CreateUIObject("container", "RecordSafeArea", "_fi", 0,0,0,0);
				_parent.background = "";
				_parent.enabled = false;
				_parent.zorder = 100;
				_parent:AttachToRoot();

				local _border = ParaUI.CreateUIObject("container", "border", "_fi", 0,0,0,0);
				_border.background = "";
				_border.enabled = false;
				_parent:AddChild(_border);

				local _this = ParaUI.CreateUIObject("container", "top", "_mt", 0, 0, 0, margin_top);
				_this.background = "Texture/whitedot.png";
				_this.enabled = false;
				_border:AddChild(_this);

				local _this = ParaUI.CreateUIObject("container", "left", "_ml", 0, margin_top, margin_left, margin_bottom);
				_this.background = "Texture/whitedot.png";
				_this.enabled = false;
				_border:AddChild(_this);

				local _this = ParaUI.CreateUIObject("container", "right", "_mr", 0, margin_top, margin_right, margin_bottom);
				_this.background = "Texture/whitedot.png";
				_this.enabled = false;
				_border:AddChild(_this);
				
				local _this = ParaUI.CreateUIObject("container", "top", "_mb", 0, 0, 0, margin_bottom);
				_this.background = "Texture/whitedot.png";
				_this.enabled = false;
				_border:AddChild(_this);
				
				local _this = ParaUI.CreateUIObject("container", "logo", "_lt", margin_left+20, margin_top+20, 200, 103);
				_this.background = L"Texture/Aries/Creator/Login/ParaCraftMovieWaterMark.png;0 0 200 103";
				_this.enabled = false;
				_parent:AddChild(_this);
			end
			_parent.visible = true;

			local last_text = ParaEngine.GetWindowText();
			local tip_text = L"正在录制中: F9停止";
			if(last_text~=tip_text) then
				VideoRecorder.last_text = last_text;
				ParaEngine.SetWindowText(tip_text);
			end
			VideoRecorder.start_time = ParaGlobal.timeGetTime();
			VideoRecorder.title_timer = VideoRecorder.title_timer or commonlib.Timer:new({callbackFunc = function(timer)
				local elapsed_time = ParaGlobal.timeGetTime() - VideoRecorder.start_time;
				local h,m,s = commonlib.timehelp.SecondsToHMS(elapsed_time/1000);
				local strTime = string.format(L"正在录制中: %02d:%02d (F9停止)", m, math.floor(s));
				ParaEngine.SetWindowText(strTime);
			end})
			VideoRecorder.title_timer:Change(1000,1000);

			_parent:GetChild("logo").visible = VideoRecorderSettings.IsShowLogo();

			local border_cont = _parent:GetChild("border");

			if(ParaMovie.IsRecording()) then
				border_cont.colormask = "255 0 0 192";
				border_cont:ApplyAnim();
			else
				border_cont.colormask = "0 255 0 192";
				border_cont:ApplyAnim();
			end

		end
	end
end

--[[
Title: actor commands
Author(s): LiXizhi
Date: 2014/4/9
Desc: a number of command that is executed on the time line. 
Please note, only movie related command is recommended to use, such that dragging timeline will match the actual output
current supported addkey command is:
	/addkey text [any text]
	/addkey tip [any text]
	/addkey fadein [seconds or 0.5]
	/addkey fadeout [seconds or 0.5]
	/addkey time [number:-1,1]
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorCommands.lua");
local actor = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorCommands");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorGUIText.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorBlocks.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorMovieSequence.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Commands/CommandManager.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorMusic.lua");
local ActorMusic = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorMusic");
local CommandManager = commonlib.gettable("MyCompany.Aries.Game.CommandManager");
local ActorBlocks = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorBlocks");
local ActorGUIText = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorGUIText");
local ActorMovieSequence = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorMovieSequence");
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.Actor"), commonlib.gettable("MyCompany.Aries.Game.Movie.ActorCommands"));

Actor.class_name = "ActorCommands";

function Actor:ctor()
	self.actor_text = ActorGUIText:new();
	self.actor_blocks = ActorBlocks:new();
	self.actor_movie_sequence = ActorMovieSequence:new();
	self.actor_movie_sequence:SetParentActor(self);
	self.actor_music = ActorMusic:new();

	self.actor_text:Connect("keyChanged", self, "keyChanged");
	self.actor_text:Connect("valueChanged", self, "valueChanged");
	self.actor_blocks:Connect("keyChanged", self, "keyChanged");
	self.actor_blocks:Connect("valueChanged", self, "valueChanged");
	self.actor_movie_sequence:Connect("keyChanged", self, "keyChanged");
	self.actor_movie_sequence:Connect("valueChanged", self, "valueChanged");
	self.actor_music:Connect("keyChanged", self, "keyChanged");
	self.actor_music:Connect("valueChanged", self, "valueChanged");
end

function Actor:SetItemStack(itemStack)
	self.actor_text:SetItemStack(itemStack);
	self.actor_blocks:SetItemStack(itemStack);
	self.actor_movie_sequence:SetItemStack(itemStack);
	self.actor_music:SetItemStack(itemStack);
	-- base class must be called last, so that child actors have initialized their own variables on itemStack. 
	Actor._super.SetItemStack(self, itemStack);
end

-- get child actor
-- @param name: "actor_text", "actor_blocks", etc
function Actor:GetChildActor(name)
	return self[name];
end

function Actor:Init(itemStack, movieclipEntity, isReuseActor, newName, movieclip)
	local timeseries = self.TimeSeries;
	self.actor_text:Init(itemStack, movieclipEntity, movieclip);
	self.actor_blocks:Init(itemStack, movieclipEntity, movieclip);
	self.actor_movie_sequence:Init(itemStack, movieclipEntity, movieclip);
	-- background music track1
	self.actor_music:Init(itemStack, movieclipEntity, movieclip);
	-- base class must be called last, so that child actors have created their own variables on itemStack. 
	if(not Actor._super.Init(self, itemStack, movieclipEntity, movieclip)) then
		return;
	end

	timeseries:CreateVariableIfNotExist("cmd", "Discrete");
	timeseries:CreateVariableIfNotExist("tip", "Discrete");
	-- time of day
	timeseries:CreateVariableIfNotExist("time", "Linear"); 
	return self;
end

-- get display name
function Actor:GetDisplayName()
	return L"全局";
end

local selectable_var_list = {"text", "time", "blocks", "cmd", "movieblock", "music"};

-- @return nil or a table of variable list. 
function Actor:GetEditableVariableList()
	return selectable_var_list;
end

-- @param selected_index: if nil,  default to current index
-- @return var
function Actor:GetEditableVariable(selected_index)
	selected_index = selected_index or self:GetCurrentEditVariableIndex();
	return self.TimeSeries:GetVariable(selectable_var_list[selected_index]);
end

function Actor:IsKeyFrameOnly()
	return true;
end

-- @return true if recording. 
function Actor:SetRecording(isRecording)
	-- disable recording camera. 
	return false
end

-- the same command can only be played once. 
function Actor:PlayCmd(curTime)
	local cmd = self:GetValue("cmd", curTime, true);
	if(cmd) then
		if(self.last_cmd~=cmd) then
			self.last_cmd = cmd;
			CommandManager:RunText(cmd, self:GetMovieClipEntity());
		end
	end
end

function Actor:PlayTip(curTime)
	-- local tip = self:GetValue("tip", curTime);
end

-- day time. 
function Actor:PlayTime(curTime)
	local time = self:GetValue("time", curTime, true);
	if(time) then
		ParaScene.SetTimeOfDaySTD(time);
		GameLogic.GetSim():OnTickDayLight();
	end
end

-- add movie text at the current time. 
function Actor:AddKeyFrameOfText(text)
	self.actor_text:AddKeyFrameOfText(text)
end

-- add movie text at the current time. 
function Actor:AddKeyFrameOfTime(time)
	if(type(time) == "number") then
		self:AddKeyFrameByName("time", nil, time);
	end
end

-- let the user to create a key and add to current timeline 
function Actor:CreateKeyFromUI(keyname, callbackFunc)
	local curTime = self:GetTime();
	local h,m,s = commonlib.timehelp.SecondsToHMS(curTime/1000);
	local strTime = string.format("%.2d:%.2d", m,math.floor(s));
	local old_value = self:GetValue(keyname, curTime);

	if(keyname == "text") then
		self.actor_text:CreateKeyFromUI(keyname, callbackFunc);
	elseif(keyname == "movieblock") then
		self.actor_movie_sequence:CreateKeyFromUI(keyname, callbackFunc);
	elseif(keyname == "music") then
		self.actor_music:CreateKeyFromUI(keyname, callbackFunc);
	elseif(keyname == "time") then
		local title = format(L"起始时间%s, 请输入时间[-1,1]", strTime);
		old_value = ParaScene.GetTimeOfDaySTD();
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value);
	elseif(keyname == "blocks") then
		self.actor_blocks:AddKeyFrameOfSelectedBlocks();
		if(callbackFunc) then
			callbackFunc(true);
		end
	elseif(keyname == "cmd") then
		local title = format(L"起始时间%s, 请输入命令行(/)", strTime);
		if(old_value) then
			old_value = old_value:gsub(";/", "\n/");
		end
		-- TODO: use a dedicated UI 
		-- show as multiline text input box. 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="" and result:match("^/")) then
				result=result:gsub("[\r\n]+/", ";/");
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value,true); 
	end
end

-- virtual function: display a UI to let the user to edit this keyframe's data. 
function Actor:EditKeyFrame(keyname, time)
	time = time or self:GetTime();
	local old_value = self:GetValue(keyname, time);
	if(old_value) then
		if(keyname == "text") then
			self.actor_text:EditKeyFrame(keyname, time)
		elseif(keyname == "blocks") then
			self.actor_blocks:EditKeyFrame(keyname, time)
		elseif(keyname == "movieblock") then
			self.actor_movie_sequence:EditKeyFrame(keyname, time)
		elseif(keyname == "music") then
			self.actor_music:EditKeyFrame(keyname, time)
		elseif(keyname == "time") then
			-- TODO: edit the key and set back
			-- _guihelper.MessageBox(old_value);
		end
	end
end

-- remove GUI text
function Actor:OnRemove()
	self.actor_text:OnRemove();
	self.actor_blocks:OnRemove();
	self.actor_movie_sequence:OnRemove();
	self.actor_music:OnRemove();

	Actor._super.OnRemove(self);
end

function Actor:FrameMovePlaying(deltaTime, bIsSelected)
	local curTime = self:GetTime();
	if(not curTime) then
		return
	end
	self.actor_text:FrameMovePlaying(deltaTime, bIsSelected)
	self.actor_blocks:FrameMovePlaying(deltaTime, bIsSelected);
	self.actor_movie_sequence:FrameMovePlaying(deltaTime, bIsSelected);
	self.actor_music:FrameMovePlaying(deltaTime, bIsSelected);

	self:PlayCmd(curTime);
	self:PlayTip(curTime);
	self:PlayTime(curTime);
end

--[[
Title: mob entity actor
Author(s): LiXizhi
Date: 2014/3/30
Desc: for recording and playing back of mob and NPC
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorNPC.lua");
local ActorNPC = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorNPC");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/Actor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorBlock.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Entity/PlayerAssetFile.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/MultiAnimBlock.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Commands/CmdParser.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/BonesVariable.lua");
NPL.load("(gl)script/ide/math/Quaternion.lua");
local Matrix4 = commonlib.gettable("mathlib.Matrix4");
local Quaternion = commonlib.gettable("mathlib.Quaternion");
local math3d = commonlib.gettable("mathlib.math3d");
local BonesVariable = commonlib.gettable("MyCompany.Aries.Game.Movie.BonesVariable");
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");
local MultiAnimBlock = commonlib.gettable("MyCompany.Aries.Game.Common.MultiAnimBlock");
local PlayerAssetFile = commonlib.gettable("MyCompany.Aries.Game.EntityManager.PlayerAssetFile")
local ActorBlock = commonlib.gettable("MyCompany.Aries.Game.Movie.ActorBlock");
local EntityNPC = commonlib.gettable("MyCompany.Aries.Game.EntityManager.EntityNPC")
local SlashCommand = commonlib.gettable("MyCompany.Aries.SlashCommand.SlashCommand");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");


local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.Actor"), commonlib.gettable("MyCompany.Aries.Game.Movie.ActorNPC"));

Actor.class_name = "ActorNPC";
Actor:Property({"entityClass", "EntityNPC"});
Actor:Property({"offset_facing", nil, "GetOffsetFacing", "SetOffsetFacing", auto=true});
-- asset file is changed
Actor:Signal("assetfileChanged");

-- recommended to set to true to use script to calculate pose for each frame precisely. 
local animate_by_script = true;
			

-- keyframes that can be edited from UI keyframe. 
local selectable_var_list = {
	"anim", "bones", "assetfile", "skin", "blockinhand",
	"pos", -- multiple of x,y,z
	"facing", 
	"rot", -- multiple of "roll", "pitch", "facing"
	"head", -- multiple of "HeadUpdownAngle", "HeadTurningAngle"
	"scaling", "speedscale", "gravity", "opacity", "blocks", "parent", 
	"static", -- multiple of "name" and "isAgent"
};


function Actor:ctor()
	self.actor_block = ActorBlock:new();
end

function Actor:DeleteThisActor()
	self:OnRemove();
	self:Destroy();
end

function Actor:GetMultiVariable()
	local var = self:GetCustomVariable("multi_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new();
		var:AddVariable(self:GetVariable("x"));
		var:AddVariable(self:GetVariable("y"));
		var:AddVariable(self:GetVariable("z"));
		var:AddVariable(self:GetVariable("facing")); -- facing is yaw, actually
		var:AddVariable(self:GetVariable("pitch"));
		var:AddVariable(self:GetVariable("roll"));
		var:AddVariable(self:GetVariable("anim"));
		var:AddVariable(self:GetVariable("skin"));
		var:AddVariable(self:GetVariable("blockinhand"));
		var:AddVariable(self:GetVariable("assetfile"));
		var:AddVariable(self:GetVariable("scaling"));
		self:SetCustomVariable("multi_variable", var);
		return var;
	end
end

-- get rotate multi variable
function Actor:GetStaticVariable()
	local var = self:GetCustomVariable("static_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="static"});
		var:AddVariable(self:GetVariable("name"));
		var:AddVariable(self:GetVariable("isAgent"));
		self:SetCustomVariable("static_variable", var);
		return var;
	end
end

-- get position multi variable
function Actor:GetPosVariable()
	local var = self:GetCustomVariable("pos_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="pos"});
		var:AddVariable(self:GetVariable("x"));
		var:AddVariable(self:GetVariable("y"));
		var:AddVariable(self:GetVariable("z"));
		self:SetCustomVariable("pos_variable", var);
		return var;
	end
end

-- get rotate multi variable
function Actor:GetRotateVariable()
	local var = self:GetCustomVariable("rot_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="rot"});
		var:AddVariable(self:GetVariable("roll"));
		var:AddVariable(self:GetVariable("pitch"));
		var:AddVariable(self:GetVariable("facing"));
		self:SetCustomVariable("rot_variable", var);
		return var;
	end
end

function Actor:GetBlocksVariable()
	return self.actor_block.blocks;
end

-- get position multi variable
function Actor:GetHeadVariable()
	local var = self:GetCustomVariable("head_variable");
	if(var) then
		return var;
	else
		var = MultiAnimBlock:new({name="head"});
		var:AddVariable(self:GetVariable("HeadTurningAngle"));
		var:AddVariable(self:GetVariable("HeadUpdownAngle"));
		self:SetCustomVariable("head_variable", var);
		return var;
	end
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

function Actor:GetSelectionName()
	local name = self:GetDisplayName() or "";
	local var = self:GetEditableVariable();

	if(var) then
		name = format("%s::%s", name, var.name);
		if(var.name == "bones") then
			local bone_name = var:GetSelectedBoneName();
			if(bone_name) then
				name = format("%s::%s", name, bone_name);
			else
				name = format("%s::[all]", name);
			end
		end
	end
	return name;
end

function Actor:GetBonesVariable()
	if(not self.bones_variable) then
		self.bones_variable = BonesVariable:new():init(self);
		self:Connect("dataSourceChanged", self.bones_variable, self.bones_variable.LoadFromActor)
		self:Connect("assetfileChanged", self.bones_variable, self.bones_variable.OnAssetFileChanged)
	end
	return self.bones_variable;
end

-- @param isReuseActor: whether we will reuse actor in the scene with the same name instead of creating a new entity. default to false.
-- @param newName: if not provided, it will use the name in itemStack
function Actor:Init(itemStack, movieclipEntity, isReuseActor, newName, movieclip)
	self.actor_block:Init(itemStack, movieclipEntity);
	-- base class must be called last, so that child actors have created their own variables on itemStack. 
	if(not Actor._super.Init(self, itemStack, movieclipEntity, movieclip)) then
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
	timeseries:CreateVariableIfNotExist("gravity", "Discrete");
	timeseries:CreateVariableIfNotExist("scaling", "Linear");
	timeseries:CreateVariableIfNotExist("name", "Discrete");
	timeseries:CreateVariableIfNotExist("isAgent", "Discrete"); -- true, nil|false, "relative", "searchNearPlayer"
	timeseries:CreateVariableIfNotExist("skin", "Discrete");
	timeseries:CreateVariableIfNotExist("blockinhand", "Discrete");
	timeseries:CreateVariableIfNotExist("opacity", "Linear");
	timeseries:CreateVariableIfNotExist("parent", "LinearTable");
	
	self:AddValue("position", self.GetPosVariable);

	-- get initial position from itemStack, if not exist, we will use movie clip entity's block position. 
	local movieClip = self:GetMovieClip();
	if(movieClip) then
		local x, y, z = self:CheckSetDefaultPosition();

		local HeadUpdownAngle, HeadTurningAngle, anim, facing,skin, opacity, name;
		HeadUpdownAngle = self:GetValue("HeadUpdownAngle", 0);
		HeadTurningAngle = self:GetValue("HeadTurningAngle", 0);
		anim = self:GetValue("anim", 0);
		facing = self:GetValue("facing", 0);
		skin = self:GetValue("skin", 0);
		opacity = self:GetValue("opacity", 0);
		name = newName or self:GetValue("name", 0);
		local isAgent = self:GetValue("isAgent", 0);
		if(isReuseActor == nil) then
			isReuseActor = isAgent
		end

		if((isReuseActor or isAgent) and name and name~="") then
			local entity;
			local offsetFacing;
			if(name == "player") then
				entity = EntityManager.GetPlayer();
			else
				if(isReuseActor == "searchNearPlayer") then
					local playerActor = movieClip:FindActor("player");
					if(playerActor) then	
						-- if the movie clip already contains a player, we will use it to locate the entity
						local x, y, z = playerActor:TransformToEntityPosition(x, y, z)
						local bx, by, bz = BlockEngine:block(x, y+0.1, z);
						local r = 1;
						local entities = EntityManager.GetEntitiesByMinMax(bx-r, by-r, bz-r, bx+r, by+r, bz+r)
						if(entities and #entities>0) then
							-- tricky: we will match either name or assetfile 
							local assetfile = self:GetValue("assetfile", 0);
							for i, entity_ in ipairs(entities) do
								if(entity_:GetName() == name) then
									entity = entity_;
									break;
								elseif(entity_.GetModelFile and entity_:GetModelFile() == assetfile) then
									entity = entity_;
									break;
								end
							end
						end
						if (entity) then
							-- tricky: always use relative facing of the nearby player actor
							offsetFacing = playerActor:GetOffsetFacing()
						end
					else
						-- search near the current player
						local x, y, z = EntityManager.GetPlayer():GetBlockPos()
						local r = 5;
						local entities = EntityManager.FindEntities({name = name, x=x,  y=y, z=z, r=r})
						if(entities and #entities>0) then
							entity = entities[1];
							if(entity and not entity.SetActor) then
								entity = nil;
							end
						end
					end
				end
				if(not entity) then
					entity = EntityManager.GetEntity(name);
					if(entity and not entity.SetActor) then
						entity = nil;
					end
				end
			end
			if(isAgent and isReuseActor==false and (not newName) and entity) then
				-- tricky: we still need to reuse actor, even if isReuseActor == false under above conditions
				isReuseActor = true;
			end

			if(isReuseActor and entity) then
				self:BecomeAgent(entity);
				if(isReuseActor == "relative" or isReuseActor == "searchNearPlayer") then
					self:CalculateRelativeParams();
					if(offsetFacing) then
						self:SetOffsetFacing(offsetFacing);
					end
				end
			end
		end
		if(not self.entity) then
			self.entity = EntityManager[self.entityClass]:Create({name=name, x=x,y=y,z=z, facing=facing, 
				opacity = opacity, item_id = block_types.names.TimeSeriesNPC, 
			});	
		end
		
		if(self.entity and not self:IsAgent()) then
			self.entity:SetActor(self);
			self.entity:SetPersistent(false);
			self.entity:SetDummy(true);
			if(skin) then
				self.entity:SetSkin(skin);
			end
			self.entity:SetCanRandomMove(false);
			self.entity:SetDisplayName(name);
			self.entity:EnableAnimation(not animate_by_script);
			-- self.entity:EnableLOD(false);
			self.entity:Attach();
			self:CheckLoadBonesAnims();

			if(isReuseActor) then
				-- just incase the reused actor is not found, we will create a new one and become an agent of it. 
				self:BecomeAgent(self.entity);
			end
		end
		return self;
	end
end

-- from data source coordinate to entity coordinate according to CalculateRelativeParams()
function Actor:TransformToEntityPosition(x, y, z)
	x = x + (self.offset_x or 0);
	y = y + (self.offset_y or 0);
	z = z + (self.offset_z or 0);
	
	if((self.offset_facing or 0) ~= 0) then
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

function Actor:IsAgentRelative()
	return self.origin_x~=nil;
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

-- set the default position
-- @param bUseCurrentPosition: true to use the current entity's position. false or nil to use the entaining movie block's position.
-- @return x,y,z at time 0
function Actor:CheckSetDefaultPosition(bUseCurrentPosition)
	local x = self:GetValue("x", 0);
	local y = self:GetValue("y", 0);
	local z = self:GetValue("z", 0);
	if(not x or not y or not z) then
		if(bUseCurrentPosition) then
			x,y,z = self.entity:GetPosition();
		else
			local movieClip = self:GetMovieClip();
			if(movieClip) then
				x, y, z = movieClip:GetOrigin();
				y = y + BlockEngine.blocksize;
			end
		end
		if(x) then
			self:AddKey("x", 0, x);
			self:AddKey("y", 0, y);
			self:AddKey("z", 0, z);
		end
	end
	return x,y,z;
end

function Actor:OnRemove()
	self.actor_block:OnRemove();
	
	Actor._super.OnRemove(self);
end

function Actor:SetItemStack(itemStack)
	self.actor_block:SetItemStack(itemStack);
	-- base class must be called last, so that child actors have initialized their own variables on itemStack. 
	Actor._super.SetItemStack(self, itemStack);
end

-- @return nil or a table of variable list. 
function Actor:GetEditableVariableList()
	return selectable_var_list;
end

-- @param selected_index: if nil,  default to current index
-- @return var
function Actor:GetEditableVariable(selected_index)
	selected_index = selected_index or self:GetCurrentEditVariableIndex();
	
	local name = selectable_var_list[selected_index];
	local var;
	if(name == "pos") then
		var = self:GetPosVariable();
	elseif(name == "rot") then
		var = self:GetRotateVariable();
	elseif(name == "head") then
		var = self:GetHeadVariable();
	elseif(name == "bones") then
		var = self:GetBonesVariable();
	elseif(name == "blocks") then
		var = self:GetBlocksVariable();
	elseif(name == "static") then
		var = self:GetStaticVariable();
	else
		var = self.TimeSeries:GetVariable(name);
	end
	return var;
end

function Actor:CreateKeyFromUI(keyname, callbackFunc)
	local curTime = self:GetTime();
	local h,m,s = commonlib.timehelp.SecondsToHMS(curTime/1000);
	local strTime = string.format("%.2d:%.2d", m,math.floor(s));
	local old_value = self:GetValue(keyname, curTime);

	if(keyname == "anim") then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Effects/EntityAnimation.lua");
		local EntityAnimation = commonlib.gettable("MyCompany.Aries.Game.Effects.EntityAnimation");
			
		-- get {{value, text}} array of all animations in the asset file. 
		local options = {};
		local assetfile = self:GetValue("assetfile", curTime);
		if(assetfile) then
			assetfile = PlayerAssetFile:GetFilenameByName(assetfile)
			NPL.load("(gl)script/ide/System/Scene/Assets/ParaXModelAttr.lua");
			local ParaXModelAttr = commonlib.gettable("System.Scene.Assets.ParaXModelAttr");
			local attr = ParaXModelAttr:new():initFromAssetFile(assetfile);
			local animations = attr:GetAnimations()
			if(animations) then
				for _, anim in ipairs(animations) do
					if(anim.animID) then
						options[#options+1] = {value = anim.animID, text = EntityAnimation.GetAnimTextByID(anim.animID)}
					end
				end
				table.sort(options, function(a, b)
					return a.value < b.value;
				end)
			end
			if(assetfile:match("%.bmax$")) then
				-- we will add some more default values
				local hasAnims = {};
				for _, option in ipairs(options) do
					hasAnims[option.value] = true;
				end
				local default_anim_placeholders = {0,4,5,13, 37,38,39,41,42,43,44,45,91,135,153, 154, 155, 156,}
				for _, animId in ipairs(default_anim_placeholders) do
					if(not hasAnims[animId]) then
						options[#options+1] = {value = animId, text = EntityAnimation.GetAnimTextByID(animId)};
					end
				end
			end
		end
		
		local title = format(L"起始时间%s, 请输入动画ID或名称:", strTime);

		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result ~= "") then
				result = EntityAnimation.CreateGetAnimId(result);	
				if( type(result) == "number") then
					self:AddKeyFrameByName(keyname, nil, result);
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value, "select", options);

	elseif(keyname == "assetfile") then
		local title = format(L"起始时间%s, 请输入模型路经或名称(默认default)", strTime);

		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/OpenAssetFileDialog.lua");
		local OpenAssetFileDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.OpenAssetFileDialog");
		OpenAssetFileDialog.ShowPage(title, function(result)
			if(result) then
				local filepath = PlayerAssetFile:GetValidAssetByString(result);
				if(filepath or result=="0" or result=="") then
					-- PlayerAssetFile:GetNameByFilename(filename)
					self:AddKeyFrameByName(keyname, nil, result);
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
						return
					end
				end
			end
			if(callbackFunc) then
				callbackFunc(false);
			end
		end, old_value, L"选择模型文件", "model");

	elseif(keyname == "blockinhand") then
		local title = format(L"起始时间%s, 请输入手持物品ID(空为0)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "skin") then
		local title = format(L"起始时间%s, 请输入皮肤ID或名称", strTime);

		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/OpenFileDialog.lua");
		local OpenFileDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.OpenFileDialog");
		OpenFileDialog.ShowPage(title, function(result)
			if(result and result~="") then
				if(result:match("^%d+$")) then
					NPL.load("(gl)script/apps/Aries/Creator/Game/Entity/PlayerSkins.lua");
					local PlayerSkins = commonlib.gettable("MyCompany.Aries.Game.EntityManager.PlayerSkins");
					result = PlayerSkins:GetSkinByString(result);
				end
				-- trim strings
				result = result:gsub("%s+$", "")
				result = result:gsub("^%s+", "")
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value, L"贴图文件", "texture");

	elseif(keyname == "scaling") then
		local title = format(L"起始时间%s, 请输入放大系数(默认1)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "opacity") then
		local title = format(L"起始时间%s, 请输入透明度[0,1](默认1)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result and result>=0 and result<=1) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "facing" or keyname == "HeadUpdownAngle" or keyname=="HeadTurningAngle") then
		local title;
		if(keyname == "facing") then
			title = format(L"起始时间%s, 请输入转身的角度(-3.14, 3.14)", strTime);
		elseif(keyname == "HeadUpdownAngle") then
			title = format(L"起始时间%s, 请输入头部上下运动的角度(-1.57, 1.57)", strTime);
		elseif(keyname == "HeadTurningAngle") then
			title = format(L"起始时间%s, 请输入头部左右运动的角度(-1.57, 1.57)", strTime);
		end

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "head") then
		local title = format(L"起始时间%s, 请输入头部角度(-1.57, 1.57)<br/>左右角度, 上下角度:", strTime);
		old_value = string.format("%f, %f", self:GetValue("HeadTurningAngle", curTime) or 0,self:GetValue("HeadUpdownAngle", curTime) or 0);
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
				if(result and vars[1] and vars[2]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("HeadTurningAngle", nil, vars[1]);
					self:AddKeyFrameByName("HeadUpdownAngle", nil, vars[2]);
					self:EndUpdate();
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value)
	elseif(keyname == "rot") then
		local title = format(L"起始时间%s, 请输入roll, pitch, yaw (-1.57, 1.57)<br/>", strTime);
		old_value = string.format("%f, %f, %f", self:GetValue("roll", curTime) or 0,self:GetValue("pitch", curTime) or 0,self:GetValue("facing", curTime) or 0);
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
				if(result and vars[1] and vars[2] and vars[3]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("roll", nil, vars[1]);
					self:AddKeyFrameByName("pitch", nil, vars[2]);
					self:AddKeyFrameByName("facing", nil, vars[3]);
					self:EndUpdate();
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value)
	elseif(keyname == "pos") then
		local title = format(L"起始时间%s, 请输入位置x,y,z:", strTime);
		old_value = string.format("%f, %f, %f", self:GetValue("x", curTime) or 0,self:GetValue("y", curTime) or 0, self:GetValue("z", curTime) or 0);
		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			if(result and result~="") then
				local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
				if(result and vars[1] and vars[2] and vars[3]) then
					self:BeginUpdate();
					self:AddKeyFrameByName("x", nil, vars[1]);
					self:AddKeyFrameByName("y", nil, vars[2]);
					self:AddKeyFrameByName("z", nil, vars[3]);
					self:EndUpdate();
					self:FrameMovePlaying(0);
					if(callbackFunc) then
						callbackFunc(true);
					end
				end
			end
		end,old_value)
	elseif(keyname == "gravity") then
		local title = format(L"起始时间%s, 请输入重力加速度(默认18.36)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "speedscale") then
		local title = format(L"起始时间%s, 请输入运动速度系数(默认1)", strTime);

		-- TODO: use a dedicated UI 
		NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
		local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
		EnterTextDialog.ShowPage(title, function(result)
			result = tonumber(result);
			if(result) then
				self:AddKeyFrameByName(keyname, nil, result);
				self:FrameMovePlaying(0);
				if(callbackFunc) then
					callbackFunc(true);
				end
			end
		end,old_value)
	elseif(keyname == "bones") then
		local var = self:GetBonesVariable();
		if(var) then
			local bone = var:GetSelectedBone();
			if(bone) then
				local rotVarCpp = bone:GetVariable(1);
				local rotVar = rotVarCpp:CreateGetTimeVar();
				local quat = rotVar:getValue(1, curTime);
				if(quat) then
					local yaw, roll, pitch = Quaternion.ToEulerAngles(quat) 
					local title = format(L"起始时间%s, 请输入roll, pitch, yaw (-1.57, 1.57)<br/>", strTime);
					old_value = string.format("%f, %f, %f", roll or 0,pitch or 0,yaw or 0);
					-- TODO: use a dedicated UI 
					NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/EnterTextDialog.lua");
					local EnterTextDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.EnterTextDialog");
					EnterTextDialog.ShowPage(title, function(result)
						if(result and result~="") then
							local vars = CmdParser.ParseNumberList(result, nil, "|,%s");
							if(result and vars[1] and vars[2] and vars[3]) then
								self:BeginUpdate();
								roll, pitch, yaw  = vars[1], vars[2], vars[3];
								self:BeginModify();
								quat = Quaternion.FromEulerAngles(quat, yaw, roll, pitch);
								rotVarCpp:LoadFromTimeVar();
								self:SetModified();
								self:EndModify();
								self:EndUpdate();
								self:FrameMovePlaying(0);
								if(callbackFunc) then
									callbackFunc(true);
								end
							end
						end
					end,old_value)
				end
			end
		end
	elseif(keyname == "parent") then
		NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/EditParentLinkPage.lua");
		local EditParentLinkPage = commonlib.gettable("MyCompany.Aries.Game.Movie.EditParentLinkPage");
		EditParentLinkPage.ShowPage(strTime, self, function(values)
			if(values.target=="") then
				-- this will automatically add a key frame, when link is removed. 
				self:KeyTransform();
			end
			self:AddKeyFrameByName(keyname, nil, values);
			self:FrameMovePlaying(0);
			if(target~="") then
				-- this will automatically add a key frame at the position. 
				self:KeyTransform();
			end
			if(callbackFunc) then
				callbackFunc(true);
			end
		end, old_value);
	elseif(keyname == "static") then
		old_value = {name = self:GetValue("name", 0) or "", isAgent = self:GetValue("isAgent", 0)}
		NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/EditStaticPropertyPage.lua");
		local EditStaticPropertyPage = commonlib.gettable("MyCompany.Aries.Game.Movie.EditStaticPropertyPage");
		EditStaticPropertyPage.ShowPage(function(values)
			if(values.name ~= old_value.name) then
				self:AddKeyFrameByName("name", 0, values.name);
				self:SetDisplayName(values.name)
			end
			if(values.isAgent ~= old_value.isAgent) then
				self:AddKeyFrameByName("isAgent", 0, values.isAgent);
			end
			if(callbackFunc) then
				callbackFunc(true);
			end
		end, old_value);
	end
end


-- clear all record to a given time. if curTime is nil, it will use the current time. 
function Actor:ClearRecordToTime(curTime)
	-- trim all keys to current time
	local curTime = curTime or self:GetTime();

	Actor._super.ClearRecordToTime(self, curTime);
	self.actor_block:ClearRecordToTime(curTime);
end

function Actor:SetControllable(bIsControllable)
	local entity = self:GetEntity()
	if(entity) then
		local obj = entity:GetInnerObject();
		if(obj) then
			obj:SetField("IsControlledExternally", not bIsControllable);
			obj:SetField("EnableAnim", not animate_by_script or bIsControllable);
		end
	end
end

-- whether the actor can create blocks. The camera actor can not create blocks
function Actor:CanCreateBlocks()
	return true;
end

-- this function is called whenver the create block task is called. i.e. the user has just created some block
function Actor:OnCreateBlocks(blocks)
	if(self:IsRecording())then
		self.actor_block:AddKeyFrameOfBlocks(blocks);
	end
end

-- this function is called whenver the destroy block task is called. i.e. the user has just destroyed some blocks
function Actor:OnDestroyBlocks(blocks)
	if(self:IsRecording())then
		self.actor_block:AddKeyFrameOfBlocks(blocks);
	end
end

function Actor:SaveStaticAppearance()
	local curTime = 0;
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	
	self:BeginUpdate();

	local obj = entity:GetInnerObject();
	if(obj) then
		local assetfile = obj:GetPrimaryAsset():GetKeyName();
		self:AutoAddKey("assetfile", curTime, PlayerAssetFile:GetNameByFilename(assetfile));
	end
	local skin = entity:GetSkin();
	if(skin) then
		self:AutoAddKey("skin", curTime, skin);
	end

	-- name property can not be animated and only save/replace the name key at frame 0. 
	local displayname = entity:GetDisplayName();
	if(displayname and displayname~="") then
		self:AddKey("name", 0, displayname);
		self:GetItemStack():SetTooltip(displayname);
	end

	self:EndUpdate();
end

-- force adding current values to all transform variables, these include position and rotation.
function Actor:KeyTransform()
	local curTime = self:GetTime();
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	entity:UpdatePosition();
	local x,y,z = entity:GetPosition();
	self:BeginUpdate();

	self:AutoAddKey("x", curTime, x);
	self:AutoAddKey("y", curTime, y);
	self:AutoAddKey("z", curTime, z);

	local obj = entity:GetInnerObject();

	if(obj) then
		local yaw = obj:GetField("yaw", 0);
		self:AutoAddKey("facing", curTime, yaw);
		local roll = obj:GetField("roll", 0);
		self:AutoAddKey("roll", curTime, roll);
		local pitch = obj:GetField("pitch", 0);
		self:AutoAddKey("pitch", curTime, pitch);
	end
	self:EndUpdate();
end

function Actor:FrameMoveRecording(deltaTime)
	local curTime = self:GetTime();
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	entity:UpdatePosition();
	local x,y,z = entity:GetPosition();
	local skin = entity:GetSkin();
	
	self:BeginUpdate();

	self:AutoAddKey("x", curTime, x);
	self:AutoAddKey("y", curTime, y);
	self:AutoAddKey("z", curTime, z);
	if(skin) then
		self:AutoAddKey("skin", curTime, skin);
	end
	
	local obj = entity:GetInnerObject();

	if(obj) then
		obj:SetField("IsControlledExternally", false);
		obj:SetField("EnableAnim", true);

		local yaw = obj:GetField("yaw", 0);
		self:AutoAddKey("facing", curTime, yaw);
		local roll = obj:GetField("roll", 0);
		self:AutoAddKey("roll", curTime, roll);
		local pitch = obj:GetField("pitch", 0);
		self:AutoAddKey("pitch", curTime, pitch);
		local scaling = obj:GetScale();
		self:AutoAddKey("scaling", curTime, scaling);

		local anim = obj:GetField("AnimID", 0);
		if(anim > 1000) then
			anim = 0;
		end
		self:AutoAddKey("anim", curTime, anim);

		local HeadUpdownAngle = obj:GetField("HeadUpdownAngle", 0);
		self:AutoAddKey("HeadUpdownAngle", curTime, HeadUpdownAngle);

		local HeadTurningAngle = obj:GetField("HeadTurningAngle", 0);
		self:AutoAddKey("HeadTurningAngle", curTime, HeadTurningAngle);

		local speedscale = entity:GetSpeedScale();
		self:AutoAddKey("speedscale", curTime, speedscale);

		local gravity = obj:GetField("Gravity", 9.18);
		self:AutoAddKey("gravity", curTime, gravity);

		local blockinhand = entity:GetBlockInRightHand();
		self:AutoAddKey("blockinhand", curTime, blockinhand or 0);

		local assetfile = obj:GetPrimaryAsset():GetKeyName();
		self:AutoAddKey("assetfile", curTime, PlayerAssetFile:GetNameByFilename(assetfile));
	end
	self:EndUpdate();
end

-- return the parent link and parent actor if found.
-- @return parent, curTime, parentActor, keypath: where parent contains local transform relative to target:
--  in the form {target="fullname", pos={}, rot={}, use_rot=true}
function Actor:GetParentLink(curTime)
	curTime = curTime or self:GetTime();
	local parent = self:GetValue("parent", curTime);
	if(parent and type(parent) == "table" and parent.target and parent.target ~="")then
		-- animate linking to another actor's bone animation. 
		local actorname, keypath = parent.target:match("^([^:]+):*(.*)"); 
		if(actorname) then
			local parentActor = self:FindActor(actorname);
			if(parentActor and parentActor~=self) then
				return parent, curTime, parentActor, keypath;
			end
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

-- in world coordinate system
-- @param boneName: name of the bone. if nil or "", it is the current actor's root position
-- @return x,y,z, roll, pitch yaw, scale: in world space.  
function Actor:ComputeBoneWorldTransform(bonename, bUseParentRotation)
	local link_x, link_y, link_z = self:GetEntity():GetPosition();
	if(bonename and bonename~="") then
		local bFoundTarget;
		self.parentPivot = self.parentPivot or mathlib.vector3d:new();
						
		local parentBoneRotMat;
		local bones = self:GetBonesVariable();
		local boneVar = bones:GetChild(bonename);
		if(boneVar) then
			self:UpdateAnimInstance();
			local pivot = boneVar:GetPivot(true);
			self.parentPivot:set(pivot);
			if(bUseParentRotation) then
				parentBoneRotMat = boneVar:GetPivotRotation(true);
			end
			bFoundTarget = true;
		end
		if(bFoundTarget) then
			local parentObj = self:GetEntity():GetInnerObject();
			local parentScale = parentObj:GetScale() or 1;
			local dx,dy,dz = 0,0,0;
			if(not bUseParentRotation and localPos) then
				self.parentPivot:add((localPos[1] or 0), (localPos[2] or 0), (localPos[3] or 0));
			end

			self.parentTrans = self.parentTrans or mathlib.Matrix4:new();
			self.parentTrans = parentObj:GetField("LocalTransform", self.parentTrans);
			self.parentPivot:multiplyInPlace(self.parentTrans);
			self.parentQuat = self.parentQuat or mathlib.Quaternion:new();
			if(parentScale~=1) then
				self.parentTrans:RemoveScaling();
			end
			self.parentQuat:FromRotationMatrix(self.parentTrans);
			if(bUseParentRotation and parentBoneRotMat) then
				self.parentPivotRot = self.parentPivotRot or Quaternion:new();
				self.parentPivotRot:FromRotationMatrix(parentBoneRotMat);
				self.parentQuat:multiplyInplace(self.parentPivotRot);
			end
			
			local p_roll, p_pitch, p_yaw = self.parentQuat:ToEulerAnglesSequence("zxy");
			
			return link_x + self.parentPivot[1] + dx, link_y + self.parentPivot[2] + dy, link_z + self.parentPivot[3] + dz,
				 p_roll, p_pitch, p_yaw, parentScale;
		end
	end
	return link_x, link_y, link_z;
end

-- get world transform of a given sub part (bone).
-- @param keypath: subpart of this actor of which we are computing, such as "bones::R_Hand", if nil it is current actor.
-- @param localPos: if not nil, this is the local offset
-- @param localRow: if not nil, this is the local rotation {roll, pitch yaw}
-- @param bUseParentRotation: use the parent rotation
-- @return x,y,z, roll, pitch yaw, scale: in world space.  
-- return nil, if such information is not available, such as during async loading.
function Actor:ComputeWorldTransform(keypath, curTime, localPos, localRot, bUseParentRotation)
	local link_x = self:GetValue("x", curTime);
	local link_y = self:GetValue("y", curTime);
	local link_z = self:GetValue("z", curTime);
	if(not link_x) then
		return
	end
	if(keypath and keypath~="") then
		local bFoundTarget;
		self.parentPivot = self.parentPivot or mathlib.vector3d:new();
						
		local bonename = keypath:match("^bones::(.+)");
		local parentBoneRotMat;
		if(bonename) then
			local bones = self:GetBonesVariable();
			local boneVar = bones:GetChild(bonename);
			if(boneVar) then
				self:UpdateAnimInstance();
				local pivot = boneVar:GetPivot(true);
				self.parentPivot:set(pivot);
				if(bUseParentRotation) then
					parentBoneRotMat = boneVar:GetPivotRotation(true);
				end
				bFoundTarget = true;
			end
		else
			self.parentPivot:set(0,0,0);
			bFoundTarget = true;
		end 
		if(bFoundTarget) then
			local parentObj = self:GetEntity():GetInnerObject();
			local parentScale = parentObj:GetScale() or 1;
			local dx,dy,dz = 0,0,0;
			if(not bUseParentRotation and localPos) then
				self.parentPivot:add((localPos[1] or 0), (localPos[2] or 0), (localPos[3] or 0));
			end

			self.parentTrans = self.parentTrans or mathlib.Matrix4:new();
			self.parentTrans = parentObj:GetField("LocalTransform", self.parentTrans);
			self.parentPivot:multiplyInPlace(self.parentTrans);
			self.parentQuat = self.parentQuat or mathlib.Quaternion:new();
			if(parentScale~=1) then
				self.parentTrans:RemoveScaling();
			end
			self.parentQuat:FromRotationMatrix(self.parentTrans);
			if(bUseParentRotation and parentBoneRotMat) then
				self.parentPivotRot = self.parentPivotRot or Quaternion:new();
				self.parentPivotRot:FromRotationMatrix(parentBoneRotMat);
				self.parentQuat:multiplyInplace(self.parentPivotRot);

				if(localRot) then
					self.localRotQuat = self.localRotQuat or Quaternion:new();
					self.localRotQuat:FromEulerAngles((localRot[3] or 0), (localRot[1] or 0), (localRot[2] or 0));
					self.parentQuat:multiplyInplace(self.localRotQuat);
				end

				--local az,ax,ay = self.parentQuat:ToEulerAnglesSequence("zxy");
				--local q = Quaternion:new():FromEulerAnglesSequence(az,ax,ay,"zxy");
				--echo({self.parentQuat, self.parentQuat:tostringAngleAxis(),"zxy--->", az,ax,ay, "angle, axis-->",q:tostringAngleAxis(), "-->", q})
				
				if(localPos) then
					self.localPos = self.localPos or mathlib.vector3d:new();
					self.localPos:set((localPos[1] or 0), (localPos[2] or 0), (localPos[3] or 0));
					self.localPos:rotateByQuatInplace(self.parentQuat);
					dx, dy, dz = self.localPos[1], self.localPos[2], self.localPos[3];
				end
			end
			
			local p_roll, p_pitch, p_yaw = self.parentQuat:ToEulerAnglesSequence("zxy");
			
			if(not bUseParentRotation and localRot) then
				-- just for backward compatibility, bUseParentRotation should be enabled in most cases
				p_roll = (localRot[1] or 0) + p_roll;
				p_pitch = (localRot[2] or 0) + p_pitch;
				p_yaw = (localRot[3] or 0) + p_yaw;
			end
			
			return link_x + self.parentPivot[1] + dx, link_y + self.parentPivot[2] + dy, link_z + self.parentPivot[3] + dz,
				 p_roll, p_pitch, p_yaw, parentScale;
		end
	else
		return link_x, link_y, link_z;
	end
end

function Actor:ComputePosAndRotation(curTime)
	local new_x = self:GetValue("x", curTime);
	local new_y = self:GetValue("y", curTime);
	local new_z = self:GetValue("z", curTime);
	local yaw = self:GetValue("facing", curTime);
	local roll = self:GetValue("roll", curTime);
	local pitch = self:GetValue("pitch", curTime);

	-- animate linking to another actor's bone animation. 
	local parent, _, parentActor, keypath = self:GetParentLink(curTime);
	if(keypath and parentActor and parentActor.ComputeWorldTransform)then
		local p_x, p_y, p_z, p_roll, p_pitch, p_yaw, p_scale = parentActor:ComputeWorldTransform(keypath, curTime, parent.pos, parent.rot, parent.use_rot); 
		if(p_x) then
			new_x, new_y, new_z = p_x, p_y, p_z;
			if(p_roll) then
				roll, pitch, yaw = p_roll, p_pitch, p_yaw;
			end
			if(p_scale) then
				-- scale = p_scale * (scale or 1);
			end
		else
			if(self.last_unknown_keypath~=keypath and keypath and keypath~="") then
				-- here we just wait 500 and try again only once for a given bone keypath.
				self.last_unknown_keypath = keypath;
				self.loader_timer = self.loader_timer or commonlib.Timer:new({callbackFunc = function(timer)
					self:FrameMovePlaying(0);
				end})
				LOG.std(nil, "info", "ActorNPC", "parent bone may be async loading, wait 500ms");
				self.loader_timer:Change(500, nil);
			end
		end
	end
	if(self:IsAgentRelative()) then
		new_x, new_y, new_z = self:TransformToEntityPosition(new_x, new_y, new_z);
	end
	yaw = self:TransformToEntityFacing(yaw or 0);
	return new_x, new_y, new_z, yaw, roll, pitch;
end

function Actor:ComputeScaling(curTime)
	return self:GetValue("scaling", curTime) or 1;
end

function Actor:FrameMovePlaying(deltaTime)
	local curTime = self:GetTime();
	self.lastPlayTime = curTime;
	local entity = self.entity;
	if(not entity or not curTime) then
		return
	end
	-- allow adding keyframe while playing during the last segment. 
	local allow_user_control = self:IsAllowUserControl() and
		((self:GetMultiVariable():GetLastTime()+1) <= curTime);

	if(allow_user_control) then
		local obj = entity:GetInnerObject();
		if(obj) then
			obj:SetField("IsControlledExternally", false);
			obj:SetField("EnableAnim", true);
		end
		if(deltaTime ~= 0) then
			return;
		end
	end
	local obj = entity:GetInnerObject();
	local new_x, new_y, new_z, yaw, roll, pitch = self:ComputePosAndRotation(curTime);
	
	local HeadUpdownAngle, HeadTurningAngle, anim, skin, speedscale, scaling, gravity, opacity, blockinhand, assetfile;
	HeadUpdownAngle = self:GetValue("HeadUpdownAngle", curTime);
	HeadTurningAngle = self:GetValue("HeadTurningAngle", curTime);
	anim = self:GetValue("anim", curTime);
	skin = self:GetValue("skin", curTime);
	speedscale = self:GetValue("speedscale", curTime);
	scaling = self:ComputeScaling(curTime);
	gravity = self:GetValue("gravity", curTime);
	opacity = self:GetValue("opacity", curTime);
	assetfile = self:GetValue("assetfile", curTime);
	blockinhand = self:GetValue("blockinhand", curTime);

	if(new_x) then
		entity:SetPosition(new_x, new_y, new_z);
	end

	if(obj) then
		-- in case of explicit animation
		obj:SetField("yaw", yaw or 0);
		obj:SetField("roll", roll or 0);
		obj:SetField("pitch", pitch or 0);
		
		-- this may cause animation instance to lose all custom bones, Time and EnableAnim properties. 
		if(entity:SetMainAssetPath(PlayerAssetFile:GetFilenameByName(assetfile))) then
			self:assetfileChanged();
		end
		entity:SetSkin(skin);
		entity:SetBlockInRightHand(blockinhand);

		obj:SetField("Time", curTime); 
		obj:SetField("IsControlledExternally", true);
		obj:SetField("EnableAnim", not animate_by_script);


		if(anim) then
			if(anim~=obj:GetField("AnimID", 0)) then
				obj:SetField("AnimID", anim);
			end
			if(animate_by_script) then
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
			else
				if(curTime < 500) then
					-- if this the first animation, set it without using a blending factor. 
					obj:SetField("BlendingFactor", 0);
				end
			end
		end

		obj:SetField("HeadUpdownAngle", HeadUpdownAngle or 0);
		obj:SetField("HeadTurningAngle", HeadTurningAngle or 0);
		
		entity:SetSpeedScale(speedscale or 1);
		obj:SetField("Speed Scale", speedscale or 1);
		obj:SetScale(scaling or 1);
		
		if(gravity) then
			obj:SetField("Gravity", gravity);
		end
		obj:SetField("opacity", opacity or 1);
	end

	self.actor_block:FrameMovePlaying(deltaTime);
end

-- select me: for further editing. 
function Actor:SelectMe()
	local entity = self:GetEntity();
	if(entity) then
		local editmodel = entity:GetEditModel();
		editmodel:Connect("EndEdit", self, "OnEndEdit");
		Actor._super.SelectMe(self);	
	end
end

function Actor:OnEndEdit()
	local entity = self:GetEntity();
	if(entity) then
		local displayname = entity:GetDisplayName();
		if(displayname and displayname~="") then
			self:AddKey("name", 0, displayname);
			self:GetItemStack():SetTooltip(displayname);
		end
	end
end

-- bone selection changed in editor
function Actor:OnChangeBone(bone_name)
	local var = self:GetBonesVariable();
	if(var) then
		var:SetSelectedBone(bone_name);
		-- signal
		self:keyChanged();
	end
end

-- set the local bone time
-- @param boneName: a precise bone name or regular expression, like "hand" or ".*hand"
-- @param time: if nil or -1, it will remove bone time. 
function Actor:SetBoneTime(boneName, time)
	local var = self:GetBonesVariable();
	if(var) then
		local variables = var:GetVariables();
		if(variables[boneName]) then
			variables[boneName]:SetTime(time);
		else
			for name, bone in pairs(variables) do
				if(name:match(boneName)) then
					bone:SetTime(time);
				end
			end
		end
	end
end

function Actor:DestroyEntity()
	Actor._super.DestroyEntity(self)
	if(self.bones_variable) then
		self:Disconnect("dataSourceChanged", self.bones_variable, self.bones_variable.LoadFromActor)
		self:Disconnect("assetfileChanged", self.bones_variable, self.bones_variable.OnAssetFileChanged)
		self.bones_variable = nil;
	end
end

function Actor:UnbindAnimInstance()
	if(self.bones_variable) then
		self:Disconnect("dataSourceChanged", self.bones_variable, self.bones_variable.LoadFromActor)
		self:Disconnect("assetfileChanged", self.bones_variable, self.bones_variable.OnAssetFileChanged)
		self.bones_variable:UnbindAnimInstance();
		self.bones_variable = nil;
	end
end

function Actor:BecomeAgent(entity)
	Actor._super.BecomeAgent(self, entity);
	self:CheckLoadBonesAnims();
end

-- when deactivated we will release the control to human player with this function.
function Actor:ReleaseEntityControl()
	self:SetControllable(true);
	self:UnbindAnimInstance();
end

function Actor:DestroyEntity()
	if(self:IsAgent() and self.entity) then
		self:ReleaseEntityControl();
	end
	Actor._super.DestroyEntity(self);
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

```