# NexusPM - Sistema de Gerenciamento de Projetos

![Status](https://img.shields.io/badge/Status-Em%20Produção-orange)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚧 **PROJETO EM DESENVOLVIMENTO ATIVO**

Este projeto está atualmente em **desenvolvimento ativo** e **produção**. Algumas funcionalidades podem estar incompletas ou em processo de implementação.

## 📋 Visão Geral

O **NexusPM** é um sistema completo de gerenciamento de projetos desenvolvido com tecnologias modernas, oferecendo uma solução robusta para equipes que precisam organizar, acompanhar e colaborar em projetos de forma eficiente.

## 🏗️ Arquitetura do Projeto

```
NexusPM/
├── 📁 frontend/           # Aplicação React/Next.js
│   ├── 📁 src/           # Código fonte do frontend
│   ├── 📁 .storybook/    # Configurações do Storybook
│   ├── 📁 public/        # Arquivos estáticos
│   └── 📄 package.json   # Dependências do frontend
├── 📁 backend/           # API Node.js/Express
│   ├── 📁 src/          # Código fonte da API
│   ├── 📁 config/       # Configurações do backend
│   └── 📄 package.json  # Dependências do backend
├── 📁 mobile/           # Aplicação React Native
├── 📁 docs/             # Documentação do projeto
└── 📁 scripts/          # Scripts de automação
```

## 🚀 Tecnologias Utilizadas

### Frontend
- **React 18** - Biblioteca para interfaces de usuário
- **Next.js 14** - Framework React para produção
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **Storybook** - Ferramenta para desenvolvimento de componentes
- **React Query** - Gerenciamento de estado servidor

### Backend
- **Node.js** - Runtime JavaScript
- **Express.js** - Framework web
- **TypeScript** - Tipagem estática
- **Prisma** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Redis** - Cache e sessões
- **JWT** - Autenticação

### Mobile
- **React Native** - Framework para aplicações móveis
- **Expo** - Plataforma de desenvolvimento

### DevOps & CI/CD
- **Docker** - Containerização
- **GitHub Actions** - CI/CD
- **Azure DevOps** - Pipelines alternativos
- **CircleCI** - Integração contínua
- **Jenkins** - Automação
- **GitLab CI** - Pipelines GitLab

## 🎯 Funcionalidades Principais

### ✅ Implementadas
- [x] Sistema de autenticação e autorização
- [x] Dashboard principal com métricas
- [x] Gerenciamento de projetos
- [x] Sistema de tarefas e subtarefas
- [x] Colaboração em tempo real
- [x] Notificações push
- [x] Interface responsiva
- [x] Documentação com Storybook

### 🚧 Em Desenvolvimento
- [ ] Sistema de relatórios avançados
- [ ] Integração com calendário
- [ ] Chat interno integrado
- [ ] Sistema de arquivos e anexos
- [ ] API REST completa
- [ ] Testes automatizados
- [ ] Deploy automatizado

### 📋 Planejadas
- [ ] Aplicativo móvel nativo
- [ ] Integração com Slack/Teams
- [ ] Sistema de timesheet
- [ ] Relatórios personalizados
- [ ] Dashboard executivo
- [ ] Integração com Git

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Node.js 18+
- npm ou yarn
- PostgreSQL 14+
- Redis 6+
- Docker (opcional)

### Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/SSilvestreS/NexusPM.git
cd NexusPM
```

2. **Instale as dependências do frontend**
```bash
cd frontend
npm install
```

3. **Instale as dependências do backend**
```bash
cd ../backend
npm install
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute as migrações do banco**
```bash
npm run db:migrate
```

6. **Inicie os serviços**
```bash
# Frontend (porta 3000)
cd frontend && npm run dev

# Backend (porta 8000)
cd backend && npm run dev

# Storybook (porta 6006)
cd frontend && npm run storybook
```

### 🐳 Instalação com Docker

```bash
# Clone e entre no diretório
git clone https://github.com/SSilvestreS/NexusPM.git
cd NexusPM

# Execute com Docker Compose
docker-compose up -d
```

## 📚 Documentação

- **[Storybook](http://localhost:6006)** - Documentação de componentes
- **[API Docs](./docs/api/)** - Documentação da API
- **[Guia do Desenvolvedor](./docs/developer-guide.md)** - Guia para contribuidores
- **[Arquitetura](./docs/architecture.md)** - Visão técnica do sistema

## 🧪 Testes

```bash
# Testes do frontend
cd frontend && npm test

# Testes do backend
cd backend && npm test

# Testes e2e
npm run test:e2e

# Coverage
npm run test:coverage
```

## 🚀 Deploy

### Ambientes Disponíveis

- **Desenvolvimento**: `http://localhost:3000`
- **Staging**: `https://staging.nexuspm.com` (Em breve)
- **Produção**: `https://nexuspm.com` (Em desenvolvimento)

### CI/CD Pipeline

O projeto utiliza múltiplas estratégias de CI/CD:

- **GitHub Actions** - Pipeline principal
- **Azure DevOps** - Pipeline alternativo
- **CircleCI** - Testes e validação
- **GitLab CI** - Deploy secundário

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- **ESLint** - Linting JavaScript/TypeScript
- **Prettier** - Formatação de código
- **Husky** - Git hooks
- **Conventional Commits** - Padrão de commits

## 📊 Status do Projeto

### Progresso Geral: 65% ✅

| Módulo | Status | Progresso |
|--------|--------|-----------|
| Frontend | 🚧 Em desenvolvimento | 70% |
| Backend | 🚧 Em desenvolvimento | 60% |
| Mobile | 📋 Planejado | 0% |
| Testes | 🚧 Em desenvolvimento | 45% |
| Deploy | 🚧 Em desenvolvimento | 50% |
| Docs | ✅ Completo | 90% |

### Próximos Marcos

- **v1.1.0** - Sistema de relatórios (Março 2024)
- **v1.2.0** - Chat integrado (Abril 2024)
- **v2.0.0** - Aplicativo móvel (Junho 2024)

## 🐛 Problemas Conhecidos

- [ ] Performance do dashboard com muitos projetos
- [ ] Notificações em tempo real ocasionalmente falham
- [ ] Upload de arquivos grandes pode falhar
- [ ] Interface mobile precisa de otimizações

## 📞 Suporte

- **Email**: suporte@nexuspm.com
- **Discord**: [NexusPM Community](https://discord.gg/nexuspm)
- **Issues**: [GitHub Issues](https://github.com/SSilvestreS/NexusPM/issues)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Equipe

- **Desenvolvedor Principal**: [SSilvestreS](https://github.com/SSilvestreS)
- **Contribuidores**: Veja [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

<div align="center">
  
**⚠️ AVISO IMPORTANTE ⚠️**

Este projeto está em **desenvolvimento ativo** e algumas funcionalidades podem não estar completamente implementadas. Use em ambiente de produção por sua própria conta e risco.

</div>