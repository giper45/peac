# File: Dockerfile.frontend
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy source files
COPY . /app

# Install dependencies
RUN npm install

# Build the React application
RUN npm run build

# Serve the app
EXPOSE 3000
CMD ["npm", "start"]
