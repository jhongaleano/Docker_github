FROM python
WORKDIR /home/jhon/Proyectos/python-docker/

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python3", "sample-app.py"]