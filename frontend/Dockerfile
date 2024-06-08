FROM node:20.12.2-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV REACT_APP_BACKEND_URL=nginx_container:80

RUN npm run build

Expose 3000

CMD ["npm", "run", "production"]