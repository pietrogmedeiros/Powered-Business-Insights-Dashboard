# AI-Powered Business Insights Dashboard - No Docker Setup

Este guia explica como executar o projeto sem Docker, usando instalações locais do Python e Node.js.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm** (vem com Node.js)

### Verificar instalações:
```bash
python3 --version
node --version
npm --version
```

## 🚀 Início Rápido

### Opção 1: Script Automático
```bash
./start.sh
```

Este script irá:
- Verificar dependências
- Criar ambiente virtual Python
- Instalar dependências do backend e frontend
- Iniciar ambos os serviços

### Opção 2: Script de Desenvolvimento (Recomendado)
```bash
./dev.sh
```

Este script oferece um menu interativo com opções para:
1. Setup do ambiente
2. Iniciar apenas backend
3. Iniciar apenas frontend
4. Iniciar aplicação completa
5. Executar testes
6. Build de produção
7. Limpar ambiente

## 🛠️ Setup Manual

### Backend (FastAPI)

1. **Navegar para o diretório do backend:**
```bash
cd backend
```

2. **Criar ambiente virtual:**
```bash
python3 -m venv venv
```

3. **Ativar ambiente virtual:**
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

5. **Executar o servidor:**
```bash
python -m app.main
```

O backend estará disponível em: http://localhost:8000

### Frontend (React)

1. **Navegar para o diretório do frontend:**
```bash
cd frontend
```

2. **Instalar dependências:**
```bash
npm install
```

3. **Executar o servidor de desenvolvimento:**
```bash
npm start
```

O frontend estará disponível em: http://localhost:3000

## 🌐 URLs de Acesso

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentação da API:** http://localhost:8000/docs
- **API Alternativa (ReDoc):** http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
ai-business-insights/
├── backend/
│   ├── app/
│   │   ├── main.py          # Aplicação FastAPI principal
│   │   ├── api/             # Rotas da API
│   │   ├── models/          # Modelos de dados
│   │   ├── services/        # Lógica de negócio
│   │   └── utils/           # Utilitários
│   ├── venv/                # Ambiente virtual Python
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── src/                 # Código fonte React
│   ├── public/              # Arquivos públicos
│   ├── node_modules/        # Dependências Node.js
│   └── package.json         # Configuração do projeto
├── start.sh                 # Script de início automático
├── dev.sh                   # Script de desenvolvimento
└── README_NO_DOCKER.md     # Este arquivo
```

## 🔧 Comandos Úteis

### Backend
```bash
# Ativar ambiente virtual
cd backend && source venv/bin/activate

# Instalar nova dependência
pip install nome-do-pacote

# Atualizar requirements.txt
pip freeze > requirements.txt

# Executar com reload automático (desenvolvimento)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Instalar nova dependência
cd frontend && npm install nome-do-pacote

# Build para produção
npm run build

# Executar testes
npm test

# Analisar bundle
npm run build && npx serve -s build
```

## 🐛 Solução de Problemas

### Erro de porta em uso
Se as portas 3000 ou 8000 estiverem em uso:

```bash
# Encontrar processo usando a porta
lsof -i :3000
lsof -i :8000

# Matar processo
kill -9 PID
```

### Problemas com ambiente virtual Python
```bash
# Remover e recriar ambiente virtual
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problemas com dependências Node.js
```bash
# Limpar cache e reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 Desenvolvimento

Para desenvolvimento ativo, recomenda-se:

1. **Backend:** Use `uvicorn app.main:app --reload` para reload automático
2. **Frontend:** Use `npm start` que já inclui hot reload
3. **Use o script `dev.sh`** para facilitar o gerenciamento

## 🔄 Atualizações

Para atualizar dependências:

```bash
# Backend
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

---

**Nota:** Este setup substitui completamente o Docker, permitindo desenvolvimento local mais rápido e flexível.
