#TFIDF
import preprocessing
import codecs
import math
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys 
import pickle
from nltk.stem import PorterStemmer
import json
import numpy as np
import nltk
from nltk.corpus import wordnet
from autocorrect import spell
import wiki



with open("list_vocab.json") as json_data:
    list_vocab = json.load(json_data)
    
with open("list_fileNames.json") as json_data:
    list_fileNames = json.load(json_data)
    
    
rows, cols = len(list_vocab) , len(list_fileNames)
TFIDFMatrix = [[0 for x in range(cols)] for y in range(rows)] 


with open("TFIDFMatrix.json") as json_data:
    TFIDFMatrix = json.load(json_data)
    
QueryVector = [0]*len(list_vocab)


    
def cos_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
    
    
def generateTFIDFforUserQuery(userQuery):
   corrected_list = []
   set_expandQuery = set()
   word_tokens = word_tokenize(userQuery)
   
   for token in word_tokens:
       corrected_list.append(spell(token))
       
   print " ".join(corrected_list)   
   set_expandQuery = set(preprocessing.fn_preprocessingtoken(" ".join(corrected_list)))
   
   for item in set_expandQuery:
       if item in list_vocab:
          QueryVector[list_vocab.index(item)]=1
   
   return QueryVector

    
    
def UserQuery():
    ageGroup = ""
    age = raw_input("Please enter your age group:(1:less than 10, 2: 10-50 , 3: 50 & above): ")
    if age=="1":
        ageGroup="child"
    if age=="2":
        ageGroup="adult"
    if age=="3":
        ageGroup="old"
        
    print "ageGroup",ageGroup  
    gender = raw_input("Please enter your gender(Male/Female): ")
    print gender
    symptoms = raw_input("Please enter the list of symptoms you are facing: ")
    queryVector = generateTFIDFforUserQuery(symptoms+" "+ageGroup+" "+gender)
    
    transposedTFIDF = np.transpose(TFIDFMatrix)
    list_cosineval = []
    
    for i in range(0,len(list_fileNames)):
        list_cosineval.append(cos_similarity(queryVector, transposedTFIDF[i]))
    
    
    item_index_1 = list_cosineval.index(sorted(list_cosineval)[-1])
    item_index_2 = list_cosineval.index(sorted(list_cosineval)[-2])
    item_index_3 = list_cosineval.index(sorted(list_cosineval)[-3])
    print wiki.getEntityLabel(list_fileNames[item_index_1])
    print wiki.getEntityLabel(list_fileNames[item_index_2])
    print wiki.getEntityLabel(list_fileNames[item_index_3])
    
    
#    dict_expected_disease_symptom = {}
#    dict_expected_disease_symptom["Q12125"]=["Q35805","Q1292082"]
#    dict_expected_disease_symptom["Q12090"]=["Q1292082"]
#    dict_expected_disease_symptom["Q178623"]=["Q1115038"]
#    print dict_expected_disease_symptom
#    
#    disease_classifier = {}
#    
#    for key in dict_expected_disease_symptom:
#        for i in range(0,len(dict_expected_disease_symptom[key])):
#           flag = raw_input("Are you feeling something similar to"+ dict_expected_disease_symptom[key][i])
#           if flag == "1":
#                 if disease_classifier.has_key(key):
#                         disease_classifier[key]=disease_classifier[key]+1
#                 else:
#                         disease_classifier[key]=1
#                         
#    print disease_classifier
                 
    
    
    
    

          
UserQuery()    
#generateTFIDFforUserQuery("diclonac soium salt nose child male")

