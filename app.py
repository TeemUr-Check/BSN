from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import base64

app = Flask(__name__)


# Фильтр для base64 кодирования
@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  image_url TEXT,
                  nickname TEXT,
                  description TEXT,
                  image_data BLOB)''')  # Добавляем BLOB поле
    conn.commit()
    conn.close()


init_db()  # Создаем таблицу при старте


# Главная страница
@app.route('/')
def home():
    return render_template('before.html')


# Рассыльник
@app.route('/main')
def main():
    return render_template('index.html')


# О нас
@app.route('/about')
def about():
    return render_template('about.html')


# Галерея книг
@app.route('/gallery')
def gallery():
    conn = sqlite3.connect('images.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM images ORDER BY id DESC")
    images = c.fetchall()
    conn.close()
    return render_template('gallery.html', images=images)


# Страница добавления книги
@app.route('/share')
def share():
    return render_template('add_article.html')


# Обработчик загрузки
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            # Получаем данные формы
            nickname = request.form['nickname']
            description = request.form['description']
            image_file = request.files['image']

            # Читаем изображение
            image_data = image_file.read()

            # Сохраняем в БД
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute('''INSERT INTO images 
                        (nickname, description, image_data) 
                        VALUES (?, ?, ?)''',
                      (nickname, description, image_data))
            conn.commit()
            conn.close()

            return redirect(url_for('gallery'))
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return redirect(url_for('share'))


# Авторизация (без изменений)
@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        cursor_db.execute('''SELECT password FROM passwords WHERE login = ?''', (Login,))
        pas = cursor_db.fetchone()
        cursor_db.close()

        if not pas or pas[0] != Password:
            return render_template('auth_bad.html')

        return render_template('successfulauth.html')
    return render_template('authorization.html')


# Регистрация (без изменений)
@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_lp = sqlite3.connect('login_password.db')
        cursor_db = db_lp.cursor()
        try:
            cursor_db.execute('''INSERT INTO passwords VALUES(?,?)''', (Login, Password))
            db_lp.commit()
            return render_template('successfulregis.html')
        except sqlite3.IntegrityError:
            return "Пользователь уже существует"
        finally:
            cursor_db.close()
            db_lp.close()
    return render_template('registration.html')


# Поиск (без изменений)
@app.route('/explorer')
def searching_page():
    return render_template('prob.html')


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search']
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM images WHERE description LIKE ?",
                   ('%' + search_term + '%',))
    position = cursor.fetchone()
    conn.close()
    return render_template('prob.html', position=position[0] if position else "Не найдено")


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
