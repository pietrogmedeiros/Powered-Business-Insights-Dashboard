#!/bin/bash

echo "🛠️ AI Business Insights Dashboard - Development Mode"

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Menu de opções
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1) Setup environment (install dependencies)"
    echo "2) Start backend only"
    echo "3) Start frontend only"
    echo "4) Start both (full application)"
    echo "5) Run backend tests"
    echo "6) Build frontend for production"
    echo "7) Clean environment (remove node_modules and venv)"
    echo "8) Exit"
    echo ""
}

# Setup do ambiente
setup_environment() {
    echo "🔧 Setting up development environment..."
    
    # Backend setup
    echo "Setting up Python backend..."
    cd backend
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # Frontend setup
    echo "Setting up React frontend..."
    cd frontend
    npm install
    cd ..
    
    echo "✅ Environment setup complete!"
}

# Iniciar apenas o backend
start_backend() {
    echo "🐍 Starting backend server..."
    cd backend
    source venv/bin/activate
    python -m app.main
}

# Iniciar apenas o frontend
start_frontend() {
    echo "⚛️ Starting frontend server..."
    cd frontend
    npm start
}

# Iniciar ambos
start_both() {
    echo "🚀 Starting both backend and frontend..."
    
    # Função para cleanup
    cleanup() {
        echo "🛑 Stopping services..."
        kill $BACKEND_PID 2>/dev/null
        kill $FRONTEND_PID 2>/dev/null
        exit 0
    }
    
    trap cleanup SIGINT SIGTERM
    
    # Iniciar backend
    cd backend
    source venv/bin/activate
    python -m app.main &
    BACKEND_PID=$!
    cd ..
    
    sleep 3
    
    # Iniciar frontend
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "✅ Services running:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    wait
}

# Executar testes do backend
run_tests() {
    echo "🧪 Running backend tests..."
    cd backend
    source venv/bin/activate
    # Adicionar comando de teste quando implementado
    echo "Tests not implemented yet"
    cd ..
}

# Build do frontend
build_frontend() {
    echo "📦 Building frontend for production..."
    cd frontend
    npm run build
    echo "✅ Frontend built successfully!"
    echo "Build files are in frontend/build/"
    cd ..
}

# Limpar ambiente
clean_environment() {
    echo "🧹 Cleaning development environment..."
    read -p "Are you sure? This will remove node_modules and venv (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf backend/venv
        rm -rf frontend/node_modules
        echo "✅ Environment cleaned!"
    else
        echo "Cancelled."
    fi
}

# Loop principal
while true; do
    show_menu
    read -p "Enter your choice (1-8): " choice
    
    case $choice in
        1)
            setup_environment
            ;;
        2)
            start_backend
            ;;
        3)
            start_frontend
            ;;
        4)
            start_both
            ;;
        5)
            run_tests
            ;;
        6)
            build_frontend
            ;;
        7)
            clean_environment
            ;;
        8)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 1-8."
            ;;
    esac
done
