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
  .poster {
    display: block;
    margin: 0 -60px;
  }
  .courseExperience {
    display: block;
    height: 153px;
    width: 246px;
    position: absolute;
    bottom: 55px;
    left: 105px;
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
  .teacher-acquire-box .acquire-item .access p {
    padding-left: 28px;
    position: relative;
  }
  .teacher-acquire-box .acquire-item .access p .img-wrap {
    position: absolute;
    left: 0;
    top: 4px;
  }
  .teacher-acquire-box .acquire-item .access .teaching-function {
    margin-left: 20px;
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
      width: 100px;
      position: absolute;
      bottom: 30px;
      left: 0;
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
      src="https://api.keepwork.com/storage/v0/siteFiles/1950/raw#画板 1 拷贝 2.png"
    />
  </a>
  <a href="#courseExperience" class="courseExperience"></a>
</div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text">Built for Educators</span>
    <span class="eductors-tab-title-line"></span>
  </div>
  <div>No experience required!</div>
</div>
<div class="educators-acquire">
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1898/raw#NPL-CAD1.png"
      alt=""
    />
    <p class="intro">Comprehensive Curriculum</p>
    <a href="#teachingPlan" class="detail-wrap"
      ><div class="detail">View More</div></a
    >
  </div>
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1899/raw#评估.png"
      alt=""
    />
    <p class="intro">Automatic Assessments and Summaries</p>
    <a href="#studentPerformance" class="detail-wrap"
      ><div class="detail">View More</div></a
    >
  </div>
  <div class="box">
    <img
      src="https://api.keepwork.com/storage/v0/siteFiles/1900/raw#创建课程_24.png"
      alt=""
    />
    <p class="intro">Personalized Lessons Development</p>
    <a href="#custom" class="detail-wrap"><div class="detail">How to</div></a>
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="courseExperience">Try A Demo Lesson</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
  <div>Watch the demo video</div>
</div>
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/storage/v0/siteFiles/2239/raw#课堂教学演示.mp4
  ext: mp4
  filename: 课堂教学演示.mp4
  size: 241319520
          
```
<div></div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="toBeEducator">Become An Instructor</a></span
    >
    <span class="eductors-tab-title-line"></span>
  </div>
</div>
<div class="identities-info">
  <div class="identity-item identity-teacher">
    <div class="itentity-title">Become An Instructor or A Lesson Developer</div>
    <div class="identity-content">
      <div class="identity-desc">
        you need to pay ￥5000/person/year. Instructors can create an online
        class for 50 students to join.
      </div>
      <div class="identity-showy">
        For further information, please contact Mr Cheng: 13267059950
        (Tel/Wechat)、846704851(QQ)
      </div>
    </div>
  </div>
  <div class="identity-item identity-alliance">
    <div class="itentity-title">To become a Lesson Developer</div>
    <div class="identity-content">
      <div class="identity-showy">you need to pay ￥100 per year.</div>
    </div>
    <div class="identity-wait">To be released</div>
  </div>
</div>
<!-- <div class="tip">
  <span class="hint"
    >An all-in-one solution for educators, starting at
    <span class="money">￥5000/person/year.</span></span
  >
</div>
<div class="contact">
  For further information, please contact Mr Cheng: 13267059950
  （Tel/Wechat）、846704851（QQ）
</div> -->
<div class="teacher-acquire">
  <h4 class="teacher-acquire-title">What you will get</h4>
  <div class="teacher-acquire-box">
    <div class="acquire-item item-left">
      <div class="role">
        <div class="role-text">Learners</div>
        <span class="role-cost">Free</span>
      </div>
      <div class="access">
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Self-learning
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to learn amazing lessons.
            <span class="money">(partially free)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your will be shown real-time feedback on your progress and
            skillpoint development.
          </p>
        </div>
        <p class="not-student-privilege-text">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Lesson development
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to creat lessons.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to submit lessons to our public platform where all
            users could get access to them.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to get benefits from lesson development.
          </p>
        </div>
        <p class="not-student-privilege-text">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Classroom teaching
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >All lessons on the platform are free for classroom teaching.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your students could learn all lessons on the platform free of
            charge in the class.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track students' real-time performance in a
            class.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be shown teaching reports including accuracy analysis and
            testing results of students after a class, which support printing
            and sending to mailboxes.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track your teaching progress.
          </p>
        </div>
      </div>
    </div>
    <div class="acquire-item item-left">
      <div class="role">
        <div class="role-text">Lesson Developers</div>
        <span class="role-cost">￥100/person/year</span>
      </div>
      <div class="access">
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Self-learning
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to learn amazing lessons.
            <span class="money">(partially free)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your will be shown real-time feedback on your progress and
            skillpoint development.
          </p>
        </div>
        <p class="not-student-privilege-text">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Lesson development
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to creat lessons.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to submit lessons to our public platform where all
            users could get access to them.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to get benefits from lesson development.
          </p>
        </div>
        <p class="not-student-privilege-text">
          <span class="img-wrap"
            ><img
              class="not-student-privilege"
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Classroom teaching
        </p>
        <div class="teaching-function">
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >All lessons on the platform are free for classroom teaching.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your students could learn all lessons on the platform free of
            charge in the class.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track students' real-time performance in a
            class.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be shown teaching reports including accuracy analysis and
            testing results of students after a class, which support printing
            and sending to mailboxes.
          </p>
          <p class="not-student-privilege-text">
            <span class="img-wrap"
              ><img
                class="not-student-privilege"
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track your teaching progress.
          </p>
        </div>
      </div>
    </div>
    <div class="acquire-item">
      <div class="role">
        <div class="role-text">Instructors</div>
        <span class="role-cost">￥5000/person/year</span>
      </div>
      <div class="access">
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Self-learning
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to learn amazing lessons.
            <span class="money">(wholly free)</span>
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your will be shown real-time feedback on your progress and
            skillpoint development.
          </p>
        </div>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Lesson development
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to creat lessons.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to submit lessons to our public platform where all
            users could get access to them.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to get benefits from lesson development.
          </p>
        </div>
        <p>
          <span class="img-wrap"
            ><img
              src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
              alt=""/></span
          >Classroom teaching
        </p>
        <div class="teaching-function">
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >All lessons on the platform are free for classroom teaching.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >Your students could learn all lessons on the platform free of
            charge in the class.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track students' real-time performance in a
            class.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be shown teaching reports including accuracy analysis and
            testing results of students after a class, which support printing
            and sending to mailboxes.
          </p>
          <p>
            <span class="img-wrap"
              ><img
                src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
                alt=""/></span
            >You will be able to track your teaching progress.
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
      ><a name="teachingPlan">Comprehensive Curriculum</a></span
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
      The curriculum includes animations, programming and CAD. Our game-based
      lessons could make students totally engaged.
    </p>
    <a
      class="all-course-btn"
      href="https://keepwork.com/l/student/center"
      target="_blank"
      >View Curriculum</a
    >
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="studentPerformance">Automatic Assessments</a></span
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
      src="https://api.keepwork.com/storage/v0/siteFiles/2238/raw#自动评估总结.mp4"
    ></video>
  </div>
  <div class="text">
    <p>
      <span class="img-wrap"
        ><img
          src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
          alt=""/></span
      >Quizzes
    </p>
    <p class="explain">
      Quizzes at the end of each lesson ensure that students understand each
      concept.
    </p>
    <p>
      <span class="img-wrap"
        ><img
          src="https://api.keepwork.com/storage/v0/siteFiles/1902/raw#legal_privilege.png"
          alt=""/></span
      >Skillpoints
    </p>
    <p class="explain">
      The growth in skillpoints is a good indicator of students' pfoficiency in
      each subject.
    </p>
  </div>
</div>
<div class="gutter-line"></div>
<div class="eductors-tab-title-wrap">
  <div class="eductors-tab-title">
    <span class="eductors-tab-title-line"></span>
    <span class="eductors-tab-title-text"
      ><a name="custom">Personalized Lessons Development</a></span
    >
    <span class="eductors-tab-title-line"></span>
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
      <p>Step 1:</p>
      <p class="explain">
        In MY DESK > Lesson Management > Lessons , create a new lesson.
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
      <p>Step 2:</p>
      <p class="explain">
        In Editor, create a page, link the page to the lesson, and complete the
        content.
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
      <p>Step 3:</p>
      <p class="explain">
        In MY DESK > Lesson Management > Packages, complete the basic
        information, add lessons to the package, and save it.
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
      <p>Step 4:</p>
      <p class="explain">
        You can teach with the lesson packages you created. If you want to share
        your lessons with other users on our platform, please submit the
        packages for audit. And the result will be informed within 5 workdays.
        Once the lesson packages are approved, all our uses could get access to
        them.
      </p>
    </div>
  </div>
</div>