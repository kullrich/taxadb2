FROM python:3

MAINTAINER Kristian Ullrich <ullrich@evolbio.mpg.de>

WORKDIR /usr/src/app

RUN pip install taxadb2

CMD [ "taxadb2" ]
