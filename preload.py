from PIL import Image,JpegImagePlugin,PngImagePlugin,WebPImagePlugin
from PIL import Image as PILImage
import hashlib
import os
import piexif
import piexif.helper

def get_range(input:str,offset:int,range_len=4):
    if (offset+range_len)<len(input):
        return input[offset:offset+range_len]
    else: return input[offset:]+input[:range_len - (len(input) - offset)]

def get_sha256(input:str):
    hash_object = hashlib.sha256()
    # 更新hash对象的内容
    hash_object.update(input.encode('utf-8'))
    return hash_object.hexdigest()

def shuffle_arr(arr,key:str):
    sha_key = get_sha256(key)
    key_offset = 0
    for i in range(len(arr)):
        to_index = int(get_range(sha_key,key_offset,range_len=8),16) % (len(arr) -i)
        key_offset += 1
        if key_offset >= len(sha_key): key_offset = 0
        arr[i],arr[to_index] = arr[to_index],arr[i]
    return arr

def encrypt_image(image:Image,psw:str):
    x_arr = [i for i in range(image.width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(image.height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            pixels[x, y], pixels[x_arr[x],y_arr[y]] = pixels[x_arr[x],y_arr[y]],pixels[x, y]

def dencrypt_image(image:Image,psw:str):
    x_arr = [i for i in range(image.width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(image.height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixels = image.load()
    for x in range(image.width):
        _x = image.width-x-1
        for y in range(image.height):
            _y = image.height-y-1
            pixels[_x, _y], pixels[x_arr[_x],y_arr[_y]] = pixels[x_arr[_x],y_arr[_y]],pixels[_x, _y]
          

class EncryptedImage(Image.Image):
    password = ''
    __name__ = 'EncryptedImage'
    
    @staticmethod
    def set_password(password):
        if PILImage.__name__ == 'EncryptedImage':
            print('supter')
            PILImage.password = password
        EncryptedImage.password = password
    
    @staticmethod
    def open(fp,*args, **kwargs):
        image = PILImage.open(fp,*args, **kwargs)
        encrypt_type = ''
        
        if image.format.lower() == PngImagePlugin.PngImageFile.format.lower():
            pnginfo = image.info or PngImagePlugin.PngInfo()
            encrypt_type = pnginfo["Encrypt"]
        elif image.format.lower() in (JpegImagePlugin.JpegImageFile.format.lower(), WebPImagePlugin.WebPImageFile.format.lower()):
            exif_dict = piexif.load(image.info["exif"])
            encrypt_type = exif_dict["Exif"]['Encrypt']
            
        if encrypt_type == 'pixel_shuffle':
            print('dencrypt: '+str(fp))
            dencrypt_image(image, EncryptedImage.password)
        return image

    def save(self, filename, format = None, pnginfo=None, *args, **kwargs):
        if not EncryptedImage.password:
            # 如果没有密码，直接保存
            super().save(filename, format = format, *args, **kwargs)
            print('***********')
        
        encrypt_image(self, get_sha256(EncryptedImage.password))
        print('***********')
        self.format = format or self.format or PngImagePlugin.PngImageFile.format
        if self.format.lower() == PngImagePlugin.PngImageFile.format.lower():
            pnginfo = pnginfo or PngImagePlugin.PngInfo()
            pnginfo.add_text('Encrypt', 'pixel_shuffle')
            super().save(filename, format=format, pnginfo=pnginfo, *args, **kwargs)
        elif self.format.lower() in (JpegImagePlugin.JpegImageFile.format.lower(), WebPImagePlugin.WebPImageFile.format.lower()):
            super().save(filename, format=format, *args, **kwargs)
            # self.info = self.info or {"exif":{'Exif':{}}}
            exif_dict = piexif.load(filename)
            if not exif_dict: exif_dict = {'Exif':{}}
            exif_dict["Exif"]['Encrypt'] = 'pixel_shuffle'
            exif_bytes = piexif.dump(exif_dict)
            super().save(filename, format=format, exif=exif_bytes, *args, **kwargs)
        else:
            super().save(filename, format=format, *args, **kwargs)

if Image.Image.__name__ != 'EncryptedImage':
    Image.Image = EncryptedImage

def preload(parser):
    parser.add_argument("--encrypt-pass", type=str, help="The password to enable image encryption.", default=None)
