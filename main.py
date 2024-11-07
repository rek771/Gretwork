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

# 禁用 TensorFlow 日志
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# 全局变量
running = True
browser_manager = BrowserManager()

def check_proxy_status(browser):
    """检查代理连接状态"""
    try:
        browser.get("http://ip-api.com/json")
        WebDriverWait(browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        return True, "代理连接正常"
    except Exception as e:
        error_msg = str(e)
        if "ERR_PROXY_CONNECTION_FAILED" in error_msg:
            return False, "代理连接失败"
        elif "timeout" in error_msg.lower():
            return False, "代理连接超时"
        else:
            return False, "代理异常"

def worker(proxy):
    """工作线程"""
    browser = None
    try:
        log("启动浏览器实例", "info", proxy)
        browser = browser_manager.init_browser(proxy)
        
        log("开始登录", "info", proxy)
        try:
            browser.get("https://app.gradient.network/")
        except Exception as e:
            if running:
                if "Connection aborted" in str(e) or "Connection reset" in str(e):
                    log(f"代理 {proxy} 无法访问，请检查代理地址或端口是否正确", "error", proxy)
                    return
                raise e
            return
        
        # 登录流程
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
        
        # 验证登录成功
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(text(), "Copy Referral Link")]')
        ))
        log("登录成功", "success", proxy)
        
        # 加载扩展
        log("正在加载扩展", "info", proxy)
        try:
            browser.get(f"chrome-extension://{EXTENSION_ID}/popup.html")
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Status")]')
            ))
            log("扩展加载成功，开始运行...", "success", proxy)
        except Exception as e:
            if running:
                raise e
            return
        
        # 状态监控
        while running:
            proxy_ok, proxy_status = check_proxy_status(browser)
            proxy_display = proxy.split('@')[0] if '@' in proxy else proxy
            status_msg = (
                f"[proxy: {proxy_display}] "
                f"Browser Status: {'正常运行中' if proxy_ok else '异常'} "
                f"Proxy Status: {proxy_status}"
            )
            log(status_msg, "status", proxy)
            
            # 如果代理连接失败，关闭浏览器并退出线程
            if not proxy_ok:
                log(f"代理 {proxy_display} 连接失败，关闭浏览器实例", "error", proxy)
                if browser:
                    browser.quit()
                return
                
            time.sleep(60)
            
    except Exception as e:
        if running:
            proxy_display = proxy.split('@')[0] if '@' in proxy else proxy
            log(f"代理 {proxy_display} 发生错误，关闭浏览器实例", "error", proxy)
    finally:
        if browser:
            try:
                browser.quit()
            except:
                pass

def main():
    try:
        # 显示启动横幅
        print_banner()
        
        if not USER or not PASSWORD:
            log("请设置 APP_USER 和 APP_PASS 环境变量", "error", "system")
            return
            
        log(f"启动程序 - 用户: {USER}", "info", "system")
        log(f"调试模式: {ALLOW_DEBUG}", "info", "system")
        
        # 设置信号处理
        setup_signal_handlers(browser_manager)
        
        # 启动工作线程
        proxies = os.getenv('PROXY', '').split(',')
        proxies = [p.strip() for p in proxies if p.strip()]
        
        threads = []
        for proxy in proxies:
            thread = threading.Thread(target=worker, args=(proxy,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # 主循环
        while running and any(t.is_alive() for t in threads):
            time.sleep(1)
            
    except KeyboardInterrupt:
        log("程序被用户终止", "info")
    except Exception as e:
        log(f"程序异常: {str(e)}", "error")
    finally:
        browser_manager.close_all()

if __name__ == '__main__':
    main()