FROM node:18

# Рабочая директория
WORKDIR /app

# Установка зависимостей
COPY front/package*.json ./
RUN npm install

# Копируем проект
COPY front ./

# Сборка прод-версии
RUN npm run build

# Сервер для фронта (используем nginx или http-server)
RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
