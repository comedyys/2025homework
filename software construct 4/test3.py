from flask import Flask, render_template, request, send_file, url_for
import csv
import chardet
import re
import requests
from io import BytesIO

app = Flask(__name__)

def load_movies_from_csv(filename='douban_movies.csv'):
    try:
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result.get('encoding') if result else None
        if not encoding:
            raise ValueError("无法检测到文件编码")
        
        movies = []
        with open(filename, mode='r', encoding=encoding) as file:
            first_line = file.readline()
            file.seek(0)
            if first_line.startswith('\ufeff'):
                reader = csv.DictReader(file, fieldnames=['标题', '评分', '评论数', '年份', '链接', '图片链接'])
                next(reader)
            else:
                file.seek(0)
                reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    comment_num = int(re.sub(r'[^\d]', '', row['评论数']))
                    movies.append({
                        'title': row['标题'].strip(),
                        'rating': float(row['评分']),
                        'comments': comment_num,
                        'year': int(row['年份']),
                        'url': row['链接'].strip(),
                        'image_url': row['图片链接'].strip()
                    })
                except (ValueError, KeyError) as e:
                    print(f"解析失败的行: {row}，错误: {e}")
                    continue
        
        print(f"成功加载电影数量: {len(movies)}")
        return movies
    except Exception as e:
        print(f"加载CSV文件失败: {e}")
        raise

def filter_movies_by_year(movies, year):
    return [movie for movie in movies if movie['year'] == year]

@app.route('/proxy-image/<path:image_url>')
def proxy_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        return send_file(BytesIO(response.content), mimetype=response.headers['Content-Type'])
    except Exception as e:
        print(f"代理图片失败: {e}")
        return send_file('static/no-image.jpg', mimetype='image/jpeg')

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        movies = load_movies_from_csv()
    except Exception as e:
        return render_template('error.html', error=f"无法加载电影数据: {str(e)}")
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    total = len(movies)
    start = (page - 1) * per_page
    end = start + per_page
    
    filtered_movies = []
    year_filter = None
    
    if request.method == 'POST':
        year_str = request.form.get('year')
        if year_str:
            try:
                year_filter = int(year_str)
                filtered_movies = filter_movies_by_year(movies, year_filter)
            except ValueError:
                error = "请输入有效的年份(如: 2020)"
                return render_template('index.html', error=error, movies=movies[start:end], 
                                     year_filter=year_filter, total_movies=total, 
                                     filtered_count=len(movies[start:end]), page=page,
                                     pages=(total + per_page - 1) // per_page)
    
    if not filtered_movies and year_filter is None:
        filtered_movies = movies
    
    paginated_movies = filtered_movies[start:end]
    
    return render_template('index.html', 
                         movies=paginated_movies, 
                         year_filter=year_filter,
                         total_movies=total,
                         filtered_count=len(filtered_movies),
                         page=page,
                         pages=(len(filtered_movies) + per_page - 1) // per_page)

if __name__ == '__main__':
    app.run(debug=True)