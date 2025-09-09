import streamlit as st
import qrcode
from fpdf import FPDF
from math import ceil
from PIL import Image
import os
import tempfile

# ส่วนหัวโปรแกรม
st.title("📄 QR Code Generator to PDF")
st.write("อัปโหลดไฟล์ .txt ที่มีรายการรหัส (ทีละบรรทัด) → โปรแกรมจะสร้าง QR Code PDF ให้คุณ")

# อัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์ .txt", type=["txt"])

if uploaded_file is not None:
    # อ่านรหัสจากไฟล์
    content = uploaded_file.read().decode("utf-8")
    ids = [line.strip() for line in content.splitlines() if line.strip().isdigit()]

    if len(ids) == 0:
        st.error("❌ ไม่พบรหัสในไฟล์ (ต้องเป็นตัวเลขทีละบรรทัด)")
    else:
        st.success(f"✅ พบ {len(ids)} รหัส")

        if st.button("สร้าง PDF"):
            with tempfile.TemporaryDirectory() as tmpdir:
                image_paths = []

                # สร้าง QR Code
                for id_code in ids:
                    qr = qrcode.make(id_code)
                    path = os.path.join(tmpdir, f"{id_code}.png")
                    qr.save(path)
                    image_paths.append((path, id_code))

                # สร้าง PDF
                pdf = FPDF()
                pdf.set_auto_page_break(False)

                cols, rows = 4, 5
                qr_size = 40  # mm
                x_margin, y_margin = 10, 10

                cell_width = (210 - 2 * x_margin) / cols
                cell_height = (297 - 2 * y_margin) / rows

                for page in range(ceil(len(image_paths) / 20)):
                    pdf.add_page()

                    # วาดเส้นแนวตั้ง
                    for i in range(cols + 1):
                        x = x_margin + i * cell_width
                        pdf.line(x, y_margin, x, 297 - y_margin)

                    # วาดเส้นแนวนอน
                    for j in range(rows + 1):
                        y = y_margin + j * cell_height
                        pdf.line(x_margin, y, 210 - x_margin, y)

                    # วาง QR
                    for i in range(20):
                        index = page * 20 + i
                        if index >= len(image_paths):
                            break
                        image_path, code = image_paths[index]

                        col = i % cols
                        row = i // cols
                        x = x_margin + col * cell_width
                        y = y_margin + row * cell_height

                        qr_x = x + (cell_width - qr_size) / 2
                        qr_y = y + (cell_height - qr_size) / 2 - 5

                        pdf.image(image_path, x=qr_x, y=qr_y, w=qr_size, h=qr_size)

                        pdf.set_xy(x, qr_y + qr_size + 2)
                        pdf.set_font("Arial", size=8)
                        pdf.cell(cell_width, 5, code, align='C')

                output_file = os.path.join(tmpdir, "qr_codes.pdf")
                pdf.output(output_file)

                with open(output_file, "rb") as f:
                    st.download_button(
                        label="⬇️ ดาวน์โหลด PDF",
                        data=f,
                        file_name="qr_codes.pdf",
                        mime="application/pdf"
                    )
