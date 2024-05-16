# Item Dialog
Dialog is a rule item, which is defined by an xml file. Dialog rule is usually associated with an NPC entity. 
When the NPC is clicked, the dialog rule is activated. It will display UI dialog to the user according to the 
internal rules defined, such as whether a given quest is active, accepted or finished, etc. 

There are three types of dialogs: gossips, quests and triggers:
* gossips: a randomly picked dialog will be shown when there is no other options
* quests: one or more quest related dialogs
   * startdialog: dialogs to show to the user, when pre-condition is met, but froms and goals are not met.
   * acceptdialog: dialogs to show to the user has already accepted the quest. 
   * enddialog: dialogs to show to the user, when froms and goals are met, before rule is executed. 
* triggers: one or more dialog that is only triggered when virtual item or precondition is found on the target NPC
            triggers themselves can be used to complete simple one-time tasks.
   * input: virtual items or real items before this trigger can be activated. Item listed will be removed after dialog is shown.
   * dialogs: dialogs to show when this item is triggered. 
   * output: virtual items or real items to be given to the user when the dialog is finished. 

## 对话物品
对话物品被激活时，可以产生可交互的对话框。对话框的内容由XML文件定义， 例如`filename.dialog.xml`文件。 
![questitem](https://cloud.githubusercontent.com/assets/94537/14173488/c6ea17ec-f770-11e5-9968-87846b9b46d3.png)

激活方式：
 * 放到命令方块的背包中，随命令一起激活
 * 放到NPC人物的规则背包中，当用户左键点击人物时激活。 
 * 拿在手上，按Ctrl+右键强制激活（一般用于调试）。

## 对话编辑
* 右键点击对话物品的Icon可编辑。每个对话物品对应一个XML文件
* 在弹出对话框中，点击`编辑`按钮新建或编辑当前文件。 此时会打开默认的网页浏览器
   * 编辑器是用`HTML5/NPL`写的，所以需要最新的支持HTML5的浏览器，推荐Chrome
   * 网页其实是对`xxx.dialog.xml`的编辑，请见下节。
   * ![editdialogitem](https://cloud.githubusercontent.com/assets/94537/14372855/1d6637d4-fd77-11e5-80f9-062cd3c7de1f.png)
* 你可以在网页中改变XML的文件名，修改后要点击`save`按钮。
* 编辑好后，对话会自动刷新， 你可以Ctrl+右键点击对话物品来测试。

### `xxx.dialog.xml`文件定义
Dialog文件可以定义多种触发条件，和对应的对话内容。 触发分成3类
* gossip: 随机对话： 从中随机抽取一个和最近抽取的不重复的对话
* quests: 任务对话：当符合任务条件时触发（可接， 可完成，进行中）三种触发条件都可设置独立的对话。详见[item_Rule](item_Rule)规则。
* trigger: 条件触发： 当用户背包中的物品符合某条件时触发。 可以代替quests,做一些简单的任务。

> 触发优先级是`trigger > quests > gossips`

例如：
```html
<!--There are three types of dialogs: gossips, quests and triggers-->
<dialogs>
  <!--gossips dialogs are triggered randomly when no other triggers are available-->
  <gossips>
    <dialog>
      <item>
        <avatar name="test">Mr. Avatar</avatar>
        <content>
          If no buttons are provided, a default one will be used.
        </content>
      </item>
      <item>
        <avatar name="player"></avatar>
        <content>if avatar name is player, it will show current player.</content>
        <buttons>
          <button action="doaccept" >OK. I got it.</button>
        </buttons>
      </item>
    </dialog>
    <dialog>
      <item>
        <content>
          this is a random gossip text 2
        </content>
        <buttons>
          <button action="gotonext">I got it</button>
        </buttons>
      </item>
    </dialog>
  </gossips>
  <!--quest dialog is triggered according to quest's active, accept, finish state.-->
  <quests>
    <!--here we will handle triggers from quest id 1001-->
    <quest id="1001">
      <!--dialogs to show when quest is active, but can not be completed. -->
      <startdialog>
        <item>
          <avatar name="test">Mr. Avatar</avatar>
          <content>
            If no buttons are provided, a default one will be used.
          </content>
        </item>
        <item>
          <avatar name="player"></avatar>
          <content>if avatar name is player, it will show current player.</content>
          <buttons>
            <button action="doaccept" >OK. I got it.</button>
          </buttons>
        </item>
      </startdialog>
      <!--dialogs to show when quest can be completed. -->
      <enddialog>
        <item>
          <avatar></avatar>
          <content>
            congratulations, you have completed the quest so fast
          </content>
          <buttons>
            <button action="dofinished" >you are welcome</button>
          </buttons>
        </item>
      </enddialog>
    </quest>
  </quests>
  <!--triggers are simple quest system. It is simple three phase design: 
  inputs are deleted, dialog is shown and then output is given.-->
  <triggers>
    <trigger>
      <input>
        <!--please note virtual items will be deleted when dialog is confirmed-->
        <virtualitem id="quest1111" value="1" />
      </input>
      <dialog>
        <item>
          <avatar></avatar>
          <content>
            dialog is the first output to show to the user
          </content>
          <buttons>
            <button action="gotonext">OK</button>
          </buttons>
        </item>
      </dialog>
      <output>
        <virtualitem id="quest2222" value="1" />
      </output>
    </trigger>
  </triggers>
</dialogs>
```

### 定义Dialog
一个Dialog可以由多个Item构成。 每个Item代表一段话， 可包含`avatar`, `content`, `buttons`。
每个Item可以有一个name. 
 * avatar 表示显示什么人物和名字。 如果没有为当前被触发的角色。
   * avatar.name: 可以为场景中的某个人物的名字, name为`player`代表主角
 * content 表示对话的内容， 里面可以有复杂的格式和动作标记
 * buttons 表示用户需点击的一个或多个按钮。如果没有会默认一个`继续`按钮
   * button.action可以有多个命令
     * `gotonext`: 这个是默认命令，不填也是这个
     * `goto [itemname]`: 跳到指定item. 实现根据用户的选择，在各种对话间跳来跳去。

例如：
```xml
    <dialog>
      <item name="name1">
        <content>
          This demonstrate button action with "goto"
          this is first one.
        </content>
        <buttons>
          <button action="goto name3">goto 3</button>
        </buttons>
      </item>
      <item name="name2">
        <content>
          This is second one
        </content>
        <buttons>
          <button action="goto name1">goto 1</button>
        </buttons>
      </item>
      <item name="name3">
        <content>
          This is third
        </content>
        <buttons>
          <button action="goto name2">goto 2</button>
        </buttons>
      </item>
    </dialog>
```
### 定义Trigger
Trigger是触发器，包含input, dialog, output三个部分，见下文。
* `input`: 这里是输入物品，可以是真实物品`item`或虚拟物品`virtualitem`。当input条件满足时，对话可被触发。但不是执行。
* `dialog`: 对话内容，见上文。当用户点击对话的buttons.action为`accept`的按钮时，Trigger会被执行。此时所有input中的物品被删除，所有output的物品会被放入用户的背包中。
* `output`: 这里是输出物品，可以是真实物品`item`或虚拟物品`virtualitem` 

> 虚拟物品`virtualitem`: 可以是任何不重复的数字或字符例如`quest1001`。所有的虚拟物品被统一记录在触发用户的背包中的`日志物品`中

```html
   <trigger>
      <input>
        <!--please note items will be deleted when dialog is confirmed-->
        <virtualitem id="quest1111" value="1" />
        <item id="62" value="1" />
      </input>
      <dialog>
        <item>
          <avatar></avatar>
          <content>
            You must have `quest1111` and id:62 to trigger this dialog.
          </content>
        </item>
        <item>
          <avatar></avatar>
          <content>
            when you click OK, you will be given `quest2222`. `quest1111` and id:62 will be removed.
          </content>
          <buttons>
            <button action="accept">OK</button>
          </buttons>
        </item>
      </dialog>
      <output>
        <virtualitem id="quest2222" value="1" />
      </output>
    </trigger>
```