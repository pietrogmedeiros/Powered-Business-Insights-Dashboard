#!/bin/bash

echo "🚀 Starting AI Business Insights Dashboard (without Docker)..."

# Criar diretórios necessários
mkdir -p backend/app/models backend/app/services backend/app/api
mkdir -p frontend/src/components frontend/src/services frontend/public

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências
echo "🔍 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ All dependencies found!"

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências Python
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Voltar para o diretório raiz
cd ..

# Setup Frontend
echo "⚛️ Setting up React frontend..."
cd frontend

# Instalar dependências Node.js
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Voltar para o diretório raiz
cd ..

# Iniciar os serviços
echo "🚀 Starting services..."

# Função para cleanup quando o script for interrompido
cleanup() {
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar backend em background
echo "Starting backend server..."
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!
cd ..

# Aguardar um pouco para o backend iniciar
sleep 3

# Iniciar frontend em background
echo "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Dashboard disponível em:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Aguardar indefinidamente
wait