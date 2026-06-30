import cv2


class Camera:
    def __init__(self, index=0):
        self.index = index
        self.cap = None
        self.active = False

    def start(self):
        self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = None
            return False
        self.active = True
        return True

    def stop(self):
        self.active = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        if not self.cap:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame