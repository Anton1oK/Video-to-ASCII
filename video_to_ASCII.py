import cv2
import brotli
import json

# Settings
VIDEO_PATH = 'Video/input_video.mp4'  # Replace with your video file
OUTPUT_JSON = 'Result/ascii_frames.json.br'
FRAME_WIDTH = 80  # Adjust for ASCII width (smaller for lighter size)
FRAME_RATE = 10  # Frames per second in the final animation

# ASCII characters for different brightness levels
ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(image, width):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, original_width = gray_image.shape
    aspect_ratio = height / original_width
    new_height = int(aspect_ratio * width * 0.55)  # 0.55 to adjust for character height
    resized_gray = cv2.resize(gray_image, (width, new_height))

    # Map pixels to ASCII characters
    ascii_frame = ""
    for row in resized_gray:
        line = "".join(ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in row)
        ascii_frame += line + "\n"
    return ascii_frame

def process_video(video_path, width, frame_rate):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frame_rate)

    ascii_frames = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            ascii_frame = frame_to_ascii(frame, width)
            ascii_frames.append(ascii_frame)
        frame_count += 1

    cap.release()
    return ascii_frames

def save_compressed_json(data, output_path):
    json_data = json.dumps(data).encode('utf-8')
    compressed_data = brotli.compress(json_data)
    with open(output_path, 'wb') as f:
        f.write(compressed_data)

# Process and save
ascii_frames = process_video(VIDEO_PATH, FRAME_WIDTH, FRAME_RATE)
save_compressed_json(ascii_frames, OUTPUT_JSON)

print(f"Processed {len(ascii_frames)} frames and saved to {OUTPUT_JSON}")