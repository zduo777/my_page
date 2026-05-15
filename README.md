# MyPage - 个人导航与博客系统

一个基于 Flask 的个人导航站与博客系统，支持 Markdown 文章渲染。

## 目录结构

```
my_page/
├── app.py               # Flask 主程序
├── requirements.txt     # Python 依赖
├── posts/               # Markdown 文章目录
├── templates/           # HTML 模板
│   ├── base.html
│   ├── index.html
│   ├── blog.html
│   ├── nav.html
│   └── post.html
├── static/              # 静态文件 (CSS)
└── data/                # 数据文件
    └── nav.json         # 导航配置
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python app.py
```

### 访问

浏览器打开 http://127.0.0.1:5000

## 功能

- 首页
- 博客文章列表
- 文章详情页（Markdown 渲染）
- 导航站 - 可自定义配置
- 导航设置面板（拖拽排序）

## 写新文章

在 `posts/` 目录下新建 `.md` 文件，重启服务即可自动导入。

## 部署到服务器

```bash
# 修改 deploy.sh 中的仓库地址
./deploy.sh
```

## 常用运维命令

```bash
sudo systemctl status my_page   # 查看状态
sudo systemctl restart my_page  # 重启服务
sudo journalctl -u my_page -f   # 查看日志
```