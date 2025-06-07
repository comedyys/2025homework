from flask import Flask,render_template
from flask import request
app = Flask(__name__)

# 首页路由
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# 登录表单路由(GET请求时显示表单)
@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">登录</button></p>
              </form>'''

# 登录处理路由(POST请求时验证)
@app.route('/signin', methods=['POST'])
def signin():
    # 从请求对象读取表单数据
    if request.form['username']=='admin' and request.form['password']=='password':
        return render_template('signin-ok.html')
    return '<h3>用户名或密码错误。</h3>'

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/signin-ok')
def signin_ok():
    return render_template('signin-ok.html')


if __name__ == '__main__':
    app.run(debug=True)