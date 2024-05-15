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
  function getUserInfo() {
    appUtil
      .getUserData({
        appId: 1651567,
      })
      .then((res) => {
        return res.data.encryptStr;
      })
      .then((data) => {
        $.ajax({
          type: "post",
          url: "http://api.keepwork.com/core/v0/crypto/sm4/decrypt",
          data: JSON.stringify({
            key: "hFpVK3Krn4NNkk1U",
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


## 虚拟课程与创作工具介绍
帕拉卡Paracraft是一款面向老师和学生的3D虚拟现实课件创作工具。
- 帕拉卡是完全中国**自主原创**和开源的工具，对标unity等专业3D引擎。
- 内置3D建模、3D动画、沉浸式编程与调试、CAD建模、虚拟仿真、GIT云端版本控制、多人协作等功能。
- 可以研发从**青少年个人编程项目**到百万行代码的**大型商业化APP**。


<details style="background-color:white">
  <summary>点击观看介绍视频</summary><p>

<video width="100%" controls controlslist="nodownload nofullscreen noremoteplayback" disablePictureInPicture>
  <source src="https://api.keepwork.com/ts-storage/siteFiles/21029/raw#16294741581302minsParacraftIntroSmall.mp4" type="video/mp4" />
  你的浏览器不支持播放
</video>

![](https://api.keepwork.com/ts-storage/siteFiles/22940/raw#1663759622462image.png)
  
帕拉卡paracraft集探索、学习、创造于一身，为老师和学生提供了统一的虚拟现实课程的集成开发工具，极大的降低了学习成本，让人人可以创造出属于自己的3D世界。通过3D动画，虚拟现实，元宇宙等技术可以让互联网中的教育更加智慧。我们的工具适合研发面向幼儿园、小学、中学、职业教育、高等教育的**全学科**的虚拟现实课程。

</p></details>

## Web 3D 互动课件演示
> 请根据指引**点击**或**拖动**蓝色圆圈，右下角有**全屏**按钮。

<div class="aspect-ratio">
  <iframe src="https://macros.keepwork.com/?projectId=1110679&capture=[1,2,3,4,5,6]"   frameborder="0" allowfullscreen="true"></iframe>
</div>

下载帕拉卡，人人都可以开发和发布上面的虚拟现实课件。

### 更多Web 3D 互动课程

| 《S1 入门建造》项目式课程 （16）|
|-----|
| **项目1：五子棋** | 
| [1 创建棋盘和棋子](/official/open/lessons/s1/1_1) 、[2 开启多人联机](/official/open/lessons/s1/1_2) 、[3 自动生成棋盘](/official/open/lessons/s1/1_3) |
| **项目2：飞翔的小鸟** |
| [1 创建场景与角色模型](/official/open/lessons/s1/2_1) 、[2 碰撞检测](/official/open/lessons/s1/2_2) 、[3 提示的设计](/official/open/lessons/s1/2_3) |
| **项目3：我是小画家** |
| [1 创建画板与画笔](/official/open/lessons/s1/3_1) 、[2 给画笔编程](/official/open/lessons/s1/3_2) 、[3 给橡皮擦编程](/official/open/lessons/s1/3_3) |
| **项目4：超级农场** |
| [1 创建苹果与胡萝卜](/official/open/lessons/s1/4_1) 、[2 添加青蛙与小狗](/official/open/lessons/s1/4_2) 、[3 编程实现浇水效果](/official/open/lessons/s1/4_3) 、[4 会动的小兔子](/official/open/lessons/s1/4_4)|

| 《S2 入门动画》 项目式课程|
|-----|
| **项目1：我的云画室** | 
| [1 制作可点击的相册](/official/open/lessons/s2/1_1) 、[2 对图片进行解说](/official/open/lessons/s2/1_2) 、[3 给画室添加雕塑、背景音乐](/official/open/lessons/s2/1_3)、[4 制作一段动画，参观画室](/official/open/lessons/s2/1_4) |
| **项目2：超级农场2.0** |
| [1 编程实现播放稻草人的骨骼动画](/official/open/lessons/s2/2_1) 、[2 搭建虫子模型，为其制作骨骼动画](/official/open/lessons/s2/2_2) 、[3 搭建小鸡模型，为其制作骨骼动画](/official/open/lessons/s2/2_3)、[4 制作介绍农场的摄影机动画](/official/open/lessons/s2/2_4) |
| **项目3：密室逃脱** |
| [1 设计一个可以打开和关闭的密室门](/official/open/lessons/s2/3_1) 、[2 拖动机关打开密室门](/official/open/lessons/s2/3_2) 、[3 将物品摆放到正确位置打开密室门](/official/open/lessons/s2/3_3)、[4 制作密室的提示动画和开场动画](/official/open/lessons/s2/3_4) |