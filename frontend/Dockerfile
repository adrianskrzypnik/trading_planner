FROM node:18-alpine

WORKDIR /app

# Instalacja zależności
COPY package.json package-lock.json* ./
RUN npm ci

# Kopiowanie kodu źródłowego
COPY . .

# Expose port used by the application
EXPOSE 5173

# Define command to run when container starts
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]