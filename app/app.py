from PIL import Image as PILImage
import hashlib
import os

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

import os
from tkinter import *
from tkinter import filedialog, messagebox
base_directory = ''
def browse_directory():
    directory = filedialog.askdirectory()
    global base_directory
    if directory:
        label_base_dir.config(text=directory)
        base_directory = directory

def encrypt_files():
    password = entry.get()
    directory = base_directory
    if not password:
        messagebox.showerror("错误", "请输入密码")
        return
    
    password = get_sha256(password)
    
    while True:
        choice = messagebox.askquestion("解密文件", "是否解密全部文件？")
        
        if choice == 'yes':
            break
        
        elif choice == 'no':
            return
        
   
    output_dir = os.path.join(directory, "dencrypt_output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    skipped_files = []  
    status.config(text='正在解密')
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if (os.path.isfile(filepath) and 
            (filename.endswith('.jpg') or 
                filename.endswith('.png') or 
                filename.endswith('.webp') or 
                filename.endswith('.jpeg'))): 
                
            output_filename = os.path.join(output_dir, filename)
            
            if os.path.exists(output_filename):
                skipped_files.append(filename)
                print(f"已跳过 {filename} 文件")
                continue
            try:
                image = PILImage.open(filepath)
                dencrypt_image(image, password) 
                image.save(output_filename)
                image.close()
                    
            except Exception as e:
                print(str(e))
                print(f"解密 {filename} 文件时出错")
                        
    if skipped_files:
        messagebox.showinfo("已跳过文件", "\n".join(skipped_files))

    status.config(text='解密完成')
    
root = Tk()
root.title("图片解密工具")
root.geometry('500x200')

label = Label(root, text="请输入密码：")
label.pack()

entry = Entry(root)
entry.pack()

button = Button(root, text="选择目录", command=browse_directory)
button.pack()

label_base_dir = Label(root, text="")
label_base_dir.pack()

button_start = Button(root, text="开始解密", command=encrypt_files)
button_start.pack()

status = Label(root, text="")
status.pack()

root.mainloop()