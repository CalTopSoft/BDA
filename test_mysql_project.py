import mysql.connector
from mysql.connector import Error

# Inicializar la conexión como None
conn = None

try:
    # Intentar conectar a la base de datos MySQL
    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='hojas_de_vida'  # Asegúrate de que el nombre sea correcto
)

    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
        c = conn.cursor()

        # Crear la tabla si no existe
        def crear_tabla():
            c.execute('''
            CREATE TABLE IF NOT EXISTS hojas_de_vida (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                direccion VARCHAR(255),
                telefono VARCHAR(15),
                email VARCHAR(255),
                jornada TEXT,  # Cambié "educacion" por "jornada"
                curso TEXT     # Cambié "experiencia" por "curso"
            )
            ''')
            conn.commit()

        # Función para agregar una hoja de vida
        def agregar_hoja_de_vida(nombre, direccion, telefono, email, jornada, curso):
            c.execute('''
            INSERT INTO hojas_de_vida (nombre, direccion, telefono, email, jornada, curso)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, direccion, telefono, email, jornada, curso))
            conn.commit()
            print("Hoja de vida agregada correctamente.")

        # Función para obtener todas las hojas de vida
        def obtener_hojas_de_vida():
            c.execute('SELECT * FROM hojas_de_vida')
            return c.fetchall()

        # Función para obtener una hoja de vida por ID
        def obtener_hoja_de_vida_por_id(id):
            c.execute('SELECT * FROM hojas_de_vida WHERE id = %s', (id,))
            return c.fetchone()

        # Función para mostrar todas las hojas de vida
        def mostrar_hojas_de_vida():
            hojas_de_vida = obtener_hojas_de_vida()
            if hojas_de_vida:
                for hoja in hojas_de_vida:
                    print(f'ID: {hoja[0]} - Nombre: {hoja[1]} - Dirección: {hoja[2]} - Teléfono: {hoja[3]} - Email: {hoja[4]} - Jornada: {hoja[5]} - Curso: {hoja[6]}')
            else:
                print("No hay hojas de vida registradas.")

        # Función para mostrar una hoja de vida por ID
        def mostrar_hoja_de_vida_por_id(id):
            hoja = obtener_hoja_de_vida_por_id(id)
            if hoja:
                print(f'ID: {hoja[0]} - Nombre: {hoja[1]} - Dirección: {hoja[2]} - Teléfono: {hoja[3]} - Email: {hoja[4]} - Jornada: {hoja[5]} - Curso: {hoja[6]}')
            else:
                print("No se encontró la hoja de vida con ese ID.")

        # Función para interactuar con el usuario
        def menu():
            while True:
                print("\n=== Menú de Gestión de Hojas de Vida ===")
                print("1. Agregar nueva hoja de vida")
                print("2. Mostrar todas las hojas de vida")
                print("3. Buscar hoja de vida por ID")
                print("4. Salir")
                
                opcion = input("Selecciona una opción (1/2/3/4): ")
                
                if opcion == '1':
                    nombre = input("Nombre: ")
                    direccion = input("Dirección: ")
                    
                    # Bucle para asegurar que el teléfono tenga exactamente 10 dígitos
                    while True:
                        telefono = input("Teléfono (10 dígitos): ")
                        if len(telefono) == 10 and telefono.isdigit():
                            break
                        else:
                            print("Error: El número debe tener exactamente 10 dígitos y solo números.")
                    
                    # Bucle para asegurar que el email contenga el símbolo '@'
                    while True:
                        email = input("Email: ")
                        if '@' not in email:
                            print("Error: El correo electrónico debe contener el símbolo '@'.")
                        else:
                            break

                    jornada = input("Jornada: ")  # Cambié "educacion" por "jornada"
                    curso = input("Curso: ")      # Cambié "experiencia" por "curso"
                    agregar_hoja_de_vida(nombre, direccion, telefono, email, jornada, curso)
                
                elif opcion == '2':
                    mostrar_hojas_de_vida()
                
                elif opcion == '3':
                    try:
                        id_buscar = int(input("Introduce el ID de la hoja de vida a buscar: "))
                        mostrar_hoja_de_vida_por_id(id_buscar)
                    except ValueError:
                        print("Error: Debes ingresar un número entero válido.")
                
                elif opcion == '4':
                    print("Saliendo del programa...")
                    break
                
                else:
                    print("Opción no válida. Intenta de nuevo.")

        # Crear la tabla al iniciar el programa
        crear_tabla()

        # Iniciar el menú interactivo
        menu()

except Error as e:
    print(f"Error al conectar a MySQL: {e}")

finally:
    # Cerrar la conexión si fue establecida
    if conn and conn.is_connected():
        conn.close()
        print("Conexión cerrada")