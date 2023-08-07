from view.view import View
from model.video_recorder import VideoRecorder
from model.cv_utility import mat_to_qpixmap
from PySide6.QtCore import QDir, QCoreApplication, QFile, QIODevice, QFileInfo, Qt, Slot, QObject
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication
from PySide6.QtGui import QImage, QPixmap, QColor
import threading
import cv2

class Controller:
    def __init__(self):
        self.view = View()
        self.view.ui.pushButton_start.clicked.connect(self.start_recording)
        self.view.ui.pushButton_pause.clicked.connect(self.pause_recording)
        self.view.ui.pushButton_resume.clicked.connect(self.resume_recording)
        self.view.ui.pushButton_stop.clicked.connect(self.stop_recording)
        
        self.recorder_thread = threading.Thread(target=self.run_recorder_thread)

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
            self.recorder.new_frame_grabbed.disconnect(self.on_new_frame_grabbed)
            self.recorder.new_video_file_created.disconnect(self.on_new_video_file_created)
            self.recorder.stop()
   
    def run_recorder_thread(self):
        self.recorder = VideoRecorder()
        self.recorder.new_frame_grabbed.connect(self.on_new_frame_grabbed)
        self.recorder.new_video_file_created.connect(self.on_new_video_file_created)
        self.recorder.start()        

    @Slot(cv2.Mat)
    def on_new_frame_grabbed(self, frame):
        
        # print(f"on_new_frame_grabbed")
        q_pixmap = mat_to_qpixmap(frame)
        self.view.ui.label_display_image.setPixmap(q_pixmap)

    @Slot(str)
    def on_new_video_file_created(self, filename):
        # print(f"New video recorder: {filename}")  
        self.view.ui.listWidget.addItem(filename)



        
        
        
        




