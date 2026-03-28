import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import io

try:
    from rembg import remove
    REMBG = True
except:
    REMBG = False

st.title("🛍️ Thalir Saree Poster Generator")

# INPUTS
saree_list = ["Mul Mul Cotton", "Silk Saree", "Linen Saree", "Banarasi"]
selected_saree = st.selectbox("Select Saree Name", saree_list)
custom_saree = st.text_input("Or Enter Custom Saree Name")
saree_type = custom_saree if custom_saree else selected_saree

feature_list = ["Soft & Breathable", "Lightweight", "Premium Quality", "Easy Wash"]

def feature_input(label):
    choice = st.selectbox(label, ["Select"] + feature_list)
    custom = st.text_input(f"Custom {label}")
    return custom if custom else (choice if choice != "Select" else "")

feature1 = "✓ " + feature_input("Feature 1")
feature2 = "✓ " + feature_input("Feature 2")
feature3 = "✓ " + feature_input("Feature 3")

price = st.text_input("Price", "680")
phone = st.text_input("Phone", "+91 9342665700")

uploaded_files = st.file_uploader("Upload Sarees", accept_multiple_files=True)

# FONT
def font(size):
    try:
        return ImageFont.truetype("assets/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def draw_center(draw, x, y, text, f, color):
    w = draw.textlength(text, font=f)
    draw.text((x - w//2, y), text, fill=color, font=f)

if st.button("Generate Posters"):

    for idx, file in enumerate(uploaded_files):

        poster = Image.open("assets/template.png").convert("RGBA").resize((1080,1350))
        draw = ImageDraw.Draw(poster)

        # IMAGE
        img = Image.open(file).convert("RGBA")
        saree = remove(img) if REMBG else img

        # ✅ NATURAL LOOK (NO COLOR DAMAGE)
        saree = ImageEnhance.Brightness(saree).enhance(1.05)
        saree = ImageEnhance.Contrast(saree).enhance(1.03)
        saree = ImageEnhance.Sharpness(saree).enhance(1.08)

        saree = saree.resize((520,750))

        x = (1080-520)//2
        y = 240

        # ❌ NO HEAVY SHADOW (clean look)
        poster.paste(saree, (x,y), saree)

        # ✅ LOGO (FIXED)
        try:
            logo = Image.open("assets/logo.png").convert("RGBA").resize((140,140))
            poster.paste(logo, (x+280, y+470), logo)
        except:
            pass

        # PRICE BOX
        box = (820, 400, 1040, 560)
        draw.rounded_rectangle(box, radius=60, fill="#b30000")

        cx = (box[0]+box[2])//2
        cy = (box[1]+box[3])//2

        draw_center(draw, cx, 420, "PRICE", font(30), "#ffffff")

        price_text = f"₹{price}"
        draw_center(draw, cx+2, cy-5, price_text, font(65), "#000")
        draw_center(draw, cx, cy-8, price_text, font(65), "#ffffff")

        # NAME
        name_y = y + 850
        draw_center(draw, 540, name_y, saree_type, font(52), "#1a2e1a")

        # FEATURES (EVEN SPACING)
        fy = name_y + 110
        gap = 300

        def clean(text): return text[:22]

        f1 = clean(feature1)
        f2 = clean(feature2)
        f3 = clean(feature3)

        draw_center(draw, 540-gap, fy, f1, font(24), "#1a2e1a")
        draw_center(draw, 540, fy, f2, font(24), "#1a2e1a")
        draw_center(draw, 540+gap, fy, f3, font(24), "#1a2e1a")

        draw.line((540-gap//2, fy-10, 540-gap//2, fy+25), fill="#caa84a", width=2)
        draw.line((540+gap//2, fy-10, 540+gap//2, fy+25), fill="#caa84a", width=2)

        # ORDER BOX (FINAL PERFECT POSITION)
        order_y = fy + 60

        box_top = order_y
        box_bottom = order_y + 70

        draw.rounded_rectangle((180, box_top, 900, box_bottom),
                               radius=40,
                               fill="#fffdf5",
                               outline="#caa84a",
                               width=2)

        # ✅ PERFECT CENTER + SLIGHT UP
        center_y = (box_top + box_bottom) // 2 - 8

        draw_center(draw, 540, center_y,
                    f"📞 To Order: {phone}",
                    font(32),
                    "#1a2e1a")

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
