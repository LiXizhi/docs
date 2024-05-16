<style>
  .eductors-tab-title-wrap {
    margin: 50px 0 40px;
    text-align: center;
  }
  .eductors-tab-title {
    margin: 50px 0 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .eductors-tab-title-line {
    width: 85px;
    height: 3px;
    background: #409efe;
    border-radius: 3px;
  }
  .eductors-tab-title-text {
    font-size: 36px;
    margin: 0 36px;
  }
  .poster-wrap {
    position: relative;
  }
  .poster-wrap {
    position: relative;
  }
  .poster {
    display: block;
    margin: 0 -60px;
  }
  .courseExperience {
    display: block;
    height: 170px;
    width: 180px;
    position: absolute;
    bottom: 55px;
    left: 0;
  }
  .educators-title {
    position: relative;
    margin: 30px 0;
    width: 80%;
    margin: 50px auto 40px;
  }

  .educators-title::after {
    content: '';
    height: 2px;
    width: 100%;
    position: absolute;
    right: 0;
    top: 30px;
    background: #d6e6f4;
  }
  .educators-title .text {
    background: #fff;
    margin: 0 auto;
    text-align: center;
  }
  .educators-title .text .headline {
    font-size: 36px;
    text-align: center;
    position: relative;
    z-index: 2;
    background: #fff;
    padding: 0 20px;
  }
  .educators-title .text .hint {
    margin: 10px;
    font-size: 18px;
    display: block;
    text-align: center;
  }
  .money {
    color: #ff742e;
  }
  .educators-acquire {
    display: flex;
    justify-content: space-around;
  }
  .educators-acquire .box {
    text-align: center;
  }
  .educators-acquire .box img {
    width: 90%;
    object-fit: cover;
  }
  .educators-acquire .box .detail-wrap {
    display: block;
  }
  .educators-acquire .box .detail {
    width: 240px;
    border: 1px solid #409efe;
    border-radius: 4px;
    line-height: 40px;
    margin: 40px auto;
    color: #409efe;
  }
  .contact {
    line-height: 50px;
    background-color: #eef7ff;
    border: solid 1px #3ba4ff;
    text-align: center;
    color: #3ba4ff;
  }
  .teacher-acquire {
    padding-bottom: 40px;
    background: #fff;
  }
  .teacher-acquire .teacher-acquire-title {
    text-align: center;
    font-size: 24px;
    padding-top: 30px;
  }

  .teacher-acquire-box {
    display: flex;
    justify-content: space-around;
    margin: 30px 0;
  }
  .teacher-acquire-box .acquire-item {
    max-width: 570px;
    font-size: 14px;
    line-height: 30px;
    /* // box-shadow: 1px 1px 5px #ddd9d9, -1px -1px 5px #ddd9d9; */
    border: 1px solid #eee;
    flex: 1;
  }
  .item-left {
    margin-right: 8px;
  }
  .teacher-acquire-box .acquire-item .access {
    padding: 44px 25px;
    background: #fff;
  }
  .teacher-acquire-box .acquire-item .access .caption {
    margin: 10px 0 0 0;
  }
  .teacher-acquire-box .acquire-item .access .teaching-function {
    margin-left: 20px;
  }
  .teacher-acquire-box .acquire-item .access .teaching-function p {
    margin: 0;
  }
  .teacher-acquire-box .acquire-item .access .not-student-privilege-text {
    color: rgb(179, 177, 177);
  }
  .teacher-acquire-box .acquire-item .access p {
    align-items: center;
  }
  .teacher-acquire-box .acquire-item .access p .img-wrap {
    margin-right: 8px;
    display: inline-block;
    width: 20px;
    height: 20px;
  }
  .teacher-acquire-box
    .acquire-item
    .access
    p
    .img-wrap
    .not-student-privilege {
    visibility: hidden;
  }
  .teacher-acquire-box .acquire-item .role {
    height: 100px;
    text-align: center;
    font-size: 24px;
    color: #333333;
    background: #f7f7f7;
  }
  .teacher-acquire-box .acquire-item .role .role-text {
    font-weight: bold;
    color: #333;
    padding-top: 20px;
  }
  .teacher-acquire-box .acquire-item .role .role-cost {
    font-size: 18px;
    color: #10c55b;
  }
  .courseware {
    display: flex;
    padding: 20px 0;
  }
  .courseware .img-cover {
    width: 584px;
  }
  .courseware .img-cover .video-sty {
    border: 2px solid #cecece;
  }
  .courseware .img-cover img {
    width: 100%;
  }
  .courseware .text {
    width: 580px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding-left: 70px;
  }
  .courseware .text p {
    font-size: 18px;
    padding-left: 24px;
    position: relative;
    margin-bottom: 5px;
    color: #333;
  }
  .courseware .text p.course-content {
    padding-left: 2px;
  }
  .courseware .text p .img-wrap {
    position: absolute;
    left: 0;
    top: 2px;
  }
  .courseware .text .explain {
    font-size: 14px;
    color: #777;
    margin-bottom: 40px;
  }
  .courseware .text .all-course-btn {
    font-size: 14px;
    line-height: 40px;
    padding: 0;
    width: 50%;
    text-align: center;
    background-color: #409efe;
    border-radius: 4px;
    color: #fff;
    text-decoration: none;
  }
  .courseware .text .all-course-btn:hover {
    text-decoration: none;
  }
  .courseware .text .all-course-btn span a {
    color: #fff;
    text-decoration: none;
  }
  .tip {
    text-align: center;
    color: #777;
    margin-bottom: 18px;
  }
  .identities-info {
    display: flex;
    align-items: center;
  }
  .identity-item {
    background-color: #ecf5ff;
    height: 257px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .identity-teacher {
    flex: 1;
    padding: 0 48px;
  }
  .identity-alliance {
    margin-left: 16px;
    padding: 0 50px;
    width: 422px;
  }
  .itentity-title {
    font-size: 16px;
    color: #333;
  }
  .identity-content {
    padding: 20px 24px;
    border: 1px dashed;
    font-size: 14px;
    color: #409efe;
    margin-top: 16px;
  }
  .identity-desc {
    color: #777;
    margin-bottom: 6px;
  }
  .identity-wait {
    font-size: 14px;
    color: #777;
    margin-top: 5px;
  }
  .gutter-line {
    height: 15px;
    background: #f5f5f5;
    margin: 0 -60px 40px;
  }
  @media screen and (max-width: 768px) {
    .courseExperience {
      height: 51px;
      width: 68px;
      position: absolute;
      bottom: 30px;
      left: 0;
    }
    .poster {
      margin: 0 -20px;
    }
    .gutter-line {
      margin: 0 -20px 40px;
    }
    .educators-title .text .headline {
      font-size: 16px;
      font-weight: bold;
    }
    .educators-title .text .hint {
      font-size: 12px;
    }
    .educators-title::after {
      top: 12px;
    }
    .educators-acquire {
      display: block;
    }
    .teacher-acquire-box .acquire-item.item-left {
      margin-right: 0;
      margin-bottom: 16px;
    }
    .teacher-acquire-box {
      display: block;
    }
    .courseware {
      display: block;
    }
    .courseware .img-cover {
      width: 90%;
      margin: 0 auto;
    }
    .courseware .text {
      width: 90%;
      padding: 10px;
      margin: 0 auto;
    }
  }
</style>
<div class="poster-wrap">
  <a href="#toBeEducator" class="poster">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1943/raw#teacher.png"
    />
  </a>
  <a href="#courseExperience" class="courseExperience"></a>
</div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text">教师可以获得</span>
    <span class="eductors-tab-title-line"></span>
  </div>
  <div>没有编程经验也能教编程</div>
</div>
<div class="educators-acquire">
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1898/raw#NPL-CAD1.png"
      alt=""
    />
    <p class="intro">优秀的教案、课件</p>
    <a href="#teachingPlan" class="detail-wrap"
      ><div class="detail">查看详情</div></a
    >
  </div>
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1899/raw#评估.png"
      alt=""
    />
    <p class="intro">对学生的课堂表现自动评估和总结</p>
    <a href="#studentPerformance" class="detail-wrap"
      ><div class="detail">查看详情</div></a
    >
  </div>
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1900/raw#创建课程_24.png"
      alt=""
    />
    <p class="intro">创建自己的个性化课程</p>
    <a href="#custom" class="detail-wrap"><div class="detail">如何创建</div></a>
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="courseExperience">课程快速体验</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
  <div>观看课堂演示视频</div>
</div>
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/770/raw#宣传视频01.mp4
  ext: mp4
  filename: op0RRhMEtBeE9B0sMLQ@@hd_hq.mp4
  size: 15700734

```
<div class=""></div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="toBeEducator">申请成为共享课程讲师/课程联盟会员</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="identities-info">
  <div class="identity-item identity-teacher">
    <div class="itentity-title">成为共享课程讲师</div>
    <div class="identity-content">
      <div class="identity-desc">
        仅需 ￥5000/年/人，即可成为共享课程讲师，创建的班级可同时容纳50个学生。
      </div>
      <div class="identity-showy">
        如需购买，请联系：程老师 13267059950 （电话/微信）、846704851（QQ）
      </div>
    </div>
  </div>
  <div class="identity-item identity-alliance">
    <div class="itentity-title">成为课程联盟会员</div>
    <div class="identity-content">
      <div class="identity-showy">仅需￥100/年/人，即可成为课程联盟会员。</div>
    </div>
    <div class="identity-wait">敬请期待...</div>
  </div>
</div>
<!-- <div class="tip">
  <span class="hint"
    >仅需 <span class="money">￥5000/年/人</span>，即可成为共享课程讲师。</span
  >
</div>
<div class="contact">
  如需咨询，请联系：程老师 13267059950 （电话/微信）、846704851（QQ）
</div> -->
<div class="teacher-acquire">
  <h4 class="teacher-acquire-title">具体服务如下</h4>
  <div class="teacher-acquire-box">
    <div class="acquire-item item-left">
      <div class="role">
        <div class="role-text">自主学习用户</div>
        <span class="role-cost">免费</span>
      </div>
      <div class="access">
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >自主学习
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >学习优质课程<span class="money">(部分课程免费)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学习情况、技能增长情况
          </p>
        </div>
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课程开发
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >创建课程
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >发表课程，可供平台用户教学
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >获得收益
          </p>
        </div>
        <p class="not-student-privilege-text caption">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课堂教学
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >平台所有课程可免费用于课堂教学
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >班级学生可免费在课堂中学习平台所有课程
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学生的课堂表现和作答情况
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >自动生成课堂总结报告，支持打印、发送到邮箱
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >跟踪授课进度，追溯授课轨迹
          </p>
        </div>
      </div>
    </div>
    <div class="acquire-item item-left">
      <div class="role">
        <div class="role-text">课程联盟会员</div>
        <span class="role-cost">￥ 100/年 /人</span>
      </div>
      <div class="access">
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >自主学习
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >学习优质课程<span class="money">(部分课程免费)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学习情况、技能增长情况
          </p>
        </div>
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课程开发
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >创建课程
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >发表课程，可供平台用户教学
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >获得收益
          </p>
        </div>
        <p class="not-student-privilege-text caption">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课堂教学
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >平台所有课程可免费用于课堂教学
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >班级学生可免费在课堂中学习平台所有课程
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学生的课堂表现和作答情况
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >自动生成课堂总结报告，支持打印、发送到邮箱
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >跟踪授课进度，追溯授课轨迹
          </p>
        </div>
      </div>
    </div>
    <div class="acquire-item item-right">
      <div class="role">
        <div class="role-text">共享课程讲师</div>
        <span class="role-cost">￥ 5000/年 /人</span>
      </div>
      <div class="access">
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >自主学习
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >学习优质课程<span class="money">(全部课程免费)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学习情况、技能增长情况
          </p>
        </div>
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课程开发
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >创建课程
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >发表课程，可供平台用户教学
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >获得收益
          </p>
        </div>
        <p class="caption">
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >课堂教学
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >平台所有课程可免费用于课堂教学
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >班级学生可免费在课堂中学习平台所有课程
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >实时反馈学生的课堂表现和作答情况
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >自动生成课堂总结报告，支持打印、发送到邮箱
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >跟踪授课进度，追溯授课轨迹
          </p>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="teachingPlan">优秀的教案、课件</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="courseware">
  <div>
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1903/raw#NPLCAD.png"
      alt=""
    />
  </div>
  <div class="text">
    <p class="course-content">
      教案课件涵盖动画教学、编程教学、NPL CAD教学，
      用动画的形式进行教学，内容生动有趣。
    </p>
    <a
      class="all-course-btn"
      href="https://keepwork.com/l/student/center"
      target="_blank"
      >全部课程</a
    >
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="studentPerformance">对学生的课堂表现自动评估和总结</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <video
      width="100%"
      controls="controls"
      class="video-sty"
      src="https://api.keepwork.com/storage/v0/siteFiles/770/raw#%E5%AE%A3%E4%BC%A0%E8%A7%86%E9%A2%9101.mp4"
    ></video>
  </div>
  <div class="text">
    <p>
      <span class="img-wrap"
        ><img
          src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
          alt=""/></span
      >测试题
    </p>
    <p class="explain">每堂课配置测试题，对学生的学习情况进行评估</p>
    <p>
      <span class="img-wrap"
        ><img
          src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
          alt=""/></span
      >技能点
    </p>
    <p class="explain">课程设置了技能点，记录学生的学习成长情况。</p>
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="custom">创建自己的个性化课程</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <video
      width="100%"
      controls="controls"
      class="video-sty"
      src="https://api.keepwork.com/storage/v0/siteFiles/2007/raw#001.mp4"
    ></video>
  </div>
  <div class="text">
    <p>第1步：</p>
    <p class="explain">
      在 “学习中心（教师页）- 课程管理 - 课程” 页面，完成课程的新建。
    </p>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <video
      width="100%"
      controls="controls"
      class="video-sty"
      src="https://api.keepwork.com/storage/v0/siteFiles/2008/raw#002.mp4"
    ></video>
  </div>
  <div class="text">
    <p>第2步：</p>
    <p class="explain">
      在Keepwork编辑器中，创建课程的内容页面，完成课程关联和课程内容的编辑。
    </p>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <video
      width="100%"
      controls="controls"
      class="video-sty"
      src="https://api.keepwork.com/storage/v0/siteFiles/2009/raw#003.mp4"
    ></video>
  </div>
  <div class="text">
    <p>第3步：</p>
    <p class="explain">
      在“学习中心（教师页）- 课程管理 -
      课程包”页面中，编辑课程包的信息，并将课程添加到课程包，保存即可。
    </p>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <video
      width="100%"
      controls="controls"
      class="video-sty"
      src="https://api.keepwork.com/storage/v0/siteFiles/2010/raw#004.mp4"
    ></video>
  </div>
  <div class="text">
    <p>第4步：</p>
    <p class="explain">
      课程包创建好后，您就可以用这个课程包讲课啦。如果希望平台上其他用户也可以使用您创建的课程包，需将课程包提交审核，系统会在5个工作日反馈审核结果。审核通过后，平台上其他用户也可以用这个课程上课、学习。
    </p>
  </div>
</div>