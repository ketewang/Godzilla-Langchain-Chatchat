
### 1. nvidia驱动问题

+ 首先，确保你的机器安装了 Python 3.8 - 3.10
```
$ nvidia-smi

NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.
```

方案1
原因：系统内核升级，导致新版本内核和原来显卡驱动不匹配
解决方案：使用dkms生成对应的内核文件

+ 查看驱动版本
```
$ ls /usr/src | grep nvidia
```
例如我得到的结果是nvidia-525.105.17

+ 匹配
```
$ sudo apt-get install dkms
$ sudo dkms install -m nvidia -v 525.105.17
```

### 2 pytorch与transformer兼容问题
````
这个错误是由于缺少 sentence_transformers Python 包引起的。要修复这个错误，可以执行以下步骤：

1、确保你的环境中已经安装了 sentence_transformers 包。你可以使用以下命令来安装它：
pip install sentence_transformers
2、如果已经安装了 sentence_transformers 包，但仍然出现错误，可以尝试更新它：
pip install --upgrade sentence_transformers
3、确保你的Python环境与 sentence_transformers 包的依赖兼容。有时候，不同的Python版本和包版本之间可能会出现兼容性问题。检查包的官方文档以获取兼容性信息。
4、如果你使用的是Conda环境，还可以考虑更新Conda本身和PyTorch，因为错误信息中涉及到了PyTorch。你可以使用以下命令来更新Conda：
conda update --all
5、然后，更新PyTorch：
conda install pytorch torchvision torchaudio -c pytorch
````