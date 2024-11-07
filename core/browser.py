import os
import logging
import threading
import psutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import USER_AGENT, ALLOW_DEBUG
from core.logger import log
from core.extension import download_extension

class BrowserManager:
    def __init__(self):
        self.browsers = []
        self._lock = threading.Lock()
        self.driver_pids = set()
        
    def init_browser(self, proxy):
        """初始化浏览器实例"""
        options = webdriver.ChromeOptions()
        
        if proxy:
            log(f"设置代理: {proxy}", "info", proxy)
            time.sleep(0.1)
            options.add_argument(f'--proxy-server={proxy}')
        
        extension_path = download_extension()
        time.sleep(0.1)
        options.add_extension(extension_path)

        options.add_argument(f'user-agent={USER_AGENT}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-allow-origins=*')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        
        if not ALLOW_DEBUG:
            options.add_argument('--headless=new')
        
        service = Service(
            ChromeDriverManager().install(),
            log_output=os.devnull,
            log_level=logging.ERROR
        )
        browser = webdriver.Chrome(service=service, options=options)
        
        # 保存浏览器进程ID
        self.driver_pids.add(browser.service.process.pid)
        
        with self._lock:
            self.browsers.append(browser)
        return browser
    
    def close_all(self):
        """强制关闭所有浏览器进程"""
        log("正在关闭所有浏览器...", "info")
        
        def kill_process_tree(pid):
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.kill()
                parent.kill()
            except:
                pass

        # 立即终止所有Chrome进程
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc.info['pid'])
            except:
                continue

        # 并行终止所有进程
        threads = []
        for pid in chrome_processes:
            thread = threading.Thread(target=kill_process_tree, args=(pid,))
            thread.start()
            threads.append(thread)

        # 等待最多3秒
        start_time = time.time()
        while time.time() - start_time < 3:
            if not any(t.is_alive() for t in threads):
                break
            time.sleep(0.1)

        # 清理资源
        with self._lock:
            self.browsers.clear()
            self.driver_pids.clear()

        # 最后一次检查和强制清理
        for proc in psutil.process_iter(['name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass