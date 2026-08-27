FROM python:3.8-slim-buster
WORKDIR /home/jhon/Proyectos/python-docker/
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python3", "sample_app.py"]