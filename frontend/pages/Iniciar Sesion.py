import streamlit as st
import sqlite3

# Función para verificar las credenciales del usuario en la base de datos
def authenticate_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Verificar si las credenciales son correctas
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        authenticated_user = cursor.fetchone()

        conn.close()

        return authenticated_user is not None
    except sqlite3.Error as e:
        st.error(f"Error al autenticar usuario: {e}")
        return False

def app():
    st.set_page_config(
        page_title="LinkScribe",
        page_icon="/Users/juesm/Workspace/Projects-AI_2023/First-Project/frontend/icono.png",
        layout="wide"
    )

    # Título de la aplicación
    st.title('Inicio de Sesión')

    # Campos de entrada de usuario
    username = st.text_input('Nombre de usuario')
    password = st.text_input('Contraseña', type='password')

    # Botón para iniciar sesión
    if st.button('Iniciar Sesión'):
        # Verificar las credenciales del usuario
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.success('Inicio de sesión exitoso.')
        else:
            st.error('Credenciales incorrectas. Por favor, inténtalo de nuevo.')

    # Si el usuario no ha iniciado sesión, no mostrar el contenido de Home
    if not st.session_state.get('logged_in', False):
        return

    # Aquí comienza el contenido de Home
    st.title("Bienvenido a la aplicación ")
    # Agrega aquí el resto del contenido de la página de inicio


    


if __name__ == "__main__":
    app()
