<<<<<<< HEAD
FROM node:20-alpine
=======
# Picked from https://hub.docker.com/_/node
FROM node:25-alpine
>>>>>>> ba967eb5a787e7bc79aafb924ee62614baa0fac4

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

<<<<<<< HEAD
EXPOSE 3000

CMD ["npm", "run", "dev"]
=======
# Build the Next.js application
RUN npm run build

# Default Port for Next.js app
EXPOSE 3000

CMD ["npm", "start"]
>>>>>>> ba967eb5a787e7bc79aafb924ee62614baa0fac4
