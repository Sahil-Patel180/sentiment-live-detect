@echo off
echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo Installing frontend dependencies...
cd frontend
call npm install

echo.
echo Setup complete!
echo.
echo To start the application:
echo 1. In terminal 1: python app.py
echo 2. In terminal 2: cd frontend && npm start
echo.
pause
