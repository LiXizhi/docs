# 会员空间


会员列表：
- [X琪](/official/paracraft/vips/students/liujiaqi)
- [X雨](/official/paracraft/vips/students/rainy)
- [X富](/official/paracraft/vips/students/wolf2018)


[老师列表](/official/paracraft/vips/teachers/index)
会员请选择上面老师列表里的一位老师作为自己的导师，并告知[程老师](official/paracraft/contact)您的选择。我们会做进一步的安排。

**会员QQ群:876028123**
用于关于paracraft的一般讨论。预约线上或线下一对一指导暂时也在这里预约。已经是会员的学员或家长可以告知[程老师](official/paracraft/contact)，告诉他你的QQ号，我们会将其加入会员QQ讨论群。如果有顾虑的家长，可以新注册一个QQ号给我们。

  


问答平台：
  <p id="demo"></p>

  <iframe name="theFrame" id="gitlabFrame" width=1000 height=1000>Your browser doesn't support iframe!</iframe>
 

<script type="text/javascript"> 
var xhttp = new XMLHttpRequest();


xhttp.open("POST", "https://git.keepwork.com/users/sign_in", true);
xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");  
xhttp.setRequestHeader("Referer", "https://git.keepwork.com/users/sign_in");
xhttp.setRequestHeader("Origin", "");

  xhttp.send("utf8=✓&authenticity_token=hfGQm1WH4amxpEtWAxISM2/Gl8UK4SxL2076df0fGrkZYywTAlzDG4exJpndhHMoen9D3Km8VPJa77sAUaOS0Q==&user[login]=gitlab_rls_leon&user[password]=1536119588&user[remember_me]=0");

  
  
  
function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

  
  
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      //document.getElementById("demo").innerHTML = this.responseText;
      res = JSON.parse(this.responseText);
      var user_git_token = res.data.defaultSiteDataSource.dataSourceToken;      
      url =  'https://git.keepwork.com/gitlab_rls_official/keepworkmentor?private_token='+user_git_token
      console.log('url:'+url);
      window.open(url, "theFrame");  
  
  wait(1000);
  //change all links in the iframe page by adding private_token
  var iframe = document.getElementById('gitlabFrame');
  var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
  var links = innerDoc.getElementsByTagName("A");
  for(var j = 0; j <links.length; j++){
                               // alert('link:');
      console.log(links[j].getAttribute("href")); 
                                
  }
  
  
    }
  };
  
var token = getCookie('token');  
if (token == "")  {
   document.getElementById("demo").innerHTML = "您未登录。请先登录以使用问答平台！";
   document.getElementById("gitlabFrame").style.display='none';    
}else{  
//xhttp.open("POST", "https://keepwork.com/api/wiki/models/user/getProfile", true);
//xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");  
//xhttp.setRequestHeader("Authorization", 'Bearer '+token);
//xhttp.send();
}
  
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}  
                                 
                                 
</script>