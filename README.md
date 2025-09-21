# To-Do List Application

This is a full-stack, three-tier web application. It is a secure to-do list where users can register, log in, and manage their own private tasks. The project demonstrates the separation of concerns between a frontend user interface, a backend API for business logic, and a relational database for data persistence.


---

## Features

* **User Authentication:** Secure user registration and login using JWT (JSON Web Tokens).
    
* **Private To-Do Lists:** Each user can only view and manage their own tasks.
    
* **Full CRUD Functionality:** Create, Read, Update (mark as complete), and Delete tasks.
    
* **RESTful API:** A well-structured backend API to handle all application logic.
    

---

## Tech Stack & Architecture

This application uses a classic three-tier architecture:

* **Presentation Tier (Frontend):**
    
    * [React.js](https://reactjs.org/)
        
    * [React Router](https://reactrouter.com/) for page navigation.
        
    * [Axios](https://axios-http.com/) for making API requests.
        
* **Application Tier (Backend):**
    
    * [Python 3](https://www.python.org/)
        
    * [Flask](https://flask.palletsprojects.com/) as the web framework.
        
    * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) as the ORM.
        
    * [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/) for password hashing.
        
    * [PyJWT](https://pyjwt.readthedocs.io/) for generating and validating JSON Web Tokens.
        
* **Data Tier (Database):**
    
    * [PostgreSQL](https://www.postgresql.org/) for relational data storage.
        
    * [Psycopg2](https://www.psycopg.org/docs/) as the Python-PostgreSQL adapter.
        

```plaintext
+------------------+          +-----------------------+          +-----------------------+
|  React Frontend  |  <-----> |   Flask Backend API   |  <-----> |  PostgreSQL Database  |
| (localhost:3000) |          |   (localhost:5001)    |          |                       |
+------------------+          +-----------------------+          +-----------------------+
```

---

## Local Setup Instructions

Follow these steps carefully to get the application running on your local machine.

### Prerequisites

Make sure you have the following software installed on your system:

* [Git](https://git-scm.com/)
    
* [Node.js and npm](https://nodejs.org/en/download/) (v16 or higher)
    
* [Python 3 and Pip](https://www.python.org/downloads/) (v3.8 or higher)
    
* [PostgreSQL Server](https://www.postgresql.org/download/)
    

### 1\. Clone the Repository

First, clone this repository to your local machine.

Bash

```bash
git clone https://github.com/your-username/secure-todo-app.git
cd secure-todo-app
```

### 2\. Database Setup

1. Make sure your PostgreSQL server is running.
    
2. Connect to PostgreSQL and create the database for this project.
    
    SQL
    
    ```bash
    -- Using the psql command-line tool
    CREATE DATABASE todolist;
    ```
    
    The `users` and `todos` tables will be created automatically by the backend server on its first run.
    

### 3\. Backend Setup

1. Navigate to the `backend` directory.
    
    Bash
    
    ```bash
    cd backend
    ```
    
2. Create and activate a Python virtual environment.
    
    * **On macOS/Linux:**
        
        Bash
        
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
        
    * **On Windows:**
        
        Bash
        
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
        
3. Install all the required Python packages.
    
    Bash
    
    ```bash
    pip install Flask Flask-SQLAlchemy psycopg2-binary Flask-Bcrypt PyJWT Flask-Cors
    ```
    
4. Configure Environment Variables
    
    You must provide the database credentials and a secret key to the application.
    
    * In the `backend` directory, find the `app.py` file.
        
    * **Locate the configuration section** and replace the placeholder values with your actual PostgreSQL username and password.
        
    
    Python
    
    ```bash
    # File: backend/app.py
    
    # ...
    # --- Configuration ---
    # IMPORTANT: Change this secret key!
    app.config['SECRET_KEY'] = 'a-very-secret-key-that-you-should-change'
    
    # IMPORTANT: Update this with your PostgreSQL credentials!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/todolist'
    # ...
    ```
    
    For example, if your username is postgres and your password is admin123, the line should be:
    
    app.config\['SQLALCHEMY\_DATABASE\_URI'\] = 'postgresql://postgres:admin123@localhost/todolist'
    

### 4\. Frontend Setup

1. Navigate to the `frontend` directory from the project root.
    
    Bash
    
    ```bash
    cd ../frontend
    ```
    
2. Install all the required npm packages. This might take a few minutes.
    
    Bash
    
    ```bash
    npm install
    ```
    

---

## Running the Application

To run the application, you need **two separate terminals**.

### Terminal 1: Start the Backend Server

Bash

```bash
# Navigate to the backend directory
cd backend

# Make sure your virtual environment is activated
source venv/bin/activate

# Run the Flask server
python app.py
```

Your backend API is now running and listening for requests on `http://localhost:5001`.

### Terminal 2: Start the Frontend Application

```bash
# Navigate to the frontend directory
cd frontend

# Run the React development server
npm start
```

This will automatically open your default web browser to `http://localhost:3000`. You can now register a new user, log in, and start using the application!

---

## API Endpoints

The backend server provides the following RESTful API endpoints. All `/api/todos` routes require a valid JWT to be sent in the `x-access-token` header.

<table><tbody><tr><td colspan="1" rowspan="1"><p>Method</p></td><td colspan="1" rowspan="1"><p>Endpoint</p></td><td colspan="1" rowspan="1"><p>Description</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>POST</code></p></td><td colspan="1" rowspan="1"><p><code>/api/register</code></p></td><td colspan="1" rowspan="1"><p>Register a new user.</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>POST</code></p></td><td colspan="1" rowspan="1"><p><code>/api/login</code></p></td><td colspan="1" rowspan="1"><p>Log in a user and receive an auth token.</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>GET</code></p></td><td colspan="1" rowspan="1"><p><code>/api/todos</code></p></td><td colspan="1" rowspan="1"><p>Retrieve the logged-in user's to-do list.</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>POST</code></p></td><td colspan="1" rowspan="1"><p><code>/api/todos</code></p></td><td colspan="1" rowspan="1"><p>Create a new to-do for the user.</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>PUT</code></p></td><td colspan="1" rowspan="1"><p><code>/api/todos/&lt;int:id&gt;</code></p></td><td colspan="1" rowspan="1"><p>Update an existing to-do (e.g., complete).</p></td></tr><tr><td colspan="1" rowspan="1"><p><code>DELETE</code></p></td><td colspan="1" rowspan="1"><p><code>/api/todos/&lt;int:id&gt;</code></p></td><td colspan="1" rowspan="1"><p>Delete a to-do by its ID.</p></td></tr></tbody></table>

---

## Project Structure

```plaintext
secure-todo-app/
├── backend/
│   ├── venv/
│   └── app.py              # Main Flask application file
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js          # Main component with routing
│   │   ├── Login.js
│   │   └── Register.js
│   └── package.json
└── README.md
```