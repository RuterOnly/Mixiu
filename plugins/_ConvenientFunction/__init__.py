# -*- coding: utf-8 -*-
from utils.message.decorated import Commands
from botpy import BotAPI
from botpy.message import Message
from utils.mixiu_api.get_mixiu_data import (
    getTodayInHistory,
    getJoke,
    getAJoke,
    getVarse,
    get_rainbow_flatter,
    getBingHpimage,
    get_one,
    get_clerk,
    get_soul_soother,
    getLickdogdiary,
    getHitokoto,
    )
from utils.message.words import BotReply
from utils.message.send_msg import (
    post_msg_common,
    post_msg_embed,)
from utils.img.signimg import(
    imgYaSuoUrl,
)
from utils.message.string import (
    set_embed
)

# 便民功能集
from utils.message.log import _log


@Commands(name=("/一言", "一言", "随机一言",))
async def OneSentence(api: BotAPI, message: Message, params=None):
    txt = await getHitokoto()
    if txt == None:
        txt = BotReply.NO_FUNCTION
    await post_msg_common(api, message, 2, content = txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True,content='内容来自hitokoto,若侵权请联系删除。')
    return True  


@Commands(name=("笑话", "/笑话", "随机笑话"))
async def Joke(api: BotAPI, message: Message, params=None):
    txt = ''
    txt = await getJoke()
    if txt == '':
        txt = await getAJoke()
        if txt == '':
            txt = BotReply.NO_FUNCTION    
    txt = txt.replace('\r\n','\n')
    await post_msg_common(api, message, 2, content=txt)
    return True

@Commands(name=("诗句", "/诗句", "随机诗句",))
async def Varse(api: BotAPI, message: Message, params=None):
    txt = await getVarse()
    if txt == None:
        txt = BotReply.NO_FUNCTION
    txt = [txt]
    txt = set_embed(message.author.avatar,'诗句',txt)
    await post_msg_embed(api, message, 2, embed=txt)
    return True


@Commands(name=("/情话",'情话'))
async def MorningNewspaper(api: BotAPI, message: Message, params=None):
    txt = await get_rainbow_flatter()
    if txt == None:
        txt = BotReply.NO_FUNCTION
    await post_msg_common(api, message, 2, content = txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True,content='内容来自互联网,若侵权请联系删除。')
    return True      

@Commands(name=("壁纸", "/壁纸", "每日壁纸"))
async def wallpaper(api: BotAPI, message: Message, params=None):
    txt = await getBingHpimage()
    if txt == None:
        txt = BotReply.NO_FUNCTION
        await post_msg_common(api, message, 2, content = txt)
        return False     
    try:
        await post_msg_common(api, message, 4, image_url = txt['bing_pic'], content = txt['bing_tip'])
    except:
        txt = txt['bing_pic']
        txts = await imgYaSuoUrl(txt,'壁纸',5*60,True)
        _log.info(f"{message.id}:【壁纸】图片下载：{txts}")
        if txts !='':
            if await post_msg_common(api, message,  4, image_path = txts) == False:
                _log.info(f"{message.id}:【壁纸】发送失败：{txts}")
        else:
            _log.info(f"{message.id}:【壁纸】网络发图：{txt}")
            await post_msg_common(api, message,  4, image_url = txt)
    await post_msg_common(api, message, 2, at = True, content='内容来自Bing,若侵权请联系删除。')
    _log.info(f"{message.id}:【壁纸】处理完毕")
    return True


@Commands(name=("one", '/one'))
async def mood(api: BotAPI, message: Message, params=None):
    txt = await get_one()
    if txt == None or txt == '':
        txt = BotReply.NO_FUNCTION
        await post_msg_common(api, message, 2, content=txt)
        return False
         
    strs = await imgYaSuoUrl(txt['content'],'one',0,is_yasuo_jpg=True)
    if strs == '':
        txts = set_embed(txt['content'],'one',[txt['name']])
        await post_msg_embed(api, message, 2, embed=txts)
    else:
        await post_msg_common(api, message,  6, image_path =  strs)
    await post_msg_common(api, message, 2, content=txt['name'])
    await post_msg_common(api, message, 2, at = True, content='内容来自One,若侵权请联系删除。')

    return True        

@Commands(name=("文案", "朋友圈"))
async def Copywriting(api: BotAPI, message: Message, params=None):
    txt = await get_clerk()
    if txt == None:
        txt = BotReply.NO_FUNCTION

    await post_msg_common(api, message, 2, content=txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True, content='内容来自网络,若侵权请联系删除。')
    return True


@Commands(name=("历史今天", "历史上的今天"))
async def Today_In_History(api: BotAPI, message: Message, params=None):
    txt = await getTodayInHistory()
    if txt == None:
        txt = BotReply.NO_FUNCTION

    await post_msg_common(api, message, 2, content=txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True, content='内容来自网络,若侵权请联系删除。')
    return True


@Commands(name=("心灵鸡汤", "毒鸡汤"))
async def SoulSoothe(api: BotAPI, message: Message, params=None):
    txt = await get_soul_soother()
    if txt == None:
        txt = BotReply.NO_FUNCTION    
    await post_msg_common(api, message, 2, content=txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True, content='内容来自互联网,若侵权请联系删除。')
    return True


@Commands(name=("舔狗日记"))
async def LickDogDiary(api: BotAPI, message: Message, params=None):
    txt = await getLickdogdiary()
    if txt == None:
        txt = BotReply.NO_FUNCTION    
    await post_msg_common(api, message, 2, content=txt)
    if txt != BotReply.NO_FUNCTION:
        await post_msg_common(api, message, 2, at = True, content='内容来自互联网,若侵权请联系删除。')
    return True