FROM python:3.7-alpine

ADD ./ /tatiana/
WORKDIR /tatiana
RUN pip install -r requirements.txt
WORKDIR /tatiana
CMD cd /tatiana; sleep 30; flask db upgrade; python3 app.py

EXPOSE 80