FROM python:slim

RUN useradd non-root

WORKDIR /home/lunch-coupon-service

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY server.py config.py start.sh ./
RUN chmod +x start.sh

ENV FLASK_APP server.py

RUN chown -R non-root:non-root ./

USER non-root

EXPOSE 5000

ENTRYPOINT ["./start.sh"]