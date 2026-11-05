import pymysql
from getpass import getpass

# 输入 MySQL 登录信息
user = input("请输入 MySQL 用户名：")
password = getpass("请输入 MySQL 密码：")

connection = None

try:
    # 连接本地 MySQL 数据库
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user=user,
        password=password,
        database="student_analysis",
        charset="utf8mb4"
    )

    print("✅ MySQL 连接成功！")

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("\n数据库中的数据表：")
        for table in tables:
            print(table[0])

except pymysql.MySQLError as error:
    print("❌ 数据库连接失败：", error)

finally:
    if connection is not None:
        connection.close()
        print("\n数据库连接已关闭。")