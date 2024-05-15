<!-- 与学有优教对接，复制以下内容，修改appId和secret -->
<script src="https://jjjc.zxxs.moe.edu.cn/app/jaydentech/jaydentech.sdk.1.0.0.js"></script>
<script>
 function addScript(url) {
    var script = document.createElement("script");
    script.setAttribute("type", "text/javascript");
    script.setAttribute("src", url);
    document.getElementsByTagName("head")[0].appendChild(script);
  }
  addScript("https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js");
</script>
<script>
  var appUtil;
  document.addEventListener("UniAppJSBridgeReady", function () {
    appUtil = uni;
    getUserInfo()
  });
  function getUserInfo() {
    appUtil
      .getUserData({
        appId: 1647568,
      })
      .then((res) => {
        return res.data.encryptStr;
      })
      .then((data) => {
        $.ajax({
          type: "post",
          url: "http://api.keepwork.com/core/v0/crypto/sm4/decrypt",
          data: JSON.stringify({
            key: "6otsLdAbWjWUDpae",
            text: data,
          }),
          dataType: "json",
          contentType: "application/json",
          success: function (data) {
            const userInfo = data;
            const node = document.getElementsByClassName("c0035")[0];
            if (userInfo && userInfo.name) {
              node.innerText = `你好，${userInfo.name}`;
            }
          },
        });
      });
  }
    
  let box = document.querySelector('body') // 监听对象
  let startTime = '' // 触摸开始时间
  let startDistanceX = '' // 触摸开始X轴位置
  let startDistanceY = '' // 触摸开始Y轴位置
        let endTime = '' // 触摸结束时间
        let endDistanceX = '' // 触摸结束X轴位置
        let endDistanceY = '' // 触摸结束Y轴位置
        let moveTime = '' // 触摸时间
        let moveDistanceX = '' // 触摸移动X轴距离
        let moveDistanceY = '' // 触摸移动Y轴距离
        box.addEventListener("touchstart", (e) => {
            startTime = new Date().getTime()
            startDistanceX = e.touches[0].screenX
            startDistanceY = e.touches[0].screenY
        })
        box.addEventListener("touchend", (e) => {
            endTime = new Date().getTime()
            endDistanceX = e.changedTouches[0].screenX
            endDistanceY = e.changedTouches[0].screenY
            moveTime = endTime - startTime
            moveDistanceX = startDistanceX - endDistanceX
            moveDistanceY = startDistanceY - endDistanceY
            console.log(moveDistanceX, moveDistanceY)
            // 判断滑动距离超过40 且 时间小于500毫秒
            if ((Math.abs(moveDistanceX) > 40 || Math.abs(moveDistanceY) > 40) && moveTime < 500) {
                // 判断X轴移动的距离是否大于Y轴移动的距离
                if (Math.abs(moveDistanceX) > Math.abs(moveDistanceY)) {
                    // 左右
                    console.log(moveDistanceX > 0 ? '左' : '右')
   appUtil.goBack({});
                } else {
                    // 上下
                    console.log(moveDistanceY > 0 ? '上' : '下')
                }
            }
        })
</script>
<script>
  function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split("=");
      if (pair[0] == variable) {
        return pair[1];
      }
    }
    return false;
  }
  var topHeight = getQueryVariable("topHeight");
  if (topHeight) {
    const head = document.getElementsByClassName("index-page-container")[0];
                       
    head.style.marginTop = topHeight + "px";
    const div = document.createElement("div");
    div.style.height = topHeight + "px";
    div.style.width = "100%";
    div.style.position = "fixed";
    div.style = `
    height: 30px;
    width: 100%;
    background-color: #ffffff;
    position: fixed;
    top: 0px;
    left:0px;
    z-index: 999;                                
    `
    document.body.insertBefore(div,document.body.firstChild);
  }
</script>
<script src="https://cdn.jsdelivr.net/npm/vconsole@3.11.0/dist/vconsole.min.js"></script>
  <script>
    
   function getConsole() {
    // VConsole 默认会挂载到 `window.VConsole` 上
    var vConsole = new window.VConsole();
    // 接下来即可照常使用 `console` 等方法
    console.log("Hello world");
  }
  </script>

## 虚拟校园介绍

在虚拟世界中，给每个学校分配一个3D虚拟校园。老师、学生、家长可以登录虚拟校园，并在其中创造、探索、学习。本质上，是一个由本校师生共同搭建的虚拟现实的数字孪生3D世界，更是一个学校虚拟现实与人工智能教育实践平台和成果发布和展示平台。

- 增值服务: 学生（家长）可报名参加帕拉卡课后服务长期班。

### 虚拟校园介绍视频

```@TencentVideo
styleID: 0
tencentVideo:
  vid: 'r3162mdx0yp'

```

<details >
  <summary>点击查看视频字幕介绍</summary>
  
这里是我们的产品矩阵，包括刚刚看到的3D动画编程课，数字美术课程，
还有AI机器人设计和制造平台，创意空间3D虚拟校园，玩学课堂游戏化编程教育课，以及帕拉卡家校互动小程序。
今天后面会重点介绍3D虚拟校园。
我们希望将中国二十一万所中小学和大学全部都搬到互联网上，由学校发起搭建3D虚拟校园，
为中国青少年创造一个学习和实践人工智能的舞台。
在虚拟校园的最中央，有代表这个城市或者学校的地标性建筑，可以展示个人作品，展示AI虚拟机器人，陈列优秀的学生作品。
同学们可以在虚拟世界中交流，可以举办比赛，有星光大道，还有学习和测评。
我们希望把它打造成一个学生在家自主学习的社区，不仅可以创造和分享每个人的作品，
还是每个学生展现自己作品的舞台，另外还可以参加全国性的比赛。
我们以佛山为例，我们和当地的教育局达成合作，将广东省佛山市上百所的学校搬到了互联网上。
当孩子们登录到Paracraft时，同一个学校的孩子会出现在同一个3D校园中。
像这样，这里边有**创造**，**探索**，**学习**，还可以有**每周实战**，**参加比赛**等等内容。
每个孩子都有自己的名字，下面是他所属的学校。
在3D校园的周围，一环，二环和三环都是学生们的个人家园或者是个人作品。
不断地向远处走，可以看到越来越多的本校师生的作品。
向上或者向下其他方向走的时候，还可以看到其他城市或者其他地域学生们的作品。
在虚拟世界中，人挨着人，学校挨着学校，作品挨着作品。
我们认为这种新的虚拟校园将成为新时代的学校展示名片。
所有的学校都是本校的学生创建的，它会成为全国师生了解学校，了解学校文化的重要媒介，让孩子们获得成就感。
下面我们来看一段虚拟校园的宣导片，全部是实景拍摄。
Paracraft还为学校和培训机构提供了全面的服务与支持，包括在线教学管理平台，
在这里学校的老师可以管理课程，新建班级，管理学生的作品，还提供了多维度的测评报告。
此外我们还提供了大量的针对不同年龄段孩子们的课程，包含老师用的教案和在课堂上在线使用的PPT。
我们还为合作的学校提供师资培训，这里看到的是我们和中国科学院先进技术研究院实验小学开展的3D动画编程课。
目前有上百家学校和机构在使用Paracraft开展学校内的课程。
有的学校老师接受培训之后可以自主上课，而我们也提供在线课程，学校老师只需要在教室里播放我们的视频就可以了。

</details>


### 管理功能
学生可以每人一块虚拟土地，管理者可后台管理虚拟土地权限。 

![](https://api.keepwork.com/ts-storage/siteFiles/24790/raw#1670402667972image.png)

### 用户案例1: 肇庆市第一中学 

<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/15734/raw" type="video/mp4" />
  你的浏览器不支持播放
</video>

### 学校案例: 小学

- [丰南实验学校（小学）](https://www.bilibili.com/video/BV1zs411m71G)
- [荔园小学](https://www.bilibili.com/video/BV1xv411i7zw)

### 学校案例: 大学

- [华中农业大学](https://www.bilibili.com/video/BV1XW4y1E7JF)
- [北京科技大学](https://www.bilibili.com/video/BV1RB4y1j79H)


## 更多用户作品


<iframe src="https://keepwork.com/explore?tab=pickedProjects" id='iframe1' width='100%' height="800p"> </iframe>
<script>
var iframeWindow = document.getElementById("iframe1").contentWindow; 
setTimeout(function(){
   const node = iframeWindow.document.getElementsByClassName('index-page-header')[0];
   node.style.display = 'none';
   const node2 = iframeWindow.document.getElementsByClassName('exploration-page-theme')[0];
   node2.style.display = 'none';
   const node4 = iframeWindow.document.getElementsByClassName('home-page-footer')[0];
   node4.style.display = 'none';
   const node3 = iframeWindow.document.getElementsByClassName('perfect-common-footer')[0];
   node3.style.display = 'none';
  }, 3000)
</script>