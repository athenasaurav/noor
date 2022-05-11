FROM rasa/rasa:3.0

WORKDIR /app
COPY . /app
COPY ./data /app/data

RUN  rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug", "--endpoints", "endpoints.yml" ]