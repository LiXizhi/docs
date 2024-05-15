``` javascript
<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import LoginDialog from '@/components/common/LoginDialog'
export default {
  data() {
    return {
      isLoginDialogShow: false,
      _notify: null,
      _interval: null
    }
  },
  components: {
    LoginDialog
  },
  methods: {
    ...mapActions({
      checkClassroom: 'lesson/student/checkClassroom',
      toggleLoginDialog: 'lesson/toggleLoginDialog',
      changeStatus: 'lesson/student/changeStatus',
      uploadLearnRecords: 'lesson/student/uploadLearnRecords',
      resumeTheClass: 'lesson/student/resumeTheClass'
    }),
    closeLoginDialog() {
      this.toggleLoginDialog(false)
    },
    async backToClassroom() {
      if (!this.enterClassInfo.packageId || !this.enterClassInfo.lessonId) {
        await this.resumeTheClass()
      }
      const { packageId = '', lessonId = '' } = this.enterClassInfo
      this._notify && this._notify.close()
      if (packageId && lessonId) {
        this.$router.push(`/student/package/${packageId}/lesson/${lessonId}`)
      } else {
        this.$message({
          type: 'warning',
          message: this.$t('lesson.classIsOver')
        })
      }
    },
    async intervalCheckClass(delay = 10 * 1000) {
      await this.checkClassroom()
      clearTimeout(this._interval)
      this._interval = setTimeout(async () => {
        await this.intervalCheckClass().catch(e => {
          this.$message({
            message: this.$t('lesson.classIsOver'),
            type: 'warning'
          })
          this._notify.close()
        })
      }, delay)
    }
  },
  beforeRouteUpdate(to, from, next) {
    const {
      name: toName,
      params: { packageId, lessonId }
    } = to

    const { name: fromName } = from
    let _route = ['LessonStudent']

    this._notify && this._notify.close()
    if (!this.isBeInClassroom) {
      return next()
    }
    const { packageId: _packageId, lessonId: _lessonId } = this.enterClassInfo
    let isCurrentClass =
      _route.some(i => i === toName) &&
      packageId == _packageId &&
      lessonId == _lessonId
    if (!isCurrentClass) {
      this.changeStatus(2)
      if (_route.some(i => i === fromName)) {
        this.uploadLearnRecords().catch(e => console.error(e))
      }
      !this._interval && this.intervalCheckClass()
      // 不在当前课堂里面
      this._notify = this.$notify({
        customClass: 'back-to-classroom-notify',
        iconClass: 'el-icon-warning',
        dangerouslyUseHTMLString: true,
        message: this.$t('lesson.notifyTipsStudent', {
          spanStart: '<span class="back-to-classroom">',
          spanEnd: '</span>'
        }),
        duration: 0,
        position: 'top-left',
        onClick: this.backToClassroom
      })
    } else {
      this.changeStatus(1)
      this._interval && clearTimeout(this._interval)
    }
    next()
  },
  computed: {
    ...mapGetters({
      isLogined: 'user/isLogined',
      isBeInClassroom: 'lesson/student/isBeInClassroom',
      enterClassInfo: 'lesson/student/enterClassInfo'
    })
  }
}
</script>

<style lang="scss">
$background: #ed9f21;
$icon: #e54104;
$blue: #5353ff;
.back-to-classroom-notify {
  background: $background;
  .el-notification__icon {
    color: $icon;
    background: white;
    border-radius: 50%;
  }
  .el-notification__content {
    color: white;
    line-height: 14px;
  }
  .back-to-classroom {
    color: $blue;
    cursor: pointer;
  }
  .el-notification__closeBtn {
    color: white;
  }
}
</style>

<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import LoginDialog from '@/components/common/LoginDialog'
export default {
  data() {
    return {
      isLoginDialogShow: false,
      _notify: null
    }
  },
  components: {
    LoginDialog
  },
  methods: {
    ...mapActions({
      toggleLoginDialog: 'lesson/toggleLoginDialog'
    }),
    backToClassroom() {
      const { packageId, lessonId } = this.classroom
      this._notify && this._notify.close()
      this.$router.push(`/teacher/package/${packageId}/lesson/${lessonId}`)
    }
  },
  beforeRouteUpdate(to, from, next) {
    const { name: toName, params: { packageId, lessonId } } = to
    let _route = [
      'LessonTeacherPlan',
      'LessonTeacherPerformance',
      'LessonTeacherPlan'
    ]
    // if (toName === 'TeacherColumn' && !this.isLogined) {
    //   this.toggleLoginDialog(true)
    //   return next(false)
    // }
    if (!this.isBeInClass) return next()
    const { packageId: _packageId, lessonId: _lessonId } = this.classroom
    let isCurrentClass =
      _route.some(i => i === toName) &&
      packageId == _packageId &&
      lessonId == _lessonId
    this._notify && this._notify.close()
    if (!this.isClassIsOver && !isCurrentClass) {
      this._notify = this.$notify({
        customClass: 'back-to-classroom-notify',
        iconClass: 'el-icon-warning',
        dangerouslyUseHTMLString: true,
        message: this.$t('lesson.notifyTips', {
          spanStart: '<span class="back-to-classroom">',
          spanEnd: '</span>'
        }),
        duration: 0,
        position: 'top-left',
        onClick: this.backToClassroom
      })
    }
    next()
  },
  computed: {
    ...mapGetters({
      isLogined: 'user/isLogined',
      isBeInClass: 'lesson/teacher/isBeInClass',
      isClassIsOver: 'lesson/teacher/isClassIsOver',
      classroom: 'lesson/teacher/classroom',
    })
  }
}
</script>

<style lang="scss">
$background: #ed9f21;
$icon: #e54104;
$blue: #5353ff;
.back-to-classroom-notify {
  background: $background;
  .el-notification__icon {
    color: $icon;
    background: white;
    border-radius: 50%;
  }
  .el-notification__content {
    color: white;
    line-height: 14px;
  }
  .back-to-classroom {
    color: $blue;
    cursor: pointer;
  }
  .el-notification__closeBtn {
    color: white;
  }
}
</style>

<template>
  <div class="about">
    <div class="about-carousel">
      <el-carousel
        @change="getImgIndex"
        @click.native="downloadTool"
      >
        <el-carousel-item
          v-for="(img,index) in imgUrls"
          :key="index"
        >
          <img
            class="about-carousel-img"
            :src="img.url"
            alt=""
          >
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="about-title">
      <img
        class="rectangle1"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
      <span class="topic">{{$t('lesson.about.hottestLessons')}}</span>
      <img
        class="rectangle2"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
    </div>
    <div class="about-video">
      <el-row :gutter="20">
        <el-col
          :sm="24"
          :md="8"
          v-for="(coursePackage,index) in hotsPackages"
          v-if="index < 3"
          :key="coursePackage.id"
        >
          <div class="subject-desc">
            <div
              class="img-wrap"
              @click="enterPackageDetailPage(coursePackage.id)"
            ><img
                class="subject-cover"
                :src="coursePackage.extra.coverUrl"
                alt=""
              ></div>
            <h4
              :title="coursePackage.packageName"
              :class="['subject-title']"
              @click="enterPackageDetailPage(coursePackage.id)"
            >{{coursePackage.packageName}}</h4>
            <span>{{$t('lesson.include')}}: {{coursePackage.lessons.length}} {{$t('lesson.lessonsCount')}}</span>
            <span>{{$t('lesson.ages')}}: {{getCoursePackageSuitableAge(coursePackage)}}</span>
            <span :title="coursePackage.intro">{{$t('lesson.intro')}}: {{coursePackage.intro}}</span>
            <div class="purchase-lesson-package">
              <div
                :class="['purchase-tip',{'hidden': coursePackage.rmb == 0}]"
                v-html="$t('lesson.backInfo', { backCoinCount: `<span class='red'>${coursePackage.rmb}</span>` })"
              ></div>
              <div :class="['purchase-money',{'hidden': coursePackage.rmb == 0}]">
                <span class="money">
                  {{$t('lesson.rmbPrice')}}:
                  <span class="red">￥{{coursePackage.rmb}}</span>
                </span>
              </div>
              <div class="purchase-money">
                <span
                  class="money free"
                  v-if="coursePackage.rmb == 0"
                >{{$t('lesson.free')}}</span>
                <span
                  class="money"
                  v-else
                >
                  {{$t('lesson.coinsPrice')}}:
                  <span class="red">{{coursePackage.coin}}</span> {{$t('lesson.coins')}}
                </span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="about-view-more">
      <div
        class="about-view-more-btn"
        @click="gotoLessons"
      >
        <span class="tip">{{$t('lesson.about.viewMoreLessons')}}</span>
        <img
          class="next next-1"
          src="@/assets/lessonImg/aboutPageImg/next.png"
          alt=""
        >
        <img
          class="next next-2"
          src="@/assets/lessonImg/aboutPageImg/next.png"
          alt=""
        >
        <img
          class="next next-3"
          src="@/assets/lessonImg/aboutPageImg/next.png"
          alt=""
        >
      </div>
    </div>
    <div class="about-teacher-student">
      <div class="content">
        <el-row>
          <el-col
            class="right-line"
            :sm="12"
            :xs="24"
          >
            <div class="content-img"><img
                src="@/assets/lessonImg/aboutPageImg/teacher.png"
                alt=""
              ></div>
            <h1>{{$t('lesson.about.teacher')}}</h1>
            <h5 style="font-size:24px;">{{$t('lesson.about.engageStudents')}}</h5>
            <p>{{$t('lesson.about.teacherTalk')}}</p>
          </el-col>
          <el-col
            :sm="12"
            :xs="24"
          >
            <div class="content-img"><img
                src="@/assets/lessonImg/aboutPageImg/student.png"
                alt=""
              ></div>
            <h1>{{$t('lesson.about.student')}}</h1>
            <h5 style="font-size:24px;">{{$t('lesson.about.playGame')}}</h5>
            <p>{{$t('lesson.about.studentTalk')}}</p>
          </el-col>
        </el-row>
        <div class="line hidden-xs-only"></div>
      </div>
    </div>
    <div class="about-title">
      <img
        class="rectangle1"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
      <span class="topic">{{$t('lesson.about.aboutLessons')}}</span>
      <img
        class="rectangle2"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
    </div>
    <div class="about-lesson">
      <el-row>
        <el-col
          :md="12"
          :xs="24"
        >
          <el-row>
            <el-col :span="6">
              <div class="desc-img"><img
                  src="@/assets/lessonImg/aboutPageImg/animation.png"
                  alt=""
                ></div>
            </el-col>
            <el-col :span="18">
              <div class="desc-text">
                <h2>{{$t('lesson.about.animations')}}</h2>
                <p>{{$t('lesson.about.animationsTalk')}}</p>
              </div>
            </el-col>
          </el-row>
        </el-col>
        <el-col
          :md="12"
          :xs="24"
        >
          <el-row>
            <el-col :span="6">
              <div class="desc-img"><img
                  src="@/assets/lessonImg/aboutPageImg/solve_problem.png"
                  alt=""
                ></div>
            </el-col>
            <el-col :span="18">
              <div class="desc-text">
                <h2>{{$t('lesson.about.usage')}}</h2>
                <p>{{$t('lesson.about.usageTalk')}}</p>
              </div>
            </el-col>
          </el-row>
        </el-col>
        <el-col
          :md="12"
          :xs="24"
        >
          <el-row>
            <el-col :span="6">
              <div class="desc-img"><img
                  src="@/assets/lessonImg/aboutPageImg/convenient_service.png"
                  alt=""
                ></div>
            </el-col>
            <el-col :span="18">
              <div class="desc-text">
                <h2>{{$t('lesson.about.teachProgramming')}}</h2>
                <p>{{$t('lesson.about.teachProgrammingTalk')}}</p>
              </div>
            </el-col>
          </el-row>
        </el-col>
        <el-col
          :md="12"
          :xs="24"
        >
          <el-row>
            <el-col :span="6">
              <div class="desc-img price-pic"><img
                  src="@/assets/lessonImg/aboutPageImg/friendly_prices.png"
                  alt=""
                ></div>
            </el-col>
            <el-col :span="18">
              <div class="desc-text">
                <h2>{{$t('lesson.about.expensive')}}</h2>
                <p>{{$t('lesson.about.expensiveTalk')}}</p>
              </div>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </div>
    <div
      class="about-letter"
      v-if="isEn"
    >
      <div class="about-letter-border">
        <div class="about-letter-content">
          <div class="about-letter-content-title">
            <span>A Letter to Parents and Teachers</span>
            <span><img
                class="letter"
                src="@/assets/lessonImg/aboutPageImg/letter.png"
                alt=""
              ></span>
          </div>
          <p>Hi, Parents and Teachers,</p>
          <p>I am Xizhi, the developer of
            <a href="https://keepwork.com/intro/keepwork/NPL">Neural Parallel Language</a> and the 3d animation & game making tool called
            <a href="https://keepwork.com/intro/keepwork/paracraft">Paracraft</a>. In 1989, at the age of 7, I wrote my first program on a IBM PC in my father’s lab. From March 2018, I made a decision to create one computer science lesson every week using Paracraft and NPL. Throughout the lessons, I want to share my first 12 years of programming life with all kids around the world including my own. Click
            <a
              href="#"
              @click.stop.prevent="gotoHere"
            >here</a> to read my autobiography on programming.</p>
          <p>All software used in the lessons are free and open source, including paracraft and NPL. All lessons we sell are also free to read online, and we only charge you a small subscription fee in order for your kids to read the source code of the animation or game while they play it. We encourage you to see the
            <a
              href="#"
              @click.stop.prevent="gotoLessons"
            >lessons</a> yourself and read together with your kids, as I would do the same thing with my own child.</p>
          <p>I have a small International team that is doing Artificial Intelligence research using NPL and paracraft. The software and language that is taught in our lessons is the same set of tools we use for our serious research in AI. Our NPL research center at Tatfook has open sourced over
            <a href="https://github.com/LiXizhi/NPLRuntime/wiki">2 million lines of code</a> written by
            <a href="https://github.com/tatfook">ourselves on github</a>. Your payment or donation will greatly help us to continue our work with more and more talented programmers and scientists.</p>
          <p>Finally, if you or your kids want to join us one day, please email me: lixizhi@yeah.net</p>

          Best<br> Xizhi, Li<br> CTO of Tatfook Network Co.<br>
        </div>
      </div>
    </div>
    <div
      class="about-letter"
      v-else
    >
      <div class="about-letter-border">
        <div class="about-letter-content">
          <div class="about-letter-content-title">
            <span>致家长和老师的一封信</span>
            <span><img
                class="letter"
                src="@/assets/lessonImg/aboutPageImg/letter.png"
                alt=""
              ></span>
          </div>
          <p>各位家长和老师，你们好！</p>
          <p>我是西峙，NPL语言
            <a href="https://keepwork.com/intro/keepwork/NPL">Neural Parallel Language</a>和3D动画游戏制作软件Paracraft的开发者。 在1989年，我七岁的时候就利用IBM计算机在我父亲的实验室编写了我的第一个程序。 从2018年3月起，我决定利用
            <a href="https://keepwork.com/intro/keepwork/paracraft">Paracraft</a>和NPL语言在每周都创建一节计算机课程。 我想通过课程向全世界所有的儿童包括我自己来分享我十二年的编程生活。点击
            <a
              href="#"
              @click.stop.prevent="gotoHere"
            >这里</a>来阅读我的编程生涯自传。</p>
          <p>在课程中所有的软件都是免费并且开源的，包括paracraft和NPL。 我们的所有课程都可以在线免费阅读，我们只收取你一小部分订阅费用为了帮助你的孩子在玩的过程中阅读动画或者游戏的源代码。 我们鼓励你自己去看
            <a
              href="#"
              @click.stop.prevent="gotoLessons"
            >课程</a>并和你的孩子一起阅读，因为我也在和我自己的孩子在做同样的事情。</p>
          <p>我有一个小的国际团队在用NPL和paracraft做人工智能。 我们课程中的软件和语言是和我们应用在人工智能研究中同样一套工具。 我们的大富科技NPL研究中心已经开源了
            <a href="https://github.com/LiXizhi/NPLRuntime/wiki">两百万行代码</a>可以在
            <a href="https://github.com/tatfook">我们的github</a>中查看。你的付款或者捐赠将极大的帮助我们与更多的有天赋的程序员或者科学家工作。</p>
          <p>最后，如果你的孩子有一天想加入我们，可以联系我 ：lixizhi@yeah.net</p>
          大富网络科技有限公司技术总监<br> 李西峙
          <br>
        </div>
      </div>
    </div>
    <div class="about-title">
      <img
        class="rectangle1"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
      <span class="topic">{{$t('lesson.about.Partners')}}</span>
      <img
        class="rectangle2"
        src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png"
        alt=""
      >
    </div>
    <div class="about-badge">
      <el-row>
        <el-col :span="4">
          <div class="img-wrap"><img
              src="@/assets/lessonImg/aboutPageImg/beijing_open_university.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.beijingOpenUniversity')}}</div>
        </el-col>
        <el-col :span="4">
          <div class="img-wrap"><img
              src="@/assets/lessonImg/aboutPageImg/zhejiang_university_logo.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.zhejiangUniversity')}}</div>
        </el-col>
        <el-col :span="4">
          <div class="img-wrap"><img
              src="@/assets/lessonImg/aboutPageImg/harbin_institute_of_technology.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.harbinInstituteOfTechnology')}}</div>
        </el-col>
        <el-col :span="4">
          <div class="img-wrap"><img
              src="@/assets/lessonImg/aboutPageImg/anhui_polytechnic_university.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.anhuiPolytechnicUniversity')}}</div>
        </el-col>
        <el-col :span="4">
          <div class="img-wrap"><img
              src="@/assets/lessonImg/aboutPageImg/beijing_union_university.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.beijingUnionUniversity')}}</div>
        </el-col>
        <el-col :span="4">
          <div class="img-wrap"><img
              class="tatfook"
              src="@/assets/lessonImg/aboutPageImg/tatfook.png"
              alt=""
            ></div>
          <div>{{$t('lesson.about.tatfook')}}</div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import "element-ui/lib/theme-chalk/display.css";
import { locale } from "@/lib/utils/i18n";
import { lesson } from "@/api";
import img1 from "@/assets/lessonImg/aboutPageImg/top_banner1.png";
import img2 from "@/assets/lessonImg/aboutPageImg/top_banner2.png";
import img3 from "@/assets/lessonImg/aboutPageImg/top_banner3.png";
import img4 from "@/assets/lessonImg/aboutPageImg/top_banner4.png";

const TeacherPageReg = /^\/teacher/;
const StudentPageReg = /^\/student/;
export default {
  name: "About",
  data() {
    return {
      isEn: locale === "en-US",
      imgUrls1: [{ url: img1 }, { url: img2 }],
      imgUrls2: [{ url: img3 }, { url: img4 }],
      imgIndex: 0,
      hotsPackages: [],
      animation: ""
    };
  },
  async mounted() {
    this.hotsPackages = await lesson.packages.getHotsPackages();
  },
  computed: {
    imgUrls() {
      return this.isEn ? this.imgUrls1 : this.imgUrls2;
    },
    nowFullPath() {
      return this.$route.fullPath;
    },
    isTeacherPage() {
      return TeacherPageReg.test(this.nowFullPath);
    },
    isStudentPage() {
      return StudentPageReg.test(this.nowFullPath);
    }
  },
  methods: {
    getImgIndex(index) {
      this.imgIndex = index;
    },
    downloadTool() {
      if (this.imgIndex === 1) {
        window.location.href = "http://www.paracraft.cn/download?lang=zh";
      }
    },
    gotoLessons() {
      if (this.isStudentPage) {
        this.$router.push({
          path: `/student/center`
        });
      } else {
        this.$router.push({
          path: `/teacher/center`
        });
      }
    },
    gotoHere() {
      if (this.isStudentPage) {
        this.$router.push({
          path: `/student/autobiography`
        });
      } else {
        this.$router.push({
          path: `/teacher/autobiography`
        });
      }
    },
    enterPackageDetailPage(packageId) {
      this.$router.push({
        path: `package/${packageId}`
      });
    },
    getCoursePackageSuitableAge(packageDetail) {
      let { minAge, maxAge } = packageDetail;
      if (minAge == 0 && maxAge == 0) {
        return this.$t("lesson.packageManage.SuitableForAll");
      }
      return `${minAge}-${maxAge}`;
    }
  }
};
</script>

<style lang="scss">
.about {
  &-carousel {
    .el-carousel__container {
      height: 500px !important;
    }
    &-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      cursor: pointer;
    }
  }
  &-title {
    margin: 40px auto;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    .topic {
      padding: 0 30px;
      font-size: 40px;
      letter-spacing: 2px;
      color: #333333;
    }
    .rectangle2 {
      transform: rotateY(-180deg);
      height: 100%;
      line-height: 100%;
    }
  }
  &-video {
    max-width: 1200px;
    margin: 0 auto;
    .subject-desc {
      width: 287px;
      height: 415px;
      padding: 34px 34px 6px;
      margin: 20px auto;
      border: solid 2px #d2d2d2;
      border-radius: 1px;
      background: #fff;
      .img-wrap {
        width: 287px;
        height: 160px;
        border-radius: 6px;
        margin: 0 auto;
        cursor: pointer;
        .subject-cover {
          width: 287px;
          height: 160px;
          object-fit: cover;
          border-radius: 6px;
        }
      }
      .subject-title {
        font-size: 18px;
        margin-bottom: 10px;
        height: 24px;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #333333;
      }
      span {
        display: block;
        font-size: 14px;
        line-height: 22px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #777;
      }
      .purchase-lesson-package {
        margin: 10px 0;
        border-top: 1px solid #e3e3e3;
        .hidden {
          visibility: hidden;
        }
        .red {
          color: #e4461f;
          display: inline;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .purchase-tip {
          color: #3491f0;
          margin: 14px 0 5px 0;
          font-size: 14px;
        }
        .purchase-money {
          margin: 2px 0;
          cursor: default;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          .free {
            color: #67c23a;
          }
          .money {
            font-size: 14px;
            display: inline-block;
            padding: 0 12px;
            height: 27px;
            border: solid 2px #f3f3f3;
            text-align: left;
            line-height: 27px;
            border-radius: 15px;
            max-width: 255px;
            min-width: 132px;
            text-align: center;
          }
        }
      }
    }
  }
  &-view-more {
    &-btn {
      width: 322px;
      margin: 30px auto;
      position: relative;
      cursor: pointer;
      height: 77px;
      background: url("../../../assets/lessonImg/aboutPageImg/view_more_lesson.png")
        no-repeat;
      background-size: cover;
      padding-left: 20px;
      .tip {
        text-align: center;
        line-height: 70px;
        font-size: 18px;
        color: #ffffff;
        display: inline-block;
        width: 200px;
      }
      .next {
        position: absolute;
        top: 28px;
        left: 230px;
        &-2 {
          left: 240px;
        }
        &-3 {
          left: 250px;
        }
      }
    }
  }
  &-teacher-student {
    background: #f8edd9;
    padding: 50px;
    margin: 40px 0;
    .content {
      max-width: 1200px;
      margin: 0 auto;
      text-align: center;
      position: relative;
      &-img {
        width: 396px;
        height: 383px;
        margin: 0 auto;
      }
      p {
        text-align: left;
        padding-left: 10px;
      }
      .el-row {
        .el-col {
          padding: 0 50px;
        }
      }
      .line {
        width: 2px;
        height: 100%;
        background: #fff;
        position: absolute;
        top: 20px;
        left: 50%;
      }
    }
  }
  &-lesson {
    max-width: 1200px;
    margin: 0 auto;
    padding: 10px;
    .desc-img {
      width: 100%;
      padding: 20px 0;
      text-align: center;
      img {
        width: 100%;
        max-width: 165px;
        object-fit: contain;
      }
    }
    .price-pic {
      width: 80%;
    }
    .desc-text {
      flex: 1;
      padding-left: 20px;
      min-height: 256px;
    }
    .el-row .el-col .el-row {
      padding: 0 30px;
    }
  }
  &-letter {
    background: #f8edd9;
    margin: 80px 0;
    padding: 80px;
    &-border {
      max-width: 1200px;
      margin: 0 auto;
      padding: 46px;
      background: repeating-linear-gradient(
        -45deg,
        rgb(240, 50, 92) 0,
        rgb(240, 50, 92) 30px,
        #fff 30px,
        #fff 60px,
        rgb(33, 39, 82) 60px,
        rgb(33, 39, 82) 90px,
        #fff 0,
        #fff 120px
      );
    }
    &-content {
      padding: 110px 190px;
      background-color: #fff;
      &-title {
        text-align: center;
        span {
          font-size: 40px;
        }
      }
    }
  }
  &-badge {
    margin: 0 auto 160px;
    max-width: 1200px;
    text-align: center;
    .tatfook {
      margin: 20px 0;
    }
  }
}
</style>
<style lang="scss">
@media (max-width: 768px) {
  .about {
    &-carousel {
      .el-carousel__container {
        height: 200px !important;
      }
    }
    &-teacher-student {
      .content {
        &-img {
          width: 200px;
          height: 200px;
          img {
            width: 100%;
          }
        }
      }
    }
    &-lesson {
      margin: 0 auto;
      padding: 10px;
      &-desc {
        display: block;
        .desc-img {
          margin: 0 auto;
          padding: 20px 0;
        }
        .desc-text {
          padding-left: 20px;
          min-height: 220px;
        }
      }
    }
    &-view-more {
      &-btn {
        width: 222px;
        height: 50px;
        margin: 0 auto;
        position: relative;
        .tip {
          color: #ffffff;
          display: inline-block;
          width: 180px;
          line-height: 45px;
          font-size: 14px;
        }
        .next {
          width: 12px;
          position: absolute;
          top: 18px;
          left: 180px;
          &-2 {
            left: 190px;
          }
          &-3 {
            left: 200px;
          }
        }
      }
    }
    &-letter {
      background: #f8edd9;
      margin: 40px 0;
      padding: 20px;
      &-border {
        margin: 0 auto;
        padding: 26px;
      }
      &-content {
        padding: 10px;
        &-title {
          text-align: center;
          span {
            font-size: 20px;
          }
          .letter {
            width: 40px;
          }
        }
      }
    }
    &-badge {
      margin: 0 auto;
      text-align: center;
      font-size: 14px;
      .img-wrap {
        height: 50px;
        max-width: 86px;
        text-align: center;
        img {
          width: 40px;
        }
      }
      .tatfook {
        margin: 20px 0;
      }
    }
  }
}
</style>

<template>
  <div class="all-teaching-video">
    <div class="all-teaching-video-content">
      <div class="all-teaching-video-content-sidebar">
        <el-tree
          ref="tree"
          :data="data"
          node-key="id"
          :current-node-key="defaultKey"
          :default-expand-all="true"
          :highlight-current="true"
          :props="defaultProps"
          @node-click="handleNodeClick"
        ></el-tree>
      </div>
      <div class="all-teaching-video-content-main">
        <combo-box
          :routes="routes"
          :autoWidth="true"
        ></combo-box>
      </div>
    </div>
  </div>
</template>
<script>
import ComboBox from '@/components/combo/ComboBox'
const TeacherPageReg = /^\/teacher/

export default {
  name: 'AllTeachingVideo',
  components: {
    ComboBox
  },
  data() {
    return {
      routes: {
        animate: {
          projectName: 'official/paracraft',
          filePath: 'animation-tutorials-2'
        },
        program: {
          projectName: 'official/paracraft',
          filePath: 'CodeblockList'
        },
        cad: {
          projectName: 'intro/keepwork',
          filePath: 'NPLCAD'
        }
      },
      data: [
        {
          id: 1,
          label: `${this.$t("lesson.instructionalVideos")}:`,
          children: [
            {
              id: 2,
              label: this.$t("lesson.animationsLesson"),
              value: 'animate'
            },
            {
              id: 3,
              label: this.$t("lesson.programmingLesson"),
              value: 'program'
            },
            {
              id: 4,
              label: this.$t("lesson.CADLesson"),
              value: 'cad'
            }
          ]
        },
      ],
      defaultKey: 2,
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    }
  },
  mounted(){
    let currentParam = this.$route.params.command
    switch(currentParam){
      case 'animate': 
        this.$refs.tree.setCurrentKey(2)
        break
      case 'program':
        this.$refs.tree.setCurrentKey(3)
        break
      case 'cad':
        this.$refs.tree.setCurrentKey(4)
        break
      default: 
        this.$refs.tree.setCurrentKey(2)
        break
    }
  },
  computed: {
    isTeacherPage() {
      return TeacherPageReg.test(this.nowFullPath)
    },
    currentPath() {
      return this.isTeacherPage ? '/teacher' : '/student'
    },
  },
  methods: {
    handleNodeClick(data) {
      if (data.value) {
        this.$router.push({ path: `${this.currentPath}/allteachingvideo/${data.value}` })
      }
    }
  }
}
</script>
<style lang="scss">
.all-teaching-video {
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  &-content {
    display: flex;
    height: 100%;
    &-sidebar {
      width: 274px;
      height: 100%;
      margin-right: 10px;
      background: #fff;
    }
    &-main {
      flex: 1;
      background: #fff;
      height: 100%;
      overflow: hidden;
      padding-left: 10px;
      .el-row {
        width: auto;
        max-width: 930px;
      }
      div[data-mod] {
        width: auto;
        max-width: 930px;
      }
    }
  }
}
@media screen and (max-width: 768px) {
  .all-teaching-video {
    display: block;
    height: auto;
    &-content {
      display: block;
      height: auto;
      &-sidebar {
        width: 100%;
      }
    }
  }
}
</style>

<template>
  <div class="here-page">
    <div class="here-page-content">
      <div class="here-page-content-title">
        <img class="rectangle1" src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png" alt="">
        <span class="topic">{{$t('lesson.herePageText.title')}}</span>
        <img class="rectangle2" src="@/assets/lessonImg/aboutPageImg/rounded_rectangle.png" alt="">
      </div>
      <div class="here-page-content-sub-title">{{$t('lesson.herePageText.subTitle')}}</div>

      <div class="here-page-content-opening-words">
        <p>{{$t('lesson.herePageText.openingWords1')}}</P>
        <p>{{$t('lesson.herePageText.openingWords2')}}</p>
        <p>{{$t('lesson.herePageText.openingWords3')}}</p>
      </div>

      <div class="here-page-content-key-point point1">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core1')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint1-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent1')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint1-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-img">
        <img class="pic" src="@/assets/lessonImg/aboutPageImg/here_page_img1.png" alt="">
      </div>

      <div class="here-page-content-key-point point2">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core2')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint2-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent2')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint2-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-key-point point3">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core3')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint3-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent3')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint3-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-key-point point4">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core4')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint4-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent4')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint4-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-img">
        <img class="pic" src="@/assets/lessonImg/aboutPageImg/here_page_img2.png" alt="">
      </div>

      <div class="here-page-content-key-point point5">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core5')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint5-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent5')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint5-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-key-point point6">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core6')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint6-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent6')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint6-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-key-point point7">
        <div class="here-page-content-key-point-title"><img class="title-img" src="@/assets/lessonImg/aboutPageImg/star.png" alt="">{{$t('lesson.herePageText.core7')}}</div>
        <div class="here-page-content-key-point-part1">
          <p>{{$t('lesson.herePageText.keyPoint7-part1')}}</p>
        </div>
        <div class="here-page-content-key-point-part2">
          <h4>{{$t('lesson.herePageText.coreContent7')}}</h4>
          <p>{{$t('lesson.herePageText.keyPoint7-part2')}}</p>
        </div>
      </div>

      <div class="here-page-content-img">
        <img class="pic" src="@/assets/lessonImg/aboutPageImg/here_page_img3.png" alt="">
      </div>

      <div class="here-page-content-conclusions">
        <h3>{{$t('lesson.herePageText.conclusions')}}</h3>
        <p>{{$t('lesson.herePageText.conclusionsOpeningWords')}}</p>
        <p>{{$t('lesson.herePageText.contrast')}}</p>
        <table  border="1" cellpadding="6" cellspacing="0" borderColor="#f5f7fa">
          <tr class="header" align="center">
            <td width="190"></td>
            <td>{{$t('lesson.herePageText.contrastTitle1')}}</td>
            <td>{{$t('lesson.herePageText.contrastTitle2')}}</td>
          </tr>
          <tr>
            <td>{{$t('lesson.herePageText.catalog1')}}</td>
            <td>{{$t('lesson.herePageText.catalog1-qiankun')}}</td>
            <td>{{$t('lesson.herePageText.catalog1-other')}}</td>
          </tr>
          <tr>
            <td>{{$t('lesson.herePageText.catalog2')}}</td>
            <td>{{$t('lesson.herePageText.catalog2-qiankun')}}</td>
            <td>{{$t('lesson.herePageText.catalog2-other')}}</td>
          </tr>
          <tr>
            <td>{{$t('lesson.herePageText.catalog3')}}</td>
            <td>{{$t('lesson.herePageText.catalog3-qiankun')}}</td>
            <td>{{$t('lesson.herePageText.catalog3-other')}}</td>
          </tr>
          <tr>
            <td>{{$t('lesson.herePageText.catalog4')}}</td>
            <td>{{$t('lesson.herePageText.catalog4-qiankun')}}</td>
            <td>{{$t('lesson.herePageText.catalog4-other')}}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "Autobiography",
  data() {
    return {}
  },
  created(){
    this.fromTopToShow()
  },
  methods:{
    fromTopToShow(){
      window.scrollTo(0, 0)
    }
  }
}
</script>

<style lang="scss">
.here-page {
  &-content {
    max-width: 860px;
    margin: 0 auto 26px;
    padding: 50px 20px;
    background: #fff;
    line-height: 26px;
    .pic{
      width: 100%;
      object-fit: contain;
    }
    &-title {
      margin: 0 auto;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      .topic {
        padding: 0 30px;
        font-size: 30px;
        letter-spacing: 2px;
        color: #333333;
      }
      .rectangle2 {
        transform: rotateY(-180deg);
        height: 100%;
        line-height: 100%;
      }
    }
    &-sub-title {
      text-align: center;
      margin: 18px 0 50px;
    }
    &-key-point {
      margin: 25px 0;
      &-title {
        padding: 15px 0;
        display: flex;
        justify-content: center;
        align-items: Center;
        .title-img {
          width: 38px;
          margin-right: 15px;
        }
      }
      &-part2 {
        padding: 10px 18px;
        border-left: 10px #50bfff solid;
        border-radius: 5px;
        background: #ecf8ff;
      }
    }
    &-conclusions{
      .header{
        height: 50px;
        background: #f5f7fa;
      }
    }
  }
}
</style>

<template>
  <div class="coin-purchase">
    <div class="coin-purchase-info">
      <el-checkbox class="coin-purchase-checkbox" v-model='isPayByCoin' v-show="isUserHaveEnoughCoin">{{$t('lesson.purchaseWithCoins')}}</el-checkbox>
      <span v-show="!isUserHaveEnoughCoin">{{$t('lesson.purchaseWithCoins')}}</span>
    </div>
    <div class="coin-purchase-card" :class="{'coin-purchase-card-selected': isPayByCoin}">
      <label class="coin-purchase-card-label">{{$t('lesson.availableCoins')}}</label>
      <div class="coin-purchase-card-value">
        <img v-show="isUserHaveEnoughCoin" class="coin-purchase-card-bg-icon" src="@/assets/lessonImg/coin_available.png" alt="">
        <img v-show="!isUserHaveEnoughCoin" class="coin-purchase-card-bg-icon" src="@/assets/lessonImg/coin_disabled.png" alt=""> {{restCoin}} {{$t('lesson.coins')}}
      </div>
    </div>
  </div>
</template>
<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'
export default {
  name: 'CoinPurchase',
  props: {
    packageDetail: Object
  },
  computed: {
    ...mapGetters({
      userinfo: 'lesson/userinfo'
    }),
    restCoin() {
      return _.get(this.userinfo, 'coin', 0)
    },
    packageNeedCoinsCount() {
      return _.get(this.packageDetail, 'coin')
    },
    isUserHaveEnoughCoin() {
      return this.restCoin >= this.packageNeedCoinsCount
    }
  },
  data() {
    return {
      isPayByCoin: false
    }
  }
}
</script>
<style lang="scss">
.coin-purchase {
  &-info {
    color: #333;
  }
  &-card {
    width: 266px;
    height: 127px;
    background-color: #f3f3ef;
    font-size: 18px;
    margin-top: 18px;
    text-align: center;
    padding: 30px 15px;
    box-sizing: border-box;
    border-radius: 4px;
    &-selected {
      background-color: #66cd2e;
    }
    &-label {
      color: #172d0b;
    }
    &-value {
      background-color: #fff;
      color: #333;
      font-weight: bold;
      position: relative;
      height: 50px;
      line-height: 50px;
      text-align: center;
      margin: 10px 30px 0 43px;
      white-space: nowrap;
    }
    &-bg-icon {
      position: absolute;
      width: 50px;
      height: 50px;
      left: -25px;
      top: 0;
    }
  }
  .el-checkbox__inner {
    border-radius: 50%;
    width: 20px;
    height: 20px;
  }
  .el-checkbox__inner::after {
    width: 5px;
    height: 10px;
    border-width: 2px;
    left: 6px;
  }
  .el-checkbox__label {
    font-size: 16px;
    color: #333;
  }
  .el-checkbox__input.is-checked + .el-checkbox__label {
    color: #333;
  }
}
</style>

<template>
  <div class="eductors-tab">
    <div class="eductors-tab-title">
      <span class="eductors-tab-title-line"></span>
      <span class="eductors-tab-title-text">{{$t('lesson.teachingContent')}}</span>
      <span class="eductors-tab-title-line"></span>
    </div>
    <div class="eductors-tab-operations">
      <span
        :class="['eductors-tab-operations-button', {'selected': currentTab === 0 }]"
        @click="switchTab(0)"
      >{{$t('lesson.onlineLessons')}}</span>
      <span
        :class="['eductors-tab-operations-button', {'selected': currentTab === 1 }]"
        @click="switchTab(1)"
      >{{$t('lesson.offlineGuidingLessons')}}</span>
      <span
        :class="['eductors-tab-operations-button', {'selected': currentTab === 2 }]"
        @click="switchTab(2)"
      >{{$t('lesson.instructionalVideos_2')}}</span>
    </div>

    <div class="eductors-tab-main">
      <div
        class="eductors-tab-main-item eductors-tab-main-item-online"
        v-show="currentTab === 0"
      >
        <div class="eductors-tab-main-title">{{$t('lesson.about.hottestLessons')}}</div>
        <div class="eductors-tab-main-item-wrap">
          <div
            class="eductors-tab-main-item-wrap-cell"
            v-for="(item, index) in lessons"
            :key="index"
          >
            <img
              class="eductors-tab-main-item-wrap-cell-img"
              :src="item.extra.coverUrl"
              :alt="item.packageName"
              @click="goLessonPackage(item)"
            >
            <div class="eductors-tab-main-item-wrap-cell-text-title" @click="goLessonPackage(item)">{{item.packageName}}</div>
            <div class="eductors-tab-main-item-wrap-cell-text">{{$t('lesson.include')}}: {{item.lessons.length}}{{$t('lesson.lessonsCount')}}</div>
            <div class="eductors-tab-main-item-wrap-cell-text"> {{$t('lesson.ages')}}: {{getPackageSuitableAge(item)}}</div>
            <div class="eductors-tab-main-item-wrap-cell-text-desc">{{$t('lesson.intro')}}: {{item.intro}}</div>
          </div>
        </div>
      </div>

      <div
        class="eductors-tab-main-item eductors-tab-main-item-offline"
        v-show="currentTab === 1"
      >
        <div class="eductors-tab-main-item-offline-wrap">
          <combo-box
            projectName="official/paracraft"
            filePath="learn/parent_tab_offline"
          ></combo-box>
        </div>
      </div>

      <div
        class="eductors-tab-main-item eductors-tab-main-item-video"
        v-show="currentTab === 2"
      >
        <div
          class="eductors-tab-main-item-video-tab"
          @click="handleMore"
        >
          <img
            src="@/assets/lessonImg/teaching-video_2.png"
            alt=""
          >
          <p>{{$t('lesson.animationsLesson')}}</p>
        </div>
        <div
          class="eductors-tab-main-item-video-tab"
          @click="handleMore"
        >
          <img
            src="@/assets/lessonImg/teaching-video_1.png"
            alt=""
          >
          <p>{{$t('lesson.programmingLesson')}}</p>
        </div>
        <div
          class="eductors-tab-main-item-video-tab"
          @click="handleMore"
        >
          <div>
            <img
              src="@/assets/lessonImg/teaching-video_3.png"
              alt=""
            >
          </div>
          <div>{{$t('lesson.CADLesson')}}</div>
        </div>
      </div>
    </div>
    <div class="eductors-tab-footer">
      <div
        class="eductors-tab-footer-more"
        @click="handleMore"
      >
        {{$t('lesson.viewMore')}}
      </div>
    </div>
  </div>

</template>

<script>
import { lesson } from '@/api'
import ComboBox from '@/components/combo/ComboBox'
export default {
  name: 'EductorsTab',
  components: {
    ComboBox
  },
  data() {
    return {
      currentTab: 0,
      lessons: []
    }
  },
  async mounted() {
    let res = await lesson.packages.getHotsPackages()
    res.length = 3
    this.lessons = res
  },
  methods: {
    switchTab(index) {
      this.currentTab = index
    },
    goLessonPackage(lessonPackage) {
      window.open(`/l/student/package/${lessonPackage.id}`)
    },
    getPackageSuitableAge(lessonPackage) {
      let { maxAge, minAge } = lessonPackage
      if (maxAge == 0 && minAge == 0) {
        return this.$t('lesson.packageManage.SuitableForAll')
      }
      return `${minAge}-${maxAge}`
    },
    goLesson() {
      this.$router.push(`/student/allteachingvideo`)
    },
    handleMore() {
      if (this.currentTab === 1) {
        return this.$router.push('/student/moreResources/offline')
      }
      if (this.currentTab === 2) {
        return this.$router.push('/student/allteachingvideo/animate')
      }
      this.$router.push(`/student/center`)
    }
  }
}
</script>


<style lang="scss">
.eductors-tab {
  max-width: 1200px;
  min-height: 645px;
  margin: auto;
  position: relative;
  &-title {
    margin-top: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    &-line {
      width: 85px;
      height: 3px;
      background: #409efe;
    }
    &-text {
      font-size: 36px;
      margin: 0 36px;
    }
  }
  &-operations {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 46px;
    &-button {
      cursor: pointer;
      margin: 0 15px;
      width: 240px;
      height: 39px;
      line-height: 39px;
      border: solid 1px #bcbcbc;
      border-radius: 19px;
      text-align: center;
      &.selected {
        background: #409eff;
        color: #fff;
        border: none;
      }
    }
  }
  &-main {
    &-title {
      font-size: 18px;
      color: #333;
      margin: 20px;
    }
    &-item-wrap {
      display: flex;
      justify-content: space-around;
      &-cell {
        &-img {
          height: 207px;
          width: 381px;
          border-radius: 6px;
          object-fit: cover;
          cursor: pointer;
        }
        &-text {
          color: #818181;
          font-size: 14px;
          line-height: 23px;
          width: 350px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          margin: 5px;
          &-title {
            color: #333;
            margin: 5px;
            font-weight: bold;
            cursor: pointer;
          }
          &-desc {
            margin: 5px;
            color: #818181;
            font-size: 14px;
            height: 40px;
            width: 350px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            line-height: 20px;
            -webkit-box-orient: vertical;
          }
        }
      }
    }

    &-item-offline {
      height: 450px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    &-item-video {
      margin-top: 62px;
      display: flex;
      justify-content: space-around;
      &-tab {
        text-align: center;
        font-size: 16px;
        cursor: pointer;
        img {
          width: 382px;
          height: 212px;
          object-fit: cover;
        }
      }
    }
  }
  &-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
    position: absolute;
    bottom: 10px;
    left: 0;
    right: 0;
    &-more {
      cursor: pointer;
      height: 40px;
      line-height: 40px;
      padding: 0 130px;
      border-radius: 4px;
      font-size: 14px;
      color: #409eff;
      border-radius: 4px;
      border: solid 2px #409efe;
    }
  }
}

@media (max-width: 768px) {
  .eductors-tab {
    min-width: auto;
    min-height: auto;
    padding-bottom: 60px;
    &-main {
      &-title {
        display: none;
      }
      &-item {
        &-wrap {
          margin-top: 10px;
          flex-direction: column;
          &-cell {
            &-img {
              width: 100%;
            }
            &-text {
              width: 95%;
              &-desc {
                width: 95%;
              }
            }
          }
        }

        &-offline {
          height: auto;
          margin-top: 10px;
          &-wrap {
            background-color: #ffffff;
            border-radius: 4px;
            border: solid 2px #ffc46c;
            margin: 10px;
            padding: 10px 15px;
          }
        }

        &-video {
          flex-direction: column;
          margin-top: 0;
          &-tab {
            img {
              width: 100%;
              object-fit: contain;
            }
            p {
              margin: 0;
            }
          }
        }
      }
    }
    &-title {
      justify-content: flex-start;
      &-text {
        font-size: 16px;
        margin: 11px;
      }
      &-line {
        display: none;
      }
    }
    &-operations {
      margin-top: 0px;
      &-button {
        border-radius: 0px;
        flex: 1;
        margin: 0;
        border: none;
        font-size: 14px;
        color: #777;
        background: #f5f5f5;
      }
    }
    &-footer {
      &-more {
        width: 90%;
        margin: 0 auto;
        padding: 0;
        text-align: center;
      }
    }
  }
}
</style>


<template>
  <div class="study-page-header">
    <div class="study-page-header-menu">
      <div class="study-page-header-menu-left">
        <span
          @click="goToSpecialColumn"
          :class="['study-page-header-menu-left-button', { 'selected': activeIndex === 1 }]"
        >{{$t('lesson.myDesk')}}</span>
        <span
          @click="goToLessonsCenter"
          :class="['study-page-header-menu-left-button', { 'selected': activeIndex === 2 }]"
        >{{$t('lesson.allLessons')}}</span>
      </div>
      <div class="study-page-header-menu-right">
        <el-dropdown
          class="study-page-header-menu-right-dropdown"
          @command="getSolution"
        >
          <span :class="['el-dropdown-link', { 'selected': activeIndex === 3}]">
            {{$t("lesson.solutions")}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="teachingIdea">{{$t("lesson.ourIdeas")}}</el-dropdown-item>
            <el-dropdown-item command="teacher">{{$t("lesson.forEducations")}}</el-dropdown-item>
            <el-dropdown-item command="parents">{{$t("lesson.forLearners")}}</el-dropdown-item>
            <el-dropdown-item command="organization">{{$t("lesson.partnership")}}</el-dropdown-item>
            <el-dropdown-item command="competition">{{$t("lesson.worksAndContests")}}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

        <el-dropdown
          class="study-page-header-menu-right-dropdown"
          @command="hanldOperation"
        >
          <span :class="['el-dropdown-link', { 'selected': activeIndex === 4}]">
            {{$t("lesson.resources")}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="teaching-video">{{$t("lesson.videos")}}</el-dropdown-item>
            <el-dropdown-item command="download">{{$t("lesson.paracraftDownload")}}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <span
          class="study-page-header-menu-right-link"
          @click="switchIdentity"
        >{{toggleButtonText}}</span>
      </div>
    </div>
  </div>
</template>
<script>
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'
import LoginDialog from '@/components/common/LoginDialog'

const StudentPageReg = /^\/student/
const TeacherPageReg = /^\/teacher/
const AboutActivePageNameReg = /^(TeacherAbout|StudentAbout)$/
const LessonsActivePageNameReg = /^(TeacherCenter|StudentCenter)$/
const ColumnActivePageNameReg = /^(TeacherColumn|StudentColumn)+/
const LEARN_CNETER_TAG = ['TeacherColumn', 'TeacherColumnApply', 'TeacherColumnReview', 'TeacherColumnLessonManager', 'TeacherColumnPackageManager', 'TeacherColumnEditPackage', 'TeacherColumnMentorInvite', 'LearningCenterPackages', 'OfflineGuidanceCourse', 'TeachingVideo', 'SharedCourseLecturer', 'MentorService']
const ALL_LESSON_TAG = ['StudentCenter', 'TeacherCenter']
const SOLUTION_TAG = ['StudentSolution', 'TeacherSolution']
const VIDEO_TAG = ['TeacherAllTeachingVideo', 'StudentAllTeachingVideo']
export default {
  name: 'Header',
  data() {
    return {
      activeIndex: 0
    }
  },
  watch: {
    $route(to) {
      const { name } = to
      if (LEARN_CNETER_TAG.some(i => i === name)) {
        return this.activeIndex = 1
      }
      if (ALL_LESSON_TAG.some(i => i === name)) {
        return this.activeIndex = 2
      }
      if (SOLUTION_TAG.some(i => i === name)) {
        return this.activeIndex = 3
      }
      if (VIDEO_TAG.some(i => i === name)) {
        return this.activeIndex = 4
      }
      this.activeIndex = 0
    }
  },
  computed: {
    ...mapGetters({
      userIsLogined: 'user/isLogined'
    }),
    isLogin() {
      return this.userIsLogined
    },
    nowFullPath() {
      return this.$route.fullPath
    },
    nowPagename() {
      return this.$route.name
    },
    activeNavType() {
      let type
      if (this.nowPagename === 'Lesson') {
        type = 'lessons'
      } else {
        type = AboutActivePageNameReg.test(this.nowPagename)
          ? 'about'
          : LessonsActivePageNameReg.test(this.nowPagename)
            ? 'lessons'
            : ColumnActivePageNameReg.test(this.nowPagename)
              ? 'column'
              : ''
      }
      return type
    },
    isTeacherPage() {
      return TeacherPageReg.test(this.nowFullPath)
    },
    isStudentPage() {
      return !this.isTeacherPage
    },
    columnText() {
      if (this.isStudentPage) {
        return this.$t('lesson.studentColumn')
      }
      if (this.isTeacherPage) {
        return this.$t('lesson.teacherColumn')
      }
    },
    statusTogglePath() {
      return this.isTeacherPage ? '/student' : '/teacher'
    },
    currentPath() {
      return this.isTeacherPage ? '/teacher' : '/student'
    },
    toggleButtonText() {
      if (this.isStudentPage) {
        return this.$t('lesson.viewTeacherPage')
      }
      if (this.isTeacherPage) {
        return this.$t('lesson.viewStudentPage')
      }
    }
  },
  components: {
    LoginDialog
  },
  methods: {
    ...mapActions({
      toggleLoginDialog: 'lesson/toggleLoginDialog'
    }),
    getSolution(command) {
      this.$router.push({
        path: `${this.currentPath}/solution/${command}`
      })
    },
    hanldOperation(command) {
      switch (command) {
        case 'teaching-video':
          return this.$router.push({
            path: `${this.currentPath}/allteachingvideo/animate`
          })
          break
        case 'download':
          window.open('http://paracraft.keepwork.com/download?lang=zh')
          break
        default:
          break
      }
    },
    switchIdentity() {
      if (!this.userIsLogined) {
        return this.toggleLoginDialog({ show: true })
      }
      let _page = this.$router.resolve({ path: this.statusTogglePath })
      window.open(_page.href, '_blank')
    },
    goToAboutUs() {
      this.isStudentPage
        ? this.$router.push(`/student/about`)
        : this.$router.push(`/teacher/about`)
    },
    goToLessonsCenter() {
      this.isStudentPage
        ? this.$router.push(`/student/center`)
        : this.$router.push(`/teacher/center`)
    },
    goToSpecialColumn() {
      this.isStudentPage
        ? this.$router.push(`/student`)
        : this.$router.push(`/teacher`)
    }
  }
}
</script>



<style lang="scss">
.study-page-header {
  border-bottom: 1px solid #eee;
  &-menu {
    margin: 0 auto;
    max-width: 1200px;
    height: 87px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    &-left {
      &-button {
        padding: 8px 25px;
        color: #909399;
        font-size: 14px;
        background: #f5f5f5;
        border-radius: 4px;
        border: solid 1px #e8e8e8;
        cursor: pointer;
        margin-right: 20px;
        &:hover {
          background: #4db5ff;
          color: #ffffff;
        }
        &.selected {
          background: #409efe;
          color: #ffffff;
        }
      }
    }
    &-right {
      &-dropdown {
        margin-right: 70px;
        cursor: pointer;
        .el-dropdown-link {
          &.selected {
            color: #409efe;
          }
        }
      }
      &-link {
        color: #409efe;
        font-size: 16px;
        cursor: pointer;
        &:hover {
          color: #4db5ff;
        }
        &.selected {
          color: #409efe;
        }
      }
    }
    .el-row {
      margin-right: 0 !important;
      margin-left: 0 !important;
    }
  }
}

@media (max-width: 768px) {
  .study-page-header {
    margin: 0;
    &-menu {
      height: 50px;
      padding: 10px;
      flex-direction: column;
      align-items: flex-start;
      &-left-button {
        margin-right: 0px;
        font-size: 14px;
        padding: 4px 8px;
      }
      &-right {
        &-dropdown {
          margin-right: 0px;
        }
        &-link {
          font-size: 14px;
        }
      }
    }
  }
}

</style>

<template>
  <div class="hint-container">
    <div class="hint-title">{{$t('lesson.teachers')}}</div>
    <vue-markdown :source="content" />
  </div>
</template>


<script>
import VueMarkdown from 'vue-markdown'
export default {
  name: 'Hint',
  components: {
    VueMarkdown
  },
  data() {
    return {}
  },
  mounted() {},
  props: {
    data: Object
  },
  computed: {
    content() {
      return _.get(this.data, 'data.hint.data', '')
    }
  }
}
</script>


<style lang="scss">
.hint-container {
  max-width: 1229px;
  min-height: 100px;
  padding: 20px;
  margin: 0 auto;
  background: #fef6ef;
  box-sizing: border-box;
  .hint-title {
    color: #fd7a05;
    font-weight: 600;
    background: white;
    display: inline-block;
    height: 49px;
    line-height: 38px;
    text-align: center;
    width: 122px;
    background: url('../../../assets/lessonImg/teachers_pop.png') no-repeat
      center center;
  }
  .hint-content {
    white-space: normal;
    word-wrap: break-word;
    margin-top: 20px;
  }
}
</style>

<template>
  <div ref="sticky" class="keep-work-sticky" :style="{'width': `${width}px`}" :class="{'fixed': isFixed}">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'sticky',
  props: {
    width: {
      type: Number,
      default: 1229
    },
    resetTop: {
      type: Number,
      default: 310
    },
    fixedTop: {
      type: Number,
      default: 50
    }
  },
  async mounted() {
    window.addEventListener('scroll', _.debounce(this.handleScroll, 100))
  },
  data() {
    return {
      isFixed: false
    }
  },
  methods: {
    async handleScroll() {
      await this.$nextTick()
      if (!this.$refs.sticky) return
      let clientRect = this.$refs.sticky.getBoundingClientRect()
      let top = clientRect.top
      let scrollTop =
        window.pageYOffset ||
        document.documentElement.scrollTop ||
        document.body.scrollTop
      if (this.isFixed && scrollTop < this.resetTop) {
        this.isFixed = false
      }
      if (!this.isFixed && top < this.fixedTop && top !== 0) {
        this.isFixed = true
      }
    }
  },
  computed: {
    stickyWidth() {
      return `width: ${width}px`
    }
  }
}
</script>


<style lang="scss">
.keep-work-sticky {
  max-width: 100%;
  padding: 30px 0;
  background: #f8f8f8;
  &.fixed {
    padding: 0;
    box-sizing: border-box;
    position: fixed;
    z-index: 200;
    top: 0;
    box-shadow: 1px 1px 5px #dadada;
  }
}
</style>
<style lang="scss" scoped>
@media (max-width: 768px) {
  .keep-work-sticky {
    &.fixed {
      width: 100% !important;
    }
  }
}
</style>

<template>
  <div class="learner-and-teacher">
    <h4 class="learner-and-teacher-title">{{$t('lesson.whatYouWillGet')}}</h4>
    <div class="learner-and-teacher-box">
      <div class="acquire-item" :class="{'learner-and-teacher-teacher': n=== 3}" v-for="n in 3" :key="n">
        <div class="role">
          <div class="role-text">{{getRoleTitle(n)}}</div>
          <span class="role-cost">{{getRolePrice(n)}}</span>
        </div>
        <div class="access">
          <p class="caption">
            <span class="img-wrap"><img src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.selfLearning')}}</p>
          <div class="teaching-function">
            <p>
              <span class="img-wrap"><img src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.learnAmazingLessons')}}<span class="learner-and-teacher-light">({{(n == 1 || n == 2) ? $t('lesson.partiallyFree') : $t('lesson.allFree')}})</span></p>
            <p>
              <span class="img-wrap"><img src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.realTimeFeedback')}}</p>
          </div>
          <p class="caption">
            <span class="img-wrap"><img src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.lessonDevelopment')}}</p>
          <div class="teaching-function">
            <p>
              <span class="img-wrap"><img src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.createLesson')}}</p>
            <p :class="{'not-student-privilege-text': n === 1}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n === 1}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.submitLessons')}}</p>
            <p :class="{'not-student-privilege-text': n === 1}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n === 1}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t("lesson.getBenefit")}}</p>
          </div>
          <p :class="[{'not-student-privilege-text': n <= 2},'caption']">
            <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.classroomTeaching')}}</p>
          <div class="teaching-function">
            <p :class="{'not-student-privilege-text': n <= 2}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.freeForClassroomTeaching')}}</p>
            <p :class="{'not-student-privilege-text': n <= 2}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.freeForClassroomLearning')}}</p>
            <p :class="{'not-student-privilege-text': n <= 2}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.trackStudentsPerformance')}}</p>
            <p :class="{'not-student-privilege-text': n <= 2}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.beShownReport')}}</p>
            <p :class="{'not-student-privilege-text': n <= 2}">
              <span class="img-wrap"><img :class="{'not-student-privilege': n <= 2}" src="@/assets/lessonImg/legal_privilege.png" alt=""></span>{{$t('lesson.trackTeachingProgress')}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LearnerAndTeacher',
  methods: {
    getRoleTitle(index) {
      return index === 1
        ? this.$t('lesson.learners')
        : index === 2
        ? this.$t('lesson.lessonDevelopers')
        : this.$t('lesson.instructors')
    },
    getRolePrice(index) {
      return index === 1
        ? this.$t('lesson.free')
        : index === 2
        ? `￥100${this.$t('lesson.perYearPerPerson')}`
        : `￥5000${this.$t('lesson.perYearPerPerson')}`
    }
  }
}
</script>
<style lang="scss">
.learner-and-teacher {
  padding-bottom: 40px;
  background: #fff;
  &-teacher {
    margin-top: 40px;
  }
  &-light {
    color: #ff742e;
  }
  &-title {
    text-align: center;
    font-size: 24px;
    padding-top: 30px;
  }
  &-box {
    display: flex;
    justify-content: space-around;
    margin: 30px 0;
    .acquire-item {
      max-width: 570px;
      font-size: 14px;
      line-height: 30px;
      // box-shadow: 1px 1px 5px #ddd9d9, -1px -1px 5px #ddd9d9;
      border: 1px solid #eee;
      .role {
        height: 100px;
        text-align: center;
        font-size: 24px;
        color: #333333;
        background: #f7f7f7;
        &-text {
          font-weight: bold;
          color: #333;
          padding-top: 20px;
        }
        &-cost {
          font-size: 18px;
          color: #10c55b;
        }
      }
      .access {
        padding: 44px 25px;
        background: #fff;
        .caption {
          margin-bottom: 2px;
        }
        p {
          padding-left: 24px;
          position: relative;
          .img-wrap {
            margin-right: 8px;
            display: inline-block;
            width: 20px;
            height: 20px;
            top: 6px;
            position: absolute;
            left: 0;
            .not-student-privilege {
              visibility: hidden;
            }
          }
        }
        .not-student-privilege-text {
          color: rgb(179, 177, 177);
        }
        .teaching-function {
          margin-left: 20px;
          p {
            margin: 2px;
          }
        }
      }
    }
  }
}
@media (max-width: 768px) {
  .learner-and-teacher {
    &-box {
      display: block;
      .acquire-item {
        margin-bottom: 20px;
      }
    }
  }
}
</style>

<template>
  <div class="lesson-center">
    <div class="lesson-center-container" v-if="!isPreseting" v-loading='loading'>
      <div class="lesson-center-info">{{$t('lesson.include')}}:
        <span>{{sortedPackagesList.length}}</span> {{$t('lesson.packagesCount')}}
      </div>
      <div class="lesson-center-list">
        <div class="lesson-center-item" v-for="coursePackage in sortedPackagesList" :key="coursePackage.id">
          <img class="lesson-center-item-cover" :src="coursePackage.extra && coursePackage.extra.coverUrl" alt="" @click="enterPackageDetailPage(coursePackage.id)">
          <h4 :title="coursePackage.packageName" class="lesson-center-item-title" @click="enterPackageDetailPage(coursePackage.id)">{{coursePackage.packageName}}</h4>
          <span class="lesson-center-item-info">{{$t('lesson.include')}}: {{coursePackage.lessons.length}} {{$t('lesson.lessonsCount')}}</span>
          <span class="lesson-center-item-info">{{$t('lesson.ages')}}: {{getCoursePackageSuitableAge(coursePackage)}}</span>
          <span class="lesson-center-item-info" :title="coursePackage.intro">{{$t('lesson.intro')}}: {{coursePackage.intro}}</span>
          <div class="lesson-center-item-purchase">
            <div class="lesson-center-item-tip" :class="{'lesson-center-item-hidden': isTeacher || coursePackage.rmb == 0 }" v-html="$t('lesson.backInfo', { backCoinCount: `<span class='lesson-center-item-warning'>${coursePackage.rmb}</span>` })"></div>
            <div class="lesson-center-item-money" :class="{'lesson-center-item-hidden': isTeacher || coursePackage.rmb == 0 }">
              <span class="lesson-center-item-money-item">
                {{$t('lesson.rmbPrice')}}:
                <span class="lesson-center-item-warning">￥{{coursePackage.rmb}}</span>
              </span>
            </div>
            <div class="lesson-center-item-money">
              <span class="lesson-center-item-money-item lesson-center-item-free" v-if="isTeacher || coursePackage.rmb == 0">{{$t('lesson.free')}}</span>
              <span class="lesson-center-item-money-item" v-else>
                {{$t('lesson.coinsPrice')}}:
                <span class="lesson-center-item-warning">{{coursePackage.coin}}</span> {{$t('lesson.coins')}}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="lesson-center-pages" v-if="packagesCount > perPage">
        <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="packagesCount">
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'LessonCenter',
  data() {
    return {
      isPreseting: true,
      loading: true,
      perPage: 15,
      page: 1
    }
  },
  computed: {
    ...mapGetters({
      packages: 'lesson/packagesList',
      isTeacher: 'lesson/isTeacher'
    }),
    packagesList() {
      return _.get(this.packages, 'rows', [])
    },
    packagesCount() {
      return _.get(this.packages, 'count', 0)
    },
    sortedPackagesList() {
      let approvedPackages = _.filter(this.packagesList, i => i.state == 2)
      return approvedPackages.sort(this.sortByUpdateAt)
    }
  },
  async mounted() {
    await this.toGetPackagesList()
    this.isPreseting = false
  },
  methods: {
    ...mapActions({
      getPackagesList: 'lesson/getPackagesList'
    }),
    sortByUpdateAt(obj1, obj2) {
      return obj1.updatedAt >= obj2.updatedAt ? -1 : 1
    },
    enterPackageDetailPage(packageId) {
      if (this.$route.name === 'Lesson') {
        this.$router.push({
          path: `/student/package/${packageId}`
        })
      } else {
        this.$router.push({
          path: `package/${packageId}`
        })
      }
    },
    async toGetPackagesList() {
      this.loading = true
      let params = { perPage: this.perPage, page: this.page }
      await this.getPackagesList(params).catch()
      this.loading = false
      return Promise.resolve()
    },
    async targetPage(targetPage) {
      this.page = targetPage
      await this.toGetPackagesList()
      window.scrollTo(0, 0)
    },
    getCoursePackageSuitableAge(packageDetail) {
      let { minAge, maxAge } = packageDetail
      if (minAge == 0 && maxAge == 0) {
        return this.$t('lesson.packageManage.SuitableForAll')
      }
      return `${minAge}-${maxAge}`
    }
  }
}
</script>

<style lang="scss">
.lesson-center {
  background: #fff;
  &-container {
    max-width: 1200px;
    margin: 0 auto;
  }
  &-info {
    padding: 60px 0 5px;
    font-size: 17px;
  }
  &-list {
    display: flex;
    flex-wrap: wrap;
  }
  &-item {
    width: 360px;
    padding: 34px 36px 6px;
    margin: 20px 60px 20px 0;
    border: solid 2px #d2d2d2;
    border-radius: 1px;
    background: #fff;
    box-sizing: border-box;
    &:nth-child(3n) {
      margin-right: 0;
    }
    &-cover {
      display: inline-block;
      width: 287px;
      height: 160px;
      border-radius: 6px;
      margin: 0 auto;
      object-fit: cover;
      cursor: pointer;
    }
    &-title {
      font-size: 18px;
      margin-bottom: 10px;
      height: 24px;
      cursor: pointer;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #333;
    }
    &-info {
      display: block;
      font-size: 14px;
      line-height: 22px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: #777;
    }
    &-purchase {
      margin: 10px 0;
      border-top: 1px solid #e3e3e3;
    }
    &-tip {
      color: #3491f0;
      margin: 14px 0 5px 0;
      font-size: 14px;
    }
    &-money {
      margin: 2px 0;
      cursor: default;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      &-item {
        font-size: 14px;
        display: inline-block;
        padding: 0 12px;
        height: 27px;
        border: solid 2px #f3f3f3;
        text-align: left;
        line-height: 27px;
        border-radius: 15px;
        max-width: 255px;
        min-width: 132px;
        text-align: center;
      }
    }
    &-hidden {
      visibility: hidden;
    }
    &-free {
      color: #67c23a;
    }
    &-warning {
      color: #e4461f;
      display: inline;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
  &-pages {
    text-align: center;
    padding: 40px 0;
  }
}
@media (max-width: 768px) {
  .lesson-center {
    &-item {
      max-width: 287px;
      box-sizing: border-box;
      padding: 4px 4px 6px;
      border: none;
      margin: 20px auto;
      border-bottom: solid 2px #d2d2d2;
      &:nth-child(3n) {
        margin-right: auto;
      }
    }
    &-cover {
      width: 100%;
    }
  }
}
</style>

<template>
  <el-row class="lesson-header-container">
    <el-dialog class="lesson-header-container-video" :visible.sync="dialogVisible" width="50%">
      <video v-if="dialogVisible" controls="" width="100%" autoplay="" name="media">
        <source :src="videoUrl" type="video/mp4">
      </video>
    </el-dialog>
    <el-dialog :visible.sync="classIdDialogVisible" center custom-class="class-id-dialog" width="600px">
      <div>{{$t('lesson.curentClassId')}}
        <span class="class-id">C{{classroomId}}</span>
      </div>
      <div v-html="$t('lesson.studentEnterClassId',{studentsPerformance:`<span class='performance'>${$t('lesson.studentsPerformance')}</span>`})">
      </div>
      <div class="tips" v-html="$t('lesson.studentAttention',{Attention:`<span class='attention'>${$t('lesson.attention')}</span>`})">
      </div>
      <span slot="footer">
        <el-button @click="classIdDialogVisible = false" class="lesson-confirm-button" type="primary">{{$t('common.Sure')}}</el-button>
      </span>
    </el-dialog>
    <el-dialog :visible.sync="classIdFullScreen" :fullscreen="true" custom-class="class-id-full-page" top="0">
      <div class="full-font">C {{classroomId | idPretty}}</div>
    </el-dialog>
    <el-row>
      <el-col :sm="12" :xm="24" class="lesson-cover" :style="loadCover()" @click.native="openAnimations">
        <img v-if="isHasVideo" src="@/assets/lessonImg/play2.png" alt="">
      </el-col>
      <el-col :sm="12" :xm="24" class="lesson-desc">
        <div v-if="isTeacher && isBeInClass && isInCurrentClass && !isClassIsOver" class="class-id-sign-wrap">
          <el-tooltip placement="bottom">
            <div slot="content">{{$t('lesson.fullPage')}}</div>
            <div class="class-id-sign" @click="classIdToFullScreen"> {{$t('lesson.class')}} ID: C{{classroomId}}</div>
          </el-tooltip>
          <el-tooltip placement="bottom">
            <div slot="content" style="max-width: 400px; font-size: 14px; line-height: 18px; padding:10px 20px;">
              <div v-html="$t('lesson.classIdExplain',{ classId: `<span style='color:red'> ${$t('lesson.class')} ID</span>` })"></div>
            </div>
            <span class="question-mark-icon"></span>
          </el-tooltip>
        </div>
        <div v-if="isSelfLearning" class="class-id-sign-wrap">
          <div class="class-id-sign"> {{$t('lesson.lessonId')}} {{haqiCode}}</div>
          <el-tooltip placement="bottom">
            <div slot="content" style="max-width: 400px; font-size: 14px; line-height: 18px; padding:10px 20px;">
              <div v-html="$t('lesson.haqiIdExplain')"></div>
            </div>
            <span @click="handleExplanHaqiCode" class="question-mark-icon"></span>
          </el-tooltip>
        </div>

        <div class="lesson-info title">
          {{$t('card.lesson')}} {{lessonNo}}: {{lessonName}}
        </div>
        <div class="lesson-info intro">
          <div class="intro-title">
            {{$t('lesson.intro')}}:
          </div>
          <div class="intro-list">
            {{lessonGoals}}
          </div>
          <!-- <el-scrollbar class="intro-list" :native="false"> -->
          <!-- </el-scrollbar> -->
        </div>
        <div class="lesson-info duration">
          <div class="duration-title">{{$t('lesson.duration')}}: </div>
          <div>45 {{$t('lesson.mins')}}</div>
        </div>
        <div class="lesson-info skills">
          <div class="skills-title">
            {{$t('lesson.skillPoints')}}:
          </div>
          <el-scrollbar :class="['skills-list',{'reset-height': isTeacher}]" :native="false">
            <div v-for="(item, index) in lessonSkills" :key="index">{{item}}</div>
          </el-scrollbar>
        </div>
        <div v-if="isTeacher" class="lesson-button-wrap">
          <el-button v-if="isBeInClass && isInCurrentClass" @click="handleDismissTheClass" :disabled="isClassIsOver" type="primary" :class="['lesson-button',{'class-is-over': isClassIsOver}]" size="medium">{{$t('lesson.dismiss')}}</el-button>
          <el-button v-if="(!isBeInClass || !isInCurrentClass) && userIsTeacher" @click="handleBeginTheClass" :disabled="isBeInClass && !isInCurrentClass" type="primary" class="lesson-button" size="medium">{{$t('lesson.begin')}}</el-button>
          <span v-if="isBeInClass && isInCurrentClass" class="lesson-button-tips">{{$t('lesson.dismissTips')}}</span>
          <span v-if="(!isBeInClass || !isInCurrentClass) && userIsTeacher" class="lesson-button-tips">{{$t('lesson.beginTips')}}</span>
        </div>
      </el-col>
    </el-row>
    <keep-work-sticky>
      <el-row v-if="isPreview" :gutter="20" class="lesson-progress-wrap">
        <el-col :span="20" :sm="20">
          <lesson-preview-progress/>
        </el-col>
        <el-col :span="4" :sm="4" class="lesson-references">
          <!-- <lesson-references /> -->
        </el-col>
      </el-row>
      <el-row v-else-if="isTeacher" :gutter="20" class="lesson-progress-wrap">
        <el-col :span="20" :sm="20">
          <lesson-teacher-progress :reset="!isInCurrentClass" />
        </el-col>
        <el-col :span="4" :sm="4" class="lesson-references">
          <!-- <lesson-references /> -->
        </el-col>
      </el-row>
      <el-row v-else :gutter="20" class="lesson-progress-wrap">
        <el-col :span="2" :sm="2" class="lesson-award">
          <!-- <lesson-jewel-box v-if="!isVisitor" /> -->
        </el-col>
        <el-col :span="18" :sm="18">
          <lesson-student-progress :isVisitor="isVisitor" />
        </el-col>
        <el-col :span="4" :sm="4" class="lesson-references">
          <!-- <lesson-references /> -->
        </el-col>
      </el-row>
    </keep-work-sticky>

  </el-row>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from 'axios'
import qs from 'qs'
import _ from 'lodash'
import colI18n from '@/lib/utils/i18n/column'
import LessonJewelBox from '../student/LessonJewelBox'
import LessonStudentProgress from '../student/LessonStudentProgress'
import LessonTeacherProgress from '../teacher/LessonTeacherProgress'
import LessonPreviewProgress from '../preview/LessonPreviewProgress'
import LessonReferences from './LessonReferences'
import KeepWorkSticky from './KeepWorkSticky'
export default {
  name: 'LessonHeader',
  components: {
    LessonJewelBox,
    LessonStudentProgress,
    LessonTeacherProgress,
    KeepWorkSticky,
    LessonReferences,
    LessonPreviewProgress
  },
  filters: {
    idPretty(value) {
      return _.map(_.chunk(value.toString().split(''), 3), i =>
        i.join('')
      ).join(' ')
    }
  },
  props: {
    data: Object,
    isTeacher: {
      type: Boolean,
      default: false
    },
    isInCurrentClass: {
      type: Boolean,
      default: true
    },
    isVisitor: {
      type: Boolean,
      default: false
    },
    isPreview: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dialogVisible: false,
      classIdDialogVisible: false,
      classIdFullScreen: false,
      _interval: null
    }
  },
  methods: {
    ...mapActions({
      beginTheClass: 'lesson/teacher/beginTheClass',
      copyClassroomQuiz: 'lesson/teacher/copyClassroomQuiz',
      dismissTheClass: 'lesson/teacher/dismissTheClass',
      updateLearnRecords: 'lesson/teacher/updateLearnRecords'
    }),
    generateStyleString(style) {
      let string = ''
      _.forEach(style, (value, key) => {
        string = string + key + ':' + value + ';'
      })
      return string
    },
    loadCover() {
      return this.generateStyleString({
        background: 'url(' + this.coverUrl + ')',
        'background-position': 'center',
        'background-size': 'cover',
        'background-color': '#eee',
        opacity: '0.8',
        'border-radius': '8px'
      })
    },
    openAnimations() {
      this.isHasVideo && (this.dialogVisible = true)
    },
    classIdToFullScreen() {
      this.classIdFullScreen = true
    },
    leaveConfirm(event) {
      event.returnValue = 'are you ok?'
    },
    async handleBeginTheClass() {
      if (this.userInfo.identify !== 2) {
        const h = this.$createElement
        // this.$t('lesson.teacherFunction')
        return this.$confirm(
          h(
            'span',
            { style: 'color: #F56C6C' },
            this.$t('lesson.teacherFunction')
          ),
          '',
          {
            confirmButtonText: this.$t('lesson.activate'),
            cancelButtonText: this.$t('lesson.no'),
            type: 'warning',
            customClass: 'teach-function-style'
          }
        )
          .then(() => {
            this.$router.push(`/teacher`)
          })
          .catch(e => {
            console.error(e)
          })
      }
      if (!this.isInCurrentClass) return
      const { packageId, lessonId } = this.$route.params
      await this.beginTheClass({
        packageId: Number(packageId),
        lessonId: Number(lessonId)
      })
        .then(res => {
          this.classIdDialogVisible = true
          this.copyClassroomQuiz()
          this.$emit('intervalUpdateLearnRecords')
          window.addEventListener('beforeunload', this.leaveConfirm, true)
        })
        .catch(e => {
          this.$message.error(this.$t('lesson.beginTheClassFail'))
          this.$emit('clearUpdateLearnRecords')
          console.error(e)
        })
    },
    async handleDismissTheClass() {
      await this.$confirm(
        this.$t('lesson.dismissConfirm'),
        this.$t('lesson.dismiss'),
        {
          type: 'warning',
          distinguishCancelAndClose: true,
          confirmButtonText: this.$t('common.Sure'),
          cancelButtonText: this.$t('common.Cancel'),
          customClass: 'dismiss-class'
        }
      )
        .then(async () => {
          await this.dismissTheClass()
            .then(res => {
              this.$emit('clearUpdateLearnRecords')
              const { lessonId, id } = this.classroom
              this.$router.push({
                name: 'LessonTeacherSummary',
                params: {
                  classId: id,
                  lessonId: Number(lessonId)
                }
              })
              window.removeEventListener(
                'beforeunload',
                this.leaveConfirm,
                true
              )
            })
            .catch(e => {
              this.$message.error(this.$t('lesson.failure'))
              console.error(e)
            })
        })
        .catch(e => console.error(e))
    },
    handleExplanHaqiCode() {
      let helpUrl = 'https://keepwork.com/lesson9527/lessons/help_lessonID '
      window.open(helpUrl)
    }
  },
  computed: {
    ...mapGetters({
      isBeInClass: 'lesson/teacher/isBeInClass',
      classroomId: 'lesson/teacher/classroomId',
      isClassIsOver: 'lesson/teacher/isClassIsOver',
      classroom: 'lesson/teacher/classroom',
      isBeInClassroom: 'lesson/student/isBeInClassroom',
      userInfo: 'lesson/userinfo',
      userIsTeacher: 'lesson/isTeacher'
    }),
    lesson() {
      return this.data
    },
    codeReadLine() {
      return _.get(this.lesson, 'CodeReadLine', 0)
    },
    commands() {
      return _.get(this.lesson, 'Commands', 0)
    },
    codeWriteLine() {
      return _.get(this.lesson, 'CodeWriteLine', 0)
    },
    lessonName() {
      return _.get(this.lesson, 'lessonName', '')
    },
    lessonNo() {
      return _.get(this.lesson, 'packageIndex', '')
    },
    lessonSkills() {
      return _.map(
        _.get(this.lesson, 'skills', []),
        skill => `${colI18n.getLangValue(skill, 'skillName')} +${skill.score}`
      )
    },
    lessonGoals() {
      return _.get(this.lesson, 'goals', '')
    },
    title() {
      return _.get(this.lesson, 'Title', '')
    },
    coverUrl() {
      return _.get(this.lesson, 'extra.coverUrl', '')
    },
    isHasVideo() {
      return Boolean(this.videoUrl)
    },
    videoUrl() {
      return _.get(this.lesson, 'extra.videoUrl', '')
    },
    isSelfLearning() {
      return !this.isTeacher && !this.isBeInClassroom
    },
    haqiCode() {
      const { packageId = 0, lessonId = 0 } = this.$route.params
      return `${packageId}x${lessonId}`
    }
  }
}
</script>


<style lang="scss">
.lesson-header-container {
  max-width: 1229px;
  margin: 50px auto 0;
  $green: #66cd2e;
  $grey: #d2d2d2;
  .class-id-dialog {
    .class-id {
      color: #f75858;
      font-weight: bold;
      font-size: 22px;
    }
    .performance {
      color: #1982ff;
      font-weight: 500;
    }
    .tips {
      margin-top: 20px;
      color: #a9a9a9;
      .attention {
        color: #f75858;
      }
    }
  }

  .lesson-cover {
    height: 340px;
    max-width: 600px;
    cursor: pointer;
    background: #eee;
    opacity: 0.8;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    &:hover {
      opacity: 1 !important;
    }
  }

  .lesson-desc {
    padding-left: 28px;
    box-sizing: border-box;
    position: relative;
    height: 340px;
    .class-id-sign-wrap {
      display: flex;
      align-items: center;
      position: absolute;
      top: -36px;
      .class-id-sign {
        font-size: 20px;
        background: #ed9f21;
        display: inline-block;
        padding: 1px 10px;
        border-radius: 3px;
        color: white;
        cursor: pointer;
      }
      .question-mark-icon {
        display: inline-block;
        cursor: pointer;
        width: 32px;
        height: 32px;
        margin-left: 5px;
        background: url('../../../assets/lessonImg/question_mark.png') no-repeat
          center center;
      }
    }

    .lesson-info {
      display: flex;
      margin-top: 10px;
      &.title {
        font-size: 20px;
        color: #111;
        width: 90%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-family: 'MicrosoftYaHei';
      }
      &.intro {
        color: #4c4c4c;
        font-size: 18px;
        .intro-title {
          margin-right: 10px;
        }
        .intro-list {
          flex: 1;
          line-height: 26px;
          max-height: 78px;
          word-break: break-all;
          overflow-x: none;
          overflow-y: auto;
        }
      }

      &.duration {
        color: #4c4c4c;
        font-size: 16px;
        .duration-title {
          margin-right: 10px;
        }
      }

      &.skills {
        color: #4c4c4c;
        display: flex;
        flex-direction: row;
        .skills-list {
          font-size: 16px;
          height: 90px;
          width: 70%;
          white-space: pre-line;
          line-height: 26px;
          margin-left: 12px;
          &.reset-height {
            height: 100px;
          }
          .el-scrollbar__wrap {
            overflow-x: hidden;
          }
        }
      }
    }
  }
  .lesson-button-wrap {
    margin: 10px 0;
    position: absolute;
    bottom: 0;
    .lesson-button {
      height: 36px;
      width: 190px;
      position: static;
      &.class-is-over {
        background: #d2d2d2;
        border-color: #d2d2d2;
      }
    }
    .lesson-button-tips {
      color: #a9a9a9;
      font-size: 14px;
      margin-left: 5px;
    }
  }
  .lesson-progress-wrap {
    box-sizing: border-box;
    // background: #f8f8f8;
    padding: 26px 20px;
    display: flex;
    align-items: center;
    &.el-row {
      // fix inline elrow style margin-left and right -10px;
      margin: 0 !important;
    }
    .lesson-references {
      display: flex;
      justify-content: flex-end;
    }
  }

  .class-id-dialog {
    .lesson-confirm-button {
      height: 42px;
      width: 158px;
      font-size: 18px;
    }
  }
  .class-id-full-page {
    display: flex;
    align-items: center;
    justify-content: center;
    .full-font {
      font-size: 15vw;
      font-weight: bold;
    }
  }
}
@media screen and (max-width: 768px) {
  .lesson-header-container {
    .lesson-cover {
      height: 200px;
      width: 80%;
      margin: 0 10px;
    }
    &-video {
      .el-dialog {
        width: 90% !important;
      }
    }
    .lesson-progress-wrap {
      &.el-row {
        padding: 16px;
      }
    }
  }
  .teach-function-style {
    max-width: 86%;
  }
  .class-id-dialog {
    max-width: 90%;
  }
  .dismiss-class {
    max-width: 90%;
  }
}
</style>

<template>
  <div>
    <div @click="showReferences" class="lesson-references-wrap">
      <span class="references-icon"></span>
      <span class="references-title">{{$t('lesson.references')}}</span>
    </div>
    <el-dialog :append-to-body="true" class="references-dialog" center :visible.sync="isShowReferences" :title="$t('lesson.references')" @close="closeReferences" width="600px">
      <el-row v-if="false" style="z-index:999" :gutter="20">
        <el-scrollbar class="referencs-files-wrap" :native="false">
          <el-col :span="8" v-for="(file, index) in files" :key="index" class="references-file">
            <span class="file-type" :class="checkFileType(file.type)"></span>
            <span class="references-file-name">{{file.name}}</span>
          </el-col>
        </el-scrollbar>
      </el-row>
      <div v-else class="references-no-files">
        <img class="references-no-files-icon" src="@/assets/lessonImg/no_packages.png">
        <div class="references-no-files-title">{{$t('lesson.noReference')}}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Referencs',
  props: {
    data: Object
  },
  data() {
    return {
      isShowReferences: false,
      files: [
        {
          type: 'txt',
          name: 'file1'
        },
        {
          type: 'pdf',
          name: 'file2'
        },
        {
          type: 'word',
          name: 'file3'
        },
        {
          type: 'excel',
          name: 'file4'
        },
        {
          type: 'mp3',
          name: 'file5'
        },
        {
          type: 'gif',
          name: 'file6'
        },
        {
          type: 'rar',
          name: 'file6'
        },
        {
          type: 'mp4',
          name: 'file6'
        },
        {
          type: 'movie',
          name: 'file6'
        },
        {
          type: 'mp411',
          name: 'file6'
        }
      ]
    }
  },
  methods: {
    showReferences() {
      this.isShowReferences = true
    },
    closeReferences() {
      this.isShowReferences = false
    },
    checkFileType(type) {
      switch (type) {
        case 'excel':
          return 'excel'
        case 'mp3':
          return 'mp3'
        case 'mp4':
          return 'mp4'
        case 'pdf':
          return 'pdf'
        case 'gif':
          return 'gif'
        case 'rar':
          return 'rar'
        case 'txt':
          return 'txt'
        case 'word':
          return 'word'
        case 'movie':
          return 'movie'
        default:
          return 'unknown'
      }
    }
  }
}
</script>

<style lang="scss">
.lesson-references-wrap {
  display: flex;
  align-items: center;
  cursor: pointer;
  .references {
    &-icon {
      display: inline-block;
      height: 16px;
      width: 23px;
      background: url('../../../assets/lessonImg/references.png') no-repeat
        center #fff;
    }
    &-title {
      color: #818181;
      font-weight: bold;
      margin-left: 10px;
    }
  }
}

.references-dialog {
  .references-no-files {
    text-align: center;
    padding-top: 60px;
    &-icon {
      width: 220px;
    }
    &-title {
      font-size: 20px;
      margin-top: 20px;
    }
  }
  .el-dialog__body {
    padding: 0 10px 0;
  }
  .referencs-files-wrap {
    height: 500px;
    .el-scrollbar__wrap {
      overflow-x: hidden;
    }
  }
  .references-file {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    &-name {
      margin-top: 15px;
      cursor: pointer;
    }
  }
  .el-dialog__header {
    padding: 0;
    background: #409efe;
    .el-dialog__title {
      display: block;
      color: white;
      padding: 10px;
    }
    .el-dialog__headerbtn {
      top: 16px;
      .el-dialog__close {
        color: white;
      }
    }
  }
  .el-dialog__body {
    min-height: 350px;
  }
}

.file-type {
  display: block;
  height: 129px;
  width: 111px;
  cursor: pointer;
  &.excel {
    background: url('../../../assets/lessonImg/fileType/excel.png') no-repeat
      center #fff;
  }
  &.gif {
    background: url('../../../assets/lessonImg/fileType/gif.png') no-repeat
      center #fff;
  }
  &.movie {
    background: url('../../../assets/lessonImg/fileType/movie.png') no-repeat
      center #fff;
  }
  &.mp3 {
    background: url('../../../assets/lessonImg/fileType/mp3.png') no-repeat
      center #fff;
  }
  &.mp4 {
    background: url('../../../assets/lessonImg/fileType/mp4.png') no-repeat
      center #fff;
  }
  &.pdf {
    background: url('../../../assets/lessonImg/fileType/mp4.png') no-repeat
      center #fff;
  }
  &.rar {
    background: url('../../../assets/lessonImg/fileType/rar.png') no-repeat
      center #fff;
  }
  &.txt {
    background: url('../../../assets/lessonImg/fileType/txt.png') no-repeat
      center #fff;
  }
  &.unknown {
    background: url('../../../assets/lessonImg/fileType/unknown.png') no-repeat
      center #fff;
  }
  &.word {
    background: url('../../../assets/lessonImg/fileType/word.png') no-repeat
      center #fff;
  }
}
</style>

<template>
  <div>
    <hint v-if="isTeacher && mod.cmd === 'Hint' && isShowHint" :data="mod" :key="mod.key"></hint>
    <quiz v-else-if="mod.cmd === 'Quiz'" :data="mod" :isPreview="isPreview" :isPrint="isPrint" :isVisitor="isVisitor" :key="mod.key"></quiz>
    <div v-else class="mod-item-container">
      <mod-loader :mod="mod" :theme="theme" :key="mod.key"></mod-loader>
    </div>

  </div>
</template>

<script>
import ModLoader from '@/components/viewer/ModLoader'
import themeFactory from '@/lib/theme/theme.factory'
import ThemeHelper from '@/lib/theme'
import Quiz from './Quiz'
import Hint from './Hint'
import { mapGetters } from 'vuex'
export default {
  name: 'LessonWrap',
  components: {
    Quiz,
    Hint,
    ModLoader
  },
  props: {
    mod: Object,
    originData: Array,
    modList: Array,
    isPreview: {
      type: Boolean,
      default: false
    },
    isPrint: {
      type: Boolean,
      default: false
    },
    isTeacher: {
      type: Boolean,
      default: false
    },
    isVisitor: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters({
      isShowHint: 'lesson/teacher/isShowHint'
    }),
    theme() {
      let newTheme = themeFactory.generate(ThemeHelper.defaultTheme)
      if (this.storedTheme === newTheme) return this.storedTheme
      if (this.storedTheme) this.storedTheme.sheet.detach()
      this.storedTheme = newTheme
      this.storedTheme.sheet.attach()
      return this.storedTheme
    }
  }
}
</script>

<style lang="scss">
.mod-item-container {
  background: white;
  max-width: 100%;
  overflow: auto;
  margin: 0 auto;
}
</style>

<template>
  <div class="lesson-wrap-by-glass">
    <div :class="{'forsted-glass-shade': isForbidden }">
      <lesson-wrap v-for="mod in lessonMain" :key="mod.key" :mod="mod" />
    </div>
    <div class="org-list" v-if="isForbidden">
      <div class="org-title">
        <span class="org-title-icon"></span>
        <span>观看完整内容需要向机构购买</span>
      </div>
      <div class="org-list-item" v-for="item in organizations" :key="item.name">
        <span class="org-list-item-name">
          {{item.name}}
        </span>
        <span class="org-list-item-cellphone">
          {{item.cellphone}}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import LessonWrap from './LessonWrap'
export default {
  name: 'LessonWrapByGlass',
  components: {
    LessonWrap
  },
  props: {
    lessonMain: {
      type: Array,
      default() {
        return []
      }
    },
    organizations: {
      type: Array,
      default() {
        return []
      }
    },
    authUserPrivilege: {
      type: Number,
      default: 1
    }
  },
  computed: {
    isForbidden() {
      return this.authUserPrivilege === 0
    }
  },
  methods: {
    stopClick(e) {
      return e.stopPropagation()
    }
  }
}
</script>

<style lang="scss" scoped>
.lesson-wrap-by-glass {
  position: relative;
  .forsted-glass-shade {
    pointer-events: none;
    cursor: not-allowed;
    user-select: none;
    min-height: 600px;
    opacity: 0.6;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 8;
    filter: blur(10px);
  }
  .org-list {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    margin: 100px auto 0;
    z-index: 10;
    width: 459px;
    min-height: 200px;
    box-sizing: border-box;
    background-color: #ffffff;
    box-shadow: 0px 4px 12px 0px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    border: solid 1px #e8e8e8;
    padding: 50px;
    &-item {
      text-align: center;
      font-size: 16px;
      margin-top: 20px;
      &-name {
        color: #333;
        margin-right: 30px;
      }
      &-cellphone {
        color: #999;
      }
    }
    .org-title {
      font-size: 24px;
      color: #303133;
      text-align: center;
      height: 80px;
      display: flex;
      justify-content: center;
      align-items: center;
      line-height: 80px;
      &-icon {
        display: inline-block;
        height: 45px;
        width: 32px;
        margin-right: 10px;
        background: url('../../../assets/lessonImg/lock.png') no-repeat;
      }
    }
  }
}
</style>

<template>
  <div class="lesson-markdown-container">
    <div class="lesson-markdown-icon-wrap">
      <i class="lesson-markdown-icon"></i>
    </div>
    <vue-markdown :source="mdStr" />
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'
export default {
  name: 'LessonMarkdown',
  components: {
    VueMarkdown
  },
  props: {
    data: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  computed: {
    mdStr() {
      return this.data.data.md.data
    },
    mdArr() {
      return this.data.md
    }
  }
}
</script>


<style lang="scss">
.lesson-markdown-container {
  padding: 10px 15px;
  max-width: 1229px;
  box-sizing: border-box;
  margin: 0 auto;
  background: white;
  display: flex;
  flex-direction: row;
  .lesson-markdown-icon-wrap {
    width: 100px;
    .lesson-markdown-icon {
      display: inline-block;
      height: 72px;
      width: 61px;
      background: url('../../../assets/lessonImg/markdown.png') no-repeat center
        #fff;
    }
  }
}
</style>

<template>
  <div class="parent-more-container">
    <combo-box :routes="routes"></combo-box>
  </div>
</template>

<script>
import ComboBox from '@/components/combo/ComboBox'
export default {
  name: 'MoreResources',
  components: {
    ComboBox
  },
  data() {
    return {
      routes: {
        offline: {
          projectName: 'official/paracraft',
          filePath: 'offline-courses'
        },
        mentor: {
          projectName: 'official/paracraft',
          filePath: 'learn/mentor_service'
        },
        our_ideas_view_more: {
          projectName: 'official/paracraft',
          filePath: 'learn/our_ideas_view_more'
        }
      },
      currentFilePath: ''
    }
  },
  mounted() {
    const { params: { command } } = this.$route
    const { projectName, filePath } = this.routes[command]
    this.currentFilePath = filePath
  },
  watch: {
    $route(to) {
      const { params: { command } } = to
      const { projectName, filePath } = this.routes[command]
      this.currentFilePath = filePath
    }
  }
}
</script>

<style lang="scss">
.parent-more-container {
  background: #fff;
  max-width: 1200px;
  margin: 0 auto;
  div[data-mod] {
    .el-row {
      width: auto;
      max-width: 1200px;
    }
    .el-carousel__container {
      width: auto;
      max-width: 1200px;
    }
  }
}
</style>

<template>
  <el-dialog class="operate-result-dialog" :class="{'operate-result-dialog-danger': infoDialogData.type === 'danger'}" :visible.sync="isInfoDialogVisible" width="560px" :before-close="handleClose">
    <i class="iconfont" :class="iconClass"></i>
    <div class="operate-result-dialog-para" :class="{'operate-result-dialog-danger-text': index === 0}" v-for="(para, index) in infoDialogData.paras" :key="index">{{para}}</div>
    <span slot="footer" class="operate-result-dialog-footer">
      <el-button @click="handleClose" v-if="cancelButtonText">{{cancelButtonText}}</el-button>
      <el-button type="primary" @click="handleEnsure">{{continueButtonText || $t('common.Sure')}}</el-button>
    </span>
  </el-dialog>
</template>
<script>
export default {
  name: 'OperateResultDialog',
  props: {
    infoDialogData: Object,
    isInfoDialogVisible: Boolean
  },
  computed: {
    continueButtonText() {
      return _.get(this.infoDialogData, 'continueButtonText')
    },
    cancelButtonText() {
      return _.get(this.infoDialogData, 'cancelButtonText')
    },
    iconClass() {
      let iconClassName = ''
      switch (this.infoDialogData.iconType) {
        case 'submit':
          iconClassName = 'icon-submit'
          break
        case 'delete':
          iconClassName = 'icon-delete'
          break
        case 'release':
          iconClassName = 'icon-Release'
          break
        case 'revoca':
          iconClassName = 'icon-recall'
          break
        default:
          break
      }
      return iconClassName
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },
    handleEnsure() {
      this.$emit('close', this.infoDialogData.continueFnNameAfterEnsure)
    }
  }
}
</script>

<style lang="scss">
.operate-result-dialog {
  text-align: center;
  .el-dialog {
    max-width: 100%;
  }
  .el-icon-close {
    font-size: 20px;
    color: #cecece;
    font-weight: bold;
  }
  .el-dialog__body {
    font-size: 16px;
    color: #414141;
    padding: 30px 20px 0;
  }
  &-danger {
    &-text {
      color: #f75858;
    }
  }
  .iconfont {
    font-size: 88px;
    color: #cecece;
    line-height: 1;
    margin-bottom: 28px;
    display: inline-block;
  }
  .el-dialog__footer {
    padding: 30px 0;
    text-align: center;
  }
  .el-button {
    width: 103px;
    font-size: 17px;
  }
  .el-button + .el-button {
    margin-left: 30px;
  }
  &-para {
    margin-bottom: 14px;
  }
}
</style>

<template>
  <div class="package-basic-detail">
    <div class="package-basic-detail-cover">
      <div class="package-basic-detail-cover-wrap">
        <img class="package-basic-detail-cover-inner" :src="packageCoverUrl" alt="">
      </div>
    </div>
    <div class="package-basic-detail-text-desc">
      <h1>{{packageDetail.packageName}}</h1>
      <div class="package-basic-detail-content">
        <div class="package-basic-detail-content-item">
          <span class="package-basic-detail-label">{{$t('lesson.include')}}:</span>
          <span class="package-basic-detail-lessons-count">{{packageLessonsCount}}</span>
          <span class="package-basic-detail-info">{{$t('lesson.lessonsCount')}}</span>
        </div>
        <div class="package-basic-detail-content-item">
          <span class="package-basic-detail-label">{{$t('lesson.ages')}}:</span>
          <span class="package-basic-detail-info">{{packageSuitableAge}}</span>
        </div>
      </div>
      <div class="package-basic-detail-skills">
        <div class="package-basic-detail-label">{{$t('lesson.intro')}}:</div>
        <el-scrollbar class="package-basic-detail-skills-detail" :class="{'package-basic-detail-skills-detail-isSubscribe': !isPackageCostAndBackShow && !isFreeLabelShow && isPurchaseButtonHide}">{{packageDetail.intro}}</el-scrollbar>
      </div>
      <div v-show="!isPendingReview && isPackageCostAndBackShow" class="package-basic-detail-backcoin" v-html="$t('lesson.backInfo', { backCoinCount: backCoinHtml })">
      </div>
      <div v-show="!isPendingReview && isPackageCostAndBackShow" class="package-basic-detail-costs">
        <div class="package-basic-detail-costs-item">
          <span class="package-basic-detail-costs-label">{{$t('lesson.rmbPrice')}}:</span>
          <span class="package-basic-detail-costs-value">￥ {{packageDetail.rmb}}</span>
          <el-button v-show="!isPreview && !isPendingReview && !isPurchaseButtonHide" class="package-basic-detail-costs-button" type="warning" @click="addPackage('rmb')">{{$t('lesson.add')}}</el-button>
        </div>
        <div class="package-basic-detail-costs-item">
          <span class="package-basic-detail-costs-label">{{$t('lesson.coinsPrice')}}:</span>
          <span class="package-basic-detail-costs-value">{{packageDetail.coin}} {{$t('lesson.coins')}}</span>
          <el-button v-show="!isPreview && !isPendingReview && !isPurchaseButtonHide" class="package-basic-detail-costs-button" type="primary" @click="addPackage('coin')">{{$t('lesson.add')}}</el-button>
        </div>
      </div>
      <div v-show="!isPendingReview && isFreeLabelShow" class="package-basic-detail-free">{{$t('lesson.free')}}</div>
      <div v-if="isPendingReview" class="package-basic-detail-warning">{{$t('lesson.Unapproved')}}</div>
      <el-button v-if="!isPreview" v-show="!isPendingReview && !isPurchaseButtonHide && !isPackageCostAndBackShow" type="primary" class="package-basic-detail-operate-button" @click="addPackage">{{$t('lesson.add')}}</el-button>
      <div @click.stop v-if="isLoginDialogShow">
        <login-dialog :show="isLoginDialogShow" @close="closeLoginDialog"></login-dialog>
      </div>
    </div>
  </div>
</template>
<script>
import _ from 'lodash'
import { mapGetters, mapActions } from 'vuex'
import LoginDialog from '@/components/common/LoginDialog'
export default {
  name: 'PackageBasicDetail',
  props: {
    packageDetail: Object,
    actorType: String,
    isPreview: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    if (!this.userIsLogined) {
      this.userGetProfile({ forceLogin: false })
        .then(() => {
          this.isLogin = true
        })
        .catch(() => {
          this.isLogin = false
        })
    }
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/profile',
      userIsLogined: 'user/isLogined',
      isLoginUserBeTeacher: 'lesson/isTeacher'
    }),
    isLogin: {
      get() {
        return this.userIsLogined
      },
      set() {}
    },
    isTeacher() {
      return this.actorType === 'teacher'
    },
    loginUserId() {
      return _.get(this.userProfile, 'id')
    },
    packageOwnerId() {
      return _.get(this.packageDetail, 'userId')
    },
    isOwnPackage() {
      return this.loginUserId === this.packageOwnerId
    },
    isUserSubscribePackage() {
      if (this.isPackageFree || this.isLoginUserBeTeacher) {
        return this.isOwnPackage || this.packageDetail.isSubscribe
      }
      return (
        this.isOwnPackage ||
        (this.packageDetail.isSubscribe && this.packageDetail.isBuy)
      )
    },
    isPackageFree() {
      return (
        this.isLoginUserBeTeacher ||
        this.packageDetail.rmb === 0 ||
        this.packageDetail.coin === 0
      )
    },
    isPackageCostAndBackShow() {
      return !this.isPackageFree && !this.isUserSubscribePackage
    },
    isFreeLabelShow() {
      return this.isPackageFree && !this.isUserSubscribePackage
    },
    nowPath() {
      return this.$route.path
    },
    nowPageName() {
      return this.$route.name
    },
    purchasePath() {
      return this.nowPath + '/purchase'
    },
    packageLessonsCount() {
      return _.get(this.packageDetail, 'lessons', []).length
    },
    packageCoverUrl() {
      return _.get(this.packageDetail, 'extra.coverUrl', '')
    },
    packageId() {
      return _.get(this.packageDetail, 'id')
    },
    backCoinHtml() {
      return `<span>${this.packageDetail.rmb}</span>`
    },
    isPurchaseButtonHide() {
      return (
        this.isUserSubscribePackage ||
        this.nowPageName === 'StudentPurchase' ||
        this.nowPageName === 'TeacherPurchase'
      )
    },
    packageSuitableAge() {
      let { minAge, maxAge } = this.packageDetail
      if (minAge == 0 && maxAge == 0) {
        return this.$t('lesson.packageManage.SuitableForAll')
      }
      return `${minAge}-${maxAge}`
    },
    isPendingReview() {
      return this.packageDetail.state !== 2
    }
  },
  data() {
    return {
      isLoginDialogShow: false
    }
  },
  methods: {
    ...mapActions({
      lessonSubscribePackage: 'lesson/subscribePackage',
      userGetProfile: 'user/getProfile'
    }),
    async addPackage(payment) {
      if (this.isLogin) {
        if (this.isPackageFree) {
          await this.lessonSubscribePackage({ packageId: this.packageId })
          this.$message({
            message: this.$t('lesson.addPackageSuccess'),
            type: 'success'
          })
          return
        }
        window.location.href = `${window.location.origin}/a/orderConfirm?id=${
          this.packageId
        }&type=2&payment=${payment}`
        // this.$router.push({
        //   path: this.purchasePath
        // })
      } else {
        this.isLoginDialogShow = true
      }
    },
    closeLoginDialog() {
      this.isLoginDialogShow = false
    }
  },
  components: {
    LoginDialog
  }
}
</script>
<style lang="scss">
$dangerColor: #e4461f;
.package-basic-detail {
  display: flex;
  &-cover {
    width: 436px;
    &-wrap {
      padding-bottom: 56.25%;
      position: relative;
    }
    &-inner {
      position: absolute;
      top: 0;
      left: 0;
      object-fit: cover;
      width: 100%;
      height: 100%;
    }
  }
  &-text-desc {
    flex: 1;
    margin-left: 25px;
    color: #4c4c4c;
    min-width: 0;
  }
  &-content {
    margin: 12px 0;
    &-item {
      display: inline-block;
      margin-right: 30px;
      font-size: 18px;
    }
  }
  h1 {
    margin: 0;
    font-size: 20px;
    color: #111;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }
  &-label {
    font-size: 18px;
    margin-right: 3px;
  }
  &-info {
    color: #818181;
  }
  &-lessons-count {
    color: $dangerColor;
  }
  &-skills-detail {
    margin: 0;
    height: 70px;
    white-space: pre-line;
    font-size: 16px;
    line-height: 30px;
    &-isSubscribe {
      height: 146px;
    }
  }
  &-backcoin {
    color: #3491f0;
    font-size: 16px;
    margin-top: 6px;
    span {
      color: $dangerColor;
    }
  }
  &-costs {
    margin: 7px 0;
    &-item {
      display: inline-flex;
      align-items: center;
      border: 1px solid #f3f3f3;
      background-color: #fff;
      margin-right: 16px;
      margin-top: 4px;
      font-size: 16px;
      color: #111;
      padding: 0 1px 0 10px;
      height: 32px;
      line-height: 32px;
      box-sizing: border-box;
      border-radius: 32px;
      border: solid 2px #eeeeee;
    }
    &-value {
      color: $dangerColor;
    }

    &-button {
      height: 26px;
      box-sizing: border-box;
      border-radius: 26px;
      padding: 6px 13px;
      margin-left: 20px;
    }
  }
  &-free {
    font-size: 24px;
    color: #7ac558;
    margin: 24px 0;
  }
  &-warning {
    border-radius: 4px;
    background: #e6a23c;
    color: white;
    margin: 24px 0;
    width: 160px;
    height: 30px;
    line-height: 30px;
    text-align: center;
  }
  &-operate-item {
    display: inline-block;
  }
  &-price-count {
    font-size: 24px;
    color: #ff4c4c;
  }
}
@media screen and (max-width: 768px) {
  .package-basic-detail {
    display: block;
    &-cover {
      width: 90%;
      margin: 20px;
    }
  }
}
</style>
<style lang="scss">
.el-scrollbar__wrap {
  overflow-x: auto;
}
</style>

<template>
  <div class="package-catalogue">
    <div class="package-catalogue-progress" v-show="isUserSubscribePackage && !isTeacher">
      <div class="package-catalogue-progress-detail">
        <el-progress :show-text='false' :stroke-width="18" :percentage="lessonProgressPercent"></el-progress>
        <el-button type="primary" :disabled="lessonProgressPercent === 100" class="package-catalogue-progress-button" @click="continueToLearn">{{buttonText}}</el-button>
      </div>
      <p>{{lessonProgressInfo}}</p>
    </div>
    <div class="package-catalogue-title">{{$t('lesson.catalogue')}}</div>
    <div class="package-catalogue-box">
      <div class="package-catalogue-item" :class="{'package-catalogue-item-disabled': !isPreview && !isPendingReview && !isUserSubscribePackage}" v-for="(lesson, index) in lessonsList" :key='index' @click='handleUnSubscribe'>
        <div class="package-catalogue-item-cover-box">
          <div class="package-catalogue-item-mark" v-show="lesson.isFinished">
            <i class="el-icon-check"></i>
          </div>
          <div class="package-catalogue-item-cover" @click="toLessonDetail(lesson)">
            <div class="package-catalogue-item-cover-wrap">
              <img class="package-catalogue-item-cover-inner" :src="lesson.extra.coverUrl" alt="">
            </div>
          </div>
        </div>
        <div class="package-catalogue-item-detail">
          <div class="package-catalogue-item-title" @click="toLessonDetail(lesson)">
            <span>{{$t('lesson.lessonIndexLabel') + (index + 1) + ": " + lesson.lessonName}}</span>
          </div>
          <div class="package-catalogue-item-info">{{$t('lesson.intro')}}:</div>
          <div class="package-catalogue-item-goals">
            <p class="package-catalogue-item-goals-item">{{lesson.goals}}</p>
          </div>
          <div class="package-catalogue-item-duration">{{$t('lesson.duration')}}:
            <span>45{{$t('lesson.minUnit')}}</span>
          </div>
          <el-button v-show="lesson.isFinished && !isTeacher" type="primary" size="small" class="package-catalogue-item-button" @click="toViewSummary(lesson)">{{$t('lesson.viewLearnSummary')}}</el-button>
          <el-button v-show="lesson.isFinished && !isTeacher" plain size="small" class="package-catalogue-item-button learn-again" @click="toLearnAgain(lesson)">{{$t('lesson.learnAgain')}}</el-button>
          <el-button v-show="!lesson.isFinished && !isTeacher" type="primary" size="small" class="package-catalogue-item-button start-button" @click="toLessonDetail(lesson)">{{$t('card.startToLearn')}}</el-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { lesson } from '@/api'
import _ from 'lodash'
export default {
  name: 'PackageCatalogue',
  props: {
    packageDetail: Object,
    actorType: String,
    isPreview: {
      type: Boolean,
      default: false
    },
    previewToken: String
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/profile',
      enterClassInfo: 'lesson/student/enterClassInfo',
      isBeInClassroom: 'lesson/student/isBeInClassroom',
      isLoginUserBeTeacher: 'lesson/isTeacher'
    }),
    loginUserId() {
      return _.get(this.userProfile, 'id')
    },
    packageOwnerId() {
      return _.get(this.packageDetail, 'userId')
    },
    isOwnPackage() {
      return this.loginUserId === this.packageOwnerId
    },
    isPackageFree() {
      return (
        this.isLoginUserBeTeacher ||
        this.packageDetail.rmb === 0 ||
        this.packageDetail.coin === 0
      )
    },
    isUserSubscribePackage() {
      if (this.isPackageFree || this.isLoginUserBeTeacher) {
        return this.isOwnPackage || this.packageDetail.isSubscribe
      }
      return (
        this.isOwnPackage ||
        (this.packageDetail.isSubscribe && this.packageDetail.isBuy)
      )
    },
    isInClassroom() {
      const state = this.enterClassInfo.state
      return state == undefined ? false : state != 2
    },
    lessonsList() {
      let lessons = _.get(this.packageDetail, 'lessons', [])
      _.map(this.lessonFinishedList, finishedLessonId => {
        let finishedLessonInLessonListIndex = _.findIndex(lessons, lesson => {
          return lesson.id === finishedLessonId
        })
        lessons[finishedLessonInLessonListIndex].isFinished = true
      })
      return lessons
    },
    continueLearnedLesson() {
      let lastLessonId = this.learnedLessons[this.learnedLessons.length - 1]
      if (lastLessonId) {
        let lastLessonIndex = _.findIndex(
          this.lessonsList,
          lesson => lesson.id === lastLessonId
        )
        while (++lastLessonIndex < this.lessonsList.length) {
          if (!this.lessonsList[lastLessonIndex].isFinished) {
            return this.lessonsList[lastLessonIndex]
          }
        }
      }
      return _.find(this.lessonsList, lesson => !lesson.isFinished)
    },
    learnedLessons() {
      return _.get(this.packageDetail, 'learnedLessons', [])
    },
    teachedLessons() {
      return _.get(this.packageDetail, 'teachedLessons', [])
    },
    lessonFinishedList() {
      return this.actorType === 'teacher'
        ? this.teachedLessons
        : this.learnedLessons
    },
    lessonProgressPercent() {
      return (
        (this.lessonFinishedList.length / this.lessonsList.length) * 100 || 0
      )
    },
    lessonProgressInfo() {
      return (
        this.$t('lesson.haveLearn') +
        this.lessonFinishedList.length +
        this.$t('lesson.lessonsCount')
      )
    },
    buttonText() {
      return this.lessonProgressPercent === 100
        ? this.$t('lesson.finished')
        : this.$t('lesson.continue')
    },
    isTeacher() {
      return this.actorType === 'teacher'
    },
    isPendingReview() {
      return this.packageDetail.state === 0 || this.packageDetail.state === 1
    }
  },
  methods: {
    toLessonDetail(lesson) {
      if (this.isPreview) {
         return this.$router.push({
          path: `/preview/package/${this.packageDetail.id}/lesson/${lesson.id}?token=${this.previewToken}`
        })
      }
      if (!this.isTeacher && this.isPendingReview) {
        return this.$message({
          type: 'warning',
          message: this.$t('lesson.packagePendingReview')
        })
      }
      if (this.isBeInClassroom) {
        const {
          name,
          params: { id: _packageId }
        } = this.$route
        const { packageId, lessonId } = this.enterClassInfo
        if (
          name === 'StudentPackage' &&
          (_packageId != packageId || lesson.id != lessonId)
        )
          return this.$message.error(this.$t('lesson.beInClass'))
      }
      if (this.isUserSubscribePackage) {
        let targetLessonPath = `/${this.actorType}/package/${
          this.packageDetail.id
        }/lesson/${lesson.id}`
        if (this.$route.name === 'StudentPackage') {
          return this.toLearnConfirm(
            this.packageDetail.id,
            lesson.id,
            targetLessonPath
          )
        }
        this.$router.push({
          path: targetLessonPath
        })
      }
    },
    handleUnSubscribe() {
      if (!this.isPreview && !this.isPendingReview && !this.isUserSubscribePackage) {
        this.$alert(
          this.$t('lesson.addPackageFirst'),
          this.$t('lesson.infoTitle')
        )
      }
    },
    toViewSummary(lesson) {
      let targetLessonPath = `/${this.actorType}/learnSummary/package/${
        this.packageDetail.id
      }/lesson/${lesson.id}`
      this.$router.push({
        path: targetLessonPath
      })
    },
    continueToLearn() {
      if (!this.isTeacher && this.isPendingReview) {
        return this.$message({
          type: 'warning',
          message: this.$t('lesson.packagePendingReview')
        })
      }
      if (this.isBeInClassroom) {
        return this.$message.error(this.$t('lesson.beInClass'))
      }
      let targetLessonPath = `/${this.actorType}/package/${
        this.packageDetail.id
      }/lesson/${this.continueLearnedLesson.id}`
      this.toLearnConfirm(
        this.packageDetail.id,
        this.continueLearnedLesson.id,
        targetLessonPath
      )
    },
    toLearnAgain(lesson) {
      if (!this.isTeacher && this.isPendingReview) {
        return this.$message({
          type: 'warning',
          message: this.$t('lesson.packagePendingReview')
        })
      }
      if (this.isBeInClassroom) {
        return this.$message.error(this.$t('lesson.beInClass'))
      }
      let targetLessonPath = `/${this.actorType}/package/${
        this.packageDetail.id
      }/lesson/${lesson.id}`
      return this.toLearnConfirm(
        this.packageDetail.id,
        lesson.id,
        targetLessonPath
      )
    },
    async toLearnConfirm(_packageId, _lessonId, path) {
      let res = await lesson.lessons
        .getLastLearnRecords()
        .catch(e => console.error(e))
      let lastLearnRecods = _.get(res, 'rows', [])
      if (lastLearnRecods.length === 0) {
        return this.$router.push({
          path
        })
      }
      if (lastLearnRecods[0].state === 1) {
        return this.$router.push({
          path
        })
      }

      const { packageId, lessonId } = lastLearnRecods[0]
      if (_packageId === packageId && _lessonId === lessonId) {
        return this.$router.push({
          path
        })
      }
      this.$confirm(this.$t('lesson.learnLessonConfirm'), '', {
        confirmButtonText: this.$t('common.Yes'),
        cancelButtonText: this.$t('common.No'),
        type: 'warning',
        customClass: 'leave-current-class'
      })
        .then(() => this.$router.push({ path }))
        .catch(e => console.error(e))
    }
  }
}
</script>
<style lang="scss" scoped>
.package-catalogue {
  padding-bottom: 30px;
  &-progress {
    padding: 13px 20px;
    color: #818181;
    font-size: 14px;
    &-detail {
      .el-progress {
        width: 760px;
        max-width: 86%;
        display: inline-block;
        vertical-align: bottom;
      }
    }
    &-button {
      padding: 10px 14px;
      margin-left: 22px;
    }
    p {
      margin: 5px 0 0;
    }
  }
  &-title {
    font-size: 16px;
    color: #333;
    height: 50px;
    line-height: 50px;
    padding: 0 20px;
    font-weight: bold;
    background-color: #fff;
    border: 1px solid #e5e5e5;
    border-bottom: none;
  }
  &-item {
    background-color: #fff;
    border: 1px solid #e5e5e5;
    padding: 16px 20px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #333;
    font-weight: lighter;
    &-cover-box {
      margin-right: 22px;
      position: relative;
      padding-left: 19px;
    }
    &-cover {
      width: 234px;
      cursor: pointer;
      &-wrap {
        padding-bottom: 56.25%;
        position: relative;
      }
      &-inner {
        position: absolute;
        top: 0;
        left: 0;
        object-fit: cover;
        width: 100%;
        height: 100%;
      }
    }
    &-detail {
      flex: 1;
      min-width: 0;
    }
    &-title {
      margin: 12px 0 8px;
      font-size: 18px;
      color: #181818;
      font-weight: normal;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
      cursor: pointer;
    }
    &-disabled {
      background-color: #bfbfbf;
      cursor: not-allowed;
    }
    &-disabled &-title,
    &-disabled &-cover {
      cursor: not-allowed;
    }
    &-info {
      color: #999;
    }
    &-duration {
      margin: 25px 0 15px;
    }
    &-mark {
      position: absolute;
      top: -4px;
      left: 0;
      font-size: 14px;
      color: #67c23a;
      z-index: 1;
      .el-icon-check {
        font-weight: bold;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background-color: #67c23a;
        color: #fff;
        text-align: center;
        line-height: 38px;
        font-size: 24px;
        margin-left: 4px;
        vertical-align: middle;
        border: 2px solid #fff;
      }
    }
    &-button {
      margin-bottom: 16px;
      &.start-button {
        margin-left: 0;
      }
      &.learn-again {
      }
    }
    &-goals {
      max-height: 100px;
      overflow: auto;
      &-item {
        padding-left: 12px;
        position: relative;
        margin: 0;
        line-height: 22px;
      }
      &-item::before {
        content: '';
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background-color: #666;
        position: absolute;
        left: 0;
        top: 10px;
      }
    }
  }
}
@media screen and (max-width: 768px) {
  .package-catalogue {
    &-item {
      display: block;
    }
  }
}
</style>
<style lang="scss">
.package-catalogue {
  &-progress {
    .el-progress-bar__outer {
      background-color: #d2d2d2;
    }
    .el-progress-bar__inner {
      background-color: #66cd2e;
    }
  }
}
@media screen and (max-width: 768px) {
  .leave-current-class {
    max-width: 90%;
  }
}
</style>

<template>
  <div class="package-detail-page" v-loading="isLoading">
    <package-basic-detail v-if="!isFirstGetData" :packageDetail='packageDetail' :actorType='actorType'></package-basic-detail>
    <package-catalogue v-if="!isFirstGetData" class="package-detail-page-catalogue" :packageDetail='packageDetail' :actorType='actorType'></package-catalogue>
  </div>
</template>
<script>
import PackageBasicDetail from './PackageBasicDetail'
import PackageCatalogue from './PackageCatalogue'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'PackageDetail',
  async mounted() {
    this.isFirstGetData = true
    await this.getPackageDetail({
      packageId: this.packageId
    })
    let { packageName } = this.packageDetail
    if (packageName) {
      window.document.title = packageName
    }
    this.isLoading = false
    this.isFirstGetData = false
  },
  props: {
    actorType: String,
    packageId: String
  },
  computed: {
    ...mapGetters({
      lessonPackageDetail: 'lesson/packageDetail'
    }),
    packageDetail() {
      return this.lessonPackageDetail({
        packageId: this.packageId
      })
    }
  },
  data() {
    return {
      isLoading: true,
      isFirstGetData: true
    }
  },
  methods: {
    ...mapActions({
      getPackageDetail: 'lesson/getPackageDetail'
    })
  },
  destroyed() {
    window.document.title = 'KeepWork'
  },
  components: {
    PackageBasicDetail,
    PackageCatalogue
  }
}
</script>
<style lang="scss" scoped>
.package-detail-page {
  max-width: 1150px;
  margin: 0 auto;
  padding-top: 30px;
  &-catalogue {
    margin-top: 40px;
  }
}
</style>


<template>
  <div class="purchase-package" v-loading='isLoading'>
    <div class="purchase-package-warning" v-show="!isResultShow">
      <div class="purchase-package-container">
        <p class="purchase-package-warning-title">
          <i class="el-icon-warning"></i>{{$t('lesson.payAfterConfirmation')}}
        </p>
        <p class="purchase-package-warning-content">{{$t('lesson.confirmFollowInformation')}}</p>
      </div>
    </div>
    <div class="purchase-package-container" v-show="!isResultShow">
      <package-basic-detail :packageDetail='packageDetail'></package-basic-detail>
      <coin-purchase ref="coinPurchaseComp" :packageDetail='packageDetail' class="purchase-package-coin"></coin-purchase>
      <div class="purchase-package-info">{{$t('lesson.youNeedToPay')}}{{payCount}}</div>
      <el-button @click="subscribePackage" class="purchase-package-button" size="medium" type="primary">{{$t('lesson.goToPay')}}
        <i class="el-icon-back"></i>
      </el-button>
    </div>
    <purchase-package-result v-show="isResultShow" :packageDetail='packageDetail'></purchase-package-result>
    <div @click.stop v-if="isLoginDialogShow">
      <login-dialog :show="isLoginDialogShow" @close="closeLoginDialog" />
    </div>
  </div>
</template>
<script>
import _ from 'lodash'
import PackageBasicDetail from './PackageBasicDetail'
import PurchasePackageResult from './PurchasePackageResult'
import CoinPurchase from './CoinPurchase'
import LoginDialog from '@/components/common/LoginDialog'
import { mapGetters, mapActions } from 'vuex'
const PACKAGE_GOOD_DETAIL_APP_NAME = process.env.PACKAGE_GOOD_DETAIL_APP_NAME
const PACKAGE_GOOD_DETAIL_APP_GOODS_ID =
  process.env.PACKAGE_GOOD_DETAIL_APP_GOODS_ID
export default {
  name: 'PurchasePackage',
  async mounted() {
    if (!this.userIsLogined) {
      await this.userGetProfile({ forceLogin: false })
        .then(() => {
          this.isLogin = true
        })
        .catch(() => {
          this.isLogin = false
        })
    }
    if (!this.isLogin) {
      this.isLoginDialogShow = true
      return
    }
    await this.getPackageDetail({
      packageId: this.packageId
    })
    this.packageDetail = this.lessonPackageDetail({
      packageId: this.packageId
    })
    if (
      this.isLoginUserBeTeacher ||
      (this.packageDetail.isSubscribe && this.packageDetail.isBuy)
    ) {
      this.handleAlreadyPurchased()
    }
    this.isMounted = true
    this.isLoading = false
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/profile',
      userIsLogined: 'user/isLogined',
      lessonPackageDetail: 'lesson/packageDetail',
      isLoginUserBeTeacher: 'lesson/isTeacher'
    }),
    username() {
      return _.get(this.userProfile, 'username')
    },
    isLogin: {
      get() {
        return this.userIsLogined
      },
      set() {}
    },
    packageId() {
      return this.$route.params.id
    },
    isPayByCoin() {
      if (this.isMounted) {
        return this.$refs['coinPurchaseComp'].isPayByCoin
      }
    },
    payCount() {
      return this.isPayByCoin
        ? `${this.packageDetail.coin} ${this.$t('lesson.coins')}`
        : `￥ ${this.packageDetail.rmb}`
    },
    nowPath() {
      return this.$route.path
    },
    origin() {
      return window.location.origin
    },
    packageDetailLink() {
      let nowPageLink = window.location.href
      return _.replace(nowPageLink, '/purchase', '')
    },
    packageDetailPath() {
      return _.replace(this.nowPath, '/purchase', '')
    }
  },
  data() {
    return {
      packageDetail: {},
      isLoginDialogShow: false,
      isLoading: true,
      isResultShow: false,
      isMounted: false
    }
  },
  methods: {
    ...mapActions({
      userGetProfile: 'user/getProfile',
      getPackageDetail: 'lesson/getPackageDetail',
      lessonSubscribePackage: 'lesson/subscribePackage'
    }),
    objectToQueryString(obj) {
      const results = []
      _.forOwn(obj, (value, key) => {
        if (_.isObject(value)) {
          value = JSON.stringify(value)
        }
        results.push(`${key}=${encodeURIComponent(value)}`)
      })
      return results.join('&')
    },
    async subscribePackage() {
      this.isLoading = true
      if (this.isPayByCoin) {
        await this.lessonSubscribePackage({ packageId: this.packageId })
        this.isResultShow = true
      } else {
        let payParams = {
          username: this.username,
          app_name: PACKAGE_GOOD_DETAIL_APP_NAME,
          app_goods_id: PACKAGE_GOOD_DETAIL_APP_GOODS_ID,
          price: this.packageDetail.rmb,
          redirect: this.packageDetailLink,
          additional: {
            packageId: this.packageId
          }
        }
        let paramsString = this.objectToQueryString(payParams)
        let payPath = `${this.origin}/wiki/pay?${paramsString}`
        window.location.href = payPath
      }
      this.isLoading = false
    },
    handleAlreadyPurchased() {
      this.$alert(
        this.$t('lesson.havePurchased'),
        this.$t('lesson.infoTitle'),
        {
          confirmButtonText: this.$t('lesson.viewPackage'),
          callback: action => {
            this.backToPackageDetailPage()
          }
        }
      )
    },
    backToPackageDetailPage() {
      this.$router.push({
        path: this.packageDetailPath
      })
    },
    closeLoginDialog() {
      this.$message({
        message: this.$t('lesson.loginBeforePurchase'),
        type: 'warning'
      })
    }
  },
  components: {
    LoginDialog,
    PackageBasicDetail,
    PurchasePackageResult,
    CoinPurchase
  }
}
</script>
<style lang="scss">
.purchase-package {
  padding-bottom: 100px;
  background-color: #fff;
  &-container {
    max-width: 1150px;
    margin: 0 auto;
  }
  &-warning {
    color: #333;
    padding: 16px 0;
    background-color: #fbfbfb;
    &-title {
      font-size: 18px;
      margin: 0 0 57px;
      .el-icon-warning {
        color: #d81e06;
        font-size: 28px;
        margin-right: 17px;
      }
    }
    &-content {
      font-size: 16px;
    }
  }
  &-coin {
    margin: 100px 0;
  }
  &-button {
    width: 266px;
    margin-top: 18px;
    .el-icon-back {
      margin-left: 12px;
      transform: rotate(180deg);
    }
  }
}
</style>

<template>
  <div class="quiz-container" :class="{'is-preview': isPreview}" :id="key">
    <!-- <div class="splic"></div> -->
    <div class="quiz-no-wrap">
      <i class="quiz-icon"></i>
      <span class="quiz-no">
        {{$t('card.quiz')}}
      </span>
      <span v-if="isMutipleChoice" class="mutiple-choice-tips">({{$t('card.multipleChoices')}})</span>
    </div>
    <div class="question">{{ question }}
    </div>

    <el-radio-group class="quiz" v-if="isSingleChoice" v-model="quizAnswer">
      <div class="quiz-option" v-for="(item, index) in options" :key="index">
        <el-radio :disabled="isDone" :label="alphabet[index]">{{alphabet[index]}} {{item.item}}</el-radio>
      </div>
    </el-radio-group>

    <el-checkbox-group class="quiz" v-if="isMutipleChoice" v-model="quizMutipleAnswer">
      <div class="quiz-option" v-for="(item, index) in options" :key="index">
        <el-checkbox :disabled="isDone" :label="alphabet[index]">{{alphabet[index]}} {{item.item}}</el-checkbox>
      </div>
    </el-checkbox-group>

    <el-radio-group class="quiz" v-if="isTFNG" v-model="quizAnswer">
      <div class="quiz-option" v-for="(item, index) in options" :key="index">
        <el-radio :disabled="isDone" :label="alphabet[index]">{{$t(`card.${item.item}`)}}</el-radio>
      </div>
    </el-radio-group>

    <div v-if="isTextMatch" class="quiz-text-match">
      <div v-for="(item, index) in options" :key="index">
        <div>{{$t('modList.text')}} {{index+1}}</div>
        <pre>{{item.item}}</pre>
      </div>
      <el-input v-if="!isDone" type="textarea" maxlength="512" v-model="quizAnswer" :placeholder="$t('card.textMatchPlaceholder')"></el-input>
    </div>

    <div v-if="isDone" class="quiz-result" :class="{'error': isError}">
      <div v-if="isSingleChoice || isMutipleChoice || isTFNG" class="answer">
        {{$t('card.rightAnswerColon')}}
        <span v-if="isTFNG" :class="[isError ? 'error-highlight': 'highlight']">{{TFNGAnswer}}</span>
        <span v-else :class="[isError ? 'error-highlight': 'highlight']">{{answer}}</span>
      </div>
      <div v-if="isTextMatch" class="answer">
        {{$t('card.yourAnswerColon')}}
        <span :class="[isError ? 'error-highlight': 'highlight']">{{quizAnswer}}</span>
      </div>
      <div class="desc">
        {{$t('card.explanationColon')}}
        <span :class="['explan',isError ? 'error-highlight': 'highlight']">{{desc}}</span>
      </div>
    </div>
    <div v-if="isFormatError" class="is-format-error">{{$t('lesson.formatError')}}</div>
    <el-button v-if="!isDone && !isPreview" class="quiz-submit" size="small" type="primary" @click="checkAnswer">{{$t('card.submit')}}</el-button>
  </div>
</template>


<script>
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'
import { lesson } from '@/api'
export default {
  name: 'Quiz',
  props: {
    data: {
      type: Object,
      default() {
        return {}
      }
    },
    isPreview: {
      type: Boolean,
      default: false
    },
    isPrint: {
      type: Boolean,
      default: false
    },
    isVisitor: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      quizAnswer: '',
      quizMutipleAnswer: [],
      isError: false,
      isRight: false,
      isDone: false
    }
  },
  methods: {
    ...mapActions({
      doQuiz: 'lesson/student/doQuiz',
      uploadLearnRecords: 'lesson/student/uploadLearnRecords',
      createLearnRecords: 'lesson/student/createLearnRecords',
      uploadSelfLearnRecords: 'lesson/student/uploadSelfLearnRecords',
      uploadVisitorLearnRecords: 'lesson/student/uploadVisitorLearnRecords',
      switchSummary: 'lesson/student/switchSummary'
    }),
    checkAnswer() {
      this.isSingleChoice && this.checkSingleChoice()
      this.isMutipleChoice && this.checkMutipleChoice()
      this.isTFNG && this.checkTFNG()
      this.isTextMatch && this.checkTextMatch()
    },
    checkSingleChoice() {
      if (!this.quizAnswer) {
        return this.$message.error(this.$t('card.pleaseSelectOne'))
      }
      let result = this.answer.some(item => item === this.quizAnswer)
      this.showResultAndSubmit(result, this.quizAnswer)
    },
    checkMutipleChoice() {
      if (this.quizMutipleAnswer.length < 1) {
        return this.$message.error(this.$t('card.pleaseSelectOne'))
      }
      let quizMutipleAnswer = [...this.quizMutipleAnswer].sort()
      let answer = [...this.answer].sort()
      let result = JSON.stringify(quizMutipleAnswer) === JSON.stringify(answer)
      this.showResultAndSubmit(result, quizMutipleAnswer)
    },
    checkTFNG() {
      // true or false
      if (!this.quizAnswer) {
        return this.$message.error(this.$t('card.pleaseSelectOne'))
      }
      let result = this.answer[0] === this.quizAnswer
      this.showResultAndSubmit(result, this.quizAnswer)
    },
    checkTextMatch() {
      let quizAnswer = this.quizAnswer.trim()
      if (!quizAnswer.trim()) {
        return this.$message.error(this.$t('card.pleaseInputAnswer'))
      }
      let result = this.answer.some(({ item }) => item.trim() === quizAnswer)
      this.showResultAndSubmit(result, quizAnswer)
    },
    showResultAndSubmit(result, answer) {
      this.isError = !result
      this.isRight = result
      this.isDone = true
      this.submit(result, answer)
    },
    async submit(result, answer) {
      this.doQuiz({ key: this.key, question: this.question, result, answer })
      if (this.isBeInClassroom) {
        let state = this.lessonIsDone ? 1 : 0
        return await this.uploadLearnRecords(state).catch(e => console.error(e))
      }
      // 一次只能自学一个页面
      if (!this.isVisitor) {
        let lastLearnRecords = await lesson.lessons
          .getLastLearnRecords()
          .catch(e => console.error(e))
        lastLearnRecords = _.get(lastLearnRecords, 'rows', [])
        if (
          lastLearnRecords.length > 0 &&
          this.learnRecordsId !== lastLearnRecords[0].id
        ) {
          return this.$router.push({ name: 'StudentCenter' })
        }
      }

      // FIXME: 这里应该改成从store里面去课程包和课程的id
      const { packageId, lessonId } = this.$route.params
      // 首次需要先创建学习记录
      // if (!this.learnRecordsId && !this.isVisitor) {
      //   await this.createLearnRecords({
      //     packageId: Number(packageId),
      //     lessonId: Number(lessonId)
      //   })
      // }
      this.isVisitor
        ? await this.uploadVisitorLearnRecords({
            packageId: Number(packageId),
            lessonId: Number(lessonId),
            state: this.lessonIsDone ? 1 : 0
          })
        : await this.uploadSelfLearnRecords({
            packageId: Number(packageId),
            lessonId: Number(lessonId),
            state: this.lessonIsDone ? 1 : 0
          })
    }
  },
  watch: {
    quizzes(quizzes) {
      let quiz = quizzes.find(
        ({
          data: {
            quiz: { data }
          }
        }) => data[0].id === this.key
      )
      if (quiz && quiz.state && quiz.state.answer) {
        this.isDone = true
        this.isError = !quiz.state.result
        this.isRight = quiz.state.result
        this.quizAnswer = quiz.state.answer
        this.quizMutipleAnswer = quiz.state.answer
      }
    }
  },
  computed: {
    ...mapGetters({
      lessonDetail: 'lesson/student/lessonDetail',
      isBeInClassroom: 'lesson/student/isBeInClassroom',
      learnRecordsId: 'lesson/student/learnRecordsId',
      lessonIsDone: 'lesson/student/lessonIsDone'
    }),
    modList() {
      return this.lessonDetail.modList || []
    },
    quizzes() {
      return this.modList.filter(item => item.cmd === 'Quiz')
    },
    key() {
      return _.get(this.data, 'data.quiz.data[0].id')
    },
    quizData() {
      return _.get(this.data, 'data.quiz.data[0]')
    },
    question() {
      return _.get(this.quizData, 'title')
    },
    answer() {
      return this.isTextMatch ? this.options : _.get(this.quizData, 'answer')
    },
    TFNGAnswer() {
      if (this.answer[0] === 'A') {
        return this.$t('card.true')
      }
      if (this.answer[0] === 'B') {
        return this.$t('card.false')
      }
      return false
    },
    desc() {
      return _.get(this.quizData, 'desc')
    },
    options() {
      return _.get(this.quizData, 'options')
    },
    quizType() {
      return _.get(this.quizData, 'type', '0')
    },
    isSingleChoice() {
      return this.quizType === '0'
    },
    isMutipleChoice() {
      return this.quizType === '1'
    },
    isTFNG() {
      return this.quizType === '2'
    },
    isTextMatch() {
      return this.quizType === '3'
    },
    alphabet() {
      return Array.from({ length: 26 }, (i, index) =>
        String.fromCharCode(65 + index)
      )
    },
    isFormatError() {
      return _.isEmpty(this.data.data)
    }
  }
}
</script>

<style lang="scss">
.quiz-container {
  box-sizing: border-box;
  margin-top: 10px;
  padding: 10px 15px;
  font-size: 16px;
  border: 1px solid #fff;
  color: #4c4c4c;
  background: white;
  max-width: 1229px;
  margin: 0 auto;
  .is-format-error {
    color: #F56C6C;
    margin-left: 60px;
  }
  &.is-preview {
    .el-radio__input,
    .el-checkbox__inner,
    .el-textarea {
      display: none;
    }
    .el-radio__input.is-checked ~ .el-radio__label,
    .el-checkbox__input.is-checked ~ .el-checkbox__label {
      color: #606266;
      font-weight: normal;
    }

    .el-radio__input.is-disabled + span.el-radio__label,
    .el-checkbox__input.is-disabled + span.el-checkbox__label {
      color: #606266;
      font-weight: normal;
    }
  }
  .quiz-no-wrap {
    display: flex;
    align-items: center;
    margin-top: 10px;
    i {
      color: #1982ff;
      display: inline-block;
      width: 41px;
      height: 38px;
      font-size: 22px;
      font-weight: 600;
      padding-right: 12px;
      background: url('../../../assets/lessonImg/editIcon.png') no-repeat center
        #fff;
    }
    .quiz-no {
      margin-left: 10px;
      display: inline-block;
      font-weight: 600;
      height: 38px;
    }
    .mutiple-choice-tips {
      margin-left: 10px;
      display: inline-block;
      height: 38px;
    }
  }
  $marginLeft: 60px;
  $marginTop: 20px;
  .question {
    margin-left: $marginLeft;
    margin-top: $marginTop;
    white-space: normal;
    word-wrap: break-word;
  }
  .quiz {
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-weight: 600;
    &-option {
      margin-top: $marginTop;
      font-size: 18px;
      margin-left: $marginLeft;
    }
  }
  .quiz-text-match {
    padding: 20px 30px 0 70px;
    user-select: none;
    pre {
      white-space: pre-line;
    }
  }
  .quiz-result {
    margin-left: 20px;
    margin-top: $marginTop;
    background: rgba(64, 158, 254, 0.05);
    padding: 10px 20px;
    .desc,
    .answer {
      font-weight: 600;
      margin: 20px;
    }
    .highlight {
      color: #409efe;
    }
    .explan {
      word-break: break-all;
    }
  }
  .quiz-submit {
    margin-top: $marginTop;
    margin-left: $marginLeft;
  }
  .el-checkbox__inner {
    // border-radius: 50%;
    height: 20px;
    width: 20px;
    &::after {
      // border: 2px solid #fff;
      border-width: 2px;
      height: 11px;
      width: 5px;
      left: 5px;
    }
  }

  .el-radio__input {
    .el-radio__inner {
      height: 20px;
      width: 20px;
    }
    &.is-checked .el-radio__inner {
      &::after {
        box-sizing: content-box;
        display: inline-block;
        content: '';
        border: 2px solid #fff;
        background: none;
        border-radius: 0;
        border-left: 0;
        border-top: 0;
        height: 11px;
        width: 5px;
        left: 3px;
        position: absolute;
        top: 8px;
        transform: rotate(45deg) translate(-50%, -50%) scale(1);
      }
    }
    &.is-checked.is-disabled .el-radio__inner {
      &::after {
        border-color: #c0c4cc;
      }
    }
  }

  .el-radio__input.is-checked ~ .el-radio__label,
  .el-checkbox__input.is-checked ~ .el-checkbox__label {
    font-weight: 600;
    color: black;
  }

  .el-radio__input.is-disabled + span.el-radio__label,
  .el-checkbox__input.is-disabled + span.el-checkbox__label {
    color: black;
  }

  .splic {
    height: 1px;
    margin: 0 0 30px 40px;
    border-bottom: 1px dashed #bfbfbf;
  }

  .error-highlight {
    color: #f53838;
  }

  .mutiple-choice-tips {
    color: #ff414a;
  }

  .error {
    margin-bottom: 20px;
    border: 1px solid #f53838;
    background: rgba(245, 56, 56, 0.05);
    .quiz-result {
      background: none;
    }
  }
}
</style>

<template>
  <div class="solution">
    <combo-box
      v-show="isParents"
      projectName="official/paracraft"
      filePath="learn/parent_banner"
    ></combo-box>
    <educators-tab v-show="isParents"></educators-tab>
    <combo-box :routes="routes"></combo-box>
  </div>
</template>
<script>
import EducatorsTab from './EducatorsTab'
import ComboBox from '@/components/combo/ComboBox'
import _ from 'lodash'
export default {
  name: 'Solution',
  components: {
    ComboBox,
    EducatorsTab
  },
  watch: {
    $route(to) {
      const { params: { command } } = to
      const { projectName, filePath } = this.routes[command]
      this.currentFilePath = filePath
    }
  },
  mounted() {
    const { params: { command } } = this.$route
    const { projectName, filePath } = this.routes[command]
    this.currentFilePath = filePath
  },
  computed: {
    isParents() {
      return this.currentFilePath === 'learn/parents'
    }
  },
  data() {
    return {
      routes: {
        teachingIdea: {
          projectName: 'official/paracraft',
          filePath: 'learn/our_ideas'
        },
        teacher: {
          projectName: 'official/paracraft',
          filePath: 'learn/educators'
        },
        parents: {
          projectName: 'official/paracraft',
          filePath: 'learn/parents'
        },
        organization: {
          projectName: 'official/paracraft',
          filePath: 'learn/partnership'
        },
        competition: {
          projectName: 'official/paracraft',
          filePath: 'learn/works_and_contests'
        }
      },
      currentFilePath: ''
    }
  },
}
</script>

<style lang="scss">
.solution {
  background: #fff;
  max-width: 1200px;
  margin: 0 auto 80px;
}
</style>


```