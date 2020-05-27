FROM python:latest

WORKDIR /usr/src/app2

RUN mkdir ./resources

COPY ./resources/resource.json ./resources/resource.json

COPY app2.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app2.py" ]
