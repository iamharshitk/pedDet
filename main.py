import numpy as np
import cv2 as cv

# Load YOLOv3 model
net = cv.dnn.readNet("YOLO WEIGHTS","YOLO")

# Load class names
with open("YOLO CLASS NAMES", 'r') as f:
    classes = f.read().strip().split('\n')
 
vid=cv.VideoCapture("INPUT VIDEO")
bg_object=cv.createBackgroundSubtractorMOG2(history=10)


kernel1=np.ones((4,4), np.uint8)
kernel2=None


while True:
    
    ret , frame=vid.read()
    if not ret:
        break

    fgmask=bg_object.apply(frame)
    
    _, fgmask=cv.threshold(fgmask, 20, 255, cv.THRESH_BINARY)
    
    fgmask=cv.erode(fgmask, kernel1, iterations=1)
   
    fgmask=cv.dilate(fgmask, kernel2, iterations=10)
    
    

    cont,_=cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    fgr=cv.bitwise_and(frame, frame, mask=fgmask)


    # Prepare the frame for object detection
    blob = cv.dnn.blobFromImage(fgr, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Get detections
    layer_names = net.getUnconnectedOutLayersNames()
    detections = net.forward(layer_names)
    counter=0

    # Process detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # If the detected object is a pedestrian and confidence is above a threshold
            if class_id == 0 and confidence > 0.9:
                counter+=1
                center_x = int(obj[0] * fgr.shape[1])
                center_y = int(obj[1] * fgr.shape[0])
                width = int(obj[2] * fgr.shape[1])
                height = int(obj[3] * fgr.shape[0])

                # Calculate coordinates for drawing the bounding box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                # Draw a bounding box and label
                cv.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
    cv.putText(frame, "No. of pedestrians: "+str(counter), (0,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
    cv.imshow("output", frame)



    if cv.waitKey(1) == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()
