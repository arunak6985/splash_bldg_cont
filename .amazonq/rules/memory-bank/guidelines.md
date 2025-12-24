# Development Guidelines and Standards

## Code Quality Standards

### Python/Django Code Formatting
- **Function Documentation**: Use triple-quoted docstrings for function descriptions (found in 100% of analyzed functions)
- **Import Organization**: Group imports by type - Django imports first, then local imports, followed by third-party libraries
- **Line Length**: Keep lines readable, break complex expressions across multiple lines
- **Variable Naming**: Use descriptive snake_case names (e.g., `attendance_data`, `selected_month`, `days_in_month`)

### JavaScript Code Standards
- **Function Structure**: Use IIFE (Immediately Invoked Function Expression) pattern for main application logic
- **Strict Mode**: Always use `"use strict";` at the beginning of JavaScript files
- **Event Handling**: Use `addEventListener` for DOM event binding rather than inline handlers
- **Variable Declarations**: Use `const` and `let` appropriately, avoid `var`

### HTML/Template Standards
- **Template Inheritance**: Use Django template inheritance with base templates
- **CSS Classes**: Use semantic class names with kebab-case (e.g., `mobile-nav-toggle`, `scroll-top`)
- **Form Handling**: Implement proper CSRF protection for all forms
- **Responsive Design**: Use Bootstrap classes and custom CSS for mobile-first design

## Structural Conventions

### Django Application Architecture
- **App Separation**: Maintain clear separation between `admin_panel` (internal) and `site_application` (public) apps
- **Model Organization**: Place related models in their respective app's `models.py` file
- **View Decorators**: Use custom decorators like `@custom_staff_required` and `@supervisor_required` for access control
- **URL Patterns**: Organize URLs by functionality with descriptive names

### File Organization Patterns
- **Static Files**: Organize by type - `css/`, `js/`, `img/`, `scss/`, `vendor/`
- **Templates**: Use app-specific template directories with shared base templates
- **Media Files**: Store user uploads in organized subdirectories (e.g., `resumes/`)
- **Migrations**: Keep migration files organized by app with descriptive names

### Database Design Patterns
- **Model Properties**: Use `@property` decorators for calculated fields (e.g., `available_positions`)
- **Meta Classes**: Include ordering and other metadata in model Meta classes
- **Foreign Keys**: Use `on_delete=models.CASCADE` for dependent relationships
- **Default Values**: Use `timezone.now` for timestamp fields, not `auto_now_add`

## Semantic Patterns

### Authentication and Authorization
- **Custom Decorators**: Implement role-based access control with custom decorators
- **Session Management**: Use Django sessions for supervisor authentication alongside Django auth
- **Permission Checks**: Validate user permissions at both view and template levels
- **Logout Handling**: Clear all session data on logout for security

### Data Processing Patterns
- **Excel File Handling**: Use `openpyxl` for Excel file processing with proper error handling
- **Date Parsing**: Implement flexible date parsing functions to handle multiple formats
- **JSON Responses**: Return consistent JSON structure with `success` and `message` fields
- **Bulk Operations**: Support bulk actions for efficiency (delete, PDF generation)

### PDF Generation Standards
- **ReportLab Usage**: Use ReportLab for PDF generation with proper styling
- **Table Formatting**: Apply consistent table styles with borders, colors, and fonts
- **Layout Management**: Use proper margins and positioning for professional appearance
- **File Naming**: Use descriptive filenames with relevant data (ref_no, month, year)

## Internal API Usage and Patterns

### Django ORM Patterns
```python
# Use update_or_create for upsert operations
AttendanceRecord.objects.update_or_create(
    ref_no=ref_no, month=month, year=year,
    defaults={'name': name, 'attendance_data': data}
)

# Use get_object_or_404 for single object retrieval
record = get_object_or_404(AttendanceRecord, id=record_id)

# Use filter with exists() for existence checks
exists = Supervisor.objects.filter(username=username).exists()
```

### AJAX Request Handling
```javascript
// Standard AJAX pattern with CSRF protection
$.ajax({
    url: url,
    method: 'POST',
    data: formData,
    headers: {'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()},
    success: function(response) {
        if (response.success) {
            // Handle success
        } else {
            alert(response.message);
        }
    }
});
```

### Form Processing Patterns
```python
# Standard form processing with validation
if request.method == 'POST':
    try:
        # Process form data
        # Validate input
        # Save to database
        return JsonResponse({'success': True, 'message': 'Success message'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
```

## Frequently Used Code Idioms

### Error Handling
- **Try-Catch Blocks**: Wrap risky operations in try-except blocks with meaningful error messages
- **Validation**: Validate user input before processing (file types, data formats, permissions)
- **Graceful Degradation**: Provide fallbacks when optional features fail (background images, logos)

### Data Transformation
- **String Processing**: Use `.strip()` for cleaning user input, `.upper()` for standardization
- **Date Handling**: Implement flexible date parsing with multiple format support
- **JSON Processing**: Use `json.loads()` and `json.dumps()` for data serialization

### UI/UX Patterns
- **Loading States**: Show loading modals during AJAX operations
- **Confirmation Dialogs**: Use `confirm()` for destructive operations
- **Dynamic Content**: Update UI elements based on user actions without page refresh
- **Responsive Tables**: Implement horizontal scrolling for data tables on mobile devices

## Popular Annotations and Decorators

### Django Decorators
- `@custom_staff_required`: Custom decorator for admin access control
- `@supervisor_required`: Custom decorator for supervisor access control
- `@login_required`: Django built-in for authenticated users
- `@user_passes_test`: Django built-in for custom permission tests

### Model Annotations
- `@property`: For calculated model fields
- `help_text`: For field documentation in admin interface
- `default=timezone.now`: For timestamp fields
- `blank=True`: For optional fields

### JavaScript Patterns
- Event delegation for dynamic content
- Module pattern with IIFE for encapsulation
- Progressive enhancement for accessibility
- Smooth scrolling and animation effects