# Project Structure

## Directory Organization

### Root Structure
```
splash_bldg_cont/
├── env/                    # Python virtual environment
├── splash_bldg/           # Main Django project directory
└── .amazonq/              # Amazon Q configuration and rules
```

### Main Application Structure
```
splash_bldg/
├── admin_panel/           # Administrative functionality app
├── site_application/      # Public job application app
├── splash_bldg/          # Django project configuration
├── media/                # User uploaded files (resumes)
├── db.sqlite3           # Database file
└── manage.py            # Django management script
```

## Core Components and Relationships

### Django Applications

#### admin_panel/
- **Purpose**: Administrative interface for managing vacancies and applications
- **Key Components**:
  - `views_yesterday.py` - Historical data views
  - `bulk_pdf_views.py` - Bulk document processing
  - `models.py` - Administrative data models
  - `templates/` - Admin interface templates
  - `management/` - Custom Django commands

#### site_application/
- **Purpose**: Public-facing job application system
- **Key Components**:
  - `models.py` - Application and job data models
  - `views.py` - Public interface logic
  - `templates/` - Public website templates
  - `migrations/` - Database schema changes

#### splash_bldg/ (Project Configuration)
- **Purpose**: Django project settings and configuration
- **Key Components**:
  - `settings.py` - Application configuration
  - `urls.py` - URL routing
  - `static/` - CSS, JavaScript, and image assets
  - `wsgi.py` - Web server gateway interface

## Architectural Patterns

### Model-View-Template (MVT) Architecture
- **Models**: Database layer handling job applications, vacancies, and user data
- **Views**: Business logic processing requests and responses
- **Templates**: HTML presentation layer with dynamic content

### Application Separation
- Clear separation between public-facing functionality (`site_application`) and administrative features (`admin_panel`)
- Shared configuration and static assets in the main project directory

### Media Management
- Centralized media handling for file uploads (resumes, documents)
- Static file organization for CSS, JavaScript, and images

### Database Architecture
- PostgreSQL database for production data storage
- Django ORM for database abstraction and migrations
- Separate models for different functional areas