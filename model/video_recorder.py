import time
import cv2
from PySide6.QtCore import QObject, Signal, QTime
from model.cv_utility import mat_to_qpixmap

class VideoRecorder(QObject):
    # a new video file created
    new_video_file_created = Signal(str)
    # a new frame grabbed
    new_frame_grabbed = Signal(cv2.Mat)

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
        self.new_video_file_created.emit(video_filename)

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
                    self.new_frame_grabbed.emit(frame)                               
                    
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
        
        self.cap.release()    

        

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False