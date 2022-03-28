FROM python:3

ADD backend.py /
ADD requirements.txt /

ENV FLASK_APP=backend.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN pip install -r requirements.txt



CMD [ "waitress-serve", "--port=5000", "backend:app" ]
EXPOSE 5000