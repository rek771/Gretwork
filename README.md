# Gradient Network Bot

一个用于 Gradient Network 的多代理自动化工具，支持多IP并发挂机。通过使用多个代理IP同时运行，提高挖矿效率。

[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-red?logo=telegram&logoColor=white)](https://t.me/ScriptFreedom)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-red?logo=telegram&logoColor=white)](https://t.me/ScriptFreedomGroup)

[![Gradient Airdrop Link](https://img.shields.io/badge/Gradient-Airdrop%20Link-red?logo=telegram&logoColor=white)](https://app.gradient.network/signup?code=D427WC)



## ✨ 主要特性

- 🚀 支持多个代理IP同时运行
- 🔄 自动登录并保持在线状态
- 👀 实时监控每个代理的连接状态
- 🛡️ 智能检测代理可用性
- 🎯 异常代理自动重连
- 🎨 美观的控制台界面
- 🔒 安全的进程管理

## 📋 系统要求

- Python 3.8+
- Chrome 浏览器
- 稳定的网络环境
- 充足的系统内存

## ☕如果你要请我喝咖啡 [手动狗头]

- **USDT (Solana):** `0xe8c36583d65d832d8c9f5b16193e156a12fae3f4`
- **USDT (BNB Smart Chain):** `0xe8c36583d65d832d8c9f5b16193e156a12fae3f4`
- **USDT (Arbitrum One):** `0xe8c36583d65d832d8c9f5b16193e156a12fae3f4`


## 🚀 快速开始

1. 克隆仓库
   ```bash
   git clone https://github.com/SaulGoodManC99/gradient-network-bot.git
   cd gradient-network-bot
   ```

2. 安装依赖
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows

   copy .env.example .env
   pip install -r requirements.txt
   ```

3. 配置环境变量
   修改 `.env` 文件：
   ```plaintext
   APP_USER=your_email@example.com
   APP_PASS=your_password
   PROXY=http://ip1:port1,http://ip2:port2
   ALLOW_DEBUG=False
   ```

4. 运行程序
   ```bash
   python main.py
   ```

5. 监控控制台输出以确保一切正常运行。

## ⚙️ 配置说明

### 代理配置
- 支持多种代理格式：
  ```
  http://ip:port
  http://username:password@ip:port
  socks5://ip:port
  ```
- 多个代理用逗号分隔
- 建议使用高质量的私人代理

### 环境变量
- `APP_USER`: Gradient 账号邮箱
- `APP_PASS`: Gradient 账号密码
- `PROXY`: 代理服务器列表
- `ALLOW_DEBUG`: 是否开启调试模式
- `FORCE_DOWNLOAD_CRX`: 是否强制更新扩展

## 📊 状态说明

程序运行时会显示以下状态：
- 代理连接状态
- 浏览器运行状态
- 登录状态
- 错误信息

示例：

## ⚠️ 注意事项

1. 账号安全
   - 请勿将配置文件上传至公开仓库
   - 定期更改账号密码
   - 使用可靠的代理服务商

2. 系统资源
   - 监控系统内存使用
   - 根据配置适当调整代理数量
   - 保持系统稳定运行

3. 网络环境
   - 确保网络稳定
   - 使用高质量代理
   - 避免使用公共代理

## 🔍 故障排除

1. 代理连接失败
   - 检查代理地址格式
   - 验证代理是否可用
   - 确认网络连接正常

2. 浏览器启动失败
   - 检查 Chrome 安装状态
   - 确保系统资源充足
   - 验证扩展文件完整性
   

3. 登录失败
   - 确认账号密码正确
   - 检查网络连接
   - 查看是否触发安全验证



