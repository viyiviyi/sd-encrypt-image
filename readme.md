# stable-diffusion-webui 图片加密插件

**这个插件会导致 ```jpg``` 和 ```webp``` 图片质量降低，和这两个格式的图片压缩算法有关。**

- 这个插件会修改Image对象，重写了save方法，启用将会导致所有的图片保存行为都被加密
- 这个插件会导致图片浏览器不能正确显示缩略图，因为缩略图是在加密后的图像上产生的
- 这个插件会导致读取未加密的图片时出现错误，因为没有给图片做标记是否加密
- 这个插件很危险，可能会导致你无法还原你的图像。
  - preload.py 文件的 dencrypt_image 方法可以用来还原你的图像，如果你需要批量还原，可以写一个简单的脚本，用密码还原
  - utils/dencrypt_image_all.py 文件是批量还原的脚本
  - 发行版的 dencrypt_images_v1.exe 文件是将解密逻辑打包后的可执行文件

- 这个插件仅能在webui界面还原查看的图片，对类似[无边图像浏览器](https://github.com/zanllp/sd-webui-infinite-image-browsing.git)这种将图片渲染在iframe标签内的无法生效，也就不能在查看时解密

## 启用方式

1. 安装到插件目录
2. 在启动参数增加 ```--encrypt-pass=你的密码```

## 批量解密脚本使用方式

1. 将utils文件夹内的 dencrypt_image_all.py 文件放到包含加密图片的文件夹（尽量文件夹内只有已加密的图片，否则正常文件解密后会得到乱码的文件，不会影响原文件）
2. 如果有Python环境，在图片文件夹打开命令行 执行 ```python dencrypt_image_all.py``` (dencrypt_image_all.py 只是示例名，实际名称看你复制的脚本文件)
3. 如果没有Python环境，需要安装Python环境后再执行步骤2，也可以使用发行版的 dencrypt_images_v1.exe 软件
   
