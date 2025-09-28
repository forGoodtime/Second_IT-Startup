FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application (for production)
# RUN npm run build

EXPOSE 3000

# Development command (change to npm start for production)
CMD ["npm", "run", "dev"]
