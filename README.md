# automx2: Email client configuration made easy

Successor to _automx_, designed to be easier to configure and use.
Written by [Ralph Seichter](https://gitlab.com/rseichter) for [sys4 AG](https://sys4.de/).
The [project home](https://gitlab.com/automx/automx2) resides on GitLab and is
[mirrored](https://github.com/rseichter/automx2) to GitHub.

_This software is considered to be in Beta state, so make sure to use protection._

# Installing from scratch

**Do not execute the manual installation procedure as root!** The application does not require super user
privileges. It is recommended that you create a user account specifically for automx2, but other unprivileged users
will do as well.

1.  Check the output of `python3 --version` on your machine to verify that the command executes Python 3.7 or higher.
If you see version 3.6 or lower, you'll need to either change the active Python version for the shell session or edit
`setupvenv.sh` after downloading the script in step #3.

2.  Prepare installation directory.
```shell
mkdir -p /path/to/automx2
cd /path/to/automx2
```

3.  Download virtual environment [setup script](https://gitlab.com/automx/automx2/blob/master/contrib/setupvenv.sh).
```shell
wget -O setupvenv.sh 'https://gitlab.com/automx/automx2/raw/master/contrib/setupvenv.sh?inline=false'
chmod u+x setupvenv.sh
```

4.  Execute setup script. It creates a Python virtual environment `venv` in the current directory.
```shell
./setupvenv.sh
```

5.  Activate virtual environment and install the latest automx2 release from [PyPI](https://pypi.org/project/automx2/).
Make sure to pick the correct activation for your shell from the `venv/bin` directory. This is an example for BASH.
```shell
. venv/bin/activate
pip install automx2
```

# Updating

An existing installation can be updated like this:

```shell
. venv/bin/activate
pip install -U automx2
```

# Configuring

When run by user `alice`, automx2 attempts to load configuration data from the following files, in the specified order,
stopping at the first match:

1.  Value of `AUTOMX2_CONF` environment variable (if available)
2.  `~alice/.automx2.conf` (note the leading dot)
3.  `/etc/automx2/automx2.conf`
4.  `/etc/automx2.conf`

While automx2 can be launched without a configuration file, the internal defaults are only suitable for testing, in
particular because an in-memory sqlite database will be used, meaning all data is lost once the application terminates.

The file format is an [INI variant](https://docs.python.org/3.7/library/configparser.html#supported-ini-file-structure).
An example configuration file is available
[here](https://gitlab.com/automx/automx2/blob/master/contrib/automx2-sample.conf). A minimal configuration file only
needs to contain one `db_uri` entry in the defaults section, pointing to a non-transient database.

# Database support

This application uses the excellent SQLAlchemy toolkit which supports various SQL
[dialects](https://docs.sqlalchemy.org/dialects/). While you probably already have SQLite support available on your
local machine, you may need to install additional Python packages for PostgreSQL, MySQL, etc. Detailed instructions
to support a particular database dialect are out of scope for this document, but there are numerous guides available.

# Launching

Once configured, you can launch the configured application from a shell on UNIX-like systems:

```shell
cd /path/to/automx2
contrib/flask.sh run
```

See [flask.sh](https://gitlab.com/automx/automx2/blob/master/contrib/flask.sh) for a descriptions of additional
parameter you can use, like hostname and port.

# Web server integration

In a production environment, it is recommended that you run automx2 behind a web server like Apache or NGINX, with
your web server acting as a reverse proxy, potentially also providing HTTPS support. If you do use a proxy, add
`proxy_count = 1` (adjust to number of proxies in call chain) to your configuration file. While automx2 will work
without this setting, only your proxy's IP address will be reported as a request source.

1.  Apache: TODO
2.  NGINX: [Example configuration](https://gitlab.com/automx/automx2/blob/master/contrib/nginx-sample.conf)
