FROM ubuntu:latest 
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update

RUN apt install -y nano

# for postgres
RUN apt install -y sudo tzdata postgresql postgresql-contrib

RUN apt install -y python-setuptools python3-pip

RUN apt install -y nodejs npm

COPY load_to_db load_to_db
COPY visualizer visualizer

COPY docker-assets/initialize.sh /initialize.sh
COPY docker-assets/postgresql.conf /etc/postgresql/14/main/postgresql.conf
COPY docker-assets/pg_hba.conf /etc/postgresql/14/main/pg_hba.conf

RUN /initialize.sh

# 80 is nodejs, 5000 is flask, 5432 is postgres
EXPOSE 22
EXPOSE 80 
EXPOSE 5000
EXPOSE 5432
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
