# Best Practices and Coding Conventions

This document outlines the best practices and coding conventions used in this FastAPI project. Following these guidelines will help maintain code quality, consistency, and ease of maintenance.

## 1. Project Structure

The project follows a modular and layered architecture, with the main application code residing in the `app` directory. The structure is as follows:

```
app/
├── base/           # Base classes and utilities
├── config/         # Application configuration
├── controllers/    # API endpoint definitions (routers)
├── dependency/     # FastAPI dependency injection setup
├── models/         # SQLAlchemy ORM models
├── routers/        # (If used) API router modules
├── schemas/        # Pydantic schemas for data validation
├── services/       # Business logic layer
├── utils/          # Utility functions
├── __init__.py
└── main.py         # Application entry point
```

- **`main.py`**: The main entry point of the application. It creates the FastAPI app instance, includes routers, and sets up middleware.
- **`controllers/`**: Each file in this directory corresponds to a specific API module (e.g., `user_controller.py`). It defines the API routes, handles request and response cycles, and calls the appropriate service for business logic.
- **`services/`**: This layer contains the core business logic of the application. Services are responsible for interacting with the database (via models) and performing any necessary computations or data manipulations.
- **`models/`**: Defines the SQLAlchemy ORM models, which represent the database tables.
- **`schemas/`**: Contains Pydantic schemas used for request body validation, response serialization, and data transfer between layers.
- **`dependency/`**: Manages dependencies for FastAPI's dependency injection system, such as database sessions, service instances, and authentication.
- **`base/`**: Contains base classes that provide common functionality, such as `BaseRouter`, `BaseService`, and standardized response functions.

## 2. Controllers

Controllers are responsible for handling HTTP requests and returning responses.

- **Routing**: Use the `BaseRouter` class to create and manage routers for each module. This ensures a consistent URL structure and dependency management.
- **Dependency Injection**: Inject services, database sessions, and other dependencies using the functions defined in the `dependency/` directory (e.g., `user_service_dependency`, `db_dependency`).
- **Response Format**: Use the standardized response functions (`response_json`, `response_json_pagination`) from the `app.base` module to ensure a consistent JSON response structure across all endpoints.
- **Error Handling**:
    - Wrap endpoint logic in a `try...except` block.
    - Catch specific `HTTPException`s and re-raise them.
    - Catch generic `Exception`s and raise a custom `InternalServerException` to provide a standardized internal server error response.

**Example:**
```python
# app/controllers/user_controller.py

from fastapi import HTTPException, status
from app.base import *
from app.dependency.deps import user_service_dependency, db_dependency
from app.schemas.user_schema import UserReadSchema, UserCreateSchema

class UserController(BaseRouter):
    base_router = BaseRouter(module="User")
    router = base_router.get_router()

    @router.post("", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[UserReadSchema])
    async def create_user(
        create_schema: UserCreateSchema,
        db: db_dependency,
        service: user_service_dependency,
    ):
        try:
            data = await service.create_user(create_schema, db)
            return response_json(
                message="Successfully register new user",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e, create_schema)
```

## 3. Services

Services contain the core business logic of the application.

- **Base Service**: Inherit from the `BaseService` class to get common CRUD (Create, Read, Update, Delete) functionality.
- **Database Interaction**: Services are the only layer that should directly interact with the database (via the injected `db` session).
- **Error Handling**: Raise custom exceptions (e.g., `NotFoundException`) when a resource is not found or a business rule is violated. These exceptions are then caught and handled in the controller layer.
- **Data Conversion**: Services should handle the conversion between Pydantic schemas and SQLAlchemy models where necessary.

**Example:**
```python
# app/services/user_service.py

from app.base import *
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreateSchema

class UserService(BaseService):
    model = User
    module = "user"

    async def get_user_by_id(self, id: str, db: Session):
        data = await self.get_by_id(id=id, db=db)
        if not data:
            raise NotFoundException("User", data={"user_id": id})
        return data

    async def create_user(self, user_schema: UserCreateSchema, db: Session):
        # Business logic for creating a user
        ...
```

## 4. Dependency Injection

- **Centralized Dependencies**: Define all dependencies in the `app/dependency/deps.py` file. This makes them easy to manage and reuse across the application.
- **Typed Dependencies**: Use type hints for injected dependencies to improve code completion and static analysis.

## 5. Error Handling

- **Custom Exception Handlers**: The `app/main.py` file defines custom exception handlers for `RequestValidationError` and `ValueError` to provide consistent error responses.
- **Custom Exceptions**: Use custom exception classes defined in `app/base/base_error.py` (e.g., `NotFoundException`, `InternalServerException`) to represent specific error scenarios in the service layer.

## 6. Naming Conventions

- **Modules/Files**: Use snake_case for filenames (e.g., `user_controller.py`).
- **Classes**: Use PascalCase for class names (e.g., `UserService`, `UserCreateSchema`).
- **Functions/Methods/Variables**: Use snake_case for functions, methods, and variables (e.g., `get_user_by_id`, `create_schema`).
- **API Endpoints**: Use kebab-case for URL paths where necessary (e.g., `/change-password`).