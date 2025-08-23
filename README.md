# NexusPM - Sistema de Gerenciamento de Projetos

Sistema completo de gerenciamento de projetos colaborativos em tempo real, similar ao Jira/Asana.

## 🚀 Tecnologias

### Backend
- **Python 3.11** com FastAPI
- **PostgreSQL** com busca full-text
- **Redis** para cache e sessões
- **Celery** com RabbitMQ para tarefas assíncronas

### Frontend
- **React 18** com TypeScript
- **Vite** para build e desenvolvimento
- **Tailwind CSS** para estilização
- **WebSockets** para comunicação em tempo real

## 📋 Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento frontend)
- Python 3.11+ (para desenvolvimento backend)

## 🚀 Quick Start

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/nova-pasta.git
   cd nova-pasta
   ```

2. **Configure as variáveis de ambiente:**
   ```bash
   cp env.example .env
   # Edite o arquivo .env com suas configurações
   ```

3. **Inicie com Docker:**
   ```bash
   docker-compose up -d
   ```

4. **Acesse a aplicação:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs

## 🛠️ Desenvolvimento

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📚 Documentação

- [API Docs](http://localhost:8000/docs) - Swagger/OpenAPI
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
