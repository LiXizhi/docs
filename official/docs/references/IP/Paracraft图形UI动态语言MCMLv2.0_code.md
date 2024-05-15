```lua

--[[
Title: Page
Author(s): LiXizhi
Date: 2015/4/27
Desc:
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/ide/System/Windows/mcml/Page.lua");
local Page = commonlib.gettable("System.Windows.mcml.Page");
local page = Page:new();
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Core/ToolBase.lua");
NPL.load("(gl)script/ide/System/Windows/mcml/PageLayout.lua");
NPL.load("(gl)script/ide/System/Windows/mcml/Style.lua");
local Style = commonlib.gettable("System.Windows.mcml.Style");
local mcml = commonlib.gettable("System.Windows.mcml");
local Elements = commonlib.gettable("System.Windows.mcml.Elements");
local PageLayout = commonlib.gettable("System.Windows.mcml.PageLayout");

local Page = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.createtable("System.Windows.mcml.Page", {
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
	-- this is a user-defined call back function (filelist) end. it is called whenever user drop files on this page.
	-- note return true to tell dispatcher we're interested in this message, otherwise return false.
	OnDropFiles = nil,
}));
Page:Property("Name", "Page");
Page:Signal("created");

-- make jquery-like invoke
getmetatable(Page:new()).__call = function(self, ...)
	return self:jquery(...)
end

function Page:ctor()
	-- this will prevent recursive calls to self:Refresh(), which makes self:Refresh(0) pretty safe.
	self.refresh_depth = 0;
	self.hotkeyNodes = {};
	self.tabIndexNodes = {};
	self.currentTabNode = nil;
end

-- Init control with a MCML treenode or page url. If a local version is found, it will be used regardless of whether it is expired or not.
-- It does not create UI until Page:Create() is called.
-- _NOTE_: Calling this function with different urls after Page:Create() will refresh the UI by latest url.
--@param url: the url of the MCML page. It must contain one <pe:mcml> node. Page should be UTF-8 encoded. It will automatically replace %params% in url if any
-- if url is nil, content will be cleared. if it is a table, it will be the mcmlNode to open.
--@param cache_policy: cache policy object. if nil, default is used.
--@param bRefresh: whether to refresh if url is already loaded before.
function Page:Init(url, cache_policy, bRefresh)
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
		Page.OnPageDownloaded_CallBack(url, nil, self)
		return
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
			ls:CallXML(cache_policy or self.cache_policy, url, Page.OnPageDownloaded_CallBack, self)
		end
	else
		-- for local file, open it directly
		-- remove requery string when parsing file.
		local filename = string.gsub(url, "%?.*$", "")

		local xmlRoot = ParaXML.LuaXML_ParseFile(filename);
		if(type(xmlRoot)=="table" and table.getn(xmlRoot)>0) then
			Page.OnPageDownloaded_CallBack(xmlRoot, nil, self)
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
function Page:Goto(url, cache_policy, bRefresh)
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
function Page:Rebuild(url, cache_policy, bRefresh)
	self:Goto(url or "refresh", cache_policy, bRefresh);
end

-- close and destory all UI objects created by this page.
-- only call this function if self.name is a global name.
function Page:Close()
	if(self.name) then
		ParaUI.Destroy(self.name)
	end
end

-- in case this page is inside an iframe, the parentpage contains the page control that created the iframe.
function Page:GetParentPage()
	return self.parentpage
end

-- Get the top most root page
function Page:GetRootPage()
	if(self.parentpage) then
		return self.parentpage:GetRootPage();
	else
		return self;
	end
end

-- get the parent window containing this page.
function Page:GetWindow()
	if(self.layout) then
		local window = self.layout:widget();
		if(window) then
			return window:GetWindow();
		end
	else
		if(self:GetParentPage()) then
			return self:GetParentPage():GetWindow();
		end
	end
end

-- a safe method to decide if the page is visible or not.
-- @return true if page is visible.
function Page:IsVisible()
end

-- get the parent ui object
function Page:GetParentUIObject()
end

-- close the containing window
-- @param bDestroy: if true, it will destroy the window, otherwise it will just hide it.
function Page:CloseWindow(bDestroy)
	local wnd = self:GetWindow();
	if(wnd) then
		wnd:CloseWindow(bDestroy);
	end
end

-- set the text and/or icon of the page's container window
function Page:SetWindowText(text,icon)
	local wnd = self:GetWindow();
	if(wnd) then
		-- wnd:SetWindowText(text,icon);
	end
end

-------------------------------------
-- overridable functions
-------------------------------------

-- this function is overridable. it is called before page UI is about to be created.
-- You cannot use view-state information within this event; it is not populated yet.
-- @param self.mcmlNode: the root pe:mcml node, one can modify it here before the UI is created, such as filling in default data.
function Page:OnLoad()
end

-- this function is overridable. it is called after page UI is created.
-- One can perform any processing steps that are set to occur on each page request. You can access view state information. You can also access controls within the page's control hierarchy.
-- In other words, one can have direct access to UI object created in the page control. Note that some UI are lazy created
-- such as treeview item and tab view items. They may not be available here yet.
function Page:OnCreate()
end

-- forcing a repaint in the next frame. this function does nothing if SelfPaint is false.
function Page:InvalidateRect()
	if(self.SelfPaint) then
		local parent = self:GetParentUIObject()
		if(parent) then
			parent:InvalidateRect();
		end
	end
end
-- get the used size of the page. This is called to obtain the actual size used to render the mcml page.
function Page:GetUsedSize()
	return self.used_width, self.used_height;
end

-- add current opened url to the opened urls stack so that we can move forward or backward.
-- if the last url is the same as current, url will not be added.
-- @param url; nil or url string to add. if nil, self.url is used.
function Page:AddOpenedUrl(url)
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
function Page:Refresh(DelayTime)

	DelayTime = DelayTime or self.DefaultRefreshDelayTime;
	self.RefreshCountDown = (self.RefreshCountDown or 0);
	if(self.RefreshCountDown < DelayTime) then
		self.RefreshCountDown = DelayTime;
	end
	if(self.RefreshCountDown<=0) then
		self:OnRefresh();
	else
		self:ChangeTimer(DelayTime*1000);
	end
end

-- virtual: do refresh page if there is a request
function Page:OnTick()
	-- in case there is page error in previous page load, this will recover the refresh depth.
	self.refresh_depth = 0;

	if(self.RedirectCountDown) then
		self.RedirectCountDown = nil;
		if(self.redirectParams) then
			self:Goto(self.redirectParams.url, self.redirectParams.cache_policy, self.redirectParams.bRefresh);
			self.redirectParams = nil;
			self.RefreshCountDown = nil;
		end
	end
	if(self.RefreshCountDown) then
		self.RefreshCountDown = nil;
		self:OnRefresh();
	end
end

-- Same as Goto(), except that it contains a delay time. this function is safe to be called via embedded page code.
-- it will redirect page in DelayTime second
-- @param url: relative or absolute url, like you did in a src tag
-- if url is nil, content will be cleared. if it is a table, it will be the mcmlNode to open.
-- @param cache_policy: cache policy object. if nil, default is used.
-- @param bRefresh: whether to refresh if url is already loaded before.
-- @param DelayTime: if nil, it will default to self.DefaultRedirectDelayTime(usually 1 second). we do not allow immediate redirection, even delayTime is 0
function Page:Redirect(url, cache_policy, bRefresh, DelayTime)
	if(self.mcmlNode) then
		url = self.mcmlNode:GetAbsoluteURL(url);
	end

	self.RedirectCountDown = DelayTime or self.DefaultRedirectDelayTime;
	-- we do not allow immediate redirection, even delayTime is 0
	self.redirectParams = {url=url, cache_policy=cache_policy, bRefresh=bRefresh};
	self:ChangeTimer(DelayTime*1000);
end

-- get the url request of the mcml node if any. It will search for "request_url" attribtue field in the ancestor of this node.
-- Page and BrowserWnd will automatically insert "request_url" attribtue field to the root MCML node before instantiate them.
-- @return: nil or the request_url is returned. we can extract requery string parameters using regular expressions or using GetRequestParam
function Page:GetRequestURL()
	return self.mcmlNode:GetAttribute("request_url");
end

-- if you want to modify request_url and then refresh the page. call this function.
function Page:SetURL(url)
	self.url = url;
	if(self.mcmlNode) then
		self.mcmlNode:SetAttribute("request_url", url)
	end
end


-- get request url parameter by its name. for example if page url is "www.paraengine.com/user?id=10&time=20", then GetRequestParam("id") will be 10.
-- @param paramName: if nil, it will return a table containing all name,value pairs.
-- @return: nil or string value or a table.
function Page:GetRequestParam(paramName)
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
function Page:DataBind()
end

-- Gets the first data item by its name in the data-binding context of this page.
function Page:GetDataItem(name)
end

-- Sets the focus to the control with the specified name.
-- @param name: The name of the control to set focus to
function Page:SetFocus(name)
end

-- Searches the page naming container for a server control with the specified identifier.
-- @note: this function is NOT available in OnInit(). use this function in OnCreate()
-- @return: It returns the ParaUIObject or CommonCtrl object depending on the type of the control found.
function Page:FindControl(name)
	local node = self:GetNode(name)
	if(node and self.name) then
		return node:GetControl(self.name);
	end
end

-- same as FindControl, except that it only returns UI object.
function Page:FindUIControl(name)
	local node = self:GetNode(name)
	if(node and self.name) then
		return node:GetUIControl(self.name);
	end
end

-- Get bindingtext in the page by its name.
-- a page will automatically create a binding context for each <pe:editor> and <form> node.
-- @return : binding context is returned or nil. bindContext.values contains the data source for the databinding controls.
function Page:GetBindingContext(name)
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
function Page:GetRoot()
	return self.mcmlNode
end

-- provide jquery-like syntax to find all nodes that match a given name pattern and then use the returned object to invoke a method on all returned nodes.
--  e.g. node:jquery("a"):show();
-- @param pattern: The valid format is [tag_name][#name_id][.class_name].
--  e.g. "div#name.class_name", "#some_name", ".some_class", "div"
function Page:jquery(...)
	if(self.mcmlNode) then
		return self.mcmlNode:jquery(...);
	end
end

-- get a mcmlNode by its name.
-- @return: the first mcmlNode found or nil is returned.
function Page:GetNode(name)
	if(self.mcmlNode and name) then
		return self.mcmlNode:SearchChildByAttribute("name", name)
	end
end

-- get a mcmlNode by its id.  if not found we will get by name
-- @param id: id or name of the node.
-- @return: the first mcmlNode found or nil is returned.
function Page:GetNodeByID(id)
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
function Page:SetNodeText(name, text)
	local node = self:GetNode(name)
	if(node) then
		node:SetInnerText(text);
	end
end

-- set a MCML node value by its name
-- @param name: name of the node
-- @param value: value to be set
function Page:SetNodeValue(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetValue(value);
	end
end

-- Get a MCML node value by its name
-- @param name: name of the node
-- @return: the value is returned
function Page:GetNodeValue(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetValue();
	end
end

-- set a MCML node UI value by its name. Currently support: text input
-- @param name: name of the node
-- @param value: value to be set
function Page:SetUIValue(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetUIValue(value);
	else
		-- log("warning: mcml page item "..tostring(name).."not found in SetUIValue \n")
	end
end

-- Get a MCML node UI value by its name. Currently support: text input
-- @param name: name of the node
-- @return: the value is returned
function Page:GetUIValue(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetUIValue(self.name);
	else
		LOG.std(nil, "debug", "mcml",  "mcml page item "..tostring(name).."not found in SetUIValue")
	end
end

-- Get UI value if UI can be found or get Node value
function Page:GetValue(name, value)
	local value_ = self:GetUIValue(name);
	if(value_==nil) then
		return self:GetNodeValue(name, value);
	else
		return value_;
	end
end

-- set node value and set UI value if UI can be found.
function Page:SetValue(name, value)
	self:SetNodeValue(name,value)
	self:SetUIValue(name,value)
end

-- set node value and set UI value if UI can be found.
function Page:SetUIEnabled(name, value)
	local node = self:GetNode(name);
	if(node) then
		node:SetUIEnabled(self.name, value);
	end
end

-- Get UI background if UI can be found or get Node value
function Page:GetUIBackground(name)
	local node = self:GetNode(name);
	if(node) then
		return node:GetUIBackground(self.name);
	else
		LOG.std(nil, "debug", "mcml", "mcml page item "..tostring(name).."not found in GetUIBackground");
	end
end

-- set node value and set UI backgroud if UI can be found.
function Page:SetUIBackground(name, value)
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
function Page:CallMethod(name, methodName, ...)
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
function Page:UpdateRegion(name)
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
function Page:SubmitForm(formNode)
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
function Page:GetPageScope()
	if(not self._PAGESCRIPT) then
		self._PAGESCRIPT = {
			-- evaluate a value in page scope
			Eval = Elements.pe_script.PageScope.Eval,
			-- evaluate a value in page scope. supports hierachy such as "Book/Title", "Book.Title"
			XPath = Elements.pe_script.PageScope.XPath,
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

--------------------------------------
-- private method
--------------------------------------

-- called when page is downloaded
function Page.OnPageDownloaded_CallBack(xmlRoot, entry, self)
	if(self and (not entry or self.status~=1))then
		-- NOTE: only update if page is not ready yet. this will ignore expired remote page update.
		if(xmlRoot) then
			local mcmlNode = commonlib.XPath.selectNode(xmlRoot, "//pe:mcml");

			if(mcmlNode) then
				self:LoadFromXmlNode(mcmlNode);
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

-- load the page from xml Node
function Page:LoadFromXmlNode(xmlNode)
	-- ready status
	self.status=1;
	self.style = nil;
	self.mcmlNode = mcml:createFromXmlNode(xmlNode);
	self._PAGESCRIPT = nil; -- clear page scope
	-- rebuild UI
	self:OnRefresh();
end

-- refresh the page UI. It will remove all previous UI and rebuild (render) from current MCML page data.
-- it will call the OnLoad method.
-- _Note_ One can override this method to owner draw this control.
-- @param _parent: if nil, it will get using the self.name.
-- @return: the parent container of page ctrl is returned.
function Page:OnRefresh()
	self.RefreshCountDown = nil;
	local layout = self.layout;
	if(not layout) then
		return;
	end
	local uiElem = layout:widget();

	if(self.refresh_depth > 0) then
		-- if we are refreshing a page within a page, we will automatically delay it.
		LOG.std("", "warning", "mcml", "recursive page refresh is detected for page %s. Please use page:Refresh() instead of Refresh(0).", tostring(self.url));
		-- self:Refresh(0.01);
		return;
	end
	self.refresh_depth = self.refresh_depth + 1;

	if(self.status== 1 and self.mcmlNode) then
		-- call OnLoad
		self:OnLoad();

		-- create the mcml UI controls.
		local width, height = uiElem:width(), uiElem:height();
		-- secretely inject the "request_url" in it, so that we can make href using relative to site or url path.
		self.mcmlNode:SetAttribute("request_url", self.url);
		-- secretely put this page control object into page_ctrl field, so that we can refresh this page with a different url, such as in pe_a or form submit button.
		self.mcmlNode:SetAttribute("page_ctrl", self);

		self:LoadComponent();

		self.used_width, self.used_height = layout:GetUsedSize();

		self:OnCreate();
		-- add url
		self:AddOpenedUrl();
	else
		-- TODO: display an animated background in _parent for other self.status values, such as downloading or error.
		-- TODO: we can also display a user defined self.errorpage page.
		-- log("warning:"..tostring(self.status_line).."\n")
	end
	self.refresh_depth = self.refresh_depth - 1;
end

-- create all ui elements recursively using the layout.
function Page:LoadComponent()
	local layout = self.layout;
	if(layout and self.mcmlNode) then
		local parentElem = layout:widget();
		if(parentElem) then
			self.mcmlNode:LoadComponent(parentElem, layout, nil);
		end
	end
end

-- Get the page style object
function Page:GetStyle()
	if(not self.style) then
		self.style = Style:new():init(self);
		self.style:AddReference(mcml:GetStyle(), "mcss");
	end
	return self.style;
end

-- create (instance) the page UI. It will create UI immediately after the page is downloaded. If page is local, it immediately load.
-- @param name: name of the control. it should be globally unique if page is asynchronous. and it can be anything, if page is local.
function Page:Create(name, _parent, alignment, left, top, width, height, bForceDisabled)
	-- obsoleted: create empty window instead to make it API compatible with old version.
	-- TODO:
end

function Page:Attach(uiElement)
	if(uiElement) then
		uiElement:deleteChildren();
		if(uiElement.layout) then
			uiElement.layout = nil;
		end
		self:Detach();
		self.layout = PageLayout:new();
		self.layout:SetPage(self, uiElement);
		uiElement.layout = self.layout;
	end
end

function Page:Detach()
	if(self.layout) then
		local uiElem = self.layout:widget();
		if(uiElem) then
			uiElem:deleteChildren();
			uiElem.layout = nil;
		end
		self.layout = nil;
	end
end


function Page:AddHotkeyNode(node, hotkey, func)
	if(not func) then
		func = node.OnClick;
	end
	self.hotkeyNodes[hotkey] = {node = node, func = func};
end

function Page:RemoveHotkeyNode(node, hotkey)
	local hotkeyNode = self.hotkeyNodes[hotkey];
	if(hotkeyNode and hotkeyNode.node == node) then
		self.hotkeyNodes[hotkey] = nil;
	end
end

function Page:HandlHotkeyEvent(hotkey)
	-- 支持组合按键识别
	local ctrl_pressed = ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_LCONTROL) or ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_RCONTROL);
	local alt_pressed = ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_LMENU) or ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_RMENU);
	local shift_pressed = ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_LSHIFT) or ParaUI.IsKeyPressed(DIK_SCANCODE.DIK_RSHIFT);
	local comboKeyStr = "";
	if ctrl_pressed and hotkey ~= "DIK_LCONTROL" and hotkey ~= "DIK_RCONTROL" then
		comboKeyStr = comboKeyStr .. "DIK_CONTROL + ";
	elseif alt_pressed and hotkey ~= "DIK_LMENU" and hotkey ~= "DIK_RMENU" then
		comboKeyStr = comboKeyStr .. "DIK_MENU + ";
	elseif shift_pressed and hotkey ~= "DIK_LSHIFT" and hotkey ~= "DIK_RSHIFT" then
		comboKeyStr = comboKeyStr .. "DIK_SHIFT + ";
	end
	hotkey = comboKeyStr .. hotkey;

	local hotkeyNode = self.hotkeyNodes[hotkey];
	if(hotkeyNode and hotkeyNode.func) then
		hotkeyNode.func(hotkeyNode.node);
		return true;
	end
	return false;
end

function Page:AddTabIndexNode(index, node)
	local insert_pos;
	for pos, node in ipairs(self.tabIndexNodes) do
		local node_index = node:TabIndex();
		if(index < node_index) then
			insert_pos = pos;
		end
	end
	if(insert_pos) then
		table.insert(self.tabIndexNodes, insert_pos, node);
	else
		table.insert(self.tabIndexNodes, node);
	end
end

function Page:FocusNode()
	return self.currentTabNode;
end

function Page:SetFocusNode(node)
	self.currentTabNode = node;
end

function Page:NextTabNode()
	if(not self.currentTabNode and #self.tabIndexNodes ~= 0) then
		return self.tabIndexNodes[1];
	end

	if(not self.currentTabNode) then
		return self.mcmlNode:NextTabNode();
	end

	local size = #self.tabIndexNodes;
	if(self.currentTabNode:TabIndex() ~= 0) then
		-- self.currentTabNode isn't the last node in self.tabIndexNodes;
		for i = 1, size do
			local node = self.tabIndexNodes[i];
			if(self.currentTabNode == node) then
				if(i < size) then
					return self.tabIndexNodes[i + 1];
				else
					return self.mcmlNode:NextTabNode();
				end
			end
		end
	end

	return self.currentTabNode:NextTabNode()
end

function Page:HandlKeyPressEvent(key)
	if(self:HandlHotkeyEvent(key)) then
		return true;
	end

	if(key == "DIK_TAB") then
		if(self.currentTabNode and not self.currentTabNode:TabLostFocus()) then
			return false;
		end
		self.currentTabNode = self:NextTabNode();
		if(not self.currentTabNode) then
			self.currentTabNode = self:NextTabNode();
		end
		self.currentTabNode:SetFocus();
		return true;
	end

	return false;
end

--[[
Title: PageLayout
Author(s): LiXizhi
Date: 2015/4/27
Desc: the layout manager used by mcml Page.
Each mcml page has only one page layout manager attached to the root UIElement that the page is associated with. 
Unlike other Layout manager, the mcml page layout manager will use the PageElement as LayoutItem directly. 
Hence there is no need to create addition layoutitem object. 

use the lib:
------------------------------------------------------------
NPL.load("(gl)script/ide/System/Windows/mcml/PageLayout.lua");
local PageLayout = commonlib.gettable("System.Windows.mcml.PageLayout");
local layout = PageLayout:new();
local parentLayout = PageLayout:new():init(0,0,200,100);

-- clone child object
parentLayout:NewLine();
local myLayout = parentLayout:clone();
myLayout:SetUsedSize(0,0);

-- update parent
myLayout:NewLine();
local left, top = parentLayout:GetAvailablePos();
local width, height = myLayout:GetUsedSize();
width, height = width-left, height -top;
parentLayout:AddObject(width, height);
parentLayout:NewLine();
	
-- add full size
parentLayout:NewLine();
local left, top, width, height = parentLayout:GetPreferredRect();
parentLayout:AddObject(width-left, height-top);
parentLayout:NewLine();
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/Windows/Layout.lua");
local PageLayout = commonlib.inherit(commonlib.gettable("System.Windows.Layout"), commonlib.createtable("System.Windows.mcml.PageLayout", {
	-- the next available renderable position 
	availableX = 0,
	availableY = 0,
	-- the next new line position
	newlineX = 0,
	newlineY = 0,
	-- the current preferred size of the container control. It may be enlarged by child controls. 
	width = 0,
	height = 0,
	-- the min region in the container control which is occupied by its child controls
	usedWidth = 0,
	usedHeight = 0,
	-- the real region in the container control which is occupied by its child controls
	realWidth = 0,
	realHeight = 0,
}));

function PageLayout:ctor()
end

-- return a clone of this PageLayout object. 
-- in most cases, one also calls SetUsedSize(0,0) to make the copy useful for a child PageLayout. 
function PageLayout:clone()
	return self:new({
		availableX = self.availableX,
		availableY = self.availableY,
		newlineX = self.newlineX,
		newlineY = self.newlineY,
		width = self.width,
		height = self.height,
		usedWidth = self.usedWidth,
		usedHeight = self.usedHeight,
		realWidth = self.realWidth,
		realHeight = self.realHeight,
	});
end

-- initialize a top level layout manager for a given page object(parent).
function PageLayout:SetPage(page, uiElement)
	self.parent = uiElement;
	self.page = page;
	self.topLevel = true;
end

-- recalculate the layout according to current uiElement (Window)'s size
function PageLayout:activate()
	if (self.activated) then
        return false;
	end
	if(self.page and self.parent) then
		local pageElem = self.page:GetRoot();
		if(pageElem) then
			self:doResize(self.parent:width(), self.parent:height());
			self.activated = true;
		end
	end
end

function PageLayout:invalidate()
	self:reset(0,0,0,0);
    PageLayout._super.invalidate(self);
end

-- virtual function: 
function PageLayout:doResize(width, height)
	if(self.page) then
		local pageElem = self.page:GetRoot();
		if(pageElem) then
			if(width == 0 and height == 0) then
				-- skip layout, if size is not known yet. This can happen when we show a widow without specifying its size.  
			else
				if(self.width ~= width or self.height~=height) then
					self:reset(0, 0, width, height);
					pageElem:UpdateLayout(self, nil);
				end
			end
		end
	end
end

function PageLayout:init(left, top, width, height)
	self:reset(left, top, width, height);
	return self;
end

-- return the top level mcml page object. 
function PageLayout:GetPage()
	if(self.topLevel) then
		return self.page;
	elseif(self.parent) then
		return self.parent:GetPage();
	end
end

-- If this item is a UI element, it is returned as a UI element; otherwise nil is returned. 
function PageLayout:widget()
	return self.parent;
end

-- create a new PageLayout, that is the same size of the preferred size but left, top is 0,0;
function PageLayout:new_child()
	local o = PageLayout:new()
	local width, height = self:GetPreferredSize();
	o:reset(0, 0, width, height);
	return o;
end

-- reset with newline position (left, top) and container size (width and height). 
function PageLayout:reset(left, top, width, height)
	self.newlineX = left;
	self.newlineY = top;
	if(left<width) then
		self.width = width;
	else
		self.width = left;
	end	
	if(top<height) then
		self.height = height;
	else
		self.height = top;
	end	
	self:NewLine();
end

-- a control may call this function to check its preferred size. 
-- if the preferred size is big enough, it can use this size when calling AddObject,
-- otherwise, it can either call NewLine() or AddObject with a bigger size. 
-- return preferred width, height
function PageLayout:GetPreferredSize()
	return self.width-self.availableX, self.height - self.availableY;
end

function PageLayout:GetPreferredRect()
	return self.availableX, self.availableY, self.width, self.height;
end

function PageLayout:GetPreferredPos()
	return self.availableX, self.availableY;
end

function PageLayout:SetPreferredPos(x, y)
	self.availableX, self.availableY = x, y; 
end

-- get the max available size
function PageLayout:GetMaxSize()
	return self.width-self.newlineX, self.height - self.newlineY;
end

-- get the size
function PageLayout:GetSize()
	return self.width, self.height;
end
-- set the size
function PageLayout:SetSize(width, height)
	self.width, self.height = width, height;
end

-- get used size
function PageLayout:GetUsedSize()
	return self.usedWidth, self.usedHeight;
end

-- set used size
function PageLayout:SetUsedSize(width, height)
	self.usedWidth, self.usedHeight = width, height;
end

-- get real size
function PageLayout:GetRealSize()
	return self.realWidth, self.realHeight;
end

-- set real size
function PageLayout:SetRealSize(width, height)
	self.realWidth, self.realHeight = width, height;
end

-- clear the used size to currently available pos. 
function PageLayout:ResetUsedSize()
	self.usedWidth, self.usedHeight = self.availableX, self.availableY;
end

-- get the available rect by left, top, right, bottom. 
function PageLayout:GetAvailableRect()
	return self.availableX, self.availableY, self.width, self.height;
end

-- get the available rect by left, top
function PageLayout:GetAvailablePos()
	return self.availableX, self.availableY;
end

-- get the newline position (left, top)
function PageLayout:GetNewlinePos()
	return self.newlineX, self.newlineY;
end

-- offset the new line and available position of this PageLayout. 
function PageLayout:OffsetPos(dx, dy)
	if(dx) then
		self.newlineX = self.newlineX+dx;
		self.availableX = self.availableX+dx;
	end
	if(dy) then
		self.newlineY = self.newlineY+dy;
		self.availableY = self.availableY+dy;
	end
end
-- Set the new line and available absolute position of this PageLayout. 
function PageLayout:SetPos(x,y)
	if(x) then
		self.newlineX = x;
		self.availableX = x;
	end
	if(y) then
		self.newlineY = y;
		self.availableY = y;
	end
end

-- childLayout is usually cloned from this PageLayout and this PageLayout will expand to accommandate childLayout. 
function PageLayout:AddChildLayout(childLayout)
	local left, top = self:GetAvailablePos();
	local width, height = childLayout:GetUsedSize();
	self:AddObject(width-left, height-top);
end

-- add object at the current available position. if available position is not big enough, it will start a new line. 
-- object still can not fit in a newline, it will increase its container size. 
-- THIS IS A TRICKY FUNCTION
-- return the left, top position of the added object. 
function PageLayout:AddObject(width, height)
	local left, top;
	if((self.availableX+width)>self.width) then
		-- start a new line. 
		self:NewLine();
	end
	left, top = self.availableX, self.availableY;
	self.availableX = left+width;
	if((top+height)>self.newlineY) then
		self.newlineY = top+height
		if(self.newlineY>self.height) then
			-- increase height to best contain the child object
			self.height = self.newlineY;
		end
	end
	if(self.availableX>self.width) then
		-- increase width to best contain the child object
		self.width = self.availableX;
		-- start new line since it used up all horizontal spaces after object is added. 
		self:NewLine(); 
	end
	if(self.usedWidth<(left+width)) then
		self.usedWidth = left+width;
	end	
	if(self.usedHeight<(top+height)) then
		self.usedHeight = top+height;
	end
	return left, top;
end

-- make a new line in the PageLayout
function PageLayout:NewLine()
	self.availableX = self.newlineX
	self.availableY = self.newlineY
	--log("newline:"..self.newlineX.." "..self.newlineY.."\n")
end

-- increase preferred height of this PageLayout
function PageLayout:IncHeight(dHeight)
	self.height = self.height + dHeight;
end

-- increase preferred width of this PageLayout
function PageLayout:IncWidth(dWidth)
	self.width = self.width + dWidth;
end

--[[
Title: PageElement
Author(s): LiXizhi
Date: 2015/4/27
Desc: base class to all page elements. 
Page element is responsible for creation, layout, editing(via external mcml editors) of UIElements. 
Each page element may be associated with zero or more UI elements. 

virtual functions:
	LoadComponent(parentElem, parentLayout, style) 
		OnLoadComponentBeforeChild(parentElem, parentLayout, css)
		OnLoadComponentAfterChild(parentElem, parentLayout, css)
	UpdateLayout(layout) 
		OnBeforeChildLayout(layout)
		OnAfterChildLayout(layout, left, top, right, bottom)
	paintEvent(painter)

---++ Guideline for subclass PageElement. 
Whenever a page is first loaded or refreshed, LoadComponent() is called once.
You need to overload either LoadComponent, OnLoadComponentBeforeChild, or OnLoadComponentAfterChild 
to create any inner UI Element and attach them properly to the passed-in parent UI element. 
Remember to keep a reference of the UI element on the page element as well, so that you can re-position them 
during UpdateLayout(). If there is only one UI element, we usually call SetControl() to assign it to self.control. 

After all page component is loaded, the UpdateLayout will be called. 
You need to override either UpdateLayout, OnBeforeChildLayout or OnAfterChildLayout,
 to setGeometry of any loaded components(i.e. UI Element). UpdateLayout may be called recursively. 
It is also called when the top level layout resizes due to user interaction or resize event. 

If your page element handles paintEvent, you must call EnableSelfPaint() during one of the LoadComponent overrides.
It will create a dummy UIElement which redirect paintEvent to the pageElement. 

use the lib:
------------------------------------------------------------
NPL.load("(gl)script/ide/System/Windows/mcml/PageElement.lua");
local PageElement = commonlib.gettable("System.Windows.mcml.PageElement");
local elem = PageElement:new();
------------------------------------------------------------
]]
NPL.load("(gl)script/ide/System/localserver/UrlHelper.lua");
NPL.load("(gl)script/ide/System/Windows/mcml/StyleItem.lua");
local StyleItem = commonlib.gettable("System.Windows.mcml.StyleItem");
local mcml = commonlib.gettable("System.Windows.mcml");
local Elements = commonlib.gettable("System.Windows.mcml.Elements");
local PageElement = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.gettable("System.Windows.mcml.PageElement"));
-- default style sheet
PageElement:Property("Name", "PageElement");
PageElement:Property({"class_name", nil});
PageElement:Property({"tab_index", -1, "TabIndex", "SetTabIndex", auto=true});
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
local LOG = LOG;
local NameNodeMap_ = {};
local commonlib = commonlib.gettable("commonlib");

function PageElement:ctor()
end

-- virtual public function: create a page element (and recursively all its children) according to input xmlNode o.
-- generally one do not need to override this function, unless you want to control how child nodes are initialized. 
-- @param o: pure xml node table. 
-- @return the input o is returned. 
function PageElement:createFromXmlNode(o)
	o = self:new(o);
	o:createChildRecursive_helper();
	return o;
end

function PageElement:clone()
	local o = self:new();
	o.name = self.name;
	o.attr = commonlib.copy(self.attr);
	if(#self ~= 0) then
		for i, child in ipairs(self) do
			if(type(child) == "table" and child.clone) then
				o:AddChild(child:clone());
			else
				o:AddChild(commonlib.copy(child));
			end
		end
	end
	return o;
end

-- static public function
function PageElement:createChildRecursive_helper()
	if(#self ~= 0) then
		for i, child in ipairs(self) do
			if(type(child) == "table") then
				local class_type = mcml:GetClassByTagName(child.name or "div");
				if(class_type) then
					class_type:createFromXmlNode(child);
				else
					LOG.std(nil, "warn", "mcml", "can not find tag name %s", child.name or "");
				end
			else
				-- for inner text of xml
				child = Elements.pe_text:createFromString(child);
				self[i] = child;
			end
			child.parent = self;
			child.index = i;
		end
	end
end

-- static function: register as a given tag name. 
-- @param name1, name2, name3, name4: can be nil, or alias name. 
function PageElement:RegisterAs(name, name1, name2, name3, name4)
	mcml:RegisterPageElement(name, self);
	if(name1) then
		mcml:RegisterPageElement(name1, self);
		if(name2) then
			mcml:RegisterPageElement(name2, self);
			if(name3) then
				mcml:RegisterPageElement(name3, self);
				if(name4) then
					mcml:RegisterPageElement(name4, self);
				end
			end
		end
	end
end

-- @param src: can be relative to current file or global filename.
function PageElement:LoadScriptFile(src)
	if(src ~= nil and src ~= "") then
		src = string.gsub(src, "^(%(.*%)).*$", "");
		src = self:GetAbsoluteURL(src);
		--if(ParaIO.DoesFileExist(src, true) or ParaIO.DoesFileExist(string.gsub(src, "(.*)lua", "bin/%1o"), true)) then
		-- SECURITY NOTE: load script in global environment
		NPL.load("(gl)"..src);
		--else
			--log("warning: MCML script does not exist locally :"..src.."\n");
		--end	
	end
end

--local skip_treenode_names = {
--	["NodeTemplates"] = true,
--	["EmptyDataTemplate"] = true,
--	["FetchingDataTemplate"] = true,
--}

local no_parse_nodes = {
	["option"] = true,
	["NodeTemplates"] = true,
	["EmptyDataTemplate"] = true,
	["FetchingDataTemplate"] = true,
	["Columns"] = true,
	["PagerTemplate"] = true,
}

function PageElement:Rebuild(parentElem)
	local styleItem;
	if(self.parent) then
		styleItem = self.parent:GetStyle();
		parentElem = parentElem or self.parent.control;
	end
	self:LoadComponent(parentElem, nil, styleItem)
end

-- virtual function: load component recursively. 
-- generally one do not need to override this function, override 
--  OnLoadComponentBeforeChild and OnLoadComponentAfterChild instead. 
-- @param parentLayout: only for casual initial layout. 
-- @return used_width, used_height
function PageElement:LoadComponent(parentElem, parentLayout, styleItem)
	if(self:GetAttribute("display") == "none") then 
		return 
	end
	if(no_parse_nodes[self.name]) then
		return;
	end


	-- apply models
	self:ApplyPreValues();

	-- process any variables that is taking place. 
	self:ProcessVariables();

	--self:checkAttributes();
	
	if(self:GetAttribute("trans")) then
		-- here we will translate all child nodes recursively, using the given lang 
		-- unless any of the child attribute disables or specifies a different lang
		self:TranslateMe();
	end

	local css = self:CreateStyle(nil, styleItem);

	css.background = css.background or self:GetAttribute("background", nil);

	self:OnLoadComponentBeforeChild(parentElem, parentLayout, css);

	self:OnLoadChildrenComponent(parentElem, parentLayout, css);
	
	self:OnLoadComponentAfterChild(parentElem, parentLayout, css);
	
	-- call onload(self) function if any. 
	local onloadFunc = self:GetString("onload");
	if(onloadFunc and onloadFunc~="") then
		Elements.pe_script.BeginCode(self);
		local pFunc = commonlib.getfield(onloadFunc);
		if(type(pFunc) == "function") then
			pFunc(self);
		else
			LOG.std("", "warn", "mcml", "%s node's onload call back: %s is not a valid function.", self.name, onloadFunc)	
		end
		Elements.pe_script.EndCode(rootName, self, bindingContext, _parent, left, top, width, height,style, parentLayout);
	end
	self:UnapplyPreValues();
end

-- private: redirector
local function paintEventRedirectFunc(uiElement, painter)
	local page_element = uiElement:PageElement();
	if(page_element) then
		page_element:paintEvent(painter);
	end
end

-- enable self.paintEvent for this page element by creating a delegate UIElement and attach it to parentElem. 
-- only call this function once during LoadComponent.
function PageElement:EnableSelfPaint(parentElem)
	if(not self.control) then
		local _this = System.Windows.UIElement:new():init(parentElem);
		--_this._page_element = self;
		_this.paintEvent = paintEventRedirectFunc;
		self:SetControl(_this);
	else
		if(self.control:PageElement() == self) then
			self.control:SetParent(parentElem);
		else
			LOG.std("", "error", "mcml", "self paint can only be enabled when there is no control created for the page element");
		end
	end
end

-- virtual function: only called if EnableSelfPaint() is called during load component. 
function PageElement:paintEvent(painter)
end

-- this function is called automatically after page component is loaded and whenever the window resize. 
function PageElement:UpdateLayout(parentLayout)
	if(self:isHidden()) then 
		return 
	end
	if(no_parse_nodes[self.name]) then
		return;
	end
	local css = self:GetStyle();
	if(not css) then
		return;
	end
	local padding_left, padding_top, padding_right, padding_bottom = css:paddings();
	local margin_left, margin_top, margin_right, margin_bottom = css:margins();
	local availWidth, availHeight = parentLayout:GetPreferredSize();
	local maxWidth, maxHeight = parentLayout:GetMaxSize();
	local left, top;
	local width, height = self:GetAttribute("width"), self:GetAttribute("height");
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
		if(css.width) then
			if(availWidth<(css.width+margin_left+margin_right)) then
				parentLayout:NewLine();
			end
		end	
	else
		parentLayout:NewLine();
	end
	local myLayout = parentLayout:clone();
	myLayout:ResetUsedSize();

	local align = self:GetAttribute("align") or css["align"];
	local valign = self:GetAttribute("valign") or css["valign"];

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
		local left, top = self:GetAttribute("left"), self:GetAttribute("top");
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

	-- self.m_left, self.m_top = left+margin_left, top+margin_top;
	-----------------------------
	-- self and child layout recursively.
	-----------------------------

	if(not self:OnBeforeChildLayout(myLayout)) then
		self:UpdateChildLayout(myLayout);
	end
	
	local width, height = myLayout:GetUsedSize()
	local real_w = width + padding_right - left - margin_left;
	local real_h = height + padding_bottom - top - margin_top;
	myLayout:SetRealSize(real_w, real_h);
	width = width + padding_right + margin_right
	height = height + padding_bottom + margin_bottom
	if(css.width) then
		width = left + css.width + margin_left + margin_right;
	end	
	if(css.height) then
		height = top + css.height + margin_top + margin_bottom;
	end
	if(css["min-width"]) then
		local min_width = css["min-width"];
		if((width-left - margin_left-margin_right) < min_width) then
			width = left + min_width + margin_left + margin_right;
		end
	end
	if(css["min-height"]) then
		local min_height = css["min-height"];
		if((height-top - margin_top - margin_bottom) < min_height) then
			height = top + min_height + margin_top + margin_bottom;
		end
	end
	if(css["max-height"]) then
		local max_height = css["max-height"];
		if((height-top) > max_height) then
			height = top + max_height;
		end
	end
	myLayout:SetUsedSize(width, height);
	-- self.m_right, self.m_bottom = width-margin_right, height-margin_bottom;
	-- call virtual function for final size calculation. 
	self:OnAfterChildLayout(myLayout, left+margin_left, top+margin_top, width-margin_right, height-margin_bottom);
	width, height = myLayout:GetUsedSize();

	local size_width, size_height = width-left, height-top;
	local offset_x, offset_y = 0, 0;
	
	-- align at center. 
	if(align == "center") then
		offset_x = (maxWidth - size_width)/2
	elseif(align == "right") then
		offset_x = (maxWidth - size_width);
	end	
	
	if(valign == "center") then
		offset_y = (maxHeight - size_height)/2
	elseif(valign == "bottom") then
		offset_y = (maxHeight - size_height);
	end	
	if(offset_x~=0 or offset_y~=0) then
		-- offset and recalculate if there is special alignment. 
		myLayout = parentLayout:clone();
		local left, top = left+offset_x, top+offset_y;
		myLayout:SetPos(left, top);
		myLayout:SetSize(left+size_width, top+size_height);
		myLayout:OffsetPos(margin_left+padding_left, margin_top+padding_top);
		myLayout:IncWidth(-margin_right-padding_right);
		myLayout:IncHeight(-margin_bottom-padding_bottom);
		myLayout:ResetUsedSize();
		if(not self:OnBeforeChildLayout(myLayout)) then
			self:UpdateChildLayout(myLayout);
		end
		local right, bottom = left+size_width, top+size_height
		myLayout:SetUsedSize(right, bottom);
		self:OnAfterChildLayout(myLayout, left+margin_left, top+margin_top, right-margin_right, bottom-margin_bottom);
		width, height = myLayout:GetUsedSize();
	end

	if(bUseSpace) then
		parentLayout:AddObject(width-left, height-top);
		if(not css.float) then
			parentLayout:NewLine();
		end	
	end
end

-- virtual function: adjust control size according to preferred rect of layout. 
-- before child node layout is updated.
-- @return normally return nil. if return true, child nodes will be skipped. 
function PageElement:OnBeforeChildLayout(layout)
	
end

-- virtual function: 
-- after child node layout is updated
-- @param left, top, right, bottom: may be nil. it can also be preferred size of the control after child layout is calculated (margins are already removed). 
function PageElement:OnAfterChildLayout(layout, left, top, right, bottom)
	
end

function PageElement:UpdateChildLayout(layout)
	for childnode in self:next() do
		childnode:UpdateLayout(layout);
	end
end

-- virtual function: 
-- @param css: style
function PageElement:OnLoadComponentBeforeChild(parentElem, parentLayout, css)
	local tab_index = self:GetAttributeWithCode("tabindex", nil, true);
	if(tab_index) then
		tab_index = tonumber(tab_index);
	end
	if(tab_index and tab_index > 0) then
		self:SetTabIndex(tab_index);
		local page = self:GetPageCtrl();
		page:AddTabIndexNode(tab_index, self);
	end
end

function PageElement:OnLoadComponentAfterChild(parentElem, parentLayout, css)
--	if(css) then
--		local default_css = mcml:GetStyleItem(self.class_name);
--		css:Merge(default_css);
--	end
end

function PageElement:OnLoadChildrenComponent(parentElem, parentLayout, css)
	for childnode in self:next() do
		childnode:LoadComponent(parentElem, parentLayout, css);
	end
end

local reset_layout_attrs = {
	["display"] = true,
	["style"] = true,
};

-- set the value of an attribute of this node. This function is rarely used. 
function PageElement:SetAttribute(attrName, value, beForceResetLayout)
	self.attr = self.attr or {};
	if(self.attr[attrName] ~= value) then
		self.attr[attrName] = value;

		if(attrName == "style") then
			-- tricky code: since we will cache style table on the node, we need to delete the cached style when it is changed. 
			self.style = nil;
		end

		if(beForceResetLayout ~= false and reset_layout_attrs[attrName]) then
			self:resetLayout();
		end
	end
end

-- set the attribute if attribute is not code. 
function PageElement:SetAttributeIfNotCode(attrName, value)
	self.attr = self.attr or {};
	local old_value = self.attr[attrName];
	if(type(old_value) == "string") then
		local code = string_match(old_value, "^[<%%]%%(=.*)%%[%%>]$")
		if(code) then
			return;
		end
	end

	self:SetAttribute(attrName,value);
end

-- get the value of an attribute of this node as its original format (usually string)
function PageElement:GetAttribute(attrName,defaultValue)
	if(self.attr and self.attr[attrName]) then
		return self.attr[attrName];
	end
	return defaultValue;
end

local EscapeCharacters = {
	["&#10;"] = "\n",
	["&#13;"] = "\r",
	["&#32;"] = " ",
	["&#33;"] = "!",
	["&#34;"] = '"',
	["&quot;"] = '"',
}

local function processEscapeCharacters(str)
	for escapeChar, realChar in pairs(EscapeCharacters) do
		str = string.gsub(str, escapeChar, realChar);
	end
	return str;
end

-- get the value of an attribute of this node (usually string)
-- this differs from GetAttribute() in that the attribute string may contain embedded code block which may evaluates to a different string, table or even function. 
-- please note that only the first call of this method will evaluate embedded code block, subsequent calls simply return the previous evaluated result. 
-- in most cases the result is nil or string, but it can also be a table or function. 
-- @param bNoOverwrite: default to nil. if true, the code will be reevaluated the next time this is called, otherwise the evaluated value will be saved and returned the next time this is called. 
-- e.g. attrName='<%="string"+Eval("index")}%>' attrName1='<%={fieldname="table"}%>'
function PageElement:GetAttributeWithCode(attrName,defaultValue, bNoOverwrite)
	if(self.attr) then
		local value = self.attr[attrName];
		if(type(value) == "string") then
			local code = string_match(value, "^[<%%]%%(=.*)%%[%%>]$")
			if(code) then
				value = Elements.pe_script.DoPageCode(code, self:GetPageCtrl());
				if(type(value) == "string") then
					value = processEscapeCharacters(value);
				end
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

function PageElement:checkAttributes()
	if(self.attr) then
		for name, value in pairs(self.attr) do
			if(type(value) == "string") then
				local code = string_match(value, "^[<%%]%%(=.*)%%[%%>]$")
				if(code) then
					value = Elements.pe_script.DoPageCode(code, self:GetPageCtrl());
					self.attr[name] = value;
				end
			end
		end
	end
end


-- get an attribute as string
function PageElement:GetString(attrName,defaultValue)
	if(self.attr and self.attr[attrName]) then
		return self.attr[attrName];
	end
	return defaultValue;
end

-- get an attribute as number
function PageElement:GetNumber(attrName,defaultValue)
	if(self.attr and self.attr[attrName]) then
		return tonumber(self.attr[attrName]);
	end
	return defaultValue;
end

-- get an attribute as integer
function PageElement:GetInt(attrName, defaultValue)
	if(self.attr and self.attr[attrName]) then
		return math.floor(tonumber(self.attr[attrName]));
	end
	return defaultValue;
end


-- get an attribute as boolean
function PageElement:GetBool(attrName, defaultValue)
	if(self.attr and self.attr[attrName]) then
		local v = string_lower(tostring(self.attr[attrName]));
		if(v == "false") then
			return false
		elseif(v == "true") then
			return true
		end
	end
	return defaultValue;
end

-- get all pure text of only text child node
function PageElement:GetPureText()
	local nSize = #(self);
	local text = "";
	for i=1, nSize do
		node = self[i];
		if(node) then
			if(type(node) == "string") then
				text = text..node;
			elseif(node.name== "text" and type(node.value) == "string") then
				text = text..node.value;
			end
		end
	end
	return text;
end

-- get all inner text recursively (i.e. without tags) as string. 
function PageElement:GetInnerText()
	local node;
	local text = "";
	for i=1, #(self) do
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
function PageElement:SetInnerText(text)
	self[1] = text;
	commonlib.resize(self, 1);
end

-- get value: it is usually one of the editor tag, such as <input>
function PageElement:GetValue()
end

-- set value: it is usually one of the editor tag, such as <input>
function PageElement:SetValue(value)
end

-- get UI value: get the value on the UI object with current node
-- @param instName: the page instance name. 
function PageElement:GetUIValue(pageInstName)
end

-- set UI value: set the value on the UI object with current node
function PageElement:SetUIValue(pageInstName, value)
end


-- set UI enabled: set the enabled on the UI object with current node
function PageElement:SetUIEnabled(pageInstName, value)
end

-- get UI value: get the value on the UI object with current node
-- @param instName: the page instance name. 
function PageElement:GetUIBackground(pageInstName)
end

-- set UI value: set the value on the UI object with current node
function PageElement:SetUIBackground(pageInstName, value)
end

-- call a control method
-- @param instName: the page instance name. 
-- @param methodName: name of the method.
-- @return: the value from method is returned
function PageElement:CallMethod(pageInstName, methodName, ...)
	if(self[methodName]) then
		return self[methodName](self, pageInstName, ...);
	else
		LOG.warn("CallMethod (%s) on object %s is not supported\n", tostring(methodName), self.name)
	end
end

-- return true if the page node contains a method called methodName
function PageElement:HasMethod(pageInstName, methodName)
	if(self[methodName]) then
		return true;
	end
end

-- invoke a control method. this is same as CallMethod, except that pageInstName is ignored. 
-- @param methodName: name of the method.
-- @return: the value from method is returned
function PageElement:InvokeMethod(methodName, ...)
	if(self[methodName]) then
		return self[methodName](self, ...);
	else
		LOG.warn("InvokeMethod (%s) on object %s is not supported\n", tostring(methodName), self.name)
	end
end

function PageElement:SetObjId(id)
	self.uiobject_id = id;
end

function PageElement:SetControl(control)
	self.control = control;
	if(control) then
		control:setPageElement(self);
	end
end

-- get the control associated with this node. 
-- if self.uiobject_id is not nil, we will fetch it using this id, if self.control is not nil, it will be returned, otherwise we will use the unique path name to locate the control or uiobject by name. 
-- @param instName: the page instance name. if nil, we will ignore global control search in page. 
-- @return: It returns the ParaUIObject or CommonCtrl object depending on the type of the control found.
function PageElement:GetControl(pageName)
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
function PageElement:CalculateFont(css)
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
function PageElement:GetUIControl(pageName)
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
function PageElement:printParents()
	log(tostring(self.name).." is a child of ")
	if(self.parent == nil) then
		log("\n")
	else
		self.parent:printParents();
	end
end

function PageElement:printLayout(layout)
	if(layout) then
		local temp = {};
		local name, value
		for name, value in pairs(layout) do
			if(type(value) ~= "table") then
				temp[name] = value;
			end
		end
		echo(temp);
	end	
end

-- print this node to log file for debugging purposes. 
function PageElement:print()
	log("<"..tostring(self.name));
	if(self.attr) then
		local name, value
		for name, value in pairs(self.attr) do
			commonlib.log(" %s=\"%s\"", name, value);
		end
	end	
	local nChildSize = #(self);
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
function PageElement:SetCssStyle(attrName, value)
	if(not self.style) then
		self:CreateStyle();
	end

	if(self.style[attrName] ~= value) then
		self.style[attrName] = value;
		if(self.control) then
			self.control:ApplyCss(self.style);
		end
		if(StyleItem.isResetField(attrName)) then
			self:resetLayout();
		end
	end
end

-- get the ccs attribute of a given css style attribute value. 
function PageElement:GetCssStyle(attrName)
	if(type(self.style) == "table") then
		return self.style[attrName];
	end
end

-- update the css attribute.
-- this function is called when the texture attribute changed, such as "background", "background-color","background2", "background2-color", "background-image"
function PageElement:UpdateCssStyle()
	if(self.control) then
		self.control:ApplyCss(self.style);
	end
end

function PageElement:InvalidateStyle()
	self.style = nil;
end

-- get style item
function PageElement:GetStyle()
	return self.style;
end

-- apply any css classnames in class attribute
function PageElement:ApplyClasses()
	local pageStyle = self:GetPageStyle();
	if(pageStyle) then
		local style = self:GetStyle();
		-- apply name first such as "pe:button"
		pageStyle:ApplyToStyleItem(style, self.class_name or self.name);

		pageStyle:ApplyCssStyleToStyleItem(style, self);

		-- apply attribute class names
		if(self.attr and self.attr.class) then
			local class_names = self:GetAttributeWithCode("class", nil, true);
			if(class_names) then
				for class_name in class_names:gmatch("[^ ]+") do
					pageStyle:ApplyToStyleItem(style, class_name);
				end
			end
		end
	end
end

-- get the css style object if any. Style will only be evaluated once and saved to self.style as a table object, 
-- unless style attribute is changed by self:SetAttribute("style", value) method. 
-- order of style inheritance: base_baseStyle, baseStyle, style specified by attr.class.
-- @param baseStyle: nil or usually the default style with which the current node's style is merged.
-- @param base_baseStyle: this is optional. where to copy inheritable fields, usually from parent element's style object. 
-- @return: style table is a table of name value pairs. such as {color=string, href=string}
function PageElement:CreateStyle(baseStyle, base_baseStyle)
	local style = StyleItem:new():init(self:GetPageCtrl():GetStyle(), self);
	self.style = style;

	style:MergeInheritable(base_baseStyle);
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
function PageElement:AddChild(child, index)
	if(type(child)=="table") then
		local nCount = #(self) or 0;
		child.index = commonlib.insertArrayItem(self, index, child)
		child.parent = self;
	elseif(type(child)=="string") then	
		local nCount = #(self) or 0;
		commonlib.insertArrayItem(self, index, child)
	end	
	self:resetLayout();
end

-- Clear all child nodes
function PageElement:ClearAllChildren()
	self:DetachControls();
	commonlib.resize(self, 0);
end

function PageElement:DetachControls()
	if(self.control) then
		self.control:SetParent(nil);
	end
	for i=1, #self do
		local child = self[i];
		if(type(child) == "table") then
			child:DetachControls();
		end
	end
end

function PageElement:DeleteControls()
	if(self.control) then
		self.control:SetParent(nil);
		self.control = nil;
	end
	for i=1, #self do
		local child = self[i];
		if(type(child) == "table") then
			child:DeleteControls();
		end
	end
end

-- detach this node from its parent node. 
function PageElement:Detach()
	self:DetachControls();

	local parentNode = self.parent
	if(parentNode == nil) then
		return
	end
	local nSize = #(parentNode);
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
end

-- check whether this baseNode has a parent with the given name. It will search recursively for all ancesters. 
-- @param name: the parent name to search for. If nil, it will return parent regardless of its name. 
-- @return: the parent object is returned. 
function PageElement:GetParent(name)
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
function PageElement:GetRoot()
	local parent = self;
	while (parent.parent~=nil) do
		parent = parent.parent;
	end
	return parent;
end

-- Get the page control(PageCtrl) that loaded this mcml page. 
function PageElement:GetPageCtrl()
	return self:GetAttribute("page_ctrl") or self:GetParentAttribute("page_ctrl");
end	

-- get the page style object shared by all page elements.
function PageElement:GetPageStyle()
	local page = self:GetPageCtrl();
	if(page) then
		return page:GetStyle();
	end
end

-- search all parent with a given attribute name. It will search recursively for all ancesters.  
-- this function is usually used for getting the "request_url" field which is inserted by MCML web browser to the top level node. 
-- @param attrName: the parent field name to search for
-- @return: the nearest parent object field is returned. it may return, if no such parent is found. 
function PageElement:GetParentAttribute(attrName)
	local parent = self.parent;
	while (parent~=nil) do
		if(parent.GetAttribute and parent:GetAttribute(attrName)~=nil) then
			return parent:GetAttribute(attrName);
		end
		parent = parent.parent;
	end
end

-- get the url request of the mcml node if any. It will search for "request_url" attribtue field in the ancestor of this node. 
-- PageCtrl and BrowserWnd will automatically insert "request_url" attribtue field to the root MCML node before instantiate them. 
-- @return: nil or the request_url is returned. we can extract requery string parameters using regular expressions or using GetRequestParam
function PageElement:GetRequestURL()
	return self:GetParentAttribute("request_url") or self:GetAttribute("request_url");
end

-- get request url parameter by its name. for example if page url is "www.paraengine.com/user?id=10&time=20", then GetRequestParam("id") will be 10.
-- @return: nil or string value.
function PageElement:GetRequestParam(paramName)
	local request_url = self:GetRequestURL();
	return System.localserver.UrlHelper.url_getparams(request_url, paramName)
end

-- convert a url to absolute path using "request_url" if present
-- it will replace %NAME% with their values before processing next. 
-- @param url: it is any script, image or page url path which may be absolute, site root or relative path. 
--  relative to url path can not contain "/", anotherwise it is regarded as client side relative path. such as "Texture/whitedot.png"
-- @return: it always returns absolute path. however, if path cannot be resolved, the input is returned unchanged. 
function PageElement:GetAbsoluteURL(url)
	if(not url or url=="") then return url end
	
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
function PageElement:GetOwnerUserID()
	local profile = self:GetParent("pe:profile") or self;
	if(profile) then
		return profile:GetAttribute("uid");
	end
end

-- Get child count
function PageElement:GetChildCount()
	return #(self);
end

-- remove all child nodes and move them to an internal template node
function PageElement:MoveChildrenToTemplate()
	local templateNode;
	if(#self == 1) then
		templateNode = self[1];
	else
		-- use anonymous parent element if multiple nodes in the template 
		templateNode = PageElement:new(); 
		for child in self:next() do
			templateNode:AddChild(child);
		end
	end
	self.templateNode = templateNode;
	self:ClearAllChildren();
end

-- this may return nil if self:MoveChildrenToTemplate is never called. 
function PageElement:GetTemplateNode()
	return self.templateNode;
end

-- generate a less compare function according to a node field name. 
-- @param fieldName: the name of the field, such as "text", "name", etc
function PageElement.GenerateLessCFByField(fieldName)
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
--   One can also build a compare function by calling PageElement.GenerateLessCFByField(fieldName) or PageElement.GenerateGreaterCFByField(fieldName)
function PageElement.GenerateGreaterCFByField(fieldName)
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
function PageElement:SortChildren(compareFunc)
	compareFunc = compareFunc or PageElement.GenerateLessCFByField("name");
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
function PageElement:GetNodePath()
	local path = tostring(self.index);
	while (self.parent ~=nil) do
		path = tostring(self.parent.index).."/"..path;
		self = self.parent;
	end
	return path;
end

-- @param rootName: a name that uniquely identifies a UI instance of this object, usually the userid or app_key. The function will generate a sub control name by concartinating this rootname with relative baseNode path. 
function PageElement:GetInstanceName(rootName)
	return tostring(rootName)..self:GetNodePath();
end

-- get the first occurance of first level child node whose name is name
-- @param name: if can be the name of the node, or it can be a interger index. 
function PageElement:GetChild(name)
	if(type(name) == "number") then
		return self[name];
	else
		local nSize = #(self);
		local node;
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
function PageElement:GetChildWithAttribute(name, value)
	local nSize = #(self);
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
function PageElement:SearchChildByAttribute(name, value)
	local nSize = #(self);
	local i, node;
	for i=1, nSize do
		node = self[i];
		if(type(node)=="table") then
			if(value == node:GetAttributeWithCode(name, nil, true) or (node.buttonName and node.buttonName == value)) then
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
function PageElement:next(name)
	local nSize = #(self);
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
function PageElement:jquery(pattern, param1)
	local tagName = pattern and pattern:match("^<([^%s]*).*/>$") or pattern:match("^<([^%s]*)>.*</(%1)>$");
	--local tagName = pattern and pattern:match("^<([^%s/>]*)");
	if(tagName) then
		param1 = param1 or {name=tagName, attr={}};
		param1.name = param1.name or tagName;
		return mcml:createFromXmlNode(param1);
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
function PageElement:show()
	self:SetAttribute("display", nil);
end

-- hide this node. one may needs to refresh the page if page is already rendered
function PageElement:hide()
	self:SetAttribute("display", "none")
end

-- get/set inner text
-- @param v: if not nil, it will set inner text instead of get
-- return the inner text or empty string. 
function PageElement:text(v)
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
function PageElement:value(v)
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
function PageElement:GetAllChildWithNameIDClass(name, id, class, output)
	local nSize = #(self);
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
function PageElement:GetAllChildWithName(name, output)
	local nSize = #(self);
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
function PageElement:GetAllChildWithAttribute(attrName, attrValue, output)
	local nSize = #(self);
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

-- get code value in NPL code script. 
-- @param name: can be any name with commmar 
function PageElement:GetScriptValue(name)
	local pageScope = self:GetPageCtrl():GetPageScope();
	return commonlib.getfield(name, pageScope);
end

-- this function will apply self.pre_values to current page scope during rendering.
-- making it accessible to XPath and Eval function.  
function PageElement:ApplyPreValues()
	if(type(self.pre_values) == "table") then
		local pageScope = self:GetPageCtrl():GetPageScope();
		if(pageScope) then
			for name, value in pairs(self.pre_values) do
				pageScope[name] = value;
			end
		end
	end
end

-- pop page script 
function PageElement:UnapplyPreValues()
	if(type(self.pre_values) == "table") then
		local pageScope = self:GetPageCtrl():GetPageScope();
		if(pageScope) then
			for name, value in pairs(self.pre_values) do
				pageScope[name] = nil;
			end
		end
	end
end

-- apply a given pre value to this node, so that when the node is rendered, the name, value pairs will be
-- written to the current page scope. Not all mcml node support pre values. it is most often used by databinding template node. 
function PageElement:SetPreValue(name, value)
	self.pre_values = self.pre_values or {};
	self.pre_values[name] = value;
end

-- get a prevalue by name. this function is usually called on data binded mcml node 
-- @param name: name of the pre value
-- @param bSearchParent: if true, it will search parent node recursively until name is found or root node is reached. 
function PageElement:GetPreValue(name, bSearchParent)
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
function PageElement:TranslateMe(langTable, transName)
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
		local nSize = #(self);
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
function PageElement:ProcessVariables()
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

function PageElement:ReplaceVariables(variables)
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
		local nSize = #(self);
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

-- fire a given page event
-- @param handlerScript: the call back script function name or function itself.
--  the script function will be called with function(...) end
-- @param ... : event parameter
function PageElement:DoPageEvent(handlerScript, ...)
	local pageEnv, result;
	if(self) then
		-- get the page env table where the inline script function is defined, it may be nil if there is no page control or there is no inline script function. 
		local pageCtrl = self:GetPageCtrl();
		if(pageCtrl) then
			pageEnv = pageCtrl._PAGESCRIPT
		end
		
		Elements.pe_script.BeginCode(self);
	end
	if(type(handlerScript) == "string") then
		if(string.find(handlerScript, "http://")) then
			-- TODO: post values using http post. 
		else
			-- first search function in page script environment and then search in global environment. 
			local pFunc;
			if(pageEnv) then
				pFunc = commonlib.getfield(handlerScript, pageEnv);
			end
			if(type(pFunc) ~= "function") then
				pFunc = commonlib.getfield(handlerScript);
			end	
			if(type(pFunc) == "function") then
				result = pFunc(...);
			else
				log("warning: MCML page event call back "..handlerScript.." is not a valid function. \n")	
			end
		end	
	elseif(type(handlerScript) == "function") then
		--result = pFunc(...);
		result = handlerScript(...);
	end
	if(self) then
		Elements.pe_script.EndCode();
	end
	return result;
end

function PageElement:isHidden() 
	local parent = self;
	while (parent ~= nil) do
		if(parent:GetAttribute("display") == "none") then
			return true;
		end
		local css = parent:GetStyle();
		if(css and css["display"] == "none") then
			return true;
		end
		parent = parent.parent;
	end
	return false;
end

function PageElement:resetLayout()
	local page = self:GetPageCtrl();
	if(page and page.layout) then
		local window = page:GetWindow();
		if(window and window:testAttribute("WA_WState_Created")) then
			page.layout:invalidate();
		end
	end
end

function PageElement:IsClip()
	local parent = self;
	while(parent) do
		local control = self.control;
		if(control and control:IsClip()) then
			return true;
		end
		parent = parent.parent;
	end
end

-- clip region. 
function PageElement:ClipRegion()
	local parent = self;
	while(parent) do
		local control = parent.control;
		if(control and control:IsClip()) then
			local clip_rect = control:ClipRegion();
			if(clip_rect) then
				clip_rect:setX(control:x() + clip_rect:x() - self:x());
				clip_rect:setY(control:y() + clip_rect:y() - self:y());
				return clip_rect;
			end
		end
		parent = parent.parent;
	end
end

function PageElement:SetFocus()
	if(self.control) then
		self.control:setFocus("TabFocusReason");
	end
end

function PageElement:TabLostFocus()
	return true;
end

function PageElement:Focused()
	return self:GetPageCtrl():FocusNode() == self;
end

function PageElement:FocusInEvent()
	if(not self:Focused()) then
		self:GetPageCtrl():SetFocusNode(self);
	end
end

function PageElement:FocusOutEvent()
	if(self:Focused()) then
		self:GetPageCtrl():SetFocusNode();
	end
end

function PageElement:NextTabNode(node)
	if(self:TabIndex() == 0 and not self:Focused()) then
		return self;
	end

	local size = #self;
	if(size == 0 or (node and node.index == size)) then
		if(self.parent) then
			return self.parent:NextTabNode(self);
		else
			return;
		end
	else
		if(node) then
			node = self[node.index + 1];
		else
			node = self[1];
		end
		return node:NextTabNode();
	end
end

--[[
Title: Document
Author(s): LiXizhi
Date: 2015/4/27
Desc: The Document object represents the entire MCML document and can be used to access all elements in a page.
use the lib:
------------------------------------------------------------
NPL.load("(gl)script/ide/System/Windows/mcml/DOM.lua");
local Document = commonlib.gettable("System.Windows.mcml.Document");
local elem = Document:new();
------------------------------------------------------------
]]
local mcml = commonlib.gettable("System.Windows.mcml");

local Document = commonlib.inherit(commonlib.gettable("System.Core.ToolBase"), commonlib.createtable("System.Windows.mcml.Document", {
	-- Returns the domain name for the current document
	domain = nil,
	-- Returns the date and time a document was last modified
	lastModified = nil,
	-- Returns the title of the current document
	title = nil,
	-- Returns the URL of the current document
	URL = nil,
	-- gives direct access to the root mcml object, usually <pe:mcml> 
	body = nil,
	-- text Buffer
	textbuffer_ = nil,
}));

Document:Property("Name", "Document");

-- constructor
function Document:ctor()
end

-- Opens a stream to collect the output from any document.write() or document.writeln() methods
function Document:open()
end

-- Closes an output stream opened with the document.open() method, and displays the collected data
function Document:close()
end

-- Writes HTML expressions or JavaScript code to a document 
-- tricky code: we can call document:write("hello") or document.write("hello"). they are the same. 
-- @param self: string or self.
-- @param code: string
function Document.write(self, code) 
	if(type(self) ~= "table") then
		code = self;
		self = document;
		if(self == nil) then
			self = Document:new(o);
		end
	end
	if(code) then
		if(not self.textbuffer_) then
			self.textbuffer_ = tostring(code);
		else
			self.textbuffer_ = self.textbuffer_..code;
		end
	end
end

-- private: never call this function from MCML script yourself. This function is called automatically.
-- flush all previous write operations to create a node 
-- @return: return nil or the root MCML node containing MCML node contents from previous write functions. The root node name is always "p"
function Document:flush() 
	if(self.textbuffer_~=nil) then
		self.textbuffer_ = "<p>"..self.textbuffer_.."</p>";
		--self.textbuffer_ = ParaMisc.EncodingConvert("", "HTML", self.textbuffer_);
		local xmlRoot = ParaXML.LuaXML_ParseString(self.textbuffer_);
		if(type(xmlRoot)=="table" and table.getn(xmlRoot)>0) then
			local xmlRoot = mcml:createFromXmlNode(xmlRoot);
			return xmlRoot[1];
		end
	end	
end

-- return the page control. document.GetPageCtrl() or document:GetPageCtrl() both works. 
function Document.GetPageCtrl(self)
	if(self == nil) then
		self = document;
	end
	if(self and self.body) then
		return self.body:GetPageCtrl();
	end
end


```