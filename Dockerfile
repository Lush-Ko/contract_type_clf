FROM jupyter/datascience-notebook

USER 0

RUN apt update

RUN apt install default-jdk -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


