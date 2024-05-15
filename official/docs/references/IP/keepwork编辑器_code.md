``` javascript
<template>
  <el-row :gutter="0" type="flex" class="full-height editor-page-container">
    <el-col id="managerWin" class="manager-win" v-show="isManagerShow">
      <el-row class="toolbar">
        <el-button-group>
          <el-tooltip :content="$t('editor.files')">
            <el-button id="file-manager-button" class="iconfont icon-list_directory" :class="{'el-button--primary': activeManagePaneComponentName=='FileManager'}" @click="changeView('FileManager')"></el-button>
          </el-tooltip>
          <el-tooltip v-if="activePage && hasOpenedFiles" :content="$t('common.myWebDisk')">
            <el-button class="iconfont icon-upload" @click="openSkyDriveManagerDialog"></el-button>
          </el-tooltip>
          <el-tooltip v-if="activePage && hasOpenedFiles" :content="$t('common.oldVersions')">
            <el-button class="iconfont icon-historyrecord" @click="showFileHistory"></el-button>
          </el-tooltip>
        </el-button-group>
        <sky-drive-manager-dialog :isInsertable="true" :show="showSkyDrive" @close="closeSkyDriveManagerDialog"></sky-drive-manager-dialog>
      </el-row>
      <el-scrollbar wrap-class="manager-content-box el-row" view-class="manager-content-inner" :native="false">
        <keep-alive>
          <component :is="activeManagePaneComponentName" v-bind="activeManagePaneComponentProps" v-keep-scroll-position></component>
        </keep-alive>
      </el-scrollbar>
    </el-col>
    <div class="col-between flex-order-one" v-show="isManagerShow"></div>
    <el-col id="previewWin" v-show="!isWelcomeShow && isPreviewShow" class="preview-win" :style="setPreviewWinStyle" @mousemove.native="dragMouseMove" @mouseup.native="dragMouseUp">
      <el-row class="toolbar">
        <el-button-group>
          <el-tooltip :content="$t('editor.preview')">
            <el-button class="iconfont icon-new_open_window" @click="showPreview"></el-button>
          </el-tooltip>
        </el-button-group>
      </el-row>
      <iframe id="frameViewport" src="/vp" style="height: 100%; width: 100%; background: #fff" />
      <iframe-dialog></iframe-dialog>
      <div class="mouse-event-backup" v-show="resizeWinParams.isResizing"></div>
      <el-dialog class="multiple-text-dialog" :title="$t('card.paragraph')" :visible="isMultipleTextDialogShow" top="6vh" :before-close="handleMultipleTextDialogClose" @open="initMarkdownModDatas">
        <el-input type="textarea" resize="none" :placeholder="$t('field.' + editingMarkdownModDatas.key)" v-model="editingMarkdownModDatas.content"></el-input>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="handleMultipleTextDialogClose('save')">{{$t('common.confirmButtonText')}}</el-button>
        </span>
      </el-dialog>
    </el-col>
    <div class="col-between editor-resizer flex-order-two" v-show="!isWelcomeShow && isPreviewShow && isCodeShow" @mousedown="resizeCol($event, 'previewWinWidth', 'codeWinWidth')" @mousemove.native="dragMouseMove" @mouseup.native="dragMouseUp"></div>
    <el-col id="codeWin" v-if="isCodeShow" v-show="!isWelcomeShow" class="code-win" :style="setCodeWinStyle" @mousemove.native="dragMouseMove" @mouseup.native="dragMouseUp">
      <el-row class="toolbar">
        <el-scrollbar wrap-class="toolbar" :native="false">
          <el-col class="toolbar-content">
            <div class="zenmode-icon" v-if="isZenMode">
              <img :src="require('@/assets/img/zen.png')">
            </div>
            <div class="toolbar-content_left">
              <el-button-group>
                <el-tooltip :content="$t('editor.title') + '1'">
                  <el-button class="iconfont icon-h1" @click="insertHeadline(1)"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.title') + '2'">
                  <el-button class="iconfont icon-h2" @click="insertHeadline(2)"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.title') + '3'">
                  <el-button class="iconfont icon-h3" @click="insertHeadline(3)"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.bold')">
                  <el-button class="iconfont icon-thickening" @click="setFontStyle('bold')"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.italic')">
                  <el-button class="iconfont icon-incline" @click="setFontStyle('italic')"></el-button>
                </el-tooltip>
              </el-button-group>
              <el-button-group>
                <el-tooltip :content="$t('editor.horizontalDiv')">
                  <el-button class="iconfont icon-code_division_line" @click="insertLine"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.code')">
                  <el-button class="iconfont icon-code" @click="insertCode"></el-button>
                </el-tooltip>
                <el-tooltip :content="$t('editor.link')">
                  <el-button class="iconfont icon-link_" @click="insertLink"></el-button>
                </el-tooltip>
              </el-button-group>
              <el-button-group v-if="!isZenMode">
                <el-tooltip :content="$t('tips.mod')">
                  <el-button class="iconfont icon-module" @click="addModToMarkdown"></el-button>
                </el-tooltip>
              </el-button-group>
            </div>
            <el-tooltip :content="$t('tips.ShowZenMode')">
              <el-button-group class="fullScreenBtn">
                <el-button :icon="fullscreenIcon" circle @click="openZenMode"></el-button>
              </el-button-group>
            </el-tooltip>
          </el-col>
        </el-scrollbar>
      </el-row>
      <editor-markdown ref="codemirror" @insertBigfile="insertBigfile"></editor-markdown>
    </el-col>
    <el-col v-if="isWelcomeShow" class="guid-col">
      <el-row>
        <el-col :span="3">&nbsp;</el-col>
        <el-col :span="21">
          <editor-welcome></editor-welcome>
        </el-col>
      </el-row>
      <div class="guid-help">
        <a href="https://keepwork.com/official/help/index" target="_blank">{{$t('editor.help')}}</a>
      </div>
    </el-col>
    <file-history v-if="isFileHistoryVisible" class="editor-page-container-history"></file-history>
  </el-row>
</template>

<script>
import _ from 'lodash'
import { gConst } from '@/lib/global'
import EditorMarkdown from './EditorMarkdown'
import EditorWelcome from './EditorWelcome'
import ModPropertyManager from './ModPropertyManager'
import FileManager from './FileManager'
import ModsList from './ModsList'
import FileHistory from './FileHistory'
import Search from './Search'
import PageSetting from './PageSetting'
import SkyDriveManagerDialog from '@/components/common/SkyDriveManagerDialog'
import { mapGetters, mapActions } from 'vuex'
import IframeDialog from '@/components/common/IframeDialog'
import resize from './base/resize'
export default {
  name: 'Editor',
  mixins: [resize],
  data() {
    return {
      managerWinWidth: 0,
      previewWinWidth: 50,
      codeWinWidth: 50,
      gConst,
      editingMarkdownModDatas: {
        key: 'data',
        content: ''
      }
    }
  },
  created() {
    this.changeView('FileManager')
  },
  mounted() {
    this.$nextTick(function() {
      window.addEventListener('resize', function(e) {
        _.throttle(function() {
          this.bodyWidth = document.body.clientWidth
        }, 1000)
      })
    })
  },
  watch: {
    isPreviewShow: {
      handler(newVal, oldVal) {
        if (newVal === oldVal) {
          return
        }
        if (newVal === false) {
          this.previewWinWidth = 0
          this.codeWinWidth = 100 - this.managerWinWidth
        } else if (this.isCodeShow === false) {
          this.previewWinWidth = 100 - this.managerWinWidth
        } else {
          let halfWidth = (100 - this.managerWinWidth) / 2
          this.previewWinWidth = halfWidth
          this.codeWinWidth = halfWidth
        }
      },
      deep: true
    },
    isCodeShow: {
      handler(newVal, oldVal) {
        if (newVal === oldVal) {
          return
        }
        if (newVal === false) {
          this.codeWinWidth = 0
          this.previewWinWidth = 100 - this.managerWinWidth
        } else if (this.isPreviewShow === false) {
          this.codeWinWidth = 100 - this.managerWinWidth
        } else {
          let halfWidth = (100 - this.managerWinWidth) / 2
          this.previewWinWidth = halfWidth
          this.codeWinWidth = halfWidth
        }
      },
      deep: true
    }
  },
  components: {
    EditorMarkdown,
    EditorWelcome,
    ModPropertyManager,
    Search,
    ModsList,
    FileHistory,
    FileManager,
    PageSetting,
    SkyDriveManagerDialog,
    IframeDialog
  },
  computed: {
    ...mapGetters({
      activePage: 'activePage',
      activeMod: 'activeMod',
      preModKey: 'preModKey',
      activePageUrl: 'activePageUrl',
      personalSiteList: 'user/personalSiteList',
      isFileHistoryVisible: 'isFileHistoryVisible',
      activeManagePaneComponentName: 'activeManagePaneComponentName',
      activeManagePaneComponentProps: 'activeManagePaneComponentProps',
      showingCol: 'showingCol',
      activePageInfo: 'activePageInfo',
      isMultipleTextDialogShow: 'isMultipleTextDialogShow',
      activePropertyData: 'activePropertyData',
      hasOpenedFiles: 'hasOpenedFiles',
      showSkyDrive: 'showSkyDrive',
      showAngle: 'showAngle',
      isCodeShow: 'isCodeShow',
      isPreviewShow: 'isPreviewShow',
      isManagerShow: 'isManagerShow',
      isZenMode: 'isZenMode'
    }),
    isWelcomeShow() {
      return !this.activePageInfo.sitename
    },
    isDisplayButton() {
      if (this.isPreviewShow) {
        return this.generateStyleString({
          display: 'inline-block'
        })
      } else {
        return this.generateStyleString({
          display: 'none'
        })
      }
    },
    setPreviewWinStyle() {
      const style = {}
      if (!this.showAngle) {
        style.order = 3
      } else {
        style.order = 5
      }
      style.width = this.previewWinWidth + '%'
      return style
    },
    setCodeWinStyle() {
      const style = {}
      if (!this.showAngle) {
        style.order = 5
      } else {
        style.order = 3
      }
      style.width = this.codeWinWidth + '%'
      return style
    },
    showContent() {
      return this.isFullscreen
        ? this.$t('editor.fullScreen')
        : this.$t('editor.exitFullScreen')
    },
    fullscreenIcon() {
      return this.isManagerShow
        ? 'iconfont icon-full-screen_'
        : 'iconfont icon-full_screen_exit'
    }
  },
  methods: {
    ...mapActions({
      toggleFileHistoryVisibility: 'toggleFileHistoryVisibility',
      resetShowingCol: 'resetShowingCol',
      setIsMultipleTextDialogShow: 'setIsMultipleTextDialogShow',
      setActivePropertyData: 'setActivePropertyData',
      toggleSkyDrive: 'toggleSkyDrive'
    }),
    changeView(type) {
      this.$store.dispatch('setActiveManagePaneComponent', type)
    },
    openZenMode() {
      const dom = this.$el.querySelector('#codeWin')
      if (!dom) {
        return false
      }
      this.resetShowingCol({
        isZenMode: true
      })
      this.$fullscreen.toggle(dom, {
        wrap: false,
        fullscreenClass: 'zenmode',
        callback: state => {
          if (!state) {
            this.resetShowingCol({
              isZenMode: false
            })
            const vscroolbar = dom.querySelector('.CodeMirror-vscrollbar')
            // Is very strange. when I set display none, scroolbar is normally
            vscroolbar.style.display = 'none'
          }
        }
      })
    },
    generateStyleString(style) {
      let string = ''
      _.forEach(style, (value, key) => {
        string = string + key + ':' + value + ';'
      })
      return string
    },
    showPreview() {
      this.$emit('showPreview')
    },
    setFontStyle(style) {
      this.$refs.codemirror.setFontStyle(style)
    },
    insertHeadline(level) {
      this.$refs.codemirror.insertHeadline(level)
    },
    insertCode() {
      this.$refs.codemirror.insertCode()
    },
    insertLine() {
      this.$refs.codemirror.insertLine()
    },
    insertLink() {
      this.$refs.codemirror.insertLink()
    },
    insertImage() {
      this.$refs.codemirror.insertFile()
    },
    addModToMarkdown() {
      this.$refs.codemirror.addMod()
    },
    openSkyDriveManagerDialog() {
      this.toggleSkyDrive({
        showSkyDrive: true
      })
    },
    showFileHistory() {
      this.toggleFileHistoryVisibility({ isVisible: true })
    },
    async insertBigfile({ file, url }) {
      if (!url) return
      let ext = file.ext || (file.filename || '').split('.').pop()
      let filename = file.filename || url
      const modContent = `
bigFile:
  src: >-
    ${url}
  ext: ${ext}
  filename: ${filename}
  size: ${file.size}
          `
      const payload = {
        modName: 'ModBigFile',
        modContent
      }
      this.$refs.codemirror.updateActiveCursor()
      this.$store.dispatch('addBigFileToMarkdown', payload)
    },
    closeSkyDriveManagerDialog({ file, url }) {
      this.toggleSkyDrive({
        showSkyDrive: false
      })
      this.insertBigfile({
        file,
        url
      })
    },
    initMarkdownModDatas() {
      this.editingMarkdownModDatas = {
        content: this.activePropertyData.data,
        key: 'data'
      }
    },
    closeMultipleTextDialog() {
      this.setIsMultipleTextDialogShow({
        isShow: false
      })
    },
    saveMultipleTextDatas() {
      this.setActivePropertyData({
        data: {
          data: this.editingMarkdownModDatas.content
        }
      })
    },
    checkIsModified() {
      return (
        this.editingMarkdownModDatas.content !== this.activePropertyData.data
      )
    },
    handleMultipleTextDialogClose(type) {
      if (type === 'save') {
        this.saveMultipleTextDatas()
        this.closeMultipleTextDialog()
      } else {
        let isModified = this.checkIsModified()
        if (isModified) {
          let that = this
          this.$confirm(
            this.$t('editor.unSaveConfirm'),
            this.$t('editor.closeDialogTitle'),
            {
              confirmButtonText: that.$t('common.Sure'),
              cancelButtonText: that.$t('common.Cancel'),
              type: 'warning'
            }
          ).then(() => {
            this.closeMultipleTextDialog()
          })
        } else {
          this.closeMultipleTextDialog()
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.editor-page-container {
  background-color: #cdd4db;
  padding: 17px 0;
  &-history {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #fff;
    z-index: 2000;
  }
}
.full-height {
  height: 100%;
}
.manager-win,
.preview-win,
.code-win {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: auto;
}
.manager-win {
  order: 1;
  flex-basis: 460px;
  flex-shrink: 0;
}
.manager-content-box {
  flex: 1;
  background-color: #fff;
  overflow-y: auto;
}
.col-between {
  flex-basis: 17px;
  flex-shrink: 0;
  background-color: #cdd4db;
}
.flex-order-one {
  order: 2;
}
.flex-order-two {
  order: 4;
}
.editor-resizer {
  cursor: col-resize;
}
.editor-resizer:hover {
  background-color: #d9eafb;
}
#frameViewport {
  border: none;
}
.mouse-event-backup {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-color: transparent;
  z-index: 122;
}
.manager-win .el-button,
.code-win .el-button {
  width: 50px;
  height: 40px;
}
.code-win .el-button.is-circle {
  width: 40px;
  border-radius: 50%;
  padding: 0;
}
.code-win .is-circle .iconfont {
  font-size: 18px;
}
.manager-win .el-button-group .el-button--primary {
  border-color: #409eff;
}
.toolbar {
  background-color: #fff;
  padding: 9px 20px;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
  position: relative;
  flex-shrink: 0;
}
.toolbar-content {
  min-width: 500px;
  margin: 0 auto;
}
.toolbar-content_left {
  display: inline-block;
  vertical-align: middle;
}
.toolbar::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  background-color: #f5f5f5;
}
.toolbar::-webkit-scrollbar-track {
  border-radius: 0px;
  background-color: #f5f5f5;
}
.toolbar::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #555;
}
.toolbar .fullScreenBtn {
  float: right;
}
.toolbar .fullScreenBtn .el-button {
  border-radius: 4px;
}
.iconfont {
  padding: 0;
  width: 50px;
  height: 40px;
  font-size: 27px;
}
.code-win .iconfont {
  font-size: 16px;
}
.guid-col {
  order: 6;
  background: url('../../assets/img/background.png') no-repeat top right #fff;
  background-size: 45%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  color: #48a3ff;
  position: relative;
}
.guid-col .guid-help {
  width: 56px;
  height: 56px;
  background-color: #ffa33e;
  border: solid 4px #ffc586;
  border-radius: 50%;
  line-height: 56px;
  justify-content: center;
  text-align: center;
  font-size: 17px;
  color: #fff;
  position: absolute;
  bottom: 20px;
  right: 20px;
}
.guid-col .guid-help a {
  color: #fff;
  text-decoration: none;
}
.guid-col .guid-help::before {
  content: '';
  width: 21px;
  height: 21px;
  background-color: rgba(202, 149, 91, 0.28);
  position: absolute;
  right: -16px;
  bottom: -16px;
  border-radius: 50%;
}
.guid-col h1 {
  margin: 0 0 36px 0;
  font-size: 46px;
}
.code-win-fullscreen {
  width: 100% !important;
  height: 100%;
  background-color: #cdd4dc;
  max-width: 1080px;
}
@media (max-width: 1920px) {
  .manager-win {
    flex-basis: 320px;
  }
}
</style>

<style lang="scss">
.zenmode {
  background-color: black;
  background-image: url('../../assets/img/cubes.png');
  .toolbar {
    width: 100%;
    margin: 0 auto !important;
    padding: 0;
    overflow: hidden;
    background-color: #1c1c1c;
    .el-scrollbar {
      width: 1080px;
      margin: 0 auto;
    }
    .toolbar-content {
      padding: 8px;
      .zenmode-icon {
        float: left;
        margin-top: 5px;
        img {
          vertical-align: middle;
        }
        i {
          color: #5e5e5e;
          vertical-align: middle;
        }
      }
      .toolbar-content_left {
        text-align: right;
        float: right;
        button {
          background-color: #1c1c1c;
          border-color: #303133;
        }
        button:hover {
          background-color: #333333;
          color: white;
        }
        button:active {
          color: white;
        }
      }
    }
    .fullScreenBtn {
      display: none;
    }
  }
  .kp-md-editor {
    width: 1080px;
    margin: 0 auto;
    .CodeMirror-vscrollbar::-webkit-scrollbar {
      width: 10px;
    }
    .CodeMirror-vscrollbar::-webkit-scrollbar-thumb {
      background: #3b3b3b;
      border-radius: 20px;
    }
    .CodeMirror-vscrollbar::-webkit-scrollbar-track {
      background: #1c1c1c;
      border-radius: 20px;
    }
  }
}
.manager-win {
  .el-scrollbar {
    height: 100%;
  }
  .el-scrollbar__wrap {
    overflow-x: auto;
  }
  .manager-content-box {
    background-color: #fff;
  }
  .manager-content-inner {
    height: 100%;
  }
}
.el-tooltip__popper {
  font-size: 14px;
}
.multiple-text-dialog {
  .el-dialog {
    width: 1300px;
    max-width: 80vw;
  }
  .el-dialog__header {
    background-color: #3ba4ff;
    padding: 8px 30px;
  }
  .el-dialog__title {
    color: #fff;
    font-size: 16px;
  }
  .el-dialog__headerbtn {
    top: 15px;
    right: 14px;
  }
  .el-dialog__headerbtn .el-dialog__close {
    color: #fff;
  }
  .el-diaog__body {
    padding: 30px 0;
  }
  .el-textarea__inner {
    border: none;
    height: 640px;
    max-height: 70vh;
  }
  .el-button--primary {
    padding: 7px 45px;
  }
}
</style>

<template>
  <div class='editor-header'>
    <el-menu mode='horizontal'>
      <el-menu-item index="2">
        <el-dropdown placement="bottom-end" class="kp-dropdown-menu">
          <span class="el-dropdown-link">
            <img class='kp-logo' src='@/assets/img/logo.svg' alt='Menu'>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown" class="kp-dropdown-menu-content">
            <el-dropdown-item>
              <div class="kp-menu-top">
                <div class="kp-icon">
                  <i class="iconfont icon-add1"></i>
                </div>
                <div class="kp-submenu-top-content">
                  <button @click.stop="openNewWebsiteDialog">{{$t('editor.newWebsite')}}</button>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div :class="['kp-menu-top',currentDisabled ? 'isDisabled disabled-bgc':'']">
                <div class="kp-icon">
                  <i class="iconfont icon-setting"></i>
                </div>
                <div class="kp-submenu-top-content">
                  <button :disabled='currentDisabled' @click.stop="openWebsiteSettingDialog">{{$t('editor.setUpTheWebsite')}}</button>
                  <button :disabled='currentDisabled' @click.stop="goSettingPage">{{$t('editor.setUpThePage')}}</button>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div :class="['kp-menu-top',currentDisabled ? 'isDisabled disabled-bgc':'']">
                <div class="kp-icon">
                  <i class="iconfont icon-delete1"></i>
                </div>
                <div class="kp-submenu-top-content">
                  <button :disabled='currentDisabled' @click="removeCurrentPage(currentPagePath)">{{$t('editor.deleteTheCurrentPage')}}</button>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div :class="['kp-menu-top',isSaveAll ? 'isDisabled disabled-bgc':'']">
                <div class="kp-icon">
                  <i class="iconfont icon-save1"></i>
                </div>
                <div class="kp-submenu-top-content">
                  <button :disabled='isActivePageSaved' @click.stop="save">{{$t('editor.save')}}</button>
                  <button :disabled='isSaveAll' @click.stop="saveAllOpenedFiles">{{$t('editor.saveAll')}}</button>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div :class="['kp-menu-top',currentDisabled ? 'isDisabled disabled-bgc':'']">
                <div class="kp-icon">
                  <i class="iconfont icon-close1"></i>
                </div>
                <div class="kp-submenu-top-content">
                  <button :disabled='currentDisabled' @click.stop="handleCloseConfirm">{{$t('editor.close')}}</button>
                  <button :disabled='currentDisabled' @click.stop="closeAllOpenedFilesConfirm">{{$t('editor.closeAll')}}</button>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div class="kp-menu">
                <button @click.stop="refreshOpenedFile(activeFilePath)" :disabled='currentDisabled'>
                  <i class="iconfont icon-refresh1"></i>{{$t('editor.refresh')}}</button>
                <button @click.stop='undo' :disabled='!canUndo'>
                  <i class="iconfont icon-pre-step"></i>{{$t('editor.revoke')}}</button>
                <button @click.stop='redo' :disabled='!canRedo'>
                  <i class="iconfont icon-redo"></i>{{$t('editor.redo')}}</button>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div class="kp-menu">
                <button :disabled='currentDisabled' @click="changeView('ModsList')">
                  <i class="iconfont icon-mod"></i>{{$t('editor.modules')}}</button>
                <button :disabled='currentDisabled' @click="openSkyDriveManagerDialog">
                  <i class="iconfont icon-lfile"></i>{{$t('modList.bigFile')}}</button>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div class="kp-menu">
                <button :disabled='currentDisabled' @click='togglePreviewWin'>
                  <i class="iconfont icon-preview1"></i>{{$t('tips.ShowPreviewOnly')}}
                </button>
                <button :disabled='currentDisabled' @click='toggleBoth'>
                  <i class="iconfont icon-both"></i>{{$t('tips.ShowBoth')}}
                </button>
                <button :disabled='currentDisabled' @click='toggleCodeWin'>
                  <i class="iconfont icon-code1"></i>{{$t('tips.ShowCodeOnly')}}
                </button>
                <button :disabled='currentDisabled' @click='openZenMode'>
                  {{$t('tips.ShowZenMode')}}
                </button>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div class="kp-menu">
                <button>
                  <i class="iconfont icon-help"></i>
                  <a class="kp-menu-help" href="https://keepwork.com/official/help/index" target="_blank">{{$t('editor.help')}}</a>
                </button>
                <button :class=" isEnglish ? 'btn-language' : '' " @click="toggleLanguage">
                  <i :class="['iconfont', 'icon-Chinese-english', isEnglish ? 'icon-language' : '']"></i>
                  {{$t('common.chinese-englishSwitch')}}
                </button>
                <button :class=" isEnglish ? 'btn-angles' : '' " @click="toggleLeftAndRightAngles" :disabled="isWelcomeShow || !(isPreviewShow && isCodeShow)">
                  <i class="iconfont icon-qiehuan"></i>
                  {{$t('common.left-rightAngles')}}
                </button>
                <button :disabled='currentDisabled' :class=" isEnglish ? 'btn-angles' : '' " @click="showFileHistory">
                  <i class="iconfont icon-historyrecord"></i>
                  {{$t('common.oldVersions')}}
                </button>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <div class="kp-menu">
                <button @click="backHome">
                  <i class="iconfont icon-home"></i>{{$t('editor.backHomePage')}}</button>
              </div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-menu-item>
      <el-menu-item index='3' class='li-btn save-btn' :disabled='isActivePageSaved'>
        <el-tooltip :content="$t('editor.save')">
          <span v-loading='savePending' class='iconfont icon-save' @click='save'></span>
        </el-tooltip>
      </el-menu-item>
      <el-menu-item index='4' class='li-btn' @click='undo' :disabled='!canUndo'>
        <el-tooltip :content="$t('editor.revoke')">
          <span class='iconfont icon-return'></span>
        </el-tooltip>
      </el-menu-item>
      <el-menu-item index='5' class='li-btn' @click='redo' :disabled='!canRedo'>
        <el-tooltip :content="$t('editor.redo')">
          <span class='iconfont icon-revocation'></span>
        </el-tooltip>
      </el-menu-item>
      <el-menu-item index='6' class="link-box" v-if="activePage && hasOpenedFiles">
        <el-tooltip :content="$t('tips.copyUrl')">
          <i class="iconfont icon-copy" @click='doCopyLink'></i>
        </el-tooltip>
        <el-tooltip :content="$t('tips.openInNewWindow')">
          <a :href='activePageFullUrl' target='_blank'>{{ activePageFullUrl }}</a>
        </el-tooltip>
      </el-menu-item>
      <el-menu-item index='7' class='unsaved-tip'>
        <!-- <span>{{ isActivePageSaved ? '' : $t('editor.unsavedTip') }}</span> -->
      </el-menu-item>
      <el-menu-item index='8' class='pull-right user-profile-box'>
        <img class='user-profile' :src='userProfile.portrait' alt=''>
      </el-menu-item>
      <el-menu-item v-if="!isWelcomeShow" index='9' class='switch-box'>
        <el-tooltip :content="$t('tips.ShowPreviewOnly')">
          <span class="iconfont icon-preview1" :class='{"switch-box-active": isPreviewShow && !isCodeShow}' @click="togglePreviewWin()"></span>
        </el-tooltip>
        <el-tooltip :content="$t('tips.ShowBoth')">
          <span class="iconfont icon-both" :class='{"switch-box-active": isPreviewShow && isCodeShow}' @click="toggleBoth()"></span>
        </el-tooltip>
        <el-tooltip :content="$t('tips.ShowCodeOnly')">
          <span class="iconfont icon-code1" :class='{"switch-box-active": !isPreviewShow && isCodeShow}' @click="toggleCodeWin()"></span>
        </el-tooltip>
      </el-menu-item>
    </el-menu>
    <new-website-dialog :show='isNewWebsiteDialogShow' @close='closeNewWebsiteDialog'></new-website-dialog>
    <div @click.stop v-if='isWebsiteSettingShow'>
      <website-setting-dialog :show='isWebsiteSettingShow' :sitePath='currentPath' @close='closeWebsiteSettingDialog'></website-setting-dialog>
    </div>
    <el-dialog center :visible.sync="dialogVisible" width="300px" closed="handleCloseDialog">
      <center v-if="closeOneFile">{{`"${fileName}" ${this.$t("editor.fileUnSaved")}`}}</center>
      <center v-else>{{`"${toBeCloseFileName}" ${this.$t("editor.fileUnSaved")}`}}</center>
      <span slot="footer" class="dialog-footer">
        <el-button type="warning" @click.stop="handleClose" :disabled="savePending">{{this.$t("editor.unSaveClose")}}</el-button>
        <el-button type="primary" @click.stop="saveHandleClose" :disabled="savePending">{{this.$t("editor.saveClose")}}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Mousetrap from 'mousetrap'
import { gConst } from '@/lib/global'
import { toggleLanguage, locale } from '@/lib/utils/i18n'
import NewWebsiteDialog from '@/components/common/NewWebsiteDialog'
import WebsiteSettingDialog from '@/components/common/WebsiteSettingDialog'

export default {
  name: 'EditorHeader',
  data: function() {
    return {
      savePending: false,
      isNewWebsiteDialogShow: false,
      isWebsiteSettingShow: false,
      dialogVisible: false,
      closeOneFile: false,
      toBeCloseFileName: '',
      toBeCloseFilePath: '',
      gConst,
      nowOrigin: document.location.origin
    }
  },
  mounted() {
    Mousetrap.unbind('mod+s')
    Mousetrap.bind('mod+s', () => {
      this.save()
      return false
    })
    Mousetrap.unbind('mod+z')
    Mousetrap.bind('mod+z', () => {
      this.undo()
      return false
    })
    Mousetrap.unbind('mod+y')
    Mousetrap.bind('mod+y', () => {
      this.redo()
      return false
    })
  },
  computed: {
    ...mapGetters({
      userProfile: 'user/profile',
      showingCol: 'showingCol',
      activePageInfo: 'activePageInfo',
      canUndo: 'canUndo',
      canRedo: 'canRedo',
      openedFiles: 'openedFiles',
      activeAreaData: 'activeAreaData',
      activeAreaFile: 'activeAreaFile',
      activePage: 'activePage',
      hasOpenedFiles: 'hasOpenedFiles',
      isCodeShow: 'isCodeShow',
      isPreviewShow: 'isPreviewShow',
      getSiteLayoutConfigBySitePath: 'user/siteLayoutConfigBySitePath',
      showAngle: 'showAngle',
      updateRecentUrlList: 'updateRecentUrlList'
    }),
    isWelcomeShow() {
      return !this.activePageInfo.sitename
    },
    isEnglish() {
      return locale === 'en-US' ? true : false
    },
    activeFilePath() {
      return { path: this.currentPagePath }
    },
    currentDisabled() {
      return !(this.activePage && this.hasOpenedFiles)
    },
    fileName() {
      return this.activePageInfo.sitename + '/' + this.activePageInfo.pagename
    },
    currentPath() {
      return this.activePageInfo.sitepath
    },
    currentPagePath() {
      return this.activePageInfo.barePath
    },
    hasUnSaveOpenedFiles() {
      return this.unSavedOpenedFiles.length > 0
    },
    isSaveAll() {
      return this.unSavedOpenedFiles.length === 0
    },
    unSavedOpenedFiles() {
      return _.filter(_.values(this.openedFiles), ({ saved }) => !saved)
    },
    unSavedOpenedFilesPaths() {
      return _.map(this.unSavedOpenedFiles, ({ path }) => `${path}.md`.slice(1))
    },
    showingType() {
      if (
        this.showingCol.isCodeShow === false &&
        this.showingCol.isPreviewShow === true
      ) {
        return this.$t('editor.preview')
      }
      if (
        this.showingCol.isCodeShow === true &&
        this.showingCol.isPreviewShow === false
      ) {
        return this.$t('editor.code')
      }
      if (
        this.showingCol.isCodeShow === true &&
        this.showingCol.isPreviewShow === true
      ) {
        return this.$t('editor.splitScreen')
      }
    },
    activePageFullUrl() {
      let { fullPath = '' } = this.activePageInfo
      let url = `${this.nowOrigin}/${fullPath}`
      return (url || '').replace(/\.md$/, '')
    },
    isActivePageSaved() {
      let { saved } = this.activeAreaFile || {}
      return saved === false ? false : true
    }
  },
  methods: {
    ...mapActions({
      saveActivePage: 'saveActivePage',
      undo: 'undo',
      redo: 'redo',
      setActiveManagePaneComponent: 'setActiveManagePaneComponent',
      savePageByPath: 'savePageByPath',
      closeOpenedFile: 'closeOpenedFile',
      closeAllOpenedFile: 'closeAllOpenedFile',
      toggleSkyDrive: 'toggleSkyDrive',
      resetShowingCol: 'resetShowingCol',
      refreshOpenedFile: 'refreshOpenedFile',
      gitlabRemoveFile: 'gitlab/removeFile',
      userGetSiteLayoutConfig: 'user/getSiteLayoutConfig',
      userDeletePagesConfig: 'user/deletePagesConfig',
      toggleFileHistoryVisibility: 'toggleFileHistoryVisibility',
      toggleAngles: 'toggleAngles',
      addRecentOpenedSiteUrl: 'addRecentOpenedSiteUrl'
    }),
    openZenMode() {
      const dom = document.querySelector('#codeWin')

      if (!dom) {
        return false
      }

      this.resetShowingCol({
        isZenMode: true
      })

      this.$fullscreen.toggle(dom, {
        wrap: false,
        fullscreenClass: 'zenmode',
        callback: state => {
          if (!state) {
            this.resetShowingCol({
              isZenMode: false
            })
            const vscroolbar = dom.querySelector('.CodeMirror-vscrollbar')
            // Is very strange. when I set display none, scroolbar is normally
            vscroolbar.style.display = 'none'
          }
        }
      })
    },
    toggleBoth() {
      this.resetShowingCol({
        isPreviewShow: true,
        isCodeShow: true,
        isManagerShow: true
      })
    },
    toggleCodeWin() {
      this.resetShowingCol({
        isPreviewShow: false,
        isCodeShow: true,
        isManagerShow: true
      })
    },
    togglePreviewWin() {
      this.resetShowingCol({
        isPreviewShow: true,
        isCodeShow: false,
        isManagerShow: true
      })

      // we should improve performance
      // this.isCodeShow &&
      //   this.$store.dispatch('setAddingArea', {
      //     area: this.gConst.ADDING_AREA_ADI
      //   })
    },
    toggleLeftAndRightAngles() {
      if (!this.showAngle) {
        this.toggleAngles({ showAngle: true })
      } else {
        this.toggleAngles({ showAngle: false })
      }
    },
    showFileHistory() {
      this.toggleFileHistoryVisibility({ isVisible: true })
    },
    async save() {
      let self = this

      if (this.isActivePageSaved) {
        return
      }
      if (!this.savePending) {
        this.savePending = true
        await this.saveActivePage()
          .then(() => {
            this.$message({
              showClose: true,
              message: self.$t('editor.saveSuccess'),
              type: 'success'
            })
          })
          .catch(e => {
            console.log(e)
            this.$message({
              showClose: true,
              message: self.$t('editor.saveFail'),
              type: 'error'
            })
          })
        this.savePending = false
      }
    },
    openNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = true
    },
    closeNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = false
    },
    openWebsiteSettingDialog() {
      this.isWebsiteSettingShow = true
    },
    closeWebsiteSettingDialog() {
      this.isWebsiteSettingShow = false
    },
    goSettingPage() {
      this.setActiveManagePaneComponent({
        name: 'PageSetting',
        props: {
          pagePath: this.currentPagePath
        }
      })
    },
    removeCurrentPage(path) {
      let pathArr = path.split('/')
      let siteName = pathArr.slice(1, 2).join()
      let pageName = pathArr.slice(-1).join()
      const h = this.$createElement
      this.$msgbox({
        title: this.$t('editor.modDelMsgTitle'),
        message: h('p', null, [
          h('span', null, `${this.$t('editor.delConfirm')}`),
          h('span', { style: 'color: #FF4342' }, ` "${siteName}/${pageName}" `),
          h('span', null, `${this.$t('editor.page')}?`)
        ]),
        showCancelButton: true,
        confirmButtonText: this.$t('el.messagebox.confirm'),
        cancelButtonText: this.$t('el.messagebox.cancel')
      })
        .then(async () => {
          this.deletePending = true
          await this.gitlabRemoveFile({ path: `${path}.md` }).catch(e => {
            this.$message.error(this.$t('editor.deleteFail'))
            this.deletePending = false
          })
          await this.deletePagesFromLayout({ paths: [path] })
          this.removeRecentOpenFile(path)
          this.resetPage(path)
          this.deletePending = false
        })
        .catch(e => console.error(e))
    },
    async deletePagesFromLayout({ paths = [] }) {
      const re = /^\w+\/\w+\//
      let sitePath = paths[0].match(re)
      if (sitePath) sitePath = sitePath[0].replace(/\/$/, '')
      let pages = _.map(paths, page => page.replace(re, ''))
      await this.userGetSiteLayoutConfig({ path: sitePath })
      let config = this.getSiteLayoutConfigBySitePath(sitePath)
      await this.userDeletePagesConfig({ sitePath, pages })
    },
    removeRecentOpenFile(path) {
      let delPath = `/${path.replace(/\.md$/, '')}`
      let updateRecentUrlList = this.updateRecentUrlList.filter(
        item => item.path !== delPath
      )
      this.addRecentOpenedSiteUrl({ updateRecentUrlList })
    },
    async saveAllOpenedFiles() {
      if (!this.hasUnSaveOpenedFiles) return
      let num = this.unSavedOpenedFilesPaths.length
      let paths = this.unSavedOpenedFilesPaths
      let isSuccess = true
      this.savePending = true
      while (num--) {
        await this.savePageByPath(paths[num]).catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          isSuccess = false
        })
      }
      isSuccess &&
        this.$message({
          message: this.$t('editor.saveSuccess'),
          type: 'success'
        })
      this.savePending = false
    },
    handleCloseOpenedFile() {
      let path = _.get(this.activePageInfo, 'fullPath', '')
      this.closeAndReset(path)
      this.handleCloseDialog()
      this.closeOneFile = false
    },
    async saveAndCloseOpenedFile() {
      let path = this.activePageInfo.fullPath
      this.savePending = true
      await this.savePageByPath(path)
        .then(() => {
          this.closeAndReset(path)
          this.handleCloseDialog()
          this.savePending = false
          this.closeOneFile = false
        })
        .catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          this.handleCloseDialog()
          this.savePending = false
        })
    },
    async closeAllOpenedFilesConfirm() {
      if (this.unSavedOpenedFilesPaths.length > 0) {
        this.dialogVisible = true
        let path = this.unSavedOpenedFilesPaths[0]
        let siteName = path
          .split('/')
          .slice(1, 2)
          .join()
        let fileName = path
          .split('/')
          .slice(-1)
          .join()
          .replace(/\.md$/, '')
        this.toBeCloseFileName = `${siteName}/${fileName}`
        this.toBeCloseFilePath = path
      } else {
        this.$router.push('/')
        this.closeAllOpenedFile()
      }
    },
    handleCloseOpenedFileAndNext() {
      let path = this.toBeCloseFilePath
      path && this.closeAndResetFile(path)
      this.checkHasNext()
    },
    async saveAndCloseOpenedFileAndNext() {
      this.savePending = true
      let path = this.toBeCloseFilePath
      await this.savePageByPath(path)
        .then(() => {
          this.closeAndResetFile(path)
          this.savePending = false
          this.checkHasNext()
        })
        .catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          this.handleCloseAllDialog()
          this.savePending = false
        })
    },
    handleClose() {
      return this.closeOneFile
        ? this.handleCloseOpenedFile()
        : this.handleCloseOpenedFileAndNext()
    },
    saveHandleClose() {
      return this.closeOneFile
        ? this.saveAndCloseOpenedFile()
        : this.saveAndCloseOpenedFileAndNext()
    },
    closeAndResetFile(path) {
      let _path = Object.keys(this.openedFiles).filter(name => name !== path)
      this.closeOpenedFile({ path })
      if (this.$route.path.slice(1) !== path.replace(/\.md$/, '')) return
      if (_path.length === 0) {
        this.$router.push('/')
      } else {
        this.$router.push('/' + _path[0].replace(/\.md$/, ''))
      }
    },
    checkHasNext() {
      if (this.unSavedOpenedFilesPaths.length > 0) {
        this.closeAllOpenedFilesConfirm()
      } else {
        this.closeAllOpenedFile()
        this.dialogVisible = false
        this.$router.push('/')
      }
    },
    doCopyLink() {
      let that = this
      let toCopyLink = this.activePageFullUrl
      this.$copyText(toCopyLink).then(
        function(e) {
          that.$message({
            showClose: true,
            message: that.$t('editor.copySuccess'),
            type: 'success'
          })
        },
        function(e) {
          console.log(e)
          that.$message({
            showClose: true,
            message: that.$t('editor.copyFail'),
            type: 'error'
          })
        }
      )
    },
    handleCloseDialog() {
      this.dialogVisible = false
    },
    async handleCloseConfirm() {
      this.closeOneFile = true
      let path = _.get(this.activePageInfo, 'fullPath', '')
      if (this.isActivePageSaved) {
        this.closeAndReset(path)
      } else {
        this.dialogVisible = true
      }
    },
    closeAndReset(path) {
      let _path = Object.keys(this.openedFiles).filter(name => name !== path)
      this.closeOpenedFile({ path })
      if (this.$route.path.slice(1) !== path.replace(/\.md$/, '')) return
      _path.length === 0
        ? this.$router.push('/')
        : this.$nextTick(() =>
            this.$router.push({ path: `/${_path[0].replace(/\.md$/, '')}` })
          )
    },
    changeView(type) {
      this.setActiveManagePaneComponent(type)
    },
    openSkyDriveManagerDialog() {
      this.toggleSkyDrive({ showSkyDrive: true })
    },
    toggleLanguage,
    backHome() {
      window.location.href = this.nowOrigin
    },
    resetPage(currentPath = null) {
      if (
        currentPath &&
        currentPath.replace(/\.md$/, '') === this.$route.path.substring(1)
      ) {
        return this.$router.push('/')
      }
    }
  },
  components: {
    NewWebsiteDialog,
    WebsiteSettingDialog
  }
}
</script>

<style lang="scss" scoped>
.kp-dropdown-menu {
  padding: 0 0 0 10px;
}
.kp-dropdown-menu:hover {
  background-color: rgba(40, 140, 233, 0.1);
}
.el-menu-item.is-active {
  border-bottom: none;
}
.unsaved-tip {
  display: inline-flex;
  align-items: center;
}
.unsaved-tip span {
  line-height: 1.7em;
  position: relative;
  top: 0.3em;
  border-bottom: 2px solid #f7bc2a !important;
}
.save-btn:not(.is-disabled) .icon-save {
  background: #f7bc2a;
  border-color: #f7bc2a;
  color: white;
}
.el-dropdown-link {
  display: inline-block;
  height: 60px;
}
.kp-logo {
  width: 127px;
}
.el-dropdown-menu__item {
  line-height: 24px;
  padding: 0;
}
.el-dropdown-menu__item:hover {
  color: inherit;
  background-color: inherit;
}

.li-btn {
  padding: 0 8px;
}
.btn {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 1px solid #ddd;
  border-radius: 50%;
}
.pull-right {
  float: right !important;
}
.user-profile-box {
  padding-right: 0;
}
.user-profile {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.input-link-copy-box {
  display: inline-block;
  width: 367px;
  border: 1px solid #dcdfe6;
  height: 40px;
  line-height: 40px;
  border-radius: 4px;
  padding: 0 16px;
}
.input-link-copy-box a {
  color: #288ce9;
  text-decoration: none;
}
.dropdown-btn {
  font-size: 16px;
  padding: 10px;
}
.dropdown-arrow {
  font-size: 12px;
  margin: 0 6px 0 10px;
  width: auto;
  margin-left: 0px;
}
.iconfont {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  border: 1px solid #ddd;
  text-align: center;
  font-size: 21px;
  color: #666;
}
.link-box .iconfont {
  border: none;
}
.link-box a {
  text-decoration: none;
}
.link-box .iconfont:hover,
.link-box a:hover {
  color: #429efd;
}
.switch-box {
  float: right;
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-right: 15px;
  padding-left: 6px;
  padding-right: 6px;
  height: 40px;
  line-height: 40px;
  border-radius: 20px;
  border-bottom: none;
  background-color: #efefef !important;
  .iconfont {
    width: 60px;
    height: 32px;
    line-height: 32px;
    border: none;
  }
  &-active {
    background-color: #1278e1;
    color: #fff;
    border-radius: 16px;
  }
}
</style>
<style lang="scss">
.logo-submenu {
  .el-menu .el-submenu__title,
  a {
    color: #909399;
  }
  a {
    text-decoration: none;
  }
  .el-menu .el-submenu__title:hover,
  a:hover {
    color: #303133;
  }
}
.kp-menu-top {
  display: flex;
  &:hover {
    .kp-icon {
      background-color: rgba(40, 140, 233, 0.1);
      .iconfont {
        color: #409eff;
      }
    }
  }
  &.disabled-bgc:hover {
    .kp-icon {
      background-color: #f5f5f5;
    }
  }
  .kp-icon {
    width: 20px;
    padding: 0 4px 0 20px;
    height: 24px;
    .iconfont {
      border: none;
      line-height: 24px;
      width: 0;
      font-size: inherit;
    }
  }
  .kp-submenu-top-content {
    flex: 1;
    button {
      width: 100%;
      height: 24px;
      border: none;
      background-color: transparent;
      text-align: left;
      color: #909399;
      border-left: 1px solid #ccc;
      margin-top: -1px;
      padding: 0 0 0 10px;
      cursor: pointer;
      &:focus {
        outline: none;
      }
      &:hover {
        background-color: rgba(40, 140, 233, 0.1);
        color: #409eff;
      }
      &[disabled] {
        color: #ccc;
        cursor: default;
        &:hover {
          background-color: #f5f5f5;
        }
      }
    }
  }
}
.isDisabled {
  .iconfont {
    color: #ccc !important;
  }
  &:hover {
    .kp-icon {
      .iconfont {
        color: #ccc !important;
      }
    }
  }
}
.kp-dropdown-menu-content {
  &.el-popper[x-placement^='bottom'] {
    min-width: 164px;
    max-width: 216px;
    left: 40px !important;
  }
  .el-dropdown-menu__item {
    cursor: default;
  }
  .el-dropdown-menu__item--divided:before {
    margin: 0;
  }
}
.kp-menu button {
  display: block;
  width: 100%;
  height: 24px;
  border: none;
  background-color: transparent;
  color: #909399;
  position: relative;
  cursor: pointer;
  text-align: left;
  padding-left: 56px;
  .kp-menu-help {
    display: inline-block;
    width: 100%;
    height: 24px;
    line-height: 24px;
  }
  .iconfont {
    border: none;
    font-size: 14px;
    width: 0;
    height: 0;
    line-height: 24px;
    position: absolute;
    left: 20px;
    top: 0;
  }
  &:hover {
    color: #409eff;
    background-color: rgba(40, 140, 233, 0.1);
    .iconfont {
      color: #409eff;
    }
  }
  &:focus {
    outline: none;
  }
  a {
    text-decoration: none;
    color: inherit;
  }
}
.kp-menu button[disabled] {
  &:hover {
    background-color: #f5f5f5;
  }
  color: #ccc;
  cursor: default;
  .iconfont {
    color: #ccc;
  }
}
.kp-menu {
  .btn-language,
  .btn-angles {
    height: 48px;
    .iconfont {
      line-height: 48px;
    }
  }
}
</style>

<template>
  <div class='kp-md-editor'>
    <codemirror ref='mdEditor' :options='options' :value='code' @changes='updateMarkdown' />
  </div>
</template>

<script>
import _ from 'lodash'
import Parser from '@/lib/mod/parser'
import CmdHelper from '@/lib/mod/parser/cmdHelper'
import BlockHelper from '@/lib/mod/parser/blockHelper'
import waitForMilliSeconds from '@/lib/utils/waitForMilliSeconds'
import { mapGetters, mapActions } from 'vuex'
import { codemirror } from 'vue-codemirror'
import _CodeMirror from 'codemirror'
import Mousetrap from 'mousetrap'
import { gConst } from '@/lib/global'

import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/3024-night.css'
import 'codemirror/mode/markdown/markdown'
import 'codemirror/addon/hint/show-hint.js'
import 'codemirror/addon/hint/show-hint.css'
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldcode.js'
import 'codemirror/addon/fold/foldgutter.js'
import 'codemirror/addon/fold/xml-fold'
import 'codemirror/addon/fold/markdown-fold'
import 'codemirror/addon/lint/json-lint'
import 'codemirror/addon/selection/active-line.js'

const CodeMirror = window.CodeMirror || _CodeMirror

export default {
  name: 'EditorMarkdown',
  data() {
    return {
      gConst,
      qiniuUploadSubscriptions: {},
      preClickedMod: '',
      parserTimer: null,
      parserCache: {}
    }
  },
  components: {
    codemirror
  },
  created() {
    CodeMirror.registerHelper('fold', 'wikiCmdFold', this.wikiCmdFold)
  },
  mounted() {
    this.foldAllCodes(this.editor)
    this.editor.on('drop', this.onDropFile)
    this.editor.on('paste', this.onPaste)
    this.editor.on('mousedown', this.handleClick)
    this.enableParserTick()
  },
  beforeDestroy() {
    this.disableParserTick()
  },
  watch: {
    activeMod(newActiveMod, oldActiveMod) {
      newActiveMod && this.highlightCodeByMod(newActiveMod)
    },
    cursorPos(newCursor, oldCursor) {
      newCursor &&
        this.$nextTick(() => {
          this.editor.setCursor(CodeMirror.Pos(newCursor.line, newCursor.ch))
        })
    },
    activePage(page) {
      this.preClickedMod = ''
    },
    isZenMode(state) {
      if (state) {
        this.editor.setOption('theme', '3024-night')
      } else {
        this.editor.setOption('theme', 'default')
      }
    }
  },
  computed: {
    ...mapGetters({
      activePageInfo: 'activePageInfo',
      activePage: 'activePage',
      code: 'code',
      modList: 'modList',
      activeMod: 'activeMod',
      cursorPos: 'cursorPos',
      isZenMode: 'isZenMode'
    }),
    options() {
      const save = () => Mousetrap.trigger('mod+s')
      const undo = () => Mousetrap.trigger('mod+z')
      const redo = () => Mousetrap.trigger('mod+y')

      const newTab = cm => {
        if (cm.somethingSelected()) {
          cm.indentSelection('add')
        } else {
          const str = cm.getOption()
            ? '\t'
            : Array(cm.getOption('indentUnit') + 1).join(' ')
          cm.replaceSelection(str, 'end', '+input')
        }
      }
      return {
        mode: 'markdown',
        theme: 'default',
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        tabSize: 2,
        indentWithTabs: false,
        styleActiveLine: true,
        foldGutter: true,
        foldOptions: {
          rangeFinder: new CodeMirror.fold.combine(CodeMirror.fold.wikiCmdFold),
          clearOnEnter: false
        },
        gutters: [
          'CodeMirror-linenumbers',
          'CodeMirror-foldgutter',
          'CodeMirror-lint-markers'
        ],
        matchBrackets: true,
        undoDepth: 0,
        dragDrop: true,
        allowDropFileTypes: ['jpg', 'jpeg'], // codemirror will automatically parse the dropped file and insert the content into editing area, eg: js, svg, xml...
        extraKeys: {
          'Ctrl-S': save,
          'Cmd-S': save,
          'Ctrl-Z': undo,
          'Cmd-Z': undo,
          'Ctrl-Y': redo,
          'Cmd-Y': redo,
          'Ctrl-Space': 'autocomplete',
          'Cmd-Space': 'autocomplete',
          Tab: newTab
        }
      }
    },
    editor() {
      return this.$refs.mdEditor.codemirror
    },
    activeCursorLine() {
      const cursor = this.editor.getCursor()
      return cursor.line || this.editor.lastLine()
      // return cursor.sticky ? cursor.line : this.editor.lastLine()
    }
  },
  methods: {
    ...mapActions({
      gitlabUploadFile: 'gitlab/uploadFile',
      userUploadFileAndUseInSite: 'user/uploadFileAndUseInSite',
      setActiveMod: 'setActiveMod'
    }),
    updateActiveCursor() {
      this.$store.dispatch('setAddingArea', {
        area: gConst.ADDING_AREA_MARKDOWN,
        cursorPosition: this.activeCursorLine
      })
    },
    addMod() {
      this.updateActiveCursor()
      this.$store.dispatch('setActiveManagePaneComponent', 'ModsList') // TODO: move wintype defination to gConst
    },
    highlightCodeByMod(mod) {
      if (mod.modType === 'ModMarkdown') return this.clearHighlight()
      let lineBegin = mod.lineBegin - 1
      let lineEnd = BlockHelper.endLine(mod)
      this.clearHighlight()
      this.editor.addLineClass(lineBegin, 'background', 'mark-text')
      this.editor.addLineClass(lineEnd - 1, 'background', 'mark-text')
    },
    clearHighlight() {
      let lineCount = this.editor.lineCount()
      while(lineCount--) {
          this.editor.removeLineClass(lineCount, 'background', 'mark-text')
      }
    },
    handleClick(codeMirror) {
      this.$nextTick(() => {
        let line = codeMirror.getCursor().line
        let mod = Parser.getBlockByCursorLine(this.modList || [], line + 1)
        if (mod && this.activeMod && mod.key === this.activeMod.key) return
        if (mod) {
          // this.highlightCodeByMod(mod)
          let currentActiveModKey = this.activeMod && this.activeMod.key
          if (mod.key !== currentActiveModKey) this.setActiveMod(mod.key)
          if (mod.cmd === 'Markdown') {
            this.$store.dispatch('setActiveManagePaneComponent', 'FileManager')
          }
          this.preClickedMod = mod.cmd
        }
      })
    },
    checkIfInComposing(change) {
      // see https://codemirror.net/doc/manual.html#selection_origin
      // When it starts with *, it will always replace the previous event (if that had the same origin)
      return (
        change.origin &&
        change.origin[0] === '*' &&
        change.removed &&
        change.removed[0] === ''
      )
    },
    enableParserTick() {
      this.parserTimer = setInterval(() => {
        this.flushParserCache()
      }, 1000)
    },
    disableParserTick() {
      if (this.parserTimer) window.clearTimeout(this.parserTimer)
    },
    flushParserCache() {
      if (
        this.parserCache.code !== undefined &&
        this.parserCache.code !== this.code
      ) {
        return this.$store.dispatch('updateMarkDown', this.parserCache)
      }
    },
    updateMarkdown() {
      let code = this.editor.getValue()
      let cursor = this.editor.getCursor()
      this.parserCache.code = code
      this.parserCache.cursor = cursor
      if (code === undefined) return
      if (code === this.code) {
        // update by ADI
        this.foldAllCodes(this.editor)
      }
    },
    foldAllCodes(cm = this.editor) {
      for (let l = cm.firstLine(); l <= cm.lastLine(); ++l) {
        cm.foldCode({ line: l, ch: 0 }, null, 'fold')
      }
    },
    wikiCmdFold(cm, start) {
      let line = cm.getLine(start.line)
      if (!line || !CmdHelper.isCmdLine(line)) return
      let end = start.line + 1
      let lastLineNo = cm.lastLine()
      while (end < lastLineNo) {
        line = cm.getLine(end)
        if (line) {
          if (CmdHelper.isCmdEnd(line)) break
          else if (CmdHelper.isCmdLine(line)) {
            end--
            break
          }
        }
        end++
      }
      return {
        from: CodeMirror.Pos(start.line),
        to: CodeMirror.Pos(end, cm.getLine(end).length)
      }
    },
    setFontStyle(style) {
      let wrapper = ''
      if (style === 'bold') wrapper = '**'
      else if (style === 'italic') wrapper = '*'

      if (this.editor.somethingSelected()) {
        let selection = this.editor.getSelection()
        let replaceStr =
          wrapper + selection.replace(/\n/g, wrapper + '\n' + wrapper) + wrapper
        this.editor.replaceSelection(replaceStr)
      }
    },
    insertHeadline(level) {
      let preChar = ''
      while (level > 0) {
        preChar += '#'
        level--
      }
      preChar += ' '

      let cursor = this.editor.getCursor()
      let content = this.editor.getLine(cursor.line)

      let iSpace = 0
      let chrCmp = ''
      for (let i = 0; i < content.length; i++) {
        chrCmp = content.substr(i, 1)
        if (chrCmp === '#') {
          continue
        } else {
          if (chrCmp === ' ') {
            iSpace = i + 1
          }
          break
        }
      }
      this.editor.replaceRange(
        preChar,
        CodeMirror.Pos(cursor.line, 0),
        CodeMirror.Pos(cursor.line, iSpace)
      )
      this.editor.focus()
    },
    insertCode() {
      let selection = this.editor.getSelection()
      let replaceStr = '```\n' + selection + '\n```'
      this.editor.replaceSelection(replaceStr)

      let cursor = this.editor.getCursor()
      this.editor.setCursor(CodeMirror.Pos(cursor.line - 1, cursor.ch))
      this.editor.focus()
    },
    insertLine() {
      let cursor = this.editor.getCursor()
      this.addNewLine(cursor.line, '---')
      this.editor.setCursor(CodeMirror.Pos(cursor.line + 2, 0))
      this.editor.focus()
    },
    insertLink(txt, url, coords) {
      let replaceStr = ''
      if (txt) {
        replaceStr += '[' + txt + ']'
      } else if (!coords && this.editor.somethingSelected()) {
        replaceStr += '[' + this.editor.getSelection() + ']'
      } else {
        replaceStr += '[]'
      }

      let cursorLineNo = coords ? coords.line : this.editor.getCursor().line
      let lineContent = this.editor.getLine(cursorLineNo)
      replaceStr += url ? `(${url})` : '()'
      replaceStr = lineContent ? '\n' + replaceStr : replaceStr
      coords
        ? this.editor.replaceRange(replaceStr, coords)
        : this.editor.replaceSelection(replaceStr)
      this.editor.focus()
    },
    insertFile(txt, url, coords) {
      let replaceStr = ''
      if (txt) {
        replaceStr += '![' + txt + ']'
      } else if (!coords && this.editor.somethingSelected()) {
        replaceStr += '![' + this.editor.getSelection() + ']'
      } else {
        replaceStr += '![]'
      }

      let cursorLineNo = coords ? coords.line : this.editor.getCursor().line
      let lineContent = this.editor.getLine(cursorLineNo)
      replaceStr += url ? `(${url})` : '()'
      replaceStr = lineContent ? '\n' + replaceStr : replaceStr
      coords
        ? this.editor.replaceRange(replaceStr, coords)
        : this.editor.replaceSelection(replaceStr)
      this.editor.focus()
    },
    addNewLine(lineNo, content) {
      // add new line after line {lineNo}
      if (!lineNo) lineNo = this.editor.getCursor().line
      let replaceStr = content ? `${content}\n` : '\n'
      this.editor.replaceRange(
        replaceStr,
        CodeMirror.Pos(lineNo + 1, 0),
        CodeMirror.Pos(lineNo + 1, 0)
      )
      return lineNo + 1
    },
    getEmptyLine(lineNo) {
      let content = this.editor.getLine(lineNo)
      while (content) {
        content = this.editor.getLine(++lineNo)
      }
      if (undefined === content) {
        this.editor.replaceRange('\n', { line: lineNo, ch: 0 })
      }
    },
    replaceLine(lineNo, content) {
      const originalContent = this.editor.getLine(lineNo)
      const offsetX = originalContent && originalContent.length
      this.editor.replaceRange(
        content,
        CodeMirror.Pos(lineNo, 0),
        CodeMirror.Pos(lineNo, offsetX)
      )
    },
    async uploadFile(file, coords) {
      let lineNo = coords ? coords.line : this.editor.getCursor().line
      let originText = this.editor.getLine(lineNo)
      if (originText) {
        this.replaceLine(
          lineNo,
          originText + '\n' + this.$t('editor.readFileFromLocal')
        )
        lineNo++
      } else {
        this.replaceLine(lineNo, this.$t('editor.readFileFromLocal'))
      }
      let filename = `${file.name}`

      await this.userUploadFileAndUseInSite({
        file,
        filename,
        sitePath: this.activePageInfo.sitepath,
        onStart: subscirbtion => {
          this.replaceLine(lineNo, this.$t('editor.uploadingToSkyDriveText'))
          this.qiniuUploadSubscriptions[file.name] = subscirbtion
        },
        onProgress: progress => {
          this.replaceLine(lineNo, this.$t('editor.uploadingToSkyDriveText'))
        }
      })
        .then(({ file, url }) => {
          this.replaceLine(lineNo, ' ')
          this.updateMarkdown()
          this.flushParserCache()
          this.$emit('insertBigfile', { file, url: `${url}#${file.filename}` })
        })
        .catch(err => {
          console.error(err)
          this.replaceLine(lineNo, '')
          this.insertLink(null, '***Upload Failed!***', coords)
        })
    },
    onDropFile(cm, evt) {
      let files = evt.dataTransfer.files
      const coords = cm.coordsChar({ left: evt.x, top: evt.y })
      _.forEach(files, file => {
        this.uploadFile(file, coords)
      })
      return false
    },
    onPaste(cm, evt) {
      if (evt.clipboardData && evt.clipboardData.files.length > 0) {
        let files = evt.clipboardData.files
        _.forEach(files, file => {
          this.uploadFile(file)
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.kp-md-editor {
  flex: 1;
  overflow: auto;
}
.vue-codemirror {
  background-color: #ffffff;
  height: 100%;
}
</style>
<style lang="css">
.kp-md-editor .CodeMirror {
  margin: 0 auto;
  height: 100%;
}
.kp-md-editor .CodeMirror-gutters {
  background-color: transparent;
  border: none;
}
.mark-text {
  background-color: #cdd4db;
  /* border-right: 4px solid #ffac36; */
}
.mark-bg {
  background: #ffe193;
}
</style>

<template>
  <div :class="{'mod-wrap':true,'mod-active': isActive, }">
    <div :class="['kp-mod-selector',mod.cmd === 'Markdown' ? 'no-mask' : '']" @click='setActive'>
      <div class="delete-mod" @click.stop.prevent='toDeleteMod'>
        <i class="iconfont icon-delete icon-del"></i>
      </div>
      <div class='mod'>
        <component :is='modComponent' :rootMod='mod' :mod='mod' :conf='modConf' :theme='theme' :editMode='true' :active='isActive'></component>
        <span v-if='invalid'>{{$t('editor.wrongModDirective')}}</span>
      </div>
      <div class='operator' v-if='isActive'>
        <el-tooltip :content="$t('editor.addModHere')">
          <el-button class="add-mod-btn add-before" @click.stop.prevent='newMod(gConst.POSITION_BEFORE)'> + </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('editor.addModHere')">
          <el-button class="add-mod-btn add-after" @click.stop.prevent='newMod(gConst.POSITION_AFTER)'> + </el-button>
        </el-tooltip>
      </div>
    </div>
    <quick-to-top></quick-to-top>
  </div>
</template>

<script>
import ModLoader from '@/components/adi/mod'
import VueScrollTo from 'vue-scrollto'
import { mapGetters, mapActions } from 'vuex'
import { gConst } from '@/lib/global'
import QuickToTop from '@/components/common/QuickToTop'

export default {
  props: {
    mod: Object,
    theme: Object
  },
  data() {
    return {
      gConst
    }
  },
  watch: {
    isActive(newVal) {
      if (newVal) this.scrollToCurrentMod()
    }
  },
  computed: {
    ...mapGetters({
      activeMod: 'activeMod',
      modList: 'modList'
    }),
    modComponent() {
      if (this.modConf) return this.modConf.mod
    },
    modConf() {
      return ModLoader.load(this.mod.modType)
    },
    isActive() {
      return this.activeMod && this.mod.key === this.activeMod.key
    },
    invalid() {
      return !this.modConf
    }
  },
  methods: {
    ...mapActions({
      deleteMod: 'deleteMod',
      setPreMod: 'setPreMod',
      setNewModPosition: 'setNewModPosition',
      toggleIframeDialog: 'toggleIframeDialog'
    }),
    newMod(position) {
      this.$store.dispatch('setNewModPosition', position)
      this.$emit('onAddMod', this.mod.key)
    },
    setActive() {
      this.$store.dispatch('setActiveMod', this.mod.key)
    },
    scrollToCurrentMod() {
      const options = {
        easing: 'ease-in',
        offset: -30,
        x: false,
        y: true
      }
      VueScrollTo.scrollTo(this.$el, 500, options)
    },
    getPreMod() {
      let modList = this.modList
      let index = modList.findIndex(i => i.key === this.mod.key)
      return index ? modList[index - 1] : modList[index || 0]
    },
    toDeleteMod() {
      let preMod = this.getPreMod()
      if (preMod) {
        this.setPreMod(preMod)
        this.setNewModPosition(gConst.POSITION_AFTER)
      }
      let data = {
        show: true,
        title: this.$t('editor.modDelMsgTitle'),
        message: this.$t('editor.modDelMsg'),
        action: 'deleteMod',
        payload: this.mod.key
      }
      this.toggleIframeDialog(data)
    }
  },
  components: {
    QuickToTop
  }
}
</script>

<style scoped>
.add-mod-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  color: #fff;
  text-align: center;
  padding: 0;
  font-size: 30px;
  border: none;
  position: absolute;
  left: 50%;
  margin-left: -19px;
  z-index: 99;
}
.add-before {
  top: -19px;
}
.add-after {
  bottom: -19px;
}
.add-mod-btn:hover {
  color: #fff;
  font-size: 38px;
  transition: all 0.2s;
}
</style>

<style lang="scss">
.mod-wrap {
  border: 2px solid transparent;
  &:hover {
    border: 2px dashed #3ab4ff;
  }
}
.mod-active {
  border: 2px dashed #f7a935;
  position: relative;
  .add-mod-btn {
    background-color: #f7a935;
  }
  &:hover {
    border: 2px dashed #f7a935;
  }
}
.kp-mod-selector .comp {
  position: relative;
}
.kp-mod-selector {
  position: relative;
  .delete-mod {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    line-height: 24px;
    text-align: center;
    background-color: #f56c6c;
    color: #ffffff;
    border-radius: 50%;
    z-index: 99;
    display: none;
    cursor: pointer;
    .icon-delete:hover {
      font-size: 20px;
      transition: all 0.1s;
    }
  }
  &:hover {
    .delete-mod {
      display: inline;
    }
  }
}
.kp-mod-selector .comp:hover {
  background-color: rgba(127, 195, 255, 0.4);
  cursor: pointer;
}
.kp-mod-selector .comp-proptype-hover::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(127, 195, 255, 0.4);
  cursor: pointer;
}
.kp-mod-selector.no-mask .comp:hover {
  background-color: transparent;
  cursor: pointer;
}
.el-tooltip__popper {
  font-size: 14px;
}
</style>

<template>
  <div class='viewport-container' v-if='layout'>
    <component :is='layoutTemplate'>
      <editor-viewport-partial v-if='headerModList' slot='header' :modList='headerModList' :theme='theme' :area='HEADER_AREA' />
      <editor-viewport-partial v-if='footerModList' slot='footer' :modList='footerModList' :theme='theme' :area='FOOTER_AREA' />
      <editor-viewport-partial v-if='sidebarModList' slot='sidebar' :modList='sidebarModList' :theme='theme' :area='SIDEBAR_AREA' />
      <editor-viewport-partial :modList='mainModList' :theme='theme' :area='MAIN_AREA' />
    </component>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import {
  MAIN_AREA,
  HEADER_AREA,
  FOOTER_AREA,
  SIDEBAR_AREA
} from '@/lib/mod/layout/const'
import EditorViewportPartial from './EditorViewportPartial'
import layoutTemplates from '@/components/adi/layout/templates'
import themeFactory from '@/lib/theme/theme.factory'

export default {
  name: 'EditorViewport',
  data() {
    return {
      MAIN_AREA,
      HEADER_AREA,
      FOOTER_AREA,
      SIDEBAR_AREA
    }
  },
  components: {
    EditorViewportPartial
  },
  computed: {
    ...mapGetters({
      layout: 'layout',
      mainModList: 'mainModList',
      headerModList: 'headerModList',
      footerModList: 'footerModList',
      sidebarModList: 'sidebarModList',
      themeConf: 'themeConf',
      activeArea: 'activeArea'
    }),
    theme() {
      let newTheme = themeFactory.generate(this.themeConf)
      if (this.storedTheme === newTheme) return this.storedTheme
      if (this.storedTheme) this.storedTheme.sheet.detach()
      this.storedTheme = newTheme
      this.storedTheme.sheet.attach()
      return this.storedTheme
    },
    layoutTemplate() {
      return layoutTemplates[this.layout.styleName]['component']
    }
  },
  methods: {
    openModSelector(key) {
      this.$store.dispatch('setActiveManagePaneComponent', 'ModsList')
    },
    changeDraggableList(evt) {
      if (evt.moved) {
        this.$store.dispatch('moveMod', {
          oldIndex: evt.moved.oldIndex,
          newIndex: evt.moved.newIndex
        })
      }
    }
  }
}
</script>
<style scoped>
.viewport-container {
  flex: 1;
  background-color: #fff;
  overflow-x: hidden;
  overflow-y: auto;
}
.add-btn-row {
  text-align: center;
  padding-top: 43px;
  cursor: pointer;
}
.add-mod-btn {
  width: 66px;
  height: 66px;
  background-color: #3ba4ff;
  color: #fff;
  padding: 0;
  font-size: 40px;
}
.info {
  font-size: 25px;
  color: #c0c4cc;
  margin-top: 13px;
}
</style>

<template>
  <div class='viewport-partial' :class='activeClass'>
    <div class='mask' v-if='unActive' @click='setActiveArea' :title="$t('editor.edit')">
    </div>
    <div class="add-btn-row" @click='openModSelector' v-show='modList.length <= 0'>
      <el-button class='add-mod-btn' type='primary' circle icon='el-icon-plus'></el-button>
      <p class="info">{{$t('editor.addMod')}}</p>
    </div>
    <draggable v-model='modDraggableList' @change="changeDraggableList">
      <template v-for='mod in modList'>
        <editor-mod-selector :key='mod.uuid' :mod='mod' :theme='theme' @onAddMod='openModSelector'></editor-mod-selector>
      </template>
    </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import { mapGetters, mapActions } from 'vuex'
import EditorModSelector from './EditorModSelector'
import themeFactory from '@/lib/theme/theme.factory'

export default {
  name: 'EditorViewportPartial',
  props: {
    theme: Object,
    modList: Array,
    isActive: Boolean,
    area: String
  },
  components: {
    EditorModSelector,
    draggable
  },
  computed: {
    ...mapGetters({
      activeArea: 'activeArea'
    }),
    modDraggableList: {
      get() {
        return this.modList
      },
      set(value) {
        // do nothing
      }
    },
    unActive() {
      return this.activeArea !== this.area
    },
    activeClass() {
      if (this.activeArea === this.area) return 'active'
    }
  },
  methods: {
    openModSelector(key) {
      this.$store.dispatch('setActiveManagePaneComponent', 'ModsList')
    },
    changeDraggableList(evt) {
      if (evt.moved) {
        this.$store.dispatch('moveMod', {
          oldIndex: evt.moved.oldIndex,
          newIndex: evt.moved.newIndex
        })
      }
    },
    setActiveArea() {
      this.$store.dispatch('setActiveArea', this.area)
    }
  }
}
</script>

<style lang="scss"  scoped>
.viewport-partial {
  background-color: #fff;
  overflow-x: hidden;
  overflow-y: auto;
  position: relative;
  &.active {
    padding: 20px 0;
  }
}
.add-btn-row {
  text-align: center;
  padding-top: 43px;
  cursor: pointer;
}
.add-mod-btn {
  width: 66px;
  height: 66px;
  background-color: #3ba4ff;
  color: #fff;
  padding: 0;
  font-size: 40px;
}
.info {
  font-size: 25px;
  color: #c0c4cc;
  margin-top: 13px;
}
.mask {
  z-index: 99999;
  cursor: pointer;
  background-color: rgba(0, 0, 0, .2);
  -moz-opacity: 0.5;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  &:hover {
    background-color: rgba(0, 0, 0, .35);
  }
}
</style>

<template>
  <div class="guid-content">
    <h1 class="welcomeText">{{ $t('common.welcomeToKeepwork') }}</h1>
    <div>
      <div class="welcomeButton" @click="openNewWebsiteDialog">
        {{ $t('common.createNewWebsite') }}
        <i class="iconfont icon-next"></i>
      </div>
    </div>
    <div class="historical-records">
      <div class="historical-records-text" @click="handleOpenedClick(item)" v-for="item in openedTreeData" :key="item">{{dataPrefix + item}}</div>
    </div>
    <div class="historical-hr"></div>
    <div class="tips-text">{{getText()}}</div>
    <div class="tips-img">
      <img :src='getImg()'>
    </div>
    <i class="iconfont icon-next changeButton-next" @click="hintTransformation"></i>
    <new-website-dialog :show='isNewWebsiteDialogShow' @close='closeNewWebsiteDialog'></new-website-dialog>
    <div style="height: 100px;"></div>
  </div>
</template>

<script>
import NewWebsiteDialog from '@/components/common/NewWebsiteDialog'
import { mapGetters } from 'vuex'
import axios from 'axios'
import { mdToJson, jsonToMd } from '@/lib/mod/parser/mdParser/yaml'

export default {
  name: 'EditorWelcome',
  data() {
    return {
      isNewWebsiteDialogShow: false,
      tips: new Array(),
      tipsNumber: Number,
    }
  },
  methods: {
    openNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = true
    },
    closeNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = false
    },
    gotoPath(path) {
      this.$router.push(path)
    },
    hintTransformation(){
      let numberRepeatedJudgment = () => {
        let repeatedNumber = Math.floor(Math.random()*this.tips.length)
        if(repeatedNumber != this.tipsNumber) {
          this.tipsNumber = repeatedNumber
        } else {
          numberRepeatedJudgment()
        }
      }
      numberRepeatedJudgment()
    },
    getText(){
      if(this.tips[this.tipsNumber] && this.tips[this.tipsNumber].text){
        return this.tips[this.tipsNumber].text
      }
    },
    getImg(){
      if(this.tips[this.tipsNumber] && this.tips[this.tipsNumber].img){
        return this.tips[this.tipsNumber].img
      }
    },
    handleOpenedClick(index){
      if(!index){
        return false
      }
      this.$router.push(index)
    }
  },
  computed:{
    ...mapGetters({
      recentOpenedList: 'recentOpenedList',
      showOpenedFiles: 'showOpenedFiles',
    }),
    openedTreeData() {
      let clonedopenedFiles = _.clone(this.showOpenedFiles)
      let treeDatas = []
      let that = this
      _.forOwn(clonedopenedFiles, function(value, key) {
        if(typeof key != 'string'){
          return false
        }
        let pathArr = key.split('/')
        let pathLen = pathArr.length
        let pageName = pathArr[pathLen - 1].replace(/.md$/, '')
        let userName = pathArr[0]
        let siteName = pathArr[1]
        let nodeData = `/${userName}/${siteName}/${pageName}`
        treeDatas.push(nodeData)
      })
      return treeDatas
    },
    dataPrefix() {
      return location.origin
    },
    tipsData(){
      if(!process.env.EDITOR_WELCOME){
        return false
      }
      axios.get(process.env.EDITOR_WELCOME)
      .then((response) => {
        if(!response || !response.data || typeof (response.data.content) != 'string'){
          return false
        }
        this.tips = mdToJson(response.data.content)
        if(!Array.isArray(this.tips)){
          return false
        }
        this.tipsNumber = Math.floor(Math.random()*this.tips.length)
      })
      .catch((error) => {
        this.tips = []
      });
    }
  },
  created(){
    this.tipsData
  },
  components: {
    NewWebsiteDialog
  }
}
</script>
<style lang="scss" scoped>
.guid-content{
  .welcomeText{
    color: #000;
    font-size: 46px;
  }
  div{
    .welcomeButton {
      border-radius: 5px;
      letter-spacing: 4px;
      color: #fff;
      font-size: 18px;
      text-align: center;
      padding: 10px;
      background-color: #48a3ff;
      width: 180px;
      height: 20px;
      line-height: 21px;
      cursor:pointer;
    }
    .icon-next {
      float: right;
      color: #fff;
      font-size: 16px;
    }
  }
  .historical-hr {
    width: 439px;
    height: 1px;
    border-bottom: 1px dashed #ebebeb;
  }
  .recordsWeb{
    border-left: 2px solid #dc75cd;
    margin: 40px 0;
    ul
    {
      margin: 0;
      padding: 0 22px;
       li{
      list-style: none;
      margin: 8px 0;
      a{
        text-decoration: none;
        color:#535353;
      }
    }
    }
  }
  .tips-text{
    padding-top: 20px;
    font-size: 16px;
    padding-bottom: 10px;
    font-weight: 600;
    color: #777;
    max-width: 306px;
    white-space: normal;
  }
  .tips-img{
    width: 300px;
    height: 150px;
    border: 3px solid #ebebeb;
    img{
      width: 100%;
      height: 100%;
      object-fit:cover;
    }
  }
  .changeButton-next {
    width: 14px;
    height: 14px;
    font-size: 18px;
    color: #fff;
    display: block;
    line-height: 17px;
    padding: 6px;
    background-color: #a6a09e;
    border-radius: 50%;
    opacity:0.8;
    margin-top: -35px;
    margin-left: 270px;
    cursor:pointer;
  }
  .changeButton-next:hover {
    background-color: #48a3ff;
  }
  .historical-records {
    margin-top: 20px;
    margin-bottom: 15px;
    height: 150px;
    overflow-y:auto;
    .historical-records-text {
      font-size: 14px;
      display: block;
      color: #48a3ff;
      cursor:pointer;
      width: 350px;
    }
  }
}
@media only screen and (max-width: 1366px){
  .guid-content{
    .tips-text{
      font-size: 14px;
      max-width: 206px;
    }
    .tips-img{
      width: 200px;
      height: 100px;
      img{
        width: 100%;
        height: 100%;
      }
    }
    .changeButton-next {
      width: 13px;
      height: 13px;
      font-size: 12px;
      color: #fff;
      display: block;
      line-height: 15px;
      padding: 2px;
      margin-top: -25px;
      margin-left: 180px;
    }
  }
}
</style>

<template>
  <div class="file-history">
    <div class="file-history-sidebar">
      <div class="file-history-sidebar-header">
        <i class="iconfont icon-historyrecord"></i>
        <span class="file-history-sidebar-header-title">{{$t('common.oldVersions')}}</span>
        <el-tooltip :content="$t('editor.recoverThisVersion')">
          <i class="iconfont icon-ziyuan1" @click="recoverVersion"></i>
        </el-tooltip>
      </div>
      <history-list @selectHistory="getFileContentByCommitId"></history-list>
    </div>
    <div class="file-history-main" v-loading="isLoading">
      <div class="file-history-header">
        <span class="file-history-header-version">{{activeVersion}}</span>
        <div class="file-history-main-operations">
          <div class='file-history-header-switch'>
            <el-tooltip :content="$t('tips.ShowPreviewOnly')">
              <span class="iconfont icon-preview1" :class='{"file-history-header-switch-active": isPreviewShow && !isCodeShow}' @click="switchViewShow(true, false)"></span>
            </el-tooltip>
            <el-tooltip :content="$t('tips.ShowBoth')">
              <span class="iconfont icon-both" :class='{"file-history-header-switch-active": isPreviewShow && isCodeShow}' @click="switchViewShow(true, true)"></span>
            </el-tooltip>
            <el-tooltip :content="$t('tips.ShowCodeOnly')">
              <span class="iconfont icon-code1" :class='{"file-history-header-switch-active": !isPreviewShow && isCodeShow}' @click="switchViewShow(false, true)"></span>
            </el-tooltip>
          </div>
          <el-tooltip :content="$t('editor.close')">
            <i class="iconfont icon-ziyuan3" @click="closeHistory"></i>
          </el-tooltip>
        </div>
      </div>
      <div class="file-history-main-col-between" v-if="isPreviewShow"></div>
      <div class="file-history-main-preview" v-if="isPreviewShow">
        <md-viewer :content="activeCommitIdContent"></md-viewer>
      </div>
      <div class="file-history-main-col-between" v-if="isCodeShow"></div>
      <div class="file-history-main-raw" v-if="isCodeShow">
        <codemirror ref='mdEditor' :options='options' :value='activeCommitIdContent' />
      </div>
    </div>
  </div>
</template>
<script>
import MdViewer from '@/components/viewer/MdViewer'
import HistoryList from './HistoryList'
import { codemirror } from 'vue-codemirror'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'FileHistory',
  data() {
    return {
      isLoading: false,
      activeCommitId: undefined,
      activeVersion: undefined,
      isPreviewShow: true,
      isCodeShow: true,
      options: {
        readOnly: 'nocursor',
        mode: 'markdown',
        theme: 'default',
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        tabSize: 2,
        indentWithTabs: false,
        styleActiveLine: true,
        foldGutter: true,
        matchBrackets: true
      }
    }
  },
  computed: {
    ...mapGetters({
      activePageInfo: 'activePageInfo',
      getFileCommitContent: 'gitlab/getFileCommitContent'
    }),
    activeBarePath() {
      return _.get(this.activePageInfo, 'barePath')
    },
    activeFullPath() {
      return _.get(this.activePageInfo, 'fullPath')
    },
    activeCommitIdContent() {
      return this.getFileCommitContent({
        path: this.activeBarePath,
        commitId: this.activeCommitId
      })
    }
  },
  methods: {
    ...mapActions({
      closeOpenedFile: 'closeOpenedFile',
      gitlabReadFileForOwnerWithCommitId: 'gitlab/readFileForOwnerWithCommitId',
      gitlabSaveFile: 'gitlab/saveFile',
      toggleFileHistoryVisibility: 'toggleFileHistoryVisibility'
    }),
    switchViewShow(isPreviewShow, isCodeShow) {
      this.isPreviewShow = isPreviewShow
      this.isCodeShow = isCodeShow
    },
    closeHistory() {
      this.toggleFileHistoryVisibility({ isVisible: false })
    },
    async getFileContentByCommitId({ commitId, version }) {
      this.activeCommitId = commitId
      this.activeVersion = version
      this.isLoading = true
      await this.gitlabReadFileForOwnerWithCommitId({
        path: this.activeFullPath,
        barePath: this.activeBarePath,
        commitId
      }).catch()
      this.isLoading = false
    },
    async recoverVersion() {
      this.isLoading = true
      await this.gitlabSaveFile({
        path: this.activeFullPath,
        content: this.activeCommitIdContent,
        source_version: this.activeVersion
      })
        .then(async () => {
          this.closeOpenedFile({ path: this.activeFullPath })
          window.location.reload()
        })
        .catch()
      this.isLoading = false
      this.closeHistory()
    }
  },
  components: {
    HistoryList,
    MdViewer,
    codemirror
  }
}
</script>
<style lang="scss">
.file-history {
  display: flex;
  &-sidebar {
    width: 318px;
    position: relative;
    padding-top: 60px;
    &-header {
      height: 59px;
      line-height: 59px;
      border-bottom: 1px solid #eaecef;
      padding: 0 20px;
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      display: flex;
      &-title {
        flex: 1;
      }
      .icon-ziyuan1 {
        font-size: 20px;
        vertical-align: middle;
        cursor: pointer;
        &:hover {
          color: #288ce9;
        }
      }
    }
  }
  &-main {
    min-width: 0;
    flex: 1;
    display: flex;
    position: relative;
    padding-top: 72px;
    background-color: #cdd4db;
    &-col-between {
      width: 15px;
      background-color: #cdd4db;
    }
    &-preview,
    &-raw {
      flex: 1;
      background-color: #fff;
      min-width: 0;
      overflow: auto;
    }
    .iconfont {
      cursor: pointer;
    }
    .vue-codemirror,
    .CodeMirror-wrap {
      height: 100%;
    }
  }
  &-header {
    padding: 0 18px;
    background-color: #fff;
    height: 60px;
    line-height: 60px;
    position: absolute;
    top: 0;
    left: 15px;
    right: 0;
    display: flex;
    &-version {
      flex: 1;
    }
    &-switch {
      display: inline-flex;
      align-items: center;
      margin: 0 16px;
      height: 40px;
      line-height: 40px;
      border-radius: 20px;
      border-bottom: none;
      background-color: #efefef;
      .iconfont {
        width: 60px;
        height: 32px;
        line-height: 32px;
        text-align: center;
      }
      &-active {
        background-color: #1278e1;
        color: #fff;
        border-radius: 16px;
      }
    }
    .icon-ziyuan3 {
      &:hover {
        color: #288ce9;
      }
    }
  }
}
</style>

<template>
  <div class="file-manager">
    <div v-show="hasOpenedFiles" class="opened-tree tree-item" :class="{'is-active': trees.isOpenedShow}" v-loading="savePending">
      <div class="opened-files-container">
        <h1 class="toggle-bar" @click='toggleContent("isOpenedShow")'>
          <i class="el-icon-arrow-right"></i> {{ $t('editor.openedFiles') }}
        </h1>
        <span class="opened-files-buttons" v-show="trees.isOpenedShow && hasOpenedFiles">
          <el-tooltip :content="$t('editor.saveAll')">
            <el-button class="iconfont icon-save" size="mini" type="text" @click.stop='saveAllOpenedFiles'></el-button>
          </el-tooltip>
          <el-tooltip :content="$t('editor.closeAll')">
            <el-button class="iconfont icon-delete____" size="mini" type="text" @click.stop='closeAllOpenedFilesConfirm'></el-button>
          </el-tooltip>
        </span>
      </div>
      <div @click.stop class="close-dialog">
        <el-dialog center :visible.sync="dialogCloseAllVisible" width="360px" closed="handleCloseAllDialog">
          <div class="dialog-content">{{`"${toBeCloseFileName}" ${this.$t("editor.fileUnSaved")}`}}</div>
          <div slot="footer" class="dialog-footer">
            <el-button type="warning" @click.stop="handleCloseOpenedFileAndNext" :disabled="savePending">{{this.$t("editor.unSaveClose")}}</el-button>
            <el-button type="primary" @click.stop="saveAndCloseOpenedFileAndNext" :loading="savePending">{{this.$t("editor.saveClose")}}</el-button>
          </div>
        </el-dialog>
      </div>
      <el-collapse-transition>
        <el-tree v-show="trees.isOpenedShow && openedTreeData.length > 0" ref='openedTree' node-key='path' :data="openedTreeData" :props="openedTreesProps" :render-content="renderOpenedFile" highlight-current @node-click="handleOpenedClick">
        </el-tree>
      </el-collapse-transition>
    </div>

    <div class="my-tree tree-item" :class="{'is-active': trees.isMyShow}">
      <div class="my-files-container">
        <h1 class="toggle-bar" @click='togglePersonalSiteList'>
          <i class="el-icon-arrow-right"></i> {{ $t('editor.myPersonalWebsites') }}
        </h1>
        <span class="pull-right-icon">
          <el-tooltip :content="$t('editor.newWebsite')">
            <el-button class="iconfont icon-add2" type="text" @click='openNewWebsiteDialog()'></el-button>
          </el-tooltip>
        </span>
      </div>
      <el-collapse-transition>
        <el-tree v-show="personalSiteList.length > 0 && trees.isMyShow" ref='fileManagerTree' node-key="path" :data="personalSiteList | sortBy('domain')" :props="filesTreeProps" :render-content="renderContent" highlight-current @node-click="handleNodeClick" @node-expand="handleNodeExpand" @node-collapse="handleNodeCollapse">
        </el-tree>
      </el-collapse-transition>
      <el-collapse-transition>
        <div class="empty" v-if="personalSiteList.length <= 0">
          <p class="info">{{ $t('editor.noPersonalWebsite') }}</p>
          <el-button type="text" @click="openNewWebsiteDialog">{{ $t('editor.createWebsiteNow') }}</el-button>
        </div>
      </el-collapse-transition>
    </div>

    <div class="joined-tree tree-item" :class="{'is-active': trees.isContributedShow}">
      <h1 class="toggle-bar" @click='toggleContributedSiteList'>
        <i class="el-icon-arrow-right"></i> {{ $t('editor.myContributedWebsites') }}
      </h1>
      <el-collapse-transition>
        <el-tree v-show="contributedSiteList.length > 0 && trees.isContributedShow" ref='fileManagerTree' node-key="path" :data="contributedSiteList | sortBy('username')" :props="filesTreeProps" :render-content="renderContent" highlight-current @node-click="handleNodeClick" @node-collapse="handleNodeCollapse" @node-expand="handleNodeExpand">
        </el-tree>
      </el-collapse-transition>
      <el-collapse-transition>
        <div class="empty" v-show="trees.isContributedShow">
          <p class="info">{{ $t('editor.myContributedWebsitesTip') }}</p>
        </div>
      </el-collapse-transition>
    </div>
    <new-website-dialog :show='isNewWebsiteDialogShow' @close='closeNewWebsiteDialog'></new-website-dialog>
  </div>
</template>
<script>
import _ from 'lodash'
import { mapGetters, mapActions } from 'vuex'
import FileManagerCustomTreeNode from './FileManagerCustomTreeNode'
import FileManagerOpenedFileNode from './FileManagerOpenedFileNode'
import { getFileFullPathByPath } from '@/lib/utils/gitlab'
import NewWebsiteDialog from '@/components/common/NewWebsiteDialog'

export default {
  name: 'FileManager',
  data() {
    return {
      savePending: false,
      dialogVisible: false,
      dialogCloseAllVisible: false,
      toBeCloseFilePath: '',
      toBeCloseFileName: '',
      filesTreeProps: {
        children: 'children',
        label: 'sitename'
      },
      trees: {
        isOpenedShow: true,
        isMyShow: true,
        isContributedShow: false
      },
      openedTreesProps: {
        children: 'children',
        label: 'label'
      },
      isNewWebsiteDialogShow: false
    }
  },
  async mounted() {
    this.$route.path !== '/' && (await this.checkSitePath())
    await this.initUrlExpandSelect()
    this.$nextTick(() => {
      let ele = document.querySelector('.is-current:last-child')
      ele && ele.scrollIntoView()
    })
  },
  computed: {
    ...mapGetters({
      personalSiteList: 'user/personalSiteList',
      personalSitePaths: 'user/personalSitePathMap',
      contributedSiteList: 'user/contributedSiteList',
      showOpenedFiles: 'showOpenedFiles',
      allSiteNameList: 'user/personalAndContributedSiteNameList',
      openedFiles: 'openedFiles',
      activePageUrl: 'activePageUrl',
      activePageInfo: 'activePageInfo',
      filemanagerTreeNodeExpandMapByPath: 'filemanagerTreeNodeExpandMapByPath',
      getOpenedFileByPath: 'getOpenedFileByPath',
      username: 'user/username',
      hasOpenedFiles: 'hasOpenedFiles',
      updateRecentUrlList: 'updateRecentUrlList'
    }),
    openedTreeData() {
      let clonedopenedFiles = _.clone(this.showOpenedFiles)
      let treeDatas = []
      let that = this
      _.forOwn(clonedopenedFiles, function(value, key) {
        let pathArr = key.split('/')
        let pathLen = pathArr.length
        let pageName = pathArr[pathLen - 1].replace(/.md$/, '')
        let userName = pathArr[0]
        let siteName = pathArr[1]
        let nodeData = {
          label: `${pageName}(${userName}/${siteName})`,
          path: key,
          isModified: value && value.timestamp
        }
        treeDatas.push(nodeData)
      })
      return treeDatas
    },
    openedFilesPaths() {
      return _.keys(this.openedFiles)
    },
    hasUnSaveOpenedFiles() {
      return this.unSavedOpenedFiles.length > 0
    },
    unSavedOpenedFiles() {
      return _.filter(_.values(this.showOpenedFiles), ({ saved }) => !saved)
    },
    unSavedOpenedFilesPaths() {
      return _.map(this.unSavedOpenedFiles, ({ path }) => `${path}.md`.slice(1))
    },
    openedFilesPathAndTime() {
      return _.map(this.showOpenedFiles, ({ path, timestamp }) => ({
        path,
        timestamp
      }))
    }
  },
  watch: {
    openedFilesPathAndTime(newVal, oldVal) {
      if (JSON.stringify(newVal) === JSON.stringify(oldVal)) return
      let updateRecentUrlList = this.updateRecentUrlList.concat(newVal)
      updateRecentUrlList = updateRecentUrlList.sort(
        (obj1, obj2) => obj1.timestamp < obj2.timestamp
      )
      updateRecentUrlList = _.uniqBy(
        updateRecentUrlList,
        obj => obj.path
      ).slice(0, 5)
      let payload = { updateRecentUrlList }
      this.addRecentOpenedSiteUrl(payload)
    }
  },
  methods: {
    ...mapActions({
      getAllPersonalWebsite: 'user/getAllPersonalWebsite',
      getAllContributedWebsite: 'user/getAllContributedWebsite',
      getRepositoryTree: 'gitlab/getRepositoryTree',
      updateFilemanagerTreeNodeExpandMapByPath:
        'updateFilemanagerTreeNodeExpandMapByPath',
      savePageByPath: 'savePageByPath',
      refreshOpenedFile: 'refreshOpenedFile',
      closeOpenedFile: 'closeOpenedFile',
      gitlabRemoveFile: 'gitlab/removeFile',
      closeAllOpenedFile: 'closeAllOpenedFile',
      addRecentOpenedSiteUrl: 'addRecentOpenedSiteUrl'
    }),
    async checkSitePath(checkTimes = 10, waitTime = 500) {
      // No need to jump to #/ at here
      // please check EditorPage.vue L:64
      // if (this.checkUrlSite()) {
      //   return this.$router.push('/')
      // }
      const sleep = async () =>
        new Promise(resolve => setTimeout(resolve, waitTime))
      let { sitepath } = this.activePageInfo
      if (sitepath) return Promise.resolve()
      while (checkTimes--) {
        await sleep()
        let { sitepath } = this.activePageInfo
        if (sitepath) {
          return Promise.resolve()
        }
      }
      return Promise.resolve()
    },
    checkUrlSite() {
      let siteName = this.$route.path.split('/')[2]
      return !this.allSiteNameList.includes(siteName)
    },
    async initUrlExpandSelect() {
      let {
        username,
        isLegal,
        sitepath,
        fullPath,
        paths = []
      } = this.activePageInfo
      if (this.username !== username && sitepath) {
        this.$set(this.trees, 'isMyShow', false)
        this.$set(this.trees, 'isContributedShow', true)
      }
      if (!isLegal) {
        let closeAllFolder = this.personalSitePaths
          ? Object.keys(this.personalSitePaths).map(path => ({
              path,
              expanded: false
            }))
          : []
        return this.updateFilemanagerTreeNodeExpandMapByPath(closeAllFolder)
      }
      await this.getRepositoryTree({ path: sitepath })

      let folderPaths = paths.slice(0, -1)
      let expandedFolderPaths = folderPaths.reduce(
        (prev, current) => {
          let exapndedPath = prev.slice(-1) + '/' + current
          return prev.concat(exapndedPath)
        },
        [sitepath]
      )
      let expandedFolderPathsList = expandedFolderPaths.map(path => ({
        path,
        expanded: true
      }))
      let appendCloseFolderPathsList = this.personalSitePaths
        ? Object.keys(this.personalSitePaths)
            .filter(i => i !== sitepath)
            .map(path => ({ path, expanded: false }))
        : []
      this.updateFilemanagerTreeNodeExpandMapByPath([
        ...expandedFolderPathsList,
        ...appendCloseFolderPathsList
      ])
    },
    renderOpenedFile(h, { node, data, store }) {
      let { fullPath: activePageFullPath } = this.activePageInfo
      activePageFullPath === data.path && store.setCurrentNode(node)
      return <FileManagerOpenedFileNode data={data} node={node} />
    },
    renderContent(h, { node, data, store }) {
      // trick codes below
      // manipulated the node in <el-tree/>
      node.isLeaf = data.type === 'blob'
      // restore node expand status
      let path = data.path || `${data.username}/${data.sitename}`
      node.expanded = this.filemanagerTreeNodeExpandMapByPath[path]
      // modify store info
      let { fullPath: activePageFullPath } = this.activePageInfo
      activePageFullPath === data.path && store.setCurrentNode(node)
      return <FileManagerCustomTreeNode data={data} node={node} />
    },
    async handleNodeClick(data, node, component) {
      // save node expand status
      let path = data.path || `${data.username}/${data.name}`
      this.updateFilemanagerTreeNodeExpandMapByPath({
        path,
        expanded: node.expanded
      })
      // try open files list in site level
      let repositoryIsClickedAndFileListIsEmpty =
        node.level === 1 && _.isEmpty(data.children)
      if (repositoryIsClickedAndFileListIsEmpty) {
        let { username, name } = data
        let path = `${username}/${name}`
        let recursive = true
        node.loading = true
        await this.getRepositoryTree({ path })
      }
      // try open file
      // let isFileClicked = data.type === 'blob'
      if (data.type === 'blob') {
        this.$router.push('/' + data.path.replace(/\.md$/, ''))
        let url = this.$router.resolve({ path: this.$route.path }).href
        history.replaceState('', '', url)
      }
      // isFileClicked && this.$router.push('/' + data.path.replace(/\.md$/, ''))
    },
    handleNodeExpand(data, node, component) {
      let path = data.path || `${data.username}/${data.name}`
      this.updateFilemanagerTreeNodeExpandMapByPath({
        path,
        expanded: true
      })
    },
    handleNodeCollapse(data, node, component) {
      let path = data.path || `${data.username}/${data.name}`
      this.updateFilemanagerTreeNodeExpandMapByPath({
        path,
        expanded: false
      })
    },
    closeAndResetFile(path) {
      let _path = Object.keys(this.openedFiles).filter(name => name !== path)
      this.closeOpenedFile({ path })
      if (this.$route.path.slice(1) !== path.replace(/\.md$/, '')) return
      if (_path.length === 0) {
        this.$router.push('/')
      } else {
        this.$router.push('/' + _path[0].replace(/\.md$/, ''))
      }
    },
    handleCloseDialog() {
      this.toBeCloseFilePath = ''
      this.toBeCloseFileName = ''
      this.dialogVisible = false
    },
    handleCloseAllDialog() {
      this.toBeCloseFilePath = ''
      this.toBeCloseFileName = ''
      this.dialogCloseAllVisible = false
    },
    async saveAndCloseOpenedFile() {
      let path = this.toBeCloseFilePath
      this.savePending = true
      await this.savePageByPath(path)
        .then(() => {
          this.closeAndResetFile(path)
          this.handleCloseDialog()
          this.savePending = false
        })
        .catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          this.handleCloseDialog()
          this.savePending = false
        })
    },
    handleOpenedClick({ path }, node) {
      this.$router.push('/' + path.replace(/\.md$/, ''))
      let url = this.$router.resolve({ path: this.$route.path }).href
      history.replaceState('', '', url)
    },
    toggleContent(type) {
      this.trees[type] = !this.trees[type]
    },
    togglePersonalSiteList() {
      let type = 'isMyShow'
      this.toggleContent(type)
      this.trees[type] && this.getAllPersonalWebsite()
    },
    toggleContributedSiteList() {
      let type = 'isContributedShow'
      this.toggleContent(type)
      this.trees[type] && this.getAllContributedWebsite()
    },
    isSaveble(nodeData) {
      let path = nodeData.path
      return path && this.openedFiles[path] && this.openedFiles[path].timestamp
    },
    openNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = true
    },
    closeNewWebsiteDialog() {
      this.isNewWebsiteDialogShow = false
    },
    async closeAllOpenedFilesConfirm() {
      if (this.unSavedOpenedFilesPaths.length > 0) {
        this.dialogCloseAllVisible = true
        let path = this.unSavedOpenedFilesPaths[0]
        let siteName = path
          .split('/')
          .slice(1, 2)
          .join()
        let fileName = path
          .split('/')
          .slice(-1)
          .join()
          .replace(/\.md$/, '')
        this.toBeCloseFileName = `${siteName}/${fileName}`
        this.toBeCloseFilePath = path
      } else {
        this.$router.push('/')
        this.closeAllOpenedFile()
      }
    },
    checkHasNext() {
      if (this.unSavedOpenedFilesPaths.length > 0) {
        this.closeAllOpenedFilesConfirm()
      } else {
        this.closeAllOpenedFile()
        this.$router.push('/')
        this.dialogCloseAllVisible = false
      }
    },
    handleCloseOpenedFileAndNext() {
      let path = this.toBeCloseFilePath
      path && this.closeAndResetFile(path)
      this.checkHasNext()
    },
    async saveAndCloseOpenedFileAndNext() {
      this.savePending = true
      let path = this.toBeCloseFilePath
      await this.savePageByPath(path)
        .then(() => {
          this.closeAndResetFile(path)
          this.savePending = false
          this.checkHasNext()
        })
        .catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          this.handleCloseAllDialog()
          this.savePending = false
        })
    },
    async saveAllOpenedFiles() {
      if (!this.hasUnSaveOpenedFiles) return
      let num = this.unSavedOpenedFilesPaths.length
      let paths = this.unSavedOpenedFilesPaths
      let isSuccess = true
      this.savePending = true
      while (num--) {
        await this.savePageByPath(paths[num]).catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          isSuccess = false
        })
      }
      isSuccess &&
        this.$message({
          message: this.$t('editor.saveSuccess'),
          type: 'success'
        })
      this.savePending = false
    }
  },
  components: {
    NewWebsiteDialog
  },
  filters: {
    sortBy: (list, key) =>
      list.sort((obj1, obj2) => {
        let val1 = obj1[key]
        let val2 = obj2[key]
        if (val1 < val2) {
          return -1
        } else if (val1 > val2) {
          return 1
        } else {
          return 0
        }
      })
  }
}
</script>

<style lang='scss'>
.file-manager {
  height: 100%;
  background-color: #ccd3da;
  overflow-y: auto;
  .opened-files-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding-right: 20px;
    .opened-files-buttons {
      .iconfont {
        color: #535353;
        font-size: 22px;
        &:hover {
          color: #3ba4ff;
        }
      }
    }
  }

  .my-files-container {
    display: flex;
    justify-content: space-between;
    padding-right: 18px;
    .pull-right-icon {
      .iconfont {
        color: #535353;
        font-size: 18px;
        &:hover {
          color: #3ba4ff;
        }
      }
    }
  }

  h1 {
    font-size: 16px;
    color: #333;
    margin: 0;
    padding-left: 18px;
    position: relative;
  }
  .toggle-bar {
    cursor: pointer;
  }
  .toggle-bar .el-icon-arrow-right {
    position: absolute;
    left: 4px;
    top: 6px;
    font-weight: bold;
    font-size: 12px;
  }
  .is-active h1 {
    margin: 0 0 12px 0;
  }
  .is-active .el-icon-arrow-right {
    transform: rotate(90deg);
  }
  a {
    text-decoration: none;
  }
  .el-tree {
    color: #535353;
  }

  .el-tree--highlight-current .el-tree-node > .el-tree-node__content {
    .file-manager-buttons-container {
      display: none;
    }
  }
  .el-tree--highlight-current
    .el-tree-node.is-current
    > .el-tree-node__content {
    background-color: #ccfffc;
  }
  .el-tree-node__content:hover {
    background-color: #ccfffc;
    .file-manager-buttons-container {
      display: inline-block !important;
      line-height: 38px !important;
    }
  }
  .opened-tree {
    .el-tree-node__content:hover {
      background-color: #ccfffc;
      .el-tree-node__label {
        padding-right: 135px;
      }
    }
  }
  .el-tree-node__content {
    height: 32px;
    line-height: 32px;
    padding-left: 15px;
  }
  .el-tree-node__expand-icon {
    font-weight: bold;
    color: #535353;
  }
  .el-tree-node__expand-icon.is-leaf {
    color: transparent;
  }
  .el-icon-caret-right:before {
    content: '\e6e0';
  }
  .el-tree-node__label {
    width: 100%;
    position: relative;
    overflow: hidden;
    span:not(.rename-wrapper) {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: inline-block;
      max-width: 100%;
      vertical-align: middle;
    }
  }
  .file-manager-buttons-container {
    position: absolute;
    right: 20px;
  }
  .file-manager-buttons-container .iconfont {
    font-size: 20px;
    color: #777;
  }
  .el-button + .el-button {
    margin-left: 5px;
  }
  .icon-file__ {
    font-weight: bold;
    color: #000;
  }
  .icon-private {
    color: #f48622;
  }
  .icon-common_websites {
    color: #4c97d1;
  }

  .tree-item {
    background-color: #fff;
    padding: 8px 0 9px 20px;
    margin-bottom: 8px;
  }
  .tree-item.is-active {
    padding: 6px 0 6px 20px;
  }
  .info {
    font-size: 14px;
    color: #c0c4cc;
    margin: 0 0 10px 0;
  }
  .el-button--text {
    padding: 0;
  }
  .empty {
    padding-left: 35px;
  }

  .icon-edited_file.is-modified {
    color: #f4b622;
  }
  .el-loading-spinner .circular {
    width: 22px;
  }
  .el-dialog__body .dialog-content {
    text-align: center;
    word-wrap: break-word;
    white-space: normal;
    line-height: 32px;
  }
}
</style>

<template>
  <div class="file-tree-node" :class="operationButtonsCountClass">
    <div class="el-tree-node__label" v-loading="removePending || addFilePending || addFolderPending || renamePending || savePending">
      <span class="rename-wrapper" v-if="isRename">
        <el-input @click.native.stop ref="input" v-if="isRename" @blur="delayCancel" @keyup.enter.native="handleRenameConfirm" v-model="newName" class="rename-input" size="mini"></el-input>
        <el-tooltip :content="$t('editor.confirm')">
          <el-button @click.stop="handleRenameConfirm" class="rename-btn el-icon-check" type="text" size="mini"></el-button>
        </el-tooltip>
        <el-tooltip :content="$t('editor.cancel')">
          <el-button @click.stop="handleRenameCancel" class="rename-btn el-icon-close" type="text" size="mini"></el-button>
        </el-tooltip>
      </span>
      <span v-else-if="data.memberName">{{data.username}}/{{data.sitename}}({{data | treeNodeLableFilter(node)}})</span>
      <span v-else>{{data | treeNodeLableFilter(node)}}</span>
      <span class="node-icon">
        <i :class="['iconfont', isHasOpened ? 'icon-edited_file is-modified' : 'icon-file_']" v-if="isFile"></i>
        <i class="iconfont icon-folder" v-else-if="isFolder"></i>
        <i class="iconfont icon-private" v-else-if="isWebsite && data.visibility === 1"></i>
        <i class="iconfont icon-common_websites" v-else></i>
      </span>
      <div @click.stop v-if='isWebsiteSettingShow'>
        <website-setting-dialog :show='isWebsiteSettingShow' :sitePath='currentPath' @close='closeWebsiteSettingDialog'></website-setting-dialog>
      </div>
      <div @click.stop v-if='isNewWebPageDialogShow'>
        <NewWebPageDialog :show='isNewWebPageDialogShow' :folderPath='currentPath' :sitePath='sitePath' @close='closeNewWebPageDialog' />
      </div>
    </div>
    <span v-if="!isRename" :title="data | treeNodeTitleFilter(node, isFile, isFolder, isEn)" class="file-tree-node-tooltip-button">{{data | treeNodeLableFilter(node)}}</span>
    <span class="file-manager-buttons-container" v-if="!isRename">
      <el-tooltip v-if="isHasOpened" :content="$t('editor.save')">
        <el-button v-loading='data.savePending' class="iconfont icon-save edit-hover" size="mini" type="text" @click.stop='save(data)'></el-button>
      </el-tooltip>
      <el-tooltip v-if="isHasOpened" :content="$t('editor.reload')">
        <el-button class="iconfont icon-refresh edit-hover" size="mini" type="text" @click.stop='confirmRefresh'></el-button>
      </el-tooltip>
      <el-tooltip v-if="isFile || isFolder" :content="$t('editor.rename')">
        <el-button class="iconfont el-icon-edit edit-hover" size="mini" type="text" @click.stop="toggleRename"></el-button>
      </el-tooltip>
      <el-tooltip v-if="isAddable" :content="$t('editor.newPage')">
        <el-button class="iconfont icon-add_file edit-hover" size="mini" type="text" @click.stop="addFile"></el-button>
      </el-tooltip>
      <el-tooltip v-if="isAddable" :content="$t('editor.newFolder')">
        <el-button class="iconfont icon-folder_ edit-hover" size="mini" type="text" @click.stop="addFolder"></el-button>
      </el-tooltip>
      <el-tooltip v-if="isRemovable" :content="$t('editor.delete')">
        <el-button class="iconfont icon-delete edit-hover" size="mini" type="text" @click.stop="removeFile"></el-button>
      </el-tooltip>
      <el-tooltip v-if="isSettable" :content="$t('editor.settings')">
        <el-button class="iconfont icon-set_up edit-hover" size="mini" type="text" @click.stop="goSetting"></el-button>
      </el-tooltip>
    </span>
  </div>
</template>
<script>
import _ from 'lodash'
import { locale } from '@/lib/utils/i18n'
import { mapActions, mapGetters } from 'vuex'
import { suffixFileExtension, gitFilenameValidator } from '@/lib/utils/gitlab'
import WebsiteSettingDialog from '@/components/common/WebsiteSettingDialog'
import NewWebPageDialog from '@/components/common/NewWebPageDialog'

export default {
  name: 'FileManagerCustomTreeNode',
  props: {
    data: Object,
    node: Object
  },
  data() {
    return {
      addFolderPending: false,
      addFilePending: false,
      removePending: false,
      savePending: false,
      renamePending: false,
      isWebsiteSettingShow: false,
      isNewWebPageDialogShow: false,
      isRename: false,
      isValidator: false,
      newName: ''
    }
  },
  methods: {
    ...mapActions({
      setActiveManagePaneComponent: 'setActiveManagePaneComponent',
      gitlabGetRepositoryTree: 'gitlab/getRepositoryTree',
      gitlabCreateFile: 'gitlab/createFile',
      gitlabAddFolder: 'gitlab/addFolder',
      gitlabRemoveFile: 'gitlab/removeFile',
      gitlabRenameFile: 'gitlab/renameFile',
      gitlabRenameFolder: 'gitlab/renameFolder',
      gitlabRemoveFolder: 'gitlab/removeFolder',
      updateFilemanagerTreeNodeExpandMapByPath:
        'updateFilemanagerTreeNodeExpandMapByPath',
      userGetSiteLayoutConfig: 'user/getSiteLayoutConfig',
      userDeletePagesConfig: 'user/deletePagesConfig',
      savePageByPath: 'savePageByPath',
      refreshOpenedFile: 'refreshOpenedFile',
      addRecentOpenedSiteUrl: 'addRecentOpenedSiteUrl'
    }),
    async addFile() {
      this.openNewWebPageDialog()
    },
    async addFolder() {
      let self = this

      let newFolderName = await this.newFileNamePrompt({
        what: self.$t('editor.folder')
      })
      if (!newFolderName) return
      let newFolderPath = `${this.currentPath}/${newFolderName}`
      this.addFolderPending = true
      await this.gitlabAddFolder({ path: newFolderPath })
      this.expandFolder(newFolderPath)
      this.addFolderPending = false
    },
    async newFileNamePrompt({ what = this.$t('editor.website') } = {}) {
      let self = this

      await this.gitlabGetRepositoryTree({ path: this.sitePath })
      let childNames = this.gitlabChildNamesByPath(this.currentPath)

      let { value: newFileName } = await this.$prompt(
        `${what} ${self.$t('editor.name')}`,
        `${self.$t('editor.new')} ${what}`,
        {
          cancelButtonText: self.$t('el.messagebox.cancel'),
          confirmButtonText: self.$t('el.messagebox.confirm'),
          inputValidator: str => {
            let value = (str || '').trim()
            if (!value) return self.$t('editor.required')
            if (!gitFilenameValidator(value)) return self.$t('editor.nameRule')
            if (childNames.indexOf(value) > -1)
              return self.$t('editor.nameExist')
            return true
          }
        }
      )

      return newFileName && newFileName.trim()
    },
    expandFolder(path) {
      this.updateFilemanagerTreeNodeExpandMapByPath({
        path: path
          .split('/')
          .slice(0, -1)
          .join('/'),
        expanded: true
      })
    },
    removeFolder(data) {
      let folder = data.path
      let toRemoveFiles = this.recursion(data)

      const h = this.$createElement
      this.$msgbox({
        title: this.$t('editor.delete'),
        message: h('p', null, [
          h('span', null, this.$t('editor.deleteFolderBefore')),
          h('span', { style: 'color: #FF4342' }, ` "${data.name} "`),
          h('span', null, this.$t('editor.deleteFolderAfter'))
        ]),
        showCancelButton: true,
        confirmButtonText: this.$t('el.messagebox.confirm'),
        cancelButtonText: this.$t('el.messagebox.cancel')
      })
        .then(async () => {
          this.removePending = true
          await this.gitlabRemoveFolder({ folder, paths: toRemoveFiles })
          await this.deletePagesFromLayout({ paths: toRemoveFiles })
          this.removeRecentOpenFolder(toRemoveFiles)
          this.resetPage({ toRemoveFiles })
          this.removePending = false
        })
        .catch(e => console.error(e))
    },
    removeRecentOpenFolder(toRemoveFiles) {
      let toDele = _.map(toRemoveFiles, i => `/${i.replace(/\.md$/, '')}`)
      let updateRecentUrlList = this.updateRecentUrlList.filter(
        item => toDele.indexOf(item.path) === -1
      )
      this.addRecentOpenedSiteUrl({ updateRecentUrlList })
    },
    recursion(data) {
      let childrenFiles = []
      const recursionFile = data => {
        // }
        if (/.md$/.test(data.path)) {
          childrenFiles.push(data.path)
        }
        data.children && data.children.forEach(item => recursionFile(item))
      }
      recursionFile(data)
      return childrenFiles
    },
    async save(data) {
      if (data.savePending === undefined) {
        this.$set(data, 'savePending', false)
      }
      let path = data.path
      data.savePending = true
      await this.savePageByPath(path)
      data.savePending = false
    },
    confirmRefresh() {
      this.$confirm(this.$t('editor.pullServerData'), this.$t('editor.hint'), {
        confirmButtonText: this.$t('el.messagebox.confirm'),
        cancelButtonText: this.$t('el.messagebox.cancel'),
        type: 'warning'
      })
        .then(() => {
          this.refreshOpenedFile(this.data)
        })
        .catch(err => {
          console.warn(err)
        })
    },
    async toggleRename() {
      if (this.isFolder) {
        let childrenFiles = this.recursion(this.data)
        let unSavedFiles = _.intersection(this.unSavedFiles, childrenFiles)
        if (unSavedFiles.length > 0) {
          await this.$confirm(
            `${unSavedFiles.length}${this.$t('editor.filesUnSaved')}`,
            {
              confirmButtonText: this.$t('editor.confirm'),
              cancelButtonText: this.$t('editor.cancel'),
              type: 'warnning'
            }
          )
            .then(async () => {
              this.savePending = true
              let num = unSavedFiles.length
              let files = unSavedFiles.map(i => i.replace(/.md$/, ''))
              while (num--) {
                await this.savePageByPath(files[num])
              }
              this.savePending = false
            })
            .catch(() => {})
        }
      } else {
        let { saved } = this.getOpenedFileByPath(this.filePath)
        if (!saved) {
          await this.$confirm(this.$t('editor.theFileUnSaved'), {
            confirmButtonText: this.$t('el.messagebox.confirm'),
            cancelButtonText: this.$t('el.messagebox.cancel'),
            type: 'warning'
          }).then(async () => {
            await this.savePageByPath(this.filePath)
            this.$message({
              type: 'success',
              message: this.$t('editor.saveSuccess')
            })
            this.toggleInputFocus()
          })
          return
        }
      }
      this.toggleInputFocus()
    },
    toggleInputFocus() {
      this.isRename = true
      this.newName = this.data.name.replace(/.md$/, '')
      this.$nextTick(() => this.$refs.input.focus())
    },
    async handleRenameConfirm() {
      if (
        !this.newName.trim() ||
        this.newName.trim() === this.data.name.replace(/.md$/, '')
      ) {
        return (this.isRename = false)
      }
      await this.gitlabGetRepositoryTree({ path: this.sitePath })
      let childNames = await this.gitlabChildNamesByPath(
        this.currentPath
          .split('/')
          .slice(0, -1)
          .join('/')
      )
      if (childNames.indexOf(this.newName) > -1) {
        return this.$message.error(this.$t('editor.nameExist'))
      }
      if (!gitFilenameValidator(this.newName)) {
        this.isValidator = true
        return this.$message.error(
          `${this.newName} ${this.$t('editor.nameRule')}`
        )
      }
      this.renamePending = true
      if (this.isFolder) {
        let childrenFiles = this.recursion(this.data)
        await this.gitlabRenameFolder({
          currentFolderPath: this.currentPath,
          newFolderPath: `${this.parentPath}/${this.newName}`,
          childrenFiles
        })
      } else {
        let newFilePath = `${this.parentPath}/${this.newName}.md`
        await this.gitlabRenameFile({
          currentFilePath: this.data.path,
          newFilePath: newFilePath
        })
        this.updateFilemanagerTreeNodeExpandMapByPath(newFilePath)
      }
      this.isRename = false
      this.renamePending = false
      this.isValidator = false
      this.resetPage({ currentPath: this.currentPath })
    },
    handleRenameCancel() {
      this.isRename = false
      this.isValidator = false
      this.newFileName = ''
    },
    delayCancel() {
      setTimeout(
        () =>
          !this.isValidator && !this.renamePending && this.handleRenameCancel(),
        250
      )
    },
    removeFile() {
      if (this.isFolder) {
        return this.removeFolder(this.data)
      }
      const h = this.$createElement
      let siteName = this.data.path.split('/').slice(1, 2)
      let fileName = this.data.name.replace(/\.md$/, '')
      this.$msgbox({
        title: this.$t('editor.modDelMsgTitle'),
        message: h('p', null, [
          h('span', null, this.$t('editor.delConfirm')),
          h(
            'span',
            { style: 'color: #FF4342' },
            ` "${siteName}/${fileName} " `
          ),
          h('span', null, '?')
        ]),
        showCancelButton: true,
        confirmButtonText: this.$t('el.messagebox.confirm'),
        cancelButtonText: this.$t('el.messagebox.cancel')
      })
        .then(async () => {
          this.removePending = true
          await this.gitlabRemoveFile({ path: this.currentPath })
          await this.deletePagesFromLayout({ paths: [this.currentPath] })
          this.removeRecentOpenFile(this.currentPath)
          this.resetPage({ currentPath: this.currentPath })
          this.removePending = false
        })
        .catch(() => {})
    },
    removeRecentOpenFile(path) {
      let delPath = `/${path.replace(/\.md$/, '')}`
      let updateRecentUrlList = this.updateRecentUrlList.filter(
        item => item.path !== delPath
      )
      this.addRecentOpenedSiteUrl({ updateRecentUrlList })
    },
    async deletePagesFromLayout({ paths = [] }) {
      const re = /^\w+\/\w+\//
      let sitePath = paths[0].match(re)
      if (sitePath) sitePath = sitePath[0].replace(/\/$/, '')
      let pages = _.map(paths, page => page.replace(re, ''))
      await this.userGetSiteLayoutConfig({ path: sitePath })
      let config = this.getSiteLayoutConfigBySitePath(sitePath)
      await this.userDeletePagesConfig({ sitePath, pages })
    },
    resetPage({ currentPath = null, toRemoveFiles = null }) {
      if (toRemoveFiles && toRemoveFiles.length > 0) {
        let currentRoutePath = this.$route.path.substring(1)
        let isRestPage = toRemoveFiles.some(item => {
          return item.split('.')[0] === currentRoutePath
        })
        if (isRestPage) {
          return this.$router.push('/')
        }
      }
      if (
        currentPath &&
        currentPath.split('.')[0] === this.$route.path.substring(1)
      ) {
        return this.$router.push('/')
      }
    },
    goSetting() {
      if (this.isWebsite) {
        this.openWebsiteSettingDialog()
      }
      if (this.isFile) {
        this.setActiveManagePaneComponent({
          name: 'PageSetting',
          props: {
            pagePath: this.currentPath
          }
        })
      }
    },
    openWebsiteSettingDialog() {
      this.isWebsiteSettingShow = true
    },
    closeWebsiteSettingDialog() {
      this.isWebsiteSettingShow = false
    },
    openNewWebPageDialog() {
      this.isNewWebPageDialogShow = true
    },
    closeNewWebPageDialog() {
      this.isNewWebPageDialogShow = false
    }
  },
  computed: {
    ...mapGetters({
      gitlabChildNamesByPath: 'gitlab/childNamesByPath',
      getSiteLayoutConfigBySitePath: 'user/siteLayoutConfigBySitePath',
      getOpenedFileByPath: 'getOpenedFileByPath',
      openedFiles: 'openedFiles',
      username: 'user/username',
      updateRecentUrlList: 'updateRecentUrlList'
    }),
    isEn() {
      return locale === 'en-US'
    },
    operationButtonsCountClass() {
      let count = _.compact([
        this.isHasOpened,
        this.isHasOpened,
        this.isFile,
        this.isFolder,
        this.isAddable,
        this.isAddable,
        this.isRemovable,
        this.isSettable
      ]).length
      let buttonCountClass = this.isRename ? '' : `buttons-count-${count}`
      let websiteLabelClass = this.isWebsite ? ' website-node-label' : ''
      return buttonCountClass + websiteLabelClass
    },
    pending() {
      return (
        this.addFolderPending ||
        this.addFilePending ||
        this.removePending ||
        this.renamePending
      )
    },
    isFile() {
      return this.data.type === 'blob'
    },
    isHasOpened() {
      return (
        this.isFile && _.keys(this.openedFiles).indexOf(this.data.path) !== -1
      )
    },
    isFolder() {
      return this.data.type === 'tree'
    },
    isWebsite() {
      return this.node.level === 1
    },
    isAddable() {
      return !this.isFile
    },
    isRemovable() {
      return this.node.level !== 1
    },
    isSettable() {
      return this.isWebsite || this.isFile
    },
    currentPath() {
      return this.isWebsite
        ? `${this.data.username}/${this.data.name}`
        : this.data.path
    },
    sitePath() {
      if (this.isWebsite) return `${this.data.username}/${this.data.name}`

      let [username, name] = this.data.path.split('/')
      return `${username}/${name}`
    },
    filePath() {
      return this.data.path.replace(/\.md$/, '')
    },
    unSavedFiles() {
      return _.keys(_.pickBy(this.openedFiles, ({ saved }) => !saved))
    },
    parentPath() {
      return this.data.path
        .split('/')
        .slice(0, -1)
        .join('/')
    }
  },
  filters: {
    treeNodeLableFilter(data, node) {
      let str = data.displayName || data.name || node.label
      return (str && str.replace(/\.md$/, '')) || ''
    },
    treeNodeTitleFilter(data, node, isFile, isFolder, isEn) {
      let str = data.displayName || data.name || node.label
      let name = (str && str.replace(/\.md$/, '')) || ''
      let pageTypeText = isEn ? 'pageName: ' : '页面名：'
      let folderTypeText = isEn ? 'folderName: ' : '文件夹名：'
      let siteTypeText = isEn ? 'siteName: ' : '网站名：'
      let fileTypeText = isFile
        ? pageTypeText
        : isFolder
        ? folderTypeText
        : siteTypeText
      return fileTypeText + name
    }
  },
  components: {
    WebsiteSettingDialog,
    NewWebPageDialog
  }
}
</script>

<style lang="scss">
.file-tree-node {
  flex: 1;
  overflow: hidden;
  &-tooltip-button {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    font-size: 0;
    border: none;
    background-color: transparent;
    &:hover {
      background-color: transparent;
    }
  }
  .el-tree-node__label {
    padding-left: 20px;
    .node-icon {
      position: absolute;
      left: 0;
    }
  }
  .website-node-label {
    margin-left: -24px;
    padding-left: 44px;
    .node-icon {
      left: 24px;
    }
  }
  .el-tree-node__label::before {
    content: ' ';
    display: inline-block;
    position: absolute;
    margin-left: -50px;
    height: 30px;
    width: 30px;
  }

  .icon-folder::before {
    font-size: 0.8em;
    color: #ffac33;
  }
  .edit-hover:hover {
    color: #409eff !important;
  }

  .rename-wrapper {
    display: inline-flex;
    .rename-btn {
      width: 20px;
      margin: 0 10px;
      color: #8a8a8a;
      font-weight: bold;
      font-size: 1.2em;
    }
  }
  .file-manager-buttons-container {
    height: 100%;
    top: 0;
    background-color: #ccfffc;
  }
}
.el-tree-node__content {
  position: relative;
  &:hover {
    .buttons-count-3 {
      padding-right: 105px;
    }
    .buttons-count-4 {
      padding-right: 135px;
    }
    .buttons-count-5 {
      padding-right: 160px;
    }
  }
}
</style>

<template>
  <span class='joined-tree-node el-tree-node__label' v-loading="deletePending">
    <span class="node-icon">
      <i class="iconfont icon-edited_file" :class="{'is-modified': data.isModified}"></i>
    </span>
    <span class=''>{{ node.label }}</span>
    <span class="file-manager-buttons-container">
      <el-tooltip :content="$t('editor.save')">
        <el-button v-loading='data.savePending' class="iconfont icon-save edit-hover" size="mini" type="text"></el-button>
      </el-tooltip>
      <el-tooltip :content="$t('editor.reload')">
        <el-button class="iconfont icon-refresh edit-hover" size="mini" type="text" @click.stop='confirmRefresh'></el-button>
      </el-tooltip>
      <el-tooltip :content="$t('editor.close')">
        <el-button class="iconfont icon-delete____ edit-hover" size="mini" type="text" @click.stop='handleCloseConfirm(data)'></el-button>
      </el-tooltip>
    </span>
    <div @click.stop class="close-dialog">
      <el-dialog center :visible.sync="dialogVisible" width="360px" closed="handleCloseDialog">
        <div class="dialog-content">{{`"${fileName}" ${$t("editor.fileUnSaved")}`}}</div>
        <div slot="footer" class="dialog-footer">
          <el-button type="warning" @click.stop="handleCloseOpenedFile(data)" :disabled="savePending">{{$t("editor.unSaveClose")}}</el-button>
          <el-button type="primary" @click.stop="saveAndCloseOpenedFile(data)" :loading="savePending">{{$t("editor.saveClose")}}</el-button>
        </div>
      </el-dialog>
    </div>
  </span>
</template>


<script>
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'FileManagerOpenedFileNode',
  data() {
    return {
      dialogVisible: false,
      savePending: false,
      deletePending: false
    }
  },
  props: {
    data: Object,
    node: Object
  },
  computed: {
    ...mapGetters({
      getOpenedFileByPath: 'getOpenedFileByPath',
      openedFiles: 'openedFiles',
      getSiteLayoutConfigBySitePath: 'user/siteLayoutConfigBySitePath',
      username: 'user/username',
      updateRecentUrlList: 'updateRecentUrlList'
    }),
    fileName() {
      let siteName = this.data.path.split('/').slice(1, 2)
      let fileName = this.data.path.split('/').slice(-1)
      return [...siteName, ...fileName].join('/').replace(/\.md$/, '')
    }
  },
  methods: {
    ...mapActions({
      savePageByPath: 'savePageByPath',
      refreshOpenedFile: 'refreshOpenedFile',
      closeOpenedFile: 'closeOpenedFile',
      gitlabRemoveFile: 'gitlab/removeFile',
      userGetSiteLayoutConfig: 'user/getSiteLayoutConfig',
      userDeletePagesConfig: 'user/deletePagesConfig',
      addRecentOpenedSiteUrl: 'addRecentOpenedSiteUrl'
    }),
    async handleCloseConfirm({ path }) {
      let file = this.getOpenedFileByPath(path)
      let { saved = true } = file
      if (saved) {
        this.closeAndReset(path)
      } else {
        this.dialogVisible = true
      }
    },
    handleCloseDialog() {
      this.dialogVisible = false
    },
    handleCloseOpenedFile({ path }) {
      this.closeAndReset(path)
      this.handleCloseDialog()
    },
    async saveAndCloseOpenedFile({ path }) {
      this.savePending = true
      await this.savePageByPath(path)
        .then(() => {
          this.closeAndReset(path)
          this.handleCloseDialog()
          this.savePending = false
        })
        .catch(e => {
          this.$message.error(this.$t('editor.saveFail'))
          this.handleCloseDialog()
          this.savePending = false
        })
    },
    confirmRefresh(){
      this.$confirm(this.$t('editor.pullServerData'), this.$t('editor.hint'), {
        confirmButtonText: this.$t('el.messagebox.confirm'),
        cancelButtonText: this.$t('el.messagebox.cancel'),
        type: 'warning'
      }).then(() => {
        this.refreshOpenedFile(this.data)
      }).catch((err) => { console.warn(err) });
    },
    closeAndReset(path) {
      let _path = Object.keys(this.openedFiles).filter(name => name !== path)
      this.closeOpenedFile({ path })
      if (this.$route.path.slice(1) !== path.replace(/\.md$/, '')) return
      _path.length === 0
        ? this.$router.push('/')
        : this.$nextTick(() => this.$router.push({ path: `/${_path[0].replace(/\.md$/, '')}` }))
    },
    async save(data) {
      if (data.savePending === undefined) {
        this.$set(data, 'savePending', false)
      }
      let path = data.path
      data.savePending = true
      await this.savePageByPath(path)
      data.savePending = false
    },
    removeRecentOpenFile(path) {
      let delPath = `/${path.replace(/\.md$/, '')}`
      let updateRecentUrlList = this.updateRecentUrlList.filter(item => item.path !== delPath)
      this.addRecentOpenedSiteUrl({ updateRecentUrlList })
    },
    async deletePagesFromLayout({ paths = [] }) {
      const re = /^\w+\/\w+\//
      let sitePath = paths[0].match(re)
      if (sitePath) sitePath = sitePath[0].replace(/\/$/, '')
      let pages = _.map(paths, page => page.replace(re, ''))
      await this.userGetSiteLayoutConfig({ path: sitePath })
      let config = this.getSiteLayoutConfigBySitePath(sitePath)
      await this.userDeletePagesConfig({ sitePath, pages })
    },
    resetPage(currentPath = null) {
      if (
        currentPath &&
        currentPath.replace(/\.md$/, '') === this.$route.path.substring(1)
      ) {
        return this.$router.push('/')
      }
    }
  }
}
</script>
<style lang="scss">
.close-dialog{
  .el-dialog__header{
    height: 0;
  }
  .el-dialog__body .dialog-content{
    text-align: center;
    word-wrap: break-word;
    white-space: normal;
  }
  .edit-hover:hover {
    color: #409eff !important;
  }
}
</style>

<template>
  <el-scrollbar class="history-list" :native="false">
    <div class="history-list-header">
      <div class="history-list-header-version">{{$t("editor.versionLabel")}}</div>
      <div class="history-list-header-username">{{$t("editor.operatorLabel")}}</div>
      <div class="history-list-header-date">{{$t("editor.updateAtLabel")}}</div>
    </div>
    <div class="history-list-item" :class="{'history-list-item-active': activeVersion == history.version}" v-for="(history, index) in historyList" :key="index" @click="getHistoryContent(history)" :title='getHoverMessage(history)'>
      <div class="history-list-item-version">{{history.version}}
        <span class="history-list-item-version-sub">{{history.message | sourceVersionFilter}}</span>
      </div>
      <div class="history-list-item-username" :title="history.author_name | oldNameFilter">{{history.author_name | oldNameFilter}}</div>
      <div class="history-list-item-date">{{history.authored_date | formatTime }}</div>
    </div>
    <div v-infinite-scroll="loadMore" infinite-scroll-disabled="isBusy" infinite-scroll-distance="0"></div>
  </el-scrollbar>
</template>
<script>
const SourceVersionStr = '|FROM'
import moment from 'moment'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'HistoryList',
  data() {
    return {
      perPage: 10,
      historyList: [],
      isBusy: false,
      nowPage: 1,
      activeVersion: undefined
    }
  },
  computed: {
    ...mapGetters({
      activePageInfo: 'activePageInfo'
    })
  },
  methods: {
    ...mapActions({
      gitlabGetFileHistoryList: 'gitlab/getFileHistoryList'
    }),
    getHistoryList(page, perPage) {
      let projectPath = _.get(this.activePageInfo, 'sitepath')
      let filePath = _.get(this.activePageInfo, 'fullPath')
      this.isBusy = true
      return new Promise(async resolve => {
        let result = await this.gitlabGetFileHistoryList({
          projectPath,
          filePath,
          page,
          perPage
        }).catch()
        this.historyList = _.concat(this.historyList, result.commits)
        if (result.total > this.historyList.length) {
          this.isBusy = false
        }
        resolve()
      })
    },
    getHistoryContent(history) {
      let version = history.version
      let commitId = history.short_id
      this.activeVersion = version
      this.$emit('selectHistory', { commitId, version })
    },
    async loadMore() {
      await this.getHistoryList(this.nowPage++, this.perPage)
      !this.activeVersion && this.getHistoryContent(this.historyList[0])
    },
    getHoverMessage(history) {
      let commitMessage = history.message
      let index = commitMessage.indexOf(SourceVersionStr)
      if (index == -1) {
        return
      } else {
        let sourceVersion = commitMessage.substring(
          index + SourceVersionStr.length
        )
        let nowVersion = history.version
        return this.$t('editor.versionRecoverFrom', {
          nowVersion,
          sourceVersion
        })
      }
    }
  },
  filters: {
    formatTime(time) {
      return moment(time).format('YYYY/MM/DD HH:mm')
    },
    sourceVersionFilter(commitMessage) {
      let index = commitMessage.indexOf(SourceVersionStr)
      return index != -1
        ? '(' + commitMessage.substring(index + SourceVersionStr.length) + ')'
        : ''
    },
    oldNameFilter(name) {
      return _.replace(name, /^(gitlab_rls_|gitlab_www_|gitlab_test_)/, '')
    }
  }
}
</script>
<style lang="scss">
.history-list {
  padding: 16px 0;
  height: 100%;
  &-header {
    display: flex;
    padding: 8px 20px 16px;
    font-size: 14px;
    &-version {
      width: 80px;
    }
    &-username {
      flex: 1;
      padding: 0 8px;
    }
    &-date {
      width: 112px;
      text-align: center;
    }
  }
  &-item {
    font-size: 14px;
    color: #241c17;
    display: flex;
    height: 40px;
    line-height: 40px;
    padding: 0 20px;
    cursor: pointer;
    &:hover {
      background-color: #f3f6f9;
    }
    &-active {
      background-color: #d4e8fb;
    }
    &-version {
      width: 80px;
      &-sub {
        color: #909399;
      }
    }
    &-username {
      flex: 1;
      padding: 0 8px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    &-date {
      width: 112px;
      text-align: center;
      white-space: nowrap;
    }
  }
}
</style>

<template>
  <div class='property-manager-container' v-if='hasActiveMod'>
    <div class="property-manager-container-back" v-if='hasActiveSubMod' @click='backFromSubMod'>
      <i class="el-icon-arrow-left"></i>{{$t('card.back')}}
    </div>
    <el-tabs :class="{'property-manager-container-tab-no-title': hasActiveSubMod}" v-model='activeTab' @tab-click='tabClickHandle'>
      <el-tab-pane :label='$t("editor.modAttr")' name='attr'>
        <div class="currentModTilte">{{$t("modList."+currentModLabel)}}</div>
        <prop-type-card v-for="(prop, key) in editingProps" :componentName='key' :prop='BaseCompProptypes[prop]' :key='key' :cardKey='key' :cardValue='cardValues(key)' :activePropertyOptions='activePropertyOptions' :isCardActive='key === activeProperty'></prop-type-card>
      </el-tab-pane>
      <el-tab-pane :label='$t("editor.modStyle")' name='style' v-if="styleTabEnabled">
        <div class="currentModTilte">{{$t("modList."+currentModLabel)}}</div>
        <div class='styles-container'>
          <style-selector v-if="activePropertyTabType === 'style'" :mod='activeMod' />
        </div>
      </el-tab-pane>
      <!-- <el-tab-pane label='Theme'>
        <div class='styles-container'>
          <theme-selector />
        </div>
      </el-tab-pane> -->
    </el-tabs>
  </div>
</template>

<script>
import _ from 'lodash'
import scrollIntoView from 'scroll-into-view-if-needed'
import { mapGetters, mapActions } from 'vuex'
import { StyleSelector, ThemeSelector } from '@/components/adi/selector'
import modLoader from '@/components/adi/mod'
import BaseCompProptypes from '@/components/adi/common/comp.proptypes'
import PropTypeCard from '@/components/editor/PropTypeCard'

export default {
  name: 'ModPropertyManager',
  data: () => ({
    editable: true,
    BaseCompProptypes
  }),
  methods: {
    ...mapActions({
      setActivePropertyData: 'setActivePropertyData',
      deleteMod: 'deleteMod',
      setActivePropertyTabType: 'setActivePropertyTabType'
    }),
    updateActiveProperData() {
      // the data of the json_editor is in ini_data of the component
      let data = _.cloneDeep(_.get(this, ['$refs', 'editor', 'ini_data'], {}))
      this.setActivePropertyData({ data })
    },
    tabClickHandle(tabItem) {
      let activeName = tabItem.name
      this.activeName = activeName.name
      this.setActivePropertyTabType(activeName)
    },
    getPropType(prop) {
      return this.BaseCompProptypes[prop] || { data: 'subMod' }
    },
    modData(mod, key) {
      let modType = mod.modType
      let activeModDafaultDatas = modLoader.load(modType).properties
      let activeModDatas = { ...activeModDafaultDatas, ...mod.data }

      if (activeModDatas && typeof activeModDatas[key] == 'object') {
        _.forEach(activeModDatas[key], (itemA, keyA) => {
          if (typeof itemA == 'number') {
            activeModDatas[key][keyA] = String(itemA)
          }
        })

        return activeModDatas[key] || null
      }
    },
    cardValues(key) {
      return this.modData(this.activeSubMod || this.activeMod, key)
    },
    modProps(modType, modStyleID = 0) {
      let mod = modLoader.load(modType)
      let modComponents = mod.components
      let subMods = mod.subMods
      let currentStyle = mod.styles[modStyleID]
      let currentTemplate =
        mod.templates[currentStyle ? currentStyle.templateID || 0 : 0]

      let checkKeys = (item, thisProp) => {
        if (typeof item == 'object') {
          _.forEach(item, (itemA, keyA) => {
            checkKeys(itemA, thisProp)
          })
        } else if (item == thisProp.key) {
          thisProp.hasProp = true
        }
      }

      let filterModComponents = {}

      _.forEach(modComponents, (item, key) => {
        let thisProp = { key: key, hasProp: false }

        checkKeys(currentTemplate, thisProp)

        if (thisProp.hasProp) {
          if (Array.isArray(item)) {
            let componentID = 0

            if (currentStyle && currentStyle.componentID) {
              componentID = currentStyle.componentID
            }

            filterModComponents[key] = item[componentID] || ''
          } else {
            filterModComponents[key] = item
          }
        }
      })

      _.forEach(subMods, (item, key) => {
        filterModComponents[key] = item
      })

      return filterModComponents
    },
    backFromSubMod() {
      this.$store.dispatch('setActiveSubMod', null)
    }
  },
  watch: {
    activeProperty() {
      this.$nextTick(() => {
        let ele = document.querySelector('.prop-box.active')
        ele &&
          scrollIntoView(ele, {
            scrollMode: 'if-needed',
            behavior: 'smooth'
          })
      })
    }
  },
  computed: {
    activePropertyDataCopy() {
      return _.cloneDeep(this.activePropertyData)
    },
    ...mapGetters({
      activeMod: 'activeMod',
      activeSubMod: 'activeSubMod',
      activeProperty: 'activeProperty',
      activePropertyOptions: 'activePropertyOptions',
      activePropertyData: 'activePropertyData',
      hasActiveMod: 'activeMod',
      hasActiveSubMod: 'activeSubMod',
      hasActiveProperty: 'hasActiveProperty',
      activePropertyTabType: 'activePropertyTabType'
    }),
    currentModLabel() {
      return (
        this.activeMod.cmd.substring(0, 2).toLocaleLowerCase() +
        this.activeMod.cmd.substring(2)
      )
    },
    activeModProps() {
      let modType = 'Mod' + this.activeMod.cmd
      let modStyleID = this.activeMod.data.styleID || 0
      return this.modProps(modType, modStyleID)
    },
    activeSubModProps() {
      if (!this.activeSubMod) return
      let modType = this.activeSubMod.modType
      let modStyleID = this.activeSubMod.data.styleID || 0
      return this.modProps(modType, modStyleID)
    },
    editingProps() {
      return this.activeSubModProps || this.activeModProps
    },
    activeTab: {
      get() {
        return this.activePropertyTabType || 'attr'
      },
      set() {}
    },
    styleTabEnabled() {
      return !this.hasActiveSubMod && this.activeMod.cmd !== 'Markdown'
    }
  },
  components: {
    StyleSelector,
    ThemeSelector,
    PropTypeCard
  }
}
</script>
<style lang="scss">
.property-manager-container {
  min-height: 100%;
  background-color: #e9f5ff;
  padding: 0 18px;
  position: relative;
  &-back {
    font-size: 16px;
    color: #333;
    cursor: pointer;
    padding: 28px 0 24px 0;
    .el-icon-arrow-left {
      font-size: 18px;
      vertical-align: bottom;
      margin-right: 4px;
    }
    &:hover {
      color: #3ba4ff;
    }
  }
  &-tab-no-title {
    .el-tabs__header {
      display: none;
    }
  }
  > .el-tabs > .el-tabs__header {
    .el-tabs__nav-wrap.is-scrollable {
      padding: 0;
      .el-tabs__nav-prev,
      .el-tabs__nav-next {
        display: none !important;
      }
    }
    .el-tabs__nav {
      margin: 22px 0;
      .el-tabs__active-bar {
        width: 0;
        height: 0;
      }
      .el-tabs__item {
        height: 30px;
        width: 198px;
        text-align: center;
        line-height: 30px;
        margin: 0 12px 0 0;
        background-color: #fff;
        box-shadow: 3px 3px 5px #ccc;
        border-radius: 4px;
        padding: 0;
      }
      .is-active {
        background-color: #3ba4ff;
        color: #fff;
      }
    }
  }
}
.property-manager-container .delete-mod {
  position: absolute;
  right: 18px;
  top: 10px;
  cursor: pointer;
  z-index: 1;
}
.property-manager-container .el-tabs__item {
  padding: 0 20px;
  font-size: 16px;
}
.currentModTilte {
  height: 30px;
  margin: 8px 18px;
  color: #505b65;
}
.el-tabs__nav-wrap::after {
  display: none;
}
@media (max-width: 1920px) {
  .property-manager-container
    > .el-tabs
    > .el-tabs__header
    .el-tabs__nav
    .el-tabs__item {
    width: 134px;
  }
}
</style>

<template>
  <el-row type='flex' class="full-height" @mousemove.native="dragMouseMove" @mouseup.native="dragMouseUp">
    <el-col class="mods-treeview" unselectable="on" :style="getTreeViewWidth">
      <el-tree ref='tree' node-key='id' :data='mods' :props='defaultProps' :default-expanded-keys='defaultExpandedKeys' highlight-current accordion :indent=0 @node-click='nodeMenuClick' @node-collapse='nodeCollapseHandle'></el-tree>
    </el-col>
    <div class="editor-resizer" @mousedown="resizeCol($event, 'treeViewWidth', 'previewBoxViewWidth', 570)"></div>
    <el-col class="preview-box" unselectable="on" :style="getPreviewBoxWidth">
      <div v-for='mod in activeModsList' :key='mod.name' class="box-items">
        <div v-if='!style.useImage' v-for='(style, index) in mod.styles' :key='style.name' class="style-cover render box-items-item" @click='newMod(mod.name, index)'>
          <div class="render-mod-container--click-prevent"></div>
          <div class="render-mod-container" :style="getSettingStyle(style)">
            <component class="render-mod" :is='mod.mod' :renderMode='true' :mod='modFactory(mod)' :conf='modConf(mod, index)' :theme='theme'></component>
            <div class="style-mask">
              <span>{{$t('tips.clickToAdd')}}</span>
            </div>
          </div>
        </div>
        <div class="style-cover box-items-item" v-if='style.useImage' v-for='(style, index) in mod.styles' :key='style.name'>
          <img class="style-cover-image" :src="style.cover" alt="" @click='newMod(mod.name, index)'>
          <div class="style-mask">
            <span>{{$t('tips.clickToAdd')}}</span>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import mods from '@/components/adi/mod/modslist.config'
import modFactory from '@/lib/mod/factory'
import themeFactory from '@/lib/theme/theme.factory'
import { mapGetters } from 'vuex'
import _ from 'lodash'
import resize from './base/resize'
import { setTimeout } from 'timers'
export default {
  name: 'ModsList',
  mixins: [resize],
  mounted() {
    this.updateModListTitle()
    let self = this
    function i18n(data) {
      _.forEach(data, (item, key) => {
        item.label = self.$t(item.label)
        if (item.children) {
          i18n(item.children)
        }
      })
    }
    i18n(mods)
    if (mods[0].children) {
      let modsChildren = mods[0].children[0]
      this.$refs.tree.setCurrentNode(modsChildren)
      this.activeModsList = modsChildren.mods
    } else {
      this.$refs.tree.setCurrentNode(mods[0])
      this.activeModsList = mods[0].mods
    }

    if (window.innerWidth <= 1920) {
      ;(this.treeViewWidth = 48.5), (this.previewBoxViewWidth = 51.5)
    } else {
      ;(this.treeViewWidth = 30), (this.previewBoxViewWidth = 70)
    }
  },
  async updated() {
    if (!this.resizeWinParams.isResizing) {
      await this.$nextTick()
      await this.$nextTick()
      this.autoResizePreview()
    }
  },
  data() {
    return {
      mods,
      activeModsList: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      defaultExpandedKeys: ['1-1'],
      selectedModKey: null,
      treeViewWidth: 48.5,
      previewBoxViewWidth: 51.5
    }
  },
  computed: {
    ...mapGetters({
      activeMod: 'activeMod',
      themeConf: 'themeConf',
      preModKey: 'preModKey'
    }),
    theme() {
      let globalTheme = themeFactory.generate(this.themeConf)
      globalTheme.sheet.attach()
      return globalTheme
    },
    getTreeViewWidth() {
      const style = {}

      if (this.treeViewWidth < 11) {
        this.treeViewWidth = 11
      }

      style.width = this.treeViewWidth + '%'

      return style
    },
    getPreviewBoxWidth() {
      const style = {}

      if (this.previewBoxViewWidth > 89) {
        this.previewBoxViewWidth = 89
      }

      style.width = this.previewBoxViewWidth + '%'
      return style
    }
  },
  methods: {
    updateModListTitle() {
      setTimeout(() => {
        let data = this.$refs.tree.$el.children
        _.forEach(data, (item, key) => {
          _.forEach(item.children, (item2, key2) => {
            if (key2 == 0) {
              item2.title = mods[key].label
            }
            _.forEach(item2.children, (item3, key3) => {
              if (mods[key].children[key3]) {
                item3.title = mods[key].children[key3].label
              }
            })
          })
        })
      }, 0)
    },
    getSettingStyle(style) {
      if (!style || !style.renderMinHeight) {
        return ''
      }
      return `min-height: ${style.renderMinHeight}`
    },
    generateStyleString(style) {
      let string = ''
      if (style) {
        _.forEach(style, (value, key) => {
          string = string + key + ':' + value + ';'
        })
      }
      return string
    },
    nodeMenuClick(data) {
      this.updateModListTitle()
      if (data.children && data.children.length > 0) {
        return
      }
      this.activeModsList = data.mods
    },
    nodeCollapseHandle(data, node, comp) {},
    newMod(name, index) {
      this.$store.dispatch('addMod', {
        modName: name,
        preModKey: this.preModKey || (this.activeMod && this.activeMod.key),
        styleID: index
      })
    },
    modFactory(mod) {
      if (mod.name && mod.name != 'ModMarkdown') {
        return modFactory.generateProperties(mod.name)
      }
    },
    modConf(mod, index) {
      let currentMod = _.merge({}, mod)
      currentMod.properties.styleID = index
      return currentMod
    },
    autoResizePreview() {
      if (this.updatedHeight) {
        return false
      }
      this.updatedHeight = true
      let all = this.$el.querySelectorAll('[class="render-mod-container"]')
      let refactor = 0
      if (window.innerWidth <= 1920) {
        refactor = 0.1245
      } else {
        refactor = 0.254
      }
      _.forEach(all, (dom, key) => {
        dom.style.height = dom.offsetHeight * refactor + 'px'
      })
      setTimeout(() => {
        this.updatedHeight = null
      }, 0)
    }
  }
}
</script>

<style lang="scss" scoped>
.full-height {
  height: 100%;
  .editor-resizer {
    width: 3px;
    background-color: #c0c4cc;
    cursor: col-resize;
  }
}
.box-items {
  img {
    display: block;
  }
}
.style-cover {
  position: relative;
  width: 275px;
  cursor: pointer;
  display: block;
  margin: auto;
  margin-bottom: 12px;
  border: 2px solid transparent;
  padding: 10px;
  background-color: white;
  &-image {
    width: 100%;
  }
}
.style-mask {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 14px;
  width: 275px;
  padding: 6px 10px;
  color: #ffffff;
  text-align: center;
  font-size: 12px;
  background: rgba(144, 167, 191, 0.5);
  opacity: 0;
}
.box-items-item:hover {
  .style-mask {
    opacity: 1;
  }
}
.style-cover:hover {
  border: 2px solid #bcbcbc;
}
.mods-treeview {
  // border-right: 2px solid #c0c4cc;
  // flex-basis: 135px;
  // max-width: 135px;
  flex-shrink: 0;
  flex-grow: 0;
  user-seletct: none;
}
.preview-box {
  padding: 0 5px;
  background-color: #e4e7ed;
  max-height: 100%;
  overflow: auto;
}
.render {
  background-color: white;
  overflow: hidden;
  margin-bottom: 12px;
  position: relative;
  .render-mod-container--click-prevent {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
  .render-mod-container {
    width: 272px;
    overflow: hidden;
    .render-mod {
      max-width: unset;
      width: 1080px;
      transform: scale(0.254);
      transform-origin: top left;
      position: unset;
    }
  }
}
@media screen and (max-width: 1920px) {
  .style-cover {
    width: 135px;
    padding: 8px;
  }
  .render {
    .render-mod-container {
      width: 135px;
      .render-mod {
        transform: scale(0.1245);
      }
    }
  }
  .style-mask {
    width: 135px;
  }
}
</style>

<style>
.mods-treeview .el-tree-node__content > .el-tree-node__expand-icon {
  padding-left: 15px;
}
.mods-treeview .el-tree-node__content > .el-tree-node__expand-icon.expanded {
  padding: 15px;
  margin-right: -9px;
}
.mod.mods-treeview
  .el-tree-node__content
  > .el-tree-node__expand-icon.expanded {
  padding: 6px;
  padding-top: 15px;
}
.mods-treeview
  .el-tree--highlight-current
  .el-tree-node.is-current
  > .el-tree-node__content {
  background-color: #e6f7ff;
  position: relative;
}
.mods-treeview .el-tree-node__content {
  height: 40px;
  line-height: 40px;
}
.mods-treeview .el-tree-node > .el-tree-node__content {
  font-weight: 900;
  color: #000;
}
.mods-treeview
  .el-tree-node
  .el-tree-node__children
  .el-tree-node
  > .el-tree-node__content {
  color: #a9a9a9;
  font-weight: 400;
}
.mods-treeview
  .el-tree-node
  .el-tree-node__children
  .el-tree-node
  > .el-tree-node__content:hover {
  color: #000;
}
.mods-treeview .el-tree-node__label {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>

<template>
  <div class='page-setting' v-loading='loading'>
    <div class="page-setting-top">
      <h1 class="top-path" :title="barePath">{{ barePath }}</h1>
      <i class="el-icon-close" @click="changeView('FileManager')"></i>
    </div>
    <div class="page-setting-item">
      <label class="page-setting-label" for="pageDisplayName">{{$t('editor.pageTitle')}}:</label>
      <el-input size="small" v-model="pageDisplayName" @blur="savePageDisplayName"></el-input>
      <span class="el-form-item__error" v-show="displayNameError">{{displayNameError}}</span>
    </div>
    <div class="page-setting-item">
      <label class="page-setting-label">{{$t('editor.pageLayout')}}:</label>
      <div class="page-setting-select">
        <el-select size="small" v-model="selectedLayoutId" filterable @change="selectPageLayout">
          <el-option v-for="(layout) in userSiteLayoutsMap" :key="layout.id" :label="layout.name" :value="layout.id">
          </el-option>
        </el-select>
      </div>
    </div>
    <div class='page-setting-selected-style'>
      <component :is='selectedStyleComponent'>
        <div slot='header'>{{$t('editor.header')}}</div>
        <div slot='footer'>{{$t('editor.footer')}}</div>
        <div slot='sidebar'>{{$t('editor.aside')}}</div>
        {{$t('editor.main')}}
      </component>
    </div>
    <div class="layoutManagerBtnWrap" @click="openWebsiteSettingDialog">
      <el-button class="layoutManagerBtn" type="primary" size="small">{{$t('editor.layoutManagement')}}</el-button>
    </div>
    <div @click.stop v-if='isWebsiteSettingShow'>
      <website-setting-dialog :activeIndex="1" :show='isWebsiteSettingShow' :sitePath='currentPath' @close='closeWebsiteSettingDialog' />
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapGetters, mapActions } from 'vuex'
import stylesList from '@/components/adi/layout/templates'
import { getPageInfoByPath } from '@/lib/utils/gitlab'
import WebsiteSettingDialog from '@/components/common/WebsiteSettingDialog'

export default {
  name: 'PageSetting',
  props: {
    pagePath: String
  },
  data() {
    return {
      loading: true,
      selectedLayoutId: '',
      isWebsiteSettingShow: false,
      pageDisplayName: '',
      displayNameError: ''
    }
  },
  async activated() {
    await Promise.all([
      this.gitlabGetRepositoryTree({ path: this.sitePath }),
      this.userGetSiteLayoutConfig({ path: this.sitePath })
    ]).catch(e => {
      console.error(e)
    })
    this.selectedLayoutId = this.settedPageLayoutId || this.defaultLayoutId
    this.pageDisplayName = this.settedPageDisplayName
    this.loading = false
  },
  computed: {
    ...mapGetters({
      userSiteLayoutConfigBySitePath: 'user/siteLayoutConfigBySitePath',
      userGetSettedPageLayoutByPath: 'user/getSettedPageLayoutByPath'
    }),
    currentPath() {
      let pathArr = this.pageInfo.barePath.split('/')
      let path = []
      path.push(pathArr[0])
      path.push(pathArr[1])
      return path.join('/')
    },
    pageInfo() {
      return getPageInfoByPath(this.pagePath)
    },
    sitePath() {
      return this.pageInfo.sitepath
    },
    barePath() {
      let index = this.pageInfo.barePath.indexOf('/')
      return this.pageInfo.barePath.substr(index + 1)
    },
    relativePath() {
      return this.pageInfo.relativePath
    },
    defaultLayoutId() {
      return _.get(
        this.userSiteLayoutConfig,
        ['layoutConfig', 'defaultLayoutId'],
        ''
      )
    },
    userSiteLayoutConfig() {
      return this.userSiteLayoutConfigBySitePath(this.sitePath)
    },
    userSiteLayoutsMap() {
      return _.keyBy(
        _.filter(
          _.get(this.userSiteLayoutConfig, ['layoutConfig', 'layouts'], []),
          o => !o.deleted
        ),
        'id'
      )
    },
    settedPageLayout() {
      return this.userGetSettedPageLayoutByPath(this.pagePath)
    },
    settedPageLayoutId() {
      return _.get(this.settedPageLayout, 'id', '')
    },
    settedPageDisplayName() {
      return _.get(
        this.userSiteLayoutConfig,
        ['pages', this.relativePath, 'displayName'],
        ''
      )
    },
    selectedLayout() {
      return this.userSiteLayoutsMap[this.selectedLayoutId]
    },
    selectedStyleComponent() {
      return _.get(
        stylesList[_.get(this.selectedLayout, 'styleName', 'basic')],
        'component'
      )
    }
  },
  methods: {
    ...mapActions({
      userGetSiteLayoutConfig: 'user/getSiteLayoutConfig',
      userSaveSiteLayoutConfig: 'user/saveSiteLayoutConfig',
      gitlabGetRepositoryTree: 'gitlab/getRepositoryTree',
      setActiveManagePaneComponent: 'setActiveManagePaneComponent'
    }),
    changeView(type) {
      this.setActiveManagePaneComponent(type)
    },
    async savePageDisplayName() {
      this.pageDisplayName = _.trim(this.pageDisplayName)
      if (this.settedPageDisplayName === this.pageDisplayName) return
      if (this.pageDisplayName.length > 50) {
        this.displayNameError = this.$t('editor.setPageDisplayNameError')
        return
      }
      this.loading = true
      let payload = {
        sitePath: this.sitePath,
        pages: {
          [this.relativePath]: {
            displayName: this.pageDisplayName,
            layout: this.settedPageLayoutId || this.defaultLayoutId
          }
        }
      }
      await this.userSaveSiteLayoutConfig(payload).catch(e => console.error(e))
      this.displayNameError = ''
      this.loading = false
    },
    async selectPageLayout() {
      if (this.settedPageLayoutId == this.selectedLayoutId) return

      this.loading = true
      let payload = {
        sitePath: this.sitePath,
        pages: {
          [this.relativePath]: {
            layout: this.selectedLayoutId
          }
        }
      }
      await this.userSaveSiteLayoutConfig(payload).catch(e => console.error(e))
      this.loading = false
    },
    openWebsiteSettingDialog() {
      this.isWebsiteSettingShow = true
    },
    closeWebsiteSettingDialog() {
      this.isWebsiteSettingShow = false
    }
  },
  components: {
    WebsiteSettingDialog
  }
}
</script>

<style lang="scss">
.page-setting {
  padding: 20px;
  &-item {
    margin-bottom: 40px;
    position: relative;
  }
  &-label {
    font-size: 14px;
    color: #535353;
    margin-bottom: 10px;
    display: inline-block;
  }
}
.page-setting-top {
  position: relative;
  .top-path {
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 0 0 42px;
    padding-right: 30px;
  }
  i {
    position: absolute;
    right: 0px;
    top: -2px;
    font-size: 22px;
    cursor: pointer;
  }
}
.page-setting-select {
  text-align: center;
  .el-select {
    width: 100%;
  }
}
.layoutManagerBtnWrap {
  width: 270px;
  margin: auto;
  .layoutManagerBtn {
    width: 100%;
    margin: 0 auto;
    border-radius: 32px;
  }
}
.page-setting-selected-style {
  margin: 20px auto;
  width: 270px;
  height: 150px;
  // border: 5px solid #1989FA;
  .el-header,
  .el-footer,
  .el-aside,
  .el-main {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .el-header,
  .el-footer {
    background: #b3c0d1 !important;
  }
  .el-aside {
    max-width: 50px !important;
    background: #d3dce6 !important;
  }
  .el-main {
    background: #e4eef3;
  }
  .maxwidth-template {
    .el-main {
      margin: 0 !important;
      border-left: 40px solid white;
      border-right: 40px solid white;
    }
  }
  .fullscreen-template {
    &-max-width {
      border: 40px solid #fff;
      border-width: 0 40px;
    }
  }
  .content-max-width-template {
    border: 40px solid #fff;
    border-width: 0 40px;
  }
}
</style>

<template>
  <div class="prop-box" :class="{'active': isCardActive, 'card-only-title': !isCardShow}">
    <el-row v-show="isCardHeaderShow" class="prop-header" type='flex' justify='space-between'>
      <el-col>
        {{$t("card." + cardKey)}}
      </el-col>
      <el-tooltip v-if="cardKey == 'menu' || cardKey == 'board' || cardKey == 'comment' || cardKey == 'qq'" :content="tipTool()" popper-class="prop-header-tooltip-class" placement="top">
        <i class="iconfont icon-help"></i>
      </el-tooltip>
      <el-tooltip v-if="cardKey == 'md'" popper-class="prop-header-tooltip-class" placement="top">
        <i class="iconfont icon-help"></i>
        <div slot="content"><span v-html="tipTool()"></span></div>
      </el-tooltip>
      <el-col class="card-info">
        <el-tooltip :content="$t('editor.enlargeMdEditing')" placement="top">
          <i v-show="isMultiLineProp" class="iconfont icon-full-screen_" @click='showMultiTextDailog'></i>
        </el-tooltip>
        <el-tooltip :content="isToolTip" placement="top">
          <el-switch :width='32' v-model="isCardShow" active-color="#3ba4ff" inactive-color='#bfbfbf' @change='toggleModVisible'></el-switch>
        </el-tooltip>
      </el-col>
    </el-row>
    <el-row class="prop-item" v-show="isCardShow" :prop='prop' v-for='(propItem, index) in prop' :key='index'>
      <component :is='getPropType(propItem)' :prop='prop' :optionsData='optionsData' :editingKey='index' :originValue='cardValue[index]' :cardValue='cardValue' :cardKey='cardKey' :activePropertyOptions='activePropertyOptions' @onPropertyChange='changePropertyData' @onChangeValue='changeActiveProperty'></component>
    </el-row>
  </div>
</template>
<script>
import proptypes from '@/components/proptypes'
import { mapGetters, mapActions } from 'vuex'
import modLoader from '@/components/adi/mod'
import BaseCompProptypes from '@/components/adi/common/comp.proptypes'
import _ from 'lodash'

export default {
  name: 'PropTypeCard',
  props: {
    cardKey: String,
    cardValue: Object,
    prop: Object,
    componentName: String,
    activePropertyOptions: Object,
    isCardActive: Boolean
  },
  mounted() {
    this.isCardShow = this.cardValue && !this.cardValue.hidden
  },
  data() {
    return {
      isCardShow: undefined,
      proptypes,
      BaseCompProptypes
    }
  },
  computed: {
    ...mapGetters({
      activeMod: 'activeMod',
      activeSubMod: 'activeSubMod'
    }),
    isCardHeaderShow() {
      return this.cardKey !== 'list'
    },
    isToolTip() {
      if (this.isCardShow) {
        return this.$t('tips.clickToHide')
      } else {
        return this.$t('tips.clickToShow')
      }
    },
    optionsData() {
      if (
        !this.activeMod ||
        !this.activeMod.modType ||
        !this.activeMod.data ||
        !this.activeMod.data.styleID === ''
      ) {
        return {}
      }
      let modConf = modLoader.load(this.activeMod.modType)

      if (!modConf || !modConf.styles) {
        return {}
      }
      let currentStyle = modConf.styles[this.activeMod.data.styleID]

      if (
        !currentStyle ||
        !currentStyle.options ||
        !currentStyle.options.config
      ) {
        return {}
      }

      return currentStyle.options.config[this.componentName]
    },
    isMultiLineProp() {
      let propKeys = _.keys(this.prop)
      let multipleLineProps = _.filter(propKeys, propItem => {
        return this.prop[propItem] === 'autoSizeInput'
      })
      return multipleLineProps.length > 0
    }
  },
  methods: {
    getPropType(prop) {
      return this.proptypes[prop]
    },
    ...mapActions({
      setActiveProperty: 'setActiveProperty',
      setActivePropertyData: 'setActivePropertyData',
      setIsMultipleTextDialogShow: 'setIsMultipleTextDialogShow'
    }),
    changeActiveProperty() {
      this.setActiveProperty({
        key: this.activeMod.key,
        property: this.cardKey
      })
    },
    changePropertyData(changedData) {
      if (!this.changeProtyDataThrottle) {
        this.changeProtyDataThrottle = _.throttle(changedData => {
          this.changeActiveProperty()
          this.setActivePropertyData({
            data: changedData
          })
        }, 100)
      }

      this.changeProtyDataThrottle(changedData)
    },
    toggleModVisible(value) {
      this.changePropertyData({
        hidden: !value
      })
    },
    showMultiTextDailog() {
      this.changePropertyData(this.cardValue)
      this.setIsMultipleTextDialogShow({
        isShow: true
      })
    },
    tipTool() {
      return this.$t('help.' + this.cardKey)
    }
  },
  watch: {
    cardValue() {
      this.isCardShow = this.cardValue && !this.cardValue.hidden
    }
  }
}
</script>
<style lang="scss" scoped>
.prop-box {
  background-color: #fff;
  padding: 25px 18px;
  margin-bottom: 12px;
  border: 2px solid transparent;
}
.prop-box.active {
  border: 2px solid #3da4fd;
}
.card-only-title {
  padding: 16px 18px;
}
.card-only-title .prop-header {
  margin-bottom: 0;
}
.prop-header {
  margin-bottom: 12px;
  font-size: 16px;
  color: #3ba4ff;
}
.card-info {
  width: auto;
  white-space: nowrap;
  .iconfont {
    vertical-align: middle;
    color: #333;
    margin-right: 10px;
    cursor: pointer;
  }
}
.icon-help {
  line-height: 23px;
  margin-right: 10px;
  color: #4d90fe;
  height: 16px;
  width: 16px;
}
</style>
<style>
.prop-header-tooltip-class {
  max-width: 215px;
}
</style>

<template>
  <h2>搜索与替换功能</h2>
</template>
<script>
export default {
  name: 'Search'
}
</script>

export default {
  data() {
    return {
      bodyWidth: document.body.clientWidth,
      resizeWinParams: {
        mouseStartX: 0,
        isResizing: false,
        leftColWidthParam: '',
        rightColWidthParam: ''
      }
    }
  },
  methods: {
    resizeCol(event, leftColWidthParam, rightColWidthParam, rate) {
      if (!(event && event.clientX)) {
        return
      }

      this.rate = rate || 100
      this.resizeWinParams.isResizing = true
      this.resizeWinParams.mouseStartX = event.clientX

      if (this.showAngle) {
        this.resizeWinParams.leftColWidthParam = rightColWidthParam
        this.resizeWinParams.rightColWidthParam = leftColWidthParam
      } else {
        this.resizeWinParams.leftColWidthParam = leftColWidthParam
        this.resizeWinParams.rightColWidthParam = rightColWidthParam
      }
    },
    dragMouseMove(event) {
      if (!(this.resizeWinParams.isResizing && event && event.clientX)) {
        return
      }

      let mouseNowX = event.clientX
      let diffClientX = mouseNowX - this.resizeWinParams.mouseStartX
      let diffPercent = (diffClientX / this.bodyWidth) * (this.rate || 100)
      this.resizeWinParams.mouseStartX = mouseNowX
      let leftColName = this.resizeWinParams.leftColWidthParam
      let rightColName = this.resizeWinParams.rightColWidthParam

      this[leftColName] = this[leftColName] + diffPercent
      this[rightColName] -= diffPercent
    },
    dragMouseUp() {
      this.resizeWinParams.isResizing = false
      this.resizeWinParams.leftColWidthParam = ''
      this.resizeWinParams.rightColWidthParam = ''
    }
  }
}



```