from PIL import Image as PILImage,PngImagePlugin
from core import get_sha256,decrypt_image,decrypt_image_v2
import os


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