# 🚀 AI-Powered Business Insights Dashboard

<div align="center">

![Dashboard Preview](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18+-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

*Um dashboard inteligente para análise de negócios com IA integrada*

[🎯 Demo](#demo) • [🚀 Instalação](#instalação) • [📖 Documentação](#documentação) • [🤝 Contribuição](#contribuição)

</div>

---

## 📋 Sobre o Projeto

O **AI-Powered Business Insights Dashboard** é uma aplicação completa que combina análise de dados avançada com inteligência artificial para fornecer insights valiosos sobre seu negócio. Desenvolvido com FastAPI no backend e React no frontend, oferece uma experiência moderna e intuitiva para análise de dados empresariais.

### ✨ Principais Funcionalidades

- 📊 **Dashboard Interativo** - Visualização em tempo real de métricas de negócio
- 🔮 **Previsão de Vendas** - Algoritmos de ML para forecasting de vendas
- 👥 **Segmentação de Clientes** - Análise inteligente de perfis de clientes
- 💬 **Análise de Sentimentos** - Processamento de feedback e reviews
- ⚠️ **Predição de Churn** - Identificação de clientes em risco
- 📈 **Relatórios Automatizados** - Geração de insights automáticos

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem principal
- **Pandas & NumPy** - Manipulação e análise de dados
- **Uvicorn** - Servidor ASGI de alta performance

### Frontend
- **React 18** - Biblioteca para interfaces de usuário
- **Ant Design** - Componentes UI elegantes
- **Chart.js** - Visualizações interativas
- **Axios** - Cliente HTTP para APIs

### Ferramentas de Desenvolvimento
- **Docker** - Containerização (opcional)
- **Git** - Controle de versão
- **ESLint** - Linting para JavaScript
- **Prettier** - Formatação de código

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **npm** ou **yarn** - Gerenciador de pacotes

### 🎯 Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/pietrogmedeiros/Powered-Business-Insights-Dashboard.git
cd Powered-Business-Insights-Dashboard

# Execute o script de desenvolvimento
chmod +x dev.sh
./dev.sh
```

### 📋 Instalação Manual

#### Backend (FastAPI)

```bash
# Navegue para o diretório do backend
cd backend

# Crie um ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
python -m app.main
```

#### Frontend (React)

```bash
# Navegue para o diretório do frontend
cd frontend

# Instale as dependências
npm install

# Execute o servidor de desenvolvimento
npm start
```

## 🎮 Como Usar

### Script de Desenvolvimento Interativo

O projeto inclui um script interativo que facilita o desenvolvimento:

```bash
./dev.sh
```

**Opções disponíveis:**
1. **Setup do ambiente** - Instala todas as dependências
2. **Iniciar apenas backend** - Executa só a API
3. **Iniciar apenas frontend** - Executa só a interface
4. **Iniciar aplicação completa** - Backend + Frontend
5. **Executar testes** - Roda os testes automatizados
6. **Build de produção** - Gera build otimizado
7. **Limpar ambiente** - Remove dependências instaladas

### URLs de Acesso

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentação da API:** http://localhost:8000/docs
- **API Alternativa (ReDoc):** http://localhost:8000/redoc

## 📊 Funcionalidades Detalhadas

### 🎯 Dashboard Principal
- Métricas em tempo real (receita, pedidos, clientes)
- Gráficos interativos de vendas e performance
- Indicadores de crescimento e tendências

### 🔮 Previsão de Vendas
- Algoritmos de forecasting baseados em dados históricos
- Visualização de tendências futuras
- Intervalos de confiança para previsões

### 👥 Segmentação de Clientes
- Análise RFM (Recência, Frequência, Valor Monetário)
- Clustering automático de perfis de clientes
- Insights para estratégias de marketing direcionado

### 💬 Análise de Sentimentos
- Processamento de reviews e feedback
- Classificação automática de sentimentos
- Identificação de palavras-chave positivas e negativas

### ⚠️ Predição de Churn
- Identificação de clientes em risco de cancelamento
- Scoring de probabilidade de churn
- Recomendações para retenção

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000

# Database (se aplicável)
DATABASE_URL=sqlite:///./business_insights.db
```

### Personalização

O projeto foi desenvolvido com arquitetura modular, permitindo fácil customização:

- **Modelos de ML:** Localizados em `backend/app/models/`
- **Componentes React:** Disponíveis em `frontend/src/components/`
- **APIs:** Definidas em `backend/app/api/routes.py`
- **Estilos:** CSS customizável em `frontend/src/components/`

## 🧪 Testes

```bash
# Testes do Backend
cd backend
python -m pytest

# Testes do Frontend
cd frontend
npm test
```

## 📦 Build para Produção

```bash
# Build do Frontend
cd frontend
npm run build

# O backend pode ser executado com:
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### 📋 Guidelines de Contribuição

- Siga os padrões de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use mensagens de commit descritivas

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Pietro Medeiros**
- GitHub: [@pietrogmedeiros](https://github.com/pietrogmedeiros)
- LinkedIn: [Pietro Medeiros](https://www.linkedin.com/in/pietro-medeiros-770bba162/)

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) pela excelente framework
- [React](https://reactjs.org/) pela biblioteca de UI
- [Ant Design](https://ant.design/) pelos componentes elegantes
- Comunidade open source pelas ferramentas incríveis

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**

[🔝 Voltar ao topo](#-ai-powered-business-insights-dashboard)

</div>
