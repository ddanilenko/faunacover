FROM python:3.4-alpine
MAINTAINER Daria "ddanilenko@ukr.net"
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "run.py"]