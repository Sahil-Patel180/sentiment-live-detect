from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import os

app = Flask(__name__)

# Configure CORS to allow requests from your frontend
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://emotion-analyzer-frontend.onrender.com",
            "http://localhost:3000",
            "http://localhost:3001"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Load the trained model and preprocessing tools
model = None
tokenizer = None
lb = None

def load_ml_model():
    global model, tokenizer, lb
    try:
        model = load_model('models/emotion_model.keras')
        with open('models/tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        with open('models/label_binarizer.pkl', 'rb') as f:
            lb = pickle.load(f)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")

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

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        print(f"Received request from: {request.origin}")
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        input_text = data['text']
        
        if not input_text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Check if model is loaded
        if model is None or tokenizer is None or lb is None:
            return jsonify({"error": "Model not loaded"}), 503
        
        # Preprocess the input
        max_sequence_length = 100
        input_sequence = tokenizer.texts_to_sequences([input_text])
        input_padded = pad_sequences(input_sequence, maxlen=max_sequence_length)
        
        # Make prediction
        predictions = model.predict(input_padded, verbose=0)
        
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
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
