# Technology Stack

## Programming Languages and Frameworks

### Backend
- **Python**: Primary programming language
- **Django 5.2.9**: Web framework for rapid development
- **Django ORM**: Database abstraction layer

### Frontend
- **HTML/CSS**: Template markup and styling
- **JavaScript**: Client-side interactivity
- **Django Templates**: Server-side template rendering

### Database
- **PostgreSQL**: Production database system
  - Host: localhost
  - Port: 5432
  - Database: postgres
- **SQLite**: Development/testing database (db.sqlite3)

## Development Environment

### Virtual Environment
- **Location**: `env/` directory
- **Python Version**: 3.11 (based on pip3.11.exe presence)
- **Activation**: `env/Scripts/activate.bat` (Windows)

### Key Dependencies
- **Django**: Web framework
- **NumPy**: Data processing capabilities
- **SQL Formatter**: Database query formatting
- **Normalizer**: Text processing utilities

## Build System and Commands

### Django Management
- **Entry Point**: `manage.py`
- **Settings Module**: `splash_bldg.settings`

### Common Development Commands
```bash
# Activate virtual environment
env\Scripts\activate.bat

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Configuration Details

### Static Files
- **URL**: `/static/`
- **Directory**: `splash_bldg/static/`
- **Served by**: Django development server

### Media Files
- **URL**: `/media/`
- **Root**: `media/` directory
- **Purpose**: User uploads (resumes, documents)

### Security Settings
- **Debug Mode**: Enabled (development)
- **Secret Key**: Configured (should be environment variable in production)
- **CSRF Protection**: Enabled
- **Authentication**: Django built-in system

### URL Configuration
- **Root URLconf**: `splash_bldg.urls`
- **Custom Login**: `/admin-login/`
- **Login Redirect**: `/admin-vacancy-management/`

## Deployment Considerations
- **WSGI Application**: `splash_bldg.wsgi.application`
- **Template Backend**: Django templates with app directories
- **Internationalization**: English (en-us), UTC timezone
- **Password Validation**: Django standard validators enabled