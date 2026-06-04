# Books

A simple FastAPI TODO sample project to play around with FastAPI, Pydantic, SQLite and SQLAlchemy.

## Prerequisites

1. Install Python >= 3.14.2: https://www.python.org/downloads/
2. Optional Install git: https://git-scm.com/install/
3. Optional sqlite3: https://sqlite.org/download.html
4. Docker: https://www.docker.com/products/docker-desktop/ or Rancher Desktop: https://rancherdesktop.io/

## Setup the project

1. Clone this repository: `git clone https://github.com/boghas/FastAPI-ToDo.git` or download the project archive and extract the contents.
2. Create a virtual environment: `python -m venv .venv`.
3. Activate the virtual environment: On Windwows: `.venv/Scripts/activate`.
4. Install dependencies: `pip install -r requirements.txt`
5. Inside the root of the project create a `.env` file and populate it with the following environment variables:
```
JWT_SECRET_KEY=<YOUR_JWT_SECRET_KEY>
JWT_ALGORITHM=HS256
<!-- DATABASE_URL=sqlite:///./todosapp.db -->
DATABASE_URL=postgresql+psycopg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/<POSTGRES_DB>
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_USER=<your-postgres-admin-user>
POSTGRES_PASSWORD=<your-postgres-admin-password>
POSTGRES_DB=todosdb
```
6. To generate a new JWT secret key you can put any string you want, but if you want more security you can generate a stronger one by using OpenSSL: ` .\openssl rand -hex 32`
7. Run the application:
    - To run it in development mode: `uvicorn main:app --reload` or `fastapi dev main.py`.
    - To run it in production mode: `fastapi run main.py`.

## Running production database with PostgreSQL and Docker

To start the PostgreSQL container run `docker compose --env-file .env -f postgresql/docker-compose.yaml up -d`

To connect to the shell console of the container run: `docker exec -it <container-name> bash`. Example: `docker exec -it postgres-todoapp bash`

To connect to the psql of the container run: `docker exec -it <container-name> psql -U <postgresql-username> -d <db-name>`. Example: `docker exec -it postgres-todoapp psql -U pgadmin -d todosdb`.

To check that the environment variables were loaded correctly: `docker compose --env-file .env -f postgresql/docker-compose.yaml config`

To create the two tables the app uses using psql:

1. Connect to psql: `docker exec -it <container-name> psql -U <postgresql-username> -d <db-name>`
2. Run the sql script:
```
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  hashed_password varchar(200) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS todos;

CREATE TABLE todos (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  owner_id integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

To list the tables: `\dt`.

To describe a table: `\d <table-name>

To shut down the container: `docker compose -f postgresql/docker-compose.yaml down`

To shut down the container and remove the volume (the data will be lost): `docker compose -f postgresql/docker-compose.yaml down -v`

## Initializing alembic

To initialize alembic into the project run the following command: `alembic init <your_environment_name>` Example: `alembic init alembic`.

To test that alembic sees the tables run: `alembic revision --autogenerate -m "initial"'

### Running revisions

To run a new revision run: `alembic revision -m "<revision-message>"` and modify the revision code for `upgrade` and `downgrade` in `alembic/versions/<version_id>.py`

To run the upgrade run: `alembic upgrade <revision_id>`. Don't forget to also update your models.

Example:

```alembic/versions/4cce4b8846da_create_phone_number_for_user_column.py
...
def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
```

```models/user_model.py
from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
```