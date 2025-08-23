FROM node:18-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY package*.json ./

# Instala as dependências
RUN npm ci --only=production

# Copia o código fonte
COPY . .

# Constrói a aplicação para produção
RUN npm run build

# Instala o servidor estático
RUN npm install -g serve

# Expõe a porta 3000
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["serve", "-s", "build", "-l", "3000"]
