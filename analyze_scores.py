import matplotlib.pyplot as plt
import pymysql
import pandas as pd
from getpass import getpass

# 输入数据库登录信息
user = input("请输入 MySQL 用户名：")
password = getpass("请输入 MySQL 密码：")

connection = None

try:
    # 连接数据库
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user=user,
        password=password,
        database="student_analysis",
        charset="utf8mb4"
    )

    # 查询学生、课程和成绩
    sql = """
    SELECT
        s.student_name,
        c.course_name,
        e.score
    FROM students s
    JOIN enrollments e
        ON s.student_id = e.student_id
    JOIN courses c
        ON e.course_id = c.course_id
    ORDER BY s.student_id;
    """

    # 使用 Pandas 读取数据
    df = pd.read_sql(sql, connection)

    print("\n学生成绩数据：")
    print(df)

    print("\n各科平均成绩：")
    print(df.groupby("course_name")["score"].mean())

    # 计算各科平均成绩
    course_avg = df.groupby("course_name")["score"].mean()

    # 设置中文字体
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False

    # 绘制柱状图
    course_avg.sort_values(ascending=False).plot(
        kind="bar",
     figsize=(9, 5))

    plt.title("各课程平均成绩分析")
    plt.xlabel("课程名称")
    plt.ylabel("平均成绩")
    plt.xticks(rotation=30)
    plt.tight_layout()

    # 保存图片
    import os
    os.makedirs("output", exist_ok=True)

    plt.savefig("output/course_average.png", dpi=150)
    plt.show()

except pymysql.MySQLError as error:
    print("数据库连接失败：", error)

finally:
    if connection is not None:
        connection.close()
        print("\n数据库连接已关闭。")