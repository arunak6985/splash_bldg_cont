# Project Structure

## Directory Organization

```
splash_bldg_cont/
├── env/                          # Python virtual environment
├── splash_bldg/                  # Main Django project root
│   ├── admin_panel/              # Admin application module
│   │   ├── management/           # Custom Django management commands
│   │   ├── migrations/           # Database migrations for admin_panel
│   │   ├── templates/            # Admin panel HTML templates
│   │   ├── templatetags/         # Custom template tags and filters
│   │   ├── admin.py              # Django admin configuration
│   │   ├── apps.py               # App configuration
│   │   ├── bulk_pdf_views.py     # Bulk PDF generation views
│   │   ├── cheque_views.py       # Cheque management views
│   │   ├── models.py             # Database models for admin panel
│   │   ├── pdf_views.py          # PDF generation views
│   │   ├── urls.py               # URL routing for admin panel
│   │   └── views.py              # Main view controllers
│   ├── site_application/         # Public-facing application module
│   │   ├── migrations/           # Database migrations for site_application
│   │   ├── templates/            # Public site HTML templates
│   │   ├── admin.py              # Django admin configuration
│   │   ├── apps.py               # App configuration
│   │   ├── models.py             # Database models for public site
│   │   ├── urls.py               # URL routing for public site
│   │   └── views.py              # View controllers for public site
│   ├── splash_bldg/              # Django project configuration
│   │   ├── static/               # Static files (CSS, JS, images)
│   │   ├── settings.py           # Project settings and configuration
│   │   ├── urls.py               # Root URL configuration
│   │   ├── wsgi.py               # WSGI application entry point
│   │   └── asgi.py               # ASGI application entry point
│   ├── media/                    # User-uploaded files
│   │   ├── cheques/              # Uploaded cheque images
│   │   └── resumes/              # Uploaded resume files
│   ├── db.sqlite3                # SQLite database (development)
│   └── manage.py                 # Django management script
```

## Core Components and Relationships

### Application Architecture
- **Two-App Structure**: Separation between public site (site_application) and admin functionality (admin_panel)
- **Django MVT Pattern**: Models, Views, Templates architecture throughout
- **Modular Design**: Clear separation of concerns between public and administrative features

### Component Relationships
1. **site_application** → Public interface for job seekers and visitors
2. **admin_panel** → Administrative interface for staff operations
3. **splash_bldg** → Central configuration connecting both applications
4. **media/** → Shared storage for uploaded files from both applications

### Key Architectural Patterns
- **App-based modularity**: Separate Django apps for different functional areas
- **Template inheritance**: Reusable template structure
- **Custom template tags**: Extended template functionality in admin_panel
- **View separation**: Specialized view modules (pdf_views, cheque_views, bulk_pdf_views)
- **URL namespacing**: Organized routing through app-level URL configurations

## Database Architecture
- **Primary Database**: PostgreSQL (production configuration)
- **Development Database**: SQLite3 fallback
- **Migration Management**: Separate migration directories per app
- **Models**: Distributed across site_application and admin_panel apps
