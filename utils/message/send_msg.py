
# 发送消息
from botpy import BotAPI
from botpy.message import Message
import asyncio
import random
from botpy.types.message import Ark, ArkKv, ArkObj, ArkObjKv, Embed, EmbedField, Thumbnail
import traceback
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Literal, Optional,Union, BinaryIO
from utils.message.log import _log

async def post_msg_common(
        api: BotAPI, 
        message: Message, 
        number = 1, 
        content: Optional[str] = None, 
        image_path: Union[str,Path,BytesIO] = None, 
        image_url:Optional[str] = None,
        at:Optional[bool] = None,
        ) -> bool:
    """
    多次尝试发送消息 文本/本地图片/网络图片
    number: 尝试发送次数
    content: 文本消息
    image_path: 本地图片地址 
    image_url: 图片网址
    at: 艾特回复的对象
    """
    if isinstance(image_path, Path):
        image_path = str(image_path)
    if isinstance(image_path, BytesIO):
        image_path = image_path.getvalue()
    
    if at and content is not None:
        content = f'<@{message.author.id}>'+ content

    _log.info(f"{message.id}:【尝试发送消息】 {image_url} {content}")
    i = 0

    while i < number:
        
        _log.info(f"{message.id}:【发送消息{str(i)}次】")
        try:
            if content is not None and image_path is not None and image_url is not None:
                _log.info(f"【发送】:文本带本地图片带网络图片")
                await api.post_message(msg_id=message.id, channel_id = message.channel_id, file_image = image_path, image = image_url)
            elif content is not None and image_path is not None and image_url is None:
                _log.info(f"【发送】:文本带本地图片")
                await api.post_message(msg_id=message.id, content = content, channel_id = message.channel_id, file_image = image_path)
            elif content is not None and image_path is None and image_url is not None:
                _log.info(f"【发送】:文本带网络图片")
                await api.post_message(msg_id=message.id, content = content, channel_id = message.channel_id, image = image_url)  
            elif content is not None and image_path is None and image_url is None:
                _log.info(f"【发送】:纯文本")
                await api.post_message(msg_id=message.id, content = content, channel_id = message.channel_id)
            elif content is None and image_path is not None and image_url is None:
                _log.info(f"【发送】:本地图片")
                await api.post_message(msg_id=message.id, channel_id = message.channel_id, file_image = image_path)
            elif content is None and image_path is None and image_url is not None:
                _log.info(f"【发送】:网络图片")
                await api.post_message(msg_id=message.id, channel_id = message.channel_id, image = image_url)
            else:
                _log.info(f"{message.id}:【发送消息{str(i)}次】 {image_url} {content},错误信息：没有写任何发送参数")

                return False

            return True
        except asyncio.TimeoutError:

            _log.error(f"{message.id}:【发送消息{str(i)}次】 {image_url} {content},错误信息：超时请求连接")
            _log.error("post_msg_common failed: %s" % traceback.format_exc())
            await asyncio.sleep(random.randint(3, 6))
        except Exception as e:

            _log.error(f"{message.id}:【发送消息{str(i)}次】 {image_url} {content},错误信息：{repr(e)}")
            _log.error("post_msg_common failed: %s" % traceback.format_exc())
            await asyncio.sleep(random.randint(3, 6))
        i += 1
    _log.info(f"{message.id}:【发送消息{str(i)}次】 {image_url} {content},错误信息：指定重试次数完毕后依旧没有发送成功")    

    return False

async def post_msg_embed(
        api: BotAPI, 
        message: Message, 
        number : int, 
        embed: Embed
        ) -> bool:
    """
    多次尝试发送embed消息
    number: 尝试发送次数
    embed: embed消息
    
    """

    _log.info(f"{message.id}:【尝试发送消息】{embed}")
    i = 0
    while i < number:
        try:
            await api.post_message(msg_id=message.id, channel_id=message.channel_id, embed=embed)

            return  True
        except asyncio.TimeoutError:

            _log.error(f"{message.id}:【发送消息{str(i)}次】{embed},错误信息：{repr(e)}")
            _log.error("post_msg_embed failed: %s" % traceback.format_exc())
            await asyncio.sleep(random.randint(3, 6))
        except Exception as e:

            _log.error(f"{message.id}:【发送消息{str(i)}次】{embed},错误信息：{repr(e)}")
            _log.error("post_msg_embed failed: %s" % traceback.format_exc())
            await asyncio.sleep(random.randint(3, 6))
        i += 1

    return False