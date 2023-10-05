# pedDet
## About
This real-time program uses OpenCV and YOLO Algorithm in python to detect and count pedestrians.
It detects static areas in a frame and masks them. YOLO algorithm is then used over these frames to detect pedestrians, improving the overall efficiency.



## Compatibility
Python - version 3.8 

## Dataset
A video for input in which pedestrians can be clearly differentiated by the human eye. 

## Instructions to Run
-pip install numpy
-pip install opencv-python

Enter the paths to the files of YOLO model in line 5
The path to the file containing class names in line 8
The path to the input video in line 11

## Result
Successfully return a video with rectangular boxes around the identified pedestrians and a counter on the top left of the frame

