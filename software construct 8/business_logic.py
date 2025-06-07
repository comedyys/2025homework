# business_logic.py
from typing import List,Dict
from data_access import load_movies, create_user, get_user, add_favorite, get_favorites
from werkzeug.security import generate_password_hash, check_password_hash

# 电影逻辑
def filter_movies_by_year(year: str) -> List[str]:
    """根据年份筛选电影"""
    movies = load_movies()
    if year.isdigit():
        return [m['\ufeff标题'] for m in movies if m['年份'] == year]
    return []

# 用户认证逻辑
def register_user(username: str, password: str) -> bool:
    """注册新用户"""
    if get_user(username):
        return False  # 用户已存在
    hashed_password = generate_password_hash(password)
    create_user(username, hashed_password)
    return True

def validate_user(username: str, password: str) -> bool:
    """验证用户登录"""
    user = get_user(username)
    if not user:
        return False
    return check_password_hash(user['password'], password)

# 收藏逻辑
def add_movie_to_favorites(user_id: int, movie_title: str) -> None:
    """添加电影到收藏"""
    add_favorite(user_id, movie_title)

def get_user_favorites(user_id: int) -> List[Dict]:
    """获取用户收藏列表"""
    return get_favorites(user_id)