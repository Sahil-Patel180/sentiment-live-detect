# 🚀 Render Free Tier Optimizations

This document outlines the optimizations made to ensure the application runs efficiently on Render's free tier (512MB RAM limit).

## Key Optimizations

### 1. **TensorFlow CPU Version** ✅
- Switched from `tensorflow` to `tensorflow-cpu` in `requirements.txt`
- Reduces memory footprint by ~200-300MB by excluding GPU dependencies
- Critical for free tier deployments

### 2. **TensorFlow Memory Configuration** ✅
- Disabled GPU usage explicitly (`tf.config.set_visible_devices([], 'GPU')`)
- Set memory growth for GPUs (if present)
- Limited TensorFlow thread usage to prevent excessive memory allocation
- Suppressed TensorFlow logging to reduce overhead

### 3. **Gunicorn Configuration** ✅
- Reduced workers to 1 (free tier can't handle multiple workers)
- Added 2 threads per worker using `gthread` worker class
- Increased timeout to 120 seconds to handle model loading
- Updated both `Procfile` and `render.yaml`

### 4. **Model Loading Optimizations** ✅
- Load model with `compile=False` (not needed for inference)
- Added garbage collection before and after model loading
- Error handling with proper exception raising

### 5. **Prediction Optimizations** ✅
- Use `batch_size=1` for predictions to minimize memory usage
- Set `verbose=0` to suppress unnecessary output
- Added input length validation (max 500 words) to prevent memory issues

### 6. **Environment Variables** ✅
- Added `TF_CPP_MIN_LOG_LEVEL=2` to suppress TensorFlow warnings
- Added `PYTHONUNBUFFERED=1` for better logging in Render

## Memory Breakdown (Estimated)

- **TensorFlow CPU**: ~150-200MB
- **Model (LSTM)**: ~50-100MB
- **Flask/Gunicorn**: ~50-100MB
- **System/Python**: ~100-150MB
- **Total**: ~350-550MB (fits within 512MB free tier)

## Deployment Notes

1. The application should now run comfortably on Render's free tier
2. Cold starts may take 30-60 seconds due to model loading
3. Health check endpoint at `/health` helps Render monitor the service
4. Single worker with threads handles concurrent requests efficiently

## Performance Tips

- Monitor memory usage in Render dashboard
- If memory issues persist, consider:
  - Converting model to TensorFlow Lite (more complex)
  - Further reducing model complexity
  - Using model quantization

