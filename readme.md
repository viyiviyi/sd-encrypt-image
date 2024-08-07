# [stable-diffusion-webui 图片加密插件](https://github.com/viyiviyi/sd-encrypt-image.git)

[中文](readme.md) | [english](readme.en.md)

**这是一个stable-diffusion-webui的插件，实现了在图片保存到磁盘前对图片进行加密，在访问时响应解密后的图片的功能，便于在使用公有云时安全的存储图片而降低封号风险**

- 这个插件会修改Image对象，重写了save方法，启用将会导致所有的图片保存行为都被加密
- 如果忘记密码，可能会导致你无法还原你的图像。
- ~~需要增加 ```--api``` 启动参数来保证在网页可以正常浏览图片。~~
- 图片的保存格式需要设置成png，否则会导致保存图片时出现错误。
- 可能还存在其他未知问题，因为此插件工作在PIL库读取图片和保存图片的时候（重写了 save方法和open方法）。
- 独立的加密解密程序已经完成，包括windows和安卓端，Linux需要自行打包。 [https://github.com/viyiviyi/encrypt_gallery/releases/](https://github.com/viyiviyi/encrypt_gallery/releases/)
- 虽然已经没啥需要维护的了，但还是求个赞助。[爱发电主页](https://afdian.net/a/yiyiooo)
  
## 启用方式

1. 安装到插件目录
2. 在启动参数增加 ```--encrypt-pass=你的密码```

## 批量解密脚本使用方式

1. 将utils文件夹内的 dencrypt_auto.py 文件放到包含加密图片的文件夹（尽量文件夹内只有已加密的图片，否则正常文件解密后会得到乱码的文件，不会影响原文件）
2. 如果有Python环境，在图片文件夹打开命令行 执行 ```python dencrypt_auto.py```，需要安装pillow 和 numpy 库。
3. 如果没有Python环境，需要安装Python环境后再执行步骤2，也可以使用[发行版](https://github.com/viyiviyi/sd-encrypt-image/releases)的 [decrypt_images_v2.exe](https://github.com/viyiviyi/sd-encrypt-image/releases/download/1.0/decrypt_images_v2.1.exe) 软件

## 批处理

- utils目录提供了批量加密解密的py文件，可用于批量加密和解密文件，需要Python环境、pillow和numpy库
- encrypt_auto.py 文件用于加密，decrypt_auto.py 文件用于解密，这两个文件由 [Echoflare](https://github.com/Echoflare)完成。
- 比起原版的dencrypt_auto.py，这个启用了多线程，效率更高，更时候大批量处理文件。

## 特别说明

- 为了解决图片加密后保存为jpg或webp这种压缩格式的图片时会导致解密后损失过多质量的问题，所有图片的实际保存格式都将会改成png，也因此会导致以非png格式保存图片时会出现不能将生成参数写入到图片的错误，请将图片保存到格式设置为png保证功能正常。
