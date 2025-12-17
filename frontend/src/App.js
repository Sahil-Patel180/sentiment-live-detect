import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const MAX_CHARS = 2400;

  const emotionEmojis = {
    'joy': '😊',
    'sadness': '😢',
    'anger': '😠',
    'fear': '😨',
    'love': '❤️',
    'surprise': '😮'
  };

  const emotionColors = {
    'joy': '#FFD700',
    'sadness': '#4682B4',
    'anger': '#DC143C',
    'fear': '#8B008B',
    'love': '#FF1493',
    'surprise': '#FF8C00'
  };

  const emotionLabels = {
    'joy': 'Joyful',
    'sadness': 'Sad',
    'anger': 'Angry',
    'fear': 'Fearful',
    'love': 'Loving',
    'surprise': 'Surprised'
  };

  const exampleTexts = [
    "I really don't know what to do about the situation, it feels overwhelming...",
    "Wow! That is absolutely fantastic news, I can't wait to see it!",
    "This is completely unacceptable service, I want a refund now!",
    "I'm so grateful for all the support, you've made my day!",
    "I'm worried about what might happen next, this is concerning."
  ];

  useEffect(() => {
    const stored = localStorage.getItem('recentAnalyses');
    if (stored) {
      setRecentAnalyses(JSON.parse(stored));
    }
  }, []);

  const saveToRecent = (analysis) => {
    const newAnalysis = {
      text: analysis.input_text,
      emotion: analysis.predicted_emotion,
      timestamp: new Date().toISOString()
    };
    const updated = [newAnalysis, ...recentAnalyses.slice(0, 4)];
    setRecentAnalyses(updated);
    localStorage.setItem('recentAnalyses', JSON.stringify(updated));
  };

  const getTimeAgo = (timestamp) => {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, {
        text: inputText
      });
      
      setResult(response.data);
      saveToRecent(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setResult(null);
    setError('');
  };

  const handleRandomExample = () => {
    const randomText = exampleTexts[Math.floor(Math.random() * exampleTexts.length)];
    setInputText(randomText);
    setResult(null);
    setError('');
  };

  const getTopEmotions = () => {
    if (!result || !result.all_emotions) return [];
    return result.all_emotions.slice(1, 4);
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">e</div>
            <span className="logo-text">EmotionAnalyzer</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="hero-section">
          <div className="ai-badge">⚡ AI POWERED V2.0</div>
          <h1 className="main-title">
            Decode the <span className="highlight">emotion</span><br />
            behind your words.
          </h1>
          <p className="subtitle">
            Input any text to instantly reveal the underlying sentiment and confidence score<br />
            using our advanced NLP models.
          </p>
        </div>

        <div className="analysis-container">
          {/* Input Section */}
          <div className="input-section">
            <div className="section-header">
              <h3>INPUT TEXT</h3>
              <span className="char-count">{inputText.length}/{MAX_CHARS} chars</span>
            </div>
            
            <form onSubmit={handleSubmit}>
              <textarea
                className="text-input"
                value={inputText}
                onChange={(e) => setInputText(e.target.value.slice(0, MAX_CHARS))}
                placeholder="Type how you are feeling right now, or paste a conversation to analyze the tone..."
                rows="8"
                disabled={loading}
                maxLength={MAX_CHARS}
              />

              <div className="button-group">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={handleClear}
                  disabled={loading}
                >
                  Clear
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={handleRandomExample}
                  disabled={loading}
                >
                  Random Example
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={loading || !inputText.trim()}
                >
                  {loading ? 'Analyzing...' : 'Analyze Text'} →
                </button>
              </div>
            </form>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="results-section">
            <div className="section-header">
              <h3>Analysis Result</h3>
              {result && <span className="status-badge">PROCESSED</span>}
            </div>

            {!result && !loading && (
              <div className="empty-state">
                <div className="empty-icon">📊</div>
                <p>Enter text and click "Analyze Text" to see results</p>
              </div>
            )}

            {loading && (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Analyzing your text...</p>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div className="main-emotion">
                  <div className="emotion-icon-large">
                    {emotionEmojis[result.predicted_emotion] || '😐'}
                  </div>
                  <h2 className="emotion-label">
                    {emotionLabels[result.predicted_emotion] || result.predicted_emotion}
                  </h2>
                  <p className="emotion-subtitle">Primary emotion detected</p>
                </div>

                <div className="confidence-section">
                  <div className="confidence-header">
                    <span className="confidence-label">Confidence Score</span>
                    <span className="confidence-value">{Math.round(result.confidence)}%</span>
                  </div>
                  <div className="confidence-bar-container">
                    <div 
                      className="confidence-bar" 
                      style={{ width: `${result.confidence}%` }}
                    ></div>
                  </div>
                  <p className="confidence-note">Based on keyword intensity and patterns structure.</p>
                </div>

                {getTopEmotions().length > 0 && (
                  <div className="other-emotions">
                    {getTopEmotions().map((emotion, idx) => (
                      <div key={idx} className="mini-emotion">
                        <span className="mini-emotion-name">
                          {emotionLabels[emotion.emotion] || emotion.emotion.charAt(0).toUpperCase() + emotion.emotion.slice(1)}
                        </span>
                        <span className="mini-emotion-value">{Math.round(emotion.probability)}%</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Recent Analysis */}
        {recentAnalyses.length > 0 && (
          <div className="recent-analysis">
            <h3>Recent Analysis</h3>
            <div className="recent-grid">
              {recentAnalyses.map((analysis, idx) => (
                <div key={idx} className="recent-card">
                  <div className="recent-header">
                    <span className={`emotion-badge emotion-${analysis.emotion}`}>
                      {analysis.emotion.toUpperCase()}
                    </span>
                    <span className="recent-time">{getTimeAgo(analysis.timestamp)}</span>
                  </div>
                  <p className="recent-text">"{analysis.text.slice(0, 80)}{analysis.text.length > 80 ? '...' : ''}"</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>© 2023 Emotion Analyzer AI. All rights reserved</p>
      </footer>
    </div>
  );
}

export default App;
