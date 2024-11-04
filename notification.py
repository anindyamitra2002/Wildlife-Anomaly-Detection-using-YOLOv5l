from twilio.rest import Client

account_sid = 'AC0a7984a7e9eeab7e5eb04639fa730304'
auth_token = 'dbddfa547f7167c95208c3485e3d9836'
client = Client(account_sid, auth_token)

def alert(object, latitude, longitude):
    message = client.messages.create(
    body=f'''{object} Detected!
             at location {latitude}, {longitude}''',
    from_='+15179480427',
    to='+918240716218'
    )
    print("Alert sended!")

def sendAlert(result_list):
    alert_classes = ['Person', 'Vehicle', 'Fire']  # Replace 'Vehicle' and 'Fire' with the actual class names

# Initialize variables to store the last seen locations for each class
    last_seen_locations = {class_name: None for class_name in alert_classes}

    # Iterate through the frames and detections
    for frame in result_list:
        frame_number = frame['frame_number']
        detections = frame['detections']
        
        for detection in detections:
            class_name = detection['class_name']
            latitude = detection['latitude']
            longitude = detection['longitude']
            
            # Check if the class is in the alert_classes
            if class_name in alert_classes:
                # Update the last seen location for the class
                last_seen_locations[class_name] = (latitude, longitude)

    # Check if any alert was triggered for each class
    for class_name, location in last_seen_locations.items():
        if location:
            latitude, longitude = location
            # print(f"Alert: {class_name} detected at Latitude: {latitude}, Longitude: {longitude}")
            alert(class_name, latitude, longitude)