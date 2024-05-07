# -*- coding: utf-8 -*-
import json
import re
import random
from aiohttp import ClientSession
from typing import Any, Dict, Literal, Optional
from utils.mixiu_api.requests import aiorequests
from utils.mixiu_api.mixiu_api import (
    SOUL_SOOTHER_URL,
    RAINBOW_FLATTER_URL,
    CLERK_URL,
    JOKE_URL,
    AJOKE_URL,
    BING_HPIMAGE_URL,
    ONE_URL,
    LICKDOGDIARY_URL,
    VARSE_URL,
    TODAYINHISTORY_URL,
    HITOKOTO_URL)

from utils.message.log import _log

_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
async def _request(
    url: str,
    method: Literal['GET', 'POST'] = 'GET',
    header: Dict[str, Any] = _HEADER,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    sess: Optional[ClientSession] = None,
    # use_proxy: Optional[bool] = False,
)-> dict:
    '''
    :说明:
      访问URL并进行json解析返回。
    :参数:
      * url (str): API。
      * method (Literal['GET', 'POST']): `POST` or `GET`。
      * header (Dict[str, Any]): 默认为_HEADER。
      * params (Dict[str, Any]): 参数。
      * data (Dict[str, Any]): 参数(`post`方法需要传)。
      * sess (ClientSession): 可选, 指定client。
      * use_proxy (bool): 是否使用proxy 代理
    :返回:
      * result (dict): json.loads()解析字段。
    '''
    is_temp_sess = False
    if sess is None:
        sess = ClientSession()
        is_temp_sess = True
    try:

        req = await sess.request(
            method,
            url=url,
            headers=header,
            params=params,
            json=data,
            timeout=300,
        )
        text_data = await req.text()
        # DEBUG 日志
        print(f'【mhy_request】请求如下:\n{text_data}')
        if text_data.startswith('('):
            text_data = json.loads(text_data.replace('(', '').replace(')', ''))
            return text_data
        raw_data = await req.json()
        
        return raw_data
    except Exception:
        print(f'访问{url}失败！')
        return {'retcode': -1}
    finally:
        if is_temp_sess:
            await sess.close()





async def get_soul_soother():
    """
    获取毒鸡汤
    """
    try:
        data = await _request(
            url=SOUL_SOOTHER_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None 
        title = data['data']['text']
        if title == '':
            return None
        return title
    except Exception as e:
        print("获取心灵鸡汤出错:", e)
        return None





async def get_rainbow_flatter():
    """
    获取彩虹屁
    """
    try:
        data = await _request(
            url=RAINBOW_FLATTER_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None 
        title = data['data']['text']
        if title == '':
            return None
        return title
    except Exception as e:
        print("获取彩虹屁出错:", e)
        return None    

async def get_clerk():
    """
    获取文案、朋友圈
    """
    try:
        data = await _request(
            url=CLERK_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None 
        title = data['data']['text']
        if title == '':
            return None
        return title
    except Exception as e:
        print(f"获取文案、朋友圈出错:{e}")
        return None   

async def getHitokoto():
    """
    获取一言
    """
    try:
        data = await _request(
            url=HITOKOTO_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None 
        title = data['hitokoto']
        if title == '':
            return None
        return title
    except Exception as e:
        print(f"获取一言出错:{e}")
        return None   


async def getJoke():
    """
    获取笑话 http://api.juncikeji.xyz/api/qwxh.php 
    """
    try:
        data = await _request(
            url=JOKE_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None    
        title = data['result'][0]['content']
        if title == '':
            return None
        return title
    except Exception as e:
        print(f"获取笑话出错:{e}")
        return None 



async def getAJoke():
    """
    获取段子 https://www.hlapi.cn/api/gxdz
    """
    try:
        data = await aiorequests.get(
            url=AJOKE_URL,
            headers=_HEADER,
            )
        if data.status_code != 200:return None
        title = data.content.decode("utf-8")
        if title == '':
            return None
        return title
    except Exception as e:
        print(f"获取段子出错:{e}")
        return None 





async def getVarse():
    """
    获取诗句 "http://v1.jinrishici.com/rensheng.txt"
    """
    try:
        data = await aiorequests.get(
            url=VARSE_URL,
            headers=_HEADER,
            )
        if data.status_code != 200:return None
        title = data.content.decode("utf-8")
        if title == '':
            return None
        return title
    except:
        pass 
    return None

async def getTodayInHistory():
    """
    获取历史上的今天
    """
    try:
        data = await aiorequests.get(
            url=TODAYINHISTORY_URL,
            headers=_HEADER,
            )
        if data.status_code == 200:
            title = data.content.decode("utf-8")
            if '感谢 www.ipip5.com 提供数据支持!' in title:
                title = title.replace('感谢 www.ipip5.com 提供数据支持!','以史为鉴，可以知兴替')
                return title
    except:
        pass 
    return None


async def getLickdogdiary():
    """
    获取舔狗日记 https://api.juncikeji.xyz/api/tgrj.php
    """
    try:
        data = await aiorequests.get(
            url=LICKDOGDIARY_URL,
            headers=_HEADER,
            )
        if data.status_code != 200:return None
        title = data.content.decode("utf-8")
        if title == '':
            return None
        return title
    except Exception as e:
        print(f"获取舔狗日记出错:{e}")
        return None 

# 获取ONE一个图文数据

async def get_one():
    """
    获取one
    """
    data = ''
    try:
        data = await _request(
            url=ONE_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None
        return data
    except:
        pass 
    return data

# 获取bing每日壁纸数据
async def getBingHpimage():
    try:
        data = await _request(
            url=BING_HPIMAGE_URL,
            method='GET',
            header=_HEADER,
            )
        if 'retcode' in data:
            if data['retcode'] == -1:return None
        res = data["images"]
        r = list(res)
        r_number = len(r)
        if r_number == 0:return None
        r_number = random.randint(1,r_number)
        res = r[r_number-1]
        bing_pic = "https://cn.bing.com/" + res["url"]
        bing_title = res["title"]
        bing_content = re.sub("\\(.*?\\)", "", res["copyright"])
        bing_tip = f"{bing_title}——{bing_content}"
        return {
            "bing_pic": bing_pic,
            "bing_tip": bing_tip
        }
    except Exception as e:
        print("获取必应数据出错:", e)
        return None



