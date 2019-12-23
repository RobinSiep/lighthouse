from python:3.7

RUN apt-get update

RUN addgroup lighthouse 
RUN useradd -g lighthouse lighthouse


COPY lighthouse-master /home/lighthouse/lighthouse-master
WORKDIR /home/lighthouse

RUN pip install -e lighthouse-master

USER lighthouse

EXPOSE 7102
CMD ["python3", "lighthouse-master/lighthousemaster/__init__.py"]
