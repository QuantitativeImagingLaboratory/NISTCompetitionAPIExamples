import requests
import settings
import json
import cv2
import base64
import numpy as np
import datetime
import time
import Example_2


def view_object_detection_analytic_results(camera, analytic_endpoint, reshape=None):
    camera_id = camera["id"]
    camera_fps = camera["fps"]

    while True:
        response = requests.get("%s/main/camera/%s/analytic/%s/" % (settings.API_SERVER, camera_id, analytic_endpoint))
        try:
            data = json.loads(response.json())
        except:
            print("Status:", response.status_code)
            continue

        image = base64.b64decode(data["image"])
        dip = np.asarray(bytearray(image), dtype="uint8")

        image = cv2.imdecode(dip, cv2.IMREAD_COLOR)

        if reshape is not None:
            image = cv2.resize(image, reshape)
        shape = image.shape

        detection = json.loads(data["results"])

        for k in detection:
            bb = k[2]
            tl = (int(bb[0][0] * shape[1]), int(bb[0][1] * shape[0]))
            br = (int(bb[1][0] * shape[1]), int(bb[1][1] * shape[0]))

            image = cv2.rectangle(image, tl, br, (255, 0, 0), 1)

        cv2.imshow("data", image)
        key = cv2.waitKey(1)

        time.sleep(1)
        if key == 27:
            break

        print("Image with timestamp %s retrieved, press ESC to exit" % (datetime.datetime.fromtimestamp(float(data["timestamp"]))))
        print("There are %s objects in the image." % len(detection))
        time.sleep(1/camera_fps)


def retrieve_camera_details(camera_id):
    print("Retrieving details for camera %s" % camera_id)
    response = requests.get("%s/main/camera/%s" % (settings.API_SERVER, camera_id))
    camera_data = response.json()
    print("Name: ", camera_data["name"])
    print("FPS: ", camera_data["fps"])
    return camera_data


def get_analytic_endpoint(analytic_name):
    analytic_list = Example_2.list_analytics()
    for each_analytic in analytic_list:
        if each_analytic["name"] == analytic_name:
            print("%s analytic is available at endpoint %s" % (analytic_name, each_analytic["endpoint"]))
            return each_analytic["endpoint"]

    raise Exception("Analytic with id %s does not exist" % analytic_name)


if __name__ == "__main__":
    test_camera = 7
    camera_details = retrieve_camera_details(test_camera)
    analytic_endpoint = get_analytic_endpoint("Object Detection")
    view_object_detection_analytic_results(camera_details, analytic_endpoint, (640, 480))

