import cv2
import numpy as np
import serial
import time

# Serial communication setup
arduino_port = 'COM4'  # Change this to your Arduino's COM port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # wait for Arduino to initialize

# Define a window title
window_title = "Object Detection"
cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)

# YOLOv3 Tiny setup
config_path = 'yolov4-tiny.cfg'
weights_path = 'yolov4-tiny.weights'
classes_path = 'coco.names'

net = cv2.dnn.readNet(weights_path, config_path)
with open(classes_path, 'r') as f:
    classes = f.read().strip().split('\n')

# Generate color for each class randomly
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Define video capture for default cam
cap = cv2.VideoCapture(0)

def get_outputs_names(net):
    layers_names = net.getLayerNames()
    return [layers_names[i - 1] for i in net.getUnconnectedOutLayers()]

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

while True:
    has_frame, frame = cap.read()
    
    blob = cv2.dnn.blobFromImage(frame, 1.0 / 255.0, (416, 416), [0, 0, 0], True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_outputs_names(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold and class_id == 0:  # Class ID for person is 0
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = center_x - w // 2
                y = center_y - h // 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    persons_detected = 0
    for i in indices:
        i = i
        box = boxes[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        draw_prediction(frame, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
        persons_detected += 1
   
    label = f'Persons Detected: {persons_detected}'
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow(window_title, frame)
    
    # Send command to Arduino based on detection result
    if persons_detected > 0:
        command = '1'  # Turn on
    else:
        command = '0'  # Turn off
    ser.write(command.encode())
    
    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
