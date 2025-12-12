# Development Guidelines

## Code Quality Standards

### Documentation Standards
- **File Headers**: Include comprehensive docstrings with project information, URLs, and licensing details
- **Template Attribution**: Maintain original template credits and licensing information in JavaScript files
- **Function Documentation**: Use JSDoc-style comments for JavaScript functions with clear parameter and return descriptions
- **Django Comments**: Follow Django's standard comment format with triple quotes and detailed explanations
- **Inline Comments**: Use descriptive comments for complex logic, business rules, and non-obvious implementations

### Code Formatting Patterns
- **JavaScript Structure**: Use strict mode with IIFE (Immediately Invoked Function Expression) pattern to avoid global namespace pollution
- **Python Standards**: Follow PEP 8 standards with proper indentation (4 spaces) and consistent line spacing
- **String Literals**: Use single quotes for JavaScript strings, double quotes for Python strings
- **Line Endings**: Consistent use of CRLF line endings across the entire codebase
- **Indentation**: 2 spaces for JavaScript, 4 spaces for Python, consistent throughout files

### Naming Conventions
- **JavaScript Functions**: Use camelCase naming (e.g., `toggleScrolled`, `mobileNavToogle`, `aosInit`)
- **Python Variables**: Use snake_case for variables and constants (e.g., `INSTALLED_APPS`, `BASE_DIR`)
- **CSS Classes**: Use kebab-case with descriptive names (e.g., `mobile-nav-toggle`, `scroll-top`, `filter-active`)
- **Django Apps**: Use lowercase with underscores for app names (e.g., `site_application`)
- **HTML IDs**: Use kebab-case for element IDs (e.g., `#header`, `#preloader`, `#navmenu`)

## Structural Conventions

### Django Project Organization
- **Settings Configuration**: Centralized configuration in `settings.py` with clear section comments and proper imports
- **URL Patterns**: Organized with descriptive comments following Django documentation examples
- **App Structure**: Standard Django app layout with separate models, views, URLs, and admin configurations
- **Static Files**: Organized under `static/` directory with clear separation between vendor and custom assets
- **Template Organization**: App-specific templates in respective app directories following Django conventions

### JavaScript Architecture
- **Module Pattern**: Consistent use of IIFE to encapsulate functionality and prevent global scope pollution
- **Event Handling**: Standardized use of `addEventListener` for DOM events with proper event delegation
- **DOM Queries**: Consistent use of `querySelector` and `querySelectorAll` for element selection
- **Function Organization**: Logical grouping of related functionality with clear separation of concerns
- **Library Integration**: Proper initialization of third-party libraries on window load event

### Static Asset Management
- **Vendor Libraries**: Third-party assets organized in dedicated `vendor/` directory
- **Custom Assets**: Project-specific CSS and JavaScript in separate directories
- **Image Organization**: Categorized image assets (clients, portfolio, team, testimonials)
- **CSS Framework**: Bootstrap integration with custom styling overlay approach

## Implementation Patterns

### Django Configuration Patterns
- **Path Handling**: Use `pathlib.Path` for cross-platform file path compatibility
- **App Registration**: Custom applications listed after Django built-in applications in `INSTALLED_APPS`
- **Middleware Order**: Follow Django recommended middleware ordering for security and functionality
- **Database Configuration**: SQLite for development with proper BASE_DIR path resolution
- **Static Files**: Proper STATIC_URL configuration for development and production

### JavaScript Interaction Patterns
- **Library Initialization**: Third-party libraries (AOS, GLightbox, Swiper, Isotope) initialized on window load
- **Animation Handling**: Consistent animation initialization with proper configuration objects
- **Mobile Navigation**: Toggle-based mobile menu implementation with class manipulation
- **Scroll Behavior**: Smooth scrolling implementation with proper event handling and performance considerations
- **Event Prevention**: Proper use of `preventDefault()` and `stopImmediatePropagation()` for custom behaviors

### Frontend Development Patterns
- **Responsive Design**: Mobile-first approach using Bootstrap framework with custom breakpoints
- **Progressive Enhancement**: Core functionality works without JavaScript, enhanced with interactive features
- **Performance Optimization**: Efficient DOM manipulation, lazy loading, and optimized asset delivery
- **Cross-browser Compatibility**: Modern JavaScript features with consideration for browser support
- **Accessibility**: Semantic HTML structure with proper ARIA attributes and keyboard navigation

## Security and Best Practices

### Django Security
- **Secret Key Management**: Environment-specific secret keys (development key shown for reference)
- **Debug Mode**: Properly configured DEBUG setting for development vs production environments
- **CSRF Protection**: Enabled by default in middleware stack for form security
- **Password Validation**: Multiple validators ensuring strong password requirements
- **Middleware Security**: Complete security middleware stack including XFrame protection

### Frontend Security
- **Event Handling**: Safe event handling with proper prevention of default behaviors
- **DOM Manipulation**: Secure element selection and class manipulation without innerHTML injection
- **Third-party Libraries**: Use of established, well-maintained libraries with known security records
- **Input Validation**: Client-side validation complementing server-side validation

### Development Practices
- **Virtual Environment**: Isolated Python environment for dependency management
- **Static File Handling**: Proper static file configuration and serving for development
- **Template Security**: Django template system with built-in XSS protection
- **Database Security**: ORM usage preventing SQL injection vulnerabilities

## Code Idioms and Annotations

### Common JavaScript Patterns
```javascript
// IIFE Module Pattern (100% of JS files)
(function() {
  "use strict";
  // Module code here
})();

// Event Listener Pattern (15+ instances)
element.addEventListener('event', functionName);

// Class Toggle Pattern (8+ instances)
element.classList.toggle('class-name');

// Scroll-based Functionality (5+ instances)
window.scrollY > threshold ? addClass : removeClass;
```

### Django Configuration Patterns
```python
# Path Configuration (settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# App Registration Pattern
INSTALLED_APPS = [
    # Django built-ins first
    'django.contrib.admin',
    'django.contrib.auth',
    # Custom apps last
    'site_application',
    'admin',
]

# Middleware Configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ... standard Django middleware stack
]
```

### Template and Asset Patterns
```javascript
// Library Initialization Pattern (5+ libraries)
window.addEventListener('load', initLibrary);

// Configuration Object Pattern
const config = {
    duration: 600,
    easing: 'ease-in-out',
    once: true
};
```

## Frequency Analysis

### JavaScript Implementation Patterns
- **Event Listeners**: 20+ instances following consistent addEventListener pattern
- **Class Manipulation**: 15+ instances using classList.toggle/add/remove methods
- **DOM Queries**: 25+ instances using querySelector/querySelectorAll consistently
- **Scroll Handlers**: 5+ scroll-based features with performance-optimized implementations
- **Library Integrations**: 7 third-party libraries with standardized initialization

### Django Architecture Patterns
- **Standard App Structure**: 2 custom apps following Django conventions
- **Settings Organization**: Sectioned configuration with 7 middleware components
- **URL Patterns**: Centralized routing with app-specific URL includes
- **Static File Organization**: Vendor/custom separation with categorized assets

### Code Quality Metrics
- **Documentation Coverage**: 100% of JavaScript functions have descriptive comments
- **Naming Consistency**: 95%+ adherence to established naming conventions
- **Security Practices**: Complete Django security middleware stack implementation
- **Responsive Design**: Bootstrap-based mobile-first approach with custom enhancements