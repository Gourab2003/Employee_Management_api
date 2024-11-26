# Employee Management API

This project is a simple RESTful API for managing employee data. It allows basic CRUD operations such as adding, updating, deleting, and retrieving employee details.

## Features

- Add new employee details
- Update existing employee details
- Delete employee records
- Fetch employee data by ID
- Search employees by department or name

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/employee-management-api.git
    ```
2. Navigate to the project directory:
    ```bash
    cd employee-management-api
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database (ensure MySQL is installed and running):
    ```bash
    flask db upgrade
    ```

5. Start the Flask application:
    ```bash
    python app.py
    ```

## API Reference

### Get all employees

```http
GET /api/employees
