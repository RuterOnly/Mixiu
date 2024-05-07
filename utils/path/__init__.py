from pathlib import Path

# parents：如果父目录不存在，是否创建父目录。
# exist_ok：只有在目录不存在时创建目录，目录已存在时不会抛出异常。

# ==========================
# 主目录
_PATH = Path().cwd()

#缓存目录
CACHE_PATH = _PATH / 'cache'
CACHE_PATH.mkdir(parents=True, exist_ok=True)