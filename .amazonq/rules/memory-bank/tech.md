# Technology Stack

## Programming Languages and Versions

### Backend Technologies
- **Python**: Primary backend language for Django framework
- **Django 5.2.9**: Web framework for rapid development and clean design
- **SQLite**: Default database for development (easily configurable for production)

### Frontend Technologies
- **HTML5**: Semantic markup with modern web standards
- **CSS3**: Custom styling with SCSS preprocessing capabilities
- **JavaScript (ES6+)**: Modern JavaScript for interactive functionality
- **Bootstrap 5**: Responsive CSS framework for mobile-first design

### Template Engine
- **Django Template Language**: Server-side template rendering with built-in security features

## Build Systems and Dependencies

### Python Environment
- **Virtual Environment**: Isolated Python environment in `env/` directory
- **pip**: Package manager for Python dependencies
- **Django**: Core web framework dependency

### Frontend Dependencies
Located in `static/vendor/` directory:
- **Bootstrap 5**: CSS framework and JavaScript components
- **Bootstrap Icons**: Icon font for UI elements
- **AOS (Animate On Scroll)**: Scroll-triggered animations
- **GLightbox**: Modern lightbox gallery
- **Swiper**: Touch-enabled slider/carousel
- **Isotope Layout**: Masonry and filtering layouts
- **ImagesLoaded**: Image loading utility
- **PureCounter**: Animated counters
- **Waypoints**: Scroll-based triggers

### Asset Management
- **Django Static Files**: Built-in static file handling
- **Vendor Libraries**: Third-party assets organized in vendor directory
- **Custom Assets**: Project-specific CSS and JavaScript in dedicated directories

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
env\Scripts\activate

# Install Django (if not already installed)
pip install django

# Navigate to project directory
cd splash_bldg
```

### Django Development Commands
```bash
# Start development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Django shell for debugging
python manage.py shell
```

### Database Management
```bash
# Reset database (development)
python manage.py flush

# Load initial data (if fixtures exist)
python manage.py loaddata fixture_name

# Database shell access
python manage.py dbshell
```

### Development Workflow
1. **Activate Environment**: `env\Scripts\activate`
2. **Start Server**: `python manage.py runserver`
3. **Access Application**: http://127.0.0.1:8000/
4. **Admin Interface**: http://127.0.0.1:8000/admin/

### Project Configuration
- **Settings**: Configuration in `splash_bldg/settings.py`
- **URL Routing**: Main routing in `splash_bldg/urls.py`
- **Static Files**: Served from `splash_bldg/static/` during development
- **Templates**: App-specific templates in respective app directories

### Production Considerations
- **Environment Variables**: Use environment-specific settings
- **Database**: Configure PostgreSQL or MySQL for production
- **Static Files**: Use CDN or web server for static file serving
- **Security**: Update SECRET_KEY and disable DEBUG mode
- **WSGI/ASGI**: Deploy using Gunicorn, uWSGI, or similar WSGI server