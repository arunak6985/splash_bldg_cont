from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
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
import json

@custom_staff_required
def generate_bulk_pdf(request):
    """Generate PDF for multiple selected records"""
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                record_ids = data.get('record_ids', [])
            else:
                # Handle form data
                record_ids_str = request.POST.get('record_ids', '[]')
                record_ids = json.loads(record_ids_str)
            
            if not record_ids:
                return JsonResponse({'success': False, 'message': 'No records selected'})
            
            records = AttendanceRecord.objects.filter(id__in=record_ids)
            
            if not records.exists():
                return JsonResponse({'success': False, 'message': 'No records found'})
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            
            for i, record in enumerate(records):
                if i > 0:
                    p.showPage()  # New page for each record
                
                # Generate single PDF page for this record
                generate_single_page(p, record, width, height)
            
            p.save()
            buffer.seek(0)
            
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="bulk_attendance_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
            return response
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def generate_single_page(p, record, width, height):
    """Generate a single PDF page for one attendance record"""
    margin = 30
    content_width = width - (2 * margin)
    
    # Set all lines to light gray with thin width
    p.setStrokeColor(colors.lightgrey)
    p.setLineWidth(0.5)
    
    # Company header
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height-40, "SPLASH BUILDING CONTRACTING L.L.C. - U.A.E.")
    
    # Month header box
    header_y = height - 50
    p.setLineWidth(0.5)
    p.rect(margin, header_y - 25, content_width, 25, stroke=1, fill=0)
    
    # Main border
    main_border_top = header_y
    main_border_bottom = 14.4  # 0.2 inch = 14.4 points
    p.rect(margin, main_border_bottom, content_width, main_border_top - main_border_bottom, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width/2, header_y - 19, f"LABOUR ATTENDANCE CARD FOR THE MONTH OF {record.month.upper()} {record.year}")
    
    # Employee info section
    info_y = header_y - 25
    info_height = 25
    p.setLineWidth(0.5)
    p.rect(margin, info_y - info_height, content_width, info_height, stroke=1, fill=0)
    
    # Calculate section widths
    name_width = content_width * 0.4
    ref_width = content_width * 0.3
    
    # Employee info
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    p.drawString(margin + 5, info_y - 17, f"NAME: {record.name}")
    
    # Vertical lines
    ref_x = margin + name_width
    p.setLineWidth(0.3)
    p.line(ref_x, info_y, ref_x, info_y - info_height)
    p.drawString(ref_x + 5, info_y - 17, f"REF.NO - {record.ref_no}")
    
    cat_x = ref_x + ref_width
    p.setLineWidth(0.7)
    p.line(cat_x, info_y, cat_x, info_y - info_height)
    p.drawString(cat_x + 5, info_y - 17, f"CAT: {record.category}")
    
    # Attendance table
    table_start_y = info_y - info_height - 5
    
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    month_num = month_names.index(record.month) + 1
    days_in_month = calendar.monthrange(record.year, month_num)[1]
    
    headers = ['Date', 'P', 'OT', 'Bonus OT', 'Site No.', 'Remarks if any with Sign']
    
    total_fixed_width = 0.6 + 0.6 + 0.6 + 1.0 + 1.2
    remaining_width = (content_width / 72) - total_fixed_width
    col_widths = [0.6*inch, 0.6*inch, 0.6*inch, 1.0*inch, 1.2*inch, remaining_width*inch]
    
    table_data = [headers]
    absent_rows = []
    sunday_ot_rows = []  # Track Sunday OT red symbols
    
    # Date logic
    joining_day = None
    duty_stop_day = None
    effective_joining_date = None
    
    if record.new_joining:
        effective_joining_date = record.new_joining
    
    if record.re_joining:
        if not record.new_joining or record.re_joining > record.new_joining:
            effective_joining_date = record.re_joining
    
    if effective_joining_date:
        if (effective_joining_date.year == record.year and 
            effective_joining_date.month == month_num):
            joining_day = effective_joining_date.day
        elif (effective_joining_date.year < record.year or 
              (effective_joining_date.year == record.year and effective_joining_date.month < month_num)):
            joining_day = 1
        else:
            joining_day = 32
    
    if record.duty_stop:
        if (record.duty_stop.year == record.year and 
            record.duty_stop.month == month_num):
            duty_stop_day = record.duty_stop.day
        elif (record.duty_stop.year > record.year or 
              (record.duty_stop.year == record.year and record.duty_stop.month > month_num)):
            duty_stop_day = 32
        else:
            duty_stop_day = 0
    
    # Generate table rows
    for day in range(1, days_in_month + 1):
        attendance_value = record.attendance_data.get(str(day), '').strip()
        
        p_value = ''
        ot_value = ''
        bonus_ot_value = ''
        
        date_obj = datetime(record.year, month_num, day)
        is_sunday = date_obj.weekday() == 6
        
        should_have_attendance = True
        
        if joining_day and day < joining_day:
            should_have_attendance = False
        
        if duty_stop_day and day >= duty_stop_day:
            should_have_attendance = False
        
        if not should_have_attendance:
            if (joining_day and day < joining_day) or (duty_stop_day and day >= duty_stop_day):
                p_value = '-'
                ot_value = '-'
                bonus_ot_value = '-'
                absent_rows.append(day)
        elif attendance_value:
            if attendance_value == 'P':
                p_value = '8'
                if is_sunday:
                    ot_value = '-'
                    sunday_ot_rows.append(day)  # Track for red color
                else:
                    ot_value = '2'
            elif attendance_value == 'A':
                p_value = '-'
                ot_value = '-'
                bonus_ot_value = '-'
                absent_rows.append(day)
        else:
            if should_have_attendance:
                absent_rows.append(day)
        
        site_no_value = '-' if day in absent_rows else ''
        table_data.append([str(day), p_value, ot_value, bonus_ot_value, site_no_value, ''])
    
    table_data.append(['Total', '', '', '', '', ''])
    
    # Create table
    table = Table(table_data, colWidths=col_widths, rowHeights=18)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (5, 0), (5, -1), 'LEFT'),
    ]))
    
    # Mark absent days - red "-" in individual columns
    for day in absent_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('TEXTCOLOR', (1, row_index), (4, row_index), colors.red),
                ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
            ]))
    
    # Mark Sunday OT symbols as red in OT column only
    for day in sunday_ot_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('TEXTCOLOR', (2, row_index), (2, row_index), colors.red),  # OT column only
                ('FONTNAME', (2, row_index), (2, row_index), 'Helvetica-Bold'),
            ]))
    
    # Mark Sundays in medium dark blue - regardless of attendance
    for day in range(1, days_in_month + 1):
        date_obj = datetime(record.year, month_num, day)
        if date_obj.weekday() == 6:
            row_index = day
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, row_index), (0, row_index), colors.Color(0.2, 0.4, 0.8)),
                ('TEXTCOLOR', (0, row_index), (0, row_index), colors.white),
                ('FONTNAME', (0, row_index), (0, row_index), 'Helvetica-Bold'),
            ]))
    
    table.wrapOn(p, width, height)
    table.drawOn(p, margin, table_start_y - len(table_data) * 18)
    
    # Bottom section - exact match to full design image
    table_height = len(table_data) * 18
    bottom_y = table_start_y - table_height - 5
    
    # Create bottom section with 6 separate salary columns
    bottom_data = [
        ['Engineer\'s Sign', 'Employee Sign', 'No of Days :', 'Basic'],
        ['', '', '', 'OT'],
        ['', '', 'Normal OT :', 'Bonus'],
        ['', '', '', 'Gross Salary'],
        ['', '', 'Bonus OT :', 'Adv Deduction'],
        ['', '', '', 'Net Salary']
    ]
    
    # Column widths - 4 columns
    col_width = content_width / 4
    bottom_col_widths = [col_width, col_width, col_width, col_width]
    
    # Create bottom table
    bottom_table = Table(bottom_data, colWidths=bottom_col_widths, rowHeights=20)
    
    bottom_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('SPAN', (0, 0), (0, 5)),  # Engineer's Sign spans all 6 rows
        ('SPAN', (1, 0), (1, 5)),  # Employee Sign spans all 6 rows
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('LINEBELOW', (2, 0), (2, 0), 0, colors.white),  # Remove line below No of Days
        ('LINEBELOW', (2, 2), (2, 2), 0, colors.white),  # Remove line below Normal OT
        ('LINEBELOW', (2, 4), (2, 4), 0, colors.white),  # Remove line below Bonus OT
        ('LINEABOVE', (2, 2), (2, 2), 0, colors.white),  # Remove line above Normal OT
        ('LINEABOVE', (2, 4), (2, 4), 0, colors.white),  # Remove line above Bonus OT
        ('LINEBELOW', (3, 0), (3, 0), 0.5, colors.lightgrey),  # Keep line below Basic
    ]))
    
    # Position and draw bottom table
    bottom_table.wrapOn(p, width, height)
    bottom_table.drawOn(p, margin, bottom_y - 120)