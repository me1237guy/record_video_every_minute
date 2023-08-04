# record_video_every_minute
To create a PySide6 application that spawns a separate thread to handle video recording using OpenCV. 
Below is an example implementation that provides functionalities to start, pause, resume, and stop video recording in 1-minute intervals. 
We'll use Python's built-in threading module to create and control the thread.

Before running this code, make sure you have installed the necessary libraries: PySide6, OpenCV, and NumPy. 
You can install them using pip:
pip install PySide6 opencv-python numpy

The code defines a VideoRecorder class that handles the video recording in a separate thread. 
The MainWindow class creates a simple GUI with buttons to start, pause, resume, and stop the video recording.
Remember that video recording depends on your webcam's resolution and capabilities, so you might need to adjust the settings accordingly. 
The example uses the XVID codec and 640x480 resolution, but you can modify these values as needed.
