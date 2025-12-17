# Install backend dependencies
pip install -r requirements.txt

# Navigate to frontend and install dependencies
cd frontend
npm install

# Start backend (in one terminal)
python app.py

# Start frontend (in another terminal)
cd frontend
npm start
