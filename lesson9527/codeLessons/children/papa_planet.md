# 帕帕星球成长日记
<desc>本系列课程以项目式学习为导向，帮助孩子掌握3D世界创作中的搭建、动画、编程技巧，真正理解项目从0到1的制作过程，理解项目迭代的逻辑。<br/>

搭建: ★★<br/>

动画: ★★<br/>

编程: ★★★
</desc>
<code>papa_course</code>


## 帕帕星球成长日记
<div class="ppt_cover_div">
        <div class="cover_left">
            <div class="cover_title">
                <div class="cover_title_left"></div>
                <div class="cover_title_right">
                    <div class="cover_title_text">帕帕星球成长日记</div>
                  
                    <div class="cover_title_text2"></div>
                </div>
            </div>
           <div class="cover_desc">
           本系列课程以项目式学习为导向，帮助孩子掌握3D世界创作中的搭建、动画、编程技巧，真正理解项目从0到1的制作过程，理解项目迭代的逻辑。在选题上，项目以孩子们的兴趣为出发点，同时注重联系实际，让孩子既能循序渐进地学习编程知识，又能拓展视野学习其他学科知识，比如天文知识、音乐常识等。综合培养孩子的空间感知能力、知识迁移能力、问题拆解能力与项目整体设计思维等。

            </div>
            <div>课程难度：</div>
            <difficult type_name="搭建" value="2"/>
            <difficult type_name="动画" value="2"/>
            <difficult type_name="编程" value="3"/> 
        </div>
        <div class="cover_right">
            <img class="ppt_cover" src=""/> 
            
        </div>
    </div>


## 第1课 宠物跟随
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程设计一个自动跟随的宠物</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25131/raw#长期元宇宙-宠物跟随(1).webm;https://api.keepwork.com/ts-storage/siteFiles/25132/raw#长期元宇宙-宠物跟随(1).mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld"  value="创作作品" class="CreateWorldBt"/>
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


## 第2课 让宠物说话
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程让宠物说话</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25146/raw#长期-2宠物会说话.webm;https://api.keepwork.com/ts-storage/siteFiles/25147/raw#长期-2宠物会说话.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld"  value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/1_2让宠物说话" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.学会看流程图<br/>
            2.掌握条件语句与比较运算符的使用<br/>
            3.让宠物说话<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.打开上节课的世界<br/>
            2.让你的宠物说话<br/>
            3.保存并上传自己的家园作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25149/raw#2-宠物说话.png"/> 
</div>
</pe:if>



## 第3课 制作机关门
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：设计制作机关门，编程控制开和关</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25452/raw#制作机关门-test03.webm;https://api.keepwork.com/ts-storage/siteFiles/25453/raw#制作机关门-test03.mp4"/>
    </pe:container>

     <input type="button" onclick="CreateWorld" worldname="门" fork_project_id="1190145" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/2-1制作机关门" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.制作门的bmax模型<br/>
            2.编写程序控制控制门的开和关<br/>
            3.为门设计一个打开门的机关<br/>
           
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.设计制作一个机关门<br/>
            3.保存并上传自己的家园作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25206/raw#制作机关门.png"/> 
</div>
</pe:if>


## 第4课 自动感应门
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：优化门的程序，添加自动感应的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25662/raw#4-自动感应门_test04.webm;https://api.keepwork.com/ts-storage/siteFiles/25663/raw#4-自动感应门_test04.mp4"/>
    </pe:container>

   <input type="button" onclick="CreateWorld" worldname="门" fork_project_id="1190145" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/2-2自动感应门" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.修复程序bug，编程限制门远离门框<br/>
            2.编程实现门自动复位<br/>
            3.编程实现自动感应开门<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.打开上节课的世界<br/>
            2.修复开关门的程序，增加自动感应的功能<br/>
            3.保存并上传自己的家园作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25206/raw#制作机关门.png"/> 
</div>
</pe:if>


## 第5课 一起来游泳（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：制作游泳池，编程控制演员游泳</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25389/raw#一起来游泳（上）_test05.webm;https://api.keepwork.com/ts-storage/siteFiles/25390/raw#一起来游泳（上）_test05.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="游泳池" fork_project_id="1160156" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/3-1一起来游泳（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.为泳池添加水<br/>
            2.编程让角色往前游动<br/>
            3.编程实现角色来回游动效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.搭建并美化自己的泳池<br/>
            3.编写程序让角色在泳池里游泳<br/>
            4.保存并上传自己的作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25207/raw#一起来游泳.png"/> 
</div>
</pe:if>



## 第6课 一起来游泳（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：认识电影方块，并学习制作关键帧动画</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25509/raw#一起来游泳(中）_test01.webm;https://api.keepwork.com/ts-storage/siteFiles/25510/raw#一起来游泳(中）_test01.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="游泳池" fork_project_id="1160156" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/3-2一起来游泳（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.认识电影方块<br/>
            2.学习制作关键帧动画<br/>

            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.打开上节课的世界<br/>
            2.给泳池拍摄一段介绍动画<br/>
            3.保存并上传自己的作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25207/raw#一起来游泳.png"/> 
</div>
</pe:if>



## 第7课 一起来游泳（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：添加字幕，录制并分享动画作品</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25511/raw#一起来游泳(下)_test03.webm;https://api.keepwork.com/ts-storage/siteFiles/25512/raw#一起来游泳(下)_test02.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="游泳池" fork_project_id="1160156" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/3-3一起来游泳（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.学习给动画添加字幕<br/>
            2.录制并分享动画作品<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.打开上节课的世界<br/>
            2.添加字幕并录制动画作品<br/>
            3.保存并上传自己的作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25207/raw#一起来游泳.png"/> 
</div>
</pe:if>



## 第8课 跑步大比拼（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程控制运动员向前跑，并添加跑步倒计时的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25767/raw#跑步大比拼(上)_test02.webm;https://api.keepwork.com/ts-storage/siteFiles/25768/raw#跑步大比拼(上)_test02.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="田径场" fork_project_id="1161829" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/4-1跑步大比拼（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.编程控制运动员向前跑步<br/>
            2.编程添加跑步倒计时的功能<br/>
            3.复制添加更多的运动员<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.添加运动员<br/>
            2.编程实现运动员跑步的效果<br/>
            3.保存并上传自己的作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25208/raw#跑步大比拼.png"/> 
</div>
</pe:if>


## 第9课 跑步大比拼（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：为运动员设置随机跑步速度，并添加终点判定的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25769/raw#跑步大比拼(下)_test01.webm;https://api.keepwork.com/ts-storage/siteFiles/25770/raw#跑步大比拼(下)_test01.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="田径场" fork_project_id="1161829" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/4-2跑步大比拼（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.为运动员设置随机的跑步速度<br/>
            2.编程添加终点判定<br/>
            3.设置好观察视角<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.给运动员设置随机的跑步速度<br/>
            2.编程添加终点判定<br/>
            3.保存并上传自己的作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25208/raw#跑步大比拼.png"/> 
</div>
</pe:if>



## 第10课 足球小子（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：设计足球模型，编程实现对踢足球的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25850/raw#足球小子(上)_test02.webm;https://api.keepwork.com/ts-storage/siteFiles/25851/raw#足球小子(上)_test02.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="足球场" fork_project_id="1162186" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/5-1足球小子（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.使用sphere命令搭建足球<br/>
            2.添加小猫与小猴两个球员<br/>
            3.编程实现对踢足球的效果<br/>
            
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.使用sphere命令搭建足球<br/>
            3.编程实现对踢足球的效果<br/>
            4.保存并上传自己的作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25856/raw#足球小子6-一足球小子.png"/> 
</div>
</pe:if>


## 第11课 足球小子（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：添加裁判，并编程实现判断胜负的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/25852/raw#足球小子(下)_test01.webm;https://api.keepwork.com/ts-storage/siteFiles/25853/raw#足球小子(下)_test01.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="足球场" fork_project_id="1162186" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/5-2足球小子（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.添加裁判<br/>
            2.编程实现系统判断胜负<br/>
            3.编程实现裁判员判断胜负<br/>
          
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.添加裁判<br/>
            3.编程实现判断胜负的效果<br/>
            4.保存并上传自己的作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/25856/raw#足球小子6-一足球小子.png"/> 
</div>
</pe:if>


## 第12课 灌篮高手（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现篮球跳动、发球及控制篮球左右移动的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26042/raw#灌篮高手(上).webm;https://api.keepwork.com/ts-storage/siteFiles/26043/raw#灌篮高手(上)_1.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="篮球场" fork_project_id="1181657" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/6-1灌篮高手（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.编程控制篮球在原地上下跳动<br/>
            2.编程实现按键发球的功能<br/>
            3.编程控制篮球左右移动<br/>

            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.编程控制篮球在原地上下跳动<br/>
            2.编程实现按键发球的功能<br/>
            3.编程控制篮球左右移动<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26045/raw#48节元宇宙课程封面7-一灌篮高手.png"/> 
</div>
</pe:if>



## 第13课 灌篮高手（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：认识物理半径和高度，编程实现篮球碰撞检测与重新开始的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26051/raw#灌篮高手(下).webm;https://api.keepwork.com/ts-storage/siteFiles/26052/raw#灌篮高手(下)_1.mp4"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="篮球场" fork_project_id="1181657"  value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/6-2灌篮高手（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.编程检测是否碰到篮筐<br/>
            2.设置篮筐物理半径和高度<br/>
            3.编程检测是否碰到玻璃板以及重新开始的功能<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.编程检测是否碰到篮筐<br/>
            2.设置篮筐物理半径和高度<br/>
            3.编程检测是否碰到玻璃板以及重新开始的功能<br/>
            4.保存并上传自己的作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26045/raw#48节元宇宙课程封面7-一灌篮高手.png"/> 
</div>
</pe:if>

## 第14课 绘画小能手（上） 
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p2" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.如何放置方块<br/>
            2.学习如何搭建家具<br/>
            3.作品的保存与分享<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.新建一个世界<br/>
            2.搭建自己的元宇宙家园<br/>
            3.保存、上传自己的家园<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26046/raw#48节元宇宙课程封面8一绘画大师.png"/> 
</div>
</pe:if>


## 第15课 绘画小能手（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p3" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.学习商城资源的使用<br/>
            2.ggs多人联机<br/>
            3.参观世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.使用模型装饰自己的元宇宙家园<br/>
            2.为家园世界开启多人联机模式<br/>
            3.分享你的世界ID到班级群<br/>
            4.通过ID参观别人的家园<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26046/raw#48节元宇宙课程封面8一绘画大师.png"/> 
</div>
</pe:if>



## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p5" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.农田搭建<br/>
            2.添加活动模型<br/>
            3.添加电影角色<br/>
            4.调整角色属性<br/>
            5.编程实现洒水效果<br/>
           
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.在世界中开垦出合适的农田<br/>
            2.在农田上种植农作物<br/>
            3.编程为农田实现自动灌溉的效果<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24604/raw#yyz02.png"/> 
</div>
</pe:if>


## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>


## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 暂未开放，敬请期待 
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p2" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.如何放置方块<br/>
            2.学习如何搭建家具<br/>
            3.作品的保存与分享<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.新建一个世界<br/>
            2.搭建自己的元宇宙家园<br/>
            3.保存、上传自己的家园<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24606/raw#yyz04.png"/> 
</div>
</pe:if>


## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p3" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.学习商城资源的使用<br/>
            2.ggs多人联机<br/>
            3.参观世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.使用模型装饰自己的元宇宙家园<br/>
            2.为家园世界开启多人联机模式<br/>
            3.分享你的世界ID到班级群<br/>
            4.通过ID参观别人的家园<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24605/raw#yyz03.png"/> 
</div>
</pe:if>



## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p5" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.农田搭建<br/>
            2.添加活动模型<br/>
            3.添加电影角色<br/>
            4.调整角色属性<br/>
            5.编程实现洒水效果<br/>
           
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.在世界中开垦出合适的农田<br/>
            2.在农田上种植农作物<br/>
            3.编程为农田实现自动灌溉的效果<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24604/raw#yyz02.png"/> 
</div>
</pe:if>


## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>


## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 暂未开放，敬请期待
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/storage/v0/siteFiles/12015/raw#1586909581895session20.webm"/>
    </pe:container>

    <input type="button" onclick="CreateWorld" worldname="" fork_project_id="" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/official/open/lessons/experience/second/p6" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.从资源库添加活动模型<br/>
            2.复制活动模型<br/>
            3.设置活动模型自动转向属性<br/>
            4.探索外围世界<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计一个萌宠乐园<br/>
            2.添加各类宠物<br/>
            3.设置宠物为自动转向属性<br/>
            4.复制更多自己喜欢的宠物<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>
