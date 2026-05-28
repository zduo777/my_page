#!/usr/bin/env python3
"""
GitHub Webhook 接收服务
当GitHub仓库收到push时，自动触发此webhook，拉取更新并重启服务
"""

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# 简单的密钥验证（可选，建议设置）
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '')

@app.route('/webhook', methods=['POST'])
def webhook():
    # 验证密钥（如果设置了）
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            return jsonify({'error': '缺少签名'}), 401

    data = request.json

    # 只处理main分支的push事件
    if data.get('ref') == 'refs/heads/main':
        try:
            # 拉取最新代码
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd='/var/www/my_page',
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # 重启my_page服务
                subprocess.run(['sudo', 'systemctl', 'restart', 'my_page'])
                return jsonify({
                    'status': 'success',
                    'message': '更新成功',
                    'output': result.stdout
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'git pull失败',
                    'error': result.stderr
                }), 500

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'ignored', 'message': '非main分支'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)