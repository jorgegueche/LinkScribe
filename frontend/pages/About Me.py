import streamlit as st

def app():
  import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="LinkScribe",
    page_icon="/Users/juesm/Workspace/Projects-AI_2023/First-Project/frontend/icono.png",
    layout="wide"
)

# Título principal
st.title("Crear y Organizar un Grupo de Trabajo")

# Introducción
st.write('¡Bienvenido!')
st.write('Estamos emocionados de trabajar juntos en este proyecto.')

# Descripción del Grupo de Trabajo
st.write('**Grupo de Trabajo:** Equipo LinkScribe')
st.write('**Objetivo:** Diseñar, desarrollar e implementar la solución.')
st.write('**Roles y Responsabilidades:**')

# Lista de roles
st.write('- **Líder del Proyecto:** Encargado de la supervisión general y la toma de decisiones estratégicas.')
st.write('- **Diseñadores de Interfaz:** Responsables de la apariencia y usabilidad de la solución.')
st.write('- **Desarrolladores:** Encargados de la implementación técnica de la solución.')
st.write('- **Comunicación y Coordinación:** Garantizar la fluidez de la comunicación y coordinación entre los miembros del equipo.')
st.write('- **QA / Control de Calidad:** Realizar pruebas para garantizar la calidad del producto final.')

# Canales de Comunicación
st.write('**Canales de Comunicación:**')
st.write('- Utilizaremos Slack para comunicaciones diarias y actualizaciones.')
st.write('- Reuniones semanales a través de Zoom para revisar el progreso y abordar cualquier problema.')

# Cierre
st.write('Gracias por formar parte de este emocionante proyecto. ¡Esperamos lograr grandes cosas juntos!')

# Información adicional sobre la aplicación Streamlit
st.title("Acerca del Proyecto")
st.write('Esta es una aplicación Streamlit')
st.write('La aplicación está basada en el conjunto de datos clasificaion de urls.')
if __name__ == "__main__": 
  app()