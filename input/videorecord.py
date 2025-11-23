import cv2
import threading
import time

class VideoRecorder(threading.Thread):
    def __init__(self, filename="output.avi", fps=20, resolution=(640, 480)):
        super().__init__()
        self.filename = filename
        self.fps = fps
        self.resolution = resolution
        self.cap = cv2.VideoCapture(0)  # 0 for default webcam
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, self.resolution)
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)
            time.sleep(1 / self.fps)  # Control frame rate

    def stop(self):
        self.running = False
        self.cap.release()
        self.out.release()