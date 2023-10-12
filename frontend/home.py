import streamlit as st
import requests
import json
import sqlite3

# Iniciar sesión habilitado o deshabilitado

url = "http://localhost:8000/predict"



def call_api(web_link):
    try:
        request_data = {"web_link": web_link}
        request_data_json = json.dumps(request_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=request_data_json)
        response_json = response.json()
        
        predictions = response_json.get('prediction_features', [])
        metadata_url = response_json.get('metadata', {})
        
        info = metadata_url.get('title', '')
        info2 = metadata_url.get('description', '')
        info3 = metadata_url.get('image_url', '')
        info4 = metadata_url.get('article_summary', '')
        info5 = metadata_url.get('article_text', '')

        return predictions, info, info2, info3, info4, info5

    except Exception as e:
        st.error(f"Error al llamar a la API: {e}")
        return [], '', '', '', '', ''

def is_link_in_database(url):
    try:
        with sqlite3.connect("/Users/mac/Documents/uaoproyecto/my-first-project/Base_de_datos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute('SELECT COUNT(*) FROM Links WHERE url = ?', (url,))
            count = cursor.fetchone()[0]
            return count > 0
    except sqlite3.Error as e:
        st.error(f"Error al verificar la existencia en la base de datos: {e}")
        return False

def store_in_database(url, title, description, image_url, article_summary, article_text, category_id):
    try:
        if is_link_in_database(url):
            st.warning(f"La URL '{url}' ya está en la base de datos.")
            return

        with sqlite3.connect("/Users/mac/Documents/uaoproyecto/my-first-project/Base_de_datos.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO Links (url, title, description, category_id)
                VALUES (?, ?, ?, ?)
            ''', (url, title, description, category_id))

            link_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO Keywords (keyword, link_id, user_id)
                VALUES (?, ?, ?)
            ''', (article_summary, link_id, 1))

            cursor.execute('''
                INSERT INTO Keywords (keyword, link_id, user_id)
                VALUES (?, ?, ?)
            ''', (article_text, link_id, 1))

            st.success("Datos insertados en la tabla Links.")

            conexion.commit()

    except sqlite3.Error as e:
        st.error(f"Error al almacenar en la base de datos: {e}")

def app():

    st.set_page_config(
        page_title="LinkScribe",
        page_icon="/Users/mac/Documents/uaoproyecto/my-first-project/frontend/icono.png",
        layout="wide"
    )

    st.title('Clasificador de Enlaces')

    web_link = st.text_input('Ingresar el enlace', '')
    i_was_clicked = st.button("Predict")

    if i_was_clicked:
        predictions, info, info2, info3, info4, info5 = call_api(web_link)

        if predictions:
            st.write(f'Categoría: {predictions[0]}')
            st.write(f'Título: {info}')
            st.write(f'Descripción: {info2}')
            st.image(info3, caption='', use_column_width=True)
            st.write(f'Resumen: {info4}')
            st.write(f'Artículo: {info5}')

        store_in_database(
            url=web_link,
            title=info,
            description=info2,
            image_url=info3,
            article_summary=info4,
            article_text=info5,
            category_id=predictions[0] if predictions else ''
        )

    st.header('Enlaces Clasificados')


if __name__ == "__main__":
  app()