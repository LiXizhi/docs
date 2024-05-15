<script>
const GetQueryString = (key, decode) => {
  var value = ""; 
  var qs = location.search.length > 0 ? location.search.substring(1) : "";
  var items = qs.length ? qs.split('&') : [];
  for (var i = 0; i < items.length; i++) {
    var item = items[i].split('=');
    var name = decodeURIComponent(item[0]);
    if (name == key) {
      value = decode ? decodeURIComponent(item[1]) : item[1];
      break;
    }
  }
  return value;
};

const GetSystem = () => {
  if (window.paracraft_platform) return window.paracraft_platform;

  const platform = GetQueryString("platform", true);
  if (platform != "") return platform; 
  
  const { userAgent } = navigator;

  if (userAgent.match('Macintosh')) {
    return 'macos';
  }
  if (userAgent.match('Windows')) {
    return 'windows';
  }
  if (userAgent.match('Android')) {
    return 'android';
  }
  if (userAgent.match('iPhone')) {
    return 'iPhone';
  }
  if (userAgent.match('iPad')) {
    return 'iPad';
  }
  return 'unknown';
};
  
window.paracraft_platform = GetSystem();

  
allMsg = {};

window.NPL = {
  activate: function(filename, msg){
    if (GetSystem() === 'iPhone' || GetSystem() === 'macos') {
      const params = { filename, msg };
      params.msg = JSON.stringify(msg);

      if (window.webkit &&
        window.webkit.messageHandlers &&
        window.webkit.messageHandlers.activate &&
        window.webkit.messageHandlers.activate.postMessage) {
        window.webkit.messageHandlers.activate.postMessage(params);
      }
    } else if (GetSystem() === 'windows') {
      if (window.chrome &&
        window.chrome.webview &&
        window.chrome.webview.postMessage) {
        const params = { filename, msg };
        window.chrome.webview.postMessage(JSON.stringify(params))
        return
      }
      const params = { filename, msg };
      window.location.href = 'paracraft://sendMsg?' + JSON.stringify(params);
    } else if (GetSystem() === 'emscripten' && window.NPL.postMessage) {
      window.NPL.postMessage({ filename, msg });
    } else if (GetSystem() === 'android') {
      msg = JSON.stringify(msg);
      android.nplActivate(filename, msg);
    }
  },
  this: function(callback, params){
    if (params && params.filename) {
      allMsg[params.filename] = callback;
    }
  },
  receive: function(filename, msg){
    if (allMsg[filename]) {
      var msgJson = JSON.parse(msg) || {};
      allMsg[filename](msgJson);
    }
  },
};
  
if ((!window.chrome || !window.chrome.webview) && !window.android && !window.webkit) {
  window.addEventListener("message", function (event) {
    const msg = event.data;
    if (!msg.is_paracraft_message) return;
    const cmd = msg.cmd;
    if (cmd == "load") {
      if (msg.platform) window.paracraft_platform = msg.platform;
      // 回一个确定消息
      event.source.postMessage(msg, "*");

      window.NPL.postMessage = function (msg) {
        msg.is_paracraft_message = true;
        msg.cmd = "PostMessage";
        event.source.postMessage(msg, "*");
      }
    }
    else if (cmd == "PostMessage") {
      window.NPL.receive(msg.filename, msg.msg);
    }
  });
}
</script>  

<style>
.fullscreen {
  position: fixed;
  top: 0;left: 0;bottom: 0;right: 0;
  overflow: auto;
  z-index: 10;
  background-color:#e3e3e4;
  }
</style>

<div class="fullscreen">
  <div style="margin-top:0px;margin-left:0px">
    <video id="myPlayer" style="width:100%;height:100%;object-fit:fill"
           controls controlslist="nodownload nofullscreen noremoteplayback"
           autoplay 
           playsinline 
           disablePictureInPicture>
    </video>
  </div>
  <div id="video_url" />
</div>

<script>
/* Desc: This file is used for old PPT page in paracraft. It is only used when webview2 is available.
  Example:
https://keepwork.com/official/open/apps/video?video_url=https://api.keepwork.com/ts-storage/siteFiles/26256/raw#1681717764392physics_demo_small.mp4
  
NPL.activate("video.page", {cmd="pause"})
NPL.activate("video.page", {cmd="play"})
*/
  
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const video_url = urlParams.get('video_url')
document.getElementById("myPlayer").src = video_url;
const userId = urlParams.get('userId')
const code = urlParams.get('code')
const courseIndex = urlParams.get('courseIndex')
var duration;
const courseIdentity = code + "-" + courseIndex

function generateUUID() {
  let d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
    d += performance.now(); // use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = (d + Math.random()*16)%16 | 0;
    d = Math.floor(d/16);
    return (c==='x' ? r : (r&0x3|0x8)).toString(16);
  });
}
  
function videoAllFinishRequest({ userId, courseIdentity, status }) {
  let action = "";
  let data = {
    traceId: generateUUID(),
    currentAt: Date.now(),
    userId,
  }

  if (status == "start") {
    action = "crsp.course.watchVideo_inside.start"; // 1%
  } else if (status == "finish") {
    action = "crsp.course.watchVideo_inside.finish"; // 75%
  } else if (status == "videoStart") {
    action = "crsp.course.watchVideo_inside.videoStart"; // video start.
  } else if (status == "videoEnd") {
    action = "crsp.course.watchVideo_inside.videoEnd"; // video end.
    data.duration = duration;
  }
  //console.log(data)
  var jsonData = JSON.stringify({category: "behavior",action: `${action}-${courseIdentity}`,data: data,})
  //console.log(jsonData)

  fetch("https://api.keepwork.com/event-gateway/events/send", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: jsonData
  })
  .then(response => response.json())
  .then(data => console.log(`${courseIdentity} all video accomplished sent to remote: \n` +JSON.stringify(data)))
  .catch(error => console.error(error));
}
  
function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (rect.top <= (window.innerHeight || document.documentElement.clientHeight) && rect.bottom > 0);
}
  
  
const map = {};
var videoSentFlag = false;
if(userId){
  const videoCtrl = document.getElementById("myPlayer")
  var id = "myPlayer"
  var timer;
  videoCtrl.addEventListener("loadedmetadata", function () {
  //加载数据
  //视频的总长度
  duration = videoCtrl.duration;
  clearInterval(timer);
  });
  
  videoCtrl.addEventListener("playing", () => {
      //播放中
      let process = parseFloat(videoCtrl.currentTime) / duration;

      timer = setInterval(() => {
        process = parseFloat(videoCtrl.currentTime) / duration;
        map[id] = map[id] || {};

        if (!map[id].videoStart && process > 0 && isElementInViewport(videoCtrl)) {
          map[id].videoStart = 1;

          videoAllFinishRequest({ userId, courseIdentity, status: "videoStart" });
        }

        if (!map[id].started && process > 0.01 && isElementInViewport(videoCtrl)) {
          map[id].started = 1;

          videoAllFinishRequest({ userId, courseIdentity, status: "start" });
        }

        if (!map[id].finish && process > 0.75 && isElementInViewport(videoCtrl)) {
          map[id].finish = 1;

          videoAllFinishRequest({ userId, courseIdentity, status: "finish" });
        }

        if (!map[id].videoEnd && process > 0.99 && isElementInViewport(videoCtrl)) {
          map[id].videoEnd = 1;

          if (courseIdentity && map[id] && map[id].finish && !videoSentFlag) {
            videoAllFinishRequest({ userId, courseIdentity, status: "videoEnd" });
            videoSentFlag = true;
          }

          clearInterval(timer);
        }
      }, 1000);
    });
  
    videoCtrl.addEventListener("pause", () => {
      //暂停开始执行的函数
      videoAllFinishRequest({ userId, courseIdentity, status: "videoEnd" });
      clearInterval(timer);
    });

    window.onbeforeunload = () => {
      videoAllFinishRequest({ userId, courseIdentity, status: "videoEnd" });
    }
}
  
var activate = function(msg){
  if(msg.cmd === "pause"){
    document.getElementById("myPlayer").pause()
  }
  else if(msg.cmd === "play"){
    document.getElementById("myPlayer").play()
  }
};

NPL.this(activate, { filename: 'video.page' });
</script>