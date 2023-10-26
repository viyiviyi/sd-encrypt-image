# [stable-diffusion-webui Image Encryption Plugin](https://github.com/viyiviyi/sd-encrypt-image.git)

[中文](./readme.md) | english

**This is a plugin for stable-diffusion-webui that encrypts images before saving them to disk and responds with decrypted images when accessed. It allows for secure storage of images in public clouds while reducing the risk of being banned.**

- This plugin modifies the Image object and overrides the save method, enabling encryption for all image saving actions.
- Forgetting the password may result in an inability to restore your images.
- ~Due to unknown reasons, the plugin may not pass images between different functions, such as from txt2img to img2img.~ (Fixed)
- The image save format needs to be set as PNG; otherwise, errors may occur during image saving.
- There may be other unknown issues as this plugin works with PIL library to read and save images (by overriding the save and open methods).

## How to Enable

1. Install it into the plugin directory.
2. Add ```--encrypt-pass=your_password``` to the startup parameters.

## Batch Decryption Script Usage

1. Place the dencrypt_image_all.py file from the utils folder into a folder containing encrypted images (ideally, there should only be encrypted files in this folder; otherwise, normal files will become garbled after decryption without affecting original files).
2. If you have Python installed, open a command prompt in the image folder and execute ```python dencrypt_image_all.py``` (dencrypt_image_all.py is just an example name; use whatever name you copied for your script file).
3. If you don't have Python installed, install it first before proceeding with step 2; alternatively, you can use a pre-built executable software like dencrypt_images_v1.exe provided by distribution.

## Special Note

- To address quality loss caused by saving encrypted images as compressed formats like JPG or WebP, all actual saved formats will be changed to PNG instead. It is recommended to change your image format to PNG in the settings to maintain consistency.
