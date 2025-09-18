from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "gremio"

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'pg2'
}

@app.route('/cadastro', methods=['GET', 'PHOST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        conn = mysql.connector(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario   WHERE username_usuario = %s OR email_usuario = %s", (username, email))
        if cursor.fetchone():
            flash("Nome de usuario ou email já cadastrado.", "erro")
            return redirect(url_for('cadastro'))

        cursor.execute (""" INSERT INTO usuario (nome_usuario, username_usuario, password_usuario, email_usuario, conta_ativa) 
                        VALUES (%s, %s, %s, %s, %s)""", (nome, username, senha, email, True)
                        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Cadastro realizado com sucesso! Você já pode fazer login.",  "Sucesso" )
        return redirect(url_for('login'))


    return render_template('cadastro.html')

@app.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        username = request.form['username'].strip()
        senha = request.form["senha"].strip()


        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute ("SELECT * FROM usuario WHERE username_usuario = "
        "%s", (username,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()


        if usuario and check_password_hash(usuario['password_usuario'], senha ):
            if not usuario['conta_livre']:
                flash("Esta conta está desativada.", "Erro")
                return redirect(url_for('login'))