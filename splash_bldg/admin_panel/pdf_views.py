from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
import calendar
from datetime import datetime
from .models import AttendanceRecord
from .views import custom_staff_required

@custom_staff_required
def generate_attendance_pdf(request, record_id):
    record = get_object_or_404(AttendanceRecord, id=record_id)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Company header - exactly like original
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height-50, "SPLASH BUILDING CONTRACTING L.L.C. - U.A.E.")
    
    # Month header box - exactly like original
    header_y = height - 90
    p.rect(50, header_y, width-100, 30)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, header_y + 8, f"LABOUR ATTENDANCE CARD FOR THE MONTH OF {record.month.upper()} {record.year}")
    
    # Employee info section - exactly like original with proper data display
    info_y = header_y - 40
    p.rect(50, info_y, width-100, 30)
    
    # NAME section (60% width)
    name_width = 320
    p.setFont("Helvetica-Bold", 12)
    p.drawString(55, info_y + 8, f"NAME: {record.name}")
    
    # REF.NO section (25% width)
    ref_x = 50 + name_width
    p.line(ref_x, info_y, ref_x, info_y + 30)
    p.drawString(ref_x + 5, info_y + 8, f"REF.NO - {record.ref_no}")
    
    # CAT section (15% width)
    cat_x = ref_x + 100
    p.line(cat_x, info_y, cat_x, info_y + 30)
    p.drawString(cat_x + 5, info_y + 8, f"CAT: {record.category}")
    
    # Main attendance table - exactly like original
    table_y = info_y - 30
    
    # Get month details for proper calendar
    month_num = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'].index(record.month) + 1
    days_in_month = calendar.monthrange(record.year, month_num)[1]
    
    # Create table exactly like original card
    headers = ['Date', 'P', 'OT', 'Bonus OT', 'Site No.', 'Remarks if any with Sign']
    table_data = [headers]
    
    # Add all days with attendance data
    for day in range(1, days_in_month + 1):
        date_obj = datetime(record.year, month_num, day)
        is_sunday = date_obj.weekday() == 6
        
        # Get attendance value from uploaded data
        attendance_value = record.attendance_data.get(str(day), '')
        
        # Format date (mark Sundays)
        date_str = str(day)
        
        table_data.append([date_str, attendance_value, '', '', '', ''])
    
    # Add total row
    table_data.append(['Total', '', '', '', '', ''])
    
    # Create table with exact original proportions
    table = Table(table_data, colWidths=[0.8*inch, 0.6*inch, 0.8*inch, 1.2*inch, 1*inch, 2.8*inch])
    
    # Style exactly like original card
    table.setStyle(TableStyle([
        # Header styling - beige background like original
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.96, 0.87, 0.70)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        
        # Grid and borders - black lines like original
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating row colors like original
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.Color(0.96, 0.87, 0.70), colors.white]),
        
        # Total row styling - beige like original
        ('BACKGROUND', (0, -1), (-1, -1), colors.Color(0.96, 0.87, 0.70)),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    # Mark Sundays in red exactly like original
    for i, row_data in enumerate(table_data[1:-1], 1):
        date_obj = datetime(record.year, month_num, i)
        if date_obj.weekday() == 6:  # Sunday
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.red),
                ('TEXTCOLOR', (0, i), (0, i), colors.white),
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
            ]))
    
    # Position table exactly like original
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, table_y - (len(table_data) * 18))
    
    # Bottom section - exactly like original card layout
    bottom_y = 150
    bottom_height = 120
    
    # Main bottom rectangle
    p.rect(50, bottom_y-bottom_height, width-100, bottom_height)
    
    # Engineer's Sign section (left)
    eng_width = 150
    p.rect(50, bottom_y-bottom_height, eng_width, bottom_height)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(55, bottom_y-bottom_height-15, "Engineer's Sign")
    
    # Employee Sign section (middle-left)
    emp_x = 50 + eng_width
    emp_width = 150
    p.rect(emp_x, bottom_y-bottom_height, emp_width, bottom_height)
    p.drawString(emp_x + 5, bottom_y-bottom_height-15, "Employee Sign")
    
    # Calculation section (middle-right)
    calc_x = emp_x + emp_width
    calc_width = 120
    p.rect(calc_x, bottom_y-bottom_height, calc_width, bottom_height)
    
    # Calculation labels exactly like original
    p.setFont("Helvetica-Bold", 10)
    p.drawString(calc_x + 5, bottom_y - 30, "No of Days :")
    p.drawString(calc_x + 5, bottom_y - 60, "Normal OT :")
    p.drawString(calc_x + 5, bottom_y - 90, "Bonus OT :")
    
    # Salary section (right) - exactly like original
    salary_x = calc_x + calc_width
    salary_width = width - 50 - salary_x
    p.rect(salary_x, bottom_y-bottom_height, salary_width, bottom_height)
    
    # Salary items with exact original layout
    salary_items = ['Basic', 'OT', 'Bonus', 'Gross Salary', 'Adv Deduction', 'Net Salary']
    item_height = 20
    
    p.setFont("Helvetica-Bold", 10)
    for i, item in enumerate(salary_items):
        item_y = bottom_y - 20 - (i * item_height)
        
        # Horizontal lines between items
        if i > 0:
            p.line(salary_x, item_y + 15, salary_x + salary_width, item_y + 15)
        
        # Item label
        p.drawString(salary_x + 5, item_y, item)
        
        # Input box area (right side of each row)
        p.rect(salary_x + 80, item_y - 3, salary_width - 85, 15)
    
    # Vertical line to separate calculation and salary sections
    p.line(salary_x, bottom_y-bottom_height, salary_x, bottom_y)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance_{record.ref_no}_{record.month}_{record.year}.pdf"'
    return response