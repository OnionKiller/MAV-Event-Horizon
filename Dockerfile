FROM python:3.10

RUN useradd --home /opt/ --no-create-home --uid 5000 --user-group publisher

COPY . /opt

WORKDIR /opt

RUN pip install -r requirements.txt

USER publisher

EXPOSE 8000/tcp

CMD ["hug","-f","app.py"]
