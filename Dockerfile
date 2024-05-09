FROM python:latest

RUN mkdir /root/app

COPY . /root/app

WORKDIR /root/app

RUN pip install -r /root/app/requirements

CMD [ "python", "run.py" ]