# web_info.py
from bs4 import BeautifulSoup
import requests

class PaginaWebInfo:
    def __init__(self, url):
        self.url = url

    def obtener_informacion(self):
        try:
            # Realiza una solicitud GET a la página web
            response = requests.get(self.url)
            
            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Parsea el contenido HTML de la página con BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Busca la etiqueta meta "description"
                meta_description = soup.find('meta', attrs={'name': 'description'})
                
                # Busca el título de la página (etiqueta <title>)
                page_title = soup.title.string if soup.title else "Título no encontrado"
                
                # Busca la etiqueta meta "og:image" para la imagen de vista previa
                meta_image = soup.find('meta', attrs={'property': 'og:image'})
                
                # Si no se encuentra con og:image, busca en twitter:image
                if not meta_image:
                    meta_image = soup.find('meta', attrs={'name': 'twitter:image'})
                
                # Obtiene la URL de la imagen de vista previa o el favicon
                if meta_image:
                    image_url = meta_image.get('content')
                else:
                    # Realiza una solicitud HEAD para obtener el favicon
                    favicon_response = requests.head(self.url)
                    
                    # Busca el favicon en los encabezados de la respuesta
                    favicon_url = None
                    if 'favicon' in favicon_response.headers:
                        favicon_url = favicon_response.headers['favicon']
                    
                    # Si no se encuentra el favicon en los encabezados, intenta construir la URL
                    if not favicon_url:
                        base_url = self.url if self.url.endswith('/') else self.url + '/'
                        favicon_url = base_url + 'favicon.ico'
                    
                    image_url = favicon_url
                
                # Devuelve la información obtenida
                return {
                    'Titulo': page_title,
                    'Descripcion': meta_description.get("content") if meta_description else "Descripcion no encontrada",
                    'imagen': image_url
                }
            else:
                return {'Error': 'No se pudo acceder a la página web.'}
        except Exception as e:
            return {'Error': f'Error al acceder a la página web: {str(e)}'}