# frontend/Dockerfile

# --- Etap 1: Build ---
FROM node:lts-alpine as build-stage

WORKDIR /app

# Skopiuj package.json i lockfile
COPY package*.json ./
# Jeśli używasz yarn:
# COPY yarn.lock ./

# Zainstaluj zależności
RUN npm install
# Jeśli używasz yarn:
# RUN yarn install

# Skopiuj resztę kodu
COPY . .

# Zbuduj aplikację dla produkcji
# Możesz tu przekazać zmienne środowiskowe dla API URL, jeśli potrzebujesz
# ARG VITE_API_URL=/api  # Domyślna wartość, można nadpisać przy budowaniu
# ENV VITE_API_URL=$VITE_API_URL
RUN npm run build
# Jeśli używasz yarn:
# RUN yarn build

# --- Etap 2: Serwowanie (Niepotrzebny dla tego podejścia) ---
# W naszym przypadku Django/Whitenoise będzie serwować pliki statyczne Vue.
# Ten Dockerfile służy tylko do zbudowania plików statycznych,
# które zostaną skopiowane do odpowiedniego miejsca dla Django.
# Zostawiamy go tak, bo może być przydatny do lokalnego testowania builda.

# Można dodać tu etap serwowania z Nginx dla testów lokalnych, np:
# FROM nginx:stable-alpine
# COPY --from=build-stage /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]