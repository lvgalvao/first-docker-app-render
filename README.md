Esse projeto é instalado via docker

```bash
git clone ...
```

```bash
docker build -t first-docker-app .
```

```bash
docker run -d -p 8501:8501 --name my-first-container first-docker-app
```