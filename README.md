# 🎭 Emotion Analysis Web Application

A full-stack web application that uses Deep Learning to analyze emotions in text. Built with React frontend and Flask backend, designed for easy deployment on Render.

## 📁 Project Structure

```
project-root/
│
├── frontend/                    # React application
│   ├── public/
│   ├── src/
│   │   ├── App.js              # Main component
│   │   ├── App.css             # Styling
│   │   └── index.js
│   ├── package.json
│   └── .env                    # Local development config
│
├── backend/                     # Flask API
│   ├── app.py                  # Main API server
│   ├── predict.py              # Prediction utilities
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Render deployment config
│   ├── runtime.txt             # Python version
│   │
│   ├── models/                 # ML model files
│   │   ├── emotion_model.keras
│   │   ├── tokenizer.pkl
│   │   └── label_binarizer.pkl
│   │
│   └── scripts/                # Training & data processing
│       ├── train.py
│       ├── csv_json.py
│       └── combined_emotion.csv
│
├── render.yaml                 # Render Infrastructure as Code (optional)
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Local Development

**1. Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`

**2. Frontend Setup:**
```bash
cd frontend
npm install
npm start
```
Frontend runs on `http://localhost:3000`

### Mobile Testing (Same WiFi)

**1. Find your computer's IP:**
```bash
ipconfig | findstr /i "IPv4"  # Windows
ifconfig | grep "inet "        # Mac/Linux
```

**2. Update frontend/.env:**
```env
REACT_APP_API_URL=http://YOUR_IP:5000
```

**3. Access on phone:** `http://YOUR_IP:3000`

## 🌐 Render Deployment

### Option 1: Using render.yaml (Recommended)

1. Push code to GitHub
2. Connect repository to Render
3. Render auto-detects `render.yaml` and deploys both services
4. Done! ✨

### Option 2: Manual Deployment

**Backend:**
1. Create new **Web Service**
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Upload model files to `backend/models/`

**Frontend:**
1. Create new **Static Site**
2. Build Command: `cd frontend && npm install && npm run build`
3. Publish Directory: `frontend/build`
4. Environment Variable:
   - `REACT_APP_API_URL` = Your backend URL

## ✨ Features

- Real-time emotion analysis (joy, sadness, anger, fear, love, surprise)
- Beautiful responsive UI
- Confidence scores with visual indicators
- Recent analysis history
- Mobile-friendly design

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Axios for API calls
- CSS3 with modern design

**Backend:**
- Flask + Flask-CORS
- TensorFlow/Keras
- Gunicorn (production server)

**ML Model:**
- LSTM neural network
- 6 emotion classes
- 100 max sequence length

## 📊 API Endpoints

### `GET /`
API information

### `GET /health`
Health check

### `POST /predict`
Predict emotion from text

**Request:**
```json
{
  "text": "I'm so happy today!"
}
```

**Response:**
```json
{
  "input_text": "I'm so happy today!",
  "predicted_emotion": "joy",
  "confidence": 95.67,
  "all_emotions": [
    {"emotion": "joy", "probability": 95.67},
    {"emotion": "love", "probability": 2.34}
  ]
}
```

## 🔧 Environment Variables

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:5000  # or your backend URL
```

**Backend:**
```env
PORT=5000  # Set by Render automatically
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

---

**Made with ❤️ using React, Flask, and TensorFlow**
