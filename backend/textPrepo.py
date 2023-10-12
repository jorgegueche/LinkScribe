import requests
import pandas as pd
import string
import re
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import sklearn
nltk.download('stopwords')
nltk.download('punkt')


class texto():
    def __init__(self,
                 desc:str):
        self.desc = desc

    def prepro(self):
        from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
        with open("params/CountVectorizer.pk", 'rb') as file:
            count = pickle.load(file)

        # Cargar el objeto TfidfTransformer
        with open("params/TfidfTransformer.pk", 'rb') as file:
            Tfidf = pickle.load(file)
        count =  pickle.load(open("params/CountVectorizer.pk",'rb'))
        Tfidf = pickle.load(open("params/TfidfTransformer.pk",'rb'))
        description_arr = pd.DataFrame([{'descripcion': self.desc}])
        description_arr['descripcion']= description_arr['descripcion'].apply(lambda x:x.lower())
        description_arr['tokenized_words'] = description_arr['descripcion'].apply(lambda x:word_tokenize(x))
        description_arr['tokenized_words'] = description_arr['tokenized_words'].apply(lambda x:[re.sub(f'[{string.punctuation}]+','',i) for i in x if i not in list(string.punctuation)])
        description_arr['tokenized_words']= description_arr['tokenized_words'].apply(lambda x:' '.join(x))
        description_arr=description_arr[['tokenized_words']]
        X_web = description_arr['tokenized_words']
        X_web_count = count.transform(X_web)
        X_web_Tfidf = Tfidf.transform(X_web_count)
        X_web_Array = X_web_Tfidf.toarray()
        return X_web_Array

        
        