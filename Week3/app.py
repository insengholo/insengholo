from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)


def DB_connection():
    return pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = '9513',
        database = 'bulletin_board',
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )


@app.route('/')
def index():
    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')
            posts = cursor.fetchall()
        return render_template('3_index.html', posts = posts)
    finally:
        connection.close()


@app.route('/add', methods = ['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO posts (title, content) VALUES (%s, %s)'
            cursor.execute(sql, (title, content))
            connection.commit()
        return redirect('/')
    finally:
        connection.close()


@app.route('/edit/<int:id>')
def edit_post(id):
    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
            post = cursor.fetchone()
        return render_template('3_edit.html', post = post)
    finally:
        connection.close()


@app.route('/update/<int:id>', methods = ['POST'])
def update_post(id):
    title = request.form['title']
    content = request.form['content']
    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'UPDATE posts SET title = %s, content = %s WHERE id = %s'
            cursor.execute(sql, (title, content, id))
            connection.commit()
        return redirect('/')
    finally:
        connection.close()


@app.route('/delete/<int:id>')
def delete_post(id):
    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
            connection.commit()
        return redirect('/')
    finally:
        connection.close()


@app.route('/search', methods = ['GET'])
def search_posts():
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'all')

    connection = DB_connection()
    try:
        with connection.cursor() as cursor:
            if search_type == 'title':
                sql = 'SELECT * FROM posts WHERE title LIKE %s ORDER BY created_at DESC'
                cursor.execute(sql, ('%' + query + '%',))
            elif search_type == 'content':
                sql = 'SELECT * FROM posts WHERE content LIKE %s ORDER BY created_at DESC'
                cursor.execute(sql, ('%' + query + '%',))
            else:
                sql = 'SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s ORDER BY created_at DESC'
                cursor.execute(sql, ('%' + query + '%', '%' + query + '%'))

            posts = cursor.fetchall()
        return render_template('3_index.html', posts = posts)
    finally:
        connection.close()


@app.route('/')
def design():
    return render_template('insengholo.html')

if __name__ == '__main__':
    app.run(debug = True)
