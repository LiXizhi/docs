# 下载jupyter Server

Keepwork可计算文档配套的jupyter server. 

## >> Windows电脑

### 安装python

1. 下载python
进入以下页面下载最新的python版本
https://www.python.org/getit/

2. 双击安装python包,安装窗口勾选`Add python.exe to PATH`,然后点**Install now**

### 安装jupyter

1. 以管理员身份运行powerShell
在windows任务栏的搜索栏中输入“powershell”，在Windows Powershell应用下点击“以管理员身份运行”。
2. 修改powerShell执行策略，允许执行本地脚本。
在powershell命令窗口中输入

```
Set-ExecutionPolicy RemoteSigned
```
3. 下载安装jupyter脚本
https://cdn.keepwork.com/paracraft/Computable-doc/install-jupyter-win.ps1
4. 执行脚本，安装jupyter
找到下载到本地的install-jupyter-win.ps1脚本，右键单击中并选择“使用 PowerShell 运行”

### 启动jupyter-server
在windows上打开powershell,然后输入如下命令

```
python -m notebook
```


## > macOS电脑

### 安装python

启动一个Terminal.app，然后运行如下命令
```shell
##### 安装brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
##### 安装pyenv
brew install pyenv
pyenv install 3.10.0
pyenv global 3.10.0
```

### 安装jupyter环境
```shell
##### 新建一个文件夹
mkdir jupyter-project
cd jupyter-project
###### 新建一个虚拟环境
python -m venv venv
###### 如果是macOS下，激活虚拟环境
source ./venv/bin/activate
###### 安装jupyter
pip install jupyter
```

### 对jupyter-server进行配置

```shell
jupyter notebook --generate-config
```
在生成的jupyter_notebook_config.py文件后面追加如下的配置项
```yml
###### 允许跨域连接
c.NotebookApp.allow_origin = '*'
###### 当连接超过10分钟闲置时则断开
c.MappingKernelManager.cull_idle_timeout = 600
###### 连接闲置检测间隔60秒
c.MappingKernelManager.cull_interval = 60
###### 使连接不再需要检验token，所以注意请不要随便泄漏自己的jupyter-server链接
c.NotebookApp.token = ''
###### 使连接不再需要检验密码
c.NotebookApp.password = ''
###### 不需要检验跨域问题
c.ServerApp.disable_check_xsrf = True
```

### 启动jupyter-server
在windows上打开powershell或者macOS上的Terminal.app，然后输入如下命令
```shell
jupyter server
```

## > 其他

- [Windows下载连接](#)
- [Mac下载连接](#)
- [Linux下载连接](#)

