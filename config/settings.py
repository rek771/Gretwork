import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 常量定义
EXTENSION_ID = "caacbgbklghmpodbdafajbgdnegacfmo"
CRX_URL = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=98.0.4758.102&acceptformat=crx2,crx3&x=id%3D{EXTENSION_ID}%26uc&nacl_arch=x86-64"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

# 环境变量
USER = os.getenv("APP_USER", "")
PASSWORD = os.getenv("APP_PASS", "")
ALLOW_DEBUG = os.getenv("ALLOW_DEBUG") == "True"
FORCE_DOWNLOAD_CRX = os.getenv("FORCE_DOWNLOAD_CRX") == "True"

# 文件路径
EXTENSION_FILENAME = "app.crx" 