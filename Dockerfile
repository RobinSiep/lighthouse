from python:3.7

RUN apt-get update

RUN addgroup lighthouse 
RUN useradd -g lighthouse lighthouse


COPY lighthouse /home/lighthouse/lighthouse
WORKDIR /home/lighthouse

RUN pip install -e lighthouse

USER lighthouse

EXPOSE 7102
CMD ["python3", "lighthouse/lighthouse/__init__.py"]
