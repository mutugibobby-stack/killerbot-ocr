from flask import Flask, request
import cv2
import numpy as np
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])

def preprocess(img_bytes):
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cropped = img[100:200, 300:600]  # 🔧 Adjust these values to match your multiplier zone
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_multiplier(image):
    result = reader.readtext(image)
    for _, text, _ in result:
        cleaned = text.replace('O', '0').replace('x', '').replace('X', '').strip()
        try:
            return float(cleaned)
        except:
            continue
    return None

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    image = preprocess(file.read())
    multiplier = extract_multiplier(image)
    return {'multiplier': multiplier or 'unreadable'}

if __name__ == '__main__':
    app.run()
