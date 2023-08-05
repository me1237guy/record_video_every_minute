import sys
import time
import threading
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QObject, Signal, Slot, QTime


class VideoRecorder(QObject):
    # a new video file created
    new_video_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.video_writer = None
      
    def create_video(self):
        timestamp = time.strftime("%Y_%m_%d_%H%M_%S")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        video_filename = f"video_{timestamp}.avi"
        self.video_writer = cv2.VideoWriter(video_filename, fourcc, 25.0, (640, 480))
        self.start_time = QTime.currentTime()
        self.target_secs  = 60 - self.start_time.second()
        self.new_video_signal.emit(video_filename)

    def start(self):
        self.cap = cv2.VideoCapture(0) 
        self.is_running = True
        self.is_paused = False
        self.start_time = QTime.currentTime()

        while self.is_running:
            if not self.is_paused:
                ret, frame = self.cap.read()
                if ret:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, timestamp, (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)   
                    cv2.imshow("frame", frame)
                    cv2.waitKey(1)                    
                    
                elapsed_secs = self.start_time.secsTo(QTime.currentTime())
               
                # if video_writer is not being started yet
                if self.video_writer == None:
                    self.create_video()                    
                
                # if the video_writer is recording and should be ended 
                elif elapsed_secs >= self.target_secs:   
                    self.video_writer.release()
                    self.create_video()  
                # if the video_writer is recording and shouldn't be ended 
                else: 
                    self.video_writer.write(frame)
                
                time.sleep(0.033)  
            
        cv2.destroyWindow("frame")
        self.cap.release()    

        

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        self.recorder_thread = threading.Thread(target=self.run_recorder_thread)

    def run_recorder_thread(self):
        self.recorder = VideoRecorder()
        self.recorder.new_video_signal.connect(self.handle_new_video)
        self.recorder.start()

    def start_recording(self):
        if not self.recorder_thread.is_alive():
            self.recorder_thread = threading.Thread(target=self.run_recorder_thread)
        self.recorder_thread.start()


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
        print(f"New video recorder: {filename}")     


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 80)
    window.show()
    sys.exit(app.exec())   