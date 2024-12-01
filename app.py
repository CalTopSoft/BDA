from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesario para manejar sesiones

# Configuración de la conexión a MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='hojas_de_vida'
    )

# Página principal con el login
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Manejar el login
@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    # Validar usuario y contraseña en la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s", (correo, contrasena))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Almacenar información del usuario en la sesión
        session['usuario'] = correo
        return redirect(url_for('consult'))  # Redirigir a la página de consulta
    else:
        return render_template('index.html', error='Correo o contraseña incorrectos')

# Página de consulta (consult.html)
@app.route('/consult')
def consult():
    # Verificar si el usuario está autenticado
    if 'usuario' not in session:
        return redirect(url_for('home'))  # Redirigir al login si no está autenticado

    return render_template('consult.html')

# Mostrar todas las hojas de vida
@app.route('/hojas', methods=['GET'])
def obtener_hojas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hojas_de_vida')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# Buscar hoja de vida por ID
@app.route('/hojas/<int:id>', methods=['GET'])
def obtener_hoja(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hojas_de_vida WHERE id = %s', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(row)
    else:
        return jsonify({'error': 'Hoja de vida no encontrada'}), 404

# Página para agregar una nueva hoja de vida
@app.route('/nueva', methods=['POST'])
def agregar_hoja():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    jornada = request.form['jornada']
    curso = request.form['curso']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hojas_de_vida (nombre, direccion, telefono, email, jornada, curso)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (nombre, direccion, telefono, email, jornada, curso))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))  # Redirige a la página principal

if __name__ == '__main__':
    app.run(debug=True)
