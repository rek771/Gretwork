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

# ... other code remains unchanged ...

        # Load the extension
        log("Loading the extension", "info", proxy)
        browser.get(f"chrome-extension://{EXTENSION_ID}/popup.html")
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[contains(text(), "Status")]')
        ))
        log("Extension loaded successfully", "success", proxy)

# ... the rest of the code remains unchanged ...
