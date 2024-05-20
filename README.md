# FastAPI Address Book

A minimal API for an address book using FastAPI where users can create, update, delete, and retrieve addresses based on coordinates and distance.

## Features

- Create, read, update, and delete addresses
- Retrieve addresses within a given distance from specified coordinates
- Data validation using Pydantic
- SQLite database integration

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:

   git clone https://github.com/yourusername/fastapi-address-book.git
   cd fastapi-address-book

2.Create and activate a virtual environment:

For Windows:

python -m venv venv
venv\Scripts\activate

For macOS and Linux:

python3 -m venv venv
source venv/bin/activate

3.Install dependencies:

pip install -r requirements.txt

Or

pip install fastapi uvicorn sqlalchemy databases pydantic geopy

4.Create the main.py File
Ensure you have the complete main.py file from the previous steps.

### Running the Application

1.Ensure you are in the project directory:

cd fastapi-address-book

2.Run the FastAPI application:

uvicorn main:app --reload

The --reload flag makes Uvicorn restart the server when you change the code, which is useful during development.

3.Test the Endpoints
Open your web browser and go to http://127.0.0.1:8000/docs to access the interactive API documentation.
