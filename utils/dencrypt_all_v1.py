from PIL import Image
import hashlib
import os
import sys

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



def main():
    # 判断是否传入密码参数
    if '-p' in sys.argv:
        password_index = sys.argv.index('-p') + 1
        password = sys.argv[password_index]
    else:
        password = input("请输入密码：")
    password = get_sha256(password)
    print(password)
    # 询问是否解密全部文件，并循环提示直到输入合法选项（y或n）

    while True:
        choice = input("是否解密全部文件？(y/n)：")
        if choice.lower() == 'y':
            break
        elif choice.lower() == 'n':
            return
        
    # 创建保存解密后图片的目录 dencrypt_output (如果不存在)
    output_dir = "dencrypt_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    skipped_files = []  # 存储已跳过的文件名
    
    for filename in os.listdir('.'):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp') or filename.endswith('.jpeg'): 
            output_filename = os.path.join(output_dir, filename)
            if os.path.exists(output_filename):
                skipped_files.append(filename)
                print(f"已跳过 {filename} 文件")
                continue
            try:
                image = Image.open(filename)
                dencrypt_image(image,password) 
                image.save(output_filename)
                image.close()
            except Exception as e:
                print(str(e))
                print(f"解密 {filename} 文件时出错")
                    
    if skipped_files:
        print("已跳过以下文件：")
        for filename in skipped_files:
            print(filename)

if __name__ == "__main__":
    main()