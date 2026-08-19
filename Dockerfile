FROM python
WORKDIR /home/natalia/Proyecto_buenos/docker/Docker_github/

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python3", "sample_app.py"]