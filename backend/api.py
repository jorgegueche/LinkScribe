from fastapi import FastAPI,Request
import uvicorn
import numpy as np
from pathlib import Path
from model_loader import ModelLoader, Backend
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import urllib.parse
import pickle
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sb
import nltk
import string
import re
import sklearn.metrics as sm
#import imblearn
from joblib import dump, load


app = FastAPI ()
data = np.random.rand (200, 200)

@app.get ("/")
def read_root():
    return {"message": "Hi from fastapi"}

@app.on_event ("startup")
def load_model ():
    """this function will run once when 
    the application starts up""" 
print ("Loading the model.")

model = ModelLoader(
        path ='backend/modelo_entrenado.pkl' ,
        Backend=Backend.sklearn,
        labels=['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel'],
        name='modelo_entrenado', 
        version=1.1
   )
print(" Model loaded successfully! ")
app.state.model=model

tf_idf_vectorizer = load('/Users/mac/Documents/uaoproyecto/my-first-project/backend/vectorizador.joblib')


from fastapi import FastAPI, HTTPException
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import urllib.parse
from pydantic import BaseModel, Field
from validators import url


app = FastAPI()

model = ModelLoader(
        path ='backend/modelo_entrenado.pkl' ,
        Backend=Backend.sklearn,
        labels=['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel'],
        name='modelo_entrenado', 
        version=1.1
   )
print(" Model loaded successfully! ")
app.state.model=model

class PredictInput(BaseModel):
    web_link: str = Field(..., description="URL a procesar")

def get_metadata(url):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.title.string

        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else ""

        meta_image = soup.find('meta', attrs={'property': 'og:image'})
        image_url = meta_image['content'] if meta_image else ""

        meta_summary = soup.find('meta', attrs={'name': 'description'})  # Ajusta según la etiqueta real para el resumen
        summary = meta_summary['content'] if meta_summary else ""

        return {
            'title': title,
            'description': description,
            'image_url': image_url,
            'article_summary': summary,
        }
    except Exception as e:
        return {'error': str(e)}

@app.post("/predict")
async def predict(input_data: PredictInput):
    try:
        web_link = urllib.parse.unquote(input_data.web_link.strip('"'))

        if not url(web_link):
            raise HTTPException(status_code=422, detail="La URL proporcionada no es válida")

        # Obtener metadata
        metadata = get_metadata(web_link)

        # Procesamiento de NLP opcional con newspaper3k para obtener más información
        article = Article(web_link)
        article.download()
        article.parse()
        article_text = article.text
        article_summary = article.summary

        # Devolver los resultados en un diccionario
        results = {
            **metadata,
            'article_text': article_text,
            'article_summary': article_summary
        }

        # Realizar predicciones (aquí debes tener definido tu modelo 'model')
        text_raw = [metadata.get('description')]  # Asegúrate de manejar el caso en que 'description' no esté presente
        predict = model.predict(text_raw)
        print(results.get('description', ''))
        

        return {"message": "Web link received successfully", "prediction_features": predict, "metadata": results}
    except Exception as e:
        return {"error": str(e)}



    