# 课前拓展课
<desc>本系列课程包含建造、动画、编程等基础知识，帮助同学们掌握Paracraft创作技巧，感受Paracraft的魅力。<br/>

搭建: ★<br/>

动画: ★<br/>

编程: ★★
</desc>
<code>pre_tuozhanke</code>




## 课前拓展课
<div class="ppt_cover_div">
        <div class="cover_left">
            <div class="cover_title">
                <div class="cover_title_left"></div>
                <div class="cover_title_right">
                    <div class="cover_title_text">课前拓展课</div>
                  
                    <div class="cover_title_text2"></div>
                </div>
            </div>
           <div class="cover_desc">
           本系列课程作为课前的拓展练习，里面有包含建造、编程等基础知识，通过几个项目的简单练习，让同学们对于帕拉卡工具的使用更加熟练，开启创作之旅。

            </div>
            <div>课程难度：</div>
            <difficult type_name="搭建" value="1"/>
            <difficult type_name="动画" value="1"/>
            <difficult type_name="编程" value="2"/> 
        </div>
        <div class="cover_right">
            <img class="ppt_cover" src="https://api.keepwork.com/ts-storage/siteFiles/26301/raw#14.png"/> 
            
        </div>
    </div>



## 项目一 街景建筑
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
 <div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：跟着视频指引，搭建创作出街景建筑</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo"
        video_url="https://api.keepwork.com/ts-storage/siteFiles/26294/raw#拓展第一课.webm;https://api.keepwork.com/ts-storage/siteFiles/26341/raw#拓展第一课.mp4"/>
    </pe:container>
     <input type="button" onclick="CreateWorld" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>

</pe:if>




## 项目二 安全上学
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：跟着视频指引，编程实现控制角色前进、转向的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo"
        video_url="https://api.keepwork.com/ts-storage/siteFiles/26295/raw#拓展第二课.webm;https://api.keepwork.com/ts-storage/siteFiles/24816/raw#167099746220201安全上学9918（原版）.mp4"/>
    </pe:container>
     <input type="button" onclick="CreateWorld" worldname="安全上学" fork_project_id="9918" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>

</pe:if>




## 项目三 保护环境
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
 <div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：跟着视频指引，编程实现种植树木的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26296/raw#拓展第三课.webm;https://api.keepwork.com/ts-storage/siteFiles/24817/raw#02保护环境9852（原版）.mp4"/>
    </pe:container>
     <input type="button" onclick="CreateWorld" worldname="保护环境" fork_project_id="9852" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>

</pe:if>



## 项目四 驯龙高手
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
  <div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：跟着视频指引，编程实现角色与翼龙之间的交互效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo"
        video_url="https://api.keepwork.com/ts-storage/siteFiles/26297/raw#拓展第四课.webm;https://api.keepwork.com/ts-storage/siteFiles/24134/raw#166788546249407驯龙高手10797（原版）.mp4"/>
    </pe:container>
     <input type="button" onclick="CreateWorld" worldname="驯龙高手" fork_project_id="10797" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>

</pe:if>




