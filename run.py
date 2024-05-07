# -*- coding: utf-8 -*-
import botpy
from botpy.guild import Guild
from botpy.message import Message
from botpy.message import DirectMessage
import datetime
from botpy.ext.cog_yaml import read
import os
# 载入机器人配置
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
from utils.message.send_msg import post_msg_common
# 载入插件
from plugins._ConvenientFunction import (    # 便民
    OneSentence,        # 一言 
    Joke,               # 笑话
    Varse,              # 诗句
    MorningNewspaper,   # 情话
    wallpaper,          # 壁纸
    Copywriting,        # 文案
    mood,               # 心情 
    Today_In_History,   # 历史上的今天
    SoulSoothe,         # 毒鸡汤
    LickDogDiary,       # 舔狗日记 
    )

from utils.message.log import _log
class MyClient(botpy.Client):
    # 机器人上线信息
    async def on_ready(self):
        _log.info("======================")
        if self.robot != None:
            _log.info(f"机器人 「{self.robot.name}」 ")
        content =  datetime.datetime.now()
        content = content.strftime("%Y-%m-%d %H:%M:%S")
        _log.info(content)
        _log.info("上线了!")
        _log.info("======================")
    
    # 当机器人加入新guild时
    async def on_guild_create(self, guild: Guild):
        """
        此处为处理该事件的代码
        """

        # 基本信息日志输出
        _log.info("======================")
        _log.info(
            f"【机进】频道：{guild.id} ||  名称：{guild.name} || 描述：{guild.description}")
        _log.info(
            f"【咪咻机器人加入频道】")
        _log.info("======================")
        
        

        
    # 当机器人退出guild时
    async def on_guild_delete(self, guild: Guild):
        """
        此处为处理该事件的代码
        """

        # 基本信息日志输出
        _log.info("======================")
        _log.info(
            f"{guild.event_id}:【机退】频道：{guild.id} ||  名称：{guild.name} || 加入：{guild.joined_at}")
        _log.info(
            f"【咪咻机器人退出频道】")
        _log.info("======================")
        
        
        
    # 成员私信机器人信息    
    async def on_direct_message_create(self, message: DirectMessage):
        # 基本信息日志输出
        _log.info("======================")
        _log.info(
            f"{message.id}:【私信】频道：{message.guild_id} ||  用户：{message.author.id} || 昵称：{message.author.username}|| 内容：{message.content}")
        _log.info("======================")



    # 公域 艾特机器人信息
    async def on_at_message_create(self, message: Message):
        start_times = datetime.datetime.now()
        # 基本信息日志输出
        _log.info("======================")
        _log.info(
            f"{message.id}:【公域】频道：{message.guild_id} || 子频道：{message.channel_id} || 用户：{message.author.id} || 昵称：{message.author.username} || 内容：{message.content}")
        _log.info("======================")
        _log.info(f'接受消息|内容：{message.content}|处理时间:{datetime.datetime.now()} ')
    
        # 注册指令handler
        handlers = [
           
            
            # 便民
            OneSentence,             # 一言
            Joke,                    # 笑话            
            Varse,                   # 诗句
            MorningNewspaper,        # 情话
            wallpaper,               # 壁纸
            Copywriting,             # 文案
            mood,                    # 心情
            Today_In_History,        # 历史上的今天
            SoulSoothe,              # 毒鸡汤
            LickDogDiary,            # 舔狗日记


            
        ]
        
        status = None
        for handler in handlers:
            try:
                status = await handler(api=self.api, message=message)
                if status:
                    _log.info(f'有效事件|{handler}事件成功|处理时间:{datetime.datetime.now() - start_times} ')
                    return
                elif status == False:
                    _log.info(f'有效事件|{handler}事件正常处理失败|处理时间:{datetime.datetime.now() - start_times} ')
                    return
            except  Exception as e:
                _log.error(f'有效事件|{handler}事件异常处理失败|失败原因{e}|处理时间:{datetime.datetime.now() - start_times} ')
                await post_msg_common(self.api, message, 2, at =True, content = f'指令正常响应，但是处理失败，可以联系反馈。')
                return 

        if status == None:
            _log.warning(f'无效事件|未响应指令事件|处理时间:{datetime.datetime.now() - start_times} ')
            await post_msg_common(self.api, message, 2, at =True, content = f'您发送的不是指令呢？')
        return    





if __name__ == "__main__":
    # 初始化
    # 沙盒开关
    is_sandbox = False  
    intents = botpy.Intents(public_guild_messages=True, guild_members= True, direct_message=True, guilds=True)
    client = MyClient(intents = intents, is_sandbox=is_sandbox, timeout=60)
    client.run(appid=test_config["appid"], secret=test_config["secret"])

 
    
  
