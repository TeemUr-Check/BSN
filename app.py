from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Создаем базу данных SQLite
conn = sqlite3.connect('images.db')
c = conn.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, image_url TEXT, nickname, description TEXT)''')
conn.commit()

db_lp = sqlite3.connect('login_password.db')
cursor_db = db_lp.cursor()

db_lp.commit()

cursor_db.close()
db_lp.close()


# главная страница
@app.route('/')
def home():
    return render_template('before.html')


# рассыльник
@app.route('/main')
def main():
    return render_template('index.html')


# О нас
@app.route('/about')
def about():
    return render_template('about.html')


# помощник
@app.route('/AI')
def index():
    return render_template('Index2.0.html')


# страница найти книгу

@app.route('/gallery')
def gallery():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    images = c.fetchall()

    return render_template('gallery.html', images=images)


# страница поделиться с другими книгой
@app.route('/share')
def share():
    return render_template('add_article.html')


@app.route('/upload', methods=['POST'])
def upload():
    image_url = request.form['image_url']
    nickname = request.form['nickname']
    description = request.form['description']

    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute("INSERT INTO images (image_url, nickname, description) VALUES (?, ?, ?)",
                 (image_url, nickname, description))
    conn.commit()

    return redirect(url_for('index'))


# Авторизация
@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute(('''SELECT password FROM passwords
                                               WHERE login = '{}';
                                               ''').format(Login))
        pas = cursor_db.fetchall()

        cursor_db.close()
        try:
            if pas[0][0] != Password:
                return render_template('auth_bad.html')
        except:
            return render_template('auth_bad.html')

        db_lp.close()
        return render_template('successfulauth.html')

    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)

        cursor_db.execute(sql_insert)

        cursor_db.close()

        db_lp.commit()
        db_lp.close()

        return render_template('successfulregis.html')

    return render_template('registration.html')


# Функция для выполнения поиска в базе данных
def search_position(search_term):
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM images WHERE description LIKE ?", ('%' + search_term + '%',))
    position = cursor.fetchone()
    conn.close()
    return position[0] if position else "Не найдено"


# Обработчик для страницы запросов
@app.route('/explorer')
def searching_page():
    return render_template('prob.html')


# Обработчик для запросов из формы поиска
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search']
    position = search_position(search_term)
    return render_template('prob.html', position=position)


if __name__ == '__main__':
    app.run(debug=True)  # ошибки показываются на странице
