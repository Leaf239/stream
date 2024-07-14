import cv2
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import numpy as np  # Import NumPy

class Camera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.font_path = 'fonts/SCDream6.otf'
        self.font = ImageFont.truetype(self.font_path, 24)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return None

        # Convert the frame to a PIL image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # Draw text on the image
        draw = ImageDraw.Draw(pil_img)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate text size and position
        text_size = draw.textsize(f'Kami Cam - {now}', font=self.font)
        text_width, text_height = text_size
        frame_width, frame_height = pil_img.size
        position = (frame_width - text_width - 10, frame_height - text_height - 10)  # Bottom right corner with padding

        draw.text(position, f'Kami Cam - {now}', font=self.font, fill=(255, 255, 255, 255))

        # Convert back to OpenCV format
        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None
        return jpeg.tobytes()
