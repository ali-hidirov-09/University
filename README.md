# 🎓 University Management API

A RESTful backend API for managing university structure, students, teachers, and academic grades. Built with Django REST Framework.

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Environment Variables](#environment-variables)

---

## About

This project is a backend API system for university administration. It allows managing the full hierarchy of a university: from the university itself down to faculties, departments (kafedra), subjects, groups, students, teachers, and student grades.

---

## Features

- Full CRUD for university entities (University → Faculty → Kafedra → Subject → Group)
- Student and Teacher registration linked to Django's built-in User model
- Grade management with semester tracking (1–8)
- Role-based access control:
  - **Admin/Staff** — full access to all resources
  - **Teacher** — can manage grades for their department's subjects
  - **Student** — can only view their own grades
- JWT-based authentication with email activation
- Filtering and search on all endpoints
- Swagger / ReDoc API documentation
- Dockerized for easy deployment

---

## Tech Stack

- **Python** 3.11
- **Django** 5.2
- **Django REST Framework** 3.16
- **SimpleJWT** — JWT authentication
- **Djoser** — user registration, email activation, password reset
- **drf-yasg** — Swagger UI & ReDoc documentation
- **django-filter** — advanced filtering
- **Docker** + **Docker Compose**

---

## Project Structure

```
university_project/
├── config/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── university/              # Main application
│   ├── models/
│   │   ├── misc.py          # University, Faculty, Kafedra, Teacher
│   │   └── subject.py       # Subject, Group, Student, Grade
│   ├── views/
│   │   ├── misc.py          # University, Faculty, Kafedra, Subject, Group, Student ViewSets
│   │   └── grade.py         # Grade, Teacher ViewSets
│   ├── serializers/
│   │   ├── misc.py
│   │   └── grade.py
│   ├── services/
│   │   └── misc.py          # Business logic: create_teacher, create_student
│   ├── filters.py           # FilterSet classes
│   ├── permissions.py       # Custom DRF permissions
│   └── urls.py
├── dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## Getting Started

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd university_project
   ```

2. **Create a `.env` file** (see [Environment Variables](#environment-variables))

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Create a superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

The API will be available at `http://localhost:8000`

---

### Option 2: Manual Setup

1. **Clone and enter the project**
   ```bash
   git clone <repository-url>
   cd university_project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** (see below)

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

Interactive documentation is available at:

| URL | Description |
|-----|-------------|
| `/` | Swagger UI |
| `/redoc/` | ReDoc UI |

### Core Resources

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/v1/University/` | GET, POST | List / create universities |
| `/api/v1/Faculty/` | GET, POST | List / create faculties |
| `/api/v1/Kafedra/` | GET, POST | List / create departments |
| `/api/v1/Subject/` | GET, POST | List / create subjects |
| `/api/v1/Group/` | GET, POST | List / create groups |
| `/api/v1/Student/` | GET, POST | List / create students |
| `/api/v1/Teacher/` | GET, POST | List / create teachers |
| `/api/v1/Grade/` | GET, POST | List / create grades |

All endpoints support `GET <id>`, `PUT <id>`, `PATCH <id>`, `DELETE <id>`.

### Authentication Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/auth/users/` | Register new user |
| `/api/v1/auth/users/activation/` | Activate account via email |
| `/api/v1/auth/token` | Obtain JWT token pair |
| `/api/v1/auth/token/refresh` | Refresh access token |
| `/api/v1/auth/token/verify` | Verify token validity |
| `/api/v1/auth/users/reset_password/` | Request password reset |

---

## Authentication

This API uses **JWT (JSON Web Token)** authentication.

1. Register via `POST /api/v1/auth/users/`
2. Activate your account via the email link
3. Obtain tokens via `POST /api/v1/auth/token`
4. Include the token in all requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

**Token lifetimes:**
- Access token: 2 hours
- Refresh token: 1 day

---

## Permissions

| Role | Access |
|------|--------|
| **Unauthenticated** | Read-only on most resources |
| **Student** | Read-only; can only see their own grades |
| **Teacher** | Full CRUD on grades within their department |
| **Staff/Admin** | Full access to everything |

---

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key-here

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

---

## Author

Built as a learning project after 8 months of Python backend development study.