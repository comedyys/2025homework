# pylint: disable=missing-module-docstring
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent


def fetch_douban_top250():
    # 随机User-Agent生成器
    ua = UserAgent()

    # 基础URL和备用Referer列表
    base_url = "https://movie.douban.com/top250"
    referers = [
        "https://www.douban.com/",
        "https://movie.douban.com/",
        "https://www.google.com/",
        "https://www.bing.com/"
    ]

    movies = []
    session = requests.Session()

    for page in range(10):  # 抓取全部10页
        url = f"{base_url}?start={page * 25}"
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                # 动态生成请求头
                headers = {
                    "User-Agent": ua.random,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Connection": "keep-alive",
                    "Referer": random.choice(referers),
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1"
                }

                print(f"\n📺 正在抓取第 {page + 1}/10 页 | 尝试 #{retry_count + 1}")
                print(f"   User-Agent: {headers['User-Agent'][:60]}...")

                # 随机延迟 + 抖动
                delay = random.uniform(2.5, 6.0)
                time.sleep(delay)

                response = session.get(url, headers=headers, timeout=15)
                response.encoding = 'utf-8'

                # 检查验证码页面
                if "检测到有异常请求" in response.text:
                    print("❌ 触发豆瓣反爬验证码，请更换IP或稍后再试")
                    return movies

                if response.status_code != 200:
                    print(f"⚠️ 状态码异常: {response.status_code} | 等待重试...")
                    retry_count += 1
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='item')

                if not items:
                    print("⚠️ 页面解析失败: 未找到电影条目")
                    retry_count += 1
                    continue

                print(f"✅ 发现 {len(items)} 部电影")

                # 解析电影数据
                for idx, item in enumerate(items, 1):
                    try:
                        # 标题处理（中文+英文）
                        titles = [
                            t.text.strip() for t in item.find_all(
                                'span', class_='title')]
                        chinese_title = titles[0] if titles else "未知标题"
                        english_title = titles[1].replace(
                            "\xa0", " ") if len(titles) > 1 else ""
                        full_title = f"{chinese_title} {english_title}".strip()

                        # 导演和年份
                        info = item.find(
                            'div', class_='bd').p.get_text(
                            strip=True)
                        director = info.split('\n')[0].strip()
                        year = info.split('\n')[1].strip().split(
                            '/')[0].strip()

                        # 评分和引用
                        rating = item.find(
                            'span', class_='rating_num').text.strip()
                        quote_elem = item.find('span', class_='inq')
                        quote = quote_elem.text.strip() if quote_elem else "暂无引用"
                        link = item.find('a')['href']

                        movies.append({
                            'title': full_title,
                            'director': director,
                            'year': year,
                            'rating': rating,
                            'quote': quote,
                            'link': link
                        })

                        print(f"   #{idx} {full_title[:20]}... | 评分: {rating}")

                    except Exception as e:
                        print(f"   🚫 条目解析失败: {str(e)}")
                        continue

                break  # 成功抓取，跳出重试循环

            except requests.exceptions.RequestException as e:
                print(f"🌐 网络请求异常: {str(e)} | 等待重试...")
                retry_count += 1
                time.sleep(5)

            except Exception as e:
                print(f"❌ 未知错误: {str(e)}")
                retry_count += 1
                time.sleep(3)

        else:
            print(f"⛔ 第 {page + 1} 页抓取失败，已达最大重试次数")

    return movies


def save_to_html(movies, filename="douban_top250.html"):
    # 创建HTML文档结构
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>豆瓣电影Top250</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            body {
                background-color: #f5f5f5;
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                padding: 30px;
            }
            header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eaeaea;
            }
            h1 {
                color: #007722;
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            .stats {
                font-size: 1.1rem;
                color: #666;
            }
            .movie-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 25px;
            }
            .movie-card {
                background: #fff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .movie-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .movie-header {
                padding: 15px;
                background: #f8f8f8;
                border-bottom: 1px solid #eee;
            }
            .movie-title {
                font-size: 1.3rem;
                font-weight: bold;
                margin-bottom: 5px;
                color: #007722;
            }
            .movie-title a {
                color: inherit;
                text-decoration: none;
            }
            .movie-title a:hover {
                text-decoration: underline;
            }
            .movie-director, .movie-year {
                font-size: 0.9rem;
                color: #666;
            }
            .movie-body {
                padding: 15px;
            }
            .movie-rating {
                font-size: 1.5rem;
                color: #ffac2d;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .movie-quote {
                font-style: italic;
                color: #555;
                padding: 10px;
                background: #f9f9f9;
                border-left: 3px solid #ffac2d;
                border-radius: 0 4px 4px 0;
            }
            footer {
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                color: #888;
                font-size: 0.9rem;
                border-top: 1px solid #eee;
            }
            @media (max-width: 768px) {
                .movie-grid {
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>豆瓣电影Top250</h1>
                <div class="stats">共收录 <strong>""" + str(len(movies)) + """</strong> 部经典电影</div>
            </header>

            <div class="movie-grid">
    """

    # 添加电影卡片
    for i, movie in enumerate(movies, 1):
        html_content += f"""
                <div class="movie-card">
                    <div class="movie-header">
                        <div class="movie-title">
                            <span class="rank">#{i}</span>
                            <a href="{movie['link']}" target="_blank">{movie['title']}</a>
                        </div>
                        <div class="movie-director">{movie['director']}</div>
                        <div class="movie-year">年份: {movie['year']}</div>
                    </div>
                    <div class="movie-body">
                        <div class="movie-rating">评分: {movie['rating']}</div>
                        <div class="movie-quote">"{movie['quote']}"</div>
                    </div>
                </div>
        """

    # 添加页脚
    html_content += """
            </div>

            <footer>
                <p>数据来源: 豆瓣电影 | 抓取时间: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
                <p>仅用于学习目的，请勿用于商业用途</p>
            </footer>
        </div>
    </body>
    </html>
    """

    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n💾 HTML文件已保存至 {filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("🎬 豆瓣电影Top250抓取程序启动")
    print("=" * 60)

    start_time = time.time()
    movies = fetch_douban_top250()
    elapsed = time.time() - start_time

    if movies:
        print("\n" + "=" * 60)
        print(f"✅ 抓取完成! 耗时: {elapsed:.1f}秒 | 共获取 {len(movies)} 部电影")
        print("=" * 60)

        # 保存为HTML
        save_to_html(movies)

        # 显示摘要
        print("\n🏆 Top 5 电影:")
        for i, m in enumerate(movies[:5], 1):
            print(f"{i}. {m['title']} ({m['rating']})")

        print(f"\n⭐ 最低分电影: {min(movies, key=lambda x: float(x['rating']))[
              'title']} ({min(movies, key=lambda x: float(x['rating']))['rating']})")
        print(f"💾 结果已保存为 douban_top250.html")
    else:
        print("\n⚠️ 未获取到有效数据，请检查网络或反爬设置")
