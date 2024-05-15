```lua
--[[
Title: CodeBlock
Author(s): LiXizhi
Date: 2018/5/16
Desc: In addition to object oriented programming(oop), paracraft code block features an memory-oriented-programming(mop) model. 
The smallest memory unit is an animation clip over time. So we can also call it animation-oriented programming model. 
A program is made up of code block, where each code block is associated with one movie block, which contains a short animation
clip for an actor. Code block exposes a `CodeAPI` that can programmatically control the actor inside the movie block. 

CodeBlock can has unlimited inventory code actors, in addition to the default actor.

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeBlock.lua");
local CodeBlock = commonlib.gettable("MyCompany.Aries.Game.Code.CodeBlock");
local codeBlock = CodeBlock:new():Init(entityCode);
codeBlock:CompileCode('say("hi"); wait(2); say("bye")');
codeBlock:Run();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeActor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeCompiler.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeCoroutine.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeEvent.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeUIActor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Files.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/LanguageConfigurations.lua");
local LanguageConfigurations = commonlib.gettable("MyCompany.Aries.Game.Code.LanguageConfigurations");
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");
local Files = commonlib.gettable("MyCompany.Aries.Game.Common.Files");
local CodeUIActor = commonlib.gettable("MyCompany.Aries.Game.Code.CodeUIActor");
local CodeEvent = commonlib.gettable("MyCompany.Aries.Game.Code.CodeEvent");
local CodeCoroutine = commonlib.gettable("MyCompany.Aries.Game.Code.CodeCoroutine");
local CodeCompiler = commonlib.gettable("MyCompany.Aries.Game.Code.CodeCompiler");
local CodeActor = commonlib.gettable("MyCompany.Aries.Game.Code.CodeActor");
local CodeAPI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeAPI");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");

local CodeBlock = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeBlock"));
CodeBlock:Property("Name", "CodeBlock");
CodeBlock:Property({"DefaultTick", 0.02, "GetDefaultTick", "SetDefaultTick", auto=true,});
CodeBlock:Property({"AutoWait", true, "IsAutoWait", "SetAutoWait", });
CodeBlock:Property({"modified", false, "IsModified", "SetModified", auto=true});

CodeBlock:Signal("message", function(errMsg) end);
CodeBlock:Signal("actorClicked", function(actor, mouse_button) end);
CodeBlock:Signal("actorCloned", function(actor, msg) end);
CodeBlock:Signal("actorCollided", function(actor, fromActor) end);
CodeBlock:Signal("codeUnloaded", function() end);
CodeBlock:Signal("stateChanged", function() end);
CodeBlock:Signal("beforeStopped", function() end);

function CodeBlock:ctor()
	self.timers = {};
	self.timers_pool = {};
	self.actors = commonlib.UnorderedArraySet:new();
	self.events = {};
	self.startTime = 0;
	self.bAutoWait = true
end

function CodeBlock:Init(entityCode)
	self.entityCode = entityCode;
	self:AutoSetFilename();
	return self;
end

function CodeBlock:SetBlockName(name)
	if(self.entityCode and self.entityCode:GetDisplayName()~=name) then
		self.entityCode:SetDisplayName(name);
	end

	if(self.codename and self.codename~=name) then
		if(self:IsLoaded()) then
			-- it is better to reload the code block.
			self:SetModified(true);
			GameLogic.GetCodeGlobal():RemoveCodeBlock(self);
			self.codename = nil;
			self:AutoSetFilename();
			GameLogic.GetCodeGlobal():AddCodeBlock(self);
		else
			self.codename = nil;
			self:AutoSetFilename();
		end
	end
end

function CodeBlock:GetBlockName()
	if(not self.codename) then
		self.codename = self.entityCode and self.entityCode:GetDisplayName() or "";
	end
	return self.codename;
end

function CodeBlock:AutoSetFilename()
	if(self.entityCode) then
		local x,y,z = self.entityCode:GetBlockPos();
		if(x) then
			self:SetFilename(format("%s_block(%d, %d, %d)", self:GetBlockName(), x,y,z));
		end
	end
end

function CodeBlock:Destroy()
	self:Unload();
	CodeBlock._super.Destroy(self);
end

function CodeBlock:GetBlockPos()
	if(self.entityCode) then
		return self.entityCode:GetBlockPos();
	end
end

-- return the timer object
function CodeBlock:SetTimer(callbackFunc, dueTime, period)
	local timer;
	if(self.timers_pool and #self.timers_pool > 0) then
		timer = self.timers_pool[#self.timers_pool];
		self.timers_pool[#self.timers_pool] = nil;
		timer.callbackFunc = callbackFunc;
	else
		timer = commonlib.Timer:new({callbackFunc = callbackFunc})
	end
	self.timers[timer] = true;
	timer:Change(dueTime, period);
	return timer;
end

function CodeBlock:KillTimer(timer)
	timer:Change();
	if(self.timers[timer]) then
		self.timers[timer] = nil;
		if(#self.timers_pool < 10) then
			self.timers_pool[#self.timers_pool+1] = timer;
		end
	end
end

function CodeBlock:SetTimeout(duration, callbackFunc)
	return self:SetTimer(function(timer)
		self:KillTimer(timer);
		if(callbackFunc) then
			callbackFunc(timer);
		end
	end, duration, nil)
end

--@param code: the actual code
--@param filename: virtual filename, if nil, default to GetFilename()
--@return code_func, errormsg
function CodeBlock:CompileCodeImp(code, filename)
	filename = filename or self:GetFilename();
	local configFile = self:GetEntity():GetLanguageConfigFile()
	local compileCodeFunc = LanguageConfigurations:GetCompiler(configFile);
	if(compileCodeFunc) then
		return compileCodeFunc(code, filename, self)
	else
		return CodeCompiler:new():SetFilename(filename):Compile(code);
	end
end

-- compile code and reload if code is changed. 
-- @param code: string
-- return error message if any
function CodeBlock:CompileCode(code)
	if(self:IsModified() or (self.last_code ~= code or not self.code_func)) then
		self:Unload();
		self:SetModified(false);
		self.last_code = code;
		self.code_func, self.errormsg = self:CompileCodeImp(code);
		if(not self.code_func and self.errormsg) then
			LOG.std(nil, "error", "CodeBlock", self.errormsg);
			local msg = self.errormsg;
			msg = format(L"编译错误: %s\n在%s", msg, self:GetFilename());
			self:send_message(msg, "error");
		else
			self:send_message(L"编译成功!");
		end
	else
		self:send_message(L"编译成功!");
	end
	return self.errormsg;
end

-- get default virtual code block filename. 
function CodeBlock:GetFilename()
	return self.filename or "";
end

function CodeBlock:SetFilename(filename)
	self.filename = filename;
end

function CodeBlock:IsLoaded()
	return self.isLoaded;
end

-- unload code and related entities
function CodeBlock:Unload()
	self:StopLastTempCode();
	if(not self.isLoaded) then
		return;
	end
	self.isLoaded = nil;
	self:Stop();
end

-- stop all nearby code entity
function CodeBlock:StopAll()
	if(self:GetEntity()) then
		self:GetEntity():Stop();
	end
end

-- restart all nearby code entity
function CodeBlock:RestartAll()
	if(self:GetEntity()) then
		self:GetEntity():Restart();
	end
end


-- remove everything to unloaded state. 
function CodeBlock:Stop()
	self:beforeStopped();

	self:SetAutoWait(false);
	self:FireEvent("onCodeBlockStopped", nil, nil, true)
	self:SetAutoWait(true);

	self:Disconnect("beforeStopped");
	self:Disconnect("actorClicked");
	self:Disconnect("actorCloned");
	self:Disconnect("actorCollided");
	self:RemoveTimers();
	self:RemoveAllActors();
	self.inventoryActors = nil;
	self:RemoveAllEvents();
	self:StopLastTempCode();
	self:SetOutput(0);

	self.code_env = nil;
	self.isLoaded = nil;
	GameLogic.GetCodeGlobal():RemoveCodeBlock(self);
	self.codename = nil;
	self:codeUnloaded();
	self:stateChanged();
end

-- remove all timers without clearing actors.
function CodeBlock:Pause()
	self:RemoveTimers();
	self:RemoveAllEvents();
end

function CodeBlock:RemoveAllEvents()
	for name, events in pairs(self.events) do
		for _, event in ipairs(events) do
			event:Destroy();
		end
	end
	self.events = {};
end

function CodeBlock:RemoveTimers()
	if(self.timers) then
		for timer, _ in pairs(self.timers) do
			timer:Change();
		end
		self.timers = {};
	end
	if(self.timers_pool) then
		for _, timer in ipairs(self.timers_pool) do
			timer:Change();
		end
		self.timers_pool = {};
	end
end

-- usually called when movie finished playing. 
function CodeBlock:RemoveAllActors()
	self.refActors = nil;
	self.refCodeBlock = nil;
	
	self.isRemovingActors = true;
	for i, actor in ipairs(self:GetActors()) do
		actor:SetCodeBlock(nil);
		actor:OnRemove();
		actor:Destroy();
	end
	self:GetActors():clear();
	self.isRemovingActors = false;
	self:EnableActorPicking(false);
end

function CodeBlock:OnRemoveActor(actor)
	if(not self.isRemovingActors) then
		self:GetActors():removeByValue(actor);
	end
end

-- private function: do not call this function. 
function CodeBlock:AddActor(actor)
	self:GetActors():add(actor);
	actor:SetCodeBlock(self);
	actor:Connect("beforeRemoved", self:GetReferencedCodeBlock(), self:GetReferencedCodeBlock().OnRemoveActor);
	GameLogic.GetCodeGlobal():AddActor(actor);
end

function CodeBlock:GetActors()
	return self.refActors or self.actors;
end

function CodeBlock:GetLastActor()
	return self:GetActors()[#self:GetActors()];
end

-- referencing codeblock. It will share actors in the referenced code blocks. 
function CodeBlock:SetReferencedCodeBlock(codeBlock)
	if(self ~= codeBlock) then
		if(codeBlock) then
			if(self.refActors ~= codeBlock:GetActors()) then
				self.refActors = codeBlock:GetActors();
				codeBlock:Connect("actorClicked", self, self.OnClickActor, "UniqueConnection");
				codeBlock:Connect("actorCloned", self, self.OnCloneActor, "UniqueConnection");
				codeBlock:Connect("actorCollided", self, self.OnCollideActor, "UniqueConnection");
				self.refCodeBlock = codeBlock;
			end
		elseif(self.refActors) then
			self.refActors = nil;
			self.refCodeBlock = nil;
		end
	end
end

function CodeBlock:HasReferencedCodeBlock()
	return self.refActors ~= nil;
end

function CodeBlock:GetReferencedCodeBlock()
	return self.refCodeBlock or self;
end

-- get the last actor in all nearby connected code block. 
function CodeBlock:FindNearbyActor()
	local actor = self:GetLastActor();
	if(not actor and self:GetEntity() and not self:HasReferencedCodeBlock()) then
		local function getLastActor_(codeEntity)
			local x,y,z = codeEntity:GetBlockPos();
			if(codeEntity:GetNearByMovieEntity(x,y,z)) then
				local codeblock = codeEntity:GetCodeBlock();
				if(codeblock) then
					self:SetReferencedCodeBlock(codeblock);
					actor = codeblock:GetLastActor();
				end
				return true;
			end
		end
		self:GetEntity():ForEachNearbyCodeEntity(getLastActor_);
	end
	return actor;
end

function CodeBlock:GetMovieEntity()
	return self.entityCode:FindNearByMovieEntity();
end

function CodeBlock:GetEntity()
	return self.entityCode;
end


-- create a new actor from the nearby movie block. 
-- Please note one may create multiple actors from the same block.
-- return nil if no actor is found.
function CodeBlock:CreateActor()
	local actor = self:CreateFirstActorInMovieBlock();
	if(actor) then
		actor:SetName(self.entityCode:GetDisplayName());
		self:AddActor(actor);
		-- use time 0
		actor:SetTime(0);
		actor:FrameMove(0, false);
		local parentCodeBlock = self:GetReferencedCodeBlock();
		if(self:IsActorPickingEnabled()) then
			actor:EnableActorPicking(true);
			actor:Connect("clicked", parentCodeBlock, parentCodeBlock.OnClickActor);
		else
			actor:EnableActorPicking(false);
		end
		actor:Connect("collided", parentCodeBlock, parentCodeBlock.OnCollideActor);
		return actor;
	end
end

function CodeBlock:EnableActorPicking(bEnabled)
	if(self:GetActors().enableActorPicking ~= bEnabled) then
		self:GetActors().enableActorPicking	= bEnabled;
		if(bEnabled) then
			local parentCodeBlock = self:GetReferencedCodeBlock();
			for i, actor in ipairs(self:GetActors()) do
				if(not actor:IsActorPickingEnabled()) then
					actor:EnableActorPicking(true);
					actor:Connect("clicked", parentCodeBlock, parentCodeBlock.OnClickActor);
				end
			end
		end
	end
end

function CodeBlock:IsActorPickingEnabled()
	return self:GetActors().enableActorPicking;
end

-- private: 
-- @param movie_entity: can be nil
function CodeBlock:CreateFirstActorInMovieBlock(movie_entity)
	movie_entity = movie_entity or self:GetMovieEntity();
	if movie_entity and movie_entity.inventory then
		local actor;
		for i = 1, movie_entity.inventory:GetSlotCount() do
			local itemStack = movie_entity.inventory:GetItem(i)
			if (itemStack and itemStack.count > 0) then
				if (itemStack.id == block_types.names.TimeSeriesNPC) then
					actor = CodeActor:new():Init(itemStack, movie_entity, false, "codeblock");
					break;
				elseif (itemStack.id == block_types.names.TimeSeriesOverlay) then
					actor = CodeUIActor:new():Init(itemStack, movie_entity);
					break;
				end
			end 
		end
		return actor;
	end
end

function CodeBlock:GetCodeEnv()
	if(not self.code_env) then
		self.code_env = CodeAPI:new(self);
	end
	return self.code_env;
end

function CodeBlock:IsLoaded()
	return self.isLoaded;
end

-- recompile and run
function CodeBlock:Restart(onFinishedCallback)
	if(self:GetEntity()) then
		self:Unload();
		return self:Run(onFinishedCallback);
	end
end

function CodeBlock:GetInventoryActor(slotIndex)
	return self.inventoryActors and self.inventoryActors[slotIndex];
end

-- holding a weak reference to the actor
function CodeBlock:SetInventoryActor(slotIndex, actor)
	self.inventoryActors = self.inventoryActors or {};
	self.inventoryActors[slotIndex] = actor;
end

function CodeBlock:RemoveAllInventoryActors()
	if(self.inventoryActors) then
		for slotIndex, actor in pairs(self.inventoryActors) do
			actor:DeleteThisActor();
		end
		self.inventoryActors = nil;
	end
end

-- it will refresh real inventory code actors if code block is loaded
-- otherwise it will refresh inventory movie actors if code block is NOT loaded. 
-- this function is called automatically when the code block inventory is changed. 
-- @param slotIndex: if nil, it will refresh all 
function CodeBlock:RefreshInventoryActor(slotIndex)
	if(not slotIndex) then
		if(self:IsLoaded()) then
			self:RefreshAllInventoryActors()
		else
			self:RefreshAllInventoryAsMovieActors()
		end
		return 
	end
	if(self:IsLoaded()) then
		local inventory = self:GetEntity():GetInventory()
		local itemStack = inventory:GetItem(slotIndex);
		if(itemStack and not self:GetInventoryActor(slotIndex)) then
			local actor = self:CloneMyself();
			if(actor) then
				actor:SetInitParams(itemStack:GetDataTable())
				actor:ApplyInitParams()
				self:SetInventoryActor(slotIndex, actor);
			end
		elseif(not itemStack) then
			local actor = self:GetInventoryActor(slotIndex);
			if(actor) then
				actor:DeleteThisActor();
				self:SetInventoryActor(slotIndex, nil);
			end
		else
			local actor = self:GetInventoryActor(slotIndex)
			actor:ApplyInitParams();
		end
	else
		local inventory = self:GetEntity():GetInventory()
		local itemStack = inventory:GetItem(slotIndex);
		if(itemStack and not self:GetInventoryMovieActor(slotIndex)) then
			local codeActorItem = self:GetEntity():GetCodeActorItemStack(slotIndex);
			if(codeActorItem) then
				local actor = codeActorItem:CreateMovieActor();
				if(actor) then
					self:SetInventoryMovieActor(slotIndex, actor);
				end
			end
		elseif(not itemStack) then
			local actor = self:GetInventoryMovieActor(slotIndex);
			if(actor) then
				actor:DeleteThisActor();
				self:GetInventoryMovieActor(slotIndex, nil);
			end
		else
			local actor = self:GetInventoryMovieActor(slotIndex)
			local codeActorItem = self:GetEntity():GetCodeActorItemStack(slotIndex);
			if(codeActorItem) then
				codeActorItem:ApplyInitParams(actor);
			end
		end
	end
end

function CodeBlock:RefreshAllInventoryActors()
	if(self:IsLoaded()) then
		self:RemoveAllInventoryActors();
		local inventory = self:GetEntity():GetInventory()
		for slotIndex = 1, inventory:GetSlotCount() do
			local itemStack = inventory:GetItem(slotIndex)
			if(itemStack and itemStack.count > 0 and itemStack.serverdata) then
				local actor = self:CloneMyself();
				if(actor) then
					actor:SetInitParams(itemStack:GetDataTable())
					actor:ApplyInitParams()
					self:SetInventoryActor(slotIndex, actor);
				end
			end
		end
	end
end

function CodeBlock:GetInventoryMovieActor(slotIndex)
	return self.inventoryMovieActors and self.inventoryMovieActors[slotIndex];
end

-- holding a weak reference to the actor
function CodeBlock:SetInventoryMovieActor(slotIndex, actor)
	self.inventoryMovieActors = self.inventoryMovieActors or {};
	self.inventoryMovieActors[slotIndex] = actor;
end

function CodeBlock:RemoveAllInventoryMovieActors()
	if(self.inventoryMovieActors) then
		for slotIndex, actor in pairs(self.inventoryMovieActors) do
			actor:DeleteThisActor();
		end
		self.inventoryMovieActors = nil;
	end
end

-- this function is used for rendering all instanced inventory actors in editor mode. 
-- only call this when code block is not loaded, it will show all inventory actors belonging to this code block
-- this could be inaccurate in turns of rendering, since they are not using any code block logics, but just
-- using data from movie block and initial params from the inventory's item stack. 
-- when code block is loaded,  these movie actors will be removed automatically
function CodeBlock:RefreshAllInventoryAsMovieActors()
	if(not self:IsLoaded()) then
		self:RemoveAllInventoryMovieActors();
		local movieEntity = self:GetMovieEntity();
		if(movieEntity) then
			local itemStack = movieEntity:GetFirstActorStack();
			if(itemStack) then
				local item = itemStack:GetItem();
				if(item and item.CreateActorFromItemStack) then
					local inventory = self:GetEntity():GetInventory()
					for slotIndex = 1, inventory:GetSlotCount() do
						local codeActorItem = self:GetEntity():GetCodeActorItemStack(slotIndex);
						if(codeActorItem) then
							local actor = codeActorItem:CreateMovieActor();
							if(actor) then
								self:SetInventoryMovieActor(slotIndex, actor);
							end
						end
					end
				end
			end
		end
	end
end

-- run code again 
function CodeBlock:Run(onFinishedCallback)
	self:GetEntity():ClearIncludedFiles();
	self:RemoveAllInventoryMovieActors();
	self:CompileCode(self:GetEntity():GetCommand());
	if(self.code_func) then
		self:ResetTime();
		self.isLoaded = true;
		self:stateChanged();
		local co = CodeCoroutine:new():Init(self);
		co:SetFunction(self.code_func);
		local actor = self:FindNearbyActor() or self:CreateActor();
		co:SetActor(actor);
		GameLogic.GetCodeGlobal():AddCodeBlock(self);
		local inventory = self:GetEntity():GetInventory()
		if(inventory and not inventory:IsEmpty()) then
			return co:Run(nil, function(...)
				self:RefreshAllInventoryActors();
				if(onFinishedCallback) then
					onFinishedCallback(...)
				end
			end);
		else
			return co:Run(nil, onFinishedCallback);
		end
		
	else
		self:ResetTime();
		self.isLoaded = true;
		self:stateChanged();
		local actor = self:FindNearbyActor() or self:CreateActor();
		self:RefreshAllInventoryActors();
		GameLogic.GetCodeGlobal():AddCodeBlock(self);
		return false;
	end
end

-- @param msg: string
-- @param msgType: if nil, it is a normal message. 
-- it can also be "error", if it is error, we will show to user via game console. 
function CodeBlock:send_message(msg, msgType)
	self.lastMessage = msg;
	self:message(msg);
	if(msgType == "error") then
		-- LOG.std(nil, "error", "CodeBlock", msg);
		local date_str, time_str = commonlib.log.GetLogTimeString();
		local html_text = format("<div style='color:#ff0000'><span style='color:#808080'>%s %s: </span>%s%s<div>", date_str, time_str, commonlib.Encoding.EncodeHTMLInnerText(msg:sub(1, 1024)), ((#msg)>1024) and "..." or "");
		GameLogic.SetTipText(html_text, nil, 10)
	end
end

function CodeBlock:GetLastMessage()
	return self.lastMessage;
end

-- @param msg: optional message to be passed to event callback
function CodeBlock:FireEvent(event_name, actor, msg, bIsImmediate)
	event_name = event_name or "";
	local events = self.events[event_name];
	if(events) then
		for _, event in ipairs(events) do
			if(actor) then
				event:SetActor(actor);
			end
			event:Fire(msg, nil, bIsImmediate);
		end
	end
end


function CodeBlock:CreateEvent(event_name)
	event_name = event_name or "";
	local event = CodeEvent:new():Init(self, event_name);
	
	local events = self.events[event_name];
	if(not self.events[event_name]) then
		events = {};
		self.events[event_name] = events;
	end
	events[#events + 1] = event;
	return event;
end

-- when the actor start/end playing at the given time (milliseconds)
-- Only the start and end of an animation is fired. 
function CodeBlock:RegisterAnimationEvent(time, callbackFunc)
	if(callbackFunc and time) then
		local event = self:CreateEvent("onAnimateActor");
		event:SetIsFireForAllActors(false);
		event:SetCanFireCallback(function(actor, curTime)
			return (time == curTime);
		end);
		event:SetFunction(callbackFunc);
	end
end

function CodeBlock:OnAnimateActor(actor, time)
	self:FireEvent("onAnimateActor", actor, time)
end

-- actor is clicked
function CodeBlock:RegisterClickEvent(callbackFunc)
	self:EnableActorPicking(true);
	local event = self:CreateEvent("onClickActor");
	event:SetIsFireForAllActors(false);
	event:SetFunction(callbackFunc);
end

-- use this sparingly, because we will disable auto yield in this mode. 
function CodeBlock:RegisterStopEvent(callbackFunc)
	local event = self:CreateEvent("onCodeBlockStopped");
	event:SetIsFireForAllActors(true);
	event:SetFunction(callbackFunc);
end

-- @param blockname: block id or name, if nil or "any", it matches all blocks
function CodeBlock:RegisterBlockClickEvent(blockname, callbackFunc)
	local event = self:CreateEvent("onBlockClicked");
	event:SetIsFireForAllActors(true);
	event:SetFunction(callbackFunc);

	local blockid, _;
	if(type(blockname) == "string" and blockname ~= "any") then
		blockid, _ = CmdParser.ParseBlockId(blockname);
	elseif(type(blockname) == "number") then
		blockid = blockname
	end
	
	local function onEvent_(_, msg)
		if(not msg) then
			return 
		end
		local bFire;
		if(not blockid) then
			bFire = true;
		elseif(blockid == msg.blockid) then
			bFire = true;
		end
		if(bFire) then
			event:Fire(msg.param1 or msg);
			return true;
		end
	end
	event:Connect("beforeDestroyed", function()
		GameLogic.GetCodeGlobal():UnregisterBlockClickEvent(onEvent_);
	end)
	GameLogic.GetCodeGlobal():RegisterBlockClickEvent(onEvent_);
end

function CodeBlock:OnClickActor(actor, mouse_button)
	self:FireEvent("onClickActor", actor);
	self:actorClicked(actor, mouse_button);
end

-- we will accept these keys, so that base context does not process them. 
local nonAcceptingKeys = {
	["mouse_buttons"] = true, ["mouse_wheel"] = true, ["escape"] = true,
}

local mouseKeys = {
	["mouse_buttons"] = true, ["mouse_wheel"] = true
}


-- @param keyname: if nil or "any", it means any key, such as "a-z", "space", "return", "escape", "mouse_wheel", "mouse_buttons"
-- @param callbackFunc: if keyname is "any", this function will block key if it returns true. 
-- case insensitive
function CodeBlock:RegisterKeyPressedEvent(keyname, callbackFunc)
	local event = self:CreateEvent("onKeyPressed");
	event:SetIsFireForAllActors(true);
	event:SetStopLastEvent(false);
	event:SetFunction(callbackFunc);
	keyname = GameLogic.GetCodeGlobal():GetKeyNameFromString(keyname) or keyname;
	
	local function onEvent_(_, msg)
		if(not msg) then
			return 
		end
		local bFire;
		local bImmediateMode;
		local result;
		if(not keyname or keyname == "any") then
			if(not mouseKeys[msg.keyname or ""]) then
				bFire = true;
				bImmediateMode = true;
			end
		elseif(keyname == msg.keyname) then
			if(not nonAcceptingKeys[keyname]) then
				result = true;
			end
			bFire = true;
		end
		if(bFire) then
			return event:Fire(msg.param1 or msg, nil, bImmediateMode) or result;
		end
	end
	event:Connect("beforeDestroyed", function()
		GameLogic.GetCodeGlobal():UnregisterKeyPressedEvent(onEvent_);
	end)
	GameLogic.GetCodeGlobal():RegisterKeyPressedEvent(onEvent_);
end

-- if last tick event is not finished, the tick is ignored. 
-- @param ticks: default to 1 tick
function CodeBlock:RegisterTickEvent(ticks, callbackFunc)
	ticks = tonumber(ticks or 1);
	local event = self:CreateEvent("onTick");
	event:SetIsFireForAllActors(true);
	event:SetFunction(callbackFunc);
	event:SetStopLastEvent(false);
	local tick = 1;
	local function onEvent_(_, msg)
		tick = tick + 1;
		if((tick % ticks) == 0) then
			event:Fire(msg and msg.msg, msg and msg.onFinishedCallback, true);
		end
	end
	
	event.UnRegisterTextEvent = function()
		GameLogic.GetCodeGlobal():UnregisterTextEvent("onTick", onEvent_);
	end
	
	event:Connect("beforeDestroyed", event.UnRegisterTextEvent);
	GameLogic.GetCodeGlobal():RegisterTextEvent("onTick", onEvent_);
	
	return event;
end


function CodeBlock:RegisterTextEvent(text, callbackFunc)
	local event = self:CreateEvent("onText"..text);
	event:SetIsFireForAllActors(true);
	event:SetFunction(callbackFunc);
	local function onEvent_(_, msg)
		event:Fire(msg and msg.msg, msg and msg.onFinishedCallback);
	end
	
	event.UnRegisterTextEvent = function()
		GameLogic.GetCodeGlobal():UnregisterTextEvent(text, onEvent_);
	end
	
	event:Connect("beforeDestroyed", event.UnRegisterTextEvent);
	GameLogic.GetCodeGlobal():RegisterTextEvent(text, onEvent_);
	
	return event;
end

function CodeBlock:UnRegisterTextEvent(text, callbackFunc)
	local eventname = "onText"..text;
	local events = self.events[eventname];
	
	for i, event in ipairs(events) do
		if event.callbackFunc == callbackFunc then
			if(event.UnRegisterTextEvent) then
				event.UnRegisterTextEvent();
			end
			event:Destroy();
			table.remove(events, i);
			break;
		end
	end
	
	if #events == 0 then
		self.events[eventname] = nil;
	end
end

-- @param onFinishedCallback: can be nil
function CodeBlock:BroadcastTextEvent(text, msg, onFinishedCallback)
	if(type(text) == "string") then
		GameLogic.GetCodeGlobal():BroadcastTextEvent(text, msg, onFinishedCallback);
	end
end

function CodeBlock:RegisterCloneActorEvent(callbackFunc)
	local event = self:CreateEvent("onCloneActor");
	event:SetFunction(callbackFunc);
end

function CodeBlock:RegisterNetworkEvent(event_name, callbackFunc)
	local event = self:CreateEvent(event_name);
	event:SetIsFireForAllActors(true);
	event:SetFunction(callbackFunc);
	local function onEvent_(_, msg)
		event:Fire(msg and msg.msg, msg and msg.onFinishedCallback);
	end
	event:Connect("beforeDestroyed", function()
		GameLogic.GetCodeGlobal():UnregisterNetworkEvent(event_name, onEvent_);
	end)
	if(event_name == "connect") then
		self:Connect("beforeStopped", function()
			GameLogic.GetCodeGlobal():UnregisterNetworkEvent(event_name, onEvent_, self);
		end)
	end
	GameLogic.GetCodeGlobal():RegisterNetworkEvent(event_name, onEvent_);
end

function CodeBlock:BroadcastNetworkEvent(event_name, msg)
	GameLogic.GetCodeGlobal():BroadcastNetworkEvent(event_name, msg);
end

function CodeBlock:SendNetworkEvent(username, event_name, msg)
	GameLogic.GetCodeGlobal():SendNetworkEvent(username, event_name, msg);
end

-- create a clone of some code block's actor
-- @param name: if nil or "myself", it means clone myself
-- @param msg: any mesage that is forwared to clone event
function CodeBlock:CreateClone(name, msg)
	if(not name or name == "myself") then
		self:CloneMyself(msg);
	else
		local codeBlock = self:GetCodeBlockByName(name);
		if(codeBlock) then
			codeBlock:CloneMyself(msg);
		end
	end
end

function CodeBlock:GetCodeBlockByName(name)
	return GameLogic.GetCodeGlobal():GetCodeBlockByName(name);
end

-- @return the actor created
function CodeBlock:CloneMyself(msg)
	local actor = self:CreateActor();
	if(actor) then
		self:GetReferencedCodeBlock():OnCloneActor(actor, msg);
		return actor;
	end
end

function CodeBlock:OnCloneActor(actor, msg)
	self:FireEvent("onCloneActor", actor, msg);
	self:actorCloned(actor, msg);
end

-- blink the created actor 
function CodeBlock:HighlightActors()
	local actors = self:GetActors();
	if(actors:last()) then
		for i = 1, math.min(10, #actors) do
			local actor = actors[i];
			actor:SetHighlight(true);
			commonlib.TimerManager.SetTimeout(function()  
				actor:SetHighlight(false);
			end, 1000 + i*100);
		end
	end
end

function CodeBlock:CreateGetActor()
	local env = self:GetCodeEnv();
	if(env) then
		return env.actor or self:FindNearbyActor() or self:CreateActor();
	end
end

function CodeBlock:GetActor()
	local env = self:GetCodeEnv();
	if(env) then
		return env.actor or self:FindNearbyActor();
	end
end

-- usually from help window. There can only be one temp code running. 
-- @param code: string
function CodeBlock:RunTempCode(code, filename)
	local code_func, errormsg = self:CompileCodeImp(code, filename or "tempcode");
	if(not code_func and errormsg) then
		LOG.std(nil, "error", "CodeBlock", errormsg);
		local msg = errormsg;
		msg = format(L"编译错误: %s\n在%s", msg, filename);
		self:send_message(msg, "error");
	else
		local env = self:GetCodeEnv();
		if(env) then
			self:StopLastTempCode();
			local co = CodeCoroutine:new():Init(self);
			self.lastTempCodeCoroutine = co;
			self:stateChanged();
			local actor = env.actor or self:FindNearbyActor() or self:CreateActor();
			co:SetActor(actor);
			co:SetFunction(code_func);
			co:Run()
		end
	end
end

function CodeBlock:HasRunningTempCode()
	if(self.lastTempCodeCoroutine) then
		return true;
	end
end

function CodeBlock:StopLastTempCode()
	if(self.lastTempCodeCoroutine) then
		self.lastTempCodeCoroutine:Stop();
		self.lastTempCodeCoroutine = nil;
	end
end

-- in seconds
function CodeBlock:GetTime()
	return (commonlib.TimerManager.GetCurrentTime() - self.startTime)/1000;
end

function CodeBlock:ResetTime()
	self.startTime = commonlib.TimerManager.GetCurrentTime()
end

-- collision event is special that it will not overwrite the last event.
-- @param name: if nil or "", it matches all actors
-- if name is a number, it means a physics_group_id
function CodeBlock:RegisterCollisionEvent(name, callbackFunc)
	local event = self:CreateEvent("onCollideActor");
	event:SetIsFireForAllActors(false);
	event:SetStopLastEvent(false);
	if(type(name) == "number") then
		event:SetCanFireCallback(function(actor, fromActor)
			if(fromActor and (fromActor:GetGroupId() == name)) then
				return true;
			end
		end);
	else
		event:SetCanFireCallback(function(actor, fromActor)
			if(fromActor and (not name or name=="" or fromActor:GetName() == name)) then
				return true;
			end
		end);
	end
	event:SetFunction(callbackFunc);
end

function CodeBlock:OnCollideActor(actor, fromActor)
	self:FireEvent("onCollideActor", actor, fromActor);
	self:actorCollided(actor, fromActor);
end

-- set code block entity's output value. default to nil.
function CodeBlock:SetOutput(result)
	if(self:GetEntity()) then
		self:GetEntity():SetLastCommandResult(result);
	end
end

local lastErrorCallstack = "";
function CodeBlock.handleError(x)
	lastErrorCallstack = commonlib.debugstack(2, 5, 1);
	return x;
end

-- @param filename: include a file relative to current world directory
function CodeBlock:IncludeFile(filename)
	local filepath = Files.WorldPathToFullPath(filename);
	if(self:GetEntity()) then
		self:GetEntity():AddIncludedFile(filename);
	end

	local file = ParaIO.open(filepath, "r")
	if(file:IsValid()) then
		local code = file:GetText();
		file:close();
		if(code and code~="") then
			local code_func, errormsg = self:CompileCodeImp(code, filename);
			if(not code_func and errormsg) then
				LOG.std(nil, "error", "CodeBlock", errormsg);
				local msg = errormsg;
				msg = format(L"编译错误: %s\n在%s", msg, filename);
				self:send_message(msg, "error");
			else
				setfenv(code_func, self:GetCodeEnv());
				local ok, result = xpcall(code_func, CodeBlock.handleError);
				if(not ok) then
					if(result:match("_stop_all_")) then
						self:StopAll();
					elseif(result:match("_restart_all_")) then
						self:RestartAll();
					else
						LOG.std(nil, "error", "CodeBlock", "%s\n%s", result, lastErrorCallstack);
						local msg = format(L"运行时错误: %s\n在%s", tostring(result), filename);
						self:send_message(msg, "error");
					end
				end
			end
		end
	else
		LOG.std(nil, "warn", "CodeBlock", "include can not file world file %s", filename);
		local msg = format(L"没有找到文件: %s", filename);
		self:send_message(msg, "error");
	end
end

function CodeBlock:SetAutoWait(bAutoWait)
	self.bAutoWait = bAutoWait;
end

-- whether to automatically wait when a given number of instructions are executed. 
function CodeBlock:IsAutoWait()
	return self.bAutoWait;
end

function CodeBlock:handleAutoWaitCmd(params)
	local isAutowait = true;
	if(type(params) == "string") then
		isAutowait  = CmdParser.ParseBool(params)
	elseif(type(params) == "boolean") then
		isAutowait = params
	end
	self:SetAutoWait(isAutowait);
end

local codeBlockCmds = {
	["autowait"] = CodeBlock.handleAutoWaitCmd
}

function CodeBlock:RunCommand(cmd_name, cmd_text)
	if(cmd_text == nil) then
		cmd_name, cmd_text = cmd_name:match("^/*(%w+)%s*(.*)$");
	end
	local handlerFunc = codeBlockCmds[cmd_name or ""];
	if(handlerFunc) then
		handlerFunc(self, cmd_text);
	else
		return GameLogic.RunCommand(cmd_name, cmd_text);
	end
end

--[[
Title: Code Actor
Author(s): LiXizhi
Date: 2018/5/19
Desc: Code actor is the base class for CodeBlock-controlled actors. Code actor is managed by a Code Block.

use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeActor.lua");
local CodeActor = commonlib.gettable("MyCompany.Aries.Game.Code.CodeActor");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorNPC.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/EntityCodeActor.lua");
NPL.load("(gl)script/ide/math/vector.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Direction.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Physics/PhysicsWorld.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Entity/PlayerAssetFile.lua");
local PlayerAssetFile = commonlib.gettable("MyCompany.Aries.Game.EntityManager.PlayerAssetFile")
local math3d = commonlib.gettable("mathlib.math3d");
local PhysicsWorld = commonlib.gettable("MyCompany.Aries.Game.PhysicsWorld");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local vector3d = commonlib.gettable("mathlib.vector3d");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.ActorNPC"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeActor"));
Actor:Property("Name", "CodeActor");
Actor:Property({"entityClass", "EntityCodeActor"});
-- frame move interval in milliseconds
Actor:Property({"frameMoveInterval", 30, "GetFrameMoveInterval", "SetFrameMoveInterval", auto=true});
Actor:Property({"time", 0, "GetTime", "SetTime", auto=true});
Actor:Property({"playSpeed", 1, "GetPlaySpeed", "SetPlaySpeed", auto=true});
Actor:Property({"enableActorPicking", false, "IsActorPickingEnabled", "EnableActorPicking", auto=false});
-- the itemstack(TimeSeries) is changed
Actor:Signal("dataSourceChanged");
Actor:Signal("clicked", function(actor, mouseButton) end);
Actor:Signal("collided", function(actor, fromActor) end);
Actor:Signal("beforeRemoved", function(self) end);
Actor:Signal("nameChanged", function(actor, oldName, newName) end);

function Actor:ctor()
	self.offsetPos = vector3d:new(0,0,0);
	self.fromPos = vector3d:new(0,0,0);
	self.offsetYaw = 0;
	self.codeEvents = {};
end


-- @param itemStack: movie block actor's item stack where time series data source of this entity is stored. 
-- @param isReuseActor: whether we will reuse actor in the scene with the same name instead of creating a new entity. default to false.
-- @param name: if not provided, it will use the name in itemStack
function Actor:Init(itemStack, movieclipEntity, isReuseActor, name)
	if(not Actor._super.Init(self, itemStack, movieclipEntity, isReuseActor, name)) then
		return;
	end
	local entity = self.entity;
	entity:Connect("clicked", self, self.OnClick);
	entity:Connect("collided", self, self.OnCollideWithEntity);
	entity:Connect("valueChanged", self, self.OnEntityPositionChange);
	return self;
end

function Actor:ApplyInitParams()
	local pos = self:GetInitParam("pos")
	if(pos) then
		local time = self:GetInitParam("startTime") or 0;
		if(self:GetTime() ~= time) then
			self:SetTime(time);
			self:FrameMove(0);
		end

		local entity = self:GetEntity();
		if(entity) then
			if(pos[1] and pos[2] and pos[3]) then
				self:SetBlockPos(pos[1], pos[2], pos[3]);
			end

			local yaw = self:GetInitParam("yaw")
			if(yaw) then
				entity:SetFacing(yaw*3.14/180);
			end
			local pitch = self:GetInitParam("pitch")
			if(pitch) then
				entity:SetPitch(pitch*3.14/180);
			end
			local roll = self:GetInitParam("roll")
			if(roll) then
				entity:SetRoll(roll*3.14/180);
			end

			local scaling = self:GetInitParam("scaling")
			if(scaling) then
				entity:SetScaling(scaling/100);
			end
		end
	end
end

function Actor:IsActorPickingEnabled()
	return self.enableActorPicking;
end

function Actor:EnableActorPicking(bEnabled)
	self.enableActorPicking = bEnabled;
	if(self.entity) then
		self.entity:SetSkipPicking(not bEnabled);
	end
end

function Actor:SetName(name)
	if(self.name ~= name) then
		local oldName = self.name;
		self.name = name;
		if(self:IsAgent() and self.entity) then
			self.entity:SetName(name);
		end
		self:nameChanged(self, oldName, name);
	end
end

function Actor:GetName()
	return self.name;
end

function Actor:OnClick(mouse_button)
	self:clicked(self, mouse_button);
end

function Actor:OnCollideWithEntity(fromEntity)
	self:collided(self, fromEntity:GetActor());
end

-- @param block_id: if nil, it means any obstruction block.
-- @return true
function Actor:IsTouchingBlock(block_id)
	if(not self.entity) then
		return;
	end
	local aabb = self.entity:GetCollisionAABB();
	local blockMinX,  blockMinY, blockMinZ = BlockEngine:block(aabb:GetMinValues());
	local blockMaxX,  blockMaxY, blockMaxZ = BlockEngine:block(aabb:GetMaxValues());

    for bx = blockMinX, blockMaxX do
        for bz = blockMinZ, blockMaxZ do
            for by = blockMinY, blockMaxY do
                local block_template = BlockEngine:GetBlock(bx, by, bz);
                if (block_template) then
					if(block_template.id == block_id) then
						return true;
					elseif(not block_id and block_template.obstruction) then
						return true;
					end
                end
            end
		end
	end
end

function Actor:IsTouchingActorByName(actorname)
	local entity = self:GetEntity();
	if(entity) then
		local entities = EntityManager.GetEntitiesByAABBOfType(EntityManager[self.entityClass], entity:GetCollisionAABB())
		if (entities and #entities > 1) then
			for i=1, #entities do
				local entity2 = entities[i];
				if(entity2 ~= entity and entity2:GetActor():GetName() == actorname and entity:GetCollisionAABB():Intersect(entity2:GetCollisionAABB())) then
					return true
				end
			end
		end
		return false;
	end
end

-- @return false;
function Actor:IsTouchingEntity(entity2)
	if(not entity2) then
		return false;
	end
	local entity = self:GetEntity();
	if(entity and entity:GetCollisionAABB():Intersect(entity2:GetCollisionAABB())) then
		return true;
	end
end

-- static function
local function CanBeCollidedWith_(destEntity, entity)
	if(destEntity:IsVisible() and destEntity:IsStaticBlocker()) then
		return true;
	end
end

function Actor:CalculatePushOut(dx, dy, dz)
	local entity = self:GetEntity();
	if(entity) then
		return entity:CalculatePushOut(dx, dy, dz, CanBeCollidedWith_)
	end
end

-- only bounce in horizontal XZ plain, it just changes the direction/facing of the actor, so that the actor moves aways from the collision. 
function Actor:Bounce()
	if(not self.entity) then
		return;
	end
	local aabb = self.entity:GetCollisionAABB();
	local listCollisions = PhysicsWorld:GetCollidingBoundingBoxes(aabb, self.entity, CanBeCollidedWith_);

	local facing = self.entity:GetFacing();
	local dx, dz;
	dx = math.cos(facing) * 0.1;
	dz = -math.sin(facing) * 0.1;
	local offsetX, offsetZ = dx, dz;
	for i= 1, listCollisions:size() do
		offsetX = listCollisions:get(i):CalculateXOffset(aabb, offsetX, 0.3);
	end
	for i= 1, listCollisions:size() do
		offsetZ = listCollisions:get(i):CalculateZOffset(aabb, offsetZ, 0.3);
	end
	if(offsetX~=dx and offsetX*dx<0) then
		dx = -dx
	end
	if(offsetZ~=dz and offsetZ*dz<0) then
		dz = -dz
	end
	local newFacing = Direction.GetFacingFromOffset(dx, 0, dz);
	self.entity:SetFacing(newFacing);
end

function Actor:IsTouchingPlayers()
	if(not self.entity) then
		return;
	end
	local distExpand = 0.25;
	local aabb = self.entity:GetCollisionAABB();
    local listEntities = EntityManager.GetEntitiesByAABBExcept(aabb:clone():Expand(distExpand, distExpand, distExpand), self.entity);
	if(listEntities) then
		for _, entityCollided in ipairs(listEntities) do
			if(entityCollided:IsPlayer()) then
				return true;
			end
		end
	end
end

function Actor:DistanceTo(actor2)
	local entity = self:GetEntity();
	if(entity) then
		local entity2 = actor2:GetEntity();
		if(entity2) then
			local x, y, z = entity2:GetPosition();
			local dist = entity:GetDistanceSq(x,y,z);
			if(dist > 0.0001) then
				return math.sqrt(dist);
			else
				return dist;
			end
		end
	end
end

function Actor:DeleteThisActor()
	self:OnRemove();
	self:Destroy();
end

function Actor:RestoreEntityControl()
	local entity = self:GetEntity();
	if(entity) then
		entity:SetDummy(false);
		local obj = entity:GetInnerObject();
		if(obj) then
			obj:SetField("IsControlledExternally", false);
			obj:SetField("EnableAnim", true);
			
		end
		self:UnbindAnimInstance()
	end
end

function Actor:OnRemove()
	if(self:IsAgent() and self:GetEntity() == EntityManager.GetPlayer()) then
		self:RestoreEntityControl();
	end

	if(self:HasFocus()) then
		self:RestoreFocus();
	end
	self:beforeRemoved(self);

	Actor._super.OnRemove(self);
end

function Actor:SetVisible(bVisible)
	local entity = self:GetEntity();
	if(entity) then
		entity:SetVisible(bVisible);
	end
end

function Actor:SetHighlight(bHighlight)
	local entity = self:GetEntity();
	if(entity) then
		entity:SetHighlight(bHighlight);
	end
end

function Actor:SetBlockPos(bx, by, bz)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetDummy(true);
		-- we will move using real position which fixed a bug that moveTo() does not work 
		-- when we are already inside the target block
		bx, by, bz = BlockEngine:real_min(bx+0.5, by, bz+0.5);
		entity:SetPosition(bx, by, bz);
	end
end

function Actor:GetPosition()
	local entity = self:GetEntity();
	if(entity) then	
		return entity:GetPosition();
	end
end

function Actor:SetPosition(targetX,targetY,targetZ)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetDummy(true);
		entity:SetPosition(targetX,targetY,targetZ);
	end
end

function Actor:SetFacingDelta(v)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetFacingDelta(v);
		if(self:IsPlaying()) then
			self:ResetOffsetPosAndRotation();
		end
	end
end

function Actor:SetFacing(facing)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetFacing(facing);
		if(self:IsPlaying()) then
			self:ResetOffsetPosAndRotation();
		end
	end
end

function Actor:GetFacing()
	local entity = self:GetEntity()
	if(entity) then
		return entity:GetFacing();
	end
end

function Actor:IsPlaying()
	if(self.playTimer and self.playTimer:IsEnabled()) then
		return true;
	end
end

function Actor:OnEntityPositionChange()
	if(self:IsPlaying()) then
		self:ResetOffsetPosAndRotation();
	end
end

-- this allows us to play animation in movie block from current movie time to be relative to current entity's position
-- @param time: if nil, it means the current time. 
function Actor:ResetOffsetPosAndRotation()
	local curTime = self:GetTime();
	local entity = self.entity;

	if(not entity or not curTime) then
		return
	end
	local eX, eY, eZ = entity:GetPosition();
	local new_x, new_y, new_z, yaw, roll, pitch = Actor._super.ComputePosAndRotation(self, curTime);
	if(not new_x) then
		new_x, new_y, new_z = eX, eY, eZ;
	end;
	local obj = entity:GetInnerObject();
	self:SetOffsetPos(eX - new_x, eY - new_y, eZ - new_z, new_x, new_y, new_z);
	self:SetOffsetYaw(obj:GetField("yaw", 0) - (yaw or 0), yaw);
end

function Actor:ComputeScaling(curTime)
	local scale = self:GetValue("scaling", curTime)
	if(not scale) then
		local entity = self:GetEntity();
		if(entity) then
			scale = entity:GetScaling();
		end
	end
	return scale or 1;
end

function Actor:SetOffsetYaw(yaw)
	self.offsetYaw = yaw;
end

function Actor:GetOffsetYaw()
	return self.offsetYaw;
end

function Actor:SetOffsetPos(dx,dy,dz, fromX, fromY, fromZ)
	self.offsetPos:set(dx,dy,dz);
	self.fromPos:set(fromX, fromY, fromZ);
end

function Actor:GetOffsetPos()
	return self.offsetPos:get();
end

function Actor:ComputePosAndRotation(curTime)
	local new_x, new_y, new_z, yaw, roll, pitch = Actor._super.ComputePosAndRotation(self, curTime);
	
	if(new_x) then
		yaw = yaw or 0;
		local dx,dy,dz = new_x - self.fromPos[1], new_y - self.fromPos[2],  new_z - self.fromPos[3];
		if((dx~=0 or dy~=0 or dz~=0) and self.offsetYaw ~=0) then
			dx, dy, dz = math3d.vec3Rotate(dx,dy,dz, 0, self.offsetYaw, 0);
			new_x, new_y, new_z = self.fromPos[1] + dx, self.fromPos[2] + dy, self.fromPos[3] + dz;
		end
		dx, dy, dz = self:GetOffsetPos();
		return new_x+dx, new_y+dy, new_z+dz, self:GetOffsetYaw() + yaw, roll, pitch;
	end
end

-- if the same event is called multiple times, the previous one is always stopped before a new one is fired. 
function Actor:SetCodeEvent(event, co)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		last_coroutine:Stop();
	end
	self.codeEvents[event] = co;
end

-- if the same event is called multiple times, the previous one is always stopped before a new one is fired. 
function Actor:StopLastCodeEvent(event)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		last_coroutine:Stop();
		self.codeEvents[event] = nil;
	end
end

function Actor:IsRunningEvent(event)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		return not last_coroutine:IsFinished();
	end
end

-- let the camera focus on this player and take control of it. 
function Actor:SetFocus()
	local entity = self:GetEntity();
	if(entity) then
		entity:SetFocus();
	end
end

function Actor:HasFocus()
	local entity = self:GetEntity();
	if(entity) then
		return entity:HasFocus();
	end
end

function Actor:RestoreFocus()
	EntityManager.GetPlayer():SetFocus();
end

function Actor:GetPhysicsRadius()
	local entity = self:GetEntity();
	return entity and (entity:GetPhysicsRadius() * BlockEngine.blocksize_inverse) or 0.25;
end

function Actor:SetPhysicsRadius(radius)
	local entity = self:GetEntity();
	if(entity) then	
		radius = tonumber(radius);
		entity:SetPhysicsRadius(radius * BlockEngine.blocksize);
	end
end

function Actor:GetPhysicsHeight()
	local entity = self:GetEntity();
	return entity and (entity:GetPhysicsHeight() * BlockEngine.blocksize_inverse) or 1;
end

function Actor:SetPhysicsHeight(height)
	local entity = self:GetEntity();
	if(entity) then	
		height = tonumber(height);
		if(height) then
			entity:SetPhysicsHeight(height * BlockEngine.blocksize);
		end
	end
end

function Actor:GetAssetFile()
	local entity = self:GetEntity();
	return entity and entity:GetMainAssetPath();
end

function Actor:SetAssetFile(filename)
	local entity = self:GetEntity();
	if(entity) then	
		filename = PlayerAssetFile:GetFilenameByName(filename)
		entity:SetMainAssetPath(filename);
	end
end

function Actor:GetColor()
	local entity = self:GetEntity();
	return entity and entity:GetColor();
end

function Actor:SetColor(color)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetColor(color);
	end
end

function Actor:Say(text, duration)
	local entity = self:GetEntity();
	if(entity) then	
		entity:Say(text, duration)
	end
end

function Actor:SetFacingDegree(degree)
	self:SetFacing(degree/180*math.pi)
end

function Actor:GetFacingDegree()
	return self:GetFacing()*180/math.pi
end

-- floating point block position
function Actor:SetPosX(x)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(BlockEngine:real_min(x), y_, z_);
end

function Actor:GetPosX()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return x;
end

-- floating point block position
function Actor:SetPosZ(z)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(x_, y_, BlockEngine:real_min(z));
end

function Actor:GetPosZ()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return z;
end

-- floating point block position
function Actor:SetPosY(y)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(x_, BlockEngine:realY(y), z_);
end

function Actor:GetPosY()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return y;
end

-- set (physics) group id
function Actor:SetGroupId(id)
	self.groupId = id and tonumber(id);
end

-- get group id, default to nil
function Actor:GetGroupId()
	return self.groupId;
end

function Actor:SetRollDegree(degree)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetRoll(degree/180*math.pi);
	end
end

function Actor:GetRollDegree()
	local entity = self:GetEntity();
	return entity and (entity:GetRoll()*180/math.pi) or 0;
end

function Actor:SetPitchDegree(degree)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetPitch(degree/180*math.pi);
	end
end

function Actor:GetPitchDegree()
	local entity = self:GetEntity();
	return entity and (entity:GetPitch()*180/math.pi) or 0;
end

function Actor:SetMovieActorImp(itemStack, movie_entity)
	movie_entity = movie_entity or self:GetMovieClipEntity();
	local entity = self:GetEntity()
	if(entity) then
		local x, y, z = entity:GetPosition()
		local facing = entity:GetFacing()
		local wasVisible = entity:IsVisible()
		local variables = entity:GetVariables();
		
		self:DestroyEntity();
		self:Init(itemStack, movie_entity);
		self:FrameMove(self:GetTime() or 0, false);
		entity = self:GetEntity();
		if(entity) then
			entity:SetPosition(x,y,z);
			entity:SetFacing(facing);
			if(not wasVisible) then
				entity:SetVisible(wasVisible);
			end
			variables:copyTo(entity:GetVariables());
		end
		self:EnableActorPicking(self:IsActorPickingEnabled());
	end
end

-- @param actorName: if nil or 1, it is the first one in movie block
-- if number it is the actor index in movie block, if string, it is its actor name
function Actor:SetMovieActor(actorName)
	actorName = actorName or 1;
	local movie_entity = self:GetMovieClipEntity();
	if(not movie_entity) then
		return
	end
	if(type(actorName) == "number") then
		local index = 0;
		for i = 1, movie_entity.inventory:GetSlotCount() do
			local itemStack = movie_entity.inventory:GetItem(i)
			if (itemStack and itemStack.count > 0) then
				if (itemStack.id == block_types.names.TimeSeriesNPC) then
					index = index + 1;
					if(index == actorName) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end
			end 
		end
	elseif(type(actorName) == "string" and actorName~="") then
		for i = 1, movie_entity.inventory:GetSlotCount() do
			local itemStack = movie_entity.inventory:GetItem(i)
			if (itemStack and itemStack.count > 0) then
				if (itemStack.id == block_types.names.TimeSeriesNPC) then
					if(itemStack:GetDisplayName() == actorName) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end
			end 
		end
	end
end

function Actor:SetMovieBlockPosition(pos)
	if(type(pos) == "table" and pos[1] and pos[2] and pos[3]) then
		local x, y, z = unpack(pos);
		local movie_entity = BlockEngine:GetBlockEntity(x,y,z)
		
		if (movie_entity and movie_entity.class_name == "EntityMovieClip" and  movie_entity.inventory 
			and movie_entity ~= self:GetMovieClipEntity()) then
			for i = 1, movie_entity.inventory:GetSlotCount() do
				local itemStack = movie_entity.inventory:GetItem(i)
				if (itemStack and itemStack.count > 0) then
					if (itemStack.id == block_types.names.TimeSeriesNPC) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end 
			end
		end
	end
end

-- @return {x,y,z} array
function Actor:GetMovieBlockPosition()
	local movie_entity = self:GetMovieClipEntity()
	if(movie_entity) then
		local x, y, z = movie_entity:GetBlockPos()
		return {x, y, z}
	end
end


function Actor:GetTime()
	return self.time or 0;
end

function Actor:SetTime(time)
	self.time = time;
end

function Actor:GetOpacity()
	return self:GetEntity() and self:GetEntity():GetOpacity() or 1;
end

function Actor:SetOpacity(opacity)
	local entity = self:GetEntity();
	if(entity) then	
		if(type(opacity) == "number") then
			entity:SetOpacity(opacity);
		end
	end
end

function Actor:GetIsBlocker()
	return self:GetEntity() and self:GetEntity():IsStaticBlocker();
end

function Actor:SetIsBlocker(bBlocker)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetStaticBlocker(bBlocker == true);
	end
end

function Actor:SetBillboarded(att)
	local entity = self:GetEntity();
	if entity then
		local obj = entity:GetInnerObject();
		if obj then
			obj:SetField("billboarded", att.yaw == true);
			obj:SetField("billboardedRoll", att.roll == true);
			obj:SetField("billboardedPitch", att.pitch == true);
		end
	end
end

function Actor:IsBillboarded()
	local entity = self:GetEntity();
	if entity then
		local obj = entity:GetInnerObject();
		if obj then
			return obj:GetField("billboarded"), obj:GetField("billboardedRoll"), obj:GetField("billboardedPitch");
		end
	end
	
	return false, false, false;
end

-- @param speed: default to 4 m/s
function Actor:SetWalkSpeed(speed)
	local entity = self:GetEntity();
	if entity then
		if(type(speed) == "string") then
			speed = tonumber(speed)
		end
		if(type(speed) == "number") then
			entity:SetWalkSpeed(speed)
		end
	end
end

function Actor:GetWalkSpeed()
	local entity = self:GetEntity();
	return entity and entity:GetWalkSpeed()
end

-- @param effectId: 0 will use unlit biped selection effect. 1 will use yellow border style. -1 to disable it.
function Actor:SetSelectionEffect(effectId)
	local entity = self:GetEntity();
	if entity then
		if(type(effectId) == "string") then
			effectId = tonumber(effectId)
		end
		if(type(effectId) == "number") then
			entity:SetSelectionEffect(effectId)
		end
	end
end

function Actor:GetSelectionEffect()
	local entity = self:GetEntity();
	return entity and entity:GetSelectionEffect()
end


function Actor:SetShaderCaster(enabled)
	local entity = self:GetEntity();
	if entity then
		if(type(enabled) == "string") then
			enabled = enabled == "true"
		end
		entity:SetShaderCaster(enabled)
	end
end

function Actor:IsShaderCaster()
	local entity = self:GetEntity();
	return entity and entity:SetShaderCaster()
end

local internalValues = {
	["name"] = {setter = Actor.SetName, getter = Actor.GetName, isVariable = true}, 
	["time"] = {setter = Actor.SetTime, getter = Actor.GetTime, isVariable = true}, 
	["physicsRadius"] = {setter = Actor.SetPhysicsRadius, getter = Actor.GetPhysicsRadius, isVariable = false}, 
	["physicsHeight"] = {setter = Actor.SetPhysicsHeight, getter = Actor.GetPhysicsHeight, isVariable = false}, 
	["isBlocker"] = {setter = Actor.SetIsBlocker, getter = Actor.GetIsBlocker, isVariable = false}, 
	["groupId"] = {setter = Actor.SetGroupId, getter = Actor.GetGroupId, isVariable = false}, 
	["facing"] = {setter = Actor.SetFacingDegree, getter = Actor.GetFacingDegree, isVariable = false}, 
	-- tricky: pitch and roll are reversed
	["pitch"] = {setter = Actor.SetRollDegree, getter = Actor.GetRollDegree, isVariable = false}, 
	["roll"] = {setter = Actor.SetPitchDegree, getter = Actor.GetPitchDegree, isVariable = false}, 
	["x"] = {setter = Actor.SetPosX, getter = Actor.GetPosX, isVariable = false}, 
	["y"] = {setter = Actor.SetPosY, getter = Actor.GetPosY, isVariable = false}, 
	["z"] = {setter = Actor.SetPosZ, getter = Actor.GetPosZ, isVariable = false}, 
	["color"] = {setter = Actor.SetColor, getter = Actor.GetColor, isVariable = false}, 
	["opacity"] = {setter = Actor.SetOpacity, getter = Actor.GetOpacity, isVariable = false}, 
	["selectionEffect"] = {setter = Actor.SetSelectionEffect, getter = Actor.GetSelectionEffect, isVariable = false}, 
	["isAgent"] = {setter = function() end, getter = Actor.IsAgent, isVariable = false}, 
	["assetfile"] = {setter = Actor.SetAssetFile, getter = Actor.GetAssetFile, isVariable = false}, 
	["movieblockpos"] = {setter = Actor.SetMovieBlockPosition, getter = Actor.GetMovieBlockPosition, isVariable = false}, 
	["movieactor"] = {setter = Actor.SetMovieActor, isVariable = false}, 
	["walkSpeed"] = {setter = Actor.SetWalkSpeed, getter = Actor.GetWalkSpeed, isVariable = false}, 
	["billboarded"] = {setter = Actor.SetBillboarded, getter = Actor.IsBillboarded, isVariable = false},
	["shadowCaster"] = {setter = Actor.SetShaderCaster, getter = Actor.IsShaderCaster, isVariable = false},
	["initParams"] = {getter = Actor.GetInitParams, isVariable = false},
}


function Actor:GetActorValue(name)
	local entity = self:GetEntity()
	if(entity and name) then
		if(internalValues[name]) then
			return internalValues[name].getter(self)
		end
		local variables = entity:GetVariables();
		if(variables) then
			return variables:GetVariable(name);
		end
	end
end

function Actor:SetActorValue(name, value)
	local entity = self:GetEntity()
	if(entity and name) then
		if(internalValues[name]) then
			internalValues[name].setter(self, value)
			if(not internalValues[name].isVariable) then
				return
			end
		end
		local variables = entity:GetVariables();
		if(variables) then
			variables:SetVariable(name, value);
		end
	end
end

function Actor:BecomeAgent(entity)
	Actor._super.BecomeAgent(self, entity);

	if(self:IsActorPickingEnabled()) then
		entity:Connect("clicked", self, self.OnClick, "UniqueConnection");
		self:EnableActorPicking(true)
	end
	entity:Connect("collided", self, self.OnCollideWithEntity, "UniqueConnection");
	entity:Connect("valueChanged", self, self.OnEntityPositionChange, "UniqueConnection");
end

--[[
Title: Code Coroutine
Author(s): LiXizhi
Date: 2018/5/30
Desc: call back functions or the main function that must be executed in a separate coroutine. 
All coroutines share the same CodeAPI environment, except for current actor. 
MakeCallbackFunc will restore last actor and coroutine context.
Run the same coroutine multiple times will cause the previous one to stop forever.
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeCoroutine.lua");
local CodeCoroutine = commonlib.gettable("MyCompany.Aries.Game.Code.CodeCoroutine");
local co = CodeCoroutine:new():Init(codeBlock);
co:SetFunction(func)
co:SetActor(actor)
co:Run();
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeActor.lua");
local CodeAPI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeAPI");
local CodeCoroutine = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeCoroutine"));
CodeCoroutine:Signal("finished");

function CodeCoroutine:ctor()
end

function CodeCoroutine:Init(codeBlock)
	self.codeBlock = codeBlock;
	return self;
end

function CodeCoroutine:Destroy()
	CodeCoroutine._super.Destroy(self);
end

function CodeCoroutine:SetFunction(code_func)
	self.code_func = code_func;
end

function CodeCoroutine:AddTimer(timer)
	self.timers = self.timers or {}
	self.timers[timer] = true;
end

function CodeCoroutine:RemoveTimer(timer)
	if(self.timers) then
		self.timers[timer] = nil;
	end
end

function CodeCoroutine:KillAllTimers()
	if(self.timers) then
		for timer, _ in pairs(self.timers) do
			self.codeBlock:KillTimer(timer);
		end
		self.timers = nil;
	end
end

function CodeCoroutine:KillTimer(timer)
	self:RemoveTimer(timer);
	self:GetCodeBlock():KillTimer(timer);
end

-- @important: this function should be called inside coroutine, the caller must ensure that when callbackFunc called, 
-- it should NOT be inside any coroutine. Otherwise one should use MakeCallbackFuncAsync instead. 
function CodeCoroutine:MakeCallbackFunc(callbackFunc)
	return function(...)
		if(not self.isStopped) then
			self:SetCurrentCodeContext();
			if(callbackFunc) then
				callbackFunc(...);
			end
		end
	end
end

-- @important: this function should be called inside coroutine, the callbackFunc is gauranteed NOT to be inside any coroutine, because we use a timer for it. 
-- so it is always safe to call resume inside callbackFunc
function CodeCoroutine:MakeCallbackFuncAsync(callbackFunc)
	return function(p1, p2, p3, p4)
		commonlib.TimerManager.SetTimeout(function()
			if(not self.isStopped) then
				self:SetCurrentCodeContext();
				if(callbackFunc) then
					callbackFunc(p1, p2, p3, p4);
				end
			end	
		end, 0)
	end
end

function CodeCoroutine:SetTimer(callbackFunc, dueTime, period)
	local timer = self:GetCodeBlock():SetTimer(self:MakeCallbackFunc(callbackFunc), dueTime, period);
	self:AddTimer(timer);
	return timer;
end

function CodeCoroutine:SetTimeout(duration, callbackFunc)
	local timer = self:GetCodeBlock():SetTimeout(duration, function(timer)
		self:SetCurrentCodeContext()
		self:RemoveTimer(timer);
		if(callbackFunc and not self.isStopped) then
			callbackFunc(timer);
		end
	end);
	self:AddTimer(timer);
	return timer;
end

function CodeCoroutine:SetActor(actor)
	self.actor = actor;
end

function CodeCoroutine:GetActor()
	return self.actor;
end

function CodeCoroutine:GetCodeBlock()
	return self.codeBlock;
end

-- @return : "running", "dead", "suspended", nil
function CodeCoroutine:GetStatus()
	return self.co and coroutine.status(self.co);
end

function CodeCoroutine:IsRunning()
	return not self.isStopped;
end

-- the coroutine has finished the last line of its code, but it may not be stopped, since it may still contain valid timers such as playing animations. 
function CodeCoroutine:IsFinished()
	return self.isFinished;
end

function CodeCoroutine:SetFinished()
	if(not self.isFinished) then
		self.isFinished = true;
		self:finished();
	end
end

-- when stopped, it can no longer be resumed
function CodeCoroutine:Stop()
	self.isStopped = true;
	self:SetFinished();
	-- we need to stop the last coroutine timers, before starting a new one. 
	self:KillAllTimers();
end

function CodeCoroutine:SetCurrentCodeContext()
	GameLogic.GetCodeGlobal():SetCurrentCoroutine(self);
end

-- Run the same coroutine multiple times will cause the previous one to stop forever.
function CodeCoroutine:Run(msg, onFinishedCallback)
	self:Stop();
	self.isStopped = false;
	self.isFinished = false;
	self.codeBlock:Connect("beforeStopped", self, self.Stop, "UniqueConnection");
	if(self.code_func) then
		self.co = coroutine.create(function()
			local result, r2, r3, r4 = self:RunImp(msg);
			self:SetFinished();
			self.codeBlock:Disconnect("beforeStopped", self, self.Stop);
			if(onFinishedCallback) then
				onFinishedCallback(result, r2, r3, r4);
			end
			return result, r2, r3, r4;
		end)
		local ok, result, r2, r3, r4 = self:Resume();
		if(ok and self.isFinished) then
			return result, r2, r3, r4;
		end
	end
end

local lastErrorCallstack = "";
function CodeCoroutine.handleError(x)
	lastErrorCallstack = commonlib.debugstack(2, 5, 1);
	return x;
end

function CodeCoroutine:RunImp(msg)
	local code_func = self.code_func;
	if(code_func) then
		setfenv(code_func, self:GetCodeBlock():GetCodeEnv());
		local ok, result, r2, r3, r4 = xpcall(code_func, CodeCoroutine.handleError, msg);

		if(not ok) then
			if(result:match("_stop_all_")) then
				self:GetCodeBlock():StopAll();
			elseif(result:match("_restart_all_")) then
				self:GetCodeBlock():RestartAll();
			else
				LOG.std(nil, "error", "CodeCoroutine", "%s\n%s", result, lastErrorCallstack);
				local msg = format(L"运行时错误: %s\n在%s", tostring(result), self:GetCodeBlock():GetFilename());
				self:GetCodeBlock():send_message(msg, "error");
			end
		end
		return result, r2, r3, r4;
	end
end

function CodeCoroutine:Resume(err, msg, p3, p4)
	if(self.co and not self.isStopped) then
		self:SetCurrentCodeContext();
		return coroutine.resume(self.co, err, msg, p3, p4);
	end
end

-- CAUTION: only call this inside coroutine
function CodeCoroutine:Yield()
	if(self.co) then
		return coroutine.yield();
	end
end

--[[
Title: Code API Globals
Author(s): LiXizhi
Date: 2018/5/27
Desc: all global user-defined variables and shared global API in CodeAPI. 
Each world has a single shared global table, we allow users to list and define custom variables inside this table.
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeGlobals.lua");
local CodeGlobals = commonlib.gettable("MyCompany.Aries.Game.Code.CodeGlobals");
local _G = GameLogic.GetCodeGlobal():GetWorldGlobals();
GameLogic.GetCodeGlobal():GetCurrentMetaTable();
GameLogic.GetCodeGlobal():CreateGetTextEvent("msgname");
GameLogic.GetCodeGlobal():BroadcastStartEvent();
-------------------------------------------------------
]]

NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeUI.lua");
NPL.load("(gl)script/ide/System/Windows/Application.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Network/LobbyService/LobbyServer.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Network/LobbyService/LobbyServerViaTunnel.lua");
NPL.load("(gl)script/ide/math/bit.lua");
NPL.load("(gl)script/ide/System/Windows/Mouse.lua");
NPL.load("(gl)script/ide/System/Scene/Viewports/ViewportManager.lua");
local ViewportManager = commonlib.gettable("System.Scene.Viewports.ViewportManager");
local Screen = commonlib.gettable("System.Windows.Screen");
local Mouse = commonlib.gettable("System.Windows.Mouse");
local LobbyServer = commonlib.gettable("MyCompany.Aries.Game.Network.LobbyServer");
local LobbyServerViaTunnel = commonlib.gettable("MyCompany.Aries.Game.Network.LobbyServerViaTunnel");
local Application = commonlib.gettable("System.Windows.Application");
local CodeUI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeUI");
local SelectionManager = commonlib.gettable("MyCompany.Aries.Game.SelectionManager");
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine");
local CodeGlobals = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeGlobals"));

CodeGlobals:Signal("logAdded", function(text) end)

function CodeGlobals:ctor()
	-- exposing these API to globals
	self.shared_API = {
		ipairs = ipairs,
		next = next,
		pairs = pairs,
		tostring = tostring,
		tonumber = tonumber,
	
		type = type,
		unpack = unpack,
		setmetatable = setmetatable,
		getmetatable = getmetatable,
		rawset = rawset,
		rawget = rawget,
		assert = assert,
		math = { abs = math.abs, acos = math.acos, asin = math.asin, 
			  atan = math.atan, atan2 = math.atan2, ceil = math.ceil, cos = math.cos, 
			  cosh = math.cosh, deg = math.deg, exp = math.exp, floor = math.floor, 
			  fmod = math.fmod, frexp = math.frexp, huge = math.huge, 
			  ldexp = math.ldexp, log = math.log, log10 = math.log10, max = math.max, 
			  min = math.min, modf = math.modf, pi = math.pi, pow = math.pow, 
			  rad = math.rad, random = math.random, sin = math.sin, sinh = math.sinh, 
			  sqrt = math.sqrt, tan = math.tan, tanh = math.tanh },
		bit = mathlib.bit,
		string = { byte = string.byte, char = string.char, find = string.find, 
			  format = string.format, gmatch = string.gmatch, gsub = string.gsub, 
			  len = string.len, lower = string.lower, match = string.match, 
			  rep = string.rep, reverse = string.reverse, sub = string.sub, 
			  upper = string.upper },
		format = string.format,
		table = { insert = table.insert, maxn = table.maxn, remove = table.remove, 
			getn = table.getn, sort = table.sort, concat = table.concat },
		os = { clock = os.clock, difftime = os.difftime, time = os.time },
		alert = _guihelper.MessageBox, 
		real = function(bx,by,bz)
			return BlockEngine:real(bx,by,bz);
		end,
		block = function(x,y,z)
			return BlockEngine:block(x,y,z);
		end,
		select = function(block_id)
			GameLogic.SetBlockInRightHand(block_id)
		end,
		set = function(name, value)
			self:SetGlobal(name, value);
		end,
		get = function(name)
			return self:GetGlobal(name);
		end,
		hideVariable = function(name, title)
			CodeUI:HideGlobalData(name, title);
		end,
		tip = function(text, duration, color)
			return GameLogic.AddBBS("CodeGlobals", text and tostring(text), duration, color);
		end,
		-- return blockX, blockY, blockZ, block_id, side
		mousePickBlock = function(picking_dist)
			local result = SelectionManager:MousePickBlock(true, false, false, picking_dist);
			return result.blockX, result.blockY, result.blockZ, result.block_id, result.side;
		end,
		-- get block id and data at given position
		getBlock = function(x,y,z)
			return BlockEngine:GetBlockIdAndData(math.floor(x), math.floor(y), math.floor(z));
		end,
		-- get the block entity: advanced function
		getBlockEntity = function(x, y, z)
			return EntityManager.GetBlockEntity(math.floor(x), math.floor(y), math.floor(z));
		end,
		-- set block id at given position
		setBlock = function(x,y,z, blockId, blockData)
			return BlockEngine:SetBlock(math.floor(x), math.floor(y), math.floor(z), blockId, blockData);
		end,
		-- similar to commonlib.gettable(tabNames) but in page scope.
		-- @param tabNames: table names like "models.users"
		gettable = function(tabNames)
			return commonlib.gettable(tabNames, self:GetCurrentGlobals());
		end,
		-- similar to commonlib.createtable(tabNames) but in world scope.
		-- @param tabNames: table names like "models.users"
		createtable = function (tabNames, init_params)
			return commonlib.createtable(tabNames, init_params, self:GetCurrentGlobals());
		end,
		-- same as commonlib.inherit()
		-- @param baseClass: string or table or nil
		-- @param new_class: string or table or nil
		inherit = function(baseClass, new_class, ctor)
			if(type(baseClass) == "string") then
				baseClass = commonlib.gettable(baseClass, self:GetCurrentGlobals());
			end
			if(type(new_class) == "string") then
				new_class = commonlib.gettable(new_class, self:GetCurrentGlobals());
			end
			return commonlib.inherit(baseClass, new_class, ctor);
		end,
		saveUserData = function(name, value, bIsGlobal, bDeferSave)
			return GameLogic.GetPlayerController():SaveLocalUserWorldData(name, value, bIsGlobal, bDeferSave)
		end,
		loadUserData = function(name, default_value, bIsGlobal)
			return GameLogic.GetPlayerController():LoadLocalUserWorldData(name, default_value, bIsGlobal)
		end,
		saveWorldData = function(name, value, filename)
			return self:SaveWorldData(name, value, filename)
		end,
		loadWorldData = function(name, default_value, filename)
			return self:LoadWorldData(name, default_value, filename)
		end,
		-- @return x,y: x in [-500, 500] range
		getMousePoint = function()
			return self:GetMousePoint();
		end,
		----------------------
		-- @NOTE: the following may not be safe to expose to users
		----------------------
		NPL = { load = NPL.load },
		System = System, 
		commonlib = commonlib, 
		ParaIO = ParaIO,
		GameLogic = GameLogic,
        NplOce = NplOce,
		Game = MyCompany.Aries.Game,
	};

	self:Reset();

	GameLogic:Connect("beforeWorldSaved", self, self.OnWorldSave, "UniqueConnection");
	GameLogic:Connect("frameMoved", self, self.OnFrameMove, "UniqueConnection");
end

-- call this to clear all globals to reuse this class for future use. 
function CodeGlobals:Reset()
	local curGlobals = {};
	self.curGlobals = curGlobals;
	self.cur_co = nil;

	-- look in global table first, and then in shared API. 
	local meta_table = {__index = function(tab, name)
		if(name == "__LINE__") then
			local info = debug.getinfo(2, "l")
			if(info) then
				return info.currentline;
			end
		elseif(name == "co") then
			return self.cur_co;
		elseif(name == "actor") then
			return self.cur_co and self.cur_co:GetActor();
		end
		local value = curGlobals[name];
		if(value==nil) then
			value = self.shared_API[name];
		end
		return value;
	end}
	self.curMetaTable = meta_table;

	self.text_events = {};

	self.actors = {};

	-- active code blocks
	self.codeblocks= {};

	-- world data
	self.worldData = nil;

	-- clear UI if any
	CodeUI:Clear();

	-- TODO: 
	LobbyServer.GetSingleton():Connect("handleMessage", self, self.handleNetworkEvent, "UniqueConnection");
	LobbyServerViaTunnel.GetSingleton():Connect("handleMessage", self, self.handleNetworkEvent, "UniqueConnection");
end

function CodeGlobals:log(obj, ...)
	commonlib.echo(obj, ...);
	if(type(obj) == "string") then
		self:logAdded(string.format(obj, ...));
	else
		self:logAdded(commonlib.serialize_in_length(obj, 100));
	end
end

-- @return x,y: x in [-500, 500] range
function CodeGlobals:GetMousePoint()
	local x, y = Mouse:GetMousePosition();

	local viewport = ViewportManager:GetSceneViewport();
	local screenWidth, screenHeight = Screen:GetWidth()-viewport:GetMarginRight(), Screen:GetHeight() - viewport:GetMarginBottom();

	x = x * 1000 / screenWidth - 500;
	local ry = 1000 * screenHeight / screenWidth
	y = -(y * ry / screenHeight - ry * 0.5);
	return math.floor(x+0.5), math.floor(y+0.5);
end

function CodeGlobals:OnFrameMove()	
	self:BroadcastTextEvent("onTick");
end

function CodeGlobals:OnWorldSave()
	if(self.worldData) then
		for filename, data in pairs(self.worldData) do
			if(data.isDirty_) then
				local filepath = GameLogic.GetWorldDirectory().."codeblockdata/"..filename;
				ParaIO.CreateDirectory(filepath);
				local file = ParaIO.open(filepath, "w");
				if(file:IsValid()) then
					data.isDirty_ = nil;
					local text = commonlib.serialize(data, true)
					if(text) then
						file:write(text,#text);
					end
					file:close();
					LOG.std(nil, "info", "CodeGlobals", "save world data to %s", filepath);
				else
					LOG.std(nil, "warn", "CodeGlobals", "failed to save world data to %s", filepath);
				end
			end
		end
	end
end

-- save data to world directory, usually used in level editor code
-- the actual saving happens when user saved the whole world
-- @param filename: if nil, it defaults to "worlddata"
function CodeGlobals:SaveWorldData(name, value, filename)
	filename = filename or "worlddata"
	if(not self.worldData) then
		self.worldData = {};
	end
	local data = self.worldData[filename];
	if(not data) then
		data = {};
		self.worldData[filename] = data;
	end
	data.isDirty_ = true;
	data[name] = value;
end

function CodeGlobals:LoadWorldData(name, value, filename)
	filename = filename or "worlddata"
	local data = self.worldData and self.worldData[filename]
	if(not data) then
		local filepath = GameLogic.GetWorldDirectory().."codeblockdata/"..filename;
		local file = ParaIO.open(filepath, "r");
		if(file:IsValid()) then
			data = NPL.LoadTableFromString(file:GetText())
			if(type(data) == "table") then
				data.isDirty_ = false;
			end
			file:close();
		end
		self.worldData = self.worldData or {};
		data = data or {};
		self.worldData[filename] = data;
	end
	return data[name or ""];
end

function CodeGlobals:SetCurrentCoroutine(co)
	self.cur_co = co;
end

function CodeGlobals:AddCodeBlock(codeblock)
	self.codeblocks[codeblock:GetBlockName()] = codeblock;
end

function CodeGlobals:RemoveCodeBlock(codeblock)
	if(self.codeblocks[codeblock:GetBlockName()] == codeblock) then
		self.codeblocks[codeblock:GetBlockName()] = nil;
	end
end

function CodeGlobals:GetCodeBlockByName(name)
	return self.codeblocks[name];
end

function CodeGlobals:AddActor(actor)
	self.actors[actor:GetName() or ""] = actor;
	actor:Connect("nameChanged", self, self.OnActorNameChange);
	actor:Connect("beforeRemoved", self, self.RemoveActor);
end

function CodeGlobals:RemoveActor(actor)
	if(self.actors[actor:GetName() or ""] == actor) then
		self.actors[actor:GetName() or ""] = nil;
	end
end

function CodeGlobals:OnActorNameChange(actor, oldName, newName)
	if(oldName and self.actors[oldName] == actor) then
		self.actors[oldName] = nil;
	end
	if(newName) then
		self.actors[newName] = actor;
	end
end

-- return the last added actor by name
function CodeGlobals:GetActorByName(name)
	return self.actors[name];
end

-- @param name: actor name or "@p" for current player
function CodeGlobals:FindEntityByName(name)
	local actor2 = self:GetActorByName(name);
	if(actor2) then
		return actor2:GetEntity();
	elseif(name=="@p") then
		return EntityManager.GetPlayer();
	end
end

-- all user defined variables that is shared by all blocks in the current world
function CodeGlobals:GetCurrentGlobals()
	return self.curGlobals;
end

-- @return mapping of {text, event_object}
function CodeGlobals:GetAllTextEvents()
	return self.text_events;
end

function CodeGlobals:GetTextEvent(text)
	return self.text_events[text];
end

function CodeGlobals:CreateGetTextEvent(text)
	local event = self.text_events[text];
	if(not event) then
		event = commonlib.EventSystem:new();
		self.text_events[text] = event;
	end
	return event;
end

function CodeGlobals:BroadcastStartEvent()
	self:BroadcastTextEvent("start");
end

function CodeGlobals:RegisterKeyPressedEvent(callbackFunc)
	self:CreateGetTextEvent("keyPressedEvent"):AddEventListener("msg", callbackFunc);
end

function CodeGlobals:BroadcastKeyPressedEvent(keyname, param1)
	self:SetAnyKeyDown(true);
	local event = self:GetTextEvent("keyPressedEvent");
	if(event) then
		return event:DispatchEvent({type="msg", keyname = keyname, param1 = param1});
	end
end

function CodeGlobals:UnregisterKeyPressedEvent(callbackFunc)
	self:UnregisterTextEvent("keyPressedEvent", callbackFunc)
end

function CodeGlobals:RegisterBlockClickEvent(callbackFunc)
	self:CreateGetTextEvent("onBlockClicked"):AddEventListener("msg", callbackFunc);
end

function CodeGlobals:BroadcastBlockClickEvent(blockid)
	local event = self:GetTextEvent("onBlockClicked");
	if(event) then
		local result = SelectionManager:MousePickBlock();
		if(result and result.block_id and result.block_id>0 and result.blockX) then
			return event:DispatchEvent({type="msg", blockid = result.block_id, param1 = {
				blockid = result.block_id,
				x = result.blockX, y = result.blockY, z = result.blockZ, side = result.side
			}});
		end
	end
end

function CodeGlobals:UnregisterBlockClickEvent(callbackFunc)
	self:UnregisterTextEvent("onBlockClicked", callbackFunc)
end

function CodeGlobals:HandleGameEvent(event)
	local textEvent = self:GetTextEvent(event:GetType());
	if(textEvent) then
		local msg = event.msg;
		if(not msg) then
			local trigger_entity = EntityManager.GetLastTriggerEntity();
			if(trigger_entity) then
				-- if no message body is provided, we will send the triggering entity name
				-- this is useful to get the source entity's name, such as a network player
				msg = trigger_entity:GetName();
			end
		end
		
		if(event.cmd_text and event.cmd_text~="") then
			msg = event.cmd_text;
		end

		textEvent:DispatchEvent({type="msg", msg = msg,});
	end
end

function CodeGlobals:BroadcastTextEvent(text, msg, onFinishedCallback)
	local event = self:GetTextEvent(text);
	if(event) then
		if(onFinishedCallback) then
			local nHandlerCount = event:GetEventHandlerCount("msg");
			if(nHandlerCount > 1) then
				local oldCallback = onFinishedCallback;
			
				local nCount = 0;
				onFinishedCallback = function()
					nCount = nCount + 1;
					if(nHandlerCount == nCount) then
						oldCallback();
					end
				end;
			end
		end
		event:DispatchEvent({type="msg", msg=msg, onFinishedCallback=onFinishedCallback});
	else
		if(onFinishedCallback) then
			onFinishedCallback();
		end
	end
end

function CodeGlobals:RegisterTextEvent(text, callbackFunc)
	self:CreateGetTextEvent(text):AddEventListener("msg", callbackFunc);
end

function CodeGlobals:UnregisterTextEvent(text, callbackFunc)
	local event = self:GetTextEvent(text);
	if(event) then
		event:RemoveEventListener("msg", callbackFunc);
	end
end

-- try to start lobby server if not started. 
-- @param bSigninIfNot: whether to force signin
function CodeGlobals:CheckLobbyServer(bSigninIfNot)


	--self.isLobbyStarted = LobbyServer.GetSingleton():IsStarted() and LobbyServerViaTunnel.GetSingleton():IsStarted();
	
	local lobbyServerStarted = LobbyServer.GetSingleton():IsStarted();
	local LobbyServerViaTunnelStarted = LobbyServerViaTunnel.GetSingleton():IsStarted();
	
	local function OnLobbyViaTunnelStartedGlobal(_, msg)
		self:UnregisterTextEvent("OnLobbyViaTunnelStartedGlobal", OnLobbyViaTunnelStartedGlobal);
		self.hasAskedSignin = false;
	end
	
	local function OnLobbyStartedGlobal(_, msg)

		self:UnregisterTextEvent("OnLobbyStartedGlobal", OnLobbyStartedGlobal);
		if msg.msg == "true" then
			if not LobbyServerViaTunnelStarted then
				self:RegisterTextEvent("OnLobbyViaTunnelStartedGlobal", OnLobbyViaTunnelStartedGlobal);
				GameLogic.RunCommand("/startLobbyServer -callback OnLobbyViaTunnelStartedGlobal -tunnelhost 1.tunnel.keepwork.com -tunnelport 8099");
			else
				self.hasAskedSignin = false;
			end
		else
			self.hasAskedSignin = false;
		end
	end
	
	local function onSignIn(bSucceed)
		if bSucceed then
			if not lobbyServerStarted then
				self:RegisterTextEvent("OnLobbyStartedGlobal", OnLobbyStartedGlobal);
				GameLogic.RunCommand("/startLobbyServer -callback OnLobbyStartedGlobal");
			else
				OnLobbyStartedGlobal(nil, {msg="true"})
			end
		else
			self.hasAskedSignin = false;
		end
	end
	
	if((not lobbyServerStarted or not LobbyServerViaTunnelStarted) and bSigninIfNot) then
		if(not self.hasAskedSignin) then
			self.hasAskedSignin = true;
			GameLogic.SignIn(L"", onSignIn);
		end
	end
	
	self.isLobbyStarted = lobbyServerStarted or LobbyServerViaTunnelStarted;
	return self.isLobbyStarted;
end

function CodeGlobals:RegisterNetworkEvent(event_name, callbackFunc)
	self:CheckLobbyServer(true);
	local event = self:CreateGetTextEvent(event_name);
	event:AddEventListener("net", callbackFunc);
	
	if event_name == "connect" then
		local clients = LobbyServer.GetSingleton():GetClients();
		for k, v in pairs(clients) do
			event:DispatchEvent({type="net", msg={userinfo = v}});
		end
		
		clients = LobbyServerViaTunnel.GetSingleton():GetClients();
		for k, v in pairs(clients) do
			event:DispatchEvent({type="net", msg={userinfo = v}});
		end
	end
end

function CodeGlobals:UnregisterNetworkEvent(text, callbackFunc, codeblock)
	local event = self:GetTextEvent(text);
	if(event) then
		event:RemoveEventListener("net", callbackFunc);
		if(text == "connect" and event:GetEventListenerCount("net") == 0) then
			LobbyServer.GetSingleton():StopAll();
			LobbyServerViaTunnel.GetSingleton():StopAll()
			self.isLobbyStarted = false;
		end
	end
end

-- send a named message to one computer in the network
-- @param event_name: if nil, we will send an binary stream (msg) to keepworkUsername, 
-- which needs to be nid/ip:port (*8099, \\\\10.27.3.5 8099)
function CodeGlobals:SendNetworkEvent(keepworkUsername, event_name, msg)
	if(not self:CheckLobbyServer()) then
		return
	end

	if(event_name) then
		if LobbyServer.GetSingleton():IsStarted() then
			LobbyServer.GetSingleton():SendTo(keepworkUsername, event_name, msg);
		end
		
		if LobbyServerViaTunnel.GetSingleton():IsStarted() then
			LobbyServerViaTunnel.GetSingleton():SendTo(keepworkUsername, event_name, msg);
		end
	else
		if LobbyServer.GetSingleton():IsStarted() then
			LobbyServer.GetSingleton():SendOriginalMessage(keepworkUsername, msg);
		end
		
		if LobbyServerViaTunnel.GetSingleton():IsStarted() then
			LobbyServerViaTunnel.GetSingleton():SendOriginalMessage(keepworkUsername, msg);
		end
	end
end

-- send a named message to all computers in the network
function CodeGlobals:BroadcastNetworkEvent(event_name, msg)
	if(not self:CheckLobbyServer()) then
		return
	end
	
	if LobbyServer.GetSingleton():IsStarted() then
		LobbyServer.GetSingleton():BroadcastMessage(event_name, msg)
	end
	
	if LobbyServerViaTunnel.GetSingleton():IsStarted() then
		LobbyServerViaTunnel.GetSingleton():BroadcastMessage(event_name, msg)
	end
end

-- when this computer received a message from the network.
-- test code: GameLogic.GetCodeGlobal():handleNetworkEvent("updateScore", {nid="aaa", score=1121})
-- @param event_name: "disconnect", "connect" are two predefined events alongside other user events
-- @param onFinishedCallback: can be nil
function CodeGlobals:handleNetworkEvent(event_name, msg, onFinishedCallback)
	local event = self:GetTextEvent(event_name);
	if(event) then
		event:DispatchEvent({type="net", msg=msg, onFinishedCallback=onFinishedCallback});
	end
end


function CodeGlobals:GetCurrentMetaTable()
	return self.curMetaTable;
end

function CodeGlobals:GetSharedAPI()
	return shared_API;
end

function CodeGlobals:SetGlobal(name, value)
	if(name) then
		self:GetCurrentGlobals()[name] = value
	end
end

function CodeGlobals:GetGlobal(name)
	return name and self:GetCurrentGlobals()[name];
end

-- @param keyname: if nil or "any", it means any key, such as "a-z", "space", "return", "escape"
-- @return "DIK_A" or nil
function CodeGlobals:GetKeyNameFromString(name)
	if(name) then
		local name2 = "DIK_"..string.upper(name);
		if(name and DIK_SCANCODE[name2]) then
			return name2;
		end
	end
end

function CodeGlobals:GetStringFromKeyName(name)
	if(name) then
		return string.lower(name:gsub("^(DIK_)" ,""));
	end
end

function CodeGlobals:IsAnyKeyDown()
	return self.isAnyKeyDown;
end

function CodeGlobals:SetAnyKeyDown(bKeyDown)
	self.isAnyKeyDown = bKeyDown;
end

-- @param keyname: if nil or "any", it means any key, such as "a-z", "space", "return", "escape"
function CodeGlobals:IsKeyPressed(keyname)
	-- ignore key press when UI has focus
	-- TODO: use GetGUI()->IsKeyboardProcessed() in C++, instead of just MCML v2 control
	if(self:IsAnyKeyDown() and not Application:focusWidget()) then
		keyname = self:GetKeyNameFromString(keyname);
		if(keyname) then
			if(ParaUI.IsKeyPressed(DIK_SCANCODE[keyname])) then
				return true;
			end
		end
	end
	return false;
end

--[[
Title: CodeBlockWindow
Author(s): LiXizhi
Date: 2018/5/22
Desc: 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeBlockWindow.lua");
local CodeBlockWindow = commonlib.gettable("MyCompany.Aries.Game.Code.CodeBlockWindow");
CodeBlockWindow.Show(true)
CodeBlockWindow.SetCodeEntity(entityCode);
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Windows/Window.lua")
NPL.load("(gl)script/ide/System/Scene/Viewports/ViewportManager.lua");
NPL.load("(gl)script/ide/System/Windows/Mouse.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/SceneContext/AllContext.lua");
NPL.load("(gl)script/ide/System/Windows/Screen.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeHelpWindow.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Tasks/EditCodeActor/EditCodeActor.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/NplBrowser/NplBrowserLoaderPage.lua");
NPL.load("(gl)script/apps/WebServer/WebServer.lua");
NPL.load("(gl)script/ide/System/Windows/Keyboard.lua");
local Keyboard = commonlib.gettable("System.Windows.Keyboard");
local EditCodeActor = commonlib.gettable("MyCompany.Aries.Game.Tasks.EditCodeActor");
local CodeHelpWindow = commonlib.gettable("MyCompany.Aries.Game.Code.CodeHelpWindow");
local Files = commonlib.gettable("MyCompany.Aries.Game.Common.Files");
local Screen = commonlib.gettable("System.Windows.Screen");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local AllContext = commonlib.gettable("MyCompany.Aries.Game.AllContext");
local Mouse = commonlib.gettable("System.Windows.Mouse");
local ViewportManager = commonlib.gettable("System.Scene.Viewports.ViewportManager");
local NplBrowserLoaderPage = commonlib.gettable("NplBrowser.NplBrowserLoaderPage");
local CodeBlockWindow = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeBlockWindow"));

-- when entity being edited is changed. 
CodeBlockWindow:Signal("entityChanged", function(entity) end)

local code_block_window_name = "code_block_window_";
local page;
local groupindex_hint = 3; 
-- this is singleton class
local self = CodeBlockWindow;

-- show code block window at the right side of the screen
-- @param bShow:
function CodeBlockWindow.Show(bShow)
	if(not bShow) then
		CodeBlockWindow.Close();
	else
        GameLogic.GetFilters():add_filter("OnShowEscFrame", CodeBlockWindow.OnShowEscFrame);
		GameLogic.GetFilters():add_filter("ShowExitDialog", CodeBlockWindow.OnShowExitDialog);
		
		GameLogic:desktopLayoutRequested("CodeBlockWindow");
		GameLogic:Connect("desktopLayoutRequested", CodeBlockWindow, CodeBlockWindow.OnLayoutRequested, "UniqueConnection");
		GameLogic.GetCodeGlobal():Connect("logAdded", CodeBlockWindow, CodeBlockWindow.AddConsoleText, "UniqueConnection");
	
		local _this = ParaUI.GetUIObject(code_block_window_name);
		if(not _this:IsValid()) then
			self.width, self.height, self.margin_right, self.bottom, self.top = self:CalculateMargins();
			_this = ParaUI.CreateUIObject("container", code_block_window_name, "_mr", 0, self.top, self.width, self.bottom);
			_this.zorder = -2;
			_this.background="";
			_this:SetScript("onsize", function()
				CodeBlockWindow:OnViewportChange();
			end)
			local viewport = ViewportManager:GetSceneViewport();
			viewport:SetMarginRight(self.margin_right);
			viewport:SetMarginRightHandler(self);
			viewport:Connect("sizeChanged", CodeBlockWindow, CodeBlockWindow.OnViewportChange, "UniqueConnection");

			_this:SetScript("onclick", function() end); -- just disable click through 
			_guihelper.SetFontColor(_this, "#ffffff");
			_this:AttachToRoot();
			page = System.mcml.PageCtrl:new({url="script/apps/Aries/Creator/Game/Code/CodeBlockWindow.html"});
			page:Create(code_block_window_name.."page", _this, "_fi", 0, 0, 0, 0);
		end

		_this.visible = true;
		CodeBlockWindow:OnViewportChange();
		local viewport = ViewportManager:GetSceneViewport();
		viewport:SetMarginRight(self.margin_right);
		viewport:SetMarginRightHandler(self);

		GameLogic:Connect("beforeWorldSaved", CodeBlockWindow, CodeBlockWindow.OnWorldSave, "UniqueConnection");

		CodeBlockWindow:LoadSceneContext();
	end
end

function CodeBlockWindow.OnShowEscFrame(bShow)
	if(bShow or bShow == nil) then
		CodeBlockWindow.SetNplBrowserVisible(false)
	end
	return bShow;
end

function CodeBlockWindow.OnShowExitDialog(p1)
	CodeBlockWindow.SetNplBrowserVisible(false);
	return p1;
end

function CodeBlockWindow:OnLayoutRequested(requesterName)
	if(requesterName ~= "CodeBlockWindow") then
		if(CodeBlockWindow.IsVisible()) then
			CodeBlockWindow.Show(false);
		end
	end
end

-- @return width, height, margin_right, margin_bottom, margin_top
function CodeBlockWindow:CalculateMargins()
	local MAX_3DCANVAS_WIDTH = 800;
	local MIN_CODEWINDOW_WIDTH = 200+350;
	local viewport = ViewportManager:GetSceneViewport();
	local width = math.max(math.floor(Screen:GetWidth() * 1/3), MIN_CODEWINDOW_WIDTH);
	local halfScreenWidth = math.floor(Screen:GetWidth()/2);
	if(halfScreenWidth > MAX_3DCANVAS_WIDTH) then
		width = halfScreenWidth;
	elseif((Screen:GetWidth() - width) > MAX_3DCANVAS_WIDTH) then
		width = Screen:GetWidth() - MAX_3DCANVAS_WIDTH;
	end

	local bottom = math.floor(viewport:GetMarginBottom() / Screen:GetUIScaling()[2]);
	local margin_right = math.floor(width * Screen:GetUIScaling()[1]);
	local margin_top = math.floor(viewport:GetTop() / Screen:GetUIScaling()[2]);
	return width, Screen:GetHeight()-bottom-margin_top, margin_right, bottom, margin_top;
end

function CodeBlockWindow:OnViewportChange()
	if(CodeBlockWindow.IsVisible()) then
		-- TODO: use a scene/ui layout manager here
		local width, height, margin_right, bottom, top = self:CalculateMargins();
		if(self.width ~= width or self.height ~= height) then
			self.width = width;
			self.height = height;
			self.margin_right = margin_right;
			self.bottom = bottom;
			self.top = top;
			local viewport = ViewportManager:GetSceneViewport();
			viewport:SetMarginRight(self.margin_right);
			viewport:SetMarginRightHandler(self);
			local _this = ParaUI.GetUIObject(code_block_window_name);
			_this:Reposition("_mr", 0, self.top, self.width, self.bottom);
			if(page) then
				CodeBlockWindow.UpdateCodeToEntity();
				page:Rebuild();
			end
		end

	end
end

function CodeBlockWindow.OnWorldSave()
	CodeBlockWindow.UpdateCodeToEntity();
end

function CodeBlockWindow.HighlightCodeEntity(entity)
	if(self.entity) then
		local x, y, z = self.entity:GetBlockPos();
		ParaTerrain.SelectBlock(x,y,z, false, groupindex_hint);
	end
	if(entity) then
		local x, y, z = entity:GetBlockPos();
		ParaTerrain.SelectBlock(x,y,z, true, groupindex_hint);
	end
end

function CodeBlockWindow:OnEntityRemoved()
	CodeBlockWindow.SetCodeEntity(nil);
end

function CodeBlockWindow.RestoreCursorPosition()
	if(self.entity and self.entity.cursorPos) then
		commonlib.TimerManager.SetTimeout(function()  
			local ctrl = CodeBlockWindow.GetTextControl();
			if(ctrl) then
				if(self.entity and self.entity.cursorPos) then
					local cursorPos = self.entity.cursorPos;
					ctrl:moveCursor(cursorPos.line, cursorPos.pos, false, true);
				end
			end
		end, 200);
	end
end

function CodeBlockWindow.SetCodeEntity(entity)
	CodeBlockWindow.HighlightCodeEntity(entity);
	local isEntityChanged = false;
	if(self.entity ~= entity) then
		if(entity) then
			entity:Connect("beforeRemoved", self, self.OnEntityRemoved, "UniqueConnection");
			entity:Connect("editModeChanged", self, self.UpdateEditModeUI, "UniqueConnection");
		end
		if(self.entity) then
			local codeBlock = self.entity:GetCodeBlock();
			if(not self.entity:IsPowered() and (codeBlock and codeBlock:IsLoaded() or codeBlock:HasRunningTempCode())) then
				if(not self.entity:IsEntitySameGroup(entity)) then
					self.entity:Stop();
				end
			end

			self.entity:Disconnect("beforeRemoved", self, self.OnEntityRemoved);
			self.entity:Disconnect("editModeChanged", self, self.UpdateEditModeUI);
			CodeBlockWindow.UpdateCodeToEntity();
		end
		self.entity = entity;
		if(page) then
			page:Refresh(0.01);
		end
		CodeBlockWindow.RestoreCursorPosition();
		isEntityChanged = true;
	end

	local codeBlock = self.GetCodeBlock();
	if(codeBlock) then
		local text = codeBlock:GetLastMessage() or "";
		if(text == "" and not CodeBlockWindow.GetMovieEntity()) then
			if(self.entity) then
				if(self.entity:AutoCreateMovieEntity()) then
					text = L"我们在代码方块旁边自动创建了一个电影方块! 你现在可以用代码控制电影方块中的演员了!";
				else
					text = L"没有找到电影方块! 请将一个包含演员的电影方块放到代码方块的旁边，就可以用代码控制演员了!";
				end
			end
		end
		self.SetConsoleText(text);

		codeBlock:Connect("message", self, self.OnMessage, "UniqueConnection");
	end
	if(isEntityChanged) then
		CodeBlockWindow.UpdateCodeEditorStatus()

		if(EditCodeActor.GetInstance() and EditCodeActor.GetInstance():GetEntityCode() ~= entity and entity) then
			local task = EditCodeActor:new():Init(CodeBlockWindow.GetCodeEntity());
			task:Run();
		end

		self:entityChanged(self.entity);
	end
	if(not entity) then
		CodeBlockWindow.CloseEditorWindow()
	end
end

function CodeBlockWindow:OnMessage(msg)
	self.SetConsoleText(msg or "");
end

function CodeBlockWindow.GetCodeFromEntity()
	if(self.entity) then
		return self.entity:GetCommand();
	end
end

function CodeBlockWindow.GetCodeEntity(bx, by, bz)
	if(bx) then
		local codeEntity = BlockEngine:GetBlockEntity(bx, by, bz)
		if(codeEntity and codeEntity.class_name == "EntityCode") then
			return codeEntity;
		end
	else
		return CodeBlockWindow.entity;
	end
end

function CodeBlockWindow.GetCodeBlock()
	if(self.entity) then
		return self.entity:GetCodeBlock(true);
	end
end

function CodeBlockWindow.GetMovieEntity()
	local codeBlock = CodeBlockWindow.GetCodeBlock();
	if(codeBlock) then
		return codeBlock:GetMovieEntity();
	end
end

function CodeBlockWindow.IsVisible()
	return page and page:IsVisible();
end

function CodeBlockWindow.Close()
	GameLogic.GetCodeGlobal():Disconnect("logAdded", CodeBlockWindow, CodeBlockWindow.AddConsoleText);
	CodeBlockWindow:UnloadSceneContext();
	CodeBlockWindow.CloseEditorWindow();
	CodeBlockWindow.lastBlocklyUrl = nil;
end

function CodeBlockWindow.CloseEditorWindow()
	CodeBlockWindow.RestoreWindowLayout()
	CodeBlockWindow.UpdateCodeToEntity();
	CodeBlockWindow.HighlightCodeEntity(nil);

	local codeBlock = CodeBlockWindow.GetCodeBlock();
	if(codeBlock and codeBlock:GetEntity()) then
		local entity = codeBlock:GetEntity();
		if(entity:IsPowered() and (not codeBlock:IsLoaded() or codeBlock:HasRunningTempCode())) then
			entity:Restart();
		elseif(not entity:IsPowered() and (codeBlock:IsLoaded() or codeBlock:HasRunningTempCode())) then
			entity:Stop();
		end
	end
    CodeBlockWindow.SetNplBrowserVisible(false);
end

function CodeBlockWindow.RestoreWindowLayout()
	local _this = ParaUI.GetUIObject(code_block_window_name)
	if(_this:IsValid()) then
		_this.visible = false;
	end
	local viewport = ViewportManager:GetSceneViewport();
	if(viewport:GetMarginRightHandler() == self) then
		viewport:SetMarginRightHandler(nil);
		viewport:SetMarginRight(0);
	end
end

function CodeBlockWindow.UpdateCodeToEntity()
	local entity = CodeBlockWindow.GetCodeEntity()
	if(page and entity) then
		local code = page:GetUIValue("code");
		if(not entity:IsBlocklyEditMode()) then
			entity:SetNPLCode(code);

			local ctl = CodeBlockWindow.GetTextControl();
			if(ctl) then
				entity.cursorPos = ctl:CursorPos();
			end
		end
	end
end

function CodeBlockWindow.DoTextLineWrap(text)
	local lines = {};
	for line in string.gmatch(text or "", "([^\r\n]*)\r?\n?") do
		while (line) do
			local remaining_text;
			line, remaining_text = _guihelper.TrimUtf8TextByWidth(line, self.width or 300, "System;12;norm");
			lines[#lines+1] = line;
			line = remaining_text
		end
	end
	return table.concat(lines, "\n");
end

function CodeBlockWindow.SetConsoleText(text)
	if(self.console_text ~= text) then
		self.console_text = text;
		self.console_text_linewrapped = CodeBlockWindow.DoTextLineWrap(self.console_text) or "";
		if(page) then
			page:SetValue("console", self.console_text_linewrapped);
		end
	end
end

function CodeBlockWindow:AddConsoleText(text)
	if(page) then
		local textAreaCtrl = page:FindControl("console");
		local textCtrl = textAreaCtrl and textAreaCtrl.ctrlEditbox;
		if(textCtrl) then
			textCtrl = textCtrl:ViewPort();
			if(textCtrl) then
				for line in text:gmatch("[^\r\n]+") do
					textCtrl:AddItem(line)
				end
				textCtrl:DocEnd();
			end
		end
	end
end

function CodeBlockWindow.GetConsoleText()
	return self.console_text_linewrapped or self.console_text;
end

function CodeBlockWindow.OnClickStart()
	GameLogic.RunCommand("/sendevent start");
end

function CodeBlockWindow.OnClickPause()
	local codeBlock = CodeBlockWindow.GetCodeBlock();
	if(codeBlock) then
		codeBlock:Pause();
	end
end

function CodeBlockWindow.OnClickStop()
	local codeBlock = CodeBlockWindow.GetCodeBlock();
	if(codeBlock) then
		codeBlock:StopAll();
	end
end

function CodeBlockWindow.OnClickCompileAndRun()
	local codeBlock = CodeBlockWindow.GetCodeBlock();
	local codeEntity = CodeBlockWindow.GetCodeEntity();
	if(codeBlock and codeBlock:GetEntity()) then
		-- GameLogic.GetFilters():apply_filters("user_event_stat", "code", "execute", nil, nil);
		CodeBlockWindow.UpdateCodeToEntity();
		codeBlock:GetEntity():Restart();
	end
end

function CodeBlockWindow.OnClickCodeActor()
	local movieEntity = CodeBlockWindow.GetMovieEntity();
	if(movieEntity) then
		if(mouse_button=="left") then
			local codeBlock = CodeBlockWindow.GetCodeBlock();
			if(codeBlock) then
				codeBlock:HighlightActors();

				local task = EditCodeActor:new():Init(CodeBlockWindow.GetCodeEntity());
				task:Run();
			end
		else
			movieEntity:OpenEditor("entity");
		end
	else
		_guihelper.MessageBox(L"没有找到电影方块! 请将一个包含演员的电影方块放到代码方块的旁边，就可以用代码控制演员了!")
	end
end

function CodeBlockWindow.OnChangeFilename()
	if(self.entity) then
		if(page) then
			local filename = page:GetValue("filename");
			self.entity:SetDisplayName(filename);
		end
	end
end

function CodeBlockWindow.GetFilename()
	if(self.entity) then
		return self.entity:GetDisplayName();
	end
end

function CodeBlockWindow.RunTempCode(code, filename)
	local codeBlock = CodeBlockWindow.GetCodeBlock();
	if(codeBlock) then
		codeBlock:RunTempCode(code, filename);
	end
end

function CodeBlockWindow.ShowHelpWndForCodeName(name)
	CodeBlockWindow.ShowHelpWnd("script/apps/Aries/Creator/Game/Code/CodeHelpItemTooltip.html?showclose=true&name="..name);
end

function CodeBlockWindow.RefreshPage(time)
	CodeBlockWindow.UpdateCodeToEntity()
	if(page) then
		page:Refresh(time or 0.01);
	end
end

function CodeBlockWindow.ShowHelpWnd(url)
	if(url and url~="") then
		self.helpWndUrl = url;
		self.isShowHelpWnd = true;
		if(page) then
			page:SetValue("helpWnd", url);
			CodeBlockWindow.RefreshPage();
		end
	else
		self.isShowHelpWnd = false;
		CodeBlockWindow.RefreshPage();
	end
end

function CodeBlockWindow.GetHelpWndUrl()
	return self.helpWndUrl;
end

function CodeBlockWindow.IsShowHelpWnd()
	return self.isShowHelpWnd;
end

function CodeBlockWindow.OnChangeModel()
	local codeBlock = CodeBlockWindow.GetCodeBlock()
	if(codeBlock) then
		local actor;
		local movieEntity = self.entity:FindNearByMovieEntity()	
		if(movieEntity and not movieEntity:GetFirstActorStack()) then
			movieEntity:CreateNPC();
			CodeBlockWindow:GetSceneContext():UpdateCodeBlock();
		end

		local sceneContext = CodeBlockWindow:GetSceneContext();
		if(sceneContext) then
			actor = sceneContext:GetActor()
		end
		actor = actor or codeBlock:GetActor();
		if(not actor) then
			-- auto create movie block and an NPC entity if no movie actor is found
			if(self.entity) then
				local movieEntity = self.entity:FindNearByMovieEntity()	
				if(not movieEntity) then
					self.entity:AutoCreateMovieEntity()
					movieEntity = self.entity:FindNearByMovieEntity()	
				end
				if(movieEntity and not movieEntity:GetFirstActorStack()) then
					movieEntity:CreateNPC();
					CodeBlockWindow:GetSceneContext():UpdateCodeBlock();
					actor = sceneContext:GetActor();
				end
			end
		end
		if(actor) then
			actor:SetTime(0);
			actor:CreateKeyFromUI("assetfile", function(bIsAdded)
				if(bIsAdded) then
					-- do something?					
				end
				if(codeBlock:IsLoaded()) then
					CodeBlockWindow.OnClickCompileAndRun();
				else
					CodeBlockWindow:GetSceneContext():UpdateCodeBlock();
				end
			end);
		end
		CodeBlockWindow.SetNplBrowserVisible(false)
	end
end

function CodeBlockWindow.OnDragEnd(name)
end


function CodeBlockWindow.IsMousePointerInCodeEditor()
	if(page) then
		local x, y = Mouse:GetMousePosition()
		local textAreaCtrl = page:FindControl("code");
		if(textAreaCtrl.window) then
			local ctrlX, ctrlY = textAreaCtrl.window:GetScreenPos();
			if(ctrlX and x > ctrlX and y>ctrlY) then
				return true;
			end
		end
	end
end

-- @return textcontrol, multilineEditBox control.
function CodeBlockWindow.GetTextControl()
	if(page) then
		local textAreaCtrl = page:FindControl("code");
		local textCtrl = textAreaCtrl and textAreaCtrl.ctrlEditbox;
		if(textCtrl) then
			return textCtrl:ViewPort(), textCtrl;
		end
	end
end

	
-- @param bx, by, bz: if not nil, we will only insert when they match the current code block.
function CodeBlockWindow.ReplaceCode(code, bx, by, bz)
	if(CodeBlockWindow.IsSameBlock(bx, by, bz)) then
		local textCtrl = CodeBlockWindow.GetTextControl();
		if(textCtrl) then
			textCtrl:SetText(code or "");
			return true;
		end
	else
		if(bx and by and bz) then
			local codeEntity = CodeBlockWindow.GetCodeEntity(bx, by, bz)
			if(codeEntity) then
				if(not codeEntity:IsBlocklyEditMode()) then
					codeEntity:SetNPLCode(code);
				end
				return true;
			end
		end
		return false;
	end
end

-- @param bx, by, bz: we will return false if they do not match the current block. 
-- @return  it will also return true if input are nil
function CodeBlockWindow.IsSameBlock(bx, by, bz)
	if(bx and by and bz) then
		local entity = CodeBlockWindow.GetCodeEntity();
		if(entity) then
			local cur_bx, cur_by, cur_bz = entity:GetBlockPos();
			if(cur_bx==bx and cur_by == by and cur_bz==bz) then
				-- same block ready to go
			else
				return false;
			end
		end
	end
	return true;
end

-- @param blockly_xmlcode: xml text for blockly
-- @param code: this is the generated NPL code, should be readonly until we have two way binding. 
-- @param bx, by, bz: if not nil, we will only insert when they match the current code block.
function CodeBlockWindow.UpdateBlocklyCode(blockly_xmlcode, code, bx, by, bz)
	local codeEntity = CodeBlockWindow.GetCodeEntity(bx, by, bz);
	if(codeEntity) then
		codeEntity:SetBlocklyEditMode(true);
		codeEntity:SetBlocklyXMLCode(blockly_xmlcode);
		codeEntity:SetBlocklyNPLCode(code);

		if(CodeBlockWindow.IsSameBlock(bx, by, bz)) then
			CodeBlockWindow.ReplaceCode(code, bx, by, bz)
		end
	end
end

-- @param bx, by, bz: if not nil, we will only insert when they match the current code block.
function CodeBlockWindow.InsertCodeAtCurrentLine(code, forceOnNewLine, bx, by, bz)
	if(not CodeBlockWindow.IsSameBlock(bx, by, bz) or CodeBlockWindow.IsBlocklyEditMode()) then
		return false;
	end

	if(code and page) then
		local textAreaCtrl = page:FindControl("code");
		
		local textCtrl = textAreaCtrl and textAreaCtrl.ctrlEditbox;
		if(textCtrl) then
			textCtrl = textCtrl:ViewPort();
			if(textCtrl) then
				local text = textCtrl:GetLineText(textCtrl.cursorLine);
				if(text) then
					text = tostring(text);
					if(forceOnNewLine) then
						local newText = "";
						if(text:match("%S")) then
							-- always start a new line if current line is not empty
							textCtrl:LineEnd(false);
							textCtrl:InsertTextInCursorPos("\n");
							textCtrl:InsertTextInCursorPos(code);
						else
							textCtrl:InsertTextInCursorPos(code);
						end
					else
						textCtrl:InsertTextInCursorPos(code);
					end
					-- set focus to control. 
					if(textAreaCtrl and textAreaCtrl.window) then
						textAreaCtrl.window:SetFocus_sys();
						textAreaCtrl.window:handleActivateEvent(true)
					end
					return true;
				end
			end
		end
	end
end

function CodeBlockWindow.IsBlocklyEditMode()
	local entity = CodeBlockWindow.GetCodeEntity()
	if(entity) then
		return entity:IsBlocklyEditMode()
	end
end

function CodeBlockWindow.UpdateCodeEditorStatus()
	local textCtrl = CodeBlockWindow.GetTextControl();
	if(textCtrl) then
		local bReadOnly = CodeBlockWindow.IsBlocklyEditMode();
		textCtrl:setReadOnly(bReadOnly)
	end
	local entity = CodeBlockWindow.GetCodeEntity()
	if(entity) then
		CodeHelpWindow.SetLanguageConfigFile(entity:GetLanguageConfigFile());
	end
end

-- default to standard NPL language. One can create domain specific language configuration files. 
function CodeBlockWindow.OnClickSelectLanguageSettings()
	local entity = CodeBlockWindow.GetCodeEntity()
	if(not entity) then
		return
	end
	local old_value = entity:GetLanguageConfigFile();
	NPL.load("(gl)script/apps/Aries/Creator/Game/GUI/OpenFileDialog.lua");
	local OpenFileDialog = commonlib.gettable("MyCompany.Aries.Game.GUI.OpenFileDialog");
	OpenFileDialog.ShowPage('<a class="linkbutton_yellow" href="https://github.com/nplpackages/paracraft/wiki/languageConfigFile">'..L"点击查看帮助"..'</a>', function(result)
		if(result) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Code/LanguageConfigurations.lua");
			local LanguageConfigurations = commonlib.gettable("MyCompany.Aries.Game.Code.LanguageConfigurations");
			if(not LanguageConfigurations:IsBuildinFilename(result)) then
				local filename = Files.GetWorldFilePath(result)
				if(not filename) then
					filename = result:gsub("%.npl$", "");
					filename = filename..".npl";

					_guihelper.MessageBox(format("是否要新建语言配置文件:%s", filename), function(res)
						if(res and res == _guihelper.DialogResult.Yes) then
							local fullPath = Files.WorldPathToFullPath(filename);
							ParaIO.CopyFile("script/apps/Aries/Creator/Game/Code/Examples/HelloLanguage.npl", fullPath, false);
							entity:SetLanguageConfigFile(filename);
							CodeBlockWindow.UpdateCodeEditorStatus()
						end
					end, _guihelper.MessageBoxButtons.YesNo);
					_guihelper.MessageBox(L"文件不存在");
					return;
				end
			end
			entity:SetLanguageConfigFile(result);
			CodeBlockWindow.UpdateCodeEditorStatus()
		end
	end, old_value or "", L"选择语言配置文件", "npl");
end

function CodeBlockWindow.OnClickEditMode(name)
	local entity = CodeBlockWindow.GetCodeEntity()
	if(not entity) then
		return
	end
	if(CodeBlockWindow.IsBlocklyEditMode()) then
		if(name == "codeMode") then
			entity:SetBlocklyEditMode(false);
			CodeBlockWindow.UpdateCodeEditorStatus()
		end
	else
		if(name == "blockMode") then
			CodeBlockWindow.UpdateCodeToEntity();
			entity:SetBlocklyEditMode(true);
			CodeBlockWindow.UpdateCodeEditorStatus();
		end
	end
	if(mouse_button == "right") then
		CodeBlockWindow.OnClickSelectLanguageSettings()
	end
	if(name == "blockMode") then
		CodeBlockWindow.OpenBlocklyEditor();
	end
end

function CodeBlockWindow.UpdateEditModeUI()
	local textCtrl, multiLineCtrl = CodeBlockWindow.GetTextControl();
	if(page and textCtrl) then
		if(CodeBlockWindow.IsBlocklyEditMode()) then
			_guihelper.SetUIColor(page:FindControl("blockMode"), "#0b9b3a")
			_guihelper.SetUIColor(page:FindControl("codeMode"), "#808080")
			if(CodeBlockWindow.IsNPLBrowserVisible()) then
				CodeBlockWindow.SetNplBrowserVisible(true);
			end
			multiLineCtrl:SetBackgroundColor("#cccccc")
			local tipCtrl = page:FindControl("blocklyTip");
			if(tipCtrl) then
				tipCtrl.visible = true;
			end
		else
			_guihelper.SetUIColor(page:FindControl("blockMode"), "#808080")
			_guihelper.SetUIColor(page:FindControl("codeMode"), "#0b9b3a")
			CodeBlockWindow.SetNplBrowserVisible(false);
			multiLineCtrl:SetBackgroundColor("#00000000")
			local tipCtrl = page:FindControl("blocklyTip");
			if(tipCtrl) then
				tipCtrl.visible = false;
			end
		end
		
		textCtrl:SetText(CodeBlockWindow.GetCodeFromEntity());
	end
end

-- @param bForceRefresh: whether to refresh the content of the browser according to current blockly code. If nil, it will refresh if url has changed. 
function CodeBlockWindow.SetNplBrowserVisible(bVisible, bForceRefresh)
    if(page)then
		-- block NPL.activate "cef3/NplCefPlugin.dll" if npl browser isn't loaded
        -- so that we can running auto updater normally
        if(not CodeBlockWindow.NplBrowserIsLoaded())then
            return
        end
		page.isNPLBrowserVisible = bVisible;

		if(bVisible and not CodeBlockWindow.temp_nplbrowser_reload)then
			-- tricky: this will create the pe:npl_browser control on first use. 
            CodeBlockWindow.temp_nplbrowser_reload = true;
            page:Rebuild();
        end

		page:CallMethod("nplbrowser_instance","SetVisible",bVisible)
        if(bVisible) then
			if(bForceRefresh == nil) then
				if(self.lastBlocklyUrl ~= CodeBlockWindow.GetBlockEditorUrl()) then
					self.lastBlocklyUrl = CodeBlockWindow.GetBlockEditorUrl();
					bForceRefresh = true;
				end
			end
			if(bForceRefresh) then
				page:CallMethod("nplbrowser_instance","Reload",CodeBlockWindow.GetBlockEditorUrl());
			end
        end
        
    end
end

function CodeBlockWindow.IsNPLBrowserVisible()
	return page and page.isNPLBrowserVisible;
end

function CodeBlockWindow.GetBlockEditorUrl()
    local blockpos;
	local entity = CodeBlockWindow.GetCodeEntity();
	if(entity) then
		local bx, by, bz = entity:GetBlockPos();
		if(bz) then
			blockpos = format("%d,%d,%d", bx, by, bz);
		end
	end

	local request_url = "npl://blockeditor"
	if(blockpos) then
		request_url = request_url..format("?blockpos=%s", blockpos);
	end
    NPL.load("(gl)script/apps/Aries/Creator/Game/Mod/DefaultFilters.lua");
	local DefaultFilters = commonlib.gettable("MyCompany.Aries.Game.DefaultFilters");
	local url = DefaultFilters.cmd_open_url(request_url)
    return url;
end
function CodeBlockWindow.OpenBlocklyEditor()
	local blockpos;
	local entity = CodeBlockWindow.GetCodeEntity();
	if(entity) then
		local bx, by, bz = entity:GetBlockPos();
		if(bz) then
			blockpos = format("%d,%d,%d", bx, by, bz);
		end
	end

	local request_url = "npl://blockeditor"
	if(blockpos) then
		request_url = request_url..format("?blockpos=%s", blockpos);
	end
	NplBrowserLoaderPage.Check(function() 		end);

    if(CodeBlockWindow.NplBrowserIsLoaded() and not Keyboard:IsCtrlKeyPressed())then
		if(not CodeBlockWindow.IsNPLBrowserVisible()) then
			NPL.load("(gl)script/apps/Aries/Creator/Game/Network/NPLWebServer.lua");
			local NPLWebServer = commonlib.gettable("MyCompany.Aries.Game.Network.NPLWebServer");
			local bStarted, site_url = NPLWebServer.CheckServerStarted(function(bStarted, site_url)
				if(bStarted) then
					CodeBlockWindow.SetNplBrowserVisible(true)
				end
			end)
		else
			CodeBlockWindow.SetNplBrowserVisible(false)
		end
	else
		GameLogic.RunCommand("/open "..request_url);
    end
end

function CodeBlockWindow.OnOpenBlocklyEditor()
	local code = CodeBlockWindow.GetCodeFromEntity();
	CodeBlockWindow.OpenBlocklyEditor()
end

function CodeBlockWindow.GetBlockList()
	local blockList = {};
	local entity = self.entity;
	if(entity) then
		entity:ForEachNearbyCodeEntity(function(codeEntity)
			blockList[#blockList+1] = {filename = codeEntity:GetFilename() or L"未命名", entity = codeEntity}
		end);
		table.sort(blockList, function(a, b)
			return a.filename < b.filename;
		end)
	end
	return blockList;
end

function CodeBlockWindow.OnOpenTutorials()
	ParaGlobal.ShellExecute("open", L"https://keepwork.com/official/paracraft/codeblock", "", "", 1);

	GameLogic.GetFilters():apply_filters("user_event_stat", "help", "browse.codeblock", nil, nil);
end

function CodeBlockWindow.OpenExternalFile(filename)
	local filepath = Files.WorldPathToFullPath(filename);
	if(filepath) then
		GameLogic.RunCommand("/open npl://editcode?src="..filepath);
	end
end

-- Redirect this object as a scene context, so that it will receive all key/mouse events from the scene. 
-- as if this task object is a scene context derived class. One can then overwrite
-- `UpdateManipulators` function to add any manipulators. 
function CodeBlockWindow:LoadSceneContext()
	local sceneContext = self:GetSceneContext();
	if(not sceneContext:IsSelected()) then
		sceneContext:activate();
		sceneContext:SetCodeEntity(CodeBlockWindow.GetCodeEntity());
	end
end

function CodeBlockWindow:UnloadSceneContext()
	local sceneContext = self:GetSceneContext();
	if(sceneContext) then
		sceneContext:SetCodeEntity(nil);
	end
	GameLogic.ActivateDefaultContext();
end

function CodeBlockWindow:GetSceneContext()
	if(not self.sceneContext) then
		self.sceneContext = AllContext:GetContext("code");
		CodeBlockWindow:Connect("entityChanged", self.sceneContext, "SetCodeEntity")
	end
	return self.sceneContext;
end
function CodeBlockWindow.NplBrowserIsLoaded()
    return NplBrowserLoaderPage.IsLoaded();
end
CodeBlockWindow:InitSingleton();

--[[
Title: Code Compiler
Author(s): LiXizhi
Date: 2018/5/30
Desc: compiling code, we will inject checkyield() to looping code to avoid infinite loop in coroutine. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeCompiler.lua");
local CodeCompiler = commonlib.gettable("MyCompany.Aries.Game.Code.CodeCompiler");
code_func, errormsg = CodeCompiler:new():SetFilename(virtual_filename):Compile(codeString);
-------------------------------------------------------
]]

local CodeCompiler = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeCompiler"));


local inject_map = {
	{"^(%s*function%A+[^%)]+%)%s*)$", "%1 checkyield();"},
	{"^(%s*local%s+function%W+[^%)]+%)%s*)$", "%1 checkyield();"},
	{"^(%s*for%s.*%s+do%s*)$", "%1 checkyield();"},
	{"^(%s*while%A.*%Ado%s*)$", "%1 checkyield();"},
	{"^(%s*repeat%s*)$", "%1 checkyield();"},
}

local function injectLine_(line)
	for i,v in ipairs(inject_map) do
		line = string.gsub(line, v[1], v[2]);
	end
	return line;
end

function CodeCompiler:ctor()
end

function CodeCompiler:SetFilename(virtual_filename)
	self.filename = virtual_filename;
	return self;
end

function CodeCompiler:GetFilename()
	return self.filename or "";
end


-- we will inject checkyield() such as in: `for do end, while do end, function end`, etc
function CodeCompiler:InjectCheckYieldToCode(code)
	if(code) then
		local lines = {};
		local isInLongString
		for line in string.gmatch(code or "", "([^\r\n]*)\r?\n?") do
			if(isInLongString) then
				lines[#lines+1] = line;	
				isInLongString = line:match("%]%]") == nil;
			else
				isInLongString = line:match("%[%[[^%]]*$") ~= nil;
				lines[#lines+1] = injectLine_(line);	
			end
		end
		code = table.concat(lines, "\n");
		return code;
	end
end

function CodeCompiler:Compile(code)
	if(code and code~="") then
		local code_func, errormsg = loadstring(self:InjectCheckYieldToCode(code), self:GetFilename());
		if(not code_func and errormsg) then
			LOG.std(nil, "error", "CodeBlock", self.errormsg);
		end
		return code_func, errormsg;
	end
end

--[[
Title: Code UI
Author(s): LiXizhi
Date: 2018/6/17
Desc: all code blocks share the same code UI. This is also a paracraft mod.
Code UI contains an array list of Code UI Items, which are layed out in the given order unless explicitly specified. 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeUI.lua");
local CodeUI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeUI");
CodeUI:ShowGlobalData("test", "testTile")
CodeUI:ShowGlobalData("test1")
CodeUI:Show()
GameLogic.GetCodeGlobal():SetGlobal("test", "hello")
GameLogic.GetCodeGlobal():SetGlobal("test1", "world")
CodeUI:Clear()
CodeUI:ShowOverlayPickingBuffer()
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeUIItem.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeGlobals.lua");
NPL.load("(gl)script/ide/System/Windows/Window.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Mod/ModBase.lua");
NPL.load("(gl)script/ide/System/Scene/Overlays/OverlayPicking.lua");
local OverlayPicking = commonlib.gettable("System.Scene.Overlays.OverlayPicking");
local Window = commonlib.gettable("System.Windows.Window")
local CodeGlobals = commonlib.gettable("MyCompany.Aries.Game.Code.CodeGlobals");
local CodeUIItem = commonlib.gettable("MyCompany.Aries.Game.Code.CodeUIItem");

local CodeUI = commonlib.inherit(commonlib.gettable("Mod.ModBase"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeUI"));

CodeUI:Property({"pickingPointSize", 8});

function CodeUI:ctor()
	-- mapping from name to CodeUIItem
	self.items = {};
	self.itemList = commonlib.OrderedArraySet:new();
	self.entityOverlays = {};
end

function CodeUI:GetName()
	return "CodeUI"
end

function CodeUI:GetDesc()
	return "CodeUI is a plugin in paracraft"
end

function CodeUI:init()
	LOG.std(nil, "info", "CodeUI", "plugin initialized");
end

-- static function
function CodeUI.InstallMod()
	local ModManager = commonlib.gettable("Mod.ModManager");
	if(not ModManager:IsModLoaded(CodeUI)) then
		ModManager:AddMod("CodeBlockUI", CodeUI)
	end
end

function CodeUI:Clear()
	self.items = {};
	self.itemList:clear();
	self.entityOverlays = {};
	if(self.window) then
		self.window:Destroy();
	end
end

function CodeUI:GetItem(name)
	return self.items[name];
end

function CodeUI:RemoveItem(name)
	local lastItem = self:GetItem(name);
	if(lastItem) then
		self.items[name] = nil;
		self.itemList:removeByValue(lastItem);
		self:RefreshLayout();
	end
end

function CodeUI:AddItem(item)
	local lastItem = self:GetItem(item.name);
	if(lastItem) then
		if(lastItem~=item) then
			self:RemoveItem(item.name);
		else
			return;
		end
	end
	self.items[item.name] = item;
	self.itemList:add(item);
	self:RefreshLayout();
end

function CodeUI:GetItemNameForGlobalData(name)
	return "g_"..name;
end

function CodeUI:ShowGlobalData(name, title, color)
	local itemName = self:GetItemNameForGlobalData(name)
	local item = self:GetItem(itemName)
	if(not item) then
		item = CodeUIItem:new():Init(itemName, self);
		item:SetGlobalVariableName(name);
		self:AddItem(item);
	end
	if(item) then
		item:SetTitle(title or name);
		if(color) then
			item:SetColor(color);
		end
	end
	return item;
end

function CodeUI:HideGlobalData(name)
	self:RemoveItem(self:GetItemNameForGlobalData(name));
end

function CodeUI:GetWindow()
	local window = self.window;
	if(not window) then
		window = Window:new();
		self.window = window;
	end
	return window;
end

function CodeUI:Show()
	local window = self:GetWindow();
	if(not window:isVisible()) then
		window:Show("__codeUI__", nil, "_fi", 0, 0, 0, 0);
		window:SetEnabled(false);
	end
end

function CodeUI:RefreshLayoutImp()
	local window = self:GetWindow();
	window:deleteChildren();

	local x, y, width, height = 10, 140, 400, 24;
	for i, item in ipairs(self.itemList) do
		item:SetParent(window);
		item:setGeometry(x, y, width, height);
		y = y + height;
	end

	if(#self.itemList > 0) then
		local window = self:GetWindow();
		window:Show();
	end
end

function CodeUI:RefreshLayout()
	self.refrehTimer = self.refrehTimer or commonlib.Timer:new({callbackFunc = function(timer)
		self:RefreshLayoutImp();
	end})
	self.refrehTimer:Change(100, nil);
end

-- @param event: see MouseEvent 
function CodeUI:handleMouseEvent(event)
	if(event:isAccepted()) then
		return
	end

	local pickingName;
	for entity, _ in pairs(self.entityOverlays) do
		if(not pickingName) then
			pickingName = 0;
			-- TODO: only set dirty when overlay has changed since last pick call. 
			OverlayPicking:SetResultDirty(true);
			OverlayPicking:Pick(nil, nil, self.pickingPointSize, self.pickingPointSize)
			pickingName = OverlayPicking:GetActivePickingName() or 0;
			if(pickingName == 0) then
				return
			end
		end
		if(entity:IsVisible() and entity:HasPickingName(pickingName)) then
			entity:event(event);
			if(event:isAccepted()) then
				return true;
			end
			break;
		end
	end
end

function CodeUI:AddEntityOverlay(entity)
	self.entityOverlays[entity] = true;
end

function CodeUI:RemoveEntityOverlay(entity)
	self.entityOverlays[entity] = nil;
end


function CodeUI:ShowOverlayPickingBuffer()
	OverlayPicking:DebugShow("_lt", 10, 10, 128, 128);
end

CodeUI:InitSingleton();

--[[
Title: Code UI Actor
Author(s): LiXizhi
Date: 2018/5/19
Desc: UI actor that is always aligned with camera
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeUIActor.lua");
local CodeUIActor = commonlib.gettable("MyCompany.Aries.Game.Code.CodeUIActor");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/ActorOverlay.lua");
NPL.load("(gl)script/ide/math/vector.lua");
local math3d = commonlib.gettable("mathlib.math3d");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local vector3d = commonlib.gettable("mathlib.vector3d");
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local block_types = commonlib.gettable("MyCompany.Aries.Game.block_types")
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");

local Actor = commonlib.inherit(commonlib.gettable("MyCompany.Aries.Game.Movie.ActorOverlay"), commonlib.gettable("MyCompany.Aries.Game.Code.CodeUIActor"));
Actor:Property("Name", "CodeUIActor");
Actor:Property({"entityClass", "EntityCodeActor"});
Actor:Property({"enableActorPicking", false, "IsActorPickingEnabled", "EnableActorPicking", auto=false});
Actor:Signal("dataSourceChanged");
Actor:Signal("clicked", function(actor, mouseButton) end);
Actor:Signal("beforeRemoved", function(self) end);
Actor:Signal("nameChanged", function(actor, oldName, newName) end);

function Actor:ctor()
	self.offsetPos = vector3d:new(0,0,0);
	self.fromPos = vector3d:new(0,0,0);
	self.offsetYaw = 0;
	self.codeEvents = {};
	self:EnablePicking(false);
end

-- @param itemStack: movie block actor's item stack where time series data source of this entity is stored. 
function Actor:Init(itemStack, movieclipEntity)
	if(not Actor._super.Init(self, itemStack, movieclipEntity)) then
		return;
	end
	local entity = self.entity;
	entity:Connect("clicked", self, self.OnClick);
	entity:Connect("valueChanged", self, self.OnEntityPositionChange);
	return self;
end

function Actor:ApplyInitParams()
	local pos = self:GetInitParam("pos")
	if(pos) then
		local time = self:GetInitParam("startTime") or 0;
		if(self:GetTime() ~= time) then
			self:SetTime(time);
			self:FrameMove(0);
		end

		local entity = self:GetEntity();
		if(entity) then
			if(pos[1] and pos[2] and pos[3]) then
				self:SetBlockPos(pos[1], pos[2], pos[3]);
			end

			local yaw = self:GetInitParam("yaw")
			if(yaw) then
				entity:SetFacing(yaw*3.14/180);
			end
			local pitch = self:GetInitParam("pitch")
			if(pitch) then
				entity:SetPitch(pitch*3.14/180);
			end
			local roll = self:GetInitParam("roll")
			if(roll) then
				entity:SetRoll(roll*3.14/180);
			end

			local scaling = self:GetInitParam("scaling")
			if(scaling) then
				entity:SetScaling(scaling/100);
			end
		end
	end
end

function Actor:IsActorPickingEnabled()
	return self.enableActorPicking;
end

function Actor:EnableActorPicking(bEnabled)
	self.enableActorPicking = bEnabled;
	self:EnablePicking(bEnabled);
	if(self.entity) then
		self.entity:SetSkipPicking(not bEnabled);
	end
end

function Actor:SetName(name)
	if(self.name ~= name) then
		local oldName = self.name;
		self.name = name;
		self:nameChanged(self, oldName, name);
	end
end

function Actor:GetName()
	return self.name;
end

function Actor:OnClick(mouse_button)
	self:clicked(self, mouse_button);
end

function Actor:IsTouchingBlock(block_id)
	return false;
end

function Actor:IsTouchingActorByName(actorname)
	return false;
end

-- @return false;
function Actor:IsTouchingEntity(entity2)
	return false;
end

function Actor:Bounce()
end

function Actor:IsTouchingPlayers()
	return false;
end

function Actor:DistanceTo(actor2)
	return 999999
end

function Actor:DeleteThisActor()
	self:OnRemove();
	self:Destroy();
end

function Actor:OnRemove()
	self:beforeRemoved(self);
	Actor._super.OnRemove(self);
end

function Actor:SetVisible(bVisible)
	local entity = self:GetEntity();
	if(entity) then
		entity:SetVisible(bVisible);
	end
end

function Actor:SetHighlight(bHighlight)
	local entity = self:GetEntity();
	if(entity) then
		entity:SetHighlight(bHighlight);
	end
end

function Actor:SetBlockPos(bx, by, bz)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetDummy(true);
		if(entity:IsScreenMode()) then
			if(bz) then
				entity:SetScreenPos(bx, bz);
			else
				entity:SetScreenPos(bx, by, bz);
			end
		else
			-- we will move using real position which fixed a bug that moveTo() does not work 
			-- when we are already inside the target block
			bx, by, bz = BlockEngine:real_min(bx+0.5, by, bz+0.5);
			entity:SetPosition(bx, by, bz);
		end
	end
end

function Actor:GetPosition()
	local entity = self:GetEntity();
	if(entity) then	
		if(entity:IsScreenMode()) then
			local x, y = entity:GetScreenPos();
			return x, 0, y;
		else
			return entity:GetPosition();
		end
	end
end

function Actor:SetPosition(targetX,targetY,targetZ)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetDummy(true);
		if(entity:IsScreenMode()) then
			if(targetZ) then
				entity:SetScreenPos(targetX, targetZ);
			else
				entity:SetScreenPos(targetX, targetY);
			end
		else
			entity:SetPosition(targetX, targetY, targetZ);
		end
	end
end

function Actor:SetFacingDelta(v)
	local entity = self:GetEntity();
	if(entity) then	
		if(entity:IsScreenMode()) then
			entity:SetRoll(entity:GetRoll() - v);
		else
			entity:SetFacingDelta(v);
		end
		
		if(self:IsPlaying()) then
			self:ResetOffsetPosAndRotation();
		end
	end
end

function Actor:SetFacing(facing)
	local entity = self:GetEntity();
	if(entity) then	
		if(entity:IsScreenMode()) then
			entity:SetRoll(-facing);
		else
			entity:SetFacing(facing);
		end
		
		if(self:IsPlaying()) then
			self:ResetOffsetPosAndRotation();
		end
	end
end

function Actor:GetFacing()
	local entity = self:GetEntity()
	if(entity) then
		if(entity:IsScreenMode()) then
			return -entity:GetRoll();
		else
			return entity:GetFacing();
		end
	end
end

function Actor:IsPlaying()
	if(self.playTimer and self.playTimer:IsEnabled()) then
		return true;
	end
end

function Actor:OnEntityPositionChange()
	if(self:IsPlaying()) then
		self:ResetOffsetPosAndRotation();
	end
end

-- this allows us to play animation in movie block from current movie time to be relative to current entity's position
-- @param time: if nil, it means the current time. 
function Actor:ResetOffsetPosAndRotation()
	local curTime = self:GetTime();
	local entity = self.entity;

	if(not entity or not curTime or entity:IsScreenMode()) then
		return
	end
	local eX, eY, eZ = entity:GetPosition();
	local new_x, new_y, new_z, yaw, roll, pitch = Actor._super.ComputePosAndRotation(self, curTime);
	if(not new_x) then
		new_x, new_y, new_z = eX, eY, eZ;
	end;
	self:SetOffsetPos(eX - new_x, eY - new_y, eZ - new_z, new_x, new_y, new_z);
	self:SetOffsetYaw(entity:GetFacing() - (yaw or 0), yaw);
end

function Actor:ComputeScaling(curTime)
	local scale = self:GetValue("scaling", curTime)
	if(not scale) then
		local entity = self:GetEntity();
		if(entity) then
			scale = entity:GetScaling();
		end
	end
	return scale or 1;
end

function Actor:SetOffsetYaw(yaw)
	self.offsetYaw = yaw;
end

function Actor:GetOffsetYaw()
	return self.offsetYaw;
end

function Actor:SetOffsetPos(dx,dy,dz, fromX, fromY, fromZ)
	self.offsetPos:set(dx,dy,dz);
	self.fromPos:set(fromX, fromY, fromZ);
end

function Actor:GetOffsetPos()
	return self.offsetPos:get();
end

function Actor:ComputePosAndRotation(curTime)
	local new_x, new_y, new_z, yaw, roll, pitch = Actor._super.ComputePosAndRotation(self, curTime);
	
	if(new_x) then
		yaw = yaw or 0;
		local dx,dy,dz = new_x - self.fromPos[1], new_y - self.fromPos[2],  new_z - self.fromPos[3];
		if((dx~=0 or dy~=0 or dz~=0) and self.offsetYaw ~=0) then
			dx, dy, dz = math3d.vec3Rotate(dx,dy,dz, 0, self.offsetYaw, 0);
			new_x, new_y, new_z = self.fromPos[1] + dx, self.fromPos[2] + dy, self.fromPos[3] + dz;
		end
		dx, dy, dz = self:GetOffsetPos();
		return new_x+dx, new_y+dy, new_z+dz, self:GetOffsetYaw() + yaw, roll, pitch;
	end
end

-- if the same event is called multiple times, the previous one is always stopped before a new one is fired. 
function Actor:SetCodeEvent(event, co)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		last_coroutine:Stop();
	end
	self.codeEvents[event] = co;
end

-- if the same event is called multiple times, the previous one is always stopped before a new one is fired. 
function Actor:StopLastCodeEvent(event)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		last_coroutine:Stop();
		self.codeEvents[event] = nil;
	end
end

function Actor:IsRunningEvent(event)
	local last_coroutine = self.codeEvents[event];
	if(last_coroutine) then
		return not last_coroutine:IsFinished();
	end
end

function Actor:SetFocus()
end

function Actor:HasFocus()
	return false;
end

function Actor:RestoreFocus()
end

function Actor:GetColor()
	local entity = self:GetEntity();
	return entity and entity:GetColor();
end

function Actor:SetColor(color)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetColor(color);
	end
end

function Actor:GetDisplayText()
	return self.displayText or self:GetText();
end

function Actor:SetDisplayText(text)
	self.displayText = text;
	self:SetText(text);
end

function Actor:ComputeText(curTime)
	return self.displayText or self:GetValue("text", curTime);
end

function Actor:Say(text, duration)
	self:SetDisplayText(text or "");
end

function Actor:SetFacingDegree(degree)
	self:SetFacing(degree/180*math.pi)
end

function Actor:GetFacingDegree()
	return self:GetFacing()*180/math.pi
end

-- floating point block position
function Actor:SetPosX(x)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(BlockEngine:real_min(x), y_, z_);
end

function Actor:GetPosX()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return x;
end

-- floating point block position
function Actor:SetPosZ(z)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(x_, y_, BlockEngine:real_min(z));
end

function Actor:GetPosZ()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return z;
end

-- floating point block position
function Actor:SetPosY(y)
	local x_, y_, z_ = self:GetPosition();
	self:SetPosition(x_, BlockEngine:realY(y), z_);
end

function Actor:GetPosY()
	local x, y, z = self:GetPosition();
	if(x) then
		x,y,z = BlockEngine:block_float(x, y, z);
	end
	return y;
end

-- set (physics) group id
function Actor:SetGroupId(id)
	self.groupId = id;
end

-- get group id, default to nil
function Actor:GetGroupId()
	return self.groupId;
end

function Actor:SetRollDegree(degree)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetRoll(degree/180*math.pi);
	end
end

function Actor:GetRollDegree()
	local entity = self:GetEntity();
	return entity and (entity:GetRoll()*180/math.pi) or 0;
end

function Actor:SetPitchDegree(degree)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetPitch(degree/180*math.pi);
	end
end

function Actor:GetPitchDegree()
	local entity = self:GetEntity();
	return entity and (entity:GetPitch()*180/math.pi) or 0;
end

function Actor:SetMovieActorImp(itemStack, movie_entity)
	movie_entity = movie_entity or self:GetMovieClipEntity();
	local entity = self:GetEntity()
	if(entity) then
		local x, y, z = entity:GetPosition()
		local facing = entity:GetFacing()
		local wasVisible = entity:IsVisible()
		local variables = entity:GetVariables();
		
		self:DestroyEntity();
		self:Init(itemStack, movie_entity);
		self:FrameMove(self:GetTime(), false);
		entity = self:GetEntity();
		if(not entity:IsScreenMode()) then
			entity:SetPosition(x,y,z);
			entity:SetFacing(facing);
		end
		if(not wasVisible) then
			entity:SetVisible(wasVisible);
		end
		variables:copyTo(entity:GetVariables());
		
		self:EnableActorPicking(self:IsActorPickingEnabled());
	end
end


-- @param actorName: if nil or 1, it is the first one in movie block
-- if number it is the actor index in movie block, if string, it is its actor name
function Actor:SetMovieActor(actorName)
	actorName = actorName or 1;
	local movie_entity = self:GetMovieClipEntity();
	if(not movie_entity) then
		return
	end
	if(type(actorName) == "number") then
		local index = 0;
		for i = 1, movie_entity.inventory:GetSlotCount() do
			local itemStack = movie_entity.inventory:GetItem(i)
			if (itemStack and itemStack.count > 0) then
				if (itemStack.id == block_types.names.TimeSeriesOverlay) then
					index = index + 1;
					if(index == actorName) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end
			end 
		end
	elseif(type(actorName) == "string" and actorName~="") then
		for i = 1, movie_entity.inventory:GetSlotCount() do
			local itemStack = movie_entity.inventory:GetItem(i)
			if (itemStack and itemStack.count > 0) then
				if (itemStack.id == block_types.names.TimeSeriesOverlay) then
					if(itemStack:GetDisplayName() == actorName) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end
			end 
		end
	end
end

function Actor:SetMovieBlockPosition(pos)
	if(type(pos) == "table" and pos[1] and pos[2] and pos[3]) then
		local x, y, z = unpack(pos);
		local movie_entity = BlockEngine:GetBlockEntity(x,y,z)
		
		if (movie_entity and movie_entity.class_name == "EntityMovieClip" and  movie_entity.inventory 
			and movie_entity ~= self:GetMovieClipEntity()) then
			for i = 1, movie_entity.inventory:GetSlotCount() do
				local itemStack = movie_entity.inventory:GetItem(i)
				if (itemStack and itemStack.count > 0) then
					if (itemStack.id == block_types.names.TimeSeriesOverlay) then
						self:SetMovieActorImp(itemStack, movie_entity);
					end
				end 
			end
		end
	end
end

-- @return {x,y,z} array
function Actor:GetMovieBlockPosition()
	local movie_entity = self:GetMovieClipEntity()
	if(movie_entity) then
		local x, y, z = movie_entity:GetBlockPos()
		return {x, y, z}
	end
end

function Actor:GetTime()
	return self.time or 0;
end

function Actor:SetTime(time)
	self.time = time;
end

function Actor:GetOpacity()
	return self:GetEntity() and self:GetEntity():GetOpacity() or 1;
end

function Actor:SetOpacity(opacity)
	local entity = self:GetEntity();
	if(entity) then	
		if(type(opacity) == "number") then
			entity:SetOpacity(opacity);
		end
	end
end

function Actor:SetUserRenderCode(code)
	self.renderCode = code;
	self:SetRenderCode(code);
end

function Actor:GetUserRenderCode(code)
	return self.renderCode;
end

function Actor:ComputeRenderCode(curTime)
	return self.renderCode or self:GetValue("code", curTime);
end

function Actor:GetZOrder()
	return self:GetEntity() and self:GetEntity():GetZOrder() or 0;
end

function Actor:SetZOrder(zorder)
	local entity = self:GetEntity();
	if(entity) then	
		entity:SetZOrder(tonumber(zorder));
	end
end

local internalValues = {
	["name"] = {setter = Actor.SetName, getter = Actor.GetName, isVariable = true}, 
	["time"] = {setter = Actor.SetTime, getter = Actor.GetTime, isVariable = true}, 
	["groupId"] = {setter = Actor.SetGroupId, getter = Actor.GetGroupId, isVariable = false}, 
	["color"] = {setter = Actor.SetColor, getter = Actor.GetColor, isVariable = false}, 
	["opacity"] = {setter = Actor.SetOpacity, getter = Actor.GetOpacity, isVariable = false}, 
	["text"] = {setter = Actor.SetDisplayText, getter = Actor.GetDisplayText, isVariable = false}, 
	["facing"] = {setter = Actor.SetFacingDegree, getter = Actor.GetFacingDegree, isVariable = false}, 
	-- tricky: pitch and roll are reversed
	["pitch"] = {setter = Actor.SetRollDegree, getter = Actor.GetRollDegree, isVariable = false}, 
	["roll"] = {setter = Actor.SetPitchDegree, getter = Actor.GetPitchDegree, isVariable = false}, 
	["x"] = {setter = Actor.SetPosX, getter = Actor.GetPosX, isVariable = false}, 
	["y"] = {setter = Actor.SetPosY, getter = Actor.GetPosY, isVariable = false}, 
	["z"] = {setter = Actor.SetPosZ, getter = Actor.GetPosZ, isVariable = false}, 
	["zorder"] = {setter = Actor.SetZOrder, getter = Actor.GetZOrder, isVariable = false}, 
	["rendercode"] = {setter = Actor.SetUserRenderCode, getter = Actor.GetUserRenderCode,  isVariable = false}, 
	["movieblockpos"] = {setter = Actor.SetMovieBlockPosition, getter = Actor.GetMovieBlockPosition, isVariable = false}, 
	["movieactor"] = {setter = Actor.SetMovieActor, isVariable = false}, 
}


function Actor:GetActorValue(name)
	local entity = self:GetEntity()
	if(entity and name) then
		if(internalValues[name]) then
			return internalValues[name].getter(self)
		end
		local variables = entity:GetVariables();
		if(variables) then
			return variables:GetVariable(name);
		end
	end
end

function Actor:SetActorValue(name, value)
	local entity = self:GetEntity()
	if(entity and name) then
		if(internalValues[name]) then
			internalValues[name].setter(self, value)
			if(not internalValues[name].isVariable) then
				return
			end
		end
		local variables = entity:GetVariables();
		if(variables) then
			variables:SetVariable(name, value);
		end
	end
end

function Actor:BecomeAgent(entity)
end

--[[
Title: CodeAPI
Author(s): LiXizhi
Date: 2018/5/16
Desc: sandbox API environment, see also CodeGlobals for shared API and globals.
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI.lua");
local CodeAPI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeAPI");
local api = CodeAPI:new(codeBlock);
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_Events.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_MotionLooks.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_Sensing.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_Sound.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_Data.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_Control.lua");

-- all public environment methods. 
local s_env_methods = {
	"resume", 
	"yield", 
	"checkyield",
	"GetEntity",
	"restart",
	"exit",
	"xpcall",
	-- Data
	"print",
	"log",
	"echo",
	"setActorValue",
	"getActorValue",
	"showVariable",
	"include",
	"getActor",
	"cmd",

	-- Motion
	"move",
	"moveTo",
	"moveForward",
	"walk",
	"walkForward",
	"turn",
	"turnTo",
	"bounce",
	"velocity",
	"getX",
	"getY",
	"getZ",
	"getFacing",
	"getPos",
	"setPos",
	-- Looks
	"say",
	"show",
	"hide",
	"anim",
	"play",
	"playLoop",
	"playSpeed",
	"playBone",
	"stop",
	"scale",
	"scaleTo",
	"getPlayTime",
	"getScale",
	"focus",
	"camera",
	"setMovie",
	"setMovieProperty",
	"playMovie",
	"stopMovie",

	-- Events
	"registerClickEvent",
	"registerKeyPressedEvent",
	"registerAnimationEvent",
	"registerBroadcastEvent",
	"registerBlockClickEvent",
	"registerTickEvent",
	"registerStopEvent",
	"broadcast",
	"broadcastAndWait",
	"registerNetworkEvent",
	"broadcastNetworkEvent",
	"sendNetworkEvent",

	-- Control
	"wait",
	"waitUntil",
	"registerCloneEvent",
	"clone",
	"delete",
	"run",
	"runForActor",
	"becomeAgent",
	"setOutput",

	-- Sensing
	"isTouching",
	"registerCollisionEvent",
	"broadcastCollision",
	"distanceTo",
	"calculatePushOut",
	"isKeyPressed",
	"isMouseDown",
	"getTimer",
	"resetTimer",
	"ask",

	-- Sound
	"playNote",
	"playSound",
	"stopSound",
	"playMusic",
}
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic")

local CodeAPI = commonlib.gettable("MyCompany.Aries.Game.Code.CodeAPI");
local env_imp = commonlib.gettable("MyCompany.Aries.Game.Code.env_imp");
CodeAPI.__index = CodeAPI;


-- @param actor: CodeActor that this code API is controlling. 
function CodeAPI:new(codeBlock)
	local o = {
		codeblock = codeBlock,
		check_count = 0,
	};
	o._G = GameLogic.GetCodeGlobal():GetCurrentGlobals();

	CodeAPI.InstallMethods(o);
	setmetatable(o, GameLogic.GetCodeGlobal():GetCurrentMetaTable());
	return o;
end

-- install functions to code environment
function CodeAPI.InstallMethods(o)
	for _, func_name in ipairs(s_env_methods) do
		local f = function(...)
			return env_imp[func_name](o, ...);
		end
		o[func_name] = f;
	end
end


-- yield control until all async jobs are completed
-- @param bExitOnError: if true, this function will handle error 
-- @return err, msg: err is true if there is error. 
function env_imp:yield(bExitOnError)
	local err, msg, p3, p4;
	if(self.co) then
		if(self.fake_resume_res) then
			err, msg = unpack(self.fake_resume_res);
			self.fake_resume_res = nil;
			return err, msg;
		else
			self.check_count = 0;
			err, msg, p3, p4 = self.co:Yield();
			if(err and bExitOnError) then
				env_imp.exit(self);
			end
		end
	end
	return err, msg, p3, p4;
end

-- resume from where jobs are paused last. 
-- @param err: if there is error, this is true, otherwise it is nil.
-- @param msg: error message in case err=true
function env_imp:resume(err, msg, p3, p4)
	if(self.co) then
		if(self.co:GetStatus() == "running") then
			self.fake_resume_res = {err, msg, p3, p4};
			return;
		else
			self.fake_resume_res = nil;
		end
		local res, err, msg = self.co:Resume(err, msg, p3, p4);
	end
end

-- calling this function 100 times will automatically yield and resume until next tick (1/30 seconds)
-- we will automatically insert this function into while and for loop. One can also call this manually
function env_imp:checkyield()
	self.check_count = self.check_count + 1;
	if(self.check_count > 100) then
		if(self.codeblock:IsAutoWait()) then
			env_imp.wait(self, env_imp.GetDefaultTick(self));
		else
			self.check_count = 0;
		end
	end
end

-- private: 
function env_imp:GetDefaultTick()
	if(not self.default_tick) then
		self.default_tick = self.codeBlock and self.codeBlock:GetDefaultTick() or 0.02;
	end
	return self.default_tick;
end

--[[
Title: CodeAPI
Author(s): LiXizhi
Date: 2018/5/16
Desc: sandbox API environment
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/CodeAPI_MotionLooks.lua");
-------------------------------------------------------
]]
NPL.load("(gl)script/apps/Aries/Creator/Game/Common/Direction.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/SceneContext/SelectionManager.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Commands/CmdParser.lua");
NPL.load("(gl)script/ide/System/Scene/Cameras/AutoCamera.lua");
NPL.load("(gl)script/apps/Aries/Creator/Game/Movie/MovieManager.lua");
local MovieManager = commonlib.gettable("MyCompany.Aries.Game.Movie.MovieManager");
local Cameras = commonlib.gettable("System.Scene.Cameras");
local CmdParser = commonlib.gettable("MyCompany.Aries.Game.CmdParser");
local SelectionManager = commonlib.gettable("MyCompany.Aries.Game.SelectionManager");
local Direction = commonlib.gettable("MyCompany.Aries.Game.Common.Direction")
local BlockEngine = commonlib.gettable("MyCompany.Aries.Game.BlockEngine")
local EntityManager = commonlib.gettable("MyCompany.Aries.Game.EntityManager");
local GameLogic = commonlib.gettable("MyCompany.Aries.Game.GameLogic");
local env_imp = commonlib.gettable("MyCompany.Aries.Game.Code.env_imp");

-- say some text and wait for some time. 
-- @param text: if nil, it will remove text
-- @param duration: in seconds. if nil, it means forever
function env_imp:say(text, duration)
	if(duration) then
		env_imp.say(self, text);
		env_imp.wait(self, duration);
		env_imp.say(self, nil);
	else
		local actor = env_imp.GetActor(self);
		if(actor) then
			if(text~=nil) then
				text = tostring(text);
			end
			actor:Say(text, -1)
		else
			GameLogic.AddBBS("codeblock", text, 10000);
		end
	end
end

-- walk relative to current block position and make it not dummy(has physics simulations)
-- the entity maybe blocked if target unreachable. 
-- it will move at the default speed. 
-- @param dx,dy,dz: if z is nil, y is z. in block unit, can be real numbers
-- @param duration: default to none
function env_imp:walk(dx,dy,dz, duration)
	if(not dz) then
		dz = dy;
		dy = nil;
	end
	local entity = env_imp.GetEntity(self);
	if(entity) then
		local x,y,z = entity:GetBlockPos();
		x = x + math.floor((dx or 0) + 0.5);
		y = y + math.floor((dy or 0) + 0.5);
		z = z + math.floor((dz or 0) + 0.5);
		if(entity.MoveTo) then
			entity:EnableAnimation(true);
			entity:SetDummy(false);
			entity:WalkTo(x,y,z);
			if(not duration) then
				duration = math.sqrt(dx*dx + dz*dz) * BlockEngine.blocksize / entity:GetWalkSpeed();
			end
			env_imp.wait(self, duration);
		end
	end
end

-- TODO: just in case, we allow user to change rotation style.
local useFourDirectionRotationStyle = false;

-- @param dist: in block unit, can be real numbers
function env_imp:walkForward(dist, duration)
	local entity = env_imp.GetEntity(self);
	if(entity) then
		if(useFourDirectionRotationStyle) then
			local dir = Direction.GetDirectionFromFacing(entity:GetFacing());
			local dx, dy, dz = Direction.GetOffsetBySide(dir);
			env_imp.walk(self, -dx*dist, -dy*dist, -dz*dist, duration);
		else
			local facing = entity:GetFacing()
			env_imp.walk(self, math.cos(facing)*dist, 0, -math.sin(facing)*dist, duration);
		end
	end
end


-- move delta position and wait a tick. unlike walk, it will ignore physics and always move there. 
-- @param dx,dy,dz: if z is nil, y is z. in block unit, can be real numbers.
-- @param duration: seconds to move to the target. default to 1 tick time. 
function env_imp:move(dx,dy,dz, duration)
	if(not dz) then
		dz = dy;
		dy = nil;
	end
	local actor = self.actor;
	if(actor) then
		local x,y,z = actor:GetPosition();
		local targetX = x + (dx or 0)*BlockEngine.blocksize;
		local targetY = y + (dy or 0)*BlockEngine.blocksize;
		local targetZ = z + (dz or 0)*BlockEngine.blocksize;
		if(not duration) then
			actor:SetPosition(targetX,targetY,targetZ);
			env_imp.wait(self, env_imp.GetDefaultTick(self));
		elseif(duration == 0) then
			actor:SetPosition(targetX,targetY,targetZ);
		else
			local endTime = commonlib.TimerManager.GetCurrentTime()/1000 + duration;
			local stepTime = env_imp.GetDefaultTick(self);
			for i=0, math.floor(duration / stepTime) do
				local timeLeft = endTime - commonlib.TimerManager.GetCurrentTime()/1000;
				local stepCount = math.floor(timeLeft/stepTime);
				local x,y,z = actor:GetPosition();
				local dx, dy, dz = targetX - x, targetY - y, targetZ - z;
				if(stepCount>=2) then
					local inverseStep = 1/stepCount;
					dx, dy, dz = dx*inverseStep, dy*inverseStep, dz*inverseStep;	
				end
				env_imp.move(self, dx,dy,dz)
				if(stepCount<2) then
					break;
				end
			end
		end
	end
end

-- same as moveTo, except that we use real coordinate in block unit
function env_imp:setPos(x, y, z)
	local actor = self.actor;
	if(actor) then
		x,y,z = BlockEngine:real_min(x, y, z);
		actor:SetPosition(x, y, z);
	end
end

-- @param objName: nil or "self" or any actor name. if "@p" it means current player
-- same as getX(), getY(), getZ(), except that we return real coordinate in block unit
function env_imp:getPos(objName)
	local actor = self.actor;
	if(objName) then
		if( objName == "@p" ) then
			local x, y, z = EntityManager.GetPlayer():GetPosition()
			return BlockEngine:block_float(x, y, z);
		elseif( objName ~= "self" ) then
			actor = GameLogic.GetCodeGlobal():GetActorByName(objName);
		end
	end
	if(actor) then
		local x, y, z = actor:GetPosition();
		if(x) then
			return BlockEngine:block_float(x, y, z);
		end
	end
end


-- moveTo to a given block position or a actor position
-- @param x,y,z: if z is nil, y is z. 
-- x can also be "mouse-pointer" or "@p" for current player or other actor name, while y and z are nil.
-- x can also be player name + bone name like "myActorName::R_hand" or "myActorName::"
-- if name is "myActorName", we will move the block position of the given player
-- if name is "myActorName::", we will move the float position of the given player
-- if name is "myActorName::bonename", we will move the float position of the given actor's given bone
function env_imp:moveTo(x, y, z)
	local entity = env_imp.GetEntity(self);
	if(entity) then
		if(type(x) == "string") then
			if(x == "mouse-pointer") then
				local result = SelectionManager:MousePickBlock(true, false, false); 
				if(result and result.blockX) then
					local x,y,z = BlockEngine:GetBlockIndexBySide(result.blockX,result.blockY,result.blockZ,result.side);
					env_imp.moveTo(self, x,y,z);
				end
			elseif(type(x) == "string") then
				local entity2 = GameLogic.GetCodeGlobal():FindEntityByName(x);
				if(entity2) then
					local x2, y2, z2 = entity2:GetBlockPos();
					env_imp.moveTo(self, x2, y2, z2);
				else
					local actorName, boneName = x:match("^([^:]+)::(.*)$");
					if(actorName) then
						local actor = GameLogic.GetCodeGlobal():GetActorByName(actorName);
						if(actor and actor.ComputeBoneWorldTransform) then
							local wx, wy, wz = actor:ComputeBoneWorldTransform(boneName)
							if(wx) then
								entity:SetPosition(wx, wy, wz);
							end
						end
					end
				end
			end
		elseif(x and y) then
			if(not z) then
				local ox,oy,oz = entity:GetBlockPos();
				y,z = oy, y;
			end
			self.actor:SetBlockPos(x,y,z);
			env_imp.checkyield(self);
		end
	end
end

-- move forward using current direction
-- @param dist: 1 block unit, can be real number 
-- @param duration: default to 1 tick
function env_imp:moveForward(dist, duration)
	local actor = env_imp.GetActor(self);
	if(actor) then
		if(useFourDirectionRotationStyle) then
			local dir = Direction.GetDirectionFromFacing(actor:GetFacing());
			local dx, dy, dz = Direction.GetOffsetBySide(dir);
			env_imp.move(self, -dx*dist, -dy*dist, -dz*dist, duration);
		else
			local facing = actor:GetFacing()
			env_imp.move(self, math.cos(facing)*dist, 0, -math.sin(facing)*dist, duration);
		end
	end
end

function env_imp:turn(degree)
	if(self.actor) then
		self.actor:SetFacingDelta(degree*math.pi/180);
	end
	env_imp.wait(self, env_imp.GetDefaultTick(self));
end

-- @param degree: [-180, 180] or "mouse-pointer" or "@p" for current player, or any actor name
-- or "camera" for current camera
-- @param pitch, roll: can be nil. or degree can be yaw. pitch can also be "camera"
function env_imp:turnTo(degree, pitch, roll)
	local entity = env_imp.GetEntity(self);
	if(entity) then
		if(roll or pitch) then
			-- tricky: pitch and roll are reversed
			if(type(roll) == "number") then
				entity:SetPitch(roll*math.pi/180)
			end
			if(pitch) then
				if(type(pitch) == "number") then
					entity:SetRoll(pitch*math.pi/180);
				elseif(pitch == "camera") then
					local pos = Cameras:GetCurrent():GetEyePosition()
					local x, y, z = entity:GetPosition();
					local x2, y2, z2 = pos[1], pos[2], pos[3]
					if(x2 ~= x or z2 ~= z) then
						pitch = Direction.GetPitchFromOffset(x2 - x, y2 - y, z2 - z);
						entity:SetRoll(pitch);
					end
				end
			end
		end
		if(degree) then
			if(type(degree) == "number") then
				self.actor:SetFacing(degree*math.pi/180);
			elseif(degree == "mouse-pointer") then
				local result = SelectionManager:MousePickBlock(true, false, false); 
				if(result and result.blockX) then
					local x, y, z = entity:GetBlockPos();
					if(result.blockX ~= x or result.blockZ ~= z) then
						local facing = Direction.GetFacingFromOffset(result.blockX - x, result.blockY - y, result.blockZ - z);
						self.actor:SetFacing(facing);
					end
				end
			elseif(degree == "camera") then
				local pos = Cameras:GetCurrent():GetEyePosition()
				local x, y, z = entity:GetPosition();
				local x2, y2, z2 = pos[1], pos[2], pos[3]
				if(x2 ~= x or z2 ~= z) then
					local facing = Direction.GetFacingFromOffset(x2 - x, y2 - y, z2 - z);
					self.actor:SetFacing(facing);
				end
			elseif(type(degree) == "string") then
				local entity2 = GameLogic.GetCodeGlobal():FindEntityByName(degree);
				if(entity2) then
					local x2, y2, z2 = entity2:GetBlockPos();
					local x, y, z = entity:GetBlockPos();
					if(x2 ~= x or z2 ~= z) then
						local facing = Direction.GetFacingFromOffset(x2 - x, y2 - y, z2 - z);
						self.actor:SetFacing(facing);
					end
				end
			end
		end
	end
	env_imp.checkyield(self);
end

function env_imp:scale(scaleDeltaPercentage)
	local entity = env_imp.GetEntity(self);
	if(entity) then
		entity:SetScalingDelta(scaleDeltaPercentage/100);
	end
	env_imp.wait(self, env_imp.GetDefaultTick(self));
end

function env_imp:scaleTo(scalePercentage)
	local entity = env_imp.GetEntity(self);
	if(entity) then
		entity:SetScaling(scalePercentage/100);
	end
	env_imp.checkyield(self);
end


-- set animation id
-- @param anim_id: 0 for standing (default), 4 for walk. 
-- @param duration: default to 1 tick
function env_imp:anim(anim_id, duration)
	anim_id = anim_id or 0;
	local entity = env_imp.GetEntity(self);
	if(entity) then
		entity:EnableAnimation(true);
		entity:SetAnimation(anim_id);

		if(duration) then
			env_imp.wait(self, duration);
		end
	end
end

-- how fast we will play() the animation in movie block
-- @param speed: default to 1. if nil, it will return current speed.
function env_imp:playSpeed(speed)
	if(self.actor) then
		if(speed) then
			self.actor:SetPlaySpeed(speed);
		else
			return self.actor:GetPlaySpeed();
		end
	end
end

-- play a time series animation in the movie block.
-- this function will return immediately.
-- @param timeFrom: time in milliseconds, default to 0.
-- @param timeTo: if nil, default to timeFrom
-- @param isLooping: default to false.
function env_imp:play(timeFrom, timeTo, isLooping)
	timeFrom = timeFrom or 0;
	local time = timeFrom;
	local entity = env_imp.GetEntity(self);
	if(entity) then
		entity:SetDummy(true);
		entity:EnableAnimation(false);
		local actor = env_imp.GetActor(self);
		if(not actor) then
			return
		end
		actor:SetTime(time);
		actor:ResetOffsetPosAndRotation();
		actor:FrameMove(0, false);
		self.codeblock:OnAnimateActor(actor, time);

		if(timeTo and timeTo>timeFrom) then
			local deltaTime = math.floor(env_imp.GetDefaultTick(self)*1000);
			local function frameMove_(timer)
				local delta = timer:GetDelta() * actor:GetPlaySpeed();
				time = time + delta;
				if(time >= timeTo) then
					if(isLooping) then
						if((time - delta) == timeTo) then
							time = timeFrom;
						else
							time = timeTo;
						end
					else
						time = timeTo;
						timer:Change();
					end
				end
				actor:SetTime(time);
				actor:FrameMove(0, false);
				if(timeTo == time) then
					self.codeblock:OnAnimateActor(actor, time);
				end
			end
			if(not self.actor.playTimer) then
				self.actor.playTimer = self.codeblock:SetTimer(self.co:MakeCallbackFunc(frameMove_), 0, deltaTime);
				self.actor:Connect("beforeRemoved", function(actor)
					if(actor.playTimer) then
						self.codeblock:KillTimer(actor.playTimer);
						actor.playTimer = nil;
					end
				end)
			else
				self.actor.playTimer.callbackFunc = self.co:MakeCallbackFunc(frameMove_);
			end
			self.actor.playTimer:Change(0, deltaTime);
		end
	end
end

-- same as play(), but looping
function env_imp:playLoop(timeFrom, timeTo)
	env_imp.play(self, timeFrom, timeTo, true);
	env_imp.checkyield(self);
end

-- play a bone's time series animation in the movie block.
-- this function will return immediately.
-- @param boneName: bone name
-- @param timeFrom: time in milliseconds, default to 0.
-- @param timeTo: if nil, default to timeFrom
-- @param isLooping: default to false.
function env_imp:playBone(boneName, timeFrom, timeTo, isLooping)
	timeFrom = timeFrom or 0;
	local time = timeFrom;
	local entity = env_imp.GetEntity(self);
	if(entity) then
		entity:SetDummy(true);
		entity:EnableAnimation(false);
		local actor = env_imp.GetActor(self);
		if(not actor) then
			return
		end
		actor:SetBoneTime(boneName, time);

		if(timeTo and timeTo>timeFrom) then
			local deltaTime = math.floor(env_imp.GetDefaultTick(self)*1000);
			local function frameMove_(timer)
				local delta = timer:GetDelta() * actor:GetPlaySpeed();
				time = time + delta;
				if(time >= timeTo) then
					if(isLooping) then
						if((time - delta) == timeTo) then
							time = timeFrom;
						else
							time = timeTo;
						end
					else
						time = timeTo;
						timer:Change();
					end
				end
				actor:SetBoneTime(boneName, time);
			end
			if(not self.actor.playTimers) then
				self.actor.playTimers = {};
				self.actor:Connect("beforeRemoved", function(actor)
					if(actor.playTimers) then
						for _, timer in pairs(actor.playTimers) do
							self.codeblock:KillTimer(timer);
						end
						actor.playTimers = nil;
					end
				end)
			end
			if(not self.actor.playTimers[boneName]) then
				self.actor.playTimers[boneName] = self.codeblock:SetTimer(self.co:MakeCallbackFunc(frameMove_), 0, deltaTime);
			else
				self.actor.playTimers[boneName].callbackFunc = self.co:MakeCallbackFunc(frameMove_);
			end
			self.actor.playTimers[boneName]:Change(0, deltaTime);
		end
	end
end

function env_imp:stop()
	if(self.actor) then
		if(self.actor.playTimer) then
			self.codeblock:KillTimer(self.actor.playTimer);
			self.actor.playTimer = nil;
		end
		if(self.actor.playTimers) then
			for _, timer in pairs(self.actor.playTimers) do
				self.codeblock:KillTimer(timer);
			end
			self.actor.playTimers = nil;
		end
	end
	env_imp.checkyield(self);
end

function env_imp:show()
	if(self.actor) then
		self.actor:SetVisible(true);
	end
	env_imp.checkyield(self);
end

function env_imp:hide()
	if(self.actor) then
		self.actor:SetVisible(false);
	end
	env_imp.checkyield(self);
end

function env_imp:bounce()
	if(self.actor) then
		self.actor:Bounce();
	end
	env_imp.checkyield(self);
end

-- set focus to current actor or the main player 
-- @param : nil or "myself" means current actor, "player" means the main player, or it can also be actor object
function env_imp:focus(name)
	if(not name or name == "myself") then
		if(self.actor) then
			self.actor:SetFocus();
		end
	elseif(name == "player") then
		EntityManager.GetPlayer():SetFocus();
	elseif(type(name) == "string") then
		local actor = GameLogic.GetCodeGlobal():GetActorByName(name);
		if(actor) then
			actor:SetFocus();
		end
	elseif(type(name) == "table" and name.SetFocus) then
		-- actor object is also supported
		name:SetFocus()
	end
	env_imp.checkyield(self);
end

-- same as the /velocity command
-- "1,~,~"   :set current player's speed
-- "set 1,1,1"   :set speed of the test entity
-- "add 1,~,~"   :use ~ to retain last speed.
function env_imp:velocity(cmd_text)
	env_imp.checkyield(self);
	local list, bIsAdd;
	local playerEntity = env_imp.GetEntity(self);
	if(not playerEntity) then
		return;
	end
	-- default to set velocity
	bIsAdd, cmd_text = CmdParser.ParseText(cmd_text, "add");
	if(not bIsAdd) then
		bIsAdd, cmd_text = CmdParser.ParseText(cmd_text, "set");
		bIsAdd = nil;
	end
	list, cmd_text = CmdParser.ParseNumberList(cmd_text, nil, "|,%s")
	if(list) then
		local x, y, z;
		if(#list == 1) then
			x,y,z = nil,list[1],nil;
		elseif(#list == 2) then
			x,y,z = list[1],nil,list[2];
		else
			x,y,z = list[1],list[2],list[3];
		end
		if(bIsAdd) then
			playerEntity:AddVelocity(x or 0,y or 0,z or 0);
		else
			playerEntity:SetVelocity(x,y,z);
		end
		playerEntity:SetDummy(false);
	end
end

function env_imp:camera(dist, pitch, facing)
	if(dist) then
		GameLogic.options:SetCameraObjectDistance(dist)
	end
	if(pitch) then
		pitch = pitch*math.pi/180;
		local att = ParaCamera.GetAttributeObject();
		att:SetField("CameraLiftupAngle", pitch);
	end
	if(facing) then
		facing = facing*math.pi/180;
		local att = ParaCamera.GetAttributeObject();
		att:SetField("CameraRotY", facing);
	end
end

local function GetMovieChannelName_(name, codeblock)
	if(not name or name == "myself") then
		name = codeblock:GetFilename();
	end
	return name;
end

-- @param name: movie channel name. 
-- @param x, y, z: if nil or 0, it means the closest movie block
function env_imp:setMovie(name, x, y, z)
	name = GetMovieChannelName_(name, self.codeblock)
	local channel = MovieManager:CreateGetMovieChannel(name);
	if(channel) then
		if(not z or (z==0) ) then
			local movieEntity = self.codeblock:GetMovieEntity();
			if(movieEntity) then
				x, y, z = movieEntity:GetBlockPos();
			end
		end
		channel:SetStartBlockPosition(math.floor(x),math.floor(y),math.floor(z));
	end
end

-- @param key: propertyName. "ReuseActor:bool"
function env_imp:setMovieProperty(name, key, value)
	name = GetMovieChannelName_(name, self.codeblock)
	local channel = MovieManager:CreateGetMovieChannel(name);
	if(channel) then
		if(key == "ReuseActor") then
			channel:SetReuseActor(value==1 and true or value);
		elseif(key == "Speed") then
			if(type(value) == "number") then
				channel:SetSpeed(value);
			end
		elseif(key == "UseCamera") then
			channel:SetUseCamera(value==true or value==1);
		end
	end
end

function env_imp:playMovie(name, timeFrom, timeTo, bLoop)
	name = GetMovieChannelName_(name, self.codeblock)
	local channel = MovieManager:CreateGetMovieChannel(name);

	if(not channel:GetStartBlockPosition()) then
		local movieEntity = self.codeblock:GetMovieEntity();
		if(movieEntity) then
			local x, y, z = movieEntity:GetBlockPos();
			channel:SetStartBlockPosition(x, y, z);
		end
	end

	if(bLoop) then
		channel:PlayLooped(timeFrom, timeTo);
	else
		channel:Play(timeFrom, timeTo);
	end

	-- tricky: we shall stop the movie channel when code blocks playing it are all unloaded.
	local playingCodeblocks = channel.playingCodeblocks;
	if(not playingCodeblocks) then
		playingCodeblocks = {};
		channel.playingCodeblocks = playingCodeblocks;
	end
	if(not playingCodeblocks[self.codeblock]) then
		playingCodeblocks[self.codeblock] = true;
		self.codeblock:Connect("codeUnloaded", function()
			channel.playingCodeblocks[self.codeblock] = nil;
			if(not next(channel.playingCodeblocks)) then
				-- only stop when the last code block stopped. 
				channel:Stop();	
			end
		end)
	end

	if(not bLoop and channel:IsPlaying()) then
		local callbackFunc;

		callbackFunc = self.co:MakeCallbackFuncAsync(function()
			channel:Disconnect("finished", callbackFunc)
			env_imp.resume(self);
		end);
		channel:Connect("finished", callbackFunc);

		env_imp.yield(self);
	end
end

function env_imp:stopMovie(name)
	name = GetMovieChannelName_(name, self.codeblock)
	local channel = MovieManager:CreateGetMovieChannel(name);
	channel:Stop();
end


```