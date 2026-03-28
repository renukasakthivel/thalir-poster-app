import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io

try:
    from rembg import remove
    REMBG = True
except:
    REMBG = False

st.title("🛍️ Thalir Saree Poster Generator")

# INPUTS
price = st.text_input("Price", "680")
phone = st.text_input("Phone", "+91 9342665700")

saree_type = st.text_input("Saree Name", "Mul Mul cotton sarees")

feature1 = "✓ " + st.text_input("Feature 1", "Soft & Breathable")
feature2 = "✓ " + st.text_input("Feature 2", "Lightweight")
feature3 = "✓ " + st.text_input("Feature 3", "Easy Wash")

uploaded_files = st.file_uploader("Upload Sarees", accept_multiple_files=True)

# ✅ SAFE FONT FUNCTION (NO ERROR)
def get_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

# AUTO TEXT FIT
def fit_text(draw, text, max_width, start_size=50):
    size = start_size
    while size > 15:
        font = get_font(size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return get_font(20)

# CENTER TEXT
def draw_center(draw, x, y, text, font, color):
    w = draw.textlength(text, font=font)
    draw.text((x - w//2, y), text, fill=color, font=font)

if st.button("Generate Posters"):

    for idx, file in enumerate(uploaded_files):

        poster = Image.open("assets/template.png").convert("RGBA").resize((1080,1350))
        draw = ImageDraw.Draw(poster)

        font_small = get_font(26)

        # IMAGE
        img = Image.open(file).convert("RGBA")
        saree = remove(img) if REMBG else img
        saree = ImageEnhance.Brightness(saree).enhance(1.2)
        saree = saree.resize((520,750))

        x = (1080-520)//2
        y = 240

        shadow = saree.copy().filter(ImageFilter.GaussianBlur(10))
        poster.paste(shadow, (x+20,y+30), shadow)
        poster.paste(saree, (x,y), saree)

        # LOGO
        try:
            logo = Image.open("assets/logo.png").convert("RGBA").resize((130,130))
            poster.paste(logo, (x+300, y+480), logo)
        except:
            pass

        # PRICE BOX
        box = (820, 400, 1030, 520)
        draw.rounded_rectangle(box, radius=50, fill="#b30000")

        cx = (box[0]+box[2])//2
        cy = (box[1]+box[3])//2

        draw_center(draw, cx, 420, "PRICE", font_small, "#ffffff")

        price_text = f"₹{price}"
        font_big = fit_text(draw, price_text, 220, 65)

        draw_center(draw, cx+2, cy-8, price_text, font_big, "#000000")
        draw_center(draw, cx, cy-10, price_text, font_big, "#ffffff")

        # NAME
        name_y = y + 750 + 110
        font_name = fit_text(draw, saree_type, 800, 52)
        draw_center(draw, 540, name_y, saree_type, font_name, "#2f4f2f")

        fy = name_y + 110

        # FEATURES
        center_x = 540
        gap = 280

        x1 = center_x - gap
        x2 = center_x
        x3 = center_x + gap

        f1 = fit_text(draw, feature1, 250, 28)
        f2 = fit_text(draw, feature2, 250, 28)
        f3 = fit_text(draw, feature3, 250, 28)

        draw_center(draw, x1, fy, feature1, f1, "#2f4f2f")
        draw_center(draw, x2, fy, feature2, f2, "#2f4f2f")
        draw_center(draw, x3, fy, feature3, f3, "#2f4f2f")

        # GOLD LINES
        m1 = (x1 + x2) // 2
        m2 = (x2 + x3) // 2

        draw.line((m1, fy-10, m1, fy+30), fill="#caa84a", width=2)
        draw.line((m2, fy-10, m2, fy+30), fill="#caa84a", width=2)
        draw.line((x1-60, fy+60, x3+60, fy+60), fill="#caa84a", width=2)

        # ORDER BOX
        order_y = fy + 65

        draw.rounded_rectangle(
            (180, order_y, 900, order_y+70),
            radius=40,
            fill="#fffdf5",
            outline="#caa84a",
            width=2
        )

        order_text = f"📞 To Order: {phone}"
        font_order = fit_text(draw, order_text, 650, 30)

        draw_center(draw, 540, order_y+20, order_text, font_order, "#2f4f2f")

        # SHOW
        st.image(poster, caption=f"Poster {idx+1}")

        # DOWNLOAD
        buf = io.BytesIO()
        poster.save(buf, format="PNG")

        st.download_button(
            f"⬇ Download Poster {idx+1}",
            data=buf.getvalue(),
            file_name=f"poster_{idx+1}.png",
            mime="image/png"
        )

    st.success("🔥 Posters Generated Successfully!")
