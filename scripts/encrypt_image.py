
from modules import shared,script_callbacks,scripts as md_scripts
from scripts.core.core import encrypt_image,get_sha256,dencrypt_image
from PIL import Image,JpegImagePlugin,PngImagePlugin
from PIL import Image as PILImage
import numpy as np
from io import BytesIO
from typing import Optional
from fastapi import FastAPI
from gradio import Blocks
from fastapi import FastAPI, Request, Response
import os

repo_dir = md_scripts.basedir()
password = getattr(shared.cmd_opts, 'encrypt_pass', None)
super_open = PILImage.open

class EncryptedImage(Image.Image):
    def save(self, filename, format = None, pnginfo=None, *args, **kwargs):
        if not password:
            # 如果没有密码，直接保存
            super().save(filename, format = format, pnginfo=pnginfo, *args, **kwargs)
            return
        
        if 'Encrypt' in self.info and self.info['Encrypt'] == 'pixel_shuffle':
            super().save(filename, format = format, pnginfo=pnginfo, *args, **kwargs)
            return
        
        encrypt_image(self, get_sha256(password))
        self.format = PngImagePlugin.PngImageFile.format
        pnginfo = pnginfo or PngImagePlugin.PngInfo()
        pnginfo.add_text('Encrypt', 'pixel_shuffle')
        super().save(filename, format=self.format, pnginfo=pnginfo, *args, **kwargs)

PILImage.Image = EncryptedImage
        
def open(fp,*args, **kwargs):
    image = super_open(fp,*args, **kwargs)
    if password and image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
        pnginfo = image.info or PngImagePlugin.PngInfo()
        if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle':
            dencrypt_image(image, get_sha256(password))
            return image
    return image

PILImage.open = open

def on_app_started(demo: Optional[Blocks], app: FastAPI):
    @app.middleware("http")
    async def image_dencrypt(req: Request, call_next):
        endpoint:str = req.scope.get('path', 'err')
        if endpoint.startswith('/file='):
            file_path = endpoint[6:]
            ex = file_path[file_path.rindex('.'):].lower()
            if ex in ['.png','.jpg','.jpeg','.webp','.abcd']:
                image = super_open(file_path)
                if image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
                    pnginfo = image.info or PngImagePlugin.PngInfo()
                    if 'Encrypt' in pnginfo:
                        if pnginfo['Encrypt'] == 'pixel_shuffle':
                            dencrypt_image(image,get_sha256(password))
                            buffered = BytesIO()
                            image.save(buffered, format=PngImagePlugin.PngImageFile.format)
                            decrypted_image_data = buffered.getvalue()
                            response: Response = Response(content=decrypted_image_data, media_type="image/png")
                            return response
        res: Response = await call_next(req)
        return res

script_callbacks.on_app_started(on_app_started)

if password:
    print('图片加密已经启动 加密方式 1')
else:
    print('图片加密插件已安装，但缺少密码参数未启动')