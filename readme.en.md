# [stable-diffusion-webui Image Encryption Plugin](https://github.com/viyiviyi/sd-encrypt-image.git)

[中文](readme.md) | [english](readme.en.md)

**This is a plugin for stable-diffusion-webui that encrypts images before saving them to disk and responds with decrypted images when accessed. It allows for secure storage of images in public clouds and reduces the risk of being banned.**

- This plugin modifies the Image object and overrides the save method, so enabling it will encrypt all image saving behaviors.
- Forgetting the password may result in the inability to restore your images.
- ~For unknown reasons, the plugin may not be able to pass images between different functions, such as from txt2img to img2img.~ (Fixed)
- The image saving format needs to be set to png, otherwise errors may occur when saving images.
- There may be other unknown issues because this plugin works when reading and saving images using the PIL library (overriding the save and open methods).
- The standalone encryption and decryption program has been completed, including Windows and Android versions. Linux needs to be packaged separately. [https://github.com/viyiviyi/encrypt_gallery/releases/](https://github.com/viyiviyi/encrypt_gallery/releases/)

## How to enable

1. Install the plugin to the plugin directory.
2. Add ```--encrypt-pass=your_password``` to the startup parameters.

## How to use the batch decryption script

1. Place the dencrypt_auto.py file from the utils folder in the folder containing the encrypted images (it is recommended to have only encrypted images in the folder, otherwise normal files will be decrypted and result in garbled files, which will not affect the original files).
2. If you have a Python environment, open the command line in the image folder and execute ```python dencrypt_auto.py```. You need to install the pillow and numpy libraries.
3. If you don't have a Python environment, install the Python environment and then execute step 2. You can also use the [decrypt_images_v2.exe](https://github.com/viyiviyi/sd-encrypt-image/releases/download/1.0/decrypt_images_v2.1.exe) software from the [release](https://github.com/viyiviyi/sd-encrypt-image/releases) of the project.

## Batch processing

- The utils directory provides py files for batch encryption and decryption, which require a Python environment, the pillow library, and the numpy library.
- The encrypt_auto.py file is used for encryption, and the decrypt_auto.py file is used for decryption. These two files were completed by [Echoflare](https://github.com/Echoflare).
- Compared to the original dencrypt_auto.py, this version enables multi-threading, which is more efficient and suitable for processing large batches of files.

## Special note

- In order to solve the problem of losing too much quality when encrypting and saving images in compressed formats such as jpg or webp, the actual saving format of all images will be changed to png. Therefore, if you save images in a format other than png, you may encounter errors when writing the generated parameters to the images. Please save the images in png format to ensure normal functionality.
## Special Note

- To address quality loss caused by saving encrypted images as compressed formats like JPG or WebP, all actual saved formats will be changed to PNG instead. It is recommended to change your image format to PNG in the settings to maintain consistency.
