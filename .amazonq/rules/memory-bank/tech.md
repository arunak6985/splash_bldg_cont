# Technology Stack and Development Setup

## Programming Languages and Versions

### Backend
- **Python**: Primary backend language
- **Django 5.2.9**: Web framework for rapid development
- **SQL**: Database queries and schema management

### Frontend
- **HTML5**: Markup and structure
- **CSS3/SCSS**: Styling and responsive design
- **JavaScript**: Client-side interactivity and AJAX
- **jQuery**: DOM manipulation and event handling

### Database
- **PostgreSQL**: Production database system
  - Host: localhost
  - Port: 5432
  - Database: postgres
- **SQLite**: Development database (db.sqlite3)

## Build Systems and Dependencies

### Python Environment
- **Virtual Environment**: `env/` directory for isolated dependencies
- **Package Management**: pip for Python package installation
- **Django ORM**: Database abstraction and migrations

### Static Asset Management
- **Static Files**: Served from `splash_bldg/static/`
- **Media Files**: User uploads stored in `media/`
- **SCSS Compilation**: Source files in `static/scss/`
- **Vendor Libraries**: Third-party assets in `static/vendor/`

### Key Django Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', 
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'site_application',
    'admin_panel',
]
```

### Middleware Stack
- SecurityMiddleware: Security headers and HTTPS
- SessionMiddleware: User session management
- CommonMiddleware: Common HTTP features
- CsrfViewMiddleware: CSRF protection
- AuthenticationMiddleware: User authentication
- MessageMiddleware: Flash messages
- ClickjackingMiddleware: Clickjacking protection

## Development Commands

### Project Setup
```bash
# Activate virtual environment
env\Scripts\activate

# Install dependencies
pip install django psycopg2-binary

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Development Server
```bash
# Start development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations admin_panel
python manage.py makemigrations site_application

# Apply migrations
python manage.py migrate

# Database shell
python manage.py dbshell
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Development static files served automatically
```

## Configuration Details

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres', 
        'PASSWORD': 'pass@272000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### File Upload Settings
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Security Settings
- DEBUG = True (development)
- SECRET_KEY configured
- CSRF protection enabled
- Custom login URL: '/admin-login/'
- Login redirect: '/admin-vacancy-management/'

### Template Configuration
- App-based template discovery
- Context processors for request, auth, messages
- Template inheritance for consistent layouts

## Development Environment
- **IDE**: Compatible with VS Code, PyCharm
- **Version Control**: Git-based workflow
- **Operating System**: Windows development environment
- **Browser Testing**: Modern browsers with JavaScript support