"""
FICHIER model_maker.py

Ce script python génère un fichier .task, modèle qui sera entraîné sur des images dans un DataSet.
A noter :
- le modèle se réentraine sur le contenu de export_dir aussi
- rajout d'un dossier labelisé -> il faut d'abord supprimer le export_dir puis relancer le programme
"""

import os
import tensorflow as tf
assert tf.__version__.startswith('2')

from mediapipe_model_maker import gesture_recognizer
import matplotlib.pyplot as plt

DATASET_PATH = "../DataSet"
EXPORT_DIR = "exported_model" # nom du dossier où il y aura l'export

print("Dataset path:", DATASET_PATH)

labels = []
for i in os.listdir(DATASET_PATH):
    if os.path.isdir(os.path.join(DATASET_PATH, i)):
        labels.append(i)
print("Labels trouvés :", labels) # label : nom d'un dossier (ici geste)

data = gesture_recognizer.Dataset.from_folder(
    dirname=DATASET_PATH,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)

train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

hparams = gesture_recognizer.HParams(
    export_dir=EXPORT_DIR,
    learning_rate=0.0001, # baisser pour plus de précisions
    batch_size=32, # augmenter //
    epochs=70 # augmenter //
)

options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)

model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

loss, acc = model.evaluate(test_data)
print(f"Loss: {loss}")
print(f"Accuracy: {acc}")

model.export_model()
print(f"Export là : {EXPORT_DIR}/")
