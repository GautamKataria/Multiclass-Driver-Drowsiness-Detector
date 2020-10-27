import time

import cv2
import numpy as np
from cv2 import dnn

DNN = "TF"
if DNN == "CAFFE":
    modelFile = ("res10_300x300_ssd_iter_140000.caffemodel")
    configFile = "deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
    modelFile = "opencv_face_detector_uint8.pb"
    configFile = "opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
cap=cv2.VideoCapture(0)

start = time.time()
for i in range(0, 120):
	ret, frame = cap.read()
end = time.time()
sec = start - end
fps = 120 / sec
print(abs(fps))

while True:

    ret,frame=cap.read()
    #frame=cv2.cvtColor(frame,cv2.COLOR_RGB2RGB)
    (frameHeight, frameWidth) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)), 1, (300,300), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False, crop=False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []

    conf_threshold = 0.5

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < 0.5:
            continue

        box = detections[0, 0, i, 3:7] * np.array([frameWidth, frameHeight, frameWidth, frameHeight])
        (x1, y1, x2, y2) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100)
        cord_x=x1+frameWidth
        cord_y=y1+frameHeight
        cv2.rectangle(frame, (x1, y1), (x2, y2),  (0, 0, 255), 2)
        cv2.putText(frame, text, (x1, y1),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    #cv2.imwrite(img_item, roi_gray)
    cv2.imshow("Video", frame)
    if cv2.waitKey((1)) %0XFF==ord('q'):
        breakq