# Automate With Django

A Django-based automation platform inspired by “Automate the Boring Stuff”.  
This project provides multiple utilities that automate common backend and productivity-related tasks such as importing/exporting CSV data, bulk emailing, email tracking, and image compression.

---

## Live Demo

https://automate-with-django-volu.onrender.com

---

# Features

## 0. User Authentication System
- Implemented Django’s built-in authentication system
- User registration, login, and logout functionality
- Admin authentication support

---

## 1. Import Data
- Upload CSV files directly into the database
- Dynamically imports records into selected tables/models
- Simplifies bulk database insertion without manual SQL queries

---

## 2. Export Data
- Export database records into CSV format
- CSV file is automatically sent as an email attachment to the logged-in user
- Useful for reports, backups, and data sharing

---

## 3. Bulk Emails
- Send bulk emails to multiple users
- Implemented using Celery for asynchronous task processing
- Prevents blocking the main request-response cycle

---

## 4. Email Tracking
Tracks:
- Email open rates
- Email click rates

Useful for monitoring email engagement and analytics.

---

## 5. Compress Images
- Compresses uploaded image files
- Reduces image size while maintaining reasonable quality
- Helps optimize storage and performance

---

# Tech Stack

- Python
- Django
- Celery
- Redis
- SQLite / PostgreSQL
- Bootstrap
- WhiteNoise
- Render

---

# Deployment

The application is deployed on Render.

Static files are served using WhiteNoise.

---

# Important Production Notes

## Media Files on Render
Render free instances do not provide persistent local storage for media files.

Because of this:
- Uploaded media files may disappear after instance restart
- Media visibility may not work consistently in production
- Every restart creates a fresh ephemeral filesystem

Static files work correctly because they are served using WhiteNoise.


## Celery Worker Limitation on Render Free Tier

In local development:
- Celery + Redis is used for asynchronous background task processing

However, Render free tier does not provide free background worker services.

Therefore:
- A synchronous fallback process has been implemented for production deployment
- The repository still contains the complete asynchronous Celery implementation for local development and scalable deployments

---

# Local Development Setup

## Clone Repository

```bash
git clone https://github.com/Sagarsingh-git1/automate_with_django
cd AWD
```

---

## Create Virtual Environment

```bash
python -m venv env
```

---

## Activate Virtual Environment

### macOS/Linux

```bash
source env/bin/activate
```

### Windows

```bash
env\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Start Redis Server

Make sure Redis is running locally.

---

## Start Celery Worker

```bash
celery -A awd_main worker --loglevel=info
```

---

## Run Development Server

```bash
python manage.py runserver
```

---


# Future Improvements

- Cloud storage integration for media files
- Docker support
- User dashboard analytics
- Scheduled email campaigns
- Multi-format export support (Excel/PDF)

---

# Demo Credentials (For Recruiters only)

Recruiters can either:

- Register a new account and explore the application
- Or use the demo credentials below
  
Username: sunitasinha
Password: Sunita@123

---

# Author

Sagar Singh  
Python & Django Backend Developer
