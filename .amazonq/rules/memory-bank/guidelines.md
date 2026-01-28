# Development Guidelines

## Code Quality Standards

### Python/Django Code Formatting
- **Function Documentation**: All view functions include docstrings describing their purpose (e.g., `"""Admin-only view for managing job vacancies"""`)
- **Import Organization**: Imports grouped logically - Django imports first, then local imports, with clear separation
- **Line Length**: Code maintains reasonable line lengths with proper line breaks for readability
- **Variable Naming**: Descriptive variable names using snake_case convention (`total_positions`, `filled_positions`, `attendance_data`)

### Structural Conventions
- **Decorator Usage**: Consistent use of custom decorators for access control (`@custom_staff_required`, `@supervisor_required`)
- **Error Handling**: Comprehensive try-catch blocks with meaningful error messages returned as JSON responses
- **Response Patterns**: Standardized JSON response format with `success`, `message`, and data fields
- **Method Validation**: Consistent HTTP method checking (`if request.method == 'POST'`)

### Textual Standards
- **Model Field Names**: Clear, descriptive field names with help text where appropriate
- **Template Naming**: Consistent HTML template naming following Django conventions
- **URL Patterns**: Descriptive URL names matching view function purposes
- **Comment Style**: Inline comments for complex logic, especially in date parsing and attendance calculations

## Semantic Patterns

### Authentication and Authorization Patterns
- **Custom Decorators**: Implemented custom authentication decorators instead of relying solely on Django's built-in decorators
```python
def custom_staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
```

- **Session-Based Authentication**: Dual authentication system supporting both Django users and custom supervisor sessions
- **Access Control**: Granular permission checking with appropriate redirects

### Data Processing Patterns
- **Excel File Processing**: Robust Excel file handling with multiple date format parsing
- **Date Validation**: Comprehensive date parsing with fallback formats and error handling
- **Bulk Operations**: Efficient bulk processing for attendance records and PDF generation

### API Response Patterns
- **Consistent JSON Structure**: All AJAX endpoints return standardized JSON with success/error states
```python
return JsonResponse({
    'success': True,
    'message': f'Job vacancy "{job.title}" created successfully!',
    'data': additional_data
})
```

- **Error Handling**: Graceful error handling with user-friendly messages
- **Validation Responses**: Immediate feedback for form validation and data integrity

### Database Interaction Patterns
- **Model Properties**: Use of `@property` decorators for calculated fields (`available_positions`, `is_fully_filled`)
- **QuerySet Optimization**: Efficient database queries with proper filtering and ordering
- **Bulk Operations**: Use of `update_or_create` for data synchronization
- **Foreign Key Relationships**: Proper model relationships with cascade deletion

### File Management Patterns
- **Media Handling**: Organized file upload structure with dedicated directories (`resumes/`)
- **PDF Generation**: Complex PDF generation using ReportLab with detailed formatting
- **Static File Organization**: Structured static file management with proper URL configuration

### Frontend Integration Patterns
- **AJAX Communication**: Heavy use of AJAX for dynamic user interactions
- **Progressive Enhancement**: JavaScript functionality that enhances but doesn't break basic functionality
- **Template Inheritance**: Proper Django template structure with base templates
- **Static Asset Management**: Organized CSS/JS with third-party library integration

### Configuration Management
- **Settings Organization**: Clear separation of development and production settings
- **Database Configuration**: Proper database setup with PostgreSQL for production
- **Static/Media URLs**: Correct static and media file configuration
- **Security Settings**: Appropriate security middleware and authentication settings

### Business Logic Patterns
- **Attendance Management**: Complex attendance tracking with multiple states (Present, Absent, Holiday, Medical)
- **Vacancy Management**: Position tracking with available/filled position calculations
- **Supervisor Workflow**: Separate supervisor interface with limited permissions
- **Bulk Processing**: Efficient handling of multiple records for reporting and PDF generation

## Frequently Used Code Idioms

### Model Field Patterns
```python
# Standard model field setup with choices
employment_type = models.CharField(max_length=50, choices=[
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('contract', 'Contract'),
], default='full_time')

# Timestamp fields with timezone awareness
created_at = models.DateTimeField(default=timezone.now)
updated_at = models.DateTimeField(auto_now=True)
```

### View Function Structure
```python
@custom_staff_required
def view_name(request):
    """Descriptive docstring"""
    if request.method == 'POST':
        try:
            # Process data
            return JsonResponse({'success': True, 'message': 'Success message'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    # GET request handling
    context = {'data': queryset}
    return render(request, 'template.html', context)
```

### Date Processing Pattern
```python
def parse_date(date_value):
    """Parse date from various formats"""
    if isinstance(date_value, datetime):
        return date_value.date()
    elif isinstance(date_value, str):
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
            try:
                return datetime.strptime(date_value.strip(), fmt).date()
            except ValueError:
                continue
    return None
```

### Popular Annotations and Decorators
- `@custom_staff_required` - Custom authentication decorator
- `@supervisor_required` - Role-based access control
- `@property` - Model calculated fields
- `@wraps(view_func)` - Decorator preservation
- `default=timezone.now` - Timezone-aware timestamps
- `on_delete=models.CASCADE` - Relationship management