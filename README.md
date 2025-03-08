## Server Module

A backend application built with Python and FastAPI for user registration, authentication, post creation, and CRUD operations on users and posts. It uses MongoDB as the database and is containerized with Docker for quick deployment. The project follows a layered architecture (presentation, business logic, data access) for maintainability and utilizes OOP concepts like injection and inheritance for extensibility.

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
