@echo off
echo 🚀 Starting Wanjiku 2.0 - Swahili Government Services Assistant
echo ================================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️ Creating environment file...
    copy env.example .env
    echo 📝 Please edit .env file with your configuration
)

REM Run database migrations
echo 🗄️ Running database migrations...
python manage.py migrate

REM Load initial data
echo 📊 Loading initial data...
python manage.py load_initial_data

REM Create superuser if it doesn't exist
echo 👤 Creating superuser (if needed)...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@wanjiku.ai', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')"

REM Start Django server
echo 🌐 Starting Django server...
start "Django Server" cmd /k "python manage.py runserver 0.0.0.0:8000"

REM Wait a moment for Django to start
timeout /t 3 /nobreak > nul

REM Start React frontend
echo ⚛️ Starting React frontend...
cd frontend
call npm install
start "React Frontend" cmd /k "npm start"

echo.
echo 🎉 Wanjiku 2.0 is starting up!
echo ================================================================
echo 🌐 Backend API: http://localhost:8000
echo ⚛️ Frontend: http://localhost:3000
echo 👤 Admin Panel: http://localhost:8000/admin (admin/admin123)
echo.
echo Press any key to continue...
pause > nul

