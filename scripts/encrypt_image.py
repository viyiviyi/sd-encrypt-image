
import base64
import io
from pathlib import Path
from modules import shared,script_callbacks,scripts as md_scripts,images
from modules.api import api
from modules.shared import opts
from scripts.core.core import encrypt_image,get_sha256,dencrypt_image,dencrypt_image_v2,encrypt_image_v2
from PIL import PngImagePlugin,_util,ImagePalette
from PIL import Image as PILImage
from io import BytesIO
from typing import Optional
from fastapi import FastAPI
from gradio import Blocks
from fastapi import FastAPI, Request, Response
import sys

repo_dir = md_scripts.basedir()
password = getattr(shared.cmd_opts, 'encrypt_pass', None)

if PILImage.Image.__name__ != 'EncryptedImage':
    super_open = PILImage.open
    super_encode_pil_to_base64 = api.encode_pil_to_base64
    super_modules_images_save_image = images.save_image
    class EncryptedImage(PILImage.Image):
        __name__ = "EncryptedImage"
        
        @staticmethod
        def from_image(image:PILImage.Image):
            image = image.copy()
            img = EncryptedImage()
            img.im = image.im
            img.mode = image.mode
            img._size = image.size
            img.format = image.format
            if image.mode in ("P", "PA"):
                if image.palette:
                    img.palette = image.palette.copy()
                else:
                    img.palette = ImagePalette.ImagePalette()
            img.info = image.info.copy()
            return img
            
        def save(self, fp, format=None, **params):
            filename = ""
            if isinstance(fp, Path):
                filename = str(fp)
            elif _util.is_path(fp):
                filename = fp
            elif fp == sys.stdout:
                try:
                    fp = sys.stdout.buffer
                except AttributeError:
                    pass
            if not filename and hasattr(fp, "name") and _util.is_path(fp.name):
                # only set the name for metadata purposes
                filename = fp.name
            
            if not filename or not password:
                # 如果没有密码或不保存到硬盘，直接保存
                super().save(fp, format = format, **params)
                return
            
            if 'Encrypt' in self.info and (self.info['Encrypt'] == 'pixel_shuffle' or self.info['Encrypt'] == 'pixel_shuffle_2'):
                super().save(fp, format = format, **params)
                return
            
            encrypt_image_v2(self, get_sha256(password))
            self.format = PngImagePlugin.PngImageFile.format
            if self.info:
                self.info['Encrypt'] = 'pixel_shuffle_2'
            pnginfo = params.get('pnginfo', PngImagePlugin.PngInfo())
            pnginfo.add_text('Encrypt', 'pixel_shuffle_2')
            params.update(pnginfo=pnginfo)
            super().save(fp, format=self.format, **params)
            # 保存到文件后解密内存内的图片，让直接在内存内使用时图片正常
            dencrypt_image_v2(self, get_sha256(password)) 
            if self.info:
                self.info['Encrypt'] = None
            


    def open(fp,*args, **kwargs):
        image = super_open(fp,*args, **kwargs)
        if password and image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
            pnginfo = image.info or {}
            if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle':
                dencrypt_image(image, get_sha256(password))
                pnginfo["Encrypt"] = None
                image = EncryptedImage.from_image(image=image)
                return image
            if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle_2':
                dencrypt_image_v2(image, get_sha256(password))
                pnginfo["Encrypt"] = None
                image = EncryptedImage.from_image(image=image)
                return image
        return EncryptedImage.from_image(image=image)
    
    def encode_pil_to_base64(image:PILImage.Image):
        with io.BytesIO() as output_bytes:
            image.save(output_bytes, format="PNG", quality=opts.jpeg_quality)
            pnginfo = image.info or {}
            if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle':
                dencrypt_image(image, get_sha256(password))
                pnginfo["Encrypt"] = None
            if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle_2':
                dencrypt_image_v2(image, get_sha256(password))
                pnginfo["Encrypt"] = None
            bytes_data = output_bytes.getvalue()
        return base64.b64encode(bytes_data)
    
    if password:
        PILImage.Image = EncryptedImage
        PILImage.open = open
        api.encode_pil_to_base64 = encode_pil_to_base64

def on_app_started(demo: Optional[Blocks], app: FastAPI):
    from urllib.parse import unquote
    @app.middleware("http")
    async def image_dencrypt(req: Request, call_next):
        endpoint:str = req.scope.get('path', 'err')
        # 兼容无边浏览器
        if endpoint.startswith('/infinite_image_browsing/image-thumbnail') or endpoint.startswith('/infinite_image_browsing/file'):
            query_string:str = req.scope.get('query_string').decode('utf-8')
            query_string = unquote(query_string)
            if query_string and query_string.index('path=')>=0:
                query = query_string.split('&')
                path = ''
                for sub in query:
                    if sub.startswith('path='):
                        path = sub[sub.index('=')+1:]
                if path:
                    endpoint = '/file=' + path
        # 模型预览图
        if endpoint.startswith('/sd_extra_networks/thumb'):
            query_string:str = req.scope.get('query_string').decode('utf-8')
            query_string = unquote(query_string)
            if query_string and query_string.index('filename=')>=0:
                query = query_string.split('&')
                path = ''
                for sub in query:
                    if sub.startswith('filename='):
                        path = sub[sub.index('=')+1:]
                if path:
                    endpoint = '/file=' + path
        if endpoint.startswith('/file='):
            file_path = endpoint[6:] or ''
            if not file_path: return await call_next(req)
            if file_path.rfind('.') == -1: return await call_next(req)
            if not file_path[file_path.rfind('.'):]: return await call_next(req)
            if file_path[file_path.rfind('.'):].lower() in ['.png','.jpg','.jpeg','.webp','.abcd']:
                image = PILImage.open(file_path)
                pnginfo = image.info or {}
                if 'Encrypt' in pnginfo:
                    buffered = BytesIO()
                    image.save(buffered, format=PngImagePlugin.PngImageFile.format)
                    decrypted_image_data = buffered.getvalue()
                    response: Response = Response(content=decrypted_image_data, media_type="image/png")
                    return response
        res: Response = await call_next(req)
        return res

if password:
    script_callbacks.on_app_started(on_app_started)
    print('图片加密已经启动 加密方式 2')
else:
    print('图片加密插件已安装，但缺少密码参数未启动')