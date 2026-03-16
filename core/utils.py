import base64
import cv2
import numpy as np
import json

def decode_image(img_str):
    try:
        if isinstance(img_str, str):
            # If it's a JSON string from the websocket, parse it
            if img_str.startswith('{'):
                data = json.loads(img_str)
                img_str = data.get('image', '')
            
            if ',' in img_str:
                img_str = img_str.split(',')[1]
                
            img_data = base64.b64decode(img_str)
            nparr = np.frombuffer(img_data, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error decoding image: {e}")
    return None

def encode_image(frame, quality=50):
    try:
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        encoded_img = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_img}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""
