from PIL import Image
import hashlib
import numpy as np

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
    key_len = len(sha_key)
    arr_len = len(arr)
    key_offset = 0
    for i in range(arr_len):
        to_index = int(get_range(sha_key,key_offset,range_len=8),16) % (arr_len -i)
        key_offset += 1
        if key_offset >= key_len: key_offset = 0
        arr[i],arr[to_index] = arr[to_index],arr[i]
    return arr

def encrypt_image(image:Image.Image, psw):
    width = image.width
    height = image.height
    x_arr = [i for i in range(width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixels = image.load()
    for x in range(width):
        _x = x_arr[x]
        for y in range(height):
            _y = y_arr[y]
            pixels[x, y], pixels[_x,_y] = pixels[_x,_y],pixels[x, y]

def decrypt_image(image:Image.Image, psw):
    width = image.width
    height = image.height
    x_arr = [i for i in range(width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixels = image.load()
    for x in range(width-1,-1,-1):
        _x = x_arr[x]
        for y in range(height-1,-1,-1):
            _y = y_arr[y]
            pixels[x, y], pixels[_x,_y] = pixels[_x,_y],pixels[x, y]
    
def encrypt_image_v2(image:Image.Image, psw):
    width = image.width
    height = image.height
    x_arr = [i for i in range(width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixel_array = np.array(image)

    for y in range(height):
        _y = y_arr[y]
        temp = pixel_array[y].copy()
        pixel_array[y] = pixel_array[_y]
        pixel_array[_y] = temp
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    for x in range(width):
        _x = x_arr[x]
        temp = pixel_array[x].copy()
        pixel_array[x] = pixel_array[_x]
        pixel_array[_x] = temp
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))

    image.paste(Image.fromarray(pixel_array))
    return image

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
