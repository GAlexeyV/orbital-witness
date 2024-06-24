# Orbital Witness Project

## Overview
This is a web application build with a FastAPI backend and a React frontend. The backend handles API requests, 
while the frontend provides a user interface for interacting with the application.

## Running the app with Docker Compose
Navigate to a root folder and execute: `docker-compose up --build`

- Backend endpoint could be accessed on: http://0.0.0.0:8000/usage
- Frontend could be accessed on: http://localhost:3000/dashboard

## Backend Dependencies
Dependencies are managed using Poetry. The main dependencies are:
- Python 3.9
- FastAPI
- Requests
- HTTPX
- Pydantic
- Pytest
- Pytest-asyncio

## Running the Backend
1. Navigate to a server folder: `cd server`
2. Optional: create and activate virtual environment. Create: `python3 -m venv <myenvname>`. Activate: `source <myenvname>/bin/activate`
3. Install dependencies: `poetry install`
4. Run the application: `poetry run python ./app.py &`

- The backend will be running on http://0.0.0.0:8000
- Frontend on: http://0.0.0.0:8000/usage

## Frontend Dependencies
Dependencies are managed using npm. The main dependencies are:
- React
- React-DOM
- Axios
- Chart.js
- Date-fns
- Material-UI
- Testing Libraries
- Babel

## Frontend Setup
1. Navigate to the client directory: cd client
2. Install dependencies: npm install
3. Run the application: npm start

- The frontend will be running on http://0.0.0.0:3000.
- Dashboard on http://localhost:3000/dashboard

## Testing

## Backend
To run tests for the backend:
1. Navigate to the server directory: cd server
2. Run the tests: poetry run pytest 

## Frontend
To run tests for the frontend: 
1. Navigate to the client directory: cd client
2. Run the tests: npm test

## Rational
The decisions made for this project were dictated mostly by personal preferences, task requirements and time limitations.
In project requirements it is mentioned that API is supposed to be built with python. I decided to go with FastAPI framework
mostly for personal preferences as other frameworks, e.g. Flask could also fulfill the requirements. Nevertheless, I would
like to highlight some important from my point of view advantages of FastAPI which I think quite useful:
- Pydantic data schema: it helps to validate that accepted and returned data in a required shape.
- Fast: high performance, especially consider that this is a python app.
- Async nature: the project could be fulfilled using sync mode, but I think doing async request and making calculations 
  in async mode could boost performance especially considering there are quite a lot of string manipulations.
- Standards-based: FastAPI is based on (and fully compatible with) the open standards for APIs.
- Automatic Swagger documentation generation.

For a frontend I went with React because it was mentioned in requirements, and I am mostly familiar with this frontend library.
I did not use any frameworks e.g. Next.js, Gatsby, etc. as I think it is an overkill for such project.
I used relatively simple packages (mentioned in frontend dependencies) to fulfill the requirements: e.g. for preserving
filters I used "useLocation" and "useNavigate" hooks from "react-router-dom", for getting data from the backend 
I went with "axios" (Promise based HTTP client). I also decided to go with Typescript even though JavaScript could
be enough for this project because I consider it is better to start the project with it from the beginning then 
to rewrite it later (from previous work experience). Typescript provides type validation which is useful to verify
that right data shape accepted and returned.

The requirement about data correctness: "It is critical that the usage data we provide to our customers is accurate..."
is mostly achieved by using Pydantic data schema, data types in Python, Typescript types and tests.
There are definitely improvements which could be made to satisfy this requirement even bette e.g. write more
comprehensive test suits, check that received and returned data is in specific data range, etc.


## Things to improve
Because of time limitations and I suppose as it is not a goal of this task, the project is not production ready. 
By this I mean:
- It is not fully tested: tests are not provided for each module, there are no visual tests, stories, etc.
- There is no logging.
- There is no monitoring.
- There is no rollback policy for Docker / deployment.
- There is no caching.
- Optional: no saving of data to a database.
- Design is mediocre.
- Etc







