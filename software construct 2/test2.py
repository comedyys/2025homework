import os
from bs4 import BeautifulSoup
import bs4
dest_dir = "d:/data/movie/"
for html_file in os.listdir(dest_dir):
    print(html_file.title())
    with open(dest_dir+html_file,"r",encoding="utf-8") as f:
        html = f.read()
        print(html)
        # 抽取文件内容
        soup = BeautifulSoup(html, 'lxml')
        grid_view = soup.find('ol', class_='grid_view')
        if grid_view and isinstance(grid_view, bs4.element.Tag) and hasattr(grid_view, 'find_all'):
            movie_list = grid_view.find_all('li')
        else:
            movie_list = []
        for movie in movie_list:
            title = movie.find('div', class_='hd').find('span', class_='title').get_text()
            rating_num = movie.find('div', class_='bd').find('div').find('span', class_='rating_num').get_text()
            comment_num = movie.find('div', class_='bd').find('div').find_all('span')[-1].get_text()
            directors = movie.find('div', class_='bd').find('p').get_text()
            link = movie.find('div',class_='item').find('div',class_='pic').find('a').get('href')
            pic = movie.find('div',class_='item').find('div',class_='pic').find('a').find('img').get('src')
            print(title, rating_num, comment_num,directors,link,pic)