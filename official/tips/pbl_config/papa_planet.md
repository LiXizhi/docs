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
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26611/raw#灌篮高手(上)_压缩后.webm;https://api.keepwork.com/ts-storage/siteFiles/26610/raw#灌篮高手(上)_压缩后.mp4"/>
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
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/27326/raw#灌篮高手2(下).webm;https://api.keepwork.com/ts-storage/siteFiles/27327/raw#灌篮高手2(下).mp4"/>
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
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：搭建画笔模型，编程实现画笔涂色、抬笔的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26173/raw#绘画小能手(上).webm;https://api.keepwork.com/ts-storage/siteFiles/26343/raw#绘画小能手(上)_01.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="绘画小能手" fork_project_id="1226213" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/7-1绘画小能手（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.搭建画笔模型<br/>
            2.编程实现画笔涂色功能<br/>
            3.编程实现抬笔的效果<br/>
            4.添加更多颜色的画笔<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.搭建画笔模型<br/>
            2.编程实现画笔涂色功能<br/>
            3.编程实现抬笔的效果<br/>
            4.保存、上传自己的家园<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26046/raw#48节元宇宙课程封面8一绘画大师.png"/> 
</div>
</pe:if>


## 第15课 绘画小能手（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现画笔放缩功能，以及橡皮擦、画笔加粗和喷涂的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26175/raw#绘画小能手（下）.webm;https://api.keepwork.com/ts-storage/siteFiles/26342/raw#绘画小能手(下)_02.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="绘画小能手" fork_project_id="1226213" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/7-2绘画小能手（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.实现画笔放缩功能<br/>
            2.实现橡皮擦的效果<br/>
            3.实现画笔加粗效果<br/>
            4.实现喷涂效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.实现画笔放缩功能<br/>
            2.添加橡皮擦、画笔加粗和喷涂的效果<br/>
            3.分享你的世界ID到班级群<br/>
            4.通过ID参观别人的家园<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26046/raw#48节元宇宙课程封面8一绘画大师.png"/> 
</div>
</pe:if>



## 第16课 我的艺术画廊（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习放置相册添加图片，以及添加对相册的讲解与迎宾角色</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26304/raw#我的艺术画廊（上）.webm;https://api.keepwork.com/ts-storage/siteFiles/26306/raw#我的艺术画廊(上)_720.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="艺术画廊" fork_project_id="1242976" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/8-1我的艺术画廊（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.放置相册并添加图片<br/>
            2.实现相册的讲解<br/>
            3.添加迎宾角色<br/>
         
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.放置相册并添加图片<br/>
            2.实现相册的讲解<br/>
            3.添加迎宾角色<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26300/raw#48节元宇宙课程封面9一我的艺术画廊.png"/> 
</div>
</pe:if>


## 第17课 我的艺术画廊（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习放置雕塑并添加旋转效果，添加图片并编程控制图片的显示和隐藏</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26305/raw#我的艺术画廊（中）.webm;https://api.keepwork.com/ts-storage/siteFiles/26307/raw#我的艺术画廊(中)_720.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="艺术画廊" fork_project_id="1242976" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/8-2我的艺术画廊（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.放置雕塑模型并添加旋转效果<br/>
            2.电影方块中添加图层并显示图片<br/>
            3.编程控制图片的显示和隐藏<br/>

            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.放置雕塑模型并添加旋转效果<br/>
            2.电影方块中添加图层并显示图片<br/>
            3.编程控制图片的显示和隐藏<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26300/raw#48节元宇宙课程封面9一我的艺术画廊.png"/> 
</div>
</pe:if>


## 第18课 我的艺术画廊（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习推镜头、移镜头和环绕镜头，制作动画作品</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26480/raw#我的艺术画廊（下） 2.webm;https://api.keepwork.com/ts-storage/siteFiles/26479/raw#我的艺术画廊（下）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="艺术画廊" fork_project_id="1242976" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/8-3我的艺术画廊（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.制作推镜头和移镜头<br/>
            2.制作环绕镜头<br/>
            3.添加背景音乐，制作镜头切换效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.制作推镜头和移镜头<br/>
            3.制作环绕镜头<br/>
            4.添加背景音乐，制作镜头切换效果<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26300/raw#48节元宇宙课程封面9一我的艺术画廊.png"/> 
</div>
</pe:if>



## 第19课 钢琴漫游编程世界（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：搭建琴键模型，并实现点击琴键播放音符与按键播放音符的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28539/raw#钢琴漫游编程世界（上）-压缩后.webm;https://api.keepwork.com/ts-storage/siteFiles/26612/raw#钢琴漫游编程世界（上）_压缩后.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="钢琴（上）" fork_project_id="1253465" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/9-1钢琴漫游编程世界（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.搭建琴键模型并补全钢琴<br/>
            2.实现点击琴键播放音符效果<br/>
            3.实现按键播放音符效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.搭建琴键模型并补全钢琴<br/>
            3.实现点击琴键播放音符效果<br/>
            4.实现按键播放音符效果<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26616/raw#48节元宇宙课程封面10一钢琴漫游编程世界.png"/> 
</div>
</pe:if>



## 第20课 钢琴漫游编程世界（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习克隆指令，并通过角色属性区分克隆角色，实现按键播放音符的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28538/raw#钢琴漫游编程世界（中）-压缩后.webm;https://api.keepwork.com/ts-storage/siteFiles/26613/raw#钢琴漫游编程世界（中）_压缩后.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="钢琴（中）" fork_project_id="1252319" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/9-2钢琴漫游编程世界（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
           <b>学习目标：</b><br/>
            1.使用克隆补全缺少的琴键<br/>
            2.通过设置角色属性区分克隆出的角色<br/>
            3.实现按键播放音符的功能<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.使用克隆补全缺少的琴键<br/>
            3.通过设置角色属性区分克隆出的角色<br/>
            4.实现按键播放音符的功能<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26616/raw#48节元宇宙课程封面10一钢琴漫游编程世界.png"/> 
</div>
</pe:if>


## 第21课 钢琴漫游编程世界（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习自动播放音符的原理，并实现广播传递数据播放音符的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26917/raw#钢琴漫游编程世界（下）.webm;https://api.keepwork.com/ts-storage/siteFiles/26916/raw#钢琴漫游编程世界（下）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="钢琴（下）" fork_project_id="1335710" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/9-3钢琴漫游编程世界（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
         <b>学习目标：</b><br/>
            1.学习自动播放音符的原理<br/>
            2.了解字符串、获取单个字符<br/>
            3.广播传递数据播放音符<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
          <b>作品要求：</b><br/>
            1.学习自动播放音符的原理<br/>
            2.了解字符串、获取单个字符<br/>
            3.广播传递数据播放音符<br/>
            4.分享你的世界ID到班级群<br/>
            5.通过ID参观别人的家园<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26616/raw#48节元宇宙课程封面10一钢琴漫游编程世界.png"/> 
</div>
</pe:if>



## 第22课 太阳系漫游指南（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：了解太阳系，并编程实现模拟太阳、地球、月球自转与公转的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28556/raw#太阳系的奥秘（上）719.webm;https://api.keepwork.com/ts-storage/siteFiles/26973/raw#太阳系的奥秘（上）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="太阳系（上）" fork_project_id="1340583" value="创作作品" class="CreateWorldBt"/>
    
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/10-1太阳系漫游指南（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.了解太阳系<br/>
            2.太阳、地球的自转和公转<br/>
            3.月球的自转和公转<br/>
            4.为太阳添加图片介绍<br/>
           
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.太阳、地球的自转和公转<br/>
            2.月球的自转和公转<br/>
            3.为太阳添加图片介绍<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26979/raw#48节元宇宙课程封面11一太阳系漫游指南.png"/> 
</div>
</pe:if>


## 第23课 太阳系漫游指南（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：继续创作，编程模拟实现太阳系八大行星的自转与公转效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/26976/raw#太阳系的奥秘（下）.webm;https://api.keepwork.com/ts-storage/siteFiles/26975/raw#太阳系的奥秘（下）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="太阳系（下）" fork_project_id="1340626" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/10-2太阳系漫游指南（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.调整八大行星的位置<br/>
            2.实现八大行星的自转效果<br/>
            3.实现八大行星的公转效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.调整八大行星的位置<br/>
            2.实现八大行星的自转效果<br/>
            3.实现八大行星的公转效果<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/26979/raw#48节元宇宙课程封面11一太阳系漫游指南.png"/> 
</div>
</pe:if>


## 第24课 棋妙未来（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：了解CAD方块，学会使用CAD方块设计棋子</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/27197/raw#棋妙未来（上）.webm;https://api.keepwork.com/ts-storage/siteFiles/27196/raw#棋妙未来（上）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="棋妙未来（上）" fork_project_id="1376347" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/11-1棋妙未来（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.了解CAD和CAD方块<br/>
            2.使用CAD方块制作棋子模型<br/>
            3.CAD方块的拓展使用<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.使用CAD方块制作棋子模型<br/>
            2.CAD方块的拓展使用<br/>
            3.保存并上传自己的家园作品<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/27202/raw#48节元宇宙课程封面12一棋妙未来.png"/> 
</div>
</pe:if>



## 第25课 棋妙未来（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学会编程自动搭建出整个棋盘</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28555/raw#棋妙未来（下）719.webm;https://api.keepwork.com/ts-storage/siteFiles/27198/raw#棋妙未来（下）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="棋妙未来（下）" fork_project_id="1391537" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/11-2棋妙未来（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.如何搭建整个棋盘<br/>
            2.使用代码创建棋盘一条边<br/>
            3.使用代码生成整个棋盘<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.点击创作作品<br/>
            2.如何搭建整个棋盘<br/>
            3.使用代码创建棋盘一条边<br/>
            4.使用代码生成整个棋盘<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/27202/raw#48节元宇宙课程封面12一棋妙未来.png"/> 
</div>
</pe:if>



## 第26课 扫地机器人（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：使用CAD制作机器人模型，并编程实现机器人移动、转向和开关机功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/27448/raw#扫地机器人（上）.webm;https://api.keepwork.com/ts-storage/siteFiles/27445/raw#扫地机器人（上）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="扫地机器人" fork_project_id="1391528" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/12-1扫地机器人（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.知道扫地机器人的基本外观、功能和工作原理<br/>
            2.能够解释“前进”指令中不同参数对实现效果的影响<br/>
            3.能够运用“提问 回答”指令+条件分支，实现作品的交互及流程控制<br/>
            4.能够说出全局变量的作用范围，运用标志变量控制程序的运行<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.使用CAD方块创作机器人模型<br/>
            2.为机器人增加移动和转向功能<br/>
            3.为机器人增加开关机功能<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/27459/raw#48节元宇宙课程封面12一扫地机器人.png"/> 
</div>
</pe:if>



## 第27课 扫地机器人（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现垃圾随机出现，以及扫地机器人清理和计数的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/27451/raw#扫地机器人（中）.webm;https://api.keepwork.com/ts-storage/siteFiles/27446/raw#扫地机器人（中）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="扫地机器人" fork_project_id="1391528" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/12-2扫地机器人（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.知道日常生活中的四种不同垃圾类别<br/>
            2.能够熟练使用“瞬移”指令及“随机数”指令，设置角色的随机位置<br/>
            3.能够识别电影方块中不同演员的编号，并运用“设置角色的电影角色”指令切换角色<br/>
            4.能够说出“隐藏”指令和“删除此克隆角色”指令的区别<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.实现场地中随机出现垃圾的效果<br/>
            2.切换垃圾的造型<br/>
            3.实现清理和计数的效果<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/27459/raw#48节元宇宙课程封面12一扫地机器人.png"/> 
</div>
</pe:if>




## 第28课 扫地机器人（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程为扫地机器人添加调整速度和定时开关机的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/27450/raw#扫地机器人（下）.webm;https://api.keepwork.com/ts-storage/siteFiles/27447/raw#扫地机器人（下）.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="扫地机器人" fork_project_id="1391528" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/12-3扫地机器人（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够举例说明生活中的“速度”，知道速度快慢的衡量标准<br/>
            2.熟练使用分支结构，完成作品功能的设计<br/>
            3.能够说出函数的作用，通过定义函数简化程序<br/>
            4.能够发现计时中的数学规律，并通过程序中的运算符表示<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.分析如何添加调整速度功能<br/>
            2.实现调整速度的效果<br/>
            3.增加定时关机功能<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/27459/raw#48节元宇宙课程封面12一扫地机器人.png"/> 
</div>
</pe:if>




## 第29课 循线机器人（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：理解循线机器人工作原理，设计规划循迹路线，编程实现循线功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28833/raw#《巡线机器人》上.webm;https://api.keepwork.com/ts-storage/siteFiles/28832/raw#《巡线机器人》上.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="循线机器人" fork_project_id="1414302" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/13-1循线机器人（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.理解循迹机器人的基本概念和工作原理<br/>
            2.能够设计和规划循迹路线，考虑不同环境下的循迹限制和挑战<br/>
            3.能够搭建循迹机器人模型，正确设置传感器<br/>
            4.能够分析程序逻辑，并编写程序使机器人识别并按照预定路径行驶<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.设计循线路径<br/>
            2.搭建模型，设置传感器<br/>
            3.编程实现循线功能<br/>
            4.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>




## 第30课 循线机器人（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：创造送餐环境，并编程实现点餐和送餐的功能</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/30502/raw#循线机器人（中）压缩.webm;https://api.keepwork.com/ts-storage/siteFiles/30501/raw#循线机器人（中）压缩.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="循线机器人" fork_project_id="1414302" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/13-2循线机器人（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.理解送餐机器人的基本工作原理<br/>
            2.能够合理放置餐厅的桌椅装饰<br/>
            3.理解并且指令的逻辑并能使用它简化代码<br/>
            4.能够分析程序，画出流程图并根据流程图完成功能<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.装饰场地，创造送餐环境<br/>
            2.编程实现点餐和送餐功能<br/>
            3.编程实现送餐后返回功能<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第31课 循线机器人（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现最短路径循线送餐效果，为食物增加不同造型，并简化重复代码</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/28836/raw#《巡线机器人》下.webm;https://api.keepwork.com/ts-storage/siteFiles/28837/raw#《巡线机器人》下.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="循线机器人" fork_project_id="1414302" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/13-3循线机器人（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.了解最短路径规划并在送餐时实现这个效果<br/>
            2.能够列举出旋转和旋转到指令的不同之处<br/>
            3.能够熟练运用表和_的第_项指令，存储、获取数据<br/>
            4.能够从重复代码中找出规律，并总结优化<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.实现最短路径循线送餐效果<br/>
            2.为食物增加不同造型并在代码中切换<br/>
            3.观察规律，简化重复代码<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第32课 智能小管家（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：使用CAD方块编程设计风扇模型，并将它放置到场景中</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29035/raw#智能小管家（上）.webm;https://api.keepwork.com/ts-storage/siteFiles/29034/raw#32课长视频.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="智能小管家" fork_project_id="1440258" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/14-1智能小管家（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够说出CAD方块中布尔运算的具体效果<br/>
            2.在建模时，能够根据图片或模型分析使用的图形指令<br/>
            3.能够使用相交和相减运算，得出想要的图形<br/>
            4.能够使用循环变量和复制方法，快速绘制模型<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.使用CAD方块制作扇叶的粗糙模型<br/>
            2.制作单片扇叶模型<br/>
            3.完成风扇模型并放置到场景中<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第33课 智能小管家（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：了解骨骼方块的作用，学会制作骨骼动画，并保存为ParaX模型</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29037/raw#智能小管家（中）.webm;https://api.keepwork.com/ts-storage/siteFiles/29036/raw#33课长视频.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="智能小管家" fork_project_id="1440258" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/14-2智能小管家（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.了解骨骼方块的作用以及如何使用<br/>
            2.能够在电影方块中通过关键帧制作骨骼动画<br/>
            3.能够给制作的骨骼动画设置动作编号<br/>
            4.能够将骨骼动画保存为ParaX模型并在代码方块中使用<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.了解骨骼方块并为模型添加骨骼<br/>
            2.制作跳舞和待机的骨骼动画<br/>
            3.将骨骼动画保存为ParaX模型<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第34课 智能小管家（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程添加功能选项，并实现管家控制风扇开关和切换灯光氛围的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29170/raw#智能小管家（下）.webm;https://api.keepwork.com/ts-storage/siteFiles/29169/raw#34课长视频.mp4"/>
    </pe:container>
     <input type="button" onclick="CreateWorld" worldname="智能小管家" fork_project_id="1440258" value="创作作品" class="CreateWorldBt"/> 
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/14-3智能小管家（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够通过观察分析，发现风扇旋转方向的规律<br/>
            2.能够运用【设置光源颜色】指令改变发光方块的光源颜色<br/>
            3.能够理解RGB调色的原理和方法，以及预测简单色彩混合的结果<br/>
            4.能够利用【颜色】指令，简化编写代码的过程<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.添加功能选项<br/>
            2.实现管家控制风扇开关效果<br/>
            3.切换灯光氛围<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第35课 无人机编队秀（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：设计完成无人机模型，并实现螺旋桨旋转和编队飞行的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29172/raw#无人机上.webm;https://api.keepwork.com/ts-storage/siteFiles/29171/raw#无人机上·长视频_x264.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="无人机编队秀" fork_project_id="1463571" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/15-1无人机编队秀（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够通过观察分析，找到镜像指令的参考面<br/>
            2.能够给骨骼添加属性，并且在代码方块中调用<br/>
            3.能够在模型中使用高级骨骼方块，从而减少骨骼方块的数量<br/>
            4.能够解释变量是如何传递给不同的克隆体<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.完成无人机模型<br/>
            2.实现螺旋桨旋转效果<br/>
            3.实现编队飞行效果<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第36课 无人机编队秀（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现无人机沿圆形轨迹飞行，及画出飞行轨迹的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29320/raw#《无人机编队秀》中.webm;https://api.keepwork.com/ts-storage/siteFiles/29319/raw#无人机编队秀中.mp4"/>
    </pe:container>
   <input type="button" onclick="CreateWorld" worldname="无人机编队秀" fork_project_id="1463571" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/15-2无人机编队秀（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够通过观察分析，得出实现效果所需的指令<br/>
            2.能够对解决方法进行优化，实现更好的效果<br/>
            3.能够举一反三，画出更加复杂的组合图形<br/>
            4.能够说出通用的正多边形画法，只要知道边数和边长，就能画出来<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.实现无人机沿圆形轨迹飞行效果<br/>
            2.画出无人机飞行轨迹<br/>
            3.实现两种图形组合的效果<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第37课 无人机编队秀（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现矩阵编队飞行及组合图形秀的效果，呈现无人机表演秀</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29322/raw#《无人机编队秀》下.webm;https://api.keepwork.com/ts-storage/siteFiles/29321/raw#无人机编队秀下.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="无人机编队秀" fork_project_id="1463571" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/15-3无人机编队秀（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够熟练运用循环嵌套方法<br/>
            2.能够复制代码方块，调整参数，快速实现效果<br/>
            3.能够使用【广播】指令控制代码方块中代码执行的顺序<br/>
            4.能够使用录制功能录制视频并分享<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.实现矩形编队飞行的效果<br/>
            2.实现组合图形秀效果<br/>
            3.展示完整的无人机表演秀<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第38课 矿山探测器（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：学习搭建轨道的技巧，以及编写命令实现自动化矿车</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29874/raw#上 Batch-1.webm;https://api.keepwork.com/ts-storage/siteFiles/29873/raw#上_batch.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="矿山探测器" fork_project_id="1459410" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/16-1矿山探测器（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够使用铁轨方块铺设轨道，以及掌握上坡轨道搭建技巧<br/>
            2.能够了解能量传递，使用能量方块给动力铁轨提供能量<br/>
            3.能够使用命令方块，编写命令实现自动化矿车<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.完成缺失铁轨的铺设<br/>
            2.铺设上坡轨道，利用能量方块给动力铁轨充能<br/>
            3.设置宠物为自动转向属性<br/>
            4.借助命令方块实现自动化矿车<br/>
  
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>




## 第39课 矿山探测器（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编写程序自动铺设铁轨，以及利用克隆指令实现捡金币的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29876/raw#中 Batch-1.webm;https://api.keepwork.com/ts-storage/siteFiles/29875/raw#中_batch.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="矿山探测器" fork_project_id="1459410" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/16-2矿山探测器（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.通过观察分析缺失铁轨的位置关系，编写程序自动铺设铁轨<br/>
            2.了解探测铁轨，借助其散发的能量激活电灯和电影方块<br/>
            3.通过随机克隆与距离侦测，实现了捡金币的效果<br/>
        
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.完成独木桥铁轨自动铺设<br/>
            2.利用探测铁轨激活电灯和电影方块<br/>
            3.利用克隆实现捡金币的效果<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>




## 第40课 矿山探测器（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：设计程序实现音符播放效果，以及制作终点效果和关键帧动画</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/29877/raw#下 Batch-1.webm;https://api.keepwork.com/ts-storage/siteFiles/29880/raw#下_batch.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="矿山探测器" fork_project_id="1459410" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/16-3矿山探测器（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.通过系统分析，设计程序实现音符播放的效果<br/>
            2.能够使用命令方块实现终点自动化矿车效果<br/>
            3.能够结合所学电影方块相关知识，制作关键帧动画<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.完成音符播放效果<br/>
            2.实现终点效果设置<br/>
            3.制作探测指南动画<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>




## 第41课 激光感应器（上）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程完成飞船的飞行控制、太空垃圾随机出现并往返运动的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/30261/raw#激光上.webm;https://api.keepwork.com/ts-storage/siteFiles/30260/raw#激光上.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="激光感应器" fork_project_id="1463835" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/17-1激光感应器（上）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够向他人讲述太空垃圾的来源，包括发射任务、废弃物等<br/>
            2.能够说出位移指令中每个参数的作用并能够熟练调整参数，实现不同方向和距离的移动<br/>
            3.熟练应用随机指令，能够设置正确且合理的随机区间<br/>
       
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.完成飞船的飞行控制效果<br/>
            2.完成太空垃圾随机出现的效果<br/>
            3.实现垃圾在通道内往返运动的效果<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>



## 第42课 激光感应器（中）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：添加发射按钮，并利用克隆实现发射激光、重置激光状态的效果</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/30263/raw#激光中.webm;https://api.keepwork.com/ts-storage/siteFiles/30262/raw#激光中.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="激光感应器" fork_project_id="1463835" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/17-2激光感应器（中）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.能够通过观察、获取坐标，为角色设置合理的坐标和大小<br/>
            2.能够列举出【固定到_的骨骼_上】指令两种用法的不同之处，知道如何解除绑定<br/>
            3.能够说出【重复执行_直到_】指令的作用以及如何使用<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.添加发射按钮<br/>
            2.利用克隆实现发射激光的效果<br/>
            3.重置激光状态<br/>
            4.保存并上传自己的家园作品<br/>
            5.分享你的世界ID到班级群<br/>
            </div>
    </step>
</div>

<div class="right">
    <img class="step_img" src="https://api.keepwork.com/ts-storage/siteFiles/24608/raw#yyz06.png"/> 
</div>
</pe:if>




## 第43课 激光感应器（下）
<pe:if condition='<%=IsSupportVideo and IsSupportVideo()%>'>
	<div style="color: #000000;margin-top: 10px;margin-left: 3px;">学习目标：编程实现清除太空垃圾的效果，以及添加视觉效果并设置好观看视角</div>
    <pe:container name="pptvideo_container" class="VideoContainer">
        <pe:nplbrowser name="nplbrowser_pptvideo" video_url="https://api.keepwork.com/ts-storage/siteFiles/30265/raw#激光下.webm;https://api.keepwork.com/ts-storage/siteFiles/30264/raw#激光下.mp4"/>
    </pe:container>
    <input type="button" onclick="CreateWorld" worldname="激光感应器" fork_project_id="1463835" value="创作作品" class="CreateWorldBt"/>
</pe:if>


<pe:if condition='<%=not IsSupportVideo or not IsSupportVideo()%>'>
<div class="left">
    <step value="1">
        <action type="link" href="https://keepwork.com/lesson9527/codeLessons/children/C1/17-3激光感应器（下）" buseToken="true" value="点我开始学习"/>
        <div class="step_str">
          <b>学习目标：</b><br/>
            1.了解隐形阻挡方块的特点并且能在程序中使用<br/>
            2.能够列举出两种模式的不同之处并且在程序中切换<br/>
            3.能够通过代码控制界面中按钮的显示和隐藏<br/>
            4.能够说出【循环播放电影频道】指令的作用以及各项参数的效果<br/>
            </div>
    </step>
    <step value="2">
        <action type="loadworld" value="点我创作作品"/>
        <div class="step_str">
           <b>作品要求：</b><br/>
            1.清除太空垃圾<br/>
            2.添加各类宠物<br/>
            3.添加视觉效果<br/>
            4.设置观看视角<br/>
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


