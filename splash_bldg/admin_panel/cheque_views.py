from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import custom_staff_required
import os
import re
from PIL import Image
import cv2
import numpy as np
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

@custom_staff_required
def cheque_upload(request):
    """Cheque upload page"""
    return render(request, 'cheque_upload.html')

@csrf_exempt
@custom_staff_required
def process_cheque_upload(request):
    """Process uploaded cheque image and extract cheque number"""
    if request.method == 'POST' and request.FILES.get('cheque_image'):
        try:
            uploaded_file = request.FILES['cheque_image']
            manual_number = request.POST.get('manual_cheque_number', '').strip()
            
            if manual_number:
                cheque_number = manual_number
            else:
                cheque_number, _ = extract_cheque_from_image_ocr(uploaded_file)
                if not cheque_number:
                    import time
                    cheque_number = str(int(time.time()))[-6:]
            
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = f"{cheque_number}{file_extension}"
            
            media_dir = 'media/cheques'
            os.makedirs(media_dir, exist_ok=True)
            
            uploaded_file.seek(0)
            file_path = os.path.join(media_dir, new_filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'success': True,
                'cheque_number': cheque_number,
                'filename': new_filename,
                'file_path': file_path,
                'download_url': f'/media/cheques/{new_filename}',
                'message': f'Cheque uploaded successfully with number: {cheque_number}'
            })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'No image uploaded'})

def extract_cheque_from_image_ocr(uploaded_file):
    """Extract cheque number from image using OCR - simplified"""
    try:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        height, width = gray.shape
        
        if TESSERACT_AVAILABLE:
            # Scan entire image for "Cheque No." text
            full_text = pytesseract.image_to_string(gray, config='--psm 6')
            
            # Look for "Cheque No." pattern - try multiple variations
            cheque_patterns = [
                r'Cheque\s*No\.?\s*[:\s]*(\d{6,7})',
                r'Check\s*No\.?\s*[:\s]*(\d{6,7})',
                r'cheque\s*No\.?\s*[:\s]*(\d{6,7})',
                r'No\.?\s*(\d{6,7})',
            ]
            
            for pattern in cheque_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    num = match.group(1)
                    # Prefer numbers starting with 0
                    if num.startswith('0'):
                        return num, None
            
            # Return first match even if doesn't start with 0
            for pattern in cheque_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return match.group(1), None
        
        return None, None
    except:
        return None, None

def extract_cheque_from_text(text):
    """Extract cheque number from OCR text"""
    print(f"OCR Text: {text}")
    
    # Clean text - remove spaces and special chars
    cleaned = re.sub(r'[^0-9\n]', ' ', text)
    
    patterns = [
        r'By.*?Cheque.*?No.*?(\d{6})',
        r'Cheque.*?No.*?(\d{6})',
        r'Check.*?No.*?(\d{6})',
        r'(0\d{5})',
        r'(\d{6})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            for match in matches:
                match = match.strip()
                if len(match) == 6 and match.isdigit():
                    if not match.startswith(('20', '19', '24', '25', '26')):
                        return match
    
    # Fallback: find all 6-digit numbers
    all_numbers = re.findall(r'\b\d{6}\b', cleaned)
    for num in all_numbers:
        if not num.startswith(('20', '19', '24', '25', '26')):
            return num
    
    return None

def extract_cheque_from_filename(filename):
    """Extract cheque number from filename"""
    # Look for 6-8 digit numbers in filename
    numbers = re.findall(r'\d{6,8}', filename)
    return numbers[0] if numbers else None

def extract_cheque_from_image_name(filename):
    """Extract numbers from image filename like img20260128_18305928.jpg"""
    # Remove extension and split by underscore
    name_without_ext = os.path.splitext(filename)[0]
    parts = name_without_ext.split('_')
    
    # Look for the part after underscore (like 18305928)
    if len(parts) > 1:
        return parts[-1]  # Return last part after underscore
    
    # Fallback to any 6+ digit number
    numbers = re.findall(r'\d{6,}', filename)
    return numbers[0] if numbers else None