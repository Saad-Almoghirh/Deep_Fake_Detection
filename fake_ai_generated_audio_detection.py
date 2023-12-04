# -*- coding: utf-8 -*-
"""Fake_AI-generated_Audio_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17GxLfgZ3ZSlpb8qCTKCubi3qtX5IlHBN
"""

import os
import pandas as pd
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
import soundfile as sf

'''
directory_path = r"C:\mine\SDAIA T5\CAPSTONE\LA\LA\ASVspoof2019_LA_train\flac"
directory_path = r"D:\LA\LA\ASVspoof2019_LA_train\flac"
file_list = [f for f in os.listdir(directory_path) if f.endswith('.flac')]

for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    with sf.SoundFile(file_path, 'r') as mywav:
        duration_seconds = len(mywav) / mywav.samplerate
        print(f"Length of {file_name}: {duration_seconds:.1f} s")
'''

from google.colab import drive
drive.mount('/content/drive')

# Define paths and parameters
DATASET_PATH = "/content/drive/My Drive/Colab Notebooks/ASVspoof2019_PA_train_sample"
LABEL_FILE_PATH = "/content/drive/My Drive/Colab Notebooks/ASVspoof2019_PA_train_sample_labels/ASVspoof2019.PA.cm.train.sample.trn.txt"
NUM_CLASSES = 2  # Number of classes (bonafide and spoof)
SAMPLE_RATE = 16000  # Sample rate of your audio files
DURATION = 5  # Duration of audio clips in seconds
N_MELS = 128  # Number of Mel frequency bins
n_fft = 1024  # or some other larger value
hop_length = 512  # Adjust as needed
window = 'hann'  # or other window functions
#spectrogram = librosa.feature.melspectrogram(y=DATASET_PATH, sr=SAMPLE_RATE, n_fft=4096)

# Define paths and parameters
DATASET_PATH = r'C:\mine\SDAIA T5\CAPSTONE\LA\LA\ASVspoof2019_LA_train\flac'
LABEL_FILE_PATH = "ASVspoof2019.LA.cm.train.sample.trn.txt"
NUM_CLASSES = 2  # Number of classes (bonafide and spoof)
SAMPLE_RATE = 16000  # Sample rate of your audio files
DURATION = 5  # Duration of audio clips in seconds
N_MELS = 128  # Number of Mel frequency bins
n_fft = 1024  # or some other larger value
hop_length = 512  # Adjust as needed
window = 'hann'  # or other window functions
#spectrogram = librosa.feature.melspectrogram(y=DATASET_PATH, sr=SAMPLE_RATE, n_fft=4096)

df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/ASVspoof2019_PA_train_sample_labels/ASVspoof2019.PA.cm.train.sample.trn.txt", sep=" ", header=None)

df

#df.shape
df.isnull().sum()

df.columns =['speaker_id','filename','system_id','null','class_name']
df

df.drop(columns=['null'],inplace=True)
df

df['filepath'] = f'{LABEL_FILE_PATH}/ASVspoof2019_LA_train/flac/'+df.filename+'.flac'
df['target'] = (df.class_name=='spoof').astype('int32')
df

df['class_name'].value_counts()

'''
spectrogram = librosa.feature.melspectrogram(y=audio_array, sr=SAMPLE_RATE)
audio_array = np.asarray(DATASET_PATH, dtype=np.float32)
D = librosa.stft(y, n_fft=2048, hop_length=512, window='hann')
'''

#THIS TAKES A LONG TIME--NO SAMPLE
'''
labels = {}

for line in lines:
    parts = line.strip().split()
    file_name = parts[1]
    label = 1 if parts[-1] == "bonafide" else 0
    labels[file_name] = label

X = []
y = []

max_time_steps = 109  # Define the maximum time steps for your model

for file_name, label in labels.items():
    file_path = os.path.join(DATASET_PATH, file_name + ".flac")

    # Load audio file using librosa
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Extract Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Ensure all spectrograms have the same width (time steps)
    if mel_spectrogram.shape[1] < max_time_steps:
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, max_time_steps - mel_spectrogram.shape[1])), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :max_time_steps]

    X.append(mel_spectrogram)
    y.append(label)
    '''

import random

# Set the desired sample size
sample_size = 1000  # Adjust this to your desired size

labels = {}

with open(LABEL_FILE_PATH, 'r') as label_file:
    lines = label_file.readlines()

for line in lines:
    parts = line.strip().split()
    file_name = parts[1]
    label = 1 if parts[-1] == "bonafide" else 0
    labels[file_name] = label

# Extract a random sample of file names
sample_file_names = random.sample(list(labels.keys()), sample_size)

X = []
y = []

max_time_steps = 109  # Define the maximum time steps for your model

for file_name in sample_file_names:
    label = labels[file_name]
    file_path = os.path.join(DATASET_PATH, file_name + ".flac")

    # Load audio file using librosa
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Extract Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Ensure all spectrograms have the same width (time steps)
    if mel_spectrogram.shape[1] < max_time_steps:
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, max_time_steps - mel_spectrogram.shape[1])), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :max_time_steps]

    X.append(mel_spectrogram)
    y.append(label)

y_encoded = to_categorical(y, NUM_CLASSES)

# Assuming X is a 3D array with shape (number of samples, height, width)

#X = X.reshape(X.shape[0], X.shape[1] * X.shape[2])

split_index = int(0.8 * len(X))
X_train, X_val = X[:split_index], X[split_index:]
y_train, y_val = y_encoded[:split_index], y_encoded[split_index:]

import numpy as np
from sklearn.model_selection import train_test_split

# Assuming X, y are lists
X = np.array(X)
y = np.array(y)

# Perform train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Now you can print the shapes
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

X = np.array(X)
#X_train = np.array(X)
#y = np.array(y)
#X = pd.DataFrame(X_train).apply(np.argmax, axis = 1)
y = pd.DataFrame(y_train).apply(np.argmax, axis = 1)
X,y

y = pd.DataFrame(y_train).apply(np.argmax, axis = 1)

print(len(X_train[0][127]))

X_train.shape

y_train.shape

#pd.DataFrame(y_train).apply(np.argmax, axis = 1)

# Define CNN model architecture
input_shape = (N_MELS, X_train.shape[2], 1)  # Input shape for CNN (height, width, channels)
model_input = Input(shape=input_shape)

'''
import numpy as np

# Assuming X_train is a list
X_train = np.array(X_train)

# Now you can access the shape attribute
input_shape = (N_MELS, X_train.shape[2], 1)
model_input = Input(shape=input_shape)
'''

from keras.models import Sequential
from keras.layers import Dense
model = Sequential()

x = Conv2D(16, kernel_size=(3, 3), activation='relu')(model_input)
x = BatchNormalization()(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
#x = Conv2D(32, kernel_size=(3, 3), activation='relu')(x)
#x = BatchNormalization()(x)
#x = MaxPooling2D(pool_size=(2, 2))(x)
x = Flatten()(x)
x = Dense(32, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.2)(x)
model_output = Dense(1, activation='sigmoid')(x)

'''
from tensorflow.keras.layers import BatchNormalization

x = Conv2D(32, kernel_size=(3, 3))(model_input)
x = BatchNormalization()(x)
x = activation('relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Conv2D(64, kernel_size=(3, 3))(x)
x = BatchNormalization()(x)
x = activation('relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)

x = Dense(128)(x)
x = BatchNormalization()(x)
x = activation('relu')(x)
x = Dropout(0.5)(x)

model_output = Dense(NUM_CLASSES, activation='softmax')(x)
'''

model = Model(inputs=model_input, outputs=model_output)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the Model
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val))

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# saving the model
model.save("audio_classifier.h5")

"""--------
## Visualisation
"""

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load the model and preprocess test data (similar to training data preprocessing)
import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.models import load_model



# Define paths and parameters
TEST_DATASET_PATH = "/content/drive/My Drive/Colab Notebooks/TestEvaluation"
MODEL_PATH = "audio_classifier.h5"  # Replace with the actual path to your saved model
SAMPLE_RATE = 16000
DURATION = 5
N_MELS = 128
MAX_TIME_STEPS = 109

# Define paths and parameters
TEST_DATASET_PATH = r"C:\mine\SDAIA T5\CAPSTONE\LA\LA\ASVspoof2019_LA_eval\flac"
MODEL_PATH = "audio_classifier.h5"  # Replace with the actual path to your saved model
SAMPLE_RATE = 16000
DURATION = 5
N_MELS = 128
MAX_TIME_STEPS = 109

# Load the saved model
model = load_model(MODEL_PATH)

#THIS TAKES A LONG TIME--NO SAMPLE

# Load and preprocess test data using librosa
X_test = []

test_files = os.listdir(TEST_DATASET_PATH)
for file_name in test_files:
    file_path = os.path.join(TEST_DATASET_PATH, file_name)

    # Load audio file using librosa
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Extract Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Ensure all spectrograms have the same width (time steps)
    if mel_spectrogram.shape[1] < MAX_TIME_STEPS:
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, MAX_TIME_STEPS - mel_spectrogram.shape[1])), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :MAX_TIME_STEPS]

    X_test.append(mel_spectrogram)

# Convert list to numpy array
X_test = np.array(X_test)

# Predict using the loaded model
y_pred = model.predict(X_test)

# Convert probabilities to predicted classes
y_pred_classes = np.argmax(y_pred, axis=1)

y_pred

import random

# Set the desired sample size
sample_size = 1000  # Adjust this to your desired size

# Extract a random sample of file names from the test data
sample_test_files = random.sample(os.listdir(TEST_DATASET_PATH), sample_size)

X_test = []

for file_name in sample_test_files:
    file_path = os.path.join(TEST_DATASET_PATH, file_name)

    # Load audio file using librosa
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Extract Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Ensure all spectrograms have the same width (time steps)
    if mel_spectrogram.shape[1] < MAX_TIME_STEPS:
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, MAX_TIME_STEPS - mel_spectrogram.shape[1])), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :MAX_TIME_STEPS]

    X_test.append(mel_spectrogram)

# Convert list to numpy array
X_test = np.array(X_test)

# Predict using the loaded model
y_pred = model.predict(X_test)

# Convert probabilities to predicted classes
y_pred_classes = np.argmax(y_pred, axis=1)

y_pred

len(y_pred)

# Get True Labels

# Path to the ASVspoof 2019 protocol file
PROTOCOL_FILE_PATH = "/content/drive/My Drive/Colab Notebooks/TestEvaluation_Labels/ASVspoof2019.PA.cm.eval.trl.txt"

# Dictionary to store true labels for each file
true_labels = {}

# Read the protocol file
with open(PROTOCOL_FILE_PATH, 'rb') as protocol_file:
    lines = protocol_file.read().decode('utf-8').splitlines()
    print(lines)

for line in lines:
    line = line.strip()  # Strip leading/trailing whitespace
    parts = line.split()
    if len(parts) > 1:  # Check if line has enough parts to extract label
        file_audio_name = parts[1]
        label = parts[-1]  # Last part contains the label
        true_labels[file_audio_name] = label

# Now 'true_labels' contains the true labels for each file
true_labels

len(true_labels)

# Get True Labels

# Path to the ASVspoof 2019 protocol file
PROTOCOL_FILE_PATH = "/content/drive/My Drive/Colab Notebooks/TestEvaluation_Labels/ASVspoof2019.PA.cm.eval.trl.txt"

# Dictionary to store true labels for each file
true_labels = {}

# Read the protocol file
with open(PROTOCOL_FILE_PATH, 'rb') as protocol_file:
    lines = protocol_file.read().decode('utf-8').splitlines()
    print(lines)

for line in lines:
    line = line.strip()  # Strip leading/trailing whitespace
    parts = line.split()
    if len(parts) > 1:  # Check if line has enough parts to extract label
        file_audio_name = parts[1]
        label = parts[-1]  # Last part contains the label
        true_labels[file_audio_name] = label

# Now 'true_labels' contains the true labels for each file
true_labels

y_true = np.array([1 if label == "bonafide" else 0 for label in true_labels.values()]) # y_true are the true labels for each file
y_true

len(y_true)

len(y_val)

len(y_pred_classes)

y_true.dtype

y_pred.dtype

"""Ensure y_true and y_pred have the same data type:

Check the data types of y_true and y_pred. They should both be of the same type (e.g., both should be arrays of integers representing class labels).
"""

from sklearn.metrics import accuracy_score, classification_report

# Assuming y_train is one-hot encoded, and you want to compare it with predicted labels
y_true = pd.DataFrame(y_train).apply(np.argmax, axis=1)
y_pred = np.argmax(model.predict(X_train), axis=1)

# Example of using accuracy_score
accuracy = accuracy_score(y_true, y_pred)
print(f'Accuracy: {accuracy}')

# Example of using classification_report
report = classification_report(y_true, y_pred)
print('Classification Report:\n', report)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# If y_train is one-hot encoded
if len(y_train.shape) > 1:
    y_true = np.argmax(y_train, axis=1)
else:
    y_true = y_train

# Assuming y_train is one-hot encoded, and you want to compare it with predicted labels
y_pred = np.argmax(model.predict(X_train), axis=1)

# Calculate the confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Display the confusion matrix
classes = ["spoof", "bonafide"]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

model.predict(X_train)>0.5#.shape

X_train

y_train.shape

# CONFUSION MATRIX

#y_true = pd.DataFrame(y_train).apply(np.argmax, axis=1)
#y_pred = np.argmax(model.predict(X_train), axis=1)

cm = confusion_matrix(y_train, model.predict(X_train)>0.5)
#cm = confusion_matrix(pd.DataFrame(y_train).apply(np.argmax, axis = 1), model.predict(X_train))

# Display the confusion matrix
classes = ["spoof", "bonafide"]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

# CONFUSION MATRIX

cm = confusion_matrix(y_true, y_pred_classes)

# Display the confusion matrix
classes = ["spoof", "bonafide"]
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

y_true.shape

y_pred_classes.shape

model.predict(X_train)

#احس ماله لزمه

# ROC Curve

from sklearn.metrics import roc_curve, auc

# Predict using the loaded model
y_pred = model.predict(X_test)
print(y_pred)
# Get the predicted probabilities for the positive class
y_pred_prob = y_pred[:, 1]

# Compute ROC curve and AUC
fpr, tpr, _ = roc_curve(y_true, y_pred_prob)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

# Precision-Recall Curve
from sklearn.metrics import precision_recall_curve, average_precision_score

#احس ماله لزمه

# Compute precision-recall curve and average precision score
precision, recall, _ = precision_recall_curve(y_true, y_pred_prob)
avg_precision = average_precision_score(y_true, y_pred_prob)

# Plot precision-recall curve
plt.figure()
plt.plot(recall, precision, color='darkorange', lw=2, label='Avg. Precision = %0.2f' % avg_precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()

# Calibration Curve
from sklearn.calibration import calibration_curve

#احس ماله لزمه
# Compute calibration curve
prob_true, prob_pred = calibration_curve(y_true, y_pred_prob, n_bins=10)

# Plot calibration curve
plt.figure()
plt.plot(prob_pred, prob_true, marker='o', label='Calibration curve', color='darkorange')
plt.plot([0, 1], [0, 1], linestyle='--', color='navy', label='Perfectly calibrated')
plt.xlabel('Mean Predicted Probability')
plt.ylabel('Fraction of Positives')
plt.title('Calibration Curve')
plt.legend(loc="lower right")
plt.show()

# Plot bar chart of class distribution

import seaborn as sns
import matplotlib.pyplot as plt


LABELS = ['spoof', 'bonafide']

plt.figure(figsize=(6, 4))
sns.countplot(x=y_true, palette="Set2")
plt.xticks(ticks=[0, 1], labels=LABELS)
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution')
plt.show()

'''
# Visualising Mel Spectrogram

import os
import librosa.display

# Folder containing .flac audio files
folder_path = r"C:\mine\SDAIA T5\CAPSTONE\LA\LA\ASVspoof2019_LA_eval\flac"
#folder_path = "TestEvaluation"

# Get a list of all .flac files in the folder
flac_files = [file for file in os.listdir(folder_path) if file.endswith(".flac")]

# Define the hop length
HOP_LENGTH = 512  # Adjust this value based on your needs

# Loop through each .flac file and visualize its Mel spectrogram
for flac_file in flac_files:
    audio_file_path = os.path.join(folder_path, flac_file)

    # Load the audio file using librosa
    audio, _ = librosa.load(audio_file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Calculate the Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Plot the Mel spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(mel_spectrogram, x_axis='time', y_axis='mel', sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel Spectrogram - {flac_file}')
    plt.show()
'''

import os
import librosa.display
import matplotlib.pyplot as plt

# Folder containing .flac audio files
folder_path = r"C:\mine\SDAIA T5\CAPSTONE\LA\LA\ASVspoof2019_LA_eval\flac"

# Get a list of all .flac files in the folder
flac_files = [file for file in os.listdir(folder_path) if file.endswith(".flac")]

# Define the hop length
HOP_LENGTH = 512  # Adjust this value based on your needs

# Limit the number of samples to 20
num_samples = 20

# Loop through each .flac file and visualize its Mel spectrogram
for i, flac_file in enumerate(flac_files):
    if i >= num_samples:
        break  # Stop iterating after 20 samples

    audio_file_path = os.path.join(folder_path, flac_file)

    # Load the audio file using librosa
    audio, _ = librosa.load(audio_file_path, sr=SAMPLE_RATE, duration=DURATION)

    # Calculate the Mel spectrogram using librosa
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=N_MELS)
    mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Plot the Mel spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(mel_spectrogram, x_axis='time', y_axis='mel', sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel Spectrogram - {flac_file}')
    plt.show()

mod = tf.keras.saving.load_model("/content/drive/MyDrive/iit-guwahati/audio_classifier.h5")
plot_model(mod, to_file='model_architecture.png', show_shapes=True, show_layer_names=True)

