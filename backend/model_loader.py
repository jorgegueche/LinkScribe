import typing
from pathlib import Path
import numpy as np
from enum import Enum
from fastapi import FastAPI, Request
import sklearn 
from bs4 import BeautifulSoup
from newspaper import Article
from sklearn.feature_extraction.text import TfidfVectorizer

tf_idf_vectorizer= TfidfVectorizer()
# Ejemplo de uso:


class Backend(Enum):
    tensorflow = 'tensorflow'
    sklearn = 'sklearn'
    pytorch = 'pytorch'
    
class ModelLoader(object):
    def __init__(self, 
                  path: typing.Union[str, Path], 
                  name: str, 
                  version: float = 1.0,
                  Backend: str = 'sklearn', labels: typing.List[str] = None):
        self.path = path
        self.name = name
        self.version = version
        self.backend = Backend
        self.labels = labels

        if self.backend == Backend.tensorflow:
            self.model = self.__load_tensorflow_model()
        elif self.backend == Backend.sklearn:
            self.model = self.__load_sklearn_model()
        else:
            raise NotImplementedError(f'Backend {self.backend} is not supported.')
        

    def __load_tensorflow_model(self):
        """"
        Load tensorflow model from path
        """
        import tensorflow as tf
        model = tf.keras.models.load_model(self.path)
        return model
    

    def __load_sklearn_model(self):
        """"
        Load sklearn model from path
        """
        import pickle
        with open('/Users/mac/Documents/uaoproyecto/my-first-project/backend/modelo_entrenado.pkl', 'rb') as f:
            return pickle.load(f)
        

    def predict(self, data: np.ndarray) -> np.ndarray:
        """
        Predict data using model
        """
        predictions =  self.model.predict(data)
        predictions = predictions.tolist()
        if self.labels:
            if self.backend == Backend.sklearn:
                predictions = [self.labels[label_idx] for label_idx in predictions]
            elif self.backend == Backend.tensorflow:
                predictions = [self.labels[np.argmax(prediction)] for prediction in predictions]
        return predictions
    
        



if __name__ == "__main__":
    
    backend = Backend.sklearn
    models_path = {
        
        #'tensorflow': '/Users/mac/Documents/uaoproyecto/my-first-project/backend/models/tf/iris_model',
        'sklearn': 'backend/modelo_entrenado.pkl'
    }
    

    model = ModelLoader(
        path=models_path[backend.value], 
        name='modelo_entrenado', 
        version=1.1, 
        Backend=backend, 
        labels=['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel']
    )
    
    #prediction = model.predict(text_to_predict)
    #print(prediction)