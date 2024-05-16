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
  .poster {
    display: block;
    margin: 0 -60px;
  }
  .light {
    color: #3ba4ff;
  }
  .educators-title {
    position: relative;
    width: 60%;
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
    padding: 0 30px;
  }
  .educators-title .text .hint {
    margin: 10px;
    font-size: 18px;
    display: block;
    text-align: center;
  }
  .mentor-services .services {
    padding-bottom: 30px;
  }
  .mentor-services .services p.charge {
    text-align: center;
  }
  .mentor-services .services .access {
    max-width: 568px;
    margin: 0 auto;
    font-size: 14px;
    padding: 20px 10px;
    background: #fff;
  }
  .mentor-services .services .access p {
    padding-left: 24px;
    position: relative;
  }
  .mentor-services .services .access p .img-wrap {
    margin-right: 8px;
    position: absolute;
    left: 0;
    top: 1px;
  }
  .mentor-services .services .access .second-level {
    padding-left: 40px;
  }
  .mentor-services .services .access .title {
    line-height: 40px;
  }
  .contact {
    line-height: 50px;
    background-color: #eef7ff;
    border: solid 1px #3ba4ff;
    text-align: center;
    color: #409eff;
    margin: 0 -50px;
    font-size: 14px;
    line-height: 24px;
    padding: 16px 20px;
  }
  .money {
    color: #ff742e;
  }
  .markdown-body .purchase-link {
    color: #ff742e;
    text-decoration: none;
    font-weight: 700;
    margin-left: 8px;
  }
  .part-text .profile {
    border-left: 4px solid #409efe;
    padding-left: 8px;
  }
  .courseware {
    display: flex;
    margin: 30px;
    border-radius: 4px;
    border: 2px #e7f4ff dashed;
    padding: 10px 0;
  }
  .courseware .img-cover {
    width: 850px;
  }
  .courseware .img-cover img {
    width: 100%;
  }
  .courseware .text {
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding: 0 70px;
    width: 340px;
  }
  .courseware .text p {
    font-size: 18px;
  }
  .courseware .text .all-course-btn span {
    font-size: 14px;
    line-height: 40px;
    padding: 12px 100px;
    background-color: #409efe;
    border-radius: 4px;
    color: #fff;
  }
  .learn-more-btn {
    display: block;
    margin: 0 auto;
    width: 284px;
    text-decoration: none !important;
  }
  .learn-more-btn:hover {
    text-decoration: none !important;
  }
  .learn-more {
    width: 284px;
    height: 40px;
    margin: 0 auto;
    line-height: 40px;
    text-align: center;
    border-radius: 4px;
    border: solid 2px #409efe;
  }
  .gutter-line {
    height: 15px;
    background: #f5f5f5;
    margin: 0 -60px 40px;
  }
  @media screen and (max-width: 768px) {
    .poster {
      display: block;
      margin: 0 -20px;
    }
    .contact {
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
    .courseware {
      display: block;
    }
    .courseware .img-cover {
      width: 100%;
    }
  }
</style>

<div class="mentor-services">
  <div class="gutter-line"></div>
  <div class="eductors-tab-title-wrap">
    <div class="eductors-tab-title">
      <span class="eductors-tab-title-line"></span>
      <span class="eductors-tab-title-text"
        ><a name="mentorService">导师服务</a></span
      >
      <span class="eductors-tab-title-line"></span>
    </div>
  </div>
  <div class="services">
    <p class="charge">
      仅需<span class="money">￥3000/年</span
      >购买导师服务，1位家长+1个孩子即可享受职业程序员的指导。
      <a
        class="purchase-link"
        href="/a/orderConfirm?id=4&type=1&payment=rmb"
        target="_blank"
        >点击购买</a
      >
    </p>
    <div class="contact">
      购买成功后，客服将在1个工作日内联系您，请确保您在keepwork预留的手机号保持畅通。
      <br />
      如需咨询，请联系：程老师 13267059950 （电话/微信）、846704851（QQ）
    </div>
    <div class="access">
      <div class="title">具体服务包含：</div>
      <div>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >每周一对一线上指导
        </p>
        <div class="second-level">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >职业程序员通过翻转课堂的形式，通过对学员的提问了解学员自主学习的情况
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >帮助学员发现学习上的盲点并进行指导
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >学员也可以问任何关于编程的问题，不限编程语言
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >也可以审核学员的程序或者作品
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >学员有机会观摩职业程序员是如何工作的，了解产品设计开发的整个过程
          </p>
        </div>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >集体讨论和指导包括项目的开展
        </p>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >在线答疑
        </p>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >针对学员记录的重要体验等的指导（即将推出）
        </p>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >优先排位我们免费的线下课程
        </p>
      </div>
    </div>
    <a
      href="/l/student/moreResources/memtor"
      target="_black"
      class="learn-more-btn"
      ><div class="learn-more">了解更多</div></a
    >
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text">师资团队</span>
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="part-text">
  <p class="profile">
    <strong>李西峙简介：</strong>
    1982年出生于哈尔滨。2005年获浙江大学计算机学科学士学位（竺可桢荣誉学院），同年创建ParacEngine分布式游戏引擎开发工作室。在国内外会议和刊物上发表游戏引擎，脚本语言技术，三维动画制作，CPU芯片设计相关论文和著作8篇。2007年，获得美国投资基金IDG和国内著名IT企业家投资，创建深圳市派瑞安擎科技有限公司（ParaEngine），任CEO。2016年开始，因为自己小时候自主学习的深刻体验，把自己开发的游戏引擎和相关生态软件开放出来打造成一个自主学习的平台（即Paracraft+KeepWork），希望能够帮助中国培养下一代的优秀的程序员，也帮助更广大家庭的孩子们学会自主学习的方法。
    西峙在儿童编程教学方面有大量的实践经验，并结合着自己自7岁开始的30多年的编程经验，对儿童如何学习编程有着深入全面的思考。Paracraft全生态编程学习环境的设计正是来自于他的经验和思考，其中的一对一的指导服务也正是复制西峙幼年时学习编程的重要体验。
    <br />
    <a
      href="https://keepwork.com/lixizhi/note/design/future_education"
      class="light"
      >Paracraft作者李西峙关于未来教育的思考</a
    >
  </p>
  <p class="profile">
    <strong>刘远亮简介：</strong>
    开源学习创始人和自主学习布道者，知识引擎的设计者，软件构架师。浙江大学本科毕业，留美双硕士，拥有哥伦比亚大学，华尔街，国内多家知名互联网企业工作经验，前华为互联网教育首席架构师，在学习/教育领域专注了近20年。对学术界和工业界的互联网教育研究和开发有全面深入的了解，并大量参与美国民间的教育实践，结合自己的丰富的自主学习经验和软件实践，获得了对学习和教育深入系统的认识。知识引擎的设计思想相当程度上来源于他在软件编程，禅，生物医学（尤其是神经，大脑和基因），以及广泛的人文和科学等方面的自主学习的重要体验。
    <br />
    远亮拥有丰富的教学经验，教过各种不同的群体，如儿童，青少年，大学生，青年进城务工群体，老年等等，并在教学中广泛使用<a
      href=" http://blog.opensourcelearning.org/?p=122&lang=zh"
      class="light"
      >以重要体验为基础的</a
    >教学方法。实际上，因为相信教学相长的道理，他可以说无时不刻不在学习和教之中，当然除了玩的时候。：）
    <br />
    <a href="http://www.opensourcelearning.org/" class="light">了解开源学习。</a
    >开源学习组织是<a href="https://www.self-directed.org/" class="light"
      >美国自主教育联盟（ASDE)</a
    >在中国的联系组织。
  </p>
  <p class="profile">
    <strong>陈清华：</strong>Keepwork首席架构师&拥有多年开发经验的程序员。
  </p>
  <p class="profile">
    <strong>李俊杰 谭雯文：</strong
    >Paracraft动画与教学视频制作者，参与制作了大量Paracraft动画与教学视频。PAC全国3D创作大赛指导老师,
    设计师，组织过多次Paracraft大赛。<br />
    25位助教：NPL语言/Paracraft软件开发团队的程序员。
  </p>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text">学生如何学习</span>
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1960/raw#图层13.png"
      alt=""
    />
  </div>
  <div class="text"><p>记录学生的学习轨迹，快速开启课程学习</p></div>
</div>
<div class="courseware">
  <div class="img-cover">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1961/raw#图层72.png"
      alt=""
    />
  </div>
  <div class="text">
    <p>
      学习反馈：<br />
      测试题实时反馈<br />
      技能点精确统计
    </p>
  </div>
</div>
<div class="courseware">
  <div class="img-cover">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1962/raw#图层2004.png"
      alt=""
    />
  </div>
  <div class="text"><p>学习情况追溯+复习巩固</p></div>
</div>