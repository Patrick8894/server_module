## Server Module

### To start traefik, run the command:
```
docker compose -f docker-compose-traefik.yml up --build
```
### To stop traefik, first stop server, then run the command:
```
docker compose -f docker-compose-traefik.yml down
```

### To start fastapi server, run the command:
```
docker compose -f docker-compose.yml -f docker-compose-debug.yml up --build
```
### To stop fastapi server, run the command:
```
docker compose -f docker-compose.yml -f docker-compose-debug.yml down
```