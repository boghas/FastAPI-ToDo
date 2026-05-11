# Books

A simple FastAPI TODO sample project to play around with FastAPI, Pydantic, SQLite and SQLAlchemy.

## Prerequisites

1. Install Python >= 3.14.2: https://www.python.org/downloads/
2. Optional Install git: https://git-scm.com/install/
3. Optional sqlite3: https://sqlite.org/download.html

## Setup the project

1. Clone this repository: `git clone https://github.com/boghas/FastAPI-ToDo.git` or download the project archive and extract the contents.
2. Create a virtual environment: `python -m venv .venv`.
3. Activate the virtual environment: On Windwows: `.venv/Scripts/activate`.
4. Install dependencies: `pip install -r requirements.txt`
5. Inside the root of the project create a `.env` file and populate it with the following environment variables:
```
JWT_SECRET_KEY=<YOUR_JWT_SECRET_KEY>
JWT_ALGORITHM=HS256
DATABASE_URL=sqlite:///./todosapp.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
6. To generate a new JWT secret key you can put any string you want, but if you want more security you can generate a stronger one by using OpenSSL: ` .\openssl rand -hex 32`
7. Run the application:
    - To run it in development mode: `uvicorn main:app --reload` or `fastapi dev main.py`.
    - To run it in production mode: `fastapi run main.py`.

## Changing Secret Key

To generate a new secret key for JWT authorization