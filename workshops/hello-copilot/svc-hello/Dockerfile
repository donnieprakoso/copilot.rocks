FROM python:3.8.3-slim-buster
WORKDIR /app
COPY app.py /app
COPY index.html /app 
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 9090
CMD [ "python", "app.py"]
