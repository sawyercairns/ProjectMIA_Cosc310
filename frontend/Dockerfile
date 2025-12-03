# Picked from https://hub.docker.com/_/node
FROM node:25-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Build the Next.js application
RUN npm run build

# Default Port for Next.js app
EXPOSE 3000

CMD ["npm", "start"]