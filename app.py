import streamlit as st
import pyqrcode
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from pyzbar.pyzbar import decode

st.set_page_config(page_title="QR Code App", page_icon="🔗")

st.title("QR Code Generator & Scanner")

option = st.radio("Choose an option:", ["Generate QR Code", "Scan QR Code"])

# ------------------- Generate QR -------------------
if option == "Generate QR Code":
    data = st.text_input("Enter text to encode:")
    if data:
        qr = pyqrcode.create(data)
        buffer = BytesIO()
        qr.png(buffer, scale=6)
        buffer.seek(0)
        st.image(buffer, caption="Generated QR Code")
        st.download_button("Download QR Code", buffer, file_name="qrcode.png", mime="image/png")

# ------------------- Scan QR -------------------
elif option == "Scan QR Code":
    uploaded_file = st.file_uploader("Upload an image with QR code", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        decoded_objects = decode(frame)
        if decoded_objects:
            st.success("Decoded Data:")
            for obj in decoded_objects:
                st.write(obj.data.decode("utf-8"))
        else:
            st.warning("No QR code detected.")
