import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
from business_logic import (
    filter_movies_by_year, 
    validate_user, 
    register_user, 
    add_movie_to_favorites,
    get_user_favorites
)
from data_access import load_movies,get_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 生产环境需替换为随机密钥

# 初始化数据库表（首次运行时执行）
def init_database():
    import sqlite3
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    movie_title TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    conn.commit()
    conn.close()

init_database()  # 应用启动时自动创建表（开发环境适用）

# 首页
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            flash('用户名或密码不能为空', 'error')
            return redirect(url_for('register'))
        if register_user(username, password):
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
        else:
            flash('用户名已存在', 'error')
    return render_template('register.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if validate_user(username, password):
            session['user'] = username
            flash('登录成功', 'success')
            return redirect(url_for('movie_search'))
        else:
            flash('用户名或密码错误', 'error')
    return render_template('login.html')

# 登出路由
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('已登出', 'info')
    return redirect(url_for('home'))

# 电影搜索路由
@app.route('/movie_search', methods=['GET', 'POST'])
def movie_search():
    if 'user' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        year = request.form.get('release_year', '').strip()
        movies = filter_movies_by_year(year)
        return render_template('index.html', movies=movies, year=year, username=session['user'])
    return render_template('movie_search.html', username=session.get('user'))

# 添加收藏路由（通过表单提交）
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    if 'user' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('login'))
    movie_title = request.form.get('movie_title', '').strip()
    if not movie_title:
        flash('电影名称不能为空', 'error')
        return redirect(url_for('movie_search'))
    
    # 获取用户真实ID（之前用hash是临时方案，现在从数据库查询）
    user = get_user(session['user'])
    if user:
        add_movie_to_favorites(user['id'], movie_title)
        flash('电影已添加到收藏', 'success')
    else:
        flash('用户信息异常，请重新登录', 'error')
    return redirect(url_for('movie_search'))

# 查看收藏路由
@app.route('/favorites')
def favorites():
    if 'user' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('login'))
    user = get_user(session['user'])
    if not user:
        flash('用户信息异常，请重新登录', 'error')
        return redirect(url_for('login'))
    favorites = get_user_favorites(user['id'])
    return render_template('favorites.html', favorites=favorites, username=session['user'])

if __name__ == '__main__':
    app.run(debug=True)