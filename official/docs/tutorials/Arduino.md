# Arduino-C 代码方块

## 创建Arduino方块 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35143/raw#1706149595209image.png
  ext: png
  filename: 1706149595209image.png
  size: 61149
  isNew: true
          
```

注意，和[micropython](https://keepwork.com/official/docs/tutorials/micropython)不同， arduino方块的运行按钮只能运行虚拟仿真的代码， 不能用于烧录硬件。 如果需要上传烧录，请点击上传按钮。 首次运行会自动安装arduino-cli开发环境，目前自动烧录只支持windows系统，其他系统只能运行虚拟仿真代码，无法自动烧录。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35144/raw#1706149759347image.png
  ext: png
  filename: 1706149759347image.png
  size: 33036
  isNew: true
          
```

但是你可以手工烧录，点击图块2次，可以复制粘贴仿真后的arduino-c代码，然后手工复制到arduino-c的开发环境中。 您也可以点击`打开arduino...`按钮，我们会自动创建xxx.ino项目文件，并自动用本地安装的arduino开发环境打开这个文件。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35145/raw#1706149972624image.png
  ext: png
  filename: 1706149972624image.png
  size: 12811
  isNew: true
          
```
点击配置按钮，可以配置自动烧录时的端口和其他arduino-cli命令行。如果没有安装串口驱动， 可以点击下图中的下拉窗，选择安装驱动， 大多数硬件都会自动安装串口驱动，我们只提供了部分不支持自动安装的串口驱动下载链接，您也可以到网上自己安装。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35147/raw#1706150231749image.png
  ext: png
  filename: 1706150231749image.png
  size: 26613
  isNew: true
          
```
## 如何用串口实时通讯

我们可以用`普通的代码方块`通过USB或type-C等串口控制1台或多台硬件芯片。 这样我们可以将运行paracraft的电脑或手机作为控制器，利用电脑的运算能力，同时调度多台硬件。 下面是一个简单的例子，通过serialport_send命令发送消息。

```javascript
serialport_send("cmd 123\n")
```

在普通代码方块中有，也有一个图块。 注意需要将第二个参数设置为空，否则是按照micropython REPL代码的形式发送。
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35149/raw#1706150562659image.png
  ext: png
  filename: 1706150562659image.png
  size: 16915
  isNew: true
          
```

:point_right:注意：arduino方块每次自动烧录时，为了和arduino-cli烧录程序共享串口，都会**强制关闭**所有串口。 所以在串口通讯前，你需要保证串口已经链接，你可以使用下面命令会自动连接所有的硬件。请确保其他APP没有在使用串口（例如arduino的串口监控需要关闭），否则连不上相关的串口硬件。

```javascript
/serialport connect
/serialport disconnect
```
你也可以通过，菜单中的 `窗口》连接串口...` 手工连接。 
 
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35150/raw#1706150877717image.png
  ext: png
  filename: 1706150877717image.png
  size: 9037
  isNew: true
          
```
### 如何双向实时通讯？

serialport_send只能从主机向外部硬件设备发送串口信息。如何从Arduino硬件向主机发送数据呢？我们只要用`Serial.println("")`打印函数即可。 只要打印的一行数据以"/"开头，则主机会自动运行这行命令。 例如：
```@BigFile

bigFile:
  src: >-
    https://api.keepwork.com/ts-storage/siteFiles/35151/raw#1706151044983image.png
  ext: png
  filename: 1706151044983image.png
  size: 17175
  isNew: true
          
```

```javascript
void setup(){
    Serial.begin(115200);
}
void loop(){
    Serial.println('/tip hello world from arduino');
    delay(300);
    Serial.println('/sendevent hello some_msg');
    delay(300);
}

```


如果在硬件上使用**Serial.println("/sendevent hello  some_msg")** , 在PC端，我们可以使用**普通的**代码方块，接收hello消息， 如下图所示。如果你希望控制虚拟小车，可以通过设置全局变量，然后在虚拟小车的代码中检测这个全局变量。也就是你需要用一个普通的代码方块作为**消息中继器**， 接收电脑串口的数据，然后通过全局变量，通知arduino虚拟仿真方块。 注意全局变量，只存在于arduino仿真环境 (所有代码方块，包括arduino和普通代码方块是共享全局数据的)。

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

> 注意： arduino的串口监控不可以与paracraft串口通讯一起开启，会造成串口冲突。另外发送命令时，需要以`\n`结尾。