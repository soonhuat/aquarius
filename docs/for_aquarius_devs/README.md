# Aquarius Documentation for Aquarius Developers

This documentation is for someone who wants to work on the Aquarius code itself, i.e. the code in the [oceanprotocol/aquarius repository](https://github.com/oceanprotocol/aquarius).

## General Ocean Dev Docs

For information about Ocean's Python code style and related "meta" developer docs, see [the oceanprotocol/dev-ocean repository](https://github.com/oceanprotocol/dev-ocean).

## Running Locally, for Dev and Test

First, clone this repository:

```bash
git clone git@github.com:oceanprotocol/aquarius.git
cd aquarius/
```

Then run some things that the Aquarius expects to be running:

```bash
cd docker
docker-compose up
```

You can see what that runs by reading [docker/docker-compose.yml](docker/docker-compose.yml).
Note that it runs MongoDB but the Aquarius can also work with BigchainDB or Elasticsearch.
It also runs [Ganache](https://github.com/trufflesuite/ganache) with all [Ocean Protocol Keeper Contracts](https://github.com/oceanprotocol/keeper-contracts) and [Ganache CLI](https://github.com/trufflesuite/ganache-cli).

The most simple way to start is:

```bash
pip install -r requirements_dev.txt # or requirements_conda.txt if using Conda
export FLASK_APP=aquarius/run.py
export CONFIG_FILE=config.ini
./scripts/deploy
flask run
```

That will use HTTP (i.e. not SSL/TLS).

The proper way to run the Flask application is using an application server such as Gunicorn. This allow you to run using SSL/TLS.
You can generate some certificates for testing by doing:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

and when it asks for the Common Name (CN), answer `localhost`

Then edit the config file `config.ini` so that:

```yaml
aquarius.url = http://localhost:5000
```

Then execute this command:

```bash
gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:5000 -w 1 aquarius.run:app
```

## Configuration

You can pass the configuration using the CONFIG_FILE environment variable (recommended) or locating your configuration in config.ini file.

In the configuration there are now two sections:

- oceandb: Contains different values to connect with oceandb. You can find more information about how to use OceanDB [here](https://github.com/oceanprotocol/oceandb-driver-interface).
- resources: In this section we are showing the url in wich the aquarius is going to be deployed.

    ```yaml
    [resources]
    aquarius.url = http://localhost:5000
    ```

## Testing

Automatic tests are set up via Travis, executing `tox`.
Our tests use the pytest framework.

## New Version

The `bumpversion.sh` script helps bump the project version. You can execute the script using `{major|minor|patch}` as first argument, to bump the version accordingly.