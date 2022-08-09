import requests
import settings
import json
import cv2
import base64
import numpy as np
import datetime
import time


def view_camera(camera, reshape=None):
    camera_id = camera["id"]
    camera_fps = camera["fps"]

    while True:
        response = requests.get("%s/main/camera/%s/get_live_data/" % (settings.API_SERVER, camera_id))
        data = json.loads(response.json())

        image = base64.b64decode(data["image"])
        dip = np.asarray(bytearray(image), dtype="uint8")

        image = cv2.imdecode(dip, cv2.IMREAD_COLOR)
        if reshape is not None:
            image = cv2.resize(image, reshape)

        cv2.imshow("data", image)
        key = cv2.waitKey(1)

        if key == 27:
            break
        print("Image with timestamp %s retrieved, press ESC to exit" % (datetime.datetime.fromtimestamp(float(data["timestamp"]))))
        time.sleep(1/camera_fps)


def retrieve_camera_details(camera_id):
    print("Retrieving details for camera %s" % camera_id)
    response = requests.get("%s/main/camera/%s" % (settings.API_SERVER, camera_id))
    camera_data = response.json()
    print(camera_data)
    print("Name: ", camera_data["name"])
    print("FPS: ", camera_data["fps"])
    return camera_data


if __name__ == "__main__":
    test_camera = 10
    camera_details = retrieve_camera_details(test_camera)

    view_camera(camera_details, reshape=(640, 480))
