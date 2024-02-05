from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3

app = Flask(__name__)

filePath = 'templates/Limerick.txt'

# SQLite database setup
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  password TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT)''')
    conn.commit()
    conn.close()
    
create_table()


# Registration route
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        # Store user details in the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                  (username, password, first_name, last_name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    return render_template('register.html')


# Success route
@app.route('/success')
def success():
    # Retrieve user information from the last registration
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    user_info = c.fetchone()
    conn.close()

    if user_info:
        with open(filePath, 'r') as file:
            content = file.read()
        word_count = len(content.split())
        return render_template('success.html', user=user_info, word_count=word_count)
    else:
        return 'No user information found.'
    
@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user_info = c.fetchone()
        conn.close()
        if user_info:
            return render_template('user_info.html', user=user_info, filePath = filePath)
        else:
            return 'No user found with the provided credentials.'
    return render_template('retrieve.html')

@app.route('/download')
def download():
    return send_file(filePath, as_attachment=True)




if __name__ == '__main__':
    app.run(debug=True)


# [Unit]
# Description=Gunicorn daemon to serve my flaskapp
# After=network.target
# [Service]
# User=ubuntu
# Group=www-data
# WorkingDirectory=/home/ubuntu/Login_page
# ExecStart=/home/ubuntu/Login_Page/venv/bin/gunicorn --bind unix:flaskapp.sock app:app
# [Install]
# WantedBy=multi-user.target