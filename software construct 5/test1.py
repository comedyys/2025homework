"""
Flask 用户认证系统
功能：提供用户登录、首页展示等基础功能
"""
from flask import Flask, render_template, request
from flasgger import Swagger

app = Flask(__name__)

# 配置 Flasgger
swagger = Swagger(app, template={
    "info": {
        "title": "用户认证API",
        "description": "提供用户登录和页面展示功能",
        "version": "1.0"
    },
    "tags": [
        {"name": "页面", "description": "前端页面展示"},
        {"name": "认证", "description": "用户登录认证"}
    ]
})

@app.route('/', methods=['GET', 'POST'])
def home():
    """首页展示
    ---
    tags:
      - 页面
    responses:
      200:
        description: 返回首页HTML
    """
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    """显示登录表单
    ---
    tags:
      - 认证
    responses:
      200:
        description: 返回登录表单HTML
    """
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">登录</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    """处理登录请求
    ---
    tags:
      - 认证
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
        format: password
    responses:
      200:
        description: 登录成功页面
      401:
        description: 用户名或密码错误
    """
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return render_template('signin-ok.html')
    return '<h3>用户名或密码错误。</h3>', 401

@app.route('/home')
def home_page():
    """备用首页路由
    ---
    tags:
      - 页面
    responses:
      200:
        description: 返回首页HTML
    """
    return render_template('home.html')

@app.route('/form')
def form():
    """表单测试页
    ---
    tags:
      - 页面
    responses:
      200:
        description: 返回表单测试页HTML
    """
    return render_template('form.html')

@app.route('/signin-ok')
def signin_ok():
    """登录成功页
    ---
    tags:
      - 页面
    responses:
      200:
        description: 返回登录成功页HTML
    """
    return render_template('signin-ok.html')

if __name__ == '__main__':
    app.run(debug=True)
    