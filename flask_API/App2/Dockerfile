FROM python:latest

RUN mkdir -p /usr/src/app2

WORKDIR /usr/src/app2

RUN mkdir -p ./resources

#COPY ./resources/resource.json ./resources/resource.json

COPY app2.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD [ "python", "app2.py" ]