import requests
import settings


def list_cameras():
    """List Cameras"""
    url = "%s/main/camera" % settings.API_SERVER
    response = requests.get(url)

    data = response.json()

    print("There are %s cameras" % (len(data)))

    for index, camera in enumerate(data):
        print("%s. Camera" % (index+1))
        print("\t ID: %s" % camera["id"])
        print("\t Name: %s" % camera["name"])
        print("\t FPS: %s" % camera["fps"])
        print("\t Services: %s" % camera["services"])

    return data


if __name__ == "__main__":
    list_cameras()
    