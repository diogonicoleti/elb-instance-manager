FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY elb_instance_manager .

RUN addgroup -S app && adduser -S -G app app && \
    chown -R app:app /app

EXPOSE 5000

USER app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
