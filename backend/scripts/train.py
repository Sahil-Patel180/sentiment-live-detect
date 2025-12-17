import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

#Load JSON Data
def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    sentences = [entry['sentence'] for entry in data]
    emotion_labels = [entry['emotion'] for entry in data]
    return sentences, emotion_labels

#Preprocessing the text
def preprocess_data(sentences, emotion_labels, max_len=100):
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(sentences)
    sequences = tokenizer.texts_to_sequences(sentences)
    X = pad_sequences(sequences, maxlen=max_len)
    
    lb = LabelBinarizer()
    y = lb.fit_transform(emotion_labels)
    
    return X, y, tokenizer, lb

#Create the Deep Learning Model
def create_model(input_dim, embedding_dim=128, lstm_units=128, output_dim=6):
    model = Sequential([
        Embedding(input_dim, embedding_dim, input_length=100),
        LSTM(lstm_units, dropout=0.3, recurrent_dropout=0.3),
        Dropout(0.5),
        Dense(output_dim, activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#Train the Model
def train_and_evaluate_model(json_file):
    sentences, emotion_labels = load_json_data(json_file)
    X, y, tokenizer, lb = preprocess_data(sentences, emotion_labels)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    num_classes = y.shape[1]
    model = create_model(5000, output_dim=num_classes)
    model.fit(X_train, y_train, epochs=20, batch_size=1024, validation_data=(X_test, y_test))
    
    accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy[1] * 100:.2f}%")
    
    # Save model, tokenizer, and label binarizer
    model.save('emotion_model.keras')
    
    import pickle
    with open('tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    with open('label_binarizer.pkl', 'wb') as f:
        pickle.dump(lb, f)
    
    print(f"Emotion classes: {lb.classes_}")
    return model, tokenizer, lb

#Example usage
if __name__ == "__main__":
    model, tokenizer, lb = train_and_evaluate_model('combined_emotion.json')