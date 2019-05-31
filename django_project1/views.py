from django.shortcuts import render
from django.http import HttpResponse,Http404
from rest_framework.response import Response
from rest_framework import status
#from .forms import ContactForm
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.preprocessing.sequence import pad_sequences
import pickle
import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse

from rasa_nlu.model import Interpreter
from keras import backend as K
#prétraitement
import nltk                       # the natural langauage toolkit, open-source NLP
import re 
from nltk.corpus import stopwords  
from gensim import parsing        # Help in preprocessing the data, very efficiently
import gensim
import numpy as np
import pandas as pd
import os


max_words = 2000
max_len=25
@api_view(["POST"])
def prediction_urgence(text):
   try:
      msg=json.loads(text.body)
      #prétraitement
      stops = set(stopwords.words("english"))
    
      # Convert text to lower
      text = (msg["message"]).lower()
      # Removing non ASCII chars    
      text = re.sub(r'[^\x00-\x7f]',r' ',text)
    
      # Strip multiple whitespaces
      text = gensim.corpora.textcorpus.strip_multiple_whitespaces(text)
    
      # Removing all the stopwords
      filtered_words = [word for word in text.split() if word not in stops]
    
      # Removing all the tokens with lesser than 3 characters
      filtered_words = gensim.corpora.textcorpus.remove_short(filtered_words, minsize=3)
    
      # Preprocessed text after stop words removal
      text = " ".join(filtered_words)
    
      # Remove the punctuation
      text = gensim.parsing.preprocessing.strip_punctuation2(text)
    
      # Strip all the numerics
      text = gensim.parsing.preprocessing.strip_numeric(text)
    
      # Strip multiple whitespaces
      text = gensim.corpora.textcorpus.strip_multiple_whitespaces(text)
    
      # Stemming
      pretraitement=gensim.parsing.preprocessing.stem_text(text)
      #prétraitement
      #modele
      model = os.path.abspath('model_service3_pretrai.sav')
      token = os.path.abspath('token_service3_pretrai.sav')
      loaded_model = pickle.load(open(model, 'rb'))
      token = pickle.load(open(token, 'rb'))
      x_input = np.array([msg["message"]])
      #x_input = np.array([pretraitement])
      sequences= token.texts_to_sequences(x_input)
      sequences_matrix = pad_sequences(sequences,maxlen=max_len)
      result = loaded_model.predict(sequences_matrix)
      #modele
      #rasa
      rasamodel = os.path.abspath('current')
      interpreter = Interpreter.load(rasamodel)
      
      rasa= interpreter.parse(msg["message"])
      K.clear_session()
      #rasa
      if result>0.7:
            affiche = 'urgent'
            r=str(result[0][0])
      else:
            affiche= 'not_urgent'
            r=str(1-result[0][0])
      
      return HttpResponse(json.dumps({"id":msg["id"],"message":msg["message"],"label":affiche,"probability":r,"intent":rasa["intent"]["name"]}), content_type='application/json')
      #,"intent":rasa["intent"]["name"],"confidence":rasa["intent"]["confidence"]
   except ValueError as e:
      return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


