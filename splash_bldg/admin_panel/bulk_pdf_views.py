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
            
            valid_records = []
            
            # Filter out records that shouldn't have PDFs
            for record in records:
                month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                month_num = month_names.index(record.month) + 1
                
                # Skip if duty stopped before the selected month and no rejoining
                if record.duty_stop and not record.re_joining:
                    if (record.duty_stop.year < record.year or 
                        (record.duty_stop.year == record.year and record.duty_stop.month < month_num)):
                        continue  # Skip this record
                
                # Skip if duty stopped on 1st day of month and no rejoining in same month
                if record.duty_stop:
                    if (record.duty_stop.year == record.year and record.duty_stop.month == month_num):
                        if record.duty_stop.day == 1 and not record.re_joining:
                            continue  # Skip this record
                        # If duty stopped on 1st and rejoined same month, check if rejoining is valid
                        if record.duty_stop.day == 1 and record.re_joining:
                            if (record.re_joining.year == record.year and 
                                record.re_joining.month == month_num and 
                                record.re_joining.day > 1):
                                valid_records.append(record)  # Valid - rejoined after 1st
                            else:
                                continue  # Skip - no valid work days
                        else:
                            valid_records.append(record)  # Valid - duty stopped after 1st
                    else:
                        valid_records.append(record)  # Valid - duty stop not in this month
                else:
                    valid_records.append(record)  # Valid - no duty stop
            
            if not valid_records:
                return JsonResponse({'success': False, 'message': 'No valid attendance records found for PDF generation'})
            
            # Generate PDFs for valid records only
            for i, record in enumerate(valid_records):
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
    
    # Check if employee should have PDF generated for this month
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    month_num = month_names.index(record.month) + 1
    
    # Skip PDF if duty stopped before rejoining in same month and no work days
    if record.duty_stop and record.re_joining:
        if (record.duty_stop.year == record.year and record.duty_stop.month == month_num and
            record.re_joining.year == record.year and record.re_joining.month == month_num):
            if record.duty_stop.day == 1:
                return  # Skip this employee
    
    # Skip PDF if duty stopped before the selected month and no rejoining
    if record.duty_stop and not record.re_joining:
        if (record.duty_stop.year < record.year or 
            (record.duty_stop.year == record.year and record.duty_stop.month < month_num)):
            return  # Skip this employee
    margin = 30
    content_width = width - (2 * margin)
    
    # Set all lines to black with thin width
    p.setStrokeColor(colors.black)
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
    # Display ref_no - show empty if it starts with EMPTY_REF_
    display_ref = "" if record.ref_no.startswith("EMPTY_REF_") else record.ref_no
    p.drawString(ref_x + 5, info_y - 17, f"REF.NO - {display_ref}")
    
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
    
    # Calculate rejoining day for the current month/year
    rejoining_day = None
    if record.re_joining:
        if (record.re_joining.year == record.year and 
            record.re_joining.month == month_num):
            rejoining_day = record.re_joining.day
        elif (record.re_joining.year < record.year or 
              (record.re_joining.year == record.year and record.re_joining.month < month_num)):
            rejoining_day = 1
        else:
            rejoining_day = 32
    
    # Generate table rows
    holiday_rows = []
    medical_rows = []
    
    for day in range(1, days_in_month + 1):
        attendance_value = record.attendance_data.get(str(day), '').strip()
        
        p_value = ''
        ot_value = ''
        bonus_ot_value = ''
        site_no_value = ''
        
        date_obj = datetime(record.year, month_num, day)
        is_sunday = date_obj.weekday() == 6
        
        should_have_attendance = True
        
        if joining_day and day < joining_day:
            should_have_attendance = False
        
        # If employee duty stopped and not rejoined yet, no attendance
        if duty_stop_day and day >= duty_stop_day and (not rejoining_day or day < rejoining_day):
            should_have_attendance = False
        
        # If employee rejoined, has attendance from rejoining day onwards
        if rejoining_day and day >= rejoining_day:
            should_have_attendance = True
        
        if not should_have_attendance:
            if ((joining_day and day < joining_day) or 
                (duty_stop_day and day >= duty_stop_day and (not rejoining_day or day < rejoining_day))):
                p_value = '-'
                ot_value = '-'
                bonus_ot_value = '-'
                site_no_value = '-'
                absent_rows.append(day)
        elif attendance_value:
            if attendance_value == 'H':
                # Holiday - merge columns with HOLIDAY text
                p_value = 'HOLIDAY'
                ot_value = ''
                bonus_ot_value = ''
                site_no_value = ''
                holiday_rows.append(day)
            elif attendance_value == 'M':
                # Medical - merge columns with MEDICAL LEAVE text
                p_value = 'MEDICAL LEAVE'
                ot_value = ''
                bonus_ot_value = ''
                site_no_value = ''
                medical_rows.append(day)
            elif attendance_value == 'P':
                p_value = '8'
                if is_sunday:
                    ot_value = '-'
                    sunday_ot_rows.append(day)  # Track for red color
                else:
                    ot_value = '2'
            elif attendance_value == 'A':
                if is_sunday:
                    # Sunday absent - separate red dashes in each column
                    p_value = '-'
                    ot_value = '-'
                    bonus_ot_value = '-'
                    site_no_value = '-'
                else:
                    # Regular absent - merge columns with ABSENT text
                    p_value = 'ABSENT'
                    ot_value = ''
                    bonus_ot_value = ''
                    site_no_value = ''
                absent_rows.append(day)
        else:
            if should_have_attendance:
                absent_rows.append(day)
                site_no_value = '-'
        
        table_data.append([str(day), p_value, ot_value, bonus_ot_value, site_no_value, ''])
    
    # Calculate totals
    total_p_days = 0
    total_absent_days = 0
    total_medical_days = 0
    total_holiday_days = 0
    
    for day in range(1, days_in_month + 1):
        attendance_value = record.attendance_data.get(str(day), '').strip()
        
        should_have_attendance = True
        
        if joining_day and day < joining_day:
            should_have_attendance = False
        
        if duty_stop_day and day >= duty_stop_day and (not rejoining_day or day < rejoining_day):
            should_have_attendance = False
        
        if rejoining_day and day >= rejoining_day:
            should_have_attendance = True
        
        if should_have_attendance:
            if attendance_value == 'P':
                total_p_days += 1
            elif attendance_value == 'A':
                total_absent_days += 1
            elif attendance_value == 'M':
                total_medical_days += 1
            elif attendance_value == 'H':
                total_holiday_days += 1
    
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
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.white),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (5, 0), (5, -1), 'LEFT'),
    ]))
    
    # Track days before joining/rejoining and after duty stop
    no_work_rows = []
    sunday_absent_rows = []
    
    # Mark absent days
    for day in absent_rows:
        if day <= days_in_month:
            row_index = day
            date_obj = datetime(record.year, month_num, day)
            is_sunday = date_obj.weekday() == 6
            
            # Check if this is a no-work day (before joining or after duty stop)
            is_no_work_day = False
            if ((joining_day and day < joining_day) or 
                (duty_stop_day and day >= duty_stop_day and (not rejoining_day or day < rejoining_day))):
                is_no_work_day = True
                no_work_rows.append(day)
            
            if is_no_work_day:
                # No work days - separate red dashes in each column
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (1, row_index), (4, row_index), colors.red),
                    ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
                ]))
            elif is_sunday and record.attendance_data.get(str(day), '').strip() == 'A':
                # Sunday absent - separate red dashes, no merge
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (1, row_index), (4, row_index), colors.red),
                    ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
                ]))
            else:
                # Regular absent - merge P, OT, Bonus OT, Site No columns
                table.setStyle(TableStyle([
                    ('SPAN', (1, row_index), (4, row_index)),
                    ('TEXTCOLOR', (1, row_index), (4, row_index), colors.red),
                    ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
                    ('ALIGN', (1, row_index), (4, row_index), 'CENTER'),
                ]))
    
    # Mark Sunday OT symbols as red in OT column only
    for day in sunday_ot_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('TEXTCOLOR', (2, row_index), (2, row_index), colors.red),  # OT column only
                ('FONTNAME', (2, row_index), (2, row_index), 'Helvetica-Bold'),
            ]))
    
    # Merge and style Holiday rows - no background, black text
    for day in holiday_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('SPAN', (1, row_index), (4, row_index)),
                ('TEXTCOLOR', (1, row_index), (4, row_index), colors.black),
                ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
                ('ALIGN', (1, row_index), (4, row_index), 'CENTER'),
            ]))
    
    # Merge and style Medical rows - no background, black text
    for day in medical_rows:
        if day <= days_in_month:
            row_index = day
            table.setStyle(TableStyle([
                ('SPAN', (1, row_index), (4, row_index)),
                ('TEXTCOLOR', (1, row_index), (4, row_index), colors.black),
                ('FONTNAME', (1, row_index), (4, row_index), 'Helvetica-Bold'),
                ('ALIGN', (1, row_index), (4, row_index), 'CENTER'),
            ]))
    
    # Mark Sundays in medium dark blue - date column only, but not for Sunday absent days
    for day in range(1, days_in_month + 1):
        date_obj = datetime(record.year, month_num, day)
        if date_obj.weekday() == 6:
            row_index = day
            attendance_val = record.attendance_data.get(str(day), '').strip()
            if attendance_val != 'A':  # Not Sunday absent
                # Regular Sunday - blue background for all columns
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, row_index), (4, row_index), colors.Color(0.2, 0.4, 0.8)),
                    ('TEXTCOLOR', (0, row_index), (4, row_index), colors.white),
                    ('FONTNAME', (0, row_index), (4, row_index), 'Helvetica-Bold'),
                ]))
            else:
                # Sunday absent - only date column blue, no background for P,OT,Bonus,Site columns
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
    
    # Create bottom section with 6 rows and 4 columns
    bottom_data = [
        ['Engineer\'s Sign', 'Employee Sign', f'Present            : {total_p_days}', 'Basic'],
        ['', '', f'Absent             : {total_absent_days}', 'OT'],
        ['', '', f'Holiday            : {total_holiday_days}', 'Bonus'],
        ['', '', f'Medical Leave : {total_medical_days}', 'Gross Salary'],
        ['', '', 'Normal OT       : ', 'Adv Deduction'],
        ['', '', 'Bonus OT         : ', 'Net Salary']
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
        ('LINEBELOW', (2, 0), (2, 0), 0, colors.white),  # Remove line below Present
        ('LINEBELOW', (2, 1), (2, 1), 0, colors.white),  # Remove line below Absent
        ('LINEBELOW', (2, 2), (2, 2), 0, colors.white),  # Remove line below Normal OT
        ('LINEBELOW', (2, 3), (2, 3), 0, colors.white),  # Remove line below Medical Leave
        ('LINEBELOW', (2, 4), (2, 4), 0, colors.white),  # Remove line below Bonus OT
        ('LINEABOVE', (2, 1), (2, 1), 0, colors.white),  # Remove line above Absent
        ('LINEABOVE', (2, 2), (2, 2), 0, colors.white),  # Remove line above Normal OT
        ('LINEABOVE', (2, 3), (2, 3), 0, colors.white),  # Remove line above Medical Leave
        ('LINEABOVE', (2, 4), (2, 4), 0, colors.white),  # Remove line above Bonus OT
        ('SPAN', (2, 5), (2, 5)),  # Make last attendance row span only its own cell
        ('LINEBELOW', (3, 0), (3, 0), 0.5, colors.black),  # Keep line below Basic
    ]))
    
    # Position and draw bottom table
    bottom_table.wrapOn(p, width, height)
    bottom_table.drawOn(p, margin, bottom_y - 120)