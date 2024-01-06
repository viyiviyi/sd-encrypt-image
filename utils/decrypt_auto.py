import os
from PIL import Image,PngImagePlugin
import hashlib
import sys
import numpy as np
import concurrent.futures

def get_range(input:str,offset:int,range_len=4):
    input = input+input
    offset = offset % len(input)
    return input[offset:offset+range_len]

def get_sha256(input:str):
    hash_object = hashlib.sha256()
    hash_object.update(input.encode('utf-8'))
    return hash_object.hexdigest()

def shuffle_arr(arr,key):
    sha_key = get_sha256(key)
    key_offset = 0
    for i in range(len(arr)):
        to_index = int(get_range(sha_key,key_offset,range_len=8),16) % (len(arr) -i)
        key_offset += 1
        if key_offset >= len(sha_key): key_offset = 0
        arr[i],arr[to_index] = arr[to_index],arr[i]
    return arr

def decrypt_image(image:Image.Image,psw):
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

def decrypt_image_v2(image:Image.Image, psw):
    width = image.width
    height = image.height
    x_arr = [i for i in range(width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixel_array = np.array(image)

    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    for x in range(width-1,-1,-1):
        _x = x_arr[x]
        temp = pixel_array[x].copy()
        pixel_array[x] = pixel_array[_x]
        pixel_array[_x] = temp
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    for y in range(height-1,-1,-1):
        _y = y_arr[y]
        temp = pixel_array[y].copy()
        pixel_array[y] = pixel_array[_y]
        pixel_array[_y] = temp

    image.paste(Image.fromarray(pixel_array))
    return image
    
def process_image(filename, output_filename, password):
    global decrypt_count
    decrypt_count += 1
    print(f'{decrypt_count}/{file_count}')
    try:
        image = Image.open(filename,formats=['PNG'])
        pnginfo = image.info or {}
        if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle':
            decrypt_image(image, password)
            pnginfo["Encrypt"] = None
            info = PngImagePlugin.PngInfo()
            for key in pnginfo.keys():
                if pnginfo[key]:
                    info.add_text(key,pnginfo[key])
            image.save(output_filename)
        if 'Encrypt' in pnginfo and pnginfo["Encrypt"] == 'pixel_shuffle_2':
            decrypt_image_v2(image, password)
            pnginfo["Encrypt"] = None
            info = PngImagePlugin.PngInfo()
            for key in pnginfo.keys():
                if pnginfo[key]:
                    info.add_text(key,pnginfo[key])
            image.save(output_filename,pnginfo=info)
        image.close()
    except Exception as e:
        print(str(e))
        print(f"解密 {filename} 文件时出错")

def main():
    if '-t' in sys.argv:
        threads_index = sys.argv.index('-t') + 1
        threads = int(sys.argv[threads_index])
    else:
        threads = None
    if '-d' in sys.argv:
        decrypt_dir_index = sys.argv.index('-d') + 1
        decrypt_dir = sys.argv[decrypt_dir_index]
    else:
        decrypt_dir = '.'
    # 判断是否传入密码参数
    if '-p' in sys.argv:
        password_index = sys.argv.index('-p') + 1
        password = sys.argv[password_index]
    else:
        password = input("请输入密码：")
    password = get_sha256(password)
    print(password)
    
    if '-y' in sys.argv:
        pass
    else:
        while True:
            choice = input("是否解密全部文件？(y/n)：")
            if choice.lower() == 'y':
                break
            elif choice.lower() == 'n':
                return
        
    # 创建保存解密后图片的目录 decrypt_output (如果不存在)
    output_dir = f"{decrypt_dir}/decrypt_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    skipped_files = []  # 存储已跳过的文件名
    
    global file_count, decrypt_count
    file_count = sum(1 for file in os.listdir(decrypt_dir) if file.endswith(('.jpg', '.jpeg', '.png', '.webp')))
    decrypt_count = 0
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
    futures = []
    for filename in os.listdir(decrypt_dir):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp') or filename.endswith('.jpeg'): 
            output_filename = os.path.join(output_dir, filename)
            if os.path.exists(output_filename):
                skipped_files.append(filename)
                print(f"已跳过 {filename} 文件")
                continue
            futures.append(executor.submit(process_image, filename, output_filename, password))
                    
    if skipped_files:
        file_count - len(skipped_files)
        print("已跳过以下文件：")
        for filename in skipped_files:
            print(filename)

if __name__ == "__main__":
    main()