from flask import Blueprint, render_template
import mysql.connector

# 定義 Blueprint
join_bp = Blueprint('join', __name__)

# MySQL 資料庫配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '31415926',
    'database': 'flask_app_db'
}

# 定義路由和函數
@join_bp.route('/join')
def show_joined_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT posts.content AS post_content, users.name AS user_name, categories.name AS category_name
    FROM posts
    JOIN users ON posts.user_id = users.id
    JOIN categories ON posts.category_id = categories.id
    """
    cursor.execute(query)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('join.html', results=result)
