## Server Module

### To start traefik, run the command:
```
docker compose -f docker-compose-traefik.yml up -d --build
```
### To stop traefik, run the command:
```
docker compose -f docker-compose.yml -f docker-compose-debug.yml -f docker-compose-traefik.yml down
```

### To start fastapi server, run the command:
```
docker compose -f docker-compose.yml -f docker-compose-debug.yml up --build
```