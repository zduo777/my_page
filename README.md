# MyPage - 个人导航与博客系统

一个基于 Flask 的个人导航站与博客系统，支持 Markdown 文章渲染和在线编辑。

## 功能特点

- 🏠 **首页** - 每日一句名言（自动获取，防缓存）
- 📝 **博客系统** - 支持 Markdown 格式，在线写作与编辑
- 🧭 **导航站** - 可自定义配置，支持拖拽排序
- 🔐 **密码保护** - 导航站和博客管理均有密码验证
- ⚙️ **设置系统** - 全局齿轮按钮，支持导航设置和密码设置

## 目录结构

```
my_page/
├── app.py               # Flask 主程序
├── requirements.txt     # Python 依赖
├── gunicorn.conf.py     # 生产服务器配置
├── my_page.service      # Systemd 服务配置
├── nginx.conf           # Nginx 配置
├── deploy.sh            # 部署脚本
├── posts/               # Markdown 文章目录
│   └── *.md             # 博客文章文件
├── templates/           # HTML 模板
│   ├── base.html        # 基础模板（含全局齿轮按钮）
│   ├── index.html       # 首页（每日一句）
│   ├── blog.html        # 博客列表
│   ├── post.html        # 文章详情
│   ├── write.html       # 写博客页面
│   ├── nav.html         # 导航站
│   ├── nav_login.html   # 导航登录页
│   ├── settings.html    # 设置入口页面
│   ├── nav_settings.html    # 导航设置页面
│   └── password_settings.html # 密码设置页面
├── static/              # 静态文件
│   └── style.css        # 样式文件
└── data/                # 数据文件
    ├── nav.json         # 导航配置
    └── config.json      # 密码配置
```

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问 http://127.0.0.1:5000
```

### 密码配置

首次使用时，需要在 `data/config.json` 中配置密码：

```json
{ 
    "nav_password": "your_password_here",
    "nav_pattern": "your_pattern_here", 
    "blog_password": "your_password_here" 
}
```

| 配置项 | 说明 |
|--------|------|
| `nav_password` | 导航站文字密码 |
| `nav_pattern` | 导航站滑动密码（九宫格数字序列） |
| `blog_password` | 博客管理密码 |

1. **查看博客** - `/blog` 查看所有文章列表
2. **写博客** - `/write` 登录后在线写作，支持 Markdown
3. **编辑/删除** - 登录后可编辑或删除现有文章
4. **重新扫描** - 手动添加 `.md` 文件后，点击"重新扫描"导入

### 导航站

1. **访问** - `/nav` 需要密码验证
2. **设置入口** - 左下角齿轮按钮（鼠标悬停显示）
3. **拖拽排序** - 支持分类和链接的拖拽排序
4. **添加/删除** - 支持添加新分类和链接

### 设置系统

全局设置按钮位于页面左下角，鼠标悬停时显示，点击进入设置页面。

**设置入口** `/settings`
- 导航设置 → `/settings/nav`
- 密码设置 → `/settings/password`

**导航设置**
- 分类总览拖拽排序
- 分类名称编辑
- 链接添加/删除/排序

**密码设置**
- 导航页文字密码
- 导航页滑动密码（九宫格可视化设置）
- 博客管理密码

## 部署到服务器

### 一键部署

```bash
# 修改 deploy.sh 中的仓库地址
# 修改 nginx.conf 中的域名/IP

chmod +x deploy.sh
./deploy.sh
```

### 手动部署

```bash
# 安装依赖
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx -y

# 克隆代码
cd /var/www
git clone https://github.com/zduo777/my_page.git
cd my_page

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
sudo cp my_page.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable my_page
sudo systemctl start my_page

# 配置 Nginx
sudo cp nginx.conf /etc/nginx/sites-available/my_page
sudo ln -s /etc/nginx/sites-available/my_page /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

## 常用运维命令

```bash
sudo systemctl status my_page   # 查看状态
sudo systemctl restart my_page  # 重启服务
sudo journalctl -u my_page -f   # 查看日志
sudo nginx -t                   # 测试 nginx 配置
```

## 写新文章

### 方式一：在线写作
1. 访问 `/write`
2. 输入密码登录
3. 填写标题和内容（Markdown 格式）
4. 点击发布

### 方式二：本地文件
1. 在 `posts/` 目录下新建 `.md` 文件
2. 文件名格式：`文章标题.md`
3. 文件第一行写 `# 标题`
4. 登录博客管理，点击"重新扫描文章"

## 技术栈

- **后端**: Flask 2.3.3
- **前端**: HTML + CSS + JavaScript
- **数据库**: SQLite
- **渲染**: Markdown
- **生产服务器**: Gunicorn + Nginx

## License

MIT