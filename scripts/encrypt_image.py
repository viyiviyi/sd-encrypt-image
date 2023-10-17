
from modules import shared,script_callbacks
from scripts.core.core import encrypt_image,get_sha256,dencrypt_image
from PIL import Image,JpegImagePlugin,PngImagePlugin
from PIL import Image as PILImage
from io import BytesIO
from typing import Optional
from fastapi import FastAPI
from gradio import Blocks
from fastapi import FastAPI, Request, Response

class EncryptedImage(Image.Image):
    password = ''
    __name__ = 'EncryptedImage'
    
    @staticmethod
    def open(fp,*args, **kwargs):
        image = PILImage.open(fp,*args, **kwargs)
        encrypt_type = ''

        if image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
            pnginfo = image.info or PngImagePlugin.PngInfo()
            encrypt_type = pnginfo["Encrypt"]

        if encrypt_type == 'pixel_shuffle':
            print('dencrypt: '+str(fp))
            dencrypt_image(image, get_sha256(EncryptedImage.password))
        return EncryptedImage(image)

    def save(self, filename, format = None, pnginfo=None, *args, **kwargs):
        if not EncryptedImage.password:
            # 如果没有密码，直接保存
            super().save(filename, format = format, *args, **kwargs)
        
        encrypt_image(self, get_sha256(EncryptedImage.password))

        self.format = PngImagePlugin.PngImageFile.format
        pnginfo = pnginfo or PngImagePlugin.PngInfo()
        pnginfo.add_text('Encrypt', 'pixel_shuffle')
        super().save(filename, format=self.format, pnginfo=pnginfo, *args, **kwargs)

Image.Image = EncryptedImage

password = getattr(shared.cmd_opts, 'encrypt_pass', None)

def on_app_started(demo: Optional[Blocks], app: FastAPI):
    @app.middleware("http")
    async def image_dencrypt(req: Request, call_next):
        endpoint:str = req.scope.get('path', 'err')
        if endpoint.startswith('/file='):
            file_path = endpoint[6:]
            print(file_path)
            ex = file_path[file_path.rindex('.'):].lower()
            if ex in ['.png','.jpg','.jpeg','.webp','.abcd']:
                image = PILImage.open(file_path)
                if image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
                    pnginfo = image.info or PngImagePlugin.PngInfo()
                    if 'Encrypt' in pnginfo:
                        if pnginfo['Encrypt'] == 'pixel_shuffle':
                            dencrypt_image(image,get_sha256(EncryptedImage.password))
                            buffered = BytesIO()
                            image.save(buffered, format=JpegImagePlugin.JpegImageFile.format)
                            decrypted_image_data = buffered.getvalue()
                            response: Response = Response(content=decrypted_image_data, media_type="image/jpeg")
                            return response
        res: Response = await call_next(req)
        return res

script_callbacks.on_app_started(on_app_started)

if password:
    print('图片加密已经启动 加密方式 1')
    EncryptedImage.password = password
    # section = ("encrypt_image",'图片加密' if shared.opts.localization == 'zh_CN' else "encrypt image" )
    # shared.opts.add_option(
    #     "encrypt_pass_hash",
    #     shared.OptionInfo(
    #         default=get_sha256(password),
    #         label='图片解密密码的哈希值, 别改!' if shared.opts.localization == 'zh_CN' else "encrypt image hash password",
    #         section=section,
    #     ),
    # )
    # shared.opts.data['encrypt_pass_hash'] = get_sha256(password)
else:
    print('图片加密插件已安装，但缺少密码参数未启动')