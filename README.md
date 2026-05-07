# Books

A simple FastAPI TODO sample project to play around with FastAPI and Pydantic and SQLite.

## Prerequisites

1. Install Python >= 3.14.2: https://www.python.org/downloads/
2. Optional Install git: https://git-scm.com/install/

## Setup the project

1. Clone this repository: `git clone https://github.com/boghas/FastAPI-ToDo.git` or download the project archive and extract the contents.
2. Create a virtual environment: `python -m venv .venv`.
3. Activate the virtual environment: On Windwows: `.venv/Scripts/activate`.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application:
    - To run it in development mode: `uvicorn books:app --reload` or `fastapi dev books.py`.
    - To run it in production mode: `fastapi run books.py`.