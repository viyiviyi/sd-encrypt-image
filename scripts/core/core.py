from PIL import Image
import hashlib
import numpy as np

def get_range(input:str,offset:int,range_len=4):
    offset = offset % len(input)
    return (input*2)[offset:offset+range_len]

def get_sha256(input:str):
    hash_object = hashlib.sha256()
    hash_object.update(input.encode('utf-8'))
    return hash_object.hexdigest()

def shuffle_arr(arr,key):
    sha_key = get_sha256(key)
    arr_len = len(arr)
    for i in range(arr_len):
        to_index = int(get_range(sha_key,i,range_len=8),16) % (arr_len -i)
        arr[i],arr[to_index] = arr[to_index],arr[i]
    return arr

def shuffle_arr_v2(arr,key):
    sha_key = get_sha256(key)
    arr_len = len(arr)
    s_idx = arr_len
    for i in range(arr_len):
        s_idx = arr_len - i - 1
        to_index = int(get_range(sha_key,i,range_len=8),16) % (arr_len -i)
        arr[s_idx],arr[to_index] = arr[to_index],arr[s_idx]
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


def encrypt_image_v3(image:Image.Image, psw):
    '''
    return: pixel_array
    '''
    width = image.width
    height = image.height
    x_arr = np.arange(width)
    shuffle_arr_v2(x_arr,psw) 
    y_arr = np.arange(height)
    shuffle_arr_v2(y_arr,get_sha256(psw))
    pixel_array = np.array(image)
    
    _pixel_array = pixel_array.copy()
    for x in range(height): 
        pixel_array[x] = _pixel_array[y_arr[x]]
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    
    _pixel_array = pixel_array.copy()
    for x in range(width): 
        pixel_array[x] = _pixel_array[x_arr[x]]
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))

    return pixel_array

def decrypt_image_v3(image:Image.Image, psw):
    '''
    return: pixel_array
    '''
    width = image.width
    height = image.height
    x_arr = np.arange(width)
    shuffle_arr_v2(x_arr,psw)
    y_arr = np.arange(height)
    shuffle_arr_v2(y_arr,get_sha256(psw))
    pixel_array = np.array(image)
    
    _pixel_array = pixel_array.copy()
    for x in range(height): 
        pixel_array[y_arr[x]] = _pixel_array[x]
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    
    _pixel_array = pixel_array.copy()
    for x in range(width): 
        pixel_array[x_arr[x]] = _pixel_array[x]
    pixel_array = np.transpose(pixel_array, axes=(1, 0, 2))
    
    return pixel_array
