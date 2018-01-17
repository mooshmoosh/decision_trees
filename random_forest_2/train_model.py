#!/usr/bin/python3

import csv
import text_modelling
import random_forest
import pickle
import os

random_forest.DEBUG = True

model = random_forest.RandomForest(5)
print("loading text documents")
data = text_modelling.PredictedTextContainer([os.path.join('text_documents', filename) for filename in os.listdir('text_documents')])
print("done")
print("Beginning training")
model.train(data)
print("finished training")

print("saving model")
with open('model.dat', 'wb') as f:
    pickle.dump(model, f)
print("finished saving model")
