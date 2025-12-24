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
import os
from django.conf import settings

@custom_staff_required
def generate_attendance_pdf(request, record_id):
    record = get_object_or_404(AttendanceRecord, id=record_id)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Add background image
    try:
        background_path = r"D:\Website\splash_bldg_cont\splash_bldg\splash_bldg\static\img\pdf_backround_A4.png"
        if os.path.exists(background_path):
            p.drawImage(background_path, 0, 0, width=width, height=height)
    except:
        # If background image not found, continue without it
        pass
    
    # Set margins
    margin = 30
    content_width = width - (2 * margin)
    
    # Set all lines to black with thin width
    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    
    # Company logo
    try:
        logo_path = r"D:\Website\splash_bldg_cont\splash_bldg\splash_bldg\static\img\splash_building_logo.png"
        p.drawImage(logo_path, 55, height-70, width=70, height=80, mask='auto')
    except Exception as e:
        print(f"Logo error: {e}")
    
    # Company header - bold and centered (outside border)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height-40, "SPLASH BUILDING CONTRACTING L.L.C. - U.A.E.")
    
    # Month header box with light blue background
    header_y = height - 50
    p.setLineWidth(0.5)
    p.setFillColor(colors.lightblue)
    p.rect(margin, header_y - 25, content_width, 25, stroke=1, fill=1)
    
    # Main border around content (starts from month header)
    main_border_top = header_y
    main_border_bottom = 14.4  # 0.2 inch = 14.4 points
    p.rect(margin, main_border_bottom, content_width, main_border_top - main_border_bottom, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, header_y - 19, f"LABOUR ATTENDANCE CARD FOR THE MONTH OF {record.month.upper()} {record.year}")
    
    # Employee info section - single row only (NAME, REF.NO, CAT)
    info_y = header_y - 25
    info_height = 25  # Single row height
    p.setLineWidth(0.5)
    p.rect(margin, info_y - info_height, content_width, info_height, stroke=1, fill=0)
    
    # Calculate section widths
    name_width = content_width * 0.4
    ref_width = content_width * 0.3
    cat_width = content_width * 0.3
    
    # Single row - NAME, REF.NO, CAT
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    p.drawString(margin + 5, info_y - 17, f"NAME: {record.name}")
    
    # Vertical line after NAME
    ref_x = margin + name_width
    p.setLineWidth(0.3)
    p.line(ref_x, info_y, ref_x, info_y - info_height)
    p.drawString(ref_x + 5, info_y - 17, f"REF.NO - {record.ref_no}")
    
    # Vertical line after REF.NO
    cat_x = ref_x + ref_width
    p.setLineWidth(0.7)
    p.line(cat_x, info_y, cat_x, info_y - info_height)
    p.drawString(cat_x + 5, info_y - 17, f"CAT: {record.category}")
    
    # Main attendance table
    table_start_y = info_y - info_height - 5
    
    # Get month details
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    month_num = month_names.index(record.month) + 1
    days_in_month = calendar.monthrange(record.year, month_num)[1]
    
    # Table headers
    headers = ['Date', 'P', 'OT', 'Bonus OT', 'Site No.', 'Remarks if any with Sign']
    
    # Calculate column widths to merge with main border
    total_fixed_width = 0.6 + 0.6 + 0.6 + 1.0 + 1.2  # Sum of first 5 columns in inches
    remaining_width = (content_width / 72) - total_fixed_width  # Convert content_width to inches
    col_widths = [0.6*inch, 0.6*inch, 0.6*inch, 1.0*inch, 1.2*inch, remaining_width*inch]
    
    # Create table data
    table_data = [headers]
    
    # Add days 1-31 with attendance data
    absent_rows = []
    sunday_ot_rows = []  # Track Sunday OT red symbols
    
    # Enhanced date logic - consider NEW JOINING, RE JOINING, and DUTY STOP
    joining_day = None
    duty_stop_day = None
    effective_joining_date = None
    
    # Determine the effective joining date
    if record.new_joining:
        effective_joining_date = record.new_joining
    
    # If RE JOINING date exists and is later than NEW JOINING, use RE JOINING
    if record.re_joining:
        if not record.new_joining or record.re_joining > record.new_joining:
            effective_joining_date = record.re_joining
    
    # Calculate joining day for the current month/year
    if effective_joining_date:
        if (effective_joining_date.year == record.year and 
            effective_joining_date.month == month_num):
            joining_day = effective_joining_date.day
        elif (effective_joining_date.year < record.year or 
              (effective_joining_date.year == record.year and effective_joining_date.month < month_num)):
            joining_day = 1
        else:
            joining_day = 32
    
    # Calculate duty stop day for the current month/year
    if record.duty_stop:
        if (record.duty_stop.year == record.year and 
            record.duty_stop.month == month_num):
            duty_stop_day = record.duty_stop.day
        elif (record.duty_stop.year > record.year or 
              (record.duty_stop.year == record.year and record.duty_stop.month > month_num)):
            duty_stop_day = 32  # Duty stops after this month
        else:
            duty_stop_day = 0  # Duty stopped before this month
    
    for day in range(1, days_in_month + 1):
        attendance_value = record.attendance_data.get(str(day), '').strip()
        
        # Parse attendance data from Excel format
        p_value = ''
        ot_value = ''
        bonus_ot_value = ''
        
        # Check if it's Sunday
        date_obj = datetime(record.year, month_num, day)
        is_sunday = date_obj.weekday() == 6
        
        # Check if employee should have attendance for this day
        should_have_attendance = True
        
        # If employee hasn't joined yet, no attendance
        if joining_day and day < joining_day:
            should_have_attendance = False
        
        # If employee duty stopped, no attendance from duty stop date onwards (including duty stop date)
        if duty_stop_day and day >= duty_stop_day:
            should_have_attendance = False
        
        if not should_have_attendance:
            # Put red "-" for days from duty stop date onwards (including duty stop date)
            if (joining_day and day < joining_day) or (duty_stop_day and day >= duty_stop_day):
                p_value = '-'
                ot_value = '-'
                bonus_ot_value = '-'
                absent_rows.append(day)
            else:
                p_value = ''
                ot_value = ''
        elif attendance_value:
            if attendance_value == 'P':
                # P means Present: auto-fill P=8 and OT=3 (but red "-" OT on Sunday)
                p_value = '8'
                if is_sunday:
                    ot_value = '-'
                    sunday_ot_rows.append(day)  # Track for red color
                else:
                    ot_value = '2'
            elif attendance_value == 'A':
                # A means Absent: put red "-" in columns
                p_value = '-'
                ot_value = '-'
                bonus_ot_value = '-'
                absent_rows.append(day)
            elif attendance_value.startswith('P='):
                p_value = attendance_value.split('=')[1].strip()
            elif 'P=' in attendance_value and 'OT=' in attendance_value:
                parts = attendance_value.split(',')
                for part in parts:
                    part = part.strip()
                    if part.startswith('P='):
                        p_value = part.split('=')[1].strip()
                    elif part.startswith('OT='):
                        ot_value = part.split('=')[1].strip()
            elif 'P' in attendance_value and 'OT=' in attendance_value:
                p_value = '8'
                if 'OT=' in attendance_value:
                    ot_part = attendance_value.split('OT=')[1].strip()
                    ot_value = ot_part.split(',')[0].strip()
            elif attendance_value.startswith('OT='):
                ot_value = attendance_value.split('=')[1].strip()
            elif 'OT' in attendance_value and '=' not in attendance_value:
                if attendance_value == 'OT':
                    ot_value = '3'
                else:
                    ot_match = attendance_value.replace('OT', '').strip()
                    if ot_match.isdigit():
                        ot_value = ot_match
        else:
            # Only mark as absent if employee should have attendance
            if should_have_attendance:
                absent_rows.append(day)
        
        # Add Site No. value for absent days
        site_no_value = '-' if day in absent_rows else ''
        table_data.append([str(day), p_value, ot_value, bonus_ot_value, site_no_value, ''])
    
    # Add total row
    table_data.append(['Total', '', '', '', '', ''])
    
    # Create and style table
    table = Table(table_data, colWidths=col_widths, rowHeights=18)
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (5, 0), (5, -1), 'LEFT'),
    ]))
    
    # Mark absent days - red text for P, OT, Bonus OT, Site No. columns only
    for day in absent_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('TEXTCOLOR', (1, row_index), (4, row_index), colors.red),  # Columns P, OT, Bonus OT, Site No.
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
    
    # Mark Sundays in medium dark blue (date box only) - regardless of attendance
    for day in range(1, days_in_month + 1):
        date_obj = datetime(record.year, month_num, day)
        if date_obj.weekday() == 6:
            row_index = day
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, row_index), (0, row_index), colors.Color(0.2, 0.4, 0.8)),  # Medium dark blue
                ('TEXTCOLOR', (0, row_index), (0, row_index), colors.white),
                ('FONTNAME', (0, row_index), (0, row_index), 'Helvetica-Bold'),
            ]))
    
    # Position and draw table
    table_height = len(table_data) * 18
    table.wrapOn(p, width, height)
    table.drawOn(p, margin, table_start_y - table_height)
    
    # Bottom section - exact match to full design image
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
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('SPAN', (0, 0), (0, 5)),  # Engineer's Sign spans all 6 rows
        ('SPAN', (1, 0), (1, 5)),  # Employee Sign spans all 6 rows
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('LINEBELOW', (0, 0), (0, 0), 0, colors.white),  # Remove line below Engineer's Sign
        ('LINEBELOW', (1, 0), (1, 0), 0, colors.white),  # Remove line below Employee Sign
        ('LINEBELOW', (2, 0), (2, 0), 0, colors.white),  # Remove line below No of Days
        ('LINEBELOW', (2, 1), (2, 1), 0, colors.white),  # Remove line below empty box
        ('LINEBELOW', (2, 2), (2, 2), 0, colors.white),  # Remove line below Normal OT
        ('LINEBELOW', (2, 3), (2, 3), 0, colors.white),  # Remove line below empty box
        ('LINEBELOW', (2, 4), (2, 4), 0, colors.white),  # Remove line below Bonus OT
        ('LINEBELOW', (2, 5), (2, 5), 0, colors.white),  # Remove line below empty box
        ('LINEABOVE', (2, 2), (2, 2), 0, colors.white),  # Remove line above Normal OT
        ('LINEABOVE', (2, 4), (2, 4), 0, colors.white),  # Remove line above Bonus OT
        ('LINEBELOW', (3, 0), (3, 0), 0.5, colors.black),  # Keep line below Basic
    ]))
    
    # Position and draw bottom table
    bottom_table.wrapOn(p, width, height)
    bottom_table.drawOn(p, margin, bottom_y - 120)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance_{record.ref_no}_{record.month}_{record.year}.pdf"'
    return response