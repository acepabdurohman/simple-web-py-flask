FROM python:3.6.8

WORKDIR /opt/app

COPY . /opt/app

RUN pip install -r requirements.txt

CMD ["python","app.py"]