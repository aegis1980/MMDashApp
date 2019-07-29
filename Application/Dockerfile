# Docker baseimage.
FROM python:3.6

COPY . /
WORKDIR /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000 #the port
CMD ["runserver.py"]

#NOTE
#This is different to the boiler plate dockerfile that gets install in the
#azure -> devops project -> containerflashapp

#Issue with the boiler plate (flask) one is that to be useful you are probably
#using pandas with dash, and pandas need python3.5.
#The boilerplate docker only has python2 :(

# boiler plate is included commented out below.


# **********************************************************
## From automated Devops install boilerplate
## Good luck getting it to work with python 3.5
## if your project does not use numpy then you might get away with it.



#FROM ubuntu:16.10 
	#Boiler plate is 16.04, which does not have python3.x installed. 16.10 does
#LABEL maintainer="Azure App Service Container Images <appsvc-images@microsoft.com>"
	#Not sure this line has any function

#RUN apt-get clean && apt-get update -y -m
	#this throws an error with 16.10
#RUN apt-get install -y build-essential
#RUN apt-get install -y python3.6 python3-pip python3-dev
#COPY . /app
#WORKDIR /app
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
#EXPOSE 5000
#CMD ["runserver.py"]