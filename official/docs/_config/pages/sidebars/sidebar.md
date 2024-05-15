```@Menu
styleID: 18
menu:
  data:
    - name: 新手指引
      nameInputShow: false
      link: 'https://keepwork.com/official/docs/newuser'
      linkInputShow: false
    - name: 导师培训课
      link: 'https://keepwork.com/official/docs/teach/lessons/index'
      nameInputShow: false
      linkInputShow: false
    - name: 看视频，学Paracraft
      link: 'https://keepwork.com/official/docs/videoguide'
      nameInputShow: false
      linkInputShow: false
      child:
        - _key: 3-1
          _parentKeys: &ref_0
            - '3'
          name: 新手教学视频
          link: 'https://keepwork.com/official/docs/videos/new_user_video'
          nameInputShow: false
          linkInputShow: false
        - _key: 3-2
          _parentKeys: *ref_0
          name: 实例教学视频
          link: 'https://keepwork.com/official/docs/videos/operation_video'
          nameInputShow: false
          linkInputShow: false
        - _key: 3-3
          _parentKeys: *ref_0
          name: 教学视频大全80集
          link: 'https://keepwork.com/official/paracraft/VideoTutorials'
          nameInputShow: false
          linkInputShow: false
        - _key: 3-4
          _parentKeys: *ref_0
          name: 推荐用户作品100集
          link: 'http://www.paracraft.cn/videos'
          nameInputShow: false
          linkInputShow: false
        - _key: 3-5
          _parentKeys: *ref_0
          name: NPL编程基础理论教学10集
          link: 'https://keepwork.com/intro/keepwork/NPLCAD'
          nameInputShow: false
          linkInputShow: false
        - _key: 3-6
          _parentKeys: *ref_0
          name: 300集教学短视频
          link: 'https://keepwork.com/official/docs/tips/all_tips'
          nameInputShow: false
          linkInputShow: false
      defaultOpen: false
    - name: Paracraft使用手册
      link: 'https://keepwork.com/official/docs/UserGuide/intro/preface'
      nameInputShow: false
      linkInputShow: false
      child:
        - _key: 4-1
          _parentKeys: &ref_1
            - '4'
          name: 1.0 如何学习Paracraft
          link: 'https://keepwork.com/official/docs/UserGuide/intro/how_to_learn'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-1-1
              _parentKeys:
                - '4'
                - 4-1
              name: 安装Paracraft和编辑模式
              link: 'https://keepwork.com/official/docs/UserGuide/intro/install'
              nameInputShow: false
              linkInputShow: false
        - _key: 4-2
          _parentKeys: *ref_1
          name: 1.1 几何相似与构建相似的虚拟世界
          link: 'https://keepwork.com/official/docs/UserGuide/scene/intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-2-1
              _parentKeys: &ref_2
                - '4'
                - 4-2
              name: 创建方块
              link: 'https://keepwork.com/official/docs/UserGuide/scene/create_blocks'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-2
              _parentKeys: *ref_2
              name: 批量操作
              link: >-
                https://keepwork.com/official/docs/UserGuide/scene/batch_operation
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-3
              _parentKeys: *ref_2
              name: BMAX模型
              link: 'https://keepwork.com/official/docs/UserGuide/scene/bmax_model'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-4
              _parentKeys:
                - '4'
                - 4-2
              name: Voxel模型
              link: 'https://keepwork.com/official/docs/UserGuide/scene/voxelmodel'
              linkInputShow: false
              nameInputShow: false
            - _key: 4-2-4
              _parentKeys: *ref_2
              name: 方块材质
              link: >-
                https://keepwork.com/official/docs/UserGuide/scene/block_material
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-5
              _parentKeys: *ref_2
              name: 动态光源
              link: 'https://keepwork.com/official/docs/UserGuide/scene/lighting'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-6
              _parentKeys: *ref_2
              name: 文件格式
              link: 'https://keepwork.com/official/docs/UserGuide/scene/fileformat'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-7
              _parentKeys: *ref_2
              name: 导入与导出
              link: 'https://keepwork.com/official/docs/UserGuide/scene/import_export'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-2-8
              _parentKeys: *ref_2
              name: CAD计算机辅助设计
              link: 'https://keepwork.com/official/docs/CAD/intro'
              nameInputShow: false
              linkInputShow: false
        - _key: 4-3
          _parentKeys: *ref_1
          name: 1.2 虚拟人物与虚拟人物的运动
          link: 'https://keepwork.com/official/docs/UserGuide/animation/intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-3-1
              _parentKeys: &ref_3
                - '4'
                - 4-3
              name: 电影方块
              link: >-
                https://keepwork.com/official/docs/UserGuide/animation/movie_block
              nameInputShow: false
              linkInputShow: false
            - _key: 4-3-2
              _parentKeys: *ref_3
              name: 演员和动画
              link: 'https://keepwork.com/official/docs/UserGuide/animation/actor'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-3-3
              _parentKeys: *ref_3
              name: bmax简易骨骼与X文件应用
              link: 'https://keepwork.com/official/docs/UserGuide/animation/xfile'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-3-4
              _parentKeys: *ref_3
              name: 物理仿真
              link: 'https://keepwork.com/official/docs/UserGuide/animation/physics'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-3-5
              _parentKeys: *ref_3
              name: 自主人物动画
              link: >-
                https://keepwork.com/official/docs/UserGuide/animation/AutoAnimation
              nameInputShow: false
              linkInputShow: false
            - _key: 4-3-6
              _parentKeys: *ref_3
              name: 活动模型
              link: 'https://keepwork.com/official/docs/UserGuide/animation/LiveModel'
              nameInputShow: false
              linkInputShow: false
        - _key: 4-4
          _parentKeys: *ref_1
          name: 1.3 构建我的电影世界使他可持续发展
          link: 'https://keepwork.com/official/docs/UserGuide/moviemaking/intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-4-1
              _parentKeys: &ref_4
                - '4'
                - 4-4
              name: 电影方块与过山车
              link: >-
                https://keepwork.com/official/docs/UserGuide/moviemaking/roller_coaster
              nameInputShow: false
              linkInputShow: false
            - _key: 4-4-2
              _parentKeys: *ref_4
              name: 子母电影方块
              link: >-
                https://keepwork.com/official/docs/UserGuide/moviemaking/mother_block
              nameInputShow: false
              linkInputShow: false
            - _key: 4-4-3
              _parentKeys: *ref_4
              name: 方块动画
              link: >-
                https://keepwork.com/official/docs/UserGuide/moviemaking/block_animation
              nameInputShow: false
              linkInputShow: false
        - _key: 4-5
          _parentKeys: *ref_1
          name: 1.4 如何赋予虚拟人物智能？
          link: 'https://keepwork.com/official/docs/UserGuide/coding/intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-5-1
              _parentKeys: &ref_5
                - '4'
                - 4-5
              name: 代码方块
              link: 'https://keepwork.com/official/docs/UserGuide/coding/codeblock'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-2
              _parentKeys: *ref_5
              name: 代码方块教学1
              link: 'https://keepwork.com/official/docs/UserGuide/coding/codeblock1'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-3
              _parentKeys: *ref_5
              name: 代码方块教学2
              link: 'https://keepwork.com/official/docs/UserGuide/coding/codeblock2'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-4
              _parentKeys: *ref_5
              name: 双重机关与事件
              link: 'https://keepwork.com/official/docs/UserGuide/coding/mission'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-5
              _parentKeys: *ref_5
              name: 制作图形界面
              link: >-
                https://keepwork.com/official/docs/UserGuide/coding/graphic_interface
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-6
              _parentKeys: *ref_5
              name: 高级图形界面
              link: 'https://keepwork.com/official/docs/UserGuide/coding/mcml2'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-7
              _parentKeys: *ref_5
              name: 代码方块的输出
              link: 'https://keepwork.com/official/docs/UserGuide/coding/output'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-5-8
              _parentKeys: *ref_5
              name: 打字练习
              link: 'https://keepwork.com/official/docs/UserGuide/coding/learn_typing'
              nameInputShow: false
              linkInputShow: false
        - _key: 4-6
          _parentKeys: *ref_1
          name: 1.5 编程中的抽象建模
          link: 'https://keepwork.com/official/docs/UserGuide/abstract_modeling/intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-6-1
              _parentKeys: &ref_6
                - '4'
                - 4-6
              name: 了解编程思维
              link: >-
                https://keepwork.com/official/docs/UserGuide/abstract_modeling/abstract_modeling
              nameInputShow: false
              linkInputShow: false
            - _key: 4-6-2
              _parentKeys: *ref_6
              name: 3D世界的编程模型
              link: >-
                https://keepwork.com/official/docs/UserGuide/abstract_modeling/3dprogramming
              nameInputShow: false
              linkInputShow: false
            - _key: 4-6-3
              _parentKeys: *ref_6
              name: 电梯调度算法
              link: >-
                https://keepwork.com/official/docs/UserGuide/abstract_modeling/elevator
              nameInputShow: false
              linkInputShow: false
        - _key: 4-7
          _parentKeys: *ref_1
          name: 1.6 保存并分享你的作品
          link: 'https://keepwork.com/official/docs/UserGuide/share/keepwork_intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-7-1
              _parentKeys: &ref_7
                - '4'
                - 4-7
              name: 制作个人网站
              link: 'https://keepwork.com/official/docs/UserGuide/share/personalsite'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-7-2
              _parentKeys: *ref_7
              name: 创建课程
              link: 'https://keepwork.com/official/docs/UserGuide/share/createlessons'
              nameInputShow: false
              linkInputShow: false
            - _key: 4-7-3
              _parentKeys:
                - '4'
                - 4-7
              name: 发布到PPT文件
              link: 'https://keepwork.com/official/docs/UserGuide/share/ppt'
              linkInputShow: false
              nameInputShow: false
            - _key: 4-7-3
              _parentKeys: *ref_7
              name: 应用审核指南
              link: >-
                https://keepwork.com/official/docs/references/appstore/review_guideline
              nameInputShow: false
              linkInputShow: false
        - _key: 4-8
          _parentKeys:
            - '4'
          name: 1.7 脚本编程
          link: ''
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 4-8-1
              _parentKeys:
                - '4'
                - 4-8
              name: 调试
              link: 'https://keepwork.com/official/docs/UserGuide/coding/debug'
              nameInputShow: false
              linkInputShow: false
    - name: NPL基础编程理论
      link: 'https://keepwork.com/official/docs/NPL/index'
      nameInputShow: false
      linkInputShow: false
      child:
        - _key: 5-1
          _parentKeys: &ref_8
            - '5'
          name: 编程基本概念与语法
          link: 'https://keepwork.com/official/docs/NPL/syntax'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-2
          _parentKeys: *ref_8
          name: 程序的本质
          link: 'https://keepwork.com/official/docs/NPL/nature_of_program'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-3
          _parentKeys: *ref_8
          name: 数字与数学
          link: 'https://keepwork.com/official/docs/NPL/numbers'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-4
          _parentKeys: *ref_8
          name: 变量与名字
          link: 'https://keepwork.com/official/docs/NPL/names'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-5
          _parentKeys: *ref_8
          name: 字符串与文字
          link: 'https://keepwork.com/official/docs/NPL/strings'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-6
          _parentKeys: *ref_8
          name: 表与数组
          link: 'https://keepwork.com/official/docs/NPL/tables'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-7
          _parentKeys: *ref_8
          name: 函数
          link: 'https://keepwork.com/official/docs/NPL/functions'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-8
          _parentKeys: *ref_8
          name: 内置函数
          link: 'https://keepwork.com/official/docs/NPL/built_in_functions'
          nameInputShow: false
          linkInputShow: false
        - _key: 5-9
          _parentKeys: *ref_8
          name: 总结与对自学编程的建议
          link: 'https://keepwork.com/official/docs/NPL/suggestion'
          nameInputShow: false
          linkInputShow: false
    - name: 应用教程
      link: 'https://keepwork.com/official/docs/tutorials/index'
      nameInputShow: false
      linkInputShow: false
      child:
        - _key: 6-1
          _parentKeys: &ref_9
            - '6'
          name: 宏示教使用教程
          link: 'https://keepwork.com/official/docs/tutorials/macroplatform'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-2
          _parentKeys: *ref_9
          name: 网页宏示教
          link: 'https://keepwork.com/official/docs/tutorials/webmacro'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-3
          _parentKeys: *ref_9
          name: CAD建模教程
          link: 'https://keepwork.com/official/docs/CAD/tutorial'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-4
          _parentKeys: *ref_9
          name: 机器人基础介绍
          link: 'https://keepwork.com/official/docs/tutorials/robot_intro'
          nameInputShow: false
          linkInputShow: false
          child:
            - _key: 6-4-1
              _parentKeys:
                - '6'
                - 6-4
              name: 机器人教程
              link: 'https://keepwork.com/official/docs/tutorials/robot_design'
              nameInputShow: false
              linkInputShow: false
        - _key: 6-5
          _parentKeys: *ref_9
          name: VR虚拟展厅
          link: 'https://keepwork.com/official/docs/tutorials/webXR'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-6
          _parentKeys: *ref_9
          name: 导出360全景视频
          link: 'https://keepwork.com/official/docs/tutorials/vr360'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-7
          _parentKeys: *ref_9
          name: 创建智能模组
          link: 'https://keepwork.com/official/docs/tutorials/AgentSignBlock'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-8
          _parentKeys: *ref_9
          name: 自定义代码方块
          link: 'https://keepwork.com/official/docs/tutorials/custom_codeblock'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-9
          _parentKeys: *ref_9
          name: 可计算文档
          link: 'https://keepwork.com/official/docs/tutorials/keepwork'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-10
          _parentKeys: *ref_9
          name: 制作ChatGPT机器人
          link: 'https://keepwork.com/official/docs/tutorials/chatgpt'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-11
          _parentKeys: *ref_9
          name: 物联网服务器
          link: 'https://keepwork.com/official/docs/tutorials/iot_mqtt'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-12
          _parentKeys: *ref_9
          name: mpython硬件
          link: 'https://keepwork.com/official/docs/tutorials/micropython'
          nameInputShow: false
          linkInputShow: false
        - name: 蓝牙通讯
          link: 'https://keepwork.com/official/docs/tutorials/bluetooth'
          linkInputShow: false
          nameInputShow: false
        - _key: 6-13
          _parentKeys: *ref_9
          name: 虚仿课程制作入门
          link: 'https://keepwork.com/official/docs/tutorials/makelesson'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-14
          _parentKeys: *ref_9
          name: 课程相关模组
          link: 'https://keepwork.com/official/docs/tutorials/lessonMods'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-15
          _parentKeys: *ref_9
          name: Entity管理器
          link: 'https://keepwork.com/official/docs/tutorials/EntityManager'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-16
          _parentKeys: *ref_9
          name: 摄像头
          link: 'https://keepwork.com/official/docs/tutorials/camera'
          nameInputShow: false
          linkInputShow: false
        - _key: 6-17
          _parentKeys: *ref_9
          name: 发布独立应用
          link: 'https://keepwork.com/official/docs/tutorials/makeapp'
          nameInputShow: false
          linkInputShow: false
    - name: 参考资料
      link: ''
      nameInputShow: false
      child:
        - _key: 7-1
          _parentKeys: &ref_10
            - '7'
          name: 《NPL常用语法》速查表
          link: 'https://keepwork.com/official/docs/references/npl_quick_ref'
          nameInputShow: false
          linkInputShow: false
          child: []
        - _key: 7-2
          _parentKeys: *ref_10
          name: NPL语言英文官网
          link: 'https://github.com/LiXizhi/NPLRuntime/wiki'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-3
          _parentKeys: *ref_10
          name: 《代码方块》函数速查表
          link: 'https://keepwork.com/official/docs/references/codeblock_quick_ref'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-4
          _parentKeys: *ref_10
          name: Paracraft命令列表
          link: 'https://keepwork.com/official/paracraft/docs/AllCommands'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-5
          _parentKeys: *ref_10
          name: Paracraft物品列表
          link: 'https://keepwork.com/official/paracraft/docs/AllItems'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-6
          _parentKeys: *ref_10
          name: Paracraft功能列表
          link: 'https://keepwork.com/official/docs/references/features/index'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-7
          _parentKeys: *ref_10
          name: 对未来教育的思考
          link: 'https://keepwork.com/official/docs/references/future_education'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-8
          _parentKeys: *ref_10
          name: 如何学习Paracraft
          link: 'https://keepwork.com/official/docs/references/how_to_learn'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-9
          _parentKeys: *ref_10
          name: 小项目列表
          link: 'https://keepwork.com/official/docs/teach/lessons/small_proj_list'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-10
          _parentKeys: *ref_10
          name: 如何推广Paracraft
          link: 'https://keepwork.com/official/docs/videos/spread_video'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-11
          _parentKeys: *ref_10
          name: Paracraft《自我检测表》
          link: 'https://keepwork.com/official/docs/teach/lessons/paracraft_exams'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-12
          _parentKeys: *ref_10
          name: 推荐书籍
          link: 'https://keepwork.com/official/docs/references/books'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-13
          _parentKeys: *ref_10
          name: 常用教学文案
          link: 'https://keepwork.com/official/docs/teacher_center/notice'
          nameInputShow: false
          linkInputShow: false
        - _key: 7-14
          _parentKeys: *ref_10
          name: 成功案例
          link: 'https://keepwork.com/official/successful_cases/index'
          nameInputShow: false
          linkInputShow: false
  target: _self

```