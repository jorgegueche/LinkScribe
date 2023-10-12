import streamlit as st
import sqlite3

# Función para crear la tabla de usuarios (ejecutar solo una vez)
def create_users_table():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Crear la tabla de usuarios si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT
            )
        ''')

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Error al crear la tabla de usuarios: {e}")

# Función para registrar un usuario en la base de datos
def register_user(username, email, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM Users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            st.warning("Este usuario o correo electrónico ya está registrado.")
        else:
            # Insertar nuevo usuario
            cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            st.success(f'Usuario {username} registrado exitosamente.')

        conn.close()
    except sqlite3.Error as e:
        st.error(f"Error al registrar usuario: {e}")

# Crear la tabla de usuarios al inicio de la aplicación
create_users_table()

def app():
    st.set_page_config(
        page_title="LinkScribe",
        page_icon="/Users/juesm/Workspace/Projects-AI_2023/First-Project/frontend/icono.png",
        layout="wide"
    )

    st.title("Users")
    st.write('Welcome')
    st.write('This is a Streamlit app')
    st.write('Aqui te puedes logear.')

    # Título de la aplicación
    st.title('Registro de Usuarios')

    # Campos de entrada de usuario
    username = st.text_input('Nombre de usuario')
    email = st.text_input('Correo electrónico')
    password = st.text_input('Contraseña', type='password')
    confirm_password = st.text_input('Confirmar Contraseña', type='password')

    # Botón para registrar usuario
    if st.button('Registrar Usuario'):
        if password == confirm_password:
            # Registrar el usuario en la base de datos
            register_user(username, email, password)
        else:
            st.error('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')

if __name__ == "__main__":
    app()
