```lua

--[[
Title: 
Author(s): Leio
Date: 2010/06/21
Desc: 
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/aries_camera.lua");
-------------------------------------------------------
]]
local mcml = Map3DSystem.mcml;
local pairs = pairs
local ipairs = ipairs
local tostring = tostring
local tonumber = tonumber
local type = type
local string_find = string.find;
local string_format = string.format;
local string_gsub = string.gsub;
local string_lower = string.lower
local string_match = string.match;

local table_getn = table.getn;
local mcml_controls = commonlib.gettable("Map3DSystem.mcml_controls");
local LOG = LOG;
local CommonCtrl = commonlib.gettable("CommonCtrl");
local commonlib = commonlib.gettable("commonlib");

NPL.load("(gl)script/ide/MotionEx/MotionLine.lua");
local MotionLine = commonlib.gettable("MotionEx.MotionLine");

if(not Map3DSystem.mcml_controls) then Map3DSystem.mcml_controls = {} end
--�ڴ���4��λ��ʱ�����Ӧ��style2
local function canStyle2(mcmlNode)
	if(mcmlNode and mcmlNode.caster_slotid and mcmlNode.caster_slotid > 4 and mcmlNode.attr and mcmlNode.attr.style2) then
		return true;
	end	
end
--��ȡstyle2
local function getStyle2(mcmlNode)
	if(not mcmlNode)then return end
	if(mcmlNode.style2)then
		return mcmlNode.style2;
	end
	if(mcmlNode.attr and mcmlNode.attr.style2) then
		local style2 = {};
		
		local name, value;
		for name, value in string.gfind(mcmlNode.attr.style2, "([%w%-]+)%s*:%s*([^;]*)[;]?") do
			name = string_lower(name);
			value = string_gsub(value, "%s*$", "");
			style2[name] = value;
		end
		mcmlNode.style2 = style2;
		return style2;
	end
end
local function clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty)
	x = tonumber(x);
	y = tonumber(y);
	z = tonumber(z);

	dx = tonumber(dx) or 0;
	dy = tonumber(dy) or 0;
	dz = tonumber(dz) or 0;

	cameraobjectdistance = tonumber(cameraobjectdistance);
	cameraliftupangle = tonumber(cameraliftupangle);
	cameraroty = tonumber(cameraroty);

	dcameraobjectdistance = tonumber(dcameraobjectdistance) or 0;
	dcameraliftupangle = tonumber(dcameraliftupangle) or 0;
	dcameraroty = tonumber(dcameraroty) or 0;

	if( x )then x = x + dx or 0; end
	if( y )then y = y + dy or 0; end
	if( z )then z = z + dz or 0; end
	if( cameraobjectdistance )then cameraobjectdistance = cameraobjectdistance + dcameraobjectdistance; end
	if( cameraliftupangle )then cameraliftupangle = cameraliftupangle + dcameraliftupangle; end
	if( cameraroty )then cameraroty = cameraroty + dcameraroty; end

	return x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty;
end
--camera
local aries_camera = {};
Map3DSystem.mcml_controls.aries_camera = aries_camera;

function aries_camera.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local id =  mcmlNode:GetString("id");
	local nodes = {};
	local childnode;


	for childnode in mcmlNode:next() do
		childnode.start_facing = mcmlNode.start_facing;
		childnode.end_facing = mcmlNode.end_facing;
		childnode.start_point_pos = mcmlNode.start_point_pos;
		childnode.end_point_pos = mcmlNode.end_point_pos;
		childnode.ground_pos = mcmlNode.ground_pos;
		childnode.caster_slotid = mcmlNode.caster_slotid;
		childnode.target_slotids = mcmlNode.target_slotids;

		local node = Map3DSystem.mcml_controls.create(rootName, childnode, bindingContext, _parent, left, top, width, height, style, parentLayout);
		if(node)then
			if(node.frametype)then
				node.FrameType = node.frametype;
				node.frametype = nil;
			end
			if(node.cameraobjectdistance)then
				node.CameraObjectDistance = node.cameraobjectdistance;
				node.cameraobjectdistance = nil;
			end
			if(node.cameraliftupangle)then
				node.CameraLiftupAngle = node.cameraliftupangle;
				node.cameraliftupangle = nil;
			end
			if(node.cameraroty)then
				node.CameraRotY = node.cameraroty;
				node.cameraroty = nil;
			end
			if(node.CameraRotY)then
				----ȷ����0-2pi֮��
				node.CameraRotY = math.mod(node.CameraRotY,2*math.pi);
				if(node.CameraRotY < 0)then
					node.CameraRotY = node.CameraRotY + 2*math.pi;
				end
				--node.CameraRotY = math.mod(node.CameraRotY,math.pi);
			end
			table.insert(nodes,node);
		end
	end
	return nodes;
end

--camera:track
local aries_camera_track = {};
Map3DSystem.mcml_controls.aries_camera_track = aries_camera_track;

function aries_camera_track.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle(Map3DSystem.mcml_controls.pe_html.css["camera:track"], style) or {};
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
		
	local node = {
		duration = duration,
		frametype = frametype,
		x = x,
		y = y,
		z = z,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
	};
	return node;
end

--camera:point
--���һ���۲��
local aries_camera_point = {};
Map3DSystem.mcml_controls.aries_camera_point = aries_camera_point;

function aries_camera_point.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	
	--caster or target or ground	
	local point =  mcmlNode:GetString("point");

	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;
	local caster_slotid = mcmlNode.caster_slotid;
	
	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end

	local eye_pos;
	if(point == "caster")then
		eye_pos = start_point_pos;
	elseif(point == "target")then
		eye_pos = end_point_pos;
	elseif(point == "ground")then
		eye_pos = ground_pos;
	elseif(point == "ground2")then
		eye_pos = ground_pos;
		local is_pvp;
		NPL.load("(gl)script/apps/Aries/Scene/WorldManager.lua");
		local WorldManager = commonlib.gettable("MyCompany.Aries.WorldManager");
		local world_info = WorldManager:GetCurrentWorld();
		if(world_info and world_info.team_mode and world_info.team_mode == "random_pvp")then
			is_pvp = true;
		end
		if(SystemInfo.GetField("name") == "Taurus")then
			is_pvp = true;
		end
		if(is_pvp and caster_slotid and caster_slotid > 4)then
			cameraroty = cameraroty + 3.14
		end
	end
	if(not eye_pos)then return end

	local node = {
		duration = duration,
		frametype = frametype,
		x = eye_pos[1] + dx,
		y = eye_pos[2] + dy,
		z = eye_pos[3] + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
	};
	return node;
end

--camera:empty
local aries_camera_empty = {};
Map3DSystem.mcml_controls.aries_camera_empty = aries_camera_empty;

function aries_camera_empty.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle() or {};
	local duration = (css["duration"] or 0)
	duration = tonumber(duration);
	local node = {
		duration = duration,
	};
	return node;
end
local aries_camera_dynamic = {};
Map3DSystem.mcml_controls.aries_camera_dynamic = aries_camera_dynamic;
--camera:dynamic
function aries_camera_dynamic.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle() or {};
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	
	local att = ParaCamera.GetAttributeObject();
	local x,y,z = ParaCamera.GetLookAtPos(); 
	local node = {
		duration = duration,
		frametype = frametype,
		x = x,
		y = y,
		z = z,
		cameraobjectdistance = att:GetField("CameraObjectDistance",5) + dcameraobjectdistance,
		cameraliftupangle = att:GetField("CameraLiftupAngle",0.4)  + dcameraliftupangle,
		cameraroty = att:GetField("CameraRotY",0) + dcameraroty,
	};
	return node;
end
local aries_camera_caster = {};
Map3DSystem.mcml_controls.aries_camera_caster = aries_camera_caster;
--camera:caster
function aries_camera_caster.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	radius = tonumber(radius) or 4;
	angle = tonumber(angle) or 30;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 2;
	cameraliftupangle = tonumber(cameraliftupangle) or -0.3;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);

	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = start_facing;
	local center_x = start_point_pos[1];
	local center_y = start_point_pos[2];
	local center_z = start_point_pos[3];

	local rotation = 1.57 + facing + angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y + 1;
	local eye_z = center_z + math.cos(rotation) * radius;

	local cameraroty = facing - 3.14 + angle * 3.14 / 180 + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_target = {};
Map3DSystem.mcml_controls.aries_camera_target = aries_camera_target;
--camera:target
function aries_camera_target.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 4;
	angle = tonumber(angle) or 30;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 2;
	cameraliftupangle = tonumber(cameraliftupangle) or -0.3;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = end_facing;

	local center_x = end_point_pos[1];
	local center_y = end_point_pos[2];
	local center_z = end_point_pos[3];

	local rotation = 1.57 + facing - angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y + 1;
	local eye_z = center_z + math.cos(rotation) * radius;


	--local cameraroty = facing + 3.14 - angle * 3.14 / 180 + dcameraroty;
	local cameraroty = facing - 3.14 - angle * 3.14 / 180 + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_ground = {};
Map3DSystem.mcml_controls.aries_camera_ground = aries_camera_ground;
--camera:ground
function aries_camera_ground.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local rotation = 1.57 + facing - angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y;
	local eye_z = center_z + math.cos(rotation) * radius;


	local cameraroty = facing - 3.14 - angle * 3.14 / 180 + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_follow = {};
Map3DSystem.mcml_controls.aries_camera_follow = aries_camera_follow;
--camera:follow
function aries_camera_follow.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);

	local target =  mcmlNode:GetString("target");
	local node = {
		duration = duration,
		frametype = frametype,
		FollowTarget = target,
		AllowFollow = true,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
	};
	return node;
end
local aries_camera_abcenter = {};
Map3DSystem.mcml_controls.aries_camera_abcenter = aries_camera_abcenter;
--camera:abcenter
function aries_camera_abcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (end_point_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (end_point_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (end_point_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((end_point_pos[1] - start_point_pos[1]), (end_point_pos[3] - start_point_pos[3])) - math.pi/2;

	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_abgcenter = {};
Map3DSystem.mcml_controls.aries_camera_abgcenter = aries_camera_abgcenter;
--camera:abgcenter
function aries_camera_abgcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (end_point_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (end_point_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (end_point_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((end_point_pos[1] - start_point_pos[1]), (end_point_pos[3] - start_point_pos[3])) - math.pi/2;
	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = center_x + dx,
		y = center_y + dy,
		z = center_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_agcenter = {};
Map3DSystem.mcml_controls.aries_camera_agcenter = aries_camera_agcenter;
--camera:agcenter
function aries_camera_agcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (ground_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (ground_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (ground_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((ground_pos[1] - start_point_pos[1]), (ground_pos[3] - start_point_pos[3])) - math.pi/2;

	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_bgcenter = {};
Map3DSystem.mcml_controls.aries_camera_bgcenter = aries_camera_bgcenter;
--camera:agcenter
function aries_camera_bgcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = end_point_pos[1] + (ground_pos[1] - end_point_pos[1]) / 2;
	local eye_y = end_point_pos[2] + (ground_pos[2] - end_point_pos[2]) / 2;
	local eye_z = end_point_pos[3] + (ground_pos[3] - end_point_pos[3]) / 2;
	facing = math.atan2((ground_pos[1] - end_point_pos[1]), (ground_pos[3] - end_point_pos[3])) - math.pi/2;

	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end


--[[
Title: 
Author(s): Leio
Date: 2011/03/09
Desc: 
�����ռ� ��aries_camera_2��������aries_camera_2 Ϊ��aries:camera
��Ҫ��������ת�ĽǶȣ�û���޶���0-2pi֮��
use the lib:
-------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/aries_camera_2.lua");
-------------------------------------------------------
]]
local mcml = Map3DSystem.mcml;
local pairs = pairs
local ipairs = ipairs
local tostring = tostring
local tonumber = tonumber
local type = type
local string_find = string.find;
local string_format = string.format;
local string_gsub = string.gsub;
local string_lower = string.lower
local string_match = string.match;

local table_getn = table.getn;
local mcml_controls = commonlib.gettable("Map3DSystem.mcml_controls");
local LOG = LOG;
local CommonCtrl = commonlib.gettable("CommonCtrl");
local commonlib = commonlib.gettable("commonlib");

NPL.load("(gl)script/ide/MotionEx/MotionLine.lua");
local MotionLine = commonlib.gettable("MotionEx.MotionLine");

if(not Map3DSystem.mcml_controls) then Map3DSystem.mcml_controls = {} end
--�ڴ���4��λ��ʱ�����Ӧ��style2
local function canStyle2(mcmlNode)
	if(mcmlNode and mcmlNode.caster_slotid and mcmlNode.caster_slotid > 4 and mcmlNode.attr and mcmlNode.attr.style2) then
		return true;
	end	
end
--��ȡstyle2
local function getStyle2(mcmlNode)
	if(not mcmlNode)then return end
	if(mcmlNode.style2)then
		return mcmlNode.style2;
	end
	if(mcmlNode.attr and mcmlNode.attr.style2) then
		local style2 = {};
		
		local name, value;
		for name, value in string.gfind(mcmlNode.attr.style2, "([%w%-]+)%s*:%s*([^;]*)[;]?") do
			name = string_lower(name);
			value = string_gsub(value, "%s*$", "");
			style2[name] = value;
		end
		mcmlNode.style2 = style2;
		return style2;
	end
end
--��⻡�ȣ�ȷ����0-2pi
local function checkAngle(n)
	if(not n)then 
		return 0;
	end
	n = math.mod(n,math.pi);
	if(n < 0)then
		n = n + math.pi;
	end
	return n;
end
local function clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty)
	x = tonumber(x);
	y = tonumber(y);
	z = tonumber(z);

	dx = tonumber(dx) or 0;
	dy = tonumber(dy) or 0;
	dz = tonumber(dz) or 0;

	cameraobjectdistance = tonumber(cameraobjectdistance);
	cameraliftupangle = tonumber(cameraliftupangle);
	cameraroty = tonumber(cameraroty);

	dcameraobjectdistance = tonumber(dcameraobjectdistance) or 0;
	dcameraliftupangle = tonumber(dcameraliftupangle) or 0;
	dcameraroty = tonumber(dcameraroty) or 0;

	if( x )then x = x + dx or 0; end
	if( y )then y = y + dy or 0; end
	if( z )then z = z + dz or 0; end
	if( cameraobjectdistance )then cameraobjectdistance = cameraobjectdistance + dcameraobjectdistance; end
	if( cameraliftupangle )then cameraliftupangle = cameraliftupangle + dcameraliftupangle; end
	if( cameraroty )then cameraroty = cameraroty + dcameraroty; end

	return x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty;
end
--camera
local aries_camera_2 = {};
Map3DSystem.mcml_controls.aries_camera_2 = aries_camera_2;

function aries_camera_2.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local id =  mcmlNode:GetString("id");
	local nodes = {};
	local childnode;

	for childnode in mcmlNode:next() do
		childnode.start_facing = mcmlNode.start_facing;
		childnode.end_facing = mcmlNode.end_facing;
		childnode.start_point_pos = mcmlNode.start_point_pos;
		childnode.end_point_pos = mcmlNode.end_point_pos;
		childnode.ground_pos = mcmlNode.ground_pos;
		childnode.caster_slotid = mcmlNode.caster_slotid;
		childnode.target_slotids = mcmlNode.target_slotids;

		local node = Map3DSystem.mcml_controls.create(rootName, childnode, bindingContext, _parent, left, top, width, height, style, parentLayout);
		if(node)then
			if(node.frametype)then
				node.FrameType = node.frametype;
				node.frametype = nil;
			end
			if(node.cameraobjectdistance)then
				node.CameraObjectDistance = node.cameraobjectdistance;
				node.cameraobjectdistance = nil;
			end
			if(node.cameraliftupangle)then
				node.CameraLiftupAngle = node.cameraliftupangle;
				node.cameraliftupangle = nil;
			end
			if(node.cameraroty)then
				node.CameraRotY = node.cameraroty;
				node.cameraroty = nil;
			end
			if(node.CameraRotY)then
				--node.CameraRotY = checkAngle(node.CameraRotY);
			end
			table.insert(nodes,node);
		end
	end
	return nodes;
end

--camera:track
local aries_camera_2_track = {};
Map3DSystem.mcml_controls.aries_camera_2_track = aries_camera_2_track;

function aries_camera_2_track.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle() or {};
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
		
	local node = {
		duration = duration,
		frametype = frametype,
		x = x,
		y = y,
		z = z,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
	};
	return node;
end
--camera:empty
local aries_camera_2_empty = {};
Map3DSystem.mcml_controls.aries_camera_2_empty = aries_camera_2_empty;

function aries_camera_2_empty.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle() or {};
	local duration = (css["duration"] or 0)
	duration = tonumber(duration);
	local node = {
		duration = duration,
	};
	return node;
end
local aries_camera_2_dynamic = {};
Map3DSystem.mcml_controls.aries_camera_2_dynamic = aries_camera_2_dynamic;
--camera:dynamic
function aries_camera_2_dynamic.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css = mcmlNode:GetStyle() or {};
	local duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	
	local att = ParaCamera.GetAttributeObject();
	local x,y,z = ParaCamera.GetLookAtPos(); 
	local node = {
		duration = duration,
		frametype = frametype,
		x = x,
		y = y,
		z = z,
		cameraobjectdistance = att:GetField("CameraObjectDistance",5) + dcameraobjectdistance,
		cameraliftupangle = att:GetField("CameraLiftupAngle",0.4)  + dcameraliftupangle,
		cameraroty = att:GetField("CameraRotY",0) + dcameraroty,
	};
	return node;
end
local aries_camera_2_caster = {};
Map3DSystem.mcml_controls.aries_camera_2_caster = aries_camera_2_caster;
--camera:caster
function aries_camera_2_caster.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
		
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 2;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;
	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);

	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local center_x = start_point_pos[1];
	local center_y = start_point_pos[2];
	local center_z = start_point_pos[3];
	local facing = math.atan2((ground_pos[1] - start_point_pos[1]), (ground_pos[3] - start_point_pos[3])) - math.pi/2;

	local rotation = facing + angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y + 1;
	local eye_z = center_z + math.cos(rotation) * radius;
	local cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_target = {};
Map3DSystem.mcml_controls.aries_camera_2_target = aries_camera_2_target;
--camera:target
function aries_camera_2_target.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 2;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end

	local center_x = end_point_pos[1];
	local center_y = end_point_pos[2];
	local center_z = end_point_pos[3];
	local facing = math.atan2((ground_pos[1] - end_point_pos[1]), (ground_pos[3] - end_point_pos[3])) - math.pi/2;

	local rotation = facing - angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y + 1;
	local eye_z = center_z + math.cos(rotation) * radius;

	local cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_ground = {};
Map3DSystem.mcml_controls.aries_camera_2_ground = aries_camera_2_ground;
--camera:ground
function aries_camera_2_ground.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local rotation = facing - angle * 3.14 / 180;
	local eye_x = center_x + math.sin(rotation) * radius;
	local eye_y = center_y;
	local eye_z = center_z + math.cos(rotation) * radius;
	local cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_abcenter = {};
Map3DSystem.mcml_controls.aries_camera_2_abcenter = aries_camera_2_abcenter;
--camera:abcenter
function aries_camera_2_abcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (end_point_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (end_point_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (end_point_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((end_point_pos[1] - start_point_pos[1]), (end_point_pos[3] - start_point_pos[3])) - math.pi/2;
	cameraroty = facing + dcameraroty;

	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_abgcenter = {};
Map3DSystem.mcml_controls.aries_camera_2_abgcenter = aries_camera_2_abgcenter;
--camera:abgcenter
function aries_camera_2_abgcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (end_point_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (end_point_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (end_point_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((end_point_pos[1] - start_point_pos[1]), (end_point_pos[3] - start_point_pos[3])) - math.pi/2;
	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = center_x + dx,
		y = center_y + dy,
		z = center_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_agcenter = {};
Map3DSystem.mcml_controls.aries_camera_2_agcenter = aries_camera_2_agcenter;
--camera:agcenter
function aries_camera_2_agcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = start_point_pos[1] + (ground_pos[1] - start_point_pos[1]) / 2;
	local eye_y = start_point_pos[2] + (ground_pos[2] - start_point_pos[2]) / 2;
	local eye_z = start_point_pos[3] + (ground_pos[3] - start_point_pos[3]) / 2;
	facing = math.atan2((ground_pos[1] - start_point_pos[1]), (ground_pos[3] - start_point_pos[3])) - math.pi/2;
	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end
local aries_camera_2_bgcenter = {};
Map3DSystem.mcml_controls.aries_camera_2_bgcenter = aries_camera_2_bgcenter;
--camera:agcenter
function aries_camera_2_bgcenter.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	local css;
	if(canStyle2(mcmlNode))then
		css = getStyle2(mcmlNode) or {};
	else
		css = mcmlNode:GetStyle() or {};
	end
	local radius,angle,duration,frametype,x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty = 
		(css["radius"] or nil),(css["angle"] or nil),
		(css["duration"] or 0),(css["frametype"] or "None"),
		(css["x"] or nil),(css["y"] or nil),(css["z"] or nil),
		(css["dx"] or 0),(css["dy"] or 0),(css["dz"] or 0),
		(css["cameraobjectdistance"] or nil),(css["cameraliftupangle"] or nil),(css["cameraroty"] or nil),
		(css["dcameraobjectdistance"] or 0),(css["dcameraliftupangle"] or 0),(css["dcameraroty"] or 0);
	radius = tonumber(radius) or 0;
	angle = tonumber(angle) or 0;
	cameraobjectdistance = tonumber(cameraobjectdistance) or 0;
	cameraliftupangle = tonumber(cameraliftupangle) or 0;
	cameraroty = tonumber(cameraroty) or 0;

	duration = tonumber(duration);
	x,y,z,cameraobjectdistance,cameraliftupangle,cameraroty,dx,dy,dz,dcameraobjectdistance,dcameraliftupangle,dcameraroty = clipValues(x,y,z,dx,dy,dz,cameraobjectdistance,cameraliftupangle,cameraroty,dcameraobjectdistance,dcameraliftupangle,dcameraroty);
	local start_facing = mcmlNode.start_facing;
	local end_facing = mcmlNode.end_facing;
	local start_point_pos = mcmlNode.start_point_pos;
	local end_point_pos = mcmlNode.end_point_pos;
	local ground_pos = mcmlNode.ground_pos;

	if(not start_facing or not end_facing or not start_point_pos or not end_point_pos or not ground_pos)then return end
	local facing = 0;

	local center_x = ground_pos[1];
	local center_y = ground_pos[2];
	local center_z = ground_pos[3];

	local eye_x = end_point_pos[1] + (ground_pos[1] - end_point_pos[1]) / 2;
	local eye_y = end_point_pos[2] + (ground_pos[2] - end_point_pos[2]) / 2;
	local eye_z = end_point_pos[3] + (ground_pos[3] - end_point_pos[3]) / 2;
	facing = math.atan2((ground_pos[1] - end_point_pos[1]), (ground_pos[3] - end_point_pos[3])) - math.pi/2;
	cameraroty = facing + dcameraroty;
	local node = {
		duration = duration,
		frametype = frametype,

		x = eye_x + dx,
		y = eye_y + dy,
		z = eye_z + dz,
		cameraobjectdistance = cameraobjectdistance,
		cameraliftupangle = cameraliftupangle,
		cameraroty = cameraroty,
		
	};
	return node;
end


--[[
Title: a simple mcml web page browser window
Author(s): LiXizhi
Date: 2008/3/10
Desc: a thin wrapper of mcml v1 page or v2 window  in a web browser style API. 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/BrowserWnd.lua");
local ctl = Map3DSystem.mcml.BrowserWnd:new{
	name = "McmlBrowserWnd1",
	alignment = "_lt",
	left=0, top=0,
	width = 512,
	height = 290,
	parent = nil,
};
ctl:Show();
-- One can also create NavBar elsewhere, like below
ctl:CreateNavBar(_parent, "_mt", 0, 0, 0,32)
ctl:Goto("%WIKI%/Main/ParaWorldFrontPageMCML");
ctl:Goto(url, System.localserver.CachePolicy:new("access plus 1 day"));
-------------------------------------------------------
]]
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml.lua");
NPL.load("(gl)script/ide/System/localserver/factory.lua");

--------------------------------------------------------------------
-- a browser window instance
--------------------------------------------------------------------
local BrowserWnd = {
	-- the top level control name
	name = "BrowserWnd1",
	-- normal window size
	alignment = "_lt",
	left = 0,
	top = 0,
	width = 300,
	height = 290, 
	parent = nil,
	background = "",
	-- current url
	url = nil,
	-- boolean: whether to create the nav bar, if nil NavBar will not be created. if false, it will be created but not visible.
	DisplayNavBar = nil,
	-- whether to display nav address combo box, if this is DisplayNavBar is not true, this parameter takes no effect. 
	DisplayNavAddress = true,
	-- a file containing url addresses
	historyFileName = "config/mcmlbrowser_urls.txt";
	-- max number of history files 
	max_history_items = 200,
	-- window object that will be passed to the internal v1 page control.
	window = nil,
}
Map3DSystem.mcml.BrowserWnd = BrowserWnd;

-- constructor
function BrowserWnd:new (o)
	o = o or {}   -- create object if user does not provide one
	setmetatable(o, self)
	self.__index = self
	return o
end

-- Destroy the UI control
function BrowserWnd:Destroy ()
	ParaUI.Destroy(self.name);
end

-- create navigation bar for this window
function BrowserWnd:CreateNavBar(_parent, alignment, left, right, width, height)
	if(_parent==nil) then
		_parent = ParaUI.GetUIObject(self.name);
	end
	
	if(ParaUI.GetUIObject(self.name.."navBar"):IsValid())  then
		return
	end
	
	local _this = ParaUI.CreateUIObject("container", self.name.."navBar", alignment or "_mt", left or 0, right or 0, width or 0, height or 28)
	_this.background = "";
	_parent:AddChild(_this);
	_parent = _this;
	
	local left, width = 8, 28;
	_this = ParaUI.CreateUIObject("button", "RefreshBtn", "_lt", left, 5, width, 23)
	_this.background = "Texture/3DMapSystem/webbrowser/PreviousPage_32bits.png; 0 0 28 23";
	_this.tooltip= "返回上一页";
	_this.onclick = string.format(";Map3DSystem.mcml.BrowserWnd.OnClickNavBackward(%q);", self.name);
	--_this.animstyle = 12;
	_parent:AddChild(_this);
	left = left + width - 1;
		
	_this = ParaUI.CreateUIObject("button", "RefreshBtn", "_lt", left, 5, width, 23)
	_this.background = "Texture/3DMapSystem/webbrowser/NextPage_32bits.png; 0 0 28 23";
	_this.tooltip= "返回下一页";
	_this.onclick = string.format(";Map3DSystem.mcml.BrowserWnd.OnClickNavForward(%q);", self.name);
	--_this.animstyle = 12;
	_parent:AddChild(_this);
	left = left + width + 9;

	_this = ParaUI.CreateUIObject("button", "RefreshBtn", "_lt", left, 5, width, 23)
	_this.background = "Texture/3DMapSystem/webbrowser/RefreshPage_32bits.png; 0 0 28 23";
	_this.tooltip= "刷新网页";
	_this.onclick = string.format(";Map3DSystem.mcml.BrowserWnd.OnClickNavRefresh(%q);", self.name);
	--_this.animstyle = 12;
	_parent:AddChild(_this);
	left = left + width + 8;
	
	-- address bar is here. 
	_this = ParaUI.CreateUIObject("container", "navAddressBar", "_fi", left, 0, 0, 0)
	_this.background = "";
	_parent:AddChild(_this);
	_parent = _this;
	
	left, width = 10, 29;
	--_this = ParaUI.CreateUIObject("button", "RefreshBtn", "_rt", -(left+width), 3, width, width)
	--_this.background = "Texture/3DMapSystem/webbrowser/refresh.png"
	--_this.tooltip= "刷新网页";
	--_this.onclick = string.format(";Map3DSystem.mcml.BrowserWnd.OnClickNavRefresh(%q);", self.name);
	--_this.animstyle = 12;
	--_parent:AddChild(_this);
	
	_this = ParaUI.CreateUIObject("button", "navTo", "_rt", -(left+width), 5, width, 23)
	_this.background = "Texture/3DMapSystem/webbrowser/Browse_32bits.png; 0 0 29 23";
	--_this.background = "Texture/3DMapSystem/webbrowser/goto.png"
	_this.tooltip= "打开";
	_this.onclick = string.format(";Map3DSystem.mcml.BrowserWnd.OnClickNavTo(%q);", self.name);
	_parent:AddChild(_this);
	left = left + width + 6;
	
	
	NPL.load("(gl)script/ide/dropdownlistbox.lua");
	local ctl = CommonCtrl.dropdownlistbox:new{
		name = self.name.."comboBoxAddress",
		alignment = "_mt",
		left = 0,
		top = 5,
		width = left,
		height = 24,
		dropdownheight = 106,
		parent = _parent,
		
		container_bg = nil, -- the background of container that contains the editbox and the dropdown button.
		editbox_bg = "Texture/3DMapSystem/webbrowser/AddressBar_32bits.png: 6 6 6 6",
		--dropdownbutton_bg = "Texture/3DMapSystem/webbrowser/DropDownBox_32bits.png; 0 0 20 24",-- drop down button background texture
		listbox_bg = nil, -- list box background texture
		
		
		text = "",
		items = {},
		onselect = string.format("Map3DSystem.mcml.BrowserWnd.OnClickNavTo(%q);", self.name),
	};
	ctl:Show();
	
	if(not self.DisplayNavAddress) then
		_parent.visible = false;
	end	
	
	if(not self.DisplayNavBar) then
		_parent.parent.visible = false;
	end
	
	-- update address bar history. 
	self:UpdateHistoryFiles();
end

--@param bShow: boolean to show or hide. if nil, it will toggle current setting. 
--@return true if UI is created
function BrowserWnd:Show(bShow)
	local _this,_parent, UICreated;
	if(self.name==nil)then
		log("BrowserWnd instance name can not be nil\r\n");
		return
	end
	
	_this=ParaUI.GetUIObject(self.name);
	if(_this:IsValid() == false) then
		if(bShow == false) then return	end
		bShow = true;
		_this=ParaUI.CreateUIObject("container",self.name,self.alignment,self.left,self.top,self.width,self.height);
		if(self.background) then
			_this.background=self.background;
		end
		_parent = _this;
		if(self.parent==nil) then
			_this:AttachToRoot();
		else
			_this.background="";
			self.parent:AddChild(_this);
		end
		
		CommonCtrl.AddControl(self.name, self);
		
		local top = 0;
		
		-------------------------
		-- navbar
		if(self.DisplayNavBar) then
			self:CreateNavBar(_parent, "_mt", 0,top,0,32);
			top = top+32;
		end
		self.clientTop = top;

		UICreated = true;
	else
		if(bShow == nil) then
			bShow = (_this.visible == false);
		end
		_this.visible = bShow;
	end	
	return UICreated;
end

--------------------------------------
-- public method
--------------------------------------

-- create get v1 page
function BrowserWnd:GetPageRenderer(pageType)
	pageType = pageType or self.pageType;
	if(pageType ~= "mcml2") then
		-- v1
		self:CloseRendererV2(true)
		if(not self.pageCtrl ) then
			NPL.load("(gl)script/kids/3DMapSystemApp/mcml/PageCtrl.lua");
			self.pageCtrl = Map3DSystem.mcml.PageCtrl:new({
				url = self.url,
				OnPageDownloaded = string.format("Map3DSystem.mcml.BrowserWnd.OnPage_CallBack(%q)", self.name),
				window = self.window,
			});
			self.pageCtrl:Create(self.name.."_pageCtrl", ParaUI.GetUIObject(self.name), "_fi", 0, self.clientTop or 0, 0, 0);
		end
		return self.pageCtrl;
	else
		-- v2
		self:CloseRendererV1(true)
		if(not self.windowCtrl) then
			self.windowCtrl = System.Windows.Window:new();
			self.windowCtrl:Show({url="", alignment="_fi", left=0, top=self.clientTop or 0, width=0, height=0, allowDrag=false, parent = ParaUI.GetUIObject(self.name)});
			self.windowCtrl:Connect("urlChanged", self, function()
				BrowserWnd.OnPage_CallBack(self.name);
			end, "UniqueConnection");
		end
		return self.windowCtrl;
	end
end

function BrowserWnd:CloseRendererV1(bDestroy)
	if(self.pageCtrl) then
		if(self.pageCtrl.OnClose) then
			self.pageCtrl:OnClose(bDestroy);
		end
		self.pageCtrl:Close();
		self.pageCtrl = nil;
	end
end

function BrowserWnd:CloseRendererV2(bDestroy)
	if(self.windowCtrl) then
		self.windowCtrl:CloseWindow(bDestroy);
		self.windowCtrl = nil;
	end
end

-- close all v1 and v2 renderers if any. 
function BrowserWnd:CloseAllRenderers(bDestroy)
	self:CloseRendererV1(bDestroy)
	self:CloseRendererV2(bDestroy)
end
-- call back function. This function is called by MCMLBrowserWnd whenever OnClose Windows message is received. 
-- @param bDestroy:
function BrowserWnd:OnClose(bDestroy)
	self:CloseAllRenderers(bDestroy);
end

-- go to a given url, refresh
-- @param url: if nil it will clear the browser. it can also be string "backward", "forward" which opens last page and forward page. 
function BrowserWnd:Goto(url, cache_policy, bRefresh)
	local protocol = url and url:match("^(mcml%d?)://");
	if(protocol) then
		url = url:gsub("^(mcml%d?://)", "");
	end
	self.pageType = protocol;
	if(protocol == "mcml2") then
		self:GetPageRenderer():Goto(url);
	else
		self:GetPageRenderer():Goto(url, cachePolicy, bRefresh);
	end
end

-- return nil or current url 
function BrowserWnd:GetUrl()
	if(self.pageType == "mcml2") then
		return "mcml2://"..(self:GetPageRenderer().url or "");
	else
		return "mcml1://"..(self:GetPageRenderer().url or "");
	end
end

-- show or hide the nav bar on top. 
function BrowserWnd:ShowNavBar(bShow)
	if(self.DisplayNavBar ~= bShow) then
		self.DisplayNavBar = bShow;
		ParaUI.GetUIObject(self.name.."navBar").visible = bShow
	end
end

-- show or hide the nav address bar on top. 
function BrowserWnd:ShowAddressBar(bShow)
	if(self.DisplayNavAddress~=bShow) then
		self.DisplayNavAddress = bShow;
		ParaUI.GetUIObject(self.name.."navBar"):GetChild("navAddressBar").visible = bShow
	end
end
--------------------------------------
-- private method and event handlers
--------------------------------------

-- load history test files
function BrowserWnd:UpdateHistoryFiles()
	local ctl = CommonCtrl.GetControl(self.name.."comboBoxAddress");
	if(ctl==nil)then
		log("error getting instance "..self.name.."comboBoxAddress".."\r\n");
		return;
	end
	
	if(ParaIO.DoesFileExist(self.historyFileName, true)) then
		ctl.items = commonlib.LoadTableFromFile(self.historyFileName) or {};
		ctl:RefreshListBox();
	end
end

-- save recently opened file to history
function BrowserWnd:SaveToHistoryFile(url)
	local ctl = CommonCtrl.GetControl(self.name.."comboBoxAddress");
	if(ctl~=nil)then
		local index = ctl:InsertItem(url)
		log("saving file to "..self.historyFileName.."\n")	
		if(index) then
			-- save to file
			if(index>1) then
				-- shuffle selected to front
				commonlib.moveArrayItem(ctl.items, index, 1)
			end	
			if(table.getn(ctl.items)>self.max_history_items) then
				commonlib.resize(ctl.items, self.max_history_items);
			end	
			commonlib.SaveTableToFile(ctl.items, self.historyFileName);
		else
			log("error: saving file to "..self.historyFileName.."\n")	
		end
	end
end

-- called when a new page is downloaded.
function BrowserWnd.OnPage_CallBack(sCtrlName)
	local self = CommonCtrl.GetControl(sCtrlName);
	if(self==nil)then
		log("error getting BrowserWnd instance "..sCtrlName.."\r\n");
		return;
	end
	self:SaveToHistoryFile(self:GetUrl())
	local ctl = CommonCtrl.GetControl(self.name.."comboBoxAddress");
	if(ctl)then
		ctl:SetText(self:GetUrl());
	end
end

-- replace the context in this window with input mcmlNode. 
-- @param mcmlNode: must be a raw mcmlNode, such as from a url or local server. 
function BrowserWnd:open(mcmlNode)
	self:ShowMessage(nil);
	self:GetPageRenderer():Init(mcmlNode, nil, true)
end

-- show a message to inform the user about a background action or status. 
-- @param text: string or nil. if nil, it will clear the message box. 
function BrowserWnd:ShowMessage(text)
	-- TODO: use a child window to display, such as in firefox. Currently just a plain popup message box. 
	--paraworld.ShowMessage(text)
	if(text == nil) then
		_guihelper.CloseMessageBox()
	else	
		_guihelper.MessageBox(text);
	end	
end

-- navigate to last url
function BrowserWnd.OnClickNavBackward(sCtrlName)
	local self = CommonCtrl.GetControl(sCtrlName);
	if(self==nil)then
		log("error getting BrowserWnd instance "..sCtrlName.."\r\n");
		return;
	end
	self:Goto("backward");
end


-- navigate to next url
function BrowserWnd.OnClickNavForward(sCtrlName)
	local self = CommonCtrl.GetControl(sCtrlName);
	if(self==nil)then
		log("error getting BrowserWnd instance "..sCtrlName.."\r\n");
		return;
	end
	self:Goto("forward");
end

-- navigate to the current url in combo box
function BrowserWnd.OnClickNavTo(sCtrlName)
	local self = CommonCtrl.GetControl(sCtrlName);
	if(self==nil)then
		log("error getting BrowserWnd instance "..sCtrlName.."\r\n");
		return;
	end
	
	local ctl = CommonCtrl.GetControl(self.name.."comboBoxAddress");
	if(ctl)then
		local url = ctl:GetText();
		if(url) then
			self:Goto(url)
		end
	end
end

-- do not use cached version and refresh 
function Map3DSystem.mcml.BrowserWnd.OnClickNavRefresh(sCtrlName)
	local self = CommonCtrl.GetControl(sCtrlName);
	if(self==nil)then
		log("error getting BrowserWnd instance "..sCtrlName.."\r\n");
		return;
	end
	self:Goto(self:GetUrl(), System.localserver.CachePolicy:new("access plus 0"), true)
end

--[[
Title: base mcml function and base Node implementation of mcml
Author(s): LiXizhi
Date: 2008/2/15
Desc: only included and used by mcml
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml_base.lua");
local node = Map3DSystem.mcml.new("pe:profile", {})
local o = Map3DSystem.mcml.buildclass(o);

-- the following is an example of creating a custom mcml tag control.
local pe_locationtracker = commonlib.gettable("MyCompany.Aries.mcml_controls.pe_locationtracker");
function pe_locationtracker.render_callback(mcmlNode, rootName, bindingContext, _parent, left, top, right, bottom, myLayout, css)
	-- TODO: your render code here
	-- local _this=ParaUI.CreateUIObject("button","b","_lt", left, top, right-left, bottom-top);
	-- _this.background = "Texture/alphadot.png";
	-- _parent:AddChild(_this);
	-- mcmlNode:DrawChildBlocks_Callback(rootName, bindingContext, _parent, left, top, right, bottom, myLayout, css)

	return true, true, true; -- ignore_onclick, ignore_background, ignore_tooltip;
end
function pe_locationtracker.create(rootName, mcmlNode, bindingContext, _parent, left, top, width, height, style, parentLayout)
	return mcmlNode:DrawDisplayBlock(rootName, bindingContext, _parent, left, top, width, height, parentLayout, style, pe_locationtracker.render_callback);
end
-------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/localserver/UrlHelper.lua");
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/StyleItem.lua");
local StyleItem = commonlib.gettable("Map3DSystem.mcml_controls.StyleItem");
local pe_css = commonlib.gettable("Map3DSystem.mcml_controls.pe_css");

if(not Map3DSystem.mcml) then Map3DSystem.mcml = {} end

local mcml = Map3DSystem.mcml;
local pairs = pairs
local ipairs = ipairs
local tostring = tostring
local tonumber = tonumber
local type = type
local string_find = string.find;
local string_format = string.format;
local string_gsub = string.gsub;
local string_lower = string.lower
local string_match = string.match;

local table_getn = table.getn;
local mcml_controls = commonlib.gettable("Map3DSystem.mcml_controls");
local LOG = LOG;
local CommonCtrl = commonlib.gettable("CommonCtrl");
local NameNodeMap_ = {};
local commonlib = commonlib.gettable("commonlib");
local pe_html = commonlib.gettable("Map3DSystem.mcml_controls.pe_html");
----------------------------
-- helper functions
----------------------------
-- set a node by a string name, so that the node can later be retrieved by name using GetNode().
-- @param name: string, this is usually the string returned by mcml.baseNode:GetInstanceName()
-- @param node: the node table object.
function mcml.SetNode(name, node)
	NameNodeMap_[name] = node;
end

-- get a node by a string name. 
-- @param name: string, 
function mcml.GetNode(name)
	return NameNodeMap_[name];
end

----------------------------
-- base functions
----------------------------

-- create or init a new object o of tag. it will return the input object, if tag name is not found. 
-- e.g. mcml.new(nil, {name="div"})
-- @param tagName: the tag (node) name to be created or initialized. if nil, the default "baseNode" is used.
-- @param o: the tag object to be initialized. if nil, a new one will be created. 
-- @return: the tag (node) object is returned. methods of the object can be called thereafterwards. 
function mcml.new(tagName, o)
	local baseNode = mcml[tagName or "baseNode"];
	if(baseNode) then
		o = o or {}
		if(baseNode.attr and o.attr) then
			setmetatable(o.attr, baseNode.attr)
			baseNode.attr.__index = baseNode.attr
		end
		
		setmetatable(o, baseNode)
		baseNode.__index = baseNode
		return o	
	else
		-- return the input object, if tag name is not found. 
		return o;
	end
end

-- o is a pure mcml table, after building class with it, it will be deserialized from pure data to a class contain all methods and parent|child relationships. 
-- o must be a pure table that does not contains cyclic table references. 
-- for unknown node in o, it will inherite from the baseNode. 
-- @return the input o is returned. 
function mcml.buildclass(o)
	local baseNode = mcml[o.name or "baseNode"];
	if(not baseNode) then
		baseNode = mcml["baseNode"];
	end
	if(baseNode.attr and o.attr) then
		setmetatable(o.attr, baseNode.attr)
		baseNode.attr.__index = baseNode.attr
	end
	setmetatable(o, baseNode)
	baseNode.__index = baseNode
	
	local i, child;
	for i, child in ipairs(o) do
		if(type(child) == "table") then
			mcml.buildclass(child);
			child.parent = o;
			child.index = i;
		end	
	end
	return o;
end

----------------------------
-- base node class
----------------------------

-- base class for all nodes. 
mcml.baseNode = {
	name = nil,
	parent = nil,
	-- control index in its parent
	index = 1,
}

-- return a copy of this object, everything is cloned including the parent and index of its child node. 
function mcml.baseNode:clone()
	local o = mcml.new(nil, {name = self.name})
	if(self.attr) then
		o.attr = {};
		commonlib.partialcopy(o.attr, self.attr)
	end
	local nSize = table_getn(self);
	if(nSize>0) then
		local i, node;
		for i=1, nSize do
			node = self[i];
			if(type(node)=="table" and type(node.clone)=="function") then
				o[i] = node:clone();
				o[i].index = i;
				o[i].parent = o;
			elseif(type(node)=="string") then
				o[i] = node;
			else
				LOG.warn("unknown node type when mcml.baseNode:clone() \n")	
			end
		end
		table.resize(o, nSize);
		-- table.setn(o, nSize);
	end	
	return o;
end

-- set the value of an attribute of this node. This function is rarely used. 
function mcml.baseNode:SetAttribute(attrName, value)
	self.attr = self.attr or {};
	self.attr[attrName] = value;
	if(attrName == "style") then
		-- tricky code: since we will cache style table on the node, we need to delete the cached style when it is changed. 
		self.style = nil;
	end
end

-- set the attribute if attribute is not code. 
function mcml.baseNode:SetAttributeIfNotCode(attrName, value)
	self.attr = self.attr or {};
	local old_value = self.attr[attrName];
	if(type(old_value) == "string") then
		local code = string_match(old_value, "^[<%%]%%(=.*)%%[%%>]$")
		if(not code) then
			self.attr[attrName] = value;
		end
	else
		self.attr[attrName] = value;
	end
end

-- get the value of an attribute of this node as its original format (usually string)
function mcml.baseNode:GetAttribute(attrName,defaultValue)
	if(self.attr) then
		return self.attr[attrName];
	end
	return defaultValue;
end

-- get the value of an attribute of this node (usually string)
-- this differs from GetAttribute() in that the attribute string may contain embedded code block which may evaluates to a different string, table or even function. 
-- please note that only the first call of this method will evaluate embedded code block, subsequent calls simply return the previous evaluated result. 
-- in most cases the result is nil or string, but it can also be a table or function. 
-- @param bNoOverwrite: default to nil. if true, the code will be reevaluated the next time this is called, otherwise the evaluated value will be saved and returned the next time this is called. 
-- e.g. attrName='<%="string"+Eval("index")}%>' attrName1='<%={fieldname="table"}%>'
function mcml.baseNode:GetAttributeWithCode(attrName,defaultValue, bNoOverwrite)
	if(self.attr) then
		local value = self.attr[attrName];
		if(type(value) == "string") then
			local code = string_match(value, "^[<%%]%%(=.*)%%[%%>]$")
			if(code) then
				value = mcml_controls.pe_script.DoPageCode(code, self:GetPageCtrl());
				if(not bNoOverwrite) then
					self.attr[attrName] = value;
				end	
			end
		end
		if(value ~= nil) then
			return value;
		end
	end
	return defaultValue;
end


-- get an attribute as string
function mcml.baseNode:GetString(attrName,defaultValue)
	if(self.attr) then
		return self.attr[attrName];
	end
	return defaultValue;
end

-- get an attribute as number
function mcml.baseNode:GetNumber(attrName,defaultValue)
	if(self.attr) then
		return tonumber(self.attr[attrName]);
	end
	return defaultValue;
end

-- get an attribute as integer
function mcml.baseNode:GetInt(attrName, defaultValue)
	if(self.attr) then
		return math.floor(tonumber(self.attr[attrName]));
	end
	return defaultValue;
end


-- get an attribute as boolean
function mcml.baseNode:GetBool(attrName, defaultValue)
	if(self.attr) then
		local v = string_lower(tostring(self.attr[attrName]));
		if(v == "false") then
			return false
		elseif(v == "true") then
			return true
		end
	end
	return defaultValue;
end

-- get all pure text of only text node
function mcml.baseNode:GetPureText()
	local nSize = table_getn(self);
	local i, node;
	local text = "";
	for i=1, nSize do
		node = self[i];
		if(node) then
			if(type(node) == "string") then
				text = text..node;
			end
		end
	end
	return text;
end

-- get all inner text recursively (i.e. without tags) as string. 
function mcml.baseNode:GetInnerText()
	local nSize = table_getn(self);
	local i, node;
	local text = "";
	for i=1, nSize do
		node = self[i];
		if(node) then
			if(type(node) == "string") then
				text = text..node;
			elseif(type(node) == "table") then
				text = text..node:GetInnerText();
			elseif(type(node) == "number") then
				text = text..tostring(node);
			end
		end
	end
	return text;
end

-- set inner text. It will replace all child nodes with a text node
function mcml.baseNode:SetInnerText(text)
	self[1] = text;
	commonlib.resize(self, 1);
	-- table.setn(self, 1)
end

-- get value: it is usually one of the editor tag, such as <input>
function mcml.baseNode:GetValue()
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.GetValue) then
		return controlClass.GetValue(self);
	else
		--LOG.warn("GetValue on object "..self.name.." is not supported\n")	
	end
end

-- set value: it is usually one of the editor tag, such as <input>
function mcml.baseNode:SetValue(value)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.SetValue) then
		return controlClass.SetValue(self, value);
	else
		--LOG.warn("SetValue on object "..self.name.." is not supported\n")	
	end
end

-- get UI value: get the value on the UI object with current node
-- @param instName: the page instance name. 
function mcml.baseNode:GetUIValue(pageInstName)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.GetUIValue) then
		return controlClass.GetUIValue(self, pageInstName);
	else
		--LOG.warn("GetUIValue on object "..self.name.." is not supported\n")	
	end
end

-- set UI value: set the value on the UI object with current node
function mcml.baseNode:SetUIValue(pageInstName, value)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.SetUIValue) then
		return controlClass.SetUIValue(self, pageInstName, value);
	else
		--LOG.warn("SetUIValue on object "..self.name.." is not supported\n")	
	end
end


-- set UI enabled: set the enabled on the UI object with current node
function mcml.baseNode:SetUIEnabled(pageInstName, value)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.SetUIEnabled) then
		return controlClass.SetUIEnabled(self, pageInstName, value);
	else
		--LOG.warn("SetUIEnabled on object "..self.name.." is not supported\n")	
	end
end

-- get UI value: get the value on the UI object with current node
-- @param instName: the page instance name. 
function mcml.baseNode:GetUIBackground(pageInstName)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.GetUIBackground) then
		return controlClass.GetUIBackground(self, pageInstName);
	else
		--LOG.warn("GetUIValue on object "..self.name.." is not supported\n")	
	end
end

-- set UI value: set the value on the UI object with current node
function mcml.baseNode:SetUIBackground(pageInstName, value)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass.SetUIBackground) then
		return controlClass.SetUIBackground(self, pageInstName, value);
	else
		--LOG.warn("SetSetUIBackgroundUIValue on object "..self.name.." is not supported\n")	
	end
end

-- call a control method
-- @param instName: the page instance name. 
-- @param methodName: name of the method.
-- @return: the value from method is returned
function mcml.baseNode:CallMethod(pageInstName, methodName, ...)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass[methodName]) then
		return controlClass[methodName](self, pageInstName, ...);
	else
		LOG.warn("CallMethod (%s) on object %s is not supported\n", tostring(methodName), self.name)
	end
end

-- return true if the page node contains a method called methodName
function mcml.baseNode:HasMethod(pageInstName, methodName)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass[methodName]) then
		return true;
	end
end

-- invoke a control method. this is same as CallMethod, except that pageInstName is ignored. 
-- @param methodName: name of the method.
-- @return: the value from method is returned
function mcml.baseNode:InvokeMethod(methodName, ...)
	local controlClass = mcml_controls.control_mapping[self.name];
	if(controlClass and controlClass[methodName]) then
		return controlClass[methodName](self, ...);
	else
		LOG.warn("InvokeMethod (%s) on object %s is not supported\n", tostring(methodName), self.name)
	end
end

function mcml.baseNode:SetObjId(id)
	self.uiobject_id = id;
end

-- get the control associated with this node. 
-- if self.uiobject_id is not nil, we will fetch it using this id, if self.control is not nil, it will be returned, otherwise we will use the unique path name to locate the control or uiobject by name. 
-- @param instName: the page instance name. if nil, we will ignore global control search in page. 
-- @return: It returns the ParaUIObject or CommonCtrl object depending on the type of the control found.
function mcml.baseNode:GetControl(pageName)
	if(self.uiobject_id) then
		local uiobj = ParaUI.GetUIObject(self.uiobject_id);
		if(uiobj:IsValid()) then
			return uiobj;
		end
	elseif(self.control) then
		return self.control;
	elseif(pageName) then
		local instName = self:GetInstanceName(pageName);
		if(instName) then
			local ctl = CommonCtrl.GetControl(instName);
			if(ctl == nil) then
				local uiobj = ParaUI.GetUIObject(instName);
				if(uiobj:IsValid()) then
					return uiobj;
				end
			else
				return ctl;	
			end
		end
	end
end

-- return font: "System;12;norm";  return nil if not available. 
function mcml.baseNode:CalculateFont(css)
	local font;
	if(css and (css["font-family"] or css["font-size"] or css["font-weight"]))then
		local font_family = css["font-family"] or "System";
		-- this is tricky. we convert font size to integer, and we will use scale if font size is either too big or too small. 
		local font_size = math.floor(tonumber(css["font-size"] or 12));
		local font_weight = css["font-weight"] or "norm";
		font = string.format("%s;%d;%s", font_family, font_size, font_weight);
	end
	return font;
end

-- get UI control 
function mcml.baseNode:GetUIControl(pageName)
	if(self.uiobject_id) then
		local uiobj = ParaUI.GetUIObject(self.uiobject_id);
		if(uiobj:IsValid()) then
			return uiobj;
		end
	else
		local instName = self:GetInstanceName(pageName);
		if(instName) then
			local uiobj = ParaUI.GetUIObject(instName);
			if(uiobj:IsValid()) then
				return uiobj;
			end
		end
	end
end

-- print information about the parent nodes
function mcml.baseNode:printParents()
	log(tostring(self.name).." is a child of ")
	if(self.parent == nil) then
		log("\n")
	else
		self.parent:printParents();
	end
end

-- print this node to log file for debugging purposes. 
function mcml.baseNode:print()
	log("<"..tostring(self.name));
	if(self.attr) then
		local name, value
		for name, value in pairs(self.attr) do
			commonlib.log(" %s=\"%s\"", name, value);
		end
	end	
	local nChildSize = table_getn(self);
	if(nChildSize>0) then
		log(">");
		local i, node;
		local text = "";
		for i=1, nChildSize do
			node = self[i];
			if(type(node) == "table") then
				log("\n")
				node:print();
			elseif(type(node) == "string") then
				log(node)
			end
		end
		log("</"..self.name..">\n");
	else
		log("/>\n");
	end
end

-- set the value of a css style attribute after mcml node is evaluated. This function is rarely used. 
-- @note: one can only call this function when the mcml node is evaluated at least once, calling this function prior to evaluation will cause the style not to inherit its parent style 
-- alternatively, we can use self:SetAttribute("style", value) to change the entire attribute. 
-- @return true if succeed. 
function mcml.baseNode:SetCssStyle(attrName, value)
	if(type(self.style) == "table") then
		self.style[attrName] = value;
		return true
	else
		local style = self:GetStyle();
		style[attrName] = value;
	end
end

-- get the ccs attribute of a given css style attribute value. 
function mcml.baseNode:GetCssStyle(attrName)
	if(type(self.style) == "table") then
		return self.style[attrName];
	end
end

-- apply any css classnames in class attribute
function mcml.baseNode:ApplyClasses()
	-- apply attribute class names
	if(self.attr and self.attr.class) then
		local pageStyle = self:GetPageStyle();
		if(pageStyle) then
			local style = self:GetStyle();
			local class_names = self:GetAttributeWithCode("class", nil, true);
			if(class_names) then
				for class_name in class_names:gmatch("[^ ]+") do
					style:Merge(pe_css.default[class_name]);
					pageStyle:ApplyToStyleItem(style, class_name);
				end
			end
		end
	end
end

-- get the css style object if any. Style will only be evaluated once and saved to self.style as a table object, unless style attribute is changed by self:SetAttribute("style", value) method. 
-- @param baseStyle: nil or parent node's style object with which the current node's style is merged.
--  if the class property of this node is not nil, it the class style is applied over baseStyle. The style property if any is applied above the class and baseStyle
-- @param base_baseStyle: this is optional. it is the base style of baseStyle
-- @return: nil or the style table which is a table of name value pairs. such as {color=string, href=string}
function mcml.baseNode:GetStyle(baseStyle, base_baseStyle)
	if(self.style) then
		return self.style;
	end
	local style = StyleItem:new();
	self.style = style;

	style:Merge(base_baseStyle);
	style:Merge(baseStyle);

	self:ApplyClasses();

	--
	-- apply instance if any
	--
	if(self.attr and self.attr.style) then
		local style_code = self:GetAttributeWithCode("style", nil, true);
		style:Merge(style_code);
	end
	return style;
end

-- @param child: it can be mcmlNode or string node. 
-- @param index: 1 based index, at which to insert the item. if nil, it will be inserted to the end
function mcml.baseNode:AddChild(child, index)
	if(type(child)=="table") then
		local nCount = table_getn(self) or 0;
		child.index = commonlib.insertArrayItem(self, index, child)
		child.parent = self;
		-- table.setn(self, nCount + 1);
	elseif(type(child)=="string") then	
		local nCount = table_getn(self) or 0;
		commonlib.insertArrayItem(self, index, child)
		-- table.setn(self, nCount + 1);
	end	
end

-- detach this node from its parent node. 
function mcml.baseNode:Detach()
	local parentNode = self.parent
	if(parentNode == nil) then
		return
	end
	
	local nSize = table_getn(parentNode);
	local i, node;
	
	if(nSize == 1) then
		parentNode[1] = nil; 
		parentNode:ClearAllChildren();
		return;
	end
	
	local i = self.index;
	local node;
	if(i<nSize) then
		local k;
		for k=i+1, nSize do
			node = parentNode[k];
			parentNode[k-1] = node;
			if(node~=nil) then
				node.index = k-1;
				parentNode[k] = nil;
			end	
		end
	else
		parentNode[i] = nil;
	end	
	-- table.setn(parentNode, nSize - 1);
end

-- check whether this baseNode has a parent with the given name. It will search recursively for all ancesters. 
-- @param name: the parent name to search for. If nil, it will return parent regardless of its name. 
-- @return: the parent object is returned. 
function mcml.baseNode:GetParent(name)
	if(name==nil) then
		return self.parent
	end
	local parent = self.parent;
	while (parent~=nil) do
		if(parent.name == name) then
			return parent;
		end
		parent = parent.parent;
	end
end

-- get the root node, it will find in ancestor nodes until one without parent is found
-- @return root node.
function mcml.baseNode:GetRoot()
	local parent = self;
	while (parent.parent~=nil) do
		parent = parent.parent;
	end
	return parent;
end

-- Get the page control(PageCtrl) that loaded this mcml page. 
function mcml.baseNode:GetPageCtrl()
	return self:GetAttribute("page_ctrl") or self:GetParentAttribute("page_ctrl");
end	

-- get the page style object shared by all page elements.
function mcml.baseNode:GetPageStyle()
	local page = self:GetPageCtrl();
	if(page) then
		return page:GetStyle();
	end
end

-- search all parent with a given attribute name. It will search recursively for all ancesters.  
-- this function is usually used for getting the "request_url" field which is inserted by MCML web browser to the top level node. 
-- @param attrName: the parent field name to search for
-- @return: the nearest parent object field is returned. it may return, if no such parent is found. 
function mcml.baseNode:GetParentAttribute(attrName)
	local parent = self.parent;
	while (parent~=nil) do
		if(parent:GetAttribute(attrName)~=nil) then
			return parent:GetAttribute(attrName);
		end
		parent = parent.parent;
	end
end

-- get the url request of the mcml node if any. It will search for "request_url" attribtue field in the ancestor of this node. 
-- PageCtrl and BrowserWnd will automatically insert "request_url" attribtue field to the root MCML node before instantiate them. 
-- @return: nil or the request_url is returned. we can extract requery string parameters using regular expressions or using GetRequestParam
function mcml.baseNode:GetRequestURL()
	return self:GetParentAttribute("request_url") or self:GetAttribute("request_url");
end

-- get request url parameter by its name. for example if page url is "www.paraengine.com/user?id=10&time=20", then GetRequestParam("id") will be 10.
-- @return: nil or string value.
function mcml.baseNode:GetRequestParam(paramName)
	local request_url = self:GetRequestURL();
	return System.localserver.UrlHelper.url_getparams(request_url, paramName)
end

-- convert a url to absolute path using "request_url" if present
-- it will replace %NAME% with their values before processing next. 
-- @param url: it is any script, image or page url path which may be absolute, site root or relative path. 
--  relative to url path can not contain "/", anotherwise it is regarded as client side relative path. such as "Texture/whitedot.png"
-- @return: it always returns absolute path. however, if path cannot be resolved, the input is returned unchanged. 
function mcml.baseNode:GetAbsoluteURL(url)
	if(not url or url=="") then return url end
	-- it will replace %NAME% with their values before processing next. 
	if(paraworld and paraworld.TranslateURL) then
		url = paraworld.TranslateURL(url);
	end
	
	if(string_find(url, "^([%w]*)://"))then
		-- already absolute path
	else	
		local request_url = self:GetRequestURL();
		if(request_url) then
			NPL.load("(gl)script/ide/System/localserver/security_model.lua");
			local secureOrigin = System.localserver.SecurityOrigin:new(request_url)
			
			if(string_find(url, "^/\\")) then
				-- relative to site root.
				if(secureOrigin.url) then
					url = secureOrigin.url..url;
				end	
			elseif(string_find(url, "[/\\]")) then
				-- if relative to url path contains "/", it is regarded as client side SDK root folder. such as "Texture/whitedot.png"
			elseif(string_find(url, "^#")) then	
				-- this is an anchor
				url = string_gsub(request_url,"^([^#]*)#.-$", "%1")..url
			else
				-- relative to request url path
				url = string_gsub(string_gsub(request_url, "%?.*$", ""), "^(.*)/[^/\\]-$", "%1/")..url
			end
		end	
	end
	return url;
end

-- get the user ID of the owner of the profile. 
function mcml.baseNode:GetOwnerUserID()
	local profile = self:GetParent("pe:profile") or self;
	if(profile) then
		return profile:GetAttribute("uid");
	end
end

-- Get child count
function mcml.baseNode:GetChildCount()
	return table_getn(self);
end

-- Clear all child nodes
function mcml.baseNode:ClearAllChildren()
	commonlib.resize(self, 0);
	-- table.setn(self, 0);
end

-- generate a less compare function according to a node field name. 
-- @param fieldName: the name of the field, such as "text", "name", etc
function mcml.baseNode.GenerateLessCFByField(fieldName)
	fieldName = fieldName or "name";
	return function(node1, node2)
		if(node1[fieldName] == nil) then
			return true
		elseif(node2[fieldName] == nil) then
			return false
		else
			return node1[fieldName] < node2[fieldName];
		end	
	end
end

-- generate a greater compare function according to a node field name. 
-- @param fieldName: the name of the field, such as "text", "name", etc
--   One can also build a compare function by calling mcml.baseNode.GenerateLessCFByField(fieldName) or mcml.baseNode.GenerateGreaterCFByField(fieldName)
function mcml.baseNode.GenerateGreaterCFByField(fieldName)
	fieldName = fieldName or "name";
	return function(node1, node2)
		if(node2[fieldName] == nil) then
			return true
		elseif(node1[fieldName] == nil) then
			return false
		else
			return node1[fieldName] > node2[fieldName];
		end	
	end
end

-- sorting the children according to a compare function. Internally it uses table.sort().
-- Note: child indices are rebuilt and may cause UI binded controls to misbehave
-- compareFunc: if nil, it will compare by node.name. 
function mcml.baseNode:SortChildren(compareFunc)
	compareFunc = compareFunc or mcml.baseNode.GenerateLessCFByField("name");
	-- quick sort
	table.sort(self, compareFunc)
	-- rebuild index. 
	local i, node
	for i,node in ipairs(self) do
		node.index = i;
	end
end

-- get a string containing the node path. such as "1/1/1/3"
-- as long as the baseNode does not change, the node path uniquely identifies a baseNode.
function mcml.baseNode:GetNodePath()
	local path = tostring(self.index);
	while (self.parent ~=nil) do
		path = tostring(self.parent.index).."/"..path;
		self = self.parent;
	end
	return path;
end

-- @param rootName: a name that uniquely identifies a UI instance of this object, usually the userid or app_key. The function will generate a sub control name by concartinating this rootname with relative baseNode path. 
function mcml.baseNode:GetInstanceName(rootName)
	return tostring(rootName)..self:GetNodePath();
end

-- get the first occurance of first level child node whose name is name
-- @param name: if can be the name of the node, or it can be a interger index. 
function mcml.baseNode:GetChild(name)
	if(type(name) == "number") then
		return self[name];
	else
		local nSize = table_getn(self);
		local i, node;
		for i=1, nSize do
			node = self[i];
			if(type(node)=="table" and name == node.name) then
				return node;
			end
		end
	end	
end

-- get the first occurance of first level child node whose name is name
-- @param name: if can be the name of the node, or it can be a interger index. 
-- @return nil if not found
function mcml.baseNode:GetChildWithAttribute(name, value)
	local nSize = table_getn(self);
	local i, node;
	for i=1, nSize do
		node = self[i];
		if(type(node)=="table") then
			if(value == node:GetAttribute(name)) then
				return node;
			end	
		end
	end
end

-- get the first occurance of child node whose attribute name is value. it will search for all child nodes recursively. 
function mcml.baseNode:SearchChildByAttribute(name, value)
	local nSize = table_getn(self);
	local i, node;
	for i=1, nSize do
		node = self[i];
		if(type(node)=="table") then
			if(value == node:GetAttribute(name)) then
				return node;
			else
				node = node:SearchChildByAttribute(name, value);
				if(node) then
					return node;
				end
			end	
		end
	end
end

-- return an iterator of all first level child nodes whose name is name
-- a more advanced way to tranverse mcml tree is using ide/Xpath
-- @param name: if name is nil, all child is returned. 
function mcml.baseNode:next(name)
	local nSize = table_getn(self);
	local i = 1;
	return function ()
		local node;
		while i <= nSize do
			node = self[i];
			i = i+1;
			if(not name or (type(node) == "table" and name == node.name)) then
				return node;
			end
		end
	end	
end


-- this is a jquery meta table, if one wants to add jquery-like function calls, just set this metatable as the class array table. 
-- e.g. setmetatable(some_table, jquery_metatable)
local jquery_metatable = {
	-- each invocation will create additional tables and closures, hence the performance is not supper good. 
	__index = function(t, k)
		if(type(k) == "string") then
			local func = {};
			setmetatable(func, {
				-- the first parameter is always the mcml_node. 
				-- the return value is always the last node's result
				__call = function(self, self1, ...)
					local output;
					local i, node
					for i, node in ipairs(t) do
						if(type(node[k]) == "function")then
							output = node[k](node, ...);
						end
					end
					return output;
				end,
			});
			return func;
		elseif(type(k) == "number") then
			return t[k];
		end
	end,
}

-- provide jquery-like syntax to find all nodes that match a given name pattern and then use the returned object to invoke a method on all returned nodes. 
-- it can also be used to create a new node like "<div />"
--  e.g. node:jquery("a"):show();
-- @param pattern: The valid format is [tag_name][#name_id][.class_name] or "<tag_name />". 
--  e.g. "div#name.class_name", "#some_name", ".some_class", "div"
--  e.g. "<div />" will create a new node. 
-- @param param1: additional xml node when pattern is "<tag_name />"
function mcml.baseNode:jquery(pattern, param1)
	local tagName = pattern and pattern:match("^<([^%s/>]*)");
	if(tagName) then
		param1 = param1 or {name=tagName, attr={}};
		param1.name = param1.name or tagName;
		return System.mcml.new(nil, param1);
	else
		local output = {}
		if(pattern) then
			local tag_name, pattern = pattern:match("^([^#%.]*)(.*)");
			if(tag_name == "") then
				tag_name = nil;
			end
			local id;
			if(pattern) then
				id = pattern:match("#([^#%.]+)");
			end
			local class_name;
			if(pattern) then
				class_name = pattern:match("%.([^#%.]+)");
			end
			self:GetAllChildWithNameIDClass(tag_name, id, class_name, output);
		
		end
		setmetatable(output, jquery_metatable)
		return output;
	end
end

-- show this node. one may needs to refresh the page if page is already rendered
function mcml.baseNode:show()
	self:SetAttribute("display", nil)
end

-- hide this node. one may needs to refresh the page if page is already rendered
function mcml.baseNode:hide()
	self:SetAttribute("display", "none")
end

-- get/set inner text
-- @param v: if not nil, it will set inner text instead of get
-- return the inner text or empty string. 
function mcml.baseNode:text(v)
	if(v == nil) then
		local inner_text = self[1];
		if(type(inner_text) == "string") then
			return inner_text;
		else
			return ""
		end
	else
		self:ClearAllChildren();
		self[1] = v;
	end
end

-- get/set ui or node value of the node. 
-- @param v: if not nil, it will set value instead of get
function mcml.baseNode:value(v)
	if(v == nil) then
		local value_ = self:GetUIValue();
		if(value_==nil) then
			return self:GetValue();
		else
			return value_;	
		end	
	else
		self:SetUIValue(v);
		self:SetValue(v);
	end
end

-- return a table containing all child nodes whose name is name. (it will search recursively)
-- a more advanced way to tranverse mcml tree is using ide/Xpath
-- @param name: the tag name. if nil it matches all
-- @param id: the name attribute. if nil it matches all
-- @param class: the class attribute. if nil it matches all
-- @param output: nil or a table to receive the result. child nodes with the name is saved to this table array. if nil, a new table will be created. 
-- @return output: the output table containing all children. It may be nil if no one is found and input "output" is also nil.
function mcml.baseNode:GetAllChildWithNameIDClass(name, id, class, output)
	local nSize = table_getn(self);
	local i = 1;
	local node;
	while i <= nSize do
		node = self[i];
		i = i+1;
		if(type(node) == "table") then
			if( (not name or name == node.name) and
				(not id or id == node:GetAttribute("name")) and
				(not class or class==node:GetAttribute("class")) ) then
				output = output or {};
				table.insert(output, node);
			else
				output = node:GetAllChildWithNameIDClass(name, id, class, output)
			end	
		end
	end
	return output;
end

-- return a table containing all child nodes whose name is name. (it will search recursively)
-- a more advanced way to tranverse mcml tree is using ide/Xpath
-- @param name: the tag name
-- @param output: nil or a table to receive the result. child nodes with the name is saved to this table array. if nil, a new table will be created. 
-- @return output: the output table containing all children. It may be nil if no one is found and input "output" is also nil.
function mcml.baseNode:GetAllChildWithName(name, output)
	local nSize = table_getn(self);
	local i = 1;
	local node;
	while i <= nSize do
		node = self[i];
		i = i+1;
		if(type(node) == "table") then
			if(name == node.name) then
				output = output or {};
				table.insert(output, node);
			else
				output = node:GetAllChildWithName(name, output)
			end	
		end
	end
	return output;
end

-- return an iterator of all child nodes whose attribtue attrName is attrValue. (it will search recursively)
-- a more advanced way to tranverse mcml tree is using ide/Xpath
-- @param name: if name is nil, all child is returned. 
-- @param output: nil or a table to receive the result. child nodes with the name is saved to this table array. if nil, a new table will be created. 
-- @return output: the output table containing all children. It may be nil if no one is found and input "output" is also nil.
function mcml.baseNode:GetAllChildWithAttribute(attrName, attrValue, output)
	local nSize = table_getn(self);
	local i = 1;
	local node;
	while i <= nSize do
		node = self[i];
		i = i+1;
		if(type(node) == "table") then
			if(node:GetAttribute(attrName) == attrValue) then
				output = output or {};
				table.insert(output, node);
			else
				output = node:GetAllChildWithAttribute(attrName, attrValue, output)
			end	
		end
	end
	return output;
end

-- this function will apply self.pre_values to current page scope during rendering.
-- making it accessible to XPath and Eval function.  
function mcml.baseNode:ApplyPreValues()
	if(type(self.pre_values) == "table") then
		local pageScope = self:GetPageCtrl():GetPageScope();
		if(pageScope) then
			for name, value in pairs(self.pre_values) do
				pageScope[name] = value;
			end
		end
	end
end

-- apply a given pre value to this node, so that when the node is rendered, the name, value pairs will be
-- written to the current page scope. Not all mcml node support pre values. it is most often used by databinding template node. 
function mcml.baseNode:SetPreValue(name, value)
	self.pre_values = self.pre_values or {};
	self.pre_values[name] = value;
end

-- get a prevalue by name. this function is usually called on data binded mcml node 
-- @param name: name of the pre value
-- @param bSearchParent: if true, it will search parent node recursively until name is found or root node is reached. 
function mcml.baseNode:GetPreValue(name, bSearchParent)
	if(self.pre_values) then
		return self.pre_values[name];
	elseif(bSearchParent) then
		local parent = self.parent;
		while (parent~=nil) do
			if(parent.pre_values) then
				return parent.pre_values[name];
			end
			parent = parent.parent;
		end
	end
end

-- here we will translate current node and all of its child nodes recursively, using the given langTable 
-- unless any of the child attribute disables or specifies a different lang using the trans attribute
-- @note: it will secretly mark an already translated node, so it will not be translated twice when the next time this method is called.
-- @param langTable: this is a translation table from CommonCtrl.Locale(transName); if this is nil, 
-- @param transName: the translation name of the langTable. 
function mcml.baseNode:TranslateMe(langTable, transName)
	local trans = self:GetAttribute("trans");
	if(trans) then
		if(trans == "no" or trans == "none") then 
			return
		elseif(trans ~= transName) then
			langTable = CommonCtrl.Locale(trans);
			transName = trans;
			if(not langTable) then
				LOG.warn("lang table %s is not found for the mcml page\n", trans);
			end
		end	
		-- secretly mark an already translated node, so it will not be translated twice when the next time this method is called.
		if(self.IsTranslated) then
			return
		else
			self.IsTranslated = true;
		end
	end	
	-- translate this and all child nodes recursively
	if(langTable) then
		-- translate attributes of current node. 
		if(self.attr) then
			local name, value 
			for name, value in pairs(self.attr) do
				-- we will skip some attributes. 
				if(name~="style" and name~="id" and name~="name") then
					if(type(value) == "string") then
						-- TRANSLATE: translate value
						if(langTable:HasTranslation(value)) then
							--commonlib.echo(langTable(value))
							self.attr[name] = langTable(value);
						end	
					end
				end	
			end
		end
	
		-- translate child nodes recursively. 	
		local nSize = table_getn(self);
		local i = 1;
		local node;
		while i <= nSize do
			node = self[i];
			if(type(node) == "table") then
				node:TranslateMe(langTable, transName)
			elseif(type(node) == "string") then
				-- only translate if the node is not unknown and not script node.
				if(self.name ~= "script" and self.name ~= "unknown" and self.name ~= "pe:script") then
					-- TRANSLATE: translate inner text
					if(langTable:HasTranslation(node)) then
						--commonlib.echo(langTable(node))
						self[i] = langTable(node)
					end
				end	
			end
			i = i+1;
		end
	end
end

-- if there an attribute called variables. 
-- variables are frequently used for localization in mcml. Both table based localization and commonlib.Locale based localization are supported. 
function mcml.baseNode:ProcessVariables()
	local variables_str = self:GetAttribute("variables");
	if(variables_str and not self.__variable_processed) then
		self.__variable_processed = true;

		--  a table containing all variables
		local variables = {};

		local var_name, var_value
		for var_name, var_value in string.gmatch(variables_str, "%$(%w*)=([^;%$]+)") do
			local func = commonlib.getfield(var_value) or commonlib.Locale:GetByName(var_value);
			variable = {
					var_name=var_name, 
					match_exp="%$"..var_name.."{([^}]*)}", 
					gsub_exp="%$"..var_name.."{[^}]*}", 
				};
			if(not func) then
				-- try to find a locale file with value under the given folder
				-- suppose var_value is "locale.mcml.IDE", then we will first try "locale/mcml/IDE.lua" and then try "locale/mcml/IDE_enUS.lua"
				local filename = var_value:gsub("%.", "/");
				local locale_file1 = format("%s.lua", filename);
				local locale_file2 = format("%s_%s.lua", filename, ParaEngine.GetLocale());
				if(ParaIO.DoesFileExist(locale_file1)) then
					filename = locale_file1;
				elseif(ParaIO.DoesFileExist(locale_file2)) then
					filename = locale_file2;
				else
					filename = nil;
				end
				if(filename) then
					NPL.load("(gl)"..filename);
					LOG.std(nil, "system", "mcml", "loaded variable file %s for %s", filename, var_value);
					func = commonlib.getfield(var_value) or commonlib.Locale:GetByName(var_value);
					if(not func) then
						func = commonlib.gettable(var_value);
						LOG.std(nil, "warn", "mcml", "empty table is created and used for variable %s. Ideally it should be %s or %s", var_value, locale_file1, locale_file2);
					end
				else
					LOG.std(nil, "warn", "mcml", "can not find variable table file for %s. It should be %s or %s", var_value, locale_file1, locale_file2);
				end
			end

			if(type(func) == "function") then
				variable.func = func
				variables[#variables+1] = variable;
			elseif(type(func) == "table") then
				local meta_table = getmetatable(func);
				if(meta_table and meta_table.__call) then
					variable.func = func
				else
					variable.func = function(name)
						return func[name];
					end
				end
				variables[#variables+1] = variable;
			else
				LOG.std(nil, "warn", "mcml", "unsupported $ %s params", var_name);
			end
		end

		if(#variables>0) then
			self:ReplaceVariables(variables);
		end
	end
end

function mcml.baseNode:ReplaceVariables(variables)
	if(variables) then
		-- translate this and all child nodes recursively
		-- translate attributes of current node. 
		if(self.attr) then
			local name, value 
			for name, value in pairs(self.attr) do
				-- we will skip some attributes. 
				if(type(value) == "string") then
					-- REPLACE
					local k;
					for k=1, #variables do
						local variable = variables[k];
						local var_value = value:match(variable.match_exp)
						if(var_value) then
							value = value:gsub(variable.gsub_exp, variable.func(var_value) or var_value);
							self.attr[name] = value;
						end
					end
				end
			end
		end
	
		-- translate child nodes recursively. 	
		local nSize = table_getn(self);
		local i = 1;
		local node;
		while i <= nSize do
			node = self[i];
			if(type(node) == "table") then
				node:ReplaceVariables(variables)
			elseif(type(node) == "string") then
				local value = node;
				-- REPLACE
				local k;
				for k=1, #variables do
					local variable = variables[k];
					local var_value = value:match(variable.match_exp)
					if(var_value) then
						value = value:gsub(variable.gsub_exp, variable.func(var_value) or var_value); 
						self[i] = value;
					end
				end
			end
			i = i+1;
		end
	end
end

-- This callback is used mostly with DrawDisplayBlock() function. 
-- @param mcmlNode: this mcml node. 
-- @param _parent: the ui object inside which UI controls should be created. 
-- @param left, top, width, height: this is actually left, top, right, bottom relative to _parent control (css padding is NOT applied). 
-- @param myLayout: this is the layout inside which child nodes should be created (css padding is applied). 
function mcml.baseNode.DrawChildBlocks_Callback(mcmlNode, rootName, bindingContext, _parent, left, top, width, height, myLayout, css)
	for childnode in mcmlNode:next() do
		local left, top, width, height = myLayout:GetPreferredRect();
		Map3DSystem.mcml_controls.create(rootName, childnode, bindingContext, _parent, left, top, width, height, 
			{display=css["display"], color = css.color, ["font-family"] = css["font-family"],  ["font-size"]=css["font-size"], ["font-weight"] = css["font-weight"], ["text-align"] = css["text-align"], ["text-shadow"] = css["text-shadow"], ["base-font-size"] = css["base-font-size"]}, myLayout)
	end
end


-- Call this function to draw display block with a custom callback. 
-- This function is usually called by the mcml tag's create() function.
-- Right now, mcml renderer uses one pass rendering, hence there is some limitation on block layout capabilities. 
-- One of the biggest limitation is that all floating display blocks must have explicit size specified in css in order to function.
-- A multi-pass renderer can do more flexible layout, yet at the cost of code complexity and CPU. 
-- This function supports all features of the original mcml's div tag. 
-- @param parentLayout: the parent layout structure. When this function returns, the parent layout will be modified. 
-- @param _parent: the ui object inside which UI controls should be created. 
-- @param left, top, width, height: this is actually left, top, right, bottom relative to _parent control. 
-- @param style: the parent css style. 
-- @param render_callback: a function(mcmlNode, rootName, bindingContext, _parent, myLayout, css) end, inside which we can render the content.
--  this function can return ignore_onclick, ignore_background. if true it will ignore onclick and background handling 
--  see self.DrawChildBlocks_Callback for an example callback
function mcml.baseNode:DrawDisplayBlock(rootName, bindingContext, _parent, left, top, width, height, parentLayout, style, render_callback)
	local mcmlNode = self;
	if(mcmlNode:GetAttribute("display") == "none") then return end

	-- process any variables that is taking place. 
	mcmlNode:ProcessVariables();

	local css = mcmlNode:GetStyle(pe_html.css[mcmlNode.name], style) or {};
	if(style) then
		-- pass through some css styles from parent. 
		css.color = css.color or style.color;
		css["font-family"] = css["font-family"] or style["font-family"];
		css["font-size"] = css["font-size"] or style["font-size"];
		css["font-weight"] = css["font-weight"] or style["font-weight"];
		css["text-shadow"] = css["text-shadow"] or style["text-shadow"];
	end

	local padding_left, padding_top, padding_bottom, padding_right = 
		(css["padding-left"] or css["padding"] or 0),(css["padding-top"] or css["padding"] or 0),
		(css["padding-bottom"] or css["padding"] or 0),(css["padding-right"] or css["padding"] or 0);
	local margin_left, margin_top, margin_bottom, margin_right = 
		(css["margin-left"] or css["margin"] or 0),(css["margin-top"] or css["margin"] or 0),
		(css["margin-bottom"] or css["margin"] or 0),(css["margin-right"] or css["margin"] or 0);	

	local availWidth, availHeight = parentLayout:GetPreferredSize();
	local maxWidth, maxHeight = parentLayout:GetMaxSize();

	if(css["max-width"]) then
		local max_width = css["max-width"];
		if(maxWidth>max_width) then
			local left, top, right, bottom = parentLayout:GetAvailableRect();
			-- align at center. 
			local align = mcmlNode:GetAttribute("align") or css["align"];
			if(align == "center") then
				left = left + (maxWidth - max_width)/2
			elseif(align == "right") then
				left = right - max_width;
			end	
			right = left + max_width;
			parentLayout:reset(left, top, right, bottom);
		end
	end

	if(css["max-height"]) then
		local max_height = css["max-height"];
		if(maxHeight>max_height) then
			local left, top, right, bottom = parentLayout:GetAvailableRect();
			-- align at center. 
			local valign = mcmlNode:GetAttribute("valign") or css["valign"];
			if(valign == "center") then
				top = top + (maxHeight - max_height)/2
			elseif(valign == "bottom") then
				top = bottom - max_height;
			end	
			bottom = top + max_height;
			parentLayout:reset(left, top, right, bottom);
		end
	end
	
	if(mcmlNode:GetAttribute("trans")) then
		-- here we will translate all child nodes recursively, using the given lang 
		-- unless any of the child attribute disables or specifies a different lang
		mcmlNode:TranslateMe();
	end
	
	local width, height = mcmlNode:GetAttribute("width"), mcmlNode:GetAttribute("height");
	if(width) then
		css.width = tonumber(string.match(width, "%d+"));
		if(css.width and string.match(width, "%%$")) then
			if(css.position == "screen") then
				css.width = ParaUI.GetUIObject("root").width * css.width/100;
			else	
				css.width=math.floor((maxWidth-margin_left-margin_right)*css.width/100);
				if(availWidth<(css.width+margin_left+margin_right)) then
					css.width=availWidth-margin_left-margin_right;
				end
				if(css.width<=0) then
					css.width = nil;
				end
			end	
		end	
	end
	if(height) then
		css.height = tonumber(string.match(height, "%d+"));
		if(css.height and string.match(height, "%%$")) then
			if(css.position == "screen") then
				css.height = ParaUI.GetUIObject("root").height * css.height/100;
			else	
				css.height=math.floor((maxHeight-margin_top-margin_bottom)*css.height/100);
				if(availHeight<(css.height+margin_top+margin_bottom)) then
					css.height=availHeight-margin_top-margin_bottom;
				end
				if(css.height<=0) then
					css.height = nil;
				end
			end	
		end	
	end
	
	-- whether this control takes up space
	local bUseSpace; 
	if(css.float) then
		local minWidth = css.width or css["min-width"];
		if(minWidth) then
			if(availWidth<(minWidth+margin_left+margin_right)) then
				parentLayout:NewLine();
			end
		end	
	else
		parentLayout:NewLine();
	end
	local myLayout = parentLayout:clone();
	myLayout:ResetUsedSize();
	
	if(css.width) then
		local align = mcmlNode:GetAttribute("align") or css["align"];
		if(align and align~="left") then
			local max_width = css.width;
			local left, top, right, bottom = myLayout:GetAvailableRect();
			-- align at center. 
			if(align == "center") then
				left = left + (maxWidth - max_width)/2
			elseif(align == "right") then
				max_width = max_width + margin_left + margin_right;
				left = right - max_width;
			end	
			right = left + max_width
			myLayout:reset(left, top, right, bottom);
		end
	end
	if(css.height) then
		-- align at center. 
		local valign = mcmlNode:GetAttribute("valign") or css["valign"];
		if(valign and valign~="top") then
			local max_height = css.height;
			local left, top, right, bottom = myLayout:GetAvailableRect();
			if(valign == "center") then
				top = top + (maxHeight - max_height)/2
			elseif(valign == "bottom") then
				max_height = max_height + margin_top + margin_bottom;
				top = bottom - max_height;
			end	
			bottom = top + max_height
			myLayout:reset(left, top, right, bottom);
		end
	end

	if(css.position == "absolute") then
		-- absolute positioning in parent
		if(css.width and css.height and css.left and css.top) then
			-- if all rect is provided, we will do true absolute position. 
			myLayout:reset(css.left, css.top, css.left + css.width, css.top + css.height);
		else
			-- this still subject to parent rect. 
			myLayout:SetPos(css.left, css.top);
		end
		myLayout:ResetUsedSize();
	elseif(css.position == "relative") then
		-- relative positioning in next render position. 
		myLayout:OffsetPos(css.left, css.top);
	elseif(css.position == "screen") then	
		-- relative positioning in screen client area
		local offset_x, offset_y = 0, 0;
		local left, top = mcmlNode:GetAttribute("left"), mcmlNode:GetAttribute("top");
		if(left) then
			left = tonumber(string.match(left, "(%d+)%%$"));
			offset_x = ParaUI.GetUIObject("root").width * left/100;
		end
		if(top) then
			top = tonumber(string.match(top, "(%d+)%%$"));
			offset_y = ParaUI.GetUIObject("root").height * top/100;
		end
		local px,py = _parent:GetAbsPosition();
		myLayout:SetPos((css.left or 0)-px + offset_x, (css.top or 0)-py + offset_y); 
	else
		myLayout:OffsetPos(css.left, css.top);
		bUseSpace = true;	
	end
	
	left,top = myLayout:GetAvailablePos();
	myLayout:SetPos(left,top);
	width,height = myLayout:GetSize();
	
	if(css.width) then
		myLayout:IncWidth(left+margin_left+margin_right+css.width-width)
	end
	
	if(css.height) then
		myLayout:IncHeight(top+margin_top+margin_bottom+css.height-height)
	end	
	
	-- for inner control preferred size
	myLayout:OffsetPos(margin_left+padding_left, margin_top+padding_top);
	myLayout:IncWidth(-margin_right-padding_right)
	myLayout:IncHeight(-margin_bottom-padding_bottom)	

	---------------------------------
	-- draw inner nodes.
	---------------------------------
	local ignore_onclick, ignore_background, ignore_tooltip;

	
	if(render_callback) then
		local left, top, width, height = myLayout:GetPreferredRect();
		ignore_onclick, ignore_background, ignore_tooltip = render_callback(mcmlNode, rootName, bindingContext, _parent, left-padding_left, top-padding_top, width+padding_right, height+padding_bottom, myLayout, css);
	end

	local width, height = myLayout:GetUsedSize()
	width = width + padding_right + margin_right
	height = height + padding_bottom + margin_bottom
	if(css.width) then
		width = left + css.width + margin_left+margin_right;
	end	
	if(css.height) then
		height = top + css.height + margin_top+margin_bottom;
	end
	if(css["min-width"]) then
		local min_width = css["min-width"];
		if((width-left) < min_width) then
			width = left + min_width;
		end
	end
	if(css["min-height"]) then
		local min_height = css["min-height"];
		if((height-top) < min_height) then
			height = top + min_height;
		end
	end
	if(css["max-height"]) then
		local max_height = css["max-height"];
		if((height-top) > max_height) then
			height = top + max_height;
		end
	end
	if(bUseSpace) then
		parentLayout:AddObject(width-left, height-top);
		if(not css.float) then
			parentLayout:NewLine();
		end	
	end
	local onclick, ontouch;
	local onclick_for;
	if(not ignore_onclick) then
		onclick = mcmlNode:GetString("onclick");
		if(onclick == "") then
			onclick = nil;
		end
		onclick_for = mcmlNode:GetString("for");
		if(onclick_for == "") then
			onclick_for = nil;
		end
		ontouch = mcmlNode:GetString("ontouch");
		if(ontouch == "") then
			ontouch = nil;
		end
	end
	local tooltip
	if(not ignore_tooltip) then
		tooltip = mcmlNode:GetAttributeWithCode("tooltip",nil,true);
		if(tooltip == "") then
			tooltip = nil;
		end
	end
	local background;
	if(not ignore_background) then
		background = mcmlNode:GetAttribute("background") or css.background;
	end
	if(css["background-color"] and not ignore_background) then
		if(not background and not css.background2) then
			background = "Texture/whitedot.png";
		end
	end

	if(onclick_for or onclick or tooltip or ontouch) then
		-- if there is onclick event, the inner nodes will not be interactive.
		local instName = mcmlNode:GetInstanceName(rootName);
		local _this=ParaUI.CreateUIObject("button",instName or "b","_lt", left+margin_left, top+margin_top, width-left-margin_left-margin_right, height-top-margin_top-margin_bottom);
		mcmlNode.uiobject_id = _this.id;
		if(background) then
			_this.background = background;
			if(background~="") then
				if(css["background-color"]) then
					_guihelper.SetUIColor(_this, css["background-color"]);
				end	
				if(css["background-rotation"]) then
					_this.rotation = tonumber(css["background-rotation"])
				end
				if(css["background-repeat"] == "repeat") then
					_this:GetAttributeObject():SetField("UVWrappingEnabled", true);
				end
			end
			if(css["background-animation"]) then
				local anim_file = string.gsub(css["background-animation"], "url%((.*)%)", "%1");
				local fileName,animName = string.match(anim_file, "^([^#]+)#(.*)$");
				if(fileName and animName) then
					UIAnimManager.PlayUIAnimationSequence(_this, fileName, animName, true);
				end
			end
		else
			_this.background = "";
		end
		if(css.background2 and not ignore_background) then
			_guihelper.SetVistaStyleButton(_this, nil, css.background2);
		end
		local zorder = mcmlNode:GetNumber("zorder");
		if(zorder) then
			_this.zorder = zorder
		end
		if(onclick_for or onclick or ontouch) then
			local btnName = mcmlNode:GetAttributeWithCode("name")
			-- tricky: we will just prefetch any params with code that may be used in the callback 
			local i;
			for i=1,5 do
				if(not mcmlNode:GetAttributeWithCode("param"..i)) then
					break;
				end
			end
			if(onclick_for or onclick) then
				_this:SetScript("onclick", Map3DSystem.mcml_controls.pe_editor_button.on_click, mcmlNode, instName, bindingContext, btnName);
			elseif(ontouch) then
				_this:SetScript("ontouch", Map3DSystem.mcml_controls.pe_editor_button.on_touch, mcmlNode, instName, bindingContext, btnName);
			end
		end	
		if(tooltip) then
			local tooltip_page = string.match(tooltip or "", "page://(.+)");
			local tooltip_static_page = string.match(tooltip or "", "page_static://(.+)");
			if(tooltip_page) then
				CommonCtrl.TooltipHelper.BindObjTooltip(mcmlNode.uiobject_id, tooltip_page, mcmlNode:GetNumber("tooltip_offset_x"), mcmlNode:GetNumber("tooltip_offset_y"), mcmlNode:GetNumber("show_width"),mcmlNode:GetNumber("show_height"),mcmlNode:GetNumber("show_duration"), mcmlNode:GetBool("enable_tooltip_hover"), nil, mcmlNode:GetBool("tooltip_is_interactive"), mcmlNode:GetBool("is_lock_position"), mcmlNode:GetBool("use_mouse_offset"), mcmlNode:GetNumber("screen_padding_bottom"), nil, nil, nil, mcmlNode:GetBool("offset_ctrl_width"), mcmlNode:GetBool("offset_ctrl_height"));
			elseif(tooltip_static_page) then
				CommonCtrl.TooltipHelper.BindObjTooltip(mcmlNode.uiobject_id, tooltip_static_page, mcmlNode:GetNumber("tooltip_offset_x"), mcmlNode:GetNumber("tooltip_offset_y"), mcmlNode:GetNumber("show_width"),mcmlNode:GetNumber("show_height"),mcmlNode:GetNumber("show_duration"),mcmlNode:GetBool("enable_tooltip_hover"),mcmlNode:GetBool("click_through"));
			else
				_this.tooltip = tooltip;
			end
		end
		_parent:AddChild(_this);
	else
		if(background) then
			local instName;
			if(mcmlNode:GetAttribute("name") or mcmlNode:GetAttribute("id")) then
				-- this is solely for giving a global name to background image control so that it can be animated
				-- background image control is mutually exclusive with inner text control. hence if there is a background, inner text becomes anonymous
				instName = mcmlNode:GetInstanceName(rootName);
			end	
			local _this=ParaUI.CreateUIObject("button",instName or "b","_lt", left+margin_left, top+margin_top, width-left-margin_left-margin_right, height-top-margin_top-margin_bottom);
			_this.background = background;
			_this.enabled = false;
			mcmlNode.uiobject_id = _this.id;
			if(css["background-color"]) then
				_guihelper.SetUIColor(_this, css["background-color"]);
			else
				_guihelper.SetUIColor(_this, "255 255 255 255");
			end	
			if(css["background-rotation"]) then
				_this.rotation = tonumber(css["background-rotation"])
			end
			if(css["background-repeat"] == "repeat") then
				_this:GetAttributeObject():SetField("UVWrappingEnabled", true);
			end
			_parent:AddChild(_this);
			local zorder = mcmlNode:GetNumber("zorder");
			if(zorder) then
				_this.zorder = zorder
			end
			_this:BringToBack();
			if(css["background-animation"]) then
				local anim_file = string.gsub(css["background-animation"], "url%((.*)%)", "%1");
				local fileName,animName = string.match(anim_file, "^([^#]+)#(.*)$");
				if(fileName and animName) then
					UIAnimManager.PlayUIAnimationSequence(_this, fileName, animName, true);
				end
			end
		elseif(mcmlNode:GetBool("enabled") == false) then
			local _this=ParaUI.CreateUIObject("button","b","_lt", left+margin_left, top+margin_top, width-left-margin_left-margin_right, height-top-margin_top-margin_bottom);
			if(tooltip) then
				_this.tooltip = tooltip;
			end
			_this.background = background or "";
			_parent:AddChild(_this);
		end
	end	
	
	-- call onload(mcmlNode) function if any. 
	local onloadFunc = mcmlNode:GetString("onload");
	if(onloadFunc and onloadFunc~="") then
		Map3DSystem.mcml_controls.pe_script.BeginCode(mcmlNode);
		local pFunc = commonlib.getfield(onloadFunc);
		if(type(pFunc) == "function") then
			pFunc(mcmlNode);
		else
			LOG.std("", "warn", "mcml", "%s node's onload call back: %s is not a valid function.", mcmlNode.name, onloadFunc)	
		end
		Map3DSystem.mcml_controls.pe_script.EndCode(rootName, mcmlNode, bindingContext, _parent, left, top, width, height,style, parentLayout);
	end
end

-- fire a given page event by its name
-- @param event_name: such as "onclick". 
function mcml.baseNode:OnPageEvent(event_name, ...)
	local callback_script = self:GetString(event_name);
	if(callback_script and callback_script~="") then
		Map3DSystem.mcml_controls.OnPageEvent(self, callback_script, ...);
	end
end

--[[
Title: header file for all mcml tag node definitions and data binding controls
Author(s): LiXizhi, WangTian
Date: 2008/2/14
Desc: mcml is an XML format describing profile box items and other display items in paraworld, such as task, quick action, action feed, tradableitem, etc. 
One can think of it as the HTML counterpart in 3D social networking world for describing renderable objects in 2D and 3D. 
it conforms with the ide/LuaXML conversion format, so that the script table defined here has a strict XML translation. 
mcml is a universal format defined by ParaEngine. and any thing in the name space "pe" is official mcml control node that can be data binded to NPL controls. 
mcml_controls for rendering mcml data is defined in mcml/mcml_controls and mcml/pe_* files. 

tag overview: 
	- social tags: pe:profile pe:userinfo pe:friends pe:app pe:name pe:profile-action pe:profile-box pe:app-home-button
	- map tags: pe:map-mark pe:map-mark2d pe:map-tile
	- design tags: pe:container pe:dialog pe:tabs pe:tab-item pe:treeview pe:treenode pe:image pe:flash
	- component tags:pe:roomhost pe:market pe:comments 
	- editor display: pe:editor pe:editor-buttonset pe:editor-button pe:editor-text pe:editor-divider pe:editor-custom pe:editor-radiobox(same as <input type="radio">) pe:editor-checkbox (same as <input type="checkbox">)
		HTML editor tags are implemented by editor: 
		<input type="checkbox" name="option2" value="Butter" checked="true"/> 
		<input type="radio" name="group1" value="Milk"/> 
		<input type="radio" name="group1" value="Butter"/> 
		<select name="select" size="3">
			<option selected="selected">line1</option>
			<option>line2</option>
		</select>
	- control tags: pe:visible-to-owner
	- worlds tags:pe:world pe:world-ip pe:model pe:avatar
	- HTML tags:<text>, h1, h2,h3, h4, li, p, div, hr, a(href), img(attr: src,height, width, title), <form>
			anyTag(attr: style="float:left;color: #006699; left: -60px; position: relative; top: 30px;width: 100px;height: 100px;class:"box";margin:5;margin-top:5;padding:5;background:url;background-color:#FF0000"),
			By default: <text>, font,a(href) will float around previous control, allowing content to automatically wrap to the next line. 
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml.lua");
-- to create a user defined tag
local node = Map3DSystem.mcml.new("pe:profile", {})
-- to deserialize from xml data or pure table. 
local node = Map3DSystem.mcml.buildclass(node);
-- to render(create) databinding controls for an mcml node. 
Map3DSystem.mcml_controls.create("me", node, bindingContext, _parent, left, top, right, bottom)
-- one can access a node via baseNode functions (see mcml/mcml_base) or using ide/Xpath
-------------------------------------------------------
]]

if(not Map3DSystem.mcml) then Map3DSystem.mcml = {} end

-- base mcml public functions
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml_base.lua");
-- all data binding controls
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml_controls.lua");

local mcml = Map3DSystem.mcml;
--------------------------------------
-- social tags
--------------------------------------
-- the profile mcml root node that specifys a version of the mcml body. 
mcml["pe:profile"] = mcml.new("baseNode", {
	name = "pe:profile", 
	attr = {
		version = "1.0",
		-- user id
		uid = nil,
	}
	-- child nodes: "pe:userinfo", "pe:friends", "pe:app"
});

-- user info 
mcml["pe:userinfo"] = mcml.new("baseNode", {
	name = "pe:userinfo", 
	attr = {
		-- user id
		uid = nil,
		-- user name
		name = nil, 
		-- user photo path or photo id, photo path can be deduced from photo id. 
		photo = nil,
		sex = nil,
		-- user status
		userstatus = nil,
		age = nil,
		signature = nil,
		city = nil,
		nation = nil,
		-- array of friends's userid
		friends = nil,
	}
	-- child nodes: none
});

-- friends user ids
mcml["pe:friends"] = mcml.new("baseNode", {
	name = "pe:friends", 
	attr = {
		-- [string] List of user ids. This is a comma-separated list of user ids.
		uids = nil,
	}
	-- child nodes: none
});

-- application profile box: including both 3d and 2d integration points. 
mcml["pe:app"] = mcml.new("baseNode", {
	name = "pe:app", 
	attr = {
		-- required: application key
		app_key = nil,
		-- the application with a higher version must be installed on the local computer in order to render this application box. 
		-- if this is nil, the application can be rendered even the application is not installed on the local computer. 
		-- it is the app developers' responsibility to ensure that it uses no app specific resources for rendering, when version is nil,
		version = nil, -- "1.0"
	}
	-- child nodes: pe:world, pe:treeview, pe:profile-action, any
});

-- a user name in 2d. Renders the name of the user specified, optionally linked to his or her profile. 
-- You can use this tag for both the subject and the object of a sentence describing an action.
mcml["pe:name"] = mcml.new("baseNode", {
	name = "pe:name", 
	attr = {
		-- required: The ID of the user or Page whose name you want to show. You can also use "loggedinuser" or "profileowner". 
		uid = nil,
		-- following are all optional: 
		-- bool  Show only the user's first name. (default value is false)  
		firstnameonly = false, 
		-- bool:  Link to the user's profile. (default value is true)  
		linked = true,
		-- bool  Use "you" if uid matches the logged in user. (default value is true)  
		useyou = true,
	}
	-- child nodes: none
});

-- Renders a link on the user's profile under their photo (such as "View More photos of.."). 
mcml["pe:profile-action"] = mcml.new("baseNode", {
	name = "pe:profile-action", 
	attr = {
		-- If not nil, it is the URL to which the user is taken after clicking. 
		-- otherwise, the attr of the profile action is passed to the application's do quick action handler.  
		url = nil,
		-- anything that is passed to the application's do quick action handler.  
	}
	-- child nodes: text
});

-- contents in this box are rendered in profile page. 
mcml["pe:profile-box"] = mcml.new("baseNode", {
	name = "pe:profile-box", 
	attr = {
	}
	-- child nodes: any
});

-- clicks to go to the home page of an application
mcml["pe:app-home-button"] = mcml.new("baseNode", {
	name = "pe:app-home-button", 
	attr = {
		app_key = nil,
	}
	-- child nodes: none
});

--------------------------------------
-- map tags
--------------------------------------
mcml["pe:map"] = mcml.new("baseNode",{
	name = "pe:map",
	attr = {
		x = 0.5,
		y = 0.5,
		mode = nil,
		canmove = false,
		zoom = 0,
	}
});


mcml["pe:minimap"] = mcml.new("baseNode",{
	name = "pe:minimap",
	attr = {
	}
});
		

-- map mark on the 3d map layer. 
mcml["pe:map-mark"] = mcml.new("baseNode", {
	name = "pe:map-mark", 
	attr = {
		-- user id
		markid = nil,
	}
	-- child nodes: none
});

-- map mark on the 2d map layer. 
mcml["pe:map-mark2d"] = mcml.new("baseNode", {
	name = "pe:map-mark2d", 
	attr = {
		-- following is the same as Map/SideBar/Map2DMarkInfo.lua
		markID = nil,
		markType = 0,
		-- int, mark model or icon type: see MarkButton.button_style
		markStyle = 1,
		-- text style: see MarkButton.text_style
			bShowText = true,
			textColor = "0 0 0",
			textScale = 1,
			textRot = 0,
		markTitle = "未命名",
		markDesc = "",
		startTime = "",
		endTime = "",
		x = 0,
		y = 0,
		cityName = "",
		rank = 0,
		logo = "",
		signature = "",
		desc = "",
		ageGroup = 0,
		URL = "",
		isApproved = false,
		version = "",
		ownerUserID = "",
		clickCnt = 0,
		worldid = -1,
		allowEdit = false,
		z = 0,
	}
	-- child nodes: none
});

-- a map tile (land) owned by a user
mcml["pe:map-tile"] = mcml.new("baseNode", {
	name = "pe:map-tile", 
	attr = {
		-- tile id
		tileid = nil,
	}
	-- child nodes: none
});

--------------------------------------
-- Sanitization Tags: some content like flash files are sanitized. 
-- Any unknown tags are also not rendered. Please refer to mcml doc for which one is not supported or sanitized. 
--------------------------------------

--------------------------------------
-- Design tags: Design tags help define the look of a page. 
-- While mcml allows developers to render their pages using some standard HTML and CSS, 
-- we offer some custom design tags to utilize special NPL ide controls that help them blend their application into the style of the host app.
--------------------------------------

-- a group of standard tab pages. Must contain at least one pe:tab-item. 
mcml["pe:tabs"] = mcml.new("baseNode", {
	name = "pe:tabs", 
	-- child nodes: pe:tab-item
});

mcml["pe:tab-item"] = mcml.new("baseNode", {
	name = "pe:tab-item", 
	attr = {
		-- Specifies the text to display on the tab
		text = nil,
		-- optional:  [bool]  Indicates whether this tab item has the selected state. (default value is nil)  
		selected  = nil,
	}
	-- child nodes: any
});

-- content inside this node is suggested to be rendered in a treeview control. 
mcml["pe:treeview"] = mcml.new("baseNode", {
	name = "pe:treeview", 
	attr = {
		-- following are the same as ide/treeview
		-- normal window size
		alignment = "_lt",
		left = 0,
		top = 0,
		width = 300,
		height = 300, 
		-- appearance
		-- the background of container
		background = "Texture/3DMapSystem/common/ThemeLightBlue/container_bg.png: 4 4 4 4", 
		-- automatically display vertical scroll bar when content is large
		AutoVerticalScrollBar = true,
		-- offset ScrollBar postion in horizontal
		VerticalScrollBarOffsetX = 0,
		-- Vertical ScrollBar Width
		VerticalScrollBarWidth = 15,
		-- how many pixels to scroll each time
		VerticalScrollBarStep = 3,
		-- how many pixels to scroll when user hit the empty space of the scroll bar. this is usually same as DefaultNodeHeight
		VerticalScrollBarPageSize = 25,
		-- The root tree node. containing all tree node data
		RootNode = nil, 
		-- Default height of Tree Node
		DefaultNodeHeight = 25,
		-- default icon size
		DefaultIconSize = 16,
		-- whether to show icon on the left of each line. 
		ShowIcon = true,
		-- default indentation
		DefaultIndentation = 5,
	}
	-- child nodes: pe:treenode or any (if child node is not pe:treenode, it is always rendered inside an anonymous treenode using the default height)
});

-- content inside this node is suggested to be rendered as a treenode in treeview control. 
-- it may contain other pe:treenode as child or anything else. 
mcml["pe:treenode"] = mcml.new("baseNode", {
	name = "pe:treenode", 
	attr = {
		-- optional: Specifies the text to display on the tree Node
		text = nil,
		-- optional: treenode name
		name = nil,
		-- optional:  icon path. 
		icon  = nil,
		-- optional:  node height. if 0, this node is not rendered, but child nodes are rendered.
		height  = nil,
		-- optional:  indentation in pixel relative to the parent treeview control. if nil, the default is used. 
		indent = nil,
		-- optional:expanded
		expanded = true,
		-- optional:  bool : whether node is invisible. 
		invisible = nil,
	}
	-- child nodes: "pe:treenode", any
});

-- a image control. 
mcml["pe:image"] = mcml.new("baseNode", {
	name = "pe:image", 
	attr = {
		alignment = "_lt",
		left = 0,
		top = 0,
		width = 300,
		height = 300, 
	}
	-- child nodes: none
});

-- an interactive flash control.
mcml["pe:flash"] = mcml.new("baseNode", {
	name = "pe:flash", 
	attr = {
		-- TODO: see ide/flashplayer
	}
	-- child nodes: none
});

--------------------------------------
-- component tags:
-- In addition to design tags, mcml features some tags that provide richer features of the site. Component tags create widget-like components 
-- that allow for user interaction with an application on paraworld. Often these tags provide full ready made items that can be placed into the application. 
-- e.g. pe:roomhost displays a room control that allow users create and join each other's 3d world related to a given app_key. 
-- e.g. pe:comments renders a control that allows visitors to post comments to the dicussion board of an app. 
-- e.g. pe:market renders a control that allows visitors to buy and sell items via an app. 
--------------------------------------
mcml["pe:roomhost"] = mcml.new("baseNode", {
	name = "pe:roomhost", 
	attr = {
		-- optional:if nil, it will search for its parent until a pe:app node is found and use its app_key.
		app_key = nil,
		-- optional:  
		height = nil,
		width = nil,
		-- normal window size
		alignment = "_lt",
		left = 0,
		top = 0,
		-- use max width
		width = nil,
		height = 300, 
	}
	-- child nodes: none
});
mcml["pe:market"] = mcml.new("baseNode", {
	name = "pe:market", 
	attr = {
		-- optional:if nil, it will search for its parent until a pe:app node is found and use its app_key.
		app_key = nil,
		-- optional:  
		height = nil,
		width = nil,
		-- normal window size
		alignment = "_lt",
		left = 0,
		top = 0,
		-- use max width
		width = nil,
		height = 300, 
	}
	-- child nodes: none
});
mcml["pe:comments"] = mcml.new("baseNode", {
	name = "pe:comments", 
	attr = {
		-- optional:if nil, it will search for its parent until a pe:app node is found and use its app_key.
		app_key = nil,
		-- normal window size
		alignment = "_lt",
		left = 0,
		top = 0,
		-- use max width
		width = nil,
		height = 300, 
	}
	-- child nodes: none
});
mcml["pe:dialog"] = mcml.new("baseNode", {
	name = "pe:dialog", 
	attr = {
		--  string of title text or nil. 
		title = nil,
		-- position and size of the client area of the dialog. if x,y is nil, it is displayed at the center of the screen. 
		x = nil,
		y = nil,
		width = 300,
		height = 200, 
		-- int: type of _guihelper.MessageBoxButtons: OKCancel = 3,YesNo = 5, YesNoCancel = 6,
		buttons = nil,
		-- function (dialogResult) end or the function name string. 
		onclick = nil,
	}
	-- child nodes: none
});

------------------
-- editor display component tags
------------------
-- Creates a form with two columns, just like the form on the edit-profile page. The children of pe:editor specify the 
-- rows of the form. For example, an pe:editor-text child adds a row with a text field in the right column. 
-- The label attribute of the pe:editor-* child specifies what text appears in the left column of that row. 
mcml["pe:editor"] = mcml.new("baseNode", {
	name = "pe:editor", 
	attr = {
		-- required:   string: if it begins with http, it is the URL to which the form's data is posted.
		-- otherwise, it is forwarded to the doaction handler of its container app. 
		action = nil,
		-- int:  The width of the first column of the form/table, in pixels. (default value is 75). Note: This value cannot be 0 as it is ignored; use 1 instead.  
		labelwidth = 75,
		-- normal window size
		alignment = "_lt",
		left = 0,
		top = 0,
		-- The width of the form/table, in pixels. (profile default value is 425) 
		width = nil,
		height = nil, 
	}
	-- child nodes: pe:editor-buttonset, pe:editor-button, pe:editor-text, editor-divider, 
	-- pe:treenode(allows you to put any content into an pe:editor block), 
});

-- A container for one or more fb:editor-button tags, which are rendered next to each other with some space between each button. 
mcml["pe:editor-buttonset"] = mcml.new("baseNode", {
	name = "pe:editor-buttonset", 
	-- child nodes: pe:editor-button
});

-- Renders a button of type submit inside an fb:editor tag. 
-- This tag can be a child of an fb:editor-buttonset container to render multiple buttons next to each other. 
mcml["pe:editor-button"] = mcml.new("baseNode", {
	name = "pe:editor-button", 
	attr = {
		-- required:  string  The text label for the button.  
		text = nil,
		-- optional: string  The variable name that is sent in the POST request when the form is submitted.  
		name = "unamed_button",
		-- @param onclick: the onclick script name or an URL to receive result using HTTP post. 
		--  if it is a script name, the script will be called with onclick(btnName, values, bindingContext), 
		--	where btnName is name of button that is clicked and values is nil or a table collecting all name value pairs. 
		onclick = nil,
	}
	-- child nodes: none
});

-- an input edit box. it can be multiline
mcml["pe:editor-text"] = mcml.new("baseNode", {
	name = "pe:editor-text", 
	attr = {
		-- optional string  The label to display on the left side of the text box.  
		label = nil,
		-- The default text that populates the edit box. 
		text = nil,
		-- optional: string  The variable name that is sent in the POST request when the form is submitted.  
		name = "unamed_editbox",
		-- int  The maximum length of the input allowed in the edit box. 
		maxlength = 255,
		-- int  The height of the text area in number of lines of text. Default is 1 for single lined edit box. 
		rows = 1,
	}
	-- child nodes: none
});

-- Allows you to put any content into an pe:editor block, as long as it is valid mcml.
mcml["pe:editor-custom"] = mcml.new("baseNode", {
	name = "pe:editor-custom", 
	attr = {
		-- optional string  The label to display on the left side of the text box.  
		label = nil,
		-- the height of this custom node. 
		height = 26,
	}
	-- child nodes: any
});
-- Renders a horizontal line separator in the column containing the form elements.
mcml["pe:editor-divider"] = mcml.new("baseNode", {
	name = "pe:editor-divider", 
	-- child nodes: none
});

--------------------------------------
-- HTML tags: 
--------------------------------------
-- selection box: either list box or combo box (drop down list box)
mcml["select"] = mcml.new("baseNode", {
	name = "select", 
	attr = {
		-- if 1 it is combo box, if greater than 1, it is a listbox. 
		size = 1,
	}
	-- child nodes: <option>line_text</option>
});

--------------------------------------
-- control tags: 
-- The most useful of these are the visible-to-XXX tags, such as fb:visible-to-owner.
--------------------------------------
-- Displays content inside only if the viewer of the profile matches the profile owner. 
-- Note: Do not use this tag to display private or sensitive information. Content inside this tag is rendered to all users' browsers, including those who are not the profile owner. For those who are not the owner, the content is shown as white space on the page but it is still visible by viewing the page source. 
mcml["pe:visible-to-owner"] = mcml.new("baseNode", {
	name = "pe:visible-to-owner", 
	-- child nodes: any
});

--------------------------------------
-- worlds tags: 
--------------------------------------
-- a user created virtual world 
mcml["pe:world"] = mcml.new("baseNode", {
	name = "pe:worldip", 
	attr = {
		-- the unique world id
		worldid = nil,
	}
	-- child nodes: none
});

-- world integration point: the parent node for all 3D world objects in the in-game world integration point. 
mcml["pe:worldip"] = mcml.new("baseNode", {
	name = "pe:worldip", 
	attr = {
		-- optional:if nil, it will search for its parent until a pe:app node is found and use its app_key.
		app_key = nil,
		-- icon to be shown on the mini-map. if nil, the app's icon is used. 
		icon = nil,
		-- tooltip text to be displayed on the mini-map.
		text = nil,
	}
	-- child nodes: "pe:model", "pe:avatar"
});

-- a 3D model or character specified using relative positioning in pe:world integration point. 
mcml["pe:model"] = mcml.new("baseNode", {
	name = "pe:model", 
	attr = {
		-- following has the same definition as the obj_params table in ide/object_editor
		name,
		AssetFile, -- primary asset file: either string or para asset object.
		x,
		y,
		z,
		IsCharacter, -- can be nil
		scaling,	-- can be nil
		rotation,   -- can be nil or {x=0,y=0,z=0,w=1} which is rotational quaternion.
		facing,  -- can be nil
		IsGlobal,	-- can be nil
		ViewBox, -- can be nil
		Density,	-- can be nil
		PhysicsRadius, -- can be nil
		
		IsPersistent, -- can be nil
		ReplaceableTextures, -- = {[1] = "filepath"}, -- can be nil
		SkinIndex,  -- can be nil
		localMatrix, -- can be nil
		EnablePhysics, -- can be nil, whether physics is enabled for the mesh
		
		-- TODO: Customizable character properties here?
		-- TODO: dynamic properties?
	}
	-- child nodes: none
});

-- a 3D character avatar of a given user. One only needs to specify userid to render it properly
mcml["pe:avatar"] = mcml.new("baseNode", {
	name = "pe:avatar", 
	
	attr = {
		-- the user ID whose avatar this belongs. all following attributes can be nil. 
		-- If following attributes are provided, they will override default avatar settings of the given userid
		userid = nil,
		
		-- following has the same definition as the obj_params table in ide/object_editor
		name,
		AssetFile, -- primary asset file: either string or para asset object.
		x,
		y,
		z,
		IsCharacter, -- can be nil
		scaling,	-- can be nil
		rotation,   -- can be nil or {x=0,y=0,z=0,w=1} which is rotational quaternion.
		facing,  -- can be nil
		IsGlobal,	-- can be nil
		ViewBox, -- can be nil
		Density,	-- can be nil
		PhysicsRadius, -- can be nil
		
		IsPersistent, -- can be nil
		ReplaceableTextures, -- = {[1] = "filepath"}, -- can be nil
		SkinIndex,  -- can be nil
		localMatrix, -- can be nil
		EnablePhysics, -- can be nil, whether physics is enabled for the mesh
		-- TODO: Customizable character properties here?
		-- TODO: dynamic properties?
	}
	-- child nodes: none
});


--[[
Title: an interactive NPL control initialized from a MCML file
Author(s): LiXizhi
Date: 2008/3/20
Desc: In many cases, we want to build interactive control from a static or asynchronous MCML file. 
The MCML file contains the layout and default databinding for all UI elements. 
However, to make those UI element interactive, we need to associate NPL code with that MCML file. 
The PageCtrl automates the above design pattern, by creating an NPL control from an MCML file. 
One can implement predefined or MCML page defined event handlers in it. 
One can also easily nagivate and access UI and databinding controls defined in the MCML file. 
It is a Code-Behind Page pattern to seperate UI with logics. And the UI may be asynchronously loaded such as an URL. 

_Note_: it will only search and render the first occurance of pe:mcml node in the url
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/PageCtrl.lua");
MyApp.MyPage = Map3DSystem.mcml.PageCtrl:new({url="script/kids/3DMapSystemApp/mcml/test/MyPageControl_UI.html"});
-- on load
function MyApp.MyPage:OnLoad()
	-- anything here
end
-- One can also override the default refresh method to implement owner draw. 
function MyApp.MyPage:OnRefresh(_parent)
	Map3DSystem.mcml.PageCtrl.Refresh(self, _parent);
end

-- one can create a UI instance like this. 
MyApp.MyPage:Create("instanceName", _parent, "_fi", 0, 0, 0, 0)

-- call Goto to change url after or before Create is called. 
MyApp.MyPage:Goto(url, cache_policy, bRefresh)

-- jquery-like syntax (some syntactic sugar)
Page("div#my_name"):hide();
Page("a#my_name.my_class"):show();
Page("#my_name"):print();
log(Page(".my_class"):text().." is the last node's inner text\n");
-------------------------------------------------------
]]
NPL.load("(gl)script/kids/3DMapSystemApp/mcml/mcml.lua");
NPL.load("(gl)script/kids/3DMapSystemApp/API/webservice_constants.lua");
NPL.load("(gl)script/ide/System/localserver/factory.lua");
NPL.load("(gl)script/ide/System/localserver/UrlHelper.lua");
NPL.load("(gl)script/ide/XPath.lua");
NPL.load("(gl)script/ide/System/Windows/mcml/Style.lua");
local Style = commonlib.gettable("System.Windows.mcml.Style");
			
local pe_script = commonlib.gettable("Map3DSystem.mcml_controls.pe_script");

-- a browser window instance.
local PageCtrl = {
	name = nil,
	-- nil means not started downloading. 1 means ready. 0 means downloading. 2 means not able to download page.  3 means <pe:mcml> node not found in page body. 
	status = nil,
	-- the status string message
	status_line = nil,
	-- the <pe:mcml> node
	mcmlNode = nil,
	-- a function to be called when a new page is downloaded. 
	OnPageDownloaded = nil,
	-- default policy if no one is specified. 
	cache_policy = System.localserver.CachePolicy:new("access plus 1 hour"),
	-- default refresh page delay time in seconds. More information, please see Refresh() method. 
	DefaultRefreshDelayTime = 1,
	-- default page redirect delay time in seconds. More information, please see Redirect() method. 
	DefaultRedirectDelayTime = 1,
	-- time remaining till next refresh page update. More information, please see Refresh() method. 
	RefreshCountDown = nil,
	-- the init url, if this is not provided at first, one needs to call Init(url) before calling Create()
	url = nil,
	-- we will keep all opened url in a stack, so that we can move back or forward. This is just a simple table array for all opened urls. 
	opened_urls = nil,
	-- if nil it means the last one in opened_urls, otherwise, the index of the current url in opened_urls 
	opened_url_index = nil,
	-- mcml page to be displayed when an error occurs.
	errorpage = nil,
	-- in case this page is inside an iframe, the parentpage contains the page control that created the iframe. use GetParentPage() function to get it. 
	parentpage = nil,
	-- the window object containing the page control. CloseWindow() function will close this window object. 
	window = nil,
	-- this is a user-defined call back function (bDestroy) end. it is called whenever the page is closed by its container window. Please note, if the page is not inside a MCMLBrowserWnd() this function may not be called. 
	OnClose = nil,
	-- whether the page will paint on to its own render target. 
	SelfPaint = nil,
}
Map3DSystem.mcml.PageCtrl = PageCtrl;

-- make jquery-like invoke
PageCtrl.__call = function(self, ...)
	return self:jquery(...)
end
PageCtrl.__index = PageCtrl;

-- constructor
function PageCtrl:new(o)
	o = o or {}   -- create object if user does not provide one
	setmetatable(o, self);
	-- this will prevent recursive calls to self:Refresh(), which makes self:Refresh(0) pretty safe. 
	self.refresh_depth = 0;
	return o
end

-- Init control with a MCML treenode or page url. If a local version is found, it will be used regardless of whether it is expired or not. 
-- It does not create UI until PageCtrl:Create() is called. 
-- _NOTE_: Calling this function with different urls after PageCtrl:Create() will refresh the UI by latest url.
--@param url: the url of the MCML page. It must contain one <pe:mcml> node. Page should be UTF-8 encoded. It will automatically replace %params% in url if any
-- if url is nil, content will be cleared. if it is a table, it will be the mcmlNode to open. 
--@param cache_policy: cache policy object. if nil, default is used. 
--@param bRefresh: whether to refresh if url is already loaded before. 
function PageCtrl:Init(url, cache_policy, bRefresh)
	if(url == nil or url=="") then
		-- clear all 
		self.status = nil;
		self.mcmlNode = nil;
		self.style = nil;
		self:OnRefresh();
		return
	elseif(type(url) == "table" and table.getn(url)>0) then
		-- url is actually mcmlNode
		self.url="";
		PageCtrl.OnPageDownloaded_CallBack(url, nil, self)
		return
	end
	if(paraworld and paraworld.TranslateURL) then
		url = paraworld.TranslateURL(url);
	end
	self.url = url;
	-- downloading
	self.status = 0; 
	
	if(string.find(url, "^http://")) then
		self.status_line = "正在刷新页面请等待......";
		self:OnRefresh();
		-- for remote url, use the local server to retrieve the data
		local ls = System.localserver.CreateStore(nil, 2);
		if(ls)then
			ls:CallXML(cache_policy or self.cache_policy, url, PageCtrl.OnPageDownloaded_CallBack, self)
		end
	else
		-- for local file, open it directly
		-- remove requery string when parsing file. 
		local filename = string.gsub(url, "%?.*$", "")
		
		local xmlRoot = ParaXML.LuaXML_ParseFile(filename);
		if(type(xmlRoot)=="table" and table.getn(xmlRoot)>0) then
			PageCtrl.OnPageDownloaded_CallBack(xmlRoot, nil, self)
		else
			self.status_line = "无法打开页面......";
			self:OnRefresh();
			log("warning: unable to open local page "..url.."\n")
		end
	end	
end

-- go to a given url or move backward or forward. This function can NOT be called in embedded page code. In page script, use Redirect() instead. 
--@param url: it can be the url or string "backward", "forward". If it is url path, its page must contain one <pe:mcml> node. Page should be UTF-8 encoded. It will automatically replace %params% in url if any
-- if url is nil, content will be cleared. if it is a table, it will be the mcmlNode to open. 
--@param cache_policy: cache policy object. if nil, default is used. 
--@param bRefresh: whether to refresh if url is already loaded before. 
--@return true if it is processing to the next stage. 
function PageCtrl:Goto(url, cache_policy, bRefresh)
	if(url == "refresh") then
		url = self.url;
	end
	if(self.opened_urls and type(url) == "string") then
		if(url == "backward") then
			-- first search any inner iframe's pagectrl
			local InnerPageCtrl;
			if(self.mcmlNode) then
				local iframeNodes = self.mcmlNode:GetAllChildWithName("iframe");
				if(iframeNodes) then
					local index, framenode;
					for index, framenode in ipairs(iframeNodes) do
						if(framenode.pageCtrl) then
							local tabNode = framenode:GetParent("pe:tab-item");
							if(tabNode) then
								if(tabNode:GetBool("selected"))then
									InnerPageCtrl = framenode.pageCtrl
									break;
								end
							else
								InnerPageCtrl = framenode.pageCtrl
								break;
							end
						end
					end
				end
			end
			if(InnerPageCtrl) then
				if(InnerPageCtrl:Goto(url, cache_policy, bRefresh)) then
					return true;
				end
			end
			self.opened_url_index = self.opened_url_index or #self.opened_urls
			url = self.opened_urls[self.opened_url_index-1];
			if(not url) then return end
			self.opened_url_index = self.opened_url_index-1;
		elseif(url == "forward") then
			self.opened_url_index = self.opened_url_index or #self.opened_urls
			url = self.opened_urls[self.opened_url_index+1];
			if(not url) then return end
			self.opened_url_index = self.opened_url_index+1;
		end
	else
		if(url == "backward" or url == "forward") then
			return 
		end
	end
	self:Init(url, cache_policy, bRefresh)
	return true;
end

-- rebuild the page. this is slow. It will delete and reparse the entire html text. 
-- any local or global paramters defined in in-page code block will not survive during rebuild. 
-- Use self:Refresh() which is fast and all local and global paramters will survive during refresh. 
--	this will allow you programatically alter the content of the page.  
-- all paramter can be nil. 
-- @param url: if nil it is the current url. 
function PageCtrl:Rebuild(url, cache_policy, bRefresh)
	self:Goto(url or "refresh", cache_policy, bRefresh);
end

-- create (instance) the page UI. It will create UI immediately after the page is downloaded. If page is local, it immediately load.
-- @param name: name of the control. it should be globally unique if page is asynchronous. and it can be anything, if page is local. 
function PageCtrl:Create(name, _parent, alignment, left, top, width, height, bForceDisabled)
	-- in case page is asynchronous, we will need to find the control by name after page is downloaded. so name must be globally unique if page is remote. 
	self.name = name
	-- add the page control to common ctrl pool, so that we can retrieve it from mcml.baseNode:GetControl() method. 
	CommonCtrl.AddControl(name, self);
	
	local _this;
	if(_parent) then
		_this = _parent:GetChild(name);
	end	
	if(_parent==nil or not _this:IsValid()) then 
		-- create the control and wait for page download to fill its inner context. 
		_this = ParaUI.CreateUIObject("container",name,alignment,left,top,width,height);
		_this.background="";
		if(self.click_through) then
			_this:GetAttributeObject():SetField("ClickThrough", self.click_through);
		end

		if(bForceDisabled == true) then
			-- NOTE: as used in script\apps\Aries\NPCs\Doctor\30085_RainbowFlowerGame.lua
			_this.enabled = false;
		end
		if(_parent == nil) then
			_this:AttachToRoot();
		else
			_parent:AddChild(_this);
		end
	end
	_parent = _this;
	
	self.IsCreated = false;
	if(self.status == nil and self.url) then	
		-- not downloaded before, we will start downloading. 
		self:Init(self.url)
	end
	self.IsCreated = true;
		
	if(self.status == 1) then
		-- if finished downloading, we will refresh
		self:OnRefresh(_parent)
	end
	return _parent;
end

-- close and destory all UI objects created by this page. 
-- only call this function if self.name is a global name. 
function PageCtrl:Close()
	if(self.name) then
		ParaUI.Destroy(self.name)
	end
end

-- in case this page is inside an iframe, the parentpage contains the page control that created the iframe.
function PageCtrl:GetParentPage()
	return self.parentpage
end

-- Get the top most root page
function PageCtrl:GetRootPage()
	if(self.parentpage) then
		return self.parentpage:GetRootPage();
	else
		return self;
	end
end

-- get the parent window containing this page. 
function PageCtrl:GetWindow()
	if(self.window) then
		return self.window;
	else
		if(self:GetParentPage()) then
			return self:GetParentPage():GetWindow();
		end
	end
end

-- a safe method to decide if the page is visible or not. 
-- @return true if page is visible. 
function PageCtrl:IsVisible()
	if(self.parent_id and ParaUI.GetUIObject(self.parent_id):GetField("VisibleRecursive", false)) then
		return true;
	end
end

-- get the parent ui object
function PageCtrl:GetParentUIObject()
	if(self.parent_id) then
		return ParaUI.GetUIObject(self.parent_id);
	end
end

-- close the containing window
-- @param bDestroy: if true, it will destroy the window, otherwise it will just hide it.
function PageCtrl:CloseWindow(bDestroy)
	local wnd = self:GetWindow();
	if(wnd) then
		wnd:SendMessage(nil,{type=CommonCtrl.os.MSGTYPE.WM_CLOSE, bDestroy=bDestroy});
	end
end

-- set the text and/or icon of the page's container window
function PageCtrl:SetWindowText(text,icon)
	local wnd = self:GetWindow();
	if(wnd) then
		wnd:SetWindowText(text,icon);
	end
end

-------------------------------------
-- overridable functions
-------------------------------------

-- this function is overridable. it is called before page UI is about to be created. 
-- You cannot use view-state information within this event; it is not populated yet. 
-- @param self.mcmlNode: the root pe:mcml node, one can modify it here before the UI is created, such as filling in default data. 
function PageCtrl:OnLoad()
end

-- this function is overridable. it is called after page UI is created. 
-- One can perform any processing steps that are set to occur on each page request. You can access view state information. You can also access controls within the page's control hierarchy.
-- In other words, one can have direct access to UI object created in the page control. Note that some UI are lazy created 
-- such as treeview item and tab view items. They may not be available here yet. 
function PageCtrl:OnCreate()
end

-- forcing a repaint in the next frame. this function does nothing if SelfPaint is false.
function PageCtrl:InvalidateRect()
	if(self.SelfPaint) then
		local parent = self:GetParentUIObject()
		if(parent) then
			parent:InvalidateRect();
		end
	end
end

-- refresh the page UI. It will remove all previous UI and rebuild (render) from current MCML page data. 
-- it will call the OnLoad method. 
-- _Note_ One can override this method to owner draw this control. 
-- @param _parent: if nil, it will get using the self.name. 
-- @return: the parent container of page ctrl is returned. 
function PageCtrl:OnRefresh(_parent)
	self.RefreshCountDown = nil;
	if(not self.IsCreated) then
		return 
	end
	if(_parent == nil and self.name) then
		_parent = ParaUI.GetUIObject(self.name)
	end
	if(_parent == nil or not _parent:IsValid())	then
		return 
	end
	
	if(self.refresh_depth > 0) then
		-- if we are refreshing a page within a page, we will automatically delay it. 
		LOG.std("", "warning", "mcml", "recursive page refresh is detected for page %s. Please use page:Refresh() instead of Refresh(0).", tostring(self.url));
		-- self:Refresh(0.01);
		return;
	end
	self.refresh_depth = self.refresh_depth + 1;

	-- render control. 
	_parent:RemoveAll();
	self.parent_id = _parent.id;
	
	if(self.status== 1 and self.mcmlNode) then
		if(self.SelfPaint) then
			_parent:SetField("SelfPaint", true);
		end

		-- call OnLoad
		if(self.OnLoad) then
			self:OnLoad();
		end
		
		-- create the mcml UI controls. 
		local _,_, width, height = _parent:GetAbsPosition();
		-- secretely inject the "request_url" in it, so that we can make href using relative to site or url path. 
		self.mcmlNode:SetAttribute("request_url", self.url);
		-- secretely put this page control object into page_ctrl field, so that we can refresh this page with a different url, such as in pe_a or form submit button.
		self.mcmlNode:SetAttribute("page_ctrl", self);
		local parentLayout = Map3DSystem.mcml_controls.layout:new();
		parentLayout:reset(0, 0, width, height);
		Map3DSystem.mcml_controls.create(self.name, self.mcmlNode, nil, _parent, 0, 0, width, height, nil, parentLayout)
		self.used_width, self.used_height = parentLayout:GetUsedSize();
		-- call OnCreate
		if(self.OnCreate) then
			self:OnCreate();
		end
		
		-- add url
		self:AddOpenedUrl();
	else
		-- TODO: display an animated background in _parent for other self.status values, such as downloading or error. 
		-- TODO: we can also display a user defined self.errorpage page. 
		-- log("warning:"..tostring(self.status_line).."\n")
	end	
	self.refresh_depth = self.refresh_depth - 1;
end

-- get the used size of the page. This is called to obtain the actual size used to render the mcml page. 
function PageCtrl:GetUsedSize()
	return self.used_width, self.used_height;
end

-- add current opened url to the opened urls stack so that we can move forward or backward. 
-- if the last url is the same as current, url will not be added. 
-- @param url; nil or url string to add. if nil, self.url is used. 
function PageCtrl:AddOpenedUrl(url)
	url = url or self.url;
	self.opened_urls = self.opened_urls or {};
	self.opened_url_index = self.opened_url_index or #self.opened_urls;
	if(self.opened_urls[self.opened_url_index] ~= url) then
		self.opened_url_index = self.opened_url_index + 1;
		self.opened_urls[self.opened_url_index] = url;
	end
end

--------------------------------------
-- public method: for accessing mcml node, UI, and databinding objects in the page. 
--------------------------------------

-- refresh the entire page after DelayTime seconds. Please note that during the delay time period, 
-- if there is another call to this function with a longer delay time, the actual refresh page activation will be further delayed
-- Note: This function is usually used with a design pattern when the MCML page contains asynchronous content such as pe:name, etc. 
-- whenever an asychronous tag is created, it will first check if data for display is available at that moment. if yes, it will 
-- just display it as static content; if not, it will retrieve the data with a callback function. In the callback function, 
-- it calls this Refresh method of the associated page with a delay time. Hence, when the last delay time is reached, the page is rebuilt 
-- and the dynamic content will be accessible by then. 
-- @param DelayTime: if nil, it will default to self.DefaultRefreshDelayTime (usually 1.5 second). 
-- tip: If one set this to a negative value, it may causes an immediate page refresh. 
function PageCtrl:Refresh(DelayTime)
	CommonCtrl.AddControl(self.name, self);
	DelayTime = DelayTime or self.DefaultRefreshDelayTime;
	self.RefreshCountDown = (self.RefreshCountDown or 0);
	if(self.RefreshCountDown < DelayTime) then
		self.RefreshCountDown = DelayTime;
	end
	if(self.RefreshCountDown<=0) then
		self:OnRefresh();
	else
		local _parent = ParaUI.GetUIObject(self.name);
		if(_parent:IsValid())then
			_parent.onframemove = string.format(";Map3DSystem.mcml.PageCtrl.OnFrameMove_(%q)", self.name);
		end
	end
end

-- private method
function PageCtrl.OnFrameMove_(pageName)
	local self = CommonCtrl.GetControl(pageName);
	local _parent = ParaUI.GetUIObject(self.name);
	if(_parent:IsValid())then
		-- in case there is page error in previous page load, this will recover the refresh depth. 
		self.refresh_depth = 0; 
		if(self.RefreshCountDown) then
			self.RefreshCountDown = self.RefreshCountDown-deltatime;
			if(self.RefreshCountDown<=0) then
				self.RefreshCountDown = nil;
				self:OnRefresh();
			end
		end	
		if(self.RedirectCountDown) then
			self.RedirectCountDown = self.RedirectCountDown-deltatime;
			if(self.RedirectCountDown<=0) then
				self.RedirectCountDown = nil;
				if(self.redirectParams) then
					self:Goto(self.redirectParams.url, self.redirectParams.cache_policy, self.redirectParams.bRefresh);
					self.redirectParams = nil;
				end
			end
		end

		if (self.RefreshCountDown==nil and self.RedirectCountDown==nil) then
			_parent.onframemove = "";
		end
	end	
end

-- Same as Goto(), except that it contains a delay time. this function is safe to be called via embedded page code. 
-- it will redirect page in DelayTime second
-- @param url: relative or absolute url, like you did in a src tag 
-- if url is nil, content will be cleared. if it is a table, it will be the mcmlNode to open. 
-- @param cache_policy: cache policy object. if nil, default is used. 
-- @param bRefresh: whether to refresh if url is already loaded before. 
-- @param DelayTime: if nil, it will default to self.DefaultRedirectDelayTime(usually 1 second). we do not allow immediate redirection, even delayTime is 0
function PageCtrl:Redirect(url, cache_policy, bRefresh, DelayTime)
	if(self.mcmlNode) then
		url = self.mcmlNode:GetAbsoluteURL(url);
	end
	
	self.RedirectCountDown = DelayTime or self.DefaultRedirectDelayTime;
	-- we do not allow immediate redirection, even delayTime is 0
	self.redirectParams = {url=url, cache_policy=cache_policy, bRefresh=bRefresh};
	local _parent = ParaUI.GetUIObject(self.name);
	if(_parent:IsValid())then
		_parent.onframemove = string.format(";Map3DSystem.mcml.PageCtrl.OnFrameMove_(%q)", self.name);
	end
end
	
-- get the url request of the mcml node if any. It will search for "request_url" attribtue field in the ancestor of this node. 
-- PageCtrl and BrowserWnd will automatically insert "request_url" attribtue field to the root MCML node before instantiate them. 
-- @return: nil or the request_url is returned. we can extract requery string parameters using regular expressions or using GetRequestParam
function PageCtrl:GetRequestURL()
	return self.mcmlNode:GetAttribute("request_url");
end

-- if you want to modify request_url and then refresh the page. call this function. 
function PageCtrl:SetURL(url)
	self.url = url;
	if(self.mcmlNode) then
		self.mcmlNode:SetAttribute("request_url", url)
	end
end


-- get request url parameter by its name. for example if page url is "www.paraengine.com/user?id=10&time=20", then GetRequestParam("id") will be 10.
-- @param paramName: if nil, it will return a table containing all name,value pairs. 
-- @return: nil or string value or a table.
function PageCtrl:GetRequestParam(paramName)
	local request_url = self:GetRequestURL();
	local params = self.mcmlNode:GetAttribute("request_params");
	if(not params or params.url__ ~= request_url) then
		params = System.localserver.UrlHelper.url_getparams_table(request_url) or {};
		params.url__ = request_url;
		self.mcmlNode:SetAttribute("request_params", params);
	end
	if(params) then
		if(paramName) then
			return params[paramName];
		else
			return params;
		end
	end
end

-- Binds current data source to the all page controls
function PageCtrl:DataBind()
end

-- Gets the first data item by its name in the data-binding context of this page. 
function PageCtrl:GetDataItem(name)
end

-- Sets the focus to the control with the specified name.
-- @param name: The name of the control to set focus to
function PageCtrl:SetFocus(name)
end

-- Searches the page naming container for a server control with the specified identifier. 
-- @note: this function is NOT available in OnInit(). use this function in OnCreate()
-- @return: It returns the ParaUIObject or CommonCtrl object depending on the type of the control found.
function PageCtrl:FindControl(name)
	local node = self:GetNode(name)
	if(node and self.name) then	
		return node:GetControl(self.name);
	end
end

-- same as FindControl, except that it only returns UI object. 
function PageCtrl:FindUIControl(name)
	local node = self:GetNode(name)
	if(node and self.name) then	
		return node:GetUIControl(self.name);
	end
end

-- Get bindingtext in the page by its name. 
-- a page will automatically create a binding context for each <pe:editor> and <form> node. 
-- @return : binding context is returned or nil. bindContext.values contains the data source for the databinding controls. 
function PageCtrl:GetBindingContext(name)
	local node = self:GetNode(name)
	if(node) then	
		local instName = node:GetInstanceName(self.name);
		local bindingContext = Map3DSystem.mcml_controls.pe_editor.GetBinding(instName);
		if(bindingContext) then
			-- bindingContext:UpdateControlsToData();
			-- bindingContext.values
		end	
		return bindingContext;
	end
end

-- get the root node. it may return nil if page is not finished yet. 
function PageCtrl:GetRoot()
	return self.mcmlNode
end

-- provide jquery-like syntax to find all nodes that match a given name pattern and then use the returned object to invoke a method on all returned nodes. 
--  e.g. node:jquery("a"):show();
-- @param pattern: The valid format is [tag_name][#name_id][.class_name]. 
--  e.g. "div#name.class_name", "#some_name", ".some_class", "div"
function PageCtrl:jquery(...)
	if(self.mcmlNode) then
		return self.mcmlNode:jquery(...);
	end
end

-- get a mcmlNode by its name. 
-- @return: the first mcmlNode found or nil is returned. 
function PageCtrl:GetNode(name)
	if(self.mcmlNode and name) then
		return self.mcmlNode:SearchChildByAttribute("name", name)
	end
end

-- get a mcmlNode by its id.  if not found we will get by name
-- @param id: id or name of the node.
-- @return: the first mcmlNode found or nil is returned. 
function PageCtrl:GetNodeByID(id)
	if(self.mcmlNode and id) then
		local node = self.mcmlNode:SearchChildByAttribute("id", id)
		if(node) then
			return node;
		else
			return self.mcmlNode:SearchChildByAttribute("name", id)
		end
	end
end

-- set the inner text of a mcmlNode by its name. 
-- this function is usually used to change the text of a node before it is created, such as in the OnLoad event. 
function PageCtrl:SetNodeText(name, text)
	local node = self:GetNode(name)
	if(node) then	
		node:SetInnerText(text);
	end
end

-- set a MCML node value by its name
-- @param name: name of the node
-- @param value: value to be set
function PageCtrl:SetNodeValue(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetValue(value);
	end	
end	

-- Get a MCML node value by its name
-- @param name: name of the node
-- @return: the value is returned
function PageCtrl:GetNodeValue(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetValue();
	end	
end

-- set a MCML node UI value by its name. Currently support: text input
-- @param name: name of the node
-- @param value: value to be set
function PageCtrl:SetUIValue(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetUIValue(self.name, value);
	else
		-- log("warning: mcml page item "..tostring(name).."not found in SetUIValue \n")	
	end	
end	

-- Get a MCML node UI value by its name. Currently support: text input
-- @param name: name of the node
-- @return: the value is returned
function PageCtrl:GetUIValue(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetUIValue(self.name);
	else
		LOG.std(nil, "debug", "mcml",  "mcml page item "..tostring(name).."not found in SetUIValue")	
	end	
end

-- Get UI value if UI can be found or get Node value
function PageCtrl:GetValue(name, value)
	local value_ = self:GetUIValue(name);
	if(value_==nil) then
		return self:GetNodeValue(name, value);
	else
		return value_;	
	end	
end

-- set node value and set UI value if UI can be found.
function PageCtrl:SetValue(name, value)
	self:SetNodeValue(name,value)
	self:SetUIValue(name,value)
end

-- set node value and set UI value if UI can be found.
function PageCtrl:SetUIEnabled(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetUIEnabled(self.name, value);
	end
end

-- Get UI background if UI can be found or get Node value
function PageCtrl:GetUIBackground(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetUIBackground(self.name);
	else
		LOG.std(nil, "debug", "mcml", "mcml page item "..tostring(name).."not found in GetUIBackground");
	end	
end

-- set node value and set UI backgroud if UI can be found.
function PageCtrl:SetUIBackground(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetUIBackground(self.name, value);
	else
		LOG.std(nil, "debug", "mcml", "mcml page item "..tostring(name).."not found in SetUIBackground");
	end
end

-- call a page control method
-- @param name: name of the node
-- @param methodName: name of the method
-- @return: the value from method is returned
function PageCtrl:CallMethod(name, methodName, ...)
	local node = self:GetNode(name);
	if(node) then
		return node:CallMethod(self.name, methodName, ...);
	else
		LOG.std(nil, "debug", "mcml",  "mcml page item:"..tostring(name).." not found in CallMethod")
	end	
end

-- Update the region causing all MCML controls inside the region control to be deleted and rebuilt. 
-- <pe:container> and <pe:editor> are the only supported region control at the moment. 
-- This function is used to reconstruct a sub region of mcml in a page. 
-- if the region control is not created before, this function does nothing, this is the correct logic 
-- when the region control is inside a lazy loaded control such as a tab view. 
-- @param name: name of the region control.
-- @return true if succeed
function PageCtrl:UpdateRegion(name)
	local regionNode = self:GetNode(name);
	if(regionNode) then
		local _parent = regionNode:GetControl(self.name);
		if(_parent) then
			local bindingContext = self:GetBindingContext(name);
			
			local css = regionNode:GetStyle(Map3DSystem.mcml_controls.pe_html.css["pe:editor"]);
			local padding_left, padding_top, padding_bottom, padding_right = 
				(css["padding-left"] or css["padding"] or 0),(css["padding-top"] or css["padding"] or 0),
				(css["padding-bottom"] or css["padding"] or 0),(css["padding-right"] or css["padding"] or 0);
			
			local contentLayout = Map3DSystem.mcml_controls.layout:new();
			contentLayout:reset(padding_left, padding_top, _parent.width-padding_left-padding_right, _parent.height-padding_top-padding_bottom);
			
			Map3DSystem.mcml_controls.pe_editor.refresh(self.name, regionNode, bindingContext, _parent, 
				{color = css.color, ["font-family"] = css["font-family"],  ["font-size"]=css["font-size"], ["font-weight"] = css["font-weight"], ["text-align"] = css["text-align"]}, contentLayout)
		end
	end
end

-- automatically submit a form.
-- @param formNode: form node or nil. if nil, it will use the first form found.
function PageCtrl:SubmitForm(formNode)
	if(formNode==nil) then
		local formNodes = self:GetRoot():GetAllChildWithName("form") or self:GetRoot():GetAllChildWithName("pe:editor");
		if(formNodes ~= nil and table.getn(formNodes)>=1) then
			formNode = formNodes[1];
		end
	end	
	-- submit the change by locating the hidden or visible submit button inside the form node
	if(formNode~=nil) then
		local submitBtn = formNode:SearchChildByAttribute("type", "submit")
		if(submitBtn) then
			local bindingContext = Map3DSystem.mcml_controls.pe_editor.GetBinding(formNode:GetInstanceName(self.name));
			if(bindingContext) then
				local script = Map3DSystem.mcml_controls.pe_editor_button.GetOnClickScript(submitBtn:GetInstanceName(self.name), submitBtn, bindingContext)
				if(script) then
					script = string.gsub(script, "^;", "");
					NPL.DoString(script);
				end
			else
				log("warning: unable to find binding context for MCML formNode in pageCtrl SubmitForm \n");
			end	
		end
	end
end	

-- create or get page scope
function PageCtrl:GetPageScope()
	if(not self._PAGESCRIPT) then
		self._PAGESCRIPT = {
			-- evaluate a value in page scope
			Eval = pe_script.PageScope.Eval,
			-- evaluate a value in page scope. supports hierachy such as "Book/Title", "Book.Title"
			XPath = pe_script.PageScope.XPath,
			-- the page control object
			Page = self,
		};
		-- SECURITY NOTE: 
		-- expose global environment to the inline script via meta table
		local meta = getmetatable (self._PAGESCRIPT)
		if not meta then
			meta = {}
			setmetatable (self._PAGESCRIPT, meta)
		end
		meta.__index = _G	
	end
	return self._PAGESCRIPT;
end	

-- Get the page style object
function PageCtrl:GetStyle()
	if(not self.style) then
		self.style = Style:new();
	end
	return self.style;
end

--------------------------------------
-- private method
--------------------------------------

-- called when page is downloaded
function PageCtrl.OnPageDownloaded_CallBack(xmlRoot, entry, self)
	if(self and (not entry or self.status~=1))then 
		-- NOTE: only update if page is not ready yet. this will ignore expired remote page update. 
		if(xmlRoot) then
			local xmlRoot = Map3DSystem.mcml.buildclass(xmlRoot);
			local mcmlNode = commonlib.XPath.selectNode(xmlRoot, "//pe:mcml");
			
			if(mcmlNode) then
				-- ready status
				self.status=1;
				self.mcmlNode = mcmlNode;
				self.style = nil;
				self._PAGESCRIPT = nil; -- clear page scope
				
				-- rebuild UI
				self:OnRefresh();
			else
				self.status=3;
				self.status_line = "网页中没有可以显示的mcml数据。[提示]你的网页至少要包含一个<pe:mcml>";
				self:OnRefresh();
			end	
			if(type(self.OnPageDownloaded) == "function") then
				self.OnPageDownloaded();
			elseif (type(self.OnPageDownloaded) == "string") then
				NPL.DoString(self.OnPageDownloaded);
			end
		end
	end	
end




```