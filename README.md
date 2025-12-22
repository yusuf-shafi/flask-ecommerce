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
flask-ecommerce/
├── app/
│ ├── init.py # App factory and configuration
│ ├── auth.py # Authentication routes
│ ├── views.py # Main application routes
│ ├── models.py # Database models
│
├── templates/ # Jinja2 templates
│ ├── base.html
│ ├── index.html
│ ├── football.html
│ ├── basketball.html
│ ├── running.html
│ ├── basket.html
│ ├── product_management.html
│ ├── sign_in.html
│ └── sign_up.html
│
├── static/
│ ├── assets/ # CSS, JS, fonts
│ └── img/ # Product and category images
│
├── run.py # Application entry point
├── requirements.txt # Python dependencies
└── README.md