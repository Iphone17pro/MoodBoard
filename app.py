from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib

app = Flask(__name__, static_folder='static')
app.secret_key = 'mysecretkey'  # Secreto para usar flash messages

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('users.db')  # Base de datos de usuarios
    conn.row_factory = sqlite3.Row  # Para que los resultados sean accesibles como diccionarios
    return conn

# Crear la tabla de usuarios si no existe
def create_user_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Crear la tabla de correos si no existe
def create_email_table():
    conn = sqlite3.connect('emails.db')  # Base de datos de correos
    conn.execute('''CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

create_user_table()  # Crear la tabla de usuarios al iniciar la aplicación
create_email_table()  # Crear la tabla de correos al iniciar la aplicación

# Página principal con formulario
@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', usuario=session['user'])  # Pasamos el nombre del usuario
    return redirect(url_for('login'))  # Redirigir si no está autenticado


# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Consultar si el usuario existe en la base de datos
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE correo = ?', (email,)).fetchone()
        conn.close()
        
        if user and hashlib.sha256(password.encode()).hexdigest() == user['contrasena']:
            # Usuario autenticado correctamente
            session['user'] = user['nombre']  # Guardamos el nombre del usuario en la sesión
            return redirect(url_for('index'))  # Redirige a la página principal
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        # Validar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('register'))

        # Comprobar si el correo electrónico ya está registrado
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE correo = ?', (correo,)).fetchone()
        
        if user:
            flash('Este correo electrónico ya está registrado.', 'error')
            conn.close()
            return redirect(url_for('register'))

        # Hash de la contraseña antes de almacenarla
        hashed_password = hashlib.sha256(contrasena.encode()).hexdigest()

        # Guardar el nuevo usuario en la base de datos
        conn.execute('INSERT INTO users (nombre, correo, contrasena) VALUES (?, ?, ?)', 
                     (nombre, correo, hashed_password))
        conn.commit()
        conn.close()

        flash('Te has registrado con éxito. Puedes iniciar sesión ahora.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Otras páginas
@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/puntillismo')
def puntillismo():
    return render_template('puntillismo.html')

@app.route('/manchas')
def manchas():
    return render_template('manchas.html')

@app.route('/pixelart')
def pixelart():
    return render_template('pixelart.html')

@app.route('/geometrico')
def geometrico():
    return render_template('geometrico.html')

@app.route('/graffiti')
def graffiti():
    return render_template('graffiti.html')

@app.route('/texturas')
def texturas():
    return render_template('texturas.html')

# Página de comunicados
@app.route('/comunicados')
def comunicados():
    success = request.args.get('success') == 'true'
    message = "¡Te has suscrito correctamente!" if success else None
    return render_template('comunicados.html', message=message)

# Ruta para guardar el correo electrónico
@app.route('/guardar_correo', methods=['POST'])
def guardar_correo():
    correo = request.form['email']
    
    # Guardar el correo en la base de datos SQLite
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emails (email) VALUES (?)", (correo,))
    conn.commit()
    conn.close()

    # Redirigir a la página de comunicados con un parámetro de éxito en la URL
    return redirect(url_for('comunicados') + "?success=true")

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)  # Elimina al usuario de la sesión
    return redirect(url_for('login'))  # Redirige a la página de login

if __name__ == '__main__':
    app.run(debug=True)
