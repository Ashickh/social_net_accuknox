# Django Social Network Application

## Overview

This is a simple social network application built with Django and Django REST Framework. It includes functionalities for user registration, searching for users by email or name, sending/accepting/rejecting friend requests, listing friends, and listing pending friend requests.

## Features

- User Registration and Login
- Search for users by email or name (paginated)
- Send, accept, and reject friend requests
- List friends (users who have accepted friend requests)
- List pending friend requests
- Rate limiting on sending friend requests (max 3 requests per minute)

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package installer)

### Steps

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL database**

    - Create a PostgreSQL database:

        ```sql
        CREATE DATABASE social_db;
        ```

    - Create a PostgreSQL user with password:

        ```sql
        CREATE USER social_user WITH PASSWORD 'yourpassword';
        ```

    - Grant privileges to the user on the database:

        ```sql
        GRANT ALL PRIVILEGES ON DATABASE social_db TO social_user;
        ```

5. **Configure Django settings**

    Update the `DATABASES` setting in `settings.py` with your PostgreSQL database details:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'social_db',
            'USER': 'social_user',
            'PASSWORD': 'yourpassword',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    ```

6. **Run migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Create a superuser**

    ```bash
    python manage.py createsuperuser or run the script: python 1_superadmin_create
    ```

8. **Run the development server**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Registration

- **URL:** `/api/social_app/create-user/`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "email": "ashic@gmail.com",
        "username": "username",
        "password": "password"
    }
    ```

### User Login

- **URL:** `/api/social_app/login/`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "email": "ashic@gmail.com",
        "password": "password"
    }
    ```

### Search Users

- **URL:** `/api/social_app/search/?q=ashic`
- **Method:** `GET`
- **Parameters:**
    - `q`: search keyword (by email or name)

### Send Friend Request

- **URL:** `/api/social_app/send-friend-request/`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "to_user_id": "user_id"
    }
    ```

### Accept Friend Request

- **URL:** `/api/social_app/accept-friend-request/`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "from_user_id": "user_id"
    }
    ```

### Reject Friend Request

- **URL:** `/api/social_app/reject-friend-request/`
- **Method:** `POST`
- **Payload:**
    ```json
    {
        "from_user_id": "user_id"
    }
    ```

### List Friends

- **URL:** `/api/social_app/list-friends/`
- **Method:** `GET`

### List Pending Friend Requests

- **URL:** `/api/social_app/pending-list-friends/`
- **Method:** `GET`




