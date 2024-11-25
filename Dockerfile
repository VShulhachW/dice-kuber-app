FROM python:alpine3.20
RUN pip3 install --no-cache --upgrade flask && mkdir /app
COPY ./app.py /app/
WORKDIR /app
EXPOSE 8000
CMD ["python", "app.py"]