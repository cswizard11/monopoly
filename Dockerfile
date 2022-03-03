FROM python:3.8

WORKDIR /app
COPY *.py requirements.txt start.sh /app/
COPY /static /app/static/
COPY /templates /app/templates/

RUN apt-get update && apt-get -y install
RUN pip install -r requirements.txt
RUN chmod +x start.sh

CMD ["./start.sh"]