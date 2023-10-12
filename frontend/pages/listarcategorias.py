import sqlite3
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Contenido de la Base de Datos",
    page_icon="/Users/mac/Documents/uaoproyecto/my-first-project/frontend/icono1.png",
    layout="wide"
)

# Función para mostrar el contenido de la base de datos
def show_database_content():
    try:
        
        db_path = "/Users/mac/Documents/uaoproyecto/my-first-project/Base_de_datos.db"
        with sqlite3.connect(db_path) as conexion:
            # Banners
            
            #st.image("icono.jpg", use_column_width=True)

            # Imprime un mensaje de depuración para verificar la conexión
           # st.success("Conexión a la base de datos establecida correctamente.")

            # Imprime la lista de tablas en la base de datos
            cursor = conexion.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Diseño para mostrar las tablas
           # st.subheader("Tablas en la base de datos:")
           # st.table(tables)

            # Obtener y mostrar información de la tabla Links
            cursor.execute('SELECT * FROM Links')
            links_data = cursor.fetchall()
            if links_data:
                links_df = pd.DataFrame(links_data, columns=[desc[0] for desc in cursor.description])
                st.subheader("Contenido de la tabla Links:")
                st.dataframe(links_df, height=300)  
            else:
                st.info("La tabla Links está vacía.")

            # Obtener y mostrar información de la tabla Keywords
            keywords_df = pd.read_sql_query('SELECT * FROM Keywords', conexion)
            if not keywords_df.empty:
                st.subheader("Contenido de la tabla Keywords:")
                st.dataframe(keywords_df, height=300)  
            else:
                st.info("La tabla Keywords está vacía.")
            
            st.subheader("Comparación de Enlaces y Palabras Clave:")
            st.bar_chart({"Enlaces": len(links_data), "Palabras Clave": len(keywords_df)})


            # Gráfico de pastel para estadísticas
            st.subheader("Estadísticas:")
            st.write("Número de enlaces:", len(links_data))
            st.write("Número de palabras clave:", len(keywords_df))

    except sqlite3.Error as e:
        st.error(f"Error al mostrar el contenido de la base de datos: {e}")

# Llamada a la función para mostrar el contenido de la base de datos
show_database_content()


