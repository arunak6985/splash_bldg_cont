# Technology Stack

## Programming Languages
- **Python**: Primary backend language (Python 3.11 based on virtual environment)
- **HTML/CSS/JavaScript**: Frontend technologies for templates and static files

## Core Framework
- **Django 5.2.9**: Web framework for backend application
  - Django Admin: Built-in admin interface
  - Django ORM: Database abstraction layer
  - Django Templates: Template engine
  - Django Forms: Form handling and validation

## Database
- **PostgreSQL**: Production database
  - Database: postgres
  - Host: localhost
  - Port: 5432
- **SQLite3**: Development/fallback database (db.sqlite3)

## Key Dependencies
Based on virtual environment and project structure:
- **django**: Web framework (5.2.9)
- **psycopg2**: PostgreSQL adapter for Python
- **Pillow**: Image processing library (for cheque/resume handling)
- **pytesseract**: OCR capabilities (executable present in env)
- **numpy**: Numerical computing support
- **sqlparse**: SQL formatting utility

## Development Environment
- **Virtual Environment**: Python venv located in `env/` directory
- **Package Manager**: pip (pip 3.11)
- **Operating System**: Windows (based on .bat and .exe files in Scripts/)

## Project Configuration
- **Settings Module**: splash_bldg.settings
- **WSGI Application**: splash_bldg.wsgi.application
- **ASGI Application**: splash_bldg.asgi (async support)
- **Static Files**: Served from `/static/` URL
- **Media Files**: Served from `/media/` URL, stored in `media/` directory

## Development Commands

### Environment Activation
```bash
# Windows
env\Scripts\activate.bat

# PowerShell
env\Scripts\Activate.ps1
```

### Django Management
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Database Management
```bash
# Access Django shell
python manage.py shell

# Database shell
python manage.py dbshell

# SQL formatting
sqlformat [options]
```

## Security Configuration
- **SECRET_KEY**: Django secret key (should be environment variable in production)
- **DEBUG**: Currently True (must be False in production)
- **ALLOWED_HOSTS**: Currently empty (must be configured for production)
- **Custom Login**: LOGIN_URL = '/admin-login/', LOGIN_REDIRECT_URL = '/admin-vacancy-management/'

## File Upload Configuration
- **MEDIA_ROOT**: BASE_DIR / 'media'
- **MEDIA_URL**: '/media/'
- Upload directories: cheques/, resumes/
