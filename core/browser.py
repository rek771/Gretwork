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
        """Initialize browser instance"""
        options = webdriver.ChromeOptions()
        
        if proxy:
            log(f"Setting proxy: {proxy}", "info", proxy)
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
        
        # Save the browser process ID
        self.driver_pids.add(browser.service.process.pid)
        
        with self._lock:
            self.browsers.append(browser)
        return browser
    
    def close_all(self):
        """Force close all browser processes"""
        log("Closing all browsers...", "info")
        
        def kill_process_tree(pid):
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    child.kill()
                parent.kill()
            except:
                pass

        # Immediately terminate all Chrome processes
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc.info['pid'])
            except:
                continue

        # Terminate all processes in parallel
        threads = []
        for pid in chrome_processes:
            thread = threading.Thread(target=kill_process_tree, args=(pid,))
            thread.start()
            threads.append(thread)

        # Wait up to 3 seconds
        start_time = time.time()
        while time.time() - start_time < 3:
            if not any(t.is_alive() for t in threads):
                break
            time.sleep(0.1)

        # Clean up resources
        with self._lock:
            self.browsers.clear()
            self.driver_pids.clear()

        # Final check and forced cleanup
        for proc in psutil.process_iter(['name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass
