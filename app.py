# Seção 1: Importações
# ---------------------
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# Seção 2: Configuração Inicial
# ------------------------------
app = Flask(__name__)
app.secret_key = '17f5fe9813722ae4f396dc93f56b3125c7797b18e2af49a5c912de405956a009'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pg2'
}

# Seção 3: Rotas da Aplicação
# ---------------------------

# Rota de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario WHERE username_usuario = %s OR email_usuario = %s", (username, email))
        if cursor.fetchone():
            flash("Nome de usuário ou email já cadastrado.", "erro")
            return redirect(url_for('cadastro'))

        cursor.execute("""INSERT INTO usuario (nome_usuario, username_usuario, password_usuario, email_usuario, conta_ativa)
                          VALUES (%s, %s, %s, %s, %s)""", (nome, username, senha, email, True))
        
        conn.commit()
        cursor.close()
        conn.close()

        flash("Cadastro realizado com sucesso! Você já pode fazer login.", "sucesso")
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        senha = request.form['senha'].strip()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE username_usuario = "
        "%s", (username,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario and check_password_hash(usuario['password_usuario'], senha):
            if not usuario['conta_ativa']:
                flash("Esta conta está desativada.", "erro")
                return redirect(url_for('login'))
            
            session['usuario_id'] = usuario['cod_usuario']
            session['usuario_nome'] = usuario['nome_usuario']
            return redirect(url_for('dashboard'))
        else:
            flash("Usuário ou senha inválidos.", "erro")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página", "erro")
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/verificar_usuario_email', methods=['POST'])
def verificar_usuario_email():
    username = request.form['username']
    email = request.form['email']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE username_usuario = %s OR email_usuario = %s," (username, email))
    existe = cursor.fetchone()
    cursor.close()
    conn.close()
    return 'existe' if existe else 'disponivel'
