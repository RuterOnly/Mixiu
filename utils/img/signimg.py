# -*- coding: utf-8 -*-
# 图片处理
import os
import requests
import random
import hashlib
from PIL import ImageFont, ImageDraw, Image, ImageFile, ImageOps
import time

from utils.path import CACHE_PATH
from aiohttp.client import ClientSession
from typing import Tuple, Union, Optional
from aiohttp.client_exceptions import ClientConnectorSSLError,ClientConnectorError
from shutil import copyfile
import aiofiles
import numpy as np
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]



def download_from_url(url, download_path):
    with open(download_path, 'wb') as handle:
        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url=url, headers=headers, stream=True, timeout=30, allow_redirects=False, verify=False)
        chunk_size = 1024
        for chunk in response.iter_content(chunk_size=chunk_size):
            handle.write(chunk)
        response.close()  

async def download_file(
    sess: ClientSession,
    url: str,
    path: str,
) -> Optional[Tuple[str, int, str]]:
    try:
        async with sess.get(url) as res:
            content = await res.read()
    except ClientConnectorError:
        return url
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)
           
           
# 第二种 递归删除dir_path目标文件夹下所有文件，以及各级子文件夹下文件，保留各级空文件夹
# (支持文件，文件夹不存在不报错)
def del_files(dir_path):
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_lis = os.listdir(dir_path)
        for file_name in file_lis:
            if file_name != 'time.info':
                tf = os.path.join(dir_path, file_name)
                del_files(tf)

def binali_wenjianjia(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    n = len(file_list)
    ind = np.random.randint(0,n)
    img_dir = os.path.join(path,file_list[ind])
    print(img_dir)
    if 'time.info' in img_dir:
        return binali_wenjianjia(path)
    return img_dir

async def imgYaSuoUrl(user_pic:str, 
                      input: str, 
                      img_time = 0, 
                      bianli_status: bool = False, 
                      img_new_path='', 
                      resize_status: bool = True,
                      is_path: bool = False,
                      is_yasuo_jpg: bool = False):
    """

    user_pic: 网络图片地址
    input: 图片文件夹名称 功能名
    img_time: 图片保存时间
    bianli_status: 如果图片失败是否遍历文件夹
    img_new_path: 是否自定义图片地址
    resize_status: 是否压缩图片
    is_path: 是否是本地图片
    is_yasuo_jpg: 是否将图片全部压缩为jpg图片
    """
    times =time.time()
    img_path = CACHE_PATH / input
    if not os.path.isdir(img_path):
        print(f"新建缓存功能【{input}】文件夹")
        os.makedirs(img_path)
    if img_time != 0:            
        if os.path.exists(img_path / 'time.info'):
            with open(img_path / "time.info", 'r+') as f:
                try:
                    info_time = f.read()
                    print(f"{user_pic}:成功读取保存时间")
                except:
                    print(f"{user_pic}:读取保存时间失败")
                print(f"{user_pic}:上次保存时间：" + info_time)    
                if info_time == '':
                   info_time = time.time()
                   f.write(str(info_time))  
            
                time_ = time.time() - float(info_time)
                if time_ > img_time:
                    del_files(img_path)
                    with open(img_path / "time.info", 'w+') as f:
                        f.write(str(time.time()))

        else:
            with open(img_path / "time.info", 'w') as f:
                info_time = time.time()
                f.write(str(info_time))
    if img_new_path == '':
        user_pic_md5 = hashlib.md5(user_pic.encode(encoding='utf-8')).hexdigest()
    else:
        user_pic_md5 = img_new_path
    user_pic_md5 = str(img_path / user_pic_md5)
    
    if os.path.exists(user_pic_md5 + '.png') or os.path.exists(user_pic_md5 + '.jpg'):
        if os.path.exists(user_pic_md5 + '.png'):
             user_pic = user_pic_md5 + '.png'
        if os.path.exists(user_pic_md5 + '.jpg'):
             user_pic = user_pic_md5 + '.jpg'     
    else:
        if(is_path):
            copyfile(user_pic, user_pic_md5)
        else:
            if (await download_file(ClientSession(),user_pic,user_pic_md5)) == user_pic:
                print('协程下载图片失败')
                download_from_url(user_pic,user_pic_md5)
        try:
            try:
                user_pic_ = user_pic.rindex('.')
                pic_type = user_pic[user_pic_:]
                if pic_type == '.png':
                    print(f"{user_pic}:【网页】这是一张png图片")
                    user_pic_new = Image.open(user_pic_md5).convert("RGBA")
                elif pic_type == '.jpg':
                    print(f"{user_pic}:【网页】这是一张jpg图片")
                    user_pic_new = Image.open(user_pic_md5).convert("RGB")
                else:
                    try:
                        user_pic_new = Image.open(user_pic_md5).convert("RGBA")
                        pic_type = '.png'
                        print(f"{user_pic}:【网页】这是一张png图片") 
                    except:
                        user_pic_new = Image.open(user_pic_md5).convert("RGB")
                        pic_type = '.jpg'
                        print(f"{user_pic}:【网页】这是一张jpg图片") 
            except:
                try:
                    user_pic_new = Image.open(user_pic_md5).convert("RGBA")
                    pic_type = '.png'
                    print(f"{user_pic}:【尝试】这是一张png图片") 
                except:
                    user_pic_new = Image.open(user_pic_md5).convert("RGB")
                    pic_type = '.jpg'
                    print(f"{user_pic}:【尝试】这是一张jpg图片") 

            os.remove(user_pic_md5)
            user_pic_md5 = user_pic_md5 + pic_type
            if resize_status == True:
                if pic_type == '.png' or pic_type == '.jpg':
                    size = user_pic_new.size
                    if size[0] >= 1000 or size[1] >= 1000:
                        user_pic_new = user_pic_new.resize((int(size[0]/2.5),int(size[1]/2.5)))
                    elif size[0] >= 1500 or size[1] >= 1500:
                        user_pic_new = user_pic_new.resize((int(size[0]/3.5),int(size[1]/3.5)))
                    else:
                        user_pic_new = user_pic_new.resize((size[0], size[1]))

                if not is_yasuo_jpg:
                    user_pic_new.save(user_pic_md5,quality = 50)
                else:
                    user_pic_md5 = user_pic_md5.replace('png','jpg')
                    user_pic_new = user_pic_new.resize((size[0], size[1])).convert('RGB')
                    user_pic_new.save(user_pic_md5,quality = 50,subsampling=0,)        
            else:
                user_pic_new.save(user_pic_md5)
            user_pic_new.close()
            user_pic = user_pic_md5
            
            print(f"{user_pic}:保存图片成功") 
        except:
            print(f"{user_pic}:保存图片失败")
            user_pic = ''
            if os.path.exists(user_pic_md5):
                print("删除失败文件")
                os.remove(user_pic_md5) 
    if user_pic == '' and bianli_status:
        print(f"{user_pic}:文件夹随机取图片")
        return binali_wenjianjia(img_path)
    print(f"{user_pic}:本次保存图片花费{int(time.time()-times)}S")
    return user_pic  


