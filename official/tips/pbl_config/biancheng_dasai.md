# 编程大赛，巅峰挑战

<code>bc_ds</code>


## 编程大赛，巅峰挑战
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">编程大赛，巅峰挑战</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29176/raw#挑战视频-1.webm;https://api.keepwork.com/ts-storage/siteFiles/29175/raw#挑战视频-压缩.mp4"/>
    </pe:container>
        <input type="button" onclick="CreateWorld" worldname="编程大赛" fork_project_id="1463254" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/1_1宠物跟随" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.添加宠物小狗<br/>
            2.编写程序控制宠物移动<br/>
            3.编写程序实现宠物跟随效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.添加一个会跟随的宠物<br/>
            3.保存并上传自己的家园作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25100/raw#宠物跟随.png"/> 
</div>
</pe:if>