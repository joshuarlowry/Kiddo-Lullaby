#Use Specifically Node 14.15.3 LTS
FROM node:14.15.3

#Create a working directory
WORKDIR /app

#Copy our package files
COPY package.json package.json
COPY package-lock.json package-lock.json

#install
RUN npm install

#We should have an image that is based on version 14.15.3 with the relevant dependencies from our package
#Copy the files into the image
COPY . .

#Run the server
CMD [ "node", "server.js" ]