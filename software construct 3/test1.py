# pylint: disable=missing-module-docstring

import csv
import re
from peewee import Model, CharField, FloatField, IntegerField, SqliteDatabase

# 数据库连接
DB = SqliteDatabase("movie.db")  # 常量改为大写


class Movie(Model):
    """豆瓣电影数据模型
    
    属性:
        title (CharField): 电影标题(最大50字符)
        rating_num (FloatField): 评分
        comment_num (IntegerField): 评论数
        year (IntegerField): 上映年份
        link (CharField): 详情页链接(最大100字符)
        image_link (CharField): 图片链接(最大100字符)
    """
    title = CharField(max_length=50)
    rating_num = FloatField()
    comment_num = IntegerField()
    year = IntegerField()
    link = CharField(max_length=100)
    image_link = CharField(max_length=100)

    class Meta:
        """元数据配置"""
        database = DB
        table_name = 'douban_movie'


def save_data(csv_file_path):
    """将CSV电影数据保存到数据库
    
    参数:
        csv_file_path (str): CSV文件路径
        
    处理流程:
        1. 连接数据库
        2. 重建数据表
        3. 读取并清洗CSV数据
        4. 批量插入数据库
    """
    # 连接数据库
    DB.connect()

    # 删除现有表（注意：这会清空表中数据！）
    DB.drop_tables([Movie], safe=True)
    # 创建新表
    DB.create_tables([Movie], safe=True)

    movies = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # 打印列名以调试
        print("CSV 列名:", reader.fieldnames)

        for row in reader:
            try:
                # 清洗评论数
                comment_num = row['评论数'].strip()
                comment_num = int(
                    re.sub(
                        r'[^0-9]',
                        '',
                        comment_num)) if comment_num else 0

                # 创建电影记录
                movies.append({
                    'title': row['\ufeff标题'].strip()[:50] if row['\ufeff标题'] else "未知标题",
                    'rating_num': float(row['评分']) if row['评分'] else 0.0,
                    'comment_num': comment_num,
                    'year': int(row['年份']) if row['年份'] else 0,
                    'link': row['链接'].strip()[:100] if row['链接'] else "",
                    'image_link': row['图片链接'].strip()[:100] if row['图片链接'] else ""
                })
            except (ValueError, KeyError) as error:
                print(f"跳过无效行: {row}, 错误: {error}")
                continue

    # 批量插入
    if movies:
        with DB.atomic():
            Movie.insert_many(movies).execute()
        print(f"成功插入 {len(movies)} 条记录")
    else:
        print("没有数据插入，可能 CSV 文件为空或格式错误")

    DB.close()


# 示例调用
if __name__ == "__main__":
    CSV_FILE_PATH = "E:\\Microsoft VS Code Project\\douban_movies.csv"  # 常量改为大写
    save_data(CSV_FILE_PATH)