#https://www.docker.com/blog/containerized-python-development-part-1/

#Use Python 3.8
FROM python:3.8

#Create a working directory
WORKDIR /app

#install Spotipy
pip install spotipy --upgrade

#We should have an image that is based on version 14.15.3 with the relevant dependencies from our package
#Copy the files into the image
COPY . .

#Run the server
