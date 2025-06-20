# --- Stage 1: Build the React App ---
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY ./frontend/package*.json ./

# FIX: Corrected the typo from 'instaAll' to 'install'
RUN npm install

# Copy the rest of the frontend source code
COPY ./frontend ./

# Build the app for production
RUN npm run build

# --- Stage 2: Serve the App with Nginx ---
FROM nginx:alpine

# Copy the built static files from the '/app/dist' folder
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# The default Nginx command will start the server
CMD ["nginx", "-g", "daemon off;"]
