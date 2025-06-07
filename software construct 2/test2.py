import csv
from bs4 import BeautifulSoup

def extract_from_html(html_file="douban_top250.html"):
    """从 HTML 文件中提取电影信息"""
    try:
        # 读取 HTML 文件
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        movie_divs = soup.find_all('div', class_='movie')
        
        movies = []
        for movie_div in movie_divs:
            # 提取标题
            title_elem = movie_div.find('div', class_='title')
            title = title_elem.text.strip() if title_elem else "N/A"
            # 移除编号（如 "1. "）
            title = title.split('. ', 1)[1] if '. ' in title else title
            
            # 提取评分和评论人数
            rating_elem = movie_div.find('div', class_='rating')
            rating = "N/A"
            votes = "N/A"
            if rating_elem:
                rating_text = rating_elem.text.strip()
                # 解析 "评分: 9.7 (2881234人评价)"
                if '评分: ' in rating_text:
                    parts = rating_text.split(' (')
                    rating = parts[0].replace('评分: ', '').strip()
                    votes = parts[1].replace('人评价)', '').strip() if len(parts) > 1 else "N/A"
            
            # 提取导演、主演、上映时间、国家/地区、类型
            details_elems = movie_div.find_all('div', class_='details')
            director = "N/A"
            actors = "N/A"
            release_date = "N/A"
            country = "N/A"
            genres = ["N/A"]
            for detail in details_elems:
                text = detail.text.strip()
                if text.startswith('导演: '):
                    director = text.replace('导演: ', '').strip()
                elif text.startswith('主演: '):
                    actors = text.replace('主演: ', '').strip()
                elif text.startswith('上映时间: '):
                    release_date = text.replace('上映时间: ', '').strip()
                elif text.startswith('国家/地区: '):
                    country = text.replace('国家/地区: ', '').strip()
                elif text.startswith('类型: '):
                    genres = text.replace('类型: ', '').strip().split(', ')
            
            # 提取标题图链接
            img_elem = movie_div.find('img')
            img_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else "N/A"
            
            movies.append({
                'title': title,
                'rating': rating,
                'votes': votes,
                'director': director,
                'actors': actors,
                'release_date': release_date,
                'country': country,
                'genres': genres,
                'img_url': img_url
            })
        
        return movies
    except Exception as e:
        print(f"解析 HTML 文件时出错: {e}")
        return []

def save_to_csv(movies, filename="douban_top250.csv"):
    """将电影信息保存为 CSV 文件"""
    headers = ['title', 'rating', 'votes', 'director', 'actors', 'release_date', 'country', 'genres', 'img_url']
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for movie in movies:
            # 将 genres 列表转换为字符串
            movie_copy = movie.copy()
            movie_copy['genres'] = ', '.join(movie['genres'])
            writer.writerow(movie_copy)
    
    print(f"已保存 {len(movies)} 部电影到 {filename}")

if __name__ == "__main__":
    movies = extract_from_html()
    if movies:
        save_to_csv(movies)