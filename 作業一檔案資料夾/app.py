from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 資料庫配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # 修改為您的 MySQL 使用者名稱
app.config['MYSQL_PASSWORD'] = '31415926'  # 修改為您的 MySQL 密碼
app.config['MYSQL_DB'] = 'studentdb'

mysql = MySQL(app)

# 首頁路由，用來顯示輸入表單
@app.route('/')
def index():
    return render_template('index.html')

# 表單提交處理
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        grade = request.form['grade']
        
        # 插入資料進 MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (student_id, name, grade) VALUES (%s, %s, %s)", (student_id, name, grade))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
