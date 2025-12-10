import os
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

MM_WIDTH = 85.6
MM_HEIGHT = 54.0
DPI = 300
INCH_WIDTH = MM_WIDTH / 25.4
INCH_HEIGHT = MM_HEIGHT / 25.4
PX_WIDTH = int(INCH_WIDTH * DPI)
PX_HEIGHT = int(INCH_HEIGHT * DPI)

def _font(size: int) -> ImageFont.FreeTypeFont:
    paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Helvetica.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for p in paths:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def member_front_png(path: str) -> None:
    img = Image.new("RGB", (PX_WIDTH, PX_HEIGHT), (255, 255, 255))
    d = ImageDraw.Draw(img)
    green = (11, 143, 88)
    dark = (30, 30, 30)
    # Top banner
    d.rectangle([0, 0, PX_WIDTH, int(PX_HEIGHT*0.315)], fill=green)
    # Bottom ribbon
    d.rectangle([0, int(PX_HEIGHT*0.796), PX_WIDTH, PX_HEIGHT], fill=green)
    # Diagonal
    d.polygon([(0, int(PX_HEIGHT*0.796)), (int(PX_WIDTH*0.28), int(PX_HEIGHT*0.796)), (int(PX_WIDTH*0.25), PX_HEIGHT), (0, PX_HEIGHT)], fill=dark)
    # Logo circle
    cx, cy, r = int(PX_WIDTH*0.1), int(PX_HEIGHT*0.157), int(PX_HEIGHT*0.102)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=green, outline=(255,255,255), width=6)
    ftitle = _font(36)
    fsub = _font(20)
    d.text((PX_WIDTH//2, int(PX_HEIGHT*0.12)), "PAKISTAN CIVIL SOLDIER MOVEMENT", font=ftitle, fill=(255,255,255), anchor="mm")
    d.text((PX_WIDTH//2, int(PX_HEIGHT*0.195)), "Pak Forces, Pak Nation and Pakistan is One", font=fsub, fill=(232,247,239), anchor="mm")
    # Membership card label
    d.rounded_rectangle([int(PX_WIDTH*0.286), int(PX_HEIGHT*0.278), int(PX_WIDTH*0.52), int(PX_HEIGHT*0.352)], 12, fill=(198,40,40))
    d.text((int(PX_WIDTH*0.403), int(PX_HEIGHT*0.318)), "MEMBERSHIP CARD", font=_font(22), fill=(255,255,255), anchor="mm")
    # Photo placeholder
    d.rectangle([int(PX_WIDTH*0.07), int(PX_HEIGHT*0.352), int(PX_WIDTH*0.255), int(PX_HEIGHT*0.704)], outline=(136,136,136), width=3, fill=(208,208,208))
    d.text((int(PX_WIDTH*0.162), int(PX_HEIGHT*0.606)), "PHOTO", font=_font(16), fill=(85,85,85), anchor="mm")
    # Seal 786
    d.ellipse([int(PX_WIDTH*0.198)-22, int(PX_HEIGHT*0.648)-22, int(PX_WIDTH*0.198)+22, int(PX_HEIGHT*0.648)+22], fill=green, outline=(255,255,255), width=4)
    d.text((int(PX_WIDTH*0.198), int(PX_HEIGHT*0.648)), "786", font=_font(16), fill=(255,255,255), anchor="mm")
    # QR placeholder
    d.rectangle([int(PX_WIDTH*0.327), int(PX_HEIGHT*0.389), int(PX_WIDTH*0.573), int(PX_HEIGHT*0.778)], outline=(30,30,30), width=3, fill=(255,255,255))
    d.text((int(PX_WIDTH*0.45), int(PX_HEIGHT*0.584)), "QR CODE", font=_font(18), fill=(30,30,30), anchor="mm")
    # Fields
    fbold = _font(18)
    fnorm = _font(18)
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.38)), "Name", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.689), int(PX_HEIGHT*0.38)), ": Muhammad Ismail Khan", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.435)), "Father Name", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.764), int(PX_HEIGHT*0.435)), ": Sher Muhammad", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.49)), "CNIC", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.689), int(PX_HEIGHT*0.49)), ": 17301-6858660-9", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.545)), "DESIGNATION", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.777), int(PX_HEIGHT*0.545)), ": Member District Peshawar", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.6)), "Membership ID", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.777), int(PX_HEIGHT*0.6)), ": PCSM-XXXX", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.655)), "Membership Type", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.777), int(PX_HEIGHT*0.655)), ": Standard", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.71)), "Region/District", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.777), int(PX_HEIGHT*0.71)), ": Peshawar", font=fnorm, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.608), int(PX_HEIGHT*0.765)), "Issue Date", font=fbold, fill=(0,0,0))
    d.text((int(PX_WIDTH*0.69), int(PX_HEIGHT*0.765)), ": Oct-2025", font=fnorm, fill=(0,0,0))
    # Expiry box
    d.rounded_rectangle([int(PX_WIDTH*0.606), int(PX_HEIGHT*0.63), int(PX_WIDTH*0.864), int(PX_HEIGHT*0.74)], 12, fill=(198,40,40))
    d.text((int(PX_WIDTH*0.625), int(PX_HEIGHT*0.665)), "EXPIRY DATE", font=_font(20), fill=(255,255,255))
    d.text((int(PX_WIDTH*0.625), int(PX_HEIGHT*0.705)), "Oct-2026", font=_font(24), fill=(255,255,255))
    # Footer
    d.text((int(PX_WIDTH*0.1), int(PX_HEIGHT*0.88)), "Issued by PCSM", font=_font(20), fill=(255,255,255))
    img.save(path, format="PNG", dpi=(DPI, DPI))

def designator_front_png(path: str) -> None:
    img = Image.new("RGB", (PX_WIDTH, PX_HEIGHT), (11,11,11))
    d = ImageDraw.Draw(img)
    green = (11, 143, 88)
    # Top banner
    d.rectangle([0, 0, PX_WIDTH, int(PX_HEIGHT*0.259)], fill=green)
    d.text((PX_WIDTH//2, int(PX_HEIGHT*0.12)), "PAKISTAN CIVIL SOLDIER MOVEMENT", font=_font(34), fill=(255,255,255), anchor="mm")
    d.text((PX_WIDTH//2, int(PX_HEIGHT*0.195)), "Recognized by Government of Pakistan", font=_font(24), fill=(232,247,239), anchor="mm")
    # Flag
    d.rectangle([int(PX_WIDTH*0.86), int(PX_HEIGHT*0.046), int(PX_WIDTH*0.98), int(PX_HEIGHT*0.175)], fill=(16,123,62), outline=(255,255,255), width=4)
    # Card content
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.333)), "Reg. : 214332", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.83), int(PX_HEIGHT*0.333)), "Date : Oct-2025", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.407)), "MEMBERSHIP CARD", font=_font(22), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.463)), "Name :", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.19), int(PX_HEIGHT*0.463)), " Muhammad Ismail", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.518)), "Father Name :", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.28), int(PX_HEIGHT*0.518)), " Noor Hamid Jan", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.573)), "CNIC # :", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.2), int(PX_HEIGHT*0.573)), " 152303-9974536-3", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.07), int(PX_HEIGHT*0.628)), "Designation :", font=_font(18), fill=(224,224,224))
    d.text((int(PX_WIDTH*0.27), int(PX_HEIGHT*0.628)), " Deputy General Secretary – District Lower Dir", font=_font(18), fill=(224,224,224))
    # Photo
    d.rectangle([int(PX_WIDTH*0.74), int(PX_HEIGHT*0.389), int(PX_WIDTH*0.92), int(PX_HEIGHT*0.741)], outline=(136,136,136), width=3, fill=(42,42,42))
    d.text((int(PX_WIDTH*0.83), int(PX_HEIGHT*0.606)), "PHOTO", font=_font(16), fill=(187,187,187), anchor="mm")
    # Seal 786
    d.ellipse([int(PX_WIDTH*0.876)-22, int(PX_HEIGHT*0.685)-22, int(PX_WIDTH*0.876)+22, int(PX_HEIGHT*0.685)+22], fill=green, outline=(255,255,255), width=4)
    d.text((int(PX_WIDTH*0.876), int(PX_HEIGHT*0.685)), "786", font=_font(16), fill=(255,255,255), anchor="mm")
    # QR placeholder
    d.rectangle([int(PX_WIDTH*0.374), int(PX_HEIGHT*0.704), int(PX_WIDTH*0.62), int(PX_HEIGHT*0.999)], outline=(30,30,30), width=3, fill=(255,255,255))
    d.text((int(PX_WIDTH*0.497), int(PX_HEIGHT*0.85)), "QR CODE", font=_font(18), fill=(30,30,30), anchor="mm")
    # Expiry
    d.rounded_rectangle([int(PX_WIDTH*0.035), int(PX_HEIGHT*0.759), int(PX_WIDTH*0.383), int(PX_HEIGHT*0.889)], 12, fill=(198,40,40))
    d.text((int(PX_WIDTH*0.06), int(PX_HEIGHT*0.805)), "EXPIRY DATE", font=_font(20), fill=(255,255,255))
    d.text((int(PX_WIDTH*0.06), int(PX_HEIGHT*0.85)), "Oct-2026", font=_font(24), fill=(255,255,255))
    img.save(path, format="PNG", dpi=(DPI, DPI))

def png_to_pdf(png_path: str, pdf_path: str) -> None:
    pdf = FPDF(orientation="L", unit="mm", format=(MM_WIDTH, MM_HEIGHT))
    pdf.add_page()
    pdf.image(png_path, x=0, y=0, w=MM_WIDTH, h=MM_HEIGHT)
    pdf.output(pdf_path)

def main() -> None:
    base = os.path.join("fastapi_app", "static", "designs")
    os.makedirs(base, exist_ok=True)
    m_png = os.path.join(base, "member_front.png")
    d_png = os.path.join(base, "designator_front.png")
    member_front_png(m_png)
    designator_front_png(d_png)
    png_to_pdf(m_png, os.path.join(base, "member_front.pdf"))
    png_to_pdf(d_png, os.path.join(base, "designator_front.pdf"))

if __name__ == "__main__":
    main()

