# Project Structure and Architecture

## Directory Structure

```
splash_bldg_cont/
├── env/                          # Python virtual environment
├── splash_bldg/                  # Main Django project
│   ├── admin_panel/              # Admin functionality app
│   │   ├── migrations/           # Database migrations
│   │   ├── templates/            # Admin HTML templates
│   │   ├── templatetags/         # Custom template tags
│   │   ├── models.py             # Admin data models
│   │   ├── views.py              # Admin view controllers
│   │   ├── pdf_views.py          # PDF generation views
│   │   ├── bulk_pdf_views.py     # Bulk PDF operations
│   │   └── urls.py               # Admin URL routing
│   ├── site_application/         # Public site app
│   │   ├── migrations/           # Database migrations
│   │   ├── templates/            # Public HTML templates
│   │   ├── models.py             # Application data models
│   │   ├── views.py              # Public view controllers
│   │   └── urls.py               # Public URL routing
│   ├── splash_bldg/              # Project configuration
│   │   ├── static/               # Static assets
│   │   │   ├── css/              # Stylesheets
│   │   │   ├── js/               # JavaScript files
│   │   │   ├── img/              # Images
│   │   │   ├── scss/             # SASS source files
│   │   │   └── vendor/           # Third-party libraries
│   │   ├── settings.py           # Django configuration
│   │   ├── urls.py               # Main URL routing
│   │   └── wsgi.py               # WSGI application
│   ├── media/                    # User uploaded files
│   │   └── resumes/              # Resume file storage
│   ├── db.sqlite3                # SQLite database (dev)
│   └── manage.py                 # Django management script
└── .amazonq/                     # AI assistant configuration
    └── rules/                    # Project rules and documentation
```

## Core Components and Relationships

### Django Applications Architecture

#### admin_panel App
- **Purpose**: Administrative interface for HR and management operations
- **Key Models**: AttendanceRecord, EmployeeAttendance, Supervisor
- **Responsibilities**: 
  - User authentication and session management
  - Attendance data processing and visualization
  - PDF report generation (individual and bulk)
  - Job vacancy management
  - Excel file upload and processing

#### site_application App  
- **Purpose**: Public-facing website for job seekers
- **Key Models**: JobVacancy, JobApplication, Contact, JobTitle, Location
- **Responsibilities**:
  - Job listing display and management
  - Application form processing
  - Resume file handling
  - Contact form submissions

#### splash_bldg Configuration
- **Purpose**: Project-wide settings and URL routing
- **Components**:
  - Database configuration (PostgreSQL)
  - Static file management
  - Media file handling
  - Security settings

### Data Flow Architecture

```
User Request → URLs → Views → Models → Database
                ↓
            Templates ← Context Data
                ↓
            HTTP Response
```

### File Processing Pipeline

```
Excel Upload → Validation → Data Parsing → Model Creation → Database Storage
                                    ↓
PDF Generation ← Template Rendering ← Data Retrieval
```

## Architectural Patterns

### Model-View-Template (MVT)
- **Models**: Define data structure and business logic
- **Views**: Handle request processing and response generation  
- **Templates**: Render HTML with dynamic content

### Separation of Concerns
- **admin_panel**: Internal operations and management
- **site_application**: External user interactions
- **static**: Client-side assets and styling
- **media**: User-generated content storage

### Authentication Flow
- Custom login system with session management
- Role-based access control for admin functions
- Secure file upload with validation

### Database Design
- PostgreSQL for production data storage
- Django ORM for database abstraction
- Migration system for schema management