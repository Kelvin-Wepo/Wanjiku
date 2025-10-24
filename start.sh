#!/bin/bash

# Wanjiku 2.0 Startup Script

echo "🚀 Starting Wanjiku 2.0 - Swahili Government Services Assistant"
echo "================================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file..."
    cp env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Load initial data
echo "📊 Loading initial data..."
python manage.py load_initial_data

# Create superuser if it doesn't exist
echo "👤 Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@wanjiku.ai', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start Django server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Start React frontend
echo "⚛️ Starting React frontend..."
cd frontend
npm install
npm start &
REACT_PID=$!

echo ""
echo "🎉 Wanjiku 2.0 is starting up!"
echo "================================================================"
echo "🌐 Backend API: http://localhost:8000"
echo "⚛️ Frontend: http://localhost:3000"
echo "👤 Admin Panel: http://localhost:8000/admin (admin/admin123)"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait

# Cleanup on exit
echo "🛑 Stopping services..."
kill $DJANGO_PID 2>/dev/null
kill $REACT_PID 2>/dev/null
echo "✅ All services stopped"

