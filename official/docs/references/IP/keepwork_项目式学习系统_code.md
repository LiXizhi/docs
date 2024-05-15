``` javascript

<template>
  <div class="website-delete">
    <p class="website-delete-alert">{{$t('project.deleteProjectHint')}}</p>
    <p class="website-delete-hint" @click="agreeDelete"><span :class="['website-delete-hint-check',{'website-delete-hint-agree':checked}]"></span>{{$t('project.deleteProjectNotice')}}</p>
    <p class="website-delete-btn">
      <el-button type="primary" :disabled="!checked" @click="confirmDeleteProject" :loading="deleteSuccessLoading">{{$t('common.Sure')}}</el-button>
    </p>
  </div>
</template>
<script>
import _ from 'lodash'
import { keepwork } from '@/api'

export default {
  name: 'DeleteProject',
  
  data() {
    return {
      checked: false,
      deleteSuccessLoading: false
    }
  },
  computed: {
    projectId() {
      return _.get(this.$route, 'params.id')
    }
  },
  methods: {
    agreeDelete(){
      this.checked = !this.checked
    },
    async confirmDeleteProject(){
      this.deleteSuccessLoading = true
      await keepwork.projects.deleteProject(this.projectId).then(res => {
        this.deleteSuccessLoading = false
        // this.$router.push('/')
        window.location.href = window.location.origin
      }).catch(err => {
        console.error(err)
        this.$message.error($t('editor.deleteFail'))
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.website-delete {
  padding: 70px;
  max-width: 1200px;
  box-sizing: border-box;
  margin: 24px auto 120px;
  border: 1px solid #e8e8e8;
  background: #fff;
  &-alert {
    font-size: 20px;
    color: #303133;
  }
  &-hint {
    color: #666;
    max-width: 480px;
    word-break:break-all;
    line-height: 30px;
    padding-left: 26px;
    position: relative;
    cursor: pointer;
    font-size: 14px;
    &-agree {
      background: #409eff;
    }
    &-check {
      position: absolute;
      display: inline-block;
      width: 15px;
      height: 15px;
      top: 5px;
      left: 4px;
      border: 1px solid #409eff;
      border-radius: 2px;
      &::after{
        content: '';
        width: 10px;
        height: 5px;
        display: inline-block;
        border: 1px solid #fff;
        transform: rotate(-45deg);
        border-top-color: transparent;
        border-right-color: transparent;
        position: absolute;
        top: 1px;
        left: 1px;
      }
    }
  }
  &-btn {
    margin-top: 80px;
  }
}
</style>

<template>
  <div class="edit-project">
    <el-tabs v-if="isLoginUserEditable" class="edit-project-tabs container" v-model="activeName" type="card" v-loading='isLoading'>
      <el-tab-pane name="editing" class="edit-project-tabs-pane">
        <span slot="label">{{$t('project.setting')}}</span>
        <project-editing :originPrivilege='originPrivilege' :originVisibility='originVisibility' :originalProjectDetail='pblProjectDetail'></project-editing>
      </el-tab-pane>
      <el-tab-pane name="members" class="edit-project-tabs-pane">
        <span slot="label">{{$t('project.members')}}</span>
        <project-members :projectDetail='pblProjectDetail' :projectId='projectId' class="edit-project-members"></project-members>
      </el-tab-pane>
    </el-tabs>
    <p v-else>不好意思，没有编辑权限。。。</p>
  </div>
</template>
<script>
import ProjectEditing from './common/ProjectEditing'
import ProjectMembers from './common/ProjectMembers'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'EditProject',
  props: {
    pblProjectDetail: {
      type: Object,
      required: true
    },
    isLoginUserEditable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isLoading: false,
      activeName: 'editing'
    }
  },
  computed: {
    originPrivilege() {
      return _.get(this.pblProjectDetail, 'privilege')
    },
    originVisibility() {
      return _.get(this.pblProjectDetail, 'visibility')
    },
    projectId() {
      return _.get(this.$route, 'params.id')
    }
  },
  components: {
    ProjectEditing,
    ProjectMembers
  }
}
</script>
<style lang="scss">
.edit-project {
  background-color: #f5f5f5;
  padding: 24px 0;
  &-header {
    margin-bottom: 24px;
  }
  &-tabs {
    background-color: #fff;
    border: 1px solid #e8e8e8;
    &-pane {
      min-height: 400px;
    }
    .el-tabs__header {
      padding-left: 18px;
      margin-bottom: 24px;
    }
    .el-tabs__nav-wrap .el-tabs__item:last-child,
    .el-tabs__nav-wrap .el-tabs__item:nth-child(2) {
      padding: 0 6px;
    }
    .el-tabs__item {
      padding: 0 6px;
      height: 56px;
      line-height: 56px;
      span {
        color: #909399;
        display: inline-block;
        padding: 0 18px;
        height: 24px;
        line-height: 24px;
        border-radius: 24px;
      }
    }
    .el-tabs__item.is-active {
      span {
        color: #fff;
        background-color: #2296f3;
      }
    }
  }
  &-tabs > .el-tabs__header .el-tabs__nav,
  &-tabs > .el-tabs__header .el-tabs__item,
  &-tabs > .el-tabs__header .el-tabs__item.is-active {
    border: none;
  }
  &-members {
    padding: 0 24px 24px 24px;
  }
}

@media (max-width: 768px) {
  .edit-project {
    &-tabs {
      .el-tabs__content {
        overflow: auto;
      }
    }
  }
}
</style>
<template>
  <el-dialog :visible.sync="show" :before-close="handleClose" class="issue-detail-dialog">
    <h4 slot="title" class="issue-detail-title">{{projectDetail.name}}/{{$t('project.board')}}/{{$t('project.issueDetail')}}</h4>
    <div v-loading="updateLoading">
      <div class="issue-detail-header">
        <div class="issue-title">
          <div v-if="currIssue.titleIsEdit" class="issue-title-edit-box">
            <input class="issue-title-edit-box-input" type="text" v-model="currIssue.title">
            <el-button class="issue-title-button" size="mini" type="primary" @click="updateTitle">{{$t('common.Sure')}}</el-button>
            <el-button class="issue-title-button" size="mini" @click="cancelUpdateTitle">{{$t('common.Cancel')}}</el-button>
          </div>
          <div v-else class="issue-title-title-box">
            <span class="issue-title-text" :title="currIssue.title">{{currIssue.title}} #{{currIssue.no}}</span>
            <span class="issue-title-edit" @click="editIssueTitle"><i class="iconfont icon-edit-square"></i>{{$t('project.editIssueTitle')}}</span>
          </div>
        </div>
      </div>
      <div class="issue-detail-intro">
        <span class="created-time">{{relativeTime(currIssue.createdAt)}}</span>
        <span class="created-by">{{$t('project.createBy')}}<span class="name">{{issue.user.nickname}}</span>{{$t('project.created')}}</span>
        <span class="issue-detail-intro-tag">
          <el-tag :key="tag" v-for="tag in dynamicTags" :closable="isEditTags" :disable-transitions="false" @close="handleCloseTag(tag)">
            {{tag}}
          </el-tag>
          <el-input class="input-new-tag" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
          </el-input>
          <el-button v-show="isEditTags" v-else class="button-new-tag" size="small" @click="showInput">+ {{$t('project.newTag')}}</el-button>
          <el-button v-if="isEditTags" size="mini" type="primary" @click="updateTag">{{$t('common.Sure')}}</el-button>
          <span v-else class="edit-tag" @click="updateTag"><i class="iconfont icon-edit-square"></i>{{$t('project.changeLabel')}}</span>
        </span>
      </div>
      <div class="issue-detail-status">
        <div class="issue-detail-status-left">{{$t('project.status')}}：<span class="rank"><i :class="['iconfont',issue.state == 0 ? 'icon-warning-circle-fill':'icon-check-circle-fill']"></i><span class="rank-tip">{{issue.state == 0 ? $t('project.inProgressStatus') : $t('project.finishStatus')}}</span></span></div>
        <div class="issue-detail-status-right">
          <div class="principal" :class="{'principal-en': isEn}">{{$t('project.issueAsignees')}}:</div>
          <div class="member-portrait">
            <img class="player-portrait" v-for="player in assignedMembers" :key="player.id" :src="player.portrait || default_portrait" alt="" :title="player.username">
            <el-dropdown @command="handleCommand" trigger="click" placement="bottom-end">
              <span class="el-dropdown-link">
                <span class="assigns-btn"></span>
              </span>
              <el-dropdown-menu slot="dropdown" class="new-issue-assign">
                <el-dropdown-item v-if="memberList_2.length == 0">{{$t('project.noOtherMembers')}}</el-dropdown-item>
                <el-dropdown-item v-for="member in memberList_2" :key="member.id" :command="member.userId"><i :class="['icofont',{'el-icon-check': member.haveAssigned}]"></i><img class="member-portrait" :src="member.portrait || default_portrait" alt="">{{member.nickname || member.username}}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </div>
      <div class="issue-detail-idea">

        <div class="issue-detail-idea-box">
          <div class="issue-detail-idea-box-portrait">
            <img :src="issue.user.portrait || default_portrait" alt="">
          </div>
          <div class="issue-detail-idea-box-content">
            <div class="username-created-time">
              <div class="username-created-time-left">
                <span class="username">{{issue.user.username}}</span>
                <span class="time">{{relativeTime(issue.createdAt)}}</span>
              </div>
              <div class="username-created-time-right" v-if="currIssue.userId == userId">
                <el-dropdown trigger="click">
                  <span class="el-dropdown-link">
                    <i class="iconfont icon-ellipsis"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown" class="operate-comment">
                    <el-dropdown-item><span class="action" @click="handleIssueDesc(1)">{{$t('editor.edit')}}</span></el-dropdown-item>
                    <!-- <el-dropdown-item><span class="action" @click="handleIssueDesc(2)">删除</span></el-dropdown-item> -->
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <div class="idea-area">
              <div class="arrows"></div>
              <div v-if="currIssue.descEdit" class="text">
                <textarea name="" rows="8" :placeholder='$t("project.leaveAComment")' v-model.trim="currIssue.content"></textarea>
                <div class="text-button">
                  <el-button size="mini" type="primary" @click="submitModifiedIssueDesc">{{$t('common.Sure')}}</el-button>
                  <el-button size="mini" @click="cancelModifiedIssueDesc">{{$t('common.Cancel')}}</el-button>
                </div>
              </div>
              <div v-else class="text">{{currIssue.content}}</div>
            </div>
          </div>
        </div>

        <div class="issue-detail-idea-box" v-for="(comment,index) in comments" :key="index">
          <div class="issue-detail-idea-box-portrait">
            <img :src="comment.extra.portrait || default_portrait" alt="">
          </div>
          <div class="issue-detail-idea-box-content">
            <div class="username-created-time">
              <div class="username-created-time-left">
                <span class="username">{{comment.extra.username}}</span>
                <span class="time">{{relativeTime(comment.createdAt)}}</span>
              </div>
              <div class="username-created-time-right" v-if="comment.userId == userId && !isProhibitEdit">
                <el-dropdown trigger="click">
                  <span class="el-dropdown-link">
                    <i class="iconfont icon-ellipsis"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown" class="operate-comment">
                    <el-dropdown-item><span class="action" @click="handleComment(comment,1,index)">{{$t('editor.edit')}}</span></el-dropdown-item>
                    <el-dropdown-item><span class="action" @click="handleComment(comment,2,index)">{{$t('common.remove')}}</span></el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </div>
            <div class="idea-area">
              <div class="arrows"></div>
              <div v-if="comment.isEdit" class="text">
                <textarea name="" :ref="`edit${index}`" rows="8" :placeholder='$t("project.leaveAComment")' v-model.trim="comment.content"></textarea>
                <div class="text-button">
                  <el-button size="mini" type="primary" @click="submitModifiedComment(comment,index)">{{$t('project.updateComment')}}</el-button>
                  <el-button size="mini" @click="cancelModifiedComment(comment,index)">{{$t('common.Cancel')}}</el-button>
                </div>
              </div>
              <div v-else class="text">{{comment.content}}</div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isLogined && !isProhibitEdit" class="issue-detail-my-idea">
        <div class="issue-detail-my-idea-portrait">
          <img :src="userProfile.portrait || default_portrait" alt="">
        </div>
        <div class="issue-detail-my-idea-content">
          <div class="username">{{username}}</div>
          <div class="idea-area">
            <div class="arrows"></div>
            <div class="text">
              <textarea name="myIdea" rows="8" :placeholder='$t("project.leaveAComment") + $t("project.recommentMaxLength")' v-model.trim="myComment"></textarea>
            </div>
          </div>
          <div class="finish">
            <el-button size="medium" @click="closeIssue">{{currIssue.state == 0 ? $t('project.closeIssue') : $t('project.reopenIssue')}}</el-button>
            <el-button type="primary" size="medium" @click="createComment" :disabled="!myComment" :loading="createCommentLoading">{{$t('project.comment')}}</el-button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>
<script>
import moment from 'moment'
import 'moment/locale/zh-cn'
import { locale } from '@/lib/utils/i18n'
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import default_portrait from '@/assets/img/default_portrait.png'
import { mapActions, mapGetters } from 'vuex'
import { keepwork } from '@/api'
import Vue from 'vue'
import _ from 'lodash'

export default {
  name: 'IssueDetail',
  props: {
    show: Boolean,
    projectDetail: {
      type: Object,
      default() {
        return {}
      }
    },
    issue: {
      type: Object,
      default() {
        return {}
      }
    },
    currPage: {
      type: Number,
      default: 1
    },
    isProhibitEdit: {
      type: Boolean,
      default: false
    },
    searchKeyWord: String,
    state: null
  },
  data() {
    return {
      default_portrait,
      isEditTags: false,
      issueData: {},
      dynamicTags: [],
      inputVisible: false,
      inputValue: '',
      currIssue: {},
      comments: [],
      myComment: '',
      isEdit: false,
      assignedMembers: [],
      updateLoading: false,
      createCommentLoading: false
    }
  },
  async mounted() {
    this.updateLoading = true
    await Promise.all([
      this.getIssueData(),
      this.getCommentsList(),
      this.getProjectMember({
        objectId: this.projectDetail.id,
        objectType: 5
      })
    ]).catch(err => console.error(err))
    this.updateLoading = false
  },
  computed: {
    ...mapGetters({
      username: 'user/username',
      userId: 'user/userId',
      userProfile: 'user/profile',
      pblProjectMemberList: 'pbl/projectMemberList',
      isLogined: 'user/isLogined'
    }),
    isEn() {
      return locale === 'en-US'
    },
    memberList() {
      return this.pblProjectMemberList({ projectId: this.projectDetail.id })
    },
    memberList_2() {
      let memberArr1 = _.concat(this.memberList)
      let memberArr2 = _.forEach(memberArr1, member => {
        Object.assign(member, { haveAssigned: this.isAssigned(member) })
      })
      return memberArr2
    },
    assignMembersId() {
      let arrId = []
      _.map(this.assignedMembers, ({ userId }) => {
        arrId.push(userId)
      })
      return arrId.join('|')
    },
    currIssueId() {
      return _.get(this.issue, 'id', '')
    }
  },
  methods: {
    ...mapActions({
      getProjectIssues: 'pbl/getProjectIssues',
      getProjectMember: 'pbl/getProjectMember',
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    async getIssueData() {
      await keepwork.issues
        .getSingleIssue({ issueId: this.issue.id })
        .then(res => {
          this.issueData = Object.assign(res, {
            titleIsEdit: false,
            descEdit: false,
            tagEdit: false
          })
          this.currIssue = _.clone(this.issueData)
          this.dynamicTags = this.currIssue.tags.split('|').filter(x => x)
          this.assignedMembers = _.clone(this.currIssue.assigns)
        })
        .catch(err => console.error(err))
    },
    editIssueTitle() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      if (this.isProhibitEdit) {
        return this.prohibitEditWarning()
      }
      Vue.set(this.currIssue, 'titleIsEdit', true)
    },
    async updateIssueItem(item) {
      this.updateLoading = true
      this.$nextTick(async () => {
        await keepwork.issues
          .updateIssue({
            objectId: this.issue.id,
            params: item
          })
          .catch(err => console.error(err))
        let payload = {
          objectId: this.projectDetail.id,
          objectType: 5,
          'x-per-page': 25,
          'x-page': this.currPage,
          'x-order': 'createdAt-desc',
          state: this.state
        }
        if (this.searchKeyWord) payload['text-like'] = `%${this.searchKeyWord}%`
        if (this.state === null) {
          let { state, ..._payload } = payload
          await this.getProjectIssues(_payload)
        } else {
          await this.getProjectIssues(payload)
        }
        await this.getIssueData()
        this.updateLoading = false
      })
    },
    async updateTitle() {
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: this.currIssue.title
      }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.currIssue.title = _.get(sensitiveResult, '[0].word', this.currIssue.title)
        this.cretateIssueLoading = false
        return
      }
      await this.updateIssueItem({ title: this.currIssue.title })
      this.getIssueData()
    },
    async updateTag() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      if (this.isProhibitEdit) {
        return this.prohibitEditWarning()
      }
      let tags = this.dynamicTags.join('|')
      if (tags != this.currIssue.tags) {
        await this.updateIssueItem({ tags })
        await this.getIssueData()
        this.currIssue = _.clone(this.issueData)
        this.dynamicTags = this.currIssue.tags.split('|').filter( x => x)
      } else {
        this.cancelUpdateTag()
      }
      this.isEditTags = !this.isEditTags
    },
    handleIssueDesc(command) {
      if (command == 1) {
        this.currIssue.descEdit = true
      } else {
        this.$message.error('第一条评论是问题的描述，不能删除')
      }
    },
    async submitModifiedIssueDesc() {
      await this.updateIssueItem({ content: this.currIssue.content })
      this.getIssueData()
    },
    cancelModifiedIssueDesc() {
      this.currIssue = _.clone(this.issueData)
    },
    handleCloseTag(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },
    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    async handleInputConfirm() {
      let inputValue = this.inputValue
      let isExistTagIndex = _.findIndex(
        this.dynamicTags,
        tag => tag === inputValue
      )
      if (isExistTagIndex !== -1) {
        this.$message({
          showClose: true,
          message: '该标签已存在',
          type: 'error'
        })
        return
      }
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: inputValue
      }).catch()
      this.isTagLoading = false
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.inputValue = _.get(sensitiveResult, '[0].word', inputValue)
        return
      }
      if (inputValue) {
        this.dynamicTags.push(inputValue)
      }
      this.inputVisible = false
      this.inputValue = ''
    },
    cancelUpdateTitle() {
      this.currIssue = _.clone(this.issueData)
    },
    cancelUpdateTag() {
      this.currIssue = _.clone(this.issueData)
      this.dynamicTags = this.currIssue.tags.split('|').filter(x => x)
    },
    handleClose() {
      this.$emit('close')
    },
    issueTagArr(issue) {
      if(_.get(issue, 'tags', '')){
        return _.get(issue, 'tags', '').split('|')
      }
    },
    async getCommentsList() {
      await keepwork.comments
        .getComments({ objectType: 4, objectId: this.issue.id })
        .then(comments => {
          let commentsArr = _.get(comments, 'rows', [])
          let arr = _.map(commentsArr, item => ({ ...item, isEdit: false }))
          arr.sort(this.sortByCreatedAt)
          this.comments = arr
        })
        .catch(err => console.error(err))
    },
    async createComment() {
      this.createCommentLoading = true
      if (!this.myComment) {
        this.createCommentLoading = false
        return
      }
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: this.myComment
      }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.myComment = _.get(sensitiveResult, '[0].word', this.myComment)
        this.createCommentLoading = false
        return
      }
      await keepwork.comments
        .createComment({
          objectType: 4,
          objectId: _.toString(this.issue.id),
          content: this.myComment
        })
        .then(res => {
          this.createCommentLoading = false
          this.myComment = ''
          this.getCommentsList()
        })
        .catch(err => {
          this.$message.error('评论失败')
          this.createCommentLoading = false
        })
    },
    async handleComment(comment, action, index) {
      if (action == 1) {
        Vue.set(comment, 'isEdit', true)
        Vue.set(this.comments, index, comment)
        this.$nextTick(() => {
          let dom = this.$refs[`edit${index}`]
          dom[0].focus()
        })
      } else {
        await keepwork.comments.deleteComment({ commentId: comment.id })
        this.getCommentsList()
      }
    },
    sortByCreatedAt(obj1, obj2) {
      return obj1.createdAt <= obj2.createdAt ? -1 : 1
    },
    async submitModifiedComment(comment, index) {
      let copyComment = Object.assign({}, comment)
      if (!copyComment.content) {
        await this.handleComment(comment, 2, index)
        return
      }
      await keepwork.comments.updateComment({
        commentId: copyComment.id,
        content: copyComment.content
      })
      this.getCommentsList()
    },
    cancelModifiedComment(comment, index) {
      Vue.set(comment, 'isEdit', false)
      Vue.set(this.comments, index, comment)
      this.getCommentsList()
    },
    async closeIssue() {
      if (this.currIssue.state == 0) {
        await this.updateIssueItem({ state: 1 })
        this.handleClose()
      } else {
        await this.updateIssueItem({ state: 0 })
        this.handleClose()
      }
    },
    isAssigned(member) {
      let temp = false
      _.forEach(this.assignedMembers, assign => {
        if (member.userId == assign.userId) {
          temp = true
        }
      })
      return temp
    },
    async handleCommand(userId) {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      if (this.isProhibitEdit) {
        return this.prohibitEditWarning()
      }
      _.forEach(this.memberList, member => {
        if (member.userId === userId) {
          if (this.assignedMembers.length == 0) {
            return this.assignedMembers.push(member)
          }
          let i
          for (i = 0; i < this.assignedMembers.length; ++i) {
            if (this.assignedMembers[i].userId === userId) {
              break
            }
          }
          if (i === this.assignedMembers.length) {
            return this.assignedMembers.push(member)
          }
          this.assignedMembers.splice(i, 1)
        }
      })
      await this.updateIssueItem({ assigns: this.assignMembersId })
      this.getIssueData()
    },
    relativeTime(time) {
      const offset = moment().utcOffset()
      this.isEn ? moment.locale('en') : moment.locale('zh-cn')
      return moment(time)
        .utcOffset(offset)
        .fromNow()
    },
    prohibitEditWarning() {
      this.$message({
        type: 'warning',
        message: '你没有编辑权限'
      })
    }
  }
}
</script>
<style lang="scss">
.issue-detail-dialog {
  .el-dialog {
    max-width: 900px;
    .el-dialog__header {
      padding: 0;
      margin: 0;
      .el-dialog__headerbtn {
        top: 10px;
      }
    }
    .el-dialog__body {
      padding: 6px 0;
    }
  }
  .issue-detail-title {
    font-size: 12px;
    background: #f4f5f5;
    margin: 0;
    padding-left: 16px;
    line-height: 40px;
    color: #909399;
    border-bottom: 1px solid #e8e8e8;
  }
  .issue-detail {
    &-header {
      line-height: 50px;
      padding: 0 20px;
      .issue-title {
        &-edit-box {
          display: flex;
          align-items: center;
          height: 56px;
          margin-right: 10px;
          &-input {
            width: 80%;
          }
        }
        &-title-box {
          font-size: 20px;
          height: 56px;
        }
        &-text {
          display: inline-block;
          max-width: 80%;
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
        &-edit {
          font-size: 12px;
          cursor: pointer;
          color: #409eff;
          display: inline-block;
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
        &-button {
          padding: 4px 10px;
          margin-left: 10px;
        }
      }
    }
    &-intro {
      font-size: 12px;
      padding: 0 20px;
      .created-time {
        color: #909399;
        margin-right: 8px;
      }
      .created-by {
        color: #909399;
        margin-right: 20px;
        .name {
          color: #409eff;
        }
      }
      &-tag {
        .el-tag {
          height: 22px;
          line-height: 20px;
          margin-bottom: 4px;
          background-color: #eee;
          color: #909399;
          border: none;
        }
        .el-tag + .el-tag {
          margin-left: 4px;
        }
        .button-new-tag {
          padding: 4px 8px;
        }
        .input-new-tag {
          margin-bottom: 4px;
          display: inline-block;
          width: 60px;
          height: 20px;
          padding: 0;
          .el-input__inner {
            height: 24px;
            line-height: 24px;
            padding: 0 8px;
          }
        }
        .el-button {
          padding: 4px 10px;
        }
      }
      .edit-tag {
        color: #409eff;
        cursor: pointer;
      }
    }
    &-status {
      display: flex;
      padding: 20px;
      border-bottom: 1px solid #e8e8e8;
      &-left {
        flex: 1;
        height: 40px;
        line-height: 40px;
        .rank {
          margin-left: 14px;
          display: inline-flex;
          align-items: center;
          .icon-check-circle-fill {
            color: #62e08f;
            font-size: 20px;
            margin-right: 4px;
          }
          .icon-warning-circle-fill {
            color: #f3b623;
            font-size: 20px;
            margin-right: 4px;
          }
        }
      }
      &-right {
        flex: 1;
        display: flex;
        justify-content: flex-end;
        .principal {
          width: 50px;
          height: 40px;
          line-height: 40px;
          padding-right: 12px;
          display: inline-block;
        }
        .principal-en{
          width: 80px;
        }
        .member-portrait {
          flex: 1;
          .player-portrait {
            width: 24px;
            height: 24px;
            object-fit: cover;
            border: 1px solid #eee;
            border-radius: 50%;
            margin-right: 5px;
          }
          .assigns-btn {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            border: 1px solid #e8e8e8;
            display: inline-block;
            position: relative;
            margin-top: 8px;
            &::after {
              content: "";
              height: 16px;
              width: 1px;
              background: #6e6d6d;
              position: absolute;
              left: 12px;
              top: 5px;
            }
            &::before {
              content: "";
              height: 1px;
              width: 16px;
              background: #6e6d6d;
              position: absolute;
              left: 5px;
              top: 12px;
            }
          }
        }
      }
    }
    &-idea {
      padding: 12px 20px;
      &-box {
        display: flex;
        margin: 10px 0 18px;
        &-portrait {
          width: 60px;
          img {
            width: 48px;
            height: 48px;
            border-radius: 100%;
          }
        }
        &-content {
          flex: 1;
          margin-right: 90px;
          .username-created-time {
            display: flex;
            margin-bottom: 10px;
            &-left {
              flex: 1;
              .username {
                font-size: 14px;
              }
              .time {
                font-size: 12px;
                color: #909399;
                padding-left: 15px;
              }
            }
            &-right {
              width: 34px;
              text-align: right;
              cursor: pointer;
            }
          }
          .idea-area {
            background: #f9f9f9;
            border: 1px solid #e8e8e8;
            border-radius: 2px;
            padding: 4px 12px;
            position: relative;
            .arrows {
              width: 15px;
              height: 15px;
              border-left: 1px solid #e8e8e8;
              border-bottom: 1px solid #e8e8e8;
              transform: rotate(45deg);
              position: absolute;
              background: #f9f9f9;
              left: -9px;
              top: 9px;
            }
            .text {
              word-break: break-all;
              word-wrap: break-word;
              margin: 12px 0;
              textarea {
                border: none;
                resize: none;
                width: 100%;
                padding: 10px 2px;
              }
              &-button {
                padding-top: 20px;
                display: flex;
                justify-content: flex-end;
              }
            }
          }
        }
      }
    }
    &-my-idea {
      padding: 12px 20px;
      border-top: 1px solid #e8e8e8;
      display: flex;
      &-portrait {
        width: 60px;
        img {
          width: 48px;
          height: 48px;
          border-radius: 100%;
          object-fit: cover;
        }
      }
      &-content {
        flex: 1;
        margin-right: 90px;
        .username {
          margin-bottom: 10px;
          font-size: 14px;
        }
        .idea-area {
          background: #f9f9f9;
          border: 1px solid #e8e8e8;
          border-radius: 2px;
          padding: 18px;
          position: relative;
          .arrows {
            width: 15px;
            height: 15px;
            border-left: 1px solid #e8e8e8;
            border-bottom: 1px solid #e8e8e8;
            transform: rotate(45deg);
            position: absolute;
            background: #f9f9f9;
            left: -9px;
            top: 9px;
          }
          textarea {
            border: none;
            resize: none;
            width: 100%;
            padding: 10px 2px;
          }
        }
        .finish {
          margin: 20px 0;
          text-align: right;
        }
      }
    }
  }
}
.operate-comment {
  .el-dropdown-menu__item {
    padding: 0;
    .action {
      display: block;
      width: 100%;
      height: 100%;
      min-width: 108px;
      text-align: center;
    }
  }
}
.new-issue-assign {
  .member-portrait {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
  }
  .el-dropdown-menu__item {
    display: flex;
    align-items: center;
  }
}
@media screen and (max-width: 768px) {
  .issue-detail-dialog {
    .el-dialog {
      width: 94%;
    }
    .issue-detail {
      &-status {
        display: block;
        &-right {
          display: block;
        }
      }
      &-idea {
        &-box {
          &-content {
            margin-right: 10px;
          }
        }
      }
      &-my-idea {
        &-content {
          margin-right: 10px;
        }
      }
    }
  }
}
</style>

<template>
  <el-dialog :visible.sync="show" :before-close="handleClose" class="new-issue">
    <div class="new-issue-title">{{$t('project.createNewIssueTitle')}}</div>
    <div class="new-issue-sketch">
      <div class="new-issue-sketch-item">
        <div class="new-issue-sketch-label" :class="{'new-issue-sketch-label-en': isEn}">{{$t("project.title")}}</div>
        <div class="new-issue-sketch-content">
          <el-input size="medium" v-model="issueTitle" :placeholder='$t("project.pleaseInputTitle")'></el-input>
        </div>
      </div>
      <div class="new-issue-sketch-item">
        <div class="new-issue-sketch-label" :class="{'new-issue-sketch-label-en': isEn}">{{$t('project.labels')}}</div>
        <div class="new-issue-sketch-content" v-loading='isTagLoading'>
          <el-tag :key="tag" v-for="tag in dynamicTags" closable :disable-transitions="false" @close="handleCloseTag(tag)">{{tag}}</el-tag>
          <el-input class="new-issue-sketch-new-input" v-show="inputVisible" :maxlength="tagMaxLength" v-model="inputValue" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm"></el-input>
          <el-button v-show="!inputVisible" size="small" @click="showInput">+ {{$t('project.newLabel')}}</el-button>
        </div>
      </div>
      <div class="new-issue-sketch-item">
        <div class="new-issue-sketch-label" :class="{'new-issue-sketch-label-en': isEn}">{{$t('project.asignees')}}</div>
        <div class="new-issue-sketch-content new-issue-sketch-asignee">
          <img v-for="(member,index) in assignedMembers" :key="index" class="new-issue-sketch-asignee-portrait" :src="member.portrait || default_portrait" alt="">
          <el-dropdown @command="handleCommand" trigger="click" placement="bottom-start">
            <span class="el-icon-plus"></span>
            <el-dropdown-menu slot="dropdown" class="new-issue-sketch-asignee-dropdown">
              <el-dropdown-item v-if="memberList.length == 0">{{$t('project.noOtherMembers')}}</el-dropdown-item>
              <el-dropdown-item v-for="member in memberList" :key="member.id" :command="member.userId">
                <i :class="['icofont',{'el-icon-check': isAssigned(member)}]"></i>
                <img class="new-issue-sketch-asignee-dropdown-portrait" :src="member.portrait || default_portrait" alt="">
                {{member.nickname || member.username}}
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
      <div class="new-issue-sketch-item">
        <div class="new-issue-sketch-label" :class="{'new-issue-sketch-label-en': isEn}">{{$t('project.write')}}</div>
        <div class="new-issue-sketch-content">
          <el-input type="textarea" :rows="4" v-model="descriptionText" :placeholder="$t('project.writeAComment')" resize="none"></el-input>
        </div>
      </div>
    </div>
    <el-button class="new-issue-finish" size="medium" :loading="cretateIssueLoading" type="primary" @click="finishedCreateIssue" :disabled="!issueTitle || !descriptionText">{{$t('project.submitIssue')}}</el-button>
  </el-dialog>
</template>
<script>
import { locale } from '@/lib/utils/i18n'
import { keepwork } from '@/api'
import _ from 'lodash'
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import { mapActions, mapGetters } from 'vuex'
import default_portrait from '@/assets/img/default_portrait.png'
import Vue from 'vue'

export default {
  name: 'NewIssue',
  props: {
    show: Boolean,
    projectId: {
      required: true
    }
  },
  data() {
    return {
      tagMaxLength: 40,
      issueTitle: '',
      dynamicTags: [],
      inputVisible: false,
      inputValue: '',
      descriptionText: '',
      default_portrait: default_portrait,
      assignedMembers: [],
      cretateIssueLoading: false,
      isTagLoading: false
    }
  },
  async mounted() {
    await this.getProjectMember({
      objectId: this.projectId,
      objectType: 5
    })
  },
  computed: {
    ...mapGetters({
      pblProjectMemberList: 'pbl/projectMemberList'
    }),
    isEn() {
      return locale === 'en-US'
    },
    memberList() {
      return this.pblProjectMemberList({ projectId: this.projectId }) || []
    },
    assignMembersId() {
      let arrId = []
      _.map(this.assignedMembers, ({ userId }) => {
        arrId.push(userId)
      })
      return arrId.join('|')
    }
  },
  methods: {
    ...mapActions({
      getProjectIssues: 'pbl/getProjectIssues',
      getProjectMember: 'pbl/getProjectMember'
    }),
    handleCloseTag(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },
    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    async checkSensitive(checkedWords) {
      let sensitiveResult = await checkSensitiveWords({ checkedWords }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) return true
      return false
    },
    checkTagValid(tagValue) {
      if (tagValue.indexOf('|') !== -1) {
        this.$message({
          showClose: true,
          message: '标签里不能包含|',
          type: 'error'
        })
        return false
      }
      return true
    },
    checkTagWhetherExist(tagValue) {
      let isExistTagIndex = _.findIndex(
        this.dynamicTags,
        tag => tag === tagValue
      )
      if (isExistTagIndex !== -1) {
        this.$message({
          showClose: true,
          message: '该标签已存在',
          type: 'error'
        })
        return true
      }
      return false
    },
    async handleInputConfirm() {
      this.inputValue = _.trim(this.inputValue, ' ')
      let inputValue = this.inputValue
      let isTagValid = this.checkTagValid(inputValue)
      if (!isTagValid) return
      let isTagExist = this.checkTagWhetherExist(inputValue)
      if (isTagExist) return
      this.isTagLoading = true
      let isSensitive = await this.checkSensitive(inputValue)
      this.isTagLoading = false
      if (isSensitive) return
      if (inputValue) this.dynamicTags.push(inputValue)
      this.inputVisible = false
      this.inputValue = ''
    },
    handleClose() {
      this.$emit('close')
      this.resetFormData()
    },
    handleCommand(userId) {
      let findedIndex = _.findIndex(this.assignedMembers, { userId })
      if (findedIndex !== -1) {
        return this.assignedMembers.splice(findedIndex, 1)
      } else {
        let targetMember = _.find(this.memberList, { userId })
        return this.assignedMembers.push(targetMember)
      }
    },
    async finishedCreateIssue() {
      this.cretateIssueLoading = true
      const sensitiveResult = await checkSensitiveWords({checkedWords:[
        this.issueTitle,
        this.descriptionText
      ]}).catch(e => console.error(e))
      this.cretateIssueLoading = false
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.issueTitle = _.get(sensitiveResult, '[0].word', this.issueTitle)
        this.descriptionText = _.get(sensitiveResult, '[1].word', this.descriptionText)
        return
      }
      let payload = {
        objectType: 5,
        objectId: this.projectId,
        title: this.issueTitle,
        content: this.descriptionText,
        tags: this.dynamicTags.join('|'),
        assigns: this.assignMembersId
      }
      await keepwork.issues
        .createIssue(payload)
        .then(res => {
          this.getProjectIssues({
            objectId: this.projectId,
            objectType: 5,
            'x-per-page': 25,
            'x-page': 1,
            'x-order': 'createdAt-desc'
          })
          this.handleClose()
          this.cretateIssueLoading = false
        })
        .catch(err => console.error(err))
    },
    isAssigned(member) {
      return this.assignedMembers.indexOf(member) !== -1 ? true : false
    },
    resetFormData() {
      this.issueTitle = ''
      this.dynamicTags = []
      this.assignedMembers = []
      this.descriptionText = ''
    }
  }
}
</script>
<style lang="scss">
.new-issue {
  .el-dialog {
    max-width: 600px;
    margin: 0 auto;
    background: #fff;
  }
  .el-dialog__header {
    padding: 0;
  }
  .el-dialog__body {
    padding: 6px 20px;
  }
  &-title {
    line-height: 60px;
    font-size: 16px;
    color: #303133;
    padding-left: 4px;
    font-weight: bold;
    border-bottom: 1px solid #e8e8e8;
    margin-bottom: 12px;
  }
  &-sketch {
    padding-left: 6px;
    &-item {
      display: flex;
      line-height: 60px;
      max-width: 600px;
    }
    &-label {
      width: 52px;
      font-size: 14px;
      color: #909399;
      &-en {
        width: 80px;
      }
    }
    &-content {
      flex: 1;
      .el-tag + .el-tag {
        margin-left: 10px;
      }
      .player {
        line-height: 38px;
        margin-bottom: 8px;
      }
    }
    &-asignee {
      line-height: 38px;
      margin-bottom: 8px;
      &-portrait {
        vertical-align: middle;
        width: 36px;
        height: 36px;
        margin: 8px 6px 0 0;
        border-radius: 50%;
        border: 1px solid #e8e8e8;
      }
      &-dropdown {
        &-portrait {
          width: 26px;
          height: 26px;
          border-radius: 50%;
          margin-right: 10px;
          object-fit: cover;
        }
        .el-dropdown-menu__item {
          display: flex;
          align-items: center;
          position: relative;
        }
        .el-icon-check {
          position: absolute;
          left: 4px;
        }
      }
      .el-icon-plus {
        top: 8px;
        position: relative;
        display: inline-block;
        width: 36px;
        height: 36px;
        color: #6e6d6d;
        border: 1px solid #e8e8e8;
        text-align: center;
        border-radius: 50%;
        line-height: 36px;
        font-size: 24px;
        cursor: pointer;
      }
    }
    &-new-input {
      margin-bottom: 4px;
      display: inline-block;
      width: 60px;
      height: 20px;
      padding: 0;
      .el-input__inner {
        padding: 0 8px;
      }
    }
  }
  &-finish {
    margin: 24px 58px;
  }
}
@media screen and (max-width: 768px) {
  .new-issue {
    .el-dialog {
      width: 90%;
    }
  }
}
</style>

<template>
  <div class="new-project container" v-loading='isLoading'>
    <div class="new-project-step-0" v-show="nowStep === 0">
      <h1 class="new-project-title">{{$t("project.newProject")}}</h1>
      <p class="new-project-info">{{$t("create.projectIsWhereWorksStart")}}<br>{{$t("create.whatYouLearnFromProject")}}</p>
      <div class="new-project-name">
        <label for="projectName" class="new-project-label">{{$t("project.projectName")}}</label>
        <el-input id="projectName" maxlength="40" v-model="newProjectData.name"></el-input>
      </div>
      <div class="new-project-type">
        <label for="projectName" class="new-project-label">{{$t("project.projectType")}}</label>
        <div class="new-project-type-box">
          <div class="new-project-type-item" :class="{'active iconfont': projectType.type === newProjectData.type}" v-for="(projectType, index) in projectTypes" :key="index" @click='selectProjectType(projectType.type)'>
            <img class="new-project-type-item-cover" :src="projectType.type === newProjectData.type ?projectType.activeIconImgSrc:projectType.iconImgSrc" alt="">
            <p class="new-project-type-item-label">{{projectType.label}}</p>
            <p class="new-project-type-item-label new-project-type-item-label-sub" v-if="projectType.subLabel">{{projectType.subLabel}}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="new-project-step-1" v-show="nowStep === 1">
      <website-binder @confirmSiteId='handleConfirmSiteId'></website-binder>
    </div>
    <el-button v-show="isFinishShow" type="primary" :disabled="isNameEmpty" @click="createNewProject">{{$t("project.createProject")}}</el-button>
    <el-button v-show="isNextShow" type="primary" :disabled="isNameEmpty" @click="goNextStep">{{$t("project.next")}}</el-button>
    <el-button v-show="isPrevShow" type="primary" @click="goPrevStep">{{$t("project.prev")}}</el-button>
  </div>
</template>
<script>
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import { mapActions } from 'vuex'
import WebsiteBinder from './common/WebsiteBinder'
import { keepwork } from '@/api'

export default {
  name: 'NewProject',
  data() {
    return {
      isLoading: false,
      nowStep: 0,
      webFinishStepCount: 1,
      projectTypes: [
        {
          type: 1,
          label: this.$t('common.paracraft'),
          subLabel: this.$t('project.3DGameAndAnim'),
          iconImgSrc: require('@/assets/pblImg/project_paracraft.png'),
          activeIconImgSrc: require('@/assets/pblImg/project_paracraft_active.png')
        },
        {
          type: 0,
          label: this.$t('create.website'),
          iconImgSrc: require('@/assets/pblImg/project_web.png'),
          activeIconImgSrc: require('@/assets/pblImg/project_web_active.png')
        }
      ],
      newProjectData: {
        name: '',
        privilege: 165,
        visibility: 0,
        type: 1,
        description: '',
        siteId: null,
        tags: 'Paracraft|3D'
      }
    }
  },
  computed: {
    isNameEmpty() {
      let { name } = this.newProjectData
      return !name || name.length == 0
    },
    isWebType() {
      return this.newProjectData.type === 0
    },
    isFinishShow() {
      return !this.isWebType
    },
    isNextShow() {
      return this.isWebType && this.nowStep !== this.webFinishStepCount
    },
    isPrevShow() {
      return this.isWebType && this.nowStep === this.webFinishStepCount
    }
  },
  methods: {
    ...mapActions({
      pblCreateNewProject: 'pbl/createNewProject'
    }),
    selectProjectType(type) {
      this.newProjectData.type = type
      this.newProjectData.tags = type == 0 ? '网站' : 'Paracraft|3D'
    },
    handleConfirmSiteId({ siteId }) {
      this.isWebType && siteId && (this.newProjectData.siteId = siteId)
      this.createNewProject()
    },
    async checkProjectName() {
      this.isLoading = true
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: this.newProjectData.name
      }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.isLoading = false
        return false
      }
      let name = this.newProjectData.name
      keepwork.projects
        .getUserProjectsByName({ name })
        .then(res => {
          if (res.count > 0) {
            this.$message.error(this.$t('project.projectAlreadyExists'))
            this.isLoading = false
            return false
          }
        })
        .catch(e => {
          console.error(e)
        })
      this.isLoading = false
      return true
    },
    async createNewProject() {
      if (!(await this.checkProjectName())) {
        return
      }
      this.isLoading = true
      await this.pblCreateNewProject(this.newProjectData)
        .then(projectDetail => {
          this.isLoading = false
          this.$message({
            type: 'success',
            message: this.$t('project.projectCreated')
          })
          let projectId = projectDetail.id
          projectId && this.$router.push(`/project/${projectId}`)
        })
        .catch(error => {
          if (error.response.status == 409) {
            this.$message.error(this.$t('project.projectAlreadyExists'))
          } else {
            this.$message.error(this.$t('project.ProjectCreationFailed'))
          }
          this.isLoading = false
        })
    },
    goPrevStep() {
      this.nowStep--
    },
    async goNextStep() {
      if (this.nowStep === 0) {
        let isNameValid = await this.checkProjectName()
        if (!isNameValid) {
          return
        }
      }
      this.nowStep++
    }
  },
  components: {
    WebsiteBinder
  }
}
</script>
<style lang="scss">
.new-project {
  padding: 55px 0;
  &-title {
    font-size: 24px;
    color: #303133;
    margin: 0 0 10px 0;
  }
  &-info {
    font-size: 14px;
    color: #909399;
    margin: 10px 0 30px;
    line-height: 24px;
  }
  &-label {
    font-size: 14px;
    color: #909399;
    margin-bottom: 15px;
    display: block;
  }
  &-type {
    &-box {
      display: flex;
    }
    &-item {
      width: 190px;
      height: 186px;
      border: 1px solid #e8e8e8;
      text-align: center;
      margin: 0 20px 25px 0;
      position: relative;
      box-sizing: border-box;
      overflow: hidden;
      border-radius: 4px;
      cursor: pointer;
      &-cover {
        padding: 40px 36px 0;
      }
      &-label {
        position: absolute;
        left: 0;
        width: 100%;
        bottom: 32px;
        color: #303133;
        margin: 0;
        font-size: 14px;
        font-weight: bold;
        &-sub {
          font-size: 12px;
          bottom: 16px;
          color: #909399;
          font-weight: normal;
        }
      }
    }
    &-item:last-child {
      margin: 0 0 25px 0;
    }
    &-item.active {
      border: 2px solid #2397f3;
      box-shadow: 0 0 8px 3px rgba(35, 151, 243, 0.2);
    }
    &-item.active::before {
      content: '\E600';
      color: #fff;
      display: inline-block;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background-color: #2397f3;
      position: absolute;
      right: -6px;
      top: -8px;
      text-align: left;
      padding-left: 7px;
      line-height: 36px;
      box-sizing: border-box;
      font-size: 14px;
    }
  }
  &-name {
    margin-bottom: 24px;
  }
  .el-input {
    width: 600px;
  }
}
</style>

<template>
  <div class="project-detail-page">
    <div v-if="isProjectExist && isLoginUserVisible">
      <project-header class="project-detail-page-header" :projectDetail="pblProjectDetail" :editingUserId='editingUserId' :editingProjectUsername='editingProjectUsername' v-if="!isFirstGettingData" :isLoginUserEditable='loginUserIsProjectOwner' :isProhibitView="isProhibitView" ></project-header>
      <router-view v-if="!isFirstGettingData" :pblProjectDetail='pblProjectDetail' :projectId='projectId' :originProjectUsername='editingProjectUsername' :projectOwnerPortrait='projectOwnerPortrait' :isLoginUserEditable='loginUserIsProjectOwner' :projectApplyState='projectApplyState' :isLoginUsercommentable='isLoginUsercommentable' :isCommentClosed='isCommentClosed' :isProjectStopRecruit='isProjectStopRecruit' :isProhibitView="isProhibitView" :isProhibitEdit="isProhibitEdit"></router-view>
    </div>
    <div class="project-detail-page-not-found" v-if="!isProjectExist || !isLoginUserVisible">
      <img src='@/assets/img/404.png' alt="">
      <p class="project-detail-page-not-found-info">404</p>
    </div>
  </div>
</template>
<script>
import ProjectHeader from './common/ProjectHeader'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'ProjectDetailPage',
  async created() {
    this.initProjectDetail()
  },
  computed: {
    ...mapGetters({
      pblProjectApplyState: 'pbl/projectApplyState',
      loginUserId: 'user/userId',
      isLogined: 'user/isLogined',
      projectDetail: 'pbl/projectDetail',
      getDetailByUserId: 'user/getDetailByUserId',
      loginUsername: 'user/username',
      projectMemberList: 'pbl/projectMemberList'
    }),
    pblProjectDetail() {
      return this.projectDetail({ projectId: this.projectId })
    },
    projectId() {
      return _.toNumber(_.get(this.$route, 'params.id'))
    },
    projectApplyState() {
      return this.pblProjectApplyState({
        projectId: this.projectId,
        userId: this.loginUserId
      })
    },
    isLoginUserBeProjectMember() {
      return this.loginUserIsProjectOwner || this.projectApplyState === 1
    },
    projectPrivilege() {
      return _.get(this.pblProjectDetail, 'privilege')
    },
    isProjectPrivate() {
      return _.get(this.pblProjectDetail, 'visibility') === 1
    },
    isLoginUserVisible() {
      return !this.isProjectPrivate || this.isLoginUserBeProjectMember
    },
    isCommentForMember() {
      return (this.projectPrivilege & 8) > 0
    },
    isLoginUsercommentable() {
      return !this.isCommentForMember || this.isLoginUserBeProjectMember
    },
    isCommentClosed() {
      return (this.projectPrivilege & 16) > 0
    },
    isBoardViewForMember() {
      return (this.projectPrivilege & 64) > 0
    },
    isBoardEditForMember() {
      return (this.projectPrivilege & 256) > 0
    },
    isProjectStopRecruit() {
      return (this.projectPrivilege & 2) > 0
    },
    editingProjectUser() {
      let userId = this.editingUserId
      return this.getDetailByUserId({ userId })
    },
    editingProjectUsername() {
      return _.get(this.editingProjectUser, 'username')
    },
    projectOwnerPortrait() {
      return _.get(this.editingProjectUser, 'portrait')
    },
    loginUserIsProjectOwner() {
      return this.loginUsername === this.editingProjectUsername
    },
    projectMembers() {
      return this.projectMemberList({ projectId: this.projectId })
    },
    projectMembers() {
      return this.projectMemberList({ projectId: this.projectId })
    },
    isProhibitView() {
      return this.isBoardViewForMember && !this.isLoginUserBeProjectMember
    },
    isProhibitEdit() {
      return this.isBoardEditForMember && !this.isLoginUserBeProjectMember
    }
  },
  data() {
    return {
      isLoading: true,
      editingUserId: undefined,
      isFirstGettingData: true,
      isProjectExist: true
    }
  },
  methods: {
    ...mapActions({
      pblGetApplyState: 'pbl/getApplyState',
      pblGetProjectDetail: 'pbl/getProjectDetail',
      getUserDetailByUserId: 'user/getUserDetailByUserId',
      getFavoriteState: 'pbl/getFavoriteState',
      getStarState: 'pbl/getStarState',
    }),
    async initProjectDetail() {
      this.isFirstGettingData = true
      this.isLoading = true
      await this.pblGetProjectDetail({ projectId: this.projectId }).catch(
        error => {
          let statusCode = _.get(error, 'response.status', 404)
          if (statusCode === 404) {
            this.isProjectExist = false
          }
        }
      )
      await this.initProjectHeaderDetail()
      if (this.isLogined) {
        await this.pblGetApplyState({
          objectId: this.projectId,
          objectType: 5,
          applyType: 0,
          applyId: this.loginUserId
        })
      }
      this.isFirstGettingData = false
      this.isLoading = false
    },
    async initProjectHeaderDetail() {
      this.editingUserId = _.get(this.pblProjectDetail, 'userId')
      let userId = this.editingUserId
      let objectId = this.projectId
      let objectType = 5
      let promiseArray = [
        this.getUserDetailByUserId({ userId }),
        this.getFavoriteState({ objectId, objectType }),
        this.getStarState({ projectId: objectId })
      ]
      await Promise.all(
        _.map(promiseArray, promiseItem => {
          return promiseItem.catch(error => {
            return error
          })
        })
      )
    }
  },
  components: {
    ProjectHeader
  },
  watch: {
    $route: function(val) {
      this.initProjectDetail()
    }
  }
}
</script>
<style lang="scss">
.project-detail-page {
  background-color: #f5f5f5;
  &-not-found {
    text-align: center;
    padding-top: 40px;
    font-size: 28px;
    font-weight: bold;
  }
}
</style>

<template>
  <div class="project-index">
    <div class="container hidden-xs-only">
      <div class="project-index-sidebar">
        <project-intro class="project-index-sidebar-item" :originProjectDetail='pblProjectDetail' :projectId='projectId' :isLoginUserEditable='isLoginUserEditable'></project-intro>
        <project-tags class="project-index-sidebar-item" :originProjectDetail='pblProjectDetail' :projectId='projectId' :isLoginUserEditable='isLoginUserEditable'></project-tags>
        <project-joined-members-list class="project-index-sidebar-item" type='card' :projectId='projectId' :projectOwnerPortrait='projectOwnerPortrait' :projectDetail='pblProjectDetail' :originProjectUsername='originProjectUsername'></project-joined-members-list>
        <project-boards v-if="!isProhibitView" :projectId='projectId' :projectDetail='pblProjectDetail' :isProhibitView="isProhibitView" :isProhibitEdit="isProhibitEdit"></project-boards>
      </div>
      <div class="project-index-main">
        <project-basic-info descriptionId='projectBasicInfo1' class="project-index-basic" :originProjectDetail='pblProjectDetail' :projectOwnerUsername='originProjectUsername' :projectApplyState='projectApplyState' :projectId='projectId' :isProjectStopRecruit='isProjectStopRecruit' :isLoginUserEditable='isLoginUserEditable'></project-basic-info>
        <project-comments v-if='!isCommentClosed' class="project-index-comments" :projectId='projectId' :isLoginUsercommentable='isLoginUsercommentable'></project-comments>
      </div>
    </div>
    <div class="container-phone hidden-sm-and-up">
      <project-basic-info descriptionId='projectBasicInfo2' class="project-index-basic" :originProjectDetail='pblProjectDetail' :projectOwnerUsername='originProjectUsername' :projectApplyState='projectApplyState' :projectId='projectId' :isProjectStopRecruit='isProjectStopRecruit' :isLoginUserEditable='isLoginUserEditable'></project-basic-info>
      <project-tags class="project-index-sidebar-item" :originProjectDetail='pblProjectDetail' :projectId='projectId' :isLoginUserEditable='isLoginUserEditable'></project-tags>
      <project-joined-members-list class="project-index-sidebar-item" type='card' :projectId='projectId' :projectOwnerPortrait='projectOwnerPortrait' :projectDetail='pblProjectDetail' :originProjectUsername='originProjectUsername'></project-joined-members-list>
      <project-boards v-if="!isProhibitView" :projectId='projectId' :projectDetail='pblProjectDetail' :isProhibitView="isProhibitView" :isProhibitEdit="isProhibitEdit"></project-boards>
      <project-comments v-if='!isCommentClosed' id="project-index-phone-comments" class="project-index-comments" :projectId='projectId' :isLoginUsercommentable='isLoginUsercommentable'></project-comments>
    </div>
  </div>
</template>
<script>
import ProjectIntro from './common/ProjectIntro'
import ProjectTags from './common/ProjectTags'
import ProjectJoinedMembersList from './common/ProjectJoinedMembersList'
import ProjectBasicInfo from './common/ProjectBasicInfo'
import ProjectComments from './common/ProjectComments'
import ProjectBoards from './common/ProjectBoards'
import { keepwork } from '@/api'
export default {
  name: 'ProjectIndex',
  props: {
    pblProjectDetail: {
      type: Object,
      required: true
    },
    originProjectUsername: {
      type: String,
      required: true
    },
    projectOwnerPortrait: String,
    projectId: {
      type: Number,
      required: true
    },
    isLoginUserEditable: {
      type: Boolean,
      default: false
    },
    isLoginUsercommentable: {
      type: Boolean,
      default: true
    },
    isCommentClosed: {
      type: Boolean,
      default: false
    },
    isProjectStopRecruit: {
      type: Boolean,
      default: false
    },
    isProhibitView: {
      type: Boolean,
      default: false
    },
    isProhibitEdit: {
      type: Boolean,
      default: false
    },
    projectApplyState: Number
  },
  async created() {
    await keepwork.projects.visitProject(this.projectId)
  },
  computed: {
    originProjectName() {
      return _.get(this.pblProjectDetail, 'name')
    }
  },
  components: {
    ProjectIntro,
    ProjectTags,
    ProjectJoinedMembersList,
    ProjectBasicInfo,
    ProjectComments,
    ProjectBoards
  }
}
</script>

<style lang="scss">
.project-index {
  padding-top: 24px;
  &-sidebar {
    width: 276px;
    margin-right: 24px;
    &-item {
      margin-bottom: 24px;
    }
  }
  &-main {
    flex: 1;
    min-width: 0;
  }
  & > .container {
    display: flex;
  }
  &-basic {
    margin-bottom: 24px;
    border: 1px solid #e8e8e8;
    border-radius: 4px;
  }
  &-comments {
    border: 1px solid #e8e8e8;
    border-radius: 4px;
  }
}

@media (max-width: 768px) {
  .project-index {
    padding-top: 10px;
    & > .container-phone {
      display: block;
    }
    &-basic {
      margin-bottom: 8px;
    }
    &-sidebar {
      &-item {
        margin-bottom: 8px;
      }
    }
  }
}
</style>

<template>
  <div class="project-white-board">
    <div class="project-white-board-content">
      <div class="project-white-board-header">
        <div class="project-white-board-header-search">
          <el-input size="medium" :placeholder="$t('project.searchMethod')" v-model="searchKeyWord" class="input-with-select" @keyup.enter.native="searchIssue">
            <el-button slot="append" icon="el-icon-search" @click="searchIssue"></el-button>
          </el-input>
        </div>
        <div class="project-white-board-header-filter hidden-sm-and-down">
          {{$t("project.filter")}}：
          <span class="project-white-board-header-rank" @click="showAllIssues">{{$t("project.all")}}({{issuesOpenCount + issuesCloseCount}})</span>
          <span class="project-white-board-header-rank" @click="showUnfinishedIssues">
            <i class="iconfont icon-warning-circle-fill"></i>{{$t("project.inProgress")}} ({{issuesOpenCount}})
          </span>
          <span class="project-white-board-header-rank" @click="showFinishedIssues">
            <i class="iconfont icon-check-circle-fill"></i>{{$t("project.finished")}} ({{issuesCloseCount}})
          </span>
        </div>
        <el-button class="project-white-board-header-new" type="primary" :disabled="isProhibitEdit" size="medium" @click="goNewIssue">+ {{$t("project.createNewIssue")}}</el-button>
      </div>
      <div class="project-white-board-list">
        <div class="project-white-board-list-item" v-for="(issue,index) in projectIssues" :key="index">
          <div class="project-white-board-list-brief">
            <div class="project-white-board-list-title" @click="goIssueDetail(issue)">
              <i :class="['iconfont', issue.state == 0 ? 'icon-warning-circle-fill':'icon-check-circle-fill']"></i>
              <span class="project-white-board-list-text" :title="issue.title">{{issue.title}}</span>
              <span class="project-white-board-list-number">#{{issue.no}}</span>
            </div>
            <div class="project-white-board-list-intro">
              <span class="project-white-board-list-time">{{isEn ? $t('common.update')+'d' : ''}} {{relativeTime(issue.updatedAt)}}{{isEn ? '' : $t('common.update')}}</span>
              <span class="project-white-board-list-creator">
                {{$t("project.createBy")}}
                <span class="project-white-board-list-creator-name">{{issue.user.username}}</span>
                {{$t("project.created")}}
              </span>
              <div class="project-white-board-list-tags">
                <span class="project-white-board-list-tags-item" v-for="(tag,i) in issueTagArr(issue)" :key="i">{{tag}}</span>
              </div>
            </div>
          </div>
          <div class="project-white-board-list-asignees  hidden-sm-and-down" v-if="issue.assigns.length > 0">
            <img class="project-white-board-list-asignees-item" v-for="player in issue.assigns" :key="player.id" :src="player.portrait || default_portrait" alt="" :title="player.username">
          </div>
        </div>
      </div>
    </div>
    <new-issue v-if="isNewIssueRendered" :show="showNewIssue" :projectId="projectId" @close="closeNewIssue"></new-issue>
    <issue-detail v-if="showIssueDetail" :show="showIssueDetail" @close="closeIssueDetail" :issue="selectedIssue" :projectDetail="pblProjectDetail" :isProhibitEdit="isProhibitEdit" :currPage="page" :searchKeyWord="searchKeyWord" :state='state'></issue-detail>
    <div class="all-issue-pages" v-if="issuesCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="issuesCount">
      </el-pagination>
    </div>
  </div>
</template>
<script>
import 'element-ui/lib/theme-chalk/display.css'
import NewIssue from './NewIssue'
import IssueDetail from './IssueDetail'
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'
import moment from 'moment'
import 'moment/locale/zh-cn'
import { locale } from '@/lib/utils/i18n'
import default_portrait from '@/assets/img/default_portrait.png'

export default {
  name: 'ProjectWhiteBoard',
  data() {
    return {
      projectIssues: [],
      showNewIssue: false,
      showIssueDetail: false,
      isNewIssueRendered: false,
      // isIssueDetailRendered: false,
      searchKeyWord: '',
      default_portrait,
      selectedIssue: {},
      perPage: 25,
      page: 1,
      state: null
    }
  },
  props: {
    isProhibitView: {
      type: Boolean,
      default: false
    },
    isProhibitEdit: {
      type: Boolean,
      default: false
    }
  },
  components: {
    NewIssue,
    IssueDetail
  },
  computed: {
    ...mapGetters({
      issuesList: 'pbl/issuesList',
      projectDetail: 'pbl/projectDetail',
      isLogined: 'user/isLogined'
    }),
    projectIssueList() {
      return _.get(this.issuesList({ projectId: this.projectId }), 'rows', [])
    },
    issuesCount() {
      return _.get(this.issuesList({ projectId: this.projectId }), 'count', 0)
    },
    issuesOpenCount() {
      return _.get(
        this.issuesList({ projectId: this.projectId }),
        'openCount',
        0
      )
    },
    issuesCloseCount() {
      return _.get(
        this.issuesList({ projectId: this.projectId }),
        'closeCount',
        0
      )
    },
    unfinishedProjectIssueList() {
      return _.filter(this.projectIssueList, i => i.state === 0)
    },
    finishedProjectIssueList() {
      return _.filter(this.projectIssueList, i => i.state === 1)
    },
    isEn() {
      return locale === 'en-US'
    },
    projectId() {
      return _.get(this.$route, 'params.id')
    },
    pblProjectDetail() {
      return this.projectDetail({ projectId: this.projectId })
    }
  },
  async mounted() {
    if (this.isProhibitView) {
      return this.$router.push({
        name: 'ProjectIndexPage',
        params: { id: this.projectId }
      })
    }
    await this.targetPage(this.page)
    this.projectIssues = this.projectIssueList
  },
  watch: {
    projectIssueList(newIssueList) {
      this.projectIssues = _.concat(newIssueList)
    },
    async searchKeyWord(key, oldKey) {
      let payload = {
        objectId: this.projectId,
        objectType: 5,
        'x-per-page': this.perPage,
        'x-page': 1,
        'x-order': 'createdAt-desc'
      }
      if (key) payload['text-like'] = `%${key}%`
      await this.getProjectIssues(payload)
      this.projectIssues = this.projectIssueList
    }
  },
  methods: {
    ...mapActions({
      getProjectIssues: 'pbl/getProjectIssues',
      getProjectMember: 'pbl/getProjectMember',
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    async targetPage(page) {
      this.page = page
      let payload = {
        objectId: this.projectId,
        objectType: 5,
        'x-per-page': this.perPage,
        'x-page': page,
        'x-order': 'createdAt-desc',
        'text-like': this.searchKeyWord ? `%${this.searchKeyWord}%` : undefined,
        state: _.isNull(this.state) ? undefined : this.state
      }
      await this.getProjectIssues(payload)
    },
    searchIssue() {
      this.targetPage(1)
      this.projectIssues = this.projectIssueList
    },
    goNewIssue() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      if (!this.isProhibitEdit) {
        this.isNewIssueRendered = true
        this.showNewIssue = true
      }
    },
    closeNewIssue() {
      this.showNewIssue = false
    },
    goIssueDetail(issue) {
      this.selectedIssue = issue
      // this.isIssueDetailRendered = true
      this.showIssueDetail = true
    },
    closeIssueDetail() {
      this.showIssueDetail = false
    },
    showAllIssues() {
      this.state = null
      this.targetPage(1)
    },
    async showFinishedIssues() {
      this.state = 1
      this.targetPage(1)
    },
    async showUnfinishedIssues() {
      this.state = 0
      this.targetPage(1)
    },
    relativeTime(time) {
      const offset = moment().utcOffset()
      this.isEn ? moment.locale('en') : moment.locale('zh-cn')
      return moment(time)
        .utcOffset(offset)
        .fromNow()
    },
    sortByUpdateAt(obj1, obj2) {
      return obj1.updatedAt >= obj2.updatedAt ? -1 : 1
    },
    issueTagArr(issue) {
      if (_.get(issue, 'tags', '')) {
        return _.get(issue, 'tags', '').split('|')
      }
    }
  }
}
</script>

<style lang="scss">
.project-white-board {
  background: #f5f5f5;
  padding: 24px 0 120px;
  &-content {
    background: #fff;
    max-width: 1200px;
    border: 1px solid #e8e8e8;
    box-sizing: border-box;
    margin: 0 auto;
  }
  &-header {
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 16px;
    border-bottom: 1px solid #e8e8e8;
    &-search {
      width: 340px;
      .el-input-group__append {
        background: #fff;
      }
    }
    &-filter {
      flex: 1;
      font-size: 12px;
      padding-left: 40px;
      display: flex;
      align-items: center;
    }
    &-rank {
      margin-left: 14px;
      display: inline-flex;
      align-items: center;
      cursor: pointer;
      .icon-check-circle-fill {
        color: #62e08f;
        font-size: 20px;
        margin-right: 4px;
      }
      .icon-warning-circle-fill {
        color: #f3b623;
        font-size: 20px;
        margin-right: 4px;
      }
      &:hover {
        color: #409eff;
      }
    }
    &-new {
      width: 116px;
    }
  }
  &-list {
    width: 100%;
    &-item {
      padding: 6px 16px;
      display: flex;
      color: #909399;
      border-bottom: 1px solid #f5f5f5;
      &:last-child {
        border-bottom: none;
      }
    }
    &-brief {
      flex: 1;
    }
    &-title {
      display: flex;
      align-items: center;
      line-height: 35px;
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
      .iconfont {
        font-size: 22px;
        margin-right: 13px;
      }
      .icon-warning-circle-fill {
        color: #f3b623;
      }
      .icon-check-circle-fill {
        color: #62e08f;
      }
    }
    &-text {
      cursor: pointer;
      display: inline-block;
      max-width: 80%;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      color: #303133;
    }
    &-number {
      margin-left: 10px;
    }
    &-intro {
      padding-left: 35px;
      font-size: 12px;
    }
    &-time {
      margin-right: 8px;
    }
    &-creator {
      margin-right: 20px;
      &-name {
        color: #409eff;
      }
    }
    &-tags {
      display: inline-block;
      &-item {
        background: #eee;
        display: inline-block;
        padding: 2px 4px;
        border-radius: 2px;
        margin-right: 5px;
      }
    }
    &-asignees {
      width: 300px;
      display: flex;
      align-items: center;
      flex-direction: row-reverse;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      &-item {
        width: 24px;
        height: 24px;
        object-fit: cover;
        border: 1px solid #eee;
        border-radius: 50%;
        margin-right: 5px;
      }
    }
  }
  .all-issue-pages {
    margin: 50px auto 0;
    text-align: center;
  }
}
</style>

<template>
  <div class="game-entry">
    <el-dropdown class="game-entry-dropdown" placement="bottom-start" @visible-change='handleVisibleChange' @command='toJoin'>
      <div class="el-dropdown-link">
        {{$t('common.contestEntry')}}<i class="el-icon-caret-bottom"></i>
      </div>
      <el-dropdown-menu v-loading='isLoading' slot="dropdown">
        <el-dropdown-item v-show="filteredDuplicateGames.length > 0" v-for='(game, index) in filteredDuplicateGames' :key='index' :command='projectJoinedGames && projectJoinedGames.name === game ? undefined : game'>
          {{game}}<span v-if="projectJoinedGames && projectJoinedGames.name === game" class="game-entry-joined">已参赛</span>
        </el-dropdown-item>
        <el-dropdown-item class="game-entry-empty" v-show="filteredDuplicateGames.length == 0">{{$t('project.noGames')}}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <el-dialog class="game-entry-submit" :visible.sync="isSubmitWorkVisible" v-if="isSubmitWorkVisible" width="614px" :before-close="closeSubmitDialog">
      <submit-work :selectedGameAndProject='selectedGameAndProject' @close='closeSubmitDialog' @submitSuccess="handleSubmitSuccess"></submit-work>
    </el-dialog>
    <el-dialog class="game-entry-hint-dialog" :visible.sync="isHintVisible" width="375px" center :before-close="closeHintDialog">
      <p class="game-entry-hint-dialog-text">请完善个人信息</p>
      <p class="game-entry-hint-dialog-text">包括姓名、手机号、出生年月、邮箱、QQ</p>
      <a href="/u/p/userData" target="_blank" class="game-entry-hint-dialog-btn">现在就去</a>
    </el-dialog>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import SubmitWork from '@/components/common/SubmitWork'
export default {
  name: 'GameEntry',
  props: {
    projectId: {
      required: true
    },
    originProjectDetail: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isSubmitWorkVisible: false,
      isHintVisible: false,
      isLoading: false,
      selectedGameAndProject: undefined
    }
  },
  computed: {
    ...mapGetters({
      loginUserDetail: 'user/profile',
      pblGamesList: 'pbl/gamesList',
      pblProjectJoinedGames: 'pbl/projectJoinedGames'
    }),
    projectJoinedGames() {
      return this.pblProjectJoinedGames({ projectId: this.projectId })
    },
    inProgressGames() {
      return _.filter(this.pblGamesList.rows, game => {
        let startTime = new Date(game.startDate).getTime()
        let endTime = new Date(game.endDate).getTime()
        let nowTime = new Date().getTime()
        return nowTime >= startTime && nowTime <= endTime
      })
    },
    filteredDuplicateGames() {
      const inProgressGamesFilter = _.filter(this.inProgressGames, game => !['全国青少年科技创新大赛','全国中小学科学影像节','全国中小学信息技术创新与实践活动'].includes(game.name))
      let groupedGames = _.groupBy(inProgressGamesFilter, game => game.name)
      return _.keys(groupedGames)
    },
    isUserinfoSatisfied() {
      return (
        this.loginUserDetail.info &&
        this.loginUserDetail.info.name &&
        this.loginUserDetail.realname &&
        this.loginUserDetail.info.birthdate &&
        this.loginUserDetail.email &&
        this.loginUserDetail.info.qq
      )
    }
  },
  methods: {
    ...mapActions({
      pblGetGamesList: 'pbl/getGamesList',
      pblGetProjectGames: 'pbl/getProjectGames'
    }),
    async handleVisibleChange(isVisible) {
      if (isVisible) {
        this.isLoading = true
        await this.pblGetGamesList().catch()
        await this.pblGetProjectGames({ projectId: this.projectId }).catch()
        this.isLoading = false
      }
    },
    setSelectedGame(gameName) {
      this.selectedGameAndProject = {
        game: _.find(this.inProgressGames, { name: gameName }),
        projectId: this.projectId,
        originProjectDetail: this.originProjectDetail
      }
      return true
    },
    checkUserInfoMeetDemmand() {},
    showJoinComp() {
      this.isSubmitWorkVisible = true
    },
    toJoin(gameName) {
      if (!this.isUserinfoSatisfied) {
        this.isHintVisible = true
        return
      }
      gameName && this.setSelectedGame(gameName) && this.showJoinComp()
    },
    handleSubmitSuccess() {
      this.$message({
        message: '参赛成功！',
        type: 'success'
      })
      this.closeSubmitDialog()
    },
    closeHintDialog() {
      this.isHintVisible = false
    },
    closeSubmitDialog() {
      this.isSubmitWorkVisible = false
    }
  },
  components: {
    SubmitWork
  }
}
</script>
<style lang="scss">
.game-entry {
  &-dropdown {
    .el-dropdown-link {
      height: 38px;
      line-height: 38px;
      border: 1px solid #dcdfe6;
      border-radius: 4px;
      padding: 0 12px;
      color: #606266;
      cursor: pointer;
    }
    .el-icon-caret-bottom {
      color: #909399;
    }
  }
  &-joined {
    color: #2397f3;
    margin-left: 4px;
  }
  &-empty {
    color: #c0c4cc;
  }
  &-submit {
    .el-dialog__body {
      padding: 10px 80px;
    }
  }
  &-hint-dialog {
    &-text {
      text-align: center;
      color: #333;
      font-size: 16px;
    }
    &-btn {
      width: 90%;
      margin: 40px auto;
      display: block;
      width: 285px;
      height: 44px;
      line-height: 44px;
      color: #fff;
      text-align: center;
      background: #409eff;
      border-radius: 5px;
      text-decoration: none;
      font-size: 16px;
    }
  }
}
</style>
<template>
  <div class="project-applied-list">
    <el-table :data="appliedList" border style="width: 100%" class="project-applied-list-table" v-loading='isLoading'>
      <el-table-column prop="object.username" :label="$t('project.username')" width="160">
      </el-table-column>
      <el-table-column :label="$t('project.applyAt')" width="160">
        <template slot-scope="scope">{{scope.row.updatedAt | formatDate(formatType)}}</template>
      </el-table-column>
      <el-table-column prop="legend" :label="$t('project.message')">
      </el-table-column>
      <el-table-column :label="$t('project.operations')" class-name='project-applied-list-table-operate' width="160">
        <template slot-scope="scope">
          <el-button size="mini" @click="approveApply(scope.row)" v-if="scope.row.state == 0">{{$t('project.approve')}}</el-button>
          <el-button size="mini" @click="rejectApply(scope.row)" v-if="scope.row.state == 0">{{$t('project.reject')}}</el-button>
          <span class="project-applied-list-table-reject" v-if="scope.row.state == 2">{{$t('project.rejected')}}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import moment from 'moment'
export default {
  name: 'ProjectAppliedList',
  props: {
    projectId: {
      required: true
    }
  },
  async created() {
    this.isLoading = true
    await this.getProjectApplyList({
      objectId: this.projectId,
      objectType: 5,
      applyType: 0
    })
    this.isLoading = false
  },
  data() {
    return {
      isLoading: false,
      formatType: 'YYYY/MM/DD'
    }
  },
  computed: {
    ...mapGetters({
      pblProjectApplyList: 'pbl/projectApplyList'
    }),
    allAppliedList() {
      return this.pblProjectApplyList({ projectId: this.projectId })
    },
    appliedList() {
      return _.filter(this.allAppliedList, obj => obj.state != 1)
    }
  },
  methods: {
    ...mapActions({
      getProjectApplyList: 'pbl/getProjectApplyList',
      pblChangeApplyState: 'pbl/changeApplyState'
    }),
    async changeApplyState({ applyDetail, state, successMessage }) {
      let { id } = applyDetail
      this.isLoading = true
      await this.pblChangeApplyState({
        id,
        state: state,
        objectId: this.projectId,
        objectType: 5,
        applyType: 0
      })
        .then(() => {
          this.isLoading = false
          this.$message({
            type: 'success',
            message: successMessage || '操作成功'
          })
        })
        .catch(error => {
          this.isLoading = false
          console.log(error)
        })
    },
    async approveApply(applyDetail) {
      this.changeApplyState({
        applyDetail,
        state: 1,
        successMessage: '成功同意成员加入项目！'
      })
    },
    async rejectApply(applyDetail) {
      this.changeApplyState({
        applyDetail,
        state: 2,
        successMessage: '成功拒绝成员加入项目！'
      })
    }
  },
  filters: {
    formatDate(date, formatType) {
      return moment(date).format(formatType)
    }
  }
}
</script>
<style lang="scss">
.project-applied-list {
  .el-button + .el-button {
    margin-left: 8px;
  }
  .el-table__row .cell {
    color: #303133;
  }
  .cell {
    padding: 0 24px;
  }
  .el-table--border th:first-child .cell,
  .el-table--border td:first-child .cell {
    padding-left: 24px;
  }
  &-table {
    td,
    th {
      padding: 4px 0;
      font-weight: normal;
    }
    &-operate {
      .cell {
        padding: 0 12px;
        text-align: center;
      }
      .el-button--mini {
        width: 60px;
        padding: 3px;
      }
    }
    &-reject {
      color: #c0c4cc;
      font-size: 12px;
    }
  }
}
</style>
<template>
  <div class="project-basic-info">
    <div class="project-basic-info-header">
      <p class="project-basic-info-name">{{originProjectDetail.name}}
        <img class="project-basic-info-picked" :title="$t('home.selectedProjects')" v-if="originProjectDetail.choicenessNo" src="@/assets/pblImg/picked.png" alt="">
        <span class="project-basic-info-state" v-if="!isProjectStopRecruit">{{$t("explore.recruiting")}}</span>
      </p>
      <p class="project-basic-info-more">
        <span class="project-basic-info-more-created">{{$t("project.createBy")}}
          <span class="project-basic-info-more-username">{{projectOwnerUsername}}</span>
          {{$t("project.created")}}
        </span>
        <span class="project-basic-info-more-viewcount">
          <i class="icon-browse_fill iconfont"></i>{{originProjectDetail.visit + 1}}
        </span>
        <span class="project-basic-info-more-starcount">
          <i class="icon-like-fill iconfont"></i>{{originProjectDetail.star}}
        </span>
        <span class="project-basic-info-more-commentcount">
          <i class="icon-message_fill iconfont"></i>{{originProjectDetail.comment}}
        </span>
      </p>
    </div>
    <div class="project-basic-info-detail">
      <div class="project-basic-info-detail-cover" v-loading='isCoverZoneLoading'>
        <img v-show="!isVideoShow" class="project-basic-info-detail-cover-image" :src='tempCoverUrl || defaultCoverUrl' alt="" @load="coverImageLoaded">
        <video v-show="isVideoShow" class="project-basic-info-detail-cover-video" :src="tempVideoUrl" controls></video>
        <p v-if="isLoginUserEditable" class="project-basic-info-detail-cover-cursor show-on-hover" @click="showMediaSkyDriveDialog"><i class="el-icon-edit-outline"></i>{{$t("project.changeImageOrVideo")}}</p>
      </div>
      <div class="project-basic-info-detail-message">
        <p class="project-basic-info-detail-message-item"><label>{{$t("project.projectType")}}:</label>{{ projectType | projectTypeFilter(projectTypes) }}</p>
        <p class="project-basic-info-detail-message-item"><label>{{$t("project.projectId")}}:</label>{{originProjectDetail.id}}</p>
        <p class="project-basic-info-detail-message-item"><label>{{$t("project.createTime")}}:</label>{{originProjectDetail.createdAt | formatDate(formatType)}}</p>
        <!-- <p class="project-basic-info-detail-message-item"><label>当前版本:</label>12.1</p> -->
        <project-grade v-if="!isWebType" :projectDetail='originProjectDetail'></project-grade>
        <div class="project-basic-info-detail-operations">
          <el-button type="primary" @click="toProjectPage" v-show="visitButtonVisiable">{{ buttonName }}</el-button>
          <el-button @click="toEditWebsite" plain v-if="isWebType && (isProjectOwner || isLoginUserEditableForProjectSite)">{{toggleSetWebsiteWord}}</el-button>
          <el-button :disabled="isApplied" :loading='isApplyButtonLoading' plain v-show="!isLoginUserEditable && !isLoginUserBeProjectMember && !isProjectStopRecruit" @click="showApplyBox">{{projectApplyState | applyStateFilter(applyStates)}}</el-button>
          <game-entry v-if="projectType === 1 && isLoginUserBeCreator" :projectId='projectId' :originProjectDetail='originProjectDetail' class="project-basic-info-detail-operations-item"></game-entry>
        </div>
      </div>
    </div>
    <div class="project-basic-info-description" v-loading='isLoading'>
      <div class="project-basic-info-description-title">
        {{$t("project.projectDescription")}}:
        <el-button v-if="isLoginUserEditable" class="project-website-card-button" type="text" @click="toggleIsDescEditing">
          <i class="el-icon-edit-outline" v-show="!isDescriptionEditing"></i>
          <span v-show="isDescriptionEditing"><i class="iconfont icon-save3"></i>{{$t("common.Save")}}</span>
        </el-button>
      </div>
      <div class="project-basic-info-description-content" v-show="!isDescriptionEditing" v-html="tempDesc || $t('project.noDescripton')"></div>
      <div :id="descriptionId" v-show="isDescriptionEditing" class="project-basic-info-description-editor"></div>
    </div>
    <sky-drive-manager-dialog :isApplicable='true' :isNoMediaFileShow="false" :show='isMediaSkyDriveDialogShow' @close='closeSkyDriveManagerDialog'></sky-drive-manager-dialog>
    <el-dialog title="" v-loading='isBinderDialogLoading' :visible.sync="binderDialogVisible" :before-close="handleBinderDialogClose">
      <website-binder @confirmSiteId='handleConfirmSiteId'></website-binder>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleBinderDialogClose">{{$t("common.Cancel")}}</el-button>
      </span>
    </el-dialog>
    <el-dialog class="project-basic-info-apply-dialog" :title='$t("project.applyForProject")' :visible.sync="isApplyDialogVisible" width="400px" :before-close="handleApplyDialogClose">
      <el-input type="textarea" :placeholder="$t('project.enterApplicationReason')" resize='none' v-model="applyText">
      </el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleApplyDialogClose">{{$t("common.Cancel")}}</el-button>
        <el-button type="primary" @click="applyJoinProject">{{$t("common.Sure")}}</el-button>
      </span>
    </el-dialog>
    <paracraft-info :isDialogVisible='isParacraftInfoDialogVisible' :paracraftUrl='paracraftUrl' @close='handleParacraftInfoDialogClose'></paracraft-info>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import E from 'wangeditor'
import moment from 'moment'
import { locale } from '@/lib/utils/i18n'
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import paracraftUtil from '@/lib/utils/paracraft'
import SkyDriveManagerDialog from '@/components/common/SkyDriveManagerDialog'
import ParacraftInfo from '@/components/common/ParacraftInfo'
import WebsiteBinder from './WebsiteBinder'
import ProjectGrade from './ProjectGrade'
import GameEntry from './GameEntry'
import launchUri from '@/lib/utils/launchUri'

export default {
  name: 'ProjectBasicInfo',
  props: {
    originProjectDetail: {
      type: Object,
      required: true
    },
    projectOwnerUsername: {
      type: String,
      required: true
    },
    isLoginUserEditable: {
      type: Boolean,
      default: false
    },
    projectId: {
      type: Number,
      required: true
    },
    projectApplyState: Number,
    isProjectStopRecruit: Boolean,
    descriptionId: {
      type: String,
      default: 'projectDescriptoinEditor'
    }
  },
  async mounted() {
    this.copiedProjectDetail = _.cloneDeep(this.originProjectDetail)
    this.tempDesc = this.copiedProjectDetail.description
    this.tempSiteId = this.copiedProjectDetail.siteId
    this.tempCoverUrl = _.get(
      this.copiedProjectDetail,
      'extra.imageUrl',
      undefined
    )
    this.tempVideoUrl = _.get(
      this.copiedProjectDetail,
      'extra.videoUrl',
      undefined
    )
    this.isLogined &&
      Promise.all([
        this.userGetUserPrivilege({
          siteId: this.projectSiteId,
          userId: this.loginUserId
        }),
        this.getWebsiteDetailBySiteId({
          siteId: this.projectSiteId
        })
      ])
  },
  data() {
    return {
      projectTypes: [this.$t('explore.websites'), this.$t('common.paracraft')],
      applyStates: [
        this.$t('project.applyJoin'),
        this.$t('project.requested'),
        this.$t('project.joined')
      ],
      binderDialogVisible: false,
      isApplyButtonLoading: false,
      isBinderDialogLoading: false,
      isDescriptionEditing: false,
      descriptionEditor: undefined,
      copiedProjectDetail: {},
      tempSiteId: null,
      tempDesc: '',
      tempCoverUrl: '',
      tempVideoUrl: '',
      isLoading: false,
      isCoverZoneLoading: false,
      isMediaSkyDriveDialogShow: false,
      defaultCoverUrl: require('@/assets/img/pbl_default_cover.png'),
      waitUpdateCover: false,
      applyText: '',
      isApplyDialogVisible: false,
      maxDescWithHtmlLen: 65535,
      isParacraftInfoDialogVisible: false
    }
  },
  computed: {
    ...mapGetters({
      loginUserId: 'user/userId',
      loginUserDetail: 'user/profile',
      loginUsername: 'user/username',
      userToken: 'user/token',
      getSiteDetailInfoById: 'user/getSiteDetailInfoById',
      isLogined: 'user/isLogined',
      getUserSitePrivilege: 'user/getUserSitePrivilege'
    }),
    isLoginUserBeCreator() {
      return this.isLogined && this.loginUsername === this.projectOwnerUsername
    },
    isEn() {
      return locale === 'en-US' ? true : false
    },
    formatType() {
      return this.isEn ? 'YYYY-MM-DD' : 'YYYY年MM月DD日'
    },
    buttonName() {
      if (this.isWebType) {
        return this.$t('project.visit')
      }
      if (this.isCreating && !this.isProjectOwner) {
        return this.$t('project.creating')
      }
      return this.$t('project.visitWorld')
    },
    visitButtonVisiable() {
      if (!this.isWebType) {
        return true
      }
      return this.siteDetailInfo ? true : false
    },
    isCreating() {
      return !(
        this.originProjectDetail.world &&
        this.originProjectDetail.world.archiveUrl
      )
    },
    loginUserSitePrivilege() {
      return this.getUserSitePrivilege({
        siteId: this.projectSiteId,
        userId: this.loginUserId
      })
    },
    isLoginUserEditableForProjectSite() {
      return this.loginUserSitePrivilege === 64
    },
    isProjectOwner() {
      return this.loginUserId === this.originProjectDetail.userId
    },
    isApplied() {
      return this.projectApplyState === 0
    },
    isLoginUserBeProjectMember() {
      return this.projectApplyState === 1
    },
    originDesc() {
      return this.copiedProjectDetail.description
    },
    originExtra() {
      return this.originProjectDetail.extra
    },
    mergedExtra() {
      let originExtra = _.cloneDeep(this.originExtra)
      return _.merge(originExtra, {
        imageUrl: this.tempCoverUrl,
        videoUrl: this.tempVideoUrl
      })
    },
    updatingProjectData() {
      return _.merge(this.originProjectDetail, {
        siteId: this.tempSiteId,
        description: this.tempDesc,
        extra: this.mergedExtra
      })
    },
    projectType() {
      return this.originProjectDetail.type
    },
    isWebType() {
      return this.projectType === 0
    },
    projectSiteId() {
      // FIXME: 确认清楚是哪个id
      // return this.originProjectDetail.siteId || this.originProjectDetail.id
      return this.originProjectDetail.siteId
    },
    siteDetailInfo() {
      if (!this.isWebType) {
        return
      }
      return this.getSiteDetailInfoById({ siteId: this.projectSiteId })
    },
    toggleSetWebsiteWord() {
      return this.siteDetailInfo
        ? this.$t('project.edit')
        : this.$t('editor.associationWebsite')
    },
    siteUrl() {
      if (!this.isWebType) {
        return
      }
      let { sitename, username } = this.siteDetailInfo
      return `/${username}/${sitename}/index`
    },
    paracraftUrl() {
      if (this.isWebType) {
        return
      }
      if (this.isCreating) {
        return paracraftUtil.getOpenUrl({
          usertoken: this.userToken
        })
      }
      let { archiveUrl } = this.originProjectDetail.world
      return paracraftUtil.getUrl({
        link: `${archiveUrl}`,
        kpProjectId: this.projectId,
        usertoken: this.userToken
      })
    },
    isVideoShow() {
      return this.tempVideoUrl
    }
  },
  methods: {
    ...mapActions({
      pblApplyJoinProject: 'pbl/applyJoinProject',
      pblUpdateProject: 'pbl/updateProject',
      toggleLoginDialog: 'pbl/toggleLoginDialog',
      getWebsiteDetailBySiteId: 'user/getWebsiteDetailBySiteId',
      toggleLoginDialog: 'pbl/toggleLoginDialog',
      userGetUserPrivilege: 'user/getUserPrivilege',
      pblGetProjectDetail: 'pbl/getProjectDetail'
    }),
    async toggleIsDescEditing() {
      if (!this.isDescriptionEditing) {
        this.isDescriptionEditing = true
        this.$nextTick(() => {
          if (!this.descriptionEditor) {
            this.descriptionEditor = new E(`#${this.descriptionId}`)
            this.descriptionEditor.customConfig.menus = [
              'head', // 标题
              'bold', // 粗体
              'fontSize', // 字号
              'fontName', // 字体
              'italic', // 斜体
              'underline', // 下划线
              'strikeThrough', // 删除线
              'foreColor', // 文字颜色
              'backColor', // 背景颜色
              'link', // 插入链接
              'list', // 列表
              'justify', // 对齐方式
              'quote', // 引用
              'emoticon', // 表情
              'undo', // 撤销
              'redo' // 重复
            ]
            this.descriptionEditor.create()
          }
          this.descriptionEditor.txt.html(this.tempDesc)
        })
      } else {
        let editorText = this.descriptionEditor.txt
        this.tempDesc = editorText.text() && this.descriptionEditor.txt.html()
        let descLen = this.tempDesc.length
        if (descLen >= this.maxDescWithHtmlLen) {
          this.$message({
            type: 'error',
            message: '项目描述太长了，请调整'
          })
          return
        }
        let sensitiveResult = await checkSensitiveWords({
          checkedWords: editorText.text()
        }).catch()
        if (sensitiveResult && sensitiveResult.length > 0) {
          this.descriptionEditor.txt.html(sensitiveResult[0].word)
          return
        }
        this.isLoading = true
        await this.updateDescToBackend()
      }
    },
    async updateDescToBackend() {
      await this.pblUpdateProject({
        projectId: this.projectId,
        updatingProjectData: this.updatingProjectData
      })
        .then(() => {
          this.$message({
            type: 'success',
            message: this.$t('project.projectInfoUpdated')
          })
          this.isLoading = false
          this.isDescriptionEditing = false
          return Promise.resolve()
        })
        .catch(error => {
          this.$message({
            type: 'error',
            message: '项目信息更新失败,请重试'
          })
          this.isLoading = false
          return Promise.reject()
        })
    },
    handleApplyDialogClose() {
      this.isApplyDialogVisible = false
    },
    showApplyBox() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      this.isApplyDialogVisible = true
    },
    async applyJoinProject() {
      this.isApplyButtonLoading = true
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: this.applyText
      }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.applyText = _.get(sensitiveResult, '[0].word', this.applyText)
        this.isApplyButtonLoading = false
        return
      }
      await this.pblApplyJoinProject({
        objectType: 5,
        objectId: this.projectId,
        applyType: 0,
        applyId: this.loginUserId,
        legend: this.applyText,
        extra: this.loginUserDetail
      })
        .then(() => {
          this.isApplyButtonLoading = false
          this.$message({
            type: 'success',
            message: '申请成功，等待项目创建者处理'
          })
          this.handleApplyDialogClose()
        })
        .catch(error => {
          let httpCode = _.get(error, 'response.status')
          switch (httpCode) {
            case 401:
              this.toggleLoginDialog(true)
              break
            default:
              break
          }
          this.isApplyButtonLoading = false
          this.handleApplyDialogClose()
          console.error(error)
        })
    },
    toProjectPage() {
      switch (this.projectType) {
        case 0:
          this.toSitePage()
          break
        case 1:
          this.toParacraftPage()
          break
        default:
          break
      }
    },
    async toEditWebsite() {
      if (this.projectSiteId) {
        await this.getWebsiteDetailBySiteId({
          siteId: this.projectSiteId
        }).catch(e => console.error(e))
        if (this.siteDetailInfo) {
          let tempWin = window.open('_blank')
          if (this.siteUrl) {
            return (tempWin.location = `/ed${this.siteUrl}`)
          }
          tempWin.close()
        } else {
          this.binderDialogVisible = true
        }
      } else {
        this.binderDialogVisible = true
      }
    },
    async toSitePage() {
      let tempWin = window.open('_blank')
      if (this.projectSiteId) {
        await this.getWebsiteDetailBySiteId({ siteId: this.projectSiteId })
        if (this.siteUrl) {
          return (tempWin.location = this.siteUrl)
        }
        tempWin.close()
      } else {
        this.binderDialogVisible = true
      }
    },
    async toParacraftPage() {
      if (this.isCreating && !this.isProjectOwner) {
        return
      }
      if (this.paracraftUrl) {
        launchUri(this.paracraftUrl)
        this.isParacraftInfoDialogVisible = true
      }
    },
    showMediaSkyDriveDialog() {
      this.isMediaSkyDriveDialogShow = true
    },
    async closeSkyDriveManagerDialog({ file, url }) {
      this.isMediaSkyDriveDialogShow = false
      if (url) {
        let fileType = file && file.type
        if (fileType === 'videos') {
          this.tempCoverUrl = undefined
          this.tempVideoUrl = url
          this.isCoverZoneLoading = true
          await this.updateDescToBackend()
          this.isCoverZoneLoading = false
        } else {
          this.isCoverZoneLoading = true
          this.tempVideoUrl = undefined
          this.tempCoverUrl = url
          this.waitUpdateCover = true
        }
      }
    },
    async coverImageLoaded() {
      this.waitUpdateCover &&
        (await this.updateDescToBackend()) &&
        (this.waitUpdateCover = false)
      this.isCoverZoneLoading = false
    },
    async handleConfirmSiteId({ siteId }) {
      if (siteId) {
        this.tempSiteId = siteId
        this.isBinderDialogLoading = true
        await this.updateDescToBackend()
        this.isBinderDialogLoading = false
        this.handleBinderDialogClose()
      }
    },
    handleBinderDialogClose() {
      this.binderDialogVisible = false
    },
    handleParacraftInfoDialogClose() {
      this.isParacraftInfoDialogVisible = false
    }
  },
  filters: {
    projectTypeFilter(typeValue, projectTypes) {
      return projectTypes[typeValue]
    },
    formatDate(date, formatType) {
      return moment(date).format(formatType)
    },
    applyStateFilter(applyState, applyStates) {
      let stateText = ''
      switch (applyState) {
        case -1:
          stateText = applyStates[0]
          break
        case 0:
          stateText = applyStates[1]
          break
        case 1:
          stateText = applyStates[2]
          break
        case 2:
          stateText = applyStates[0]
          break
        default:
          stateText = applyStates[0]
          break
      }
      return stateText
    }
  },
  components: {
    SkyDriveManagerDialog,
    ParacraftInfo,
    ProjectGrade,
    GameEntry,
    WebsiteBinder
  }
}
</script>
<style lang="scss">
.project-basic-info {
  background-color: #fff;
  &-header {
    padding: 10px 16px;
    border-bottom: 1px solid #e8e8e8;
  }
  &-name {
    font-size: 20px;
    color: #303133;
    font-weight: bold;
    margin: 0;
  }
  &-picked {
    vertical-align: middle;
    margin: 0 4px;
  }
  &-state {
    background-color: #ef5936;
    font-size: 12px;
    position: relative;
    height: 20px;
    line-height: 20px;
    padding: 0 8px 0 20px;
    border-radius: 20px;
    display: inline-block;
    color: #fff;
  }
  &-state::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background-color: #fff;
    position: absolute;
    left: 8px;
    top: 8px;
  }
  &-more {
    font-size: 12px;
    color: #909399;
    margin: 9px 0 0;
    &-created {
      padding-right: 16px;
      margin-right: 16px;
      position: relative;
    }
    &-created::after {
      content: '';
      display: inline-block;
      width: 1px;
      height: 10px;
      background-color: #eee;
      position: absolute;
      bottom: 2px;
      right: 0;
    }
    &-starcount {
      margin: 0 10px;
    }
    .iconfont {
      color: #cdcdcd;
      margin-right: 3px;
    }
  }

  &-detail {
    display: flex;
    padding: 16px;
    border-bottom: 1px solid #e8e8e8;
    &-cover {
      width: 480px;
      height: 270px;
      background-color: #303133;
      color: #fff;
      text-align: center;
      // line-height: 270px;
      border-radius: 4px;
      margin-right: 16px;
      position: relative;
      border-radius: 4px;
      overflow: hidden;
      &-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      &-video {
        width: 100%;
        height: 100%;
      }
      &-cursor {
        position: absolute;
        margin: 0;
        cursor: pointer;
        display: none;
        z-index: 3000;
        height: 36px;
        line-height: 36px;
        right: 24px;
        top: 18px;
        font-size: 14px;
        background-color: #212121;
        color: #fff;
        border-radius: 36px;
        padding: 0 18px;
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.16);
        .el-icon-edit-outline {
          margin-right: 6px;
        }
      }
      .el-loading-spinner {
        line-height: 1;
      }
    }
    &-cover:hover {
      .show-on-hover {
        display: inline-block;
      }
    }
    &-message {
      position: relative;
      padding-bottom: 36px;
      flex: 1;
      &-item {
        font-size: 14px;
        color: #404144;
        margin: 6px 0 0;
        &:first-child {
          margin-top: 0;
        }
        label {
          color: #909399;
          width: 87px;
          display: inline-block;
        }
      }
    }
    &-operations {
      position: absolute;
      left: 0;
      bottom: 0;
      right: 0;
      &-item {
        display: inline-block;
        margin-left: 10px;
      }
    }
  }

  &-description {
    padding: 16px;
    &-title {
      margin: 8px 0 16px;
      font-size: 16px;
      font-weight: bold;
      position: relative;
      .el-button {
        position: absolute;
        top: -8px;
        right: 0;
      }
    }
    &-content {
      p {
        word-break: break-all;
      }
    }
    .w-e-toolbar {
      border-color: #e8e8e8 !important;
      border-bottom: none !important;
    }
    .w-e-text-container {
      height: 250px !important;
      border-color: #e8e8e8 !important;
    }
    .w-e-text {
      padding: 0 8px;
    }
    &-editor {
      position: relative;
      z-index: 1;
    }
  }
  &-apply-dialog {
    .el-dialog__header {
      font-size: 16px;
      color: #303133;
      border-bottom: 1px solid #e8e8e8;
      padding: 0 24px;
      height: 60px;
      line-height: 60px;
      font-weight: bold;
    }
    .el-dialog__body {
      padding: 24px;
    }
    .el-textarea__inner {
      resize: none;
      min-height: 33px;
      height: 160px;
      font-size: 14px;
      color: #303133;
    }
    .el-dialog__footer {
      padding: 0 24px 24px;
    }
  }
}

@media (max-width: 768px) {
  .project-basic-info {
    &-detail {
      display: flex;
      flex-direction: column;
      &-cover {
        width: auto;
        height: auto;
        margin-right: 0;
        padding-bottom: 56.25%;
        position: relative;
        &-image {
          position: absolute;
          top: 0;
          left: 0;
          object-fit: cover;
          width: 100%;
          height: 100%;
        }
        &-video {
          position: absolute;
          top: 0;
          left: 0;
        }
      }
      &-operations {
        bottom: -10px;
        display: flex;
        .el-button {
          flex: 1;
          height: 36px;
          font-size: 14px;
          padding: 0;
          line-height: 36px;
        }
      }
    }
    &-description-editor {
      .w-e-toolbar {
        flex-wrap: wrap;
      }
    }
    &-apply-dialog {
      .el-dialog {
        width: 94% !important;
      }
    }
  }
  .el-message {
    min-width: 90%;
  }
}
</style>

<template>
  <div class="project-boards">
    <el-card class="project-boards-card" shadow="never" v-loading='isLoading'>
      <div slot="header" class="clearfix">
        <span class="project-boards-card-label">{{$t("project.projectWhiteboard")}}</span>
        <router-link :to="{ name: 'ProjectWhiteBoard', path:moreBoardLink }" class="project-boards-card-link">{{$t("project.readMore")}}<i class="el-icon-arrow-right"></i></router-link>
      </div>
      <div class="project-boards-list" v-if="projectIssueList.length >0">
        <div class="project-boards-item" v-for="(issue, index) in projectIssueList" :key="index" @click="showIssueDetail(issue)">
          <div class="project-boards-item-icon">
            <i class="el-icon-warning" v-show="issue.state === 0"></i>
            <i class="el-icon-success" v-show="issue.state === 1"></i>
          </div>
          <span class="project-boards-item-title" :title="issue.title">{{issue.title}}</span>
          <span class="project-boards-item-time">{{isEn ? $t('common.update') : ''}} {{issue.updatedAt | relativeTimeFilter(isEn)}}{{isEn ? '' : $t('common.update')}}</span>
        </div>
      </div>
      <div class="project-boards-empty" v-else>{{$t("project.noContent")}}</div>
    </el-card>
    <issue-detail v-if="isIssueDetailDialogShow" :show='isIssueDetailDialogShow' :projectDetail='projectDetail' :issue='issueDetail' :isProhibitEdit="isProhibitEdit" @close="handleIssueDialogClose"></issue-detail>
  </div>
</template>
<script>
import IssueDetail from '@/components/pbl/IssueDetail'
import moment from 'moment'
import 'moment/locale/zh-cn'
import { locale } from '@/lib/utils/i18n'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'ProjectBoards',
  props: {
    projectId: {
      required: true
    },
    projectDetail: {
      type: Object,
      required: true
    },
    isProhibitView: {
      type: Boolean,
      default: false
    },
    isProhibitEdit: {
      type: Boolean,
      default: false
    }
  },
  async mounted() {
    await this.getProjectIssues({
      objectId: this.projectId,
      objectType: 5,
      'x-per-page': 10,
      'x-page': 1,
      'x-order': 'createdAt-desc'
    })
    this.projectIssues = this.projectIssueList
  },
  data() {
    return {
      isLoading: false,
      projectIssues: [],
      isEn: locale === 'en-US',
      isIssueDetailDialogShow: false,
      issueDetail: {}
    }
  },
  computed: {
    ...mapGetters({
      pblIssuesList: 'pbl/issuesList'
    }),
    projectIssueList() {
      return _.get(
        this.pblIssuesList({ projectId: this.projectId }),
        'rows',
        []
      ).slice(0, 10)
    },
    moreBoardLink() {
      return `${this.projectId}/whiteboard`
    }
  },
  methods: {
    ...mapActions({
      getProjectIssues: 'pbl/getProjectIssues'
    }),
    showIssueDetail(issue) {
      this.issueDetail = issue
      this.isIssueDetailDialogShow = true
    },
    handleIssueDialogClose() {
      this.isIssueDetailDialogShow = false
      this.issueDetail = {}
    }
  },
  filters: {
    relativeTimeFilter(date, isEn) {
      const offset = moment().utcOffset()
      isEn ? moment.locale('en') : moment.locale('zh-cn')
      return moment(date)
        .utcOffset(offset)
        .fromNow()
    }
  },
  components: {
    IssueDetail
  }
}
</script>
<style lang="scss">
.project-boards {
  &-card {
    &-label {
      font-weight: bold;
    }
    &-link {
      font-size: 12px;
      text-decoration: none;
      float: right;
      color: #909399;
    }
  }
  &-item {
    display: flex;
    padding: 8px 0;
    cursor: pointer;
    &-icon {
      margin-right: 8px;
      line-height: 1;
    }
    &-title {
      flex: 1;
      margin-right: 18px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-size: 14px;
      color: #303133;
      line-height: 1;
    }
    &-time {
      font-size: 12px;
      color: #909399;
      align-items: center;
    }
    .el-icon-warning {
      color: #f3b623;
    }
    .el-icon-success {
      color: #63e08f;
    }
  }
  &-empty {
    font-size: 14px;
  }
}
</style>
<template>
  <div class="project-comments">
    <div class="project-comments-header">
      {{$t('project.comment')}}<span class="project-comments-header-count">({{$t('project.having')}}{{totalCommentCount}}{{$t('project.commentCount')}})</span>
    </div>
    <div class="project-comments-sends">
      <div class="project-comments-sends-profile-input">
        <img class="hidden-xs-only project-comments-profile" :src='userPortrait || defaultPortrait' alt="">
        <el-input :disabled='!isLoginUsercommentable' :placeholder="$t('project.writeComment')" v-model='newCommenContent' maxlength="1000"></el-input>
      </div>
      <div class="project-comments-sends-operations">
        <el-button type="primary" :loading='isAddingComment' size="medium" @click="sendComment" :disabled="!newCommenContent">{{$t('project.comment')}}</el-button>
      </div>
      <div class="project-comments-sends-login" v-if="!isLogined" @click="toLogin">{{$t("project.commentAfterLogin")}}</div>
    </div>
    <div class="project-comments-list" v-loading='isLoading'>
      <div class="project-comments-item" v-for="(comment, index) in commentList" :key='index'>
        <img class="project-comments-profile project-comments-item-profile" :src="comment.extra.portrait || defaultPortrait" alt="">
        <div class="project-comments-item-detail">
          <p class="project-comments-item-username-time">{{comment.extra.nickname || comment.extra.username}}
            <span class="project-comments-item-time">{{comment.createdAt | relativeTimeFilter(isEn)}}</span>
          </p>
          <p class="project-comments-item-comment">{{comment.content}}</p>
          <el-button v-if="comment.userId === loginUserId" type="text" class="project-comments-item-delete" @click="deleteComment(comment)"><i class="iconfont icon-delete1"></i> {{$t('project.delete')}}</el-button>
        </div>
      </div>
    </div>
    <div class="project-comments-more" v-loading='isGetCommentBtnLoading' @click="getMoreComment">{{isGetAllComment?$t('project.noMoreComment'):$t('project.viewMoreComments')}}</div>
  </div>
</template>
<script>
import moment from 'moment'
import 'moment/locale/zh-cn'
import { locale } from '@/lib/utils/i18n'
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import { mapGetters, mapActions } from 'vuex'
import _ from 'lodash'
export default {
  name: 'ProjectComments',
  props: {
    projectId: {
      required: true
    },
    isLoginUsercommentable: Boolean
  },
  async created() {
    this.getCommentFromBackEnd()
  },
  data() {
    return {
      xPerPage: 6,
      xPage: 1,
      xOrder: 'updatedAt-desc',
      isAddingComment: false,
      isLoading: false,
      newCommenContent: '',
      defaultPortrait: require('@/assets/img/default_portrait.png'),
      commentList: [],
      isGetAllComment: false,
      isGetCommentBtnLoading: false,
      totalCommentCount: 0,
      isEn: locale === 'en-US'
    }
  },
  computed: {
    ...mapGetters({
      pblProjectCommentList: 'pbl/projectCommentList',
      userProfile: 'user/profile',
      loginUserId: 'user/userId',
      isLogined: 'user/isLogined'
    }),
    projectCommentList() {
      return this.pblProjectCommentList({ projectId: this.projectId }) || []
    },
    userPortrait() {
      return _.get(this.userProfile, 'portrait')
    }
  },
  methods: {
    ...mapActions({
      pblGetComments: 'pbl/getComments',
      pblCreateComment: 'pbl/createComment',
      pblDeleteComment: 'pbl/deleteComment',
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    async getCommentFromBackEnd() {
      this.isGetCommentBtnLoading = true
      let newCommentResult = await this.pblGetComments({
        objectType: 5,
        objectId: this.projectId,
        xPage: this.xPage,
        xOrder: this.xOrder,
        xPerPage: this.xPerPage
      }).catch()
      this.totalCommentCount = newCommentResult.count
      let newCommentList = newCommentResult.rows
      if (newCommentList.length > 0) {
        this.isGetAllComment = false
        this.commentList = _.concat(this.commentList, newCommentList)
      } else {
        this.isGetAllComment = true
        this.xPage--
      }
      this.isGetCommentBtnLoading = false
    },
    getMoreComment() {
      if (this.isGetAllComment) {
        return
      }
      this.xPage++
      this.getCommentFromBackEnd()
    },
    toLogin() {
      this.toggleLoginDialog(true)
    },
    async sendComment() {
      if (!this.isLogined) {
        return this.toLogin()
      }
      this.isAddingComment = true
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: this.newCommenContent
      }).catch()
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.newCommenContent = _.get(
          sensitiveResult,
          '[0].word',
          this.newCommenContent
        )
        this.isAddingComment = false
        return
      }
      await this.pblCreateComment({
        objectType: 5,
        objectId: _.toString(this.projectId),
        content: this.newCommenContent
      })
        .then(newCommentDetail => {
          this.$message({
            type: 'success',
            message: this.$t('project.commentSuccessfully')
          })
          this.isAddingComment = false
          this.newCommenContent = ''
          this.resetCommentList()
        })
        .catch(error => {
          this.$message({
            type: 'error',
            message: '评论失败'
          })
          this.isAddingComment = false
          return
        })
    },
    resetCommentList() {
      this.xPage = 1
      this.commentList = []
      this.getCommentFromBackEnd()
    },
    async deleteComment(commentDetail) {
      this.isLoading = true
      await this.pblDeleteComment({
        objectType: 5,
        objectId: this.projectId,
        commentId: commentDetail.id
      })
        .then(() => {
          this.isLoading = false
          this.$message({
            type: 'success',
            message: this.$t('project.commentDeleted')
          })
          this.resetCommentList()
        })
        .catch(error => {
          this.isLoading = false
          this.$message({
            type: 'error',
            message: '评论删除失败'
          })
          console.error(error)
        })
    }
  },
  filters: {
    relativeTimeFilter(date, isEn) {
      isEn ? moment.locale('en') : moment.locale('zh-cn')
      return moment(date).fromNow()
    }
  }
}
</script>
<style lang="scss">
.project-comments {
  background-color: #fff;
  &-profile {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
  }
  &-header {
    font-size: 16px;
    color: #303133;
    font-weight: bold;
    height: 56px;
    line-height: 56px;
    padding: 0 16px;
    &-count {
      font-size: 12px;
      font-weight: normal;
      color: #909399;
      margin-left: 8px;
    }
  }
  &-sends {
    padding: 24px 16px 24px 24px;
    border: 1px solid #e8e8e8;
    border-width: 1px 0;
    position: relative;
    &-profile-input {
      padding-left: 64px;
      position: relative;
      img {
        position: absolute;
        left: 0;
      }
    }
    &-operations {
      text-align: right;
      padding-top: 16px;
    }
    &-login {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #fff;
      background-color: rgba(0, 0, 0, 0.6);
      &:hover {
        color: #409efe;
      }
    }
  }
  &-item {
    p {
      margin: 0;
    }
    display: flex;
    align-items: flex-start;
    padding: 24px;
    &-profile {
      margin-right: 16px;
    }
    &-username-time {
      font-size: 14px;
      color: #303133;
      margin-bottom: 10px !important;
    }
    &-time {
      font-size: 12px;
      color: #909399;
      margin-left: 10px;
    }
    &-comment {
      font-size: 13px;
      color: #606266;
      padding-right: 96px;
      line-height: 1.5;
      word-break: break-word;
      word-wrap: break-word;
    }
    &-detail {
      flex: 1;
      min-width: 0;
      position: relative;
    }
    &-delete {
      position: absolute;
      right: 14px;
      top: 50%;
      padding: 0;
      font-size: 13px;
      color: #909399;
      .iconfont {
        font-size: 14px;
      }
    }
  }
  &-more {
    height: 36px;
    line-height: 36px;
    font-size: 12px;
    color: #909399;
    text-align: center;
    border-top: 1px solid #e8e8e8;
    cursor: pointer;
  }
}

@media (max-width: 768px) {
  .project-comments {
    &-sends {
      &-profile-input {
        padding-left: 0;
      }
    }
    &-item {
      padding: 12px;
      &-profile {
        height: 40px;
        width: 40px;
        margin-right: 12px;
      }
      &-comment {
        font-size: 13px;
        color: #606266;
      }
    }
  }
}
</style>
<template>
  <div class="project-editing" v-loading='isLoading'>
    <div class='project-editing-item'>
      <label class="project-editing-item-label">{{$t('project.projectStatus')}}</label>
      <el-radio-group v-model="projectVisibility" @change="handleSwitchProjectVisibility">
        <el-radio :label="0">{{$t('project.publicProject')}}</el-radio>
        <el-radio :label="1">{{$t('project.privateProject')}}</el-radio>
      </el-radio-group>
    </div>
    <div class='project-editing-item' v-for="(privilege, index) in privilegeOptions" :key='index'>
      <label class="project-editing-item-label">{{privilege.label}}</label>
      <el-radio-group v-model="projectPrivileges[privilege.dataKey]" :disabled="privilege.dataKey === 'boardEdit' && isMemberView || privilege.dataKey === 'boardView' && isPrivilegeProject" @change="handleChange">
        <el-radio v-for="(option, index) in privilege.options" :key='index' :label="option.value" :disabled="option.value === 4 && isPrivilegeProject" >{{option.label}}</el-radio>
      </el-radio-group>
    </div>
    <div class="project-editing-operate">
      <el-button type="primary" size="medium" :disabled="!isModified" @click='updatePrivilege'>{{$t("common.Save")}}</el-button>
    </div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
export default {
  name: 'ProjectEditing',
  props: {
    originalProjectDetail: {
      type: Object,
      required: true,
      validator: function (value) {
        let { visibility, privilege } = value
        return [0, 1].indexOf(visibility) !== -1 && _.isNumber(privilege)
      }
    }
  },
  mounted() {
    this.projectVisibility = this.originVisibility
    this.initPrivileges()
  },
  data() {
    return {
      isLoading: false,
      privilegeOptions: {
        comment: {
          label: this.$t('project.commentBy'),
          dataKey: 'comment',
          options: [
            { value: 4, label: this.$t('project.anyone') },
            { value: 8, label: this.$t('project.membersOnly') },
            { value: 16, label: this.$t('project.commentsOff') }
          ]
        },
        boardView: {
          label: this.$t('project.boardViewBy'),
          dataKey: 'boardView',
          options: [{ value: 32, label: this.$t('project.anyone') }, { value: 64, label: this.$t('project.membersOnly') }]
        },
        boardEdit: {
          label: this.$t('project.boardEditBy'),
          dataKey: 'boardEdit',
          options: [
            { value: 128, label: this.$t('project.anyone') },
            { value: 256, label: this.$t('project.membersOnly') }
          ]
        },
        recruit: {
          label: this.$t('project.recruitingStatus'),
          dataKey: 'recruit',
          options: [{ value: 1, label: this.$t('project.onRecruiting') }, { value: 2, label: this.$t('project.offRecruiting') }]
        }
      },
      projectVisibility: 0,
      projectPrivileges: {
        recruit: undefined,
        comment: undefined,
        boardView: undefined,
        boardEdit: undefined
      }
    }
  },
  computed: {
    editingProjectId() {
      return _.get(this.originalProjectDetail, 'id')
    },
    originPrivilege() {
      return _.get(this.originalProjectDetail, 'privilege')
    },
    originVisibility() {
      return _.get(this.originalProjectDetail, 'visibility')
    },
    newPrivilege() {
      let privilegeNumber = _.reduce(
        this.projectPrivileges,
        (sum, value) => {
          return sum + value
        },
        0
      )
      return privilegeNumber
    },
    isModified() {
      let isVisibilityModified = !_.isEqual(
        this.projectVisibility,
        this.originVisibility
      )
      let isPrivilegeModified = !_.isEqual(
        this.newPrivilege,
        this.originPrivilege
      )
      return isVisibilityModified || isPrivilegeModified
    },
    isMemberView() {
      return this.projectPrivileges['boardView'] === 64
    },
    isPrivilegeProject() {
      return this.projectVisibility === 1
    }
  },
  methods: {
    ...mapActions({
      pblUpdateProject: 'pbl/updateProject'
    }),
    handleChange(value) {
      if (value === 64) {
        this.projectPrivileges['boardEdit'] = 256
      }
    },
    initPrivileges() {
      const privilegesNumber = this.originPrivilege
      _.forEach(this.privilegeOptions, (value, key) => {
        let { dataKey, options } = value
        for (let index = 0; index < options.length; index++) {
          const option = options[index]
          let optionValue = option.value
          if ((privilegesNumber & optionValue) > 0) {
            this.projectPrivileges[dataKey] = optionValue
            return
          }
        }
      })
    },
    async updatePrivilege() {
      let { name, type, description } = this.originalProjectDetail
      let updatingProjectData = {
        name,
        type,
        description,
        visibility: this.projectVisibility,
        privilege: this.newPrivilege
      }
      this.isLoading = true
      await this.pblUpdateProject({
        projectId: this.editingProjectId,
        updatingProjectData
      })
        .then(() => {
          this.$message({
            type: 'success',
            message: this.$t('project.successfullyUpdated')
          })
          this.isLoading = false
        })
        .catch(error => {
          console.log(error)
          this.isLoading = false
        })
    },
    handleSwitchProjectVisibility(value) {
      if(value === 1) {
        this.projectPrivileges['comment'] = 8
        this.projectPrivileges['boardView'] = 64
        this.projectPrivileges['boardEdit'] = 256
      }
    }
  }
}
</script>
<style lang="scss">
.project-editing {
  font-size: 14px;
  color: #909399;
  padding: 10px 50px;
  &-item {
    margin-bottom: 20px;
    &-label {
      margin-right: 20px;
    }
  }
  &-operate {
    padding-left: 80px;
    .el-button--medium {
      padding: 10px 28px;
    }
  }
  .el-radio + .el-radio {
    margin-left: 24px;
  }
  .el-radio__label {
    padding-left: 6px;
  }
  .el-radio__inner {
    width: 16px;
    height: 16px;
  }
  .el-radio__inner::after {
    width: 8px;
    height: 8px;
    background-color: #2296f3;
  }
  .el-radio__label,
  .el-radio__input.is-checked + .el-radio__label {
    color: #303133;
  }
  .el-radio__input.is-checked {
    .el-radio__inner {
      background-color: transparent;
    }
  }
}
</style>
<template>
  <div class="project-grade">
    <div class="project-grade-summary">
      <div class="project-grade-score" :title="projectRate | rateInfoFilter(rateDetail.count)">{{projectRate | rateShowFilter(rateDetail.count)}}</div>
      <div class="project-grade-stars">
        <el-rate v-model="startRate" disabled text-color="#ff9900">
        </el-rate>
        <!-- <p class="project-grade-stars-info">已有<span class="project-grade-stars-warning">{{rateDetail.count}}</span>人评分</p> -->
        <p class="project-grade-stars-info">{{$t('project.hasRate', {number: rateDetail.count})}}</p>
      </div>
    </div>
    <div class="project-grade-detail">
      <div class="project-grade-item" v-for="index in [5,4,3,2,1]" :key="index">
        <span>{{index}}{{$t('common.star')}}</span>
        <el-progress :percentage="rateDetail[index] | percentFilter(rateDetail.count)"></el-progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectGrade',
  props: {
    projectDetail: {
      type: Object,
      required: true
    }
  },
  mounted() {
    this.startRate = this.projectRate / 20
  },
  data() {
    return {
      startRate: 0
    }
  },
  computed: {
    projectRate: {
      get() {
        return _.get(this.projectDetail, 'rate', 0)
      },
      set(rate) {
        this.startRate = rate / 20
      }
    },
    rateDetail() {
      return _.get(this.projectDetail, 'extra.rate', {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        count: 0
      })
    }
  },
  filters: {
    percentFilter(count, total) {
      count = count || 0
      return total == 0 ? 0 : _.round((count / total) * 100)
    },
    rateShowFilter(rate, markCount) {
      return markCount < 8 ? 'N/A' : _.round(rate, 1)
    },
    rateInfoFilter(rate, markCount) {
      return markCount < 8 ? '尚未收集到足够的评价' : ''
    }
  }
}
</script>
<style lang="scss">
.project-grade {
  &-summary {
    display: flex;
    align-items: center;
    margin: 14px 0 6px;
  }
  &-score {
    font-size: 44px;
    margin-right: 10px;
    line-height: 1;
  }
  &-stars {
    &-info {
      margin: 4px 0 0;
      font-size: 12px;
      color: #bbb;
    }
    &-warning {
      color: #2397f3;
    }
    .el-rate__icon {
      margin-right: 2px;
    }
  }
  &-item {
    display: flex;
    align-items: center;
    font-size: 12px;
    color: #ccc;
    .el-progress {
      width: 150px;
      margin-left: 12px;
    }
    .el-progress__text {
      font-size: 12px !important;
      color: #555;
    }
  }
}
</style>
<template>
  <div class="project-header">
    <div class="container">
      <el-breadcrumb separator="/" class="project-header-breadcrumb hidden-xs-only">
        <el-breadcrumb-item>
          <img class="project-header-breadcrumb-home-icon" src="@/assets/pblImg/home.png" alt="" @click="goHomePage">
        </el-breadcrumb-item>
        <el-breadcrumb-item>
          <a :href="`/u/${editingProjectUsername}`">{{editingProjectUsername}}</a>
        </el-breadcrumb-item>
        <el-breadcrumb-item>
          <el-dropdown @visible-change='dropdownVisibleChange' placement='bottom' trigger="click">
            <span class="el-dropdown-link">
              {{editingProjectName}}<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu class="project-header-dropdown" slot="dropdown" v-loading='isDropdownLoading'>
              <el-dropdown-item @click.native="toProjectIndexPage(project)" :disabled='editingProjectName == project.name' v-for="(project, index) in userProjectList" :key="index">{{project.name}}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-breadcrumb-item>
      </el-breadcrumb>
      <div class="project-header-operations hidden-xs-only">
        <div class="project-header-operations-item">
          <el-popover placement="top" width="160" @show='showSocialShare'>
            <div class="kp-social-share"></div>
            <el-button slot="reference" plain size="medium">
              <i class="iconfont icon-share1"></i>{{$t("project.share")}}
            </el-button>
          </el-popover>
        </div>
        <div class="project-header-operations-item">
          <el-button plain size="medium" @click="toggleFavoriteProject" :loading="isFavoriteButtonLoading">
            <i class="iconfont" :class="favoriteIconClass"></i>{{isUserFavoriteProject ? $t("project.unstar") : $t("project.star")}}
          </el-button>
          <span class="project-header-operations-item-count">{{projectDetail.favoriteCount}}</span>
        </div>
        <div class="project-header-operations-item">
          <el-button plain size="medium" @click='toggleStarProject' :loading="isStarButtonLoading">
            <i class="iconfont" :class="starIconClass"></i>{{isUserStaredProject ? $t("project.unlike") : $t("project.like")}}
          </el-button>
          <span class="project-header-operations-item-count">{{projectDetail.star}}</span>
        </div>
      </div>
      <el-tabs v-model="activePageName" class="project-header-tabs" @tab-click="handleTabClick">
        <el-tab-pane name="ProjectIndexPage">
          <span slot="label" class="project-header-tabs-label">{{$t("project.main")}}</span>
        </el-tab-pane>
        <el-tab-pane name="ProjectWhiteBoard" v-if="!isProhibitView">
          <span slot="label" class="project-header-tabs-label">{{$t("project.whiteboard")}}</span>
        </el-tab-pane>
        <el-tab-pane name="EditProject" v-if="isLoginUserEditable">
          <span slot="label" class="project-header-tabs-label">{{$t("project.setting")}}</span>
        </el-tab-pane>
        <el-tab-pane name="DeleteProject" v-if="isLoginUserEditable">
          <span slot="label" class="project-header-tabs-label">{{$t('project.deleteProject')}}</span>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="project-index-phone-operations-foot hidden-sm-and-up">
      <span class="project-index-phone-operations-foot-item" @click="showTheCommentInput">
        <i class="iconfont icon-information"></i> 评论
      </span>
      <span :class="['project-index-phone-operations-foot-item', {'item-select': isUserStaredProject}]" @click='toggleStarProject'>
        <i :class="['iconfont', isUserStaredProject ? 'icon-like-fill' : 'icon-like1' ]"></i> 点赞
      </span>
      <span :class="['project-index-phone-operations-foot-item', {'item-select': isUserFavoriteProject}]" @click="toggleFavoriteProject">
        <i :class="['iconfont', isUserFavoriteProject ? 'icon-star-fill' : 'icon-star1' ]"></i> 收藏
      </span>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import 'social-share.js/dist/js/social-share.min.js'
import 'social-share.js/dist/css/share.min.css'
import scrollIntoView from 'scroll-into-view-if-needed'
export default {
  name: 'ProjectHeader',
  props: {
    projectDetail: Object,
    editingProjectUsername: String,
    editingUserId: Number,
    isLoginUserEditable: {
      type: Boolean,
      default: false
    },
    isProhibitView: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isDropdownLoading: false,
      isFavoriteButtonLoading: false,
      isStarButtonLoading: false,
      activePageName: this.$route.name
    }
  },
  mounted() {
    window.document.title = `${this.editingProjectName}`
  },
  computed: {
    ...mapGetters({
      userProjects: 'pbl/userProjects',
      projectFavoriteState: 'pbl/projectFavoriteState',
      projectStarState: 'pbl/projectStarState',
      isLogined: 'user/isLogined'
    }),
    editingProjectName() {
      return _.get(this.projectDetail, 'name')
    },
    editingProjectId() {
      return _.get(this.projectDetail, 'id')
    },
    userProjectList() {
      let userId = this.editingUserId
      return _.get(this.userProjects({ userId }), 'rows', [])
    },
    isUserFavoriteProject() {
      return this.projectFavoriteState({
        projectId: this.editingProjectId
      })
    },
    isUserStaredProject() {
      return this.projectStarState({ projectId: this.editingProjectId })
    },
    favoriteIconClass() {
      return this.isUserFavoriteProject ? 'icon-star-fill' : 'icon-star1'
    },
    starIconClass() {
      return this.isUserStaredProject ? 'icon-like-fill' : 'icon-like1'
    },
    shareUrl() {
      let origin = window.location.origin
      return `${origin}/pbl/project/${this.editingProjectId}`
    }
  },
  methods: {
    ...mapActions({
      pblGetUserProjects: 'pbl/getUserProjects',
      favoriteProject: 'pbl/favoriteProject',
      unFavoriteProject: 'pbl/unFavoriteProject',
      starProject: 'pbl/starProject',
      unStarProject: 'pbl/unStarProject',
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    showTheCommentInput() {
      let input = document.querySelector(
        '#project-index-phone-comments .project-comments-sends-profile-input input'
      )
      input.focus()
      scrollIntoView(input)
    },
    goHomePage() {
      window.location.href = `/`
    },
    showMessage({ type = 'success', message = '操作成功' }) {
      this.$message({ type, message })
    },
    async dropdownVisibleChange(visible) {
      if (visible) {
        let userId = this.editingUserId
        this.isDropdownLoading = true
        await this.pblGetUserProjects({ userId })
        this.isDropdownLoading = false
      }
    },
    toProjectIndexPage(project) {
      let projectId = project.id
      this.$router.push({ path: `/project/${projectId}` })
    },
    async toggleStarProject() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      let projectId = this.editingProjectId
      this.isStarButtonLoading = true
      if (!this.isUserStaredProject) {
        await this.starProject({ projectId })
          .then(() => {
            this.showMessage({
              message: this.$t('project.successfullyLiked')
            })
            this.isStarButtonLoading = false
          })
          .catch(error => {
            this.showMessage({
              type: 'error',
              message: '点赞失败'
            })
            this.isStarButtonLoading = false
          })
      } else {
        await this.unStarProject({ projectId })
          .then(() => {
            this.showMessage({
              message: this.$t('project.successfullyUnliked')
            })
            this.isStarButtonLoading = false
          })
          .catch(error => {
            this.showMessage({
              type: 'error',
              message: '取消点赞失败'
            })
            this.isStarButtonLoading = false
          })
        this.isStarButtonLoading = false
      }
    },
    async toggleFavoriteProject() {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      let objectId = this.editingProjectId
      let objectType = 5
      this.isFavoriteButtonLoading = true
      if (!this.isUserFavoriteProject) {
        await this.favoriteProject({ objectId, objectType })
          .then(() => {
            this.showMessage({
              message: this.$t('project.successfullyStarred')
            })
            this.isFavoriteButtonLoading = false
          })
          .catch(error => {
            this.showMessage({
              type: 'error',
              message: '收藏失败'
            })
            this.isFavoriteButtonLoading = false
          })
      } else {
        await this.unFavoriteProject({ objectId, objectType })
          .then(() => {
            this.showMessage({
              message: this.$t('project.successfullyUnstarred')
            })
            this.isFavoriteButtonLoading = false
          })
          .catch(error => {
            this.showMessage({
              type: 'error',
              message: '取消收藏失败'
            })
            this.isFavoriteButtonLoading = false
          })
        this.isFavoriteButtonLoading = false
      }
    },
    showSocialShare() {
      let projectImageUrl = _.get(this.projectDetail, 'extra.imageUrl')
      window.socialShare('.kp-social-share', {
        mode: 'prepend',
        url: this.shareUrl,
        description: `我将${this.editingProjectUsername}的项目${
          this.editingProjectName
        }分享给你`,
        title: `我将${this.editingProjectUsername}的项目${
          this.editingProjectName
        }分享给你`,
        sites: ['qq', 'qzone', 'weibo', 'wechat'],
        wechatQrcodeTitle: '', // 微信二维码提示文字
        wechatQrcodeHelper: this.$t('common.QR'),
        image: this.coverUrl
      })
    },
    handleTabClick(tabItem) {
      let { paneName } = tabItem
      this.$router.push({ name: paneName })
    }
  }
}
</script>

<style lang="scss">
.project-header {
  background-color: #fff;
  box-shadow: 0 1px 3px 0px rgba(0, 0, 0, 0.1);
  &-breadcrumb {
    font-size: 16px;
    padding-top: 24px;
    &-home-icon {
      vertical-align: middle;
    }
    .el-breadcrumb__inner a {
      color: inherit;
      font-weight: normal;
    }
    .el-breadcrumb__inner a:hover {
      color: #2296f3;
    }
    .el-breadcrumb__separator {
      font-weight: normal;
      font-size: 12px;
      vertical-align: middle;
    }
    .el-dropdown {
      font-size: 16px;
      font-weight: bold;
      color: #303133;
      cursor: pointer;
    }
  }
  &-dropdown {
    max-height: 200px;
    overflow: auto;
  }
  &-operations {
    text-align: right;
    line-height: 1;
    &-item {
      display: inline-block;
      margin-left: 12px;
      border: 1px solid #dcdfe6;
      border-radius: 4px;
      height: 32px;
      overflow: hidden;
      .el-button {
        background: linear-gradient(#fff, #f6f7f8);
        border: none;
        height: 32px;
        padding: 0 16px;
        .iconfont {
          margin-right: 6px;
          font-size: 20px;
          vertical-align: sub;
        }
      }
      &-count {
        font-size: 14px;
        color: #606266;
        border-left: 1px solid #dcdfe6;
        display: inline-block;
        padding: 0 16px;
        margin-left: -6px;
        height: 32px;
        line-height: 32px;
      }
      &-count + .el-button {
        border-radius: 4px 0 0 4px;
      }
    }
  }
  &-tabs {
    &-label {
      padding: 0 16px;
    }
    .el-tabs__header {
      margin-bottom: 0;
    }
    .el-tabs__nav-wrap::after {
      display: none;
    }
    .el-tabs__item {
      padding: 0 0 17px 0;
      height: auto;
      line-height: 1;
      border-bottom: 3px solid transparent;
    }
    .el-tabs__item.is-active {
      color: #303133;
      font-weight: bold;
      border-bottom: 3px solid #2397f3;
      transition: all ease-in-out 0.2s;
    }
    .el-tabs__active-bar {
      display: none;
    }
  }
}
.kp-social-share.social-share {
  text-align: center;
  .icon-wechat {
    visibility: hidden;
    height: 150px;
    .wechat-qrcode {
      top: 0;
      left: -40px;
      width: 110px;
      background-color: transparent;
      box-shadow: none;
      border: none;
      visibility: visible;
      display: block;
      height: 165px;
    }
    .wechat-qrcode::after {
      content: none;
    }
    h4 {
      display: none;
    }
  }
}

@media (max-width: 768px) {
  .project-header-tabs {
    .el-tabs__nav.is-top {
      width: 100%;
      display: flex;
      height: 40px;
      .el-tabs__item {
        line-height: 40px;
        width: 33.3333%;
        text-align: center;
      }
    }
  }
  .project-index-phone-operations-foot {
    height: 40px;
    position: fixed;
    z-index: 998;
    bottom: 0;
    right: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #ffffff;
    box-shadow: 0 0 21px 8px rgba(165, 163, 139, 0.3);
    &-item {
      flex: 1;
      text-align: center;
      font-size: 16px;
      &:active {
        color: #4db5ff;
      }
      &.item-select {
        color: #2397f3;
      }
      &:not(:first-child) {
        border-left: 1px solid #cfcfcf;
      }
    }
  }
}
</style>
<template>
  <div class="project-website">
    <el-card class="project-website-card" shadow="never">
      <p class="project-website-info">{{$t("project.welcomeTo")}}{{originProjectDetail.name}}</p>
      <div class="project-website-operations" v-show="isLoginUserEditable || originInfoSiteData.displayName">
        <el-button @click="handleFakeButtonClick" size='small' type="primary">{{originInfoSiteData.displayName || $t("project.websiteSettingForResource")}}</el-button>
        <i v-show="isLoginUserEditable && isHaveOriginInfoSiteData" class="el-icon-edit-outline" @click='showEditInfoSiteDataDialog'></i>
      </div>
    </el-card>
    <el-dialog :title="$t('project.websiteSettingForResource')" :visible.sync="isEditInfoSiteDialogShow" width="420px" :before-close="handleClose" v-loading='isLoading'>
      <el-form label-position="top" :model="tempInfoSiteData">
        <el-form-item :label='$t("project.name")'>
          <el-input v-model="tempInfoSiteData.displayName" maxlength='30' @blur='checkDisplayNameLength'></el-input>
        </el-form-item>
        <el-form-item :label='$t("project.url")'>
          <el-input v-model="tempInfoSiteData.url"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">{{$t("common.Cancel")}}</el-button>
        <el-button type="primary" @click="saveInfoSiteData" :disabled="isSaveButtonDisabled">{{$t("common.Sure")}}</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import { mapActions } from 'vuex'
export default {
  name: 'ProjectIntro',
  props: {
    originProjectDetail: {
      type: Object,
      required: true
    },
    projectId: {
      required: true
    },
    isLoginUserEditable: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.copiedProjectDetail = _.cloneDeep(this.originProjectDetail)
    let originInfoSiteData = _.get(this.copiedProjectDetail, 'extra.infoSite', {
      displayName: '',
      url: ''
    })
    this.tempInfoSiteData = originInfoSiteData
  },
  data() {
    return {
      isEditInfoSiteDialogShow: false,
      isLoading: false,
      tempInfoSiteData: {
        displayName: '',
        url: ''
      }
    }
  },
  computed: {
    originInfoSiteData() {
      return _.get(this.originProjectDetail, 'extra.infoSite', {
        displayName: '',
        url: ''
      })
    },
    isHaveOriginInfoSiteData() {
      let { displayName, url } = this.originInfoSiteData
      return displayName && url
    },
    isSaveButtonDisabled() {
      let isModified = this.isModified
      return !isModified || (isModified && this.isHalfFilled)
    },
    isModified() {
      return !_.isEqual(this.originInfoSiteData, this.tempInfoSiteData)
    },
    isHalfFilled() {
      let { displayName, url } = this.tempInfoSiteData
      return (displayName && !url) || (!displayName && url) ? true : false
    },
    originExtra() {
      return this.originProjectDetail.extra
    },
    mergedExtra() {
      let originExtra = _.cloneDeep(this.originExtra)
      return _.merge(originExtra, {
        infoSite: this.tempInfoSiteData
      })
    },
    updatingProjectData() {
      return _.merge(this.copiedProjectDetail, {
        extra: this.mergedExtra
      })
    }
  },
  methods: {
    ...mapActions({
      pblUpdateProject: 'pbl/updateProject'
    }),
    showEditInfoSiteDataDialog() {
      this.isEditInfoSiteDialogShow = true
    },
    async checkSensitive(checkedWords) {
      let result = await checkSensitiveWords({ checkedWords }).catch()
      return result && result.length > 0
    },
    async saveInfoSiteData() {
      if (!this.checkDisplayNameLength()) {
        return
      }
      this.isLoading = true
      let isSensitive = await this.checkSensitive([
        this.tempInfoSiteData.displayName
      ])
      if (isSensitive) {
        this.isLoading = false
        return
      }
      await this.pblUpdateProject({
        projectId: this.projectId,
        updatingProjectData: this.updatingProjectData
      })
        .then(() => {
          this.$message({
            type: 'success',
            message: '资料网站更新成功'
          })
          this.isLoading = false
          this.handleClose()
        })
        .catch(error => {
          this.$message({
            type: 'error',
            message: '资料网站更新失败,请重试'
          })
          this.isLoading = false
          this.handleClose()
          console.error(error)
        })
    },
    handleFakeButtonClick() {
      if (this.isHaveOriginInfoSiteData) {
        let tempWin = window.open('_blank')
        tempWin.location = this.tempInfoSiteData.url
      } else {
        this.showEditInfoSiteDataDialog()
      }
    },
    handleClose() {
      this.tempInfoSiteData = _.cloneDeep(this.originInfoSiteData)
      this.isEditInfoSiteDialogShow = false
    },
    checkDisplayNameLength() {
      let displayName = this.tempInfoSiteData.displayName
      let displayNameLen = displayName.length
      if (displayNameLen < 2 || displayNameLen > 30) {
        this.$message({
          type: 'error',
          message: '资料网站名称最少2位，最多30位'
        })
        return false
      }
      return true
    }
  }
}
</script>
<style lang="scss">
.project-website {
  &-card {
    .el-card__body {
      padding: 24px 16px;
    }
  }
  &-info {
    font-size: 16px;
    color: #303133;
    font-weight: bold;
    word-break: break-word;
    margin: 4px 0 0;
  }
  &-operations {
    margin-top: 24px;
    display: flex;
    align-items: center;
    .el-button {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .el-icon-edit-outline {
      margin-left: 16px;
      cursor: pointer;
      font-size: 14px;
      color: #909399;
    }
  }
}
</style>
<template>
  <div class="project-joined-members-list">
    <el-table v-if="type === 'table'" :data="filterOwnerMemberList" border style="width: 100%" v-loading='isLoading' class="project-joined-members-list-table">
      <el-table-column prop="username" :label="$t('project.username')" width="357">
      </el-table-column>
      <el-table-column :label="$t('project.joinAt')" width="357">
        <template slot-scope="scope">{{scope.row.updatedAt | formatDate(formatType)}}</template>
      </el-table-column>
      <el-table-column :label="$t('project.operations')" class-name='project-joined-members-list-table-operate' width="160">
        <template slot-scope="scope">
          <el-button size="mini" @click="deleteFromProject(scope.row)">{{$t('project.removeMember')}}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-card v-if="type === 'card'" class="project-joined-members-list-card" shadow="never">
      <div slot="header" class="clearfix">
        <span class="project-joined-members-list-card-title">{{$t("project.projectMembers")}}</span>
      </div>
      <div class="project-joined-members-list-card-created">
        <img class="project-joined-members-list-card-profile" :src="projectOwnerPortrait || defaultPortrait" alt="" @click="goCreatorHome()">
        <span class="project-joined-members-list-card-username" :title="originProjectUsername">{{originProjectUsername}}</span>
        <span class="project-joined-members-list-card-label">{{$t("project.creator")}}</span>
      </div>
      <div v-if="filterOwnerMemberList && filterOwnerMemberList.length" class="project-joined-members-list-card-profiles">
        <img @click="goMemberHome(member)" v-for="(member, index) in filterOwnerMemberList" :key="index" class="project-joined-members-list-card-profile project-joined-members-list-card-profiles-item" :src='member.portrait || defaultPortrait' :title='member.username' alt="">
      </div>
      <div v-else class="project-joined-members-list-card-profiles-empty">{{$t("project.noOtherMembers")}}</div>
    </el-card>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import moment from 'moment'
export default {
  name: 'ProjectJoinedMembersList',
  props: {
    projectId: {
      required: true
    },
    type: {
      type: String,
      default: 'table',
      validator: function(value) {
        return ['table', 'card'].indexOf(value) !== -1
      }
    },
    projectOwnerPortrait: String,
    originProjectUsername: String,
    projectDetail: {
      type: Object,
      required: true
    }
  },
  async created() {
    this.isLoading = true
    await this.getProjectMember({
      objectId: this.projectId,
      objectType: 5
    })
    this.isLoading = false
  },
  data() {
    return {
      formatType: 'YYYY/MM/DD',
      isLoading: false,
      defaultPortrait: require('@/assets/img/default_portrait.png')
    }
  },
  computed: {
    ...mapGetters({
      pblProjectMemberList: 'pbl/projectMemberList'
    }),
    projectOwnerUserId() {
      return _.get(this.projectDetail, 'userId')
    },
    memberList() {
      return this.pblProjectMemberList({ projectId: this.projectId })
    },
    filterOwnerMemberList() {
      return _.filter(
        this.memberList,
        member => member.userId !== this.projectOwnerUserId
      )
    }
  },
  methods: {
    ...mapActions({
      getProjectMember: 'pbl/getProjectMember',
      deleteMember: 'pbl/deleteMember'
    }),
    goMemberHome(member){
      window.open(`${window.location.origin}/u/${member.username}`)
    },
    goCreatorHome(){
      window.open(`${window.location.origin}/u/${this.originProjectUsername}`)
    },
    async deleteFromProject(memberDetail) {
      let { id } = memberDetail
      this.isLoading = true
      await this.deleteMember({
        id,
        objectId: this.projectId,
        objectType: 5
      })
        .then(() => {
          this.isLoading = false
          this.$message({
            type: 'success',
            message: '移除成功'
          })
        })
        .catch(error => {
          this.isLoading = false
          console.log(error)
        })
    }
  },
  filters: {
    formatDate(date, formatType) {
      return moment(date).format(formatType)
    }
  }
}
</script>
<style lang="scss">
.project-joined-members-list {
  .el-table__row .cell {
    color: #303133;
  }
  .cell {
    padding: 0 24px;
  }
  .el-table--border th:first-child .cell,
  .el-table--border td:first-child .cell {
    padding-left: 24px;
  }
  &-table {
    td,
    th {
      padding: 4px 0;
      font-weight: normal;
    }
    &-operate {
      .cell {
        padding: 0 12px;
        text-align: center;
      }
      .el-button--mini {
        padding: 3px 19px;
      }
    }
  }
  &-card {
    &-title {
      font-weight: bold;
    }
    &-profile {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      object-fit: cover;
      cursor: pointer;
    }
    &-created {
      height: 96px;
      display: flex;
      align-items: center;
      font-size: 16px;
      color: #303133;
      border-bottom: 1px solid #e8e8e8;
      padding: 0 16px;
    }
    &-label {
      font-size: 12px;
      height: 20px;
      line-height: 20px;
      color: #909399;
      border: 1px solid #e8e8e8;
      padding: 0 8px;
      border-radius: 4px;
    }
    &-username {
      margin: 0 16px;
      flex: 1;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    &-profiles {
      padding: 16px 8px;
      &-item {
        padding: 8px;
        cursor: pointer;
      }
    }
    &-profiles-empty {
      padding: 16px 8px;
      text-align: center;
    }
    .el-card__body {
      padding: 0;
    }
  }
}

@media (max-width: 768px) {
  .project-joined-members-list {
    &-card {
      &-profile {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
      }
      &-created {
        height: 80px;
        display: flex;
        align-items: center;
        font-size: 16px;
        color: #303133;
        border-bottom: 1px solid #e8e8e8;
        padding: 0 16px;
      }
    }
  }
}
</style>
<template>
  <div class="project-members">
    <!-- <div class="project-members-invite">
      <el-input placeholder="输入用户名进行邀请" v-model="inviteUsername">
        <template slot="append">
          <el-button type="info" @click="invitToProject" :disabled="!inviteUsername">邀请</el-button>
        </template>
      </el-input>
    </div> -->
    <el-tabs class="project-members-tabs" type="card">
      <el-tab-pane :label="$t('project.applicants')">
        <project-applied-list :projectId='projectId'></project-applied-list>
      </el-tab-pane>
      <el-tab-pane :label="$t('project.projectMembers')">
        <project-joined-members-list :projectDetail='projectDetail' :projectId='projectId'></project-joined-members-list>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import ProjectAppliedList from './ProjectAppliedList'
import ProjectJoinedMembersList from './ProjectJoinedMembersList'
export default {
  name: 'ProjectMembers',
  props: {
    projectId: {
      required: true
    },
    projectDetail: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      inviteUsername: ''
    }
  },
  methods: {
    invitToProject() {
      console.log(this.inviteUsername)
    }
  },
  components: {
    ProjectAppliedList,
    ProjectJoinedMembersList
  }
}
</script>
<style lang="scss">
.project-members {
  width: 875px;
  &-invite {
    margin-bottom: 24px;
    .el-input__inner {
      color: #909399;
    }
    .el-input-group__append {
      color: #303133;
      cursor: pointer;
      background-color: transparent;
      padding: 0;
      width: 75px;
      .el-button {
        width: 100%;
        height: 100%;
        border-radius: 0;
        margin-left: 0;
        background-color: #f5f5f5;
      }
      .el-button.is-disabled {
        opacity: 0.8;
        background-color: #c8c9cc;
        color: #303133;
        border-color: #c8c9cc;
      }
    }
  }
  &-tabs {
    .el-tabs__header {
      padding-left: 0;
      margin-bottom: 0;
      border-bottom: none;
      .el-tabs__nav {
        border-radius: 8px 8px 0 0;
        border-width: 0 0 0 1px;
      }
      .el-tabs__item {
        height: 48px;
        line-height: 48px;
        padding: 0 14px;
        color: #606266;
        border-bottom-color: #e4e7ed;
        background-color: #f5f5f5;
        border-radius: 10px 10px 0px 0px;
        border: 1px solid #e4e7ed;
        margin-left: -1px;
      }
      .el-tabs__item:first-child {
        margin-left: 0;
      }
      .el-tabs__nav-wrap .el-tabs__item:last-child,
      .el-tabs__nav-wrap .el-tabs__item:nth-child(2) {
        padding: 0 14px;
      }
      .el-tabs__item.is-active {
        background-color: #fff;
        border-bottom-color: #e4e7ed;
        color: #2296f3;
      }
    }
  }
}
</style>
<template>
  <div class="project-tags">
    <el-card class="project-tags-card" shadow="never" v-loading='isLoading'>
      <div slot="header" class="clearfix">
        <span class="project-tags-card-label">{{$t("project.projectTags")}}</span>
        <el-button v-if="isLoginUserEditable" class="project-tags-card-button" type="text" @click="toggleIsTagEditing">
          <i class="el-icon-edit-outline" v-show="!isTagEditing"></i>
          <span v-show="isTagEditing"><i class="iconfont icon-save3"></i>{{$t("common.Save")}}</span>
        </el-button>
      </div>
      <div v-show="tempTags.length <= 0 && !isTagEditing">{{$t("project.noTags")}}</div>
      <el-tag v-show="tempTags.length > 0 || isTagEditing" :closable="isTagEditing" size="small" :key="tag" v-for="tag in tempTags" :disable-transitions="false" @close="handleClose(tag)">
        {{tag}}
      </el-tag>
      <el-input class="project-tags-new-input" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
      </el-input>
      <el-button v-show="isTagEditing" v-else class="project-tags-new-button" size="small" @click="showInput">+ {{$t("project.newTag")}}</el-button>
    </el-card>
  </div>
</template>
<script>
import { checkSensitiveWords } from '@/lib/utils/sensitive'
import { mapActions } from 'vuex'
export default {
  name: 'ProjectTags',
  props: {
    originProjectDetail: {
      type: Object,
      required: true
    },
    projectId: {
      required: true
    },
    isLoginUserEditable: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.copiedProjectDetail = _.cloneDeep(this.originProjectDetail)
    let tags = this.copiedProjectDetail.tags
    tags = _.trim(tags, '|')
    this.tempTags = _.filter(tags.split('|'), obj => obj) || []
  },
  data() {
    return {
      tempTags: [],
      inputVisible: false,
      inputValue: '',
      isTagEditing: false,
      isLoading: false,
      copiedProjectDetail: {}
    }
  },
  computed: {
    isModified() {
      return this.formatTagsToBackEndStyle !== this.originTagsToBackageEndStyl
    },
    formatTagsToBackEndStyle() {
      return '|' + _.join(this.tempTags, '|') + '|'
    },
    originTagsToBackageEndStyl() {
      return this.copiedProjectDetail.tags
    },
    updatingProjectData() {
      return _.merge(this.originProjectDetail, {
        tags: this.formatTagsToBackEndStyle
      })
    }
  },
  methods: {
    ...mapActions({
      pblUpdateProject: 'pbl/updateProject'
    }),
    handleClose(tag) {
      this.tempTags.splice(this.tempTags.indexOf(tag), 1)
    },
    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },
    async handleInputConfirm() {
      this.inputValue = _.trim(this.inputValue, ' ')
      let inputValue = this.inputValue
      if (inputValue.indexOf('|') !== -1) {
        this.$message({
          showClose: true,
          message: '标签里不能包含|',
          type: 'error'
        })
        return
      }
      this.isLoading = true
      let sensitiveResult = await checkSensitiveWords({
        checkedWords: inputValue
      }).catch()
      this.isLoading = false
      if (sensitiveResult && sensitiveResult.length > 0) {
        this.inputValue = _.get(sensitiveResult, '[0].word', this.inputValue)
        return
      }
      let nowTagInTagsIndex = _.findIndex(
        this.tempTags,
        tag => tag === inputValue
      )
      if (nowTagInTagsIndex !== -1) {
        this.$message({
          showClose: true,
          message: '该标签已存在',
          type: 'error'
        })
        return
      }
      inputValue && this.tempTags.push(inputValue)
      this.inputVisible = false
      this.inputValue = ''
    },
    async toggleIsTagEditing() {
      if (this.isTagEditing) {
        if (!this.isModified) {
          this.isTagEditing = !this.isTagEditing
          return
        }
        this.isLoading = true
        await this.pblUpdateProject({
          projectId: this.projectId,
          updatingProjectData: this.updatingProjectData
        })
          .then(() => {
            this.$message({
              type: 'success',
              message: this.$t('project.labelUpdated')
            })
            this.isTagEditing = !this.isTagEditing
            this.isLoading = false
          })
          .catch(error => {
            this.$message({
              type: 'error',
              message: '标签更新失败,请重试'
            })
            this.isLoading = false
            console.error(error)
          })
      } else {
        this.isTagEditing = !this.isTagEditing
      }
    }
  }
}
</script>

<style lang="scss">
.project-tags {
  &-card {
    &-label {
      font-weight: bold;
    }
    &-button {
      float: right;
      padding: 3px 0;
      color: #909399;
    }
    .el-tag {
      background-color: #eee;
      color: #909399;
      border: none;
      margin-bottom: 16px;
    }
    .el-tag--small .el-icon-close {
      width: 10px;
      right: -3px;
      color: #f56c6c;
    }
    .el-input--small .el-input__inner {
      height: 24px;
      line-height: 24px;
      padding: 0 8px;
    }
  }
  &-new-input {
    width: 54px;
    margin-left: 10px;
    vertical-align: bottom;
    height: 24px;
    line-height: 24px;
    margin-bottom: 16px;
  }
  &-new-button {
    margin-left: 10px;
    height: 24px;
    line-height: 22px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .el-tag + .el-tag {
    margin-left: 10px;
  }
}
</style>

<template>
  <div class="website-binder">
    <h1 class="website-binder-title">{{$t("project.websiteSettingForProject")}}</h1>
    <p class="website-binder-info">
      <span class="website-binder-warning">!</span>{{$t("project.canNotChangedAfterSettings")}}
    </p>
    <div class="website-binder-cards">
      <div class="website-binder-cards-item" @click="openUserSitesDialog">{{$t("project.selectExistingWebsite")}}</div>
      <div class="website-binder-cards-item" @click='openNewSiteDialog'>{{$t("project.createNewWebsite")}}</div>
    </div>
    <el-dialog v-loading='isCreating' width="760px" :title="$t('project.selectExistingSite')" :visible.sync="isUserSitesDialogShow" :append-to-body='true'>
      <user-sites-selector ref='userSitesRef'></user-sites-selector>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeUserSitesDialog">{{$t("common.Cancel")}}</el-button>
        <el-button type="primary" @click="createNewProjectByBind">{{$t("common.Sure")}}</el-button>
      </div>
    </el-dialog>
    <new-website-dialog :isContinueAfterCreate='true' :show='isNewWebsiteDialogShow' @close='closeNewWebsiteDialog' @finish='createNewProjectByNewSite'></new-website-dialog>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import NewWebsiteDialog from '@/components/common/NewWebsiteDialog'
import UserSitesSelector from '@/components/common/UserSitesSelector'
export default {
  name: 'WebsiteBinder',
  data() {
    return {
      isCreating: false,
      isNewWebsiteDialogShow: false,
      isUserSitesDialogShow: false
    }
  },
  computed: {
    ...mapGetters({
      newSiteInfo: 'user/newSiteInfo'
    })
  },
  methods: {
    ...mapActions({
      getWebsiteDetailBySiteId: 'user/getWebsiteDetailBySiteId'
    }),
    openNewSiteDialog() {
      this.isNewWebsiteDialogShow = true
    },
    closeNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = false
    },
    openUserSitesDialog() {
      this.isUserSitesDialogShow = true
    },
    closeUserSitesDialog() {
      this.isUserSitesDialogShow = false
    },
    async createNewProjectByBind() {
      let siteId = _.get(this.$refs.userSitesRef, 'selectSiteId')
      await this.getWebsiteDetailBySiteId({
        siteId: siteId
      }).catch(e => console.error(e))
      this.$emit('confirmSiteId', { siteId })
      this.closeUserSitesDialog()
    },
    async createNewProjectByNewSite() {
      let siteId = _.get(this.newSiteInfo, 'id')
      await this.getWebsiteDetailBySiteId({
        siteId: siteId
      }).catch(e => console.error(e))
      this.$emit('confirmSiteId', { siteId })
      this.closeNewWebsiteDialog()
    }
  },
  components: {
    UserSitesSelector,
    NewWebsiteDialog
  }
}
</script>
<style lang="scss">
.website-binder {
  &-title {
    font-size: 24px;
    color: #303133;
    font-weight: normal;
    margin: 0;
  }
  &-info {
    font-size: 14px;
    color: #de992d;
  }
  &-warning {
    display: inline-block;
    width: 16px;
    height: 16px;
    background-color: #de992d;
    border-radius: 50%;
    color: #fff;
    text-align: center;
    line-height: 16px;
    margin-right: 4px;
  }
  &-cards {
    display: flex;
    margin: 38px 0 80px;
    &-item {
      cursor: pointer;
      width: 254px;
      height: 136px;
      line-height: 136px;
      text-align: center;
      border-radius: 4px;
      font-size: 14px;
      color: #f5f5f5;
      margin-right: 45px;
      &:nth-child(1) {
        background: linear-gradient(to bottom, #b141f7, #a02bea);
      }
      &:nth-child(2) {
        background: linear-gradient(to bottom, #23b6f3, #2397f3);
      }
    }
  }
}
</style>


```