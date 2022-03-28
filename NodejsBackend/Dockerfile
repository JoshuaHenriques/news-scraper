FROM node:16.14.0-buster-slim
WORKDIR /app
COPY package*.json ./
RUN npm install --slient
COPY . .
CMD npm run start