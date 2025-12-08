import json 
import numpy as np


def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def quaternion_multiply(q1, q2):
    """四元数乘法"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def quaternion_conjugate(q):
    """四元数共轭（逆）"""
    return np.array([q[0], -q[1], -q[2], -q[3]])

def quaternion_to_axis_angle(q):
    """四元数 -> 轴-角表示"""
   
    angle = 2 * np.arccos(q[0])  # 旋转角度（弧度）
    if np.sin(angle / 2) != 0:
        axis = q[1:] / np.sin(angle / 2)  # 旋转轴
    else:
        axis = np.array([1, 0, 0])  # 避免除以零（无旋转时默认X轴）
    return axis, angle

def get_turn_direction_and_angle(q1, q2):
    q_rel = quaternion_multiply(q2, quaternion_conjugate(q1))
    eps=1e-1
  
    if np.allclose(q_rel, [1, 0, 0, 0], atol=eps):
        return 0,0

    axis, angle_rad = quaternion_to_axis_angle(q_rel)
    angle_deg = np.degrees(angle_rad)


    if axis[1] > 0:  # Y 轴分量决定方向
        direction = "Left" if angle_deg > 0 else "Right"
    else:
        direction = "Right" if angle_deg > 0 else "Left"
    
    return direction, abs(angle_deg)  # 返回方向和绝对值角度

def get_turn(q1,q2):

    direction, angle = get_turn_direction_and_angle(q1, q2)

    return direction,angle

def get_turn_ai2thor(q1,q2):

    angle = q2[1] - q1[1]
    
    if angle > 0:
        direction = "Right"
    else:
        direction = "Left"
    angle = abs(angle)

    return direction,angle

def get_discribe(data_path):

    with open(data_path,"r",encoding = 'utf-8') as f:
        data = json.load(f)

    points = []

    for key,value in data.items():
        points.append(value)

    res = []
    index = 1 
    last = 0
    for i in range(1,len(points)):
        
        dis = distance([points[last]["position"][0],points[i]["position"][1]] ,  [points[i]["position"][0],points[i]["position"][1]] )


        turn,angle = get_turn(points[last]["rotation"], points[i]["rotation"])

        
        if angle <20 and dis < 0.1:
            continue
        if angle == 0 and dis < 0.6:
            continue
        if angle == 0:
            action = f"{index}: Do not rotate and move forward {dis:.2f} meters"
            last = i 
        else:
            action = f"{index}:Turn {angle:.2f}° to the {turn} and move forward {dis:.2f} meters"
            
        # action = f"{index}:Turn {angle:.2f}° to the {turn} and move forward {dis:.2f} meters"
        index+=1
        
        res.append(action)

    return "\n".join(res)