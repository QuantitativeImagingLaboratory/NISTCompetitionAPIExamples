import requests
import settings
import json
import cv2
import base64
import numpy as np
import datetime
import time
import Example_2


def short_name(attribute_name):
    primary_item_list = ["lower", "upper"]
    secondary_list = ["backpack", "bag", "handbag", "clothing", "sleeve", "hair", "hat"]
    tertiary_list = ["type", "color", "length"]

    name = ""
    for k in primary_item_list:
        if k in attribute_name:
            name += k + " "
    for k in secondary_list:
        if k in attribute_name:
            name += k + " "
    for k in tertiary_list:
        if k in attribute_name:
            name += k

    if name == "":
        return attribute_name
    else:
        return name


def get_attributes_as_image(data):
    attributes_image = np.zeros((150, 150, 3)) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = .25
    color = (0, 0, 255)
    thickness = 1
    origin = np.array([10, 0])
    row_displacement = np.array([0, 10])

    for each_attribute in data:
        origin = origin + row_displacement

        string_representation = "%s : %s" % (short_name(each_attribute), data[each_attribute])

        attributes_image = cv2.putText(attributes_image, string_representation, origin, font,
                            fontScale, color, thickness, cv2.LINE_AA)

    return attributes_image


def view_object_detection_analytic_results(camera, analytic_endpoint, reshape=None):
    camera_id = camera["id"]
    camera_fps = camera["fps"]
    max_items_to_display = 5

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

        counter = 0
        for k in detection:
            bb = k["detection"][2]
            del k["detection"]
            # bb = k[2]
            attribute_image = get_attributes_as_image(k)
            tl = (int(bb[0][0] * shape[1]), int(bb[0][1] * shape[0]))
            br = (int(bb[1][0] * shape[1]), int(bb[1][1] * shape[0]))

            attribute_location = (br[0], tl[1])

            al = attribute_location  # shorter name
            attribute_shape = attribute_image.shape
            ats = attribute_shape  # shorter name

            image = cv2.rectangle(image, tl, br, (255, 0, 0), 1)

            if al[0]+ats[0] < image.shape[1] and al[1]+ats[1] < image.shape[0]:
                roi_images = image[al[1]: al[1]+ats[1], al[0]: al[0]+ats[0], :]
                roi_images = np.uint8(0.25 * roi_images + 0.75 * attribute_image)
                image[al[1]: al[1] + ats[1], al[0]: al[0] + ats[0], :] = roi_images
            counter += 1
            if counter > max_items_to_display:
                break


        cv2.imshow("data", image)
        key = cv2.waitKey(1)


        if key == 27:
            break

        print("Image with timestamp %s retrieved, press ESC to exit" % (datetime.datetime.fromtimestamp(float(data["timestamp"]))))
        print("There are %s objects in the image. Showing results for first 5 pedestrians, waiting for 10 seconds" % len(detection))
        time.sleep(9)


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
    test_camera = 10
    camera_details = retrieve_camera_details(test_camera)
    analytic_endpoint = get_analytic_endpoint("Person Attribute Recognition")
    view_object_detection_analytic_results(camera_details, analytic_endpoint, (640*2, 480*2))

