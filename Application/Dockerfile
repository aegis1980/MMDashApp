## This works on manualinstall in Azure. 

#FROM python:3.6

#WORKDIR /
#ADD requirements.txt /
#RUN pip install -r requirements.txt
#COPY . /

#ENTRYPOINT [ "python" ]
#CMD ["runserver.py"]

# **********************************************************
## From automated Devops install boilerplate

FROM ubuntu:16.04
LABEL maintainer="Azure App Service Container Images <appsvc-images@microsoft.com>"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["runserver.py"]