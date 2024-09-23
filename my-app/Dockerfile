# Use a Node.js base image
FROM node:18

# Set the working directory
WORKDIR /my-app

# Copy package.json and package-lock.json
COPY my-app/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY my-app/ ./

# Build the app for production
RUN npm run build


# Expose port 3000
EXPOSE 3000

# Start NGINX
CMD ["npm", "start"]