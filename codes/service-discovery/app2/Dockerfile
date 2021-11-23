FROM python:3.8.3-slim-buster
COPY app.py requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 9090
CMD [ "python", "app.py"]
