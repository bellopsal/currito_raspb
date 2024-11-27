import torch
import cv2
import numpy as np
from pathlib import Path

from ultralytics import YOLO
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyA3TwfeFqaU_23GhnQ19V3_mrrz6K_WEK8")

class ObjectDetector:
    def __init__(self, model_path='yolov5s.pt'):
        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', trust_repo=True)


    def detect_objects_in_image(self, image_path, output_path="output.jpg"):
        # Load the image
        img = cv2.imread(image_path)

        # Perform detection
        results = self.model(img)

        # Draw bounding boxes and labels
        labeled_img = self._draw_results(img, results)

        # Save and return the labeled image
        cv2.imwrite(output_path, labeled_img)
        return labeled_img

    def detect_objects_in_video(self, video_path, output_path="output_video.avi"):
        # Load video
        cap = cv2.VideoCapture(video_path)
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform detection on frame
            results = self.model(frame)

            # Draw results on frame
            labeled_frame = self._draw_results(frame, results)
            out.write(labeled_frame)

        cap.release()
        out.release()

        return results

    def _draw_results(self, img, results):
        labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        for label, coord in zip(labels, coords):
            label = int(label)
            x1, y1, x2, y2, conf = coord
            if conf < 0.3:  # Confidence threshold
                continue

            # Scale coordinates
            h, w, _ = img.shape
            x1, y1, x2, y2 = int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h)

            # Draw box and label
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            label_text = f"{self.model.names[label]} {conf:.2f}"
            img = cv2.putText(img, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return img






def say_something(prediction):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Tell me two interesting facts about {prediction}")
    return response.text



