from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing # processing.scale // for scaling continuous variable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

#Load model
diagnosis_model = pickle.load(open('../model/knnpickle_file', 'rb'))
#Load the sample data
sample_data = pd.read_csv('../model/Training.csv')
# Define the possible diagnosis labels
diagnosis_label=list(set(sample_data['prognosis']))
diagnosis_label.sort()
# Define the list of possible symptoms
possibleSymptoms=list(sample_data.drop(['prognosis'], axis = 1).columns)
# Define dictionary for symptoms
inputDict=dict(zip(possibleSymptoms,np.zeros(len(possibleSymptoms), np.int8)))

def getIllness(symptoms):
  inputDict=dict(zip(possibleSymptoms,np.zeros(len(possibleSymptoms), np.int8)))
  for symp in symptoms:
    print(symp)
    inputDict[symp]=1
  illnessPredicted = diagnosis_model.predict([list(inputDict.values())])
  illnessPredicted_prob = diagnosis_model.predict_proba([list(inputDict.values())])
  print(illnessPredicted)
  print(illnessPredicted_prob)
  return [illnessPredicted,illnessPredicted_prob]
  
def NextQuestion(symptoms,NegSymptoms):
  predictions,predictions_prob=getIllness(symptoms)
    #step 2:find the illness with a probability larger than 0
  predict_illness = []
  count=0
  for i in predictions_prob[0]:
    if(i > 0):
        predict_illness.append(diagnosis_label[count])
    count+=1
  print(predict_illness)
  matched_illness = sample_data[sample_data['prognosis'].isin(predict_illness)]
  dict_ill = {}
  #step 3: find the most common symptom in these illnesses
  for sym in possibleSymptoms:
    matched_symptoms = matched_illness[matched_illness[sym] == 1]
    if(len(matched_symptoms) > 0):
        dict_ill[sym] = len(matched_symptoms)
  print(dict_ill)
  for symp in symptoms+NegSymptoms:
    try:
      del dict_ill[symp]
    except:
      print("symptom not in next symptoms")
      continue
  if len(dict_ill) > 0:
    t = sorted(dict_ill.items(), key=lambda item:item[1], reverse=True)
    return t[0][0],predictions
  else:
    return "",predictions
