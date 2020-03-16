# gunicorn-python

A Gunicorn Docker base image with Python.

## Tags

* 3.8-alpine, latest
* 3.8

## Example Usage

Note: This image expects a module called "main" (e.g. main.py) in the /app directory, this should expose a variable called "app".

### No dependencies

If your app has no dependencies then you can simply run:

```bash
docker run -v /path/to/your/app:/app -p 80:80 dullage/gunicorn-python
```

### Dependencies

If you want to install dependencies then you can use this as a base image:


```dockerfile
FROM dullage/gunicorn-python:latest

COPY /path/to/your/app /app

RUN pip install --no-cache-dir -r /app/requirements.txt
```

```bash
docker build -t my-app .

docker run -p 80:80 my-app
```

## Environment Variables

WORKERS = Number of Gunicorn workers, defaults to 3

HOST = Gunicorn host, defaults to 0.0.0.0

PORT = Gunicorn port, defaults to 80
