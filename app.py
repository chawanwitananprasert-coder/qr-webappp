import streamlit as st
import pyqrcode
from io import BytesIO
from PIL import Image
import cv2
from pyzbar.pyzbar import decode

def generate_qr_code(data):
    qr = pyqrcode.create(data)
    buffer = BytesIO()
    qr.png(buffer, scale=6)
    buffer.seek(0)
    return buffer

def decode_qr_code(image):
    img = Image.open(image)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    decoded_objects = decode(frame)
    return [obj.data.decode('utf-8') for obj in decoded_objects]

st.title("QR Code Generator and Scanner")

option = st.radio("Choose an option", ["Generate QR Code", "Scan QR Code"])

if option == "Generate QR Code":
    data = st.text_input("Enter data to encode")
    if data:
        qr_image = generate_qr_code(data)
        st.image(qr_image, caption="Generated QR Code", use_column_width=True)
        st.download_button("Download QR Code", qr_image, "qrcode.png", "image/png")

elif option == "Scan QR Code":
    uploaded_file = st.file_uploader("Upload an image with a QR code", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        decoded_data = decode_qr_code(uploaded_file)
        if decoded_data:
            st.write("Decoded QR Code Data:", decoded_data)
        else:
            st.write("No QR code detected.")
