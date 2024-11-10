import os
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import USER, PASSWORD, ALLOW_DEBUG, EXTENSION_ID
from core.logger import log, print_banner
from core.browser import BrowserManager
from utils.helpers import setup_signal_handlers

# Disable TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Global variables
running = True
browser_manager = BrowserManager()

def check_proxy_status(browser):
    """Check the proxy connection status"""
    try:
        browser.get("http://ip-api.com/json")
        WebDriverWait(browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        return True, "Proxy connection is normal"
    except Exception as e:
        error_msg = str(e)
        if "ERR_PROXY_CONNECTION_FAILED" in error_msg:
            return False, "Proxy connection failed"
        elif "timeout" in error_msg.lower():
            return False, "Proxy connection timed out"
        else:
            return False, "Proxy error"

def worker(proxy):
    """Worker thread"""
    browser = None
    try:
        log("Starting browser instance", "info", proxy)
        browser = browser_manager.init_browser(proxy)
        
        log("Starting login", "info", proxy)
        try:
            browser.get("https://app.gradient.network/")
        except Exception as e:
            if running:
                if "Connection aborted" in str(e) or "Connection reset" in str(e):
                    log(f"Proxy {proxy} cannot access, please check if the proxy address or port is correct", "error", proxy)
                    return
                raise e
            return
        
        # Login process
        wait = WebDriverWait(browser, 30)
        email_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[placeholder="Enter Email"]')
        ))
        password_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[type="password"]')
        ))
        login_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button')
        ))
        
        email_input.send_keys(USER)
        password_input.send_keys(PASSWORD)
        login_button.click()
        
        # Verify login success
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(text(), "Copy Referral Link")]')
        ))
        log("Login successful", "success", proxy)
        
        # Load extension
        log("Loading extension", "info", proxy)
        try:
            browser.get(f"chrome-extension://{EXTENSION_ID}/popup.html")
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Status")]')
            ))
            log("Extension loaded successfully, starting to run...", "success", proxy)
        except Exception as e:
            if running:
                raise e
            return
        
        # Status monitoring
        while running:
            proxy_ok, proxy_status = check_proxy_status(browser)
            proxy_display = proxy.split('@')[0] if '@' in proxy else proxy
            status_msg = (
                f"[proxy: {proxy_display}] "
                f"Browser Status: {'Running normally' if proxy_ok else 'Abnormal'} "
                f"Proxy Status: {proxy_status}"
            )
            log(status_msg, "status", proxy)
            
            # If the proxy connection fails, close the browser and exit the thread
            if not proxy_ok:
                log(f"Proxy {proxy_display} connection failed, closing browser instance", "error", proxy)
                if browser:
                    browser.quit()
                return
                
            time.sleep(60)
            
    except Exception as e:
        if running:
            proxy_display = proxy.split('@')[0] if '@' in proxy else proxy
            log(f"Proxy {proxy_display} encountered an error, closing browser instance", "error", proxy)
    finally:
        if browser:
            try:
                browser.quit()
            except:
                pass

def main():
    try:
        # Display startup banner
        print_banner()
        
        if not USER or not PASSWORD:
            log("Please set APP_USER and APP_PASS environment variables", "error", "system")
            return
            
        log(f"Starting the program - User: {USER}", "info", "system")
        log(f"Debug mode: {ALLOW_DEBUG}", "info", "system")
        
        # Set up signal handling
        setup_signal_handlers(browser_manager)
        
        # Start worker threads
        proxies = os.getenv('PROXY', '').split(',')
        proxies = [p.strip() for p in proxies if p.strip()]
        
        threads = []
        for proxy in proxies:
            thread = threading.Thread(target=worker, args=(proxy,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Main loop
        while running and any(t.is_alive() for t in threads):
            time.sleep(1)
            
    except KeyboardInterrupt:
        log("Program terminated by the user", "info")
    except Exception as e:
        log(f"Program exception: {str(e)}", "error")
    finally:
        browser_manager.close_all()

if __name__ == '__main__':
    main()
