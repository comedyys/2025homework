# data_access.py
import csv
import sqlite3
from typing import List, Dict, Optional

def load_movies() -> List[Dict]:
    """从CSV加载电影数据"""
    movies = []
    csv_file_path = r'C:\Users\20342\Desktop\final\CSV\douban_movies.csv'
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

def create_user(username: str, password: str) -> None:
    """创建新用户（密码需已加密）"""
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
              (username, password))
    conn.commit()
    conn.close()

def get_user(username: str) -> Optional[Dict]:
    """根据用户名获取用户"""
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return {"id": user[0], "username": user[1], "password": user[2]} if user else None

# 收藏数据访问
def add_favorite(user_id: int, movie_title: str) -> None:
    """添加电影到收藏"""
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('INSERT INTO favorites (user_id, movie_title) VALUES (?, ?)', 
              (user_id, movie_title))
    conn.commit()
    conn.close()

def get_favorites(user_id: int) -> List[Dict]:
    """获取用户的收藏列表"""
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('SELECT * FROM favorites WHERE user_id = ?', (user_id,))
    favorites = [{"id": row[0], "movie_title": row[2]} for row in c.fetchall()]
    conn.close()
    return favorites