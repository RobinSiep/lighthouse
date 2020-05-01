from python:3.7

RUN apt-get update

RUN addgroup lighthouse 
RUN useradd -g lighthouse lighthouse

COPY . /home/lighthouse/lighthouse
WORKDIR /home/lighthouse
RUN mkdir config

RUN pip install -e lighthouse[dev]

# Download wait-for-it to allow waiting for dependency containers
RUN mkdir util
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > util/wait-for-it.sh
RUN chmod +x util/wait-for-it.sh

USER lighthouse

WORKDIR /home/lighthouse/lighthouse

EXPOSE 7102
ENTRYPOINT ["lighthouse"]
CMD ["--config", "/home/lighthouse/config/local-settings.ini"]
