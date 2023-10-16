from PIL import Image
import hashlib

def get_range(input:str,offset:int,range_len=4):
    if (offset+range_len)<len(input):
        return input[offset:offset+range_len]
    else: return input[offset:]+input[:range_len - (len(input) - offset)]

def get_sha256(input:str):
    hash_object = hashlib.sha256()
    # 更新hash对象的内容
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

def encrypt_image(image,psw):
    x_arr = [i for i in range(image.width)]
    shuffle_arr(x_arr,psw)
    y_arr = [i for i in range(image.height)]
    shuffle_arr(y_arr,get_sha256(psw))
    pixels = image.load()
    # offfset = 0
    # for x in range(image.width):
    #     for y in range(image.height):
    #         pix = pixels[x,y]
    #         arr = get_range(psw,offfset,range_len=6)
    #         offfset += 1
    #         if offfset >= len(psw): offfset = 0
    #         r = pix[0]^(int(arr[0:2],16)&0xFF)
    #         g = pix[1]^(int(arr[2:4],16)&0xFF)
    #         b = pix[2]^(int(arr[4:6],16)&0xFF)
    #         pixels[x, y] = (r,g,b) if len(pix) == 3 else (r,g,b,pix[3])
    for x in range(image.width):
        for y in range(image.height):
            pixels[x, y], pixels[x_arr[x],y_arr[y]] = pixels[x_arr[x],y_arr[y]],pixels[x, y]

def dencrypt_image(image,psw):
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
    # offfset = 0
    # for x in range(image.width):
    #     for y in range(image.height):
    #         pix = pixels[x,y]
    #         arr = get_range(psw,offfset,range_len=6)
    #         offfset += 1
    #         if offfset >= len(psw): offfset = 0
    #         r = pix[0]^int(arr[0:2],16)
    #         g = pix[1]^int(arr[2:4],16)
    #         b = pix[2]^int(arr[4:6],16)
    #         pixels[x, y] = (r,g,b) if len(pix) == 3 else (r,g,b,pix[3])
    
    print('***********')