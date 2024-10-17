from flask import Flask, render_template, request, redirect
import mysql.connector
from join import join_bp  # 引入 join.py 的 Blueprint

app = Flask(__name__)

# MySQL 資料庫配置
db_config = {
    'host': 'localhost',
    'user': 'root',  # 修改為您的 MySQL 使用者名稱
    'password': '31415926',  # 修改為您的 MySQL 密碼
    'database': 'flask_app_db'
}

# 註冊 join Blueprint
app.register_blueprint(join_bp)

@app.route('/', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post_content = request.form['content']
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        
        # 插入新貼文到 MySQL 資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (content, user_id, category_id) VALUES (%s, %s, %s)", 
                       (post_content, user_id, category_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    # 獲取所有貼文以顯示在主頁
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('template.html', posts=posts)

@app.route('/edit/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查詢要編輯的貼文
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return render_template('edit.html', post=post)

@app.route('/update/<int:post_id>', methods=['POST'])
def update_post(post_id):
    if request.method == 'POST':
        post_content = request.form['content']
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        
        # 更新貼文到 MySQL 資料庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET content = %s, user_id = %s, category_id = %s WHERE id = %s", 
                       (post_content, user_id, category_id, post_id))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    # 如果請求不是 POST，則返回編輯表單
    return redirect(f'/edit/{post_id}')

if __name__ == '__main__':
    app.run(debug=True)
