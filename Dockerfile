FROM python:3.8

WORKDIR /app
COPY * /app/

RUN apt-get update && apt-get -y install
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sleep", "infinity"]