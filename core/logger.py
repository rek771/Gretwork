from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the startup banner"""
    banner = f"""
{Fore.CYAN}
   ____               _ _            _     _   _      _                      _    ____        _   
  / ___|_ __ __ _  __| (_) ___ _ __ | |_  | \ | | ___| |___      _____  _ __| | _| __ )  ___ | |_ 
 | |  _| '__/ _` |/ _` | |/ _ \ '_ \| __| |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /  _ \ / _ \| __|
 | |_| | | | (_| | (_| | |  __/ | | | |_  | |\  |  __/ |_ \ V  V / (_) | |  |   <| |_) | (_) | |_ 
  \____|_|  \__,_|\__,_|_|\___|_| |_|\__| |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\____/ \___/ \__|
                                                                                                    
{Style.RESET_ALL}
{Fore.GREEN}[ Gradient Network Bot ]{Style.RESET_ALL} - Powered by ScriptFreedom@SaulGoodMan
{Fore.YELLOW}[ Version ]{Style.RESET_ALL} 1.0.0
"""
    print(banner)

def log(message, level="info", proxy=None):
    """Unified log output format"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if level == "info":
        print(f"{Fore.WHITE}{timestamp} {Fore.CYAN}[{proxy}] {Fore.GREEN}INFO: {Style.RESET_ALL}{message}")
    elif level == "error":
        print(f"{Fore.WHITE}{timestamp} {Fore.CYAN}[{proxy}] {Fore.RED}ERROR: {Style.RESET_ALL}{message}")
    elif level == "success":
        print(f"{Fore.WHITE}{timestamp} {Fore.CYAN}[{proxy}] {Fore.YELLOW}SUCCESS: {Style.RESET_ALL}{message}")
    elif level == "status":
        # Use different colors to distinguish different parts of status information
        proxy_part = f"[proxy: {message.split(']')[0].split(': ')[1]}]"
        browser_label = "Browser Status:"
        browser_value = "Running normally" if "正常运行中" in message else "Abnormal"
        proxy_label = "Proxy Status:"
        proxy_value = message.split("Proxy Status: ")[1]
        
        if "Proxy connection normal" in message:
            print(
                f"{Fore.WHITE}{timestamp} "
                f"{Fore.CYAN}{proxy_part} "
                f"{Fore.WHITE}{browser_label} {Fore.GREEN}{browser_value} "
                f"{Fore.WHITE}{proxy_label} {Fore.GREEN}{proxy_value}"
                f"{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.WHITE}{timestamp} "
                f"{Fore.CYAN}{proxy_part} "
                f"{Fore.WHITE}{browser_label} {Fore.RED}{browser_value} "
                f"{Fore.WHITE}{proxy_label} {Fore.RED}{proxy_value}"
                f"{Style.RESET_ALL}"
            )
