# Etap budowania
FROM node:18-alpine AS build

WORKDIR /app

# Kopiowanie plików zależności
COPY package*.json ./

# Instalacja zależności
RUN npm install

# Kopiowanie reszty kodu źródłowego
COPY . .

# Budowanie aplikacji
RUN npm run build

# Etap produkcyjny
FROM nginx:alpine

# Kopiowanie zbudowanej aplikacji z etapu budowania
COPY --from=build /app/dist /usr/share/nginx/html

# Kopiowanie konfiguracji nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Eksponowanie portu
EXPOSE 80

# Uruchamianie nginx
CMD ["nginx", "-g", "daemon off;"]