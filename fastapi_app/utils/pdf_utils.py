import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# --- CONFIGURATION ---
# Base directories derived from the file's location
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DESIGNS_DIR = STATIC_DIR / "designs"
CARDS_DIR = STATIC_DIR / "cards"
TEMP_DIR = STATIC_DIR / "temp"

# Ensure directories exist
CARDS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# File Paths
# ⚠️ IMPORTANT: You must have 'member_front.png' in static/designs/
# Do not try to convert SVG at runtime on Windows.
TEMPLATE_PATH = DESIGNS_DIR / "member_front.png" 
FONT_PATH = "arial.ttf" 
FONT_BOLD_PATH = "arialbd.ttf" # Use bold for values if available

# Card Physical Dimensions (Standard CR80)
CARD_WIDTH_MM = 85.6
CARD_HEIGHT_MM = 54.0

# --- PIXEL COORDINATES (Matched to "For Designator.jpg" Layout) ---
# Photo (Left Side)
POS_PHOTO = (45, 130)       # Top-Left corner (x, y)
SIZE_PHOTO = (190, 230)     # Width, Height

# Text Fields (Right Side)
TEXT_X_ALIGN = 320 
LINE_HEIGHT = 55            # Vertical spacing between lines

POS_NAME = (TEXT_X_ALIGN, 160)
POS_FATHER = (TEXT_X_ALIGN, 160 + LINE_HEIGHT)
POS_CNIC = (TEXT_X_ALIGN, 160 + (LINE_HEIGHT * 2))
POS_DESIGNATION = (TEXT_X_ALIGN, 160 + (LINE_HEIGHT * 3))

# Footer Elements
POS_QR = (380, 420)        # Bottom Center-ish
SIZE_QR = (140, 140)

POS_EXPIRY = (780, 510)    # Bottom Right inside Red Box
TEXT_COLOR = (0, 0, 0)     # Black
EXPIRY_COLOR = (255, 255, 255) # White text for Expiry

DEFAULT_FONT_SIZE = 28
EXPIRY_FONT_SIZE = 32

def load_font(size, is_bold=False):
    """Safe font loading for Windows"""
    try:
        font_file = FONT_BOLD_PATH if is_bold else FONT_PATH
        return ImageFont.truetype(font_file, size)
    except OSError:
        return ImageFont.load_default()

def generate_member_card(member: dict) -> str:
    """
    Composites user data onto the PNG template matching the specific design.
    Uses Pillow (Windows safe) instead of CairoSVG.
    """
    try:
        # 1. Load Background
        if not TEMPLATE_PATH.exists():
            # Fallback warning if PNG is missing
            raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}. Please export your SVG to PNG manually.")
        
        base_image = Image.open(TEMPLATE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(base_image)
        
        font_main = load_font(DEFAULT_FONT_SIZE, is_bold=True)
        font_expiry = load_font(EXPIRY_FONT_SIZE, is_bold=True)

        # 2. Overlay Text Data
        # We assume the background PNG already has labels ("Name:", etc.)
        draw.text(POS_NAME, str(member.get("name", "")), fill=TEXT_COLOR, font=font_main)
        draw.text(POS_FATHER, str(member.get("father_name", "")), fill=TEXT_COLOR, font=font_main)
        draw.text(POS_CNIC, str(member.get("cnic", "")), fill=TEXT_COLOR, font=font_main)
        draw.text(POS_DESIGNATION, str(member.get("designation", "")), fill=TEXT_COLOR, font=font_main)

        # Expiry Date (White text, bottom right)
        draw.text(POS_EXPIRY, str(member.get("expiry_date", "")), fill=EXPIRY_COLOR, font=font_expiry, anchor="mm")

        # 3. Overlay Photo (Left Side)
        photo_path = member.get("photo_path")
        if photo_path and os.path.exists(photo_path):
            try:
                user_photo = Image.open(photo_path).convert("RGBA")
                user_photo = user_photo.resize(SIZE_PHOTO, Image.Resampling.LANCZOS)
                # Paste user photo
                base_image.paste(user_photo, POS_PHOTO, user_photo if "A" in user_photo.getbands() else None)
            except Exception as e:
                print(f"Photo Error: {e}")

        # 4. Generate & Overlay QR Code
        qr_payload = f"Name:{member.get('name')}|CNIC:{member.get('cnic')}|ID:{member.get('membership_id')}"
        
        qr = qrcode.QRCode(box_size=10, border=0) # Border 0 to blend better
        qr.add_data(qr_payload)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
        qr_img = qr_img.resize(SIZE_QR, Image.Resampling.LANCZOS)
        
        base_image.paste(qr_img, POS_QR)

        # 5. Export to PDF (ReportLab)
        final_composite = base_image.convert("RGB")
        temp_img_path = TEMP_DIR / f"{member['membership_id']}_temp.jpg"
        final_composite.save(temp_img_path, quality=100)

        pdf_filename = f"{member['membership_id']}.pdf"
        pdf_path = CARDS_DIR / pdf_filename

        c = canvas.Canvas(str(pdf_path), pagesize=(CARD_WIDTH_MM * mm, CARD_HEIGHT_MM * mm))
        # Draw image covering the full canvas
        c.drawImage(str(temp_img_path), 0, 0, width=CARD_WIDTH_MM * mm, height=CARD_HEIGHT_MM * mm)
        c.save()

        # Cleanup
        if temp_img_path.exists():
            temp_img_path.unlink()

        return str(pdf_path)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        raise e