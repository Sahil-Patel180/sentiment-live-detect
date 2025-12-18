from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import os
import gc

# Configure TensorFlow for memory efficiency (critical for Render free tier)
tf.config.set_visible_devices([], 'GPU')  # Disable GPU to save memory
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

# Limit TensorFlow memory growth to prevent OOM errors
try:
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except RuntimeError as e:
    print(f"GPU configuration error: {e}")

# Set TensorFlow to use only necessary threads
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load the trained model and preprocessing tools
model = None
tokenizer = None
lb = None

def load_ml_model():
    global model, tokenizer, lb
    try:
        # Force garbage collection before loading
        gc.collect()
        
        # Load model with minimal memory allocation (no compilation needed for inference)
        model = load_model('models/emotion_model.keras', compile=False)
        
        with open('models/tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        with open('models/label_binarizer.pkl', 'rb') as f:
            lb = pickle.load(f)
        
        print("Model loaded successfully!")
        print(f"Model memory optimized for Render free tier")
        
        # Clear any unused memory
        gc.collect()
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

# Load model on startup
load_ml_model()

@app.route('/')
def home():
    return jsonify({
        "message": "Emotion Analysis API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Predict emotion from text",
            "/health": "GET - Health check"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        input_text = data['text']
        
        if not input_text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Limit input length to prevent memory issues (max 500 words)
        words = input_text.split()
        if len(words) > 500:
            return jsonify({"error": "Text too long. Maximum 500 words allowed."}), 400
        
        # Preprocess the input
        max_sequence_length = 100
        input_sequence = tokenizer.texts_to_sequences([input_text])
        input_padded = pad_sequences(input_sequence, maxlen=max_sequence_length)
        
        # Make prediction with minimal memory usage
        # Use batch_size=1 and verbose=0 to minimize memory footprint
        predictions = model.predict(input_padded, batch_size=1, verbose=0)
        
        # Get the predicted emotion
        predicted_class_idx = np.argmax(predictions, axis=1)[0]
        predicted_emotion = lb.classes_[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx] * 100)
        
        # Get all emotion probabilities
        all_emotions = []
        for emotion, prob in zip(lb.classes_, predictions[0]):
            all_emotions.append({
                "emotion": emotion,
                "probability": float(prob * 100)
            })
        
        # Sort by probability
        all_emotions.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            "input_text": input_text,
            "predicted_emotion": predicted_emotion,
            "confidence": round(confidence, 2),
            "all_emotions": all_emotions
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
