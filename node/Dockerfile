# Use Alpine Linux as the base image
FROM node:18-alpine

# Install required packages, including bash and build tools
RUN apk update && \
    apk add --no-cache bash make g++ python3

# Set the SHELL to bash
SHELL ["/bin/bash", "-c"]

# Set the working directory to /app
WORKDIR /app

# Create the 'node' directory
RUN mkdir -p ./node

# Copy package.json to /app
COPY package.json ./

# Install project dependencies
RUN npm install

# Set the working directory to /app/node
WORKDIR /app/node

# Create 'consumer' and 'producer' directories
RUN mkdir -p ./consumer ./producer

# Copy your Node.js application files to /app/node
COPY node/*.js ./

# Copy consumer and producer files
COPY node/consumer/* ./consumer
COPY node/producer/* ./producer

# Expose the port that your Node.js application listens on
EXPOSE 8080

# Set the working directory back to /app
WORKDIR /app

# Specify the command to run your application
CMD ["npm", "run", "start:consumer"]
