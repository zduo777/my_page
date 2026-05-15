import os
import sqlite3
import json
from datetime import datetime
import markdown
from flask import Flask, render_template, abort, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'myblog-secret-key-2026'

# 导航站访问密码
NAV_PASSWORD = 'csj892800'

# 解锁图案: 0-1-2-5-8 (L形)
NAV_PATTERN = '01258'

# ----- 数据库初始化 -----
DB_PATH = 'database.db'

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
    if not os.path.exists('posts'):
        os.makedirs('posts')
        # 创建一篇示例文章
        with open('posts/hello-world.md', 'w', encoding='utf-8') as f:
            f.write('# 你好，世界！\n\n这是我的第一篇博客文章。')
        with open('posts/second-post.md', 'w', encoding='utf-8') as f:
            f.write('# 第二篇文章\n\n继续写博客吧！')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 获取已有slug
    c.execute('SELECT slug FROM posts')
    existing = {row[0] for row in c.fetchall()}

    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            slug = filename[:-3]  # 去掉 .md
            if slug not in existing:
                # 读取标题（取第一行 # 内容）
                with open(os.path.join('posts', filename), 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.lstrip('# ').strip()
                    if not title:
                        title = slug.replace('-', ' ').title()
                created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c.execute('INSERT INTO posts (title, slug, created_at) VALUES (?, ?, ?)',
                          (title, slug, created))
    conn.commit()
    conn.close()

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

# ----- 启动 -----
if __name__ == '__main__':
    init_db()
    scan_posts()
    app.run(host='0.0.0.0', port=5000, debug=True)