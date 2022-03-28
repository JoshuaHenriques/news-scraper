FROM node:16.14.0-buster-slim
WORKDIR /app
COPY package*.json ./
RUN npm install --slient
COPY . .
RUN npm install -g serve --silent
CMD serve -s build