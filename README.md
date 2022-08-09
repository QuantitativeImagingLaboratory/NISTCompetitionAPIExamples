### Environement
The code has been tested using the following environment
 - Ubuntu 20.04.3 LTS
 - Python 3.8.10
 - virtualenv 20.4.2

---
### Installation:
The required packages are listed in requirements.txt

If using virtual environment (create and activate it first):
- Create virtual environment
> virtualenv venv 
- Activate the environment
> source venv/bin/activate
- Install Requirements
> pip install -r requirements.txt
- Set API_URL parameter: open settings.py and set the url for the host
  - please contact email: to request the url 

---
### Running the Examples
- Example_1: List available cameras 
- Example_2: List available analytics 
- Example_3: View live camera data
- Example_4: View live results for object detection analytic
- Example_5: View live results for pedestrian density analytic
- Example_6: View live results for person attribute recognition
- Example_7: View live results for ingress/egress counter
- Example_8: View live results for object (car) counter

Any example can be run using the code:
> python Example_*.py

replace '*' with [1, 2, .. , 8]

---
### Endpoints and JSON response Description
1. List cameras: Retrieve list of all cameras
+ Endpoint: **/main/camera/**
+ Parameters: N/A
+ Response: Returns of list of dictionaries, where each dictionary represents a camera. The following attributes are provided for each camera 
```
"id": camera_id used to retrive each camera details
"name": name of the camera
"link": link to the camera 
"fps": Camera frame rate
"services": List of analytic services available on this camera,
"config": configuration of analytics running in the camera
```

2. Retrieve single camera: Retrieve single camera cameras
+ Endpoint: **/main/camera/{id}**
+ Parameters: 
  + id - The id of the camera to retrieve 
+ Response: Returns a dictionaries representing a camera. The following attributes are provided 
```
"id": camera_id used to retrive each camera details
"name": name of the camera
"link": link to the camera 
"fps": Camera frame rate
"services": List of analytic services available on this camera,
"config": Configuration of analytics running in the camera
```

3. List analytics: Retrieve list of available analytics
+ Endpoint: **/main/list_analytic/**
+ Parameters: N/A   
+ Response: Returns a list of dictionaries representing an analytics. The following attributes are provided for each analytic 
```
"id": Id of the analytic
"name": Name of the analytic
"endpoint": The endpoint to use to reterive results for the camera
"fps": The frame rate at which the analytic results are provided
```

4. Get Live Video: Retrieve live image for each camera
+ Endpoint: **/main/camera/{id}/get_live_data/**
+ Parameters:
  + id - The id of the camera to retrieve 
+ Response: Returns a dictionary. The following attributes are provided for each analytic 
```
"image": Base64 encoded jpeg image of the camera
"timestamp": The timestamp assocated with the image
```

5. Get live analytics results: Retrieve live image and analytic results assocaited with the image
+ Endpoint: **/main/camera/{id}/analytic/{analytic_name}/**
+ Parameters:
  + id - The id of the camera to retrieve 
  + analytic_name - The endpoint of the analytic 
+ Response: Returns a dictionary. The following attributes are provided for each analytic 
```
"image": Base64 encoded jpeg image of the camera
"timestamp": The timestamp assocated with the image
"results": The analytic results assocaited with the image
```

The results are different for each analytic, and are described below

---
### Description of analytic results
The following analytics are available are the results for each analytics are described below

1. Object Detection: Identifies and localizes objects in scene
   + Results: List of list representing objects.
   + Format: [class, confidence_scores, coordinates]
     + class: The class of the object (0- person, 1- car/vehicle).
     + confidence_score: A value between [0, 1], represents the confidence of the detection. Higher value implies higher confidence.
     + coordinates: The location of the object in the image, represented as bounding box with two image coordinates
       + [[tl.x, tl.y], [br.x, br.y]]: 
         + tl.x: X co-ordinate of the top left corner
         + tl.y: Y co-ordinate of the top left corner
         + br.x: X co-ordinate of the bottom right corner
         + br.y: Y co-ordinate of the bottom right corner
2. Pedestrian Density: Returns an estimate of the count of pedestrians in crowded scenes
   + Results: One value representing the density of pedestrians 
   + Format: <density> (as string)
3. Person Attribute Recognition: Identifies attributes for each pedestrian detected in the image
   + Results: List of dictionaries representing attributes of each person. The folllowing attributes are provided
   + Format: [{person_1_attribute_1: value, person_1_attribute_2, value,...}, 
   {person_2_attribute_1: value, person_2_attribute_2, value,...}], the following attributes are provided 
   ```
   + "age": adult/teenager/etc. 
   + "carrying backpack": yes/no 
   + "carrying bag": yes/no 
   + "carrying handbag": yes/no 
   + "type of lower-body clothing": pants/shorts/etc. 
   + "length of lower-body clothing": long lower body clothing/short lower body clothing/etc. 
   + "sleeve length": short sleeve/long sleeve/etc. 
   + "hair length": long hair/short hain/long hair/etc. 
   + "wearing hat": yes/no 
   + "gender": male/female 
   + "color of upper-body clothing": black/grey/blue/etc. 
   + "color of lower-body clothing": black/grey/blue/etc., 
   + "bag_color": black/grey/blue/etc.,
   + "detection": similar to object detection results see above 
   ```

4. Ingress/Egress Counter: Provides count of people entering and exiting the hallway/building
   + Results: Dictionaries with two counts
   + Format: {ingress_count": count_i, "egress_count": count_e} 
     + count_i: Count of the number of people entered the building (as string) 
     + count_e: Count of the number of people exited the building (as string)
   
5. Object Counter: Provides count of specified object based on object detection results
   + Results: One value representing the count of the object 
   + Format: <count> (as string) 





