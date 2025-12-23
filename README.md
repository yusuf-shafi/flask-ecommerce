![CI](https://github.com/yusuf-shafi/flask-ecommerce/actions/workflows/ci.yml/badge.svg)

# Flask E-commerce Application

A simple e-commerce web application built with Flask.  
This project demonstrates backend-focused web development, including authentication, database modeling, and admin-managed product workflows.

## Features
- User registration and authentication
- Admin-only product management
- Product browsing by category
- Basket functionality
- Secure password hashing
- Server-side validation

## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite
- Bootstrap 5

## Project Structure
## Project Structure

```text
flask-ecommerce/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── views.py
│   ├── models.py
│   ├── templates/
│   └── static/
├── tests/
├── .env.example
├── pyproject.toml
├── requirements.txt
├── run.py
└── README.md


## Run locally

### 1) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

2) Install dependecies
pip install -r requirements.txt

3) Set environment variables
$env:SECRET_KEY="dev-secret"
$env:ADMIN_SIGNUP_KEY="admin-key"

