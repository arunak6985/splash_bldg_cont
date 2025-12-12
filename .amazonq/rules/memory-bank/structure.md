# Project Structure

## Directory Structure and Organization

### Root Level Structure
```
splash_bldg_cont/
├── env/                    # Python virtual environment
├── splash_bldg/           # Main Django project directory
└── .amazonq/              # Amazon Q configuration and rules
```

### Django Project Layout
```
splash_bldg/
├── manage.py              # Django management script
├── splash_bldg/          # Project configuration package
│   ├── __init__.py
│   ├── settings.py       # Django settings configuration
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # WSGI application entry point
│   ├── asgi.py          # ASGI application entry point
│   └── static/          # Static assets (CSS, JS, images)
├── site_application/     # Main website application
│   ├── migrations/      # Database migrations
│   ├── templates/       # HTML templates
│   ├── models.py        # Data models
│   ├── views.py         # View controllers
│   ├── urls.py          # App-specific URL patterns
│   └── admin.py         # Admin interface configuration
└── admin/               # Custom admin application
    ├── migrations/      # Admin app migrations
    ├── templates/       # Admin-specific templates
    ├── models.py        # Admin data models
    ├── views.py         # Admin view controllers
    └── urls.py          # Admin URL patterns
```

### Static Assets Organization
```
static/
├── css/
│   └── main.css         # Custom stylesheet
├── js/
│   └── main.js          # Custom JavaScript functionality
├── img/                 # Image assets
│   ├── clients/         # Client logos
│   ├── portfolio/       # Portfolio images
│   ├── team/           # Team member photos
│   ├── testimonials/   # Testimonial images
│   └── masonry-portfolio/ # Gallery images
├── scss/               # SCSS source files
└── vendor/             # Third-party libraries
    ├── bootstrap/      # Bootstrap framework
    ├── aos/           # Animate On Scroll library
    ├── glightbox/     # Lightbox gallery
    ├── swiper/        # Touch slider
    └── isotope-layout/ # Masonry layout
```

## Core Components and Relationships

### Django Applications
- **splash_bldg**: Main project configuration and settings
- **site_application**: Primary website functionality and content
- **admin**: Custom administrative interface and management tools

### Frontend Architecture
- **Bootstrap Framework**: Responsive grid system and UI components
- **Custom CSS**: Brand-specific styling and layout customizations
- **JavaScript Libraries**: Interactive features and animations
- **Static Asset Management**: Organized vendor and custom assets

### Data Flow
1. **URL Routing**: Main urls.py routes to application-specific URL patterns
2. **View Processing**: Django views handle request logic and template rendering
3. **Template Rendering**: HTML templates with Django template language
4. **Static Serving**: CSS, JavaScript, and images served through Django static files

## Architectural Patterns

### Django MVC Pattern
- **Models**: Data structure and database interaction (models.py)
- **Views**: Business logic and request handling (views.py)
- **Templates**: Presentation layer with HTML templates
- **URLs**: Request routing and URL pattern matching

### Frontend Architecture
- **Component-Based**: Modular CSS and JavaScript components
- **Progressive Enhancement**: Core functionality without JavaScript dependencies
- **Responsive Design**: Mobile-first approach with Bootstrap grid
- **Asset Optimization**: Minified vendor libraries and organized custom code

### Development Environment
- **Virtual Environment**: Isolated Python dependencies in env/ directory
- **Django Development Server**: Built-in server for local development
- **Static File Handling**: Django's static file system for development
- **Database**: SQLite for development with easy migration to production databases

### Security Architecture
- **Django Security Middleware**: CSRF protection, XSS prevention
- **Authentication System**: Django's built-in user authentication
- **Static File Security**: Proper static file serving configuration
- **Environment Configuration**: Separate settings for development and production