import torch
import cv2
import numpy as np
from pathlib import Path

from ultralytics import YOLO

import os
import sys
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from hablar import hablar, generate_text



class ObjectDetector:
    def __init__(self, model_path, confidence_threshold=0.5):
        """
        Initializes the ObjectDetector instance.

        :param model_path: Path to the YOLOv5 model.
        :param confidence_threshold: Minimum confidence score to consider a detection valid.
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = YOLO(self.model_path, verbose = False)
        self.already_predicted = []

    def detect_live(self, cap):
        """
        Detects objects in real-time from a video source and prints the class names of detections
        where the bounding box covers 80% or more of the frame.

        :param video_source: The video source (default is 0 for webcam).
        """
        prediction = ""
        
        new_pred = False
        
        if not cap.isOpened():
            print("Error: Unable to open video source.")
            return


        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame from video source.")
                break

            height, width, _ = frame.shape
            results = self.model.predict(frame)
  

            for result in results:
                for bbox, conf, cls_id in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                    if conf < self.confidence_threshold:
                        continue

                    x_min, y_min, x_max, y_max = bbox
                    box_width = x_max - x_min
                    box_height = y_max - y_min

                    area = width * height
                    area_box = box_width * box_height

                    percentage = 100* area_box / area

#                     # # Draw the bounding box and label (optional)
#                     area = box_width * box_height
#                     label = f"{self.model.names[int(cls_id)]} ({percentage})"
#                     cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
#                     cv2.putText(frame, label, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                    if area_box >= 0.5 * area:
                        prediction = self.model.names[int(cls_id)]
                        if prediction in self.already_predicted: new_pred = False
                        else:
                            self.already_predicted.append(prediction)
                            new_pred = True
                        

            if new_pred:
                print("Detections covering 50% or more of the frame:", prediction)
                hablar(generate_text(prediction))
                time.sleep(5)
                break
                
                

            # Display the frame (optional)
            #cv2.imshow('Live Detection', frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break






if __name__ == "__main__":
    
    detector = ObjectDetector('yolov5su.pt')
    cap = cv2.VideoCapture(0)
    while True:
        prediction = detector.detect_live(cap)









