from PIL import Image,JpegImagePlugin,PngImagePlugin,WebPImagePlugin

from core.encrypt import dencrypt_image, encrypt_image, get_sha256

class EncryptedImage(Image.Image):
    password = ''
    def open(self,fp,*args, **kwargs):
        super().open(fp,*args, **kwargs)
        exif_data = self.info.get('exif', b'')
        if 'Encrypt: pixel_shuffle' in exif_data.decode('unicode-escape'):
            dencrypt_image(self,EncryptedImage.password)
            extension = self.filename[self.filename.rfind('.'):].lower()
            if extension in ['.jpg','.jpeg']: self.format = JpegImagePlugin.JpegImageFile.format
            if extension in ['.webp'] : self.format = WebPImagePlugin.WebPImageFile.format
            if extension in ['.png']: self.format = PngImagePlugin.PngImageFile.format

    def save(self, filename,*args, **kwargs):
        # 加密图片数据
        exif_data = self.info.get('exif', b'')
        if EncryptedImage.password:
            encrypt_image(self, get_sha256(EncryptedImage.password))
            exif_data += b', Encrypt: pixel_shuffle' # 追加
            # dencrypt_image(self, get_sha256(EncryptedImage.password)) # 测试用
        # 创建新的Image对象，并保存加密后的数据
        super().save(filename,format=PngImagePlugin.PngImageFile.format, exif=exif_data, *args, **kwargs)

Image.Image = EncryptedImage

def preload(parser):
    parser.add_argument("--encrypt-pass", type=str, help="The password to enable image encryption.", default=None)
