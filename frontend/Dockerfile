FROM node:18
WORKDIR /app/frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Install specific packages
RUN npm install @radix-ui/react-switch

# Copy the rest of the application
COPY . .

# Set host and port for Vite
ENV HOST=0.0.0.0
ENV PORT=3000

# Use nodemon for hot reloading
RUN npm install -g nodemon

# Use nodemon to run the development server
CMD ["nodemon", "--watch", "src", "--exec", "npm", "run", "dev"]