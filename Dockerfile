FROM python:3.8

RUN pip3 install webthing requests

COPY ./proxy.py /proxy.py

CMD ["/proxy.py", "--port=80"]
