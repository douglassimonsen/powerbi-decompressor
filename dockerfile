FROM ubuntu:latest
RUN apt update
RUN apt install -y python3 python3-pip libpq-dev curl sudo
RUN pip install flask flask-cors psycopg2

RUN mkdir -p /usr/local/nvm
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION v19.2.0
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/bin
ENV PATH $NODE_PATH:$PATH

COPY visualizer visualizer
COPY creds.json creds.json
COPY docker-assets/run.sh run.sh

WORKDIR /visualizer/frontend/
RUN npm ci

EXPOSE 100
EXPOSE 5000
EXPOSE 5432

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["sh", "/run.sh"]