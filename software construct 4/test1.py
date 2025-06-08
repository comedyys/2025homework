# pylint: disable=missing-module-docstring
from flask import Flask, request

# 创建Flask应用实例
app = Flask(__name__)

# 首页路由 - 居中显示的Hello World


@app.route('/', methods=['GET', 'POST'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .centered {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
            }
            h1 {
                color: blue;
                font-size: 3em;
            }
        </style>
    </head>
    <body>
        <div class="centered">
            <h1>Hello World!</h1>
            <p><a href="/signin">前往登录页面</a></p>
        </div>
    </body>
    </html>
    '''

# 登录表单路由(GET方法)


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            form {
                width: 300px;
                margin: 50px auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input, button {
                width: 100%;
                padding: 8px;
                margin: 8px 0;
                box-sizing: border-box;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <form action="/signin" method="post">
            <p><input name="username" placeholder="用户名" required></p>
            <p><input name="password" type="password" placeholder="密码" required></p>
            <p><button type="submit">登录</button></p>
        </form>
    </body>
    </html>
    '''

# 登录处理路由(POST方法)


@app.route('/signin', methods=['POST'])
def signin():
    # 从请求对象获取表单数据
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    text-align: center;
                    padding: 50px;
                    font-family: Arial, sans-serif;
                }
                h3 {
                    color: green;
                }
            </style>
        </head>
        <body>
            <h3>欢迎，管理员！</h3>
            <p><a href="/">返回首页</a></p>
        </body>
        </html>
        '''
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
            }
            h3 {
                color: red;
            }
        </style>
    </head>
    <body>
        <h3>用户名或密码错误</h3>
        <p><a href="/signin">重新登录</a></p>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
