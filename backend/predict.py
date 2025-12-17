from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

#Load the trained model
model = load_model('emotion_model.keras')

#Load the tokenizer and label binarizer
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
with open('label_binarizer.pkl', 'rb') as f:
    lb = pickle.load(f)

#Sample input text for emotion analysis
input_text = "this ceo will send your kids to school, if you work for his company."

#Define parameters based on how the model was trained
max_sequence_length = 100

#Convert the input text to a sequence
input_sequence = tokenizer.texts_to_sequences([input_text])

#Pad the sequence to the same length used during training
input_padded = pad_sequences(input_sequence, maxlen=max_sequence_length)

#Make a prediction (output is a probability distribution over emotions)
predictions = model.predict(input_padded)

#Get the predicted emotion class
predicted_class_idx = np.argmax(predictions, axis=1)[0]
predicted_emotion = lb.classes_[predicted_class_idx]
confidence = predictions[0][predicted_class_idx] * 100

print(f"Input text: {input_text}")
print(f"Predicted emotion: {predicted_emotion}")
print(f"Confidence: {confidence:.2f}%")
print(f"\nAll emotion probabilities:")
for emotion, prob in zip(lb.classes_, predictions[0]):
    print(f"  {emotion}: {prob*100:.2f}%")