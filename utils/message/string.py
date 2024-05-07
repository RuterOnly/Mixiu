
# 处理消息

from botpy.types.message import Ark, ArkKv, ArkObj, ArkObjKv, Embed, EmbedField, Thumbnail


def set_embed(avatar:str, name:str, lists:list)->Embed:
    """
    author:str 头像
    name:str 菜单名称
    lists:embed
    """
    fieldes = []
    for field in lists:
        fieldes.append(EmbedField(name = field))
    embed = Embed(
                title=name,
                prompt=name,
                thumbnail=Thumbnail(url=avatar),
                fields=fieldes,)
    return embed
