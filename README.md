# accounts-management

A django server to implement the problem statement posed in [problem-statement.md](problem-statement.md).

Queries that demonstrate the functionality can be found in [queries.md](queries.md)

Answers to the questions posed can be found in [thoughts.md](thoughts.md)

### Building the docker image

You can build docker image with `./build-image.sh`

### Running the server with docker

You can use docker-compose to start up the server and the mongo database it needs (as well as the mongo admin ui)
`docker-compose up -d`

You can then access the graphql playground at http://localhost:9000/graphql/

### Running the server without docker

You will need to set up your [python virtual environment](https://docs.python.org/3/library/venv.html) first

```shell
python -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Then, you will still need to start up the mongo server, by running
`docker-compose up -d`
This will also run a copy of the server on port 9000. If you do not want that, you can comment out the
"accounts_management" section of the docker-compose.yaml file.

Start the server with `./manage.py runserver`, and then access the graphql playground at
http://localhost:8000/graphql/

### Loading some example data

You can run `load-initial-data.py` to populate the Mongo database with some simple test data