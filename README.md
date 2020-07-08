# gunicorn

A Gunicorn Docker base image with Python.

## Tags

* 20.0-python3.8-alpine3.12, latest
* 20.0-python3.8

## Example Usage

Use this image as a base:

```dockerfile
FROM dullage/gunicorn:20.0-python3.8-alpine3.12

COPY /path/to/your/app /app

RUN pip install --no-cache-dir -r /app/requirements.txt
```

```bash
docker build -t my-app .

docker run -p 80:8080 my-app
```

## Entrypoint / Default Command

The entrypoint is `gunicorn` and the default command is `-b 0.0.0.0:8080 -w 3 main:app` < Bind to all interfaces on port 8080 (inside the container), load a module called 'mail' with a variable called 'app'.

The default command can be overridden as required. Example:

```bash
docker run -p 80:8080 my-app -b 0.0.0.0:8080 -w 1 myapp:app
```
