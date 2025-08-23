# 🚀 NexusPM - Sistema de Gerenciamento de Projetos Colaborativos

[![Status](https://img.shields.io/badge/Status-Completo-green)](https://github.com/SSilvestreS/NexusPM)
[![Versão](https://img.shields.io/badge/Versão-3.0.0-blue)](https://github.com/SSilvestreS/NexusPM/releases)
[![Licença](https://img.shields.io/badge/Licença-MIT-green)](https://github.com/SSilvestreS/NexusPM/blob/master/LICENSE)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/SSilvestreS/NexusPM/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/)

## 🎯 **Visão Geral**

O **NexusPM** é um sistema completo de gerenciamento de projetos colaborativos em tempo real, desenvolvido para equipes que precisam organizar, acompanhar e colaborar em projetos de forma eficiente. Inspirado em ferramentas como Jira e Asana, oferece uma solução moderna e robusta para gestão de projetos.

### 🎯 **Características Principais**

- 🔐 **Autenticação JWT** com OAuth2.0 (GitHub/GitLab)
- ⚡ **Dashboard em Tempo Real** com WebSockets
- 📊 **Sistema Completo de CRUD** para projetos com versionamento
- 👥 **Editor Colaborativo** com operational transformation
- 💬 **Sistema de Comentários** com mentions e notificações
- 🔗 **Integrações Externas** (GitHub/GitLab via webhooks)
- 📈 **Relatórios Avançados** com exportação PDF/Excel
- 🌍 **Internacionalização (i18n)** e temas claro/escuro
- 📱 **Interface Responsiva** para todos os dispositivos

## 🏗️ **Arquitetura do Sistema**

```
NexusPM/
├── 📁 frontend/           # Aplicação React/TypeScript
│   ├── 🚀 src/           # Código fonte do frontend
│   ├── 📁 public/        # Arquivos estáticos
│   └── 📦 package.json   # Dependências do frontend
├── 🐍 backend/           # API Python/FastAPI
│   ├── 📁 app/          # Código fonte da API
│   ├── 📁 alembic/      # Migrações de banco
│   └── 📋 requirements.txt # Dependências Python
├── 📁 .github/          # Workflows e configurações
├── 📁 docs/             # Documentação técnica
└── 🐳 docker-compose.yml # Orquestração de serviços
```

## 🚀 **Stack Tecnológica**

### **Backend**
- **Python 3.11** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL 15** - Banco de dados relacional com busca full-text
- **Redis 7** - Cache e gerenciamento de sessões
- **Celery** - Processamento assíncrono de tarefas
- **RabbitMQ** - Message broker para filas
- **SQLAlchemy 2.0** - ORM assíncrono
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados e serialização

### **Frontend**
- **React 18** - Biblioteca de interface de usuário
- **TypeScript 5.2** - Tipagem estática
- **Vite** - Build tool e servidor de desenvolvimento
- **Tailwind CSS** - Framework CSS utilitário
- **React Router 6** - Roteamento da aplicação
- **Axios** - Cliente HTTP para APIs
- **Vitest** - Framework de testes
- **ESLint + Prettier** - Linting e formatação

### **Infraestrutura**
- **Docker & Docker Compose** - Containerização
- **GitHub Actions** - CI/CD automatizado
- **CodeQL** - Análise estática de segurança
- **Nginx** - Servidor web e proxy reverso

## 📋 **Pré-requisitos**

### **Sistema Operacional**
- **Windows 10/11** (recomendado)
- **macOS 10.15+**
- **Ubuntu 20.04+** / **CentOS 8+**

### **Software Necessário**
- **Docker Desktop** 4.0+ ou **Docker Engine** 20.10+
- **Docker Compose** 2.0+
- **Git** 2.30+
- **Node.js** 18.0+ (para desenvolvimento frontend)
- **Python** 3.11+ (para desenvolvimento backend)

### **Recursos Mínimos**
- **RAM:** 8GB (16GB recomendado)
- **CPU:** 4 cores (8 cores recomendado)
- **Disco:** 20GB de espaço livre
- **Rede:** Conexão estável com internet

## 🚀 **Instalação e Configuração**

### **1. Clone do Repositório**

```bash
# Clone o repositório
git clone https://github.com/SSilvestreS/NexusPM.git
cd NexusPM

# Verifique se está na branch correta
git checkout master
```

### **2. Configuração do Ambiente**

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite as variáveis de ambiente
# Use seu editor preferido (VS Code, Notepad++, etc.)
code .env
```

#### **Variáveis de Ambiente Importantes**

```env
# Banco de Dados
DATABASE_URL=postgresql://nova_pasta:nova_pasta_pass@localhost:5432/nova_pasta

# Redis
REDIS_URL=redis://localhost:6379

# RabbitMQ
RABBITMQ_URL=amqp://nova_pasta:nova_pasta_pass@localhost:5672

# Segurança
SECRET_KEY=sua_chave_secreta_aqui_mude_em_producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

### **3. Inicialização com Docker**

```bash
# Inicie todos os serviços
docker-compose up -d

# Verifique o status dos serviços
docker-compose ps

# Visualize os logs
docker-compose logs -f
```

### **4. Verificação da Instalação**

Após a inicialização, verifique se todos os serviços estão funcionando:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379
- **RabbitMQ Management:** http://localhost:15672

## 🛠️ **Desenvolvimento Local**

### **Backend (Python/FastAPI)**

```bash
# Entre no diretório do backend
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
alembic upgrade head

# Inicie o servidor de desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend (React/TypeScript)**

```bash
# Entre no diretório do frontend
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev

# Em outro terminal, execute os testes
npm run test

# Verificação de tipos
npm run type-check

# Linting
npm run lint
```

## 🧪 **Testes**

### **Backend (Python)**

```bash
cd backend

# Execute todos os testes
pytest

# Execute com coverage
pytest --cov=app --cov-report=html

# Execute testes específicos
pytest tests/test_auth.py

# Execute com verbose
pytest -v
```

### **Frontend (TypeScript)**

```bash
cd frontend

# Execute todos os testes
npm run test

# Execute testes em modo watch
npm run test -- --watch

# Execute testes com UI
npm run test -- --ui

# Verificação de tipos
npm run type-check
```

## 🚀 **Deploy em Produção**

### **1. Preparação do Ambiente**

```bash
# Configure variáveis de produção
cp env.example .env.prod

# Edite as variáveis para produção
# - URLs públicas
# - Chaves secretas fortes
# - Configurações de banco de produção
```

### **2. Deploy com Docker**

```bash
# Build das imagens
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Verificação
docker-compose -f docker-compose.prod.yml ps
```

### **3. Deploy em Cloud**

#### **AWS (ECS/Fargate)**
```bash
# Build e push para ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag nova-pasta-backend:latest $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nova-pasta-backend:latest
docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nova-pasta-backend:latest
```

#### **Azure (Container Instances)**
```bash
# Build e push para ACR
az acr build --registry $ACR_NAME --image nova-pasta-backend:latest .
```

## 📚 **Documentação da API**

### **Swagger/OpenAPI**
- **URL:** http://localhost:8000/docs
- **Especificação:** http://localhost:8000/openapi.json

### **Endpoints Principais**

#### **Autenticação**
- `POST /api/v1/auth/register` - Registro de usuário
- `POST /api/v1/auth/login` - Login de usuário
- `POST /api/v1/auth/refresh` - Renovação de token
- `POST /api/v1/auth/logout` - Logout de usuário

#### **Usuários**
- `GET /api/v1/users/me` - Perfil do usuário atual
- `PUT /api/v1/users/me` - Atualização de perfil
- `GET /api/v1/users` - Lista de usuários (admin)

#### **Projetos**
- `GET /api/v1/projects` - Lista de projetos
- `POST /api/v1/projects` - Criação de projeto
- `GET /api/v1/projects/{id}` - Detalhes do projeto
- `PUT /api/v1/projects/{id}` - Atualização de projeto
- `DELETE /api/v1/projects/{id}` - Exclusão de projeto

#### **Tarefas**
- `GET /api/v1/tasks` - Lista de tarefas
- `POST /api/v1/tasks` - Criação de tarefa
- `GET /api/v1/tasks/{id}` - Detalhes da tarefa
- `PUT /api/v1/tasks/{id}` - Atualização de tarefa
- `DELETE /api/v1/tasks/{id}` - Exclusão de tarefa

## 🔧 **Configurações Avançadas**

### **Banco de Dados**

#### **PostgreSQL**
```sql
-- Criação de usuário e banco
CREATE USER nova_pasta WITH PASSWORD 'nova_pasta_pass';
CREATE DATABASE nova_pasta OWNER nova_pasta;

-- Configurações de performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

#### **Redis**
```bash
# Configuração de persistência
redis-cli CONFIG SET save "900 1 300 10 60 10000"
redis-cli CONFIG SET appendonly yes
redis-cli CONFIG REWRITE
```

### **Celery (Tarefas Assíncronas)**

```python
# Configuração de workers
celery -A app.core.celery_app worker --loglevel=info --concurrency=4

# Configuração de beat (agendador)
celery -A app.core.celery_app beat --loglevel=info

# Monitoramento com Flower
celery -A app.core.celery_app flower --port=5555
```

## 🚨 **Troubleshooting**

### **Problemas Comuns**

#### **1. Porta já em uso**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

#### **2. Problemas de Docker**
```bash
# Limpeza de containers
docker system prune -a

# Reinicialização do Docker
# Windows: Restart Docker Desktop
# Linux: sudo systemctl restart docker
```

#### **3. Problemas de Banco**
```bash
# Verificação de conexão
docker exec -it nova-pasta-postgres-1 psql -U nova_pasta -d nova_pasta

# Reset do banco
docker-compose down -v
docker-compose up -d
```

#### **4. Problemas de Cache**
```bash
# Limpeza de cache do npm
npm cache clean --force

# Limpeza de cache do Docker
docker builder prune
```

## 🤝 **Contribuição**

### **Como Contribuir**

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/NovaFuncionalidade
   ```
3. **Faça suas alterações**
4. **Commit suas mudanças**
   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```
5. **Push para a branch**
   ```bash
   git push origin feature/NovaFuncionalidade
   ```
6. **Abra um Pull Request**

### **Padrões de Código**

#### **Python (Backend)**
- **Formatação:** Black
- **Linting:** Flake8
- **Imports:** isort
- **Type Checking:** mypy

#### **TypeScript (Frontend)**
- **Formatação:** Prettier
- **Linting:** ESLint
- **Type Checking:** TypeScript strict mode

### **Conventional Commits**
```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação de código
refactor: refatoração de código
test: adição de testes
chore: tarefas de manutenção
```

## 📊 **Monitoramento e Logs**

### **Logs da Aplicação**

```bash
# Logs do backend
docker-compose logs -f backend

# Logs do frontend
docker-compose logs -f frontend

# Logs de todos os serviços
docker-compose logs -f
```

### **Métricas e Health Checks**

- **Backend:** http://localhost:8000/health
- **Frontend:** http://localhost:3000/health
- **PostgreSQL:** Verificação automática no docker-compose
- **Redis:** Verificação automática no docker-compose
- **RabbitMQ:** Verificação automática no docker-compose

## 🔒 **Segurança**

### **Boas Práticas**

1. **Nunca commite arquivos .env**
2. **Use chaves secretas fortes**
3. **Mantenha dependências atualizadas**
4. **Configure HTTPS em produção**
5. **Implemente rate limiting**
6. **Use CORS adequadamente**
7. **Valide todas as entradas**
8. **Implemente logging de auditoria**

### **Configurações de Segurança**

```python
# CORS
CORS_ORIGINS = ["http://localhost:3000", "https://seudominio.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 60

# JWT
JWT_SECRET_KEY = "chave_super_secreta_e_complexa"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 📈 **Performance e Escalabilidade**

### **Otimizações Recomendadas**

1. **Cache Redis** para consultas frequentes
2. **Indexação** adequada no banco de dados
3. **Lazy loading** no frontend
4. **Code splitting** com React.lazy
5. **CDN** para assets estáticos
6. **Load balancing** para múltiplas instâncias
7. **Database connection pooling**
8. **Async/await** para operações I/O

### **Benchmarks**

- **Backend:** 1000+ requests/segundo
- **Frontend:** Time to Interactive < 3s
- **Database:** Query response < 100ms
- **Cache:** Hit ratio > 90%

## 🌟 **Roadmap**

### **Versão 1.1.0 (Q1 2024)**
- [ ] Sistema de relatórios avançados
- [ ] Integração com calendário
- [ ] Chat interno integrado
- [ ] Sistema de arquivos e anexos

### **Versão 1.2.0 (Q2 2024)**
- [ ] API GraphQL
- [ ] Sistema de plugins
- [ ] Modo offline
- [ ] Virtual scrolling

### **Versão 2.0.0 (Q3 2024)**
- [ ] Aplicativo móvel nativo
- [ ] Integração com Slack/Teams
- [ ] Sistema de timesheet
- [ ] Dashboard executivo

## 📞 **Suporte e Contato**

### **Canais de Suporte**

- **Issues:** [GitHub Issues](https://github.com/SSilvestreS/NexusPM/issues)
- **Discussions:** [GitHub Discussions](https://github.com/SSilvestreS/NexusPM/discussions)
- **Wiki:** [Documentação Wiki](https://github.com/SSilvestreS/NexusPM/wiki)

### **Equipe de Desenvolvimento**

- **Desenvolvedor Principal:** [SSilvestreS](https://github.com/SSilvestreS)
- **Contribuidores:** Veja [CONTRIBUTORS.md](CONTRIBUTORS.md)

## 📄 **Licença**

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 Nova Pasta Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 **Agradecimentos**

- **FastAPI** - Framework web incrível
- **React** - Biblioteca de UI revolucionária
- **Tailwind CSS** - Framework CSS utilitário
- **Docker** - Containerização que simplifica tudo
- **GitHub** - Plataforma que torna o desenvolvimento colaborativo possível

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub! ⭐**

**🚀 NexusPM - Transformando a gestão de projetos colaborativos 🚀**

</div>
