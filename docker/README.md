# AutoMX2 Docker file

## Content

This dockerfile installs AutoMX2 through the [installation script](https://github.com/rseichter/automx2/blob/master/contrib/install.sh) from the [master branch](https://github.com/rseichter/automx2).
The [installation script](https://github.com/rseichter/automx2/blob/master/contrib/install.sh) prepares a python 3 virtual environment with automx2.
In addition, PostgreSQL and MySQL drivers are installed into the virtual environment. 

## Database

The default automx2.conf places the SQLite database under _/opt/automx2/databse/db.sqlite_

## Port

The container exposes AutoMX2 on port **8080** by default and can be adjusted by the entrypoint. 

## Documentation

See the AutoMX2 configuration from [Ralph Seichter](https://github.com/rseichter) here:
https://rseichter.github.io/automx2/

## Docker compose

This [docker compose](https://docs.docker.com/compose/) shows a AutoMX2 deployment with [Traefik](https://traefik.io/traefik/) as a reverse proxy.

```YAML

version: "3.3"

services:
  automx:
    image: IMAGE_NAME
    environment:
      AUTOMX2_CONF: '/opt/automx2/config/automx2.conf' # Path to your automx2 config
    volumes:
      - config:/opt/automx2/config # Volume containing an AutoMX2 config
      - database:/opt/automx2/databse  # Volume containing the SQLite database as configured by default
    deploy:
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.automx2.tls=true"
        - "traefik.http.services.automx2.loadbalancer.server.port=8080"
        # This Regex matches any domain with the subdomains "autoconfig" and "autodiscover".
        # Dots must be escaped with "\." and the "\" must be escaped in YAML as well.
        # Therefore, the dots are represented by "\\.".
        # Same with the "$" at the end. It must be escaped by a "$". 
        - "traefik.http.routers.automx2.rule=HostRegexp(`^((autoconfig)|(autodiscover))\\..*\\.[A-Za-z]+$$`)"
    networks:
      - Traefik

volumes:
  config:
  database:


networks:
  Traefik:
    external: true

```



