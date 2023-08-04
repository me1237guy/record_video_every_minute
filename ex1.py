import sys
import time
import threading
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QObject, Signal, Slot


class VideoRecorder(QObject):
    new_video_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False

    def start(self):
        self.is_running = True
        self.is_paused = False
        while self.is_running:
            if not self.is_paused:
                self.record_video()
            time.sleep(1)

    def record_video(self):
        # Open the webcam
        cap = cv2.VideoCapture(0)
        # Set video format and resolution (you may need to adjust this depending on your webcam)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Get the current timestamp for unique filenames
        timestamp = time.strftime("%Y%m%d%H%M%S")
        video_filename = f"video_{timestamp}.avi"

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

        # Record for 60 seconds
        start_time = time.time()
        while time.time() - start_time < 60:
            ret, frame = cap.read()
            if ret:
                out.write(frame)

        # Release the VideoCapture and VideoWriter objects
        cap.release()
        out.release()

        # Emit the signal to notify that a new video was recorded
        self.new_video_signal.emit(video_filename)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Recorder")
        self.recorder_thread = None
        self.init_ui()

    def init_ui(self):
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_recording)
        self.start_button.move(20, 20)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_recording)
        self.pause_button.move(100, 20)

        self.resume_button = QPushButton("Resume", self)
        self.resume_button.clicked.connect(self.resume_recording)
        self.resume_button.move(180, 20)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.move(260, 20)

        # self.new_video_button = QPushButton("New Video", self)
        # self.new_video_button.clicked.connect(self.show_new_video_message)
        # self.new_video_button.move(340, 20)

        self.recorder_thread = threading.Thread(target=self.run_recorder_thread)

    def start_recording(self):
        if not self.recorder_thread.is_alive():
            self.recorder_thread = threading.Thread(target=self.run_recorder_thread)
        self.recorder_thread.start()

    def run_recorder_thread(self):
        self.recorder = VideoRecorder()
        self.recorder.new_video_signal.connect(self.handle_new_video)
        self.recorder.start()

    def pause_recording(self):
        if self.recorder:
            self.recorder.pause()

    def resume_recording(self):
        if self.recorder:
            self.recorder.resume()

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()

    @Slot(str)
    def handle_new_video(self, filename):
        print(f"New video recorded: {filename}")

    # def show_new_video_message(self):
    #     print("New video requested!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 80)
    window.show()
    sys.exit(app.exec())
