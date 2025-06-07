import csv
import re
from peewee import Model, CharField, FloatField, IntegerField, SqliteDatabase

# 数据库连接
db = SqliteDatabase("movie.db")

# 表结构实体
class Movie(Model):
    title = CharField(max_length=50)
    rating_num = FloatField()
    comment_num = IntegerField()
    year = IntegerField()
    link = CharField(max_length=100)
    image_link = CharField(max_length=100)

    class Meta:
        database = db
        table_name = 'douban_movie'

# 保存数据的函数
def save_data(csv_file_path):
    # 连接数据库
    db.connect()

    # 删除现有表（注意：这会清空表中数据！）
    db.drop_tables([Movie], safe=True)
    # 创建新表
    db.create_tables([Movie], safe=True)

    movies = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # 打印列名以调试
        print("CSV 列名:", reader.fieldnames)

        for row in reader:
            try:
                # 清洗评论数
                comment_num = row['评论数'].strip()
                comment_num = int(re.sub(r'[^0-9]', '', comment_num)) if comment_num else 0

                # 创建电影记录
                movies.append({
                    'title': row['\ufeff标题'].strip()[:50] if row['\ufeff标题'] else "未知标题",
                    'rating_num': float(row['评分']) if row['评分'] else 0.0,
                    'comment_num': comment_num,
                    'year': int(row['年份']) if row['年份'] else 0,
                    'link': row['链接'].strip()[:100] if row['链接'] else "",
                    'image_link': row['图片链接'].strip()[:100] if row['图片链接'] else ""
                })
            except (ValueError, KeyError) as e:
                print(f"跳过无效行: {row}, 错误: {e}")
                continue
    
    # 批量插入
    if movies:
        with db.atomic():
            Movie.insert_many(movies).execute()
        print(f"成功插入 {len(movies)} 条记录")
    else:
        print("没有数据插入，可能 CSV 文件为空或格式错误")
    
    db.close()

# 示例调用
if __name__ == "__main__":
    csv_file_path = "E:\\Microsoft VS Code Project\\douban_movies.csv"
    save_data(csv_file_path)