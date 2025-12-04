# Picked from https://hub.docker.com/_/node
FROM node:25-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Build argument for ReCAPTCHA site key
ARG NEXT_PUBLIC_RECAPTCHA_SITE_KEY
ENV NEXT_PUBLIC_RECAPTCHA_SITE_KEY=$NEXT_PUBLIC_RECAPTCHA_SITE_KEY

# Build the Next.js application
RUN npm run build

# Default Port for Next.js app
EXPOSE 3000

CMD ["npm", "start"]