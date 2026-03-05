# Student Result Management (SRM)

A Django-based web application for managing classes, subjects, students, notices, and academic results. It includes an admin dashboard for data management and a public result-check portal for students.

## Live Demo

- https://srm-4d9t.onrender.com/

## Features

- Admin authentication (`admin-login`) with protected dashboard pages.
- Class management:
  - Create, list, edit, and delete classes.
- Subject management:
  - Create, list, edit, and delete subjects.
- Subject combination mapping:
  - Assign subjects to classes.
  - Activate/deactivate subject combinations.
- Student management:
  - Add and edit student records (name, roll id, email, gender, DOB, class).
- Result management:
  - Add/update marks by class and student.
  - Manage declared results and edit existing marks.
  - Auto-compute total and percentage in result view.
- Notice board:
  - Add, edit, delete, and publish notices.
  - Public notice detail pages.
- Public result search:
  - Students can check results using roll id + class.

## Tech Stack

- Python
- Django
- SQLite (default database)
- Gunicorn (production server)
- WhiteNoise (static file serving)
- Render (deployment)

## Project Structure

```text
SRM/
|- StudentResultManagement/   # Django project settings and URL config
|- resultapp/                # Core app: models, views, templates, admin logic
|- staticfiles/              # Collected static files
|- manage.py
|- requirements.txt
|- render.yaml
|- db.sqlite3
```

## Quick Start (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/ninavevinay/SRM.git
cd SRM
```

### 2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create admin user

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Important Routes

- `/` - Home page
- `/search_result/` - Result search form
- `/check_result/` - Result output page
- `/admin-login/` - Custom admin login
- `/admin-dashboard/` - Admin dashboard
- `/admin/` - Django admin panel

## Deployment (Render)

This repository already includes `render.yaml`:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn StudentResultManagement.wsgi:application`

To deploy:

1. Push the latest code to GitHub.
2. Create a new Web Service in Render connected to this repository.
3. Render will detect and use `render.yaml`.

## Environment Notes

- `SECRET_KEY` is read from environment with a fallback value in `settings.py`.
- `DEBUG` is currently set to `False` in code.
- `ALLOWED_HOSTS` is currently `['*']`.

For production, set a secure `SECRET_KEY` and restrict `ALLOWED_HOSTS`.

## Recommended Improvements

- Add `.gitignore` updates to avoid committing virtual environment files.
- Add automated tests for models/views.
- Add role-based access control beyond superuser.
- Move configuration (`DEBUG`, hosts, DB) fully to environment variables.

## Author

- Vinay
