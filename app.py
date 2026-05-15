import os
import sqlite3
import json
from datetime import datetime
import markdown
from flask import Flask, render_template, abort, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'myblog-secret-key-2026'

# 导航站访问密码
NAV_PASSWORD = 'csj8928010'

# 博客管理密码
BLOG_PASSWORD = 'csj8928010'

# 解锁图案: 0-1-2-5-8 (L形)
NAV_PATTERN = '01258'

# ----- 数据库初始化 -----
DB_PATH = 'database.db'
POSTS_DIR = 'posts'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  slug TEXT UNIQUE NOT NULL,
                  created_at TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 扫描 posts 目录下的 .md 文件，自动导入数据库（如果尚未导入）
def scan_posts():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 获取已有slug
    c.execute('SELECT slug FROM posts')
    existing = {row[0] for row in c.fetchall()}

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]  # 去掉 .md
            if slug not in existing:
                # 读取标题（取第一行 # 内容）
                filepath = os.path.join(POSTS_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.lstrip('# ').strip()
                    if not title:
                        title = slug.replace('-', ' ').title()
                created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c.execute('INSERT INTO posts (title, slug, created_at) VALUES (?, ?, ?)',
                          (title, slug, created))
    conn.commit()
    conn.close()

# 生成唯一的 slug
def generate_slug(title):
    # 使用时间戳确保唯一性
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # 简化标题作为slug前缀
    import re
    slug_prefix = re.sub(r'[^\w一-鿿-]', '-', title.lower())[:30]
    slug_prefix = re.sub(r'-+', '-', slug_prefix).strip('-')
    return f"{slug_prefix}-{timestamp}"

# ----- 路由 -----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title, slug, created_at FROM posts ORDER BY created_at DESC')
    posts = [{'id': row[0], 'title': row[1], 'slug': row[2], 'created_at': row[3]} for row in c.fetchall()]
    conn.close()
    return render_template('blog.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT title, created_at FROM posts WHERE slug = ?', (slug,))
    row = c.fetchone()
    conn.close()
    if not row:
        abort(404)

    # 读取 Markdown 文件
    filepath = os.path.join('posts', f'{slug}.md')
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 转化为 HTML
    html_content = markdown.markdown(content, extensions=['fenced_code'])

    return render_template('post.html', title=row[0], created_at=row[1], content=html_content)

@app.route('/nav')
def nav():
    # 检查是否已验证密码
    if not session.get('nav_authenticated'):
        return render_template('nav_login.html')

    with open('data/nav.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    return render_template('nav.html', links=links)

@app.route('/nav/verify', methods=['POST'])
def nav_verify():
    password = request.form.get('password', '')
    if password == NAV_PASSWORD:
        session['nav_authenticated'] = True
        return redirect(url_for('nav'))
    else:
        return render_template('nav_login.html', error='密码错误')

@app.route('/nav/verify-pattern', methods=['POST'])
def nav_verify_pattern():
    data = request.get_json()
    pattern = data.get('pattern', '')
    if pattern == NAV_PATTERN:
        session['nav_authenticated'] = True
        return {'success': True}
    return {'success': False}

@app.route('/api/nav', methods=['GET'])
def api_get_nav():
    with open('data/nav.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/nav/save', methods=['POST'])
def api_save_nav():
    if not session.get('nav_authenticated'):
        return {'error': '未授权'}, 401
    data = request.get_json()
    with open('data/nav.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {'success': True}

# ----- 博客管理 -----
@app.route('/write')
def write():
    # 需要登录才能写博客
    if not session.get('blog_authenticated'):
        return render_template('blog_login.html')
    return render_template('write.html')

@app.route('/blog/verify', methods=['POST'])
def blog_verify():
    password = request.form.get('password', '')
    if password == BLOG_PASSWORD:
        session['blog_authenticated'] = True
        return redirect(url_for('write'))
    else:
        return render_template('blog_login.html', error='密码错误')

@app.route('/blog/logout')
def blog_logout():
    session.pop('blog_authenticated', None)
    return redirect(url_for('blog'))

@app.route('/api/blog/create', methods=['POST'])
def api_create_post():
    if not session.get('blog_authenticated'):
        return {'error': '未授权'}, 401

    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return {'error': '标题和内容不能为空'}, 400

    # 生成slug
    slug = generate_slug(title)

    # 保存markdown文件
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n{content}')

    # 写入数据库
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO posts (title, slug, created_at) VALUES (?, ?, ?)',
              (title, slug, created))
    conn.commit()
    conn.close()

    return {'success': True, 'slug': slug}

@app.route('/api/blog/update/<slug>', methods=['POST'])
def api_update_post(slug):
    if not session.get('blog_authenticated'):
        return {'error': '未授权'}, 401

    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return {'error': '标题和内容不能为空'}, 400

    # 更新markdown文件
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    if not os.path.exists(filepath):
        return {'error': '文章不存在'}, 404

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n{content}')

    # 更新数据库标题
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE posts SET title = ? WHERE slug = ?', (title, slug))
    conn.commit()
    conn.close()

    return {'success': True}

@app.route('/api/blog/delete/<slug>', methods=['POST'])
def api_delete_post(slug):
    if not session.get('blog_authenticated'):
        return {'error': '未授权'}, 401

    # 删除markdown文件
    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    if os.path.exists(filepath):
        os.remove(filepath)

    # 删除数据库记录
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE slug = ?', (slug,))
    conn.commit()
    conn.close()

    return {'success': True}

@app.route('/api/blog/rescan', methods=['POST'])
def api_rescan_posts():
    if not session.get('blog_authenticated'):
        return {'error': '未授权'}, 401

    scan_posts()
    return {'success': True}

@app.route('/api/blog/raw/<slug>', methods=['GET'])
def api_get_post_raw(slug):
    if not session.get('blog_authenticated'):
        return {'error': '未授权'}, 401

    filepath = os.path.join(POSTS_DIR, f'{slug}.md')
    if not os.path.exists(filepath):
        return {'error': '文章不存在'}, 404

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析标题和正文
    lines = content.split('\n')
    title = ''
    body_start = 0
    if lines and lines[0].startswith('#'):
        title = lines[0].lstrip('#').strip()
        body_start = 1
        # 跳过空行
        while body_start < len(lines) and lines[body_start].strip() == '':
            body_start += 1

    body_content = '\n'.join(lines[body_start:])

    return {'title': title, 'content': body_content}

# ----- 启动 -----
if __name__ == '__main__':
    init_db()
    scan_posts()
    app.run(host='0.0.0.0', port=5000, debug=True)