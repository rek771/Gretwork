import signal
import sys
import os
from core.logger import log

def setup_signal_handlers(browser_manager):
    """设置信号处理器"""
    def signal_handler(signum, frame):
        print('\n')
        log("收到终止信号，正在安全关闭...", "info")
        
        # 立即设置运行状态为False
        import main
        main.running = False
        
        # 强制关闭浏览器
        browser_manager.close_all()
        
        # 强制退出程序
        log("程序已终止", "info")
        os._exit(0)  # 使用 os._exit 来强制终止程序
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler) 