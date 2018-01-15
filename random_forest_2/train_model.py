#!/usr/bin/python3

import csv
import text_classification
import random_forest
import pickle

random_forest.DEBUG = True

model = random_forest.RandomForest(1000)
with open('labels.csv', 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        labels.append(tuple(row))
data = text_classification.TextDataContainer(labels)
model.train(data)

with open('model.dat', 'wb') as f:
    pickle.dump(model, f)
