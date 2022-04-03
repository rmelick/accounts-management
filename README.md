# accounts-management

A django server to implement the problem statement posed in [problem-statement.md](problem-statement.md).

Answers to the questions posed can be found in [thoughts.md](thoughts.md)

### Building the docker image

Build docker image with `./build-image.sh`

### Running the server

You will need to set up your [python virtual environment](https://docs.python.org/3/library/venv.html) first

```shell
python -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Start the server with `./manage.py runserver`, and then access the graphql playground at
http://localhost:8000/graphql/

