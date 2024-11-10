import os
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timedelta
from config.settings import CRX_URL, USER_AGENT, EXTENSION_FILENAME, ALLOW_DEBUG
from core.logger import log

def download_extension():
    """Download the extension file"""
    crx_path = Path(EXTENSION_FILENAME)
    if crx_path.exists():
        if datetime.fromtimestamp(crx_path.stat().st_mtime) > datetime.now() - timedelta(days=1):
            log("Extension already exists, skipping download", "info", "extension")
            return os.path.abspath(EXTENSION_FILENAME)

    log("Downloading extension...", "info", "extension")
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(CRX_URL, headers=headers)
    with open(EXTENSION_FILENAME, "wb") as f:
        f.write(response.content)
    
    if ALLOW_DEBUG:
        md5 = hashlib.md5(response.content).hexdigest()
        log(f"Extension MD5: {md5}", "info", "extension")
    
    return os.path.abspath(EXTENSION_FILENAME)
