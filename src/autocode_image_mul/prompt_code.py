



PROMPT_CODE = {}

PROMPT_CODE["object_direction_camera_complex"] = """
    示例一
    ###问题:From the current camera perspective, is the Bottle positioned at the front-left, front-right, back-left, or back-right of the curved armrest chair?
    ###code:
    ```python

    def func(metadata,camera_position):
        chair = None
        bottle = None
        for item in metadata:
            if item["id"] == "curved armrest chair":
                chair = item
            elif item["id"] == "Bottle":
                bottle = item
        
        if not chair or not bottle:
            return "Object not found"
        
        # Get centers (world coordinates)
        chair_center = chair["obb"]["center"]
        bottle_center = bottle["obb"]["center"]
        
        # Calculate relative position to camera (assuming camera_position is the origin for perspective)
        # Convert to camera-relative coordinates (camera is at camera_position)
        chair_rel = [
            chair_center[0] - camera_position[0],
            chair_center[2] - camera_position[2]  # Ignore Y-axis (height)
        ]
        bottle_rel = [
            bottle_center[0] - camera_position[0],
            bottle_center[2] - camera_position[2]  # Ignore Y-axis (height)
        ]
        
        # Determine front/back (Z-axis)
        front_back = "front" if bottle_rel[1] > chair_rel[1] else "back"
        
        # Determine left/right (X-axis)
        left_right = "left" if bottle_rel[0] < chair_rel[0] else "right"
        
        return f"{front_back}-{left_right}"
    ```
"""