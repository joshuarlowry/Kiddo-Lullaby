#https://www.docker.com/blog/containerized-python-development-part-1/
#https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/ 

#Use Python 3.8
FROM python:3.8

#Create a working directory
WORKDIR /app

COPY requirements.txt .

#install Spotipy
RUN pip install -r requirements.txt

#We should have an image that is based on version 14.15.3 with the relevant dependencies from our package
#Copy the files into the image
COPY src/ .

VOLUME /config
ENV CACHE_PATH=/config/.cache

#Run the server
CMD [ "python", "./server.py"]