#Create a ubuntu base image with python 3 installed.
FROM python:3.7

#Set the working directory
COPY . /app

#copy all the files
WORKDIR /app

#Install the dependencies
RUN pip install -r requirements.txt

#Expose the required port
EXPOSE $PORT

#Run the command
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app


