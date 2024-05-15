# MPython 硬件编程

支持matrix:bit和掌控等ESP32 + micropython的硬件。 支持通过USB串口协议对硬件编程（含网页版）。

```@Project
styleID: 1
project:
  projectId: '1522980'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```
## 使用说明

### 第一步：创建代码方块
方法1： 从工具栏中创建mPY代码方块。
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28909/raw#1690857748631image.png
  ext: png
  filename: 1690857748631image.png
  size: 53835
  isNew: true
          
```

方法2： 你也可以创建一个普通代码方块，并在代码方块设置中改变语言为micropython。 

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28904/raw#1690806302483image.png
  ext: png
  filename: 1690806302483image.png
  size: 74077
  isNew: true
          
```
### 第二步：烧录固件（可跳过）

如果你之前已经烧录过或者购买了掌控板这一步可以跳过。 首先我们需要点击**硬件::固件烧录...**将mpython固件烧录到硬件中。

注意：固件可以理解为安装软件操作系统，所以只需要安装一次即可。大多数硬件出厂时，已经安装好，因此可以跳过本步骤。

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35363/raw#1708597258042image.png
  ext: png
  filename: 1708597258042image.png
  size: 7977
  isNew: true
          
```


您也可以去 https://micropython.org/ 的官网下载和烧录固件。 我们支持所有支持micropython REPL 串口协议的硬件。但是每个硬件包含的功能不同，能用的API也会有区别。 

### 第三步：连接并运行

此时我们可以在代码方块中用图块或文本写代码了。 注意在点击运行前，需要先连接设备。连接成功后会显示`已连接`。如果你希望其他应用也访问这个端口，则需要断开连接。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28906/raw#1690806696984image.png
  ext: png
  filename: 1690806696984image.png
  size: 12199
  isNew: true
          
```
设备连接好，点击运行，代码会自动烧录到硬件中，并重新执行。

```javascript
from mpython import *

oled.fill(0)
oled.DispChar("Hello, world!", 0, 0, 1)
oled.show()
```

注意：这类代码方块一般是不需要添加拉杆。

## 如何用串口实时通讯

我们可以用正常的代码方块通过USB或type-C等串口控制1台或多台mpython硬件芯片。 这样我们可以将运行paracraft的电脑或手机作为控制器，利用电脑的运算能力，同时调度多台硬件。 下面是一个简单的例子，通过serialport_send命令发送消息。

在运行前要确保已经连接上设备。可以看到， 硬件和软件一起更新计数器。

```javascript
serialport_send("\x03") -- terminiate previous program
serialport_send("from mpython import *", "code")

for i=1, 1000 do
    say("hi: "..i)
    
    serialport_send(string.format([[
oled.fill(0)
oled.DispChar('hi: %d', 0, 0, 1)
oled.show()
]], i), "code")

    wait(1)
end
```

一些常用mPython REPL控制命令

```javascript
serialport_send('\x01')       -- on a blank line, enter raw REPL mode
serialport_send('\x02')       -- on a blank line, enter normal REPL mode
serialport_send('\x03')       -- interrupt a running program
serialport_send('\x04')       -- on a blank line, do a soft reset of the board
serialport_send('\x05')       -- on a blank line, enter paste mode
```

### 如何同时控制多个串口？

如果你同时连接了多个串口设备，连续成功后，会显示当前串口和成功连接的串口总数。当前串口只在烧录模式下有效， 也就是通过mPython代码方块点击运行，会自动烧录到当前串口中。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28997/raw#1691495446250image.png
  ext: png
  filename: 1691495446250image.png
  size: 7038
  isNew: true
          
```

如果你希望更改当前串口，可以点击返回，然后从下拉列表框中选择你要切换的端口，然后点击连接即可。 主意点击自动总是会连接所有串口，并将最后连接的端口设置为当前串口。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/28998/raw#1691495681422image.png
  ext: png
  filename: 1691495681422image.png
  size: 11031
  isNew: true
          
```
当连接多个串口时，我们可以用`serialport_send(portIndex, data)`方法向portIndex串口发消息。 如果portIndex为-1，代表向所有连接的串口发。 请看下面的代码

```javascript
serialport_send(-1, "\x03") -- terminiate previous program
serialport_send(-1, "from mpython import *", "code")

for i=1, 1000 do
    say("hi: "..i)
    
    serialport_send(1, string.format([[
oled.fill(0)
oled.DispChar('A: %d', 0, 0, 1)
oled.show()
]], i), "code")

    serialport_send(2, string.format([[
oled.fill(0)
oled.DispChar('B: %d', 0, 0, 1)
oled.show()
]], i), "code")

    wait(1)
end
```

### 如何双向实时通讯？

serialport_send只能从主机向外部硬件设备发送信息。如何从mPython硬件向主机发送数据呢？我们只要用`print("")`打印函数即可。 只要打印的一行数据以"/"开头，则主机会自动运行这行命令。 例如：

```javascript
print("/tip hello")
print("/sendevent hello {'msg'}")
```

我们也提供了一个方便的图块，内置了常用命令，如下：
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29002/raw#1691565355412image.png
  ext: png
  filename: 1691565355412image.png
  size: 190048
  isNew: true
          
```
如果在硬件上使用**print("/sendevent hello  some_msg")** , 在PC端，我们可以使用**普通的**代码方块，接收hello消息， 如下图所示。如果你希望控制虚拟小车， 可以通过设置全局变量，然后在虚拟小车的代码中检测这个全局变量。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35142/raw#1706148765689image.png
  ext: png
  filename: 1706148765689image.png
  size: 30626
  isNew: true
          
```
我们可以用双向通讯，实现下面的数字孪生的应用。注意这个方法对micropython和arduino都适用。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/30133/raw#1697627713976SimCarRemote.mp4
  ext: mp4
  filename: 1697627713976SimCarRemote.mp4
  size: 3453322
  isNew: true
  isExpand: true
          
```

### 虚拟仿真智能模组
从资源商城中，可以添加mPython的各种虚拟仿真智能模组。 每个智能模组会注册1个或多个虚拟串口， 从而通过虚拟世界中的硬件仿真mPython代码。最终可以实现一套代码驱动虚拟和物理孪生的设备。

```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32353/raw#1699941441671image.png
  ext: png
  filename: 1699941441671image.png
  size: 90704
  isNew: true
  isExpand: true
          
```

例如下面的智能巡线小车的世界：

```@Project
styleID: 1
project:
  projectId: '1650613'
  eventName: ''
  projectTagsShow: true
  projectMembersShow: true
  projectWorldShow: false
  projectWorldOpenInWebsite: true

```


```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/29929/raw#1696163759303mpython_CarDemo.mp4
  ext: mp4
  filename: 1696163759303mpython_CarDemo.mp4
  size: 59331515
  isNew: true
  isExpand: true
          
```

### 如何进入世界自动连接硬件？

使用下面命令会自动连接所有的硬件。请确保只有mPython的串口硬件，否则可能连上不相关的硬件。

```javascript
/serialport connect
/serialport disconnect
```

#### 如何让代码方块打开时，默认连接指定的串口
如果你的世界中需要同时对多个虚拟串口和物理串口进行编程。 可以给你的mpython代码方块起一个和串口相同的名字， 可以重名。 例如，如果你希望多个代码方块都自动写入虚拟串口2，则可以给这些代码方块都起名为sim2, 如下图。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32350/raw#1699941251076image.png
  ext: png
  filename: 1699941251076image.png
  size: 332956
  isNew: true
  isExpand: true
          
```

### 如何同时运行多py文件？

我们需要将多个mpython代码方块摆放在一起。并给类库文件起个py结尾的名字。 例如下面的person.py
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32347/raw#1699940859986image.png
  ext: png
  filename: 1699940859986image.png
  size: 205713
  isNew: true
  isExpand: true
          
```

默认的代码方块其实是`main.py`, 我们需要在设置中配置为`延时运行`, 这样它会比周围的代码方块后运行。 此时我们就可以在这个代码方块中使用周围代码方块定义的类了， 例如下图：
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/32348/raw#1699941093091image.png
  ext: png
  filename: 1699941093091image.png
  size: 218399
  isNew: true
  isExpand: true
          
```
###  Win32蓝牙通讯

1. 在paracraft控制台中通过串口的方式启用掌控板
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35359/raw#1708586929279image.png
  ext: png
  filename: 1708586929279image.png
  size: 284487
  isNew: true
          
```

```
NPL.load("(gl)script/apps/Aries/Creator/Game/Code/SerialPort/SerialPortConnector.lua");
local SerialPortConnector = commonlib.gettable("MyCompany.Aries.Game.Code.SerialPortConnector");
SerialPortConnector.SwitchBLEMode()
```

2. 新建mpython方块，在连接窗口中选择蓝牙

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35361/raw#1708587107689image.png
  ext: png
  filename: 1708587107689image.png
  size: 1692502
  isNew: true
          
```

3. 点击“连接设备”，看到一下画面即代表连接成功

 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35362/raw#1708587201196image.png
  ext: png
  filename: 1708587201196image.png
  size: 901229
  isNew: true
          
```

现在就可以执行掌控板程序了


