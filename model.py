import torch
import cv2
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
# Load the YOLOv8 model
day_model = torch.hub.load('yolov5', 'custom', r'weights/day-final.pt', source='local', force_reload=True, trust_repo=True,device="cpu")
thermal_model = torch.hub.load('yolov5',"custom", path=r'weights/night-final-aug.pt', source='local', force_reload=True,device='cpu')

day_class_to_animal = {
    0: 'Person',
	1: 'Elephant',
	2: 'Zebra',
	3: 'Giraffe',
	4: 'Deer',
	5: 'Bison',
	6: 'Rhino',
	7: 'Boar',
	8: 'Leopard',
	9: 'Vehicle',
   10: 'Fire'
}
thermal_class_to_animal = {
	0: "Person",
	1: "Elephant",
	2: "Deer",
	3: "Rhino",
	4: "Boar",
	5: "Leopard",
	6: "Vehicle",
	7: "Fire"
}


def plotBbox(results, frame, class_dict):
    for box in results.xyxy[0]:
        xA, yA, xB, yB, confidence, class_id = box
        class_id = int(class_id)
        class_name = class_dict.get(int(class_id), 'Unknown')
        # Define a unique color for each class
        color = get_color(class_id)
        xA = int(xA)
        xB = int(xB)
        yA = int(yA)
        yB = int(yB)
        # Draw the bounding box with the class-specific color
        cv2.rectangle(frame, (xA, yA), (xB, yB), color, 2)

        # Add text label with class name and confidence
        label = f"{class_name}: {confidence:.2f}"
        y = yA - 15 if yA - 15 > 15 else yA + 15
        cv2.putText(frame, label, (xA, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return frame

def get_color(class_id):
    # Define a list of colors for different classes
    colors = [
        (255,99,71),  
        (124,252,0),  
        (255,215,0),  
        (255, 255, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255,218,185),
        (138,43,226), 
        (255,20,147), 
        (176,196,222),  
        (0,250,154)
    ]

    return colors[class_id]


def predictVideo(temp_video_path, video_class):
    cap = cv2.VideoCapture(f'static/{temp_video_path}')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(fps)
    output_path = '/out/output_video.webm'
    out = cv2.VideoWriter(f'static/{output_path}', cv2.VideoWriter_fourcc(*"vp80"), fps, (width, height))
    result = []
    print('prediction start')
    if video_class == 'Daylight':
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                frame = cv2.resize(frame, (width, height))
                results = day_model(frame)
                print('Status: OK')

                # Check if there are any detections in this frame
                
                # Run YOLOv8 inference on the frame
                

            # Visualize the results on the frame
                # print(results.pandas().xyxy[0])
                annotated_frame = plotBbox(results=results, frame=frame, class_dict=day_class_to_animal)
                # Get bounding box coordinates and labels
                out.write(annotated_frame)
                if len(results.xyxy[0]) == 0:
                    continue
                classes = results.pandas().xyxy[0]['class']
                confidences = results.pandas().xyxy[0]['confidence']
                print(classes,confidences)
                frame_detections = {"frame_number": len(result) + 1,
                                    "detections":[]}
                for class_id, confidence in zip(classes, confidences):
                    obj = {
                            "class_id": class_id,
                            "class_name": day_class_to_animal.get(int(class_id), 'Unknown'),
                            "confidence": confidence,
                        }
                    frame_detections['detections'].append(obj)
                result.append(frame_detections)
                # Display the annotated frame
                

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break
    else:
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                frame = cv2.resize(frame, (width, height))
                results = thermal_model(frame)
                print('OK')

                # Check if there are any detections in this frame
                
                # Run YOLOv8 inference on the frame
                

            # Visualize the results on the frame
                # print(results.pandas().xyxy[0])
                annotated_frame = plotBbox(results=results, frame=frame, class_dict=thermal_class_to_animal)
                # Get bounding box coordinates and labels
                out.write(annotated_frame)
                if len(results.xyxy[0]) == 0:
                    continue
                classes = results.pandas().xyxy[0]['class']
                confidences = results.pandas().xyxy[0]['confidence']
                print(classes,confidences)
                frame_detections = {"frame_number": len(result) + 1,
                                    "detections":[]}
                for class_id, confidence in zip(classes, confidences):
                    obj = {
                            "class_id": class_id,
                            "class_name": thermal_class_to_animal.get(int(class_id), 'Unknown'),
                            "confidence": confidence,
                        }
                    frame_detections['detections'].append(obj)
                result.append(frame_detections)
                # Display the annotated frame
                

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break

    cap.release()
    out.release()
    print(result)
    return result, output_path

