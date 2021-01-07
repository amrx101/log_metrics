# log_metrics

log_metrics to extract insight from server logs.

# Features!

  - Retrieve insights about API requests.
  - 

### Installation
Requires Python 2.7 & pip

Optional(Install pip)

```shell script
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
pip install virtualenv
sudo /usr/bin/easy_install virtualenv
```

```sh
pip install virtualenv
```
Test the installation
```sh
virtualenv --version
```
Create a virtualenv
```sh
cd crserv
virtualenv venv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt

```

Running the Application
```sh
python main.py -l <log file location>
```

Running unit tests
```sh
pytest
```


### Todos

 - Dockerize the application
 - Kubernetes deployment config
 - Unit Tests

License
----

MIT

