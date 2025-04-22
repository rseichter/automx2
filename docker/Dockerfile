FROM python:3

# Preapre default config file
COPY automx2.conf /etc/automx2/automx2.conf

# Prepare user and working directory
RUN useradd --home-dir /opt/automx2 --create-home automx2
WORKDIR /opt/automx2 
USER automx2

# Install AutoMX2
RUN cd /opt/automx2 
RUN wget https://raw.githubusercontent.com/rseichter/automx2/master/contrib/install.sh
RUN bash install.sh
RUN /opt/automx2/.venv/bin/pip install --upgrade automx2

# Install database dirvers
RUN /opt/automx2/.venv/bin/pip install PyMySQL
RUN /opt/automx2/.venv/bin/pip install mysqlclient
RUN /opt/automx2/.venv/bin/pip install psycopg2

EXPOSE 8080

# Use installed default entriypoint 
ENTRYPOINT /opt/automx2/.venv/bin/flask.sh run --host=0.0.0.0 --port=8080
