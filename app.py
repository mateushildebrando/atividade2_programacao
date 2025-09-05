from flask import Flask, render_template, request, redirect, url_for, session, flash
from werqzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "gremio"

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'pg2'
}

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute ("SELECT * FROM usuario WHERE username_usuario = %s OR email usuario OR email_usuario = %s", (username, email))
if cursor.fetchone():
    flash("Nome de usuário ou email já cadastrado.", "erro")
    return redirect(url_for('cadastro'))