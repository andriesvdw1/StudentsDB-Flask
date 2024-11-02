from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'students.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the database table if it doesn't exist
def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                student_number TEXT NOT NULL UNIQUE
            )
        ''')

@app.route('/')
def index():
    with get_db() as conn:
        students = conn.execute('SELECT * FROM students').fetchall()
    return render_template('index.html', students=students)

@app.route('/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        student_number = request.form['student_number']
        with get_db() as conn:
            conn.execute('INSERT INTO students (first_name, last_name, student_number) VALUES (?, ?, ?)',
                         (first_name, last_name, student_number))
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    with get_db() as conn:
        student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        student_number = request.form['student_number']
        with get_db() as conn:
            conn.execute('UPDATE students SET first_name = ?, last_name = ?, student_number = ? WHERE id = ?',
                         (first_name, last_name, student_number, id))
        return redirect(url_for('index'))
    return render_template('update.html', student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    with get_db() as conn:
        conn.execute('DELETE FROM students WHERE id = ?', (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)