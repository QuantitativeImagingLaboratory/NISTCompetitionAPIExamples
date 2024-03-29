import requests
import settings
import json
import cv2
import base64
import numpy as np
import datetime
import time
import Example_2


def view_crowd_count_analytic_results(camera, analytic_endpoint, reshape=None):
    camera_id = camera["id"]
    camera_fps = camera["fps"]

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    font_scale = 1
    color = (0, 0, 255)
    thickness = 2

    while True:
        response = requests.get("%s/main/camera/%s/analytic/%s/" % (settings.API_SERVER, camera_id, analytic_endpoint))
        try:
            data = response.json()
        except:
            print("Status:", response.status_code)
            continue

        image = base64.b64decode(data["image"])
        dip = np.asarray(bytearray(image), dtype="uint8")

        image = cv2.imdecode(dip, cv2.IMREAD_COLOR)

        if reshape is not None:
            image = cv2.resize(image, reshape)

        density = json.loads(data["results"])
        image = cv2.putText(image, 'Density %0.2f' % density, org, font,
                            font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow("data", image)
        key = cv2.waitKey(1)

        time.sleep(1)
        if key == 27:
            break

        print("Image with timestamp %s retrieved, press ESC to exit" % (datetime.datetime.fromtimestamp(float(data["timestamp"]))))
        print("There crowd density is %s." % density)
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
    test_camera = 9
    camera_details = retrieve_camera_details(test_camera)
    analytic_endpoint = get_analytic_endpoint("Crowd Counting")
    view_crowd_count_analytic_results(camera_details, analytic_endpoint, (640, 480))

