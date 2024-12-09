
from flask import Flask, request, render_template, abort
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
conn = sqlite3.connect('../bot/database.db', check_same_thread=False)
cursor = conn.cursor()


@app.route('/webapp/<username>')
def webapp(username):
    user_id = request.args.get('id', type=int)

    # Проверяем, совпадает ли username с ID
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if not result or result[0] != user_id:
        return "Это не ваша ссылка.", 403

    return render_template('index.html', username=username, user_id=user_id)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()

    # Поиск файлов по ключевым словам
    cursor.execute('''
    SELECT file_path, keywords FROM files WHERE LOWER(keywords) LIKE ?
    ''', (f'%{query}%',))
    results = cursor.fetchall()

    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
