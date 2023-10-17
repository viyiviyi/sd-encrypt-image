# stable-diffusion-webui Image Encryption Plugin

**This is a plugin for stable-diffusion-webui that encrypts images before they are saved to disk and responds with decrypted images when accessed. It facilitates secure storage of images on public clouds and reduces the risk of being banned.**

- This plugin modifies the Image object and overrides the save method, enabling encryption for all image saving actions.
- Forgetting the password may result in the inability to restore your images.
- Due to unknown reasons, the plugin may not be able to pass images between different functions, such as from txt2img to img2img.
- There may be other unknown issues because this implementation affects other image access functions or plugins.

## Activation Method

1. Install the plugin in the plugin directory.
2. Add ```--encrypt-pass=your_password``` to the startup parameters.

## Batch Decryption Script Usage

1. Place the dencrypt_image_all.py file from the utils folder in the folder containing encrypted images (ideally, there should only be encrypted images in this folder; otherwise, normal files will be decrypted into garbled files without affecting the original files).
2. If you have a Python environment, open a command line in the image folder and execute ```python dencrypt_image_all.py``` (dencrypt_image_all.py is just an example name; please refer to your copied script file's actual name).
3. If you don't have a Python environment, install one before proceeding with step 2. Alternatively, you can use the provided dencrypt_images_v1.exe software from a distribution.

## Special Note

- To address quality loss caused by saving encrypted images as compressed formats like jpg or webp, all images will actually be saved as png format. It is recommended to change the image format to png in settings for consistency.