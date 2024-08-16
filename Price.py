import mysql.connector
import requests

# 连接到MySQL数据库
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="dbtable"
)

# 创建一个光标对象
cursor = connection.cursor()

# 执行查询语句，获取所有img_url字段的值
cursor.execute("SELECT img_url FROM phone")

# 获取所有img_url字段的值
img_urls = cursor.fetchall()

# 遍历img_urls并爬取数据
for img_url in img_urls:
    try:
        # 发送HTTP请求获取图片URL的内容
        response = requests.get(img_url)
        if response.status_code == 200:
            # 处理图片数据，例如保存到本地或进行其他操作
            print(f"成功获取图片：{img_url}")
        else:
            print(f"无法访问图片：{img_url}")
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")

    # 关闭光标和连接
cursor.close()
connection.close()