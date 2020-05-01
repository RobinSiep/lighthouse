from python:3.7

RUN apt-get update

RUN addgroup lighthouse 
RUN useradd -g lighthouse lighthouse


COPY lighthouse /home/lighthouse/lighthouse
WORKDIR /home/lighthouse

RUN pip install -e lighthouse[dev]

# Download wait-for-it to allow waiting for dependency containers
RUN mkdir util
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > util/wait-for-it.sh
RUN chmod +x util/wait-for-it.sh

USER lighthouse

WORKDIR /home/lighthouse/lighthouse

EXPOSE 7102
ENTRYPOINT ["lighthouse"]
