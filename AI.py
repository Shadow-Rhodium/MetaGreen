from ultralytics import YOLO as YoV8
AI = "Desktop/best.pt"
model = YoV8(AI) #yolov8n

results = model(source=0, show=True, conf=0.6, save=False)