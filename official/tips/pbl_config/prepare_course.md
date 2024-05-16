# 课前准备课
<desc>本节课帮助大家快速熟悉下Paracraft的编程工具和环境，了解一些基础操作和技巧。<br/>

搭建: ★<br/>

动画: ★<br/>

编程: ★
</desc>
<code>prepare_course</code>

## 课前准备课
<pe:if condition='<%=IsSupportVideo()%>'>
 <div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：了解帕拉卡创作工具及基础操作</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/24841/raw#课前准备课(1).webm"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p1" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.了解帕拉卡创作工具<br/>
            2.新建、加载、保存、分享世界<br/>
            3.认识基础方块<br/>
            4.控制主角的移动<br/>    
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
            <b>作品要求：</b><br/>
            1.新建世界，放置基础方块<br/>
            2.自行探索，创作更加丰富的作品<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24607/raw#yyz05.png"/> 
</div>
</pe:if>