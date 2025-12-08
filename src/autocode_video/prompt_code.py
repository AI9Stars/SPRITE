PROMPT_CODE = {}

PROMPT_CODE["object_in_frame"] = """
    示例一
    ###问题:List all objects that appear in the frame at the same time as the door.
    ###code:
    ```python

    def func(metadata):

        #  'door' object is present in metadata, find its appearance list
        door_appearances = None
        for obj in metadata:
            if obj['id'] == 'door':
                door_appearances = obj['appear']
                break

        if door_appearances is None:
            return "No door found in the metadata."

        # Find all objects that appear in the same frames as the door
        objects_in_same_frames = set()
        for obj in metadata:
            if obj['id'] != 'door':
                for frame in obj['appear']:
                    if frame in door_appearances:
                        objects_in_same_frames.add(obj['id'])
                        break
        return f"Objects appearing in the same frames as the door: {sorted(objects_in_same_frames)}"
    ```
"""

PROMPT_CODE["temporal_appearance_sequence"] = """

    示例一
    ###问题: Does the window appear before or after the stairs in the temporal sequence?
    ###code:
    ```python 
    def func(metadata):
        # We need to examine the temporal sequence based on the 'appear' attribute of each object.
    
        window_appear = None
        stairs_appear = None

        # Iterate over each item in the metadata list
        for item in metadata:
            id = item['id']
            appear = item['appear']
            
            # Locate the 'window' and 'stairs' based on their id
            if id == 'window':
                window_appear = appear
            elif id == 'stairs':
                stairs_appear = appear

        # If both window and stairs appear in the dataset
        if window_appear is not None and stairs_appear is not None:
            # Determine the earliest appearance of each object
            first_window_appearance = min(window_appear)
            first_stairs_appearance = min(stairs_appear)

            # Compare appearances to determine which appears first
            if first_window_appearance < first_stairs_appearance:
                return "The window appears before the stairs in the temporal sequence."
            elif first_window_appearance > first_stairs_appearance:
                return "The window appears after the stairs in the temporal sequence."
            else:
                return "The window and stairs appear simultaneously in the temporal sequence."
        else:
            return "Insufficient data to determine the temporal appearance sequence of window and stairs."

    ```
"""


PROMPT_CODE["object_appearance_order"] = """
    示例一:
    ###问题:What is the order of appearance of sofa, chair, and table in the video?
    ###code:
    ```python

    def func(metadata):
        # Initialize appearance orders
        furniture_appearance = {'sofa': None, 'chair': None, 'table': None}

        # Iterate over metadata to find items of interest
        for item in metadata:
            id = item.get('id', '')
            appear = item.get('appear', [float('inf')])

            if id in furniture_appearance and furniture_appearance[id] is None:
                furniture_appearance[id] = min(appear)

        # Sort the items by their first appearance
        sorted_furniture = sorted(furniture_appearance.items(), key=lambda x: x[1])

        # Create an ordered list of furniture categories
        order_of_appearance = [furn for furn, _ in sorted_furniture if _ is not None]

        return "The order of appearance is: " + ', '.join(order_of_appearance
    ```
"""


PROMPT_CODE["object_counting"] = """
    示例一
    ###问题:How many cushions are there in the video?
    ###code:
    ```python 
    def func(metadata):
        # Initialize a count for the cushions
        cushion_count = 0
        
        # Iterate over each item in the metadata list
        for obj in metadata:
            # Check the category of the object
            if obj['category'] == 'cushion':
                # Increment the cushion count
                cushion_count += 1        
        # Return the number of cushions found
        return str(cushion_count)
    ```

"""

PROMPT_CODE["object_height_determination"] = """
    示例一
    ###问题:Which object is the tallest among window, plant, and sofa?
    ###code:
    ```python
    def func(metadata):

        object_ids= ['window', 'plant', 'sofa']
        tallest_object = None
        max_height = -1

        for data in metadata:
            id = data.get('id')
            if id in object_ids:
                sizes = data['obb']['sizes']
                height = sizes[1]  # xyz 其中 y表示高度
                
                if height > max_height:
                    max_height = height
                    tallest_object = id

        return f"The tallest object among {', '.join(object_ids)} is {tallest_object} with a height of {max_height}."
    ```
"""


PROMPT_CODE["object_size_estimation"] = """
    示例一
    ###问题:"What is the length of the longest dimension (length, width, or height) of the table, measured in centimeters?
    ###code:
    ```python
    def func(metadata):

        # Initialize a list to hold appliance dimensions
        appliance_dimensions = []
        
        # Iterate over each item in the metadata
        for item in metadata:
            # Check if the item's id is 'table'
            if item['id'] == 'table':
                # Extract the sizes (length, width, height) from obb
                dimensions = item['obb']['sizes']
                # Append the dimensions to the appliance_dimensions list
                appliance_dimensions.append(dimensions)
        
        # Join the dimensions into a string and return the result
        res = max(appliance_dimensions)
        res = round(res,2)
        return "longest dimensions of table(length, width, height) is : " + str(res)
    ```
"""


PROMPT_CODE["object_volume_comparison"] = """
    示例一
    ###问题:Determines which object, cabinet or mirror, occupies the least volume.
    ###code:
    ```python
    import numpy as np
    def func(metadata):
        cabinet_volumes = []
        mirror_volumes = []
        for obj in metadata:
            if obj['id'] == 'cabinet':
                cabinet_volumes.append(obj['obb']['volume'])
            elif obj['id'] == 'mirror':
                mirror_volumes.append(obj['obb']['volume'])

        if cabinet_volumes and mirror_volumes:
            min_cabinet_volume = min(cabinet_volumes)
            min_mirror_volume = min(mirror_volumes)
            if min_cabinet_volume < min_mirror_volume:
                return "Cabinet occupies the least volume."
            elif min_mirror_volume < min_cabinet_volume:
                return "Mirror occupies the least volume."
            else:
                return "Cabinet and mirror occupy the same minimum volume."
        elif cabinet_volumes:
            return "Cabinet occupies the least volume (only cabinet found)."
        elif mirror_volumes:
            return "Mirror occupies the least volume (only mirror found)."
        else:
            return "Neither cabinet nor mirror found in the data."
    ```
"""


PROMPT_CODE["obj_spatial_relation"] = """
    示例一
    ###问题:Recognize spatial relation between door and chair such as proximity
    ###code:
    ```python
    
    def func(metadata):
    
        doors = [obj for obj in metadata if obj['id'] == 'door']
        chairs = [obj for obj in metadata if obj['id'] == 'chair']

        if not doors or not chairs:
            return "Error: No doors or chairs found in the metadata."

        #  Since there's no information about camera pose or orientation, we can only describe proximity based on center coordinates.
        #  A more sophisticated approach would involve considering camera pose and object orientations.

        min_distance = float('inf')
        closest_door = None
        closest_chair = None

        for door in doors:
            for chair in chairs:
                door_center = np.array(door['obb']['center'])
                chair_center = np.array(chair['obb']['center'])
                distance = np.linalg.norm(door_center - chair_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_door = door
                    closest_chair = chair

        if min_distance < 5:  # Adjust the threshold as needed.  This is an arbitrary threshold.
            return f"The closest door and chair are approximately {min_distance:.2f} units apart. They are in proximity."
        else:
            return f"The closest door and chair are approximately {min_distance:.2f} units apart. They are not in proximity."

    ```
"""



PROMPT_CODE["object_in_between"] = """
    示例一
    ###问题:Find out if the towel is located between the door and the toilet when viewed horizontally.
    ###code:
    ```python
    def func(metadata):

        towel_center = None
        door_center = None
        toilet_center = None

        # Extract the necessary centers of the towel, door, and toilet
        for item in metadata:
            id = item['id']
            center = item['obb']['center']

            if id == 'towel':
                towel_center = center
            elif id == 'door':
                door_center = center
            elif id == 'toilet':
                toilet_center = center

        if not (towel_center and door_center and toilet_center):
            return "Could not find all necessary objects."

        # Get x and z coordinates as we are interested in horizontal view
        towel_xz = (towel_center[0], towel_center[2])
        door_xz = (door_center[0], door_center[2])
        toilet_xz = (toilet_center[0], toilet_center[2])

        # Check if the towel is between door and toilet horizontally
        is_between = False
        if door_xz[0] < towel_xz[0] < toilet_xz[0] or toilet_xz[0] < towel_xz[0] < door_xz[0]:
            is_between = True

        return "Towel is between the door and the toilet horizontally." if is_between else "Towel is not between the door and the toilet horizontally."


    ```

"""

PROMPT_CODE["object_nearby"] = """
    示例一
    ###问题:From the sofa's position, what objects are in the 5 meter vicinity?
    ###code:
    ```python
        
    def func(metadata):

        import math

        # Helper function to calculate the Euclidean distance between two points in 3D.
        def distance(point1, point2):
            return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

        # Find object id is 'sofa'.
        sofas = [obj for obj in metadata if obj['id'] == 'sofa']
        sofa = sofas[0]
        # List to hold objects within 5 meters of any sofa.
        vicinity_objects = []

        # Iterate over all sofas to check each one's vicinity.
    
        sofa_center = sofa['obb']['center']
        
        # Check all other objects.
        for obj in metadata:
            if obj['id'] != 'sofa':  # Skip if the object is a sofa itself.
                distance_to_sofa = distance(sofa_center, obj['obb']['center'])
                if distance_to_sofa <= 5.0:
                    vicinity_objects.append(obj)

        # Extract the names (categories) of the objects within the vicinity.
        vicinity_names = {obj['id'] for obj in vicinity_objects}

        return f"Objects within 5 meters of the sofa are: {', '.join(vicinity_names)}"
    ```
"""


PROMPT_CODE["object_rel_distance"] = """
    示例一
    ###问题:Which object is closest to the window: the stool or the table?
    ###code:
    ```python

    def func(metadata):
        # Assuming stool, table and window presence in the metadata
        stool = None
        table = None
        window = None

        # Iterate through metadata to find the stool, table, and window objects
        for item in metadata:
            if item['id'] == 'stool':
                stool = item
            elif item['id'] == 'table':
                table = item
            elif item['id'] == 'window':
                window = item

        # If any object is missing in metadata, return empty
        if stool is None or table is None or window is None:
            return ""

        # Extracting center positions from OBB
        stool_center = stool['obb']['center']
        table_center = table['obb']['center']
        window_center = window['obb']['center']

        # Calculating Euclidean distance between window and stool
        dist_stool = ((window_center[0] - stool_center[0]) ** 2 + 
                    (window_center[1] - stool_center[1]) ** 2 + 
                    (window_center[2] - stool_center[2]) ** 2) ** 0.5

        # Calculating Euclidean distance between window and table
        dist_table = ((window_center[0] - table_center[0]) ** 2 + 
                    (window_center[1] - table_center[1]) ** 2 + 
                    (window_center[2] - table_center[2]) ** 2) ** 0.5

        # Determining closest object to the window
        if dist_stool < dist_table:
            return "The stool is closest to the window."
        else:
            return "The table is closest to the window."

        # In case no calculation can be performed, fallback message
        return "Could not determine the closest object."
    ```

"""


PROMPT_CODE["object_abs_distance"] = """
    示例一
    ###问题:Measure the absolute distance between the tv_monitor and the bed in meters.
    ###code:
    ```python

    def func(metadata):
        # Find the tv_monitor and bed in the metadata
        tv_monitor = None
        bed = None
        for item in metadata:
            if item['id'] == 'tv_monitor':
                tv_monitor = item
            elif item['id'] == 'bed':
                bed = item
        
        # Extract center coordinates
        tv_center = tv_monitor['obb']['center']
        bed_center = bed['obb']['center']
        
        # Calculate Euclidean distance
        distance = ((tv_center[0] - bed_center[0])**2 +
                    (tv_center[1] - bed_center[1])**2 +
                    (tv_center[2] - bed_center[2])**2)**0.5
        
        # Return rounded string with 2 decimal places
        return f"{round(distance, 2)} meters"

    ```

"""


PROMPT_CODE["object_direction_facing_complex"] = """
    示例一
    ###问题: If I am standing by the pillow and facing the lighting, is the cabinet to my position front-left, front-right, back-left, or back-right?
    ###code:
    ```python

    def func(metadata):
        # Extract objects from metadata
        cushion = next(item for item in metadata if item['id'] == 'cushion')
        lighting = next(item for item in metadata if item['id'] == 'lighting')
        cabinet = next(item for item in metadata if item['id'] == 'cabinet')
        
        # Get centers in xz-plane (y is vertical)
        c_center = cushion['obb']['center']
        l_center = lighting['obb']['center']
        cab_center = cabinet['obb']['center']
        
        # Calculate forward direction vector (cushion -> lighting)
        dx = l_center[0] - c_center[0]
        dz = l_center[2] - c_center[2]
        forward_mag = (dx**2 + dz**2)**0.5
        if forward_mag == 0:
            return 'unknown'
        forward_dir = (dx/forward_mag, dz/forward_mag)
        
        # Calculate right direction vector using cross product (up × forward)
        right_dir = (dz/forward_mag, -dx/forward_mag)
        
        # Calculate cabinet position relative to cushion
        cab_dx = cab_center[0] - c_center[0]
        cab_dz = cab_center[2] - c_center[2]
        
        # Calculate dot products for orientation
        dot_forward = cab_dx*forward_dir[0] + cab_dz*forward_dir[1]
        dot_right = cab_dx*right_dir[0] + cab_dz*right_dir[1]
        
        # Determine orientation
        if dot_forward > 0:
            return 'front-right' if dot_right > 0 else 'front-left'
        else:
            return 'back-right' if dot_right > 0 else 'back-left'

    ```
"""


PROMPT_CODE["object_volume_estimation"] = """
示例一
###问题:What is the volume of the bathtub in cubic meters?
###code:
```python
def func(metadata):
    volume = 0.0
    for item in metadata:
        if item.get('id') == 'bathtub':
            volume = item['obb']['volume']
            break
    return f"{volume:.3f} cubic meters"
```
"""


PROMPT_CODE["object_direction_facing_simple"] = """
    示例一
    ###问题: If I am standing by the pillow and facing the lighting, is the cabinet to my position left,right?
    ###code:
    ```python

    def func(metadata):
        # Extract objects from metadata
        cushion = next(item for item in metadata if item['id'] == 'cushion')
        lighting = next(item for item in metadata if item['id'] == 'lighting')
        cabinet = next(item for item in metadata if item['id'] == 'cabinet')
        
        # Get centers in xz-plane (y is vertical)
        c_center = cushion['obb']['center']
        l_center = lighting['obb']['center']
        cab_center = cabinet['obb']['center']
        
        # Calculate forward direction vector (cushion -> lighting)
        dx = l_center[0] - c_center[0]
        dz = l_center[2] - c_center[2]
        forward_mag = (dx**2 + dz**2)**0.5
        if forward_mag == 0:
            return 'unknown'
        
        # Calculate right direction vector using cross product (up × forward)
        right_dir = (dz/forward_mag, -dx/forward_mag)
        
        # Calculate cabinet position relative to cushion
        cab_dx = cab_center[0] - c_center[0]
        cab_dz = cab_center[2] - c_center[2]
        
        # Calculate dot products for orientation
       
        dot_right = cab_dx*right_dir[0] + cab_dz*right_dir[1]
        # Determine orientation
        if dot_right >0:
            return right
        else:
            return left

    ```
"""

PROMPT_CODE["object_below"] = """
    示例一
    ###问题: Determine whether the Vase is positioned at a lower elevation relative to the AlarmClock.
    ###code:
    ```python

    def func(metadata):
        # Extract objects from metadata
        Vase = next(item for item in metadata if item['id'] == 'Vase')
        AlarmClock = next(item for item in metadata if item['id'] == 'AlarmClock')
        vase_obb = Vase["obb"]
        alarm_clock_obb = AlarmClock["obb"]
        vase_y = vase_obb['center'][1]  # Assuming 'center' is a list/tuple in order (x, y, z)
        alarm_clock_y = alarm_clock_obb['center'][1]
        
        if vase_y < alarm_clock_y:
            return "Yes, the Vase is positioned at a lower elevation than the AlarmClock."
        elif vase_y > alarm_clock_y:
            return "No, the Vase is positioned at a higher elevation than the AlarmClock."
        else:
            return "No, the Vase and the AlarmClock are at the same elevation."

"""

PROMPT_CODE["object_above"] = """
    示例一
    ###问题: Is the Toilet located above the CounterTop?
    ###code:

    def func(metadata):
        # Extract objects from metadata
        Toilet = next(item for item in metadata if item['id'] == 'Toilet')
        CounterTop = next(item for item in metadata if item['id'] == 'CounterTop')

        toilet_obb = Toilet['obb']
        countertop_obb = CounterTop['obb']

        toilet_y = toilet_obb['center'][1]
        countertop_y = countertop_obb['center'][1]
        
        # Consider object heights (optional)
        toilet_height = toilet_obb['size'][1]
        countertop_height = countertop_obb['size'][1]
        
        # Compare bottom positions (center y - height/2)
        toilet_bottom = toilet_y - toilet_height/2
        countertop_top = countertop_y + countertop_height/2

        tolerance = 1e-6
        if toilet_bottom - countertop_top > tolerance:
            return "Yes, the Toilet is completely above the CounterTop."
        elif countertop_top - toilet_bottom > tolerance:
            return "No, the Toilet is below or at the same level as the CounterTop."
        else:
            return "The Toilet is exactly at the CounterTop's top level (within tolerance)"

"""


PROMPT_CODE["High_and_low_position"] = """
    示例一
    ###问题: Given two objects, AlarmClock and Vase, assess their relative vertical positions to identify which one is at a higher elevation.
    ###code:
    def func(metadata):
        # Extract objects from metadata
        vase = next(item for item in metadata if item['id'] == 'Vase')
        alarm_clock = next(item for item in metadata if item['id'] == 'AlarmClock')

        ac_obb = alarm_clock['obb']
        vase_obb = vase['obb']
        
        # Calculate vertical positions (center y and height)
        ac_center = ac_obb['center'][1]
        vase_center = vase_obb['center'][1]
        ac_height = ac_obb['size'][1]
        vase_height = vase_obb['size'][1]
        
        # Calculate bottom and top positions
        ac_bottom = ac_center - ac_height/2
        ac_top = ac_center + ac_height/2
        vase_bottom = vase_center - vase_height/2
        vase_top = vase_center + vase_height/2
        
        # Detailed comparison logic
        tolerance = 1e-6
        if abs(ac_center - vase_center) < tolerance:
            relation = "exactly at the same height"
        elif ac_center > vase_center:
            if ac_bottom > vase_top:
                relation = f"completely above (by {ac_bottom-vase_top:.3f} units)"
            else:
                relation = f"partially above (overlapping {vase_top-ac_bottom:.3f} units)"
        else:
            if vase_bottom > ac_top:
                relation = f"completely below (by {vase_bottom-ac_top:.3f} units)"
            else:
                relation = f"partially below (overlapping {ac_top-vase_bottom:.3f} units)"
        return f"The AlarmClock is {relation} relative to the Vase."
        
""" 