#!/bin/bash
# MyPage 部署脚本 - 在腾讯云 VPS 上执行

set -e

echo "===== 开始部署 MyPage ====="

# 配置变量
PROJECT_DIR="/var/www/my_page"
GIT_REPO="https://github.com/zduo777/my_page.git"

# 1. 安装依赖
echo ">>> 安装系统依赖..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# 2. 克隆或更新代码
if [ -d "$PROJECT_DIR" ]; then
    echo ">>> 更新代码..."
    cd $PROJECT_DIR
    git pull
else
    echo ">>> 克隆代码..."
    sudo mkdir -p /var/www
    cd /var/www
    git clone $GIT_REPO
    cd my_page
fi

# 3. 创建虚拟环境并安装依赖
echo ">>> 安装 Python 依赖..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. 初始化数据库（首次启动会自动创建）
echo ">>> 启动服务..."
python app.py &
sleep 3
pkill -f "python app.py" || true

# 5. 配置 Systemd 服务
echo ">>> 配置 Systemd 服务..."
sudo cp my_page.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable my_page
sudo systemctl start my_page

# 6. 配置 Nginx（先修改 nginx.conf 中的域名）
echo ">>> 配置 Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/my_page
sudo ln -sf /etc/nginx/sites-available/my_page /etc/nginx/sites-enabled/my_page
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 7. 开放防火墙端口
echo ">>> 配置防火墙..."
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "===== 部署完成! ====="
echo "请访问: http://你的服务器IP 或域名"
echo ""
echo "常用命令:"
echo "  查看状态: sudo systemctl status my_page"
echo "  重启服务: sudo systemctl restart my_page"
echo "  查看日志: sudo journalctl -u my_page -f"