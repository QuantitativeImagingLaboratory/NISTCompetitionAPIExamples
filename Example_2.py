import requests
import settings


def list_analytics():
    """List Analytics"""
    url = "%s/main/list_analytic" % settings.API_SERVER
    response = requests.get(url)
    data = response.json()

    print("There are %s analytics" % (len(data)))

    for index, analytic in enumerate(data):
        print("%s. Analytic" % (index + 1))
        print("\t ID : %s" % analytic["id"])
        print("\t Name: %s" % analytic["name"])
        print("\t FPS: %s" % analytic["fps"])
        print("\t Endpoint: %s" % analytic["endpoint"])

    return data


if __name__ == "__main__":
    list_analytics()
