# automx2

Successor to **automx**, designed to be easier to configure and use.
Written by Ralph Seichter for [sys4 AG](https://sys4.de/).

_This software is considered to be in Beta state, so make sure to use protection._

## Installing

TODO

## Configuring

When run by user `alice`, automx2 attempts to load configuration data from the following files, in the specified order,
stopping at the first match:

1. Value of `AUTOMX2_CONF` environment variable (if available)
2. `~alice/.automx2.conf` (note the leading dot)
2. `/etc/automx2/automx2.conf`
2. `/etc/automx2.conf`

While automx2 can be launched without a configuration file, the internal defaults are only suitable for testing, in
particular because an in-memory sqlite database will be used, meaning all data is lost once the application terminates.

The file format is an [INI variant](https://docs.python.org/3.7/library/configparser.html#supported-ini-file-structure).
An example configuration file is available [here](contrib/automx2-sample.conf). A minimal configuration file for
production use only needs to contain one `db_uri` entry in the defaults section, pointing to a non-transient database.

## Database support

This application uses the excellent SQLAlchemy toolkit which supports various SQL
[dialects](https://docs.sqlalchemy.org/dialects/). While you probably already have SQLite support available on your
local machine, you may need to install additional Python packages for PostgreSQL, MySQL, etc. Detailed instructions
to support a particular database dialect are out of scope for this document, but there are numerous guides available.

## Launching

Once configured, you can launch the configured application from a shell on UNIX-like systems:

```shell
cd /path/to/automx2
contrib/flask.sh run
```

See [flask.sh](contrib/flask.sh) for a descriptions of additional parameter you can use, like hostname and port.

## Web server integration

In a production environment, it is recommended that you run automx2 behind a web server like Apache or NGINX, with
your web server acting as a reverse proxy, potentially also providing HTTPS support. If you do use a proxy, add
`proxy_count = 1` (adjust to number of proxies in call chain) to your configuration file. While automx2 will work
without this setting, only your proxy's IP address will be reported as a request source.

* Apache: TODO
* NGINX: [Example configuration snippet](contrib/nginx-sample.conf)
