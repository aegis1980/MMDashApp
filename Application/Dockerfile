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

#FROM ubuntu:16.10 #changed from default 16.04
#LABEL maintainer="Azure App Service Container Images <appsvc-images@microsoft.com>"

#RUN apt-get clean && apt-get update -y -m
#RUN apt-get install -y build-essential
#RUN apt-get install -y python3.6 python3-pip python3-dev
#COPY . /app
#WORKDIR /app
#RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
#EXPOSE 5000
#CMD ["runserver.py"]


FROM python:3.6
LABEL maintainer="Azure App Service Container Images <appsvc-images@microsoft.com>"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["runserver.py"]