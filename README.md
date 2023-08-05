# record_video_every_minute
To create a PySide6 application that spawns a separate thread to handle video recording using OpenCV. 
Below is an example implementation that provides functionalities to start, pause, resume, and stop video recording in 1-minute intervals. 
We'll use Python's built-in threading module to create and control the thread.

Before running this code, make sure you have installed the necessary libraries: PySide6, OpenCV, and NumPy. 
You can install them using pip:
pip install PySide6 opencv-python numpy

1. ex1.py
The code defines a VideoRecorder class that handles the video recording in a separate thread. The MainWindow class creates a simple GUI with buttons to start, pause, resume, and stop the video recording.
Remember that video recording depends on your webcam's resolution and capabilities, so you might need to adjust the settings accordingly. 
The example uses the XVID codec and 640x480 resolution, but you can modify these values as needed.

2. ex2.py
The camera initialization takes too much time in ex1.py, so I created ex2.py that is able to use another way to handle the video recording per minute.

3. ex3.py 
This example demonstrates how to convert from the Mat to the qPixmap.
In the model folder, open cv_utilty.py and take a look at "mat_to_qpixmap" method.
First, check that how many channels does the input mat data have.
Second, copy the data from the Mat to the QImage.
Finally, convert QImage to QPixmap. If the Mat uses BGR order, convert it to RGB before converting to QPixmap.

In VideoRecorder class, a new_frame_grabbed signal was added in order to notify the GUI.
As the slot called on_new_frame_grabbed received the signal, it will show the frame
on the GUI immediately. 