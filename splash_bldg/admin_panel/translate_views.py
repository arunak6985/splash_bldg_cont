from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .views import custom_staff_required
import os
import io

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import RGBColor, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

@custom_staff_required
def pdf_translate(request):
    """PDF translation page"""
    return render(request, 'pdf_translate.html')

@csrf_exempt
@custom_staff_required
def process_pdf_translate(request):
    """Process uploaded PDF/DOCX and translate to Arabic maintaining format"""
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        try:
            if not TRANSLATOR_AVAILABLE:
                return JsonResponse({'success': False, 'message': 'Install: pip install googletrans==4.0.0rc1'})
            
            uploaded_file = request.FILES['pdf_file']
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            # Handle Word documents
            if file_ext in ['.docx', '.doc']:
                if not DOCX_AVAILABLE:
                    return JsonResponse({'success': False, 'message': 'Install: pip install python-docx'})
                
                # Read Word document
                doc = Document(uploaded_file)
                translator = Translator()
                
                # Translate each paragraph preserving formatting
                for para in doc.paragraphs:
                    if para.text.strip():
                        try:
                            # Translate with better handling
                            original_text = para.text
                            translated = translator.translate(original_text, src='en', dest='ar')
                            
                            # Clear paragraph and add translated text with formatting
                            for run in para.runs:
                                run.text = ''
                            
                            if para.runs:
                                para.runs[0].text = translated.text
                            else:
                                para.add_run(translated.text)
                            
                            # Set right-to-left alignment for Arabic
                            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                            
                            # Set font for Arabic support
                            for run in para.runs:
                                run.font.name = 'Arial'
                                run.font.size = Pt(12)
                        except Exception as e:
                            print(f"Translation error: {e}")
                            pass
                
                # Translate tables
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for para in cell.paragraphs:
                                if para.text.strip():
                                    try:
                                        original_text = para.text
                                        translated = translator.translate(original_text, src='en', dest='ar')
                                        
                                        for run in para.runs:
                                            run.text = ''
                                        
                                        if para.runs:
                                            para.runs[0].text = translated.text
                                        else:
                                            para.add_run(translated.text)
                                        
                                        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                                        
                                        for run in para.runs:
                                            run.font.name = 'Arial'
                                            run.font.size = Pt(11)
                                    except:
                                        pass
                
                # Save translated document
                output_filename = f"arabic_{uploaded_file.name}"
                output_dir = os.path.join('media', 'translations')
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, output_filename)
                doc.save(output_path)
                
                return JsonResponse({
                    'success': True,
                    'filename': output_filename,
                    'download_url': f'/media/translations/{output_filename}',
                    'message': 'Word document translated successfully to Arabic'
                })
            
            # Handle PDF documents
            elif file_ext == '.pdf':
                if not PYMUPDF_AVAILABLE:
                    return JsonResponse({'success': False, 'message': 'Install: pip install PyMuPDF'})
                
                pdf_bytes = uploaded_file.read()
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                translator = Translator()
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    blocks = page.get_text("dict")["blocks"]
                    
                    for block in blocks:
                        if block.get("type") == 0:
                            for line in block.get("lines", []):
                                for span in line.get("spans", []):
                                    text = span.get("text", "").strip()
                                    
                                    if text and len(text) > 1:
                                        try:
                                            translated = translator.translate(text, src='en', dest='ar')
                                            arabic_text = translated.text
                                            bbox = span["bbox"]
                                            font_size = span["size"]
                                            
                                            page.add_redact_annot(bbox, fill=(1, 1, 1))
                                            page.apply_redactions()
                                            
                                            page.insert_text(
                                                (bbox[2], bbox[3]),
                                                arabic_text,
                                                fontsize=font_size,
                                                fontname="helv",
                                                color=(0, 0, 0),
                                                rotate=0
                                            )
                                        except:
                                            pass
                
                output_filename = f"arabic_{uploaded_file.name}"
                output_dir = os.path.join('media', 'translations')
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, output_filename)
                
                doc.save(output_path)
                doc.close()
                
                return JsonResponse({
                    'success': True,
                    'filename': output_filename,
                    'download_url': f'/media/translations/{output_filename}',
                    'message': 'PDF translated successfully to Arabic'
                })
            
            else:
                return JsonResponse({'success': False, 'message': 'Only PDF and DOCX files are supported'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'No file uploaded'})
