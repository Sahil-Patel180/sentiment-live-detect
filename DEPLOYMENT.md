# 🎭 Emotion Analysis Web Application

A full-stack web application that uses Deep Learning to analyze emotions in text. Built with React frontend and Flask backend, designed for easy deployment on Render.

## 🌟 Features

- **Real-time Emotion Analysis**: Analyzes text and predicts emotions (joy, sadness, anger, fear, love, surprise)
- **Beautiful UI**: Modern, responsive React interface with gradient backgrounds and smooth animations
- **Confidence Scores**: Shows prediction confidence with visual progress bars
- **All Emotion Probabilities**: Displays probability scores for all emotions
- **Render-Ready**: Configured for easy deployment on Render

## 🚀 Project Structure

```
.
├── app.py                      # Flask backend API
├── train.py                    # Model training script
├── predict.py                  # Standalone prediction script
├── emotion_model.keras         # Trained model (generated)
├── tokenizer.pkl               # Tokenizer (generated)
├── label_binarizer.pkl         # Label encoder (generated)
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version
└── frontend/                   # React application
    ├── public/
    ├── src/
    │   ├── App.js              # Main React component
    │   ├── App.css             # Styling
    │   ├── index.js            # Entry point
    │   └── index.css           # Global styles
    └── package.json            # Node dependencies
```

## 📋 Prerequisites

### Backend
- Python 3.10+
- pip

### Frontend
- Node.js 16+
- npm or yarn

## 🛠️ Local Development Setup

### 1. Train the Model (if not already trained)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the model
python train.py
```

This will generate:
- `emotion_model.keras`
- `tokenizer.pkl`
- `label_binarizer.pkl`

### 2. Run the Backend

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run Flask server
python app.py
```

Backend will run on `http://localhost:5000`

### 3. Run the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

## 🌐 Deployment on Render

### Backend Deployment

1. **Create a New Web Service** on Render
2. **Connect your repository**
3. **Configure the service**:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.10.12 (from runtime.txt)

4. **Upload Model Files**:
   - Ensure `emotion_model.keras`, `tokenizer.pkl`, and `label_binarizer.pkl` are in your repository
   - Or upload them manually through Render's file system

5. **Deploy**: Click "Create Web Service"

### Frontend Deployment

#### Option 1: Static Site on Render

1. **Build the React app locally**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Create a New Static Site** on Render
3. **Configure**:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`

4. **Environment Variables**:
   - Add `REACT_APP_API_URL` with your backend URL (e.g., `https://your-backend.onrender.com`)

#### Option 2: Deploy Frontend Separately

You can also deploy the frontend to:
- Vercel
- Netlify
- GitHub Pages

Just remember to set the `REACT_APP_API_URL` environment variable to your backend URL.

## 🔧 Configuration

### Backend Environment Variables (Optional)

- `PORT`: Server port (default: 5000)

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

For production, update this to your deployed backend URL.

## 📝 API Endpoints

### `GET /`
Health check and API info

### `GET /health`
Check if model is loaded

### `POST /predict`
Predict emotion from text

**Request Body**:
```json
{
  "text": "I'm so excited about this new opportunity!"
}
```

**Response**:
```json
{
  "input_text": "I'm so excited about this new opportunity!",
  "predicted_emotion": "joy",
  "confidence": 95.67,
  "all_emotions": [
    {"emotion": "joy", "probability": 95.67},
    {"emotion": "surprise", "probability": 2.34},
    ...
  ]
}
```

## 🎨 Customization

### Add More Emotions

1. Update the emotion classes in your training data
2. Retrain the model with `python train.py`
3. Update the `emotionEmojis` and `emotionColors` in [frontend/src/App.js](frontend/src/App.js)

### Change UI Colors

Edit [frontend/src/App.css](frontend/src/App.css) and [frontend/src/index.css](frontend/src/index.css)

## 🧪 Testing

### Test Backend Locally

```bash
# Using curl
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!"}'
```

### Test Frontend

1. Start both backend and frontend
2. Navigate to `http://localhost:3000`
3. Enter text and click "Analyze Emotion"

## 📊 Model Information

- **Architecture**: LSTM-based neural network
- **Input**: Text sequences (max length: 100)
- **Output**: 6 emotion classes
- **Training**: 20 epochs with validation split

## 🐛 Troubleshooting

### CORS Issues
If you encounter CORS errors:
- Ensure `flask-cors` is installed
- Check that the frontend is using the correct API URL

### Model Not Loading
- Verify all three files exist: `emotion_model.keras`, `tokenizer.pkl`, `label_binarizer.pkl`
- Check file permissions
- Review backend logs

### Frontend Build Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Made with ❤️ using React, Flask, and TensorFlow**
